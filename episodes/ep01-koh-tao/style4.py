"""EP.01 scenes in the approved warm medium-shot style (round 4).
Odd Hours' own graphics (yellow Thai subs, purple-rim capsule, purple step numbers, eye watermark),
island dressing in every set (buoys, nets, shells, driftwood, lifebuoys, longtail ribbons, sea views),
fine dust that lives inside the light beams, light level set per scene.
Run: python3 style4.py -> scenes_v4.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
import kt_scenes as K
from style3 import wood_planks, jar
from scenes import cumulus, palm, boulder
ISL = K.ISL
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'

CL.RIGS['warm'] = dict(rim='#ffcf96', rim_op=.95, rim_soft_op=.3, rim_w=2.4, bloom=.38,
                       amb='#5e4a62', shade_op=.36, shade_k=14, shade_blur=10, face_shade=.18, chin_ao=.42,
                       sat=.98, lift=(.016, .012, .022), gamma=(1.03, 1.04, 1.06), gain=(1.0, .975, .93), vig=.5, grain=.075)
CL.RIGS['dusk'] = dict(rim='#ffc48a', rim_op=1.0, rim_soft_op=.34, rim_w=2.6, bloom=.42,
                       amb='#4e4468', shade_op=.4, shade_k=15, shade_blur=11, face_shade=.2, chin_ao=.45,
                       sat=.96, lift=(.014, .012, .03), gamma=(1.06, 1.06, 1.05), gain=(1.0, .97, .94), vig=.55, grain=.075)
CL.RIGS['moon'] = dict(rim='#ffcf9a', rim_op=.9, rim_soft_op=.28, rim_w=2.4, bloom=.34,
                       amb='#3a4468', shade_op=.5, shade_k=16, shade_blur=11, face_shade=.24, chin_ao=.5,
                       sat=.9, lift=(.008, .012, .04), gamma=(1.16, 1.12, 1.04), gain=(.98, .97, 1.0), vig=.62, grain=.08)

_ids = [0]


def uid(p='u'):
    _ids[0] += 1
    return f'{p}{_ids[0]}'


# ================================================================ light + dust
def beam_set(fid, quads, color='#fff0d4', op=.3):
    """Soft light beams; returns (svg, clip id) so dust can live inside the beams."""
    g, c = uid('bm'), uid('bc')
    d = (f'<linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{color}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="{c}">' + ''.join(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in q)}"/>' for q in quads) + '</clipPath>')
    s = ''.join(f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in q)}" fill="url(#{g})" opacity="{op * random.Random(i).uniform(.65, 1):.2f}" filter="url(#s4soft)" style="mix-blend-mode:screen"/>' for i, q in enumerate(quads))
    return d, s, c


def fine_dust(box, n, seed=1, color='#fff4e2', clip=None, density_far=.6):
    """Many tiny motes: sharp pin-points with a faint bloom, plus soft far ones. No sparkles."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    sharp = soft = ''
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        if rnd.random() < density_far:
            soft += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.8, 1.8):.2f}" opacity="{rnd.uniform(.15, .38):.2f}"/>'
        else:
            sharp += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rnd.uniform(.35, .85):.2f}" opacity="{rnd.uniform(.55, .95):.2f}"/>'
    inner = f'<g fill="{color}"><g filter="url(#cl-moteFar)">{soft}</g><g filter="url(#s4mote)">{sharp}</g></g>'
    return f'<g clip-path="url(#{clip})">{inner}</g>' if clip else inner


def wall_shadow(inner, tr, dx=-60, dy=-12, skew=-8, op=.3):
    return f'<g filter="url(#s4sil)" opacity="{op}" style="mix-blend-mode:multiply"><g transform="translate({dx},{dy}) {tr} skewX({skew})">{inner}</g></g>'


# ================================================================ island dressing
def buoy(x, y, r=14, c='#e8735f'):
    return (f'<path d="M {x},{y - r - 30} L {x},{y - r}" stroke="#b9a07a" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'
            f'<path d="M {x - r},{y} A {r},{r} 0 0 0 {x + r},{y}" fill="#000" opacity=".15"/><circle cx="{x - r * .35:.1f}" cy="{y - r * .35:.1f}" r="{r * .25:.1f}" fill="#fff" opacity=".5"/>'
            f'<path d="M {x - r},{y} L {x + r},{y}" stroke="#f4efe6" stroke-width="3"/>')


def net(x, y, w, h, seed=2):
    rnd = random.Random(seed)
    out = f'<path d="M {x},{y} Q {x + w / 2},{y + 18} {x + w},{y}" stroke="#b9a07a" stroke-width="3" fill="none"/>'
    for i in range(9):
        t = i / 8
        out += f'<path d="M {x + w * t:.0f},{y + 6 * math.sin(t * math.pi):.0f} Q {x + w * t + rnd.uniform(-10, 10):.0f},{y + h * .6:.0f} {x + w * (.3 + t * .4):.0f},{y + h}" stroke="#d8c8a6" stroke-width="1.2" fill="none" opacity=".75"/>'
    for j in range(1, 6):
        yy = y + h * j / 6
        out += f'<path d="M {x + w * j * .04:.0f},{yy:.0f} Q {x + w / 2},{yy + 10:.0f} {x + w * (1 - j * .04):.0f},{yy:.0f}" stroke="#d8c8a6" stroke-width="1.2" fill="none" opacity=".7"/>'
    out += ''.join(f'<path d="M {sx},{sy} q 6,-10 12,0 q -6,4 -12,0 Z" fill="#f6eadb"/>' for sx, sy in ((x + w * .3, y + h * .5), (x + w * .6, y + h * .35), (x + w * .48, y + h * .75)))
    return out


def shell_chime(x, y, n=5, length=70):
    out = f'<rect x="{x - 26}" y="{y}" width="52" height="7" rx="3" fill="#a07a58"/>'
    for i in range(n):
        sx = x - 22 + i * 11
        L = length * (.6 + .4 * math.sin(i * 1.7) ** 2)
        out += f'<path d="M {sx},{y + 7} L {sx},{y + L:.0f}" stroke="#d8c8a6" stroke-width="1"/>'
        out += f'<path d="M {sx - 5},{y + L:.0f} C {sx - 5},{y + L - 10:.0f} {sx + 5},{y + L - 10:.0f} {sx + 5},{y + L:.0f} L {sx},{y + L + 9:.0f} Z" fill="#f6eadb"/>'
    return out


