#!/usr/bin/env python3
"""
Build videos/<slug>/index.html: one self-contained, read-only page with a tab per document
that exists, and a language switch where a review copy (review_language, e.g. *.vi.md) sits beside the original.
Open it straight from disk (file://); rerun after every stage.

    python3 view.py videos/<slug>
"""

import html
import json
import re
import sys
from pathlib import Path

# (tab, original, review copy); the original's extension picks the renderer.
TABS = [
    ("Story", "01-story/story.md", "01-story/story.{rl}.md"),
    ("Story bible", "01-story/story-bible.md", "01-story/story-bible.{rl}.md"),
    ("Story review", "01-story/review.md", None),
    ("Analysis", "02-adaptation/analysis.json", None),
    ("Beats", "02-adaptation/beats.json", "02-adaptation/adaptation.{rl}.md"),
    ("Bible", "02-adaptation/bible.json", None),
    ("Screenplay", "03-script/screenplay.txt", "03-script/screenplay.{rl}.txt"),
    ("Narration", "03-script/script.{lang}.md", "03-script/script.{rl}.md"),
    ("Script review", "03-script/review.md", None),
    ("Shot list", "04-shots/shotlist.json", None),
    ("Shot review", "04-shots/review.md", None),
    ("Config", "config.json", None),
]

esc = html.escape


