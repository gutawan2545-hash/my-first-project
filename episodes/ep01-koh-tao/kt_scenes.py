"""EP.01 Koh Tao locations, third pass: new scenes built from real Koh Tao references
(Mae Haad pier, steep concrete roads with tangled power lines, dive centres, island minimarts,
hillside rental bungalows, the Koh Nang Yuan viewpoint) + new explainer graphics.
Run: python3 kt_scenes.py -> locations.html"""
import os, sys, math, random, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
from scenes import G, RG, castsh, cumulus, palm, boulder

ISL = runpy.run_path(os.path.join(HERE, '..', '..', 'characters', 'islanders_gen.py'))
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'


def blur(c, n=1):
    return f'<g filter="url(#kt-dof{n})">{c}</g>'


def txt(x, y, s, size=12, fill='#1a1626', weight=600, anchor='middle', font=TH, extra=''):
    return f'<text x="{x}" y="{y}" {font} font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'


# ================================================================ props (block-shaded, light from the left unless noted)
def scooter(x, y, s=1.0, body='#d8655a', flip=False):
    f = -1 if flip else 1
    return (f'<g transform="translate({x},{y}) scale({s * f},{s})">'
            '<circle cx="-34" cy="0" r="15" fill="#1d1f26"/><circle cx="-34" cy="0" r="7" fill="#9aa1b0"/>'
            '<circle cx="36" cy="0" r="15" fill="#1d1f26"/><circle cx="36" cy="0" r="7" fill="#9aa1b0"/>'
            f'<path d="M -50,-10 C -48,-28 -30,-34 -6,-32 L 14,-32 L 22,-14 L -10,-12 C -24,-12 -40,-8 -50,-10 Z" fill="{body}"/>'
            '<path d="M -44,-26 C -30,-34 -14,-36 6,-36 L 8,-30 L -40,-22 Z" fill="#2a2c34"/>'
            f'<path d="M 14,-32 L 30,-60 L 38,-58 L 26,-28 L 40,-10 L 22,-6 Z" fill="{body}"/>'
            '<path d="M 26,-62 L 46,-66" stroke="#2a2c34" stroke-width="5" stroke-linecap="round"/>'
            '<rect x="34" y="-60" width="10" height="8" rx="2" fill="#f2eee6"/>'
            '<path d="M 36,-6 L 30,-40" stroke="#5e6270" stroke-width="3"/>'
            '<path d="M -50,-10 L -18,-10" stroke="#ffffff" stroke-opacity=".35" stroke-width="2"/></g>')


def powerpole(x, top, bot):
    return (f'<rect x="{x - 5}" y="{top}" width="10" height="{bot - top}" fill="#b9b4ae"/><rect x="{x - 5}" y="{top}" width="4" height="{bot - top}" fill="#d6d1ca"/>'
            f'<rect x="{x - 34}" y="{top + 18}" width="68" height="6" fill="#8a857e"/><rect x="{x - 26}" y="{top + 44}" width="52" height="5" fill="#8a857e"/>'
            + ''.join(f'<rect x="{x + dx - 3}" y="{top + 10}" width="6" height="9" rx="2" fill="#e9e4dc"/>' for dx in (-28, -10, 10, 28))
            + f'<rect x="{x + 6}" y="{top + 70}" width="22" height="30" rx="3" fill="#5e6270"/><rect x="{x + 8}" y="{top + 104}" width="18" height="16" rx="2" fill="#4a4e5a"/>'
            + f'<path d="M {x - 6},{top + 120} q -18,30 -4,60 q 14,26 -2,50" stroke="#2a2c34" stroke-width="2" fill="none"/>')


def wires(pts, sag=26, n=5, color='#2a2c34'):
    out = ''
    for i in range(n):
        d = f'M {pts[0][0]},{pts[0][1] + i * 6}'
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            d += f' Q {(x0 + x1) / 2},{(y0 + y1) / 2 + sag + i * 4} {x1},{y1 + i * 6}'
        out += f'<path d="{d}" stroke="{color}" stroke-width="{1.6 - i * .15:.2f}" fill="none" opacity=".85"/>'
    return out


def bougainvillea(x, y, w, h, seed=1):
    rnd = random.Random(seed)
    out = ''.join(f'<ellipse cx="{x + rnd.uniform(0, w):.0f}" cy="{y + rnd.uniform(0, h):.0f}" rx="{rnd.uniform(8, 16):.0f}" ry="{rnd.uniform(6, 11):.0f}" fill="{rnd.choice(["#2f6b5a", "#3f8a6e"])}"/>' for _ in range(int(w * h / 260)))
    out += ''.join(f'<circle cx="{x + rnd.uniform(0, w):.0f}" cy="{y + rnd.uniform(0, h):.0f}" r="{rnd.uniform(3, 6):.1f}" fill="{rnd.choice(["#d9478f", "#e86aa6", "#c23a7c"])}"/>' for _ in range(int(w * h / 90)))
    return out


def frangipani(x, y, s=1.0):
    br = (f'<path d="M 0,0 C -4,-40 -30,-60 -46,-90 M 0,-30 C 10,-60 34,-70 44,-96 M -20,-56 C -10,-80 -12,-100 -4,-118" stroke="#8a7462" stroke-width="7" fill="none" stroke-linecap="round"/>')
    leaves = ''.join(f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="9" fill="{c}" transform="rotate({r} {cx} {cy})"/>'
                     for cx, cy, r, c in ((-52, -96, -30, '#3f8a6e'), (-40, -102, 20, '#2f6b5a'), (50, -100, 30, '#3f8a6e'), (38, -106, -20, '#2f6b5a'), (-6, -126, 80, '#3f8a6e'), (6, -122, -60, '#2f6b5a')))
    fl = ''.join(f'<g transform="translate({cx},{cy})">' + ''.join(f'<ellipse cx="0" cy="-4" rx="3" ry="5" fill="#fbf7f0" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288)) + '<circle r="2" fill="#f2c26a"/></g>'
                 for cx, cy in ((-56, -104), (-36, -110), (44, -108), (54, -96), (-2, -132), (10, -128)))
    return f'<g transform="translate({x},{y}) scale({s})">{br}{leaves}{fl}</g>'


def sign(x, y, w, h, lines, bg='#f8f4ec', fg='#1a1626', size=12, font=TH, border=None):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{bg}"' + (f' stroke="{border}" stroke-width="2"' if border else '') + '/>'
    lh = h / (len(lines) + .4)
    for i, (t, c, sz) in enumerate(lines):
        out += txt(x + w / 2, y + lh * (i + .9), t, sz or size, c or fg, 700, font=font)
    return out


def plastic_chair(x, y, c='#d8655a', s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M -14,-40 L 14,-40 L 16,-12 L -16,-12 Z" fill="{c}"/>'
            f'<path d="M -18,-14 L 18,-14 L 20,-8 L -20,-8 Z" fill="{c}"/><path d="M -18,-8 L -20,14 M 18,-8 L 20,14 M -10,-8 L -12,12 M 10,-8 L 12,12" stroke="{c}" stroke-width="4"/>'
            '<path d="M -10,-34 L 10,-34 M -10,-26 L 10,-26" stroke="#ffffff" stroke-opacity=".3" stroke-width="2"/></g>')


def longtail(x, y, s=1.0, ribbon='#e86aa6', hull='#7e5338'):
    return (f'<g transform="translate({x},{y}) scale({s})"><path d="M -80,0 C -50,14 50,14 90,-4 L 104,-30 C 80,-12 34,-8 -70,-8 Z" fill="{hull}"/>'
            '<path d="M -80,0 C -50,14 50,14 90,-4 L 88,2 C 50,18 -50,18 -80,4 Z" fill="#5e3c28"/><path d="M -70,-8 L 80,-12" stroke="#2f6fb5" stroke-width="4"/>'
            f'<path d="M 100,-28 l 8,-12 m -10,10 l 2,-16 m -6,14 l -5,-12" stroke="{ribbon}" stroke-width="3"/><path d="M 98,-26 l 12,-4" stroke="#7fd3d6" stroke-width="3"/><path d="M 96,-24 l 10,6" stroke="#fbf7f0" stroke-width="3"/>'
            '<path d="M -74,-8 L -112,12" stroke="#3c4458" stroke-width="3"/><rect x="-80" y="-24" width="20" height="16" rx="2" fill="#4a4e5a"/>'
            '<rect x="-30" y="-36" width="70" height="6" fill="#f2eee6"/><rect x="-26" y="-30" width="3" height="20" fill="#8a7462"/><rect x="34" y="-30" width="3" height="20" fill="#8a7462"/></g>')


def ferry(x, y, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<path d="M -170,0 L 170,0 L 150,34 L -150,34 Z" fill="#f4f2ee"/><path d="M -170,0 L 170,0 L 166,8 L -166,8 Z" fill="#2fb3b8"/>'
            '<path d="M -150,34 L 150,34 L 146,40 L -146,40 Z" fill="#c9ced8"/>'
            '<path d="M -130,0 L -110,-50 L 120,-50 L 140,0 Z" fill="#ffffff"/><path d="M -110,-50 L -96,-80 L 96,-80 L 110,-50 Z" fill="#eef0f4"/>'
            + ''.join(f'<rect x="{-104 + i * 26}" y="-42" width="20" height="16" rx="3" fill="#3a4b6a"/>' for i in range(9))
            + ''.join(f'<rect x="{-86 + i * 26}" y="-74" width="20" height="14" rx="3" fill="#3a4b6a"/>' for i in range(7))
            + '<rect x="-60" y="-96" width="120" height="16" fill="#e2e5ec"/><path d="M -60,-96 L 60,-96" stroke="#2fb3b8" stroke-width="4"/>'
            + txt(0, -10, 'KOH TAO EXPRESS', 13, '#2a7f86', 800, font=EN) + '</g>')


def pickup_taxi(x, y, s=1.0, c='#3d6fb0'):
    return (f'<g transform="translate({x},{y}) scale({s})">'
            '<circle cx="-50" cy="0" r="16" fill="#1d1f26"/><circle cx="-50" cy="0" r="7" fill="#9aa1b0"/><circle cx="56" cy="0" r="16" fill="#1d1f26"/><circle cx="56" cy="0" r="7" fill="#9aa1b0"/>'
            f'<path d="M -80,-8 L 90,-8 L 90,-34 L 50,-36 L 34,-62 L -6,-62 L -6,-34 L -80,-34 Z" fill="{c}"/>'
            '<path d="M 2,-56 L 30,-56 L 42,-36 L 2,-36 Z" fill="#bfe3ee"/>'
            '<path d="M -86,-34 L -6,-34 L -6,-80 L -86,-80 Z" fill="none" stroke="#5e6270" stroke-width="4"/><rect x="-90" y="-86" width="88" height="8" rx="2" fill="#2fb3b8"/>'
            '<path d="M -80,-34 L -10,-34" stroke="#8a7462" stroke-width="6"/>'
            '<rect x="-20" y="-98" width="40" height="14" rx="3" fill="#f2eee6"/>' + txt(0, -87, 'TAXI', 10, '#1a1626', 800, font=EN)
            + '<path d="M -80,-8 L 90,-8" stroke="#ffffff" stroke-opacity=".3" stroke-width="3"/></g>')


def cardboard(x, y, w, h, label=''):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#c49a6c"/><rect x="{x + w * .62:.0f}" y="{y}" width="{w * .38:.0f}" height="{h}" fill="#a97f55"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="5" fill="#d8b488"/><rect x="{x + w / 2 - 4:.0f}" y="{y}" width="8" height="{h}" fill="#e6d2b0" opacity=".8"/>'
            + (txt(x + w * .32, y + h * .62, label, 9, '#5e3c28', 700) if label else ''))


