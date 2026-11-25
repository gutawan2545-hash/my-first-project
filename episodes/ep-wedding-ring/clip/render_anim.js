// เรนเดอร์ anim_test.html ทีละเฟรม (1080x1920) ส่งต่อให้ ffmpeg รวมกับเสียงเป็น out/test_anim.mp4
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
(async () => {
  const tl = JSON.parse(fs.readFileSync(path.join(__dirname, 'out', process.env.TL || 'test_timeline.json')));
  const n = Math.floor(tl.total * tl.fps);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, process.env.PAGE || 'anim_test.html'));
  await p.waitForTimeout(2500);
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(tl.fps), '-i', '-', '-i', path.join(__dirname, 'out', process.env.WAV || 'test_audio.wav'),
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', path.join(__dirname, 'out', process.env.OUT || 'test_anim.mp4')]);
  const stage = await p.$('#stage');
  for (let f = 0; f < n; f++) {
    await p.evaluate(t => window.renderAt(t), f / tl.fps);
    const buf = await stage.screenshot({ type: 'jpeg', quality: 90 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 120 === 0) console.log('frame', f, '/', n);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
  console.log('done');
})();
