// เรนเดอร์ทุกเฟรมจาก storyboard_svg.html ที่ 1080x1920 ลง clip/hd/NN.jpg และการ์ด A/B ลง clip/hd/card_A.jpg, card_B.jpg
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, '..', 'storyboard', process.env.SRC || 'storyboard_svg.html'));
  await p.waitForTimeout(1500);
  await p.addStyleTag({ content: '.grid{display:block!important} figure{display:block!important;width:540px!important;margin:0 0 20px!important} figcaption{display:none!important}' });
  await p.$$eval('figure svg', els => els.forEach(e => { e.style.width = '540px'; e.style.height = '960px'; e.style.borderRadius = '0'; e.style.boxShadow = 'none'; }));
  const svgs = await p.$$('figure svg');
  for (const s of svgs) {
    const num = await s.evaluate(e => e.getAttribute('aria-label').replace(/\D/g, ''));
    await s.scrollIntoViewIfNeeded();
    await s.screenshot({ path: path.join(__dirname, process.env.OUTDIR || 'hd', String(num).padStart(2, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  const c = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  for (const sel of ['A', 'B']) {
    await c.goto('file://' + path.join(__dirname, 'card_' + sel + '.html'));
    await c.waitForTimeout(600);
    await c.screenshot({ path: path.join(__dirname, 'hd', 'card_' + sel + '.jpg'), type: 'jpeg', quality: 92 });
  }
  console.log('hd frames', svgs.length);
  await b.close();
})();
