#!/usr/bin/env python3
"""
Build and check a video's 04-shots/shotlist.json (format: ../SKILL.md).

    python3 shots.py build videos/<slug>   # ai-gen: fill prompts + references; always: write shotlist.csv
    python3 shots.py check videos/<slug>   # exit 0 clean, 1 problems listed, 2 can't run

Prompts are assembled here, not by a model, so every shot copies the bible's
canonical descriptions word for word and a character looks the same in every frame.
"""

import csv
import json
import sys
from pathlib import Path

SIZES = {
    "EWS": "Extreme wide shot", "WS": "Wide shot", "MS": "Medium shot", "MCU": "Medium close-up",
    "CU": "Close-up", "ECU": "Extreme close-up", "INSERT": "Insert shot",
}
NO_FACE = {"EWS", "WS", "INSERT"}  # sizes where a speaker's lips can't be read
COVERED = {"action", "dialogue", "vo"}  # element types every scene must show; sound rides along
CSV_COLS = ["shot_id", "scene_id", "order", "duration_sec", "shot_size", "angle", "camera_move", "lens",
            "purpose", "subject_action", "sfx", "needs_lipsync", "image_prompt", "motion_prompt", "references", "status"]


def load(video: Path):
    def read(rel):
        return json.loads((video / rel).read_text(encoding="utf-8"))
    return read("config.json"), read("03-script/screenplay.json"), read("02-adaptation/bible.json"), read("04-shots/shotlist.json")


def prompts(shot, bible):
    """(image_prompt, negative_prompt, motion_prompt, references) by the fixed formula:
    style, shot, characters, action, location, entity, lighting, composition, atmosphere."""
    style = bible.get("style_guide", {})
    chars = {c["id"]: c for c in bible.get("characters", [])}
    locs = {l["id"]: l for l in bible.get("locations", [])}
    stage = shot.get("entity_stage", "none")
    entity = bible.get("entity", {}).get("stages", {}).get(stage, {}) if stage != "none" else {}
    loc = locs.get(shot.get("location_id"), {})
    camera = ", ".join(p for p in (SIZES[shot["shot_size"]], shot.get("angle"), shot.get("lens")) if p)
    figure = ", ".join(p for p in (" and ".join(chars[c]["visual_en"] for c in shot.get("characters", [])),
                                   shot.get("subject_action")) if p)
    parts = [
        style.get("prefix_en"), camera, figure, loc.get("description_en"), entity.get("visual_en"),
        shot.get("lighting"), shot.get("composition"), shot.get("framing_note"), style.get("atmosphere_en"),
    ]
    image = " ".join(sentence(p) for p in parts if p)
    motion = " ".join(sentence(p) for p in (shot.get("camera_move"), shot.get("motion_note")) if p)
    refs = {"characters": [f"refs/char_{c}.png" for c in shot.get("characters", [])]}
    if loc:
        refs["location"] = f"refs/loc_{loc['id']}.png"
    if entity:
        refs["entity"] = f"refs/entity_{stage}.png"
    return image, style.get("negative_en", ""), motion, refs


def sentence(text):
    """
    >>> sentence("slow dolly in"), sentence("Done.")
    ('Slow dolly in.', 'Done.')
    """
    t = text.strip()
    t = t[0].upper() + t[1:]
    return t if t[-1] in ".!?" else t + "."


