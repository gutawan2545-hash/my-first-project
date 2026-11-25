#!/usr/bin/env python3
"""บ้านตรงข้าม: ฉากหลังทุกฉาก (ยังไม่ใส่ตัวละคร)
รัน: python3 scenes.py  ->  scenes.html
เฟรม 540x960 (9:16) · โทนพาสเทลตาม CLAUDE.md · เว้นช่วง y 576-720 ให้เรียบไว้วางซับ
"""
import random, html

W, H = 540, 960

# ---------- palette (CLAUDE.md, ตอนบ้านตรงข้าม) ----------
LAV = '#ab9cd8'; LAV2 = '#cdb6dd'; LILAC = '#e6cfe2'
IVORY = '#f3ede2'; IVORY_SH = '#ddd2c8'; FLOOR = '#ede5ea'
ROSE = '#d88d9c'; ROSE_LT = '#eeb0bb'; SILVER = '#d6d4d5'
CANDLE = '#f6e8c8'; WINE = '#74222e'
CITY = '#9990bb'; SAGE = '#9fb8a4'; SAGE_DK = '#7d9a88'
ROOF = '#9a86ad'; ROOF_DK = '#7c6a92'; TRIM = '#fbf8f4'
NAVY = '#4f4a86'; NIGHT1 = '#5d5aa0'; NIGHT2 = '#8f84c4'

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stipple" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="moteBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="dof" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="dof2" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="haze" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="skyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a493d6"/><stop offset=".55" stop-color="#c9b3de"/><stop offset="1" stop-color="#ead3e4"/></linearGradient>
<linearGradient id="skyMorning" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b3a6e0"/><stop offset=".6" stop-color="#dcc6e6"/><stop offset="1" stop-color="#f6e2e6"/></linearGradient>
<linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7d74c0"/><stop offset=".6" stop-color="#b29ad2"/><stop offset="1" stop-color="#e2bfd8"/></linearGradient>
<linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4c4890"/><stop offset=".6" stop-color="#6e66ae"/><stop offset="1" stop-color="#9a8cc6"/></linearGradient>
<linearGradient id="skyFlash" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9c8fb8"/><stop offset="1" stop-color="#e6c9c6"/></linearGradient>
<linearGradient id="beamW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6ea" stop-opacity=".42"/><stop offset="1" stop-color="#fff6ea" stop-opacity="0"/></linearGradient>
<linearGradient id="beamC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eae6ff" stop-opacity=".38"/><stop offset="1" stop-color="#eae6ff" stop-opacity="0"/></linearGradient>
<radialGradient id="poolW" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#fff3e0" stop-opacity=".75"/><stop offset="1" stop-color="#fff3e0" stop-opacity="0"/></radialGradient>
<radialGradient id="poolC" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#e6e2ff" stop-opacity=".6"/><stop offset="1" stop-color="#e6e2ff" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".45" r=".75"><stop offset=".6" stop-color="#3a2f5a" stop-opacity="0"/><stop offset="1" stop-color="#3a2f5a" stop-opacity=".35"/></radialGradient>
<linearGradient id="wallDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efe4ec"/><stop offset="1" stop-color="#e4d6e2"/></linearGradient>
<linearGradient id="wallNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a80b8"/><stop offset="1" stop-color="#a698c8"/></linearGradient>
<linearGradient id="floorWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c8cc"/><stop offset="1" stop-color="#d4b2ba"/></linearGradient>
<linearGradient id="floorNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8c7eb4"/><stop offset="1" stop-color="#7a6ca6"/></linearGradient>
<linearGradient id="road" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b8aac8"/><stop offset="1" stop-color="#cbbdd6"/></linearGradient>
<linearGradient id="roadNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6a62a0"/><stop offset="1" stop-color="#7d73b0"/></linearGradient>
<linearGradient id="winLit" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4e2"/><stop offset="1" stop-color="#f6dcc8"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#d9d0f0"/><stop offset=".5" stop-color="#bfb2e2"/><stop offset="1" stop-color="#d4c8ec"/></linearGradient>
<linearGradient id="glassN" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5c5596"/><stop offset="1" stop-color="#4a447e"/></linearGradient>
<linearGradient id="phoneScr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f7f2fb"/><stop offset="1" stop-color="#e8def2"/></linearGradient>
</defs></svg>'''

TEX = ('<rect width="540" height="960" filter="url(#stipple)" opacity=".07" style="mix-blend-mode:overlay"/>'
       '<rect width="540" height="960" fill="url(#vig)"/>')

def dust(seed, box, n, col='#fff8f0'):
    r = random.Random(seed); x0, y0, x1, y1 = box
    far = ''.join(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(1.4,2.6):.1f}" opacity="{r.uniform(.25,.5):.2f}"/>' for _ in range(n))
    near = ''.join(f'<circle cx="{r.uniform(x0,x1):.0f}" cy="{r.uniform(y0,y1):.0f}" r="{r.uniform(.6,1.2):.1f}" opacity="{r.uniform(.6,.95):.2f}"/>' for _ in range(n//2))
    return f'<g fill="{col}"><g filter="url(#moteBlur)">{far}</g><g filter="url(#moteGlow)">{near}</g></g>'

def shadow(shape, dx=14, dy=16, op=.28, col='#5a3f6e'):
    return f'<g transform="translate({dx},{dy})" filter="url(#sh)" opacity="{op}" fill="{col}">{shape}</g>'

def beam(pts, grad='beamW', op=1):
    return f'<polygon points="{pts}" fill="url(#{grad})" filter="url(#haze)" opacity="{op}" style="mix-blend-mode:screen"/>'

def lit_dots(seed, x0, x1, y0, y1, n, col=CANDLE):
    r = random.Random(seed)
    return ''.join(f'<rect x="{r.uniform(x0,x1):.0f}" y="{r.uniform(y0,y1):.0f}" width="2.4" height="3.2" fill="{col}" opacity="{r.uniform(.5,.95):.2f}"/>' for _ in range(n))

def skyline(y, col=CITY, night=False, seed=4):
    r = random.Random(seed); out = []; x = -10
    while x < W + 10:
        w = r.randint(26, 54); h = r.randint(50, 150)
        out.append(f'<rect x="{x}" y="{y-h}" width="{w}" height="{h+40}" fill="{col}"/>')
        if night: out.append(lit_dots(seed + x, x + 3, x + w - 5, y - h + 6, y + 20, w // 5))
        x += w + r.randint(-4, 6)
    return f'<g filter="url(#dof2)" opacity=".9">{"".join(out)}</g>'

def tree(x, y, s=1, col=SAGE, dk=SAGE_DK):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<rect x="-4" y="0" width="8" height="46" fill="#9c8a9e"/>'
            f'<circle cx="0" cy="-12" r="34" fill="{dk}"/><circle cx="-18" cy="-2" r="24" fill="{col}"/>'
            f'<circle cx="14" cy="-26" r="26" fill="{col}"/><circle cx="-8" cy="-30" r="16" fill="#b8ceb9"/></g>')

def car(x, y, s=1, col='#c9c3d6', night=False):
    win = '#5e5894' if night else '#a9a0cf'
    return (f'<g transform="translate({x},{y}) scale({s})">'
            f'<path d="M -70,0 L -66,-24 C -60,-34 -40,-36 -28,-36 L 22,-36 C 38,-36 50,-30 58,-22 L 70,-18 L 72,0 Z" fill="{col}"/>'
            f'<path d="M -54,-26 L -46,-34 L -6,-34 L -6,-24 Z M 0,-34 L 24,-34 C 34,-34 42,-30 48,-24 L 0,-24 Z" fill="{win}"/>'
            f'<rect x="-72" y="-6" width="146" height="6" rx="3" fill="#a69fba"/>'
            f'<circle cx="-42" cy="2" r="11" fill="#4a4566"/><circle cx="44" cy="2" r="11" fill="#4a4566"/>'
            f'<circle cx="-42" cy="2" r="4" fill="#c9c3d6"/><circle cx="44" cy="2" r="4" fill="#c9c3d6"/></g>')

def streetlamp(x, y, h=300, on=False):
    g = f'<ellipse cx="{x+30}" cy="{y-h+20}" rx="70" ry="70" fill="url(#poolW)" filter="url(#glow)"/>' if on else ''
    return (g + f'<rect x="{x-3}" y="{y-h}" width="6" height="{h}" fill="#b6b0c8"/>'
            f'<path d="M {x},{y-h} C {x},{y-h-20} {x+30},{y-h-20} {x+36},{y-h-6}" fill="none" stroke="#b6b0c8" stroke-width="5"/>'
            f'<path d="M {x+24},{y-h-8} L {x+48},{y-h-8} L {x+44},{y-h} L {x+28},{y-h} Z" fill="{CANDLE if on else "#d8d2e4"}"/>')

# ---------- the house across: one design, reused everywhere ----------
def house(x, y, s=1, mode='day'):
    """mode: day | morning | night (lights on) | fight (lit, curtain half) | dark | shadow (silhouettes on curtain) | party"""
    night = mode in ('night', 'fight', 'dark', 'shadow', 'party')
    wall = '#f1e9e2' if not night else '#a79bc8'
    wall_sh = IVORY_SH if not night else '#8f83b8'
    roof = ROOF if not night else '#5e548e'
    roof_dk = ROOF_DK if not night else '#4d4579'
    trim = TRIM if not night else '#c4b9dc'
    lit = mode in ('night', 'fight', 'shadow', 'party')
    lr_fill = 'url(#winLit)' if lit else ('url(#glassN)' if night else 'url(#glass)')
    up_fill = 'url(#winLit)' if mode in ('night', 'party') else ('url(#glassN)' if night else 'url(#glass)')
    curtain = '#f4d6dc' if not night else ('#f0cfd2' if lit else '#6d6299')
    out = []
    # body
    out.append(f'<rect x="-150" y="-250" width="300" height="250" fill="{wall}"/>')
    out.append(f'<rect x="60" y="-250" width="90" height="250" fill="{wall_sh}"/>')
    # roof
    out.append(f'<path d="M -172,-246 L 0,-350 L 172,-246 Z" fill="{roof}"/>')
    out.append(f'<path d="M 0,-350 L 172,-246 L 120,-246 Z" fill="{roof_dk}"/>')
    out.append(f'<rect x="-174" y="-250" width="348" height="8" fill="{trim}"/>')
    # attic round window
    out.append(f'<circle cx="0" cy="-286" r="16" fill="{trim}"/><circle cx="0" cy="-286" r="11" fill="{up_fill}"/>')
    # upstairs window
    out.append(f'<rect x="-104" y="-226" width="80" height="78" fill="{trim}"/><rect x="-98" y="-220" width="68" height="66" fill="{up_fill}"/>')
    out.append(f'<path d="M -64,-220 L -64,-154 M -98,-187 L -30,-187" stroke="{trim}" stroke-width="3"/>')
    out.append(f'<rect x="-108" y="-150" width="88" height="7" fill="{trim}"/>')
    # balcony upstairs right
    out.append(f'<rect x="20" y="-226" width="96" height="84" fill="{trim}"/><rect x="26" y="-220" width="84" height="76" fill="{up_fill}"/>')
    out.append(f'<path d="M 68,-220 L 68,-144" stroke="{trim}" stroke-width="3"/>')
    out.append(f'<rect x="12" y="-150" width="112" height="6" fill="{trim}"/>')
    out.append(''.join(f'<rect x="{16+i*12}" y="-150" width="3" height="-0" fill="{trim}"/>' for i in range(0)))
    out.append(f'<path d="M 14,-178 L 122,-178 M 14,-150 L 122,-150" stroke="#c9bed8" stroke-width="2.4"/>')
    out.append(''.join(f'<rect x="{18+i*13}" y="-178" width="2.4" height="28" fill="#c9bed8"/>' for i in range(9)))
    # living room big window (left, ground floor)
    out.append(f'<rect x="-134" y="-126" width="130" height="98" fill="{trim}"/>')
    out.append(f'<rect x="-128" y="-120" width="118" height="86" fill="{lr_fill}"/>')
    if mode == 'fight':
        out.append(f'<path d="M -128,-120 L -96,-120 C -98,-90 -100,-60 -104,-34 L -128,-34 Z" fill="{curtain}"/>')
        out.append(f'<path d="M -10,-120 L -58,-120 C -56,-90 -54,-60 -50,-34 L -10,-34 Z" fill="{curtain}" opacity=".95"/>')
    elif mode == 'shadow':
        out.append(f'<rect x="-128" y="-120" width="118" height="86" fill="{curtain}" opacity=".9"/>')
        out.append(''.join(f'<path d="M {-120+i*14},-120 L {-120+i*14},-34" stroke="#e4b9c0" stroke-width="2"/>' for i in range(8)))
    elif mode == 'dark':
        out.append(f'<rect x="-128" y="-120" width="118" height="86" fill="{curtain}"/>')
    else:
        out.append(f'<path d="M -128,-120 L -108,-120 C -110,-90 -110,-60 -114,-34 L -128,-34 Z" fill="{curtain}"/>')
        out.append(f'<path d="M -10,-120 L -30,-120 C -28,-90 -28,-60 -24,-34 L -10,-34 Z" fill="{curtain}"/>')
    if mode == 'party':
        out.append(''.join(f'<circle cx="{-110+i*22}" cy="{-104+(i%2)*10}" r="7" fill="{c}"/>' for i, c in enumerate([ROSE_LT, '#c9b8f0', '#f6e2b0', '#b9dccb', ROSE_LT])))
    out.append(f'<path d="M -69,-120 L -69,-34 M -128,-77 L -10,-77" stroke="{trim}" stroke-width="3"/>')
    out.append(f'<rect x="-140" y="-30" width="142" height="7" fill="{trim}"/>')
    # front door (right, ground floor) + porch
    door = '#8c6f8e' if not night else '#4f4677'
    out.append(f'<rect x="34" y="-132" width="62" height="132" fill="{trim}"/>')
    out.append(f'<rect x="40" y="-126" width="50" height="126" fill="{door}"/>')
    out.append(f'<rect x="46" y="-118" width="38" height="44" fill="none" stroke="{trim}" stroke-width="2" opacity=".5"/>')
    out.append(f'<circle cx="82" cy="-62" r="2.6" fill="{SILVER}"/>')
    out.append(f'<path d="M 22,-140 L 108,-140 L 100,-150 L 30,-150 Z" fill="{roof_dk}"/>')
    lamp = CANDLE if night else '#ece6f2'
    out.append(f'<rect x="102" y="-110" width="10" height="16" rx="2" fill="{lamp}"/>')
    if night: out.append(f'<circle cx="107" cy="-100" r="26" fill="url(#poolW)" filter="url(#glow)"/>')
    # steps + planters
    out.append(f'<rect x="28" y="0" width="74" height="8" fill="#d8cedd"/><rect x="22" y="8" width="86" height="8" fill="#cdc2d4"/>')
    for px in (-140, -60):
        out.append(f'<rect x="{px}" y="-14" width="56" height="20" fill="#cfc3d8"/>')
        out.append(f'<circle cx="{px+12}" cy="-20" r="11" fill="{SAGE_DK}"/><circle cx="{px+30}" cy="-26" r="14" fill="{SAGE}"/><circle cx="{px+46}" cy="-18" r="10" fill="{SAGE_DK}"/>')
        out.append(''.join(f'<circle cx="{px+10+i*12}" cy="{-26+(i%2)*6}" r="3.2" fill="{ROSE_LT}"/>' for i in range(4)))
    return f'<g transform="translate({x},{y}) scale({s})">{"".join(out)}</g>'

def fence(y, x0=0, x1=W, col='#f6f1f5', night=False):
    c = col if not night else '#b2a6d0'
    posts = ''.join(f'<rect x="{x}" y="{y-34}" width="6" height="40" fill="{c}"/>' for x in range(x0, x1, 22))
    return f'<rect x="{x0}" y="{y-26}" width="{x1-x0}" height="4" fill="{c}"/><rect x="{x0}" y="{y-10}" width="{x1-x0}" height="4" fill="{c}"/>{posts}'

def street_view(mode='day', sky='skyDay', truck=False, car_trunk=False, extra=''):
    """the street seen from the hero's 2nd-floor window: house across centered"""
    night = mode in ('night', 'fight', 'dark', 'shadow', 'party')
    o = [f'<rect width="{W}" height="{H}" fill="url(#{sky})"/>']
    o.append(skyline(330, '#8f86b6' if not night else '#4d4785', night))
    o.append(f'<g filter="url(#dof)">{tree(40, 420, 1.3)}{tree(500, 430, 1.2)}</g>' if not night else
             f'<g filter="url(#dof)" opacity=".8">{tree(40, 420, 1.3, "#6f78a6", "#5a6290")}{tree(500, 430, 1.2, "#6f78a6", "#5a6290")}</g>')
    o.append(f'<rect x="0" y="560" width="{W}" height="400" fill="{"#d9cfe0" if not night else "#7a70ac"}"/>')
    o.append(house(270, 560, 1.18, mode))
    o.append(fence(600, 0, W, night=night))
    o.append(f'<rect x="0" y="606" width="{W}" height="20" fill="{"#e4dbe6" if not night else "#8a80b8"}"/>')
    o.append(f'<rect x="0" y="626" width="{W}" height="334" fill="url(#{"road" if not night else "roadNight"})"/>')
    o.append(''.join(f'<rect x="{x}" y="760" width="46" height="6" fill="{"#f6f0f4" if not night else "#a79bd0"}" opacity=".8"/>' for x in range(10, W, 90)))
    if truck:
        o.append(shadow('<rect x="30" y="500" width="190" height="90" rx="6"/>'))
        o.append('<g transform="translate(30,506) scale(.82)"><rect width="170" height="104" rx="5" fill="#f4eef3"/><rect width="170" height="12" fill="#e2d7e6"/>'
                 '<rect x="170" y="30" width="62" height="74" rx="6" fill="#c9b8e0"/><rect x="182" y="40" width="40" height="28" rx="3" fill="#8f86c0"/>'
                 '<circle cx="40" cy="106" r="15" fill="#4a4566"/><circle cx="196" cy="106" r="15" fill="#4a4566"/>'
                 '<text x="85" y="62" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#a08fb8" text-anchor="middle">ขนย้าย</text></g>')
        o.append('<g transform="translate(230,566) scale(.8)"><rect width="44" height="36" fill="#e8d6c4"/><rect x="50" y="10" width="36" height="26" fill="#dcc6b4"/><rect x="18" y="-24" width="30" height="24" fill="#efdccd"/></g>')
    if car_trunk:
        o.append(shadow('<rect x="340" y="580" width="150" height="36"/>'))
        o.append(car(400, 616, 1.0, '#bdb4d4', True))
        o.append('<path d="M 452,584 L 480,550 L 490,556 L 468,588 Z" fill="#a69fc4"/>')  # open trunk lid
    o.append(extra)
    return ''.join(o)

def window_frame(night=False, curtain=True):
    """hero's own 2nd-floor window as a big foreground frame"""
    wall = 'url(#wallDay)' if not night else 'url(#wallNight)'
    frame = TRIM if not night else '#cfc4e6'
    o = [f'<path d="M 0,0 L {W},0 L {W},{H} L 0,{H} Z M 44,96 L 496,96 L 496,640 L 44,640 Z" fill="{wall}" fill-rule="evenodd"/>']
    o.append(f'<path d="M 44,96 L 496,96 L 496,640 L 44,640 Z M 58,110 L 482,110 L 482,626 L 58,626 Z" fill="{frame}" fill-rule="evenodd"/>')
    o.append(f'<rect x="264" y="110" width="12" height="516" fill="{frame}"/><rect x="58" y="352" width="424" height="10" fill="{frame}"/>')
    o.append(f'<rect x="30" y="636" width="480" height="30" fill="{frame}"/><rect x="30" y="662" width="480" height="8" fill="{"#d9cdd8" if not night else "#a497c6"}"/>')
    if curtain:
        cc = '#f2d4da' if not night else '#b89cc6'; cd = '#e2b8c2' if not night else '#9f84b4'
        o.append(f'<path d="M 0,60 L 70,60 C 80,240 60,420 90,700 L 0,700 Z" fill="{cc}"/><path d="M 30,60 L 46,60 C 52,260 40,460 56,700 L 34,700 Z" fill="{cd}"/>')
        o.append(f'<path d="M {W},60 L 470,60 C 460,240 480,420 450,700 L {W},700 Z" fill="{cc}"/><path d="M 508,60 L 494,60 C 488,260 500,460 486,700 L 506,700 Z" fill="{cd}"/>')
        o.append(f'<rect x="0" y="50" width="{W}" height="10" rx="5" fill="{SILVER}"/>')
    # things on the sill + the hero's desk below it, so the lower frame is not empty
    pot = '#e6d3dc' if not night else '#a596c8'; leaf = SAGE if not night else '#7d86b2'
    o.append(shadow('<rect x="96" y="590" width="50" height="46"/>', 8, 8))
    o.append(f'<path d="M 98,600 L 142,600 L 136,636 L 104,636 Z" fill="{pot}"/>'
             f'<ellipse cx="108" cy="590" rx="14" ry="20" fill="{leaf}" transform="rotate(-20 108 590)"/><ellipse cx="128" cy="584" rx="12" ry="22" fill="{leaf}" transform="rotate(18 128 584)"/><ellipse cx="120" cy="576" rx="9" ry="18" fill="{"#b8ceb9" if not night else "#959dc4"}"/>')
    o.append(shadow('<rect x="380" y="606" width="40" height="30"/>', 8, 8))
    o.append(f'<rect x="380" y="604" width="30" height="32" rx="4" fill="#f8f2f5"/><path d="M 410,612 C 420,612 420,626 410,626" fill="none" stroke="#f8f2f5" stroke-width="4"/>')
    o.append(f'<path d="M 388,598 C 384,588 394,584 390,574 M 400,598 C 396,588 406,584 402,574" fill="none" stroke="#ffffff" stroke-width="1.6" opacity=".55"/>')
    o.append(f'<rect x="250" y="626" width="84" height="10" fill="{"#c9b8e6" if not night else "#8f81c0"}" transform="rotate(-3 290 630)"/><rect x="256" y="618" width="76" height="9" fill="{"#eeb0bb" if not night else "#b08cb8"}" transform="rotate(2 290 622)"/>')
    desk = '#f2e9ee' if not night else '#9e92c6'; desk_sh = '#ddd0da' if not night else '#887cb4'
    o.append(f'<rect x="20" y="760" width="500" height="22" fill="{desk}"/><rect x="20" y="782" width="500" height="10" fill="{desk_sh}"/>')
    o.append(f'<rect x="40" y="792" width="14" height="168" fill="{desk_sh}"/><rect x="486" y="792" width="14" height="168" fill="{desk_sh}"/>')
    o.append(f'<rect x="70" y="736" width="120" height="24" rx="3" fill="{"#d9cce8" if not night else "#8a7dbc"}"/><rect x="74" y="740" width="112" height="16" fill="{"#c6b6e0" if not night else "#7568aa"}"/>')
    o.append(f'<path d="M 400,760 L 420,690 L 470,690 L 450,760 Z" fill="{"#c9b8e6" if not night else "#7f72b4"}"/><ellipse cx="445" cy="690" rx="30" ry="8" fill="{CANDLE}" opacity="{".5" if not night else ".9"}"/>')
    if night: o.append('<ellipse cx="440" cy="740" rx="80" ry="50" fill="url(#poolW)" filter="url(#glow)" opacity=".8"/>')
    return ''.join(o)

def frame(content):
    return f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{content}{TEX}</svg>'

# ================= SCENES =================
S = []

# 1A flashback chase alley (warm faded)
o = ['<rect width="540" height="960" fill="url(#skyFlash)"/>']
o.append(skyline(300, '#a796b4', True, 9))
o.append('<path d="M 0,240 L 150,280 L 150,960 L 0,960 Z" fill="#c4aec0"/><path d="M 540,220 L 390,280 L 390,960 L 540,960 Z" fill="#b39fb8"/>')
o.append(''.join(f'<rect x="{20+i*0}" y="{330+i*90}" width="60" height="40" fill="#e9d2c8" opacity=".8"/>' for i in range(4)))
o.append(''.join(f'<rect x="440" y="{320+i*96}" width="70" height="44" fill="#ead6cc" opacity=".75"/>' for i in range(4)))
o.append('<path d="M 150,600 L 390,600 L 540,960 L 0,960 Z" fill="#d8c0c4"/>')
o.append('<path d="M 150,600 L 390,600 L 380,560 L 160,560 Z" fill="#cbb4c0"/>')
o.append(streetlamp(130, 600, 280, True) + streetlamp(410, 600, 260, True))
o.append(beam('150,330 230,330 330,820 40,820', 'beamW', .9))
o.append(shadow('<path d="M 300,820 L 380,780 L 420,830 L 340,870 Z"/>'))
o.append('<g transform="translate(330,800) rotate(-24)"><rect x="-40" y="-26" width="80" height="52" rx="6" fill="#bfa8c4"/><ellipse cx="-40" cy="0" rx="10" ry="26" fill="#a690b0"/></g>')  # knocked-over bin
o.append('<g fill="#f2e2da">' + ''.join(f'<rect x="{x}" y="{y}" width="14" height="10" transform="rotate({r} {x} {y})"/>' for x, y, r in [(250, 860, 20), (290, 900, -30), (190, 880, 50)]) + '</g>')
o.append(dust(11, (150, 340, 330, 800), 22))
o.append('<rect width="540" height="960" fill="#f2d8c8" opacity=".18" style="mix-blend-mode:soft-light"/>')
S.append(('1A', 'ฉาก 1 · ย้อนอดีต: ตรอกที่ไล่จับคนร้าย', 'โทนอุ่นซีดแบบความทรงจำ ไฟถนนสองดวง ถังขยะล้มกลางทาง ใช้กับช็อตอุบัติเหตุ', ''.join(o)))

# 1B / 2 bedroom day (hero's room, later investigation room)
def bedroom(night=False, board=False):
    wall = 'url(#wallDay)' if not night else 'url(#wallNight)'
    o = [f'<rect width="540" height="960" fill="{wall}"/>']
    # window to the street (right) with the house across visible, blurred
    view = street_view('night' if night else 'day', 'skyNight' if night else 'skyDay')
    o.append(f'<clipPath id="bw{int(night)}{int(board)}"><rect x="300" y="150" width="200" height="300"/></clipPath>')
    o.append(f'<g clip-path="url(#bw{int(night)}{int(board)})"><g filter="url(#dof)" transform="translate(300,150) scale(.37) translate(0,-120)">{view}</g></g>')
    fr = TRIM if not night else '#cfc4e6'
    o.append(f'<path d="M 290,140 L 510,140 L 510,460 L 290,460 Z M 300,150 L 500,150 L 500,450 L 300,450 Z" fill="{fr}" fill-rule="evenodd"/>')
    o.append(f'<rect x="395" y="150" width="8" height="300" fill="{fr}"/><rect x="284" y="456" width="232" height="14" fill="{fr}"/>')
    cc = '#f2d4da' if not night else '#b89cc6'
    o.append(f'<path d="M 270,120 L 304,120 C 300,260 306,380 296,500 L 270,500 Z" fill="{cc}"/><path d="M 530,120 L 496,120 C 500,260 494,380 504,500 L 530,500 Z" fill="{cc}"/>')
    o.append(f'<rect x="262" y="112" width="278" height="8" rx="4" fill="{SILVER}"/>')
    # wardrobe left
    wd = '#f6f0f2' if not night else '#b0a4d0'; wds = '#e2d6de' if not night else '#988cbc'
    o.append(shadow('<rect x="20" y="170" width="150" height="430"/>'))
    o.append(f'<rect x="14" y="160" width="150" height="430" fill="{wd}"/><rect x="118" y="160" width="46" height="430" fill="{wds}"/>')
    o.append(f'<path d="M 89,166 L 89,584" stroke="{wds}" stroke-width="3"/><circle cx="82" cy="380" r="3" fill="{SILVER}"/><circle cx="96" cy="380" r="3" fill="{SILVER}"/>')
    o.append(f'<rect x="10" y="150" width="158" height="12" fill="{wds}"/>')
    # wall frames (or investigation board)
    if board:
        o.append(shadow('<rect x="180" y="150" width="96" height="210"/>', 8, 10))
        o.append('<rect x="176" y="146" width="98" height="212" fill="#d9c0b0"/><rect x="180" y="150" width="90" height="204" fill="#e8d2c2"/>')
        pins = [(196, 168), (240, 176), (204, 230), (250, 238), (214, 300), (246, 316)]
        o.append(''.join(f'<rect x="{x-14}" y="{y-6}" width="30" height="36" fill="#fbf7f2" transform="rotate({(i*7)%13-6} {x} {y})"/><rect x="{x-11}" y="{y-3}" width="24" height="22" fill="#b9add2" transform="rotate({(i*7)%13-6} {x} {y})"/>' for i, (x, y) in enumerate(pins)))
        o.append('<path d="M 196,168 L 240,176 L 204,230 L 250,238 L 214,300 L 246,316 M 196,168 L 214,300" fill="none" stroke="#b03a48" stroke-width="1.6"/>')
        o.append(''.join(f'<circle cx="{x}" cy="{y}" r="3" fill="{WINE}"/>' for x, y in pins))
        o.append('<rect x="186" y="330" width="44" height="14" fill="#fff4b8" transform="rotate(-4 200 336)"/><rect x="236" y="268" width="28" height="12" fill="#fff4b8" transform="rotate(5 250 274)"/>')
    else:
        for (x, y, w, h) in [(190, 180, 60, 76), (196, 280, 48, 56)]:
            o.append(shadow(f'<rect x="{x}" y="{y}" width="{w}" height="{h}"/>', 6, 8))
            o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SILVER}"/><rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" fill="#cbbde6"/>'
                     f'<path d="M {x+6},{y+h-6} L {x+w/2-4},{y+h/2} L {x+w-6},{y+h-10} Z" fill="#9f8fc8"/><circle cx="{x+w-16}" cy="{y+18}" r="5" fill="{CANDLE}"/>')
    # floor
    o.append(f'<rect x="0" y="590" width="540" height="370" fill="url(#{"floorWood" if not night else "floorNight"})"/>')
    o.append(''.join(f'<path d="M 0,{y} L 540,{y}" stroke="{"#d6bcc2" if not night else "#7266a0"}" stroke-width="1.4"/>' for y in (650, 730, 830)))
    # bed behind (left-center), low so subtitle band stays calm
    bed = '#f7f1f4' if not night else '#b6aad6'
    o.append(shadow('<rect x="40" y="520" width="250" height="110"/>'))
    o.append(f'<rect x="30" y="486" width="22" height="130" fill="#c8b2c4"/>')
    o.append(f'<rect x="30" y="540" width="250" height="70" rx="8" fill="{bed}"/><rect x="30" y="566" width="250" height="44" fill="{ROSE_LT if not night else "#a690c4"}"/>')
    o.append(f'<ellipse cx="90" cy="540" rx="40" ry="16" fill="#ffffff" opacity="{".9" if not night else ".5"}"/>')
    # window seat chair + side table with coffee (hero sits here later)
    o.append(shadow('<rect x="330" y="560" width="150" height="80"/>'))
    o.append(f'<rect x="320" y="520" width="150" height="40" rx="10" fill="{"#c9b8e6" if not night else "#8a7cbc"}"/><rect x="320" y="556" width="150" height="40" rx="8" fill="{"#d8caee" if not night else "#9a8ccc"}"/>')
    o.append('<rect x="330" y="596" width="8" height="26" fill="#a99ac2"/><rect x="452" y="596" width="8" height="26" fill="#a99ac2"/>')
    o.append(f'<rect x="478" y="520" width="50" height="8" fill="{SILVER}"/><rect x="500" y="528" width="6" height="90" fill="{SILVER}"/>')
    o.append('<path d="M 492,506 L 512,506 L 510,520 L 494,520 Z" fill="#f6eef2"/><path d="M 512,510 C 518,510 518,516 512,516" fill="none" stroke="#f6eef2" stroke-width="2"/>')
    if board:
        # camera with telephoto on a tripod at the window, papers on floor, desk lamp glow
        o.append('<g transform="translate(410,420)"><path d="M 0,40 L -30,200 M 0,40 L 30,200 M 0,40 L 0,205" stroke="#6f6890" stroke-width="3"/>'
                 '<rect x="-22" y="16" width="34" height="24" rx="3" fill="#4f4870"/><rect x="10" y="20" width="44" height="16" rx="3" fill="#5d5680"/><circle cx="56" cy="28" r="9" fill="#3d3860"/></g>')
        o.append('<g fill="#fbf6f2">' + ''.join(f'<rect x="{x}" y="{y}" width="34" height="26" transform="rotate({r} {x} {y})"/>' for x, y, r in [(80, 800, -12), (150, 850, 8), (240, 790, 20), (320, 880, -6)]) + '</g>')
        o.append('<g fill="#b9add2">' + ''.join(f'<rect x="{x+4}" y="{y+4}" width="22" height="14" transform="rotate({r} {x} {y})"/>' for x, y, r in [(80, 800, -12), (240, 790, 20)]) + '</g>')
        o.append('<ellipse cx="230" cy="520" rx="120" ry="90" fill="url(#poolW)" filter="url(#glow)" opacity=".8"/>')
    if night:
        o.append(beam('300,450 500,450 470,900 220,900', 'beamC', .7))
        o.append(dust(21, (260, 460, 500, 880), 20, '#efeaff'))
    else:
        o.append(beam('300,450 500,450 520,920 250,920', 'beamW', .85))
        o.append(dust(22, (270, 460, 520, 900), 24))
    return ''.join(o)

S.append(('1B', 'ฉาก 1–2 · ห้องนอนพระเอก ชั้นสอง (กลางวัน)', 'ตู้เสื้อผ้า กรอบรูป เตียงด้านหลัง และมุมนั่งริมหน้าต่างที่มีกาแฟ ใช้กับช็อตชีวิตพักขาและช็อตนั่งดื่มกาแฟ ข้างนอกเห็นบ้านตรงข้ามแบบเบลอ', bedroom()))

S.append(('2', 'ฉาก 2 · มองจากหน้าต่าง: รถขนของมาจอดบ้านตรงข้าม', 'มุมมองพระเอก ขอบหน้าต่างและผ้าม่านเป็นฉากหน้า บ้านตรงข้ามอยู่กลางเฟรม รถขนของกับกล่องหน้าบ้าน',
          street_view('day', 'skyDay', truck=True, extra=dust(31, (60, 120, 480, 600), 16)) + window_frame()))

S.append(('3A', 'ฉาก 3 · บ้านตรงข้ามยามเช้า', 'แสงเช้าอ่อน กระถางดอกไม้หน้าบ้านสำหรับช็อตภรรยารดน้ำต้นไม้ มองผ่านหน้าต่างพระเอก',
          street_view('morning', 'skyMorning', extra=beam('0,100 160,100 420,620 160,620', 'beamW', .7) + dust(32, (60, 120, 420, 600), 18)) + window_frame()))

S.append(('3B', 'ฉาก 3 · คืนวันศุกร์ ห้องนั่งเล่นเปิดไฟ', 'ไฟห้องนั่งเล่นเปิด ผ้าม่านแง้ม เห็นเงาคนทะเลาะในช็อตถัดไป แล้วปิดม่าน ไฟดับ',
          street_view('fight', 'skyNight', extra=dust(33, (80, 380, 300, 600), 12, '#fff2e2')) + window_frame(True)))

S.append(('4', 'ฉาก 4 · ตีสอง ลากถุงดำขึ้นท้ายรถ', 'ไฟบ้านดับเกือบหมด เหลือไฟหน้าประตู ไฟถนนส่องลงลานหน้าบ้าน รถเปิดท้ายรออยู่',
          street_view('dark', 'skyNight', car_trunk=True, extra=streetlamp(500, 640, 300, True) + beam('470,340 560,340 560,700 380,700', 'beamW', .6) + dust(34, (390, 360, 540, 680), 14, '#fff2e2')) + window_frame(True)))

S.append(('5A', 'ฉาก 5 · ห้องนอนกลายเป็นห้องสืบสวน (กลางคืน)', 'บอร์ดรูปถ่ายโยงด้ายแดง โน้ตเหลือง กล้องเลนส์ยาวบนขาตั้งหันออกหน้าต่าง กระดาษกระจายบนพื้น',
          bedroom(night=True, board=True)))

# 5B phone on bedside table, top-down
o = ['<rect width="540" height="960" fill="#cbb8d6"/>']
o.append(''.join(f'<path d="M 0,{y} L 540,{y-60}" stroke="#bda8cc" stroke-width="2"/>' for y in range(80, 1100, 70)))  # wood grain, top-down
o.append('<ellipse cx="270" cy="400" rx="260" ry="260" fill="url(#poolC)" filter="url(#glow)"/>')
o.append(shadow('<rect x="150" y="150" width="240" height="470" rx="30"/>', 16, 20, .35))
o.append('<rect x="150" y="150" width="240" height="470" rx="30" fill="#3f3a5c"/><rect x="160" y="160" width="220" height="450" rx="24" fill="url(#phoneScr)"/>')
o.append('<rect x="236" y="170" width="68" height="14" rx="7" fill="#3f3a5c"/>')
o.append('<text x="270" y="232" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#8a7fa6" text-anchor="middle">ไม่ทราบหมายเลข</text>')
o.append('<text x="270" y="252" font-family="Inter, sans-serif" font-size="11" fill="#a99fc0" text-anchor="middle">02:47</text>')
o.append('<rect x="176" y="276" width="176" height="74" rx="16" fill="#e6dcf0"/>')
o.append('<text font-family="IBM Plex Sans Thai, sans-serif" font-size="17" fill="#3b3346"><tspan x="192" y="306">ช่วยฉันด้วย</tspan><tspan x="192" y="332">ฉันยังอยู่ในบ้าน</tspan></text>')
o.append('<rect x="176" y="556" width="188" height="32" rx="16" fill="#efe8f6"/>')
o.append('<path d="M 410,640 C 440,700 470,740 520,760" fill="none" stroke="#efe6f4" stroke-width="5" opacity=".8"/>')  # charger cable
o.append('<g transform="translate(70,740)"><circle r="44" fill="#f6eef2"/><circle r="34" fill="#c99a8a"/><circle r="34" fill="#a9705e" opacity=".5"/></g>')  # coffee cup top-down
o.append(dust(35, (120, 160, 420, 600), 12, '#f2eeff'))
S.append(('5B', 'ฉาก 5 · ข้อความจากเบอร์ไม่รู้จัก', 'มุมมองจากบนลงโต๊ะข้างเตียง จอมือถือเรืองแสง ข้อความ "ช่วยฉันด้วย ฉันยังอยู่ในบ้าน" เวลา 02:47', ''.join(o)))

# 5C window shadow pounding glass (close on the house across upstairs window)
o = ['<rect width="540" height="960" fill="url(#skyNight)"/>']
o.append(f'<g transform="translate(270,980) scale(2.6)">{house(0, 0, 1, "dark")}</g>')
o.append('<rect x="80" y="140" width="210" height="200" fill="url(#winLit)" opacity=".85"/>')
o.append('<path d="M 150,340 C 146,280 160,236 186,226 C 178,210 182,190 196,186 C 212,184 220,200 214,218 C 236,228 248,262 252,340 Z" fill="#4b3f72" opacity=".85" filter="url(#dof)"/>')  # silhouette placeholder
o.append('<path d="M 222,214 L 252,170 L 262,176 L 232,222 Z" fill="#4b3f72" opacity=".85" filter="url(#dof)"/>')  # raised arm hitting glass
o.append('<path d="M 250,168 L 270,150 M 250,168 L 276,176 M 250,168 L 262,196 M 250,168 L 236,148" stroke="#ffffff" stroke-width="1.4" opacity=".8"/>')  # crack
o.append(dust(36, (80, 140, 300, 340), 10, '#fff2e2'))
S.append(('5C', 'ฉาก 5 · เงาผู้หญิงทุบกระจกชั้นบน', 'ซูมเข้าหน้าต่างชั้นบนของบ้านตรงข้าม ไฟในห้องสลัว เงาผู้หญิงชูแขนทุบกระจก กระจกร้าว เงาเป็นตัวแทนชั่วคราว จะวาดตอนทำตัวละคร', ''.join(o)))

S.append(('6A', 'ฉาก 6 · ถนนหน้าบ้านตอนโพล้เพล้', 'มุมกว้างจากหน้าต่าง ถนนว่างสำหรับช็อตแฟนสาวเดินข้ามไปกดกริ่ง ไฟหน้าประตูบ้านตรงข้ามเปิด',
          street_view('night', 'skyDusk', extra=streetlamp(40, 640, 300, True) + beam('20,340 120,340 260,900 0,900', 'beamW', .55) + dust(37, (0, 360, 240, 880), 14)) + window_frame(True)))

S.append(('6B', 'ฉาก 6 · เงาสองคนบนผ้าม่าน แล้วไฟดับ', 'ผ้าม่านห้องนั่งเล่นปิดสนิท ไฟในห้องเปิด ใช้วางเงาสองคนต่อสู้กันในช็อตถัดไป ก่อนไฟทั้งบ้านดับ',
          street_view('shadow', 'skyNight') + window_frame(True)))

# 7A staircase going down (hero's house, night)
o = ['<rect width="540" height="960" fill="url(#wallNight)"/>']
o.append('<rect x="0" y="0" width="540" height="200" fill="#9e92c6"/>')
o.append('<ellipse cx="380" cy="80" rx="200" ry="140" fill="url(#poolW)" filter="url(#glow)" opacity=".7"/>')
for i in range(9):
    y = 300 + i * 70; x = 120 + i * 30
    o.append(f'<rect x="{x}" y="{y}" width="{540-x}" height="70" fill="{"#a094c8" if i % 2 else "#9488bf"}"/><rect x="{x}" y="{y}" width="{540-x}" height="10" fill="#c2b6e2"/>')
o.append('<path d="M 60,180 L 420,960" stroke="#cfc4e6" stroke-width="10"/>')  # handrail
o.append(''.join(f'<rect x="{90+i*34}" y="{260+i*74}" width="6" height="{100}" fill="#cfc4e6"/>' for i in range(10)))
o.append(f'<rect x="0" y="0" width="80" height="960" fill="#7f73ae"/>')
o.append(beam('300,0 470,0 540,700 260,700', 'beamW', .6))
o.append(dust(38, (260, 40, 540, 680), 16))
S.append(('7A', 'ฉาก 7 · บันไดบ้านพระเอก', 'พระเอกคว้าไม้ค้ำยันรีบลงบันได แสงจากห้องชั้นบนส่องตามขั้นบันได ราวจับเป็นเส้นนำสายตา', ''.join(o)))

# 7B front door ajar, dark inside, phone ringing glow
o = ['<rect width="540" height="960" fill="#5a5296"/>']
o.append('<rect x="80" y="120" width="380" height="700" fill="#cfc4e6"/><rect x="100" y="140" width="340" height="680" fill="#2e2a52"/>')
o.append('<path d="M 100,140 L 330,180 L 330,820 L 100,820 Z" fill="#4f4677"/><path d="M 100,140 L 330,180 L 330,820 L 100,820 Z" fill="#000" opacity=".12"/>')  # door swung in
o.append('<circle cx="304" cy="510" r="5" fill="#d6d4d5"/>')
o.append('<ellipse cx="400" cy="760" rx="70" ry="28" fill="url(#poolC)" filter="url(#glow)"/>')
o.append('<rect x="384" y="752" width="30" height="14" rx="3" fill="#dcd4ff"/>')  # phone glowing on the floor inside
o.append('<rect x="60" y="820" width="420" height="20" fill="#9a8ec4"/><rect x="40" y="840" width="460" height="120" fill="#7d73b0"/>')
o.append('<rect x="458" y="300" width="16" height="26" rx="3" fill="#f6e8c8"/><circle cx="466" cy="312" r="40" fill="url(#poolW)" filter="url(#glow)"/>')
o.append(beam('330,180 440,150 520,960 330,960', 'beamW', .35))
o.append(dust(39, (330, 200, 520, 900), 12))
S.append(('7B', 'ฉาก 7 · ประตูบ้านตรงข้ามเปิดแง้ม', 'ข้างในมืดสนิท มีแสงมือถือของแฟนเรืองอยู่บนพื้นห้อง ไฟหน้าประตูดวงเดียว เว้นจังหวะเงียบก่อนผลักประตู', ''.join(o)))

# 7C surprise party living room, lights on
o = ['<rect width="540" height="960" fill="url(#wallDay)"/>']
o.append('<rect x="300" y="120" width="210" height="320" fill="url(#skyNight)"/>' + f'<g clip-path="url(#pv)"></g>')
o.append(f'<path d="M 290,110 L 520,110 L 520,450 L 290,450 Z M 300,120 L 510,120 L 510,440 L 300,440 Z" fill="{TRIM}" fill-rule="evenodd"/><rect x="401" y="120" width="8" height="320" fill="{TRIM}"/>')
o.append('<path d="M 270,96 L 306,96 C 302,240 308,380 298,470 L 270,470 Z" fill="#f2d4da"/><path d="M 536,96 L 504,96 C 508,240 502,380 512,470 L 536,470 Z" fill="#f2d4da"/>')
# banner
o.append('<path d="M 30,90 Q 270,170 510,90" fill="none" stroke="#c9b8d8" stroke-width="2"/>')
cols = [ROSE_LT, '#c9b8f0', '#f6e2b0', '#b9dccb']
for i, ch in enumerate('SURPRISE'):
    t = (i + .5) / 8; x = 30 + 480 * t; y = 90 + 80 * 4 * t * (1 - t) * .5 + 6
    o.append(f'<path d="M {x-22},{y} L {x+22},{y} L {x},{y+46} Z" fill="{cols[i%4]}"/><text x="{x}" y="{y+22}" font-family="Inter, sans-serif" font-weight="700" font-size="16" fill="#6b5a86" text-anchor="middle">{ch}</text>')
# balloons
for (x, y, c) in [(60, 260, ROSE_LT), (100, 220, '#c9b8f0'), (140, 270, '#f6e2b0'), (470, 520, '#b9dccb'), (510, 480, ROSE_LT)]:
    o.append(f'<path d="M {x},{y+30} C {x+6},{y+80} {x-6},{y+120} {x+4},{y+170}" fill="none" stroke="#bcaed0" stroke-width="1.2"/><ellipse cx="{x}" cy="{y}" rx="24" ry="30" fill="{c}"/><ellipse cx="{x-8}" cy="{y-10}" rx="6" ry="9" fill="#ffffff" opacity=".6"/>')
# sofa + cake table
o.append(shadow('<rect x="40" y="480" width="250" height="110"/>'))
o.append('<rect x="30" y="460" width="250" height="60" rx="16" fill="#c9b8e6"/><rect x="20" y="510" width="270" height="70" rx="14" fill="#d8caee"/><rect x="40" y="580" width="10" height="20" fill="#a99ac2"/><rect x="260" y="580" width="10" height="20" fill="#a99ac2"/>')
o.append(f'<rect x="0" y="600" width="540" height="360" fill="url(#floorWood)"/>')
o.append('<ellipse cx="270" cy="760" rx="230" ry="60" fill="#f4e8ee"/>')
o.append(shadow('<rect x="150" y="560" width="220" height="60"/>'))
o.append(f'<rect x="140" y="546" width="240" height="14" fill="#f8f2f6"/><rect x="160" y="560" width="10" height="70" fill="{SILVER}"/><rect x="350" y="560" width="10" height="70" fill="{SILVER}"/>')
o.append('<g transform="translate(260,546)"><rect x="-44" y="-44" width="88" height="44" rx="6" fill="#fbf6f4"/><rect x="-44" y="-30" width="88" height="10" fill="#eeb0bb"/><rect x="-30" y="-70" width="60" height="28" rx="5" fill="#fdf8f6"/>'
         + ''.join(f'<rect x="{-22+i*14}" y="-86" width="4" height="16" fill="#c9b8f0"/><ellipse cx="{-20+i*14}" cy="-90" rx="3" ry="5" fill="{CANDLE}"/>' for i in range(4)) + '</g>')
o.append('<ellipse cx="262" cy="460" rx="70" ry="50" fill="url(#poolW)" filter="url(#glow)"/>')
o.append('<g>' + ''.join(f'<rect x="{x}" y="{y}" width="6" height="10" fill="{c}" transform="rotate({r} {x} {y})"/>' for x, y, r, c in
         [(90, 300, 20, ROSE), (200, 240, -30, '#b6a2e8'), (330, 280, 45, '#e8c46a'), (420, 220, 10, ROSE), (150, 380, -15, '#8fc4ae'), (380, 360, 30, '#b6a2e8'), (470, 300, -40, ROSE)]) + '</g>')
o.append(beam('20,0 200,0 360,620 60,620', 'beamW', .5))
o.append(dust(40, (20, 60, 360, 600), 18))
S.append(('7C', 'ฉาก 7 · เซอร์ไพรส์! ห้องนั่งเล่นเปิดไฟพร้อมกัน', 'ป้าย SURPRISE ลูกโป่งพาสเทล เค้กเทียนบนโต๊ะ โซฟา กระดาษสีลอย เว้นพื้นกลางห้องไว้วางทุกคน', ''.join(o)))

S.append(('8A', 'ฉาก 8 · กล้องถอยออกจากหน้าต่างงานเลี้ยง', 'มองจากถนน หน้าต่างห้องนั่งเล่นสว่างและมีลูกโป่ง เสียงหัวเราะค่อยจาง ก่อนแพนไปบ้านหลังที่สาม',
          street_view('party', 'skyNight', extra=streetlamp(500, 640, 300, True) + dust(41, (80, 380, 300, 600), 10, '#fff2e2'))))

# 8B third house, dark upstairs room with binoculars and photos
o = ['<rect width="540" height="960" fill="#4a4580"/>']
o.append('<rect x="140" y="110" width="300" height="340" fill="url(#skyNight)"/>')
o.append(f'<g clip-path="url(#tw)"></g><clipPath id="tw"><rect x="140" y="110" width="300" height="340"/></clipPath><g clip-path="url(#tw)"><g filter="url(#dof2)" transform="translate(140,110) scale(.56) translate(0,-160)">{street_view("party","skyNight")}</g></g>')
o.append('<path d="M 130,100 L 450,100 L 450,460 L 130,460 Z M 140,110 L 440,110 L 440,450 L 140,450 Z" fill="#6a6299" fill-rule="evenodd"/><rect x="286" y="110" width="8" height="340" fill="#6a6299"/>')
o.append('<path d="M 100,80 L 150,80 C 146,240 152,380 140,520 L 100,520 Z" fill="#3e3a6c"/><path d="M 480,80 L 430,80 C 434,240 428,380 440,520 L 480,520 Z" fill="#3e3a6c"/>')
o.append(beam('140,450 440,450 470,960 80,960', 'beamC', .55))
# desk covered in photos
o.append('<rect x="0" y="560" width="540" height="400" fill="#3a3668"/>')
o.append('<rect x="40" y="540" width="460" height="22" fill="#5a5290"/><path d="M 40,562 L 500,562 L 540,960 L 0,960 Z" fill="#4d4682"/>')
r = random.Random(8)
for i in range(16):
    x = r.uniform(30, 470); y = r.uniform(580, 900); a = r.uniform(-25, 25)
    o.append(f'<g transform="rotate({a:.0f} {x+24:.0f} {y+18:.0f})"><rect x="{x:.0f}" y="{y:.0f}" width="52" height="40" fill="#e6e0f2"/><rect x="{x+4:.0f}" y="{y+4:.0f}" width="44" height="28" fill="#8c84b8"/></g>')
o.append('<g transform="translate(150,640) rotate(-8)"><rect x="0" y="0" width="70" height="54" fill="#f2ecf8"/><rect x="5" y="5" width="60" height="38" fill="#9a92c4"/>'
         '<path d="M 14,43 L 14,22 L 30,14 L 46,22 L 46,43 Z" fill="#6d6599"/><rect x="40" y="20" width="16" height="12" fill="#f6e8c8"/></g>')  # photo of the hero's window
o.append(''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{WINE}"/>' for x, y in [(160, 646), (200, 700), (330, 760)]))
# binoculars on the sill
o.append('<g transform="translate(250,476)"><rect x="-40" y="-14" width="34" height="30" rx="8" fill="#26233f"/><rect x="6" y="-14" width="34" height="30" rx="8" fill="#26233f"/><rect x="-8" y="-6" width="16" height="12" fill="#1d1a33"/>'
         '<circle cx="-23" cy="-14" r="10" fill="#3a3660"/><circle cx="23" cy="-14" r="10" fill="#3a3660"/><circle cx="-26" cy="-17" r="3" fill="#cfc8ff" opacity=".8"/><circle cx="20" cy="-17" r="3" fill="#cfc8ff" opacity=".8"/></g>')
o.append(dust(42, (100, 460, 480, 940), 18, '#e6e2ff'))
o.append('<rect width="540" height="960" fill="#2a2450" opacity=".18"/>')
S.append(('8B', 'ฉาก 8 · ห้องมืดในบ้านหลังที่สาม', 'กล้องส่องทางไกลวางหันออกหน้าต่าง เห็นงานเลี้ยงไกล ๆ แบบเบลอ โต๊ะเต็มไปด้วยรูปถ่าย รวมรูปหน้าต่างห้องพระเอก ฉากนี้เย็นและมืดกว่าที่อื่น แต่ยังเห็นรายละเอียด', ''.join(o)))

# ---------- page ----------
cards = []
for sid, title, note, body in S:
    cards.append(f'''<figure><div class="fr">{frame(body)}<div class="sub" aria-hidden="true"></div></div>
