// Render anim_ep1.html segment by segment (24 fps, 1080x1920), piping JPEG frames straight into ffmpeg (no frames on disk).
// Usage: node anim_render_ep1.js                 -> all segments, 4 parallel workers -> segments/seg_###.mp4
//        node anim_render_ep1.js only 3 4 5      -> just those segment indexes
//        node anim_render_ep1.js check 3:1.5 10:4 -> stills check_<seg>_<t>.png for review
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const here = __dirname, outDir = path.join(here, 'segments');
const TL = JSON.parse(fs.readFileSync(path.join(here, 'ep1_timeline.json'), 'utf8'));
const FPS = 24;

async function openPage(b) {
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(here, 'anim_ep1.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(1000);
  return p;
}

async function renderSeg(p, si) {
  const seg = TL.segments[si];
  const out = path.join(outDir, `seg_${String(si).padStart(3, '0')}.mp4`);
  if (fs.existsSync(out)) return;
  const tmp = out + '.part.mp4';
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'veryfast', '-r', String(FPS), tmp], { stdio: ['pipe', 'inherit', 'inherit'] });
  const done = new Promise(r => ff.on('close', r));
  const n = Math.round(seg.dur * FPS);
  for (let i = 0; i < n; i++) {
    await p.evaluate(([si, t]) => render(si, t), [si, i / FPS]);
    const buf = await p.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await done;
  fs.renameSync(tmp, out);
}

(async () => {
  const args = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch();
  if (args[0] === 'check') {
    const p = await openPage(b);
    for (const a of args.slice(1)) {
      const [si, t] = a.split(':').map(Number);
      await p.evaluate(([si, t]) => render(si, t), [si, t]);
      await p.screenshot({ path: path.join(here, `check_${si}_${t}.png`) });
    }
    await b.close(); return;
  }
  let todo = args[0] === 'only' ? args.slice(1).map(Number) : TL.segments.map((s, i) => i);
  todo = todo.filter(i => TL.segments[i].type === 'html');
  // longest first so the workers finish together
  todo.sort((a, b2) => TL.segments[b2].dur - TL.segments[a].dur);
  const W = Math.min(4, todo.length);
  let k = 0, finished = 0;
  const t0 = Date.now();
  await Promise.all([...Array(W)].map(async () => {
    const p = await openPage(b);
    while (k < todo.length) {
      const si = todo[k++];
      await renderSeg(p, si);
      finished++;
      console.log(`seg ${si} done (${finished}/${todo.length}) ${((Date.now() - t0) / 60000).toFixed(1)} min`);
    }
  }));
  await b.close();
})();
