// Renders every animated shot frame by frame: aframes/sNN/fFFFF.jpg (1080x1920)
// usage: node anim_render.js [fps] [shotIndex|all] [maxSeconds]
const { chromium } = require('playwright');
const fs = require('fs');
const FPS = +(process.argv[2] || 24);
const ONLY = process.argv[3] || 'all';
const MAXS = +(process.argv[4] || 0);
(async () => {
  const durs = JSON.parse(fs.readFileSync('anim.json'));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 600, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto('file://' + process.cwd() + '/anim.html');
  await p.waitForTimeout(1000);
  await p.addStyleTag({ content: `body{padding:0!important}.wrap{max-width:none!important}header{display:none!important}
    .grid{display:block!important}figure svg{width:540px!important;height:960px!important;border-radius:0!important;box-shadow:none!important}` });
  const shots = ONLY === 'all' ? durs.map((_, i) => i) : [+ONLY];
  for (const i of shots) {
    await p.evaluate(k => window.showOnly(k), i);
    const dir = `aframes/s${String(i + 1).padStart(2, '0')}`;
    fs.mkdirSync(dir, { recursive: true });
    const svg = await p.$(`figure[data-i="${i}"] svg`);
    const n = Math.round((MAXS || durs[i]) * FPS);
    for (let f = 0; f < n; f++) {
      await p.evaluate(([k, t]) => window.setT(k, t), [i, f / FPS]);
      await svg.screenshot({ path: `${dir}/f${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 90 });
    }
    console.log('shot', i + 1, n, 'frames');
  }
  await b.close();
})();
