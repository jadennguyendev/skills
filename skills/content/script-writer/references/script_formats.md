# YouTube Script Formats and Structures

## Standard Script Structure (10-minute example)

```
[HOOK - 0:00-0:10]        Opening line that stops the scroll
[INTRO - 0:10-0:45]       What the video is about, why watch, what they'll learn, credibility
[MAIN CONTENT - 0:45-8:30]
  Section per point:      Intro to point > explanation > example/story > benefit > transition
[CONCLUSION - 8:30-9:30]  Recap, key takeaway, final thought, setup for CTA
[CTA - 9:30-10:00]        Primary CTA, secondary CTA (link, next video), sign-off
```

## Chapters (production: opuscar-chapters)

Each chapter is rendered as its own Opuscar film, then the films are joined with hard cuts. So every chapter must work alone and still flow into the next.

- **Length**: 60-120 s, 150-300 words. Never over 150 s - Opuscar's cost climbs steeply past 2-3 minutes. A 10-minute video is 6-8 chapters.
- **One idea per chapter**, with its own small arc: question or tension, explanation, turn.
- **Open on a hook in the first 3 seconds** - Opuscar demands it. No "In this chapter...", no title card at the start (use YouTube chapter markers instead).
- **End on a hand-off**: a line that closes this idea and opens the next ("But if printing money doesn't create bread... who ends up eating less?"). The next chapter opens by answering it, so the hard cut reads as continuous.
- **ch01** = video hook + intro + first idea. **Last chapter** = conclusion + CTA.
- **A visual through-line** (a recurring metaphor, object or character) carried across all chapters - it is what makes separately rendered films feel like one video.

## Output Files

```
videos/<slug>/
  script.en.md    # narration only - what the voice says, nothing else
  brief.md        # Series section + one visual brief per chapter, for Opuscar
  script.vi.md    # review translation of script.en.md (when review_translation is set)
  chNN/           # one Opuscar project per chapter (opuscar-chapters), rendering <slug>-chNN.mp4
  <slug>.mp4      # the chapters joined by assemble.py
```

All three use the same chapter headings (`## ch01 - <title>`), so they line up. Without chapters, use one heading per section (`## hook`, `## intro`, `## s1`...).

### script.en.md

Spoken words only, ready for TTS and subtitles: no cues, no brackets, no stage directions. Numbers written the way they should be read when it matters ("nine percent", "two thousand eight").

```markdown
# Why Printing Money Doesn't Make Anyone Richer

## ch01 - The billion-dollar question (~90 s, 220 words)

If the government printed a billion dollars for every person tomorrow... would you be richer?
...
But to see why, we need an island with ten people and ten loaves of bread.

## ch02 - What money really is (~100 s, 240 words)
...
```

### brief.md

```markdown
# Brief - Why Printing Money Doesn't Make Anyone Richer

## Series (same for every chapter)
- Opuscar style: <slug> - one style for all chapters
- Voice: Kokoro <voice name>, English
- Size/fps: 1920x1080, style default fps
- Subtitles: burned in, plus .srt
- Through-line: the island - same ten villagers and the same bakery in every chapter
- Score: same instrument palette and tempo across chapters; each chapter ends on a resolved cadence with ~0.5 s of room tone and opens without a musical pickup, so hard cuts land clean
- Audience: 18-30, no economics background

## ch01 - The billion-dollar question
- Length: ~90 s
- Viewer must understand: money is not the same thing as wealth (setup only)
- Must show: a billion arriving in everyone's account; the island introduced at the end
- Mood: curious, calm
- Enters from: cold open | Exits to: ch02 (the island)
- Facts to verify: none

## ch02 - What money really is
...
- Facts to verify: Berlin bread price 1923 (~250 marks in January to ~200 billion marks in November)
```

Describe what the viewer must see and understand - never camera moves, cuts or shot types. Opuscar writes its own treatment, shot list and transitions, and fights a shot list handed to it.

### script.vi.md

A faithful translation for the creator to review meaning and facts - not for publishing. Same headings; translate sentence by sentence, keep numbers and names identical, don't polish or adapt jokes.

## Common YouTube Video Types

### 1. Educational/Tutorial Videos
**Structure:**
- Hook (0-10 seconds)
- Introduction (10-30 seconds)
- Main content with clear sections (bulk of video)
- Recap/Summary
- Call to action

**Characteristics:**
- Clear, step-by-step explanations
- Visual cues mentioned ("as you can see here")
- Numbered points or sections
- Pause points for viewer to follow along

### 2. Listicle/Top X Videos
**Structure:**
- Hook with the promise
- Quick intro
- Item #X (countdown or count up)
- Each item: Name → Explanation → Why it matters
- Conclusion with recap
- CTA