def tank(x, y, c='#9aa6b8', s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-11" y="-80" width="22" height="80" rx="10" fill="{c}"/><rect x="-11" y="-80" width="8" height="80" rx="5" fill="#ffffff" opacity=".35"/>'
            '<rect x="-5" y="-92" width="10" height="12" rx="2" fill="#2a2c34"/><rect x="-11" y="-30" width="22" height="6" fill="#2fb3b8"/></g>')


def wetsuit(x, y, c='#1f2b46', stripe='#2fb3b8'):
    return (f'<g transform="translate({x},{y})"><path d="M -4,-6 L 4,-6 L 2,4 L -2,4 Z" fill="#5e6270"/><path d="M -16,0 L 16,0 L 22,30 L 14,32 L 14,96 L 2,96 L 0,46 L -2,96 L -14,96 L -14,32 L -22,30 Z" fill="{c}"/>'
            f'<path d="M -16,0 L -8,0 L -10,96 L -14,96 L -14,32 L -22,30 Z" fill="#ffffff" opacity=".08"/><path d="M -20,20 L -12,60 M 20,20 L 12,60" stroke="{stripe}" stroke-width="2.4"/></g>')


# ================================================================ frame scaffold
DEFS = ('<filter id="kt-dof1" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter>'
        '<filter id="kt-dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3"/></filter>'
        '<filter id="sb-sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>'
        '<filter id="sb-dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2"/></filter>'
        '<filter id="sb-dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.4"/></filter>')

NECK = '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'
_n = [0]


def sun_island(fid, tx, ty, s, light, head='smirk', rig='day'):
    _n[0] += 1
    inner = R.tanify(ISL['SUN_ISLAND']) + f'<use href="#{R.HEADS[head]}_t"/>' + NECK
    d = CL.aim((tx, ty + 120 * s), light)
    return CL.character(f'{fid}-s{_n[0]}', inner, d, rig, transform=f'translate({tx},{ty}) scale({s})', heads=[('sun', '')], prefix=fid)


def sun_city(fid, tx, ty, s, light, head='smirk', rig='day', **kw):
    _n[0] += 1
    d = CL.aim((tx, ty + 120 * s), light)
    return CL.character(f'{fid}-s{_n[0]}', R.body(head=head, **kw), d, rig, transform=f'translate({tx},{ty}) scale({s})', heads=[('sun', '')], prefix=fid)


def other(fid, tx, ty, s, light, inner, face='tawan', rig='day'):
    _n[0] += 1
    d = CL.aim((tx, ty + 120 * s), light)
    return CL.character(f'{fid}-o{_n[0]}', inner, d, rig, transform=f'translate({tx},{ty}) scale({s})', heads=[], prefix=fid)


def frame(fid, rig, bg, shadow='', chars=(), fg='', light='', atmos='', defs=''):
    return CL.compose(rig, bg=bg, shadow=shadow, chars=''.join(c[1] for c in chars) + fg, light=light, atmos=atmos,
                      ui='', extra_defs=''.join(c[0] for c in chars) + defs, prefix=fid, label=fid)


