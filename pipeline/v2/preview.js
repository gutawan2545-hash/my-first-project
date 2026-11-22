// One test frame per shot at a telling moment -> pv/NN.png ; usage: node preview.js [t-overrides json]
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const frames = JSON.parse(fs.readFileSync('frames.json'));
  const pick = JSON.parse(process.argv[2] || '{}');
  fs.mkdirSync('pv', { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 } });
  p.on('pageerror', e => console.log('PAGE ERROR', e.message));
  await p.goto('file://' + process.cwd() + '/v2.html');
  await p.waitForTimeout(1500);
  for (let i = 0; i < frames.length; i++) {
    const dur = frames[i] / 24;
    const t = pick[i] != null ? pick[i] : dur * 0.7;
    await p.evaluate(([k, tt]) => { window.showOnly(k); window.setT(k, tt, Math.floor(tt * 24)); }, [i, t]);
    const svg = await p.$(`figure[data-i="${i}"] svg`);
    await svg.screenshot({ path: `pv/${String(i + 1).padStart(2, '0')}.png` });
  }
  await b.close();
})();
