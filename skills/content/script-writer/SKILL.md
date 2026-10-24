---
name: script-writer
description: Write production-ready YouTube video scripts in the user's saved style, optionally split into chapters that are each rendered as a Lemo-Opuscar film and joined into one video. Use when the user asks for a YouTube script, video script, hook or intro for a video, a script outline, a Shorts script, chapters for a long video, a brief for Opuscar, or wants to rewrite, trim, or change the tone of an existing script. On first use collects preferences (tone, length, audience, hook style, language, production) and keeps them plus past scripts per project for consistent voice.
---

# Script Writer

Run the DB commands from inside the user's project - data is stored per project, in `.script-writer.json` at the git root (or the cwd if there is no git repo). `scripts/...` means the scripts in this skill's folder; call them by that path, don't `cd` into the skill. Structures, chapter rules, the output files and tone examples live in `references/script_formats.md` - read it before writing.

## Workflow

### 1. Load preferences

```bash
python3 scripts/script_db.py is_initialized
python3 scripts/script_db.py get_preferences
```

`false` - go to step 2. `true` - go to step 3.

### 2. Collect preferences (first use only)

Ask in one round, skipping what the user already said:

- **Tone**: professional, casual-friendly, energetic, educational-patient, inspirational, humorous, conversational
- **Default length**: short (3-5 min), medium (7-12 min), long (15-30 min)
- **Audience**: age range, knowledge level
- **Hook style**: question, bold statement, conflict, promise, shock, story opening
- **Language**: script language, plus a review translation if the user wants one (e.g. English script + Vietnamese for review)
- **Production**: `opuscar-chapters` (each chapter rendered as a Lemo-Opuscar film, then joined) or `none`

Pick sensible defaults for the rest (personality, humor, CTA style, storytelling weight) from the tone, and tell the user what you picked. Save:

```bash
python3 scripts/script_db.py save_preferences <<'EOF'
{"tone": "educational-patient", "video_length": "medium", "hook_style": "question",
 "target_audience": {"age_range": "18-30", "knowledge_level": "beginner"},
 "language": "en", "review_translation": "vi", "production": "opuscar-chapters",
 "opuscar_style": "", "voice": "",
 "personality": "calm-measured", "use_humor": "sparingly", "call_to_action_preference": "soft",
 "channel_niche": "economics explained"}
EOF
```

`opuscar_style` and `voice` stay empty until the first video picks them; save them then so later videos match.

### 3. Gather the brief

Topic/title, angle, must-include/avoid, CTA target. Ask only for what's missing; propose the key points yourself.

### 4. Outline

Size to ~150 words per minute. With `opuscar-chapters`, split into chapters per the reference's chapter rules; otherwise use sections. Show the outline as a table (id, title, one-line goal, seconds, words, hand-off to next) plus the through-line, and wait for the user's OK - fixing structure here is cheap, after the full script it isn't.

### 5. Write

Write the files in `scripts/<slug>/` in the user's project, as specified in the reference: `script.en.md` (narration only), `brief.md` (Series section + per-chapter visual intent and facts to verify), `script.vi.md` (review translation, only if `review_translation` is set). Pick the template matching the video type. Report each chapter's word count and estimated seconds.

### 6. Refine and save

Offer adjustments (stronger hook, trim/expand, tone, humor, data, storytelling, CTA). Keep the three files in sync on every change. Once the user accepts:

```bash
python3 scripts/script_db.py add_script <<'EOF'
{"title": "Why Printing Money Doesn't Make Anyone Richer", "type": "explainer",
 "tone": "educational-patient", "path": "scripts/why-printing-money", "chapters": 7,
 "word_count": 1500, "duration_minutes": 10}
EOF
```

The DB stores the path, not the text - the files are the source of truth.

### 7. Produce with Opuscar (production: opuscar-chapters)

Render each chapter as its own film with the `lemo-opuscar` skill, one run per chapter, using this prompt:

> Use lemo-opuscar. Make chapter chNN of "<title>", project folder `<slug>-chNN`. Follow the Series section and the chNN section of `scripts/<slug>/brief.md`. Narration is the chNN section of `scripts/<slug>/script.en.md`, word for word. The brief answers your questions; only ask about what it leaves open.

Render ch01 first and review it: the style, voice and subtitle look it lands on become the Series settings for every other chapter (write them into `brief.md` and the preferences). Then join:

```bash
python3 scripts/assemble.py <slug>.mp4 <slug>-ch01/<slug>-ch01.mp4 <slug>-ch02/<slug>-ch02.mp4 ...
```

It stream-copies the chapters (they must share style, size and fps), merges their `.srt` files with shifted timings, and prints YouTube chapter timestamps.

## DB commands

```bash
python3 scripts/script_db.py is_initialized
python3 scripts/script_db.py get_preferences
python3 scripts/script_db.py get_scripts                        # past scripts, for matching voice
python3 scripts/script_db.py stats
python3 scripts/script_db.py save_preferences < prefs.json      # merges into existing
python3 scripts/script_db.py add_script < script.json           # prints new id
python3 scripts/script_db.py update_script <id> < changes.json  # merges into that script
```
