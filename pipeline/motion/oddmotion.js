/* Odd Hours motion engine (reusable for every episode).
 *
 * Deterministic: every element's state is a pure function of time t, so the same code plays live in a
 * browser (OM.play) and renders frame-exact video (OM.seek(t) per frame from Playwright).
 *
 * Elements opt in with data attributes (emitted by pipeline/motion/omkit.py):
 *   data-in="fade|fade-up|fade-left|fade-right|mask-right|mask-left|mask-up|grow|pop|draw|lines|words|count|arrow"
 *   data-at (s)  data-dur (s)  data-out="fade|fade-down|mask-left|mask-right|draw-back|shrink"  data-out-at  data-out-dur
 *   data-stagger (s, for lines/words)  data-count-to, data-count-from, data-count-fmt (e.g. "{n} ฿")
 *   data-cam="s0,s1,dx,dy"   slow push / pan over the whole scene      data-par="k" parallax factor for a layer
 *   data-float="amp,period"  idle bob     data-breath="amp,period"  character breathing (inner transform group)
 * Classes picked up for micro animation: .om-dust (drift + twinkle) .om-beam (soft flicker) .om-cloud (slow drift)
 *   .om-wave (swell) .om-caps (whitecaps slide) .om-spray (burst pulse)
 * Joints (articulated limbs): <g data-rot="px,py" data-k="t,deg;t,deg;..." data-sway="amp,period,phase"> rotates about the pivot;
 *   nest an elbow group inside a shoulder group so the forearm follows the upper arm (shoulder -> elbow -> hand).
 * Moves: data-mv="t,x,y;t,x,y" keyframed translation (walk in / out of frame) with data-bob="amp" step bob while moving.
 * Zoom blur transition: data-zb="t0,dur,in|out,blurId" on a wrapper group (blurId = feGaussianBlur element id).
 * Lip sync: talk entries may be [t0,t1,key] with window.OM_ENV[key] = loudness 0..1 at 50 fps (from the voice file).
 * Faces: OM.face(svg, id, {talk:[[t0,t1],...], glance:[[t,dx,dy],...], blinkEvery, seed})
 *   expects defs groups  #id-iL #id-iR (irises)  #id-bl (closed lids, display none)  #id-m1 #id-m2 (open mouths)
 *   <use> clones follow their source, so state is set on the source groups (display attribute, not CSS).
 */
