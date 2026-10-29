#!/usr/bin/env python3
"""
Reframe a 16:9 film into a 9:16 Short (YouTube Shorts, TikTok, Reels): the full frame, or one crop per shot.

    python3 reframe.py plan.json

plan.json:
    {
      "src": "videos/<slug>/ch02/<slug>-ch02.mp4",   # a 16:9 render
      "srt": "videos/<slug>/ch02/<slug>-ch02.srt",   # optional: trimmed and shifted next to the output
      "out": "videos/<slug>/shorts/<name>.mp4",
      "start": 0, "end": 58.5,                       # source seconds; end defaults to the source's end
      "bridge": "videos/<slug>/shorts/series/out/part2-bridge.mp4",   # optional: 1080x1920, played before (its .srt beside it)
      "tail": "videos/<slug>/shorts/series/out/part2-tail.mp4",       # optional: 1080x1920, played after
      "label": "part 2/5 · the gas tank",           # optional: the series label at the top, over the intro only
      "shots": [                                     # optional (no shots: full); source seconds, each shot runs to the next one's t
        {"t": 0,    "x": 960, "w": 608},             # x: crop centre in source px, w: crop width (608..1920)
        {"t": 11.0, "x": 1100, "w": 760}
      ]
    }

Full (no "shots"): the whole 16:9 frame scales to a 1080x608 band across the middle of a black 1080x1920 frame.
Shots: each shot crops w x 1080 around x, scales it to 1080 wide and centres it on the black frame:
w=608 fills the frame, wider crops keep more of the picture as a band on the black stage. A contact
sheet of one frame per shot (in full, five across the chapter) is written next to the output for review. The chapter sinks to black over its last 0.3 s.
"""

import json
import re
import subprocess
from fractions import Fraction
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "script-writer/scripts"))   # the sibling skill
from assemble import cues, probe  # noqa: E402

W, H, SW, SH = 1080, 1920, 1920, 1080
MIN_W = round(SH * W / H)          # 608: the crop that fills the frame
FADE = 72                          # px: how far a band's edges sink into the black
LABEL_Y, LABEL_PX = 300, 40        # the series label's centre line and size; it shows only in the intro, over bare stage
LABEL_MAX = 8.0                    # s: the longest the label stays with no bridge (the intro, not the whole part)
LABEL_BOX = (180, 260, 900, 340)   # x0, y0, x1, y1 on the 1080x1920 frame that must be bare stage for it
DARK = 24                          # Y: brightest pixel still counted as bare stage (its lift, grain)
FONT = Path(__file__).resolve().parents[3] / "style/demo/fonts/DidactGothic-Regular.ttf"


def stamp(t: float) -> str:
    """SRT time.

    >>> stamp(61.25)
    '00:01:01,250'
    """
    ms = round(t * 1000)
    return f"{ms // 3600000:02}:{ms // 60000 % 60:02}:{ms // 1000 % 60:02},{ms % 1000:03}"


def windows(shots, start, end):
    """Clip each shot to [start, end): (t0, t1, x0, w) with the crop clamped inside the source.

    >>> windows([{"t": 0, "x": 100, "w": 608}, {"t": 5, "x": 1900, "w": 700}, {"t": 9, "x": 960, "w": 1920}], 2, 7)
    [(2, 5, 0, 608), (5, 7, 1220, 700)]
    """
    out = []
    for s, nxt in zip(shots, shots[1:] + [{"t": float("inf")}]):
        t0, t1 = max(s["t"], start), min(nxt["t"], end)
        if t1 <= t0:
            continue
        w = max(MIN_W, min(SW, int(s.get("w", MIN_W))))
        x0 = max(0, min(SW - w, round(s["x"] - w / 2)))
        out.append((t0, t1, x0, w))
    return out


def covered(src, t0, t1, x0, w) -> bool:
    """Whether anything is drawn under the label box during this shot (measured on the source, before the band's fade)."""
    k = W / w
    h = 2 * round(SH * k / 2)
    top = (H - h) // 2
    y0, y1 = max(LABEL_BOX[1], top), min(LABEL_BOX[3], top + h)
    if y1 <= y0:
        return False
    cx0, cx1, cy0, cy1 = (round(x0 + LABEL_BOX[0] / k), round(x0 + LABEL_BOX[2] / k), round((y0 - top) / k), round((y1 - top) / k))
    log = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-to", str(t1), "-i", str(src), "-vf",
                          f"crop={cx1 - cx0}:{max(2, cy1 - cy0)}:{cx0}:{cy0},signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=-",
                          "-f", "null", "-"], check=True, capture_output=True, text=True).stdout
    return max(map(float, re.findall(r"YMAX=([\d.]+)", log)), default=0) > DARK


