#!/usr/bin/env python3
"""Chapel test frame v2: white, ornate, old-palace chapel gone eerie. 540x960, full-body characters.
Run: python3 chapel.py -> chapel-test-frame.html"""
import os, random, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cf", os.path.join(HERE, "..", "characters", "build_cast_full.py"))
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)

VX, VY = 270, 400          # vanishing point
BW = (176, 364, 236, 520)  # back wall: x0, x1, y_top, y_bottom
R = random.Random(4)

def lerp(a, b, t): return a + (b - a) * t
# side-wall edges: near (t=0) to back wall (t=1)
def lx(t): return lerp(-70, BW[0], t)
def rx(t): return lerp(610, BW[1], t)
def top(t): return lerp(-40, BW[2], t)
def bot(t): return lerp(1010, BW[3], t)
def proj(t):  # perspective spacing: equal real steps look closer near the back
    return 1 - 1 / (1 + 2.6 * t)

out = []
A = out.append

# ---------- base ----------
A('<rect width="540" height="960" fill="#151219"/>')

# ---------- ceiling: barrel vault with coffers and ribs ----------
A(f'<path d="M -70,-40 L 610,-40 L {BW[1]},{BW[2]} L {BW[0]},{BW[2]} Z" fill="#3a3644"/>')
A(f'<path d="M -70,-40 L 270,-40 L 270,{BW[2]} L {BW[0]},{BW[2]} Z" fill="#45404f"/>')
for i in range(1, 9):
    t = proj(i / 9)
    xl, xr, yt = lx(t), rx(t), top(t)
    sag = 70 * (1 - t)
    A(f'<path d="M {xl:.1f},{yt:.1f} Q 270,{yt - sag:.1f} {xr:.1f},{yt:.1f}" fill="none" stroke="#5a5466" stroke-width="{4 * (1 - t) + 1:.1f}"/>')
    A(f'<path d="M {xl:.1f},{yt + 3:.1f} Q 270,{yt - sag + 3:.1f} {xr:.1f},{yt + 3:.1f}" fill="none" stroke="#24202c" stroke-width="{2 * (1 - t) + .6:.1f}"/>')
    A(f'<circle cx="270" cy="{yt - sag / 2 + 4:.1f}" r="{7 * (1 - t) + 2:.1f}" fill="#6a6278"/><circle cx="270" cy="{yt - sag / 2 + 4:.1f}" r="{3.5 * (1 - t) + 1:.1f}" fill="#8a8094"/>')
for u in (-0.55, -0.25, 0.25, 0.55):
    A(f'<path d="M {270 + u * 680:.0f},-40 L {270 + u * (BW[1] - BW[0]):.0f},{BW[2]}" stroke="#2c2834" stroke-width="2"/>')

# ---------- back wall / apse ----------
x0, x1, yt, yb = BW
A(f'<rect x="{x0}" y="{yt}" width="{x1 - x0}" height="{yb - yt}" fill="#a8a2b0"/>')
A(f'<rect x="{x0}" y="{yt}" width="{(x1 - x0) / 2}" height="{yb - yt}" fill="#b6b0be"/>')
A(f'<path d="M {x0 + 14},{yb} L {x0 + 14},{yt + 70} C {x0 + 14},{yt + 10} {x1 - 14},{yt + 10} {x1 - 14},{yt + 70} L {x1 - 14},{yb} Z" fill="#8e8898"/>')  # apse niche
A(f'<path d="M {x0 + 14},{yt + 70} C {x0 + 14},{yt + 10} {x1 - 14},{yt + 10} {x1 - 14},{yt + 70}" fill="none" stroke="#d8d2dc" stroke-width="5"/>')
A(f'<path d="M {x0 + 22},{yt + 72} C {x0 + 24},{yt + 22} {x1 - 24},{yt + 22} {x1 - 22},{yt + 72}" fill="none" stroke="#6e6878" stroke-width="2"/>')
# half-dome rays
for k in range(9):
    a = 3.1416 * (k + .5) / 9
    A(f'<path d="M 270,{yt + 74} L {270 - 80 * __import__("math").cos(a):.1f},{yt + 74 - 50 * __import__("math").sin(a):.1f}" stroke="#7a7486" stroke-width="1.4"/>')
