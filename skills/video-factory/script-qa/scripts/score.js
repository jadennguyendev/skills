#!/usr/bin/env node
// Deterministic layer of script-qa: runs the vendored avoid-ai-writing detector on a narration script.
// Usage: node score.js <script.en.md>  -> JSON on stdout; exit 0 pass, 1 fail, 2 error.
const fs = require('fs');
const path = require('path');

// Narration allows these; script-qa judges them by hand against narration-profile.md.
// title-case-header: video and chapter titles are headings, never spoken.
const NARRATION_ALLOWED = ['rhetorical-question', 'lets-construction', 'title-case-header'];
// Same as the upstream gate default, calibrated on written prose.
// ponytail: recalibrate once ~10 real narration scripts have been scored.
const MAX_FLAGGED = 6;

function score(text, AIDetector) {
  const result = AIDetector.analyzeText(text, { contextMode: 'general', sourceMode: 'rendered-markdown' });
  if (result.tooLong || result.unsupportedScript) return { error: result.tooLong ? 'over 10,000 words' : 'unsupported script (English only)' };
  const flagged = result.issues.filter((i) => !NARRATION_ALLOWED.includes(i.type));
  const critical = flagged.filter((i) => i.severity === 'critical').length;
  return {
    score: result.score,
    label: result.label,
    words: result.stats.wordCount,
    findings: result.issues.length,
    critical,
    flagged: flagged.map(({ type, severity, text }) => ({ type, severity, text })),
    allowed: result.issues.filter((i) => NARRATION_ALLOWED.includes(i.type)).map(({ type, text }) => ({ type, text })),
    pass: critical === 0 && flagged.length <= MAX_FLAGGED,
  };
}

function loadDetector() {
  const p = path.join(__dirname, '..', '..', 'avoid-ai-writing', 'detector', 'patterns.js');
  if (!fs.existsSync(p)) throw new Error(`detector not found at ${p} - install the avoid-ai-writing skill next to script-qa`);
  return require(p);
}

if (require.main === module) {
  try {
    const file = process.argv[2];
    if (!file) throw new Error('usage: node score.js <script.en.md>');
    const out = score(fs.readFileSync(file, 'utf8'), loadDetector());
    if (out.error) throw new Error(out.error);
    process.stdout.write(JSON.stringify(out, null, 2) + '\n');
    process.exit(out.pass ? 0 : 1);
  } catch (e) {
    process.stderr.write(`score.js: ${e.message}\n`);
    process.exit(2);
  }
}

module.exports = { score, loadDetector };
