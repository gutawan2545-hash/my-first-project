#!/usr/bin/env python3
"""Animated test: Sister Rosa, shots 17-19 (tears well up -> candle goes out -> kneels and prays).
Builds anim_rosa.html with window.setTime(t). Render with: node anim_render_rosa.js  ->  frames/ + rosa_tears.mp4
Characters, room and lighting come from the approved storyboard (storyboard.py / sb_stages2.py)."""
import os, re, sys, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
NS = {"__file__": os.path.join(HERE, "storyboard.py"), "__name__": "sb"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(HERE, "storyboard.py")).read(), NS)
cf, room_rosa, P = NS["cf"], NS["room_rosa"], NS["P"]

# ---------- Rosa as one live figure: arms + head addressable from JS ----------
fig = cf.F["rosa"].replace('id="fb-rosa"', 'id="rosaFig"', 1)
# face overlays in head-local coordinates (same space as the approved face), inside the head's 0.82 scale
SKIN, SHADE = "#f5d3b4", "#e2b08f"
def eye_overlay(side):
    """Overlay for one eye, drawn in left-eye coordinates; the right eye is the same drawing mirrored."""
    s = side
    lidcol = SKIN if s < 0 else "#efc8a8"
    o = f'<g id="rim{s}" opacity="0"><ellipse cx="-13" cy="1" rx="12" ry="8" fill="#e8807e" opacity=".55"/></g>'
    o += f'<path id="water{s}" d="M -20,2.6 C -15,5.4 -10,5.4 -5.5,2.4" stroke="#e8f4ff" stroke-width="1.8" fill="none" opacity="0" stroke-linecap="round"/>'
    o += f'<g id="glint{s}" opacity="0"><circle cx="-16" cy="1.6" r="1.1" fill="#fff"/><circle cx="-10" cy="2.4" r=".7" fill="#fff"/></g>'
    lid = "M -22.5,-1 C -19,-10.5 -7,-10.5 -3.5,-1 C -7,4.2 -19,4.2 -22.5,-1 Z"
    o += (f'<g id="lid{s}" transform="translate(0,-10) scale(1,0) translate(0,10)"><path d="{lid}" fill="{lidcol}"/>'
          f'<path d="M -22.5,-1 C -19,4.2 -7,4.2 -3.5,-1" stroke="#1b1316" stroke-width="1.8" fill="none"/>'
          f'<path d="M -21,0 L -25,-2.5 M -17,2.6 L -19,5.6 M -12,3.4 L -12.6,6.6" stroke="#1b1316" stroke-width="1.1"/></g>')
    o += (f'<g id="tear{s}" opacity="0"><path id="trail{s}" d="M -15,4.6 C -16,14 -18,22 -19,34" stroke="#dcecff" stroke-width="1.6" fill="none" opacity=".7" stroke-dasharray="40" stroke-dashoffset="40"/>'
          f'<path id="drop{s}" d="M 0,-3.2 C 1.8,-.6 2.4,1 2.4,2 C 2.4,3.6 -2.4,3.6 -2.4,2 C -2.4,1 -1.8,-.6 0,-3.2 Z" fill="#eef6ff" stroke="#b8d0ec" stroke-width=".5" transform="translate(-15,5)"/></g>')
    return o if s < 0 else f'<g transform="scale(-1,1)">{o}</g>'
mouth = (f'<ellipse cx="0" cy="24.5" rx="6.6" ry="5" fill="{SKIN}"/>'   # covers the drawn "o" mouth
         f'<path id="mouthTop" d="M -5,23.6 Q 0,22.4 5,23.6" stroke="#8e4a4c" stroke-width="1.9" fill="none" stroke-linecap="round"/>'
         f'<path id="mouthLow" d="M -3.4,26 Q 0,27 3.4,26" stroke="#d27e7e" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
         f'<ellipse id="mouthGap" cx="0" cy="24.6" rx="0" ry="0" fill="#6a3036"/>')
overlay = f'<g id="faceFx" transform="translate(0,9) scale(.82)">{eye_overlay(-1)}{eye_overlay(1)}{mouth}</g>'
fig = fig[:fig.rstrip().rfind("</g>")]          # open the outer figure group
fig = fig[:fig.rstrip().rfind("</g>")] + overlay + "</g></g>"   # put the overlay inside the head group