<figcaption><b>{sid}</b> {html.escape(title)}<span>{html.escape(note)}</span></figcaption></figure>''')

page = f'''<title>บ้านตรงข้าม ฉากทั้งหมด</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: grid of 9:16 frames, 4 per row on desktop, 2 on phones. Bright pastel page to match the episode. */
:root {{ --bg:#f5f0f3; --card:#ffffff; --ink:#3b3346; --muted:#847a90; --line:#e2d9e3; --accent:#8a6cc8; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:light; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:20px; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }}
header p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.6; max-width:80ch; }}
label {{ font-size:13px; color:var(--muted); display:inline-flex; gap:6px; align-items:center; margin-top:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:18px; }}
figure {{ margin:0; display:grid; gap:8px; min-width:0; }}
.fr {{ position:relative; border-radius:6px; overflow:hidden; box-shadow:0 0 0 1px var(--line); }}
.fr svg {{ display:block; width:100%; height:auto; }}
.sub {{ position:absolute; left:0; right:0; top:60%; height:15%; border-block:1px dashed rgba(255,255,255,.9); background:rgba(255,255,255,.08); display:none; }}
body.guides .sub {{ display:block; }}
figcaption {{ font-size:13px; line-height:1.55; }}
figcaption b {{ color:var(--accent); font-weight:500; margin-right:4px; }}
figcaption span {{ display:block; color:var(--muted); font-size:12px; margin-top:2px; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&family=Inter:wght@700&display=swap">
{DEFS}
<div class="wrap">
<header><h1>บ้านตรงข้าม · ฉากทั้งหมด ({len(S)} ฉาก)</h1>
<p>ฉากหลังอย่างเดียว ยังไม่ใส่ตัวละคร · โทนพาสเทลลาเวนเดอร์ ขาวงาช้าง ชมพูกุหลาบ · กลางคืนใช้ฟ้าลาเวนเดอร์อมน้ำเงินแทนความมืด · บ้านตรงข้ามใช้แบบเดียวกันทุกฉากเพื่อความต่อเนื่อง · เม็ดเกรน ลำแสง ฝุ่น เงาตก และฉากหลังเบลอตามมาตรฐานช่อง</p>
<label><input type="checkbox" id="g" onchange="document.body.classList.toggle('guides',this.checked)"> แสดงช่วงวางซับ (60–75% ของความสูง)</label></header>
<div class="grid">{"".join(cards)}</div></div>'''

open('scenes.html', 'w', encoding='utf-8').write(page)
print('scenes:', len(S))
