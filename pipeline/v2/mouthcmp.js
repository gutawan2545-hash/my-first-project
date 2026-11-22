const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 }, deviceScaleFactor: 2 });
  for (const v of ['A', 'B']) {
    await p.goto('file://' + process.cwd() + `/v2_mouth${v}.html`); await p.waitForTimeout(800);
    for (const [i, t, f] of [[3, 1.5, 0], [10, 0.4, 1]]) {
      await p.evaluate(([k, tt, ff]) => { window.showOnly(k); window.setT(k, tt, 0); if (ff) { document.querySelectorAll('.mouthJ').forEach(e => e.setAttribute('display', 'inline')); } }, [i, t, f]);
      const svg = await p.$(`figure[data-i="${i}"] svg`);
      await svg.screenshot({ path: `m${v}_${i}.png` });
    }
  }
  await b.close();
})();