def main() -> None:
    plan_path = Path(sys.argv[1])
    plan = json.loads(plan_path.read_text())
    src, out = Path(plan["src"]), Path(plan["out"])
    dur, streams = probe(src)
    v = next(s for s in streams if s["codec_type"] == "video")
    if (v["width"], v["height"]) != (SW, SH):
        sys.exit(f"{src}: expected {SW}x{SH}, got {v['width']}x{v['height']}")
    start, end = plan.get("start", 0), min(plan.get("end", dur), dur)
    shots = sorted(plan.get("shots") or [{"t": start, "x": SW / 2, "w": SW}], key=lambda s: s["t"])
    if not shots or shots[0]["t"] > start:
        sys.exit(f"the first shot must start at or before {start}")
    if end - start > 180:
        print(f"warning: {end - start:.1f} s is over YouTube Shorts' 3-minute limit", file=sys.stderr)
    win = windows(shots, start, end)

    parts = []
    for i, (t0, t1, x0, w) in enumerate(win):
        h = 2 * round(SH * W / w / 2)
        shot = f"[0:v]trim=start={t0}:end={t1},setpts=PTS-STARTPTS,crop={w}:{SH}:{x0}:0,scale={W}:{h}:flags=lanczos"
        if w > MIN_W:
            # a band on the black: its edges sink into the dark (STYLE.md §8) instead of cutting the drawing off hard
            shot += (f",format=gbrp[b{i}];color=white:s={W}x{h}:d=1,format=gray,"
                     f"geq=lum='255*clip(min(min(X\\,W-1-X)\\,min(Y\\,H-1-Y))/{FADE}\\,0\\,1)',format=gbrp,"
                     f"loop=loop=-1:size=1,trim=duration={t1 - t0}[m{i}];[b{i}][m{i}]blend=all_mode=multiply:shortest=1")
        parts.append(shot + f",format=yuv420p,pad={W}:{H}:0:(oh-ih)/2:black,setsar=1[s{i}]")
    d = end - start
    graph = ";".join(parts) + ";" + "".join(f"[s{i}]" for i in range(len(win))) + f"concat=n={len(win)}:v=1:a=0,fade=t=out:st={d - 0.3:.3f}:d=0.3"
    graph += f"[vo];[0:a]atrim=start={start}:end={end},asetpts=PTS-STARTPTS,afade=t=out:st={d - 0.3:.3f}:d=0.3[ao]"
    # the series pieces around the chapter: [bridge] chapter [tail]
    pieces = [Path(plan[k]) for k in ("bridge", "tail") if plan.get(k)]
    for i, p in enumerate(pieces, 1):
        graph += (f";[{i}:v]fps=24,format=yuv420p,setsar=1[pv{i}];"
                  f"[{i}:a]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[pa{i}]")
    graph += ";[ao]aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[ac]"
    seq = (["[pv1][pa1]"] if plan.get("bridge") else []) + ["[vo][ac]"] + ([f"[pv{len(pieces)}][pa{len(pieces)}]"] if plan.get("tail") else [])
    lead = probe(Path(plan["bridge"]))[0] if plan.get("bridge") else 0
    tail = probe(Path(plan["tail"]))[0] if plan.get("tail") else 0
    # re-encoding the AAC lifts its true peak a little: hold the samples at -1.6 dB so the part stays under STYLE.md's -1.2
    graph += ";" + "".join(seq) + f"concat=n={len(seq)}:v=1:a=1" + ("[vc][ac0]" if plan.get("label") else "[v][ac0]")
    graph += ";[ac0]alimiter=limit=0.83:level=false[a]" + (";[vc]" if plan.get("label") else "")
    if plan.get("label"):
        # only in the intro: over the bridge (it leaves the label's band bare), or with no bridge over the first shot when that
        # leaves it bare. On from the first frame, it sinks over 0.3 s with the intro, into black
        t0, t1, x0, w = win[0]
        end_ = lead if lead else (0 if covered(src, t0, t1, x0, w) else min(t1 - start, LABEL_MAX))
        alpha = f"between(t,0,{end_:.3f})*min(({end_:.3f}-t)/0.3,1)"
        text = plan["label"].replace("\\", "\\\\").replace("'", "\\'").replace(":", "\\:")
        graph += (f"drawtext=fontfile='{FONT}':text='{text}':fontsize={LABEL_PX}:fontcolor=0xbdbdbd:"
                  f"x=(w-text_w)/2:y={LABEL_Y}-text_h/2:alpha='{alpha}'[v]")
        print(f"label over 0-{end_:.1f} s")
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(src)] + sum((["-i", str(p)] for p in pieces), []) + ["-filter_complex", graph,
                    "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "18", "-preset", "slow",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)], check=True)

    if plan.get("srt"):
        kept, n = [], 0
        stamps = lambda timing: [sum(float(p) * m for p, m in zip(x.replace(",", ".").split(":"), (3600, 60, 1))) for x in timing.split(" --> ")]
        for timing, text in cues(Path(plan["bridge"]).with_suffix(".srt")) if plan.get("bridge") else []:
            a, b = stamps(timing)
            n += 1
            kept.append(f"{n}\n{stamp(a)} --> {stamp(min(b, lead))}\n" + "\n".join(text) + "\n")
        for timing, text in cues(Path(plan["srt"])):
            a, b = stamps(timing)
            if b <= start or a >= end:
                continue
            n += 1
            kept.append(f"{n}\n{stamp(lead + max(a, start) - start)} --> {stamp(lead + min(b, end) - start)}\n" + "\n".join(text) + "\n")
        out.with_suffix(".srt").write_text("\n".join(kept), encoding="utf-8")

    # one frame from the middle of each shot (in full, five across the chapter), and of the bridge and the tail, side by side
    sheet = out.with_name(out.stem + "-sheet.jpg")
    body = [(t0 + t1) / 2 for t0, t1, _, _ in win] if plan.get("shots") else [start + d * (i + 0.5) / 5 for i in range(5)]
    mids = ([lead / 2] if lead else []) + [lead + m - start for m in body] + ([lead + d + tail / 2] if tail else [])
    sel = "+".join(f"eq(n\\,{round(m * Fraction(v['r_frame_rate']))})" for m in mids)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(out), "-vf",
                    f"select='{sel}',scale=270:480,tile={len(mids)}x1:padding=8:color=0x404040", "-frames:v", "1",
                    "-fps_mode", "vfr", str(sheet)], check=True)
    print(f"{out} ({lead + d + tail:.1f} s: {lead:.1f} s bridge, {f'{len(win)} shots' if plan.get('shots') else 'full frame'}, {tail:.1f} s tail)")
    print(sheet)


if __name__ == "__main__":
    main()