def lifebuoy(x, y, r=34):
    return (f'<g transform="translate({x},{y})"><circle r="{r}" fill="#e2574c"/><circle r="{r * .5:.0f}" fill="#7d553c"/>'
            + ''.join(f'<path d="M {r * math.cos(a):.1f},{r * math.sin(a):.1f} A {r},{r} 0 0 1 {r * math.cos(a + .6):.1f},{r * math.sin(a + .6):.1f} L {r * .5 * math.cos(a + .6):.1f},{r * .5 * math.sin(a + .6):.1f} A {r * .5},{r * .5} 0 0 0 {r * .5 * math.cos(a):.1f},{r * .5 * math.sin(a):.1f} Z" fill="#f4efe6"/>' for a in (0, math.pi / 2, math.pi, 3 * math.pi / 2))
            + f'<circle r="{r}" fill="none" stroke="#b9a07a" stroke-width="2" stroke-dasharray="6 5"/></g>')


def driftwood_sign(x, y, w, text, sub='', rot=-3, color='#2a7f86'):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><path d="M 0,6 C 10,-4 {w - 10},-2 {w},6 L {w - 4},{46} C {w * .6:.0f},52 {w * .3:.0f},50 4,46 Z" fill="#c9b08a"/>'
            f'<path d="M 6,14 C {w * .4:.0f},10 {w * .7:.0f},16 {w - 8},12" stroke="#a88c66" stroke-width="1.5" fill="none"/>'
            f'<text x="{w / 2:.0f}" y="{30 if sub else 34}" {TH} font-size="15" font-weight="800" fill="{color}" text-anchor="middle">{text}</text>'
            + (f'<text x="{w / 2:.0f}" y="42" {EN} font-size="9" font-weight="700" fill="#5e4a3a" text-anchor="middle">{sub}</text>' if sub else '') + '</g>')


def flipflops_rack(x, y):
    cols = ['#2fb3b8', '#e8735f', '#3d6fb0', '#e88aa8', '#7fb07a']
    out = f'<rect x="{x}" y="{y}" width="110" height="5" fill="#7d553c"/>'
    for i, c in enumerate(cols):
        fx = x + 6 + i * 21
        out += f'<path d="M {fx},{y + 6} L {fx + 14},{y + 6} L {fx + 13},{y + 46} C {fx + 13},{y + 52} {fx + 1},{y + 52} {fx + 1},{y + 46} Z" fill="{c}"/><path d="M {fx + 3},{y + 14} L {fx + 7},{y + 22} L {fx + 11},{y + 14}" stroke="#f4efe6" stroke-width="2" fill="none"/>'
    return out


def coconut(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="-16" rx="18" ry="16" fill="#6f8a4a"/><path d="M -18,-16 C -18,-30 18,-30 18,-16" fill="#86a65a"/>'
            '<ellipse cx="0" cy="-30" rx="8" ry="3" fill="#f2eee6"/><path d="M 2,-30 L 10,-58" stroke="#e8735f" stroke-width="3"/><path d="M 8,-56 l 6,-4" stroke="#e8735f" stroke-width="3"/></g>')


# ================================================================ Odd Hours graphics (own look, not the reference's)
EYE = ('<g transform="translate(506,36)" opacity=".85"><path d="M -13,0 Q 0,-10 13,0 Q 0,10 -13,0 Z" fill="none" stroke="#b18cff" stroke-width="2"/>'
       '<circle cx="0" cy="0" r="4" fill="#b18cff"/></g>')


def tag(text, x=20, y=22):
    w = 26 + len(text) * 8.4
    return (f'<g {TH}><rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#120e1c" fill-opacity=".82" stroke="#9a86ff" stroke-opacity=".8"/>'
            f'<circle cx="{x + 15}" cy="{y + 15}" r="4.5" fill="#9a86ff"/><text x="{x + 26}" y="{y + 20}" font-size="13" font-weight="600" fill="#f2eefa">{text}</text></g>')


def step(n, title, sub, y=66):
    return (f'<g {TH}><rect x="26" y="{y + 5}" width="488" height="74" rx="14" fill="#120e1c" opacity=".35"/>'
            f'<rect x="22" y="{y}" width="488" height="74" rx="14" fill="#f8f3ea"/><rect x="22" y="{y}" width="8" height="74" rx="4" fill="#9a86ff"/>'
            f'<rect x="44" y="{y + 13}" width="48" height="48" rx="12" fill="#7a5ab8"/><text x="68" y="{y + 47}" font-size="26" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>'
            f'<text x="108" y="{y + 38}" font-size="23" font-weight="800" fill="#1d1626">{title}</text>'
            f'<text x="108" y="{y + 60}" {EN} font-size="11" font-weight="700" fill="#8a7fa0" letter-spacing=".8">{sub}</text></g>')


def callout(x, y, text, px, py, w=None, color='#c4463d'):
    w = w or 24 + len(text) * 13
    return (f'<g {TH}><path d="M {x + w / 2:.0f},{y + 40} Q {(x + w / 2 + px) / 2:.0f},{y + 60} {px},{py}" stroke="#ffffff" stroke-width="3" stroke-dasharray="6 5" fill="none"/>'
            f'<circle cx="{px}" cy="{py}" r="5" fill="#ffffff"/><circle cx="{px}" cy="{py}" r="11" fill="none" stroke="#ffffff" stroke-opacity=".6"/>'
            f'<rect x="{x}" y="{y}" width="{w:.0f}" height="40" rx="10" fill="{color}"/><text x="{x + w / 2:.0f}" y="{y + 27}" font-size="16" font-weight="800" fill="#fff" text-anchor="middle">{text}</text></g>')


def subs(th, en, y=712):
    th = [l for l in th.split('/') if l.strip()]
    en = [l for l in en.split('/') if l.strip()]
    h = len(th) * 26 + 6 + len(en) * 17
    top = y - h / 2
    out = f'<g {TH} font-weight="700" font-size="20" text-anchor="middle" fill="#ffd84a" stroke="#0b0812" stroke-width="5" stroke-linejoin="round" paint-order="stroke">'
    out += ''.join(f'<text x="270" y="{top + 19 + i * 26:.0f}">{l.strip()}</text>' for i, l in enumerate(th))
    out += f'</g><g {EN} font-weight="500" font-size="13" text-anchor="middle" fill="#ffffff" stroke="#0b0812" stroke-width="4" stroke-linejoin="round" paint-order="stroke">'
    out += ''.join(f'<text x="270" y="{top + len(th) * 26 + 18 + i * 17:.0f}">{l.strip()}</text>' for i, l in enumerate(en))
    return out + '</g>'


