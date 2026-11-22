// Re-renders only the given shots into fr/ at their original frame numbers. usage: node render_tail.js 11 12
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const frames = JSON.parse(fs.readFileSync('frames.json'));
  const shots = process.argv.slice(2).map(Number);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + process.cwd() + '/v2.html');
  await p.waitForTimeout(1500);
  for (const i of shots) {
    let n = frames.slice(0, i).reduce((a, b) => a + b, 0);
    await p.evaluate(k => window.showOnly(k), i);
    const svg = await p.$(`figure[data-i="${i}"] svg`);
    for (let f = 0; f < frames[i]; f++) {
      await p.evaluate(([k, tt, ff]) => window.setT(k, tt, ff), [i, f / 24, f]);
      await svg.screenshot({ path: `fr/${String(n).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 90 });
      n++;
    }
    console.log('re-rendered shot', i + 1);
  }
  await b.close();
})();
