const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1240, height: 900 } });
  await p.goto('file://' + process.cwd() + '/storyboard3.html');
  await p.waitForTimeout(400);
  const f = await p.$$('figure svg');
  await f[6].screenshot({ path: 'z7.png' });
  await b.close();
})();
