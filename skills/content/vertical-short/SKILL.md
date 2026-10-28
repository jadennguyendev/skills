---
name: vertical-short
description: Turn a 16:9 Trainer Kai film into 9:16 vertical Shorts for YouTube Shorts, TikTok or Reels (a long video becomes a series of parts, one per chapter), either the full frame on black (default) or one crop per shot, with trimmed captions. Use when the user asks for a Short, a TikTok, a Reel, a vertical or 9:16 version, or to "cut the YouTube video for TikTok".
---

# Vertical Short

Reframes a 16:9 Manga Ink on Black film to 1080x1920 with `reframe.py`, in one of two modes:

- **full** (the default, whenever the user asks for nothing else): the whole 16:9 frame, scaled to a 1080x608 band across the middle of the black 9:16 frame, its edges fading into the dark. Nothing is cut and nothing is planned shot by shot, but text shrinks to 56% (a 54 px card becomes 30 px).
- **shots** (only when the user asks for it: "crop it", "fill the screen", bigger text): every shot gets its own crop. A single centre crop (what `ffmpeg-skill`'s `fit.py --fit crop` does) throws away 70% of the width and cuts off word cards and labels that sit beside Kai, so each shot is fitted on its own; a shot that needs more width becomes a band on black.

## 1. Pick the source and the range

- A long video becomes a series of parts, never one long Short: one part per chapter (`part1` from ch01 … `part5` from ch05), each its own Short from that chapter's film. The sponsor slot is never a part.
- Source: the chapter's 16:9 render, `videos/<slug>/chNN/<slug>-chNN.mp4`, or in shots mode its `?short` render (§2).
- Range (`start`, `end`): a part opens on its chapter's hook and ends on a payoff, never mid-sentence. It may drop the chapter's last lines when they only hand off to the next chapter, or keep them when that question makes the next part's hook. Cut on phrase boundaries from the chapter's `.srt`. YouTube Shorts takes up to 3 minutes; 30-60 s works best.

## 2. Write the plan

The plan lives in `videos/<slug>/shorts/partN-<name>.json` (tracked; its renders are ignored). In full mode it has no `shots`:

```json
{
  "src": "videos/<slug>/ch02/<slug>-ch02.mp4",
  "srt": "videos/<slug>/ch02/<slug>-ch02.srt",
  "out": "videos/<slug>/shorts/part2-<name>.mp4",
  "page": "videos/<slug>/ch02",
  "start": 0, "end": 58.5
}
```

That is the whole plan for full mode; go on to §3. Shots mode adds one crop per shot:

```json
{
  "src": "videos/<slug>/ch02/out/short-src.mp4",
  "srt": "videos/<slug>/ch02/<slug>-ch02.srt",
  "out": "videos/<slug>/shorts/part2-<name>.mp4",
  "page": "videos/<slug>/ch02",
  "q": "short=1",
  "start": 0, "end": 58.5,
  "shots": [
    {"t": 0,    "x": 960,  "w": 608},
    {"t": 11.0, "x": 1100, "w": 760}
  ]
}
```

- One entry per shot, `t` in source seconds (from the chapter's `TREATMENT.md` shot table or its `index.html` `SHOTS`). Change crop only where the film changes shot, through black: a crop change inside a shot reads as a jump cut and breaks STYLE.md's transitions.
- `x` is the crop centre in source pixels, `w` the crop width. `w: 608` fills the phone screen (Kai standing, a centred card). Widen only as far as the shot needs to keep everything that matters: Kai plus a label beside him, a chart, a fibre bundle with its label. Text shrinks by `1080 / w`; keep labels at 36 px or more on the 1080-wide frame (a 54 px card holds to `w` about 1600, a 42 px label to about 1260).
- When a shot can't keep its text at 36 px (a 16:9 layout with Kai on the left third and the cards far right leaves a wide black gap), don't shrink the text: give the chapter page a `?short` layout (`new URLSearchParams(location.search).has('short')`) that pulls the cards toward Kai, narrows charts and floors text at 38 px, and render it as the plan's `src` with a `short` mode in the chapter's `build.sh` (`video.mjs --q short=1`, muxed with the film's own `mix.wav`, readcheck with the same query). The film itself is unchanged. Reference: `videos/the-gas-tank/ch02/` and `shorts/part2-recovery-test.json`.
- `page` and `q` are the chapter page and query that made `src`, for `safe.mjs` (§4).
- Fit each shot from measurements, not by guessing: the horizontal extent of everything drawn in the shot (the source frames' pixels brighter than the stage) and the text boxes from `window.TEXTS`. Map the span [L, R] that must stay onto [76, 955] of the 1080-wide frame: `k = 879 / (R - L)`, `w = 1080 / k`, `x = L - 76 / k + w / 2`. Lines (a chart's axis, a floor) and Kai's far arm may run into the fade; text may not. Reference: `videos/the-gas-tank/ch02/` and `shorts/part2-recovery-test.json`.

## 3. Tie the parts into a series

A viewer who lands on part 3 has seen neither part 1 nor part 2, so each part says where it sits and what came before:

- **The label**: `"label": "part N/M · <video>"` in the plan. `reframe.py` draws it (Didact Gothic 40 px, grey, centred at y 300) in the intro only, never through the whole part: over the bridge, or in part 1 over the first shot (at most 8 s; in full mode the first 8 s) when it leaves the label's band (y 260-340) bare (it measures the source there). It sinks with the intro, into black.
- **The bridge** (parts 2…M): `"bridge"`, a 1080x1920 clip played before the chapter. Kai on black recalls the part before in one line that is also a hook: "Part N." then one sentence on what the last part found, then the question this part answers ("Part three. Most people credit Khabib's gas tank to the mountains. Look where he really trained."), with a keyword card on its word. Every term it names is on a card; it explains whatever the chapter's opening takes for granted ("the session I promised"). About 6-8 s; the channel's voice rules apply.
- **The tail** (parts 1…M-1): `"tail"`, 3 s after the chapter sinks to black: Kai opens a hand to the card `next · part N+1`.
- Both are drawn by one Opuscar page per video, `videos/<slug>/shorts/series/` (`?part=N` the bridge, `?part=N&tail=1` the tail; reference: `videos/the-gas-tank/shorts/series/`), rendered with `sh videos/<slug>/shorts/series/build.sh` into its `out/`: `partN-bridge.mp4` with its `.srt` (`reframe.py` puts its cues first), `partN-tail.mp4`. Its `mix.py` masters a bridge to -14 LUFS and a tail's lone piano chord to about -24 (the chapters' piano under the voice), with no loudness pass in the mux, so the part plays at one level. A bridge keeps the label's band bare.

## 4. Render and check

```bash
python3 .claude/skills/vertical-short/reframe.py videos/<slug>/shorts/partN-<name>.json
```

It writes `partN-<name>.mp4` (1080x1920, H.264, AAC: bridge, chapter sinking to black over its last 0.3 s, tail), `partN-<name>.srt` (the cues in range, shifted to 0) and `partN-<name>-sheet.jpg` (one frame from the middle of each shot; in full mode five across the chapter). Then:

- `node .claude/skills/vertical-short/safe.mjs <plan>.json` maps every piece of the page's `window.TEXTS` through its shot's crop and must print `clean`: no text under 36 px, under the right-side buttons (x over 960 from y 768 down), in the bottom 20% (TikTok's caption and Shorts' title cover it) or in a band's fade. In full mode it flags most text as under 36 px: that is the mode's price, not a defect to fix in the plan. Tell the user how small the smallest text gets and offer shots mode for that part; the other flags (fade, buttons, bottom) still need fixing.
- Read the sheet (the bridge, the chapter's frames, the tail): in every frame Kai and the highlighted muscle are whole and readable, and the label (in the intro) never touches the picture.
- Measure the part: about -14 LUFS and a true peak at -1.2 dB or under (`ffmpeg -i <part>.mp4 -af ebur128=peak=true -f null -`).
- Look at one full-size frame of every banded shot: the band's edges fade into the black, no line stops at a hard edge.
- In shots mode, fix the plan and re-run until all of these hold.

## 5. Upload notes

For TikTok and Reels, upload `partN-<name>.mp4` and use the platform's own auto-captions or upload `partN-<name>.srt` where supported (YouTube Shorts takes it as CC). Title and description follow the channel's `publish.md` rules; a Short gets its own short title, never a copy of the long video's. Each part goes in the video's `publish.md` under "Shorts": its bridge line, its title, the description (the honesty line; "Part N of M" with the long video's title; the sources for its claims; `#shorts`), how to rebuild it, and the long video as its related video. Post the parts in order, a day or two apart.