DEFS = ('<filter id="s4soft" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>'
        '<filter id="s4dof" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.2"/></filter>'
        '<filter id="s4dof2" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="2.4"/></filter>'
        '<filter id="s4mote" x="-400%" y="-400%" width="900%" height="900%"><feGaussianBlur stdDeviation=".35" result="a"/><feGaussianBlur in="SourceGraphic" stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="a"/></feMerge></filter>'
        '<filter id="s4sil" x="-20%" y="-20%" width="140%" height="140%"><feFlood flood-color="#2e1c2a"/><feComposite in2="SourceAlpha" operator="in"/><feGaussianBlur stdDeviation="6"/></filter>'
        '<radialGradient id="s4bulb"><stop offset="0" stop-color="#fff2d0" stop-opacity=".9"/><stop offset="1" stop-color="#ffcf96" stop-opacity="0"/></radialGradient>')


def char(fid, inner, tr, light_pt, at, rig, face):
    return CL.character(uid(f'{fid}c'), inner, CL.aim(at, light_pt), rig, transform=tr, heads=[(face, '')] if face else [], prefix=fid)


def sun_now(head='smirk'):
    return R.tanify(ISL['SUN_ISLAND']) + f'<use href="#{R.HEADS[head]}_t"/>' + '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'


def sun_then(head='dead', **kw):
    return R.body(head=head, **kw)


def compose(fid, rig, bg, shadow, chars, fg, light, atmos, ui, defs):
    return CL.compose(rig, bg=bg, shadow=shadow, chars=''.join(c[1] for c in chars) + fg, light=light, atmos=atmos, ui=ui + EYE,
                      extra_defs=DEFS + defs + ''.join(c[0] for c in chars), prefix=fid, label=fid)


# ================================================================ 1. island wooden shop (moderate light)
def shop():
    fid = 'W1'
    wall = wood_planks(0, 0, 540, 640, '#9c6e52', '#ad7f60', '#8a5e44', seed=2)
    ceiling = '<rect x="0" y="0" width="540" height="64" fill="#5e3e2c"/>' + ''.join(f'<rect x="{x}" y="0" width="20" height="74" fill="#4e3224"/>' for x in (60, 280, 480))
    win = ('<rect x="300" y="190" width="200" height="200" fill="#ffd9b8"/><rect x="300" y="300" width="200" height="90" fill="#6fb2c2"/><path d="M 300,300 L 500,300 L 500,306 L 300,308 Z" fill="#ffe8cc"/>'
           + K.longtail(390, 330, .28) + '<path d="M 300,300 C 340,286 380,290 420,296 L 300,300 Z" fill="#6f9a7a"/>'
           '<rect x="290" y="180" width="220" height="10" fill="#5e3e2c"/><rect x="290" y="390" width="220" height="14" fill="#5e3e2c"/>'
           '<rect x="290" y="180" width="10" height="220" fill="#5e3e2c"/><rect x="500" y="180" width="10" height="220" fill="#5e3e2c"/><rect x="396" y="190" width="8" height="200" fill="#5e3e2c"/>'
           '<path d="M 510,184 L 536,194 L 536,394 L 510,404 Z" fill="#7d553c"/>' + ''.join(f'<path d="M 512,{204 + k * 16} L 534,{200 + k * 16}" stroke="#5e3e2c" stroke-width="3"/>' for k in range(12)))
    shelves = ''
    rnd = random.Random(7)
    for sy in (300, 420):
        shelves += f'<rect x="-10" y="{sy}" width="250" height="9" fill="#6e4a34"/>'
        x = 4
        while x < 230:
            if rnd.random() < .5:
                w, h = 24, rnd.randint(32, 44)
                shelves += jar(x, sy - h, w, h, rnd.choice(['#e88aa8', '#f0b46a', '#7fb07a', '#d8655a', '#c9a2e0']), rnd.choice(['#d8655a', '#2fb3b8', '#3d6fb0']))
                x += w + 6
            else:
                w, h = 20, 28
                shelves += f'<rect x="{x}" y="{sy - h}" width="{w}" height="{h}" rx="3" fill="{rnd.choice(["#d8655a", "#2f6fb5", "#e8a43a", "#3fa06a"])}"/><rect x="{x}" y="{sy - h + 7}" width="{w}" height="6" fill="#fff" opacity=".7"/>'
                x += w + 4
    island = (net(20, 470, 200, 120, 3) + buoy(60, 520, 13, '#e8735f') + buoy(120, 540, 11, '#2fb3b8') + buoy(176, 516, 12, '#f4efe6')
              + shell_chime(450, 64, 5, 90) + flipflops_rack(330, 440)
              + driftwood_sign(70, 130, 150, 'ร้านป้าแดง', 'SINCE 2529', -2, '#b0463c'))
    back = f'<g filter="url(#s4dof)">{wall}{ceiling}{win}{shelves}{island}</g>'
    bulb = '<path d="M 200,64 L 200,112" stroke="#2a1c18" stroke-width="2"/><path d="M 184,112 L 216,112 L 208,98 L 192,98 Z" fill="#2f8f94"/><circle cx="200" cy="120" r="6" fill="#fff4dc"/><circle cx="200" cy="120" r="40" fill="url(#s4bulb)" style="mix-blend-mode:screen"/>'
    bd, bs, bc = beam_set(fid, [[(306 + k * 24, 196), (324 + k * 24, 196), (190 + k * 24, 900), (170 + k * 24, 900)] for k in range(7)], op=.26)
    counter = (wood_planks(-10, 640, 560, 26, '#b8865f', '#c99872', '#a07250', 560, 5, vertical=False) + '<rect x="-10" y="664" width="560" height="10" fill="#4e3224" opacity=".7"/>'
               + wood_planks(-10, 674, 560, 300, '#7d553c', '#8a6246', '#6e4a34', 60, 9) + '<rect x="-10" y="674" width="560" height="22" fill="#2e1a12" opacity=".35"/>')
    goods = (jar(26, 582, 44, 60, '#f0b46a', '#d8655a') + jar(78, 596, 38, 46, '#e88aa8', '#2fb3b8')
             + '<g transform="translate(150,640)">' + ''.join(f'<path d="M {k * 12 - 22},0 C {k * 12 - 30},-34 {k * 12 - 8},-48 {k * 12 + 4},-44" stroke="#e8c35e" stroke-width="10" fill="none" stroke-linecap="round"/>' for k in range(5)) + '</g>'
             + coconut(230, 640, 1.0) + coconut(262, 642, .85)
             + '<g transform="translate(330,640)"><rect x="-30" y="-56" width="60" height="56" rx="6" fill="#2f6fb5"/><rect x="-30" y="-56" width="60" height="14" rx="5" fill="#2c5a96"/>'
             f'<text x="0" y="-18" {TH} font-size="11" font-weight="800" fill="#fff" text-anchor="middle">น้ำแข็ง</text></g>')
    aunt_in = ISL['AUNT_BODY'] + '<use href="#h_aunt"/>'
    sun_in = sun_then('annoy', tote=True, camera=False)
    a_tr, s_tr = 'translate(230,250) scale(1.5)', 'translate(462,392) scale(1.62)'
    sh = wall_shadow(aunt_in, a_tr, -70, -18, op=.3)
    chars = [char(fid, aunt_in, a_tr, (400, 260), (230, 400), 'warm', 'tawan')]
    sun = char(fid, sun_in, s_tr, (400, 260), (462, 560), 'warm', 'sun')
    light = bs + bulb + CL.glow(400, 290, 220, '#ffd9a8', .24, core=False) + fine_dust((150, 190, 540, 900), 260, 4, clip=bc) + fine_dust((0, 80, 540, 900), 50, 9)
    ui = (tag('ปีแรกบนเกาะ') + step(1, 'ของบนเกาะแพงกว่าฝั่ง', 'EVERYTHING ARRIVES BY BOAT') + callout(30, 770, 'ค่าเรือรวมอยู่ในราคา', 160, 652)
          + subs('ของบางอย่างแพงกว่าฝั่งนิดหน่อย/เพราะค่าเรือรวมอยู่ในนั้นแล้ว', 'Some things cost a bit more here,/the boat ride is in the price.'))
    return compose(fid, 'warm', back, sh, chars, counter + goods + sun[1], light, '', ui, bd + sun[0])


