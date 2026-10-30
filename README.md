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
  video-factory/    # retired: points to movie-factory
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

## Video Factory (retired)

video-factory is retired in favour of the [movie-factory](https://github.com/jadennguyendev/movie-factory) Claude Code plugin. The group now holds only `skills/video-factory/video-factory/SKILL.md`, which tells anyone who installs it how to switch. The old skills live on in git history.
