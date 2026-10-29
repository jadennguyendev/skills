# skills

Company agent skills, installable via [skills.sh](https://skills.sh) (`npx skills`).

## Install

```bash
# Interactive - pick skills and agents
npx skills add <org>/skills

# List available skills without installing
npx skills add <org>/skills --list

# Install everything
npx skills add <org>/skills --all

# Install one skill
npx skills add <org>/skills --skill <name>
```

Private repo: the CLI uses your existing git credentials, `gh` auth, or `GITHUB_TOKEN` - no extra setup needed.

## Layout

```
skills/
  video-factory/    # end-to-end video production
  marketing/        # marketing skills
  product/          # product skills
  qa/               # general content QA
    <skill-name>/
      SKILL.md
skills.sh.json      # controls grouping on the skills.sh repo page
```

One folder per skill: `skills/<team>/<skill-name>/SKILL.md`. Extra files the skill
needs (templates, checklists, scripts) live alongside its `SKILL.md`.

## Add a skill

```bash
mkdir -p skills/<team>/<skill-name>
# write skills/<team>/<skill-name>/SKILL.md
```

Minimum `SKILL.md` frontmatter:

```markdown
---
name: my-skill
description: What it does and when to use it - list concrete trigger phrases.
---
```

Then add the skill name to its group in `skills.sh.json` so it shows under the
right section on the skills.sh page. The `description` is what agents match on -
spend your words there, not in the title.

## Video Factory pipeline

Pre-production only: the pipeline turns an idea, a story or a topic into review-ready documents and stops there. Rendering is the user's choice (Opuscar, AI image/video tools, TTS). `video-factory` is the entry point: it sets up `videos/<slug>/config.json` (asking which production tool the user will render with), runs each stage, and rebuilds a local viewer, `videos/<slug>/index.html`, at every review gate.

| Stage | Skill | Reads | Writes |
|-------|-------|-------|--------|
| Setup | `video-factory` | `.video-factory.json`, the user's material | `config.json`, `00-source/source.md` |
| Story (film, optional) | `story-writer` | `00-source/` | `01-story/story-bible.md`, `story.md`, `review.md` |
| Adaptation (film) | `screen-adapter` | `01-story/` or `00-source/` | `02-adaptation/analysis.json`, `beats.json`, `bible.json`; `03-script/screenplay.json`, `screenplay.txt`, `review.md` |
| Narration | `narration-script` | `00-source/` | `02-adaptation/bible.json`; `03-script/screenplay.json`, `script.en.md`, `screenplay.txt` |
| QA gate (narration, English) | `script-qa` (fresh subagent) | `03-script/script.en.md` | `03-script/review.md` - PASS / REVISE / FAIL + score |
| Shot list | `shot-list` | `03-script/`, `02-adaptation/bible.json` | `04-shots/shotlist.json`, `shotlist.csv`, `review.md`; image/motion prompts only when `production_tool` is `ai-gen` |

`screenplay.json` is the one source for both branches; the text versions are rendered from it. Everything is English by default, with a Vietnamese review copy (`*.vi.md`, `screenplay.vi.txt`) beside each document the user reviews. Every writing stage hands its draft to a fresh reviewer subagent and fixes findings for at most 2 rounds.

Outside the pipeline: `tts` voices `script.en.md`, `vertical-short` cuts 9:16 Shorts from a finished film.

Tests: `python3 skills/video-factory/video-factory/scripts/screenplay_test.py`, `view_test.py`, `skills/video-factory/shot-list/scripts/shots_test.py`, `node --test skills/video-factory/script-qa/scripts/score.test.js`.

## Credits

`skills/video-factory/avoid-ai-writing/` is [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) by Conor Bronsdon, MIT License (copy in that folder's `LICENSE`). Vendored unmodified from `plugins/avoid-ai-writing/skills/avoid-ai-writing/` at commit `9cd07215982eca9736e14caaa63241c0264856f3` (v3.38.0). `script-qa` runs its detector and applies its rulebook.

To update: download the upstream repo at a newer commit, replace the whole folder with that commit's `plugins/avoid-ai-writing/skills/avoid-ai-writing/` plus its `LICENSE`, update the sha above, then run `node --test skills/video-factory/script-qa/scripts/score.test.js`.
