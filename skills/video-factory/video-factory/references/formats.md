# Shared formats

The files more than one skill reads. `screen-adapter` and `narration-script` write them, `shot-list`, `script-qa` and `scripts/` read them. Stage-only files (`analysis.json`, `beats.json`, `shotlist.json`) are specified in the skill that writes them.

Ids are lowercase snake_case (`lan`, `old_house`) and never change once written; every other file refers to characters and locations by id.

## config.json

`videos/<slug>/config.json`, written at setup from `.video-factory.json` (the project defaults, same keys) plus the user's answers.

```json
{
  "title": "The Comb in the Mirror",
  "slug": "comb-in-the-mirror",
  "branch": "film",
  "genre": ["horror"],
  "language": "en",
  "review_language": "vi",
  "production_tool": "none",
  "target_duration_min": 8,
  "aspect_ratio": "16:9",
  "platform": "YouTube",
  "audience": "18-35, horror fans",
  "tone": "slow, mournful dread",
  "visual_style": "cinematic, cold desaturated grade, film grain, low light",
  "max_characters": 4,
  "max_locations": 3,
  "max_clip_sec": 8
}
```

| Key | Values | Read by |
|-----|--------|---------|
| `branch` | `film` (story -> screenplay) or `narration` (voice-over video) | all |
| `genre` | primary first, optional secondary; narration: `explainer`, `history-documentary`, `true-crime`, `horror`, `fiction`, `comedy`; film: `horror` or a free word with no genre file | writers, script-qa |
| `language` | language of everything the audience hears or reads; default `en` | writers, `screenplay.py` |
| `review_language` | language of the review copies (see SKILL.md, Gates); default `vi`; empty for none | gates |
| `production_tool` | `none` (default), `opuscar`, `ai-gen`; only `ai-gen` makes `shot-list` build prompts and reference names | `shot-list` |
| `max_characters`, `max_locations` | caps for the bible; fewer means steadier visuals | `screenplay.py check` |
| `max_clip_sec` | longest single clip the production tool makes | `shot-list` |

## bible.json

`02-adaptation/bible.json`. The canonical description of everything that must look and sound the same everywhere. Fields ending in `_en` are always English, whatever `language` is: they are copied word for word into image prompts, so write each one once, concretely (age, build, face, hair, fixed costume), and never paraphrase it elsewhere.

```json
{
  "series": {
    "through_line": "the ivory comb: found in scene 1, in the ghost's hand in the last scene",
    "audience": "18-35, horror fans",
    "notes": ["Reveal ledger: ..."]
  },
  "style_guide": {
    "palette": "wood brown, candle amber, black",
    "lighting": "motivated low-key: candles and oil lamps only",
    "texture": "35mm film grain",
    "forbidden": ["harsh daylight", "crowds"],
    "prefix_en": "Cinematic horror film still, cold desaturated color grade, 35mm film grain, low-key lighting.",
    "atmosphere_en": "Eerie, quiet, suffocating atmosphere.",
    "negative_en": "bright daylight, cartoon, anime, extra fingers, deformed face, text, watermark, oversaturated"
  },
  "characters": [
    {
      "id": "lan", "name": "Lan", "role": "protagonist",
      "visual_en": "A Vietnamese woman in her early 20s, long straight black hair, pale oval face, wearing a faded white ao ba ba",
      "personality": "quiet, stubborn", "voice": "young female, soft, slightly trembling", "arc": "denial to acceptance"
    }
  ],
  "locations": [
    {
      "id": "old_house", "name": "Old house by the river", "int_ext": "INT",
      "description_en": "Old three-room wooden house in the Mekong Delta, dark ironwood pillars, ancestral altar in the center",
      "key_props": ["tarnished mirror", "ivory comb"],
      "lighting": "candles and an oil lamp, deep shadow in the corners",
      "sound_ambience": "river water, night insects, creaking wood",
      "scare_zones": ["dark corner behind the altar", "the mirror"]
    }
  ]
}
```

- `series.notes` holds what a genre file's "Bible additions" asks for.
- A genre may add one top-level block (horror adds `entity`, see `screen-adapter/references/genres/horror.md`).
- Narration videos keep a lean bible: `series` and `style_guide`, plus characters and locations only when the video shows recurring ones.

## screenplay.json

`03-script/screenplay.json`, the single source for both branches. `screenplay.txt` and the narration text are rendered from it by `scripts/screenplay.py render`; edit the JSON, never the renders.

```json
{
  "title": "The Comb in the Mirror",
  "scenes": [
    {
      "scene_id": 5,
      "title": "The mirror",
      "heading": { "int_ext": "INT", "location_id": "old_house", "sublocation": "Lan's room", "time": "NIGHT" },
      "beat": "Escalation",
      "tension": 7,
      "characters": ["lan"],
      "purpose": "Lan sees the figure in the mirror for the first time",
      "est_duration_sec": 45,
      "facts_to_verify": [],
      "elements": [
        { "type": "action", "text": "Lan brushes her hair at the mirror. The candle flame wavers." },
        { "type": "sound", "text": "A lullaby, very faint, from nowhere." },
        { "type": "dialogue", "character": "lan", "emotion": "trembling", "text": "Who's there?" },
        { "type": "action", "text": "In the mirror, behind Lan, a long-haired figure stands still." },
        { "type": "vo", "character": "lan", "text": "That night, I knew I was not alone." }
      ]
    }
  ]
}
```

- `elements` keeps the order things happen; `shot-list` points at them by 0-based index.
- Element types: `action` (what is seen), `sound`, `dialogue` (needs `character`), `vo` (`character` optional; none means the narrator).
- Film scenes need `heading`, `beat` and `tension`. Narration scenes (one per chapter) need `title`, may drop `heading`, and put each spoken paragraph in its own `vo` element and the visual intent in `action` elements.
- `facts_to_verify`: every number, name, date or quote the scene states as real fact, with its claimed value. Empty for invented stories.