# ---------- backgrounds per shot ----------
ROOM = room_rosa()
st_old = NS["ST"]["oldwing"]
BG_A = f'<svg id="bgA" x="0" y="0" width="540" height="960" viewBox="10 120 300 533" preserveAspectRatio="xMidYMid slice"><g filter="url(#blurBg)">{ROOM}</g></svg>'
BG_B = (f'<g id="bgB" style="display:none"><svg x="0" y="0" width="540" height="960" viewBox="196 380 172 306" preserveAspectRatio="xMidYMid slice">{st_old}'
        f'<rect id="winDark" x="267.6" y="489" width="62.4" height="104" fill="#0d090c" opacity="0"/>'
        f'<circle id="candleGlow" cx="299" cy="546" r="70" fill="url(#lg_ffe6c4)" opacity="1"/>'
        f'<path id="smoke" d="M 299,540 C 292,520 306,500 298,480 C 292,466 304,452 298,438" stroke="#c8c4d0" stroke-width="2.4" fill="none" opacity="0" stroke-dasharray="120" stroke-dashoffset="120"/></svg></g>')
BG_C = f'<svg id="bgC" style="display:none" x="0" y="0" width="540" height="960" viewBox="170 330 300 533" preserveAspectRatio="xMidYMid slice">{ROOM}</svg>'

FIG_WRAP = f'<g id="rosaWrap">{fig}<g id="rosary" opacity="0"><path d="M -6,226 C -10,246 -4,262 0,268 C 4,262 10,246 6,226" fill="none" stroke="#6a4a3a" stroke-width="2.2" stroke-dasharray="2.2 1.6"/><rect x="-1.2" y="268" width="2.4" height="12" fill="#4a3328"/><rect x="-4.5" y="271" width="9" height="2.4" fill="#4a3328"/></g></g>'

# light + grade in the tone of the approved chapel frame (purple-brown, cool window light, soft vignette)
LIGHT = ('<rect id="moonA" width="540" height="960" fill="url(#moonGrad)" style="mix-blend-mode:screen"/>'
         '<rect width="540" height="960" fill="#2a1830" opacity=".18" style="mix-blend-mode:multiply"/>'
         '<rect width="540" height="960" fill="url(#vig)"/>'
         '<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:screen"/>')

SUBS = [  # (start, end, thai lines, english)
    (1.4, 6.0, ["พระเจ้า…", "ลูกขอโทษ… ลูกขอโทษ"], "God... I'm sorry... I'm sorry."),
    (6.7, 9.6, ["แล้วแสงเทียนก็ดับ", "เหมือนมีคนเป่ามันทิ้ง"], "Then the candle went out, as if someone had blown on it."),
    (10.0, 16.4, ["เธอสวดมนต์อยู่อย่างนั้นจนฟ้าสาง", "โดยไม่กล้าหันกลับไปมองหน้าต่างอีกเลย"], "She prayed until dawn, never daring to look back at the window."),
]
def sub_svg(i, th, en):
    y = 712 - (len(th) * 27 + 17) / 2 + 20
    o = f'<g id="sub{i}" opacity="0" font-family="IBM Plex Sans Thai, sans-serif" text-anchor="middle" filter="url(#subStroke)">'
    for L in th: o += f'<text x="270" y="{y:.0f}" font-size="20" font-weight="700" fill="#ffd84a">{L}</text>'; y += 27
    return o + f'<text x="270" y="{y:.0f}" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#fff">{en}</text></g>'
SUB_SVG = "".join(sub_svg(i, th, en) for i, (a, b, th, en) in enumerate(SUBS))

DEFS = NS["DEFS"].replace('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>', '').replace('</defs></svg>', '')
EXTRA_DEFS = ('<filter id="blurBg" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="2.2"/></filter>'
              '<radialGradient id="moonGrad" cx="18%" cy="30%" r="70%"><stop offset="0" stop-color="#b8c4ff" stop-opacity=".22"/><stop offset="1" stop-color="#b8c4ff" stop-opacity="0"/></radialGradient>'
              '<radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset=".55" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".6"/></radialGradient>'
              '<filter id="grain" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="5" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>'
              '<filter id="subStroke" x="-10%" y="-30%" width="120%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="2.2" result="d"/><feFlood flood-color="#120e18"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')

