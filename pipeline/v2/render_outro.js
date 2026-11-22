// Renders the logo outro: ofr/NNNN.jpg (1080x1920), 2.6 s at 24 fps
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  fs.mkdirSync('ofr', { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/outro.html');
  await p.waitForTimeout(500);
  const svg = await p.$('svg');
  const n = Math.round(2.6 * 24);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => window.setT(t), f / 24);
    await svg.screenshot({ path: `ofr/${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 92 });
  }
  await b.close();
  console.log('outro frames', n);
})();