# ================================================================ 1. hillside road above Mae Haad, morning
def road():
    fid = 'L1'
    d = G(f'{fid}sky', [(0, '#6eaee0'), (.7, '#cde4f2'), (1, '#eef5f7')]) + G(f'{fid}rd', [(0, '#cfc9c0'), (1, '#b2aaa0')], 0, 0, 0, 1) + G(f'{fid}sea', [(0, '#2a8fbd'), (1, '#6fd0cf')])
    sky = f'<rect width="540" height="420" fill="url(#{fid}sky)"/>' + cumulus(380, 90, .8) + cumulus(120, 150, .6, .9)
    far = (f'<rect x="300" y="250" width="240" height="130" fill="url(#{fid}sea)"/>'
           + ''.join(f'<path d="M {310 + i * 30},{270 + (i % 3) * 30} q 8,-3 16,0" stroke="#fff" stroke-opacity=".5" stroke-width="1.5" fill="none"/>' for i in range(8))
           + longtail(420, 330, .35) + longtail(500, 300, .28, '#7fd3d6')
           + '<path d="M 300,250 C 360,240 420,236 540,240 L 540,252 L 300,262 Z" fill="#8fb5c4" opacity=".7"/>')
    hill = ('<path d="M 280,420 C 300,330 340,280 400,260 C 450,246 500,250 540,264 L 540,420 Z" fill="#5f985e"/>'
            '<path d="M 280,420 C 300,330 340,280 400,260 C 380,300 360,350 352,420 Z" fill="#78b07a"/>'
            + palm(330, 330, .55) + palm(470, 300, .5, True, 1) + boulder(390, 330, 70, 40) + boulder(450, 320, 50, 26, 1))
    # shophouses on the left, stepping up the slope
    shops = ''
    for i, (x, y, w, h, wall, aw, lines) in enumerate((
            (-20, 560, 170, 250, '#f2eee6', '#2fb3b8', [('DIVE CENTER', '#2a7f86', 14), ('สอนดำน้ำ · Fun Dive', '#1a1626', 10)]),
            (110, 470, 130, 210, '#f6d8cf', '#d8655a', [('มินิมาร์ท', '#c4463d', 14), ('Minimart', '#1a1626', 10)]),
            (210, 400, 110, 170, '#dfeaf0', '#3d6fb0', [('ซัก อบ รีด', '#3d6fb0', 12), ('Laundry', '#1a1626', 9)]))):
        shops += (f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{wall}"/><rect x="{x + w * .7:.0f}" y="{y - h}" width="{w * .3:.0f}" height="{h}" fill="#000" opacity=".06"/>'
                  f'<rect x="{x - 6}" y="{y - h - 10}" width="{w + 12}" height="12" fill="#b9b4ae"/>'
                  f'<rect x="{x + 12}" y="{y - h + 22}" width="{w * .36:.0f}" height="{h * .22:.0f}" fill="#3a4b6a"/><rect x="{x + w * .56:.0f}" y="{y - h + 22}" width="{w * .32:.0f}" height="{h * .22:.0f}" fill="#3a4b6a"/>'
                  f'<rect x="{x + w * .58:.0f}" y="{y - h + 26}" width="{w * .12:.0f}" height="{h * .08:.0f}" fill="#d6dfe8"/>'
                  f'<rect x="{x + w - 40}" y="{y - h + 70}" width="28" height="18" rx="2" fill="#e9e6e0"/><circle cx="{x + w - 26}" cy="{y - h + 79}" r="6" fill="#b9b4ae"/>'
                  f'<rect x="{x}" y="{y - h * .5:.0f}" width="{w}" height="6" fill="#b9b4ae"/>'
                  + sign(x + 8, y - h * .5 + 8, w - 16, h * .17, lines, '#f8f4ec')
                  + f'<path d="M {x - 4},{y - h * .27:.0f} L {x + w + 4},{y - h * .27:.0f} L {x + w - 6},{y - h * .2:.0f} L {x + 6},{y - h * .2:.0f} Z" fill="{aw}"/>'
                  + ''.join(f'<path d="M {x + 6 + k * 18},{y - h * .2:.0f} l 9,8 l 9,-8" fill="{aw}" opacity=".85"/>' for k in range(int((w - 12) / 18)))
                  + f'<rect x="{x + 10}" y="{y - h * .19:.0f}" width="{w - 20}" height="{h * .19:.0f}" fill="#4a3f3a" opacity=".55"/>')
    shops += (tank(30, 548, '#9aa6b8', .8) + tank(48, 548, '#b9c2d0', .8) + tank(66, 548, '#9aa6b8', .8)
              + wetsuit(100, 450) + plastic_chair(170, 456, '#d8655a', .9) + plastic_chair(196, 458, '#3d6fb0', .9)
              + '<rect x="124" y="430" width="44" height="30" rx="4" fill="#3d6fb0"/><rect x="124" y="430" width="44" height="8" rx="3" fill="#2c5a96"/>'
              + txt(146, 452, 'ICE', 9, '#ffffff', 800, font=EN))
    wall = ('<path d="M 300,560 L 540,520 L 540,600 L 300,640 Z" fill="#cfc9c0"/><path d="M 300,560 L 540,520 L 540,528 L 300,568 Z" fill="#e6e1d8"/>'
            + bougainvillea(300, 470, 240, 90, 3) + frangipani(500, 560, .9))
    road_ = (f'<path d="M 40,960 L 520,960 L 360,420 L 300,420 Z" fill="url(#{fid}rd)"/>'
             + ''.join(f'<path d="M {40 + (300 - 40) * t:.0f},{960 - 540 * t:.0f} L {520 + (360 - 520) * t:.0f},{960 - 540 * t:.0f}" stroke="#a69e94" stroke-width="{2.4 - t * 1.6:.1f}" opacity=".7"/>' for t in [k / 14 for k in range(1, 14)])
             + '<path d="M 280,960 L 330,420" stroke="#efe9df" stroke-width="3" stroke-dasharray="26 22" opacity=".85"/>'
             + '<path d="M 40,960 L 300,420" stroke="#9a9288" stroke-width="5"/>')
    poles = powerpole(250, 150, 470) + powerpole(470, 60, 560)
    w_ = wires([(-10, 190), (250, 170), (470, 80), (560, 60)], 30, 6) + wires([(-10, 260), (250, 200), (470, 110), (560, 96)], 22, 3)
    parked = scooter(120, 640, .9, '#d8655a') + scooter(210, 580, .75, '#eef0f4')
    ground = ('<rect y="400" width="540" height="560" fill="#bdb6aa"/>'
              '<path d="M 330,420 L 540,400 L 540,960 L 470,960 Z" fill="#5f985e"/><path d="M 330,420 L 400,412 L 520,960 L 470,960 Z" fill="#78b07a"/>'
              + palm(520, 820, .9, True) + bougainvillea(440, 640, 100, 200, 7) + boulder(440, 940, 100, 70))
    bg = blur(sky + far + hill, 1) + ground + shops + wall + road_ + parked + poles + w_
    ch = [sun_island(fid, 300, 560, .72, (560, -120)),
          other(fid, 220, 830, .55, (560, -120), ISL['DOG'], 'dog')]
    sh = (CL.contact_shadow(300, 914, 44) + CL.contact_shadow(220, 926, 46, 8) + castsh(parked, 10, 10, .3)
          + CL.ao_line(300, 640, 540, 600, 14, .35) + CL.ao_line(-20, 560, 150, 560, 12, .3))
    fg = scooter(420, 900, 1.05, '#2fb3b8', True)
    light = CL.glow(560, -60, 420, '#fff6ea', .3, core=False) + CL.shaft([(540, 0), (540, 160), (160, 960), (20, 960)], '#fff6ea', .12, src=(540, 60), end=(200, 900), dust_n=30, seed=1)
    return frame(fid, 'day', bg, sh, ch, fg, light, defs=d)


# ================================================================ 2. Mae Haad pier, moving day
def pier():
    fid = 'L2'
    d = G(f'{fid}sky', [(0, '#5aa2da'), (.75, '#c6e3f2'), (1, '#eef5f6')]) + G(f'{fid}sea', [(0, '#2a8fbd'), (.5, '#3fb4c6'), (1, '#7fdcd2')]) + G(f'{fid}deck', [(0, '#d6cfc4'), (1, '#bdb3a6')])
    sky = f'<rect width="540" height="380" fill="url(#{fid}sky)"/>' + cumulus(130, 120, 1) + cumulus(430, 180, .7)
    hills = ('<path d="M -20,380 C 40,300 120,250 220,246 C 320,242 420,280 560,330 L 560,380 Z" fill="#5f985e"/>'
             '<path d="M -20,380 C 40,300 120,250 220,246 C 160,270 110,320 80,380 Z" fill="#78b07a"/>'
             + ''.join(f'<rect x="{x}" y="{y}" width="12" height="9" fill="#f4f1ec"/><path d="M {x - 2},{y} l 8,-6 l 8,6 Z" fill="{c}"/>' for x, y, c in ((120, 300, '#c87a5e'), (160, 286, '#3d6fb0'), (250, 278, '#c87a5e'), (300, 292, '#d8655a'), (380, 310, '#3d6fb0'), (420, 318, '#c87a5e')))
             + palm(60, 360, .5) + palm(340, 350, .45, True) + boulder(440, 384, 80, 40) + boulder(500, 384, 60, 26, 1))
    water = f'<rect y="380" width="540" height="580" fill="url(#{fid}sea)"/>' + ''.join(f'<path d="M {x},{y} q 12,-4 24,0" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none"/>' for x, y in ((30, 420), (120, 440), (220, 410), (420, 430), (480, 470), (60, 500), (380, 520)))
    boats = ferry(330, 456, .9) + longtail(80, 520, .6) + longtail(470, 560, .5, '#7fd3d6', '#6a4a34')
    deck = (f'<path d="M -20,600 L 560,560 L 560,960 L -20,960 Z" fill="url(#{fid}deck)"/><path d="M -20,600 L 560,560 L 560,576 L -20,616 Z" fill="#e6e1d8"/>'
            + ''.join(f'<rect x="{x}" y="{596 - x * .07:.0f}" width="10" height="26" fill="#f2c26a" opacity=".0"/><rect x="{x}" y="{588 - x * .07:.0f}" width="12" height="20" rx="3" fill="#5e6270"/>' for x in (20, 200, 380))
            + '<path d="M 20,606 C 60,640 120,640 160,600" stroke="#c4b89c" stroke-width="4" fill="none"/>')
    booth = ('<g><rect x="380" y="430" width="160" height="150" fill="#f4f1ec"/><rect x="380" y="430" width="160" height="16" fill="#2fb3b8"/>'
             '<path d="M 370,430 L 550,430 L 530,400 L 390,400 Z" fill="#c87a5e"/><rect x="396" y="470" width="128" height="60" fill="#3a4b6a"/>'
             + sign(392, 448, 136, 20, [('ท่าเรือแม่หาด · Mae Haad Pier', '#1a1626', 10)], '#f8f4ec') + '</g>')
    taxis = pickup_taxi(110, 720, 1.05, '#3d6fb0') + pickup_taxi(440, 700, .95, '#d8655a')
    boxes = (cardboard(240, 690, 60, 50, 'ครัว') + cardboard(300, 700, 50, 40) + cardboard(250, 646, 52, 44, 'เสื้อผ้า') + cardboard(296, 664, 44, 36)
             + '<g transform="translate(276,646)"><rect x="-18" y="-40" width="36" height="40" rx="4" fill="#eef0f4"/><circle cx="0" cy="-22" r="13" fill="#c9ced8"/><circle cx="0" cy="-22" r="4" fill="#5e6270"/></g>'
             + '<g transform="translate(318,664)"><rect x="-16" y="-24" width="32" height="24" rx="8" fill="#f4efe6"/><rect x="-16" y="-24" width="32" height="8" rx="4" fill="#d6d0c4"/></g>'
             + '<g transform="translate(296,610)"><ellipse cx="0" cy="0" rx="24" ry="6" fill="#2a2c34"/><path d="M 22,0 L 44,-6" stroke="#2a2c34" stroke-width="4"/></g>')
    crowd = ''.join(f'<g transform="translate({x},{y}) scale(.42)" opacity=".95">{R.TOURIST}</g>' for x, y in ((40, 470), (470, 440)))
    bg = blur(sky + hills, 1) + water + blur(boats, 1) + booth + deck + crowd
    ch = [sun_city(fid, 210, 500, .8, (-200, -100), head='dead', tote=True, camera=True)]
    sh = CL.contact_shadow(210, 896, 46) + castsh(taxis + boxes, 10, 10, .3) + CL.ao_line(-20, 610, 560, 570, 12, .3)
    light = CL.glow(-60, -40, 420, '#fff6ea', .3, core=False) + CL.shaft([(0, 0), (160, 0), (480, 960), (200, 960)], '#fff6ea', .1, src=(60, 40), end=(330, 900), dust_n=26, seed=2)
    return frame(fid, 'day', bg, sh, ch, taxis + boxes, light, defs=d)


