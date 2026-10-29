#!/usr/bin/env python3
"""
Check and render a video's screenplay.json (format: ../references/formats.md).

    python3 screenplay.py check  videos/<slug>   # exit 0 clean, 1 problems listed, 2 can't run
    python3 screenplay.py render videos/<slug>   # writes 03-script/screenplay.txt (+ script.<lang>.md for narration)
"""

import json
import sys
import textwrap
from pathlib import Path

TYPES = {"action", "sound", "dialogue", "vo"}
SCENE_WORD = {"en": "SCENE", "vi": "CẢNH"}
CHAPTER_WORD = {"en": "CHAPTER", "vi": "CHƯƠNG"}


def load(video: Path):
    """(config, screenplay, bible, beats); bible and beats are {} when missing."""
    def read(rel, required=True):
        p = video / rel
        if not p.exists():
            if required:
                raise FileNotFoundError(p)
            return {}
        return json.loads(p.read_text(encoding="utf-8"))
    return (read("config.json"), read("03-script/screenplay.json"),
            read("02-adaptation/bible.json", False), read("02-adaptation/beats.json", False))


def check(config, play, bible, beats):
    """List every problem; empty means clean."""
    errs = []
    film = config.get("branch", "film") == "film"
    chars = {c["id"] for c in bible.get("characters", [])}
    locs = {l["id"] for l in bible.get("locations", [])}
    targets = {b["name"]: b["tension_target"] for b in beats.get("beats", [])}

    if len(chars) > config.get("max_characters", 99):
        errs.append(f"bible: {len(chars)} characters, max_characters is {config['max_characters']}")
    if len(locs) > config.get("max_locations", 99):
        errs.append(f"bible: {len(locs)} locations, max_locations is {config['max_locations']}")

    scenes = play.get("scenes") or []
    if not scenes:
        return errs + ["screenplay: no scenes"]
    seen = set()
    for s in scenes:
        sid = s.get("scene_id")
        at = f"scene {sid}"
        if sid in seen:
            errs.append(f"{at}: duplicate scene_id")
        seen.add(sid)
        if not isinstance(s.get("est_duration_sec"), (int, float)) or s["est_duration_sec"] <= 0:
            errs.append(f"{at}: est_duration_sec must be a positive number")
        if not s.get("elements"):
            errs.append(f"{at}: no elements")
        if film:
            h = s.get("heading") or {}
            if not all(h.get(k) for k in ("int_ext", "location_id", "time")):
                errs.append(f"{at}: heading needs int_ext, location_id and time")
            elif h["location_id"] not in locs:
                errs.append(f"{at}: location '{h['location_id']}' is not in the bible")
            if targets and s.get("beat") not in targets:
                errs.append(f"{at}: beat '{s.get('beat')}' is not in beats.json")
            elif targets and abs(s.get("tension", 0) - targets[s["beat"]]) > 2:
                errs.append(f"{at}: tension {s.get('tension')} is more than 2 off its beat's target {targets[s['beat']]}")
            if len(s.get("characters", [])) > 3:
                errs.append(f"{at}: {len(s['characters'])} characters, keep a scene to 3")
        elif not s.get("title"):
            errs.append(f"{at}: narration chapters need a title")
        for c in s.get("characters", []):
            if c not in chars:
                errs.append(f"{at}: character '{c}' is not in the bible")
        for i, e in enumerate(s.get("elements", [])):
            if e.get("type") not in TYPES:
                errs.append(f"{at} element {i}: type must be one of {sorted(TYPES)}")
            if not str(e.get("text", "")).strip():
                errs.append(f"{at} element {i}: empty text")
            if e.get("type") == "dialogue" and not e.get("character"):
                errs.append(f"{at} element {i}: dialogue needs a character")
            if e.get("character") and e["character"] not in chars:
                errs.append(f"{at} element {i}: speaker '{e['character']}' is not in the bible")

    target = config.get("target_duration_min")
    if target:
        total = sum(s.get("est_duration_sec") or 0 for s in scenes)
        if abs(total - target * 60) > target * 60 * 0.15:
            errs.append(f"total {total:.0f} s is more than 15% off the {target} min target")
    return errs


def heading(scene, bible, lang, film):
    """
    >>> heading({"scene_id": 5, "heading": {"int_ext": "INT", "location_id": "h", "sublocation": "Lan's room", "time": "NIGHT"}},
    ...         {"locations": [{"id": "h", "name": "Old house"}]}, "en", True)
    "SCENE 5. INT. OLD HOUSE - LAN'S ROOM - NIGHT"
    >>> heading({"scene_id": 2, "title": "What money is"}, {}, "en", False)
    'CHAPTER 2 - WHAT MONEY IS'
    """
    if not film:
        return f"{CHAPTER_WORD.get(lang, 'CHAPTER')} {scene['scene_id']} - {scene['title']}".upper()
    h = scene["heading"]
    names = {l["id"]: l["name"] for l in bible.get("locations", [])}
    place = " - ".join(p for p in (names.get(h["location_id"], h["location_id"]), h.get("sublocation")) if p)
    return f"{SCENE_WORD.get(lang, 'SCENE')} {scene['scene_id']}. {h['int_ext']}. {place} - {h['time']}".upper()


def speaker(e, bible):
    names = {c["id"]: c["name"] for c in bible.get("characters", [])}
    name = names.get(e.get("character"), e.get("character") or "NARRATOR").upper()
    return f"{name} (V.O.)" if e["type"] == "vo" else name


def screenplay_txt(config, play, bible):
    """Industry layout: action flush left, speaker at 20 spaces, parenthetical at 10, lines at 5."""
    lang, film = config.get("language", "en"), config.get("branch", "film") == "film"
    out = [play.get("title", "").upper(), ""]
    for s in play["scenes"]:
        out += [heading(s, bible, lang, film), ""]
        for e in s["elements"]:
            if e["type"] in ("action", "sound"):
                out += textwrap.wrap(e["text"], 60) + [""]
                continue
            out.append(" " * 20 + speaker(e, bible))
            if e.get("emotion"):
                out.append(" " * 10 + f"({e['emotion']})")
            out += textwrap.wrap(e["text"], 35, initial_indent=" " * 5, subsequent_indent=" " * 5) + [""]
    return "\n".join(out).rstrip() + "\n"


def narration_md(play):
    """Spoken words only, one '## chNN - title (~N s, W words)' heading per chapter: the text script-qa scores."""
    out = [f"# {play.get('title', '')}", ""]
    for n, s in enumerate(play["scenes"], 1):
        paras = [e["text"].strip() for e in s["elements"] if e["type"] == "vo"]
        words = sum(len(p.split()) for p in paras)
        out += [f"## ch{n:02} - {s['title']} (~{s['est_duration_sec']:.0f} s, {words} words)", ""]
        out += [p + "\n" for p in paras]
    return "\n".join(out).rstrip() + "\n"


def render(video: Path):
    config, play, bible, _ = load(video)
    written = [video / "03-script/screenplay.txt"]
    written[0].write_text(screenplay_txt(config, play, bible), encoding="utf-8")
    if config.get("branch") == "narration":
        md = video / f"03-script/script.{config.get('language', 'en')}.md"
        md.write_text(narration_md(play), encoding="utf-8")
        written.append(md)
    return written


def main(argv):
    if len(argv) != 3 or argv[1] not in ("check", "render"):
        print(__doc__.strip(), file=sys.stderr)
        return 2
    video = Path(argv[2])
    try:
        if argv[1] == "render":
            for p in render(video):
                print(f"wrote {p}")
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
