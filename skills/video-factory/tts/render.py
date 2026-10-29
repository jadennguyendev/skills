#!/usr/bin/env python3
"""
Render a voice plan into one voiceover: narration with Qwen3-TTS, climax lines with Chatterbox.

    "$(uv tool dir)/mlx-audio/bin/python" render.py videos/<slug>/voice.json [-o voice.wav]

Writes <out>.wav (24 kHz mono 16-bit) and <out>.segments.json (start/end per segment).
Each segment's clip is cached in <out>.cache/ by a hash of its settings, so after editing one
line only that line is generated again. Paths in the plan are relative to the plan file.
"""

import argparse
import hashlib
import json
import sys
import wave
from pathlib import Path

import numpy as np

NARRATOR_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit"
DESIGN_MODEL = "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-8bit"
CHARACTER_MODEL = "mlx-community/chatterbox-fp16"
SR = 24000
PAUSE = 0.35
EXAGGERATION = 0.8
CFG_WEIGHT = 0.3
# Read by VoiceDesign to make a character's reference clip (~10 s; Chatterbox clones from it).
DESIGN_LINE = (
    "I have been waiting in the dark for a very long time. Every night I listen to the house, "
    "and every night I hear you breathing. Come closer. Let me see your face."
)


def validate(plan: dict) -> list:
    """Return every problem in the plan, empty when it can be rendered.

    >>> validate({"narrator": {"voice": "Ryan"}, "segments": [{"text": "Hi."}]})
    []
    >>> validate({"narrator": {}, "segments": [{"speaker": "x", "text": ""}]})
    ['narrator.voice is missing', 'segment 1: text is empty', 'segment 1: unknown speaker x']
    """
    errors = []
    characters = plan.get("characters", {})
    if not plan.get("narrator", {}).get("voice"):
        errors.append("narrator.voice is missing")
    for name, c in characters.items():
        if not c.get("ref_audio"):
            errors.append(f"character {name}: ref_audio is missing")
    if not plan.get("segments"):
        errors.append("segments is empty")
    for i, seg in enumerate(plan.get("segments", []), 1):
        if not seg.get("text", "").strip():
            errors.append(f"segment {i}: text is empty")
        speaker = seg.get("speaker")
        if speaker is not None and speaker not in characters:
            errors.append(f"segment {i}: unknown speaker {speaker}")
        if not 0.25 <= seg.get("exaggeration", EXAGGERATION) <= 2.0:
            errors.append(f"segment {i}: exaggeration must be 0.25-2.0")
    return errors


def rms(audio: np.ndarray) -> float:
    return float(np.sqrt(np.mean(np.square(audio)))) if audio.size else 0.0


def assemble(plan: dict, clips: list) -> tuple:
    """Join clips with pauses; level character clips to the narrator's loudness.

    Returns (audio, timeline). Clips are float arrays at SR, one per segment.
    """
    segments = plan["segments"]
    narration = [c for s, c in zip(segments, clips) if "speaker" not in s]
    target = rms(np.concatenate(narration)) if narration else None
    parts, timeline, t = [], [], 0.0
    for seg, clip in zip(segments, clips):
        clip = np.asarray(clip, dtype=np.float32)
        if "speaker" in seg and target and rms(clip):
            clip = clip * (target / rms(clip))
        peak = float(np.max(np.abs(clip))) if clip.size else 0.0
        if peak > 0.99:
            clip = clip * (0.99 / peak)
        end = t + len(clip) / SR
        timeline.append({"start": round(t, 3), "end": round(end, 3),
                         "speaker": seg.get("speaker", "narrator"), "text": seg["text"]})
        pause = seg.get("pause_after", PAUSE)
        parts += [clip, np.zeros(round(pause * SR), dtype=np.float32)]
        t = end + pause
    audio = np.concatenate(parts[:-1]) if parts else np.zeros(0, dtype=np.float32)
    return audio, timeline


def read_wav(path: Path) -> np.ndarray:
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32767


def write_wav(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())


class Models:
    """Loads each model on first use, so a cached render loads none."""

    def __init__(self):
        self._loaded = {}

    def __getitem__(self, repo):
        if repo not in self._loaded:
            from mlx_audio.tts.utils import load_model
            model = load_model(repo)
            if model.sample_rate != SR:
                sys.exit(f"{repo} outputs {model.sample_rate} Hz, expected {SR}")
            self._loaded[repo] = model
        return self._loaded[repo]


def collect(results) -> np.ndarray:
    return np.concatenate([np.array(r.audio, dtype=np.float32) for r in results])


def generate(models: Models, plan: dict, seg: dict, base: Path) -> np.ndarray:
    speaker = seg.get("speaker")
    if speaker is None:
        n = plan["narrator"]
        return collect(models[NARRATOR_MODEL].generate_custom_voice(
            text=seg["text"], speaker=n["voice"], language="English", instruct=n.get("instruct")))
    return collect(models[CHARACTER_MODEL].generate(
        text=seg["text"], ref_audio=str(base / plan["characters"][speaker]["ref_audio"]),
        exaggeration=seg.get("exaggeration", EXAGGERATION),
        cfg_weight=seg.get("cfg_weight", CFG_WEIGHT), verbose=False))


def ensure_refs(models: Models, plan: dict, base: Path) -> None:
    for name, c in plan.get("characters", {}).items():
        ref = base / c["ref_audio"]
        if ref.exists():
            continue
        if not c.get("design"):
            sys.exit(f"character {name}: {ref} does not exist and has no design to create it")
        print(f"designing voice for {name} -> {ref}")
        write_wav(ref, collect(models[DESIGN_MODEL].generate_voice_design(
            text=DESIGN_LINE, instruct=c["design"], language="English")))


def cache_key(plan: dict, seg: dict, base: Path) -> str:
    speaker = seg.get("speaker")
    if speaker is None:
        voice = [NARRATOR_MODEL, plan["narrator"]]
    else:
        ref = base / plan["characters"][speaker]["ref_audio"]
        voice = [CHARACTER_MODEL, hashlib.sha1(ref.read_bytes()).hexdigest()]
    return hashlib.sha1(json.dumps([voice, seg], sort_keys=True).encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("plan", type=Path)
    ap.add_argument("-o", "--out", type=Path, help="output .wav (default: voice.wav next to the plan)")
    args = ap.parse_args()

    plan = json.loads(args.plan.read_text())
    if errors := validate(plan):
        sys.exit("invalid plan:\n  " + "\n  ".join(errors))
    base = args.plan.parent
    out = args.out or base / "voice.wav"
    cache = out.with_suffix(".cache")
    cache.mkdir(parents=True, exist_ok=True)

    models = Models()
    ensure_refs(models, plan, base)
    clips = []
    for i, seg in enumerate(plan["segments"], 1):
        path = cache / f"{cache_key(plan, seg, base)}.wav"
        if not path.exists():
            print(f"[{i}/{len(plan['segments'])}] {seg.get('speaker', 'narrator')}: {seg['text'][:60]}")
            write_wav(path, generate(models, plan, seg, base))
        clips.append(read_wav(path))

    audio, timeline = assemble(plan, clips)
    write_wav(out, audio)
    out.with_suffix(".segments.json").write_text(json.dumps(timeline, indent=1) + "\n")

    total = len(audio) / SR
    character = sum(s["end"] - s["start"] for s in timeline if s["speaker"] != "narrator")
    share = character / total if total else 0
    print(f"{out}: {total:.1f} s, Chatterbox {share:.0%} of it")
    if share > 0.2:
        print("warning: Chatterbox is over 20% - keep it for the climax lines only")


if __name__ == "__main__":
    main()
