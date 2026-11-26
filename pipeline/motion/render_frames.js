// Frame-exact renderer for Odd Hours motion pages.
// usage: node render_frames.js <page.html> <out_dir> <seconds> [fps=24] [scale=2]
// The page must mount its scene into window.S and set window.READY; this script calls OM.seek(t, S) per frame.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [page, outDir, secs, fps = 24, scale = 2] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: +scale });
  await p.goto('file://' + require('path').resolve(page));
  await p.waitForFunction('window.READY === true');
  await p.waitForTimeout(800);                                   // fonts
  const el = await p.$('svg[data-scene]');
  const n = Math.round(+secs * +fps);
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => OM.seek(t, window.S), f / +fps);
    await el.screenshot({ path: `${outDir}/f${String(f).padStart(5, '0')}.png` });
  }
  await b.close();
  console.log('frames', n);
})();
