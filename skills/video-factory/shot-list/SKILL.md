---
name: shot-list
description: Break a screenplay into a shot list - coverage per scene, shot size, angle, camera move, lens, lighting, composition, duration, lip-sync flags - and, for AI image/video tools, assemble consistent image and motion prompts from the bible. Use when the user wants a shot list, shooting script, coverage plan, storyboard prep, or image/video prompts for a screenplay or narration script. Writes videos/<slug>/04-shots/.
---

# Shot List

The screenplay says what happens; the shot list decides how the viewer sees it. Two passes per scene, then code: coverage (as the director), shot design (as the director of photography), prompt assembly and checks (`scripts/shots.py`).

Reads `03-script/screenplay.json`, `02-adaptation/bible.json` and `config.json` (formats: `../video-factory/references/formats.md`; without a `config.json`, set up through `../video-factory/SKILL.md` first). Read `references/camera.md`, and `references/genres/<genre>.md` when the primary genre has one. The gates are the routine in `../video-factory/SKILL.md`, "Gates".

## Workflow

### 1. Coverage

For each scene, split it into shots: purpose, the script elements each shot shows (0-based indexes into the scene's `elements`), duration.

- Shot count is about the scene's length over the average shot length: 6-10 s for slow, tense scenes; 2-4 s for climax and panic.
- No shot runs longer than `max_clip_sec`; a longer moment becomes consecutive shots.
- Durations add up to the scene's `est_duration_sec` (within 10%).
- Every `action`, `dialogue` and `vo` element is shown by at least one shot.
- A scene at a location seen for the first time opens on an establishing shot.
- One main action per shot, at most 2 characters in frame.
- Use the sequence patterns in `references/camera.md` and the genre file where they fit.

### 2. Shot design

For each shot choose, from the vocabulary in `references/camera.md` only: `shot_size`, `angle`, `camera_move`, `lens`, `composition`, `lighting`, plus `subject_action`, `motion_note`, `framing_note`, `entity_stage` and `sfx`. Rules:

- The 180-degree rule: within a scene the camera stays on one side of the line between two characters.
- Light has a source in the location (motivated).
- One simple, slow camera move per shot.
- `entity_stage` matches the bible's `stage_by_beat` for the scene's beat (`none` when the bible has no entity).
- `needs_lipsync: true` when the shot shows a speaker's face while they talk.

Write all shots to `04-shots/shotlist.json` as `{"shots": [...]}`, in English whatever the screenplay language (the design fields feed prompts):

```json
{
  "shot_id": "5C", "scene_id": 5, "order": 3, "location_id": "old_house", "characters": ["lan"],
  "entity_stage": "shadow", "script_elements": [3], "purpose": "first glimpse of the figure in the mirror",
  "duration_sec": 5, "shot_size": "MCU", "angle": "over-the-shoulder, eye level", "camera_move": "slow dolly in",
  "lens": "50mm, shallow depth of field", "composition": "frame within frame (the mirror), foreground obstruction",
  "lighting": "single candle from the left, low-key, half her face in deep shadow",
  "subject_action": "brushing her hair with an ivory comb, then stopping",
  "motion_note": "she keeps brushing slowly, then stops; the candle flickers; the figure stays completely still",
  "framing_note": "her blurred shoulder in the foreground, the mirror centered, a faint figure in it behind her",
  "has_dialogue": false, "needs_lipsync": false, "sfx": "a faint lullaby", "status": "pending"
}
```

### 3. Build and check

From the user's project, with this skill's folder as `<skill-dir>`:

```bash
python3 <skill-dir>/scripts/shots.py build videos/<slug>
python3 <skill-dir>/scripts/shots.py check videos/<slug>
```

`build` writes `shotlist.csv` (the production tracker: one row per shot, a `status` column the user updates). When `production_tool` is `ai-gen` it also fills each shot's `image_prompt`, `negative_prompt`, `motion_prompt` and `references` (`refs/char_<id>.png`, `refs/loc_<id>.png`, `refs/entity_<stage>.png`), copying the bible's `_en` descriptions word for word; never write or reword a prompt by hand, change the shot or the bible and rebuild. Fix everything `check` lists until it prints `clean`.

Then hand `shotlist.json`, `screenplay.json`, `bible.json` and `references/camera.md` to a fresh subagent with this brief, never reviewing your own shots in this context:

> You are the visual supervisor. Do not rewrite; report. Check the shot list for: two consecutive shots too alike; a 180-degree rule break; an entity stage that does not match its scene's beat; a shot too hard to generate or shoot (complex movement, physical contact, fast action); a term outside the vocabulary in `references/camera.md`. Write `04-shots/review.md`: a verdict line (PASS or REVISE, round N), then a table (shot, problem, fix). PASS means no findings.

Fix exactly its findings, rebuild, recheck, rerun: at most 2 fix rounds, then show the user `review.md` and let them decide. Hold a **gate** on the shot list.
