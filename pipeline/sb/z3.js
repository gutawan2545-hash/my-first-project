const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1240, height: 900 } });
  await p.goto('file://' + process.cwd() + '/storyboard3.html');
  await p.waitForTimeout(400);
  const f = await p.$$('figure svg');
  for (const i of [5, 7, 10]) await f[i].screenshot({ path: 'zz' + (i + 1) + '.png' });
  await b.close();
})();
