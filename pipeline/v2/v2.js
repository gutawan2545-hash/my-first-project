<script>
const CFG = __CFG__;
const ease = x => x <= 0 ? 0 : x >= 1 ? 1 : x * x * (3 - 2 * x);
const clamp = x => Math.max(0, Math.min(1, x));
const SW = {};
['blinkJ', 'blinkT', 'blinkC', 'mouthJ', 'mouthT'].forEach(c => { SW[c] = { els: [...document.querySelectorAll('.' + c)], on: null }; SW[c].els.forEach(e => e.setAttribute('display', 'none')); });
function setSw(c, on) { const w = SW[c]; if (w.on === on) return; w.on = on; w.els.forEach(e => e.setAttribute('display', on ? 'inline' : 'none')); }
const q = (svg, s) => svg.querySelector(s);
const ST = [...document.querySelectorAll('figure svg')].map((svg, i) => {
  const dust = [...svg.querySelectorAll('g[filter="url(#moteBlur)"] circle, g[filter="url(#moteGlow)"] circle')].map((c, k) => ({ c, k, x: +c.getAttribute('cx'), y: +c.getAttribute('cy'), o: +(c.getAttribute('opacity') || 1) }));
  const refs = ['#jbody', '#jbodyNH', '#jbodyS', '#jbodySNH', '#jbodySNHL', '#tbody', '#tbodyS', '#catSide', '#catSideAlert'];
  const bob = [];
  svg.querySelectorAll('use').forEach(u => {
    const h = u.getAttribute('href'); if (!refs.includes(h)) return;
    let t = u; let p = u.parentNode;
    while (p && p.getAttribute && !p.getAttribute('transform') && (p.classList.contains('lookA') || p.classList.contains('lookB'))) p = p.parentNode;
    if (p && p.getAttribute && p.getAttribute('transform') && !p.classList.contains('cam')) t = p;
    if (!bob.find(b => b.el === t)) bob.push({ el: t, base: t.getAttribute('transform') || '', ph: bob.length * 1.3 });
  });
  return {
    svg, cam: q(svg, '.cam'), blur: q(svg, `#zb${i} feGaussianBlur`), dust, bob, subs: [...svg.querySelectorAll('.sub')], info: q(svg, '.info'), wm: q(svg, '.wm'),
    glow: [...svg.querySelectorAll('[fill*="faceLight"],[fill*="scrGlow"],[fill*="coolPool"],[fill*="monBeam"]')].map(e => ({ el: e, o: +(e.getAttribute('opacity') || 1) })),
    paw: q(svg, 'g[transform="translate(540,560)"]')
  };
});
const DL = { head: document.querySelector('#deanLie .cathead'), eS: document.querySelector('#deanLie .eS'), eA: document.querySelector('#deanLie .eA') };
function blink(t, off, per) { return ((t + off) % per) < 0.13; }

