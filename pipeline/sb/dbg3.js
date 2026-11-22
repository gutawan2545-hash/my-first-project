const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 } });
  await p.goto('file://' + process.cwd() + '/anim.html');
  await p.waitForTimeout(800);
  await p.addStyleTag({content:'body{padding:0!important}header{display:none!important}.grid{display:block!important}figure svg{width:540px!important;height:960px!important}'});
  await p.evaluate(() => { window.showOnly(5); });
  const svg = await p.$('figure[data-i="5"] svg');
  // t where Tawan blinks (offset 1.5, period 3.6 -> t=2.1) and talks
  for (const t of [1.0, 2.15]) { await p.evaluate(tt => window.setT(5, tt), t); await svg.screenshot({ path: 'dbg_' + t + '.png' }); }
  await b.close();
})();