(function () {
  // ---------------------------------------------------------------- easing (cubic-bezier, solved numerically)
  function bezier(x1, y1, x2, y2) {
    const cx = 3 * x1, bx = 3 * (x2 - x1) - cx, ax = 1 - cx - bx;
    const cy = 3 * y1, by = 3 * (y2 - y1) - cy, ay = 1 - cy - by;
    const fx = t => ((ax * t + bx) * t + cx) * t, fy = t => ((ay * t + by) * t + cy) * t;
    const dx = t => (3 * ax * t + 2 * bx) * t + cx;
    return x => {
      if (x <= 0) return 0; if (x >= 1) return 1;
      let t = x;
      for (let i = 0; i < 6; i++) { const d = dx(t); if (Math.abs(d) < 1e-6) break; t -= (fx(t) - x) / d; }
      return fy(Math.min(1, Math.max(0, t)));
    };
  }
  const E = {
    inOut: bezier(.65, 0, .35, 1),         // default, presentation feel
    out: bezier(.16, 1, .3, 1),            // entrances: fast start, long settle
    in: bezier(.7, 0, .84, 0),             // exits
    soft: bezier(.4, 0, .2, 1),
    back: bezier(.34, 1.36, .64, 1),       // gentle overshoot (pop), never a bounce
  };
  const clamp = v => Math.max(0, Math.min(1, v));
  const prog = (t, at, dur) => clamp((t - at) / Math.max(dur, 1e-6));
  const rnd = seed => { let s = seed >>> 0 || 1; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); };

  function keyed(keys, t, n) {                      // keys: [[t, v1, v2...]], eased inOut between keys
    if (!keys.length) return Array(n).fill(0);
    if (t <= keys[0][0]) return keys[0].slice(1);
    for (let i = 1; i < keys.length; i++) if (t < keys[i][0]) {
      const a = keys[i - 1], b = keys[i], q = E.inOut((t - a[0]) / Math.max(1e-6, b[0] - a[0]));
      return a.slice(1).map((v, j) => v + (b[j + 1] - v) * q);
    }
    return keys[keys.length - 1].slice(1);
  }
  const parseKeys = str => (str || '').split(';').filter(x => x.trim()).map(x => x.split(',').map(Number));

  // ---------------------------------------------------------------- element setup
  function prepare(el) {
    const d = el.dataset;
    const st = { el, kind: d.in || 'fade', at: +d.at || 0, dur: +(d.dur || .7), out: d.out || 'fade', outAt: d.outAt !== undefined ? +d.outAt : null, outDur: +(d.outDur || .5) };
    st.base = el.getAttribute('transform') || '';
    if (st.kind === 'draw' || st.kind === 'arrow' || st.out === 'draw-back') {
      const paths = el.tagName === 'path' ? [el] : [...el.querySelectorAll('path.om-line')];
      st.paths = paths.map(p => { const L = p.getTotalLength(); p.style.strokeDasharray = `${L} ${L}`; return { p, L, dash: p.getAttribute('data-dash') }; });
      st.head = el.querySelector('.om-head');
    }
    if (st.kind.startsWith('mask') || st.kind === 'grow') {
      const bb = el.getBBox();
      const ns = 'http://www.w3.org/2000/svg';
      const cp = document.createElementNS(ns, 'clipPath');
      cp.setAttribute('id', 'omc' + Math.random().toString(36).slice(2, 8));
      const r = document.createElementNS(ns, 'rect');
      Object.assign(st, { bb, rect: r });
      r.setAttribute('x', bb.x - 2); r.setAttribute('y', bb.y - 2); r.setAttribute('width', bb.width + 4); r.setAttribute('height', bb.height + 4);
      cp.appendChild(r); el.ownerSVGElement.querySelector('defs').appendChild(cp);
      el.setAttribute('clip-path', `url(#${cp.id})`);
    }
    if (st.kind === 'lines' || st.kind === 'words') st.parts = [...el.querySelectorAll(st.kind === 'lines' ? '.om-l' : '.om-w')];
    if (st.kind === 'count') { st.to = +d.countTo; st.from = +(d.countFrom || 0); st.fmt = d.countFmt || '{n}'; }
    if (st.kind === 'pop' || st.out === 'shrink') { const bb = el.getBBox(); st.cx = bb.x + bb.width / 2; st.cy = bb.y + bb.height / 2; }
    st.stagger = +(d.stagger || .12);
    return st;
  }

  function apply(st, t) {
    const el = st.el;
    let pin = st.kind === 'lines' || st.kind === 'words' ? 1 : E.out(prog(t, st.at, st.dur));
    let pout = st.outAt === null ? 0 : E.in(prog(t, st.outAt, st.outDur));
    let op = 1, tx = 0, ty = 0, sc = 1;
    switch (st.kind) {
      case 'fade': op = pin; break;
      case 'fade-up': op = pin; ty = (1 - pin) * 18; break;
      case 'fade-left': op = pin; tx = (1 - pin) * -26; break;
      case 'fade-right': op = pin; tx = (1 - pin) * 26; break;
      case 'pop': { const q = E.back(prog(t, st.at, st.dur)); op = clamp(prog(t, st.at, st.dur * .6)); sc = .55 + .45 * q; break; }
      case 'mask-right': case 'mask-left': case 'mask-up': case 'grow': {
        const { bb, rect } = st;
        if (st.kind === 'mask-right') { rect.setAttribute('width', (bb.width + 4) * pin); }
        if (st.kind === 'mask-left') { rect.setAttribute('x', bb.x - 2 + (bb.width + 4) * (1 - pin)); rect.setAttribute('width', (bb.width + 4) * pin); }
        if (st.kind === 'mask-up') { rect.setAttribute('y', bb.y - 2 + (bb.height + 4) * (1 - pin)); rect.setAttribute('height', (bb.height + 4) * pin); }
        if (st.kind === 'grow') { const w = (bb.width + 4) * pin, h = (bb.height + 4) * (.35 + .65 * pin); rect.setAttribute('x', bb.x + bb.width / 2 - w / 2); rect.setAttribute('width', w); rect.setAttribute('y', bb.y + bb.height / 2 - h / 2); rect.setAttribute('height', h); }
        op = clamp(pin * 3); break;
      }
      case 'draw': case 'arrow': {
        const pd = E.inOut(prog(t, st.at, st.dur));
        st.paths.forEach(({ p, L }) => { p.style.strokeDashoffset = L * (1 - pd); });
        if (st.head) st.head.setAttribute('opacity', clamp((pd - .82) / .18));
        if (pd >= 1) st.paths.forEach(({ p, dash }) => { if (dash) { p.style.strokeDasharray = dash; p.style.strokeDashoffset = 0; } });
        break;
      }
      case 'lines': case 'words': {
        st.parts.forEach((w, i) => {
          const q = E.out(prog(t, st.at + i * st.stagger, st.dur));
          w.setAttribute('opacity', q.toFixed(3));
          w.setAttribute('transform', `translate(0,${((1 - q) * 10).toFixed(2)})`);
        });
        op = 1; break;
      }
      case 'count': {
        const q = E.soft(prog(t, st.at, st.dur));
        const n = Math.round(st.from + (st.to - st.from) * q);
        el.textContent = st.fmt.replace('{n}', n.toLocaleString('en-US'));
        op = clamp(prog(t, st.at, .25)); break;
      }
    }
    // exits
    if (pout > 0) {
      switch (st.out) {
        case 'fade': op *= 1 - pout; break;
        case 'fade-down': op *= 1 - pout; ty += pout * 16; break;
        case 'shrink': op *= 1 - pout; sc *= 1 - .25 * pout; break;
        case 'mask-left': if (st.rect) { st.rect.setAttribute('width', (st.bb.width + 4) * (1 - pout)); } op *= 1 - pout * .3; break;
        case 'mask-right': if (st.rect) { st.rect.setAttribute('x', st.bb.x - 2 + (st.bb.width + 4) * pout); st.rect.setAttribute('width', (st.bb.width + 4) * (1 - pout)); } op *= 1 - pout * .3; break;
        case 'draw-back': if (st.paths) st.paths.forEach(({ p, L }) => { p.style.strokeDasharray = `${L} ${L}`; p.style.strokeDashoffset = -L * pout; }); if (st.head) st.head.setAttribute('opacity', 1 - pout); break;
      }
    }
    let tr = st.base;
    if (tx || ty) tr += ` translate(${tx.toFixed(2)},${ty.toFixed(2)})`;
    if (sc !== 1) tr += ` translate(${st.cx},${st.cy}) scale(${sc.toFixed(4)}) translate(${-st.cx},${-st.cy})`;
    if (tr) el.setAttribute('transform', tr); else el.removeAttribute('transform');
    el.setAttribute('opacity', op.toFixed(3));
  }

  // ---------------------------------------------------------------- scene mount
  function mount(svg, opts = {}) {
    const S = { svg, dur: opts.dur || 8, items: [], micro: [], faces: [], cam: null, t: 0 };
    svg.querySelectorAll('[data-in]').forEach(el => S.items.push(prepare(el)));
    const cam = svg.querySelector('[data-cam]');
    if (cam) { const [s0, s1, dx, dy, c0, c1] = cam.dataset.cam.split(',').map(Number); S.cam = { el: cam, s0, s1, dx, dy, c0: isNaN(c0) ? 0 : c0, c1: isNaN(c1) ? S.dur : c1, base: cam.getAttribute('transform') || '' }; }
    svg.querySelectorAll('[data-rot]').forEach(el => { const [px, py] = el.dataset.rot.split(',').map(Number); const sw = (el.dataset.sway || '0,3,0').split(',').map(Number); S.micro.push({ type: 'rot', el, px, py, keys: parseKeys(el.dataset.k), sw, base: el.getAttribute('transform') || '' }); });
    svg.querySelectorAll('[data-mv]').forEach(el => S.micro.push({ type: 'mv', el, keys: parseKeys(el.dataset.mv), bob: +(el.dataset.bob || 0), base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('[data-zb]').forEach(el => { const [z0, zd, dir, bid] = el.dataset.zb.split(','); S.micro.push({ type: 'zb', el, z0: +z0, zd: +zd, dir, blur: svg.ownerDocument.getElementById(bid), base: el.getAttribute('transform') || '' }); });
    svg.querySelectorAll('[data-par]').forEach(el => S.micro.push({ type: 'par', el, k: +el.dataset.par, base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('[data-float]').forEach(el => { const [a, p] = el.dataset.float.split(',').map(Number); S.micro.push({ type: 'float', el, a, p, ph: Math.random() * 6, base: el.getAttribute('transform') || '' }); });
    svg.querySelectorAll('[data-breath]').forEach(el => { const [a, p] = (el.dataset.breath || '1.2,3.6').split(',').map(Number); S.micro.push({ type: 'breath', el, a, p, base: el.getAttribute('transform') || '' }); });
    svg.querySelectorAll('.om-dust').forEach((el, i) => S.micro.push({ type: 'dust', el, i, seed: +(el.dataset.seed || i) }));
    svg.querySelectorAll('.om-beam').forEach((el, i) => S.micro.push({ type: 'beam', el, i, base: +el.getAttribute('opacity') }));
    svg.querySelectorAll('.om-cloud').forEach((el, i) => S.micro.push({ type: 'cloud', el, i, base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('.om-wave').forEach((el, i) => S.micro.push({ type: 'wave', el, i, base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('.om-caps').forEach((el, i) => S.micro.push({ type: 'caps', el, i, base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('.om-spray').forEach((el, i) => S.micro.push({ type: 'spray', el, i, base: el.getAttribute('transform') || '' }));
    svg.querySelectorAll('.om-rain').forEach((el, i) => S.micro.push({ type: 'rain', el, i }));
    svg.querySelectorAll('.om-envbar').forEach(el => S.micro.push({ type: 'envbar', el, key: el.dataset.key, t0: +el.dataset.t0, i: +el.dataset.i }));
    (opts.faces || []).forEach(f => S.faces.push(faceSetup(svg, f)));
    return S;
  }

  function seekScene(S, t) {
    S.t = t;
    if (S.cam) {
      const q = E.inOut(clamp((t - S.cam.c0) / Math.max(1e-6, S.cam.c1 - S.cam.c0)));
      const s = S.cam.s0 + (S.cam.s1 - S.cam.s0) * q, dx = S.cam.dx * q, dy = S.cam.dy * q;
      S.cam.el.setAttribute('transform', `${S.cam.base} translate(${270 + dx},${480 + dy}) scale(${s.toFixed(4)}) translate(-270,-480)`);
      S.camState = { dx, dy };
    }
    for (const m of S.micro) {
      switch (m.type) {
        case 'par': { const c = S.camState || { dx: 0, dy: 0 }; m.el.setAttribute('transform', `${m.base} translate(${(c.dx * m.k).toFixed(2)},${(c.dy * m.k).toFixed(2)})`); break; }
        case 'float': m.el.setAttribute('transform', `${m.base} translate(0,${(m.a * Math.sin(2 * Math.PI * t / m.p + m.ph)).toFixed(2)})`); break;
        case 'breath': { const k = Math.sin(2 * Math.PI * t / m.p); m.el.setAttribute('transform', `${m.base} translate(0,${(-m.a * .5 * (1 + k)).toFixed(2)})`); break; }
        case 'dust': { const y = -((t * 6 + m.seed * 3) % 40) + 20, x = 4 * Math.sin(t * .7 + m.i); m.el.setAttribute('transform', `translate(${x.toFixed(2)},${y.toFixed(2)})`); m.el.setAttribute('opacity', (.75 + .25 * Math.sin(t * 2.3 + m.i * 1.7)).toFixed(3)); break; }
        case 'beam': m.el.setAttribute('opacity', (m.base * (.86 + .14 * Math.sin(t * 1.1 + m.i * 1.9) * Math.sin(t * .37 + m.i))).toFixed(3)); break;
        case 'cloud': m.el.setAttribute('transform', `${m.base} translate(${(t * (2 + m.i % 3)).toFixed(2)},0)`); break;
        case 'wave': m.el.setAttribute('transform', `${m.base} translate(${(8 * Math.sin(t * .9 + m.i)).toFixed(2)},${(5 * Math.sin(t * 1.3 + m.i)).toFixed(2)})`); break;
        case 'caps': m.el.setAttribute('transform', `${m.base} translate(${((t * 9) % 30 - 15).toFixed(2)},0)`); m.el.setAttribute('opacity', (.85 + .15 * Math.sin(t * 2)).toFixed(3)); break;
        case 'rot': { const [a] = keyed(m.keys, t, 1); const sw = m.sw[0] ? m.sw[0] * Math.sin(2 * Math.PI * t / m.sw[1] + m.sw[2]) : 0; m.el.setAttribute('transform', `${m.base} rotate(${(a + sw).toFixed(2)} ${m.px} ${m.py})`); break; }
        case 'mv': { const [x, y] = keyed(m.keys, t, 2); let b = 0; if (m.bob) { const [x2, y2] = keyed(m.keys, t - .04, 2); if (Math.hypot(x - x2, y - y2) > .05) b = -m.bob * Math.abs(Math.sin(t * Math.PI * 3.6)); } m.el.setAttribute('transform', `${m.base} translate(${x.toFixed(2)},${(y + b).toFixed(2)})`); break; }
        case 'zb': { let q = clamp((t - m.z0) / m.zd); q = m.dir === 'out' ? E.in(q) : 1 - E.out(q); const sc = 1 + .35 * q; m.el.setAttribute('transform', `${m.base} translate(270,480) scale(${sc.toFixed(4)}) translate(-270,-480)`); if (m.blur) m.blur.setAttribute('stdDeviation', (14 * q).toFixed(2)); m.el.setAttribute('opacity', (1 - .25 * q).toFixed(3)); break; }
        case 'rain': m.el.setAttribute('transform', `translate(${(-(t * 90) % 18).toFixed(2)},${((t * 420 + m.i * 37) % 60).toFixed(2)})`); break;
        case 'envbar': { const env = window.OM_ENV && window.OM_ENV[m.key]; const j = Math.floor((t - m.t0) * 50); const v = env && j >= 0 && j < env.length ? env[j] : 0; const k = .18 + .82 * v * (.55 + .45 * Math.sin(m.i * 1.9 + t * 11)); m.el.setAttribute('transform', `scale(1,${k.toFixed(3)})`); break; }
        case 'spray': { const ph = (t % 2.6) / 2.6; const s = .85 + .3 * Math.sin(ph * Math.PI); m.el.setAttribute('transform', `${m.base} translate(150,860) scale(${s.toFixed(3)}) translate(-150,-860)`); m.el.setAttribute('opacity', (.55 + .45 * Math.sin(ph * Math.PI)).toFixed(3)); break; }
      }
    }
    for (const it of S.items) apply(it, t);
    for (const f of S.faces) faceApply(f, t);
  }

  // ---------------------------------------------------------------- faces: blink, glance, talk
  function faceSetup(svg, f) {
    const root = svg.ownerDocument;
    const g = id => root.getElementById(`${f.id}-${id}`);
    const r = rnd(f.seed || 7);
    const blinks = [];
    for (let t = .6 + r() * 1.5; t < 200; t += (f.blinkEvery || 3.2) * (.6 + r() * .8)) blinks.push(t);
    (f.blinkAt || []).forEach(b => blinks.push(b));
    const talkPat = [];                                       // mouth shapes cycle ~9 Hz with natural variation
    for (let i = 0; i < 2000; i++) talkPat.push(r() < .55 ? 2 : (r() < .7 ? 1 : 0));
    return { f, iL: g('iL'), iR: g('iR'), bl: g('bl'), m1: g('m1'), m2: g('m2'), blinks, talkPat };
  }
  function faceApply(F, t) {
    const { f } = F;
    if (F.bl) F.bl.setAttribute('display', F.blinks.some(b => t >= b && t < b + .13) ? 'inline' : 'none');
    let gx = 0, gy = 0;
    for (const [at, dx, dy] of (f.glance || [])) { const q = E.inOut(prog(t, at, .35)); gx = gx + (dx - gx) * q; gy = gy + (dy - gy) * q; }
    [F.iL, F.iR].forEach(e => e && e.setAttribute('transform', `translate(${gx.toFixed(2)},${gy.toFixed(2)})`));
    let shape = 0;
    for (const [a, b, key] of (f.talk || [])) if (t >= a && t < b) {
      const env = key && window.OM_ENV && window.OM_ENV[key];
      if (env) { const i = Math.floor((t - a) * 50), v = Math.max(env[i] || 0, .7 * (env[i + 1] || 0)); shape = v < .2 ? 0 : (v < .56 ? 1 : 2); }
      else { shape = F.talkPat[Math.floor((t - a) * 9) % F.talkPat.length]; if (b - t < .08) shape = 0; }
    }
    if (F.m1) F.m1.setAttribute('display', shape === 1 ? 'inline' : 'none');
    if (F.m2) F.m2.setAttribute('display', shape === 2 ? 'inline' : 'none');
  }

  // ---------------------------------------------------------------- public API
  const scenes = [];
  window.OM = {
    ease: E,
    mount(svg, opts) { const S = mount(svg, opts); scenes.push(S); seekScene(S, 0); return S; },
    seek(t, S) { (S ? [S] : scenes).forEach(s => seekScene(s, t)); },
    play(loop = true) {
      const t0 = performance.now();
      const step = now => {
        const t = (now - t0) / 1000;
        if (!window.__freeze) scenes.forEach(s => seekScene(s, loop ? t % s.dur : Math.min(t, s.dur)));
        requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    },
  };
})();