# ================================================================ 3. hillside bungalow, first night (interior)
def bungalow():
    fid = 'L3'
    d = G(f'{fid}wall', [(0, '#9a7458'), (1, '#7d5c46')], 0, 0, 1, 0) + G(f'{fid}night', [(0, '#1b2a4a'), (1, '#3a4e78')]) + G(f'{fid}fl', [(0, '#8a6a52'), (1, '#6a4e3c')])
    wall = (f'<rect width="540" height="640" fill="url(#{fid}wall)"/>'
            + ''.join(f'<rect x="{x}" y="0" width="3" height="640" fill="#6a4c38" opacity=".7"/>' for x in range(0, 540, 34))
            + '<rect y="0" width="540" height="40" fill="#5e4434"/>' + ''.join(f'<rect x="{x}" y="0" width="14" height="40" fill="#4a3428"/>' for x in range(20, 540, 90)))
    window = (f'<rect x="300" y="120" width="210" height="250" fill="url(#{fid}night)"/>'
              '<circle cx="440" cy="170" r="18" fill="#f6f1e6"/><circle cx="446" cy="166" r="16" fill="#2a3a5c"/>'
              '<path d="M 300,300 L 510,300 L 510,370 L 300,370 Z" fill="#14203a"/>'
              + ''.join(f'<circle cx="{x}" cy="300" r="2.4" fill="#d9f2ff"/><circle cx="{x}" cy="300" r="7" fill="#d9f2ff" opacity=".25"/>' for x in (320, 352, 390, 430, 468, 496))
              + '<path d="M 300,320 C 360,300 420,330 510,310 L 510,370 L 300,370 Z" fill="#2f4a3a"/>'
              + ''.join(f'<rect x="{x}" y="120" width="6" height="250" fill="#5e4434"/>' for x in (300, 404, 504))
              + '<rect x="294" y="114" width="222" height="8" fill="#5e4434"/><rect x="294" y="368" width="222" height="12" fill="#4a3428"/>'
              # open louvre shutters
              + '<path d="M 300,120 L 270,130 L 270,360 L 300,370 Z" fill="#6f5442"/>' + ''.join(f'<path d="M 272,{140 + k * 16} L 298,{134 + k * 16}" stroke="#4a3428" stroke-width="3"/>' for k in range(14))
              + '<path d="M 510,120 L 536,130 L 536,360 L 510,370 Z" fill="#5e4434"/>')
    floor = (f'<rect y="640" width="540" height="320" fill="url(#{fid}fl)"/>'
             + ''.join(f'<path d="M {270 + (x - 270) * .3:.0f},640 L {x},960" stroke="#5a402e" stroke-width="2"/>' for x in range(-300, 860, 60))
             + '<ellipse cx="230" cy="800" rx="170" ry="40" fill="#c9a87a" opacity=".85"/>' + ''.join(f'<ellipse cx="230" cy="800" rx="{r}" ry="{r * .24:.0f}" fill="none" stroke="#a6825a" stroke-width="2"/>' for r in (150, 120, 90)))
    bed = ('<path d="M 20,560 L 300,560 L 300,700 L 20,700 Z" fill="#6f5442"/><rect x="20" y="520" width="280" height="60" rx="6" fill="#f2eee6"/>'
           '<path d="M 16,540 C 100,520 220,526 304,516 L 304,620 C 220,630 100,628 20,632 Z" fill="#7fb3c4"/><path d="M 16,540 C 100,520 220,526 304,516 L 304,536 C 220,544 100,546 20,556 Z" fill="#9ccbd6"/>'
           '<rect x="30" y="480" width="90" height="46" rx="14" fill="#f8f6f4"/>'
           # mosquito net gathered from the ceiling
           '<path d="M 160,40 C 100,200 40,380 20,560 L 300,560 C 280,380 220,200 160,40 Z" fill="#f4f6fa" opacity=".18"/>'
           + ''.join(f'<path d="M 160,40 C {150 - k * 22},220 {120 - k * 30},400 {110 - k * 30},560" stroke="#f4f6fa" stroke-width="1.4" fill="none" opacity=".35"/>' for k in range(-4, 4))
           + '<circle cx="160" cy="40" r="6" fill="#d6d0c4"/>')
    fan = ('<g transform="translate(400,560)"><rect x="-4" y="0" width="8" height="90" fill="#d6d0c4"/><ellipse cx="0" cy="92" rx="30" ry="8" fill="#c9c3b8"/>'
           '<circle cx="0" cy="-30" r="34" fill="none" stroke="#e8e4dc" stroke-width="3"/><circle cx="0" cy="-30" r="34" fill="#7fb3c4" opacity=".25"/>'
           + ''.join(f'<ellipse cx="0" cy="-48" rx="9" ry="18" fill="#9ccbd6" transform="rotate({a} 0 -30)"/>' for a in (0, 120, 240)) + '<circle cx="0" cy="-30" r="7" fill="#e8e4dc"/></g>')
    stuff = (cardboard(330, 620, 70, 54, 'ครัว') + cardboard(380, 640, 60, 40) + cardboard(334, 580, 56, 42, 'มีด')
             + '<g transform="translate(470,620)"><rect x="-24" y="-60" width="48" height="60" rx="4" fill="#eef0f4"/><rect x="-24" y="-60" width="48" height="22" rx="4" fill="#e2e5ec"/><rect x="16" y="-52" width="3" height="10" fill="#9aa1b0"/></g>'
             + '<g transform="translate(250,450)"><rect x="-30" y="0" width="60" height="4" fill="#5e4434"/><rect x="-26" y="-34" width="18" height="34" fill="#c87a5e"/><rect x="-6" y="-26" width="14" height="26" fill="#2f5a5e"/><circle cx="18" cy="-10" r="10" fill="#3f8a6e"/></g>'
             + '<g transform="translate(90,250)"><rect x="-26" y="-36" width="52" height="68" fill="#f2eee6"/><rect x="-22" y="-32" width="44" height="44" fill="#2fb3b8"/><path d="M -22,0 q 11,-10 22,0 q 11,10 22,0 L 22,12 L -22,12 Z" fill="#1f6f8e"/>'
             + txt(0, 26, 'KOH TAO', 8, '#1a1626', 800, font=EN) + '</g>'
             + '<g transform="translate(470,60)"><path d="M 0,0 L 0,40" stroke="#c9b89c" stroke-width="1.5"/>' + ''.join(f'<path d="M {dx},40 L {dx},{60 + abs(dx)}" stroke="#c9b89c" stroke-width="1"/><ellipse cx="{dx}" cy="{64 + abs(dx)}" rx="4" ry="6" fill="#f3ece0"/>' for dx in (-12, -4, 4, 12)) + '</g>'
             + ''.join(f'<circle cx="{x}" cy="{70 + 14 * math.sin(x / 40):.0f}" r="3" fill="#ffe2b0"/>' for x in range(30, 280, 22))
             + '<path d="M 20,72 C 100,96 180,60 280,80" stroke="#3a2a22" stroke-width="1" fill="none"/>')
    lamp = ('<g transform="translate(250,450)"><path d="M 30,-60 L 52,-60 L 58,-40 L 24,-40 Z" fill="#f2e2c4"/><rect x="38" y="-40" width="4" height="40" fill="#8a6a50"/></g>')
    gecko = f'<g transform="translate(220,170) rotate(20) scale(.32)">{ISL["GECKO"]}</g>'
    bg = wall + window + floor + bed + fan + stuff + lamp + gecko
    ch = [sun_city(fid, 180, 440, .82, (291, 400), head='dead', rig='interior', tote=False, camera=False)]
    sh = CL.contact_shadow(180, 846, 46) + CL.ao_line(0, 640, 540, 640, 18, .5) + castsh(stuff, 8, 8, .3)
    light = (CL.falloff(290, 420, 520, .55) + CL.glow(291, 400, 220, '#ffd9a8', .38) + CL.glow(405, 245, 160, '#9fb8ff', .18, core=False)
             + CL.shaft([(300, 120), (510, 120), (420, 960), (120, 960)], '#b9ccff', .08, src=(405, 150), end=(270, 900), dust_n=24, seed=5))
    return frame(fid, 'interior', bg, sh, ch, '', light, defs=d)


