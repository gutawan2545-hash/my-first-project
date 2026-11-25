// renders every shot frame by frame: node render.js [first] [last] [fpsOverride] [maxFrames]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const shots = JSON.parse(fs.readFileSync(path.join(__dirname, 'shots.json'), 'utf8'));
const FPS = +(process.argv[4] || 24), A = +(process.argv[2] || 1), B = +(process.argv[3] || shots.length), MAX = +(process.argv[5] || 1e9);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'page.html')); await p.waitForTimeout(1500);
  for (const s of shots.filter(s => s.n >= A && s.n <= B)) {
    const dir = path.join(__dirname, 'frames', 's' + String(s.n).padStart(2, '0')); fs.mkdirSync(dir, { recursive: true });
    await p.evaluate(([svg, spec]) => load(svg, spec), [s.svg, { move: s.move }]);
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(150);
    const N = Math.min(MAX, Math.round(s.dur * FPS)); const t0 = Date.now();
    const el = await p.$('#f');
    for (let i = 0; i < N; i++) {
      await p.evaluate(([t, d]) => setT(t, d), [i / FPS, s.dur]);
      await el.screenshot({ path: path.join(dir, String(i).padStart(5, '0') + '.jpg'), type: 'jpeg', quality: 90 });
    }
    console.log('shot', s.n, N, 'frames', ((Date.now() - t0) / N).toFixed(0), 'ms/frame');
  }
  await b.close();
})();
