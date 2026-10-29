# Adaptation formats and rules

The core for every genre. A genre file in `genres/` adds fields, replaces the beat structure and adds rules and doctor checks.

## analysis.json

```json
{
  "meta": { "pov": "first person", "era": "1990s", "region": "Mekong Delta", "tone": "mournful, haunting" },
  "characters": [
    { "id": "lan", "name": "Lan", "role": "protagonist", "appearance": "...", "personality": "...", "relationships": "...", "arc": "..." }
  ],
  "locations": [ { "id": "old_house", "name": "Old house by the river", "time_of_day": "...", "description": "..." } ],
  "timeline": [ { "order": 1, "event": "...", "told_as_flashback": true } ],
  "key_moments": [ { "id": "m1", "description": "...", "intensity": 7, "evidence": "short quote from the text" } ],
  "motifs": ["ivory comb", "lullaby"],
  "cultural_elements": ["..."],
  "unfilmable": [ { "content": "Lan feels someone watching her", "note": "inner feeling" } ]
}
```

| Field | Why the next passes need it |
|-------|-----------------------------|
| `meta` | point of view decides whether the film uses voice-over; era and region set the look |
| `characters`, `locations` | raw material for the bible |
| `timeline` | true order, apart from the order of telling, so flashbacks can be rearranged |
| `key_moments` | the moments the film is built around, intensity 1-10, so the beat sheet can pace them |
| `motifs` | a visual thread across scenes |
| `cultural_elements` | beliefs, rituals, customs to get right |
| `unfilmable` | inner monologue, smell, abstract description: each must become image, sound or voice-over in the screenplay |

## beats.json

```json
{
  "decisions": [ { "action": "merge", "what": "the two aunts become one aunt", "why": "max_characters is 4" } ],
  "logline": "One sentence: who, what they want, what stands in the way.",
  "synopsis": "200-300 words, the whole film including the ending.",
  "beats": [ { "name": "Hook", "description": "...", "duration_sec": 20, "tension_target": 6 } ]
}
```

**Decisions** (`keep`, `cut`, `merge`, `add`), each with its reason:

- **Cut** to one main line: drop or merge minor characters, compress several chapters into one scene.
- **Externalize** the inner life: every thought the film needs becomes an action, an expression, an image or a line of voice-over.
- **Restructure** into one clear line: the novel may braid timelines; the film needs an opening, turning points, a climax and an end.
- Keep the source's world rules and main motifs; an `add` needs a reason the source cannot supply.

**Beat sheet** - the default structure for a short film (a genre file can replace it):

| Beat | Share of length | Holds |
|------|-----------------|-------|
| Hook | 0-5% | a first image that makes the viewer stay |
| Setup | 5-15% | the protagonist's normal world and want |
| Inciting incident | 15-25% | the event that breaks the normal |
| Rising complications | 25-60% | each attempt makes things worse |
| Revelation | 60-75% | the truth that changes the plan |
| Climax | 75-90% | the final confrontation |
| Resolution | 90-100% | what changed, or a last turn that lingers |

Length drives everything: about one scene per 40-60 seconds, so an 8-minute film has 8-12 scenes. The tension curve rises overall, with a release before each peak.

## Bible

Build `bible.json` (format in `../../video-factory/references/formats.md`) from the analysis and the decisions. Every `_en` field is the one canonical description, concrete enough to draw the same person twice: age, build, face, hair, a fixed costume. Add a voice description per character for dubbing, and lighting and ambient sound per location. Fewer characters and locations means more consistent pictures.

## Writing rules for screenplay.json

Film craft:

- Write only what can be seen and heard. Not "Lan is afraid" but "Lan freezes. Her breath quickens. She does not turn around."
- Every `unfilmable` item from the analysis becomes an image, a sound or voice-over.
- Dialogue short and sparse; silence carries more than talk.
- One scene, one purpose: the `purpose` line names what changes in it.

Production-aware writing (the film will be made with AI tools or a small crew):

- At most 2-3 characters on screen in a scene.
- Keep out crowds, fights, embraces and other complex physical contact.
- Favor still frames, slow movement and low light.
- Each action fits a single 5-10 second clip.
- Long lines spoken straight to camera are hard to lip-sync: use voice-over, or dialogue with the speaker turned away.

## Script doctor brief

Give the subagent `03-script/screenplay.txt`, `screenplay.json`, `02-adaptation/bible.json`, `beats.json`, `analysis.json` and this brief:

> You are the script doctor. Do not rewrite; report. Check the screenplay for: logic and continuity errors across scenes; any line of inner feeling that cannot be filmed; any `unfilmable` item from the analysis left unconverted; a scene too hard to produce under the production-aware rules (crowd, fight, more than 3 characters, an action longer than one 10-second clip); a world rule from the bible broken; a beat from the beat sheet missing or out of order. Write `03-script/review.md`: a verdict line (PASS or REVISE, round N), then a table (scene, quote, problem, fix). PASS means no findings.