# ================================================================ 4. island minimart (โชห่วย)
def shop():
    fid = 'L4'
    d = G(f'{fid}wall', [(0, '#e9ece8'), (1, '#d6dbd6')]) + G(f'{fid}fl', [(0, '#cfd3cf'), (1, '#b2b8b2')])
    rnd = random.Random(9)
    bg = f'<rect width="540" height="960" fill="url(#{fid}wall)"/><rect y="620" width="540" height="340" fill="url(#{fid}fl)"/>'
    bg += ''.join(f'<path d="M 0,{y} L 540,{y}" stroke="#a9b0a9" stroke-width="1" opacity=".6"/>' for y in range(660, 960, 50))
    bg += ''.join(f'<path d="M {270 + (x - 270) * .3:.0f},620 L {x},960" stroke="#a9b0a9" stroke-width="1" opacity=".6"/>' for x in range(-300, 860, 70))
    shelves = ''
    for sx, sw in ((-10, 250), (330, 230)):
        shelves += f'<rect x="{sx}" y="90" width="{sw}" height="540" fill="#e2e5e2"/>'
        for row in range(6):
            y = 140 + row * 82
            shelves += f'<rect x="{sx}" y="{y + 40}" width="{sw}" height="8" fill="#9aa1a8"/>'
            x = sx + 6
            while x < sx + sw - 16:
                w = rnd.choice([14, 18, 22, 26]); h = rnd.randint(22, 38)
                c = rnd.choice(['#d8655a', '#3d6fb0', '#2fb3b8', '#e88aa8', '#f2eee6', '#7fb07a', '#c87a5e', '#5a6c8e', '#f0956e', '#ffffff'])
                shelves += f'<rect x="{x}" y="{y + 40 - h}" width="{w}" height="{h}" rx="2" fill="{c}"/><rect x="{x}" y="{y + 40 - h}" width="{w * .35:.0f}" height="{h}" fill="#ffffff" opacity=".18"/>'
                if rnd.random() < .35:
                    shelves += f'<rect x="{x + 2}" y="{y + 40 - h * .6:.0f}" width="{w - 4}" height="5" fill="#ffffff" opacity=".7"/>'
                x += w + 2
            if row % 2 == 0:
                shelves += f'<rect x="{sx + 20 + row * 10}" y="{y + 48}" width="30" height="13" rx="2" fill="#ffd84a"/>' + txt(sx + 35 + row * 10, y + 58, f'{rnd.randint(15, 89)}฿', 9, '#c4463d', 800)
    snacks = ''.join(f'<rect x="{250 + i * 14}" y="80" width="10" height="{rnd.randint(160, 230)}" fill="{rnd.choice(["#d8655a", "#2fb3b8", "#e88aa8", "#3d6fb0"])}" opacity=".9"/>' for i in range(6))
    fridge = ('<g transform="translate(240,250)"><rect x="0" y="0" width="90" height="370" rx="6" fill="#d8655a"/><rect x="8" y="30" width="74" height="300" fill="#bfe3ee" opacity=".55"/>'
              + ''.join(f'<rect x="12" y="{50 + k * 70}" width="66" height="4" fill="#9aa1a8"/>' + ''.join(f'<rect x="{14 + j * 13}" y="{24 + k * 70}" width="10" height="26" rx="4" fill="{rnd.choice(["#2fb3b8", "#3fa06a", "#f2eee6", "#d8655a", "#c87a5e"])}"/>' for j in range(5)) for k in range(4))
              + txt(45, 22, 'COLD', 12, '#ffffff', 800, font=EN) + '</g>')
    counter = ('<path d="M 40,640 L 500,640 L 520,720 L 20,720 Z" fill="#8a6a50"/><rect x="20" y="720" width="500" height="200" fill="#6f5442"/>'
               '<path d="M 40,640 L 500,640 L 502,646 L 38,646 Z" fill="#a8835f"/>'
               '<g transform="translate(400,612)"><rect x="-34" y="0" width="68" height="28" rx="3" fill="#2a2c34"/><rect x="-28" y="4" width="40" height="12" fill="#7fd3d6"/><rect x="-30" y="-30" width="20" height="30" fill="#2a2c34"/></g>'
               '<g transform="translate(120,600)"><rect x="-40" y="0" width="80" height="40" rx="6" fill="#3d6fb0"/><rect x="-40" y="0" width="80" height="10" rx="4" fill="#2c5a96"/>' + txt(0, 30, 'น้ำแข็ง', 11, '#ffffff', 700) + '</g>'
               '<g transform="translate(230,624)"><path d="M -20,0 L 20,0 L 16,-14 L -16,-14 Z" fill="#c9ced8"/><rect x="-24" y="0" width="48" height="16" rx="2" fill="#9aa1b0"/></g>'
               '<g transform="translate(300,620)">' + ''.join(f'<path d="M {k * 10 - 16},0 C {k * 10 - 22},-24 {k * 10 - 6},-34 {k * 10 + 2},-30" stroke="#e8c35e" stroke-width="7" fill="none" stroke-linecap="round"/>' for k in range(4)) + '</g>')
    fan = '<g transform="translate(480,60)"><rect x="-2" y="0" width="4" height="40" fill="#9aa1a8"/>' + ''.join(f'<ellipse cx="0" cy="40" rx="44" ry="6" fill="#d6dbd6" transform="rotate({a} 0 40)"/>' for a in (0, 60, 120)) + '<circle cx="0" cy="40" r="7" fill="#9aa1a8"/></g>'
    signs = (sign(140, 30, 260, 40, [('ร้านป้าแดง · มินิมาร์ท', '#c4463d', 15)], '#fff4d6', border='#d8655a')
             + '<g transform="translate(30,40) rotate(-4)">' + sign(0, 0, 90, 34, [('ของสดมาพรุ่งนี้', '#1a1626', 10), ('(ถ้าเรือมา)', '#c4463d', 9)], '#ffffff') + '</g>')
    aunt = other(fid, 300, 470, .95, (-200, 100), ISL['AUNT_BODY'] + '<use href="#h_aunt"/>')
    bg += shelves + snacks + fridge + signs + fan
    ch = [aunt]
    s2 = sun_city(fid, 120, 520, 1.0, (-200, 100), head='annoy', tote=True, camera=False)
    fg = counter + s2[1]
    d += s2[0]
    ch2 = []
    light = CL.glow(270, 120, 360, '#ffffff', .2, core=False) + CL.glow(-40, 500, 300, '#fff6ea', .25, core=False)
    sh = CL.ao_line(0, 620, 540, 620, 16, .35) + castsh(counter, 6, 10, .35)
    return frame(fid, 'interior', bg, sh, ch + ch2, fg, light, defs=d)


