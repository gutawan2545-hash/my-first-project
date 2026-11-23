// เรนเดอร์ anim/anim.html ทีละเฟรม -> anim/fr/sNN/0000.jpg (1080x1920) · ข้ามช็อตสุดท้าย (การ์ดโหวตใช้ภาพจาก render_layers.js)
// ใช้: node render_anim.js [ช็อตที่ต้องการ เช่น 2,4]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'anim', 'anim.html'));
  await p.waitForTimeout(900);
  const frames = await p.evaluate(() => window.FRAMES);
  for (let n = 1; n < frames.length; n++) {
    if (only && !only.includes(n)) continue;
    const dir = path.join(__dirname, 'anim', 'fr', `s${String(n).padStart(2, '0')}`);
    fs.mkdirSync(dir, { recursive: true });
    for (let f = 0; f < frames[n - 1]; f++) {
      await p.evaluate(([n, f]) => window.setShot(n, f), [n, f]);
      await p.screenshot({ path: path.join(dir, `${String(f).padStart(4, '0')}.jpg`), type: 'jpeg', quality: 90, clip: { x: 0, y: 0, width: 540, height: 960 } });
    }
    console.log('shot', n, frames[n - 1], 'frames');
  }
  await b.close();
})();
