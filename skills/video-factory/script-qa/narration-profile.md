# Narration profile

Upstream avoid-ai-writing has no profile for spoken scripts. This one adds it. Start from the `linkedin` column of the tolerance matrix in `../avoid-ai-writing/references/patterns.md`, then apply the overrides below. The detector runs in `general` context (upstream maps `linkedin` to `marketing`, which the detector scores the same as `general`).

Writers: use the `warm` voice, or `casual` when the saved script-writer tone is casual-friendly or humorous. Reviewers: voice does not change the score.

The text is `script.en.md`: words a TTS voice reads, nothing else. Headings (`# title`, `## chNN - title`) are never spoken and are not audited.

## Overrides

| Rule | Narration | Why |
|------|-----------|-----|
| Rhetorical questions | relaxed: one per chapter as a hook or turn; a stacked run of 2+ is still a finding | A question is how a speaker hands the listener a problem |
| Direct address ("you", "we") | allowed | Spoken register |
| "Let's" constructions | relaxed: one plain "let's" per video ("Let's start with the bread"); "Let's dive in", "Let's break this down", "Let's take a closer look" stay findings | The stock ones are the tell, not the word |
| Subjectless fragments | relaxed: a deliberate fragment for emphasis is fine; three or more in a row is staccato drama | Speech is fragmentary, drama-by-fragment is the tell |
| Transitions | Moreover / Furthermore / Additionally / In conclusion are findings; spoken signposts ("First", "Here is the problem", "Back to the island") are fine | Listeners need signposts, not essay connectors |
| Uniform paragraph length | skip | Paragraphs are invisible in audio |
| Sentence rhythm | strict: varied lengths, read aloud it must not sound like a metronome | Replaces upstream's "read-aloud test", which assumes TTS-sounding means bad; here TTS is the medium, so judge the rhythm a listener hears |
| Em dashes | strict, target zero | TTS reads them inconsistently; use a period or comma |
| Infomercial hooks ("Here's the thing", "The catch?", "Plot twist:", "But wait", "Wait until you see") | strict | The most common AI-script tell |
| Speculative openers ("Imagine a world where") | strict | Open on a concrete scene or number instead |
| Significance inflation, Tier 1 words, vague attribution ("experts say", "studies show") | strict | Same as upstream: credibility killers |
| CTA | one specific ask in the last chapter ("If you want the next one on inflation, subscribe"); engagement bait ("Trust me, you'll want to save this", "You won't want to miss this") is a finding | Upstream social-endorsement closers |
| Generic conclusions ("So to recap", "At the end of the day") | strict | End on the payoff of the through-line instead |

## Tier map

Upstream P0/P1/P2 apply as written. Detector severities map critical = P0, high = P1, medium = P2; low is a note, not scored. For rules upstream or the detector leave untiered:

- **P1**: infomercial hooks, speculative openers, engagement-bait CTA, stacked rhetorical questions, staccato drama (3+ fragments in a row), invented specifics (see below).
- **P2**: same-opener runs, manufactured punchlines, performed insight ("That is the whole trick"), metronome rhythm, spoken mechanics below.

**Invented specifics.** Nonfiction: any number, name, date or quote not in the brief's "Facts to verify". Declared fiction: a name, place, world rule or plot fact that contradicts the story bible, or a new named character, place or rule missing from it. Incidental texture (a time of day, a gesture, a count of knocks) is not a finding unless it contradicts the bible.

Genre files in `../script-writer/references/genres/` can relax or tighten any rule in this profile through their "QA overrides" table; script-qa applies them per the `Genre:` line in `brief.md`.

## Spoken mechanics (P2 when broken)

- Numbers, dates, units and symbols written the way they should be read ("nine percent", "two thousand eight").
- No stage directions, brackets, cues, URLs or markdown emphasis inside narration.
- Abbreviations the voice must spell out are written out ("for example", not "e.g.").
- A sentence a listener must hold in memory over 30 words is a finding: split it.

## What a clean hook looks like

- A concrete question with stakes: "If the government printed a billion dollars for every person tomorrow, would you be richer?"
- A specific claim with a number the video pays off: "In 1923 a loaf of bread in Berlin cost two hundred billion marks."
- A scene: "Ten people live on an island with ten loaves of bread."
