// Render anim_rosa.html frame by frame (24 fps, 1080x1920) into frames_rosa/, then encode with ffmpeg (see makeclip_rosa.sh).
// Usage: node anim_render_rosa.js            -> all frames
//        node anim_render_rosa.js 2.5 5 11   -> stills at those seconds (check_*.png) for review
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const here = __dirname;
  const out = path.join(here, 'frames_rosa');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(here, 'anim_rosa.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(800);
  const stage = await p.$('#stage');
  const args = process.argv.slice(2).map(Number);
  if (args.length) {
    for (const t of args) { await p.evaluate(t => setTime(t), t); await stage.screenshot({ path: path.join(here, `check_${t}.png`) }); }
  } else {
    fs.mkdirSync(out, { recursive: true });
    const dur = await p.evaluate(() => window.DURATION), fps = 24, n = Math.round(dur * fps);
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => setTime(t), i / fps);
      await stage.screenshot({ path: path.join(out, String(i).padStart(4, '0') + '.png') });
      if (i % 48 === 0) console.log(`frame ${i}/${n}`);
    }
  }
  await b.close();
})();