# ================================================================ 2. hillside bungalow, first night (dim)
def bungalow():
    fid = 'W2'
    wall = wood_planks(0, 0, 540, 660, '#6e5042', '#7a5a4a', '#5e4436', 52, seed=4)
    win = ('<rect x="40" y="150" width="210" height="230" fill="#1e2a4a"/><circle cx="190" cy="200" r="16" fill="#f4efe4"/><circle cx="196" cy="196" r="14" fill="#1e2a4a"/>'
           '<rect x="40" y="300" width="210" height="80" fill="#152036"/>' + ''.join(f'<circle cx="{x}" cy="300" r="2.4" fill="#e0f4ff"/><circle cx="{x}" cy="300" r="8" fill="#e0f4ff" opacity=".22"/>' for x in (60, 92, 126, 160, 200, 232))
           + '<path d="M 40,318 C 100,300 170,322 250,306 L 250,380 L 40,380 Z" fill="#24382e"/>'
           '<rect x="30" y="140" width="230" height="10" fill="#3e2c22"/><rect x="30" y="380" width="230" height="14" fill="#3e2c22"/><rect x="30" y="140" width="10" height="250" fill="#3e2c22"/><rect x="250" y="140" width="10" height="250" fill="#3e2c22"/>'
           '<rect x="142" y="150" width="8" height="230" fill="#3e2c22"/>')
    island = (shell_chime(220, 40, 6, 100) + net(300, 120, 220, 130, 5) + buoy(340, 170, 12, '#e8735f') + buoy(420, 190, 13, '#2fb3b8') + buoy(480, 168, 11, '#f4efe6')
              + '<g transform="translate(330,300)"><rect x="-4" y="-4" width="128" height="88" fill="#3e2c22"/><rect x="0" y="0" width="120" height="80" fill="#2fb3b8"/>'
              '<path d="M 0,50 q 30,-14 60,0 q 30,14 60,0 L 120,80 L 0,80 Z" fill="#1f6f8e"/>' f'<text x="60" y="32" {EN} font-size="16" font-weight="800" fill="#fff" text-anchor="middle">KOH TAO</text></g>'
              '<rect x="300" y="430" width="200" height="8" fill="#a88c66"/><path d="M 300,438 C 340,446 460,446 500,438" stroke="#8a7050" stroke-width="3" fill="none"/>'
              + ''.join(f'<path d="M {x},430 q 6,-12 12,0 q -6,4 -12,0 Z" fill="#f6eadb"/>' for x in (318, 352, 410, 470)) + coconut(440, 430, .7))
    gecko = f'<g transform="translate(470,90) rotate(-30) scale(.26)">{ISL["GECKO"]}</g>'
    back = f'<g filter="url(#s4dof)">{wall}{win}{island}</g>' + gecko
    floor = wood_planks(0, 660, 540, 300, '#5a4034', '#664a3c', '#4e382e', 64, 6, vertical=False)
    bed = ('<path d="M -10,640 L 380,640 L 380,780 L -10,780 Z" fill="#4e382e"/><rect x="-10" y="600" width="390" height="60" rx="8" fill="#e8e4ea"/>'
           '<path d="M -14,620 C 100,598 260,606 384,596 L 384,700 C 260,710 100,708 -10,712 Z" fill="#6f9fb4"/><path d="M -14,620 C 100,598 260,606 384,596 L 384,616 C 260,624 100,626 -10,636 Z" fill="#8fb8c8"/>'
           '<path d="M 180,0 C 100,220 30,440 -10,620 L 384,620 C 340,440 260,220 180,0 Z" fill="#eef2f8" opacity=".12"/>'
           + ''.join(f'<path d="M 180,0 C {170 - k * 26},240 {130 - k * 34},450 {120 - k * 34},620" stroke="#eef2f8" stroke-width="1.3" fill="none" opacity=".3"/>' for k in range(-5, 5)))
    lamp = ('<g transform="translate(440,640)"><rect x="-40" y="-6" width="80" height="140" fill="#3e2c22"/><rect x="-44" y="-12" width="88" height="10" fill="#5e4436"/>'
            '<path d="M -18,-70 L 18,-70 L 26,-36 L -26,-36 Z" fill="#f2dcb8"/><rect x="-3" y="-36" width="6" height="26" fill="#8a6a50"/><ellipse cx="0" cy="-10" rx="16" ry="5" fill="#8a6a50"/>'
            '<g transform="translate(-26,-20)"><rect x="-8" y="-18" width="16" height="18" rx="2" fill="#2f8f94"/></g></g>')
    flops = '<g transform="translate(470,860)"><path d="M -30,0 L -6,0 L -8,40 L -28,40 Z" fill="#2fb3b8"/><path d="M 6,6 L 30,6 L 28,46 L 8,46 Z" fill="#2fb3b8" transform="rotate(10)"/></g>'
    sun_in = sun_then('dead', tote=False, camera=False)
    s_tr = 'translate(196,330) scale(1.42)'
    md, ms, mc = beam_set(fid, [[(48 + k * 30, 150), (68 + k * 30, 150), (210 + k * 30, 900), (186 + k * 30, 900)] for k in range(7)], '#b8ccff', .16)
    light = (CL.falloff(440, 580, 520, .55) + CL.glow(440, 590, 230, '#ffd29a', .4) + ms + CL.glow(150, 260, 170, '#9fb8ff', .14, core=False)
             + fine_dust((40, 150, 420, 900), 180, 6, '#dfe8ff', clip=mc) + fine_dust((300, 420, 540, 760), 70, 11, '#fff0d8'))
    sh = wall_shadow(sun_in, s_tr, 80, -30, 10, op=.34)
    chars = [char(fid, sun_in, s_tr, (440, 580), (196, 480), 'moon', 'sun')]
    ui = (tag('คืนแรกในบ้านเช่า') + callout(330, 30, 'รูมเมทคนแรก', 470, 104, 150, '#7a5ab8')
          + subs('รูมเมทคนแรก/มาเองไม่ต้องหา', 'The first roommate/moved in on its own.'))
    return compose(fid, 'moon', back, sh, chars, bed + lamp + flops, light, '', ui, md)


