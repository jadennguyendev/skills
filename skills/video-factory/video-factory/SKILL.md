---
name: video-factory
description: Run the video pre-production pipeline end to end, from an idea, a story or a topic to review-ready documents (novel, bible, screenplay, narration, shot list) in videos/<slug>/. Use when the user wants to start a new video, film or YouTube video project, continue or check the status of an existing one in videos/, turn a story into a film, set up channel defaults, or view a video's documents. Stops at documents; rendering (Opuscar, AI image/video tools, TTS) is the user's next step.
---

# Video Factory

The pipeline's entry point: set up a video, route each stage to its skill, hold the gates. Every stage skill sits next to this one (`../<skill>/SKILL.md`) and needs this one for `scripts/` and `references/formats.md` - the group installs together. Run everything from the user's project; call `scripts/...` by this skill's path.

## Branches

| Branch | For | Stages |
|--------|-----|--------|
| `film` | a story told in scenes, with characters and dialogue | `story-writer` (only when the user has no finished story) -> `screen-adapter` -> `shot-list` |
| `narration` | a voice-over video: explainer, documentary, true crime, a narrated story | `narration-script` (runs `script-qa` for English) -> `shot-list` |

## Folder layout

```
<project>/
  .video-factory.json          # project defaults, same keys as config.json
  videos/<slug>/
    config.json                # this video's settings (references/formats.md)
    index.html                 # the viewer, rebuilt at every gate
    00-source/source.md        # what the user gave, verbatim
    01-story/                  # story-writer: story-bible.md, story.md, review.md
    02-adaptation/             # screen-adapter: analysis.json, beats.json, bible.json (narration: bible.json only)
    03-script/                 # screenplay.json, screenplay.txt, script.<lang>.md (narration), review.md
    04-shots/                  # shot-list: shotlist.json, shotlist.csv, review.md
    refs/                      # reference images the user adds, named as shotlist.json says (ai-gen)
```

Each stage writes only its own folder and reads the earlier ones. To redo from a stage, delete that folder and every later one.

## Workflow

### 1. Find or set up the video

An existing `videos/<slug>/` means resume: go to step 2. Otherwise set up:

1. Read `.video-factory.json` at the git root (or the cwd). Missing: ask once for the project defaults (audience, tone, platform, aspect ratio, visual style) and write it, with `language: "en"`, `review_language: "vi"`, `production_tool: "none"`, `max_characters: 4`, `max_locations: 3`, `max_clip_sec: 8` unless the user says otherwise.
2. Ask in one round, skipping what the user already said: what the video is (to pick the branch and genre; propose both), title, target length, and which **production tool** they will render with: `none` (undecided or manual storyboard), `opuscar`, or `ai-gen` (AI image and video tools; adds prompts to the shot list). Default `none`.
3. Write `videos/<slug>/config.json` (defaults merged with the answers; keys in `references/formats.md`) and save what the user gave, verbatim, to `00-source/source.md`.

### 2. Run the next stage

The first stage of the branch whose folder is missing or incomplete is next. Read its `SKILL.md` and run it; it stops at its own gates. After a stage's last gate passes, go on to the next stage without asking. The video is done when `shot-list` passes its gate: tell the user which files to hand to their production tool (`opuscar`: `03-script/` and `02-adaptation/bible.json`; `ai-gen`: `04-shots/` and the images to put in `refs/`).

## Gates

A gate is a stop for the user's review. Every stage skill names its gates; at each one:

1. **Review copies** - when `review_language` is set (`vi` below), write the review copy of each file this gate shows the user, in the same folder: `story.vi.md`, `story-bible.vi.md`, `screenplay.vi.txt`, `script.vi.md` (of `script.<lang>.md`), and for `02-adaptation/` one `adaptation.vi.md` that renders the decisions, logline, synopsis, beats and bible as prose. A faithful sentence-by-sentence translation: names, numbers and ids unchanged, nothing polished or adapted. Rewrite it whenever the original changes. JSON, CSV, prompts and `review.md` stay untranslated.
2. **Viewer** - `python3 scripts/view.py videos/<slug>` and give the user the printed `file://` link.
3. **Ask** - say what to check, in one or two lines, and wait. A change request means: apply it, rerun the stage's checks, and hold the same gate again.