window.showOnly = i => document.querySelectorAll('figure').forEach((f, k) => f.style.display = k == i ? '' : 'none');
window.setT = function (i, t, f) {
  const c = CFG[i], s = ST[i], svg = s.svg, d = c.dur;
  // camera: slow push, zoom-blur cuts, shake on twists
  let z = c.key === 'endcard' ? 1 : 1 + 0.025 * t / d, blur = 0, dx = 0, dy = 0;
  if (c.zb && t < 0.22) { const k = 1 - t / 0.22; z += 0.28 * k * k; blur = 9 * k; }
  if (c.zbNext && t > d - 0.16) { const k = (t - (d - 0.16)) / 0.16; z += 0.22 * k * k; blur = Math.max(blur, 8 * k); }
  if (c.shake != null) { const k = t - c.shake; if (k >= 0 && k < 0.7) { const a = 10 * Math.exp(-k * 5); dx = a * Math.sin(k * 71); dy = a * Math.cos(k * 53); } }
  s.cam.setAttribute('transform', `translate(${(270 + dx).toFixed(1)} ${(480 + dy).toFixed(1)}) scale(${z.toFixed(4)}) translate(-270 -480)`);
  s.blur.setAttribute('stdDeviation', blur.toFixed(2));
  // dust drifting up, swaying, twinkling
  for (const p of s.dust) {
    const k = p.k, ddx = 7 * Math.sin(t * 0.7 + k * 1.9) + ((k % 3) - 1) * 2.5 * t, ddy = -(5 + (k % 5) * 1.6) * t + 4 * Math.sin(t * 0.9 + k * 2.7);
    p.c.setAttribute('cx', (p.x + ddx).toFixed(1)); p.c.setAttribute('cy', (p.y + ddy).toFixed(1));
    const glint = Math.max(0, Math.sin(t * 1.3 + k * 4.1) - 0.93) * 9; p.c.setAttribute('opacity', Math.min(1, p.o * (0.55 + 0.45 * Math.sin(t * 2.2 + k * 2.3)) + glint * 0.5).toFixed(2));
  }
  for (const b of s.bob) { const y = 3 * Math.sin(t * 2 * Math.PI / 3.4 + b.ph); b.el.setAttribute('transform', `translate(0 ${y.toFixed(2)}) ${b.base}`); }
  for (const g of s.glow) g.el.setAttribute('opacity', (g.o * (0.9 + 0.1 * Math.sin(t * 11) * Math.sin(t * 2.7 + 1))).toFixed(3));
  if (s.paw) { const x = -14 * Math.max(0, Math.sin(t * 1.6)); s.paw.setAttribute('transform', `translate(${(540 + x).toFixed(1)},560)`); }
  // blink + lip flags from the voice track
  setSw('blinkJ', blink(t + i * 0.7, 0.4, 3.1)); setSw('blinkT', blink(t + i * 0.5, 1.5, 3.6)); setSw('blinkC', blink(t + i * 0.3, 2.2, 4.2));
  setSw('mouthJ', !!c.mJ[f]); setSw('mouthT', !!c.mT[f]);
  // subtitles by time window
  s.subs.forEach((g, j) => { const [a, b] = c.subs[j]; g.setAttribute('opacity', Math.min(clamp((t - a) / 0.12), clamp((b - t) / 0.12)).toFixed(2)); });
  if (s.info) s.info.setAttribute('opacity', clamp((t - 0.3) / 0.3));
  if (s.wm) s.wm.setAttribute('opacity', (0.85 * (c.card_in != null ? 1 - clamp((t - c.card_in) / 0.4) : 1)).toFixed(2));
  // per-shot moves
  const el = sel => q(svg, sel);
  if (c.key === 'headphones') {
    const a = t < 0.6 ? 0 : t < 1.3 ? -40 * ease((t - 0.6) / 0.7) : -40 - 55 * ease((t - 1.3) / 0.7);
    el('.hpgrp').setAttribute('transform', `rotate(${a.toFixed(2)} -57 64)`);
    const g = t < 0.15 ? 0.05 : 0.18 + 0.5 * Math.exp(-(t - 0.15) * 1.2);
    el('.phoneglow').setAttribute('opacity', g.toFixed(3));
  }
  if (c.key === 'scroll') {
    const k = ease((t - 0.4) / (c.stop - 0.4));
    el('.scrollList').setAttribute('transform', `translate(0 ${(-212 * k).toFixed(1)})`);
    el('.hl').setAttribute('opacity', clamp((t - c.stop) / 0.3).toFixed(2));
    const sw = t > 0.4 && t < c.stop ? -16 * Math.abs(Math.sin((t - 0.4) * 4)) : 0;
    el('.swipe').setAttribute('transform', `translate(0 ${sw.toFixed(1)})`);
  }
  if (c.key === 'read') el('.writeArm').setAttribute('transform', `rotate(${(3 * Math.sin(t * 9)).toFixed(2)} 20 140)`);
  if (c.key === 'write') {
    const dg = [...svg.querySelectorAll('.dg')];
    let tip = null;
    dg.forEach((e, k) => { const on = t > c.pens[k]; e.setAttribute('opacity', on ? 1 : 0); if (t > c.pens[k] - 0.2) tip = +e.getAttribute('x') + 12 + 10 * clamp((t - c.pens[k]) / 0.2); });
    if (tip == null) tip = 150;
    if (t > c.pens[9] + 0.35) tip = +dg[6].getAttribute('x') - 6;     // hand rests over the last four digits
    el('.penhand').setAttribute('transform', `translate(${tip.toFixed(1)} 478)`);
  }
  if (c.key === 'glance') {
    const look = t > 0.2; el('.lookA').setAttribute('display', look ? 'none' : 'inline'); el('.lookB').setAttribute('display', look ? 'inline' : 'none');
    const a = 40 * ease((t - c.hangup) / 0.25); el('.hangarm').setAttribute('transform', `rotate(${a.toFixed(1)} 50 70)`);
  }
  if (c.key === 'dean') {
    const k = ease((t - 0.06) / 0.28);
    DL.head.setAttribute('transform', `translate(66 ${(-30 - 9 * k).toFixed(1)}) rotate(${(-8 * k).toFixed(1)}) scale(0.95)`);
    const alert = t > 0.1; DL.eS.setAttribute('display', alert ? 'none' : 'inline'); DL.eA.setAttribute('display', alert ? 'inline' : 'none');
  } else if (DL.head) { DL.head.setAttribute('transform', 'translate(66 -30) scale(0.95)'); DL.eS.setAttribute('display', 'inline'); DL.eA.setAttribute('display', 'none'); }
  if (c.key === 'door' || c.key === 'ots') {
    const p = el('.pulse'); if (p) { const k = (t * 1.6) % 1; const cx = c.key === 'ots' ? 322 : 270, cy = c.key === 'ots' ? 400 : 430; p.setAttribute('transform', `translate(${cx} ${cy}) scale(${(1 + 0.25 * k).toFixed(3)}) translate(${-cx} ${-cy})`); p.setAttribute('opacity', (0.9 * (1 - k) + 0.1).toFixed(2)); }
    const u = el('.underlight'); if (u) u.setAttribute('opacity', (0.6 + 0.4 * Math.abs(Math.sin(t * 7))).toFixed(2));
  }
  if (c.key === 'dialpad') {
    const NUM = '0815923746', n = c.taps.filter(x => t >= x).length;
    const shown = NUM.slice(0, n).replace(/^(\d{3})(\d{0,3})(\d{0,4}).*/, (m, a, b, d) => [a, b, d].filter(Boolean).join(' '));
    const num = el('.num'); num.textContent = n < 3 ? NUM.slice(0, n) : shown;
    el('.caret').setAttribute('opacity', (Math.floor(t * 3) % 2) ? 1 : 0.2);
    const keys = [...svg.querySelectorAll('.key')];
    const pos = d => { const k = keys.find(e => e.dataset.d === d); const ci = k.querySelector('circle'); return [+ci.getAttribute('cx'), +ci.getAttribute('cy')]; };
    keys.forEach(k => k.querySelector('.flash').setAttribute('opacity', 0));
    let target = [300, 520];
    for (let i = 0; i < c.taps.length; i++) {
      if (t >= c.taps[i] - 0.12) target = pos(NUM[i]);
      if (t >= c.taps[i] && t < c.taps[i] + 0.12) keys.find(e => e.dataset.d === NUM[i]).querySelector('.flash').setAttribute('opacity', 0.7);
    }
    if (t >= c.call - 0.15) target = [270, 482];
    el('.callbtn').setAttribute('fill', (t >= c.call && t < c.call + 0.2) ? '#6be09a' : '#3cb46e');
    const press = (t % 0.17) < 0.06 ? 3 : 0;
    el('.tap').setAttribute('transform', `translate(${(target[0] - 288 + 6).toFixed(1)} ${(target[1] - 487 + 6 + press).toFixed(1)})`);
  }
  if (c.key === 'tawanlook') {
    const st = t < 0.3 ? 'A' : t < 0.55 ? 'B' : 'C';
    ['A', 'B', 'C'].forEach(x => el('.f' + x).setAttribute('display', x === st ? 'inline' : 'none'));
  }
  if (c.key === 'ots') {
    const turn = t > 0.55; el('.hA').setAttribute('display', turn ? 'none' : 'inline'); el('.hB').setAttribute('display', turn ? 'inline' : 'none');
    const k = ease((t - 1.2) / 1.1), dip = (t > 1.2 && t < 2.3) ? -6 * Math.sin(Math.PI * (t - 1.2) / 1.1) : 0;
    el('.jstep').setAttribute('transform', `translate(${(185 + 10 * k).toFixed(1)} ${(470 - 22 * k + dip).toFixed(1)}) scale(${(2.0 - 0.18 * k).toFixed(3)})`);
  }
  if (c.key === 'oldtone') {
    [...svg.querySelectorAll('.note')].forEach((n, k) => { if (!n.dataset.base) n.dataset.base = n.getAttribute('transform') || '';
      const y = -((t * 14 + k * 20) % 60); n.setAttribute('transform', `translate(0 ${y.toFixed(1)}) ${n.dataset.base}`); });
  }
  if (c.key === 'choice') {
    const k = ease(t / c.hand_stop), x = -40 * (1 - k);
    el('.reach').setAttribute('transform', `translate(${x.toFixed(1)} 0)`);
  }
  if (c.key === 'endcard') {
    const k = ease(t / 0.55), x = -70 * (1 - k), y = 90 * (1 - k);
    el('.reach').setAttribute('transform', `translate(${x.toFixed(1)} ${y.toFixed(1)})`);
    el('.q').setAttribute('opacity', clamp((t - c.card_in) / 0.25).toFixed(2));
    el('.logo').setAttribute('opacity', clamp((t - c.card_in - 0.35) / 0.35).toFixed(2));
    el('.logolid').setAttribute('display', (t > c.dur - 0.2) ? 'inline' : 'none');
  }
};
</script>
