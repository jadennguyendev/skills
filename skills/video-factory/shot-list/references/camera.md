# Camera vocabulary

The only terms shot design may use. A genre file adds what each term does for that genre and its own sequence patterns.

## Shot size (`shot_size`, exact codes; `shots.py` checks them)

| Code | Name | Use |
|------|------|-----|
| `EWS` | Extreme wide shot | a small figure in a large place: isolation, scale |
| `WS` | Wide shot | establish the place; leave room in the frame |
| `MS` | Medium shot | action and body language |
| `MCU` | Medium close-up | dialogue and reactions |
| `CU` | Close-up | emotion on a face |
| `ECU` | Extreme close-up | a detail: eyes, a hand, a motif object |
| `INSERT` | Insert shot | an object on its own: the comb, the candle going out |

## Angle (`angle`)

| Term | Use |
|------|-----|
| eye level | neutral, real |
| low angle | the subject dominates |
| high angle | the subject looks small, weak |
| top-down / bird's eye | watched from above |
| Dutch angle | unease, a world off balance; use rarely |
| POV | through a character's eyes, or a watcher's |
| over-the-shoulder (OTS) | the viewer stands behind a character; good with mirrors and conversations |

## Camera move (`camera_move`)

| Term | Use |
|------|-----|
| static / locked-off | hold long; the viewer searches the frame |
| slow push in / slow dolly in | tension builds |
| slow pull out | reveals what surrounds the subject |
| pan | sweep a room; pan back and something has changed |
| tilt | reveal top to bottom or bottom to top |
| tracking | follow a character through a space |
| handheld | panic, chase; AI tools render it poorly, keep it rare |

## Lens (`lens`)

| Focal length | Effect |
|--------------|--------|
| 18-24mm wide | slight edge distortion, deep uneasy space |
| 35mm | natural, documentary feel |
| 50mm | close to the human eye |
| 85mm and longer | soft background, subject cut off from the world |

Add depth of field when it matters: "50mm, shallow depth of field".

## Composition and lighting (`composition`, `lighting`)

| Term | Use |
|------|-----|
| negative space | empty area in the frame the viewer watches |
| foreground obstruction | shoot through a door gap, curtain or bars: being watched |
| frame within frame | doorway, mirror, window |
| rule of thirds | balanced, everyday framing |
| low-key lighting | dark, high contrast |
| high-key lighting | bright, low contrast |
| motivated light | light from a visible source: candle, torch, lamp, window |
| under-lighting | lit from below |
| silhouette / backlight | shape without a face |

## Sequence patterns

- **Shot / reverse shot** - alternate over-the-shoulder shots of two speakers, same side of the line.
- **Establish, then close in** - WS of the place, MS of the action, CU of the reaction.
- **Look and reveal** - CU of a character looking, POV of what they see, CU of the reaction.
- **Insert for the motif** - an INSERT of the recurring object at each of its appearances, framed the same way.

## Prompt formula (built by `shots.py`, ai-gen only)

- Image: style prefix + shot size, angle, lens + characters (bible `visual_en`) with `subject_action` + location (`description_en`) + entity stage (`visual_en`) + `lighting` + `composition` + `framing_note` + atmosphere.
- Motion: `camera_move` + `motion_note`. The keyframe already holds the picture, so the motion prompt describes movement only: one camera move, one or two actions, slow words ("slowly", "subtle", "barely moving").
- Each tool (Kling, Runway, Veo...) has its own prompt habits; adapt the built prompt at generation time, never in the shot list.