# stained glass in the apse
cx = 270; gw, gh, gy = 76, 150, yt + 86
A(f'<path d="M {cx - gw / 2 - 5},{gy + gh + 5} L {cx - gw / 2 - 5},{gy + 30} C {cx - gw / 2 - 5},{gy - 8} {cx + gw / 2 + 5},{gy - 8} {cx + gw / 2 + 5},{gy + 30} L {cx + gw / 2 + 5},{gy + gh + 5} Z" fill="#2a2430"/>')
A(f'<clipPath id="sgc"><path d="M {cx - gw / 2},{gy + gh} L {cx - gw / 2},{gy + 30} C {cx - gw / 2},{gy - 2} {cx + gw / 2},{gy - 2} {cx + gw / 2},{gy + 30} L {cx + gw / 2},{gy + gh} Z"/></clipPath>')
A(f'<g clip-path="url(#sgc)"><rect x="{cx - gw / 2}" y="{gy - 5}" width="{gw}" height="{gh + 10}" fill="#2b2f5c"/><rect x="{cx - gw / 2}" y="{gy - 5}" width="{gw / 2}" height="{gh + 10}" fill="#363b72"/>'
  f'<rect x="{cx - gw / 2}" y="{gy + gh * .6}" width="{gw}" height="{gh * .4}" fill="#3c2f52"/>'
  f'<circle cx="{cx}" cy="{gy + 22}" r="11" fill="#4c4f8c"/><circle cx="{cx}" cy="{gy + 22}" r="5" fill="#8f7ab8"/>'
  f'<path d="M {cx - 32},{gy + gh} L {cx - 30},{gy + 80} C {cx - 28},{gy + 70} {cx - 10},{gy + 70} {cx - 8},{gy + 80} L {cx - 6},{gy + gh} Z" fill="#5a2f45"/>'
  f'<circle cx="{cx - 19}" cy="{gy + 66}" r="9" fill="#b8a46e" opacity=".55"/><ellipse cx="{cx - 19}" cy="{gy + 67}" rx="5.5" ry="6" fill="#07060a"/>'
  f'<path d="M {cx + 6},{gy + gh} L {cx + 8},{gy + 80} C {cx + 10},{gy + 70} {cx + 28},{gy + 70} {cx + 30},{gy + 80} L {cx + 32},{gy + gh} Z" fill="#2f4f86"/>'
  f'<circle cx="{cx + 19}" cy="{gy + 66}" r="9" fill="#b8a46e" opacity=".55"/><ellipse cx="{cx + 19}" cy="{gy + 67}" rx="5.5" ry="6" fill="#d9c9c0"/>'
  f'<g stroke="#120e16" stroke-width="2" fill="none"><line x1="{cx}" y1="{gy - 5}" x2="{cx}" y2="{gy + gh}"/><line x1="{cx - gw / 2}" y1="{gy + 44}" x2="{cx + gw / 2}" y2="{gy + 44}"/><line x1="{cx - gw / 2}" y1="{gy + 104}" x2="{cx + gw / 2}" y2="{gy + 104}"/></g></g>')
# altar: white marble with faded gilding
ay = yb - 44
A(f'<rect x="{cx - 70}" y="{ay - 6}" width="140" height="8" fill="#e6e0e8"/><rect x="{cx - 64}" y="{ay + 2}" width="128" height="42" fill="#c9c3cf"/><rect x="{cx - 64}" y="{ay + 2}" width="64" height="42" fill="#d8d2dc"/>')
A(f'<rect x="{cx - 52}" y="{ay + 10}" width="104" height="26" fill="none" stroke="#a8945e" stroke-width="1.6"/><path d="M {cx - 6},{ay + 14} L {cx + 6},{ay + 14} L {cx + 6},{ay + 32} L {cx - 6},{ay + 32} Z M {cx - 12},{ay + 20} L {cx + 12},{ay + 20} L {cx + 12},{ay + 25} L {cx - 12},{ay + 25} Z" fill="#a8945e" opacity=".8"/>')
A(f'<rect x="{cx - 80}" y="{yb - 4}" width="160" height="6" fill="#b6b0be"/>')
for dx in (-48, -30, 30, 48):
    A(f'<rect x="{cx + dx - 2}" y="{ay - 34}" width="4" height="28" fill="#a8945e"/><rect x="{cx + dx - 1.5}" y="{ay - 46}" width="3" height="12" fill="#efe8da"/>')
