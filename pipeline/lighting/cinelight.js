// Odd Hours cinematic lighting: runtime helper for animated renders.
// Re-aims each character's rim + form shade toward its light source every frame,
// so the rim stays on the lit side while the character moves across the frame.
// Usage (inside the page, after the SVG is built by cinelight.py):
//   CineLight.track('#c-james', [ -80, 430 ]);      // light position in frame units
//   ...then call CineLight.update() once per rendered frame.
(function () {
  const tracked = [];
  function centre(el) {
    const b = el.getBBox();
    // getBBox is in the element's own user space; wrappers are untransformed, so this is frame space
    return [b.x + b.width / 2, b.y + b.height * 0.35];
  }
  function setDir(el, dx, dy) {
    const f = document.getElementById(el.id + '-f');
    if (!f) return;
    const o1 = f.querySelector('.cl-o1'), o2 = f.querySelector('.cl-o2');
    const shade = f.querySelector('feOffset:not(.cl-o1):not(.cl-o2)');
    const w1 = parseFloat(f.dataset.w1 || Math.hypot(+o1.getAttribute('dx'), +o1.getAttribute('dy')));
    const w2 = parseFloat(f.dataset.w2 || Math.hypot(+o2.getAttribute('dx'), +o2.getAttribute('dy')));
    const k = parseFloat(f.dataset.k || Math.hypot(+shade.getAttribute('dx'), +shade.getAttribute('dy')));
    f.dataset.w1 = w1; f.dataset.w2 = w2; f.dataset.k = k;
    o1.setAttribute('dx', (-dx * w1).toFixed(2)); o1.setAttribute('dy', (-dy * w1).toFixed(2));
    o2.setAttribute('dx', (-dx * w2).toFixed(2)); o2.setAttribute('dy', (-dy * w2).toFixed(2));
    shade.setAttribute('dx', (dx * k).toFixed(2)); shade.setAttribute('dy', (dy * k).toFixed(2));
  }
  window.CineLight = {
    track(sel, light) { const el = document.querySelector(sel); if (el) tracked.push({ el, light }); },
    update() {
      for (const t of tracked) {
        const [cx, cy] = centre(t.el);
        const dx = t.light[0] - cx, dy = t.light[1] - cy, m = Math.hypot(dx, dy) || 1;
        setDir(t.el, dx / m, dy / m);
      }
    },
    // flicker a practical light a little (lamps, screens); call per frame with time in seconds
    flicker(sel, t, amount = 0.04) {
      document.querySelectorAll(sel).forEach((el, i) => {
        const base = parseFloat(el.dataset.op || el.getAttribute('opacity') || 1);
        el.dataset.op = base;
        el.setAttribute('opacity', (base * (1 - amount + amount * Math.sin(t * 7.3 + i) * Math.sin(t * 2.1))).toFixed(3));
      });
    },
  };
})();
