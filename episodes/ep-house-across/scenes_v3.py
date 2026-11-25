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
    # stone path, mailbox, picket fence
    o.append(f'<polygon points="{pts((250+10*hs,hy+28*hs),(250+90*hs,hy+28*hs),(330,hy+40),(196,hy+40))}" fill="{"#b8a898" if day else "#4e4448"}"/>')
    fc = '#e8dccb' if day else '#8a7c74'
    o.append(f'<rect x="0" y="{hy+4}" width="{W}" height="4" fill="{fc}"/><rect x="0" y="{hy+18}" width="{W}" height="4" fill="{fc}"/>'
             + ''.join(f'<path d="M {xx},{hy+30} L {xx},{hy-6} L {xx+3},{hy-10} L {xx+6},{hy-6} L {xx+6},{hy+30} Z" fill="{fc}"/>' for xx in list(range(0, 190, 14)) + list(range(340, W, 14))))
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

# ======================= SCENES =======================
S = []

# ---- 1A flashback alley (one-point, warm faded, purple shadows) ----
o = []
vp = (280, 470)
o.append('<rect width="540" height="960" fill="#6e5450"/>')
o.append('<rect width="540" height="480" fill="#a08480"/>' + glow(280, 440, 200, '#ffd8b8', .6))
# buildings left/right receding
for side_ in (-1, 1):
    near_x = 0 if side_ < 0 else W
    far_x = 230 if side_ < 0 else 330
    o.append(f'<polygon points="{pts((near_x,0),(far_x,330),(far_x,520),(near_x,960))}" fill="{"#6a4a44" if side_<0 else "#553a3a"}"/>')
    for k in range(6):  # windows along the facade
        t0, t1 = k / 6 + .02, k / 6 + .1
        a0 = lerp((near_x, 0), (far_x, 330), t0); a1 = lerp((near_x, 0), (far_x, 330), t1)
        b0 = lerp((near_x, 960), (far_x, 520), t0); b1 = lerp((near_x, 960), (far_x, 520), t1)
        for v0, v1 in ((.12, .24), (.34, .46)):
            q = [lerp(a0, b0, v0), lerp(a1, b1, v0), lerp(a1, b1, v1), lerp(a0, b0, v1)]
            o.append(f'<polygon points="{pts(*q)}" fill="{"#f6c9a8" if (k+side_)%3 else "#3a2828"}" opacity=".85"/>')
o.append(f'<polygon points="{pts((230,520),(330,520),(540,960),(0,960))}" fill="#7a5e58"/>')
o.append(f'<polygon points="{pts((262,520),(298,520),(380,960),(160,960))}" fill="#9a7a74" opacity=".6"/>')  # wet sheen centre
o.append(f'<path d="M 120,0 L 220,330" stroke="#2a1c1c" stroke-width="2"/><path d="M 420,0 L 330,330" stroke="#2a1c1c" stroke-width="2"/>')
for (lx, ly, sc) in ((150, 600, 1.1), (395, 560, .8), (250, 500, .45)):
    o.append(f'<rect x="{lx-3*sc}" y="{ly-300*sc}" width="{6*sc}" height="{300*sc}" fill="#2e2020"/><path d="M {lx},{ly-300*sc} q {20*sc},-14 {40*sc},0" fill="none" stroke="#2e2020" stroke-width="{4*sc}"/>')
    o.append(f'<rect x="{lx+30*sc}" y="{ly-298*sc}" width="{20*sc}" height="{8*sc}" fill="{WARM}"/>' + glow(lx + 40 * sc, ly - 290 * sc, 120 * sc, WARM, .7) + pool(lx + 40 * sc, ly + 20 * sc, 150 * sc, 40 * sc, WARM, .5))