def inline(text):
    """
    >>> inline('a **b** *c* `d` <e>')
    'a <strong>b</strong> <em>c</em> <code>d</code> &lt;e&gt;'
    """
    t = esc(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    return re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", t)


def markdown(src):
    """Headings, paragraphs, lists, pipe tables, rules and inline marks: what the pipeline writes.

    >>> markdown('# T\\n\\nOne\\ntwo\\n\\n- a\\n- b\\n\\n| x | y |\\n|---|---|\\n| 1 | 2 |')
    '<h1>T</h1>\\n<p>One two</p>\\n<ul><li>a</li><li>b</li></ul>\\n<table><tr><th>x</th><th>y</th></tr><tr><td>1</td><td>2</td></tr></table>'
    """
    out, para, items, rows = [], [], [], []

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{inline(i)}</li>" for i in items) + "</ul>")
        if rows:
            head, *body = [r for r in rows if not re.fullmatch(r"[\s|:-]+", r)]
            out.append(f"<table><tr>{cells(head, 'th')}</tr>" + "".join(f"<tr>{cells(r, 'td')}</tr>" for r in body) + "</table>")
        para.clear()
        items.clear()
        rows.clear()

    def cells(row, tag):
        return "".join(f"<{tag}>{inline(c.strip())}</{tag}>" for c in row.strip().strip("|").split("|"))

    for line in src.splitlines():
        s = line.strip()
        if m := re.match(r"(#{1,6})\s+(.*)", s):
            flush()
            out.append(f"<h{len(m[1])}>{inline(m[2])}</h{len(m[1])}>")
        elif s.startswith("|"):
            if para:
                flush()
            rows.append(s)
        elif re.match(r"[-*]\s+", s):
            if para or rows:
                flush()
            items.append(s[2:].strip())
        elif re.fullmatch(r"-{3,}|\*{3,}", s) or not s:
            flush()
            if s:
                out.append("<hr>")
        else:
            if items or rows:
                flush()
            para.append(s)
    flush()
    return "\n".join(out)


def data(value):
    """Any JSON as nested HTML: objects as definition lists, lists of objects as tables.

    >>> data([{"age": 22, "id": "lan"}, {"age": 30, "id": "mai"}])
    '<div class="scroll"><table><tr><th>id</th><th>age</th></tr><tr><td>lan</td><td>22</td></tr><tr><td>mai</td><td>30</td></tr></table></div>'
    """
    if isinstance(value, dict):
        return "<dl>" + "".join(f"<dt>{esc(str(k))}</dt><dd>{data(v)}</dd>" for k, v in value.items()) + "</dl>"
    if isinstance(value, list):
        if value and all(isinstance(v, dict) for v in value):
            keys = sorted(dict.fromkeys(k for v in value for k in v), key=column_rank)
            head = "".join(f"<th>{esc(k)}</th>" for k in keys)
            body = "".join("<tr>" + "".join(cell(v.get(k, "")) for k in keys) + "</tr>" for v in value)
            return f'<div class="scroll"><table><tr>{head}</tr>{body}</table></div>'
        if all(not isinstance(v, (dict, list)) for v in value):
            return ", ".join(esc(str(v)) for v in value)
        return "<ol>" + "".join(f"<li>{data(v)}</li>" for v in value) + "</ol>"
    return esc("" if value is None else str(value))


def column_rank(key):
    """Ids lead a table: id, name, shot_id, scene_id, then other *_id keys, then the rest in order.

    >>> sorted(["purpose", "location_id", "scene_id", "shot_id"], key=column_rank)
    ['shot_id', 'scene_id', 'location_id', 'purpose']
    """
    lead = ["id", "name", "shot_id", "scene_id"]
    return lead.index(key) if key in lead else len(lead) if key.endswith("_id") else len(lead) + 1


def cell(value):
    long = isinstance(value, str) and len(value) > 60
    return f'<td class="long">{data(value)}</td>' if long else f"<td>{data(value)}</td>"


def body(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        obj = json.loads(text)
        if isinstance(obj, dict) and len(obj) == 1:  # {"shots": [...]}: show the list itself
            obj = next(iter(obj.values()))
        return f'<div class="data">{data(obj)}</div>'
    if path.suffix == ".md":
        return f'<article>{markdown(text)}</article>'
    return f"<pre>{esc(text)}</pre>"


def build(video: Path):
    config = json.loads((video / "config.json").read_text(encoding="utf-8"))
    lang, rl = config.get("language", "en"), config.get("review_language", "")
    tabs, panels = [], []
    for n, (name, orig, review) in enumerate(TABS):
        orig = video / orig.format(lang=lang)
        if not orig.exists():
            continue
        review = video / review.format(rl=rl) if review and rl else None
        has_vi = bool(review and review.exists())
        tabs.append(f'<button role="tab" data-tab="t{n}">{esc(name)}</button>')
        inner = f'<div class="en">{body(orig)}</div>'
        if has_vi:
            inner += f'<div class="vi">{body(review)}</div>'
        panels.append(f'<section id="t{n}" class="{"has-vi" if has_vi else ""}" hidden>'
                      f'<p class="src">{esc(str(orig.relative_to(video)))}</p>{inner}</section>')
    title = esc(config.get("title", video.name))
    switch = f'<button class="lang" type="button">{esc(lang.upper())} / {esc(rl.upper())}</button>' if "has-vi" in "".join(panels) else ""
    return PAGE.format(title=title, switch=switch, tabs="".join(tabs), panels="".join(panels))


PAGE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
:root {{ --bg:#faf9f6; --fg:#1d1d1b; --muted:#6b6a65; --line:#e3e1da; --accent:#8a3b12; --panel:#ffffff; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#141413; --fg:#ecebe6; --muted:#a09e96; --line:#2f2e2b; --accent:#e0915f; --panel:#1c1c1a; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg); font:16px/1.6 -apple-system, "Segoe UI", system-ui, sans-serif; }}
header {{ position:sticky; top:0; background:var(--bg); border-bottom:1px solid var(--line); padding:12px 16px 0; z-index:1; }}
h1.title {{ font-size:18px; margin:0 0 8px; display:flex; justify-content:space-between; align-items:center; gap:12px; }}
nav {{ display:flex; gap:4px; overflow-x:auto; }}
nav button, .lang {{ font:inherit; font-size:14px; border:0; background:none; color:var(--muted); padding:8px 10px; cursor:pointer; white-space:nowrap; border-bottom:2px solid transparent; }}
nav button[aria-selected=true] {{ color:var(--fg); border-bottom-color:var(--accent); }}
.lang {{ border:1px solid var(--line); border-radius:6px; padding:4px 10px; }}
main {{ max-width:1100px; margin:0 auto; padding:16px; }}
section {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; padding:16px 20px; min-width:0; }}
.src {{ color:var(--muted); font-size:13px; margin:0 0 12px; font-family:ui-monospace, Menlo, monospace; }}
article {{ max-width:70ch; }}
pre {{ font:14px/1.5 "Courier Prime", "Courier New", ui-monospace, monospace; white-space:pre; overflow-x:auto; margin:0; }}
table {{ border-collapse:collapse; font-size:14px; margin:8px 0; }}
th, td {{ border:1px solid var(--line); padding:6px 8px; text-align:left; vertical-align:top; }}
th {{ color:var(--muted); font-weight:600; }}
dl {{ margin:0; display:grid; grid-template-columns:minmax(120px, max-content) 1fr; gap:4px 16px; }}
dt {{ color:var(--muted); }} dd {{ margin:0; }}
.data {{ font-size:14px; }} .data td dl {{ grid-template-columns:max-content 1fr; gap:2px 8px; }}
.data th {{ white-space:nowrap; }} .data td.long {{ min-width:44ch; }}
.scroll {{ overflow-x:auto; max-width:100%; }} dd {{ min-width:0; }}
code {{ font-family:ui-monospace, Menlo, monospace; font-size:.9em; }}
.vi, body.show-vi .has-vi .en {{ display:none; }}
body.show-vi .has-vi .vi {{ display:block; }}
</style></head>
<body>
<header><h1 class="title"><span>{title}</span>{switch}</h1><nav role="tablist">{tabs}</nav></header>
<main>{panels}</main>
<script>
const tabs = [...document.querySelectorAll('nav button')];
const show = id => {{
  tabs.forEach(b => b.setAttribute('aria-selected', b.dataset.tab === id));
  document.querySelectorAll('main section').forEach(s => s.hidden = s.id !== id);
}};
tabs.forEach(b => b.onclick = () => show(b.dataset.tab));
if (tabs.length) show(tabs[0].dataset.tab);
document.querySelector('.lang')?.addEventListener('click', () => document.body.classList.toggle('show-vi'));
</script>
</body></html>
"""


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    video = Path(argv[1])
    out = video / "index.html"
    out.write_text(build(video), encoding="utf-8")
    print(f"open file://{out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