A(f'<rect x="{cx - 1.5}" y="{ay - 70}" width="3" height="60" fill="#8a7a4e"/><rect x="{cx - 12}" y="{ay - 58}" width="24" height="3" fill="#8a7a4e"/>')
# draped statues in niches either side
for sx in (x0 + 30, x1 - 30):
    A(f'<path d="M {sx - 16},{yb - 4} L {sx - 16},{yt + 120} C {sx - 16},{yt + 96} {sx + 16},{yt + 96} {sx + 16},{yt + 120} L {sx + 16},{yb - 4} Z" fill="#6e6878"/>')
    A(f'<path d="M {sx - 11},{yb - 6} C {sx - 13},{yb - 60} {sx - 10},{yt + 150} {sx - 6},{yt + 130} C {sx - 8},{yt + 112} {sx + 8},{yt + 112} {sx + 6},{yt + 130} C {sx + 10},{yt + 150} {sx + 13},{yb - 60} {sx + 11},{yb - 6} Z" fill="#e2dde6"/>')
    A(f'<path d="M {sx},{yt + 128} C {sx + 2},{yt + 170} {sx + 6},{yb - 60} {sx + 11},{yb - 6} L {sx + 2},{yb - 6} C {sx + 2},{yb - 60} {sx},{yt + 170} {sx},{yt + 128} Z" fill="#b9b3c2"/>')

