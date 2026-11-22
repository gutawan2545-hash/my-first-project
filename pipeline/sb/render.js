// Renders each storyboard shot as two 1080x1920 PNG layers:
//   frames/bNN.png  picture only (no subtitles, no graphics)
//   frames/oNN.png  subtitles + graphics on a transparent background
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  fs.mkdirSync('frames', { recursive: true });
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 700, height: 1100 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/storyboard3.html');
  await p.waitForTimeout(800);
  await p.addStyleTag({ content: `
    figure svg{width:540px!important;height:960px!important;border-radius:0!important;box-shadow:none!important}
    .grid{grid-template-columns:540px!important}
    .guide{display:none!important}
    body.base .info, body.base .subs{display:none!important}
    body.over, body.over html{background:transparent!important}
    body.over figure svg > *{visibility:hidden}
    body.over figure svg > .info, body.over figure svg > .subs{visibility:visible}
  ` });
  await p.evaluate(() => { document.documentElement.style.background = 'transparent'; });
  const n = (await p.$$('figure svg')).length;
  for (const mode of ['base', 'over']) {
    await p.evaluate(m => { document.body.className = m; }, mode);
    await p.waitForTimeout(200);
    const svgs = await p.$$('figure svg');
    for (let i = 0; i < n; i++) {
      const name = `frames/${mode[0]}${String(i + 1).padStart(2, '0')}.png`;
      await svgs[i].screenshot({ path: name, omitBackground: mode === 'over' });
    }
  }
  await b.close();
  console.log('rendered', n);
})();
