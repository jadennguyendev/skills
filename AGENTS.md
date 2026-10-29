# AGENTS.md

Custom agent skills, installable via skills.sh (`npx skills add jadennguyendev/skills`).

## Layout

- One folder per skill: `skills/<group>/<skill-name>/SKILL.md`
- Existing groups: `video-factory`, `marketing`, `product`, `qa`
- `video-factory` covers video pre-production: the `video-factory` skill routes a video through story -> screenplay or narration -> shot list, ending at documents (rendering is the user's choice of tool). Shared scripts and formats live in `skills/video-factory/video-factory/`, so the group installs together. Video-specific QA lives here, not in `qa`
- `skills.sh.json` groups skills on the repo's skills.sh page
- `skills/video-factory/avoid-ai-writing/` is vendored from upstream (see README Credits). Never edit it by hand - resync the whole folder at a new upstream sha. The em dash rule does not apply inside it

## Adding a skill

1. Pick the group that fits. If none fits, recommend a new group folder name to the user first - do not create it silently or force the skill into a group it does not belong to.
2. `mkdir skills/<group>/<skill-name>`; write `SKILL.md` with frontmatter `name` (lowercase-hyphen, matches folder) and `description` listing concrete trigger cases - the description is what agents match on.
3. Supporting files (templates, scripts, checklists) live beside the `SKILL.md`.
4. Add the skill's `name` under its group in `skills.sh.json`. WIP skills get `metadata.internal: true`.

## Verify

`npx skills add . --list` - the new skill must appear.

## Style

Plain `-`, never an em dash. Prose stays lean - cut lines an agent already does by default.
