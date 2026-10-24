---
name: idea-hunter
description: Find, score, and stress-test consumer app ideas for Gen Z US/EU with $10k MRR potential and TikTok/IG virality, across a wide spread of topics. Use when the user asks to hunt or brainstorm app ideas, rate or validate an idea ("is this idea good", "rate this", "worth building"), audit an existing app or repo for viral features and monetization gaps, or mentions consumer app, Gen Z, viral loop, holy-shit moment, or idea evaluation.
---

# Consumer App Idea Hunter

Find or evaluate consumer app ideas for Gen Z US/EU: plausible $10k MRR path, demoable on TikTok/Reels/Shorts.

## Modes

Infer from what the user brings; ask only if ambiguous:

- **hunt** - no idea given. Optional inputs: niche, audience, platform, constraints. Pick domains per **Spread**, research, output 3-5 ranked ideas.
- **rate** - user describes an idea. Score it.
- **audit** - user points at an existing app or repo. Inventory its features (codegraph if the project has it, else README/routes/screens), score each feature as a viral candidate, then output: lead feature to market with, 2-3 concrete TikTok demo scripts for it, and the monetization gaps.

## Spread

Hunt output is a spread: every idea in a batch sits in a different domain AND uses a different core mechanic. Before researching, list the chosen domain + emotion + mechanic per slot, so the spread is visible.

No niche given: draw from at least 3 different buckets, and rotate away from domains already covered earlier in the conversation. Niche given: spread across emotions and mechanics inside it instead.

| Bucket | Domains |
|---|---|
| Money | budgeting, side hustles, resale/thrifting, deals, first job pay, splitting costs |
| People | dating, friendships, group chats, roommates, family, breakups |
| Self | style, skin/hair, fitness, sleep, period/hormones, mental health, habits |
| Growth | study, languages, career, interviews, creator skills, public speaking |
| Life | food/cooking, renting/moving, travel, nightlife/going out, pets, plants, cars/commute |
| Play | music, gaming, fandoms, astrology/spirituality, sports, art/making, collecting |
| World | sustainability, local events, civic/politics, news literacy |

Mechanics: photo/scan, rating, prediction, transformation, comparison, quiz, voice, matching, recap/wrapped, screenshot or receipt parsing, map/location, generator (plan, outfit, playlist), what-if simulation, challenge/streak, multiplayer/group.

## Research

Web search, free, never blocks. Recipe per domain:

- Reddit pain threads: complaints, "is there an app that", workaround posts.
- TikTok hashtags and creators in the niche: what formats already get views.
- App Store / Google Play competitors and their 1-3 star reviews.

**Deep** (user asks, or validating a single idea in rate mode): add Meta Ad Library / TikTok Creative Center (is anyone paying to acquire users here?), and a second pass validating the top 1-2 ideas before the final verdict.

Cite the threads, apps and reviews behind each score.

## Scoring /10

Score each criterion 0-10 and show the full table:

1. **Pain** - real, felt problem? Problem > trend.
2. **Frequency** - how often it hits.
3. **Emotion** - ties to insecurity, money, appearance, relationships, status, confidence, loneliness, belonging, curiosity, or self-improvement.
4. **Holy Sh*t Moment** - one feature that produces "I need to try this" in seconds, with a personalized result.
5. **Virality** - core feature demoable in a 5-second clip using one of the mechanics above.
6. **Monetization** - clear reason to pay: premium results, tracking, recurring analysis, personalization, subscription or credits.
7. **Retention** - recurring use, or strong one-shot with a viral loop or heavy one-time monetization.
8. **MVP simplicity** - solo founder can build fast with AI APIs, camera, vision, audio, LLM, simple backend.
9. **Differentiation** - checked against real App Store competitors, not vibes.
10. **$10k MRR potential** - plausible math (e.g. ~1k subscribers at $10/mo) given niche size and price point.

Gates: **Pain <6 or Holy Sh*t Moment <6 -> reject**, regardless of total.
Verdict bands: **>=8 pursue / 6.5-8 iterate / <6.5 drop**.
On reject or iterate, give exactly ONE concrete pivot: the weakest axis and how to fix it.

## Output

Hunt opens with the spread table (slot -> domain -> emotion -> mechanic). Per idea, in order:

```
**Problem** -> **App** -> **Holy Sh*t Moment** -> **Why it spreads** -> **Monetization** -> **Score** table -> **Verdict** (+ pivot if rejected)
```

Simple-concept test: the idea must explain in 3 sentences max (problem -> action -> result). If it can't, that itself is a finding - say so.

Audit mode output: feature inventory -> per-feature HSM/virality score -> recommended lead feature -> 2-3 TikTok demo scripts -> monetization gaps.

All output is conversational - write files only if the user asks.