**Characteristics:**
- High energy
- Quick pace
- Transitions between items
- Suspense building (save best for last)

### 3. Story/Narrative Videos
**Structure:**
- Compelling hook
- Setup/Context
- Rising action
- Climax
- Resolution
- Reflection/Lesson
- CTA

**Characteristics:**
- Emotional connection
- Descriptive language
- Pacing variety
- Character development
- Plot twists or reveals

### 4. Review Videos
**Structure:**
- Hook with verdict tease
- Introduction to product/subject
- Pros
- Cons
- Comparisons (if applicable)
- Final verdict
- Who it's for
- CTA

**Characteristics:**
- Balanced perspective
- Specific examples
- Personal experience
- Clear criteria
- Honest assessment

### 5. Vlog Style
**Structure:**
- Energetic hook
- What's happening today
- Chronological or thematic sections
- Behind-the-scenes moments
- Reflection/Lesson learned
- CTA

**Characteristics:**
- Conversational
- Personal
- Authentic
- Energy shifts
- Direct address to camera

### 6. Commentary/Opinion Videos
**Structure:**
- Hook with controversial/interesting take
- Context/Background
- Main argument with supporting points
- Counter-arguments addressed
- Conclusion with final stance
- CTA

**Characteristics:**
- Strong voice
- Persuasive language
- Evidence and examples
- Conversational yet authoritative
- Engagement with opposing views

## Detailed Templates

### Educational Tutorial
```
[HOOK] Problem statement + promise of solution
[INTRO] Personal context + what you'll learn + why it matters
[SECTION 1] Concept: what it is, why it matters, common mistakes
[SECTION 2] Step-by-step: each step with visuals, examples, tips
[SECTION 3] Pitfalls: what to avoid, troubleshooting
[CONCLUSION] Recap + key takeaway + next steps
[CTA] Subscribe + resources + comment prompt
```

### Listicle (countdown)
```
[HOOK] Number tease + unexpected angle
[INTRO] Context + why this list matters
[ITEM 5..2] What it is, why it works, how to use it
[ITEM 1] Most important/surprising - extra emphasis, best benefit
[CONCLUSION] Recap numbers + ultimate takeaway
[CTA] Strong directive + resource mention
```

### Story/Narrative
```
[HOOK] Compelling story opening
[INTRO] Setup the story context
[SECTION 1] Problem/conflict: build tension, show stakes, make it relatable
[SECTION 2] Journey: challenges, attempts and failures, learning moments
[SECTION 3] Resolution: how it worked out, the transformation
[CONCLUSION] Lesson learned + how viewers can apply it
[CTA] Invite similar stories + subscribe
```

## Script Components Breakdown

### The Hook (First 5-10 seconds)
**Purpose:** Stop the scroll, capture attention immediately

**Techniques:**
- Question: "Have you ever wondered why...?"
- Bold statement: "This changed everything I thought I knew about..."
- Conflict: "I made a huge mistake and here's what happened..."
- Promise: "By the end of this video, you'll know exactly how to..."
- Shock: "I lost $10,000 in 5 minutes..."
- Pattern interrupt: "Stop! Before you [common action], watch this..."

**Examples:**
- "In the next 60 seconds, I'm going to show you a trick that will save you hours"
- "This is the most important thing I've learned in 10 years of..."
- "Everyone gets this wrong, and it's costing them..."

### The Introduction (10-45 seconds)
**Purpose:** Establish credibility, set expectations, deliver on hook promise

**Elements:**
- Who you are (if relevant)
- What the video is about
- Why it matters to viewer
- What they'll learn/gain
- Quick preview of main points

**Example:**
"Hey everyone, I'm [Name], and today we're diving into [topic]. If you've ever struggled with [problem], this video is for you. I'm going to show you [solution] that [benefit]. We'll cover [point 1], [point 2], and [point 3]. Let's get started."

### The Main Content
**Purpose:** Deliver the value promised in hook and intro

**Best Practices:**
- Break into clear sections
- Use transitions
- Repeat key points
- Provide examples
- Address common objections
- Maintain energy
- Include visual references

**Transition Phrases:**
- "Now that we've covered X, let's move on to Y"
- "Here's where it gets interesting..."
- "The next point is crucial..."
- "Before we continue, quick note about..."

### The Conclusion
**Purpose:** Reinforce key takeaways, create satisfaction

**Elements:**
- Summarize main points
- Restate key benefit
- Final thoughts or reflection
- Bridge to CTA

