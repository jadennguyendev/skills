---
name: tts
description: Turn a video script into the voiceover, locally on Apple Silicon - Qwen3-TTS reads the narration, Chatterbox voices the few climax lines (a terrified character, a demon losing its temper) with high emotion. Use when the user asks for a voiceover, narration, TTS or "read the script", wants character voices or a scarier/angrier delivery on a line, wants to re-record or fix one line, choose or change the narrator voice, fix a mispronounced word, or needs segment timings for subtitles.
---

# TTS

Two local models, both run by `mlx-audio` on the Mac GPU:

- **Qwen3-TTS** (`Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit`) reads the narration, 80-90% of the runtime. A preset speaker plus a style `instruct`.
- **Chatterbox** (`chatterbox-fp16`) speaks only the climax lines, with `exaggeration` 0.7-1.0. It clones each character from a reference clip, which **Qwen3 VoiceDesign** creates once from a text description.

`render.py` (beside this file) renders a voice plan into one WAV. Every clip is cached, so changing one line only regenerates that line.

## 1. Check the install

```bash
command -v mlx_audio.tts.generate || uv tool install mlx-audio --prerelease=allow
```

Run scripts with the tool's Python: `PY="$(uv tool dir)/mlx-audio/bin/python"`. Models download from Hugging Face on first use (~9 GB for the three TTS models, plus 2.3 GB for the optional ASR check).

## 2. Write the voice plan

`03-script/script.en.md` (rendered by narration-script) stays spoken words only, so who-says-what lives in `videos/<slug>/voice.json`:

```json
{
  "narrator": {"voice": "Ryan", "instruct": "Low, calm, slightly ominous storyteller, unhurried pace"},
  "characters": {
    "anna":  {"design": "Young woman in her twenties, breathy and trembling, terrified", "ref_audio": "voices/anna.wav"},
    "demon": {"design": "Deep, gravelly, inhuman male voice, slow and menacing, with a rasp", "ref_audio": "voices/demon.wav"}
  },
  "segments": [
    {"text": "On the third night, she woke to slow footsteps in the hallway. They stopped outside her door."},
    {"speaker": "anna", "text": "Who's there? Please, just leave me alone!", "exaggeration": 0.7},
    {"text": "For a long moment, nothing answered. Then the door handle began to turn."},
    {"speaker": "demon", "text": "You should never have come back to this house!", "exaggeration": 1.0, "pause_after": 0.8}
  ]
}
```

- One segment per 1-3 sentences. Paragraphs of `script.en.md` map to segments in order; never reword the script here.
- A segment without `speaker` is narration. Ordinary dialogue stays with the narrator.
- Give a line to Chatterbox only at a peak: fear, a scream, the monster's rage. Keep Chatterbox at 10-20% of the runtime; `render.py` warns above 20%.
- `exaggeration`: 0.7 for fear, 0.8 default, 1.0 for rage. Higher speeds speech up; `cfg_weight` (default 0.3) slows it back down - lower it toward 0.2 if a line rushes.
- `pause_after` (seconds, default 0.35) holds silence after a segment. Use 0.8-1.5 after a scare.
- Narrator voices for English: `Ryan`, `Aiden`. The `instruct` steers tone and pace.
- `ref_audio` paths are relative to the plan. A missing one is created from `design`; to use a real recording instead, drop a 10 s clean WAV at that path.

Series voices: on the first video, render a short sample with `Ryan` and with `Aiden` and let the user pick by ear. Then keep `voices/` and the `narrator` block the same for every later video (copy them from the first video's folder), and save the choice as `voice` in the project's `.video-factory.json`. Re-designing a character makes a different voice.

## 3. Render

```bash
"$PY" render.py videos/<slug>/voice.json
```

Writes, beside the plan: `voice.wav` (24 kHz mono 16-bit), `voice.segments.json` (start/end/speaker/text per segment, for subtitles and cutting to picture) and `voice.cache/`. Character lines are levelled to the narrator's loudness.

Done when the run prints the duration and Chatterbox share, and the duration is plausible (about 150 words per minute). Then listen to every Chatterbox line (`afplay`) - it can slur or add sounds at exaggeration 1.0. To fix a line, edit its `text`, `exaggeration` or `cfg_weight` and render again; to re-roll it unchanged, add `"take": 2` (3, 4...) to the segment - any change to a segment gives it a fresh take.

To check the words without listening, transcribe and compare with the script:

```bash
mlx_audio.stt.generate --model mlx-community/Qwen3-ASR-1.7B-8bit --audio voice.wav --output-path transcript --format txt
```

## Text that reads well

- Write numbers, symbols and abbreviations the way they are spoken ("nineteen eighty-four", "per cent", "for example").
- A word said wrong: respell it phonetically in `voice.json` only ("Nyarlathotep" -> "Nyar-lath-oh-tep"), never in `script.en.md`.
- Chatterbox output carries Resemble AI's inaudible Perth watermark.
