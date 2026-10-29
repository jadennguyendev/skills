---
name: script-qa
description: Independently QA and score an English video narration script against the avoid-ai-writing standard, and write a PASS / REVISE / FAIL verdict with quoted findings to qa.md. Use when the user asks to QA, review, grade, score or audit a video script, check whether a script "sounds like AI" or is ready to record or render, or when script-writer reaches its QA gate. Scores only, never rewrites.
---

# Script QA

You are the reviewer, not the writer: read the script cold and judge it. Never edit the script; the writer fixes from your report. English only - for any other language, say it is unsupported and stop.

`scripts/...` and `narration-profile.md` live in this skill's folder; run from the user's project and call them by that path. The rulebook is the vendored `avoid-ai-writing` skill next to this one (`../avoid-ai-writing/`). If it is missing, stop and tell the user to install `avoid-ai-writing` from this repo.

## Workflow

### 1. Load the standard

Read in full: `../avoid-ai-writing/SKILL.md`, `../avoid-ai-writing/references/patterns.md` (about 870 lines - read it in pages), then `narration-profile.md`. The profile overrides the upstream tolerances and tiers for spoken scripts.

Then the genre: read the `Genre:` line in the Series section of `videos/<slug>/brief.md` (missing means `explainer`). For each genre other than `explainer`, read the "Brief additions" and "QA overrides" sections of `../script-writer/references/genres/<genre>.md`. The primary genre's overrides win over the narration profile; a secondary genre's apply only where the primary is silent. Its "Genre clichés" are P1 findings. Anything its "Brief additions" asks for that `brief.md` lacks goes in Notes, not scored. Name the genre and the overrides you applied in `qa.md`. Use the upstream rules, not its output format: `qa.md` below replaces upstream's detect-mode report.

### 2. Deterministic layer

From the user's project, with this skill's folder as `<skill-dir>`:

```bash
node <skill-dir>/scripts/score.js videos/<slug>/script.en.md
```

Exit 0 pass, 1 fail, 2 error. The JSON holds the detector `score` (0-100, higher is more AI-like), the `critical` count, `flagged` findings and the `allowed` ones the narration profile tolerates. `pass` is the detector gate: no critical finding and at most 6 flagged. If Node is unavailable or the script errors, record the layer as `not run` and continue - never claim it ran.

### 3. Judgment layer

Every `flagged` and `allowed` item is a candidate: confirm it against the rule's context exceptions (editing contract in the upstream SKILL.md) and the narration profile, then tier it per the profile's tier map. Only confirmed findings count toward the QA score.

Then read the whole script, chapter by chapter, for what the detector cannot see: staccato drama, same-opener runs, manufactured punchlines, copula avoidance, rhythm, stacked questions, invented specifics (checked against `videos/<slug>/brief.md`: "Facts to verify" for nonfiction, the story bible for invented stories; no brief means note it as not checked), hooks and CTA. Each finding needs the exact quote, the chapter, the tier, the rule, and a concrete fix. Several tells in one sentence that one edit fixes count as one finding, at the highest tier.

Judge the current script in full every round; do not carry findings over from an older `qa.md`.

Also compare each heading's estimate (words, or seconds at 150 words per minute) with the narration under it as written now, CTA included; a gap over 15% goes in Notes (timing, not scored).

### 4. Score and verdict

```
QA score = 100 - 25 x P0 - 8 x P1 - 2 x P2   (floor 0)
PASS    P0 = 0, score.js exit 0, QA score >= 85
REVISE  P0 = 0, but score.js failed or QA score < 85
FAIL    any P0
```

The detector gate is a floor: it misses judgment-only tells, so a script can pass score.js and still get REVISE.

ponytail: the weights and the 85 cut are a first guess; recalibrate once ~10 real scripts have been scored.

### 5. Write `videos/<slug>/qa.md`

Overwrite on each run, so `qa.md` is always the latest round. The caller gives the round number (script-writer does); without one, use 1:

```markdown
# QA - <title>

Verdict: PASS | REVISE | FAIL - QA score 91 (P0 0, P1 1, P2 0) - round 1

## Checks
- Detector (score.js): executed - exit 0, score 8 (Minimal), 2 flagged, 1 allowed
- Judgment pass: model-only, narration profile + genre horror (QA overrides: staccato relaxed, second-person opener allowed)

## Findings
| # | Chapter | Tier | Rule | Quote | Fix |
|---|---------|------|------|-------|-----|
| 1 | ch03 | P1 | Infomercial hook | "Here's the thing." | Cut it; open on "Prices doubled in a month." |

## Notes
Judgment calls kept as-is and why; anything not checked.
```

Then report the verdict and score in one line, with the path to `qa.md`.
