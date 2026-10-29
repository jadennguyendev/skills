#!/usr/bin/env python3
"""
Join chapter films into one video.

    python3 assemble.py out.mp4 ch01/ch01.mp4 ch02/ch02.mp4 ...

Each chapter's .srt (same name, next to its .mp4) is merged into out.srt with shifted timings,
and YouTube chapter timestamps are printed. Chapters are stream-copied, so they must share
codec, size, fps and pixel format - render every chapter with the same style and settings.
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TS = re.compile(r"(\d+):(\d\d):(\d\d),(\d{3})")


def shift(timing: str, offset: float) -> str:
    """Shift an SRT timing line by offset seconds.

    >>> shift("00:00:01,500 --> 00:00:03,000", 61.25)
    '00:01:02,750 --> 00:01:04,250'
    """
    def move(m):
        h, mi, s, ms = map(int, m.groups())
        t = (h * 3600 + mi * 60 + s) * 1000 + ms + round(offset * 1000)
        return f"{t // 3600000:02}:{t // 60000 % 60:02}:{t // 1000 % 60:02},{t % 1000:03}"
    return TS.sub(move, timing)


def cues(srt: Path):
    """Yield (timing line, text lines) for each cue."""
    for block in re.split(r"\n\s*\n", srt.read_text(encoding="utf-8-sig").strip()):
        lines = block.splitlines()
        i = next(i for i, line in enumerate(lines) if "-->" in line)
        yield lines[i], lines[i + 1:]


def probe(mp4: Path):
    """Duration in seconds, plus the stream parameters that must match for stream copy."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-of", "json", "-show_entries",
         "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels",
         str(mp4)],
        check=True, capture_output=True, text=True).stdout
    data = json.loads(out)
    streams = [{k: v for k, v in s.items() if k not in ("index", "disposition", "tags")} for s in data["streams"]]
    return float(data["format"]["duration"]), streams


def clock(seconds: float) -> str:
    m, s = divmod(int(seconds), 60)
    return f"{m // 60}:{m % 60:02}:{s:02}" if m >= 60 else f"{m}:{s:02}"


def main() -> None:
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    out, chapters = Path(sys.argv[1]), [Path(p) for p in sys.argv[2:]]
    missing = [str(c) for c in chapters if not c.is_file()]
    if missing:
        sys.exit(f"Chapter files not found: {', '.join(missing)}")
    info = [probe(c) for c in chapters]
    mismatched = [str(c) for c, (_, streams) in zip(chapters, info) if streams != info[0][1]]
    if mismatched:
        sys.exit(f"Streams differ from {chapters[0]}: {', '.join(mismatched)}. "
                 "Re-render those chapters with the same style, size and fps.")

    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as listing:
        for c in chapters:
            listing.write("file '" + str(c.resolve()).replace("'", r"'\''") + "'\n")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listing.name,
                    "-c", "copy", "-movflags", "+faststart", str(out)], check=True)
    Path(listing.name).unlink()

    srt, offset, n = [], 0.0, 0
    print("YouTube chapters:")
    for c, (duration, _) in zip(chapters, info):
        print(f"{clock(offset)} {c.parent.name if c.parent.name else c.stem}")
        if c.with_suffix(".srt").exists():
            for timing, text in cues(c.with_suffix(".srt")):
                n += 1
                srt.append(f"{n}\n{shift(timing, offset)}\n" + "\n".join(text) + "\n")
        offset += duration
    if srt:
        out.with_suffix(".srt").write_text("\n".join(srt), encoding="utf-8")
    print(f"\n{out} ({clock(offset)})" + (f" + {out.with_suffix('.srt')}" if srt else ""))


if __name__ == "__main__":
    main()
