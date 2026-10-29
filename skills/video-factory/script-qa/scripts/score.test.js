// Run: node --test skills/video-factory/script-qa/scripts/score.test.js
const test = require('node:test');
const assert = require('node:assert');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const CLEAN = `# Why Printing Money Doesn't Make Anyone Richer

## ch01 - The billion-dollar question

If the government printed a billion dollars for every person tomorrow, would you be richer? For about a week, maybe. You would pay off the car and book the flight you keep putting off.

Then the baker raises the price of bread. So does the landlord, and so does everyone else who noticed that their customers suddenly have a billion dollars each.

To see why, we need an island with ten people and ten loaves of bread.
`;

const SLOP = `# The Future of Money

## ch01 - Intro

Let's dive in! In today's fast-paced world, money is a testament to human ingenuity. This game-changer has fundamentally transformed the landscape of our economy, and experts say it plays a pivotal role in shaping our future.

Moreover, it is crucial to delve into the intricate tapestry of monetary policy. Furthermore, this seamless ecosystem fosters robust growth.

I hope this helps! Trust me, you'll want to save this for later.
`;

function run(text) {
  const file = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'score-')), 'script.en.md');
  fs.writeFileSync(file, text);
  try {
    return { code: 0, out: JSON.parse(execFileSync('node', [path.join(__dirname, 'score.js'), file])) };
  } catch (e) {
    return { code: e.status, out: e.stdout.length ? JSON.parse(e.stdout) : null };
  }
}

test('clean narration passes', () => {
  const { code, out } = run(CLEAN);
  assert.strictEqual(code, 0);
  assert.strictEqual(out.pass, true);
});

test('AI-heavy narration fails with critical findings', () => {
  const { code, out } = run(SLOP);
  assert.strictEqual(code, 1);
  assert.ok(out.critical > 0);
});

test('narration-allowed types do not block', () => {
  const { out } = run(CLEAN.replace('To see why,', "So why does this happen? Let's take a look. To see why,"));
  assert.ok(out.allowed.length > 0);
  assert.ok(out.flagged.every((i) => !['rhetorical-question', 'lets-construction'].includes(i.type)));
});
