#!/usr/bin/env python3
"""บ้านตรงข้าม: ฉากหลังทุกฉาก v3 (น้ำตาลผสมม่วง เฟอร์นิเจอร์แน่น บ้านไม้ทรงคอทเทจ หมอกและ low-key)
รัน: python3 scenes.py  ->  scenes.html
เฟรม 540x960 · ห้องเป็นเปอร์สเปกทีฟจุดเดียว · บรรยากาศม่วงคราม + แสงอุ่นเป็นวงจากโคม/หน้าต่าง
"""
import random, html

W, H = 540, 960
_uid = [0]
def uid(p='g'):
    _uid[0] += 1; return f'{p}{_uid[0]}'

def pts(*ps): return ' '.join(f'{x:.1f},{y:.1f}' for x, y in ps)
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)

# ---------------- palette v3: brown + purple (wood, wallpaper) with purple shadows, warm practical lights ----------------
SKY_N = ('#1c1838', '#36295e', '#5e4680')   # night sky top -> horizon
WALL = '#6b4c50'; WALL_LT = '#7c5a5a'; WALL_DK = '#4a3442'; STRIPE = '#5c4048'
WAIN = '#4a2e2a'; WAIN_LT = '#5e3a32'
CEIL = '#2e2230'; FLOOR = '#6e4634'; FLOOR_LT = '#83563e'; FLOOR_LINE = '#4a2c22'
WOOD = '#7a4a32'; WOOD_LT = '#9a6444'; WOOD_DK = '#55301f'
FAB = '#9a5a6a'; FAB_LT = '#b87a88'; TEAL = '#4f6f72'; PURP = '#6a5a8a'; PURP_LT = '#8a7aa8'
WARM = '#ffcf9e'; WARM2 = '#ffb27a'; COOL = '#a9b6ff'; MOON = '#e6e4ff'
PAPER = '#efe6e0'; RED = '#c2404f'; INK = '#2a1e28'

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stipple" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="moteBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="dof" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.4"/></filter>
<filter id="dof2" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="2.6"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="12"/></filter>
<filter id="haze" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="soft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3"/></filter>
<linearGradient id="beamW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd9b0" stop-opacity=".5"/><stop offset="1" stop-color="#ffd9b0" stop-opacity="0"/></linearGradient>
<linearGradient id="beamC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c8ccff" stop-opacity=".45"/><stop offset="1" stop-color="#c8ccff" stop-opacity="0"/></linearGradient>
<linearGradient id="winLit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe3b8"/><stop offset="1" stop-color="#f6a878"/></linearGradient>
<linearGradient id="winDark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3170"/><stop offset="1" stop-color="#241d4c"/></linearGradient>
<linearGradient id="phoneScr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4f0ff"/><stop offset="1" stop-color="#d9d0f6"/></linearGradient>
<filter id="sceneGrade" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values=".92"/><feComponentTransfer><feFuncR type="table" tableValues="0.02 0.16 0.48 0.8 0.98"/><feFuncG type="table" tableValues="0.02 0.15 0.46 0.78 0.96"/><feFuncB type="table" tableValues="0.05 0.2 0.48 0.77 0.95"/></feComponentTransfer></filter>
<radialGradient id="vig" cx=".5" cy=".46" r=".72"><stop offset=".55" stop-color="#140f30" stop-opacity="0"/><stop offset="1" stop-color="#140f30" stop-opacity=".6"/></radialGradient>
</defs></svg>'''

TEX = ('<rect width="540" height="960" filter="url(#stipple)" opacity=".08" style="mix-blend-mode:overlay"/>'
       '<rect width="540" height="960" fill="url(#vig)"/>')

# ---------------- lighting helpers ----------------
def glow(x, y, r, col=WARM, op=.9, sy=1):
    i = uid('lg')
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset=".45" stop-color="{col}" stop-opacity="{op*.35:.2f}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r*sy}" fill="url(#{i})" style="mix-blend-mode:screen"/>')

def pool(x, y, rx, ry, col=WARM, op=.55):
    """light pool on floor/wall (soft ellipse, screen)"""
    i = uid('pl')
    return (f'<defs><radialGradient id="{i}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs>'
            f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="url(#{i})" style="mix-blend-mode:screen"/>')

def shade(x, y, r, col='#2c1f5e', op=.75):
    """purple shadow over everything except around (x,y): multiply"""
    i = uid('sd')
    return (f'<defs><radialGradient id="{i}" gradientUnits="userSpaceOnUse" cx="{x}" cy="{y}" r="{r}"><stop offset=".15" stop-color="#ffffff"/>'
            f'<stop offset="1" stop-color="{col}"/></radialGradient></defs>'
            f'<rect width="540" height="960" fill="url(#{i})" opacity="{op}" style="mix-blend-mode:multiply"/>')

def beam(points, grad='beamW', op=1):
    return f'<polygon points="{points}" fill="url(#{grad})" filter="url(#haze)" opacity="{op}" style="mix-blend-mode:screen"/>'

def dust(seed, box, n, col='#fff1e0'):
    r = random.Random(seed); x0, y0, x1, y1 = box
    far = ''.join(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(1.4,2.6):.1f}" opacity="{r.uniform(.25,.5):.2f}"/>' for _ in range(n))
    near = ''.join(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(.6,1.2):.1f}" opacity="{r.uniform(.6,.95):.2f}"/>' for _ in range(n // 2))
    return f'<g fill="{col}"><g filter="url(#moteBlur)">{far}</g><g filter="url(#moteGlow)">{near}</g></g>'

def cast(shape, dx=14, dy=16, op=.45):
    return f'<g transform="translate({dx},{dy})" filter="url(#sh)" opacity="{op}" fill="#1a1238">{shape}</g>'

def stars(seed, n, y1=400):
    r = random.Random(seed)
    return ''.join(f'<circle cx="{r.uniform(0,W):.0f}" cy="{r.uniform(0,y1):.0f}" r="{r.uniform(.5,1.3):.1f}" fill="#efeaff" opacity="{r.uniform(.3,.9):.2f}"/>' for _ in range(n))

def night_sky(moon=(400, 150), seed=1, horizon=520):
    i = uid('sk')
    o = [f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKY_N[0]}"/><stop offset=".6" stop-color="{SKY_N[1]}"/><stop offset="1" stop-color="{SKY_N[2]}"/></linearGradient></defs>',
         f'<rect width="{W}" height="{horizon+40}" fill="url(#{i})"/>', stars(seed, 60, horizon - 120)]
    if moon:
        mx, my = moon
        o.append(glow(mx, my, 170, '#b9b4ff', .55))
        o.append(f'<circle cx="{mx}" cy="{my}" r="38" fill="{MOON}"/><circle cx="{mx-10}" cy="{my-8}" r="7" fill="#d4d0f4"/><circle cx="{mx+12}" cy="{my+10}" r="5" fill="#d4d0f4"/>')
    r = random.Random(seed + 7)
    for _ in range(4):  # long purple clouds
        cx = r.uniform(-40, W); cy = r.uniform(60, horizon - 200); w = r.uniform(160, 300)
        o.append(f'<path d="M {cx},{cy} q {w*.2},-26 {w*.45},-8 q {w*.25},-24 {w*.55},6 q -{w*.5},18 -{w},2 z" fill="#5a4a92" opacity=".55"/>')
    return ''.join(o)

# ---------------- one-point perspective room ----------------
class Room:
    def __init__(self, vp, x0, y0, x1, y1):
        self.vp = vp; self.x0, self.y0, self.x1, self.y1 = x0, y0, x1, y1
        self.TL, self.TR, self.BR, self.BL = (x0, y0), (x1, y0), (x1, y1), (x0, y1)
    def at(self, p, s):  # point p (on back wall plane) moved toward viewer by depth scale s>=1
        return (self.vp[0] + (p[0] - self.vp[0]) * s, self.vp[1] + (p[1] - self.vp[1]) * s)
    def P(self, face, s, a):
        if face == 'L': return lerp(self.at(self.TL, s), self.at(self.BL, s), a)
        if face == 'R': return lerp(self.at(self.TR, s), self.at(self.BR, s), a)
        if face == 'F': return lerp(self.at(self.BL, s), self.at(self.BR, s), a)
        if face == 'C': return lerp(self.at(self.TL, s), self.at(self.TR, s), a)
        if face == 'B': return lerp(lerp(self.TL, self.TR, s), lerp(self.BL, self.BR, s), a)  # back wall: s=x frac, a=y frac
    def quad(self, face, s0, s1, a0, a1, fill, extra=''):
        if face == 'B':
            p = [self.P('B', s0, a0), self.P('B', s1, a0), self.P('B', s1, a1), self.P('B', s0, a1)]
        else:
            p = [self.P(face, s0, a0), self.P(face, s1, a0), self.P(face, s1, a1), self.P(face, s0, a1)]
        return f'<polygon points="{pts(*p)}" fill="{fill}" {extra}/>'
    def shell(self, wall=WALL, wall_lt=WALL_LT, wall_dk=WALL_DK, ceil=CEIL, floor=FLOOR, planks=True):
        F = 12
        o = [f'<rect width="{W}" height="{H}" fill="{ceil}"/>',
             f'<polygon points="{pts(self.TL, self.TR, self.at(self.TR, F), self.at(self.TL, F))}" fill="{ceil}"/>',
             f'<polygon points="{pts(self.BL, self.BR, self.at(self.BR, F), self.at(self.BL, F))}" fill="{floor}"/>',
             f'<polygon points="{pts(self.TL, self.BL, self.at(self.BL, F), self.at(self.TL, F))}" fill="{wall_lt}"/>',
             f'<polygon points="{pts(self.TR, self.BR, self.at(self.BR, F), self.at(self.TR, F))}" fill="{wall_dk}"/>',
             f'<rect x="{self.x0}" y="{self.y0}" width="{self.x1-self.x0}" height="{self.y1-self.y0}" fill="{wall}"/>']
        if planks:
            for k in range(1, 12):
                a = k / 12; p = lerp(self.BL, self.BR, a)
                o.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{self.at(p, F)[0]:.1f}" y2="{self.at(p, F)[1]:.1f}" stroke="{FLOOR_LINE}" stroke-width="1.3" opacity=".7"/>')
            for s in (1.25, 1.6, 2.1, 2.8, 3.8):
                a, b = self.P('F', s, 0), self.P('F', s, 1)
                o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{FLOOR_LINE}" stroke-width="1" opacity=".45"/>')
        # skirting + crown lines
        for face in ('L', 'R'):
            o.append(self.quad(face, 1, F, .97, 1, '#3e2f62'))
        o.append(f'<rect x="{self.x0}" y="{self.y1-8}" width="{self.x1-self.x0}" height="8" fill="#3e2f62"/>')
        return ''.join(o)
    def box(self, s0, s1, u0, u1, h, top, front, side, h0=0):
        """box standing on the floor: depth s0..s1, across u0..u1 (0=left wall, 1=right wall), height h as fraction of room height"""
        Hh = self.y1 - self.y0
        f = lambda s, u: self.P('F', s, u)
        up = lambda p, s, hh: (p[0], p[1] - Hh * s * hh)
        A, B, C, D = f(s1, u0), f(s1, u1), f(s0, u1), f(s0, u0)
        a, b, c, d = up(A, s1, h), up(B, s1, h), up(C, s0, h), up(D, s0, h)
        A0, B0, C0, D0 = up(A, s1, h0), up(B, s1, h0), up(C, s0, h0), up(D, s0, h0)
        o = []
        if B[0] < self.vp[0]:   # box left of centre: we see its right side
            o.append(f'<polygon points="{pts(B0, C0, c, b)}" fill="{side}"/>')
        elif A[0] > self.vp[0]:
            o.append(f'<polygon points="{pts(A0, D0, d, a)}" fill="{side}"/>')
        if a[1] > self.vp[1] or h < 1:
            o.append(f'<polygon points="{pts(a, b, c, d)}" fill="{top}"/>')
        o.append(f'<polygon points="{pts(A0, B0, b, a)}" fill="{front}"/>')
        return ''.join(o)

# ---------------- props ----------------
def lamp_desk(x, y, s=1, on=True):
    o = (f'<g transform="translate({x},{y}) scale({s})"><rect x="-14" y="-4" width="28" height="6" rx="2" fill="#3a2c58"/>'
         f'<path d="M 0,-4 L -10,-46 L 14,-74" fill="none" stroke="#3a2c58" stroke-width="4"/>'
         f'<path d="M 4,-84 L 34,-70 L 26,-56 L 0,-66 Z" fill="#4c3a70"/><path d="M 26,-56 L 0,-66 L 14,-58 Z" fill="{WARM if on else "#6a5a90"}"/></g>')
    if on:
        o += glow(x + 18 * s, y - 60 * s, 90 * s, WARM, .8) + pool(x + 30 * s, y + 6, 120 * s, 40 * s, WARM, .55)
    return o

def frame_pic(x, y, w, h, col='#d7cde6', inner='#7d6aa8'):
    return (cast(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>', 5, 6, .5) +
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD_DK}"/><rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" fill="{inner}"/>'
            f'<path d="M {x+4},{y+h-4} L {x+w*.45},{y+h*.5} L {x+w-4},{y+h-8} Z" fill="#5a4888"/><circle cx="{x+w-12}" cy="{y+12}" r="4" fill="{col}"/>')

def corkboard(x, y, w, h, seed=3, lit=True):
    r = random.Random(seed)
    o = [cast(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>', 6, 8, .55),
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{WOOD_DK}"/><rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" fill="#a77a6c"/>']
    pins = []
    for i in range(9):
        px = x + 16 + r.uniform(0, w - 50); py = y + 14 + r.uniform(0, h - 50); a = r.uniform(-10, 10)
        o.append(f'<g transform="rotate({a:.0f} {px+14:.0f} {py+14:.0f})"><rect x="{px:.0f}" y="{py:.0f}" width="30" height="34" fill="{PAPER}"/><rect x="{px+3:.0f}" y="{py+3:.0f}" width="24" height="20" fill="#6c5b98"/></g>')
        pins.append((px + 15, py + 3))
    o.append(f'<polyline points="{pts(*pins)}" fill="none" stroke="{RED}" stroke-width="1.4"/>')
    o.append(f'<line x1="{pins[0][0]:.0f}" y1="{pins[0][1]:.0f}" x2="{pins[5][0]:.0f}" y2="{pins[5][1]:.0f}" stroke="{RED}" stroke-width="1.4"/>')
    o.append(''.join(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="2.6" fill="#ffd34a"/>' for px, py in pins))
    o.append(f'<rect x="{x+w-46}" y="{y+h-30}" width="34" height="18" fill="#ffe58a" transform="rotate(-6 {x+w-30} {y+h-20})"/>')
    return ''.join(o)

def pole_lines(xs, y_top, y_base):
    o = []
    for x in xs:
        o.append(f'<rect x="{x-4}" y="{y_top}" width="8" height="{y_base-y_top}" fill="#2a2150"/><rect x="{x-22}" y="{y_top+14}" width="44" height="5" fill="#2a2150"/>')
    for k in range(3):
        d = ' '.join(f'{"M" if j==0 else "Q"} ' + (f'{xs[j]},{y_top+16+k*6}' if j == 0 else f'{(xs[j-1]+xs[j])/2},{y_top+40+k*6} {xs[j]},{y_top+16+k*6}') for j in range(len(xs)))
        o.append(f'<path d="M -20,{y_top+30+k*6} Q {xs[0]/2-10},{y_top+44+k*6} {xs[0]},{y_top+16+k*6} ' +
                 ''.join(f'Q {(xs[j-1]+xs[j])/2},{y_top+40+k*6} {xs[j]},{y_top+16+k*6} ' for j in range(1, len(xs))) +
                 f'Q {(xs[-1]+W+20)/2},{y_top+40+k*6} {W+20},{y_top+26+k*6}" fill="none" stroke="#221a44" stroke-width="1.4"/>')
    return ''.join(o)

def tree_dark(x, y, s=1, col='#2c2456'):
    return (f'<g transform="translate({x},{y}) scale({s})" fill="{col}"><rect x="-6" y="-10" width="12" height="70"/>'
            f'<circle cx="0" cy="-40" r="48"/><circle cx="-36" cy="-14" r="34"/><circle cx="34" cy="-20" r="36"/><circle cx="-6" cy="-80" r="30"/></g>')

def frame_svg(content):
    return (f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><g filter="url(#sceneGrade)">{content}</g>{TEX}</svg>')

def fog(y, h=90, col='#b8a8d8', op=.28):
    """low ground mist band (screen)"""
    i = uid('fg')
    return (f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{col}" stop-opacity="{op}"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs>'
            f'<rect x="-20" y="{y}" width="580" height="{h}" fill="url(#{i})" filter="url(#haze)" style="mix-blend-mode:screen"/>')

def walls_detail(R, wall_stripe=STRIPE, wain=WAIN, wain_lt=WAIN_LT, wain_h=.34, stripes=True, F=12):
    """wallpaper stripes above a wood wainscot on back + side walls, in perspective"""
    o = []
    top = 1 - wain_h
    if stripes:
        for k in range(1, 14):
            x = R.x0 + (R.x1 - R.x0) * k / 14
            o.append(f'<line x1="{x:.1f}" y1="{R.y0}" x2="{x:.1f}" y2="{R.y0 + (R.y1-R.y0)*top:.1f}" stroke="{wall_stripe}" stroke-width="3" opacity=".55"/>')
        for face in ('L', 'R'):
            s = 1.0
            while s < 4.6:
                a, b = R.P(face, s, 0), R.P(face, s, top)
                o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{wall_stripe}" stroke-width="{3*s:.1f}" opacity=".5"/>')
                s *= 1.12
    # wainscot: back wall + both side walls
    o.append(f'<rect x="{R.x0}" y="{R.y0 + (R.y1-R.y0)*top:.1f}" width="{R.x1-R.x0}" height="{(R.y1-R.y0)*wain_h:.1f}" fill="{wain}"/>')
    o.append(f'<rect x="{R.x0}" y="{R.y0 + (R.y1-R.y0)*top - 4:.1f}" width="{R.x1-R.x0}" height="5" fill="{wain_lt}"/>')
    for face in ('L', 'R'):
        o.append(R.quad(face, 1, F, top, 1, wain))
        o.append(R.quad(face, 1, F, top - .015, top + .005, wain_lt))
        for s in (1.15, 1.35, 1.6, 1.95, 2.4, 3.0, 3.8):
            a, b = R.P(face, s, top + .04), R.P(face, s, .97)
            o.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#341e1c" stroke-width="{1.2*s:.1f}" opacity=".6"/>')
    for k in range(1, 7):
        x = R.x0 + (R.x1 - R.x0) * k / 7
        o.append(f'<line x1="{x:.1f}" y1="{R.y0 + (R.y1-R.y0)*(top+.04):.1f}" x2="{x:.1f}" y2="{R.y1-6:.1f}" stroke="#341e1c" stroke-width="1.4" opacity=".6"/>')
    return ''.join(o)

def on_floor(R, s, u, h=0):
    """screen point standing on the floor at depth s, across u, raised by h (fraction of room height)"""
    p = R.P('F', s, u)
    return (p[0], p[1] - (R.y1 - R.y0) * s * h)

def books(x, y, k=1, cols=('#7a3a3a', '#3e5a62', '#c9a46a', '#5a4a7a', '#8a6a4a')):
    o = []; xx = x
    for i, c in enumerate(cols):
        w = (5 + (i % 3)) * k; hh = (18 + (i * 5) % 9) * k
        o.append(f'<rect x="{xx:.1f}" y="{y-hh:.1f}" width="{w:.1f}" height="{hh:.1f}" fill="{c}"/>')
        xx += w + .6 * k
    return ''.join(o)

def plant(x, y, k=1, pot='#8a5a44'):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({k})"><path d="M -12,0 L 12,0 L 9,-20 L -9,-20 Z" fill="{pot}"/><rect x="-11" y="-22" width="22" height="4" fill="#6a4232"/>'
            f'<ellipse cx="-8" cy="-34" rx="7" ry="15" fill="#3f6250" transform="rotate(-25 -8 -34)"/><ellipse cx="8" cy="-36" rx="7" ry="16" fill="#4f7660" transform="rotate(22 8 -36)"/>'
            f'<ellipse cx="0" cy="-42" rx="6" ry="16" fill="#5e8a6e"/></g>')

def mug(x, y, k=1, col='#e6dcd0'):
    return (f'<g transform="translate({x:.1f},{y:.1f}) scale({k})"><rect x="-6" y="-12" width="12" height="12" rx="2" fill="{col}"/><path d="M 6,-9 C 10,-9 10,-3 6,-3" fill="none" stroke="{col}" stroke-width="2"/></g>')

# ---------------- the house across v3: brown wooden cottage, same design everywhere ----------------
def house3d(x, y, s=1, mode='night'):
    """mode: day | morning | night | fight | dark | shadow | party"""
    day = mode in ('day', 'morning')
    lit_lr = mode in ('night', 'fight', 'shadow', 'party')
    lit_up = mode in ('night', 'party')
    front = '#9a7c70' if day else '#6e5452'
    front_lt = '#ae8e80' if day else '#7e6260'
    side = '#6e5660' if day else '#45343e'
    roof = '#4a3232' if day else '#2e1f22'; roof_sd = '#38262a' if day else '#21161a'; roof_lt = '#5e4040' if day else '#3a282c'
    trim = '#efe2d0' if day else '#c4b2a4'
    shutter = '#4a5a52' if day else '#2e3a36'
    brick = '#7a4a3c' if day else '#4e2e28'
    win_lr = 'url(#winLit)' if lit_lr else ('#8e86b8' if day else 'url(#winDark)')
    win_up = 'url(#winLit)' if lit_up else ('#8e86b8' if day else 'url(#winDark)')
    dx, dt, db = 92, 14, -18
    o = []
    # chimney behind the roof
    o.append(f'<rect x="{80}" y="-372" width="26" height="70" fill="{brick}"/><rect x="76" y="-378" width="34" height="8" fill="{roof}"/>')
    o.append(''.join(f'<line x1="80" y1="{yy}" x2="106" y2="{yy}" stroke="#3a2420" stroke-width="1" opacity=".6"/>' for yy in range(-366, -302, 8)))
    # side face
    o.append(f'<polygon points="{pts((130,-230),(130+dx,-230+dt),(130+dx,db),(130,0))}" fill="{side}"/>')
    o.append(''.join(f'<line x1="130" y1="{yy}" x2="{130+dx}" y2="{yy + dt*(1 - (yy+230)/230) + db*((yy+230)/230):.0f}" stroke="#2e2028" stroke-width="1" opacity=".35"/>' for yy in range(-216, 0, 14)))
    o.append(f'<polygon points="{pts((150,-170),(196,-165),(196,-110),(150,-112))}" fill="{win_up if lit_up else ("#6e66a0" if day else "#231c3c")}"/><polygon points="{pts((146,-174),(200,-168),(200,-162),(146,-168))}" fill="{trim}"/>')
    # front face + clapboard siding
    o.append(f'<rect x="-130" y="-230" width="260" height="230" fill="{front}"/><rect x="-130" y="-230" width="70" height="230" fill="{front_lt}" opacity=".55"/>')
    o.append(''.join(f'<rect x="-130" y="{yy}" width="260" height="2" fill="#3a2a2a" opacity=".22"/>' for yy in range(-224, 0, 12)))
    # roof: front gable + side plane with dormer
    o.append(f'<polygon points="{pts((-150,-222),(0,-334),(150,-222))}" fill="{roof}"/>')
    o.append(f'<polygon points="{pts((0,-334),(dx,-334+dt*.8),(150+dx,-222+dt),(150,-222))}" fill="{roof_sd}"/>')
    for t in (.25, .5, .75):   # shingle rows on the side plane
        o.append(f'<line x1="{150*t + dx*0:.0f}" y1="{-334 + 112*t:.0f}" x2="{150*t+dx:.0f}" y2="{-334+112*t+dt*.9:.0f}" stroke="{roof_lt}" stroke-width="1.4" opacity=".7"/>')
    # dormer on the side roof
    o.append(f'<polygon points="{pts((98,-284),(122,-306),(146,-280),(146,-258),(98,-262))}" fill="{side}"/><polygon points="{pts((94,-282),(122,-310),(150,-278),(146,-276),(122,-302),(98,-280))}" fill="{roof}"/>')
    o.append(f'<rect x="110" y="-284" width="24" height="20" fill="{win_up}"/><path d="M 122,-284 L 122,-264" stroke="{trim}" stroke-width="2"/>')
    # gable wall with scalloped shingles + round window
    o.append(f'<polygon points="{pts((-120,-230),(0,-314),(120,-230))}" fill="{front_lt}"/>')
    sc = []
    for row, yy in enumerate(range(-296, -232, 9)):
        half = (yy + 314) / 84 * 120
        xx = -half + (row % 2) * 6
        while xx < half - 6:
            sc.append(f'<path d="M {xx:.0f},{yy} a 6,6 0 0 0 12,0" fill="none" stroke="{front}" stroke-width="1.6"/>')
            xx += 12
    o.append(''.join(sc))
    o.append(f'<polygon points="{pts((-154,-218),(0,-338),(154,-218),(144,-214),(0,-326),(-144,-214))}" fill="{trim}"/>')
    o.append(f'<circle cx="0" cy="-268" r="18" fill="{trim}"/><circle cx="0" cy="-268" r="13" fill="{win_up}"/><path d="M 0,-281 L 0,-255 M -13,-268 L 13,-268" stroke="{trim}" stroke-width="2"/>')
    if lit_up: o.append(glow(0, -268, 46, WARM, .6))
    # upstairs windows with shutters + flower boxes
    for wx in (-100, 34):
        o.append(f'<rect x="{wx-14}" y="-206" width="12" height="70" fill="{shutter}"/><rect x="{wx+68}" y="-206" width="12" height="70" fill="{shutter}"/>')
        o.append(''.join(f'<line x1="{xx}" y1="{yy}" x2="{xx+10}" y2="{yy}" stroke="#1e2622" stroke-width="1"/>' for xx in (wx-13, wx+69) for yy in range(-200, -140, 7)))
        o.append(f'<rect x="{wx}" y="-206" width="66" height="70" fill="{trim}"/><rect x="{wx+5}" y="-201" width="56" height="60" fill="{win_up}"/>')
        o.append(f'<path d="M {wx+33},-201 L {wx+33},-141 M {wx+5},-171 L {wx+61},-171" stroke="{trim}" stroke-width="2.6"/>')
        o.append(f'<rect x="{wx-4}" y="-138" width="74" height="12" fill="{WOOD_DK if day else "#3a2018"}"/>' + ''.join(f'<circle cx="{wx+2+i*9}" cy="{-140+(i%2)*3}" r="4" fill="{("#e79ab0" if i%2 else "#f2d6a8") if day else ("#a8607e" if i%2 else "#b8a070")}"/>' for i in range(8)))
        o.append(''.join(f'<ellipse cx="{wx+6+i*12}" cy="-137" rx="6" ry="3.6" fill="{"#5d7f6a" if day else "#2c3e34"}"/>' for i in range(6)))
        if lit_up: o.append(glow(wx + 33, -170, 52, WARM, .5))
    # porch roof + columns
    o.append(f'<polygon points="{pts((-142,-100),(142,-100),(154,-84),(-154,-84))}" fill="{roof}"/><rect x="-154" y="-86" width="308" height="6" fill="{trim}"/>')
    o.append(''.join(f'<path d="M {xx},-84 a 7,7 0 0 0 14,0" fill="{trim}"/>' for xx in range(-150, 150, 14)))   # gingerbread trim
    for cx in (-138, -20, 134):
        o.append(f'<rect x="{cx-5}" y="-80" width="10" height="80" fill="{trim}"/><rect x="{cx+2}" y="-80" width="3" height="80" fill="#8a7a70" opacity=".6"/>')
    # living-room window (ground floor left)
    o.append(f'<rect x="-124" y="-72" width="96" height="58" fill="{trim}"/><rect x="-119" y="-67" width="86" height="48" fill="{win_lr}"/>')
    cur = '#f2c0b8' if lit_lr else ('#b89aa8' if day else '#3a2c3e')
    if mode == 'shadow':
        o.append(f'<rect x="-119" y="-67" width="86" height="48" fill="{cur}" opacity=".9"/>' + ''.join(f'<line x1="{-114+i*10}" y1="-67" x2="{-114+i*10}" y2="-19" stroke="#e0a49c" stroke-width="1.6"/>' for i in range(9)))
    elif mode == 'dark':
        o.append(f'<rect x="-119" y="-67" width="86" height="48" fill="{cur}"/>')
    elif mode == 'fight':
        o.append(f'<path d="M -119,-67 L -98,-67 C -99,-50 -100,-34 -103,-19 L -119,-19 Z" fill="{cur}"/><path d="M -33,-67 L -60,-67 C -58,-50 -57,-34 -54,-19 L -33,-19 Z" fill="{cur}"/>')
    else:
        o.append(f'<path d="M -119,-67 L -108,-67 C -109,-50 -109,-34 -112,-19 L -119,-19 Z" fill="{cur}"/><path d="M -33,-67 L -44,-67 C -43,-50 -43,-34 -40,-19 L -33,-19 Z" fill="{cur}"/>')
    if mode == 'party':
        o.append(''.join(f'<circle cx="{-106+i*16}" cy="{-56+(i%2)*8}" r="5.5" fill="{c}"/>' for i, c in enumerate(['#ff9fb4', '#b9a2ff', '#ffe08a', '#9fe0c8', '#ff9fb4', '#b9a2ff'])))
    o.append(f'<path d="M -76,-67 L -76,-19" stroke="{trim}" stroke-width="2.6"/>')
    if lit_lr: o.append(glow(-76, -42, 84, WARM, .55))
    # front door: deep red-brown with a fan light, twin lanterns
    door = '#6a3028' if day else '#3e1e1c'
    o.append(f'<rect x="18" y="-80" width="50" height="80" fill="{trim}"/><rect x="23" y="-70" width="40" height="70" fill="{door}"/>')
    o.append(f'<path d="M 23,-70 A 20,10 0 0 1 63,-70 Z" fill="{win_lr if lit_lr else trim}"/>')
    o.append(f'<rect x="28" y="-62" width="30" height="24" fill="none" stroke="#2a1210" stroke-width="1.4" opacity=".6"/><rect x="28" y="-32" width="30" height="26" fill="none" stroke="#2a1210" stroke-width="1.4" opacity=".6"/><circle cx="58" cy="-34" r="2.2" fill="#d9b25a"/>')
    for lx in (6, 80):
        o.append(f'<rect x="{lx}" y="-66" width="8" height="14" rx="2" fill="{WARM if not day else "#d8c8a0"}"/><path d="M {lx-1},-66 L {lx+4},-72 L {lx+9},-66 Z" fill="#2a1e1a"/>')
        if not day: o.append(glow(lx + 4, -59, 40, WARM, .8))
    if not day: o.append(pool(43, 8, 90, 22, WARM, .45))
    # porch rail with balusters, steps
    o.append(f'<path d="M -154,-30 L 6,-30 M 82,-30 L 154,-30" stroke="{trim}" stroke-width="3"/>')
    o.append(''.join(f'<rect x="{xx}" y="-30" width="3" height="30" fill="{trim}"/>' for xx in list(range(-150, 6, 10)) + list(range(84, 154, 10))))
    o.append(f'<rect x="12" y="0" width="62" height="8" fill="{trim}"/><rect x="6" y="8" width="74" height="8" fill="#8a7a70"/><rect x="0" y="16" width="86" height="8" fill="{trim}" opacity=".85"/>')
    # porch string lights + hanging baskets
    o.append(f'<path d="M -150,-80 Q -80,-66 -20,-80 Q 60,-66 150,-80" fill="none" stroke="#2a1a14" stroke-width="1"/>')
    for t in [i / 14 for i in range(15)]:
        xx = -150 + 300 * t; yy = -80 + 14 * (4 * ((t * 2) % 1) * (1 - (t * 2) % 1))
        o.append(f'<circle cx="{xx:.0f}" cy="{yy:.0f}" r="2" fill="#ffe8a8"/>' + (glow(xx, yy, 10, WARM, .7) if not day else ''))
    for hx in (-80, 104):
        o.append(f'<line x1="{hx}" y1="-84" x2="{hx}" y2="-66" stroke="#2a1a14" stroke-width="1"/><path d="M {hx-9},-66 L {hx+9},-66 L {hx+6},-58 L {hx-6},-58 Z" fill="#8a5a3a"/>'
                 + ''.join(f'<path d="M {hx+dx},-62 C {hx+dx-2},-52 {hx+dx+2},-44 {hx+dx},-38" fill="none" stroke="{"#5e8a6e" if day else "#2e4a3a"}" stroke-width="2.4"/>' for dx in (-6, -2, 3, 7)))
    # brick foundation strip
    o.append(f'<rect x="-130" y="-8" width="260" height="10" fill="{brick}"/>' + ''.join(f'<line x1="{xx}" y1="-8" x2="{xx}" y2="2" stroke="#2a1410" stroke-width="1" opacity=".5"/>' for xx in range(-124, 130, 12)))
    # rose bushes
    for bx in (-152, -92, 108):
        o.append(f'<ellipse cx="{bx+24}" cy="2" rx="34" ry="18" fill="{"#4e6a58" if day else "#24302a"}"/><ellipse cx="{bx+12}" cy="-6" rx="18" ry="12" fill="{"#668a70" if day else "#2e3e34"}"/>')
        o.append(''.join(f'<circle cx="{bx+6+i*12}" cy="{-4+(i%2)*6}" r="3.2" fill="{"#e79ab0" if day else "#8a4e66"}"/>' for i in range(4)))
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(o)}</g>'

def side_house(x, y, s=1, flip=False, lit=True):
    """neighbour houses, darker, for depth"""
    t = f'translate({x},{y}) scale({-s if flip else s},{s})'
    w = 'url(#winLit)' if lit else 'url(#winDark)'
    return (f'<g transform="{t}"><polygon points="{pts((-90,-160),(0,-240),(90,-160))}" fill="#2a1e24"/><rect x="-80" y="-160" width="160" height="160" fill="#3e2e34"/>'
            f'<rect x="-60" y="-130" width="34" height="40" fill="{w}"/><rect x="14" y="-130" width="34" height="40" fill="url(#winDark)"/><rect x="-24" y="-60" width="30" height="60" fill="#22161a"/></g>')

def street(mode='night', moon=(420, 140), extra_back='', extra_front='', with_house=True, seed=5, hy=600, hs=1.15):
    day = mode in ('day', 'morning')
    o = []
    if day:
        i = uid('sk')
        top, mid, bot = (('#6c5ca8', '#a088c4', '#e2bcc8') if mode == 'day' else ('#7a6cb4', '#b49ccc', '#f0c8c4'))
        o.append(f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".6" stop-color="{mid}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{i})"/>')
        o.append(glow(460 if mode == 'day' else 80, 140, 220, '#fff0d8', .6))
        r = random.Random(seed)
        for _ in range(4):
            cx = r.uniform(-40, W); cy = r.uniform(60, 300); w = r.uniform(160, 280)
            o.append(f'<path d="M {cx},{cy} q {w*.2},-26 {w*.45},-8 q {w*.25},-24 {w*.55},6 q -{w*.5},18 -{w},2 z" fill="#f2dcef" opacity=".5"/>')
    else:
        o.append(night_sky(moon, seed, hy - 60))
        if moon:   # a thin cloud drifting across the moon
            o.append(f'<path d="M {moon[0]-90},{moon[1]+10} q 40,-22 90,-6 q 40,-16 80,4 q -70,18 -170,2 z" fill="#3e3266" opacity=".75"/>')
    r = random.Random(seed + 3); x = -10
    col = '#7a6898' if day else '#2a2048'
    while x < W:
        w = r.randint(28, 50); h = r.randint(60, 150)
        o.append(f'<rect x="{x}" y="{hy-170-h}" width="{w}" height="{h+60}" fill="{col}" filter="url(#dof2)"/>')
        if not day:
            o.append(''.join(f'<rect x="{x+4+r.randint(0,w-10)}" y="{hy-160-h+r.randint(0,h)}" width="2.4" height="3" fill="{WARM}" opacity=".7"/>' for _ in range(w // 6)))
        x += w + 2
    tcol = '#4e5e56' if day else '#1c1a2a'
    o.append(f'<g filter="url(#dof)">{tree_dark(40, hy-120, 1.3, tcol)}{tree_dark(520, hy-130, 1.2, tcol)}</g>')
    o.append(f'<g filter="url(#dof)" opacity=".95">{side_house(-40, hy-40, .9, lit=not day)}{side_house(600, hy-40, .9, True, lit=not day)}</g>')
    o.append(extra_back)
    o.append(f'<rect x="0" y="{hy-60}" width="{W}" height="80" fill="{"#5a6a4e" if day else "#22281e"}"/>')
    if with_house:
        o.append(house3d(250, hy, hs, mode))
    # big leafy tree beside the house (front of the neighbour), lit from the porch at night
    tx = 250 + 200 * hs; ty = hy + 10
    leaf = ('#4e6a52', '#5e7e60', '#6e9070') if day else ('#20281e', '#2a3626', '#36442e')
    o.append(f'<rect x="{tx-8}" y="{ty-170}" width="16" height="180" fill="{"#5a4030" if day else "#2a1e18"}"/><path d="M {tx},{ty-120} L {tx-40},{ty-170} M {tx},{ty-140} L {tx+36},{ty-190}" stroke="{"#5a4030" if day else "#2a1e18"}" stroke-width="7"/>')
    r2 = random.Random(seed + 9)
    for _ in range(26):
        cx = tx + r2.uniform(-90, 90); cy = ty - 200 + r2.uniform(-90, 50); rr = r2.uniform(26, 44)
        o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{r2.choice(leaf)}"/>')
    if not day:
        o.append(f'<path d="M {tx-90},{ty-180} C {tx-60},{ty-260} {tx-20},{ty-270} {tx-10},{ty-200}" fill="none" stroke="#c89a70" stroke-width="10" opacity=".25" filter="url(#soft)"/>')   # warm rim on the leaves facing the porch
    # stone path, mailbox, picket fence
    o.append(f'<polygon points="{pts((250+10*hs,hy+28*hs),(250+90*hs,hy+28*hs),(330,hy+40),(196,hy+40))}" fill="{"#b8a898" if day else "#4e4448"}"/>')
    fc = '#e8dccb' if day else '#8a7c74'
    o.append(f'<rect x="0" y="{hy+4}" width="{W}" height="4" fill="{fc}"/><rect x="0" y="{hy+18}" width="{W}" height="4" fill="{fc}"/>'
             + ''.join(f'<path d="M {xx},{hy+30} L {xx},{hy-6} L {xx+3},{hy-10} L {xx+6},{hy-6} L {xx+6},{hy+30} Z" fill="{fc}"/>' for xx in list(range(0, 190, 14)) + list(range(340, W, 14))))
    for (bx_, by_) in ((60, hy + 2), (440, hy + 4)):   # flower beds along the fence
        o.append(f'<ellipse cx="{bx_}" cy="{by_}" rx="70" ry="16" fill="{"#4e6a52" if day else "#1e2a20"}"/>' + ''.join(f'<circle cx="{bx_-56+i*14}" cy="{by_-6+(i%3)*4}" r="4.4" fill="{["#e79ab0","#f2d6a8","#c87a8a","#b8a2e0"][i%4] if day else ["#8a4e66","#8a7a58","#7a4a5a","#5a4e7a"][i%4]}"/>' for i in range(9)))
    for t_ in (.2, .5, .8):   # little garden lights along the path
        px_ = 250 + 10 * hs + (80 * hs) * 0 + (196 - (250 + 10 * hs)) * t_; py_ = hy + 28 * hs + (12) * t_
        o.append(f'<rect x="{px_-2:.0f}" y="{py_-14:.0f}" width="4" height="14" fill="#2a1e1a"/><circle cx="{px_:.0f}" cy="{py_-16:.0f}" r="3.4" fill="{WARM if not day else "#d8c8a0"}"/>' + (glow(px_, py_ - 16, 18, WARM, .8) if not day else ''))
    # stone gate pillars with lanterns at the path, clipped hedges, topiary pots by the steps
    for gx in (186, 338):
        o.append(f'<rect x="{gx-10}" y="{hy-30}" width="20" height="60" fill="{"#b8aa9a" if day else "#5a5250"}"/><rect x="{gx-13}" y="{hy-34}" width="26" height="6" fill="{"#d8ccbc" if day else "#7a706c"}"/>'
                 + ''.join(f'<line x1="{gx-10}" y1="{yy}" x2="{gx+10}" y2="{yy}" stroke="#3a3230" stroke-width="1" opacity=".4"/>' for yy in range(hy - 22, hy + 30, 9))
                 + f'<rect x="{gx-6}" y="{hy-52}" width="12" height="18" rx="2" fill="{WARM if not day else "#e8dcc0"}"/><path d="M {gx-8},{hy-52} L {gx},{hy-60} L {gx+8},{hy-52} Z" fill="#1e1a18"/>' + (glow(gx, hy - 44, 34, WARM, .85) if not day else ''))
    hedge = '#3e5a46' if day else '#1c2a20'; hedge_lt = '#4e6e56' if day else '#26362a'
    for (x0_, x1_) in ((0, 176), (348, W)):
        o.append(f'<rect x="{x0_}" y="{hy-8}" width="{x1_-x0_}" height="30" rx="8" fill="{hedge}"/><rect x="{x0_}" y="{hy-8}" width="{x1_-x0_}" height="8" rx="4" fill="{hedge_lt}"/>')
    for tx_ in (250 + 4 * hs, 250 + 92 * hs):
        o.append(f'<path d="M {tx_-10},{hy+22*hs} L {tx_+10},{hy+22*hs} L {tx_+8},{hy+8*hs} L {tx_-8},{hy+8*hs} Z" fill="#e8dccb"/><rect x="{tx_-1.5}" y="{hy-10*hs}" width="3" height="{18*hs}" fill="#4a3a2a"/><circle cx="{tx_}" cy="{hy-16*hs}" r="{12*hs}" fill="{hedge_lt}"/>')
    o.append(f'<rect x="150" y="{hy-24}" width="4" height="54" fill="#3a2a24"/><rect x="138" y="{hy-40}" width="28" height="18" rx="6" fill="{"#7a3a34" if day else "#4a2422"}"/><rect x="164" y="{hy-40}" width="3" height="10" fill="#d9b25a"/>')
    o.append(f'<polygon points="{pts((0,hy+30),(W,hy+30),(W,hy+46),(0,hy+46))}" fill="{"#b0a2b0" if day else "#4a4050"}"/>')
    o.append(f'<rect x="0" y="{hy+46}" width="{W}" height="{H-hy-46}" fill="{"#7a6e88" if day else "#2e2838"}"/>')
    o.append(''.join(f'<rect x="{xx}" y="{hy+150}" width="52" height="6" fill="{"#e0d6e4" if day else "#6e6480"}" opacity=".7"/>' for xx in range(0, W, 96)))
    o.append(pole_lines([90, 470], hy - 360, hy + 30))
    if not day:
        o.append(fog(hy - 40, 110, '#9a8cc8', .3))
    o.append(extra_front)
    return ''.join(o)

def window_fg(lit_inside=WARM, night=True, sill=True):
    """the hero's own window: dark wood frame as a back-lit foreground with rim light"""
    fr = '#2a1a18' if night else '#4a2e26'; rim = '#c2a0e0' if night else '#f0dccc'; wall = '#3a2630' if night else '#5a3e40'
    o = [f'<path d="M 0,0 L {W},0 L {W},{H} L 0,{H} Z M 52,110 L 488,110 L 488,640 L 52,640 Z" fill="{wall}" fill-rule="evenodd"/>']
    o.append(f'<path d="M 36,96 L 504,96 L 504,652 L 36,652 Z M 52,110 L 488,110 L 488,640 L 52,640 Z" fill="{fr}" fill-rule="evenodd"/>')
    o.append(f'<rect x="262" y="110" width="16" height="530" fill="{fr}"/><rect x="52" y="368" width="436" height="12" fill="{fr}"/>')
    o.append(f'<path d="M 52,110 L 52,640 M 278,110 L 278,640 M 52,380 L 488,380" stroke="{rim}" stroke-width="2" opacity=".6"/>')
    o.append(f'<path d="M 0,40 L 74,40 C 86,240 64,440 96,720 L 0,720 Z" fill="#4a2a38"/><path d="M 74,40 C 86,240 64,440 96,720 L 88,720 C 58,440 78,240 66,40 Z" fill="{rim}" opacity=".45"/>')
    o.append(f'<path d="M {W},40 L 466,40 C 454,240 476,440 444,720 L {W},720 Z" fill="#40243a"/><path d="M 466,40 C 454,240 476,440 444,720 L 452,720 C 482,440 462,240 474,40 Z" fill="{rim}" opacity=".4"/>')
    o.append(f'<rect x="0" y="30" width="{W}" height="12" rx="6" fill="#6a4a3a"/>')
    o.append(f'<polygon points="{pts((20,640),(520,640),(540,676),(0,676))}" fill="#6a4232"/><polygon points="{pts((20,640),(520,640),(516,646),(24,646))}" fill="{rim}" opacity=".55"/>')
    o.append(f'<rect x="0" y="676" width="{W}" height="284" fill="{"#2a1a1e" if night else "#4a3034"}"/>')
    if sill:
        o.append(cast('<rect x="96" y="596" width="48" height="44"/>', 10, 6, .5) + plant(120, 640, 1.1))
        o.append(mug(398, 640, 1.4))
        o.append(f'<path d="M 392,604 C 388,594 398,590 394,580 M 404,604 C 400,594 410,590 406,580" fill="none" stroke="#ffffff" stroke-width="1.4" opacity=".5"/>')
        o.append(books(232, 640, 1.2) + f'<rect x="300" y="630" width="56" height="10" fill="#c9b49a" transform="rotate(-4 328 635)"/>')
        o.append(f'<path d="M 410,740 L 432,690 L 486,690 L 466,740 Z" fill="#5a3a2e"/>' + (glow(458, 712, 110, lit_inside, .7) if lit_inside else ''))
        o.append(f'<rect x="60" y="716" width="130" height="24" rx="3" fill="#3a2420"/><rect x="64" y="720" width="122" height="16" fill="#4e3028"/>')
        o.append(f'<rect x="210" y="722" width="90" height="14" fill="{PAPER}" opacity=".85" transform="rotate(-3 255 729)"/><rect x="220" y="712" width="70" height="12" fill="#d9c8b8" opacity=".8" transform="rotate(4 255 718)"/>')
    return ''.join(o)

# ---------------- new rooms: police station · ground-floor living room · 2nd-floor family room ----------------
def sofa(R, s0, s1, u0, u1, col='#7a5a6e', dk='#4e3446', lt='#94728a', back='L'):
    """sofa: seat + back + arms. back='L' means the backrest is against the left side (sofa faces right); 'B' faces the viewer"""
    o = []
    if back == 'B':
        o.append(R.box(s0, s0 + .08, u0, u1, .24, lt, dk, col))
        o.append(R.box(s0 + .08, s1, u0, u1, .11, lt, dk, col))
        o.append(R.box(s0 + .08, s1, u0, u0 + .05, .17, lt, dk, col))
        o.append(R.box(s0 + .08, s1, u1 - .05, u1, .17, lt, dk, col))
    else:
        o.append(R.box(s0, s1, u0, u0 + .06, .24, lt, dk, col))
        o.append(R.box(s0, s1, u0 + .06, u1, .11, lt, dk, col))
        o.append(R.box(s0, s0 + .06, u0, u1, .17, lt, dk, col))
        o.append(R.box(s1 - .06, s1, u0, u1, .17, lt, dk, col))
    return ''.join(o)

def cushions(R, pts_list, cols=('#c88a6a', '#8a7aa8', '#b85a6a')):
    o = []
    for (s_, u_, h_), c in zip(pts_list, cols):
        p = on_floor(R, s_, u_, h_)
        o.append(f'<rect x="{p[0]-14*s_:.0f}" y="{p[1]-20*s_:.0f}" width="{28*s_:.0f}" height="{22*s_:.0f}" rx="{6*s_:.0f}" fill="{c}"/>')
    return ''.join(o)

def police_station():
    """detective squad room at night: rows of desks, case board, blinds, fluorescent panels"""
    R = Room((270, 420), 110, 220, 430, 560)
    o = [R.shell(wall='#5e5258', wall_lt='#6e6066', wall_dk='#463c44', ceil='#2a2428', floor='#4a4044', planks=False)]
    # floor tiles
    for k in range(1, 8):
        p = lerp(R.BL, R.BR, k / 8); q = R.at(p, 12)
        o.append(f'<line x1="{p[0]:.0f}" y1="{p[1]:.0f}" x2="{q[0]:.0f}" y2="{q[1]:.0f}" stroke="#3a3034" stroke-width="1.2"/>')
    for s_ in (1.2, 1.5, 1.9, 2.5, 3.4):
        a, b = R.P('F', s_, 0), R.P('F', s_, 1); o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#3a3034" stroke-width="1"/>')
    o.append(R.quad('L', 1, 12, .72, 1, '#3e3438') + R.quad('R', 1, 12, .72, 1, '#342c30') + f'<rect x="{R.x0}" y="{R.y0+(R.y1-R.y0)*.72:.0f}" width="{R.x1-R.x0}" height="{(R.y1-R.y0)*.28:.0f}" fill="#46393e"/>')
    # windows with blinds (night city) on the back wall
    for wx in (130, 290):
        o.append(f'<rect x="{wx}" y="250" width="120" height="130" fill="url(#winDark)"/>' + ''.join(f'<rect x="{wx+8+i*16}" y="{280+(i%3)*20}" width="8" height="10" fill="{WARM}" opacity=".6"/>' for i in range(7)))
        o.append(''.join(f'<rect x="{wx}" y="{yy}" width="120" height="5" fill="#8a7e80" opacity=".85"/>' for yy in range(252, 380, 10)))
        o.append(f'<rect x="{wx-4}" y="246" width="128" height="6" fill="#3a3034"/>')
    # case board on the left wall
    o.append(R.quad('L', 1.08, 1.7, .14, .56, '#2e2a2c') + R.quad('L', 1.11, 1.67, .17, .53, '#a6845e'))
    r = random.Random(31); pins = []
    for i in range(11):
        s0 = 1.14 + r.uniform(0, .44); a0 = .2 + r.uniform(0, .24)
        o.append(R.quad('L', s0, s0 + .07, a0, a0 + .08, PAPER) + R.quad('L', s0 + .008, s0 + .062, a0 + .01, a0 + .055, '#5a5266'))
        pins.append(R.P('L', s0 + .035, a0 + .005))
    o.append(f'<polyline points="{pts(*pins)}" fill="none" stroke="{RED}" stroke-width="1.6"/>' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffd34a"/>' for x, y in pins))
    # filing cabinets + water cooler on the right wall, clock
    o.append(R.box(1.04, 1.3, .86, 1.0, .46, '#6a6a74', '#40404a', '#52525c') + R.box(1.32, 1.5, .86, 1.0, .46, '#6a6a74', '#40404a', '#52525c'))
    o.append(R.box(1.58, 1.68, .88, 1.0, .3, '#e6e2ea', '#b0aab8', '#c8c2d0') + R.box(1.6, 1.66, .9, .98, .42, '#9ac0e0', '#6a90b0', '#7aa0c0', h0=.3))
    o.append('<circle cx="270" cy="236" r="12" fill="#e8e4ea"/><circle cx="270" cy="236" r="9.6" fill="#2a2428"/><path d="M 270,236 L 270,228 M 270,236 L 275,240" stroke="#e8e4ea" stroke-width="1.6"/>')
    # rows of desks with monitors, folders, mugs, desk lamps
    for row, s0 in enumerate((1.25, 1.75, 2.45)):
        for u0, u1 in ((.06, .42), (.58, .94)):
            o.append(R.box(s0, s0 + .26, u0, u1, .21, '#7a6a5a', '#4a3e34', '#5e5044'))
            tp = on_floor(R, s0 + .08, (u0 + u1) / 2, .21); k = s0 * .9
            o.append(f'<rect x="{tp[0]-18*k:.0f}" y="{tp[1]-30*k:.0f}" width="{36*k:.0f}" height="{24*k:.0f}" rx="2" fill="#1a161a"/><rect x="{tp[0]-15*k:.0f}" y="{tp[1]-27*k:.0f}" width="{30*k:.0f}" height="{18*k:.0f}" fill="#5a6a9a"/>')
            o.append(f'<rect x="{tp[0]+22*k:.0f}" y="{tp[1]-10*k:.0f}" width="{20*k:.0f}" height="{10*k:.0f}" fill="#d8c8a0"/><rect x="{tp[0]+24*k:.0f}" y="{tp[1]-16*k:.0f}" width="{18*k:.0f}" height="{6*k:.0f}" fill="#b89a70"/>' + mug(tp[0] - 26 * k, tp[1], k * .9))
            o.append(R.box(s0 + .28, s0 + .38, u0 + .12, u0 + .24, .12, '#2e2a30', '#1e1a20', '#262228'))
            o.append(glow(tp[0], tp[1] - 18 * k, 40 * k, '#a8b8ff', .35))
        o.append(lamp_desk(*on_floor(R, s0 + .05, .4, .21), .5 + row * .2, on=True))
    # fluorescent ceiling panels
    for s_ in (1.3, 1.8, 2.6):
        a, b, c, d = R.P('C', s_, .3), R.P('C', s_, .7), R.P('C', s_ + .12, .7), R.P('C', s_ + .12, .3)
        o.append(f'<polygon points="{pts(a,b,c,d)}" fill="#e8ecf4"/>' + glow((a[0]+b[0])/2, (a[1]+c[1])/2, 80 * s_, '#dfe6ff', .35))
    o.append(shade(270, 520, 620, '#1e1830', .45))
    o.append(dust(32, (100, 300, 460, 900), 16, '#eef0ff'))
    return ''.join(o)


def hospital_room():
    """hospital room at dusk after the accident: empty bed with the leg sling ready, IV stand, flowers from the girlfriend"""
    R = Room((290, 430), 130, 230, 450, 560)
    o = [R.shell(wall='#8a7a7c', wall_lt='#9a8a8a', wall_dk='#6a5a62', ceil='#4a3e44', floor='#7a6a6a', planks=False)]
    for k in range(1, 8):
        p0 = lerp(R.BL, R.BR, k / 8); q0 = R.at(p0, 12)
        o.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{q0[0]:.0f}" y2="{q0[1]:.0f}" stroke="#6a5a5c" stroke-width="1.2"/>')
    for s_ in (1.2, 1.5, 1.9, 2.5, 3.4):
        a, b = R.P('F', s_, 0), R.P('F', s_, 1); o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#6a5a5c" stroke-width="1"/>')
    o.append(R.quad('L', 1, 12, .8, 1, '#6e5e62') + R.quad('R', 1, 12, .8, 1, '#5e5056') + f'<rect x="{R.x0}" y="{R.y0+(R.y1-R.y0)*.8:.0f}" width="{R.x1-R.x0}" height="{(R.y1-R.y0)*.2:.0f}" fill="#7a6a6e"/>')
    # window with dusk sky and city, blinds half down
    o.append('<rect x="230" y="262" width="170" height="150" fill="#5e4680"/><rect x="230" y="262" width="170" height="70" fill="#7a5e92"/>' + glow(380, 330, 90, '#ffb890', .5))
    r = random.Random(41); x = 230
    while x < 400:
        w = r.randint(16, 30); h = r.randint(30, 90)
        o.append(f'<rect x="{x}" y="{412-h}" width="{w}" height="{h}" fill="#3a2e52"/>' + ''.join(f'<rect x="{x+3+r.randint(0,w-6)}" y="{412-h+r.randint(4,h-4)}" width="2.4" height="3" fill="{WARM}" opacity=".7"/>' for _ in range(w // 5)))
        x += w + 2
    o.append(''.join(f'<rect x="230" y="{yy}" width="170" height="4" fill="#d8ccc8" opacity=".9"/>' for yy in range(262, 318, 7)))
    o.append('<path d="M 222,254 L 408,254 L 408,420 L 222,420 Z M 230,262 L 400,262 L 400,412 L 230,412 Z" fill="#d8ccc8" fill-rule="evenodd"/><rect x="312" y="262" width="6" height="150" fill="#d8ccc8"/>')
    # curtain track + privacy curtain on the left
    o.append(f'<path d="M {R.P("C",1.1,.05)[0]:.0f},{R.P("C",1.1,.05)[1]+8:.0f} L {R.P("C",2.6,.05)[0]:.0f},{R.P("C",2.6,.05)[1]+8:.0f}" stroke="#b8acb0" stroke-width="3"/>')
    o.append(R.quad('L', 2.3, 2.9, .02, .86, '#8aa0a8') + R.quad('L', 2.42, 2.46, .02, .86, '#6e8890') + R.quad('L', 2.62, 2.66, .02, .86, '#6e8890'))
    # TV high on the right wall, clock
    o.append(R.quad('R', 1.2, 1.5, .1, .28, '#1a1618') + R.quad('R', 1.22, 1.48, .12, .26, '#2e3046'))
    o.append('<circle cx="190" cy="290" r="12" fill="#efe8ea"/><circle cx="190" cy="290" r="9.6" fill="#4a3e44"/><path d="M 190,290 L 190,282 M 190,290 L 195,293" stroke="#efe8ea" stroke-width="1.6"/>')
    # hospital bed: frame, raised head, mattress, rumpled blanket, pillow
    o.append(R.box(1.2, 2.2, .1, .5, .12, '#c8c4cc', '#8a8690', '#a8a4ae'))
    o.append(R.box(1.2, 2.2, .1, .5, .18, '#f0ecee', '#c8c0c8', '#dcd6dc', h0=.12))
    o.append(R.box(1.2, 1.32, .1, .5, .34, '#c8c4cc', '#8a8690', '#a8a4ae'))
    o.append(R.box(1.32, 1.5, .14, .46, .26, '#ffffff', '#e0d8e0', '#ece6ec', h0=.18))
    o.append(R.box(1.6, 2.2, .1, .5, .2, '#9ab0c8', '#6a7e98', '#7e92ac', h0=.18))
    # leg sling: overhead bar + strap
    a, b = on_floor(R, 1.25, .3, .62), on_floor(R, 2.05, .3, .62)
    o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#b8b4bc" stroke-width="4"/><line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{a[0]:.0f}" y2="{on_floor(R,1.25,.3,.12)[1]:.0f}" stroke="#b8b4bc" stroke-width="4"/>')
    sl = on_floor(R, 1.95, .3, .62)
    o.append(f'<line x1="{sl[0]:.0f}" y1="{sl[1]:.0f}" x2="{sl[0]:.0f}" y2="{sl[1]+60:.0f}" stroke="#e8e4ea" stroke-width="2"/><path d="M {sl[0]-20:.0f},{sl[1]+60:.0f} q 20,16 40,0" fill="none" stroke="#e8e4ea" stroke-width="5"/>')
    # IV stand + monitor
    iv = on_floor(R, 1.25, .58)
    o.append(f'<line x1="{iv[0]:.0f}" y1="{iv[1]:.0f}" x2="{iv[0]:.0f}" y2="{iv[1]-260:.0f}" stroke="#b8b4bc" stroke-width="3"/><path d="M {iv[0]-18:.0f},{iv[1]:.0f} L {iv[0]+18:.0f},{iv[1]:.0f}" stroke="#8a8690" stroke-width="4"/>'
             f'<rect x="{iv[0]-12:.0f}" y="{iv[1]-256:.0f}" width="20" height="32" rx="6" fill="#e6f0f4" opacity=".85"/><path d="M {iv[0]-2:.0f},{iv[1]-224:.0f} C {iv[0]-10:.0f},{iv[1]-180:.0f} {iv[0]-30:.0f},{iv[1]-160:.0f} {iv[0]-50:.0f},{iv[1]-150:.0f}" fill="none" stroke="#e6f0f4" stroke-width="1.4" opacity=".8"/>')
    mo = on_floor(R, 1.05, .32, .5)
    o.append(f'<rect x="{mo[0]-26:.0f}" y="{mo[1]-28:.0f}" width="52" height="34" rx="3" fill="#1e1c22"/><rect x="{mo[0]-22:.0f}" y="{mo[1]-24:.0f}" width="44" height="26" fill="#0e1a1a"/><path d="M {mo[0]-20:.0f},{mo[1]-10:.0f} l 8,0 l 3,-8 l 4,14 l 3,-6 l 22,0" fill="none" stroke="#6fe0a8" stroke-width="1.6"/>' + glow(mo[0], mo[1] - 10, 40, '#6fe0a8', .3))
    # bedside table: flowers + fruit basket + get-well card; visitor chair
    o.append(R.box(1.3, 1.5, .55, .7, .17, '#d8d0d4', '#a8a0a6', '#c0b8be'))
    bt = on_floor(R, 1.4, .62, .17)
    o.append(f'<path d="M {bt[0]-10:.0f},{bt[1]:.0f} L {bt[0]+6:.0f},{bt[1]:.0f} L {bt[0]+4:.0f},{bt[1]-20:.0f} L {bt[0]-8:.0f},{bt[1]-20:.0f} Z" fill="#c8d8e0" opacity=".8"/>'
             + ''.join(f'<circle cx="{bt[0]-2+dx:.0f}" cy="{bt[1]-30+dy:.0f}" r="5" fill="{c}"/>' for dx, dy, c in [(-8, 0, '#e8a0b0'), (6, -4, '#f2d6a8'), (0, -10, '#d8607a'), (-4, -6, '#ffffff')]))
    o.append(f'<ellipse cx="{bt[0]+26:.0f}" cy="{bt[1]-6:.0f}" rx="14" ry="7" fill="#b8905a"/><circle cx="{bt[0]+20:.0f}" cy="{bt[1]-12:.0f}" r="5" fill="#d84a4a"/><circle cx="{bt[0]+30:.0f}" cy="{bt[1]-12:.0f}" r="5" fill="#e8b84a"/>'
             f'<path d="M {bt[0]-30:.0f},{bt[1]:.0f} L {bt[0]-20:.0f},{bt[1]-16:.0f} L {bt[0]-10:.0f},{bt[1]:.0f}" fill="#f6e8ec"/><path d="M {bt[0]-22:.0f},{bt[1]-8:.0f} l 2,-2 l 2,2 l -2,3 Z" fill="#d8607a"/>')
    o.append(R.box(1.9, 2.15, .66, .86, .12, '#7a6a8a', '#4e425a', '#62546e') + R.box(1.9, 1.95, .66, .86, .28, '#7a6a8a', '#4e425a', '#62546e', h0=.12))
    # crutches waiting against the wall + discharge folder
    cr = on_floor(R, 1.6, .96)
    o.append(f'<path d="M {cr[0]:.0f},{cr[1]:.0f} L {cr[0]-14:.0f},{cr[1]-220:.0f} M {cr[0]-12:.0f},{cr[1]:.0f} L {cr[0]-24:.0f},{cr[1]-216:.0f}" stroke="#a3a9b6" stroke-width="4"/>')
    o.append(beam('230,412 400,412 470,960 140,960', 'beamW', .45))
    o.append(shade(330, 360, 560, '#2a1e3a', .5))
    o.append(dust(43, (220, 420, 460, 880), 16, '#ffe8d8'))
    return ''.join(o)

# ---- 1B flashback: a busy back alley (soi) at night, rich detail, warm faded memory tone ----
def alley():
    R = Room((270, 470), 208, 300, 332, 552)
    Hh = R.y1 - R.y0
    o = []
    # sky + far street glow at the end of the alley
    o.append('<rect width="540" height="960" fill="#3a2a40"/>')
    o.append('<rect x="0" y="0" width="540" height="520" fill="#4e3650"/>' + glow(270, 470, 170, '#ffc8a0', .7))
    o.append(stars(51, 12, 200))
    # far end: cross street with a passing light and a lit shop
    o.append(f'<rect x="{R.x0}" y="{R.y0}" width="{R.x1-R.x0}" height="{Hh}" fill="#6a4a50"/><rect x="{R.x0}" y="{R.y1-60}" width="{R.x1-R.x0}" height="60" fill="#ffd8a8" opacity=".7"/><rect x="{R.x0+8}" y="{R.y0+40}" width="20" height="16" fill="{WARM}"/><rect x="{R.x0+36}" y="{R.y0+70}" width="18" height="14" fill="{WARM}" opacity=".7"/>')
    # floor: worn concrete with a centre drain, puddles
    F = 12
    o.append(f'<polygon points="{pts(R.BL, R.BR, R.at(R.BR, F), R.at(R.BL, F))}" fill="#5e4848"/>')
    o.append(f'<polygon points="{pts(R.P("F",1,.46), R.P("F",1,.54), R.P("F",8,.54), R.P("F",8,.46))}" fill="#4a3638"/>')
    for s_ in (1.3, 1.7, 2.3, 3.1, 4.2):
        a, b = R.P('F', s_, .46), R.P('F', s_, .54)
        o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#2e2224" stroke-width="{s_*1.4:.1f}"/>')
    for (s_, u_, w_) in ((2.2, .3, 60), (3.0, .66, 90), (1.6, .62, 34)):
        p = R.P('F', s_, u_)
        o.append(f'<ellipse cx="{p[0]:.0f}" cy="{p[1]:.0f}" rx="{w_:.0f}" ry="{w_*.22:.0f}" fill="#9a7a84" opacity=".55"/><ellipse cx="{p[0]-w_*.2:.0f}" cy="{p[1]-2:.0f}" rx="{w_*.4:.0f}" ry="{w_*.06:.0f}" fill="#ffd8b0" opacity=".45"/>')
    # facades: shophouses down both sides
    for face, base, lit_col, base_dk in (('L', '#7a5650', '#ffcf9e', '#5a3c3a'), ('R', '#644650', '#ffb8c8', '#4a3040')):
        o.append(R.quad(face, 1, F, 0, 1, base))
        bounds = [1.0, 1.22, 1.5, 1.86, 2.36, 3.0, 3.9, 5.2, 7.0]
        for k in range(len(bounds) - 1):
            s0, s1 = bounds[k], bounds[k + 1]; m = (s0 + s1) / 2
            o.append(R.quad(face, s1 - .015 * s1, s1, 0, 1, base_dk))                         # party wall pilaster
            # ground floor: alternate open shop / rolling shutter
            if k % 3 == 1:
                o.append(R.quad(face, s0 + .02 * s0, s1 - .03 * s1, .7, 1, lit_col) + R.quad(face, s0 + .02 * s0, s1 - .03 * s1, .7, .74, '#7a3a34'))
                o.append(R.quad(face, s0 + .1 * (s1 - s0), s0 + .4 * (s1 - s0), .8, .92, '#c8a080'))   # counter
            else:
                o.append(R.quad(face, s0 + .02 * s0, s1 - .03 * s1, .7, 1, '#8a8486'))
                for t in range(10):
                    a_ = .7 + t * .03
                    p0, p1 = R.P(face, s0 + .02 * s0, a_), R.P(face, s1 - .03 * s1, a_)
                    o.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="#6a6466" stroke-width="{.6*m:.1f}"/>')
            # awning over the shop
            o.append(R.quad(face, s0 + .02 * s0, s1 - .03 * s1, .66, .7, ['#8a3a3a', '#3a6a6a', '#a07a3a'][k % 3]))
            # upper floors: windows with grilles, AC units, balconies with laundry
            for a0, a1 in ((.42, .56), (.16, .3)):
                lit = (k + int(a0 * 10)) % 3 == 0
                o.append(R.quad(face, s0 + .2 * (s1 - s0), s0 + .75 * (s1 - s0), a0, a1, lit_col if lit else '#2e2228'))
                for g in (.33, .5, .66):
                    p0, p1 = R.P(face, s0 + .2 * (s1 - s0), a0 + (a1 - a0) * g), R.P(face, s0 + .75 * (s1 - s0), a0 + (a1 - a0) * g)
                    o.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="#2a1a1c" stroke-width="{.5*m:.1f}"/>')
                if lit: 
                    c = R.P(face, m, (a0 + a1) / 2); o.append(glow(c[0], c[1], 30 * m, lit_col, .35))
            o.append(R.quad(face, s0 + .78 * (s1 - s0), s0 + .95 * (s1 - s0), .5, .58, '#c8c4c0') + R.quad(face, s0 + .8 * (s1 - s0), s0 + .93 * (s1 - s0), .51, .57, '#9a9694'))  # AC unit
            if k % 2 == 0:   # balcony rail + laundry
                o.append(R.quad(face, s0 + .15 * (s1 - s0), s0 + .8 * (s1 - s0), .3, .315, '#2a1e20'))
                for t, col in zip((.25, .4, .55, .7), ('#e8d8c8', '#6a8aa8', '#c86a6a', '#e8c86a')):
                    p = R.P(face, s0 + t * (s1 - s0), .31)
                    o.append(f'<rect x="{p[0]-4*m:.0f}" y="{p[1]:.0f}" width="{8*m:.0f}" height="{12*m:.0f}" fill="{col}"/>')
            # pipes and gutters
            p0, p1 = R.P(face, s1 - .02 * s1, .05), R.P(face, s1 - .02 * s1, .7)
            o.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="#3a2a2a" stroke-width="{1.2*m:.1f}"/>')
            # projecting shop signs (perpendicular to the wall)
            if k in (1, 3, 5):
                p = R.P(face, m, .6); d = 1 if face == 'L' else -1
                w_, h_ = 15 * m, 24 * m
                col = ['#c83a4a', '#2a8a8a', '#d8a83a'][k % 3]
                o.append(f'<rect x="{p[0] if d>0 else p[0]-w_:.0f}" y="{p[1]-h_:.0f}" width="{w_:.0f}" height="{h_:.0f}" fill="{col}"/>'
                         f'<rect x="{p[0]+2*m if d>0 else p[0]-w_+2*m:.0f}" y="{p[1]-h_+3*m:.0f}" width="{w_-4*m:.0f}" height="{h_-6*m:.0f}" fill="none" stroke="#ffe8c8" stroke-width="{.6*m:.1f}"/>'
                         f'<text x="{p[0]+w_/2 if d>0 else p[0]-w_/2:.0f}" y="{p[1]-h_/2+3*m:.0f}" font-family="IBM Plex Sans Thai, sans-serif" font-size="{5.4*m:.0f}" fill="#fff4e0" text-anchor="middle">{["ข้าวต้ม","ร้านยา","ซ่อม"][k%3]}</text>')
                o.append(glow(p[0] + d * w_ / 2, p[1] - h_ / 2, 50 * m, col, .45))
    # overhead: tangled power lines and a string of lanterns
    for (s_, sag, n) in ((1.35, 60, 3), (1.9, 40, 2), (2.8, 26, 4), (4.0, 18, 2)):
        a, b = R.P('L', s_, .08), R.P('R', s_, .1)
        for j in range(n):
            o.append(f'<path d="M {a[0]:.0f},{a[1]+j*6:.0f} Q {(a[0]+b[0])/2:.0f},{a[1]+sag+j*8:.0f} {b[0]:.0f},{b[1]+j*5:.0f}" fill="none" stroke="#1e1416" stroke-width="{1+.4*j:.1f}"/>')
    a, b = R.P('L', 2.2, .22), R.P('R', 2.2, .22)
    o.append(f'<path d="M {a[0]:.0f},{a[1]:.0f} Q 270,{a[1]+60:.0f} {b[0]:.0f},{b[1]:.0f}" fill="none" stroke="#2a1a1a" stroke-width="1.4"/>')
    for t in [i / 9 for i in range(1, 9)]:
        x = a[0] + (b[0] - a[0]) * t; y = a[1] + 60 * 4 * t * (1 - t) * .5 + 8
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="7" ry="9" fill="{["#e86a5a","#ffcf7a"][int(t*9)%2]}"/>' + glow(x, y, 26, WARM, .5))
    # street lamp bracket on the left wall
    lp = R.P('L', 1.6, .32)
    o.append(f'<path d="M {lp[0]:.0f},{lp[1]:.0f} l 40,0 l 0,10" fill="none" stroke="#2a1a1a" stroke-width="4"/><path d="M {lp[0]+28:.0f},{lp[1]+10:.0f} l 24,0 l -4,10 l -16,0 Z" fill="#2a1a1a"/><rect x="{lp[0]+32:.0f}" y="{lp[1]+18:.0f}" width="16" height="4" fill="{WARM}"/>')
    o.append(glow(lp[0] + 40, lp[1] + 24, 160, WARM, .75) + beam(f'{lp[0]+30:.0f},{lp[1]+22:.0f} {lp[0]+50:.0f},{lp[1]+22:.0f} {lp[0]+250:.0f},860 {lp[0]-80:.0f},860', 'beamW', .55))
    # props on the ground (near to far drawn far first)
    def stool(s_, u_, col):
        p = R.P('F', s_, u_); k = s_ * .55
        return f'<g transform="translate({p[0]:.0f},{p[1]:.0f}) scale({k:.2f})"><path d="M -9,-16 L 9,-16 L 11,0 L 7,0 L 6,-10 L -6,-10 L -7,0 L -11,0 Z" fill="{col}"/><rect x="-10" y="-19" width="20" height="4" rx="2" fill="{col}"/></g>'
    def table(s_, u_):
        p = R.P('F', s_, u_); k = s_ * .55
        return f'<g transform="translate({p[0]:.0f},{p[1]:.0f}) scale({k:.2f})"><rect x="-20" y="-28" width="40" height="4" fill="#c8b8a8"/><rect x="-17" y="-24" width="3" height="24" fill="#8a7a6a"/><rect x="14" y="-24" width="3" height="24" fill="#8a7a6a"/><ellipse cx="-6" cy="-30" rx="5" ry="2" fill="#f2e6d8"/><rect x="6" y="-36" width="3" height="8" fill="#c83a3a"/></g>'
    for s_, u_ in ((3.0, .2), (2.2, .16)):
        o.append(table(s_, u_) + stool(s_ + .1, u_ + .1, '#c83a3a') + stool(s_ - .1, u_ + .08, '#3a6aa8'))
    # motorbike parked on the right
    mp = R.P('F', 2.0, .82)
    o.append(f'<g transform="translate({mp[0]:.0f},{mp[1]:.0f}) scale(1.3)"><circle cx="-16" cy="-8" r="8" fill="#1a1416"/><circle cx="16" cy="-8" r="8" fill="#1a1416"/><circle cx="-16" cy="-8" r="3" fill="#8a8486"/><circle cx="16" cy="-8" r="3" fill="#8a8486"/>'
             f'<path d="M -18,-10 L -6,-24 L 10,-24 L 18,-12 L 8,-12 L 2,-18 L -8,-12 Z" fill="#8a3a3a"/><path d="M -8,-26 L 6,-26 L 4,-22 L -6,-22 Z" fill="#2a1a1a"/><path d="M 12,-26 L 18,-36 L 22,-34" fill="none" stroke="#2a1a1a" stroke-width="2"/><circle cx="21" cy="-30" r="3" fill="#ffe8b0"/></g>')
    # crates, trash bags, potted plants, the knocked-over bin
    cp = R.P('F', 1.55, .08)
    o.append(f'<g transform="translate({cp[0]:.0f},{cp[1]:.0f}) scale(1.1)"><rect x="-20" y="-24" width="40" height="24" fill="#8a6a3a"/><rect x="-14" y="-46" width="32" height="22" fill="#a07a44"/><path d="M -20,-12 L 20,-12 M -14,-35 L 18,-35" stroke="#5a4020" stroke-width="2"/></g>')
    for (s_, u_) in ((1.4, .9), (1.55, .96), (2.6, .9)):
        p = R.P('F', s_, u_)
        o.append(f'<ellipse cx="{p[0]:.0f}" cy="{p[1]-6*s_:.0f}" rx="{8*s_:.0f}" ry="{7*s_:.0f}" fill="#1e1a20"/><ellipse cx="{p[0]-4*s_:.0f}" cy="{p[1]-16*s_:.0f}" rx="{4*s_:.0f}" ry="{3*s_:.0f}" fill="#4a4250"/>')
    for (s_, u_) in ((2.7, .06), (3.6, .94)):
        o.append(plant(*R.P('F', s_, u_), s_ * .4, '#8a5a44'))
    o.append(cast('<path d="M 300,830 L 390,790 L 430,840 L 340,880 Z"/>'))
    o.append('<g transform="translate(350,812) rotate(-24)"><rect x="-44" y="-28" width="88" height="56" rx="6" fill="#4a5a5a"/><rect x="-44" y="-28" width="88" height="14" fill="#5a6a6a"/><ellipse cx="-44" cy="0" rx="10" ry="28" fill="#3a4848"/></g>')
    o.append('<g fill="#e8d4c4">' + ''.join(f'<rect x="{x}" y="{y}" width="16" height="11" transform="rotate({r} {x} {y})"/>' for x, y, r in [(250, 870, 20), (290, 910, -30), (190, 890, 50), (430, 912, 10), (210, 930, -12)]) + '</g>')
    o.append('<g transform="translate(120,880)"><circle cx="10" cy="-4" r="16" fill="#e8d0b8" opacity=".85"/><rect x="2" y="-30" width="6" height="24" fill="#e8d0b8" opacity=".6"/></g>')   # spilled takeaway cup
    # cat on a ledge, steam from the noodle shop
    ct = R.P('L', 1.86, .69)
    o.append(f'<g transform="translate({ct[0]+4:.0f},{ct[1]:.0f}) scale(.8)"><ellipse cx="0" cy="-8" rx="12" ry="8" fill="#1a1214"/><circle cx="10" cy="-16" r="6" fill="#1a1214"/><path d="M 7,-21 L 8,-26 L 11,-21 Z M 12,-21 L 14,-26 L 15,-20 Z" fill="#1a1214"/><path d="M -12,-8 C -22,-10 -22,-22 -16,-24" fill="none" stroke="#1a1214" stroke-width="3"/><circle cx="12" cy="-17" r="1.2" fill="#e8d870"/></g>')
    sp = R.P('L', 1.36, .76)
    o.append(''.join(f'<path d="M {sp[0]+20+i*10:.0f},{sp[1]:.0f} c -8,-16 8,-24 0,-44" fill="none" stroke="#fff4e8" stroke-width="5" opacity=".18" filter="url(#soft)"/>' for i in range(3)))
    # mood: warm faded memory, purple shadows
    o.append(shade(300, 560, 560, '#2e1e3a', .5))
    o.append(fog(560, 140, '#ffd8c0', .2))
    o.append(dust(11, (lp[0], lp[1], lp[0] + 260, 860), 30, '#ffe8d4'))
    o.append('<rect width="540" height="960" fill="#e8c4b0" opacity=".2" style="mix-blend-mode:soft-light"/>')
    return ''.join(o)

# ---- window close-ups of the house across, for the shadow play ----
def window_closeup(mode='open'):
    """mode 'open': curtains open, lit living room visible (fight, wine glass) · 'closed': curtain drawn and lit, blank for silhouettes · 'dark': lights out"""
    o = [night_sky((470, 90), 33, 300)]
    # siding wall fills the frame
    o.append('<rect x="0" y="120" width="540" height="840" fill="#6e5452"/>' + ''.join(f'<rect x="0" y="{yy}" width="540" height="3" fill="#3a2a2a" opacity=".3"/>' for yy in range(126, 960, 22)))
    o.append('<polygon points="0,120 540,120 540,70 270,-40 0,70" fill="#2e1f22"/><rect x="0" y="112" width="540" height="12" fill="#c4b2a4"/>')
    # window: deep trim, shutters, flower box
    X0, Y0, X1, Y1 = 92, 230, 448, 560
    o.append(f'<rect x="{X0-56}" y="{Y0}" width="44" height="{Y1-Y0}" fill="#2e3a36"/><rect x="{X1+12}" y="{Y0}" width="44" height="{Y1-Y0}" fill="#26302c"/>')
    o.append(''.join(f'<line x1="{xx}" y1="{yy}" x2="{xx+36}" y2="{yy}" stroke="#1a2220" stroke-width="2"/>' for xx in (X0 - 52, X1 + 16) for yy in range(Y0 + 10, Y1 - 6, 12)))
    o.append(f'<rect x="{X0-14}" y="{Y0-18}" width="{X1-X0+28}" height="{Y1-Y0+36}" fill="#c4b2a4"/><rect x="{X0-22}" y="{Y0-30}" width="{X1-X0+44}" height="14" fill="#b4a294"/>')
    lit = mode != 'dark'
    o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="{"url(#winLit)" if lit else "#1e1628"}"/>')
    if mode == 'open':
        # the lit living room seen through the glass
        o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#e8b890"/>')
        o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="80" fill="#d8a080"/>' + ''.join(f'<line x1="{xx}" y1="{Y0}" x2="{xx}" y2="{Y0+250}" stroke="#c8906e" stroke-width="3"/>' for xx in range(X0 + 20, X1, 26)))
        o.append(f'<rect x="{X0+30}" y="{Y0+60}" width="70" height="56" fill="#6a4a3a"/><rect x="{X0+36}" y="{Y0+66}" width="58" height="44" fill="#8aa0b0"/>')        # painting
        o.append(f'<rect x="{X1-90}" y="{Y0+40}" width="4" height="150" fill="#3a2a22"/><path d="M {X1-110},{Y0+40} L {X1-66},{Y0+40} L {X1-76},{Y0+10} L {X1-100},{Y0+10} Z" fill="#fff0d0"/>' + glow(X1 - 88, Y0 + 30, 90, WARM, .8))  # floor lamp
        o.append(f'<path d="M {X0},{Y0+250} L {X1},{Y0+250} L {X1},{Y1} L {X0},{Y1} Z" fill="#9a6a50"/><rect x="{X0+60}" y="{Y0+200}" width="200" height="60" rx="14" fill="#7a4a52"/><rect x="{X0+50}" y="{Y0+236}" width="220" height="50" rx="12" fill="#8a5660"/>')  # sofa back
        o.append(f'<path d="M {X0+250},{Y1-30} l 6,-14 l 8,10 l -6,6 Z M {X0+268},{Y1-24} l 10,-4 l 2,8 Z M {X0+240},{Y1-20} l -8,-6 l 6,-4 Z" fill="#f4f0f8" opacity=".9"/>')   # broken wine glass on the floor
        o.append(f'<ellipse cx="{X0+262}" cy="{Y1-14}" rx="26" ry="6" fill="#7a2030" opacity=".85"/>')   # spilled wine
        # curtains pulled to the sides, inside
        o.append(f'<path d="M {X0},{Y0} L {X0+46},{Y0} C {X0+40},{Y0+120} {X0+50},{Y0+240} {X0+36},{Y1} L {X0},{Y1} Z" fill="#c88a7a"/><path d="M {X1},{Y0} L {X1-46},{Y0} C {X1-40},{Y0+120} {X1-50},{Y0+240} {X1-36},{Y1} L {X1},{Y1} Z" fill="#b87a6a"/>')
    elif mode == 'closed':
        # drawn curtain lit from behind: soft folds, empty stage for silhouettes
        o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#f2c4a8"/>')
        o.append(''.join(f'<rect x="{xx}" y="{Y0}" width="14" height="{Y1-Y0}" fill="#e2a68c" opacity=".7"/>' for xx in range(X0 + 6, X1, 34)))
        o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="url(#poolW)" opacity=".0"/>' + glow((X0 + X1) / 2, Y0 + 120, 220, '#fff0d8', .55))
        o.append(f'<path d="M {X0},{Y1-40} L {X1},{Y1-40}" stroke="#d89a80" stroke-width="2" opacity=".6"/>')
    # mullions over everything
    o.append(f'<rect x="{(X0+X1)/2-6}" y="{Y0}" width="12" height="{Y1-Y0}" fill="#c4b2a4"/><rect x="{X0}" y="{Y0+150}" width="{X1-X0}" height="10" fill="#c4b2a4"/>')
    o.append(f'<path d="M {X0+8},{Y0+8} L {X0+60},{Y0+8} L {X0+8},{Y0+60} Z" fill="#ffffff" opacity=".12"/>')
    # flower box + sill
    o.append(f'<rect x="{X0-30}" y="{Y1+18}" width="{X1-X0+60}" height="12" fill="#b4a294"/><rect x="{X0-16}" y="{Y1+30}" width="{X1-X0+32}" height="34" fill="#4a2a1e"/>')
    o.append(''.join(f'<ellipse cx="{X0-6+i*24}" cy="{Y1+28}" rx="16" ry="10" fill="#2c3e34"/>' for i in range(16)))
    o.append(''.join(f'<circle cx="{X0+i*24}" cy="{Y1+20+(i%2)*6}" r="5" fill="{["#a8607e","#b8a070","#c87a8a"][i%3]}"/>' for i in range(15)))
    # light spill outside
    if lit:
        o.append(glow(270, Y1 + 80, 260, WARM, .35) + beam(f'{X0},{Y1} {X1},{Y1} 560,960 -20,960', 'beamW', .35))
    o.append(shade(270, 400, 600, '#140e24', .55))
    o.append(fog(820, 160, '#9a8cc8', .22))
    o.append(dust(61, (X0, Y1, X1, 940), 16, '#ffe8d4'))
    return ''.join(o)

# ---------------- prop library v2: shaped furniture sprites (bottom-centre origin, scale k = depth s) ----------------
def g(x, y, k, body):
    return f'<g transform="translate({x:.1f},{y:.1f}) scale({k:.3f})">{body}</g>'

# ---------------- upscale finish kit: panel mouldings, herringbone floor, tray ceiling, brass + velvet ----------------
CREAM = '#e6d6c4'; CREAM_SH = '#c8b4a2'; BRASS = '#c9a45a'; BRASS_DK = '#8a6a34'

def luxe_walls(R, wall='#7a5e60', panel='#86686a', mould='#d8c4b0', F=12):
    """classic picture-frame mouldings on the back + side walls, crown and skirting"""
    o = []
    Hh = R.y1 - R.y0
    # back wall panels: dado rail at 62%, tall panels above, short below
    o.append(f'<rect x="{R.x0}" y="{R.y0 + Hh*.62:.0f}" width="{R.x1-R.x0}" height="4" fill="{mould}"/>')
    n = 4
    for i in range(n):
        x0 = R.x0 + 8 + i * (R.x1 - R.x0 - 16) / n; x1 = x0 + (R.x1 - R.x0 - 16) / n - 8
        o.append(f'<rect x="{x0:.0f}" y="{R.y0+Hh*.66:.0f}" width="{x1-x0:.0f}" height="{Hh*.26:.0f}" fill="{panel}" stroke="{mould}" stroke-width="2"/>')
        o.append(f'<rect x="{x0:.0f}" y="{R.y0+Hh*.08:.0f}" width="{x1-x0:.0f}" height="{Hh*.5:.0f}" fill="none" stroke="{mould}" stroke-width="2" opacity=".8"/>')
    for face in ('L', 'R'):
        o.append(R.quad(face, 1, F, .615, .625, mould))
        s = 1.04
        while s < 5:
            s2 = s * 1.22
            o.append(R.quad(face, s + .02 * s, s2 - .04 * s, .66, .92, panel))
            for (a0, a1) in ((.66, .92), (.08, .58)):
                p = [R.P(face, s + .02 * s, a0), R.P(face, s2 - .04 * s, a0), R.P(face, s2 - .04 * s, a1), R.P(face, s + .02 * s, a1)]
                o.append(f'<polygon points="{pts(*p)}" fill="none" stroke="{mould}" stroke-width="{1.6*s:.1f}" opacity=".85"/>')
            s = s2
        o.append(R.quad(face, 1, F, 0, .03, mould) + R.quad(face, 1, F, .965, 1, '#efe4d6'))   # crown + skirting
    o.append(f'<rect x="{R.x0}" y="{R.y0}" width="{R.x1-R.x0}" height="{Hh*.03:.0f}" fill="{mould}"/><rect x="{R.x0}" y="{R.y1-Hh*.035:.0f}" width="{R.x1-R.x0}" height="{Hh*.035:.0f}" fill="#efe4d6"/>')
    return ''.join(o)

def herringbone(R, light='#9a6a48', dark='#7e5236', line='#5a3624', F=8):
    """herringbone parquet in perspective"""
    o = [f'<polygon points="{pts(R.BL, R.BR, R.at(R.BR, F), R.at(R.BL, F))}" fill="{light}"/>']
    rows = []; s = 1.0
    while s < F:
        rows.append(s); s *= 1.09
    cols = 14
    for i in range(len(rows) - 1):
        s0, s1 = rows[i], rows[i + 1]
        for j in range(cols):
            u0, u1 = j / cols, (j + 1) / cols
            a, b, c, d = R.P('F', s0, u0), R.P('F', s0, u1), R.P('F', s1, u1), R.P('F', s1, u0)
            if (i + j) % 2:
                o.append(f'<polygon points="{pts(a, b, c, d)}" fill="{dark}" opacity=".55"/>')
            o.append(f'<line x1="{(a[0] if (i+j)%2 else b[0]):.1f}" y1="{a[1]:.1f}" x2="{(c[0] if (i+j)%2 else d[0]):.1f}" y2="{c[1]:.1f}" stroke="{line}" stroke-width="{.5*s0:.2f}" opacity=".6"/>')
    return ''.join(o)

def tray_ceiling(R, col='#d8c8b8', recess='#c8b6a4', lights=True):
    F = 12
    o = [f'<polygon points="{pts(R.TL, R.TR, R.at(R.TR, F), R.at(R.TL, F))}" fill="{col}"/>']
    q = [R.P('C', 1.25, .18), R.P('C', 1.25, .82), R.P('C', 3.2, .82), R.P('C', 3.2, .18)]
    o.append(f'<polygon points="{pts(*q)}" fill="{recess}"/><polygon points="{pts(*q)}" fill="none" stroke="#efe4d6" stroke-width="3"/>')
    if lights:
        for s_ in (1.4, 2.0, 2.9):
            for u_ in (.1, .9):
                p = R.P('C', s_, u_)
                o.append(f'<ellipse cx="{p[0]:.0f}" cy="{p[1]:.0f}" rx="{5*s_:.0f}" ry="{2*s_:.0f}" fill="#fff6e0"/>' + glow(p[0], p[1] + 6 * s_, 26 * s_, WARM, .35))
    return ''.join(o)

def chandelier(x, y, k, drop=60):
    arms = ''.join(f'<line x1="0" y1="0" x2="{dx}" y2="{dy}" stroke="{BRASS}" stroke-width="2"/><circle cx="{dx}" cy="{dy}" r="4" fill="#fff4d8"/>' for dx, dy in
                   [(-34, 4), (34, 4), (-22, 14), (22, 14), (-12, -10), (12, -10), (0, 18)])
    b = (f'<line x1="0" y1="-{drop}" x2="0" y2="0" stroke="{BRASS_DK}" stroke-width="2"/><circle cx="0" cy="0" r="7" fill="{BRASS}"/>{arms}')
    return g(x, y, k, b) + glow(x, y, 70 * k, WARM, .7)

def round_marble_table(x, y, k):
    b = (f'<ellipse cx="0" cy="2" rx="70" ry="9" fill="#1a1012" opacity=".35"/>'
         f'<path d="M -10,0 L 10,0 L 4,-38 L -4,-38 Z" fill="{BRASS}"/><ellipse cx="0" cy="0" rx="26" ry="5" fill="{BRASS_DK}"/>'
         f'<ellipse cx="0" cy="-42" rx="66" ry="14" fill="#efe8e2"/><ellipse cx="0" cy="-44" rx="66" ry="12" fill="#f6f0ea"/>'
         f'<path d="M -40,-48 C -20,-40 0,-50 24,-42" fill="none" stroke="#c8beb8" stroke-width="1.4"/><path d="M -10,-52 C 6,-46 20,-50 40,-46" fill="none" stroke="#d8d0ca" stroke-width="1"/>'
         + books(-40, -48, .8) + f'<g transform="translate(26,-48)"><path d="M -8,0 L 8,0 L 6,-22 L -6,-22 Z" fill="#e8dccb"/>'
         + ''.join(f'<path d="M 0,-22 C {dx*.3:.0f},-40 {dx},-56 {dx*1.4:.0f},-66" fill="none" stroke="#e8d8b8" stroke-width="3"/>' for dx in (-10, -4, 3, 9)) + '</g>'
         + f'<ellipse cx="-4" cy="-48" rx="10" ry="3" fill="{BRASS}"/>')
    return g(x, y, k, b)

def drapes(x0, y0, x1, y1, col='#3e4a6a', dk='#2a3450', lt='#5a6a8a'):
    """floor-length velvet drapes over sheers, brass rod"""
    o = [f'<rect x="{x0-30}" y="{y0-10}" width="{x1-x0+60}" height="5" rx="2" fill="{BRASS}"/><circle cx="{x0-30}" cy="{y0-8}" r="6" fill="{BRASS}"/><circle cx="{x1+30}" cy="{y0-8}" r="6" fill="{BRASS}"/>',
         f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#f6eee6" opacity=".18"/>']
    for xa, d in ((x0 - 26, 1), (x1 + 26, -1)):
        xb = xa + d * 56
        o.append(f'<path d="M {xa},{y0-6} L {xb},{y0-6} C {xb-d*6},{(y0+y1)/2} {xb+d*4},{y1-20} {xb+d*10},{y1} L {xa},{y1} Z" fill="{col}"/>')
        for t, c in ((.25, dk), (.5, lt), (.75, dk)):
            xx = xa + d * 56 * t
            o.append(f'<path d="M {xx:.0f},{y0-6} C {xx-d*2:.0f},{(y0+y1)/2} {xx+d*3:.0f},{y1-20} {xx+d*6:.0f},{y1}" fill="none" stroke="{c}" stroke-width="3"/>')
    return ''.join(o)

def art_canvas(x, y, w, h, seed=1):
    r = random.Random(seed)
    o = [f'<rect x="{x-4}" y="{y-4}" width="{w+8}" height="{h+8}" fill="{BRASS}"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8dccb"/>']
    for _ in range(5):
        cx = x + r.uniform(.15, .85) * w; cy = y + r.uniform(.15, .85) * h; rr = r.uniform(.12, .3) * min(w, h)
        o.append(f'<circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rr:.0f}" fill="{r.choice(["#c86a5a","#3e5a6a","#d8a85a","#7a5a8a","#5e7e6a"])}" opacity=".85"/>')
    o.append(f'<path d="M {x+w*.1:.0f},{y+h*.7:.0f} C {x+w*.4:.0f},{y+h*.4:.0f} {x+w*.6:.0f},{y+h*.9:.0f} {x+w*.9:.0f},{y+h*.5:.0f}" fill="none" stroke="#2a1e1a" stroke-width="2"/>')
    return ''.join(o)

def olive_tree(x, y, k):
    leaves = ''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="22" ry="16" fill="{c}"/>' for dx, dy, c in
                     [(-26, -150, '#6e7e5e'), (20, -160, '#7e8e6a'), (-4, -184, '#8a9a74'), (-36, -176, '#5e6e50'), (34, -186, '#6e7e5e'), (4, -206, '#7e8e6a')])
    b = (f'<ellipse cx="0" cy="1" rx="30" ry="5" fill="#1a1012" opacity=".35"/><path d="M -2,-40 C -6,-80 6,-110 0,-150" fill="none" stroke="#5a4a3a" stroke-width="5"/>{leaves}'
         f'<path d="M -26,0 L 26,0 L 30,-46 L -30,-46 Z" fill="#e8dccb"/><rect x="-32" y="-50" width="64" height="6" fill="#d8c8b4"/>')
    return g(x, y, k, b)

def sofa_front(x, y, k, c=('#3e4a6a', '#56628a', '#2a3450'), pillows=('#d8a070', '#e8dccb', '#c86a6a')):
    """tufted velvet sofa with brass legs"""
    m, lt, dk = c
    tufts = ''.join(f'<circle cx="{tx}" cy="{ty}" r="1.8" fill="{dk}"/>' for tx in range(-100, 104, 20) for ty in (-96, -78))
    b = (f'<ellipse cx="0" cy="2" rx="130" ry="10" fill="#1a1012" opacity=".35"/>'
         f'<path d="M -116,-8 L -112,4 L -108,-8 Z M 108,-8 L 112,4 L 116,-8 Z" fill="{BRASS}"/>'
         f'<path d="M -126,-40 L -126,-96 C -126,-116 126,-116 126,-96 L 126,-40 Z" fill="{dk}"/>'
         f'<path d="M -118,-46 L -118,-94 C -118,-108 118,-108 118,-94 L 118,-46 Z" fill="{m}"/>{tufts}'
         f'<path d="M -118,-92 C -60,-104 60,-104 118,-92" fill="none" stroke="{lt}" stroke-width="5" opacity=".6"/>'
         f'<rect x="-122" y="-50" width="244" height="42" rx="12" fill="{m}"/><rect x="-120" y="-50" width="240" height="10" rx="5" fill="{lt}"/>'
         f'<line x1="-40" y1="-50" x2="-40" y2="-10" stroke="{dk}" stroke-width="2"/><line x1="40" y1="-50" x2="40" y2="-10" stroke="{dk}" stroke-width="2"/>'
         f'<path d="M -140,-8 L -140,-70 C -140,-86 -112,-86 -112,-70 L -112,-8 Z" fill="{m}"/><path d="M 140,-8 L 140,-70 C 140,-86 112,-86 112,-70 L 112,-8 Z" fill="{dk}"/>'
         f'<rect x="-100" y="-88" width="40" height="36" rx="8" fill="{pillows[0]}" transform="rotate(-8 -80 -70)"/><rect x="60" y="-88" width="40" height="36" rx="8" fill="{pillows[1]}" transform="rotate(8 80 -70)"/>'
         f'<rect x="-18" y="-86" width="36" height="32" rx="8" fill="{pillows[2]}"/><path d="M 60,-60 L 130,-60 L 126,-20 L 70,-24 Z" fill="#c8a080" opacity=".9"/>')
    return g(x, y, k, b)

def sofa_back(x, y, k, c=('#3e4a6a', '#56628a', '#2a3450')):
    m, lt, dk = c
    b = (f'<path d="M -132,0 L -132,-100 C -132,-124 132,-124 132,-100 L 132,0 Z" fill="{dk}"/><path d="M -128,-104 C -60,-122 60,-122 128,-104" fill="none" stroke="{lt}" stroke-width="4" opacity=".6"/>'
         f'<path d="M -152,0 L -152,-80 C -152,-98 -118,-98 -118,-80 L -118,0 Z" fill="{m}"/><path d="M 152,0 L 152,-80 C 152,-98 118,-98 118,-80 L 118,0 Z" fill="{dk}"/>'
         f'<path d="M 50,-118 C 60,-80 80,-40 90,0 L 50,0 C 46,-40 40,-80 30,-118 Z" fill="#8a6a5a" opacity=".95"/>')
    return g(x, y, k, b)

def armchair(x, y, k, c=('#7a3a46', '#94525e', '#5a2a34')):
    """velvet wingback with brass feet"""
    m, lt, dk = c
    b = (f'<ellipse cx="0" cy="2" rx="60" ry="7" fill="#1a1012" opacity=".35"/><path d="M -44,-8 L -42,4 L -40,-8 Z M 40,-8 L 42,4 L 44,-8 Z" fill="{BRASS}"/>'
         f'<path d="M -48,-50 L -50,-104 C -50,-128 50,-128 50,-104 L 48,-50 Z" fill="{dk}"/><path d="M -40,-56 L -42,-102 C -42,-118 42,-118 42,-102 L 40,-56 Z" fill="{m}"/>'
         f'<path d="M -50,-104 L -64,-96 L -62,-50 L -48,-50 Z" fill="{m}"/><path d="M 50,-104 L 64,-96 L 62,-50 L 48,-50 Z" fill="{dk}"/>'
         f'<rect x="-52" y="-50" width="104" height="42" rx="10" fill="{m}"/><rect x="-50" y="-50" width="100" height="10" rx="5" fill="{lt}"/>'
         f'<rect x="-64" y="-66" width="20" height="58" rx="8" fill="{m}"/><rect x="44" y="-66" width="20" height="58" rx="8" fill="{dk}"/>'
         f'<rect x="-14" y="-78" width="30" height="26" rx="7" fill="#e8dccb"/>')
    return g(x, y, k, b)

def coffee_table(x, y, k, items=True):
    b = (f'<ellipse cx="0" cy="2" rx="80" ry="7" fill="#1a1012" opacity=".35"/>'
         f'<rect x="-66" y="-40" width="6" height="40" fill="#4a2c1c"/><rect x="60" y="-40" width="6" height="40" fill="#3a2016"/>'
         f'<rect x="-62" y="-16" width="124" height="5" fill="#5a341f"/>'
         f'<path d="M -74,-50 L 74,-50 L 70,-40 L -70,-40 Z" fill="#9a6444"/><rect x="-74" y="-54" width="148" height="5" fill="#b07a54"/>')
    if items:
        b += (books(-50, -54, .9) + f'<rect x="-10" y="-62" width="34" height="8" fill="#e8dccb"/>' + mug(40, -54, 1) +
              f'<g transform="translate(-30,-16)"><rect x="-10" y="-10" width="24" height="10" fill="#c9a46a"/><rect x="-8" y="-18" width="20" height="8" fill="#6a7a9a"/></g>')
    return g(x, y, k, b)

def side_table(x, y, k, lamp=True, lit=True):
    b = (f'<ellipse cx="0" cy="1" rx="26" ry="4" fill="#1a1012" opacity=".35"/><rect x="-3" y="-50" width="6" height="50" fill="#4a2c1c"/><path d="M -16,0 L 16,0 L 4,-6 L -4,-6 Z" fill="#4a2c1c"/>'
         f'<ellipse cx="0" cy="-52" rx="24" ry="5" fill="#9a6444"/>')
    if lamp:
        b += (f'<rect x="-6" y="-70" width="12" height="18" rx="4" fill="#d8c0a0"/><rect x="-1" y="-84" width="2" height="14" fill="#3a2a22"/><path d="M -18,-82 L 18,-82 L 12,-104 L -12,-104 Z" fill="#f2dcc0"/>')
    b += mug(14, -56, .8)
    o = g(x, y, k, b)
    if lamp and lit: o += glow(x, y - 92 * k, 70 * k, WARM, .8)
    return o

def floor_lamp(x, y, k, lit=True):
    b = (f'<ellipse cx="0" cy="1" rx="22" ry="4" fill="#2a1a14"/><rect x="-2" y="-200" width="4" height="200" fill="#2a1a14"/>'
         f'<path d="M -26,-196 L 26,-196 L 16,-232 L -16,-232 Z" fill="#f2dcc0"/><path d="M -26,-196 L 26,-196" stroke="#c8a888" stroke-width="2"/>')
    o = g(x, y, k, b)
    if lit: o += glow(x, y - 210 * k, 90 * k, WARM, .85) + pool(x, y, 110 * k, 26 * k, WARM, .4)
    return o

def big_plant(x, y, k, pot='#8a5a44'):
    leaves = ''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="13" ry="22" fill="{c}" transform="rotate({r} {dx} {dy})"/>' for dx, dy, r, c in
                     [(-22, -110, -40, '#3f6250'), (20, -120, 35, '#4f7660'), (-6, -150, -10, '#5e8a6e'), (18, -170, 30, '#4f7660'), (-20, -180, -30, '#3f6250'),
                      (4, -200, 5, '#6e9a7e'), (-28, -140, -60, '#4f7660'), (28, -146, 60, '#3f6250')])
    b = (f'<ellipse cx="0" cy="1" rx="26" ry="5" fill="#1a1012" opacity=".35"/><rect x="-1.5" y="-190" width="3" height="150" fill="#4a3a2a"/>{leaves}'
         f'<path d="M -22,0 L 22,0 L 26,-44 L -26,-44 Z" fill="{pot}"/><rect x="-28" y="-48" width="56" height="6" fill="#6a4232"/>')
    return g(x, y, k, b)

def hanging_plant(x, y, k):
    b = (f'<line x1="0" y1="-80" x2="-10" y2="0" stroke="#c8b49a" stroke-width="1"/><line x1="0" y1="-80" x2="10" y2="0" stroke="#c8b49a" stroke-width="1"/>'
         f'<path d="M -14,0 L 14,0 L 10,14 L -10,14 Z" fill="#c8a080"/>'
         + ''.join(f'<path d="M {dx},{8} C {dx-4},{30} {dx+4},{50} {dx-2},{60+abs(dx)}" fill="none" stroke="#4f7660" stroke-width="3"/>' for dx in (-10, -4, 3, 9))
         + ''.join(f'<ellipse cx="{dx}" cy="{dy}" rx="4" ry="2.4" fill="#5e8a6e"/>' for dx, dy in [(-11, 24), (-5, 40), (4, 30), (8, 52), (-2, 56), (10, 20)]))
    return g(x, y, k, b)

def builtin_shelf(x0, y0, x1, y1, seed=1, rows=5):
    """front-facing built-in shelving filled with books, plants, frames, jars"""
    r = random.Random(seed)
    o = [f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{WOOD_DK}"/><rect x="{x0+5}" y="{y0+5}" width="{x1-x0-10}" height="{y1-y0-10}" fill="#3a2016"/>']
    hh = (y1 - y0 - 10) / rows
    for k in range(rows):
        yb = y0 + 5 + hh * (k + 1)
        o.append(f'<rect x="{x0+5}" y="{yb-4}" width="{x1-x0-10}" height="5" fill="{WOOD}"/>')
        xx = x0 + 9
        while xx < x1 - 16:
            kind = r.random()
            if kind < .55:
                w = r.randint(4, 7); h = r.uniform(hh * .55, hh * .85)
                o.append(f'<rect x="{xx}" y="{yb-4-h:.1f}" width="{w}" height="{h:.1f}" fill="{r.choice(["#7a3a3a","#3e5a62","#c9a46a","#5a4a7a","#8a6a4a","#a85a4a","#4a6a4a"])}"/>'); xx += w + 1
            elif kind < .7:
                o.append(plant(xx + 9, yb - 4, .45 * hh / 40)); xx += 20
            elif kind < .85:
                o.append(f'<rect x="{xx}" y="{yb-4-hh*.6:.1f}" width="{hh*.5:.1f}" height="{hh*.6:.1f}" fill="#c9b49a"/><rect x="{xx+2}" y="{yb-2-hh*.6:.1f}" width="{hh*.5-4:.1f}" height="{hh*.6-4:.1f}" fill="{r.choice(["#6e7ea0","#a08068","#7a9a8a"])}"/>'); xx += hh * .5 + 4
            else:
                o.append(f'<ellipse cx="{xx+6}" cy="{yb-4-hh*.25:.1f}" rx="6" ry="{hh*.25:.1f}" fill="{r.choice(["#d8c8b0","#9ab0b8","#c88a6a"])}"/>'); xx += 14
    # fairy lights along the top
    o.append(f'<path d="M {x0+6},{y0+10} Q {(x0+x1)/2},{y0+26} {x1-6},{y0+10}" fill="none" stroke="#3a2a22" stroke-width="1"/>')
    o.append(''.join(f'<circle cx="{x0+6+(x1-x0-12)*t:.1f}" cy="{y0+10+16*4*t*(1-t):.1f}" r="2" fill="#ffe8a8"/>' for t in [i/10 for i in range(11)]))
    return ''.join(o)

def curtain_pair(x0, y0, x1, y1, col='#8a5a5a', dk='#6a3e40', lt='#a0706a'):
    """gathered curtains with tie-backs either side of a window"""
    def one(xa, side):
        d = 1 if side == 'L' else -1; xw = xa + d * 60
        return (f'<path d="M {xa},{y0} L {xw},{y0} C {xw-d*10},{y0+120} {xa+d*22},{(y0+y1)/2} {xa+d*18},{(y0+y1)/2+20} C {xa+d*30},{(y0+y1)/2+60} {xa+d*42},{y1-20} {xa+d*46},{y1+30} L {xa},{y1+30} Z" fill="{col}"/>'
                f'<path d="M {xa+d*14},{y0} C {xa+d*14},{y0+100} {xa+d*12},{(y0+y1)/2} {xa+d*10},{y1+30}" stroke="{dk}" stroke-width="3" fill="none"/>'
                f'<path d="M {xa+d*30},{y0} C {xa+d*28},{y0+80} {xa+d*20},{(y0+y1)/2-10} {xa+d*18},{(y0+y1)/2+20}" stroke="{lt}" stroke-width="3" fill="none"/>'
                f'<ellipse cx="{xa+d*20}" cy="{(y0+y1)/2+18}" rx="8" ry="5" fill="#c9a46a"/>')
    return (f'<rect x="{x0-20}" y="{y0-8}" width="{x1-x0+40}" height="5" rx="2" fill="#2a1a16"/><circle cx="{x0-20}" cy="{y0-6}" r="5" fill="#c9a46a"/><circle cx="{x1+20}" cy="{y0-6}" r="5" fill="#c9a46a"/>'
            + one(x0 - 14, 'L') + one(x1 + 14, 'R'))

def wallpaper(R, base_col, motif='#ffffff', op=.08, top=.66):
    """small diamond motif wallpaper on the back wall and side walls (above the wainscot)"""
    o = []
    for row in range(14):
        y = R.y0 + 10 + row * ((R.y1 - R.y0) * top - 10) / 14
        for col in range(16):
            x = R.x0 + 8 + col * (R.x1 - R.x0 - 16) / 15 + (row % 2) * 9
            if x < R.x1 - 4:
                o.append(f'<path d="M {x:.1f},{y-3:.1f} l 3,3 l -3,3 l -3,-3 Z" fill="{motif}" opacity="{op}"/>')
    for face in ('L', 'R'):
        s = 1.04
        while s < 4.4:
            for j in range(10):
                a = .06 + j * (top - .1) / 10 + (.03 if int(s * 10) % 2 else 0)
                p = R.P(face, s, a); sz = 3 * s
                o.append(f'<path d="M {p[0]:.1f},{p[1]-sz:.1f} l {sz*.6:.1f},{sz:.1f} l {-sz*.6:.1f},{sz:.1f} l {-sz*.6:.1f},{-sz:.1f} Z" fill="{motif}" opacity="{op}"/>')
            s *= 1.14
    return ''.join(o)

def rug_pattern(R, s0, s1, u0, u1, base='#6a3e4e', border='#c9a07a', inner='#8a5a62'):
    q = [R.P('F', s0, u0), R.P('F', s0, u1), R.P('F', s1, u1), R.P('F', s1, u0)]
    def inset(t): return [lerp(q[0], q[2], t), lerp(q[1], q[3], t), lerp(q[2], q[0], t), lerp(q[3], q[1], t)]
    o = [f'<polygon points="{pts(*q)}" fill="{base}"/>', f'<polygon points="{pts(*inset(.05))}" fill="none" stroke="{border}" stroke-width="3"/>',
         f'<polygon points="{pts(*inset(.12))}" fill="{inner}"/>', f'<polygon points="{pts(*inset(.2))}" fill="none" stroke="{border}" stroke-width="2" stroke-dasharray="6 5"/>']
    c = lerp(lerp(q[0], q[2], .5), lerp(q[1], q[3], .5), .5)
    o.append(f'<ellipse cx="{c[0]:.0f}" cy="{c[1]:.0f}" rx="{(q[1][0]-q[0][0])*.18:.0f}" ry="{(q[3][1]-q[0][1])*.16:.0f}" fill="none" stroke="{border}" stroke-width="3"/>')
    return ''.join(o)

def family_room(night=False, board=False):
    """2nd-floor family room / home studio v2: built-in shelves around a big window, shaped furniture, cosy clutter"""
    R = Room((280, 430), 120, 220, 440, 570)
    Hh = R.y1 - R.y0
    o = [R.shell(wall='#6e5054' if not night else '#4a3442', wall_lt='#7c5c5e' if not night else '#56404c', wall_dk='#4e3842' if not night else '#34242e',
                 ceil='#2e2228' if not night else '#1c1418', floor='#7a4e38' if not night else '#4e3226')]
    o.append(tray_ceiling(R, '#cdbcac' if not night else '#5a4a48', '#bfac9a' if not night else '#4e403e', lights=True))
    o.append(herringbone(R, '#9a6a48' if not night else '#5e3e2c', '#7e5236' if not night else '#4a2e20'))
    o.append(luxe_walls(R, panel='#86686a' if not night else '#56404a', mould='#d8c4b0' if not night else '#8a7a72'))
    # ceiling beams + skylight-free coffered feel

    # back wall: big arched window with window seat, built-in shelves either side
    wx0, wy0, wx1, wy1 = 200, 262, 360, 470
    view = street('night' if night else 'day', (130, 120), hy=600, hs=1.1)
    cid = uid('cw')
    o.append(f'<clipPath id="{cid}"><path d="M {wx0},{wy1} L {wx0},{wy0+40} A 80,44 0 0 1 {wx1},{wy0+40} L {wx1},{wy1} Z"/></clipPath>')
    o.append(f'<g clip-path="url(#{cid})"><g filter="url(#dof)" transform="translate({wx0-20},{wy0}) scale(.36) translate(0,-150)">{view}</g></g>')
    o.append(f'<path d="M {wx0-10},{wy1+8} L {wx0-10},{wy0+40} A 90,52 0 0 1 {wx1+10},{wy0+40} L {wx1+10},{wy1+8} Z M {wx0},{wy1} L {wx0},{wy0+40} A 80,44 0 0 1 {wx1},{wy0+40} L {wx1},{wy1} Z" fill="#e8dccb" fill-rule="evenodd"/>')
    o.append(f'<path d="M {(wx0+wx1)/2},{wy0-4} L {(wx0+wx1)/2},{wy1} M {wx0},{wy0+100} L {wx1},{wy0+100}" stroke="#e8dccb" stroke-width="5"/>')
    o.append(f'<path d="M {wx0+14},{wy0+40} A 66,34 0 0 1 {wx1-14},{wy0+40}" fill="none" stroke="#e8dccb" stroke-width="3"/>')
    o.append(builtin_shelf(R.x0 + 4, 236, wx0 - 26, R.y1 - 60, seed=3) + builtin_shelf(wx1 + 26, 236, R.x1 - 4, R.y1 - 60, seed=8))
    o.append(drapes(wx0, wy0 - 30, wx1, R.y1 - 70, '#3e4a6a', '#2a3450', '#5a6a8a'))
    o.append(f'<rect x="{wx0-22}" y="{wy1+8}" width="{wx1-wx0+44}" height="58" fill="{WOOD_DK}"/><rect x="{wx0-22}" y="{wy1+8}" width="{wx1-wx0+44}" height="8" fill="{WOOD_LT}"/>'
             f'<rect x="{wx0-16}" y="{wy1+16}" width="{wx1-wx0+32}" height="16" rx="6" fill="#6a5a8a"/>'
             f'<rect x="{wx0-4}" y="{wy1-14}" width="44" height="32" rx="10" fill="#d8a070" transform="rotate(-6 {wx0+18} {wy1})"/><rect x="{wx1-48}" y="{wy1-12}" width="40" height="30" rx="10" fill="#c86a6a" transform="rotate(6 {wx1-28} {wy1})"/>')
    o.append(''.join(f'<rect x="{wx0-14+i*40}" y="{wy1+40}" width="32" height="20" fill="#4a2c1c"/>' for i in range(5)))   # drawers under the seat
    # hanging plants + pendant lamps
    for (s_, u_) in ((1.3, .22), (1.3, .78)):
        p = R.P('C', s_, u_); o.append(hanging_plant(p[0], p[1] + 90 * s_ * .5, s_ * .8))
    cp0 = R.P('C', 1.9, .5); o.append(chandelier(cp0[0], cp0[1] + 60, 1.9 * .75, 80))
    for s_ in ():
        pc = R.P('C', s_, .5)
        o.append(f'<line x1="{pc[0]:.0f}" y1="{pc[1]:.0f}" x2="{pc[0]:.0f}" y2="{pc[1]+34*s_:.0f}" stroke="#1a1012" stroke-width="2"/><path d="M {pc[0]-18*s_:.0f},{pc[1]+52*s_:.0f} Q {pc[0]:.0f},{pc[1]+26*s_:.0f} {pc[0]+18*s_:.0f},{pc[1]+52*s_:.0f} Z" fill="#c8945a"/>')
        if night or True: o.append(glow(pc[0], pc[1] + 54 * s_, 46 * s_, WARM, .55 if night else .3))
    # side walls: gallery of frames (left), studio desk + pinboard or frames (right)
    for (s0, s1, a0, a1, c) in ((1.12, 1.3, .14, .32, '#6e7ea0'), (1.34, 1.46, .18, .3, '#a08068'), (1.12, 1.26, .36, .48, '#7a9a8a'), (1.3, 1.46, .34, .5, '#b8806a')):
        o.append(R.quad('L', s0, s1, a0, a1, '#2a1a14') + R.quad('L', s0 + .01, s1 - .01, a0 + .015, a1 - .015, c))
    # rug + furniture: watching armchair by the window, coffee table, sofa (back to camera) in front, desk on the right
    o.append(rug_pattern(R, 1.5, 2.6, .14, .86, '#5a3a4e', '#d8b88a', '#7a4a5e'))
    ap = on_floor(R, 1.12, .78); o.append(armchair(ap[0], ap[1], 1.12 * .9))
    sp = on_floor(R, 1.08, .94); o.append(side_table(sp[0], sp[1], 1.08 * .9, lamp=True, lit=True))
    fl = on_floor(R, 1.1, .1); o.append(floor_lamp(fl[0], fl[1], 1.1 * .85, lit=night))
    dk_ = on_floor(R, 1.35, .2)
    desk = (f'<ellipse cx="0" cy="2" rx="90" ry="7" fill="#1a1012" opacity=".35"/><rect x="-76" y="-82" width="152" height="8" fill="#9a6444"/><rect x="-74" y="-74" width="8" height="74" fill="#5a341f"/><rect x="66" y="-74" width="8" height="74" fill="#5a341f"/>'
            f'<rect x="20" y="-74" width="46" height="50" fill="#7a4a32"/><rect x="24" y="-70" width="38" height="20" fill="#8a5a3c"/><circle cx="43" cy="-60" r="2" fill="#d9b25a"/>'
            f'<rect x="-40" y="-132" width="66" height="44" rx="3" fill="#1a1418"/><rect x="-36" y="-128" width="58" height="36" fill="{"#8aa0d8" if night else "#3a4a6a"}"/><rect x="-10" y="-88" width="6" height="8" fill="#1a1418"/>'
            f'<rect x="-60" y="-86" width="36" height="4" fill="#2a2228"/>' + mug(52, -82, 1) + books(-70, -82, .8))
    o.append(g(dk_[0], dk_[1], 1.35 * .8, desk))
    o.append(lamp_desk(dk_[0] + 44, dk_[1] - 82 * 1.08, .8, on=night or board))
    ch = on_floor(R, 1.6, .26)
    o.append(g(ch[0], ch[1], 1.6 * .8, '<rect x="-24" y="-54" width="48" height="8" rx="3" fill="#8a5a3c"/><rect x="-22" y="-120" width="44" height="64" rx="10" fill="#6a3e4a"/><rect x="-3" y="-46" width="6" height="34" fill="#2a1a14"/><path d="M -26,0 L 26,0 L 4,-12 L -4,-12 Z" fill="#2a1a14"/>'))
    ct = on_floor(R, 1.9, .55); o.append(round_marble_table(ct[0], ct[1], 1.9 * .72))
    bp = on_floor(R, 2.1, .88); o.append(olive_tree(bp[0], bp[1], 2.1 * .62))
    sb = on_floor(R, 3.3, .46); o.append(sofa_back(sb[0], sb[1], 3.3 * .5))
    # crutches leaning on the sofa's back corner
    cr = on_floor(R, 3.1, .74)
    o.append(f'<path d="M {cr[0]:.0f},{cr[1]:.0f} L {cr[0]-30:.0f},{cr[1]-330:.0f} M {cr[0]+18:.0f},{cr[1]:.0f} L {cr[0]-12:.0f},{cr[1]-326:.0f}" stroke="#a3a9b6" stroke-width="6"/>'
             f'<rect x="{cr[0]-44:.0f}" y="{cr[1]-342:.0f}" width="26" height="12" rx="5" fill="#4a4e5c"/><rect x="{cr[0]-24:.0f}" y="{cr[1]-338:.0f}" width="26" height="12" rx="5" fill="#3a3d49"/>')
    if board:
        # investigation: pinboard over the desk (left wall), map, tripod camera at the window, papers everywhere
        o.append(R.quad('L', 1.16, 1.5, .1, .5, '#2a1a14') + R.quad('L', 1.18, 1.48, .12, .48, '#a77a5c'))
        r = random.Random(4); pins = []
        for i in range(11):
            s0 = 1.2 + r.uniform(0, .22); a0 = .15 + r.uniform(0, .24)
            o.append(R.quad('L', s0, s0 + .05, a0, a0 + .08, PAPER) + R.quad('L', s0 + .006, s0 + .044, a0 + .01, a0 + .055, '#5e5070'))
            pins.append(R.P('L', s0 + .025, a0 + .005))
        o.append(f'<polyline points="{pts(*pins)}" fill="none" stroke="{RED}" stroke-width="1.6"/>' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffd34a"/>' for x, y in pins))
        tp = on_floor(R, 1.2, .55)
        o.append(f'<g transform="translate({tp[0]:.0f},{tp[1]-150:.0f})"><path d="M 0,36 L -24,150 M 0,36 L 24,150 M 0,36 L 0,154" stroke="#1e1214" stroke-width="3"/><rect x="-18" y="14" width="30" height="22" rx="3" fill="#1e1214"/><rect x="10" y="18" width="38" height="14" rx="3" fill="#2e2024"/><circle cx="50" cy="25" r="7" fill="#120a0c"/></g>')
        r = random.Random(9)
        for _ in range(16):
            s = r.uniform(1.45, 2.5); u = r.uniform(.12, .9); p = R.P('F', s, u); a = r.uniform(-30, 30)
            o.append(f'<rect x="{p[0]:.0f}" y="{p[1]:.0f}" width="{12*s:.0f}" height="{8*s:.0f}" fill="{PAPER}" transform="rotate({a:.0f} {p[0]:.0f} {p[1]:.0f})" opacity=".9"/>')
        o.append(''.join(mug(*on_floor(R, 1.95 + i * .04, .5 + i * .06, .1), 1.3, c) for i, c in enumerate(('#c9b49a', '#e6dcd0', '#a8c0c8'))))
    if night:
        o.append(beam(f'{wx0},{wy0+30} {wx1},{wy0+30} 470,960 120,960', 'beamC', .45))
        o.append(shade(dk_[0] + 44, dk_[1] - 120, 480, '#1a1030', .66))
        o.append(dust(23, (160, 300, 460, 900), 22, '#e6e2ff'))
    else:
        sun = [R.P('F', 1.35, .3), R.P('F', 1.35, .7), R.P('F', 2.5, .78), R.P('F', 2.5, .34)]
        o.append(f'<polygon points="{pts(*sun)}" fill="#ffd8b0" opacity=".42" filter="url(#soft)" style="mix-blend-mode:screen"/>')
        o.append(beam(f'{wx0},{wy0+30} {wx1},{wy0+30} {sun[2][0]:.0f},{sun[2][1]:.0f} {sun[3][0]:.0f},{sun[3][1]:.0f}', 'beamW', .7))
        o.append(shade(290, 500, 560, '#24163a', .45))
        o.append(dust(24, (190, 300, 460, 860), 26))
    return ''.join(o)

def ground_living():
    """hero's ground-floor living room v2: front door + windows on the back wall, stairs at left, cosy furniture"""
    R = Room((290, 430), 120, 230, 450, 570)
    o = [R.shell(wall='#6a4c48', wall_lt='#7a5854', wall_dk='#4a3438', ceil='#2a1c1e', floor='#7a4e38')]
    o.append(tray_ceiling(R, '#5a4a48', '#4e403e'))
    o.append(herringbone(R, '#8a5c3e', '#6e4630'))
    o.append(luxe_walls(R, panel='#7a5a5a', mould='#c8b4a0'))

    # front door with sidelight + transom, two windows with curtains
    o.append('<rect x="250" y="300" width="84" height="270" fill="#e8dccb"/><rect x="258" y="318" width="54" height="252" fill="#6a2e26"/><rect x="316" y="318" width="12" height="252" fill="url(#winDark)"/>'
             '<path d="M 258,318 A 35,16 0 0 1 328,318 Z" fill="url(#winDark)"/><rect x="266" y="334" width="38" height="70" fill="none" stroke="#3a1a16" stroke-width="2"/><rect x="266" y="420" width="38" height="120" fill="none" stroke="#3a1a16" stroke-width="2"/><circle cx="304" cy="452" r="3" fill="#d9b25a"/>')
    for wx in (150, 372):
        o.append(f'<rect x="{wx-6}" y="294" width="78" height="120" fill="#e8dccb"/><rect x="{wx}" y="300" width="66" height="108" fill="url(#winDark)"/><path d="M {wx+33},300 L {wx+33},408 M {wx},354 L {wx+66},354" stroke="#e8dccb" stroke-width="3"/>' + stars(70 + wx, 4, 0))
        o.append(drapes(wx, 290, wx + 66, 566, '#2e5a52', '#1e3e38', '#447a6e'))
    # entry: console table with key bowl + mirror, coat rack with jacket, shoes
    o.append('<ellipse cx="216" cy="470" rx="22" ry="30" fill="#c9a46a"/><ellipse cx="216" cy="470" rx="17" ry="25" fill="#8a9ab8" opacity=".6"/>')
    ct = on_floor(R, 1.02, .3)
    o.append(g(ct[0], ct[1], 1.0, '<rect x="-40" y="-70" width="80" height="6" fill="#9a6444"/><rect x="-36" y="-64" width="5" height="64" fill="#5a341f"/><rect x="31" y="-64" width="5" height="64" fill="#5a341f"/><ellipse cx="-10" cy="-74" rx="12" ry="4" fill="#c9a46a"/>' + plant(20, -70, .5)))
    cr_ = on_floor(R, 1.04, .72)
    o.append(g(cr_[0], cr_[1], 1.0, '<rect x="-2" y="-170" width="4" height="170" fill="#3a2016"/><path d="M -18,0 L 18,0" stroke="#3a2016" stroke-width="4"/><path d="M -16,-160 L 16,-160" stroke="#3a2016" stroke-width="3"/>'
             '<path d="M -14,-158 C -22,-120 -18,-80 -10,-60 L 4,-60 C 0,-90 0,-130 -6,-158 Z" fill="#3e4a5e"/><path d="M 10,-158 C 18,-140 16,-120 12,-110 L 4,-110 C 6,-130 6,-148 4,-158 Z" fill="#9a5a3a"/>'
             '<path d="M -26,-2 L -10,-2 L -10,-10 L -22,-10 Z M -6,-2 L 10,-2 L 10,-10 L -2,-10 Z" fill="#2a2420"/>'))
    # staircase up the left wall: treads + balusters + handrail
    for k in range(10):
        s0 = 1.06 + k * .11; h = .05 + k * .065
        o.append(R.box(s0, s0 + .11, .0, .2, h, '#9a6444', '#5a3624', '#6e4630'))
    for k in range(10):
        s0 = 1.06 + k * .11 + .05; h = .05 + k * .065
        a = on_floor(R, s0, .2, h); b = on_floor(R, s0, .2, h + .16)
        o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#e8dccb" stroke-width="{1.5*s0:.1f}"/>')
    a = on_floor(R, 1.1, .2, .22); b = on_floor(R, 2.2, .2, .82)
    o.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="#5a341f" stroke-width="6"/>')
    # family photos on the right wall, TV console, plant
    for (s0, s1, a0, a1, c) in ((1.1, 1.26, .16, .3, '#a08068'), (1.3, 1.42, .14, .26, '#6e7ea0'), (1.12, 1.22, .34, .44, '#8a9a7a'), (1.26, 1.42, .32, .46, '#b8806a')):
        o.append(R.quad('R', s0, s1, a0, a1, '#2a1a14') + R.quad('R', s0 + .01, s1 - .01, a0 + .015, a1 - .015, c))
    o.append(R.box(1.5, 1.95, .86, 1.0, .14, WOOD_LT, WOOD_DK, WOOD))
    o.append(R.quad('R', 1.56, 1.9, .42, .68, '#141018') + R.quad('R', 1.58, 1.88, .44, .66, '#2a2438'))
    # rug, sofa facing camera, coffee table, armchair, floor lamp, big plant
    o.append(rug_pattern(R, 1.35, 2.45, .24, .84, '#3e3a52', '#d8b88a', '#5a4a6a'))
    sp = on_floor(R, 1.3, .55); o.append(sofa_front(sp[0], sp[1], 1.3 * .7, ('#2e5a52', '#447a6e', '#1e3e38'), ('#d8a070', '#e8dccb', '#c86a6a')))
    fl = on_floor(R, 1.28, .86); o.append(floor_lamp(fl[0], fl[1], 1.28 * .85, lit=True))
    ap = on_floor(R, 2.0, .86); o.append(armchair(ap[0], ap[1], 2.0 * .66, ('#a0783a', '#b8904e', '#7a5a2a')))
    ctb = on_floor(R, 1.85, .55); o.append(round_marble_table(ctb[0], ctb[1], 1.85 * .68))
    cl0 = R.P('C', 1.7, .55); o.append(chandelier(cl0[0], cl0[1] + 50, 1.7 * .7, 70))
    bp = on_floor(R, 2.5, .97); o.append(olive_tree(bp[0], bp[1], 2.5 * .55))
    o.append(shade(fl[0], fl[1] - 200, 520, '#1e1430', .6))
    o.append(dust(25, (fl[0] - 140, fl[1] - 240, fl[0] + 40, fl[1]), 14))
    return ''.join(o)

# ---- 7C surprise party living room v2 (inside the house across) ----
def party_room():
    R = Room((280, 440), 110, 250, 450, 590)
    o = [R.shell(wall='#8a6260', wall_lt='#9a706a', wall_dk='#6a4a50', ceil='#4a3438', floor='#7e5440')]
    o.append(tray_ceiling(R, '#d8c8b8', '#cab8a6'))
    o.append(herringbone(R, '#a07050', '#84583c'))
    o.append(luxe_walls(R, panel='#9a7270', mould='#ecdccb'))
    # back wall: fireplace with mantel in the middle, window right, shelves left
    o.append('<rect x="214" y="430" width="134" height="160" fill="#efe8e2"/><path d="M 222,440 C 250,452 280,436 300,448 C 320,440 336,452 340,446" fill="none" stroke="#c8beb8" stroke-width="2"/><rect x="204" y="420" width="154" height="14" fill="#f6f0ea"/><rect x="236" y="470" width="90" height="120" fill="#2a1612"/>'
             '<path d="M 250,590 C 252,560 266,556 270,540 C 276,556 290,560 292,546 C 300,560 312,566 312,590 Z" fill="#ffb060"/><path d="M 262,590 C 266,572 274,568 278,560 C 282,570 292,574 296,590 Z" fill="#ffe0a0"/>' + glow(281, 570, 70, '#ffb060', .8))
    o.append(art_canvas(234, 330, 94, 80, 7))  # painting over the mantel
    o.append(''.join(f'<rect x="{x}" y="{404}" width="6" height="16" fill="#f2e8da"/><ellipse cx="{x+3}" cy="400" rx="3" ry="5" fill="#ffd890"/>' for x in (214, 226, 336, 348)))
    o.append(builtin_shelf(R.x0 + 4, 270, 196, R.y1 - 40, seed=12, rows=6))
    o.append('<rect x="370" y="286" width="72" height="140" fill="#e8dccb"/><rect x="376" y="292" width="60" height="128" fill="#2e2560"/><path d="M 406,292 L 406,420 M 376,356 L 436,356" stroke="#e8dccb" stroke-width="3"/>' + drapes(376, 282, 436, 578, '#7a3a46', '#5a2a34', '#94525e'))
    # banner + balloons + string lights
    cols = ['#ff9fb4', '#b9a2ff', '#ffe08a', '#9fe0c8']
    o.append('<path d="M 112,262 Q 280,330 448,262" fill="none" stroke="#e6dcf6" stroke-width="2"/>')
    for i, ch in enumerate('SURPRISE'):
        t = (i + .5) / 8; x = 112 + 336 * t; y = 262 + 68 * 4 * t * (1 - t) * .5 + 4
        o.append(f'<path d="M {x-18},{y} L {x+18},{y} L {x},{y+38} Z" fill="{cols[i%4]}"/><text x="{x}" y="{y+18}" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#4a3a78" text-anchor="middle">{ch}</text>')
    for face in ('L', 'R'):
        for k in range(12):
            p = R.P(face, 1 + k * .22, .03)
            o.append(f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{2+k*.35:.1f}" fill="#fff0c8"/>' + (glow(p[0], p[1], 14 + k * 2, WARM, .55) if k % 2 == 0 else ''))
    for (x, y, c) in [(60, 360, '#ff9fb4'), (100, 320, '#b9a2ff'), (140, 380, '#ffe08a'), (470, 560, '#9fe0c8'), (505, 520, '#ff9fb4'), (430, 300, '#b9a2ff')]:
        o.append(f'<path d="M {x},{y+30} C {x+6},{y+80} {x-6},{y+130} {x+4},{y+190}" fill="none" stroke="#e6dcf6" stroke-width="1.2" opacity=".7"/><ellipse cx="{x}" cy="{y}" rx="24" ry="30" fill="{c}"/><ellipse cx="{x-8}" cy="{y-10}" rx="6" ry="9" fill="#ffffff" opacity=".55"/>')
    # frames on the side walls
    for face in ('L', 'R'):
        for (s0, s1, a0, a1, c) in ((1.2, 1.36, .16, .3, '#c09ad6'), (1.42, 1.56, .2, .34, '#9fb8e0')):
            o.append(R.quad(face, s0, s1, a0, a1, '#2a1a14') + R.quad(face, s0 + .01, s1 - .01, a0 + .015, a1 - .015, c))
    # rug, sofa facing camera, two armchairs, coffee/cake table, floor lamp, plants, gifts
    o.append(rug_pattern(R, 1.25, 2.4, .16, .84, '#7a4a5a', '#e8c8a0', '#9a5a6a'))
    sp = on_floor(R, 1.2, .5); o.append(sofa_front(sp[0], sp[1], 1.2 * .72, ('#d8c4b4', '#ece0d4', '#b8a494'), ('#c86a6a', '#3e4a6a', '#d8a070')))
    cl0 = R.P('C', 1.8, .5); o.append(chandelier(cl0[0], cl0[1] + 60, 1.8 * .8, 80))
    for u_ in (.12, .88):
        ap = on_floor(R, 1.75, u_); o.append(armchair(ap[0], ap[1], 1.75 * .62, ('#2e5a52', '#447a6e', '#1e3e38')))
    ctp = on_floor(R, 1.8, .5)
    cake_table = ('<ellipse cx="0" cy="2" rx="80" ry="7" fill="#1a1012" opacity=".35"/><rect x="-66" y="-40" width="6" height="40" fill="#4a2c1c"/><rect x="60" y="-40" width="6" height="40" fill="#3a2016"/>'
                  '<path d="M -80,-52 L 80,-52 L 76,-40 L -76,-40 Z" fill="#f6eef8"/><path d="M -80,-52 L 80,-52 L 80,-34 C 60,-28 40,-36 20,-30 C 0,-36 -20,-28 -40,-34 C -60,-28 -80,-34 -80,-34 Z" fill="#f6eef8"/>'
                  '<rect x="-30" y="-88" width="60" height="36" rx="6" fill="#fff8fb"/><rect x="-30" y="-78" width="60" height="8" fill="#f2a6bc"/><rect x="-20" y="-110" width="40" height="22" rx="5" fill="#fffafc"/>'
                  + ''.join(f'<rect x="{-14+i*10}" y="-124" width="3" height="14" fill="#b9a2ff"/><ellipse cx="{-12.5+i*10}" cy="-128" rx="2.4" ry="4" fill="#ffe0a8"/>' for i in range(4))
                  + '<rect x="44" y="-66" width="20" height="14" fill="#e8c46a"/><rect x="-66" y="-62" width="16" height="10" fill="#9fe0c8"/>')
    o.append(g(ctp[0], ctp[1], 1.8 * .7, cake_table) + glow(ctp[0], ctp[1] - 128 * 1.26, 70, WARM, .8))
    fl = on_floor(R, 1.15, .1); o.append(floor_lamp(fl[0], fl[1], 1.15 * .85))
    for (s_, u_) in ((1.15, .93), (2.4, .05)):
        bp = on_floor(R, s_, u_); o.append(olive_tree(bp[0], bp[1], s_ * .55))
    gf = on_floor(R, 2.2, .8)
    o.append(g(gf[0], gf[1], 2.2 * .6, '<rect x="-30" y="-34" width="40" height="34" fill="#c06a7e"/><rect x="-12" y="-34" width="6" height="34" fill="#f2d6a8"/><rect x="6" y="-24" width="30" height="24" fill="#6a7ab0"/><rect x="18" y="-24" width="6" height="24" fill="#f2d6a8"/><rect x="-18" y="-56" width="26" height="22" fill="#e8c46a"/><rect x="-7" y="-56" width="5" height="22" fill="#c06a7e"/>'))
    r = random.Random(12)
    o.append(''.join(f'<rect x="{r.uniform(40,500):.0f}" y="{r.uniform(200,760):.0f}" width="6" height="10" fill="{r.choice(cols)}" transform="rotate({r.uniform(-60,60):.0f} 270 450)"/>' for _ in range(40)))
    o.append(pool(280, 760, 260, 90, WARM, .45))
    o.append(shade(280, 520, 580, '#3a2a52', .4))
    o.append(dust(40, (60, 250, 480, 760), 20))
    return ''.join(o)


def pound_window():
    """ground-floor side window of the house across, close: a woman's shadow presses and pounds the glass, an arm reaches from the dark behind her"""
    o = [night_sky((90, 100), 37, 300)]
    o.append('<rect x="0" y="110" width="540" height="850" fill="#5e4644"/>' + ''.join(f'<rect x="0" y="{yy}" width="540" height="3" fill="#2e2020" opacity=".35"/>' for yy in range(116, 960, 22)))
    o.append('<polygon points="0,110 540,110 540,60 270,-30 0,60" fill="#26191c"/><rect x="0" y="102" width="540" height="12" fill="#a89688"/>')
    X0, Y0, X1, Y1 = 132, 190, 408, 620          # tall single-sash window, fills most of the frame
    o.append(f'<rect x="{X0-48}" y="{Y0}" width="38" height="{Y1-Y0}" fill="#26302c"/><rect x="{X1+10}" y="{Y0}" width="38" height="{Y1-Y0}" fill="#202824"/>')
    o.append(''.join(f'<line x1="{xx}" y1="{yy}" x2="{xx+30}" y2="{yy}" stroke="#141a18" stroke-width="2"/>' for xx in (X0 - 44, X1 + 14) for yy in range(Y0 + 10, Y1 - 6, 12)))
    o.append(f'<rect x="{X0-14}" y="{Y0-18}" width="{X1-X0+28}" height="{Y1-Y0+36}" fill="#a89688"/><rect x="{X0-22}" y="{Y0-30}" width="{X1-X0+44}" height="14" fill="#988678"/>')
    # dim interior: a hallway lamp far behind, sheer curtain catching it
    o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#4a2c2a"/>' + glow(X1 - 70, Y0 + 90, 200, '#ffc890', .75))
    o.append(f'<rect x="{X0}" y="{Y0}" width="{X1-X0}" height="{Y1-Y0}" fill="#f2d0b8" opacity=".22"/>' + ''.join(f'<rect x="{xx}" y="{Y0}" width="10" height="{Y1-Y0}" fill="#f6dcc8" opacity=".12"/>' for xx in range(X0 + 8, X1, 26)))
    # the woman's shadow behind the sheer, palms flat on the glass
    cx = (X0 + X1) / 2
    o.append(f'<g opacity=".92"><path d="M {cx-62},{Y1} C {cx-66},{Y1-120} {cx-50},{Y1-196} {cx-26},{Y1-214} C {cx-38},{Y1-236} {cx-36},{Y1-270} {cx-8},{Y1-282} C {cx+22},{Y1-288} {cx+40},{Y1-262} {cx+30},{Y1-228} C {cx+56},{Y1-206} {cx+70},{Y1-120} {cx+66},{Y1} Z" fill="#1e1216" filter="url(#dof)"/>'
             f'<path d="M {cx-14},{Y1-284} C {cx-40},{Y1-276} {cx-48},{Y1-240} {cx-44},{Y1-200} L {cx-30},{Y1-206} C {cx-30},{Y1-240} {cx-20},{Y1-264} {cx-10},{Y1-270} Z" fill="#1e1216" filter="url(#dof)"/>'   # loose hair
             f'<path d="M {cx-30},{Y1-196} C {cx-64},{Y1-230} {cx-86},{Y1-268} {cx-92},{Y1-300} L {cx-74},{Y1-306} C {cx-66},{Y1-276} {cx-48},{Y1-244} {cx-20},{Y1-214} Z" fill="#1e1216"/>'
             f'<path d="M {cx+28},{Y1-196} C {cx+60},{Y1-224} {cx+78},{Y1-256} {cx+82},{Y1-286} L {cx+100},{Y1-280} C {cx+94},{Y1-248} {cx+74},{Y1-214} {cx+38},{Y1-186} Z" fill="#1e1216"/></g>')
    # palms pressed on the glass: sharper and slightly lit at the edges
    for hx, hy, rot in ((cx - 84, Y1 - 318, -14), (cx + 92, Y1 - 300, 12)):
        o.append(f'<g transform="translate({hx},{hy}) rotate({rot})"><ellipse cx="0" cy="6" rx="15" ry="18" fill="#140a0e"/>'
                 + ''.join(f'<rect x="{fx-3}" y="{-22+abs(fx)*.4:.0f}" width="6" height="22" rx="3" fill="#140a0e"/>' for fx in (-11, -4, 4, 11)) + '<rect x="12" y="2" width="14" height="6" rx="3" fill="#140a0e" transform="rotate(-30 12 2)"/></g>')
    # an arm reaching out of the dark behind her shoulder
    o.append(f'<path d="M {X1},{Y0+150} C {X1-60},{Y0+170} {cx+60},{Y1-240} {cx+34},{Y1-226} L {cx+40},{Y1-210} C {cx+70},{Y1-222} {X1-50},{Y0+200} {X1},{Y0+196} Z" fill="#0c0608" opacity=".95" filter="url(#dof)"/>')
    # crack radiating from the left palm
    hx, hy = cx - 84, Y1 - 318
    cr = ''.join(f'<path d="M {hx},{hy} L {hx+dx},{hy+dy} L {hx+dx*1.6+ex},{hy+dy*1.6+ey}" fill="none" stroke="#ffffff" stroke-width="1.6" opacity=".85"/>' for dx, dy, ex, ey in
                 [(-40, -30, -6, 10), (30, -46, 8, -4), (46, 10, 10, 8), (-30, 40, -10, 6), (8, 54, 6, 10), (-56, -4, -8, -10)])
    o.append(cr + f'<circle cx="{hx}" cy="{hy}" r="22" fill="none" stroke="#ffffff" stroke-width="1" opacity=".5"/>')
    # sash, mullion, glare
    o.append(f'<rect x="{X0}" y="{(Y0+Y1)/2-6}" width="{X1-X0}" height="12" fill="#a89688"/><rect x="{cx-5}" y="{Y0}" width="10" height="{Y1-Y0}" fill="#a89688" opacity=".9"/>')
    o.append(f'<path d="M {X0+10},{Y0+10} L {X0+70},{Y0+10} L {X0+10},{Y0+70} Z" fill="#ffffff" opacity=".1"/>')
    # sill + empty planter
    o.append(f'<rect x="{X0-30}" y="{Y1+18}" width="{X1-X0+60}" height="12" fill="#988678"/><rect x="{X0-16}" y="{Y1+30}" width="{X1-X0+32}" height="30" fill="#3a2018"/>' + ''.join(f'<ellipse cx="{X0+i*24}" cy="{Y1+28}" rx="14" ry="9" fill="#1e2a20"/>' for i in range(12)))
    o.append(glow(cx, Y1 + 90, 240, WARM, .25) + beam(f'{X0},{Y1} {X1},{Y1} 520,960 20,960', 'beamW', .3))
    o.append(shade(cx, Y0 + 200, 560, '#0e0820', .62))
    o.append(fog(820, 160, '#9a8cc8', .22))
    o.append(dust(62, (X0, Y1, X1, 940), 14, '#ffe8d4'))
    return ''.join(o)

# ======================= SCENES =======================
S = []

S.append(('1A', 'ฉาก 1 · สถานีตำรวจ: ห้องนักสืบตอนกลางคืน', 'ช่วงเล่าชีวิตนักสืบที่ไม่มีวันหยุด โต๊ะทำงานเรียงลึก จอคอมเรืองแสง แฟ้มกองบนโต๊ะ บอร์ดคดีโยงด้ายแดงผนังซ้าย ตู้เอกสาร มู่ลี่หน้าต่างเห็นเมืองตอนดึก ไฟเพดานนีออน', police_station()))

S.append(('1B', 'ฉาก 1 · ย้อนอดีต: ซอยที่ไล่จับคนร้าย', 'ซอยตึกแถวตอนกลางคืน ร้านข้าวต้มเปิดไฟ โต๊ะกับเก้าอี้พลาสติก ป้ายร้านยื่นออกมา สายไฟพันกัน โคมผ้าแขวนข้ามซอย แอร์ ระเบียงตากผ้า มอเตอร์ไซค์จอด ลังไม้ ถุงขยะ แมวบนกันสาด ไอร้อนจากร้าน แอ่งน้ำสะท้อนไฟ ถังขยะล้มกลางทาง โทนอุ่นซีดแบบความทรงจำ', alley()))

# ---- 1B hero bedroom (late afternoon: purple interior, warm sun patch) ----
def bedroom(night=False, board=False):
    R = Room((300, 430), 150, 230, 440, 560)
    o = [R.shell(wall=WALL if not night else '#4a3440', wall_lt=WALL_LT if not night else '#56404a', wall_dk=WALL_DK if not night else '#34242e',
                 ceil=CEIL if not night else '#1e1620', floor=FLOOR if not night else '#4a2e24')]
    o.append(walls_detail(R))
    # back wall: big window, house across outside
    wx0, wy0, wx1, wy1 = 252, 268, 420, 448
    view = street('night' if night else 'day', (130, 120), hy=600, hs=1.1)
    cid = uid('cw')
    o.append(f'<clipPath id="{cid}"><rect x="{wx0}" y="{wy0}" width="{wx1-wx0}" height="{wy1-wy0}"/></clipPath>')
    o.append(f'<g clip-path="url(#{cid})"><g filter="url(#dof)" transform="translate({wx0},{wy0}) scale(.32) translate(-20,-160)">{view}</g></g>')
    o.append(f'<path d="M {wx0-9},{wy0-9} L {wx1+9},{wy0-9} L {wx1+9},{wy1+9} L {wx0-9},{wy1+9} Z M {wx0},{wy0} L {wx1},{wy0} L {wx1},{wy1} L {wx0},{wy1} Z" fill="{WOOD_DK}" fill-rule="evenodd"/>')
    o.append(f'<rect x="{(wx0+wx1)/2-3}" y="{wy0}" width="6" height="{wy1-wy0}" fill="{WOOD_DK}"/><rect x="{wx0-16}" y="{wy1+6}" width="{wx1-wx0+32}" height="10" fill="{WOOD}"/>')
    # curtains + rod
    o.append(f'<rect x="{wx0-40}" y="{wy0-28}" width="{wx1-wx0+80}" height="5" rx="2" fill="#2a1a16"/>')
    o.append(f'<path d="M {wx0-38},{wy0-24} L {wx0+8},{wy0-24} C {wx0+4},{wy0+80} {wx0+10},{wy0+160} {wx0-2},{wy1+70} L {wx0-40},{wy1+70} Z" fill="{FAB}"/><path d="M {wx0-20},{wy0-24} C {wx0-22},{wy0+80} {wx0-18},{wy0+160} {wx0-24},{wy1+70}" stroke="#7a4050" stroke-width="2" fill="none"/>')
    o.append(f'<path d="M {wx1+38},{wy0-24} L {wx1-8},{wy0-24} C {wx1-4},{wy0+80} {wx1-10},{wy0+160} {wx1+2},{wy1+70} L {wx1+40},{wy1+70} Z" fill="#84485a"/>')
    # window seat with cushions
    o.append(f'<rect x="{wx0}" y="{wy1+16}" width="{wx1-wx0}" height="46" fill="{WOOD_DK}"/><rect x="{wx0+4}" y="{wy1+14}" width="{wx1-wx0-8}" height="10" fill="{PURP}"/>'
             f'<rect x="{wx0+10}" y="{wy1-4}" width="50" height="24" rx="8" fill="{FAB_LT}"/><rect x="{wx0+66}" y="{wy1-2}" width="44" height="22" rx="8" fill="{PURP_LT}"/>')
    # back wall left: framed pictures + clock
    o.append(frame_pic(166, 262, 56, 72, inner='#5e6e8a') + frame_pic(176, 346, 36, 44, inner='#8a6a5a'))
    o.append(f'<circle cx="230" cy="300" r="12" fill="#e8dccb"/><circle cx="230" cy="300" r="9.6" fill="#3a2420"/><path d="M 230,300 L 230,292 M 230,300 L 236,303" stroke="#e8dccb" stroke-width="1.6"/>')
    # left wall: wardrobe (3D) + hanging coat
    o.append(R.box(1.02, 1.32, .0, .17, .82, WOOD_LT, WOOD_DK, WOOD))
    fa, fb = on_floor(R, 1.32, .02, .78), on_floor(R, 1.32, .16, .02)
    o.append(f'<line x1="{(fa[0]+fb[0])/2:.0f}" y1="{fa[1]:.0f}" x2="{(fa[0]+fb[0])/2:.0f}" y2="{fb[1]:.0f}" stroke="#341c14" stroke-width="2"/>')
    o.append(f'<circle cx="{(fa[0]+fb[0])/2-6:.0f}" cy="{(fa[1]+fb[1])/2:.0f}" r="2.4" fill="#d9b25a"/><circle cx="{(fa[0]+fb[0])/2+6:.0f}" cy="{(fa[1]+fb[1])/2:.0f}" r="2.4" fill="#d9b25a"/>')
    top_w = on_floor(R, 1.2, .08, .84)
    o.append(f'<rect x="{top_w[0]-16:.0f}" y="{top_w[1]-22:.0f}" width="34" height="22" fill="#a07a5a"/><rect x="{top_w[0]-10:.0f}" y="{top_w[1]-36:.0f}" width="26" height="14" fill="#8a6448"/>')  # boxes on top
    # bed against the left wall, nightstand, lamp
    o.append(R.box(1.36, 1.42, .0, .4, .34, WOOD_LT, WOOD_DK, WOOD))                   # headboard
    o.append(R.box(1.42, 2.15, .0, .4, .1, WOOD_LT, WOOD_DK, WOOD))                    # frame
    o.append(R.box(1.42, 2.15, .0, .4, .17, '#d8c8d8', PURP, PURP_LT, h0=.1))          # mattress + duvet
    o.append(R.box(1.44, 1.6, .03, .36, .22, '#f4ece8', '#d8ccc8', '#e6dcd8', h0=.17)) # pillows
    o.append(R.box(1.9, 2.15, .0, .4, .175, '#c07a8c', '#8a4a5c', '#a05a6c', h0=.1))   # throw at the foot
    o.append(R.box(1.36, 1.5, .44, .58, .16, WOOD_LT, WOOD_DK, WOOD))                  # nightstand
    lp = on_floor(R, 1.42, .51, .16); o.append(lamp_desk(lp[0], lp[1], .72, on=True))
    o.append(books(lp[0] + 10, lp[1], .5))
    # right wall: desk + chair (+ cork board / frames above), shelf
    o.append(R.box(1.04, 1.36, .7, 1.0, .22, WOOD_LT, WOOD_DK, WOOD))                 # desk
    o.append(R.box(1.38, 1.48, .7, .8, .11, WOOD_LT, WOOD_DK, WOOD))                  # chair seat
    o.append(R.box(1.46, 1.48, .7, .8, .24, WOOD_LT, WOOD_DK, WOOD, h0=.11))          # chair back
    o.append(R.box(1.385, 1.475, .705, .795, .118, FAB, FAB, FAB, h0=.11))            # seat cushion
    dt = on_floor(R, 1.18, .86, .22)
    o.append(books(dt[0] - 34, dt[1], .7) + mug(dt[0] + 16, dt[1], .9) + f'<rect x="{dt[0]-8:.0f}" y="{dt[1]-4:.0f}" width="26" height="4" fill="{PAPER}"/>')
    o.append(lamp_desk(dt[0] + 30, dt[1], .7, on=night or board))
    if board:
        o.append(R.quad('R', 1.06, 1.5, .1, .5, WOOD_DK) + R.quad('R', 1.09, 1.47, .13, .47, '#a77a5c'))
        r = random.Random(4); pins = []
        for i in range(9):
            s0 = 1.11 + r.uniform(0, .28); a0 = .15 + r.uniform(0, .24)
            o.append(R.quad('R', s0, s0 + .07, a0, a0 + .08, PAPER) + R.quad('R', s0 + .008, s0 + .062, a0 + .01, a0 + .055, '#5e5070'))
            pins.append(R.P('R', s0 + .035, a0 + .005))
        o.append(f'<polyline points="{pts(*pins)}" fill="none" stroke="{RED}" stroke-width="1.6"/>' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffd34a"/>' for x, y in pins))
        o.append(R.quad('R', 1.36, 1.46, .38, .44, '#ffe58a'))
    else:
        o.append(R.quad('R', 1.08, 1.3, .16, .36, WOOD_DK) + R.quad('R', 1.1, 1.28, .19, .33, '#6e7ea0'))
        o.append(R.quad('R', 1.36, 1.5, .2, .34, WOOD_DK) + R.quad('R', 1.38, 1.48, .23, .31, '#a08068'))
    # wall shelf on the right wall nearer, with plant + jars
    o.append(R.quad('R', 1.62, 2.1, .3, .325, WOOD))
    sp = R.P('R', 1.72, .3); sq = R.P('R', 1.95, .3)
    o.append(plant(sp[0] - 4, sp[1], .9) + f'<rect x="{sq[0]-14:.0f}" y="{sq[1]-26:.0f}" width="14" height="26" fill="#c9b49a"/><rect x="{sq[0]+2:.0f}" y="{sq[1]-18:.0f}" width="12" height="18" fill="#7a8a9a"/>')
    # rug, laundry basket, guitar, boxes, slippers
    rug = [R.P('F', 1.65, .3), R.P('F', 1.65, .82), R.P('F', 2.7, .86), R.P('F', 2.7, .26)]
    o.append(f'<polygon points="{pts(*rug)}" fill="#7a4a5e"/><polygon points="{pts(*[lerp(rug[0],rug[2],.06), lerp(rug[1],rug[3],.06), lerp(rug[2],rug[0],.06), lerp(rug[3],rug[1],.06)])}" fill="none" stroke="#c09080" stroke-width="2"/>')
    o.append(R.box(2.25, 2.4, .43, .51, .08, '#b89a74', '#8a6e50', '#9e8060'))         # wicker laundry basket
    o.append(f'<path d="M {R.P("F",2.25,.44)[0]:.0f},{R.P("F",2.25,.44)[1]-28:.0f} q 10,-12 20,-2" fill="none" stroke="#e8dccb" stroke-width="4"/>')
    o.append(R.box(2.75, 3.25, .8, 1.0, .1, '#a07a5a', '#7a5a42', '#8a6a4e'))           # cardboard boxes
    o.append(R.box(2.85, 3.15, .82, .97, .17, '#b08a68', '#8a6a4e', '#9a7a5a', h0=.1))
    gp = R.P('L', 2.4, .66)
    o.append(f'<g transform="translate({gp[0]+30:.0f},{gp[1]+20:.0f}) rotate(-12)"><ellipse cx="0" cy="40" rx="24" ry="30" fill="#9a5a34"/><ellipse cx="0" cy="8" rx="18" ry="22" fill="#9a5a34"/><circle cx="0" cy="26" r="7" fill="#2a1410"/>'
             f'<rect x="-3" y="-70" width="6" height="80" fill="#3a2016"/><rect x="-6" y="-86" width="12" height="18" rx="2" fill="#3a2016"/></g>')   # guitar leaning
    o.append(R.box(1.85, 2.05, .78, 1.0, .24, '#5a6a6e', '#36444a', '#46565c'))        # armchair back
    o.append(R.box(2.05, 2.3, .78, 1.0, .11, '#6a7a7e', '#36444a', '#46565c'))         # armchair seat
    o.append(R.box(2.05, 2.3, .76, .8, .16, '#5a6a6e', '#36444a', '#46565c'))          # armrest
    # pendant lamp from the ceiling
    pc = R.P('C', 1.5, .5)
    o.append(f'<line x1="{pc[0]:.0f}" y1="{pc[1]:.0f}" x2="{pc[0]:.0f}" y2="{pc[1]+50:.0f}" stroke="#1a1012" stroke-width="2"/><path d="M {pc[0]-22:.0f},{pc[1]+74:.0f} L {pc[0]+22:.0f},{pc[1]+74:.0f} L {pc[0]+12:.0f},{pc[1]+50:.0f} L {pc[0]-12:.0f},{pc[1]+50:.0f} Z" fill="#7a5a4a"/>')
    if board:
        tp = on_floor(R, 1.3, .52)
        o.append(f'<g transform="translate({tp[0]:.0f},{tp[1]-150:.0f})"><path d="M 0,36 L -24,150 M 0,36 L 24,150 M 0,36 L 0,154" stroke="#1e1214" stroke-width="3"/><rect x="-18" y="14" width="30" height="22" rx="3" fill="#1e1214"/><rect x="10" y="18" width="38" height="14" rx="3" fill="#2e2024"/><circle cx="50" cy="25" r="7" fill="#120a0c"/></g>')
        r = random.Random(9)
        for _ in range(12):
            s = r.uniform(1.6, 3.4); u = r.uniform(.12, .9); p = R.P('F', s, u); a = r.uniform(-30, 30)
            o.append(f'<rect x="{p[0]:.0f}" y="{p[1]:.0f}" width="{14*s:.0f}" height="{9*s:.0f}" fill="{PAPER}" transform="rotate({a:.0f} {p[0]:.0f} {p[1]:.0f})" opacity=".9"/>')
        o.append(mug(*on_floor(R, 2.0, .62), 2.2) + mug(*on_floor(R, 2.1, .7), 2.2, '#c9b49a'))
    # lighting
    if night:
        o.append(beam(f'{wx0},{wy0} {wx1},{wy0} 470,960 120,960', 'beamC', .5))
        o.append(shade(dt[0] + 30, dt[1] - 60, 430, '#1a1030', .72))
        o.append(dust(21, (180, 300, 460, 900), 22, '#e6e2ff'))
    else:
        sun = [R.P('F', 1.55, .45), R.P('F', 1.55, .95), R.P('F', 2.7, 1.0), R.P('F', 2.7, .5)]
        o.append(f'<polygon points="{pts(*sun)}" fill="#ffd8b0" opacity=".4" filter="url(#soft)" style="mix-blend-mode:screen"/>')
        o.append(beam(f'{wx0},{wy0} {wx1},{wy0} {sun[2][0]:.0f},{sun[2][1]:.0f} {sun[3][0]:.0f},{sun[3][1]:.0f}', 'beamW', .7))
        o.append(shade(335, 520, 520, '#24163a', .55))
        o.append(dust(22, (220, 300, 500, 860), 26))
    return ''.join(o)

S.append(('1C', 'ฉาก 1 · โรงพยาบาลหลังอุบัติเหตุ (โพล้เพล้)', 'ห้องพักผู้ป่วย เตียงพร้อมที่แขวนขาเข้าเฝือก เสาน้ำเกลือ จอวัดชีพจร ช่อดอกไม้ ตะกร้าผลไม้ และการ์ดหัวใจจากแฟนบนโต๊ะข้างเตียง ไม้ค้ำยันรออยู่ที่ผนัง แสงโพล้เพล้ลอดมู่ลี่ ใช้กับ VO "ทำให้ขาหักและต้องพักรักษาตัวสองเดือน" และช่วงแนะนำแฟนที่มาเยี่ยม', hospital_room()))
S.append(('1D', 'ฉาก 1 · ห้องนั่งเล่นชั้นล่างบ้านพระเอก (หัวค่ำ)', 'ประตูหน้าบ้านกับหน้าต่างบนผนังหลัง บันไดขึ้นชั้นสองชิดผนังซ้าย โซฟาหันหน้าเข้ากล้อง ทีวี รูปครอบครัว โคมตั้งพื้นส่องเป็นวงอุ่น ใช้กับช็อตกลับบ้านพร้อมเฝือกและประโยคของแฟน "ก็ดีแล้วไง จะได้พักบ้าง" และตอนพระเอกรีบลงบันไดออกจากบ้านในฉาก 7', ground_living()))
S.append(('2A', 'ฉาก 2 · ห้องนั่งเล่นชั้นสอง (แฟมิลีรูมกึ่งสตูดิโอ) ยามบ่าย', 'ห้องที่พระเอกใช้ชีวิตช่วงพักขา หน้าต่างบานใหญ่สามช่องเห็นบ้านตรงข้าม มุมอาร์มแชร์ริมหน้าต่างพร้อมโต๊ะข้างวางกาแฟ ชั้นหนังสือบิลต์อินผนังซ้าย โซฟากับหมอนอิง โต๊ะกลาง พรม ทีวีกับมุมทำงานผนังขวา คานเพดานไม้ ไม้ค้ำยันพิงโซฟา', family_room()))

S.append(('2B', 'ฉาก 2 · มองจากหน้าต่าง: รถขนของมาจอดบ้านตรงข้าม', 'กรอบหน้าต่างพระเอกมืดเป็นฉากหน้ามีแสงขอบ บ้านตรงข้ามเห็นด้านข้างเป็นสามมิติ มีเสาไฟและสายไฟ รถขนของกับกล่องหน้าบ้าน',
          street('day', extra_front=(cast('<rect x="40" y="560" width="200" height="70"/>') +
                 '<g transform="translate(36,540) scale(.85)"><rect width="170" height="96" rx="5" fill="#ece4f6"/><rect width="170" height="12" fill="#cfc2e6"/><rect x="0" y="80" width="170" height="16" fill="#b9aad6"/>'
                 '<rect x="170" y="28" width="60" height="68" rx="6" fill="#8f7cc8"/><rect x="180" y="38" width="40" height="26" rx="3" fill="#4a3f86"/>'
                 '<circle cx="40" cy="98" r="14" fill="#2a2148"/><circle cx="194" cy="98" r="14" fill="#2a2148"/>'
                 '<text x="85" y="56" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#8a76b8" text-anchor="middle">ขนย้าย</text></g>'
                 '<g transform="translate(240,590)"><rect width="36" height="30" fill="#c9a88e"/><rect x="40" y="8" width="30" height="22" fill="#b8967e"/><rect x="14" y="-20" width="26" height="20" fill="#d6b49a"/></g>'
                 + dust(31, (60, 120, 480, 600), 16))) + window_fg(None, night=False)))

S.append(('3A', 'ฉาก 3 · บ้านตรงข้ามยามเช้า', 'แสงเช้าส่องจากซ้าย เงาบ้านทอดยาวสีม่วง พุ่มกุหลาบหน้าบ้านสำหรับช็อตภรรยารดน้ำต้นไม้',
          street('morning', extra_front=beam('0,80 140,80 420,620 120,620', 'beamW', .6) + dust(32, (60, 120, 420, 600), 18)) + window_fg(None, night=False)))

S.append(('3B', 'ฉาก 3 · คืนวันศุกร์ ห้องนั่งเล่นเปิดไฟ', 'ท้องฟ้าม่วงคราม พระจันทร์ ไฟห้องนั่งเล่นอุ่น ผ้าม่านแง้ม รอเงาคนทะเลาะ',
          street('fight', extra_front=dust(33, (80, 380, 300, 600), 12, '#ffe8d4')) + window_fg(WARM)))

S.append(('3C', 'ฉาก 3 · ระยะใกล้หน้าต่างห้องนั่งเล่น: ทะเลาะกัน', 'กล้องซูมเข้าหน้าต่างบ้านตรงข้ามจนเต็มเฟรม ผ้าม่านเปิด เห็นห้องนั่งเล่นสว่าง โคมตั้งพื้น โซฟา แก้วไวน์แตกกับไวน์หกบนพื้น ใช้กับเงาภรรยาปาแก้ว แล้วสามีเดินมาปิดม่าน', window_closeup('open')))
S.append(('3D', 'ฉาก 3 · ระยะใกล้หน้าต่าง: ปิดม่าน ไฟดับ', 'หน้าต่างเดิมหลังไฟดับ เหลือแสงจันทร์ เว้นความเงียบสั้น ๆ ก่อน VO นับตั้งแต่คืนนั้น', window_closeup('dark')))
S.append(('4', 'ฉาก 4 · ตีสอง ลากถุงดำขึ้นท้ายรถ', 'ไฟบ้านดับหมด เหลือไฟหน้าประตู ไฟถนนส่องเป็นวง รถเปิดท้ายรออยู่ข้างบ้าน',
          street('dark', moon=(110, 120), extra_front=(cast('<rect x="330" y="580" width="170" height="40"/>') +
                 '<g transform="translate(410,618)"><path d="M -74,0 L -70,-26 C -64,-36 -42,-38 -30,-38 L 24,-38 C 40,-38 52,-32 60,-24 L 74,-20 L 76,0 Z" fill="#4a3f7e"/>'
                 '<path d="M -56,-28 L -48,-36 L -6,-36 L -6,-26 Z M 0,-36 L 24,-36 C 34,-36 42,-32 48,-26 L 0,-26 Z" fill="#241c48"/>'
                 '<path d="M 60,-24 L 92,-62 L 102,-56 L 76,-20 Z" fill="#5a4f92"/><circle cx="-44" cy="2" r="12" fill="#1a1436"/><circle cx="46" cy="2" r="12" fill="#1a1436"/>'
                 '<rect x="66" y="-18" width="8" height="6" fill="#ff7a8a"/></g>'
                 + '<rect x="497" y="300" width="6" height="330" fill="#2a2150"/><rect x="470" y="296" width="34" height="8" fill="#2a2150"/><rect x="470" y="304" width="18" height="6" fill="#ffd8a8"/>'
                 + glow(479, 312, 130, WARM, .7) + pool(470, 620, 120, 30, WARM, .5) + beam('462,310 498,310 560,640 380,640', 'beamW', .55)
                 + dust(34, (390, 320, 540, 640), 14, '#ffe8d4'))) + window_fg(None)))

S.append(('5A', 'ฉาก 5 · ห้องนั่งเล่นชั้นสองกลายเป็นห้องสืบสวน (กลางคืน)', 'ห้องเดิมตอนกลางคืน บอร์ดรูปโยงด้ายแดงกับแผนที่ถนนบนผนังขวา จอคอมกับโคมโต๊ะเปิด กล้องบนขาตั้งหันออกหน้าต่าง กระดาษกระจายเต็มพื้น แก้วกาแฟหลายใบบนโต๊ะกลาง แสงจันทร์จากหน้าต่าง', family_room(night=True, board=True)))

# ---- 5B phone on bedside table, top-down ----
o = ['<rect width="540" height="960" fill="#4a2e26"/>']
o.append(''.join(f'<path d="M -20,{y} C 160,{y-30} 380,{y+20} 560,{y-10}" stroke="#3a2420" stroke-width="2" fill="none"/>' for y in range(40, 1000, 46)))
o.append(glow(60, 120, 260, WARM, .55))  # lamp spill from the corner
o.append('<g transform="translate(30,40)"><circle r="70" fill="#5a3a2e"/><circle r="56" fill="#ffe0b8" opacity=".9"/></g>')  # lamp base from above
o.append(cast('<rect x="150" y="170" width="240" height="470" rx="30"/>', 18, 22, .6))
o.append('<rect x="150" y="170" width="240" height="470" rx="30" fill="#1d1838"/><rect x="160" y="180" width="220" height="450" rx="24" fill="url(#phoneScr)"/>')
o.append(glow(270, 400, 260, '#c8d0ff', .5))
o.append('<rect x="236" y="190" width="68" height="14" rx="7" fill="#1d1838"/>')
o.append('<text x="270" y="252" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#7a6ea0" text-anchor="middle">ไม่ทราบหมายเลข</text>')
o.append('<text x="270" y="272" font-family="Inter, sans-serif" font-size="11" fill="#9a90bc" text-anchor="middle">02:47</text>')
o.append('<rect x="176" y="296" width="176" height="74" rx="16" fill="#e2d8f6"/>')
o.append('<text font-family="IBM Plex Sans Thai, sans-serif" font-size="17" fill="#2a1a18"><tspan x="192" y="326">ช่วยฉันด้วย</tspan><tspan x="192" y="352">ฉันยังอยู่ในบ้าน</tspan></text>')
o.append('<rect x="176" y="576" width="188" height="32" rx="16" fill="#ece6fa"/>')
o.append('<path d="M 410,660 C 440,720 470,760 560,780" fill="none" stroke="#2a1a18" stroke-width="6"/>')
o.append(cast('<circle cx="90" cy="780" r="46"/>', 10, 12, .5) + '<g transform="translate(90,780)"><circle r="46" fill="#e6dcf2"/><circle r="36" fill="#6a3c38"/><ellipse cx="-8" cy="-8" rx="12" ry="6" fill="#ffffff" opacity=".25"/></g>')
o.append('<g transform="translate(430,860) rotate(18)"><rect x="-50" y="-16" width="100" height="32" rx="4" fill="#2a1a18"/><circle cx="-34" cy="0" r="9" fill="#3a2620"/></g>')  # glasses case / remote
o.append(shade(270, 400, 460, '#1a1240', .7))
o.append(dust(35, (120, 160, 420, 620), 12, '#eae6ff'))
S.append(('5B', 'ฉาก 5 · ข้อความจากเบอร์ไม่รู้จัก', 'มุมจากบนลงโต๊ะข้างเตียง จอมือถือเรืองแสงเป็นแหล่งแสงหลัก แสงโคมอุ่นล้นเข้ามาจากมุม ข้อความ "ช่วยฉันด้วย ฉันยังอยู่ในบ้าน" เวลา 02:47', ''.join(o)))

S.append(('5C', 'ฉาก 5 · ระยะใกล้หน้าต่างข้างบ้าน: เงาผู้หญิงทุบกระจก', 'หน้าต่างบานสูงชั้นล่างอีกบานของบ้านตรงข้าม (ไม่ใช่หน้าต่างห้องนั่งเล่น) เต็มเฟรม ข้างในมืดสลัว มีโคมทางเดินไกล ๆ เงาผู้หญิงผมยาวอยู่หลังผ้าม่านโปร่ง ฝ่ามือสองข้างแนบกระจก กระจกร้าวจากฝ่ามือ มีแขนอีกคนยื่นออกมาจากความมืดด้านหลังเพื่อดึงเธอกลับ', pound_window()))

# ---- 6A street level, dusk: wide, depth ----
o = []
o.append(street('night', moon=(120, 120), hy=520, hs=.95, extra_front=''))
# hero's house edge as dark foreground on the right + road receding
o.append(f'<polygon points="{pts((0,620),(540,580),(540,960),(0,960))}" fill="#3a2a2a"/>')
o.append(f'<polygon points="{pts((0,700),(540,640),(540,700),(0,790))}" fill="#4a3634"/>')
o.append(''.join(f'<polygon points="{pts((x,742-x*.1),(x+50,737-x*.1),(x+50,742-x*.1),(x,747-x*.1))}" fill="#a08a7a" opacity=".7"/>' for x in range(0, 540, 110)))
o.append('<polygon points="400,0 540,0 540,960 450,960 450,420 400,380" fill="#1e1416"/><rect x="452" y="430" width="88" height="530" fill="#2a1c1e"/>')
o.append('<rect x="470" y="470" width="50" height="70" fill="url(#winLit)"/>' + glow(495, 505, 80, WARM, .6))
o.append('<rect x="20" y="300" width="7" height="330" fill="#1e1416"/><rect x="20" y="296" width="44" height="8" fill="#1e1416"/><rect x="44" y="304" width="20" height="6" fill="#ffd8a8"/>' + glow(54, 312, 140, WARM, .75) + pool(80, 700, 170, 46, WARM, .5))
o.append(beam('36,310 70,310 240,740 0,740', 'beamW', .5))
o.append(dust(37, (0, 320, 260, 760), 16))
S.append(('6A', 'ฉาก 6 · ถนนหน้าบ้านตอนค่ำ (ระดับสายตา)', 'มุมกว้างระดับถนน บ้านตรงข้ามอยู่ไกล ขอบบ้านพระเอกมืดเป็นฉากหน้าด้านขวา ถนนทอดลึก ไฟถนนเป็นวงอุ่นให้แฟนสาวเดินข้ามผ่าน', ''.join(o)))

S.append(('6B', 'ฉาก 6 · เงาสองคนบนผ้าม่าน แล้วไฟดับ', 'ผ้าม่านห้องนั่งเล่นปิด เรืองแสงอุ่นกลางบ้านมืด ไว้วางเงาสองคนต่อสู้กัน',
          street('shadow', moon=(450, 110)) + window_fg(None)))

# ---- 7A staircase down (one-point, from the top) ----
o = []
o.append('<rect width="540" height="960" fill="#2c1e22"/>')
o.append(f'<polygon points="{pts((0,0),(160,300),(160,960),(0,960))}" fill="#5a3e3a"/><polygon points="{pts((540,0),(380,300),(380,960),(540,960))}" fill="#46302e"/>')
for i in range(12):
    t0 = i / 12; t1 = (i + 1) / 12
    y0 = 960 - (960 - 330) * (t0 ** .8); y1 = 960 - (960 - 330) * (t1 ** .8)
    xl0 = 0 + 160 * t0; xr0 = 540 - 160 * t0; xl1 = 160 * t1; xr1 = 540 - 160 * t1
    o.append(f'<polygon points="{pts((xl0,y0),(xr0,y0),(xr1,y1+ (y0-y1)*.35),(xl1,y1+(y0-y1)*.35))}" fill="{"#7a4e36" if i%2 else "#6a4430"}"/>')
    o.append(f'<polygon points="{pts((xl1,y1+(y0-y1)*.35),(xr1,y1+(y0-y1)*.35),(xr1,y1),(xl1,y1))}" fill="#4a2e22"/>')
o.append(f'<rect x="160" y="200" width="220" height="130" fill="#1a1012"/>')  # dark hallway below
o.append(f'<path d="M 10,240 L 170,420 L 170,800" fill="none" stroke="#8a5a3e" stroke-width="9"/>')
o.append(''.join(f'<line x1="{20+i*16}" y1="{254+i*18}" x2="{20+i*16}" y2="{254+i*18+90}" stroke="#8a5a3e" stroke-width="4"/>' for i in range(10)))
o.append(f'<rect x="0" y="0" width="540" height="90" fill="#46302e"/>')
o.append(glow(270, -40, 360, WARM, .7))  # light from the bedroom upstairs behind camera
o.append(beam('140,0 400,0 470,960 70,960', 'beamW', .55))
o.append(frame_pic(420, 380, 60, 80) + frame_pic(430, 520, 50, 64))
o.append(shade(270, 860, 640, '#1a1240', .6))
o.append(dust(38, (100, 60, 460, 900), 18))
S.append(('6C', 'ฉาก 6 · ระยะใกล้ผ้าม่าน: ละครเงา', 'ผ้าม่านปิดสนิทเรืองแสงอุ่นเต็มเฟรม เว้นที่ว่างให้เงาสองคนต่อสู้กัน เงาแฟนล้มลง แล้วตัดไปไฟดับ (ใช้ 3D ต่อ)', window_closeup('closed')))
S.append(('7A', 'ฉาก 7 · บันไดบ้านพระเอก', 'มองจากหัวบันไดลงไป ขั้นบันไดทอดลึกสู่โถงมืด แสงอุ่นจากห้องชั้นบนส่องตามหลัง ราวจับเป็นเส้นนำสายตา', ''.join(o)))

# ---- 7B porch: front door ajar, dark inside ----
R = Room((270, 470), 120, 170, 420, 760)
o = [R.shell(wall='#5a3e3a', wall_lt='#6a4a44', wall_dk='#42302e', ceil='#2a1c1c', floor='#5a3a2a', planks=True)]
o.append(''.join(f'<line x1="{R.x0}" y1="{yy}" x2="{R.x1}" y2="{yy}" stroke="#3a2622" stroke-width="1.4" opacity=".5"/>' for yy in range(R.y0+10, R.y1, 16)))
for face in ('L', 'R'):
    for a_ in [k/14 for k in range(1, 14)]:
        p0, p1 = R.P(face, 1, a_), R.P(face, 6, a_)
        o.append(f'<line x1="{p0[0]:.0f}" y1="{p0[1]:.0f}" x2="{p1[0]:.0f}" y2="{p1[1]:.0f}" stroke="#3a2622" stroke-width="1.6" opacity=".45"/>')
o.append(R.box(1.15, 1.45, .74, .98, .2, WOOD_LT, WOOD_DK, WOOD))              # bench on the porch
o.append(R.box(1.4, 1.45, .74, .98, .36, WOOD_LT, WOOD_DK, WOOD, h0=.2))
o.append(R.box(1.18, 1.4, .76, .96, .215, FAB, FAB, FAB, h0=.2))               # cushion
bp = on_floor(R, 1.25, .1); o.append(plant(bp[0], bp[1], 1.6, '#7a4a3a'))
bq = on_floor(R, 1.6, .9); o.append(plant(bq[0], bq[1], 2.2, '#5a3a2e'))
up = on_floor(R, 1.22, .66)
o.append(f'<rect x="{up[0]-12:.0f}" y="{up[1]-40:.0f}" width="24" height="40" fill="#3a2a2a"/><path d="M {up[0]-4:.0f},{up[1]-40:.0f} L {up[0]-8:.0f},{up[1]-92:.0f} M {up[0]+5:.0f},{up[1]-40:.0f} L {up[0]+8:.0f},{up[1]-86:.0f}" stroke="#2a1a1a" stroke-width="4"/><path d="M {up[0]-14:.0f},{up[1]-92:.0f} q 6,-8 12,0" fill="none" stroke="#2a1a1a" stroke-width="3"/>')
bt = on_floor(R, 1.5, .62)
o.append(f'<path d="M {bt[0]-26:.0f},{bt[1]:.0f} L {bt[0]-26:.0f},{bt[1]-34:.0f} L {bt[0]-12:.0f},{bt[1]-34:.0f} L {bt[0]-12:.0f},{bt[1]-10:.0f} L {bt[0]-2:.0f},{bt[1]-6:.0f} L {bt[0]-2:.0f},{bt[1]:.0f} Z M {bt[0]+4:.0f},{bt[1]:.0f} L {bt[0]+4:.0f},{bt[1]-34:.0f} L {bt[0]+18:.0f},{bt[1]-34:.0f} L {bt[0]+18:.0f},{bt[1]-10:.0f} L {bt[0]+28:.0f},{bt[1]-6:.0f} L {bt[0]+28:.0f},{bt[1]:.0f} Z" fill="#2e2a26"/>')

o.append('<rect x="170" y="230" width="200" height="530" fill="#d6cbea"/><rect x="182" y="242" width="176" height="518" fill="#0e0b22"/>')
o.append(f'<polygon points="{pts((182,242),(300,272),(300,760),(182,760))}" fill="#4a3266"/>')  # door swung inward
o.append(f'<polygon points="{pts((192,262),(290,286),(290,440),(192,430))}" fill="none" stroke="#6a4c88" stroke-width="3"/><polygon points="{pts((192,470),(290,480),(290,720),(192,720))}" fill="none" stroke="#6a4c88" stroke-width="3"/>')
o.append('<circle cx="282" cy="520" r="5" fill="#e6c38a"/>')
o.append(pool(330, 700, 60, 18, '#c8d0ff', .9) + '<rect x="318" y="694" width="26" height="12" rx="3" fill="#dcd4ff"/>')  # phone glowing on the floor inside
o.append(R.quad('R', 1.1, 1.35, .3, .4, '#2a2148') + '<rect x="0" y="0" width="0" height="0"/>')
lpt = R.P('R', 1.22, .32)
o.append(f'<rect x="{lpt[0]-6:.0f}" y="{lpt[1]-10:.0f}" width="14" height="22" rx="3" fill="{WARM}"/>' + glow(lpt[0], lpt[1], 140, WARM, .85) + pool(300, 820, 260, 80, WARM, .55))
mat = [R.P('F', 1.05, .3), R.P('F', 1.05, .7), R.P('F', 1.3, .72), R.P('F', 1.3, .28)]
o.append(f'<polygon points="{pts(*mat)}" fill="#6e4a5c"/>')
o.append(R.box(1.3, 1.6, .0, .18, .14, '#5a4888', '#3a2f62', '#4a3c78'))  # planter left
o.append('<ellipse cx="40" cy="700" rx="60" ry="44" fill="#2a3a5e"/><ellipse cx="60" cy="680" rx="30" ry="22" fill="#3b4a72"/>')
o.append('<rect x="440" y="300" width="70" height="56" fill="#2a2148"/><rect x="446" y="306" width="58" height="44" fill="#3a2f62"/>')  # mailbox / number plate
o.append(beam(f'{lpt[0]-10:.0f},{lpt[1]:.0f} {lpt[0]+20:.0f},{lpt[1]:.0f} 470,960 160,960', 'beamW', .45))
o.append(shade(lpt[0], lpt[1] + 120, 520, '#140f30', .6))
o.append(dust(39, (200, 260, 520, 900), 14))
S.append(('7B', 'ฉาก 7 · ประตูบ้านตรงข้ามเปิดแง้ม', 'ระเบียงหน้าบ้านเปอร์สเปกทีฟ ไฟหน้าประตูดวงเดียวส่องเป็นวงอุ่น ข้างในมืดสนิท มีแสงมือถือของแฟนเรืองอยู่บนพื้น เว้นจังหวะเงียบก่อนผลักประตู', ''.join(o)))

S.append(('7C', 'ฉาก 7 · เซอร์ไพรส์! ห้องนั่งเล่นเปิดไฟ', 'ห้องเปอร์สเปกทีฟจุดเดียว ป้าย SURPRISE ไฟประดับตามขอบเพดาน ลูกโป่ง โซฟาด้านหลัง เค้กเทียนกลางห้อง กระดาษสีลอย สว่างและอุ่นที่สุดในเรื่อง แต่มุมห้องยังเงาม่วง', party_room()))

# ---- 8A pull back from the party window, from the garden ----
o = [street('party', moon=(420, 110), hy=640, hs=1.25)]
o.append('<g filter="url(#dof)"><ellipse cx="60" cy="900" rx="160" ry="120" fill="#1a1436"/><ellipse cx="500" cy="920" rx="150" ry="110" fill="#1a1436"/>'
         '<ellipse cx="120" cy="840" rx="70" ry="50" fill="#241d4a"/></g>')
o.append(''.join(f'<rect x="{x}" y="{780}" width="10" height="180" fill="#211a44"/>' for x in range(0, 540, 34)) + '<rect x="0" y="800" width="540" height="8" fill="#211a44"/><rect x="0" y="860" width="540" height="8" fill="#211a44"/>')
o.append(shade(160, 560, 560, '#140f30', .45))
o.append(dust(41, (60, 440, 320, 700), 12, '#ffe8d4'))
S.append(('8A', 'ฉาก 8 · กล้องถอยออกจากหน้าต่างงานเลี้ยง', 'มองจากสวนหน้าบ้าน รั้วกับพุ่มไม้มืดเป็นฉากหน้า หน้าต่างงานเลี้ยงสว่างอุ่นมีลูกโป่ง ก่อนแพนไปบ้านหลังที่สาม', ''.join(o)))

# ---- 8B dark room in the third house ----
R = Room((270, 400), 130, 160, 410, 520)
o = [R.shell(wall='#3a2830', wall_lt='#46323a', wall_dk='#2a1c24', ceil='#16101a', floor='#2e1e1c')]
o.append(walls_detail(R, wall_stripe='#2e1e26', wain='#24161a', wain_lt='#2e1c1e'))
o.append(R.box(1.6, 1.9, .82, 1.0, .5, '#4a4a52', '#2e2e36', '#3a3a42'))           # filing cabinet
for k_ in range(3):
    fa_ = on_floor(R, 1.9, .86, .1 + k_ * .14); fb_ = on_floor(R, 1.9, .97, .1 + k_ * .14)
    o.append(f'<line x1="{fa_[0]:.0f}" y1="{fa_[1]:.0f}" x2="{fb_[0]:.0f}" y2="{fb_[1]:.0f}" stroke="#1e1e24" stroke-width="2"/>')
o.append(R.box(1.9, 2.3, .0, .2, .14, '#5a3e2e', '#3a281e', '#4a3226'))            # boxes stacked left
o.append(R.box(1.95, 2.25, .02, .18, .26, '#6a4a36', '#3a281e', '#4a3226', h0=.14))
o.append(R.box(1.55, 1.7, .4, .56, .12, '#3a2a24', '#22160f', '#2e2018'))          # chair pulled out
o.append(R.box(1.66, 1.7, .4, .56, .3, '#3a2a24', '#22160f', '#2e2018', h0=.12))

wx0, wy0, wx1, wy1 = 170, 200, 370, 430
view = street('party', (120, 120), hy=600, hs=1.1)
cid = uid('cw')
o.append(f'<clipPath id="{cid}"><rect x="{wx0}" y="{wy0}" width="{wx1-wx0}" height="{wy1-wy0}"/></clipPath><g clip-path="url(#{cid})"><g filter="url(#dof2)" transform="translate({wx0},{wy0}) scale(.4) translate(0,-120)">{view}</g></g>')
o.append(f'<path d="M {wx0-8},{wy0-8} L {wx1+8},{wy0-8} L {wx1+8},{wy1+8} L {wx0-8},{wy1+8} Z M {wx0},{wy0} L {wx1},{wy0} L {wx1},{wy1} L {wx0},{wy1} Z" fill="#3e3474" fill-rule="evenodd"/><rect x="{(wx0+wx1)/2-3}" y="{wy0}" width="6" height="{wy1-wy0}" fill="#3e3474"/>')
o.append(f'<path d="M 140,170 L 176,170 C 172,280 178,380 168,470 L 140,470 Z" fill="#1c1640"/><path d="M 400,170 L 364,170 C 368,280 362,380 372,470 L 400,470 Z" fill="#1c1640"/>')
# photos pinned on both walls
r = random.Random(13)
for face in ('L', 'R'):
    for _ in range(9):
        s0 = 1.05 + r.uniform(0, 1.2); a0 = .1 + r.uniform(0, .5)
        o.append(R.quad(face, s0, s0 + .09, a0, a0 + .1, '#cfc6e6') + R.quad(face, s0 + .01, s0 + .08, a0 + .01, a0 + .07, '#4c4280'))
# desk under the window covered in photos + binoculars on tripod
o.append(R.box(1.05, 1.5, .1, .9, .26, '#3e3474', '#241d4c', '#2e2660'))
dt = (R.y1 - R.y0)
for i in range(14):
    s = r.uniform(1.08, 1.45); u = r.uniform(.15, .85); p = R.P('F', s, u); y = p[1] - dt * s * .26
    o.append(f'<g transform="rotate({r.uniform(-25,25):.0f} {p[0]:.0f} {y:.0f})"><rect x="{p[0]-14:.0f}" y="{y-8:.0f}" width="30" height="22" fill="#d6cfec"/><rect x="{p[0]-11:.0f}" y="{y-5:.0f}" width="24" height="14" fill="#5a4f92"/></g>')
hp = R.P('F', 1.3, .4); hy_ = hp[1] - dt * 1.3 * .26
o.append(f'<g transform="translate({hp[0]-40:.0f},{hy_-12:.0f}) rotate(-8)"><rect x="0" y="0" width="70" height="52" fill="#efe8fa"/><rect x="5" y="5" width="60" height="36" fill="#6a5fa0"/><path d="M 14,41 L 14,22 L 30,14 L 46,22 L 46,41 Z" fill="#3a3070"/><rect x="38" y="20" width="16" height="12" fill="#ffd8a8"/></g>')  # photo of the hero's window
o.append(''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.4" fill="{RED}"/>' for x, y in [(hp[0] - 30, hy_ - 6), (hp[0] + 60, hy_ + 14)]))
bp = R.P('F', 1.2, .62); by_ = bp[1] - dt * 1.2 * .26
o.append(f'<g transform="translate({bp[0]:.0f},{by_-40:.0f})"><rect x="-40" y="-14" width="34" height="30" rx="8" fill="#120e26"/><rect x="6" y="-14" width="34" height="30" rx="8" fill="#120e26"/><rect x="-8" y="-6" width="16" height="12" fill="#0c0a1c"/>'
         '<circle cx="-23" cy="-14" r="10" fill="#241e48"/><circle cx="23" cy="-14" r="10" fill="#241e48"/><circle cx="-26" cy="-17" r="3" fill="#d6d0ff" opacity=".9"/><circle cx="20" cy="-17" r="3" fill="#d6d0ff" opacity=".9"/>'
         '<path d="M 0,16 L -24,56 M 0,16 L 24,56 M 0,16 L 0,58" stroke="#120e26" stroke-width="3"/></g>')
o.append(beam(f'{wx0},{wy1} {wx1},{wy1} 470,960 70,960', 'beamC', .6))
o.append(pool(270, 700, 220, 70, COOL, .35))
o.append(shade(270, 330, 460, '#0e0a24', .7))
o.append(dust(42, (150, 430, 420, 920), 18, '#e2deff'))
S.append(('8B', 'ฉาก 8 · ห้องมืดในบ้านหลังที่สาม', 'ห้องเปอร์สเปกทีฟ มืดและเย็นที่สุดในเรื่อง แสงจันทร์จากหน้าต่างเป็นแหล่งเดียว เห็นงานเลี้ยงไกล ๆ แบบเบลอ รูปถ่ายติดเต็มผนังสองข้าง โต๊ะเต็มไปด้วยรูป รวมรูปหน้าต่างห้องพระเอก กล้องส่องทางไกลบนขาตั้ง', ''.join(o)))

# ---------------- page ----------------
CH = {'1': ('นักสืบที่ไม่มีคดี', 'งานหนักที่สถานี → ไล่จับคนร้ายในตรอกจนขาหัก → นอนโรงพยาบาล แฟนมาเยี่ยม → กลับบ้านพร้อมเฝือก'),
      '2': ('วันหยุดที่ไม่มีความสุข', 'ย้ายขึ้นไปใช้ชีวิตในห้องนั่งเล่นชั้นสอง → นั่งดื่มกาแฟริมหน้าต่าง → รถขนของมาจอดบ้านตรงข้าม'),
      '3': ('เพื่อนบ้านคนใหม่', 'แอบจำกิจวัตรสามีภรรยาจากหน้าต่างเดิม → คืนวันศุกร์ทะเลาะกัน ไฟดับ'),
      '4': ('ถุงดำปริศนา', 'ตีสอง ลากถุงดำขึ้นรถ → เพื่อนตำรวจมาเช็ก → สามีเงยหน้ายิ้ม'),
      '5': ('คดีที่ไม่มีใครเชื่อ', 'ห้องนั่งเล่นชั้นสองกลายเป็นห้องสืบสวน → ข้อความตอนตีสอง → เงาทุบกระจก'),
      '6': ('แฟนสาวของผม', 'แฟนเดินข้ามถนนไปบ้านตรงข้าม → เงาสองคนบนผ้าม่าน ไฟดับ'),
      '7': ('ความจริงหลังประตู', 'รีบลงบันได → ข้ามถนนไปประตูที่เปิดแง้ม → เซอร์ไพรส์!'),
      '8': ('ผู้เฝ้ามอง', 'กล้องถอยออกจากงานเลี้ยง → ห้องมืดในบ้านหลังที่สาม')}
cards = []
cur = None; grp = []
def flush():
    if cur:
        t, beat = CH[cur]
        cards.append(f'<section class="ch"><h2><b>ฉาก {cur}</b> {t}</h2><p class="beat">{beat}</p><div class="grid">{"".join(grp)}</div></section>')
for sid, title, note, body in S:
    ch = sid[0]
    if ch != cur:
        flush(); cur = ch; grp = []
    grp.append(f'''<figure><div class="fr">{frame_svg(body)}<div class="sub" aria-hidden="true"></div></div>