**Example:**
"So to recap, we covered [point 1], [point 2], and [point 3]. The main thing to remember is [key takeaway]. Now you're ready to [apply knowledge]."

### The Call to Action (CTA)
**Purpose:** Guide viewer to next action

**Types:**
- Subscribe: "If you found this helpful, subscribe for more..."
- Like/Comment: "Let me know in the comments..."
- Watch next: "Check out this video where I show you..."
- External link: "Grab my free guide in the description..."
- Social follow: "Follow me on Instagram for..."

**Best Practices:**
- One primary CTA
- Make it specific
- Explain the benefit
- Create urgency (if appropriate)

## Tone Guidelines

Example openers:
- Casual-friendly: "Hey everyone! So, funny story - I completely messed this up last week. Like, embarrassingly bad. But here's what I learned..."
- Professional: "In today's video, we're examining the three core principles that drive successful implementation. Based on 5 years of data..."
- Energetic: "Okay, THIS is insane! I just discovered something that's going to blow your mind. Are you ready?"
- Educational-patient: "Let's break this down step by step. Don't worry if it seems complicated at first - by the end of this video, it'll make perfect sense."

### Professional/Authoritative
- Confident language
- Industry terminology (with explanations)
- Cited sources
- Measured pace
- Clear structure

### Casual/Friendly
- Conversational language
- Personal anecdotes
- "You" and "I" language
- Relaxed structure
- Humor when appropriate

### Energetic/Enthusiastic
- Exclamation points
- Quick pace
- Dynamic vocabulary
- Momentum building
- High energy throughout

### Educational/Patient
- Clear explanations
- Step-by-step approach
- Anticipate questions
- Reassuring language
- Allow processing time

### Inspirational/Motivational
- Empowering language
- Story-driven
- Emotional connection
- Aspirational examples
- Encouraging tone

## Timing Guidelines

### Short Form (3-5 minutes)
- 450-750 words
- Single focused topic
- Quick hook (5 seconds)
- Streamlined content
- Fast pace

### Medium Form (7-12 minutes)
- 1,050-1,800 words
- 2-3 main points
- Standard hook (8-10 seconds)
- Moderate depth
- Balanced pace

### Long Form (15-30 minutes)
- 2,250-4,500 words
- Deep dive
- Strong hook (10-15 seconds)
- Multiple sections
- Varied pace

## Engagement Techniques

### Retention
- Tease what's coming, pay off every promise made
- Callback references to earlier points
- Pattern interrupt every 30-60 seconds
- Vary sentence length and energy

### Pattern Interrupts
- Unexpected statements
- Questions
- Tone shifts
- Visual changes
- Sound effects

### Storytelling Elements
- Characters
- Conflict
- Resolution
- Emotional arc
- Relatability

### Social Proof
- Statistics
- Expert quotes
- Case studies
- Personal results
- Testimonials

### Curiosity Gaps
- Tease information
- "But here's the thing..."
- "Wait until you see..."
- "The surprising part is..."

## Common Script Mistakes to Avoid

1. **Burying the lede** - Get to the point quickly
2. **Rambling introduction** - Hook first, context later
3. **No clear structure** - Viewers need signposts
4. **Talking too fast** - Leave room for visuals
5. **Being too formal** - YouTube is conversational
6. **No personality** - Let your unique voice shine
7. **Forgetting the CTA** - Always guide next steps
8. **Too much information** - Focus on key takeaways
9. **No energy variation** - Monotone loses viewers
10. **Ignoring target audience** - Speak directly to them

## Visual Intent

Visual notes belong in `brief.md`, never in the narration. Write intent, not direction:

- Good: "Viewer must see the price of bread doubling while the number of loaves stays at ten."
- Bad: "[Cut to close-up of bakery shelf, slow push-in]"

For every number that will appear on screen, add it to "Facts to verify" with the claimed value - a wrong figure gets drawn into the film.

## Audience-Specific Adjustments

### Beginners
- Define terminology
- Slower pace
- More examples
- Encouragement
- Step-by-step

### Intermediate
- Assume baseline knowledge
- Faster pace
- Advanced tips
- Comparisons
- Nuance

### Expert
- Industry language
- Quick pace
- Deep insights
- Technical details
- Cutting-edge info

## Platform-Specific Considerations

### YouTube Shorts (Under 60 seconds)
- Immediate hook
- Single point
- No intro
- Fast cuts
- Vertical format
- Text on screen

### YouTube Main Feed
- Strong thumbnail/title synergy
- 8-15 minute sweet spot
- Watch time optimization
- Chapter markers
- End screen elements

### Educational Content
- Thorough explanations
- Longer acceptable
- Downloadable resources
- Chapters crucial
- Timestamps helpful
