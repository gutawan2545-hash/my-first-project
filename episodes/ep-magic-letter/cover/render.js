// เรนเดอร์ cover.html -> cover.png (1080x1920) · เตือนถ้าชื่อเรื่องหรือป้ายเกินขอบขวา
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'cover.html'));
  await p.waitForFunction(() => document.body.dataset.ready === '1', null, { timeout: 15000 });
  const over = await p.evaluate(() => document.body.dataset.overflow || '');
  if (over) console.log('WARNING: overflows right margin:', over);
  await (await p.$('#cover')).screenshot({ path: path.join(__dirname, 'cover.png') });
  await b.close();
  console.log('cover.png');
})();