# ================================================================ 3. street above Mae Haad, morning (soft dappled light)
def street():
    fid = 'W3'
    sky = '<rect width="540" height="420" fill="#9ccbea"/><rect y="220" width="540" height="200" fill="#d6ecf4"/>' + cumulus(140, 120, .9) + cumulus(430, 90, .6)
    sea = '<rect x="0" y="330" width="540" height="70" fill="#5fb8c8"/><path d="M 0,330 L 540,324 L 540,332 L 0,336 Z" fill="#a9e0e4"/>' + K.longtail(120, 360, .26) + K.longtail(330, 352, .2, '#7fd3d6')
    hill = '<path d="M -20,400 C 80,330 200,320 300,350 C 380,372 460,340 560,320 L 560,420 L -20,420 Z" fill="#6aa477"/>' + palm(60, 410, .55) + palm(480, 404, .5, True, 1)
    shopfront = (f'<rect x="0" y="230" width="540" height="430" fill="#f2ebe0"/><rect x="0" y="230" width="540" height="14" fill="#cfc6b8"/>'
                 '<rect x="20" y="300" width="230" height="300" fill="#4a3c36"/><rect x="290" y="300" width="230" height="300" fill="#4a3c36"/>'
                 + ''.join(tank_row(30 + i * 30, 590) for i in range(7))
                 + ''.join(K.wetsuit(318 + i * 34, 330, ['#1f2b46', '#2c3a54', '#3a2a40'][i % 3], ['#2fb3b8', '#e8735f', '#e88aa8'][i % 3]) for i in range(6))
                 + '<path d="M 0,276 L 540,276 L 528,300 L 12,300 Z" fill="#2fb3b8"/>' + ''.join(f'<path d="M {12 + k * 24},300 l 12,10 l 12,-10" fill="#2fb3b8"/>' for k in range(22))
                 + '<rect x="120" y="244" width="300" height="30" rx="4" fill="#1d2a3d"/>' + f'<text x="270" y="266" {EN} font-size="18" font-weight="800" fill="#fff" text-anchor="middle">TAO REEF DIVERS · ดำน้ำ</text>'
                 + lifebuoy(470, 360, 28) + flipflops_rack(30, 330) + buoy(250, 330, 12) + buoy(272, 344, 10, '#2fb3b8'))
    wires = ''.join(f'<path d="M -10,{150 + i * 7} Q 270,{210 + i * 9} 560,{120 + i * 6}" stroke="#2a2c34" stroke-width="{1.7 - i * .2:.1f}" fill="none" opacity=".85"/>' for i in range(5))
    pole = '<rect x="500" y="0" width="16" height="640" fill="#b9b4ae"/><rect x="500" y="0" width="6" height="640" fill="#d6d1ca"/><rect x="470" y="130" width="76" height="8" fill="#8a857e"/>'
    bouga = K.bougainvillea(-20, 200, 140, 90, 4) + K.bougainvillea(420, 210, 140, 70, 8)
    back = f'<g filter="url(#s4dof2)">{sky}{sea}{hill}</g><g filter="url(#s4dof)">{shopfront}{bouga}</g>' + wires + pole
    road = '<rect y="640" width="540" height="320" fill="#c9c2b6"/><path d="M 0,640 L 540,640" stroke="#a69e94" stroke-width="5"/><rect y="640" width="540" height="40" fill="#d8d2c6"/>'
    scoot = K.scooter(380, 830, 2.0, '#2fb3b8', True)
    dog_tr = 'translate(110,760) scale(.62)'
    sun_in = sun_now('smirk')
    s_tr = 'translate(250,330) scale(1.38)'
    leaves = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .45:.0f}" fill="#fff6e4" opacity=".28" filter="url(#s4soft)" style="mix-blend-mode:screen"/>' for x, y, rx in ((90, 700, 50), (230, 760, 60), (420, 720, 44), (330, 880, 56), (60, 900, 40)))
    bd, bs, bc = beam_set(fid, [[(380 + k * 36, 0), (404 + k * 36, 0), (120 + k * 36, 960), (96 + k * 36, 960)] for k in range(5)], '#fff6e4', .14)
    light = bs + leaves + CL.glow(560, -40, 380, '#fff6e4', .22, core=False) + fine_dust((60, 0, 540, 960), 180, 12, '#fffaf0', clip=bc)
    chars = [char(fid, ISL['DOG'], dog_tr, (560, -40), (110, 840), 'warm', None), char(fid, sun_in, s_tr, (560, -40), (250, 500), 'warm', 'sun')]
    sh = CL.contact_shadow(250, 1006, 80) + CL.contact_shadow(110, 870, 60, 10)
    ui = (tag('ปัจจุบัน · เกาะเต่า') + subs('ผู้ชายคนนี้ชื่อซัน/ครูสอนดำน้ำบนเกาะเต่า', 'This is Sun,/a dive instructor on Koh Tao.'))
    return compose(fid, 'warm', back + road, sh, chars, scoot, light, '', ui, bd)


