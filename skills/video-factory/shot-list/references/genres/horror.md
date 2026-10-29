# Horror

Adds to `../camera.md`: what the vocabulary does for fear, and the classic scare sequences.

## Horror uses of the vocabulary

- `WS` leaves room for the entity in the background; `ECU` and `INSERT` carry the motifs (the comb, the candle going out).
- `low angle` makes the entity overwhelming; `top-down` feels like something on the ceiling is watching; `POV` can be the entity stalking.
- `static` held long makes the viewer search the frame; `slow push in` is the genre's workhorse move; `pan` away and back, and something has changed; `tilt` up from the feet reveals the entity.
- 85mm and longer: something can hide in the blur behind the subject.
- `negative space` is where the viewer expects something to appear; `frame within frame` (doorway, mirror, window) is where the entity appears; `low-key` is the default; `under-lighting` makes a face uncanny.

## Scare sequences

1. **Slow reveal** - WS of the place, MCU of the character, POV into the dark corner, CU of the reaction, the same POV again, now with the shadow in it.
2. **Look away, look back** - the character sees an empty doorway, turns to something else, turns back: someone stands in the doorway. Each shot is a still frame, so AI tools handle it well.
3. **Background reveal** - one wide, static, long shot. The character in the foreground knows nothing; the viewer sees a figure behind them. No music sting.
4. **False scare, real scare** - tension, a cat jumps out, relief, then the entity right after.
5. **Stalker POV** - from behind bushes or a door gap, slow movement, watching a character who does not know, with foreground obstruction.

## Entity in shots

- `entity_stage` comes from the bible's `stage_by_beat` for the scene's beat; an earlier stage is fine (holding back), a later one is a finding.
- The entity "stays still" or "barely moves" in `motion_note`: stillness frightens more and breaks less in generated video than fast motion.
- The viewer sees the entity before the character does: let the character turn and find nothing.

## Example: scene 5 in five shots

| Shot | Size / angle | Move | Content | Duration |
|------|--------------|------|---------|----------|
| 5A | WS, eye level | static | dark room, Lan at the mirror, one candle | 6 s |
| 5B | INSERT | static | her hand brushing with the ivory comb | 4 s |
| 5C | MCU, over-the-shoulder | slow dolly in | the mirror, a faint figure behind her | 5 s |
| 5D | CU, eye level | static | her face freezes, trembling: "Who's there?" | 4 s |
| 5E | MS, from behind Lan | slow pan | she turns: nothing behind her | 6 s |

Look-back combined with frame within frame: the viewer sees the figure first, then watches Lan turn and see nothing.
