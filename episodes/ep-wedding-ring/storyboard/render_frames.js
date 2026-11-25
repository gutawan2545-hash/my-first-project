// เรนเดอร์ทุกเฟรมใน storyboard.html เป็น frames/NN.jpg (540x960)
// รัน: node render_frames.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(__dirname, 'storyboard_svg.html'));
  await p.waitForTimeout(1500);
  const n = await p.$$eval('figure svg', els => { els.forEach(e => { e.style.width = '540px'; e.style.height = '960px'; e.style.borderRadius = '0'; e.style.boxShadow = 'none'; }); return els.length; });
  const svgs = await p.$$('figure svg');
  for (let i = 0; i < svgs.length; i++) {
    const num = await svgs[i].evaluate(e => e.getAttribute('aria-label').replace(/\D/g, ''));
    await svgs[i].scrollIntoViewIfNeeded();
    await svgs[i].screenshot({ path: path.join(__dirname, 'frames', String(num).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 82 });
  }
  console.log('frames', n);
  await b.close();
})();
