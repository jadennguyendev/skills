---
name: narration-script
description: Write production-ready voice-over scripts for YouTube videos - explainers, documentaries, true crime, narrated stories, comedy - split into chapters, with visual intent per chapter. Use when the user asks for a YouTube or video script, a narration or voice-over script, a hook or intro, a script outline, a Shorts script, chapters for a long video, or wants to rewrite, trim or change the tone of an existing script. Writes videos/<slug>/03-script/.
---

# Narration Script

Without a `config.json`, set the video up through `../video-factory/SKILL.md` first; tone, audience, language and length come from it. The gates are the routine in that file's "Gates" section. Structures, chapter rules and tone examples live in `references/script_formats.md` - read it before writing. Story and narration craft from screenwriters, documentary makers and radio producers lives in `references/craft_principles.md`, with the source for each principle.

## Workflow

### 1. Gather the brief

Topic/title, angle, must-include/avoid, CTA target, from `00-source/source.md` and the user. Ask only for what's missing; propose the key points yourself.

Pick the genre yourself from the topic - don't ask unless two fit equally. Up to two: a primary and an optional secondary (a true-crime case told as history: `true-crime` + `history-documentary`). Tell the user which you picked in one line and record it as `genre` in `config.json`.

| Genre | Pick when the video... | Reference |
|-------|------------------------|-----------|
| `explainer` | explains how something works, why something happens, science, money, tech | core only (`craft_principles.md`) |
| `history-documentary` | tells real events, eras, places or a real person's life | `references/genres/history-documentary.md` |
| `true-crime` | follows a real crime, investigation, scam, disappearance or unsolved case | `references/genres/true-crime.md` |
| `horror` | is meant to scare: scary stories, supernatural, creepy places, folk horror | `references/genres/horror.md` |
| `fiction` | tells an invented story: drama, sci-fi, fantasy, fable, folk tale | `references/genres/fiction.md` |
| `comedy` | is mainly meant to be funny: satire, humorous narration | `references/genres/comedy.md` |

Read the genre files (primary first) next to `craft_principles.md`: they add principles, override core ones that don't fit the genre, and list what the bible must hold ("Bible additions").

### 2. Outline

Read `references/craft_principles.md` and the genre files first. Above the table, give the "a story about X, and what's interesting is Y" line and the whole video told in two or three sentences; if Y is what anyone would guess, propose a sharper angle before outlining. Size to ~150 words per minute and split into chapters per the chapter rules in `references/script_formats.md`. Show the outline as a table (chapter, title, one-line goal, seconds, words, hand-off to next) plus the through-line, and hold a **gate** - fixing structure here is cheap, after the full script it isn't.

### 3. Write

Write to the avoid-ai-writing standard from the first draft: read `../avoid-ai-writing/SKILL.md`, its `references/patterns.md` and `../script-qa/narration-profile.md` before writing. Fixing AI-isms after the fact costs a QA round. Before the QA gate, run the revision checklist at the end of `references/craft_principles.md` and fix what fails.

Write two files (formats in `../video-factory/references/formats.md`, the narration mapping in `references/script_formats.md`):

- `02-adaptation/bible.json` - the lean bible: `series` (through-line, audience, the genre's bible additions), `style_guide`, and recurring characters or places if the video shows any.
- `03-script/screenplay.json` - one scene per chapter: `title`, `est_duration_sec`, `facts_to_verify`, each spoken paragraph as a `vo` element, the visual intent as `action` elements.

Then from the user's project, with this skill's folder as `<skill-dir>`:

```bash
python3 <skill-dir>/../video-factory/scripts/screenplay.py render videos/<slug>
python3 <skill-dir>/../video-factory/scripts/screenplay.py check videos/<slug>
```

`render` writes `03-script/script.<lang>.md` (narration only, what the voice says) and `screenplay.txt`. Fix everything `check` lists until it prints `clean`. Report each chapter's word count and estimated seconds.

### 4. QA gate

English only (`language: en`); for any other language, tell the user the script has no QA and go to step 5.

Hand `03-script/script.en.md` to a fresh subagent running the `script-qa` skill, with the round number (1 for a new draft, +1 per fix round) - never review your own draft in this context. It writes `03-script/review.md` with a PASS / REVISE / FAIL verdict and quoted findings.

- PASS: show the verdict line and go on.
- REVISE or FAIL: fix exactly the listed findings in `screenplay.json` (no other rewording), rerender, and run QA again.
- At most 2 fix rounds. Still not PASS after that: stop and show the user `review.md` - they decide whether to fix further or accept.

Any later change to the narration reruns this gate.

### 5. Refine

Hold a **gate** on the script. Offer adjustments (stronger hook, trim/expand, tone, humor, data, storytelling, CTA); every change goes into `screenplay.json`, then rerender.
