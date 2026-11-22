// Renders every frame of every shot in order: fr/NNNNN.jpg (1080x1920)
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const frames = JSON.parse(fs.readFileSync('frames.json'));
  fs.mkdirSync('fr', { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 }, deviceScaleFactor: 2 });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + process.cwd() + '/v2.html');
  await p.waitForTimeout(1500);
  let n = 0;
  for (let i = 0; i < frames.length; i++) {
    await p.evaluate(k => window.showOnly(k), i);
    const svg = await p.$(`figure[data-i="${i}"] svg`);
    for (let f = 0; f < frames[i]; f++) {
      await p.evaluate(([k, tt, ff]) => window.setT(k, tt, ff), [i, f / 24, f]);
      await svg.screenshot({ path: `fr/${String(n).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 90 });
      n++;
    }
    console.log('shot', i + 1, 'done', n);
  }
  await b.close();
})();