def build(video: Path):
    config, _, bible, sheet = load(video)
    if config.get("production_tool") == "ai-gen":
        for shot in sheet["shots"]:
            shot["image_prompt"], shot["negative_prompt"], shot["motion_prompt"], shot["references"] = prompts(shot, bible)
        (video / "04-shots/shotlist.json").write_text(json.dumps(sheet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    out = video / "04-shots/shotlist.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CSV_COLS, extrasaction="ignore")
        w.writeheader()
        for shot in sheet["shots"]:
            w.writerow({**shot, "references": json.dumps(shot.get("references", ""), ensure_ascii=False) if shot.get("references") else ""})
    return out


def check(config, play, bible, sheet):
    """List every problem; empty means clean."""
    errs = []
    chars = {c["id"] for c in bible.get("characters", [])}
    locs = {l["id"] for l in bible.get("locations", [])}
    stages = set(bible.get("entity", {}).get("stages", {})) | {"none"}
    max_clip = config.get("max_clip_sec", 10)
    ai = config.get("production_tool") == "ai-gen"
    scenes = {s["scene_id"]: s for s in play["scenes"]}
    shots = sheet.get("shots") or []
    if not shots:
        return ["shotlist: no shots"]

    ids = [s.get("shot_id") for s in shots]
    for dup in {i for i in ids if ids.count(i) > 1}:
        errs.append(f"shot {dup}: duplicate shot_id")
    for s in shots:
        at = f"shot {s.get('shot_id')}"
        scene = scenes.get(s.get("scene_id"))
        if scene is None:
            errs.append(f"{at}: scene {s.get('scene_id')} is not in the screenplay")
            continue
        if s.get("shot_size") not in SIZES:
            errs.append(f"{at}: shot_size must be one of {list(SIZES)}")
        if not 0 < (s.get("duration_sec") or 0) <= max_clip:
            errs.append(f"{at}: duration {s.get('duration_sec')} s is outside 0-{max_clip} s (max_clip_sec)")
        if len(s.get("characters", [])) > 2:
            errs.append(f"{at}: {len(s['characters'])} characters in frame, keep it to 2")
        for c in s.get("characters", []):
            if c not in chars:
                errs.append(f"{at}: character '{c}' is not in the bible")
        loc = (scene.get("heading") or {}).get("location_id")
        if s.get("location_id") and s["location_id"] not in locs:
            errs.append(f"{at}: location '{s['location_id']}' is not in the bible")
        elif loc and s.get("location_id") != loc:
            errs.append(f"{at}: location '{s.get('location_id')}' differs from its scene's '{loc}'")
        if s.get("entity_stage", "none") not in stages:
            errs.append(f"{at}: entity_stage '{s['entity_stage']}' is not 'none' or a stage in the bible")
        elements = scene["elements"]
        for i in s.get("script_elements", []):
            if not 0 <= i < len(elements):
                errs.append(f"{at}: script element {i} is not in scene {scene['scene_id']}")
            elif (elements[i]["type"] == "dialogue" and elements[i]["character"] in s.get("characters", [])
                  and s.get("shot_size") not in NO_FACE and not s.get("needs_lipsync")):
                errs.append(f"{at}: shows {elements[i]['character']} speaking, set needs_lipsync")
        if ai and not (s.get("image_prompt") and s.get("motion_prompt")):
            errs.append(f"{at}: production_tool is ai-gen but prompts are missing (run build)")

    for sid, scene in scenes.items():
        own = sorted((s for s in shots if s.get("scene_id") == sid), key=lambda s: s.get("order", 0))
        total = sum(s.get("duration_sec") or 0 for s in own)
        if abs(total - scene["est_duration_sec"]) > scene["est_duration_sec"] * 0.10:
            errs.append(f"scene {sid}: shots total {total} s, scene is {scene['est_duration_sec']} s (over 10% off)")
        shown = {i for s in own for i in s.get("script_elements", [])}
        for i, e in enumerate(scene["elements"]):
            if e["type"] in COVERED and i not in shown:
                errs.append(f"scene {sid}: element {i} ({e['type']}) has no shot")
        for a, b in zip(own, own[1:]):
            if (a.get("shot_size"), a.get("angle")) == (b.get("shot_size"), b.get("angle")):
                errs.append(f"scene {sid}: shots {a.get('shot_id')} and {b.get('shot_id')} repeat size and angle back to back")
    return errs


def main(argv):
    if len(argv) != 3 or argv[1] not in ("build", "check"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    video = Path(argv[2])
    try:
        if argv[1] == "build":
            print(f"wrote {build(video)}")
            return 0
        errs = check(*load(video))
    except (OSError, ValueError, KeyError) as e:
        print(f"can't run: {e!r}", file=sys.stderr)
        return 2
    for e in errs:
        print(e)
    print("clean" if not errs else f"{len(errs)} problem(s)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