# ---------- side walls ----------
def wall(side):
    xs = lx if side < 0 else rx
    base = "#9a94a6" if side < 0 else "#6c6678"
    lit = "#aaa4b6" if side < 0 else "#7a7486"
    dark = "#7e788c" if side < 0 else "#544e60"
    A(f'<path d="M {xs(0):.0f},{top(0):.0f} L {xs(1):.0f},{top(1):.0f} L {xs(1):.0f},{bot(1):.0f} L {xs(0):.0f},{bot(0):.0f} Z" fill="{base}"/>')
    # dado (lower wall panel) and cornice
    def at(t, f): return xs(t), lerp(top(t), bot(t), f)
    for f, col, w in ((.16, "#d6d0dc", 3.0), (.19, "#5a5468", 1.6), (.78, "#5a5468", 2.0)):
        p0, p1 = at(0, f), at(1, f)
        A(f'<path d="M {p0[0]:.0f},{p0[1]:.0f} L {p1[0]:.0f},{p1[1]:.0f}" stroke="{col}" stroke-width="{w}"/>')
    q0, q1, q2, q3 = at(0, .78), at(1, .78), at(1, 1), at(0, 1)
    A(f'<path d="M {q0[0]:.0f},{q0[1]:.0f} L {q1[0]:.0f},{q1[1]:.0f} L {q2[0]:.0f},{q2[1]:.0f} L {q3[0]:.0f},{q3[1]:.0f} Z" fill="{dark}"/>')
    # dentil band under the cornice
    for i in range(40):
        t = proj(i / 40)
        p = at(t, .17)
        w = 6 * (1 - t) + 1
        A(f'<rect x="{p[0] - w / 2:.1f}" y="{p[1]:.1f}" width="{w:.1f}" height="{w * 1.4:.1f}" fill="#4e485c"/>')
    # bays: pilaster, arched window
    ts = [proj(v) for v in (.08, .26, .44, .62, .8, .98)]
    for i, t in enumerate(ts):
        # pilaster
        w = 26 * (1 - t) + 4
        xa, ya, yb_ = xs(t), lerp(top(t), bot(t), .2), lerp(top(t), bot(t), .98)
        A(f'<rect x="{xa - w / 2:.1f}" y="{ya:.1f}" width="{w:.1f}" height="{yb_ - ya:.1f}" fill="{lit}"/>')
        A(f'<rect x="{xa - w / 2:.1f}" y="{ya:.1f}" width="{w * .28:.1f}" height="{yb_ - ya:.1f}" fill="#d0cad6" opacity=".6"/>')
        A(f'<rect x="{xa + w * .2:.1f}" y="{ya:.1f}" width="{w * .3:.1f}" height="{yb_ - ya:.1f}" fill="{dark}" opacity=".7"/>')
        # capital: scrolls
        A(f'<rect x="{xa - w * .7:.1f}" y="{ya - w * .5:.1f}" width="{w * 1.4:.1f}" height="{w * .5:.1f}" fill="#d6d0dc"/>')
        A(f'<circle cx="{xa - w * .55:.1f}" cy="{ya - w * .1:.1f}" r="{w * .22:.1f}" fill="none" stroke="#5a5468" stroke-width="{w * .08 + .4:.1f}"/><circle cx="{xa + w * .55:.1f}" cy="{ya - w * .1:.1f}" r="{w * .22:.1f}" fill="none" stroke="#5a5468" stroke-width="{w * .08 + .4:.1f}"/>')
        A(f'<path d="M {xa - w * .4:.1f},{ya + w * .1:.1f} Q {xa:.1f},{ya + w * .6:.1f} {xa + w * .4:.1f},{ya + w * .1:.1f}" fill="#bcb6c4"/>')
        if i < len(ts) - 1:
            t2 = ts[i + 1]; tm0, tm1 = lerp(t, t2, .28), lerp(t, t2, .72)
            wx0, wx1 = xs(tm0), xs(tm1)
            wy0t, wy1t = lerp(top(tm0), bot(tm0), .3), lerp(top(tm1), bot(tm1), .3)
            wy0b, wy1b = lerp(top(tm0), bot(tm0), .7), lerp(top(tm1), bot(tm1), .7)
            mx, my = (wx0 + wx1) / 2, (wy0t + wy1t) / 2 - abs(wx1 - wx0) * .9
            frame_col = "#2a2632"
            glass = "#2c3a6c" if side < 0 else "#1a1c34"
            A(f'<path d="M {wx0:.1f},{wy0b:.1f} L {wx0:.1f},{wy0t:.1f} Q {mx:.1f},{my:.1f} {wx1:.1f},{wy1t:.1f} L {wx1:.1f},{wy1b:.1f} Z" fill="{frame_col}"/>')
            A(f'<path d="M {wx0 + (wx1 - wx0) * .08:.1f},{wy0b - 2:.1f} L {wx0 + (wx1 - wx0) * .08:.1f},{wy0t + 2:.1f} Q {mx:.1f},{my + 6:.1f} {wx1 - (wx1 - wx0) * .08:.1f},{wy1t + 2:.1f} L {wx1 - (wx1 - wx0) * .08:.1f},{wy1b - 2:.1f} Z" fill="{glass}"/>')
            A(f'<path d="M {mx:.1f},{my + 6:.1f} L {mx:.1f},{(wy0b + wy1b) / 2:.1f} M {wx0:.1f},{(wy0t + wy0b) / 2:.1f} L {wx1:.1f},{(wy1t + wy1b) / 2:.1f}" stroke="{frame_col}" stroke-width="{2.4 * (1 - t) + .8:.1f}"/>')
            # moulded arch over window
            A(f'<path d="M {wx0 - 4:.1f},{wy0t - 2:.1f} Q {mx:.1f},{my - 12:.1f} {wx1 + 4:.1f},{wy1t - 2:.1f}" fill="none" stroke="#d6d0dc" stroke-width="{3 * (1 - t) + 1:.1f}"/>')
            # peeling plaster & damp under some windows
            if R.random() < .7:
                px, py = (wx0 + wx1) / 2, lerp(wy0b, lerp(top(tm0), bot(tm0), .78), .5)
                pw = abs(wx1 - wx0) * .6
                A(f'<path d="M {px - pw:.1f},{py:.1f} C {px - pw * .6:.1f},{py - pw * .5:.1f} {px + pw * .3:.1f},{py - pw * .2:.1f} {px + pw * .7:.1f},{py + pw * .2:.1f} C {px + pw * .3:.1f},{py + pw * .6:.1f} {px - pw * .4:.1f},{py + pw * .5:.1f} {px - pw:.1f},{py:.1f} Z" fill="#6a6474" opacity=".55"/>')
            A(f'<path d="M {wx0 + 2:.1f},{wy0b:.1f} L {wx0 + 1:.1f},{wy0b + 60 * (1 - t):.1f} M {wx1 - 3:.1f},{wy1b:.1f} L {wx1 - 2:.1f},{wy1b + 40 * (1 - t):.1f}" stroke="#58525f" stroke-width="{3 * (1 - t) + 1:.1f}" opacity=".45"/>')
    # cracks
    for _ in range(3):
        t = R.uniform(.05, .6); f = R.uniform(.25, .7)
        x, y = at(t, f)
        d = f"M {x:.0f},{y:.0f}"
        for k in range(5):
            x += R.uniform(-8, 8); y += R.uniform(6, 16); d += f" L {x:.0f},{y:.0f}"
        A(f'<path d="{d}" fill="none" stroke="#4a4458" stroke-width="1.1"/>')
