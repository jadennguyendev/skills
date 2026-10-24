# AGENTS.md

Custom agent skills, installable via skills.sh (`npx skills add jadennguyendev/skills`).

## Layout

- One folder per skill: `skills/<group>/<skill-name>/SKILL.md`
- Existing groups: `content`, `marketing`, `product`, `qa`
- `skills.sh.json` groups skills on the repo's skills.sh page

## Adding a skill

1. Pick the group that fits. If none fits, recommend a new group folder name to the user first - do not create it silently or force the skill into a group it does not belong to.
2. `mkdir skills/<group>/<skill-name>`; write `SKILL.md` with frontmatter `name` (lowercase-hyphen, matches folder) and `description` listing concrete trigger cases - the description is what agents match on.
3. Supporting files (templates, scripts, checklists) live beside the `SKILL.md`.
4. Add the skill's `name` under its group in `skills.sh.json`. WIP skills get `metadata.internal: true`.

## Verify

`npx skills add . --list` - the new skill must appear.

## Style

Plain `-`, never an em dash. Prose stays lean - cut lines an agent already does by default.