# ================================================================ 5. dive centre on Sairee
def dive_shop():
    fid = 'L5'
    d = G(f'{fid}sky', [(0, '#5aa2da'), (1, '#e6f2f6')]) + G(f'{fid}sea', [(0, '#2a8fbd'), (.5, '#3fb4c6'), (1, '#8fe0d6')]) + G(f'{fid}deck', [(0, '#c4a083'), (1, '#a9876b')])
    view = (f'<rect width="540" height="420" fill="url(#{fid}sky)"/>' + cumulus(420, 120, .8)
            + f'<rect y="300" width="540" height="140" fill="url(#{fid}sea)"/>' + longtail(140, 360, .45) + longtail(360, 340, .35, '#7fd3d6')
            + '<path d="M 0,420 C 140,410 300,430 540,414 L 540,470 L 0,470 Z" fill="#f2ece2"/>' + palm(60, 440, .7) + palm(500, 430, .6, True))
    roof = ('<path d="M -20,0 L 560,0 L 560,90 L -20,90 Z" fill="#7d5c40"/>' + ''.join(f'<path d="M {x},60 L {x + 18},60 L {x + 12},{110 + (x % 3) * 6} L {x + 4},{106 + (x % 3) * 6} Z" fill="{["#8f6a4a", "#a37c58", "#b58d68"][x % 3]}"/>' for x in range(-10, 560, 16))
            + '<rect x="0" y="0" width="34" height="960" fill="#8a6a50"/><rect x="506" y="0" width="34" height="960" fill="#7a5b40"/>')
    deck = f'<rect y="466" width="540" height="494" fill="url(#{fid}deck)"/>' + ''.join(f'<path d="M 0,{560 + i * i * 4}" stroke="#9a7a60"/><rect y="{560 + i * i * 4}" width="540" height="2" fill="#9a7a60"/>' for i in range(1, 10))
    rack = ('<rect x="40" y="420" width="190" height="10" fill="#6f5442"/><rect x="40" y="560" width="190" height="10" fill="#6f5442"/>'
            + ''.join(tank(60 + i * 26, 556, ['#9aa6b8', '#b9c2d0'][i % 2], .9) for i in range(7)))
    suits = '<rect x="250" y="150" width="240" height="6" fill="#9aa1a8"/>' + ''.join(wetsuit(270 + i * 34, 160, ['#1f2b46', '#2c3a54', '#1f2b46', '#3a2a40', '#1f2b46', '#2c3a54', '#1f2b46'][i], ['#2fb3b8', '#d8655a', '#2fb3b8', '#e88aa8', '#2fb3b8', '#7fd3d6', '#d8655a'][i]) for i in range(7))
    board = ('<g transform="translate(250,226)"><rect x="0" y="0" width="200" height="140" rx="6" fill="#f8f8f6" stroke="#9aa1a8" stroke-width="4"/>'
             + txt(100, 26, 'TODAY · วันนี้', 14, '#1a1626', 800)
             + ''.join(txt(14, 52 + k * 22, t, 11, c, 600, 'start', EN) for k, (t, c) in enumerate((('08:00  Open Water  ·  SUN', '#2a7f86'), ('11:00  Fun Dive  ·  LAE', '#d8655a'), ('14:00  Snorkel trip', '#3d6fb0'), ('Wind: OK  ·  Sea: calm', '#5a5470'))))
             + '</g>')
    fins = ''.join(f'<path d="M {x},560 L {x + 16},560 L {x + 22},520 L {x - 6},520 Z" fill="{c}" transform="rotate({r} {x + 8} 540)"/>' for x, c, r in ((250, '#2fb3b8', -6), (276, '#d8655a', 4), (300, '#2fb3b8', -2)))
    flag = '<g transform="translate(470,240)"><rect x="0" y="0" width="4" height="120" fill="#9aa1a8"/><rect x="4" y="0" width="44" height="30" fill="#d8655a"/><path d="M 4,0 L 48,30" stroke="#fff" stroke-width="6"/></g>'
    bg = blur(view, 1) + deck + rack + suits + board + fins + flag
    lae = other(fid, 150, 480, .82, (-200, 100), ISL['LAE_BODY'] + '<use href="#h_lae"/>')
    ch = [lae, sun_island(fid, 390, 480, .86, (-200, 100), head='smirktalk')]
    sh = CL.contact_shadow(150, 862, 44) + CL.contact_shadow(390, 900, 48) + CL.ao_line(34, 560, 506, 560, 12, .3)
    light = CL.glow(-30, 200, 380, '#ffffff', .26, core=False) + CL.shaft([(40, 90), (220, 90), (460, 700), (230, 760)], '#fff8ee', .12, src=(120, 100), end=(340, 720), dust_n=26, seed=7)
    return frame(fid, 'day', bg, sh, ch, roof, light, defs=d)


# ================================================================ 6. viewpoint over Koh Nang Yuan, late afternoon
def viewpoint():
    fid = 'L6'
    d = (G(f'{fid}sky', [(0, '#86a8d8'), (.55, '#e8d2dc'), (1, '#f6e2d6')]) + G(f'{fid}sea', [(0, '#3f8fb2'), (.6, '#4fb0c0'), (1, '#6cc8c6')])
         + RG(f'{fid}shal', [(0, '#a9ece0'), (.6, '#6fd6cf'), (1, '#4fb0c0', 0)]))
    sky = f'<rect width="540" height="400" fill="url(#{fid}sky)"/><circle cx="430" cy="340" r="40" fill="#fff2e6"/><circle cx="430" cy="340" r="90" fill="#fff2e6" opacity=".25"/>' + cumulus(140, 160, .8, .8) + cumulus(330, 230, .5, .7)
    sea_ = f'<rect y="400" width="540" height="560" fill="url(#{fid}sea)"/>' + ''.join(f'<path d="M {x},{y} q 10,-3 20,0" stroke="#fff" stroke-opacity=".45" stroke-width="1.6" fill="none"/>' for x, y in ((40, 430), (300, 420), (480, 450), (90, 520), (420, 540)))
    sea_ += '<path d="M 410,402 L 450,402 L 470,560 L 390,560 Z" fill="#fff2e6" opacity=".25"/>'
    # three islands joined by a sandbar (Koh Nang Yuan)
    nangyuan = (f'<ellipse cx="270" cy="560" rx="200" ry="60" fill="url(#{fid}shal)"/>'
                '<path d="M 140,560 C 190,548 240,552 270,556 C 300,552 350,548 400,560 C 360,566 300,566 270,564 C 240,566 180,566 140,560 Z" fill="#f6eee0"/>'
                '<path d="M 90,560 C 96,520 120,496 150,494 C 176,494 196,520 196,560 Z" fill="#5f985e"/><path d="M 90,560 C 96,520 120,496 150,494 C 132,510 120,530 118,560 Z" fill="#7fb07a"/>'
                '<path d="M 232,558 C 236,530 252,516 270,516 C 290,516 304,532 306,558 Z" fill="#5f985e"/>'
                '<path d="M 350,560 C 354,526 376,508 404,508 C 430,508 446,528 450,560 Z" fill="#4f8a5e"/><path d="M 350,560 C 354,526 376,508 404,508 C 386,520 376,540 374,560 Z" fill="#6fa46c"/>'
                + boulder(100, 562, 30, 16) + boulder(430, 562, 30, 14, 1) + boulder(290, 560, 20, 10)
                + ''.join(f'<rect x="{x}" y="{y}" width="7" height="5" fill="#f4f1ec"/><path d="M {x - 1},{y} l 4.5,-3 l 4.5,3 Z" fill="#c87a5e"/>' for x, y in ((140, 520), (390, 528), (260, 540)))
                + '<path d="M 200,557 L 236,557" stroke="#8a6a50" stroke-width="2"/>')
    hillfg = ('<path d="M -20,700 C 80,640 200,630 320,660 C 420,686 500,670 560,650 L 560,960 L -20,960 Z" fill="#4f8a5e"/>'
              '<path d="M -20,700 C 80,640 200,630 320,660 C 220,660 120,680 60,720 Z" fill="#6aa477"/>')
    rocks = boulder(-30, 860, 230, 170) + boulder(380, 900, 200, 150, 1) + boulder(150, 760, 90, 50, 1)
    rail = ('<path d="M 160,700 L 560,690" stroke="#8a6a50" stroke-width="6"/><path d="M 160,730 L 560,720" stroke="#8a6a50" stroke-width="4"/>'
            + ''.join(f'<rect x="{x}" y="{690 - (x - 160) * .025:.0f}" width="8" height="70" fill="#6f5442"/>' for x in range(170, 560, 70)))
    sc = scooter(300, 800, 1.2, '#2fb3b8', True)
    bg = blur(sky, 1) + sea_ + f'<g transform="translate(270,560) scale(1.45) translate(-270,-560) translate(0,-30)">{nangyuan}</g>' + hillfg + rail + sc
    ch = [sun_island(fid, 190, 600, .68, (430, 340), head='smirk'),
          other(fid, 330, 720, .5, (430, 340), ISL['DOG'], 'dog')]
    sh = CL.contact_shadow(190, 934, 42) + castsh(sc, 10, 8, .3)
    light = CL.glow(430, 340, 300, '#ffd9b8', .34) + CL.shaft([(410, 340), (460, 340), (300, 960), (60, 960)], '#ffe2c8', .12, src=(430, 340), end=(200, 900), dust_n=28, seed=8)
    return frame(fid, 'day', bg, sh, ch, rocks, light, defs=d)