wall(-1); wall(1)

# ---------- floor: checker marble ----------
A(f'<path d="M {lx(1):.0f},{BW[3]} L {rx(1):.0f},{BW[3]} L 610,1010 L -70,1010 Z" fill="#4a4652"/>')
rows = []
n = 0
while True:
    y = VY + 600 / (1 + .32 * n)
    if y < BW[3]: break
    rows.append(y); n += 1
rows = [1010] + rows[1:] + [BW[3]]
rows = sorted(set(rows), reverse=True)
k = .19
for ri in range(len(rows) - 1):
    ya, yb2 = rows[ri], rows[ri + 1]
    for u in range(-9, 9):
        xa0, xa1 = VX + u * k * (ya - VY), VX + (u + 1) * k * (ya - VY)
        xb0, xb1 = VX + u * k * (yb2 - VY), VX + (u + 1) * k * (yb2 - VY)
        col = "#c9c3cf" if (u + ri) % 2 == 0 else "#57505e"
        A(f'<path d="M {xa0:.1f},{ya:.1f} L {xa1:.1f},{ya:.1f} L {xb1:.1f},{yb2:.1f} L {xb0:.1f},{yb2:.1f} Z" fill="{col}"/>')
# dim the floor towards the back and into the shadows
A(f'<rect x="0" y="{BW[3]}" width="540" height="{960 - BW[3]}" fill="#14111a" opacity=".38"/>')

# ---------- pews ----------
def pew(t, side):
    yb_ = lerp(960, BW[3], t) - 4
    s = 1 - t
    h = 46 * s + 8
    xa = VX + side * (2.1 * k * (yb_ - VY) + 6)
    xw = (lx(t) + 28 * s) if side < 0 else (rx(t) - 28 * s)
    x_in, x_out = (xa, xw) if side < 0 else (xw, xa)
    x_in, x_out = min(xa, xw), max(xa, xw)
    A(f'<rect x="{x_in:.1f}" y="{yb_ - h:.1f}" width="{x_out - x_in:.1f}" height="{h:.1f}" fill="#2a1e22"/>')
    A(f'<rect x="{x_in:.1f}" y="{yb_ - h:.1f}" width="{x_out - x_in:.1f}" height="{h * .18:.1f}" fill="#4a3530"/>')
    A(f'<rect x="{x_in:.1f}" y="{yb_ - h * .55:.1f}" width="{x_out - x_in:.1f}" height="{h * .08:.1f}" fill="#1a1216"/>')
    end = xa
    A(f'<path d="M {end - 4 * s - 1:.1f},{yb_:.1f} L {end - 4 * s - 1:.1f},{yb_ - h - 10 * s:.1f} C {end:.1f},{yb_ - h - 16 * s:.1f} {end + 6 * s:.1f},{yb_ - h - 8 * s:.1f} {end + 4 * s + 1:.1f},{yb_ - h:.1f} L {end + 4 * s + 1:.1f},{yb_:.1f} Z" fill="#3a2a2a"/>')
