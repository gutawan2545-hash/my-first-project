// เรนเดอร์ poster.html เป็น ../final/cover_ep2.png ขนาด 1080x1920
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'poster.html'));
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 15000 }); await p.waitForTimeout(500);
  await (await p.$('#cover')).screenshot({ path: process.env.OUT || path.join(__dirname, '..', 'final', 'cover_ep2.png') });
  await b.close();
})();