o.append(beam('170,320 210,320 300,800 40,800', 'beamW', .7))
o.append(cast('<path d="M 300,820 L 390,780 L 430,830 L 340,870 Z"/>'))
o.append('<g transform="translate(340,800) rotate(-24)"><rect x="-44" y="-28" width="88" height="56" rx="6" fill="#4e3a38"/><rect x="-44" y="-28" width="88" height="14" fill="#5e4644"/><ellipse cx="-44" cy="0" rx="10" ry="28" fill="#3e2e2e"/></g>')
o.append('<g fill="#e8d4d0">' + ''.join(f'<rect x="{x}" y="{y}" width="16" height="11" transform="rotate({r} {x} {y})"/>' for x, y, r in [(250, 860, 20), (290, 900, -30), (190, 880, 50), (420, 900, 10)]) + '</g>')
o.append(shade(280, 520, 520, '#3a2430', .55))
o.append(dust(11, (120, 300, 360, 820), 26, '#ffe8d4'))
o.append('<rect width="540" height="960" fill="#e8c4b0" opacity=".22" style="mix-blend-mode:soft-light"/>')
S.append(('1A', 'ฉาก 1 · ย้อนอดีต: ตรอกที่ไล่จับคนร้าย', 'ตรอกเปอร์สเปกทีฟจุดเดียว ไฟถนนสามดวงไล่ลึก พื้นเปียกสะท้อนแสง ถังขยะล้ม โทนอุ่นซีดแบบความทรงจำ เงาออกม่วง', ''.join(o)))

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

S.append(('1B', 'ฉาก 1–2 · ห้องนอนพระเอก ชั้นสอง (ยามบ่าย)', 'ห้องเปอร์สเปกทีฟจุดเดียว หน้าต่างใหญ่ผนังหลังมีเบาะนั่งริมหน้าต่าง เห็นบ้านตรงข้ามแบบเบลอ แดดบ่ายส่องเป็นแผ่นบนพื้น ผนังซ้ายมีประตูกับตู้เสื้อผ้า เตียง โคมหัวเตียง อาร์มแชร์ มุมห้องเงาม่วง', bedroom()))

