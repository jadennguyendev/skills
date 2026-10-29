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

Each video lives in its own folder, `videos/<slug>/`, in the user's project. Stages hand off through files in that folder:

| Stage | Skill | Reads | Writes |
|-------|-------|-------|--------|
| Research | (planned) | topic | `research.md` |
| Script | `script-writer` | brief, preferences | `script.en.md`, `brief.md`, `script.vi.md` |
| QA gate | `script-qa` (fresh subagent) | `script.en.md` | `qa.md` - PASS / REVISE / FAIL + score |
| Voice | `tts` | `script.en.md` | `voice.json`, `voice.wav`, `voice.segments.json` |
| Render | `lemo-opuscar`, one run per chapter | `script.en.md`, `brief.md` | `chNN/<slug>-chNN.mp4`, `<slug>.mp4` |
| Vertical | `vertical-short` | `<slug>.mp4` | 9:16 Shorts |

`script-writer` picks the genre from the topic (explainer, history-documentary, true-crime, horror, fiction, comedy) and reads the core craft reference plus that genre's file; `script-qa` applies the same genre's QA overrides. `script-writer` writes to the `avoid-ai-writing` standard and fixes QA findings for at most 2 rounds. Nothing renders until `qa.md` says PASS or the user accepts it. English scripts only.

## Credits

`skills/video-factory/avoid-ai-writing/` is [avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) by Conor Bronsdon, MIT License (copy in that folder's `LICENSE`). Vendored unmodified from `plugins/avoid-ai-writing/skills/avoid-ai-writing/` at commit `9cd07215982eca9736e14caaa63241c0264856f3` (v3.38.0). `script-qa` runs its detector and applies its rulebook.

To update: download the upstream repo at a newer commit, replace the whole folder with that commit's `plugins/avoid-ai-writing/skills/avoid-ai-writing/` plus its `LICENSE`, update the sha above, then run `node --test skills/video-factory/script-qa/scripts/score.test.js`.
