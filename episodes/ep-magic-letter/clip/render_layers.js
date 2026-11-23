// เรนเดอร์ทุกช็อตจาก storyboard.html เป็น 2 ชั้น ขนาด 1080x1920
//   frames/bNN.png  ภาพอย่างเดียว (ซ่อนกราฟิก data-ui)
//   frames/oNN.png  ซับ ป้าย กล่องคำอธิบาย ตัวหนังสือเอฟเฟกต์ บนพื้นโปร่งใส
//   frames/vK.png   การ์ดโหวต 4 แบบ (ไฮไลต์ A B C D) จาก vote.html
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(__dirname, 'frames');
const CSS = `
  .frame svg{width:540px!important;height:960px!important;border-radius:0!important;box-shadow:none!important}
  .grid{grid-template-columns:540px!important}
  figcaption,h1,.note{display:none!important}
  body.base [data-ui]{display:none!important}
  body.over, html.over{background:transparent!important}
  body.over .frame svg g[clip-path] > *:not([data-ui]){visibility:hidden!important}
`;
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(ROOT, 'storyboard.html'));
  await p.waitForTimeout(900);
  await p.addStyleTag({ content: CSS });
  const n = (await p.$$('.frame svg')).length;
  for (const mode of ['base', 'over']) {
    await p.evaluate(m => { document.body.className = m; document.documentElement.className = m;
      if (m === 'over') { document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent'; } }, mode);
    await p.waitForTimeout(250);
    const svgs = await p.$$('.frame svg');
    for (let i = 0; i < n; i++) {
      await svgs[i].screenshot({ path: path.join(OUT, `${mode[0]}${String(i + 1).padStart(2, '0')}.png`), omitBackground: mode === 'over' });
    }
  }
  const v = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 2 });
  await v.goto('file://' + path.join(ROOT, 'vote.html'));
  await v.waitForTimeout(700);
  await v.addStyleTag({ content: CSS });
  const vs = await v.$$('.frame svg');
  for (let i = 0; i < vs.length; i++) await vs[i].screenshot({ path: path.join(OUT, `v${i}.png`) });
  const st = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 2 });
  await st.goto('file://' + path.join(ROOT, 'steps.html'));
  await st.waitForTimeout(600);
  await st.addStyleTag({ content: CSS + 'html,body{background:transparent!important}' });
  await st.evaluate(() => { document.documentElement.style.background = 'transparent'; document.body.style.background = 'transparent'; });
  const ss = await st.$$('.frame svg');
  for (let i = 0; i < ss.length; i++) await ss[i].screenshot({ path: path.join(OUT, `step${i + 1}.png`), omitBackground: true });
  await b.close();
  console.log('rendered', n, 'shots +', vs.length, 'vote frames +', ss.length, 'step cards');
})();
