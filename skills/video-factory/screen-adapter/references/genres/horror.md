# Horror

Use when: the film is meant to frighten - ghost stories, hauntings, folk horror, curses. Adds the entity (the ghost or force), its rules and its staged reveal to the core in `../adaptation.md`.

## Analysis additions

```json
"entity": {
  "identity": "...", "origin": "...", "motive": "why it hates, what it wants",
  "rules": ["appears only when it rains", "announced by a lullaby"],
  "weaknesses": ["..."], "limits": ["..."]
}
```

- `key_moments` are the scare moments, each with intensity 1-10 and a quote as evidence: they pace the scares.
- `cultural_elements` matters most here: beliefs and rituals (ancestor offerings, water spirits, curses) are where an adaptation goes wrong.

## Beat sheet (replaces the core structure)

| Beat | Share of length | Holds |
|------|-----------------|-------|
| Hook | 0-5% | an opening that unsettles or intrigues at once |
| Normal | 5-15% | the characters and place before anything happens |
| First sign | 15-25% | something small and wrong, still explainable |
| Escalation | 25-60% | the signs grow clearer; the protagonist starts to dig |
| Discovery | 60-75% | the entity's origin comes out, often as a flashback |
| Climax | 75-90% | face to face, the peak of fear |
| End / twist | 90-100% | resolution, or a last turn that lingers |

Every peak gets a quiet beat before it; tension rises across the film.

## Bible addition: entity

```json
"entity": {
  "identity": "...",
  "rules": ["appears only when it rains", "announced by a lullaby"],
  "warning_signs": { "sound": "a faint lullaby", "visual": "candle flames bend, wet marks on the floor" },
  "stages": {
    "sign":    { "description": "not seen; only traces: water marks, fallen hair", "visual_en": "wet footprints on the wooden floor, a few long black hairs" },
    "shadow":  { "description": "a dark shape, outline only", "visual_en": "a faint dark long-haired silhouette, no face visible" },
    "partial": { "description": "part of it: a hand, wet hair, half a face", "visual_en": "a pale wet hand with long nails, wet black hair covering half a face" },
    "full":    { "description": "fully seen; the climax only", "visual_en": "a drowned young woman in a soaked white ao dai, grey skin, black eyes" }
  },
  "stage_by_beat": { "First sign": "sign", "Escalation": "shadow", "Discovery": "partial", "Climax": "full" }
}
```

`shot-list` checks every shot's `entity_stage` against these stage names, and builds prompts from their `visual_en`.

## Writing rules (add to the core)

- Before every scare: a beat of silence or a false scare.
- The entity appears only under its rules, and only at the stage `stage_by_beat` allows for the scene's beat.
- Let the entity show through shadow, reflection and the edge of the frame before it shows in full.
- Fear lives in sound: give each scare scene a `sound` element (the warning sign, then silence).

## Doctor checks (add to the brief)

- Does any scene break an entity rule, or show it at a later stage than its beat allows?
- Is there a release before each peak, and does the tension curve rise across the film?
