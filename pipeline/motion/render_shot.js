// Render a range of global frames from one shot page (Odd Hours clip pages share one clock).
// usage: node render_shot.js <page.html> <out_dir> <f0> <f1> [fps=24] [scale=2] [step=1]
// Frames are written as f<global index>.png so shots tile into one sequence.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [page, outDir, f0, f1, fps = 24, scale = 2, step = 1] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: +scale });
  p.on('pageerror', e => console.error('PAGE ERROR', page, e.message));
  await p.goto('file://' + path.resolve(page));
  await p.waitForFunction('window.READY === true', null, { timeout: 60000 });
  await p.waitForTimeout(300);
  const el = await p.$('svg[data-scene]');
  for (let f = +f0; f < +f1; f += +step) {
    const ext = process.env.OM_EXT || 'png';
    const out = `${outDir}/f${String(f).padStart(5, '0')}.${ext}`;
    if (fs.existsSync(out)) continue;
    await p.evaluate(t => OM.seek(t, window.S), f / +fps);
    await el.screenshot(ext === 'jpg' ? { path: out, type: 'jpeg', quality: 93 } : { path: out });
  }
  await b.close();
})();