# ================================================================ graphics, new style: paper-craft diorama
def koh_tao_shape(cx, cy, s=1.0):
    # stylised Koh Tao outline: long N-S, Sairee bay west, Mae Haad mid-west, Chalok bay south, Tanote bay east
    pts = [(0, -150), (28, -140), (46, -110), (50, -70), (64, -40), (58, -10), (40, 4), (60, 30), (70, 70), (54, 110), (30, 140), (6, 150),
           (-14, 136), (-6, 118), (-30, 110), (-46, 80), (-40, 50), (-56, 30), (-46, 0), (-58, -30), (-50, -60), (-42, -100), (-24, -136)]
    return ' '.join(f'{cx + x * s:.0f},{cy + y * s:.0f}' for x, y in pts)


def g_map():
    fid = 'G1'
    d = G(f'{fid}sea', [(0, '#2a6f9a'), (1, '#1d4f74')]) + G(f'{fid}land', [(0, '#e8dcc6'), (1, '#d6c6aa')])
    bg = f'<rect width="540" height="960" fill="url(#{fid}sea)"/>'
    bg += ''.join(f'<path d="M {x},{y} q 10,-4 20,0" stroke="#5f9fc4" stroke-width="1.6" fill="none" opacity=".6"/>' for x in range(20, 540, 70) for y in range(60, 940, 90))
    # mainland (Chumphon coast) on the left, paper-cut layers
    main = ('<path d="M -20,0 L 150,0 C 160,120 130,200 160,300 C 180,380 150,460 190,560 C 210,640 180,760 200,960 L -20,960 Z" fill="#000" opacity=".2" transform="translate(8,10)"/>'
            f'<path d="M -20,0 L 150,0 C 160,120 130,200 160,300 C 180,380 150,460 190,560 C 210,640 180,760 200,960 L -20,960 Z" fill="url(#{fid}land)"/>'
            '<path d="M -20,0 L 120,0 C 128,120 104,200 130,300 C 150,380 120,460 160,560 C 180,640 150,760 170,960 L -20,960 Z" fill="#9cc08e"/>'
            '<path d="M -20,0 L 80,0 C 90,160 70,300 100,440 C 120,560 100,760 120,960 L -20,960 Z" fill="#7fae74"/>')
    pier_c = (170, 330)
    tao_c = (380, 360)
    # Koh Tao, raised paper island
    tao = (f'<polygon points="{koh_tao_shape(tao_c[0] + 8, tao_c[1] + 10, 1.05)}" fill="#000" opacity=".25"/>'
           f'<polygon points="{koh_tao_shape(*tao_c, 1.05)}" fill="#e8dcc6"/>'
           f'<polygon points="{koh_tao_shape(tao_c[0], tao_c[1] - 4, .9)}" fill="#8fbf86"/>'
           f'<polygon points="{koh_tao_shape(tao_c[0] + 4, tao_c[1] - 10, .6)}" fill="#6fa46c"/>'
           f'<polygon points="{koh_tao_shape(tao_c[0] + 6, tao_c[1] - 16, .32)}" fill="#5f985e"/>'
           + '<g transform="translate(322,214)"><ellipse rx="9" ry="7" fill="#7fae74"/><ellipse cx="14" cy="4" rx="7" ry="6" fill="#7fae74"/><ellipse cx="6" cy="14" rx="6" ry="5" fill="#7fae74"/><path d="M 0,0 L 14,4 L 6,14 Z" fill="none" stroke="#f6eee0" stroke-width="2.4"/></g>')
    route = (f'<path d="M {pier_c[0]},{pier_c[1]} C 230,280 300,300 {tao_c[0] - 54},{tao_c[1] - 6}" stroke="#fff" stroke-width="4" fill="none" stroke-dasharray="10 9"/>'
             f'<g transform="translate(262,300) rotate(8)"><path d="M -22,0 L 22,0 L 15,10 L -16,10 Z" fill="#fff"/><rect x="-10" y="-10" width="20" height="10" fill="#f2eee6"/><rect x="-7" y="-8" width="4" height="4" fill="#2fb3b8"/><rect x="1" y="-8" width="4" height="4" fill="#2fb3b8"/></g>'
             + f'<circle cx="{pier_c[0]}" cy="{pier_c[1]}" r="7" fill="#d8655a" stroke="#fff" stroke-width="2"/>')
    labels = (sign(36, 300, 108, 44, [('ชุมพร', '#1a1626', 15), ('ท่าเรือฝั่ง', '#5a5470', 10)], '#f8f4ec')
              + sign(430, 120, 92, 30, [('เกาะนางยวน', '#1a1626', 11)], '#f8f4ec') + '<path d="M 430,140 L 344,218" stroke="#f8f4ec" stroke-width="1.5" stroke-dasharray="3 3"/>'
              + sign(232, 380, 86, 26, [('หาดทรายรี', '#1a1626', 11)], '#f8f4ec') + '<path d="M 318,393 L 336,330" stroke="#f8f4ec" stroke-width="1.5" stroke-dasharray="3 3"/>'
              + sign(226, 430, 92, 26, [('ท่าเรือแม่หาด', '#1a1626', 11)], '#fff4d6') + '<path d="M 318,443 L 334,368" stroke="#fff4d6" stroke-width="1.5" stroke-dasharray="3 3"/>'
              + sign(440, 400, 80, 26, [('อ่าวโตนด', '#1a1626', 11)], '#f8f4ec') + '<path d="M 440,413 L 426,392" stroke="#f8f4ec" stroke-width="1.5" stroke-dasharray="3 3"/>'
              + sign(330, 540, 120, 26, [('อ่าวโฉลกบ้านเก่า', '#1a1626', 11)], '#f8f4ec') + '<path d="M 390,540 L 386,516" stroke="#f8f4ec" stroke-width="1.5" stroke-dasharray="3 3"/>')
    noair = (f'<g transform="translate(400,690)"><rect x="-110" y="-30" width="220" height="60" rx="30" fill="#f8f4ec"/>'
             '<path d="M -82,4 L -64,-2 L -60,-14 L -56,-14 L -56,-4 L -44,-8 L -44,-4 L -56,2 L -56,10 L -52,13 L -52,15 L -60,12 L -68,14 L -68,12 L -64,9 L -64,3 L -80,8 Z" fill="#1a1626"/>'
             '<circle cx="-63" cy="0" r="19" fill="none" stroke="#d8655a" stroke-width="3.4"/><path d="M -76,-13 L -50,13" stroke="#d8655a" stroke-width="3.4"/>'
             + txt(20, 7, 'ไม่มีสนามบิน', 17, '#1a1626', 800) + '</g>')
    compass = '<g transform="translate(480,830)"><circle r="26" fill="#f8f4ec" opacity=".9"/><path d="M 0,-20 L 6,0 L 0,20 L -6,0 Z" fill="#d8655a"/><path d="M 0,0 L 6,0 L 0,20 L -6,0 Z" fill="#2a2c34"/>' + txt(0, -30, 'N', 11, '#f8f4ec', 800, font=EN) + '</g>'
    return CL.compose('day', bg=bg + main + tao + route, chars=labels + noair + compass, extra_defs=d, prefix=fid, label=fid)