for t in [proj(v) for v in (.98, .9, .82, .74, .66, .58)]:
    pew(t, -1); pew(t, 1)

# ---------- chandelier (unlit, cobwebbed) ----------
cy = 250
A(f'<path d="M 270,-10 L 270,{cy - 30}" stroke="#2a2630" stroke-width="2"/>')
A(f'<g transform="translate(270,{cy})"><ellipse cx="0" cy="0" rx="46" ry="9" fill="none" stroke="#6a5c40" stroke-width="3"/>'
  '<ellipse cx="0" cy="-22" rx="26" ry="5" fill="none" stroke="#6a5c40" stroke-width="2.4"/><path d="M 0,-30 L 0,14" stroke="#6a5c40" stroke-width="3"/>'
  + "".join(f'<path d="M {x},{-2} L {x},{-12}" stroke="#6a5c40" stroke-width="2"/><rect x="{x - 2}" y="-20" width="4" height="8" fill="#d8d0c0"/>' for x in (-40, -20, 0, 20, 40))
  + "".join(f'<path d="M {x},{4} L {x},{14 + (abs(x) % 9)}" stroke="#c8c4d8" stroke-width="1" opacity=".7"/><circle cx="{x}" cy="{15 + (abs(x) % 9)}" r="2" fill="#dcd8ec" opacity=".8"/>' for x in range(-42, 44, 7))
  + '<path d="M -46,0 C -30,20 -10,24 0,14 M 46,0 C 30,22 12,24 0,14 M -26,-22 C -20,-6 -10,0 0,-4" fill="none" stroke="#c8c4d0" stroke-width=".6" opacity=".5"/></g>')
# cobwebs in the near corners
for (x, y, sx) in ((0, 0, 1), (540, 0, -1)):
    A(f'<g transform="translate({x},{y}) scale({sx},1)" stroke="#c8c4d0" stroke-width=".7" fill="none" opacity=".35">'
      '<path d="M 0,0 L 90,40 M 0,0 L 60,80 M 0,0 L 20,100"/><path d="M 30,13 Q 26,24 20,27 Q 12,30 7,33 M 54,24 Q 46,44 36,54 Q 22,62 13,66 M 78,35 Q 66,62 52,72 Q 34,84 18,90"/></g>')

# ---------- light: moon beams from the left windows, candle rack at the altar ----------
A('<polygon points="20,250 110,300 470,960 250,960" fill="url(#beamC2)" filter="url(#haze)" style="mix-blend-mode:screen"/>')
A('<polygon points="140,330 190,360 420,780 330,800" fill="url(#beamC2)" filter="url(#haze)" opacity=".7" style="mix-blend-mode:screen"/>')
# votive rack near the altar, right
A(f'<rect x="{x1 - 46}" y="{yb - 16}" width="40" height="14" fill="#3a2a26"/>' + "".join(f'<rect x="{x1 - 44 + i * 7}" y="{yb - 24}" width="4" height="8" fill="#efe6d6"/>' for i in range(6)))
A(f'<ellipse cx="{x1 - 26}" cy="{yb - 30}" rx="40" ry="30" fill="url(#glowW)" style="mix-blend-mode:screen"/>')
A('<ellipse cx="270" cy="330" rx="70" ry="80" fill="url(#glowC)" opacity=".5" style="mix-blend-mode:screen"/>')

# dust in the beams
for i in range(46):
    t = R.random(); x = lerp(60, 400, t) + R.uniform(-40, 40); y = lerp(280, 900, t) + R.uniform(-30, 30)
    if R.random() < .6:
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(.6, 1.3):.1f}" fill="#dfe4ff" opacity="{R.uniform(.4, .85):.2f}" filter="url(#moteGlow)"/>')
    else:
        A(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(1.3, 2.2):.1f}" fill="#dfe4ff" opacity="{R.uniform(.18, .32):.2f}" filter="url(#moteFar)"/>')

BG = "".join(out)

