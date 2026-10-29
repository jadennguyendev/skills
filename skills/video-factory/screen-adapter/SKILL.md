---
name: screen-adapter
description: Adapt a story or novel into film documents - source analysis, adaptation decisions, logline, synopsis, beat sheet, character/location/style bible and a formatted screenplay. Use when the user wants to turn a story, novel or text into a film or screenplay, write a beat sheet or bible for a film, decide what to cut or merge for an adaptation, or fix an existing screenplay. Writes videos/<slug>/02-adaptation/ and 03-script/.
---

# Screen Adapter

Three passes, each answering one question: what the story has (analysis), what the film will tell and how everything looks (development), how each scene plays (screenplay). Each pass does one job; keep them apart, even for a short story.

Without a `config.json`, set the video up through `../video-factory/SKILL.md` first. The gates are the routine in that file's "Gates" section. Formats shared with other stages (`config.json`, `bible.json`, `screenplay.json`) are in `../video-factory/references/formats.md`; this stage's own formats and rules are in `references/adaptation.md`. Read both, plus `references/genres/<genre>.md` when the primary genre in `config.json` has one: it adds to and overrides the core.

The source is `01-story/story.md` when it exists, else `00-source/source.md`.

## Workflow

### 1. Analysis

Take the story apart into `02-adaptation/analysis.json` (format in `references/adaptation.md`). Extract only: what the text says, "not mentioned" where it is silent, a short quote as evidence for each key moment. Nothing invented.

A source over about 20,000 words: split it at chapter breaks into batches of about 10,000 words, give each batch to a subagent with the analysis format and the extract-only rule, and merge the partial results yourself: one id per character and place, timeline renumbered in true order.

Done when every field is filled or marked "not mentioned" and every `unfilmable` passage the text holds is listed.

### 2. Development

1. **Decisions and beats** - against `config.json` (length, `max_characters`, `max_locations`), decide what to keep, cut, merge and add, each with a reason; write the logline, the synopsis and the beat sheet into `02-adaptation/beats.json`.
2. **Bible** - write `02-adaptation/bible.json`: characters, locations, style guide, plus any block the genre file adds. Characters and locations stay within the caps.

Hold a **gate**, the most important one: changing the ending or dropping a character costs minutes here and days later.

### 3. Screenplay

Under 10 minutes: write the whole screenplay in one pass. Longer: first a scene outline (one line per scene: heading, characters, purpose, tension; within the beat sheet's durations), then each scene in turn with the bible, a summary of the scenes before it and the next scene's outline in view.

Write `03-script/screenplay.json` to the writing rules in `references/adaptation.md`, then from the user's project, with this skill's folder as `<skill-dir>`:

```bash
python3 <skill-dir>/../video-factory/scripts/screenplay.py render videos/<slug>
python3 <skill-dir>/../video-factory/scripts/screenplay.py check videos/<slug>
```

Fix everything `check` lists until it prints `clean`. Then hand the screenplay to a fresh subagent with the script doctor brief in `references/adaptation.md` (plus the genre file's doctor checks), never reviewing your own draft in this context. It writes `03-script/review.md`. Fix exactly its findings, rerender, recheck, rerun the doctor: at most 2 fix rounds, then show the user `review.md` and let them decide.

Hold a **gate** on the screenplay.
