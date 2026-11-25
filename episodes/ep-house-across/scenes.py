#!/usr/bin/env python3
"""บ้านตรงข้าม: ฉากหลังทุกฉาก v2 (มีมิติ แสงเงาโทนม่วง อารมณ์สืบสวน)
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

# ---------------- palette: purple ambient, warm practical lights ----------------
SKY_N = ('#1e1940', '#3b2f6e', '#6a4f96')   # night sky top -> horizon
WALL = '#6f5c9c'; WALL_LT = '#8a74b4'; WALL_DK = '#4a3b78'
CEIL = '#3e3170'; FLOOR = '#6b4a72'; FLOOR_LT = '#86607e'; FLOOR_LINE = '#55395e'
WOOD = '#7a4f62'; WOOD_LT = '#9a6878'; WOOD_DK = '#553648'
FAB = '#b86e8c'; FAB_LT = '#d891a8'; TEAL = '#5f8fa8'
WARM = '#ffcf9e'; WARM2 = '#ffb27a'; COOL = '#a9b6ff'; MOON = '#e6e4ff'
PAPER = '#efe6f0'; RED = '#c2404f'; INK = '#2a2148'

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

def frame_svg(content):
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{content}{TEX}</svg>'

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

# ---------------- the house across (3D: front + right side, same design everywhere) ----------------
def house3d(x, y, s=1, mode='night'):
    """mode: day | morning | night | fight | dark | shadow | party"""
    day = mode in ('day', 'morning')
    lit_lr = mode in ('night', 'fight', 'shadow', 'party')
    lit_up = mode in ('night', 'party')
    front = '#b9a6d8' if day else '#5f5196'
    front_lt = '#cdbde6' if day else '#7262aa'
    side = '#8e7cbc' if day else '#43397a'
    roof = '#6d5a9a' if day else '#352a62'; roof_sd = '#55457e' if day else '#261e4c'
    trim = '#efe6f6' if day else '#a99cd2'
    win_lr = 'url(#winLit)' if lit_lr else ('#8e86c8' if day else 'url(#winDark)')
    win_up = 'url(#winLit)' if lit_up else ('#8e86c8' if day else 'url(#winDark)')
    dx, dt, db = 92, 14, -18   # side face depth, top drop, bottom rise
    o = []
    # side face
    o.append(f'<polygon points="{pts((130,-230),(130+dx,-230+dt),(130+dx,db),(130,0))}" fill="{side}"/>')
    o.append(f'<polygon points="{pts((150,-170),(196,-165),(196,-110),(150,-112))}" fill="{win_up if lit_up else ("#7a72b0" if day else "#2a2356")}"/>')
    # front face
    o.append(f'<rect x="-130" y="-230" width="260" height="230" fill="{front}"/>')
    o.append(f'<rect x="-130" y="-230" width="70" height="230" fill="{front_lt}" opacity=".6"/>')
    # siding lines
    o.append(''.join(f'<line x1="-130" y1="{yy}" x2="130" y2="{yy}" stroke="{side}" stroke-width="1" opacity=".35"/>' for yy in range(-220, 0, 14)))
    # roof: front gable + side plane receding
    o.append(f'<polygon points="{pts((-146,-224),(0,-330),(146,-224))}" fill="{roof}"/>')
    o.append(f'<polygon points="{pts((0,-330),(dx,-330+dt*.8),(146+dx,-224+dt),(146,-224))}" fill="{roof_sd}"/>')
    o.append(f'<polygon points="{pts((-118,-230),(0,-312),(118,-230))}" fill="{front}"/>')  # gable wall
    o.append(f'<polygon points="{pts((-150,-226),(0,-334),(150,-226),(140,-222),(0,-322),(-140,-222))}" fill="{trim}"/>')
    # shingles
    o.append(''.join(f'<line x1="{146+dx*t:.0f}" y1="{-224+dt*t:.0f}" x2="{dx*t:.0f}" y2="{-330+dt*.8*t:.0f}" stroke="{roof}" stroke-width="1" opacity=".5"/>' for t in (.2, .4, .6, .8)))
    # gable round window
    o.append(f'<circle cx="0" cy="-268" r="17" fill="{trim}"/><circle cx="0" cy="-268" r="12" fill="{win_up}"/>')
    if lit_up: o.append(glow(0, -268, 40, WARM, .6))
    # upstairs windows
    for wx in (-100, 34):
        o.append(f'<rect x="{wx}" y="-206" width="66" height="70" fill="{trim}"/><rect x="{wx+5}" y="-201" width="56" height="60" fill="{win_up}"/>')
        o.append(f'<path d="M {wx+33},-201 L {wx+33},-141 M {wx+5},-171 L {wx+61},-171" stroke="{trim}" stroke-width="2.6"/>')
        o.append(f'<rect x="{wx-4}" y="-138" width="74" height="6" fill="{trim}"/>')
        if lit_up: o.append(glow(wx + 33, -170, 50, WARM, .5))
    # porch roof + columns (depth)
    o.append(f'<polygon points="{pts((-138,-98),(138,-98),(150,-84),(-150,-84))}" fill="{roof}"/>')
    o.append(f'<rect x="-150" y="-86" width="300" height="6" fill="{trim}"/>')
    for cx in (-136, -20, 132):
        o.append(f'<rect x="{cx-5}" y="-80" width="10" height="80" fill="{trim}"/><rect x="{cx+2}" y="-80" width="3" height="80" fill="{side}" opacity=".6"/>')
    # living room window (left, ground floor)
    o.append(f'<rect x="-122" y="-72" width="94" height="58" fill="{trim}"/><rect x="-117" y="-67" width="84" height="48" fill="{win_lr}"/>')
    cur = '#f2c3c8' if lit_lr else ('#c9a9d6' if day else '#3c3270')
    if mode == 'shadow':
        o.append(f'<rect x="-117" y="-67" width="84" height="48" fill="{cur}" opacity=".88"/>')
        o.append(''.join(f'<line x1="{-112+i*10}" y1="-67" x2="{-112+i*10}" y2="-19" stroke="#e2a7b0" stroke-width="1.6"/>' for i in range(8)))
    elif mode == 'dark':
        o.append(f'<rect x="-117" y="-67" width="84" height="48" fill="{cur}"/>')
    elif mode == 'fight':
        o.append(f'<path d="M -117,-67 L -96,-67 C -97,-50 -98,-34 -101,-19 L -117,-19 Z" fill="{cur}"/><path d="M -33,-67 L -60,-67 C -58,-50 -57,-34 -54,-19 L -33,-19 Z" fill="{cur}"/>')
    else:
        o.append(f'<path d="M -117,-67 L -106,-67 C -107,-50 -107,-34 -110,-19 L -117,-19 Z" fill="{cur}"/><path d="M -33,-67 L -44,-67 C -43,-50 -43,-34 -40,-19 L -33,-19 Z" fill="{cur}"/>')
    if mode == 'party':
        o.append(''.join(f'<circle cx="{-104+i*16}" cy="{-56+(i%2)*8}" r="5.5" fill="{c}"/>' for i, c in enumerate(['#ff9fb4', '#b9a2ff', '#ffe08a', '#9fe0c8', '#ff9fb4'])))
    o.append(f'<path d="M -75,-67 L -75,-19" stroke="{trim}" stroke-width="2.6"/>')
    if lit_lr: o.append(glow(-75, -42, 80, WARM, .55))
    # front door
    door = '#5a3f62' if day else '#2e2348'
    o.append(f'<rect x="20" y="-74" width="46" height="74" fill="{trim}"/><rect x="25" y="-69" width="36" height="69" fill="{door}"/>')
    o.append(f'<rect x="29" y="-64" width="28" height="22" fill="none" stroke="{trim}" stroke-width="1.6" opacity=".5"/><circle cx="56" cy="-34" r="2.2" fill="#e6e0f0"/>')
    if not day:
        o.append(f'<rect x="72" y="-66" width="8" height="12" rx="2" fill="{WARM}"/>' + glow(76, -60, 46, WARM, .8) + pool(50, 6, 80, 20, WARM, .45))
    # porch rail + steps
    o.append(f'<path d="M -150,-30 L 10,-30 M 76,-30 L 150,-30" stroke="{trim}" stroke-width="3"/>')
    o.append(''.join(f'<rect x="{xx}" y="-30" width="3" height="30" fill="{trim}"/>' for xx in list(range(-146, 10, 12)) + list(range(80, 150, 12))))
    o.append(f'<rect x="12" y="0" width="62" height="8" fill="{trim}"/><rect x="6" y="8" width="74" height="8" fill="{side}"/><rect x="0" y="16" width="86" height="8" fill="{trim}" opacity=".8"/>')
    # bushes with roses
    for bx in (-150, -90, 110):
        o.append(f'<ellipse cx="{bx+24}" cy="2" rx="34" ry="18" fill="{"#5d7f86" if day else "#2c3a5e"}"/><ellipse cx="{bx+12}" cy="-6" rx="18" ry="12" fill="{"#7aa0a0" if day else "#3b4a72"}"/>')
        o.append(''.join(f'<circle cx="{bx+6+i*12}" cy="{-4+(i%2)*6}" r="3" fill="{"#e79ab0" if day else "#a8607e"}"/>' for i in range(4)))
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(o)}</g>'

def side_house(x, y, s=1, flip=False, lit=True):
    """neighbour houses, darker, for depth"""
    t = f'translate({x},{y}) scale({-s if flip else s},{s})'
    w = 'url(#winLit)' if lit else 'url(#winDark)'
    return (f'<g transform="{t}"><polygon points="{pts((-90,-160),(0,-240),(90,-160))}" fill="#2b2256"/><rect x="-80" y="-160" width="160" height="160" fill="#3b3070"/>'
            f'<rect x="-60" y="-130" width="34" height="40" fill="{w}"/><rect x="14" y="-130" width="34" height="40" fill="url(#winDark)"/><rect x="-24" y="-60" width="30" height="60" fill="#241c48"/></g>')

def street(mode='night', moon=(420, 140), extra_back='', extra_front='', with_house=True, seed=5, hy=600, hs=1.15):
    """exterior: house across seen from the hero's side, slightly from above"""
    day = mode in ('day', 'morning')
    o = []
    if day:
        i = uid('sk')
        top, mid, bot = (('#6f62b4', '#a58fd0', '#e7c0d4') if mode == 'day' else ('#7f73c2', '#b9a0d8', '#f4cdd2'))
        o.append(f'<defs><linearGradient id="{i}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".6" stop-color="{mid}"/><stop offset="1" stop-color="{bot}"/></linearGradient></defs><rect width="{W}" height="{H}" fill="url(#{i})"/>')
        o.append(glow(460 if mode == 'day' else 80, 140, 220, '#fff0d8', .6))
        r = random.Random(seed)
        for _ in range(4):
            cx = r.uniform(-40, W); cy = r.uniform(60, 300); w = r.uniform(160, 280)
            o.append(f'<path d="M {cx},{cy} q {w*.2},-26 {w*.45},-8 q {w*.25},-24 {w*.55},6 q -{w*.5},18 -{w},2 z" fill="#f2dcef" opacity=".55"/>')
    else:
        o.append(night_sky(moon, seed, hy - 60))
    # distant skyline + neighbours for depth
    r = random.Random(seed + 3); x = -10
    col = '#8a78bd' if day else '#2e2560'
    while x < W:
        w = r.randint(28, 50); h = r.randint(60, 150)
        o.append(f'<rect x="{x}" y="{hy-170-h}" width="{w}" height="{h+60}" fill="{col}" filter="url(#dof2)"/>')
        if not day:
            o.append(''.join(f'<rect x="{x+4+r.randint(0,w-10)}" y="{hy-160-h+r.randint(0,h)}" width="2.4" height="3" fill="{WARM}" opacity=".7"/>' for _ in range(w // 6)))
        x += w + 2
    o.append(f'<g filter="url(#dof)">{tree_dark(40, hy-120, 1.3, "#5a6a9a" if day else "#241d4c")}{tree_dark(520, hy-130, 1.2, "#5a6a9a" if day else "#241d4c")}</g>')
    o.append(f'<g filter="url(#dof)" opacity=".95">{side_house(-40, hy-40, .9, lit=not day)}{side_house(600, hy-40, .9, True, lit=not day)}</g>')
    o.append(extra_back)
    # lawn, sidewalk, road (slight high angle)
    o.append(f'<rect x="0" y="{hy-60}" width="{W}" height="80" fill="{"#7d8fb0" if day else "#2a2a5a"}"/>')
    if with_house:
        o.append(house3d(250, hy, hs, mode))
    o.append(f'<polygon points="{pts((0,hy+14),(W,hy+14),(W,hy+40),(0,hy+40))}" fill="{"#c9bde0" if day else "#5a4f92"}"/>')
    o.append(f'<rect x="0" y="{hy+40}" width="{W}" height="{H-hy-40}" fill="{"#8e80b8" if day else "#3a3070"}"/>')
    o.append(''.join(f'<rect x="{xx}" y="{hy+150}" width="52" height="6" fill="{"#e8e0f4" if day else "#8a7fc0"}" opacity=".7"/>' for xx in range(0, W, 96)))
    o.append(pole_lines([90, 470], hy - 360, hy + 30))
    o.append(extra_front)
    return ''.join(o)

def window_fg(lit_inside=WARM, night=True, sill=True):
    """the hero's window as a dark, back-lit foreground frame with rim light (gives depth)"""
    fr = '#2a2050' if night else '#4a3c7c'; rim = '#9d8ee0' if night else '#e8dcff'
    o = [f'<path d="M 0,0 L {W},0 L {W},{H} L 0,{H} Z M 52,110 L 488,110 L 488,640 L 52,640 Z" fill="{fr}" fill-rule="evenodd"/>']
    o.append(f'<rect x="262" y="110" width="16" height="530" fill="{fr}"/><rect x="52" y="368" width="436" height="12" fill="{fr}"/>')
    o.append(f'<path d="M 52,110 L 52,640 M 278,110 L 278,640 M 52,380 L 488,380" stroke="{rim}" stroke-width="2" opacity=".7"/>')
    # curtains, dark with soft light edge
    o.append(f'<path d="M 0,40 L 74,40 C 86,240 64,440 96,720 L 0,720 Z" fill="#3b2c66"/><path d="M 74,40 C 86,240 64,440 96,720 L 88,720 C 58,440 78,240 66,40 Z" fill="{rim}" opacity=".5"/>')
    o.append(f'<path d="M {W},40 L 466,40 C 454,240 476,440 444,720 L {W},720 Z" fill="#33275e"/><path d="M 466,40 C 454,240 476,440 444,720 L 452,720 C 482,440 462,240 474,40 Z" fill="{rim}" opacity=".45"/>')
    o.append(f'<rect x="0" y="30" width="{W}" height="12" rx="6" fill="#4a3c7c"/>')
    # sill + desk with props, catching light from the window
    o.append(f'<polygon points="{pts((20,640),(520,640),(540,676),(0,676))}" fill="#5a4a8c"/><polygon points="{pts((20,640),(520,640),(516,646),(24,646))}" fill="{rim}" opacity=".6"/>')
    o.append(f'<rect x="0" y="676" width="{W}" height="284" fill="#2a2050"/>')
    if sill:
        o.append(cast('<rect x="96" y="596" width="48" height="44"/>', 10, 6, .5))
        o.append(f'<path d="M 98,606 L 142,606 L 136,640 L 104,640 Z" fill="#6a5698"/><ellipse cx="108" cy="594" rx="13" ry="20" fill="#3f6a74" transform="rotate(-20 108 594)"/><ellipse cx="128" cy="588" rx="11" ry="22" fill="#4f7e86" transform="rotate(18 128 588)"/>')
        o.append(f'<rect x="384" y="608" width="28" height="32" rx="4" fill="#cfc4ea"/><path d="M 412,616 C 422,616 422,630 412,630" fill="none" stroke="#cfc4ea" stroke-width="4"/>')
        o.append(f'<path d="M 392,600 C 388,590 398,586 394,576 M 404,600 C 400,590 410,586 406,576" fill="none" stroke="#ffffff" stroke-width="1.4" opacity=".5"/>')
        o.append(f'<rect x="246" y="628" width="86" height="10" fill="#8a6aa8" transform="rotate(-3 290 632)"/><rect x="252" y="620" width="78" height="9" fill="{FAB}" transform="rotate(2 290 624)"/>')
        o.append(f'<path d="M 410,740 L 432,690 L 486,690 L 466,740 Z" fill="#4a3c7c"/>' + (glow(458, 712, 110, lit_inside, .7) if lit_inside else ''))
        o.append(f'<rect x="60" y="716" width="130" height="24" rx="3" fill="#3b2f68"/><rect x="64" y="720" width="122" height="16" fill="#4c3e80"/>')
    return ''.join(o)

# ======================= SCENES =======================
S = []

# ---- 1A flashback alley (one-point, warm faded, purple shadows) ----
o = []
vp = (280, 470)
o.append('<rect width="540" height="960" fill="#7a6aa0"/>')
o.append('<rect width="540" height="480" fill="#9c88b6"/>' + glow(280, 440, 200, '#ffd8b8', .6))
# buildings left/right receding
for side_ in (-1, 1):
    near_x = 0 if side_ < 0 else W
    far_x = 230 if side_ < 0 else 330
    o.append(f'<polygon points="{pts((near_x,0),(far_x,330),(far_x,520),(near_x,960))}" fill="{"#6a5490" if side_<0 else "#574480"}"/>')
    for k in range(6):  # windows along the facade
        t0, t1 = k / 6 + .02, k / 6 + .1
        a0 = lerp((near_x, 0), (far_x, 330), t0); a1 = lerp((near_x, 0), (far_x, 330), t1)
        b0 = lerp((near_x, 960), (far_x, 520), t0); b1 = lerp((near_x, 960), (far_x, 520), t1)
        for v0, v1 in ((.12, .24), (.34, .46)):
            q = [lerp(a0, b0, v0), lerp(a1, b1, v0), lerp(a1, b1, v1), lerp(a0, b0, v1)]
            o.append(f'<polygon points="{pts(*q)}" fill="{"#f6c9a8" if (k+side_)%3 else "#4a3a70"}" opacity=".85"/>')
o.append(f'<polygon points="{pts((230,520),(330,520),(540,960),(0,960))}" fill="#8a6f8e"/>')
o.append(f'<polygon points="{pts((262,520),(298,520),(380,960),(160,960))}" fill="#9a7c98" opacity=".6"/>')  # wet sheen centre
o.append(f'<path d="M 120,0 L 220,330" stroke="#2e2450" stroke-width="2"/><path d="M 420,0 L 330,330" stroke="#2e2450" stroke-width="2"/>')
for (lx, ly, sc) in ((150, 600, 1.1), (395, 560, .8), (250, 500, .45)):
    o.append(f'<rect x="{lx-3*sc}" y="{ly-300*sc}" width="{6*sc}" height="{300*sc}" fill="#3a2c5c"/><path d="M {lx},{ly-300*sc} q {20*sc},-14 {40*sc},0" fill="none" stroke="#3a2c5c" stroke-width="{4*sc}"/>')
    o.append(f'<rect x="{lx+30*sc}" y="{ly-298*sc}" width="{20*sc}" height="{8*sc}" fill="{WARM}"/>' + glow(lx + 40 * sc, ly - 290 * sc, 120 * sc, WARM, .7) + pool(lx + 40 * sc, ly + 20 * sc, 150 * sc, 40 * sc, WARM, .5))
o.append(beam('170,320 210,320 300,800 40,800', 'beamW', .7))
o.append(cast('<path d="M 300,820 L 390,780 L 430,830 L 340,870 Z"/>'))
o.append('<g transform="translate(340,800) rotate(-24)"><rect x="-44" y="-28" width="88" height="56" rx="6" fill="#5a4a7e"/><rect x="-44" y="-28" width="88" height="14" fill="#6c5a92"/><ellipse cx="-44" cy="0" rx="10" ry="28" fill="#463a68"/></g>')
o.append('<g fill="#e8d4d0">' + ''.join(f'<rect x="{x}" y="{y}" width="16" height="11" transform="rotate({r} {x} {y})"/>' for x, y, r in [(250, 860, 20), (290, 900, -30), (190, 880, 50), (420, 900, 10)]) + '</g>')
o.append(shade(280, 520, 520, '#3a2a62', .55))
o.append(dust(11, (120, 300, 360, 820), 26, '#ffe8d4'))
o.append('<rect width="540" height="960" fill="#e8c4b0" opacity=".22" style="mix-blend-mode:soft-light"/>')
S.append(('1A', 'ฉาก 1 · ย้อนอดีต: ตรอกที่ไล่จับคนร้าย', 'ตรอกเปอร์สเปกทีฟจุดเดียว ไฟถนนสามดวงไล่ลึก พื้นเปียกสะท้อนแสง ถังขยะล้ม โทนอุ่นซีดแบบความทรงจำ เงาออกม่วง', ''.join(o)))

# ---- 1B hero bedroom (late afternoon: purple interior, warm sun patch) ----
def bedroom(night=False, board=False):
    R = Room((300, 430), 150, 230, 440, 560)
    o = [R.shell(wall='#7a66a8' if not night else '#4f4184', wall_lt='#8e78b8' if not night else '#5d4d92',
                 wall_dk='#5a4888' if not night else '#3a2f6a', ceil='#4a3c7c' if not night else '#2c2358',
                 floor='#7a5674' if not night else '#4e3a62')]
    # back wall: big window with the house across outside
    wx0, wy0, wx1, wy1 = 250, 270, 420, 470
    view = street('night' if night else 'day', (130, 120), hy=600, hs=1.1)
    cid = uid('cw')
    o.append(f'<clipPath id="{cid}"><rect x="{wx0}" y="{wy0}" width="{wx1-wx0}" height="{wy1-wy0}"/></clipPath>')
    o.append(f'<g clip-path="url(#{cid})"><g filter="url(#dof)" transform="translate({wx0},{wy0}) scale(.32) translate(-20,-160)">{view}</g></g>')
    o.append(f'<path d="M {wx0-8},{wy0-8} L {wx1+8},{wy0-8} L {wx1+8},{wy1+8} L {wx0-8},{wy1+8} Z M {wx0},{wy0} L {wx1},{wy0} L {wx1},{wy1} L {wx0},{wy1} Z" fill="#d9cdee" fill-rule="evenodd"/>')
    o.append(f'<rect x="{(wx0+wx1)/2-3}" y="{wy0}" width="6" height="{wy1-wy0}" fill="#d9cdee"/><rect x="{wx0-14}" y="{wy1+6}" width="{wx1-wx0+28}" height="10" fill="#cbbde6"/>')
    # window seat cushions
    o.append(f'<rect x="{wx0}" y="{wy1+16}" width="{wx1-wx0}" height="44" fill="#5a4888"/><rect x="{wx0+10}" y="{wy1+4}" width="56" height="26" rx="8" fill="{FAB}"/><rect x="{wx0+90}" y="{wy1+6}" width="50" height="24" rx="8" fill="#8f7cc8"/>')
    # curtains on back wall
    o.append(f'<path d="M {wx0-30},{wy0-24} L {wx0+10},{wy0-24} C {wx0+6},{wy0+80} {wx0+12},{wy0+160} {wx0},{wy1+60} L {wx0-34},{wy1+60} Z" fill="#c4a8dc" opacity=".8"/>')
    o.append(f'<path d="M {wx1+30},{wy0-24} L {wx1-10},{wy0-24} C {wx1-6},{wy0+80} {wx1-12},{wy0+160} {wx1},{wy1+60} L {wx1+34},{wy1+60} Z" fill="#b89cd2" opacity=".8"/>')
    # left wall: door (ajar) + wardrobe
    o.append(R.quad('L', 1.05, 1.5, .18, 1, WOOD_DK) + R.quad('L', 1.09, 1.46, .23, 1, WOOD))
    o.append(R.quad('L', 1.7, 2.6, .05, 1, '#6a5090') + R.quad('L', 1.72, 2.15, .08, .98, '#7a60a0') + R.quad('L', 2.17, 2.58, .08, .98, '#7a60a0'))
    # right wall: frames or cork board
    if board:
        o.append(R.quad('R', 1.15, 1.9, .14, .62, WOOD_DK) + R.quad('R', 1.18, 1.86, .17, .59, '#a77a6c'))
        r = random.Random(4); pins = []
        for i in range(7):
            s0 = 1.22 + r.uniform(0, .5); a0 = .2 + r.uniform(0, .3)
            o.append(R.quad('R', s0, s0 + .1, a0, a0 + .09, PAPER) + R.quad('R', s0 + .01, s0 + .09, a0 + .01, a0 + .06, '#6c5b98'))
            pins.append(R.P('R', s0 + .05, a0 + .005))
        o.append(f'<polyline points="{pts(*pins)}" fill="none" stroke="{RED}" stroke-width="1.6"/>' + ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="3" fill="#ffd34a"/>' for x, y in pins))
    else:
        o.append(R.quad('R', 1.2, 1.5, .2, .42, WOOD_DK) + R.quad('R', 1.23, 1.47, .23, .39, '#8c78c0'))
        o.append(R.quad('R', 1.6, 1.85, .26, .44, WOOD_DK) + R.quad('R', 1.62, 1.83, .29, .41, '#a088cc'))
    # back-wall shelf-free (no bookshelf): poster + clock
    o.append(f'<rect x="168" y="270" width="62" height="86" fill="{WOOD_DK}"/><rect x="172" y="274" width="54" height="78" fill="#5f7fb0"/><circle cx="199" cy="300" r="14" fill="#ffd8a8" opacity=".8"/>')
    o.append(f'<circle cx="199" cy="400" r="16" fill="#e8def6"/><circle cx="199" cy="400" r="13" fill="#4a3c7c"/><path d="M 199,400 L 199,390 M 199,400 L 206,404" stroke="#e8def6" stroke-width="2"/>')
    # bed (left), bedside table, lamp
    o.append(R.box(1.1, 1.16, .0, .4, .3, WOOD_LT, WOOD_DK, WOOD))  # headboard
    o.append(R.box(1.16, 1.9, .0, .4, .1, WOOD_LT, WOOD_DK, WOOD))  # bed frame
    o.append(R.box(1.16, 1.9, .0, .4, .17, '#e6dcf4', '#8a72b8', '#9c86c8', h0=.1))  # mattress + blanket
    o.append(R.box(1.18, 1.32, .04, .36, .21, '#f6f0fc', '#d6cae8', '#e2d8f0', h0=.17))  # pillow
    o.append(R.box(1.1, 1.26, .45, .58, .15, WOOD_LT, WOOD_DK, WOOD))  # bedside table
    lp = R.P('F', 1.18, .51); o.append(lamp_desk(lp[0], lp[1] - (R.y1 - R.y0) * 1.18 * .15, .7, on=True))
    # rug + armchair (right, near)
    rug = [R.P('F', 1.6, .3), R.P('F', 1.6, .8), R.P('F', 2.5, .8), R.P('F', 2.5, .3)]
    o.append(f'<polygon points="{pts(*rug)}" fill="#8e6aa8" opacity=".8"/>')
    o.append(R.box(2.1, 2.5, .76, 1.0, .26, '#4f6f90', '#2e4560', '#3a5574', h0=.0))  # armchair back
    o.append(R.box(2.5, 2.85, .76, 1.0, .12, '#5f82a6', '#36506e', '#45607e'))  # armchair seat
    if board:
        # desk with lamp under the board, tripod camera at window, papers on floor
        o.append(R.box(1.15, 1.4, .68, 1.0, .2, WOOD_LT, WOOD_DK, WOOD))
        dp = R.P('F', 1.28, .82); o.append(lamp_desk(dp[0] - 10, dp[1] - (R.y1 - R.y0) * 1.28 * .2, .8, True))
        tp = R.P('F', 1.3, .5)
        o.append(f'<g transform="translate({tp[0]:.0f},{tp[1]-160:.0f})"><path d="M 0,40 L -26,160 M 0,40 L 26,160 M 0,40 L 0,164" stroke="#2a2148" stroke-width="3"/><rect x="-20" y="16" width="32" height="24" rx="3" fill="#2a2148"/><rect x="10" y="20" width="40" height="15" rx="3" fill="#3a2f62"/><circle cx="52" cy="27" r="8" fill="#1d1738"/></g>')
        r = random.Random(9)
        for _ in range(9):
            s = r.uniform(1.6, 3.4); u = r.uniform(.1, .9); p = R.P('F', s, u); a = r.uniform(-30, 30)
            o.append(f'<rect x="{p[0]:.0f}" y="{p[1]:.0f}" width="{14*s:.0f}" height="{9*s:.0f}" fill="{PAPER}" transform="rotate({a:.0f} {p[0]:.0f} {p[1]:.0f})" opacity=".9"/>')
    # light
    if night:
        o.append(beam(f'{wx0},{wy0} {wx1},{wy0} 470,960 120,960', 'beamC', .55))
        o.append(shade(lp[0] + 20, lp[1] - 60, 420, '#1e1648', .7))
        o.append(dust(21, (180, 300, 460, 900), 22, '#e6e2ff'))
    else:
        sun = [R.P('F', 1.5, .45), R.P('F', 1.5, .95), R.P('F', 2.6, 1.0), R.P('F', 2.6, .5)]
        o.append(f'<polygon points="{pts(*sun)}" fill="#ffd8b0" opacity=".38" filter="url(#soft)" style="mix-blend-mode:screen"/>')
        o.append(beam(f'{wx0},{wy0} {wx1},{wy0} {sun[2][0]:.0f},{sun[2][1]:.0f} {sun[3][0]:.0f},{sun[3][1]:.0f}', 'beamW', .7))
        o.append(shade(335, 520, 520, '#2c2160', .55))
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
o = ['<rect width="540" height="960" fill="#4a3462"/>']
o.append(''.join(f'<path d="M -20,{y} C 160,{y-30} 380,{y+20} 560,{y-10}" stroke="#3c2a52" stroke-width="2" fill="none"/>' for y in range(40, 1000, 46)))
o.append(glow(60, 120, 260, WARM, .55))  # lamp spill from the corner
o.append('<g transform="translate(30,40)"><circle r="70" fill="#5a4278"/><circle r="56" fill="#ffe0b8" opacity=".9"/></g>')  # lamp base from above
o.append(cast('<rect x="150" y="170" width="240" height="470" rx="30"/>', 18, 22, .6))
o.append('<rect x="150" y="170" width="240" height="470" rx="30" fill="#1d1838"/><rect x="160" y="180" width="220" height="450" rx="24" fill="url(#phoneScr)"/>')
o.append(glow(270, 400, 260, '#c8d0ff', .5))
o.append('<rect x="236" y="190" width="68" height="14" rx="7" fill="#1d1838"/>')
o.append('<text x="270" y="252" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#7a6ea0" text-anchor="middle">ไม่ทราบหมายเลข</text>')
o.append('<text x="270" y="272" font-family="Inter, sans-serif" font-size="11" fill="#9a90bc" text-anchor="middle">02:47</text>')
o.append('<rect x="176" y="296" width="176" height="74" rx="16" fill="#e2d8f6"/>')
o.append('<text font-family="IBM Plex Sans Thai, sans-serif" font-size="17" fill="#2a2148"><tspan x="192" y="326">ช่วยฉันด้วย</tspan><tspan x="192" y="352">ฉันยังอยู่ในบ้าน</tspan></text>')
o.append('<rect x="176" y="576" width="188" height="32" rx="16" fill="#ece6fa"/>')
o.append('<path d="M 410,660 C 440,720 470,760 560,780" fill="none" stroke="#2a2148" stroke-width="6"/>')
o.append(cast('<circle cx="90" cy="780" r="46"/>', 10, 12, .5) + '<g transform="translate(90,780)"><circle r="46" fill="#e6dcf2"/><circle r="36" fill="#6a3c38"/><ellipse cx="-8" cy="-8" rx="12" ry="6" fill="#ffffff" opacity=".25"/></g>')
o.append('<g transform="translate(430,860) rotate(18)"><rect x="-50" y="-16" width="100" height="32" rx="4" fill="#2a2148"/><circle cx="-34" cy="0" r="9" fill="#3a2f62"/></g>')  # glasses case / remote
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
o.append(f'<polygon points="{pts((0,620),(540,580),(540,960),(0,960))}" fill="#3a3070"/>')
o.append(f'<polygon points="{pts((0,700),(540,640),(540,700),(0,790))}" fill="#4a3f82"/>')
o.append(''.join(f'<polygon points="{pts((x,742-x*.1),(x+50,737-x*.1),(x+50,742-x*.1),(x,747-x*.1))}" fill="#9a8ed0" opacity=".7"/>' for x in range(0, 540, 110)))
o.append('<polygon points="400,0 540,0 540,960 450,960 450,420 400,380" fill="#1e1840"/><rect x="452" y="430" width="88" height="530" fill="#241d4c"/>')
o.append('<rect x="470" y="470" width="50" height="70" fill="url(#winLit)"/>' + glow(495, 505, 80, WARM, .6))
o.append('<rect x="20" y="300" width="7" height="330" fill="#1e1840"/><rect x="20" y="296" width="44" height="8" fill="#1e1840"/><rect x="44" y="304" width="20" height="6" fill="#ffd8a8"/>' + glow(54, 312, 140, WARM, .75) + pool(80, 700, 170, 46, WARM, .5))
o.append(beam('36,310 70,310 240,740 0,740', 'beamW', .5))
o.append(dust(37, (0, 320, 260, 760), 16))
S.append(('6A', 'ฉาก 6 · ถนนหน้าบ้านตอนค่ำ (ระดับสายตา)', 'มุมกว้างระดับถนน บ้านตรงข้ามอยู่ไกล ขอบบ้านพระเอกมืดเป็นฉากหน้าด้านขวา ถนนทอดลึก ไฟถนนเป็นวงอุ่นให้แฟนสาวเดินข้ามผ่าน', ''.join(o)))

S.append(('6B', 'ฉาก 6 · เงาสองคนบนผ้าม่าน แล้วไฟดับ', 'ผ้าม่านห้องนั่งเล่นปิด เรืองแสงอุ่นกลางบ้านมืด ไว้วางเงาสองคนต่อสู้กัน',
          street('shadow', moon=(450, 110)) + window_fg(None)))

# ---- 7A staircase down (one-point, from the top) ----
o = []
o.append('<rect width="540" height="960" fill="#2c2358"/>')
o.append(f'<polygon points="{pts((0,0),(160,300),(160,960),(0,960))}" fill="#4a3c7c"/><polygon points="{pts((540,0),(380,300),(380,960),(540,960))}" fill="#3a2f6a"/>')
for i in range(12):
    t0 = i / 12; t1 = (i + 1) / 12
    y0 = 960 - (960 - 330) * (t0 ** .8); y1 = 960 - (960 - 330) * (t1 ** .8)
    xl0 = 0 + 160 * t0; xr0 = 540 - 160 * t0; xl1 = 160 * t1; xr1 = 540 - 160 * t1
    o.append(f'<polygon points="{pts((xl0,y0),(xr0,y0),(xr1,y1+ (y0-y1)*.35),(xl1,y1+(y0-y1)*.35))}" fill="{"#6a5498" if i%2 else "#5e4a8c"}"/>')
    o.append(f'<polygon points="{pts((xl1,y1+(y0-y1)*.35),(xr1,y1+(y0-y1)*.35),(xr1,y1),(xl1,y1))}" fill="#3e3170"/>')
o.append(f'<rect x="160" y="200" width="220" height="130" fill="#1e1840"/>')  # dark hallway below
o.append(f'<path d="M 10,240 L 170,420 L 170,800" fill="none" stroke="#7a68b0" stroke-width="9"/>')
o.append(''.join(f'<line x1="{20+i*16}" y1="{254+i*18}" x2="{20+i*16}" y2="{254+i*18+90}" stroke="#7a68b0" stroke-width="4"/>' for i in range(10)))
o.append(f'<rect x="0" y="0" width="540" height="90" fill="#3a2f6a"/>')
o.append(glow(270, -40, 360, WARM, .7))  # light from the bedroom upstairs behind camera
o.append(beam('140,0 400,0 470,960 70,960', 'beamW', .55))
o.append(frame_pic(420, 380, 60, 80) + frame_pic(430, 520, 50, 64))
o.append(shade(270, 860, 640, '#1a1240', .6))
o.append(dust(38, (100, 60, 460, 900), 18))
S.append(('7A', 'ฉาก 7 · บันไดบ้านพระเอก', 'มองจากหัวบันไดลงไป ขั้นบันไดทอดลึกสู่โถงมืด แสงอุ่นจากห้องชั้นบนส่องตามหลัง ราวจับเป็นเส้นนำสายตา', ''.join(o)))

# ---- 7B porch: front door ajar, dark inside ----
R = Room((270, 470), 120, 170, 420, 760)
o = [R.shell(wall='#4a3f80', wall_lt='#5a4c90', wall_dk='#382e68', ceil='#2a2252', floor='#4e3e6c', planks=False)]
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
o = [R.shell(wall='#8a6cb0', wall_lt='#9e82c0', wall_dk='#6a5296', ceil='#5a4890', floor='#8a6078')]
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
o = [R.shell(wall='#2e2660', wall_lt='#3a3070', wall_dk='#221c4c', ceil='#18132f', floor='#2a2250')]
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
<p>ฉากหลังอย่างเดียว ยังไม่ใส่ตัวละคร · ห้องเป็นเปอร์สเปกทีฟมีความลึก ฉากหน้ามืดกรอบภาพ · บรรยากาศรวมโทนม่วงคราม เงาออกม่วง แสงอุ่นเป็นวงจากโคมไฟ หน้าต่าง และไฟถนน · บ้านตรงข้ามเห็นด้านข้างเป็นสามมิติ ใช้แบบเดียวกันทุกฉาก</p>
<label><input type="checkbox" id="g" onchange="document.body.classList.toggle('guides',this.checked)"> แสดงช่วงวางซับ (60–75% ของความสูง)</label></header>
<div class="grid">{"".join(cards)}</div></div>'''

open('scenes.html', 'w', encoding='utf-8').write(page)
print('scenes:', len(S))