JS = r'''
const $ = id => document.getElementById(id);
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const ramp = (t, a, b) => ease((t - a) / (b - a));
function blinkAt(t, t0, close = .18, hold = .1, open = .28) {   // 0 open .. 1 closed
  if (t < t0 || t > t0 + close + hold + open) return 0;
  if (t < t0 + close) return ease((t - t0) / close);
  if (t < t0 + close + hold) return 1;
  return 1 - ease((t - t0 - close - hold) / open);
}
function setLid(s, v) { $('lid' + s).setAttribute('transform', `translate(0,-10) scale(1,${v.toFixed(3)}) translate(0,10)`); }
function tear(s, t, t0, dur) {
  const p = clamp((t - t0) / dur);
  $('tear' + s).setAttribute('opacity', t < t0 ? 0 : (p > .97 ? 1 - (p - .97) / .03 : 1));
  // path: from the lower lid down the cheek; slow start (the drop gathers), then slides
  const q = p < .25 ? p * .3 : .075 + (p - .25) / .75 * .925;
  const x = -15 - 4 * q, y = 5 + 29 * q;
  $('drop' + s).setAttribute('transform', `translate(${x.toFixed(2)},${y.toFixed(2)}) scale(${(1 + .25 * Math.min(p * 4, 1)).toFixed(2)})`);
  $('trail' + s).setAttribute('stroke-dashoffset', (40 - 40 * q).toFixed(2));
}
const SUBS = %SUBS%;
const SHOT = [[0, 6.6, 'A'], [6.6, 9.8, 'B'], [9.8, 17, 'C']];
window.setTime = function (t) {
  const shot = SHOT.find(s => t >= s[0] && t < s[1])?.[2] || 'C';
  $('bgA').style.display = shot === 'A' ? '' : 'none';
  $('bgB').style.display = shot === 'B' ? '' : 'none';
  $('bgC').style.display = shot === 'C' ? '' : 'none';
  $('rosaWrap').style.display = shot === 'B' ? 'none' : '';
  $('moonA').style.display = shot === 'B' ? 'none' : '';
  const breath = Math.sin(t * 2 * Math.PI / 3.6);           // ~3.6 s breathing cycle, quicker than calm
  const shiver = Math.sin(t * 23) * .35 + Math.sin(t * 37) * .2;
  let cam = 1, wx = 270, wy = 351, k = 3.2, armL = 0, armR = 0, head = 0, kneel = 0;
  if (shot === 'A') {
    cam = 1 + .07 * ramp(t, 0, 6.6);                          // slow push-in on her face
    head = -2 + 1.2 * Math.sin(t * 1.3) + shiver * .5;        // small trembling tilt
    const well = ramp(t, .6, 3.2);                            // tears welling
    for (const s of [-1, 1]) {
      $('rim' + s).setAttribute('opacity', (well * .55).toFixed(3));
      $('water' + s).setAttribute('opacity', (well * .95).toFixed(3));
      $('glint' + s).setAttribute('opacity', (well * .9).toFixed(3));
      $('glint' + s).setAttribute('transform', `translate(${(Math.sin(t * 17 + s) * .35).toFixed(2)},${(Math.cos(t * 13) * .25).toFixed(2)})`);
    }
    const b = Math.max(blinkAt(t, 1.9, .26, .14, .42), blinkAt(t, 4.9, .3, .16, .45));   // slow, heavy blinks
    setLid(-1, b); setLid(1, b);
    tear(-1, t, 3.4, 2.6);                                    // first tear spills from her right eye
    tear(1, t, 99, 1);
    // mouth: pressed, down-turned, quivering; parts on the words
    const q = shiver * .5, talk = (t > 2.0 && t < 5.8) ? Math.max(0, Math.sin((t - 2) * 7.5)) * .9 : 0;
    $('mouthTop').setAttribute('d', `M -5,${(23.8 + q * .3).toFixed(2)} Q 0,${(22.6 - talk * .4).toFixed(2)} 5,${(23.8 - q * .3).toFixed(2)}`);
    $('mouthLow').setAttribute('d', `M -3.4,${(26 + talk * .8).toFixed(2)} Q 0,${(27.2 + talk * 1.6).toFixed(2)} 3.4,${(26 + talk * .8).toFixed(2)}`);
    $('mouthGap').setAttribute('rx', (talk * 3).toFixed(2)); $('mouthGap').setAttribute('ry', (talk * 1.6).toFixed(2));
    wy = 351 + breath * 1.6;
  } else if (shot === 'C') {
    const tc = t - 9.8;
    k = 1.05 * 1.8; wx = (330 - 170) * 1.8; wy = (900 - 372 * 1.05 - 330) * 1.8;
    kneel = 70 * 1.8 * ramp(tc, .4, 1.6);                          // she sinks down to her knees (legs leave the frame)
    armL = -18 * ramp(tc, 1.2, 2.1); armR = 18 * ramp(tc, 1.2, 2.1);
    $('rosary').setAttribute('opacity', ramp(tc, 1.9, 2.2).toFixed(2));   // hands come together to pray
    head = -5 * ramp(tc, 1.4, 2.4) + shiver * .3;
    const closed = ramp(tc, 1.8, 2.3);                        // eyes close in prayer
    setLid(-1, closed); setLid(1, closed);
    for (const s of [-1, 1]) { $('rim' + s).setAttribute('opacity', .5); $('water' + s).setAttribute('opacity', closed > .5 ? 0 : .9); $('glint' + s).setAttribute('opacity', 0); }
    tear(-1, t, 99, 1); tear(1, t, 9.8 + 3.2, 3.0);            // a tear runs from the closed eye
    const pray = tc > 2.6 ? Math.max(0, Math.sin((tc - 2.6) * 6.2)) * .7 : 0;   // whispering
    $('mouthTop').setAttribute('d', `M -5,23.6 Q 0,${(22.6 - pray * .3).toFixed(2)} 5,23.6`);
    $('mouthLow').setAttribute('d', `M -3.4,${(26 + pray * .6).toFixed(2)} Q 0,${(27 + pray * 1.2).toFixed(2)} 3.4,${(26 + pray * .6).toFixed(2)}`);
    $('mouthGap').setAttribute('rx', (pray * 2.4).toFixed(2)); $('mouthGap').setAttribute('ry', (pray * 1.1).toFixed(2));
    wy += kneel + breath * 1.2;
    cam = 1 + .025 * ramp(tc, 0, 7);
  } else {   // B: the candle in the old wing goes out
    const tb = t - 6.6, out = ramp(tb, 1.0, 1.25);
    $('candleGlow').setAttribute('opacity', (1 - out) * (0.85 + .15 * Math.sin(tb * 30)));
    $('winDark').setAttribute('opacity', out * .92);
    $('smoke').setAttribute('opacity', out * (1 - ramp(tb, 2.4, 3.2)) * .7);
    $('smoke').setAttribute('stroke-dashoffset', (120 - 120 * ramp(tb, 1.2, 2.8)).toFixed(1));
    cam = 1 + .05 * ramp(tb, 0, 3.2);
  }
  $('rosaWrap').setAttribute('transform', `translate(${wx},${wy.toFixed(2)}) scale(${k})`);
  $('rosa-armL').setAttribute('transform', `rotate(${armL.toFixed(2)} -42 66)`);
  $('rosa-armR').setAttribute('transform', `rotate(${armR.toFixed(2)} 42 66)`);
  $('rosa-head').setAttribute('transform', `rotate(${head.toFixed(2)} 0 52)`);
  $('cam').setAttribute('transform', `translate(270,480) scale(${cam.toFixed(4)}) translate(-270,-480)`);
  SUBS.forEach((s, i) => { const a = clamp((t - s[0]) / .3) * (1 - clamp((t - s[1]) / .3)); $('sub' + i).setAttribute('opacity', a.toFixed(3)); });
  $('fade').setAttribute('opacity', (ramp(t, 16.4, 17) + (shot === 'B' ? 0 : 0)).toFixed(3));
};
window.DURATION = 17;
setTime(0);
'''.replace("%SUBS%", str([[a, b] for a, b, _, _ in SUBS]))

html = f'''<!doctype html><html><head><meta charset="utf-8"><title>Rosa tears</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@500&display=swap">
<style>html,body{{margin:0;background:#000}} svg{{display:block}}</style></head><body>
<svg id="stage" width="540" height="960" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">
<defs>{DEFS}{EXTRA_DEFS}</defs>
<g id="cam">{BG_A}{BG_B}{BG_C}{FIG_WRAP}</g>
{LIGHT}
<rect x="24" y="28" width="134" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8f74d8" stroke-width="1.4"/><text x="91" y="48" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="500" fill="#e6e0f4">18 พ.ย. · 03:00</text>
<g transform="translate(500,44)" opacity=".8"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="none" stroke="#b18cff" stroke-width="1.6"/><circle r="3.6" fill="#b18cff"/></g>
{SUB_SVG}
<rect id="fade" width="540" height="960" fill="#000" opacity="0"/>
</svg>
<script>{JS}</script></body></html>'''
open(os.path.join(HERE, "anim_rosa.html"), "w").write(html)
print("wrote anim_rosa.html", len(html) // 1024, "KB")
