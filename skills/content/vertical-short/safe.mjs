// Text safety of a Short: node safe.mjs <plan.json>   (run from the repo root; needs the plan's "page", optionally "q")
// Maps every piece of the chapter page's window.TEXTS through its shot's crop, the way reframe.py places it, and flags text that is
// under 36 px, under the right-side buttons (x over 960 from y 768 down), in the bottom 20% (y over 1536), or inside a band's fade.
// Exit 0 clean, 1 flags, 2 can't check. LIB defaults to ~/lemo-opuscar.
import fs from 'fs'; import os from 'os'; import path from 'path';
const LIB = process.env.LIB || path.join(os.homedir(), 'lemo-opuscar');
const { openDemo, closeServer } = await import(path.join(LIB, 'core/render/page.mjs'));
const plan = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
if (!plan.page) { console.error('the plan needs "page": the chapter folder whose index.html made "src"'); process.exit(2); }
const W = 1080, H = 1920, SW = 1920, SH = 1080, MIN_W = 608, FADE = 72;
const shots = [...(plan.shots ?? [{ t: 0, x: SW / 2, w: SW }])].sort((a, b) => a.t - b.t);   // no shots: full
const crop = t => {
  const s = shots.filter(s => s.t <= t).pop(), w = Math.max(MIN_W, Math.min(SW, Math.trunc(s.w ?? MIN_W)));
  const x0 = Math.max(0, Math.min(SW - w, Math.round(s.x - w / 2))), h = 2 * Math.round(SH * W / w / 2);
  return { w, x0, k: W / w, h, top: Math.floor((H - h) / 2) };
};
const { browser, page } = await openDemo(path.resolve(plan.page), { w: SW, h: SH, q: plan.q || '' });
const boxes = await page.evaluate(([a, b]) => {
  if (typeof window.TEXTS !== 'function') return null;
  const out = [];
  for (let t = a; t < b; t += 0.1) for (const r of window.TEXTS(t) || []) out.push({ t, ...r });
  return out;
}, [plan.start ?? 0, plan.end ?? 1e9]);
await browser.close(); closeServer();
if (!boxes) { console.error('the page has no window.TEXTS'); process.exit(2); }
const seen = new Map(); let min = Infinity;
for (const b of boxes) {
  const c = crop(b.t), X0 = (b.x0 - c.x0) * c.k, X1 = (b.x1 - c.x0) * c.k, Y0 = c.top + b.y0 * c.k, Y1 = c.top + b.y1 * c.k, px = (b.y1 - b.y0) / 1.2 * c.k;
  const band = c.w > MIN_W, f = [];
  if (px < 36 - 0.05) f.push(`${px.toFixed(1)} px`);
  if (X1 > 960 && Y1 > 768) f.push('under the buttons');
  if (Y1 > 1536) f.push('bottom 20%');
  if (X0 < 0 || X1 > W) f.push('cut off');
  else if (band && (X0 < FADE || X1 > W - FADE || Y0 < c.top + FADE || Y1 > c.top + c.h - FADE)) f.push('in the fade');
  min = Math.min(min, px);
  const key = b.text + '|' + f.join(',');
  if (f.length && !seen.has(key)) seen.set(key, `${b.t.toFixed(1).padStart(6)}s  ${JSON.stringify(b.text).slice(0, 30).padEnd(30)} x ${X0.toFixed(0)}-${X1.toFixed(0)} y ${Y0.toFixed(0)}-${Y1.toFixed(0)}  ${f.join(', ')}`);
}
for (const l of seen.values()) console.log(l);
console.log(`${seen.size ? 'FLAGS ' + seen.size : 'clean'}: ${boxes.length} text samples, smallest ${min.toFixed(1)} px`);
process.exit(seen.size ? 1 : 0);
