---
name: story-writer
description: Turn the user's material (an idea, an outline, notes, a draft or a story found elsewhere) into a complete novel or novella, after grilling the user until every story decision is settled. Use when the user wants a story written, rewritten or expanded as fiction prose, a novel or short story from an idea, or a source story built before adapting it into a film. Writes videos/<slug>/01-story/.
---

# Story Writer

Write in `config.json`'s `language` (default English); without a `config.json`, set the video up through `../video-factory/SKILL.md` first. The gates are the routine in that file's "Gates" section. Craft lives in `references/craft.md`: read it before the outline and again before writing.

## Workflow

### 1. Grill

Read `00-source/source.md` and work out what it already settles. Then interview the user in **rounds** until every item on the readiness checklist is settled:

- Ask every open item whose prerequisites are settled, numbered, each with your recommended answer, worded so "yes" accepts it. An item that depends on another still open waits for a later round.
- Recommend from the source and from craft; never ask what the source already answers. When the source contradicts itself, ask which version holds.
- An answer can reopen an item already settled: ask it again.

**Readiness checklist**

| Item | Settled when |
|------|--------------|
| Premise | one line: "a story about X, and what's interesting is Y", with a Y nobody would guess |
| Protagonist | name, age, look, what they want, what they need, what stops them |
| Opposition | who or what pushes back, and why it wants what it wants |
| Cast | every other named character has a job in the plot; the rest are merged or cut |
| World and rules | time, place, and every rule the plot leans on (a ghost's rules, a magic's cost, a law) |
| True timeline | what happened, in the order it happened, including before page one |
| Telling | point of view and tense, where the story opens, which events come as flashback |
| Ending | the last scene and what has changed, decided before writing |
| Genre and tone | genre, mood, audience, content limits |
| Length | target words and chapter count |
| Source fidelity | what from the user's material stays unchanged, and what must not appear |

The grill is done when every row is settled and the user agrees the story is ready to write. Write `01-story/story-bible.md` with one section per row, then hold a **gate** on it.

### 2. Outline

Above the outline, the premise line and the whole story told in three sentences. Then a table: chapter, title, what happens, whose point of view, the turn that ends it, estimated words. Every row of the true timeline is either told, implied or deliberately left out, and the outline says which. Hold a **gate**.

### 3. Write

Write chapter by chapter into `01-story/story.md`: `# <title>`, then `## Chapter N - <title>` per chapter. Before each chapter, reread its outline row and the bible sections it touches. Keep each chapter within 15% of its estimate. When done, run the revision checklist at the end of `references/craft.md`, fix what fails, and report the word count per chapter.

### 4. Review

Hand `story.md` and `story-bible.md` to a fresh subagent with this brief, never reviewing your own draft in this context:

> Check `01-story/story.md` against `01-story/story-bible.md` and write `01-story/review.md`: a verdict line (PASS or REVISE, round N), then a table of findings (chapter, quote, problem, fix). A finding is: a name, age, look, place or rule that contradicts the bible; an event out of the bible's true timeline; a bible decision missing from the story (ending, POV, a must-keep from the source); a setup never paid off or a payoff never set up; a point-of-view slip. PASS means no findings.

On REVISE, fix exactly the findings and run the review again, at most 2 fix rounds; still not PASS, show the user `review.md` and let them decide. Then hold the final **gate** on `story.md`.