<figcaption><b>{sid}</b> {html.escape(title.split(" · ",1)[-1])}<span>{html.escape(note)}</span></figcaption></figure>''')
flush()

page = f'''<title>บ้านตรงข้าม ฉากทั้งหมด</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: grid of 9:16 frames, 4 per row on desktop, 2 on phones. Dark purple page so the night scenes read correctly. */
:root {{ --bg:#141027; --card:#1f1a3a; --ink:#e4def4; --muted:#9a90bc; --line:#2e2756; --accent:#c9a8ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:20px; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }}
header p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.6; max-width:85ch; }}
label {{ font-size:13px; color:var(--muted); display:inline-flex; gap:6px; align-items:center; margin-top:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:18px; }}
.ch {{ display:grid; gap:10px; padding-top:6px; border-top:1px solid var(--line); }}
.ch h2 {{ font-size:17px; font-weight:500; margin:0; }} .ch h2 b {{ color:var(--accent); font-weight:500; margin-right:6px; }}
.beat {{ margin:0; color:var(--muted); font-size:13px; }}
.grid figure + figure {{ position:relative; }}
@media (min-width:700px) {{ .grid figure + figure::before {{ content:'→'; position:absolute; left:-15px; top:22%; color:var(--accent); font-size:16px; }} }}
figure {{ margin:0; display:grid; gap:8px; min-width:0; }}
.fr {{ position:relative; border-radius:6px; overflow:hidden; box-shadow:0 0 0 1px var(--line); }}
.fr svg {{ display:block; width:100%; height:auto; }}
.sub {{ position:absolute; left:0; right:0; top:60%; height:15%; border-block:1px dashed rgba(255,255,255,.85); background:rgba(255,255,255,.06); display:none; }}
body.guides .sub {{ display:block; }}
figcaption {{ font-size:13px; line-height:1.55; }}
figcaption b {{ color:var(--accent); font-weight:500; margin-right:4px; }}
figcaption span {{ display:block; color:var(--muted); font-size:12px; margin-top:2px; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&family=Inter:wght@700&display=swap">
{DEFS}
<div class="wrap">
<header><h1>บ้านตรงข้าม · ฉากทั้งหมด ({len(S)} ฉาก)</h1>
<p>เรียงตามเรื่อง ฉาก 1–8 · ฉากหลังอย่างเดียว ยังไม่ใส่ตัวละคร · โทนน้ำตาลผสมม่วง: วอลเปเปอร์ลายเส้น ผนังบุไม้ พื้นไม้ เฟอร์นิเจอร์ไม้ เงาออกม่วง แสงอุ่นเป็นวงจากโคมไฟ หน้าต่าง ไฟถนน · บ้านตรงข้ามเป็นบ้านไม้ทรงคอทเทจ ใช้แบบเดียวกันทุกฉาก · กลางคืนมีหมอกบาง ๆ และ low-key ให้ลึกลับ</p>
<label><input type="checkbox" id="g" onchange="document.body.classList.toggle('guides',this.checked)"> แสดงช่วงวางซับ (60–75% ของความสูง)</label></header>
{"".join(cards)}</div>'''

open('scenes.html', 'w', encoding='utf-8').write(page)
print('scenes:', len(S))