# ---------- characters ----------
# Agnes: further back in the aisle, in the gap between moonbeams, lit only by her own candle
ag_k, ag_x, ag_feet = .78, 196, 760
ag_y = ag_feet - 372 * ag_k
hand_x, hand_y = ag_x + 50 * ag_k, ag_y + 228 * ag_k
AGNES = (f'<g style="filter:brightness(.62) saturate(.55)"><g transform="translate({ag_x},{ag_y:.0f}) scale({ag_k})"><use href="#fb-agnes"/></g></g>'
         f'<rect x="{hand_x - 2.5:.0f}" y="{hand_y - 30:.0f}" width="5" height="24" fill="#efe8da"/>'
         f'<path d="M {hand_x:.0f},{hand_y - 42:.0f} C {hand_x - 3.5:.0f},{hand_y - 37:.0f} {hand_x - 3.5:.0f},{hand_y - 33:.0f} {hand_x:.0f},{hand_y - 31:.0f} C {hand_x + 3.5:.0f},{hand_y - 33:.0f} {hand_x + 3.5:.0f},{hand_y - 37:.0f} {hand_x:.0f},{hand_y - 42:.0f} Z" fill="#fff6e6"/>'
         f'<ellipse cx="{hand_x:.0f}" cy="{hand_y - 40:.0f}" rx="70" ry="70" fill="url(#glowW)" opacity=".8" style="mix-blend-mode:screen"/>'
         f'<ellipse cx="{ag_x}" cy="{ag_feet + 4}" rx="34" ry="5" fill="#0a080c" opacity=".55"/>')
# Mariam: front, in the moonbeam
ma_k, ma_x, ma_feet = 1.26, 344, 944
ma_y = ma_feet - 372 * ma_k
MARIAM = (f'<ellipse cx="{ma_x + 14}" cy="{ma_feet + 4}" rx="70" ry="9" fill="#0a080c" opacity=".55"/>'
          f'<g filter="url(#drop)"><g style="filter:brightness(.9) saturate(.85)"><g transform="translate({ma_x},{ma_y:.0f}) scale({ma_k})"><use href="#fb-mariam"/></g></g></g>'
          f'<ellipse cx="{ma_x - 40}" cy="{ma_y + 40:.0f}" rx="150" ry="150" fill="url(#glowC)" opacity=".35" style="mix-blend-mode:screen"/>')