S.append(('2', 'ฉาก 2 · มองจากหน้าต่าง: รถขนของมาจอดบ้านตรงข้าม', 'กรอบหน้าต่างพระเอกมืดเป็นฉากหน้ามีแสงขอบ บ้านตรงข้ามเห็นด้านข้างเป็นสามมิติ มีเสาไฟและสายไฟ รถขนของกับกล่องหน้าบ้าน',
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

S.append(('4', 'ฉาก 4 · ตีสอง ลากถุงดำขึ้นท้ายรถ', 'ไฟบ้านดับหมด เหลือไฟหน้าประตู ไฟถนนส่องเป็นวง รถเปิดท้ายรออยู่ข้างบ้าน',
          street('dark', moon=(110, 120), extra_front=(cast('<rect x="330" y="580" width="170" height="40"/>') +
                 '<g transform="translate(410,618)"><path d="M -74,0 L -70,-26 C -64,-36 -42,-38 -30,-38 L 24,-38 C 40,-38 52,-32 60,-24 L 74,-20 L 76,0 Z" fill="#4a3f7e"/>'
                 '<path d="M -56,-28 L -48,-36 L -6,-36 L -6,-26 Z M 0,-36 L 24,-36 C 34,-36 42,-32 48,-26 L 0,-26 Z" fill="#241c48"/>'
                 '<path d="M 60,-24 L 92,-62 L 102,-56 L 76,-20 Z" fill="#5a4f92"/><circle cx="-44" cy="2" r="12" fill="#1a1436"/><circle cx="46" cy="2" r="12" fill="#1a1436"/>'
                 '<rect x="66" y="-18" width="8" height="6" fill="#ff7a8a"/></g>'
                 + '<rect x="497" y="300" width="6" height="330" fill="#2a2150"/><rect x="470" y="296" width="34" height="8" fill="#2a2150"/><rect x="470" y="304" width="18" height="6" fill="#ffd8a8"/>'
                 + glow(479, 312, 130, WARM, .7) + pool(470, 620, 120, 30, WARM, .5) + beam('462,310 498,310 560,640 380,640', 'beamW', .55)
                 + dust(34, (390, 320, 540, 640), 14, '#ffe8d4'))) + window_fg(None)))

S.append(('5A', 'ฉาก 5 · ห้องนอนกลายเป็นห้องสืบสวน (กลางคืน)', 'ห้องเดิมตอนกลางคืน บอร์ดรูปโยงด้ายแดงบนผนังขวา โต๊ะใต้บอร์ดมีโคมส่องเป็นวงอุ่น กล้องบนขาตั้งหันออกหน้าต่าง กระดาษกระจายเต็มพื้น แสงจันทร์ฟ้าม่วงจากหน้าต่าง',
          bedroom(night=True, board=True)))

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

# ---- 5C silhouette pounding the upstairs window (close) ----
o = [night_sky((440, 120), 6, 900)]
o.append(f'<g transform="translate(300,1180) scale(3.2)">{house3d(0, 0, 1, "dark")}</g>')
o.append('<rect x="60" y="170" width="240" height="250" fill="url(#winLit)" opacity=".9"/>' + glow(180, 300, 220, WARM, .6))
o.append('<path d="M 130,420 C 126,350 142,300 172,288 C 162,268 166,244 184,240 C 202,238 212,256 204,278 C 230,290 244,330 250,420 Z" fill="#2a1f4a" opacity=".92" filter="url(#dof)"/>')
o.append('<path d="M 212,276 L 250,214 L 262,222 L 224,284 Z" fill="#2a1f4a" opacity=".92" filter="url(#dof)"/>')
o.append('<path d="M 250,212 L 274,190 M 250,212 L 282,222 M 250,212 L 264,246 M 250,212 L 232,186 M 262,200 L 290,196" stroke="#ffffff" stroke-width="1.6" opacity=".85"/>')
o.append(beam('60,420 300,420 360,960 0,960', 'beamW', .4))
o.append(shade(180, 300, 520, '#1a1240', .55))
o.append(dust(36, (60, 170, 300, 420), 12, '#ffe8d4'))
S.append(('5C', 'ฉาก 5 · เงาผู้หญิงทุบกระจกชั้นบน', 'ซูมเข้าหน้าต่างชั้นบนของบ้านตรงข้าม แสงอุ่นในห้องตัดกับผนังม่วงคราม เงาผู้หญิงชูแขนทุบกระจกจนร้าว เงานี้เป็นตัวแทนชั่วคราว', ''.join(o)))

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

# ---- 7C surprise party living room ----
R = Room((270, 450), 110, 250, 430, 580)
o = [R.shell(wall='#8a6260', wall_lt='#9a706a', wall_dk='#6a4a50', ceil='#4a3438', floor='#7e5440')]
o.append(walls_detail(R, wall_stripe='#7a5452'))
rug = [R.P('F', 1.45, .2), R.P('F', 1.45, .8), R.P('F', 2.6, .84), R.P('F', 2.6, .16)]
o.append(f'<polygon points="{pts(*rug)}" fill="#7a4a5a"/><polygon points="{pts(*[lerp(rug[0],rug[2],.07), lerp(rug[1],rug[3],.07), lerp(rug[2],rug[0],.07), lerp(rug[3],rug[1],.07)])}" fill="none" stroke="#d8b090" stroke-width="2.4"/>')
o.append(R.box(1.02, 1.3, .0, .14, .75, WOOD_LT, WOOD_DK, WOOD))                  # bookcase on the left wall
for k_ in range(4):
    sp_ = on_floor(R, 1.3, .03, .14 + k_ * .16); o.append(books(sp_[0] + 2, sp_[1], 1.1))
o.append(R.box(1.7, 2.0, .0, .2, .14, '#a06a5a', '#6a3a34', '#84504a'))           # armchair left
o.append(R.box(1.7, 1.78, .0, .2, .3, '#a06a5a', '#6a3a34', '#84504a', h0=.14))
o.append(R.box(1.6, 1.85, .8, 1.0, .14, '#a06a5a', '#6a3a34', '#84504a'))          # armchair right
o.append(R.box(1.6, 1.68, .8, 1.0, .3, '#a06a5a', '#6a3a34', '#84504a', h0=.14))
fl = on_floor(R, 1.25, .2)
o.append(f'<line x1="{fl[0]:.0f}" y1="{fl[1]:.0f}" x2="{fl[0]:.0f}" y2="{fl[1]-200:.0f}" stroke="#2a1a14" stroke-width="3"/><path d="M {fl[0]-22:.0f},{fl[1]-196:.0f} L {fl[0]+22:.0f},{fl[1]-196:.0f} L {fl[0]+14:.0f},{fl[1]-226:.0f} L {fl[0]-14:.0f},{fl[1]-226:.0f} Z" fill="#e8c8a0"/>' + glow(fl[0], fl[1] - 205, 70, WARM, .7))
pg = on_floor(R, 1.15, .7); o.append(plant(pg[0], pg[1], 1.4))
gf = on_floor(R, 2.05, .74)
o.append(f'<g transform="translate({gf[0]:.0f},{gf[1]:.0f})"><rect x="-30" y="-34" width="40" height="34" fill="#c06a7e"/><rect x="-12" y="-34" width="6" height="34" fill="#f2d6a8"/><rect x="6" y="-24" width="30" height="24" fill="#6a7ab0"/><rect x="18" y="-24" width="6" height="24" fill="#f2d6a8"/><rect x="-18" y="-56" width="26" height="22" fill="#e8c46a"/><rect x="-7" y="-56" width="5" height="22" fill="#c06a7e"/></g>')

# back wall window (night) + curtains
o.append('<rect x="300" y="290" width="110" height="160" fill="#2e2560"/>' + stars(3, 10, 0).replace('cy="', 'cy="3') )
o.append('<path d="M 294,284 L 416,284 L 416,456 L 294,456 Z M 300,290 L 410,290 L 410,450 L 300,450 Z" fill="#e6dcf6" fill-rule="evenodd"/><rect x="352" y="290" width="6" height="160" fill="#e6dcf6"/>')
o.append('<path d="M 280,270 L 304,270 C 300,340 306,420 298,470 L 280,470 Z" fill="#e6a8bc"/><path d="M 430,270 L 406,270 C 410,340 404,420 412,470 L 430,470 Z" fill="#e6a8bc"/>')
# banner across the back wall
cols = ['#ff9fb4', '#b9a2ff', '#ffe08a', '#9fe0c8']
o.append('<path d="M 112,262 Q 270,330 428,262" fill="none" stroke="#e6dcf6" stroke-width="2"/>')
for i, ch in enumerate('SURPRISE'):
    t = (i + .5) / 8; x = 112 + 316 * t; y = 262 + 68 * 4 * t * (1 - t) * .5 + 4
    o.append(f'<path d="M {x-17},{y} L {x+17},{y} L {x},{y+36} Z" fill="{cols[i%4]}"/><text x="{x}" y="{y+17}" font-family="Inter, sans-serif" font-weight="700" font-size="12" fill="#4a3a78" text-anchor="middle">{ch}</text>')
# string lights along the ceiling edges
for face in ('L', 'R'):
    for k in range(10):
        p = R.P(face, 1 + k * .25, .04)
        o.append(f'<circle cx="{p[0]:.0f}" cy="{p[1]:.0f}" r="{2+k*.4:.1f}" fill="#fff0c8"/>' + (glow(p[0], p[1], 14 + k * 2, WARM, .6) if k % 2 == 0 else ''))
# frames on left wall, sideboard on right
o.append(R.quad('L', 1.2, 1.45, .25, .45, WOOD_DK) + R.quad('L', 1.22, 1.43, .28, .42, '#c09ad6'))
o.append(R.quad('L', 1.6, 1.8, .3, .5, WOOD_DK) + R.quad('L', 1.62, 1.78, .33, .47, '#9fb8e0'))
o.append(R.box(1.1, 1.6, .82, 1.0, .3, WOOD_LT, WOOD_DK, WOOD))
# sofa (back), cake table (centre), balloons
o.append(R.box(1.04, 1.12, .12, .6, .24, '#b8a0e0', '#6a5298', '#7a62a8'))
o.append(R.box(1.12, 1.32, .12, .6, .11, '#c8b2ea', '#7a62a8', '#8e76bc'))
o.append(R.box(1.6, 1.85, .38, .64, .13, '#f6eef8', '#cdbde2', '#e6daf0'))
cp = R.P('F', 1.72, .51); ch_ = (R.y1 - R.y0) * 1.72 * .13
o.append(f'<g transform="translate({cp[0]:.0f},{cp[1]-ch_:.0f})"><rect x="-40" y="-40" width="80" height="40" rx="6" fill="#fff8fb"/><rect x="-40" y="-28" width="80" height="9" fill="#f2a6bc"/><rect x="-28" y="-64" width="56" height="26" rx="5" fill="#fffafc"/>'
         + ''.join(f'<rect x="{-20+i*13}" y="-80" width="4" height="16" fill="#b9a2ff"/><ellipse cx="{-18+i*13}" cy="-84" rx="3" ry="5" fill="#ffe0a8"/>' for i in range(4)) + '</g>')
o.append(glow(cp[0], cp[1] - ch_ - 80, 90, WARM, .8))
for (x, y, c) in [(70, 360, '#ff9fb4'), (110, 320, '#b9a2ff'), (150, 380, '#ffe08a'), (470, 600, '#9fe0c8'), (505, 560, '#ff9fb4'), (440, 300, '#b9a2ff')]:
    o.append(f'<path d="M {x},{y+30} C {x+6},{y+80} {x-6},{y+130} {x+4},{y+190}" fill="none" stroke="#e6dcf6" stroke-width="1.2" opacity=".7"/><ellipse cx="{x}" cy="{y}" rx="24" ry="30" fill="{c}"/><ellipse cx="{x-8}" cy="{y-10}" rx="6" ry="9" fill="#ffffff" opacity=".55"/>')
r = random.Random(12)
o.append(''.join(f'<rect x="{r.uniform(40,500):.0f}" y="{r.uniform(200,760):.0f}" width="6" height="10" fill="{r.choice(cols)}" transform="rotate({r.uniform(-60,60):.0f} 270 450)"/>' for _ in range(40)))
o.append(pool(270, 760, 260, 90, WARM, .45))
o.append(shade(270, 520, 560, '#3a2a72', .45))
o.append(dust(40, (60, 250, 480, 760), 20))
S.append(('7C', 'ฉาก 7 · เซอร์ไพรส์! ห้องนั่งเล่นเปิดไฟ', 'ห้องเปอร์สเปกทีฟจุดเดียว ป้าย SURPRISE ไฟประดับตามขอบเพดาน ลูกโป่ง โซฟาด้านหลัง เค้กเทียนกลางห้อง กระดาษสีลอย สว่างและอุ่นที่สุดในเรื่อง แต่มุมห้องยังเงาม่วง', ''.join(o)))

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
cards = []
for sid, title, note, body in S:
    cards.append(f'''<figure><div class="fr">{frame_svg(body)}<div class="sub" aria-hidden="true"></div></div>
<figcaption><b>{sid}</b> {html.escape(title)}<span>{html.escape(note)}</span></figcaption></figure>''')

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
<p>ฉากหลังอย่างเดียว ยังไม่ใส่ตัวละคร · โทนน้ำตาลผสมม่วง: วอลเปเปอร์ลายเส้น ผนังบุไม้ พื้นไม้ เฟอร์นิเจอร์ไม้ เงาออกม่วง แสงอุ่นเป็นวงจากโคมไฟ หน้าต่าง ไฟถนน · บ้านตรงข้ามเป็นบ้านไม้ทรงคอทเทจ ใช้แบบเดียวกันทุกฉาก · กลางคืนมีหมอกบาง ๆ และ low-key ให้ลึกลับ</p>
<label><input type="checkbox" id="g" onchange="document.body.classList.toggle('guides',this.checked)"> แสดงช่วงวางซับ (60–75% ของความสูง)</label></header>
<div class="grid">{"".join(cards)}</div></div>'''

open('scenes.html', 'w', encoding='utf-8').write(page)
print('scenes:', len(S))