def g_island():
    fid = 'G2'
    d = G(f'{fid}bg', [(0, '#e9eef2'), (1, '#d6e0e8')]) + G(f'{fid}sea', [(0, '#5ccbc9'), (1, '#2a8fbd')])
    bg = f'<rect width="540" height="960" fill="url(#{fid}bg)"/>'
    cx, cy = 270, 430
    # water plate
    plate = (f'<ellipse cx="{cx}" cy="{cy + 120}" rx="240" ry="90" fill="#000" opacity=".12"/><ellipse cx="{cx}" cy="{cy + 100}" rx="240" ry="90" fill="url(#{fid}sea)"/>'
             f'<path d="M {cx - 240},{cy + 100} C {cx - 240},{cy + 150} {cx + 240},{cy + 150} {cx + 240},{cy + 100} L {cx + 240},{cy + 116} C {cx + 240},{cy + 166} {cx - 240},{cy + 166} {cx - 240},{cy + 116} Z" fill="#1f6f8e"/>')
    # stacked contour layers = hills (paper-craft)
    layers = ''
    for k, (rx, ry, dy, c) in enumerate(((190, 72, 96, '#efe6d8'), (176, 66, 82, '#8fbf86'), (150, 56, 62, '#7fb07a'), (120, 46, 40, '#6fa46c'), (88, 34, 18, '#5f985e'), (54, 22, -4, '#4f8a5e'), (24, 10, -24, '#457c52'))):
        layers += f'<ellipse cx="{cx - 10 + k * 4}" cy="{cy + dy + 8}" rx="{rx}" ry="{ry}" fill="#000" opacity=".12"/><ellipse cx="{cx - 10 + k * 4}" cy="{cy + dy}" rx="{rx}" ry="{ry}" fill="{c}"/>'
    roads = (f'<path d="M {cx - 150},{cy + 110} C {cx - 100},{cy + 100} {cx - 60},{cy + 96} {cx - 40},{cy + 70} C {cx - 20},{cy + 46} {cx - 70},{cy + 40} {cx - 40},{cy + 20} C {cx - 10},{cy} {cx + 30},{cy + 14} {cx + 10},{cy - 10}" stroke="#f6eee0" stroke-width="5" fill="none"/>'
             f'<path d="M {cx - 150},{cy + 110} C {cx - 100},{cy + 100} {cx - 60},{cy + 96} {cx - 40},{cy + 70} C {cx - 20},{cy + 46} {cx - 70},{cy + 40} {cx - 40},{cy + 20} C {cx - 10},{cy} {cx + 30},{cy + 14} {cx + 10},{cy - 10}" stroke="#d8655a" stroke-width="1.6" fill="none" stroke-dasharray="4 4"/>')
    houses = ''.join(f'<g transform="translate({cx + x},{cy + y})"><rect x="-6" y="-6" width="12" height="9" fill="#f4f1ec"/><path d="M -8,-6 L 0,-12 L 8,-6 Z" fill="{c}"/></g>'
                     for x, y, c in ((-120, 96, '#c87a5e'), (-90, 84, '#3d6fb0'), (-60, 60, '#c87a5e'), (-30, 34, '#d8655a'), (20, 10, '#3d6fb0'), (60, 50, '#c87a5e'), (100, 80, '#d8655a')))
    trees = ''.join(f'<circle cx="{cx + x}" cy="{cy + y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((-40, 90, 8, '#3f8a6e'), (40, 80, 9, '#2f6b5a'), (110, 60, 7, '#3f8a6e'), (-100, 50, 8, '#2f6b5a'), (70, 20, 7, '#3f8a6e'), (-10, -6, 6, '#2f6b5a')))
    scoot = f'<g transform="translate({cx + 4},{cy + 2}) scale(.22)">{scooter(0, 0, 1, "#2fb3b8")}</g>'
    stat = (f'<g transform="translate(270,140)"><rect x="-150" y="-50" width="300" height="88" rx="18" fill="#1d2a3d"/>'
            + txt(0, -6, '≈ 21 ตร.กม.', 34, '#ffffff', 800) + txt(0, 22, 'ทั้งเกาะ · ส่วนใหญ่เป็นภูเขาและเนิน', 12, '#9ccbe0', 500) + '</g>')
    prof = (f'<g transform="translate(60,640)"><rect x="0" y="0" width="420" height="120" rx="16" fill="#ffffff"/>'
            + txt(210, 24, 'ทางเดิน 500 เมตร', 13, '#1a1626', 800)
            + '<path d="M 24,96 L 190,96" stroke="#7d8698" stroke-width="5" stroke-linecap="round"/>' + txt(107, 82, 'กรุงเทพ: ราบ', 11, '#5a5470', 600)
            + '<path d="M 230,96 C 262,96 280,44 316,40 C 348,38 362,58 396,46" stroke="#5f985e" stroke-width="5" fill="none" stroke-linecap="round"/>' + txt(312, 82, 'เกาะเต่า: ปีนเนิน', 11, '#5a5470', 600)
            + f'<g transform="translate(316,40) scale(.16)">{scooter(0, 0, 1, "#d8655a")}</g></g>')
    return CL.compose('day', bg=bg + plate + layers + roads + houses + trees + scoot, chars=stat + prof, extra_defs=d, prefix=fid, label=fid)


# ================================================================ page
SHOTS = [
    (road, 'ถนนชันเหนือท่าเรือแม่หาด · เช้า', 'ปัจจุบัน · ซันผิวแทนลุคชาวเกาะกับหมาเกาะ · ร้านดำน้ำ มินิมาร์ท ร้านซักผ้า ถังอากาศและชุดดำน้ำหน้าร้าน เก้าอี้พลาสติก ถังน้ำแข็ง · เสาไฟกับสายไฟระโยงระยาง · กำแพงเฟื่องฟ้า ต้นลีลาวดี · ทะเลกับเรือหางยาวโผล่ระหว่างเนิน'),
    (pier, 'ท่าเรือแม่หาด · วันย้ายบ้าน', 'อดีต · ซันผิวเดิมชุดกรุงเทพ ยืนข้างกองกล่องที่มีพัดลม หม้อหุงข้าว และกระทะเชฟ · เรือเฟอร์รี่ เรือหางยาว ซุ้มขายตั๋ว รถกระบะแท็กซี่ นักท่องเที่ยว · บ้านบนเนินด้านหลัง'),
    (bungalow, 'บ้านเช่าบนเนิน · คืนแรก', 'อดีต · ผนังไม้ หน้าต่างบานเกล็ดเปิดเห็นทะเลกลางคืน มีไฟเรือไดหมึกเรียงที่ขอบฟ้า · เตียงกับมุ้ง พัดลมตั้งพื้น ตู้เย็นเล็ก กล่องยังไม่แกะ โมบายเปลือกหอย ไฟประดับ · ตุ๊กแกน่ารักตัวเล็กบนผนัง'),
    (shop, 'ร้านโชห่วยบนเกาะ', 'อดีต · ชั้นสินค้าแน่น ขนมแผงห้อย ตู้แช่ ถังน้ำแข็ง ตาชั่ง กล้วย · ป้ายลายมือ "ของสดมาพรุ่งนี้ (ถ้าเรือมา)" · ป้าอยู่หลังเคาน์เตอร์ ซันดูป้ายราคา'),
    (dive_shop, 'ร้านดำน้ำริมหาดทรายรี', 'ปัจจุบัน · ชายคามุงจาก ชั้นถังอากาศ ราวชุดดำน้ำ ตีนกบ กระดานตารางวันนี้มีชื่อครูซันกับครูเล · ทะเลกับเรือหางยาวด้านหลัง'),
    (viewpoint, 'จุดชมวิวเกาะนางยวน · เย็น', 'ปัจจุบัน · ฉากจบ เกาะสามเกาะเชื่อมกันด้วยสันทรายและน้ำตื้นสีฟ้าใส · โขดหินแกรนิต ราวไม้ มอเตอร์ไซค์ ซันกับหมา แสงเย็นจากขวา'),
    (g_map, 'กราฟิกใหม่ · แผนที่', 'สไตล์กระดาษตัดซ้อนชั้นมีเงา · ฝั่งชุมพร เส้นเรือไปเกาะเต่า รูปเกาะจริงแบบย่อ ป้ายชื่อหาดทรายรี ท่าเรือแม่หาด อ่าวโตนด อ่าวโฉลกบ้านเก่า เกาะนางยวน · ป้ายไม่มีสนามบิน'),
    (g_island, 'กราฟิกใหม่ · เกาะทั้งเกาะ', 'เกาะแบบโมเดลกระดาษซ้อนชั้นตามความสูง ถนนคดขึ้นเนิน บ้าน ต้นไม้ มอเตอร์ไซค์ · ป้าย ≈21 ตร.กม. · กราฟเทียบทางเดิน 500 เมตร'),
]


def build():
    figs = ''
    for i, (fn, t, note) in enumerate(SHOTS, 1):
        figs += f'<figure>{fn()}<figcaption><span class="n">{i:02d}</span> <b>{t}</b><span class="note">{note}</span></figcaption></figure>'
    page = f'''<title>Odd Hours ฉากเกาะเต่า</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: grid of 9:16 location frames, 4 across on desktop, 2 on tablet, 1 on phone. Single dark look by choice, like the other Odd Hours boards. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#9a86ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:18px; }}
@media (max-width:980px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:6px; box-shadow:0 0 0 1px var(--line); overflow:hidden; }}
figcaption {{ display:grid; gap:3px; font-size:13px; line-height:1.55; }}
.n {{ font-size:11px; color:var(--accent); }} figcaption b {{ font-weight:500; }}
.note {{ color:var(--muted); font-size:12px; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700;800&family=Inter:wght@600;800&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{R.HEAD_DEFS}{ISL["CLIPS"]}{ISL["AUNT_HEAD"]}{ISL["LAE_BACK"]}{ISL["LAE_HEAD"]}{DEFS}</defs></svg>
<div class="wrap">
  <h1>ฉากใหม่ EP.01 เกาะเต่า<span>6 สถานที่ + กราฟิกใหม่ 2 แบบ · อิงสถานที่จริงบนเกาะเต่า · ใส่ตัวละครไว้ดูสเกล</span></h1>
  <div class="grid">{figs}</div>
</div>
'''
    open(os.path.join(HERE, 'locations.html'), 'w').write(page)
    print(len(page))


if __name__ == '__main__':
    build()
