// เรนเดอร์ฉากหลังนิ่งจาก bg.html เป็น bg/NAME.jpg ความละเอียด 3 เท่า (1620x2880) เผื่อซูมกล้อง
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 560, height: 980 }, deviceScaleFactor: 3 });
  await p.goto('file://' + path.join(__dirname, process.env.PAGE || 'bg.html'));
  await p.waitForTimeout(2000);
  for (const e of await p.$$('body > svg[id]')) {
    const id = await e.getAttribute('id');
    await e.scrollIntoViewIfNeeded();
    await e.screenshot({ path: path.join(__dirname, process.env.BGDIR || 'bg', id + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await b.close();
  console.log('bg done');
})();
