// เรนเดอร์ซับแต่ละช่วงจาก subs.html เป็น PNG พื้นโปร่งใส 1080x1920 ลง subs/
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'subs.html'));
  await p.waitForTimeout(1500);
  const els = await p.$$('svg');
  for (const e of els) {
    const id = await e.getAttribute('id');
    await e.scrollIntoViewIfNeeded();
    await e.screenshot({ path: path.join(__dirname, 'subs', id + '.png'), omitBackground: true });
  }
  console.log('subs', els.length);
  await b.close();
})();
