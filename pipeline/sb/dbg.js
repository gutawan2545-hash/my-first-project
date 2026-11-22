const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 }, deviceScaleFactor: 1 });
  await p.goto('file://' + process.cwd() + '/anim.html');
  await p.waitForTimeout(800); await p.addStyleTag({content:'body{padding:0!important}header{display:none!important}.grid{display:block!important}figure svg{width:540px!important;height:960px!important}'});
  const r = await p.evaluate(() => {
    window.showOnly(5);
    const out = { mouthT: document.querySelectorAll('.mouthT').length, blinkT: document.querySelectorAll('.blinkT').length, blinkJ: document.querySelectorAll('.blinkJ').length };
    document.body.classList.add('mT', 'bT');
    const m = document.querySelector('.mouthT');
    out.disp = getComputedStyle(m).display;
    return out;
  });
  console.log(JSON.stringify(r));
  const svg = await p.$('figure[data-i="5"] svg');
  await svg.screenshot({ path: 'dbg.png' });
  await b.close();
})();
