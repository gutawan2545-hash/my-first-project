// Renders cover.html to ../out/cover.png at 1080x1920
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  fs.mkdirSync('../out', { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  const [src = 'cover.html', dst = '../out/cover.png'] = process.argv.slice(2);
  await p.goto('file://' + process.cwd() + '/' + src);
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 15000 });
  const over = await p.evaluate(() => document.body.dataset.overflow || '');
  if (over) console.log('WARNING: title overflows right margin:', over);
  await (await p.$('#cover')).screenshot({ path: dst });
  const fam = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family + ' ' + f.weight).join(', '));
  console.log('fonts:', fam || 'fallback');
  await b.close();
})();