def tank_row(x, y):
    return K.tank(x, y, '#9aa6b8' if (x // 30) % 2 else '#b9c2d0', 1.0)


# ================================================================ 4. Mae Haad pier, moving day (bright midday, but held back)
def pier():
    fid = 'W4'
    sky = '<rect width="540" height="430" fill="#8ec4e8"/><rect y="250" width="540" height="180" fill="#d6ecf4"/>' + cumulus(120, 110, 1) + cumulus(420, 160, .7)
    sea = '<rect y="400" width="540" height="300" fill="#3fb0c4"/><rect y="400" width="540" height="40" fill="#2a8fb4"/>' + ''.join(f'<path d="M {x},{y} q 12,-4 24,0" stroke="#fff" stroke-opacity=".55" stroke-width="2" fill="none"/>' for x, y in ((30, 460), (150, 480), (400, 450), (470, 500), (90, 540)))
    island = '<path d="M 300,402 C 340,360 400,340 460,346 C 500,350 530,370 560,384 L 560,404 L 300,404 Z" fill="#6aa477"/>'
    ferry = f'<g transform="translate(420,420) scale(.9)">{K.ferry(0, 0, 1)}</g>'
    back = f'<g filter="url(#s4dof2)">{sky}{island}</g>' + sea + f'<g filter="url(#s4dof)">{ferry}{K.longtail(90, 470, .55)}</g>'
    deck = wood_planks(-10, 640, 560, 330, '#b89a7a', '#c8aa88', '#a68866', 34, 3, vertical=False) + '<rect x="-10" y="634" width="560" height="10" fill="#7d6450"/>'
    posts = ''.join(f'<rect x="{x}" y="560" width="22" height="90" rx="4" fill="#7d553c"/><rect x="{x}" y="560" width="8" height="90" fill="#9a6c4c"/>' for x in (30, 500))
    rope = '<path d="M 41,580 C 120,620 200,620 260,600" stroke="#c9b08a" stroke-width="5" fill="none"/>' + buoy(150, 616, 14, '#e8735f') + buoy(200, 612, 12, '#f4efe6')
    boxes = (K.cardboard(320, 650, 120, 90, 'ครัว') + K.cardboard(440, 670, 90, 70) + K.cardboard(330, 560, 100, 90, 'มีด') + K.cardboard(430, 590, 80, 80)
             + '<g transform="translate(380,560)"><rect x="-30" y="-64" width="60" height="64" rx="6" fill="#eef0f4"/><circle cx="0" cy="-34" r="20" fill="#c9ced8"/><circle cx="0" cy="-34" r="6" fill="#5e6270"/></g>'
             + '<g transform="translate(468,590)"><rect x="-28" y="-40" width="56" height="40" rx="12" fill="#f4efe6"/><rect x="-28" y="-40" width="56" height="12" rx="6" fill="#d6d0c4"/></g>'
             + '<g transform="translate(400,500)"><ellipse cx="0" cy="0" rx="44" ry="10" fill="#2a2c34"/><path d="M 40,0 L 84,-10" stroke="#2a2c34" stroke-width="6"/></g>')
    sun_in = sun_then('dead', tote=True, camera=True)
    s_tr = 'translate(170,330) scale(1.4)'
    uncle_tr = 'translate(30,420) scale(1.0)'
    uncle_in = ISL['UNCLE_BODY'] + '<use href="#h_uncle"/>'
    spray = fine_dust((0, 380, 540, 700), 120, 21, '#ffffff', density_far=.75)
    light = CL.glow(-40, -40, 420, '#fffaf0', .2, core=False) + spray
    chars = [char(fid, uncle_in, uncle_tr, (-40, -40), (30, 560), 'warm', None), char(fid, sun_in, s_tr, (-40, -40), (170, 500), 'warm', 'sun')]
    sh = CL.contact_shadow(170, 1006, 80) + K.castsh(boxes, 12, 10, .3)
    ui = (tag('สองปีก่อน · ท่าเรือแม่หาด') + callout(300, 400, 'ขนทั้งชีวิตลงเรือ', 400, 560, 180, '#7a5ab8')
          + subs('เกาะเต่าไม่มีสนามบิน/ย้ายบ้านทีต้องขนทั้งชีวิตลงเรือ', 'No airport on Koh Tao:/moving house means shipping your whole life.'))
    return compose(fid, 'warm', back, sh, chars, deck + posts + rope + boxes, light, '', ui, '')


# ================================================================ 5. dive centre (open front, bright beach behind, cool shade inside)
def dive():
    fid = 'W5'
    view = ('<rect x="0" y="120" width="540" height="300" fill="#a8d8ee"/>' + cumulus(380, 190, .6)
            + '<rect x="0" y="320" width="540" height="70" fill="#3fb4c6"/><rect x="0" y="380" width="540" height="40" fill="#f2ece2"/>' + K.longtail(160, 350, .3) + palm(60, 400, .45) + palm(490, 400, .4, True))
    wall_l = wood_planks(0, 0, 150, 660, '#8a6a52', '#9a7860', '#7a5c46', 50, 12)
    wall_r = wood_planks(390, 0, 150, 660, '#7d5e48', '#8a6a52', '#6e5240', 50, 13)
    roof = '<rect x="0" y="0" width="540" height="120" fill="#6e4a34"/>' + ''.join(f'<path d="M {x},90 L {x + 18},90 L {x + 12},{136 + (x % 3) * 6} L {x + 4},{130 + (x % 3) * 6} Z" fill="{["#8f6a4a", "#a37c58", "#b58d68"][x % 3]}"/>' for x in range(-10, 560, 16))
    gear = (''.join(K.tank(20 + i * 26, 640, ['#9aa6b8', '#b9c2d0'][i % 2], 1.0) for i in range(5)) + '<rect x="0" y="560" width="150" height="8" fill="#5e3e2c"/>'
            + ''.join(K.wetsuit(410 + i * 30, 170, ['#1f2b46', '#2c3a54', '#3a2a40', '#1f2b46'][i], ['#2fb3b8', '#e8735f', '#e88aa8', '#7fd3d6'][i]) for i in range(4))
            + '<rect x="396" y="164" width="140" height="5" fill="#9aa1a8"/>' + lifebuoy(70, 220, 36) + net(10, 300, 130, 90, 7) + buoy(40, 330, 11, '#e8735f') + buoy(100, 350, 12, '#2fb3b8')
            + '<g transform="translate(400,330)"><rect x="0" y="0" width="130" height="150" rx="6" fill="#f6f2ea" stroke="#5e3e2c" stroke-width="5"/>'
            f'<text x="65" y="24" {TH} font-size="14" font-weight="800" fill="#1d1626" text-anchor="middle">จุดดำน้ำวันนี้</text>'
            + ''.join(f'<circle cx="18" cy="{48 + k * 24}" r="5" fill="{c}"/><text x="30" y="{53 + k * 24}" {EN} font-size="11" font-weight="700" fill="#4a4458">{t}</text>' for k, (t, c) in enumerate((('Chumphon Pin.', '#e8735f'), ('Twins', '#2fb3b8'), ('Japanese Gdn.', '#7a5ab8'), ('Shark Island', '#3d6fb0'))))
            + '</g>' + shell_chime(270, 120, 6, 70))
    back = f'<g filter="url(#s4dof2)">{view}</g><g filter="url(#s4dof)">{wall_l}{wall_r}{gear}</g>' + roof
    floor = wood_planks(0, 660, 540, 300, '#b8957a', '#c4a083', '#a8876c', 50, 14, vertical=False)
    bench = (wood_planks(-10, 640, 560, 24, '#a8835f', '#b8936c', '#94704e', 560, 15, vertical=False) + wood_planks(-10, 664, 560, 300, '#7d5e48', '#8a6a52', '#6e5240', 60, 16)
             + '<g transform="translate(90,640)"><rect x="-40" y="-26" width="80" height="26" rx="8" fill="#22303f"/><rect x="-34" y="-22" width="68" height="16" rx="6" fill="#9ad7e3"/></g>'
             + '<g transform="translate(450,640)"><path d="M -40,0 L 0,0 L 6,-60 L -46,-60 Z" fill="#2fb3b8"/><path d="M 4,0 L 44,0 L 50,-60 L -2,-60 Z" fill="#e8735f"/></g>'
             + '<g transform="translate(300,640)"><rect x="-26" y="-20" width="52" height="20" rx="3" fill="#2a2c34"/><circle cx="0" cy="-10" r="7" fill="#7fd3d6"/></g>')
    lae_in = ISL['LAE_BODY'] + '<use href="#h_lae"/>'
    sun_in = sun_now('smirktalk')
    l_tr, s_tr = 'translate(170,262) scale(1.45)', 'translate(380,260) scale(1.45)'
    bd, bs, bc = beam_set(fid, [[(150 + k * 50, 136), (176 + k * 50, 136), (240 + k * 50, 900), (210 + k * 50, 900)] for k in range(5)], '#fffaf0', .16)
    light = bs + CL.glow(270, 330, 300, '#ffffff', .2, core=False) + fine_dust((120, 140, 460, 900), 200, 14, '#fffaf0', clip=bc) + fine_dust((0, 140, 540, 640), 40, 15)
    chars = [char(fid, lae_in, l_tr, (270, 330), (170, 420), 'warm', 'tawan'), char(fid, sun_in, s_tr, (270, 330), (380, 420), 'warm', 'sun')]
    ui = (tag('ปัจจุบัน · ร้านดำน้ำหาดทรายรี') + step(2, 'จากเชฟ สู่ครูสอนดำน้ำ', 'FROM THE KITCHEN TO THE REEF')
          + subs('จากเชฟหน้าเตา/กลายเป็นครูพาคนดำลงไปดูปลา', 'From a chef at the stove/to a teacher taking people to see the fish.'))
    return compose(fid, 'warm', back + floor, '', chars, bench, light, '', ui, bd)


# ================================================================ 6. viewpoint over Koh Nang Yuan, dusk
def viewpoint():
    fid = 'W6'
    sky = ('<rect width="540" height="480" fill="#9aa8d6"/><rect y="200" width="540" height="280" fill="#e6c8d2"/><rect y="320" width="540" height="160" fill="#f6dccc"/>'
           '<circle cx="420" cy="380" r="38" fill="#fff0e0"/><circle cx="420" cy="380" r="100" fill="#fff0e0" opacity=".25"/>' + cumulus(130, 170, .8, .7) + cumulus(320, 250, .5, .6))
    sea = '<rect y="430" width="540" height="300" fill="#5f9fbc"/><rect y="430" width="540" height="30" fill="#7fb4c8"/><path d="M 400,432 L 440,432 L 480,620 L 360,620 Z" fill="#fff0e0" opacity=".3"/>'
    ny = ('<g transform="translate(250,560)"><ellipse cx="0" cy="0" rx="230" ry="40" fill="#8fdcd2" opacity=".75"/>'
          '<path d="M -110,0 C -70,-8 -30,-6 0,-3 C 30,-6 70,-8 110,0 C 70,4 30,3 0,2 C -30,3 -70,4 -110,0 Z" fill="#f6eee0"/>'
          '<path d="M -180,2 C -172,-44 -146,-66 -116,-66 C -90,-66 -74,-44 -70,2 Z" fill="#4f8a5e"/><path d="M -180,2 C -172,-44 -146,-66 -116,-66 C -132,-52 -144,-30 -146,2 Z" fill="#6aa477"/>'
          '<path d="M -36,0 C -32,-30 -16,-44 0,-44 C 16,-44 30,-30 34,0 Z" fill="#4f8a5e"/>'
          '<path d="M 80,2 C 86,-38 110,-58 138,-58 C 166,-58 182,-38 188,2 Z" fill="#457c52"/><path d="M 80,2 C 86,-38 110,-58 138,-58 C 118,-46 106,-26 104,2 Z" fill="#5f985e"/>'
          + boulder(-190, 4, 30, 16) + boulder(170, 4, 30, 14, 1) + '</g>')
    back = f'<g filter="url(#s4dof2)">{sky}</g>' + f'<g filter="url(#s4dof)">{sea}{ny}</g>'
    ground = ('<path d="M -20,700 C 120,660 300,650 560,690 L 560,960 L -20,960 Z" fill="#4f7a52"/><path d="M -20,700 C 120,660 300,650 560,690 L 560,720 C 300,690 120,700 -20,736 Z" fill="#6a9a66"/>'
              + ''.join(f'<path d="M {x},{y} q 4,-14 8,0 M {x + 6},{y} q 5,-18 10,0" stroke="#86b07a" stroke-width="2" fill="none"/>' for x, y in ((40, 760), (140, 740), (300, 750), (420, 770), (490, 800), (90, 840))))
    rock = boulder(-60, 1000, 300, 220) + boulder(380, 1000, 220, 160, 1)
    scoot = K.scooter(380, 820, 2.0, '#2fb3b8', True)
    sun_in = sun_now('smirk')
    s_tr = 'translate(200,330) scale(1.4)'
    dog_tr = 'translate(90,720) scale(.6)'
    bd, bs, bc = beam_set(fid, [[(400, 380), (440, 380), (300 - k * 40, 960), (240 - k * 40, 960)] for k in range(4)], '#ffe6cc', .16)
    light = CL.glow(420, 380, 300, '#ffd2b0', .3) + bs + fine_dust((0, 380, 540, 960), 220, 31, '#fff0e0', clip=bc) + fine_dust((0, 300, 540, 900), 50, 32, '#fff0e0')
    chars = [char(fid, sun_in, s_tr, (420, 380), (200, 500), 'dusk', 'sun'), char(fid, ISL['DOG'], dog_tr, (420, 380), (90, 780), 'dusk', None)]
    sh = CL.contact_shadow(200, 1006, 70) + CL.contact_shadow(90, 826, 54, 9)
    ui = (tag('สองปีต่อมา · จุดชมวิวเกาะนางยวน') + subs('วันนี้คลื่นแรง…/ของคงไม่มาอีกแล้ว', 'Rough sea today…/my parcel isn’t coming again.'))
    return compose(fid, 'dusk', back + ground, sh, chars, scoot + rock, light, '', ui, bd)


SHOTS = [
    (street, 'ถนนหน้าร้านดำน้ำ · เช้า (ปัจจุบัน)', 'แสงเช้าลอดใบไม้เป็นดวง ๆ ไม่จ้า · หน้าร้านดำน้ำมีถังอากาศ ชุดดำน้ำ ห่วงชูชีพ ทุ่น ราวรองเท้าแตะ · สายไฟ เฟื่องฟ้า ทะเลกับเรือหางยาวไกล ๆ · ซันผิวแทนกับหมาเกาะ มอเตอร์ไซค์'),
    (pier, 'ท่าเรือแม่หาด · วันย้ายบ้าน (อดีต)', 'แดดกลางวันแต่ไม่ให้จ้าเวอร์ ละอองน้ำทะเลลอย · พื้นไม้ท่าเรือ หลักผูกเรือ เชือก ทุ่น เรือเฟอร์รี่ เรือหางยาว · ลุงรถกระบะ · ซันผิวเดิมกับกองกล่อง พัดลม หม้อหุงข้าว กระทะ'),
    (bungalow, 'บ้านเช่าบนเนิน · คืนแรก (อดีต)', 'มืดสลัว แสงจันทร์ฟ้าเย็นลอดหน้าต่าง โคมอุ่นข้างเตียง · ไฟเรือไดหมึกที่ขอบฟ้า · แหอวน ทุ่น โมบายเปลือกหอย รูป KOH TAO ชั้นไม้ลอยมีเปลือกหอยกับมะพร้าว รองเท้าแตะ มุ้ง · ตุ๊กแกน่ารักตัวเล็ก'),
    (shop, 'ร้านโชห่วยไม้ · ปีแรก (อดีต)', 'แสงพอดีขึ้นกว่าเฟรมทดลอง · เพิ่มแหอวนกับทุ่น โมบายเปลือกหอย ราวรองเท้าแตะ ป้ายไม้ทะเล "ร้านป้าแดง" มะพร้าวบนเคาน์เตอร์ วิวทะเลกับเรือหางยาว'),
    (dive, 'ร้านดำน้ำหาดทรายรี (ปัจจุบัน)', 'ในร้านร่มเย็น ข้างนอกสว่าง · ถังอากาศ ชุดดำน้ำ ห่วงชูชีพ แห ทุ่น กระดานจุดดำน้ำวันนี้ หน้ากาก ตีนกบ โมบายเปลือกหอย · ซันกับเล'),
    (viewpoint, 'จุดชมวิวเกาะนางยวน · เย็น (ปัจจุบัน)', 'แสงเย็นอมชมพูม่วง ไม่ติดเหลือง · เกาะนางยวนสามเกาะกับสันทราย · โขดหิน หญ้า มอเตอร์ไซค์ ซันกับหมา'),
]


def build():
    figs = ''.join(f'<figure>{fn()}<figcaption><span class="n">{i:02d}</span> <b>{t}</b><span class="note">{n}</span></figcaption></figure>' for i, (fn, t, n) in enumerate(SHOTS, 1))
    page = f'''<title>Odd Hours ฉาก EP.01</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: grid of 9:16 frames, 3 across on desktop, 2 on tablet, 1 on phone. Single dark look by choice, like the other Odd Hours boards. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#9a86ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1100px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
@media (max-width:900px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:8px; box-shadow:0 0 0 1px var(--line); overflow:hidden; }}
figcaption {{ display:grid; gap:3px; font-size:13px; line-height:1.55; }} .n {{ font-size:11px; color:var(--accent); }} figcaption b {{ font-weight:500; }}
.note {{ color:var(--muted); font-size:12px; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700;800&family=Inter:wght@500;700;800&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{R.HEAD_DEFS}{ISL["CLIPS"]}{ISL["AUNT_HEAD"]}{ISL["LAE_BACK"]}{ISL["LAE_HEAD"]}{ISL["UNCLE_HEAD"]}</defs></svg>
<div class="wrap">
  <h1>ฉาก EP.01 เกาะเต่า · สไตล์ใหม่<span>ภาพระยะกลาง แสงอุ่นลอดหน้าต่าง ฝุ่นละเอียดในลำแสง ของทะเลในทุกฉาก · กราฟิกแบบ Odd Hours</span></h1>
  <div class="grid">{figs}</div>
</div>
'''
    open(os.path.join(HERE, 'scenes_v4.html'), 'w').write(page)
    print(len(page))


if __name__ == '__main__':
    build()