FRAME = f'''<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="โบสถ์น้อยสีขาวตกแต่งวิจิตรแบบวังเก่า ตอนตีสาม แสงจันทร์ส่องผ่านหน้าต่างโค้ง ซิสเตอร์มาเรียมยืนเต็มตัวด้านหน้า ซิสเตอร์อักเนสยืนถือเทียนอยู่ไกลออกไปในทางเดิน">
{BG}
{AGNES}
{MARIAM}
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:screen"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".045" style="mix-blend-mode:overlay"/>
<rect x="24" y="28" width="142" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8f74d8" stroke-width="1.4"/>
<text x="95" y="48" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="500" fill="#e6e0f4">คืนที่ 1 · 03:00</text>
<g transform="translate(500,44)" opacity=".8"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="none" stroke="#b18cff" stroke-width="1.6"/><circle r="3.6" fill="#b18cff"/></g>
<g id="subs" font-family="IBM Plex Sans Thai, sans-serif" text-anchor="middle" filter="url(#subStroke)">
  <text x="270" y="684" font-size="20" font-weight="700" fill="#ffd84a">เมื่อ 20 ปีก่อน เด็กฝาแฝดคนหนึ่งตายในกองเพลิง</text>
  <text x="270" y="711" font-size="20" font-weight="700" fill="#ffd84a">แต่ไม่มีใครเคยตรวจว่า เด็กที่รอดออกมาเป็นใคร</text>
  <text x="270" y="736" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#fff">Twenty years ago, one twin died in a fire.</text>
  <text x="270" y="753" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#fff">No one ever checked which twin walked out.</text>
</g>
<g id="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/></g>
</svg>'''

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{cf.DEFS}
<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="moteFar" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation=".6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="9" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="drop" x="-20%" y="-20%" width="150%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dx="9" dy="10"/><feComponentTransfer><feFuncA type="linear" slope=".42"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="subStroke" x="-10%" y="-30%" width="120%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="2.2" result="d"/><feFlood flood-color="#120e18"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset=".5" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".85"/></radialGradient>
<radialGradient id="glowW" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff1dc" stop-opacity=".7"/><stop offset=".4" stop-color="#f3cfb8" stop-opacity=".25"/><stop offset="1" stop-color="#d9a9a0" stop-opacity="0"/></radialGradient>
<radialGradient id="glowC" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#b9c8ff" stop-opacity=".6"/><stop offset=".5" stop-color="#6f86d8" stop-opacity=".18"/><stop offset="1" stop-color="#4a5aa8" stop-opacity="0"/></radialGradient>
<linearGradient id="beamC2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#c4ceff" stop-opacity=".42"/><stop offset=".7" stop-color="#8f9ae0" stop-opacity=".1"/><stop offset="1" stop-color="#7f88d8" stop-opacity="0"/></linearGradient>
</defs></svg>'''

html = f'''<title>โบสถ์น้อย เฟรมทดสอบ</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one 9:16 frame centred, toggles under it. Single dark look by choice. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#8f86ff;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); margin:0; }}
body {{ font-family:var(--font); padding:20px max(16px, env(safe-area-inset-right,0px)) 32px max(16px, env(safe-area-inset-left,0px)); display:flex; flex-direction:column; align-items:center; gap:14px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; text-align:center; }} h1 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
.frame {{ width:min(100%, 480px, calc((100vh - 130px) * .5625)); min-width:260px; max-width:100%; aspect-ratio:9/16; box-shadow:0 0 0 1px var(--line), 0 20px 50px rgba(0,0,0,.5); }}
.frame svg {{ display:block; width:100%; height:100%; }}
#guide {{ display:none; }} .frame.g #guide {{ display:inline; }} .frame.ns #subs {{ display:none; }}
.bar {{ display:flex; gap:12px; flex-wrap:wrap; justify-content:center; font-size:13px; color:var(--muted); }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:6px; padding:6px 12px; cursor:pointer; }}
button:hover {{ border-color:var(--muted); }} button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
button[aria-pressed="true"] {{ border-color:var(--accent); color:#fff; }}
p {{ max-width:560px; margin:0; font-size:13px; color:var(--muted); line-height:1.65; text-align:center; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@500&display=swap">
{DEFS}
<h1>โบสถ์น้อย · เฟรมทดสอบ ฉบับ 2<span>โบสถ์ขาววิจิตรแบบวังเก่า · ตัวละครเต็มตัว</span></h1>
<div class="frame" id="f">{FRAME}</div>
<div class="bar"><span>9:16 TikTok</span><button id="bs" type="button" aria-pressed="true">ซับ</button><button id="bg" type="button" aria-pressed="false">พื้นที่ซับ</button></div>
<p>เพดานโค้งมีซี่โครงและดอกประดับ เสาอิงหัวม้วน บัวคิ้วและลายฟันปลาใต้ชายคา หน้าต่างโค้งเรียงลึกเข้าไป แท่นบูชาหินอ่อนขาวขลิบทองซีด รูปปั้นในซุ้มคลุมผ้าขาว โคมระย้าไม่มีไฟและมีใยแมงมุม พื้นหินอ่อนลายตาราง ปูนลอก คราบชื้น รอยร้าว · มาเรียมยืนด้านหน้าในแสงจันทร์ อักเนสยืนไกลออกไปในทางเดิน มีแสงจากเทียนในมือเธอเพียงดวงเดียว</p>
<script>
const f = document.getElementById('f');
function w(id, cls, inv) {{ const b = document.getElementById(id); b.addEventListener('click', () => {{ const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on)); f.classList.toggle(cls, inv ? !on : on); }}); }}
w('bs', 'ns', true); w('bg', 'g', false);
</script>'''

open(os.path.join(HERE, "chapel-test-frame.html"), "w").write(html)
print("wrote chapel-test-frame.html", len(html) // 1024, "KB")
