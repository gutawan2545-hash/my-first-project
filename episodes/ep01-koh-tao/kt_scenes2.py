"""EP.01 Koh Tao locations, fourth pass: every scene built through one perspective camera (persp.Cam),
so ground, buildings, props and characters share a horizon and scale. Bungalow kept from kt_scenes (owner: nearly OK).
Graphics rebuilt with more explanation. Run: python3 kt_scenes2.py -> locations.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
from persp import Cam
from scenes import G, RG, castsh, cumulus, palm, boulder
import kt_scenes as K
from kt_scenes import txt, sign, scooter, powerpole, bougainvillea, frangipani, plastic_chair, longtail, ferry, pickup_taxi, tank, wetsuit, ISL, TH, EN

NECK = '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'
_n = [0]


def person(fid, cam, X, Z, light, inner, rig='day', Y=0.0, h=1.75, face=None, units=(560, 490)):
    _n[0] += 1
    x, y, s = cam.char_transform(X, Z, Y, h, *units)
    d = CL.aim((x, y + 200 * s), light)
    return CL.character(f'{fid}-p{_n[0]}', inner, d, rig, transform=f'translate({x:.1f},{y:.1f}) scale({s:.4f})',
                        heads=[(face, '')] if face else [], prefix=fid)


def sun_now(head='smirk'):
    return R.tanify(ISL['SUN_ISLAND']) + f'<use href="#{R.HEADS[head]}_t"/>' + NECK


def sun_then(head='dead', **kw):
    return R.body(head=head, **kw)


def contact(cam, X, Z, w=0.5, Y=0.0, k=1.0):
    x, y = cam.p(X, Y, Z)
    return CL.contact_shadow(round(x, 1), round(y, 1), round(cam.ppm(Z) * w, 1), round(cam.ppm(Z) * w * .16, 1), k)


def frame(fid, rig, bg, shadow='', chars=(), fg='', light='', atmos='', defs=''):
    return CL.compose(rig, bg=bg, shadow=shadow, chars=''.join(c[1] for c in chars) + fg, light=light, atmos=atmos,
                      ui='', extra_defs=''.join(c[0] for c in chars) + defs, prefix=fid, label=fid)


def sky(fid, h, top='#5fa6dc', bot='#e8f2f6', clouds=((120, 120, .9), (420, 80, .7), (300, 200, .5))):
    return (G(f'{fid}sky', [(0, top), (.75, '#c8e3f2'), (1, bot)]),
            f'<rect width="540" height="{h}" fill="url(#{fid}sky)"/>' + ''.join(cumulus(x, y, s) for x, y, s in clouds))


# ================================================================ A. steep road above Mae Haad (one-point, road climbs)
def road():
    fid = 'A'
    cam = Cam(horizon=360, f=860, h=1.6, ox=1.4)
    S = .11                                                   # road gradient
    yy = lambda Z: S * max(Z - 1.5, 0)
    d, bg = sky(fid, 420)
    bg += ('<path d="M 300,372 C 360,330 430,316 540,330 L 540,380 L 300,380 Z" fill="#8fb5a0"/>'
           '<rect x="330" y="356" width="210" height="26" fill="#5fb8c8"/><path d="M 330,356 L 540,350 L 540,358 L 330,362 Z" fill="#9fd6dc"/>')
    items = []                                                # (Z, svg) painted far -> near
    # road + kerbs + sidewalk (left) + retaining wall (right)
    road_pts = []
    for z0, z1 in zip([1.2 + i * 1.5 for i in range(46)], [2.7 + i * 1.5 for i in range(46)]):
        c = '#c3bcb2' if int(z0 / 1.5) % 2 else '#bdb6ab'
        items.append((z1 + 100, cam.poly([(-3.2, yy(z0), z0), (3.2, yy(z0), z0), (3.2, yy(z1), z1), (-3.2, yy(z1), z1)], c)))
        items.append((z1 + 100, cam.poly([(-5.4, yy(z0) + .15, z0), (-3.2, yy(z0) + .15, z0), (-3.2, yy(z1) + .15, z1), (-5.4, yy(z1) + .15, z1)], '#d6d0c6')))
        items.append((z1 + 100, cam.poly([(-3.2, yy(z0), z0), (-3.2, yy(z0) + .15, z0), (-3.2, yy(z1) + .15, z1), (-3.2, yy(z1), z1)], '#a69e94')))
        if int(z0 / 1.5) % 3 == 0:
            items.append((z1 + 100, cam.poly([(-.08, yy(z0) + .005, z0), (.08, yy(z0) + .005, z0), (.08, yy(z0 + .9) + .005, z0 + .9), (-.08, yy(z0 + .9) + .005, z0 + .9)], '#efe9df')))
        # right wall with a lit top coping
        items.append((z1 + 100, cam.poly([(3.4, yy(z0), z0), (3.4, yy(z0) + 1.3, z0), (3.4, yy(z1) + 1.3, z1), (3.4, yy(z1), z1)], '#cfc9c0')))
        items.append((z1 + 100, cam.poly([(3.4, yy(z0) + 1.3, z0), (3.6, yy(z0) + 1.3, z0), (3.6, yy(z1) + 1.3, z1), (3.4, yy(z1) + 1.3, z1)], '#e9e4dc')))
        items.append((z1 + 100, cam.poly([(3.2, yy(z0), z0), (3.4, yy(z0), z0), (3.4, yy(z1), z1), (3.2, yy(z1), z1)], '#8f877c')))
    # green slope above the wall
    items.append((300, cam.poly([(3.6, yy(1.2) + 1.3, 1.2), (3.6, yy(70) + 1.3, 70), (40, yy(70) + 14, 70), (40, 12, 1.2)], '#5f985e')))
    items.append((299, cam.poly([(3.6, yy(1.2) + 1.3, 1.2), (3.6, yy(70) + 1.3, 70), (12, yy(70) + 6, 70), (12, 5, 1.2)], '#78b07a')))
    # shophouses on the left, each stepped up the slope, facades facing the road
    shops = [(3, 9, '#f2eee6', '#2fb3b8', 'DIVE CENTER', 'สอนดำน้ำ', '#2a7f86'), (9, 14, '#f6d8cf', '#d8655a', 'มินิมาร์ท', 'Minimart', '#c4463d'),
             (14, 19, '#dfeaf0', '#3d6fb0', 'ซัก อบ รีด', 'Laundry', '#3d6fb0'), (19, 25, '#efe2c8', '#c87a5e', 'อาหารตามสั่ง', 'Thai food', '#b05a3c'),
             (25, 31, '#e6efe2', '#3f8a6e', 'เช่ามอเตอร์ไซค์', 'Bike rent', '#2f6b5a'), (31, 38, '#f2eee6', '#7a5ab8', 'ร้านกาแฟ', 'Coffee', '#5a3a98'), (38, 46, '#f6d8cf', '#2fb3b8', 'BUNGALOW', 'ห้องพัก', '#2a7f86')]
    for z0, z1, wall, aw, t1, t2, tc in shops:
        b = yy(z0) + .15
        H = 7.2 if z0 % 2 else 6.4
        X = -5.4
        sv = cam.poly([(X, b, z0), (X, b, z1), (X, b + H, z1), (X, b + H, z0)], wall)                        # facade
        sv += cam.poly([(X, b + H, z0), (X, b + H, z1), (X - 1, b + H + .3, z1), (X - 1, b + H + .3, z0)], '#b9b4ae')     # parapet
        sv += cam.poly([(-12, b, z0), (X, b, z0), (X, b + H, z0), (-12, b + H, z0)], '#d6d0c6')            # front gable wall
        # ground-floor opening (shop interior, darker) and roller shutter half up
        sv += cam.poly([(X + .01, b, z0 + .4), (X + .01, b, z1 - .4), (X + .01, b + 2.7, z1 - .4), (X + .01, b + 2.7, z0 + .4)], '#4a3f3a')
        sv += cam.poly([(X + .02, b + 1.9, z0 + .4), (X + .02, b + 1.9, z1 - .4), (X + .02, b + 2.7, z1 - .4), (X + .02, b + 2.7, z0 + .4)], '#a9b0b8')
        # shelves / goods glowing inside
        for k in range(3):
            zz = z0 + .8 + k * (z1 - z0 - 1.6) / 3
            sv += cam.poly([(X + .03, b + .3, zz), (X + .03, b + .3, zz + .9), (X + .03, b + 1.5, zz + .9), (X + .03, b + 1.5, zz)], random.Random(int(z0 * 10 + k)).choice(['#d8655a', '#2fb3b8', '#e8c35e', '#7fb07a', '#f2eee6']), 'opacity=".55"')
        # awning sloping out over the sidewalk
        sv += cam.poly([(X, b + 3.1, z0 + .2), (X, b + 3.1, z1 - .2), (X + 1.6, b + 2.7, z1 - .2), (X + 1.6, b + 2.7, z0 + .2)], aw)
        sv += cam.poly([(X + 1.6, b + 2.7, z0 + .2), (X + 1.6, b + 2.7, z1 - .2), (X + 1.6, b + 2.5, z1 - .2), (X + 1.6, b + 2.5, z0 + .2)], '#ffffff', 'opacity=".5"')
        # upper windows + AC unit + balcony rail
        for k in range(2):
            za = z0 + .9 + k * (z1 - z0) / 2
            sv += cam.poly([(X + .01, b + 4, za), (X + .01, b + 4, za + 1.4), (X + .01, b + 5.5, za + 1.4), (X + .01, b + 5.5, za)], '#3a4b6a')
            sv += cam.poly([(X + .02, b + 4.1, za + .1), (X + .02, b + 4.1, za + .5), (X + .02, b + 5.4, za + .5), (X + .02, b + 5.4, za + .1)], '#9fb8d0', 'opacity=".6"')
        sv += cam.box(X, X + .5, b + 3.4, b + 3.9, z1 - 1.6, z1 - .9, '#e9e6e0', '#d6d1ca', '#f4f1ec')
        sv += cam.line((X + .7, b + 3.6, z0 + .3), (X + .7, b + 3.6, z1 - .3), '#5e6270', 2)
        # projecting sign facing the camera (text stays flat and readable)
        sw, sh_ = 1.6, 1.0
        sv += cam.face(X + .2, b + 5.0, z0 + .3, f'<rect x="0" y="0" width="{sw * 100}" height="{sh_ * 100}" rx="6" fill="#f8f4ec" stroke="{tc}" stroke-width="6"/>'
                       + txt(sw * 50, 44, t1, 28 if len(t1) < 10 else 22, tc, 800) + txt(sw * 50, 80, t2, 20, '#1a1626', 600))
        items.append((z0 + 50, sv))
    # parked scooters, nose-in to the kerb (side view toward the camera)
    for Z, c in ((5.5, '#d8655a'), (8, '#eef0f4'), (11.5, '#2f6fb5'), (16, '#d8655a'), (22, '#3c4458')):
        items.append((Z, cam.sprite(-3.9, yy(Z) + .15 + .3, Z, scooter(0, 0, 1, c), 55)))
    items.append((7.2, cam.sprite(-4.6, yy(7) + .15 + .55, 7, plastic_chair(0, 0, '#d8655a') + plastic_chair(26, 2, '#3d6fb0'), 70)))
    items.append((4.2, cam.sprite(-4.9, yy(4) + .15 + 1.0, 4, tank(0, 0, '#9aa6b8') + tank(24, 0, '#b9c2d0') + tank(48, 0, '#9aa6b8'), 80)))
    items.append((4.0, cam.sprite(-5.0, yy(4) + .15 + 2.3, 4, wetsuit(0, 0) + wetsuit(36, 0, '#2c3a54', '#d8655a'), 70)))
    # right side planting: bougainvillea over the wall, palms, frangipani, boulders
    for Z in (3, 7, 12, 18, 26):
        items.append((Z + .2, cam.sprite(3.5, yy(Z) + 1.3, Z, bougainvillea(-60, -50, 160, 60, int(Z)), 70)))
    for Z, X, fl in ((9, 7, True), (20, 9, False), (34, 8, True), (14, 13, False)):
        items.append((Z, cam.sprite(X, yy(Z) + 1.5, Z, palm(0, 0, 1, fl), 26)))
    items.append((5.2, cam.sprite(4.6, yy(5) + 1.3, 5, frangipani(0, 0, 1), 46)))
    items.append((10, cam.sprite(5.5, yy(10) + 1.3, 10, boulder(-80, 0, 160, 90), 60)))
    # power poles (right) + sagging wires, one bundle crossing to the houses
    poles = []
    for Z in (4.5, 16, 28, 40):
        px, py = cam.p(3.3, yy(Z), Z)
        s = cam.ppm(Z) / 36
        items.append((Z - .05, f'<g transform="translate({px:.1f},{py:.1f}) scale({s:.4f})">{powerpole(0, -330, 0)}</g>'))
        poles.append(cam.p(3.3, yy(Z) + 9.0, Z))
    wire = ''
    for i in range(6):
        dpath = f'M {poles[0][0]:.0f},{poles[0][1] + i * 5:.0f}'
        for (x0, y0), (x1, y1) in zip(poles, poles[1:]):
            dpath += f' Q {(x0 + x1) / 2:.0f},{(y0 + y1) / 2 + 26 + i * 4:.0f} {x1:.0f},{y1 + i * 3:.0f}'
        wire += f'<path d="{dpath}" stroke="#2a2c34" stroke-width="{1.8 - i * .2:.1f}" fill="none" opacity=".85"/>'
    hx, hy = cam.p(-5.4, yy(10) + 6, 10)
    wire += f'<path d="M {poles[0][0]:.0f},{poles[0][1]:.0f} Q {(poles[0][0] + hx) / 2:.0f},{(poles[0][1] + hy) / 2 + 40:.0f} {hx:.0f},{hy:.0f}" stroke="#2a2c34" stroke-width="1.6" fill="none"/>'
    wire += f'<path d="M {poles[0][0]:.0f},{poles[0][1] + 8:.0f} Q {(poles[0][0] + hx) / 2:.0f},{(poles[0][1] + hy) / 2 + 52:.0f} {hx:.0f},{hy + 10:.0f}" stroke="#2a2c34" stroke-width="1.3" fill="none"/>'
    scene = ''.join(sv for _, sv in sorted(items, key=lambda t: -t[0]))
    ch = [person(fid, cam, 1.3, 3.1, (600, -100), sun_now('smirk'), Y=yy(3.1), face='sun'),
          person(fid, cam, 2.0, 2.9, (600, -100), ISL['DOG'], Y=yy(2.9), h=.62, units=(280, 175))]
    sh = contact(cam, 1.3, 3.1, .45, yy(3.1)) + contact(cam, 2.0, 2.9, .4, yy(2.9))
    fg = cam.sprite(-1.5, yy(3.4) + .45, 3.4, scooter(0, 0, 1, '#2fb3b8'), 55)
    light = CL.glow(600, -60, 420, '#fff6ea', .28, core=False) + CL.shaft([(540, 0), (540, 200), (170, 960), (20, 960)], '#fff6ea', .1, src=(540, 60), end=(220, 900), dust_n=30, seed=1)
    return frame(fid, 'day', bg + scene + wire, sh, ch, fg, light, defs=d)


# ================================================================ B. Mae Haad pier, looking back to the village
def pier():
    fid = 'B'
    cam = Cam(horizon=420, f=820, h=1.6)
    d, bg = sky(fid, 430, clouds=((110, 110, 1), (430, 150, .7)))
    d += G(f'{fid}sea', [(0, '#3aa6c2'), (1, '#7fdcd2')])
    hills = ('<path d="M -20,420 C 40,310 140,250 260,244 C 380,240 470,290 560,330 L 560,420 Z" fill="#5f985e"/>'
             '<path d="M -20,420 C 40,310 140,250 260,244 C 190,280 120,340 90,420 Z" fill="#78b07a"/>'
             + ''.join(f'<rect x="{x}" y="{y}" width="14" height="10" fill="#f4f1ec"/><path d="M {x - 2},{y} l 9,-7 l 9,7 Z" fill="{c}"/>' for x, y, c in ((90, 330, '#c87a5e'), (140, 300, '#3d6fb0'), (190, 286, '#c87a5e'), (260, 276, '#d8655a'), (320, 290, '#3d6fb0'), (380, 300, '#c87a5e'), (440, 320, '#d8655a'), (220, 312, '#3d6fb0'), (300, 318, '#c87a5e')))
             + palm(40, 400, .5) + palm(470, 400, .5, True, 1))
    bg += hills + f'<rect y="420" width="540" height="540" fill="url(#{fid}sea)"/>'
    items = []
    # village shopfronts along the shore (front faces = flat, readable)
    Zs = 42
    xs = [(-16, -10, '#f2eee6', 'LOMPRAYAH', '#2a7f86'), (-10, -5, '#f6d8cf', '7 วัน 24 ชม.', '#c4463d'), (5, 10, '#dfeaf0', 'TAXI · แท็กซี่', '#3d6fb0'), (10, 16, '#efe2c8', 'ร้านอาหาร', '#b05a3c')]
    xs[0] = (-16, -10, '#f2eee6', 'ตั๋วเรือ · Ferry', '#2a7f86')
    for x0, x1, wall, t, tc in xs:
        sv = cam.box(x0, x1, 1.0, 7.5, Zs, Zs + 6, wall, '#d6d0c6', '#b9b4ae')
        sv += cam.face(x0 + .3, 6.9, Zs - .01, f'<rect x="0" y="0" width="{(x1 - x0 - .6) * 100}" height="110" rx="6" fill="#f8f4ec"/>' + txt((x1 - x0 - .6) * 50, 72, t, 52, tc, 800))
        sv += cam.face(x0 + .4, 4.4, Zs - .01, f'<rect x="0" y="0" width="{(x1 - x0 - .8) * 100}" height="330" fill="#4a3f3a"/>' + ''.join(f'<rect x="{30 + k * 120}" y="60" width="80" height="200" fill="#e8c35e" opacity=".45"/>' for k in range(int((x1 - x0 - .8) / 1.2))))
        items.append((Zs, sv))
    # beach strip + pier deck (planks across)
    items.append((60, cam.poly([(-30, .4, 38), (30, .4, 38), (30, .4, 50), (-30, .4, 50)], '#efe6d6')))
    for z in [1.0 + i * .8 for i in range(46)]:
        c = '#c9b296' if int(z / .8) % 2 else '#bea688'
        items.append((z + .8 + 10, cam.poly([(-3.2, 0, z), (3.2, 0, z), (3.2, 0, z + .8), (-3.2, 0, z + .8)], c)))
    items.append((49, cam.poly([(-3.2, 0, 1), (-3.2, -.5, 1), (-3.2, -.5, 38), (-3.2, 0, 38)], '#8a6a50')))
    items.append((49, cam.poly([(3.2, 0, 1), (3.2, -.5, 1), (3.2, -.5, 38), (3.2, 0, 38)], '#7a5b40')))
    for z in range(3, 38, 5):
        for X in (-3.0, 3.0):
            items.append((z, cam.box(X - .18, X + .18, 0, .6, z, z + .36, '#5e6270', '#4a4e5a', '#7d8290')))
    for z in (8, 20, 32):
        for X in (-3.1, 3.1):
            lx, ly = cam.p(X, 0, z); tx, ty = cam.p(X, 4.6, z)
            items.append((z + .1, f'<path d="M {lx:.0f},{ly:.0f} L {tx:.0f},{ty:.0f}" stroke="#9aa1a8" stroke-width="{max(1.5, cam.ppm(z) * .12):.1f}"/><circle cx="{tx:.0f}" cy="{ty:.0f}" r="{max(2, cam.ppm(z) * .22):.1f}" fill="#f4f1ec"/>'))
    # ticket kiosk on the pier + crowd + pickups at the land end
    kiosk = cam.box(-3.0, -1.4, 0, 2.8, 14, 16, '#f4f1ec', '#d6d0c6', '#c87a5e')
    kiosk += cam.face(-2.9, 2.6, 13.99, '<rect x="0" y="0" width="140" height="44" rx="4" fill="#2fb3b8"/>' + txt(70, 32, 'ท่าเรือแม่หาด', 24, '#ffffff', 800)
                      + '<rect x="14" y="70" width="112" height="90" fill="#3a4b6a"/>' + txt(70, 200, 'Mae Haad Pier', 18, '#1a1626', 700, font=EN))
    items.append((14, kiosk))
    for X, Z in ((-1.2, 18), (1.6, 22), (-.4, 26), (2.2, 15)):
        x, y, s = cam.char_transform(X, Z)
        items.append((Z, f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.4f})">{R.TOURIST}</g>'))
    items.append((36, cam.sprite(-1.2, 0, 36, pickup_taxi(0, 0, 1, '#3d6fb0'), 36)))
    items.append((35, cam.sprite(2.8, 0, 35, pickup_taxi(0, 0, 1, '#d8655a'), 36)))
    # boats: ferry moored on the right, longtails on the left
    items.append((30, cam.sprite(13, -1.0, 30, ferry(0, 0, 1), 11)))
    items.append((16, cam.sprite(-6, -1.0, 16, longtail(0, 0, 1), 22)))
    items.append((28, cam.sprite(-12, -1.0, 28, longtail(0, 0, 1, '#7fd3d6', '#6a4a34'), 22)))
    # Sun's moving-day tower of boxes (real boxes in perspective)
    bx = ''
    for x0, x1, y0, y1, z0, z1 in ((.3, 1.0, 0, .5, 4.2, 4.8), (1.0, 1.6, 0, .45, 4.3, 4.8), (.4, 1.1, .5, .95, 4.25, 4.75), (1.0, 1.5, .45, .8, 4.35, 4.75), (.5, 1.0, .95, 1.3, 4.3, 4.7)):
        bx += cam.box(x0, x1, y0, y1, z0, z1, '#c49a6c', '#a97f55', '#d8b488')
    bx += cam.face(.35, .45, 4.19, '<rect x="20" y="10" width="40" height="18" fill="#e6d2b0"/>' + txt(40, 24, 'ครัว', 14, '#5e3c28', 700))
    bx += cam.sprite(.75, 1.3, 4.5, '<rect x="-18" y="-40" width="36" height="40" rx="4" fill="#eef0f4"/><circle cx="0" cy="-22" r="13" fill="#c9ced8"/><circle cx="0" cy="-22" r="4" fill="#5e6270"/>', 100)
    bx += cam.sprite(1.25, .8, 4.55, '<rect x="-16" y="-24" width="32" height="24" rx="8" fill="#f4efe6"/><rect x="-16" y="-24" width="32" height="8" rx="4" fill="#d6d0c4"/>', 110)
    bx += cam.sprite(.9, 1.65, 4.5, '<ellipse cx="0" cy="0" rx="24" ry="6" fill="#2a2c34"/><path d="M 22,0 L 46,-6" stroke="#2a2c34" stroke-width="4"/>', 110)
    items.append((4.2, bx))
    scene = ''.join(sv for _, sv in sorted(items, key=lambda t: -t[0]))
    waves = ''.join(f'<path d="M {x},{y} q {w / 2:.0f},-3 {w:.0f},0" stroke="#fff" stroke-opacity=".5" stroke-width="1.6" fill="none"/>' for x, y, w in ((20, 470, 30), (90, 520, 40), (440, 500, 36), (490, 560, 44), (10, 620, 50), (470, 680, 56)))
    ch = [person(fid, cam, -.5, 3.3, (-200, -100), sun_then('dead', tote=True, camera=True), face='sun')]
    sh = contact(cam, -.5, 3.3, .45) + castsh(bx, 10, 10, .3)
    light = CL.glow(-60, -40, 420, '#fff6ea', .28, core=False) + CL.shaft([(0, 0), (180, 0), (480, 960), (200, 960)], '#fff6ea', .1, src=(60, 40), end=(330, 900), dust_n=26, seed=2)
    return frame(fid, 'day', bg + waves + scene, sh, ch, '', light, defs=d)


# ================================================================ D. island minimart interior
def shop():
    fid = 'D'
    cam = Cam(horizon=430, f=700, h=1.5, ox=-.3)
    rnd = random.Random(4)
    W, H, Z0, Z1 = 3.0, 3.0, 1.2, 8.5
    items = []
    # room shell
    items.append((99, cam.poly([(-W, 0, Z1), (W, 0, Z1), (W, H, Z1), (-W, H, Z1)], '#e6e9e4')))           # back wall
    items.append((98, cam.poly([(-W, 0, Z0), (-W, 0, Z1), (-W, H, Z1), (-W, H, Z0)], '#d6dbd5')))          # left wall
    items.append((98, cam.poly([(W, 0, Z0), (W, 0, Z1), (W, H, Z1), (W, H, Z0)], '#ccd2cc')))              # right wall
    items.append((98, cam.poly([(-W, H, Z0), (W, H, Z0), (W, H, Z1), (-W, H, Z1)], '#f2f4f0')))            # ceiling
    for i in range(10):                                                                                    # floor tiles
        z = Z0 + i * (Z1 - Z0) / 10
        for j in range(10):
            x = -W + j * .6
            items.append((97, cam.poly([(x, 0, z), (x + .6, 0, z), (x + .6, 0, z + (Z1 - Z0) / 10), (x, 0, z + (Z1 - Z0) / 10)], '#d8dcd6' if (i + j) % 2 else '#c9cec8')))
    for z in (2.5, 5, 7.5):                                                                                 # fluorescent tubes
        items.append((96, cam.box(-.9, .9, H - .08, H - .02, z, z + .14, '#fbfdff', '#e6eef4', '#ffffff')))
    # back wall shelving facing the camera: flat, dense, readable
    back = '<rect x="0" y="0" width="600" height="230" fill="#e2e5e2"/>'
    for r in range(4):
        y = 40 + r * 52
        back += f'<rect x="0" y="{y + 40}" width="600" height="6" fill="#9aa1a8"/>'
        x = 6
        while x < 590:
            w = rnd.choice([16, 20, 24, 30]); h = rnd.randint(22, 38)
            c = rnd.choice(['#d8655a', '#3d6fb0', '#2fb3b8', '#e88aa8', '#f2eee6', '#7fb07a', '#c87a5e', '#5a6c8e', '#f0956e'])
            back += f'<rect x="{x}" y="{y + 40 - h}" width="{w}" height="{h}" rx="2" fill="{c}"/><rect x="{x}" y="{y + 40 - h}" width="{w * .3:.0f}" height="{h}" fill="#fff" opacity=".18"/>'
            x += w + 2
    back += sign(150, -50, 300, 40, [('ร้านป้าแดง · มินิมาร์ท', '#c4463d', 22)], '#fff4d6', border='#d8655a')
    items.append((95, cam.face(-W, 2.6, Z1 - .01, f'<g transform="translate(0,30)">{back}</g>')))
    # left wall shelf unit (box) with goods on its aisle-facing side
    items.append((90, cam.box(-W, -W + .5, 0, 2.2, 3.2, Z1 - .2, '#c9cec8', '#bfc5bf', '#e2e5e2', side_dark='#b4bab4')))
    for r in range(5):
        yb = .2 + r * .42
        items.append((89, cam.poly([(-W + .5, yb, 3.2), (-W + .5, yb, Z1 - .2), (-W + .5, yb + .04, Z1 - .2), (-W + .5, yb + .04, 3.2)], '#8a929a')))
        z = 3.3
        while z < Z1 - .4:
            dz = rnd.choice([.18, .22, .28]); hgt = rnd.uniform(.18, .34)
            items.append((89, cam.poly([(-W + .51, yb + .04, z), (-W + .51, yb + .04, z + dz), (-W + .51, yb + .04 + hgt, z + dz), (-W + .51, yb + .04 + hgt, z)],
                                       rnd.choice(['#d8655a', '#3d6fb0', '#2fb3b8', '#e88aa8', '#f2eee6', '#7fb07a', '#f0956e']))))
            z += dz + .03
    # right wall: drinks fridges with glass doors
    for z0 in (3.0, 4.6, 6.2):
        items.append((88, cam.box(W - .7, W, 0, 2.1, z0, z0 + 1.5, '#d8655a', '#c4463d', '#e8836f')))
        items.append((87, cam.poly([(W - .71, .25, z0 + .1), (W - .71, .25, z0 + 1.4), (W - .71, 1.85, z0 + 1.4), (W - .71, 1.85, z0 + .1)], '#bfe3ee', 'opacity=".75"')))
        for r in range(4):
            for k in range(6):
                zz = z0 + .15 + k * .2
                yb = .35 + r * .38
                items.append((86.9, cam.poly([(W - .72, yb, zz), (W - .72, yb, zz + .12), (W - .72, yb + .26, zz + .12), (W - .72, yb + .26, zz)], rnd.choice(['#2fb3b8', '#3fa06a', '#f2eee6', '#d8655a', '#c87a5e']))))
    # hanging snack strips + wall fan
    items.append((79, cam.sprite(2.2, 2.6, 7.6, '<rect x="-3" y="-50" width="6" height="40" fill="#9aa1a8"/>' + ''.join(f'<ellipse cx="0" cy="-10" rx="40" ry="6" fill="#d6dbd6" transform="rotate({a} 0 -10)"/>' for a in (0, 60, 120)) + '<circle cx="0" cy="-10" r="7" fill="#9aa1a8"/>', 60)))
    # counter (near, left) with register, scale, ice box, bananas, hand-written sign
    cnt = cam.box(-1.9, -.8, 0, 1.0, 2.4, 3.0, '#8a6a50', '#6f5442', '#a8835f')
    cnt += cam.sprite(-1.0, 1.0, 2.6, '<rect x="-34" y="-28" width="68" height="28" rx="3" fill="#2a2c34"/><rect x="-28" y="-24" width="40" height="12" fill="#7fd3d6"/><rect x="-30" y="-58" width="20" height="30" fill="#2a2c34"/>', 200)
    cnt += cam.sprite(-1.7, 1.0, 2.8, ''.join(f'<path d="M {k * 10 - 16},0 C {k * 10 - 22},-24 {k * 10 - 6},-34 {k * 10 + 2},-30" stroke="#e8c35e" stroke-width="7" fill="none" stroke-linecap="round"/>' for k in range(4)), 220)
    cnt += cam.face(-1.85, .9, 2.39, '<g transform="rotate(-3) scale(.4)">' + sign(10, 6, 150, 56, [('ของสดมาพรุ่งนี้', '#1a1626', 18), ('(ถ้าเรือมา)', '#c4463d', 16)], '#ffffff') + '</g>')
    aunt = person(fid, cam, -1.25, 3.4, (-300, 200), ISL['AUNT_BODY'] + '<use href="#h_aunt"/>', rig='interior', h=1.6)
    scene = ''.join(sv for _, sv in sorted(items, key=lambda t: -t[0]))
    sun = person(fid, cam, .5, 3.2, (-300, 200), sun_then('annoy', tote=True, camera=False), rig='interior', face='sun')
    sh = contact(cam, .5, 3.2, .45) + CL.ao_line(*cam.p(-W, 0, Z1), *cam.p(W, 0, Z1), 14, .3)
    light = CL.glow(270, 160, 360, '#ffffff', .22, core=False) + CL.glow(-40, 600, 300, '#fff6ea', .22, core=False)
    return CL.compose('interior', bg=scene, shadow=sh, chars=aunt[1] + cnt + sun[1], light=light, ui='', extra_defs=aunt[0] + sun[0], prefix=fid, label=fid)


# ================================================================ E. dive centre on Sairee, looking out to the beach
def dive():
    fid = 'E'
    cam = Cam(horizon=440, f=700, h=1.55)
    d, sk = sky(fid, 460, clouds=((200, 190, .7), (430, 230, .5)))
    d += G(f'{fid}sea', [(0, '#2a8fbd'), (.5, '#3fb4c6'), (1, '#8fe0d6')])
    W, H, Z0, Z1 = 3.6, 3.2, 1.2, 9.5
    view = (sk + f'<rect y="420" width="540" height="60" fill="url(#{fid}sea)"/>' + K.longtail(200, 455, .3) + K.longtail(340, 448, .22, '#7fd3d6')
            + '<path d="M 0,476 C 140,470 300,482 540,472 L 540,520 L 0,520 Z" fill="#f2ece2"/>' + palm(110, 486, .35) + palm(420, 480, .3, True))
    items = [(200, f'<g filter="url(#kt-dof1)">{view}</g>')]
    items.append((99, cam.poly([(-W, 0, Z0), (-W, 0, Z1), (-W, H, Z1), (-W, H, Z0)], '#c9a888')))
    items.append((99, cam.poly([(W, 0, Z0), (W, 0, Z1), (W, H, Z1), (W, H, Z0)], '#b8977a')))
    items.append((99, cam.poly([(-W, H, Z0), (W, H, Z0), (W, H, Z1), (-W, H, Z1)], '#8f6a4a')))
    for k in range(13):                                                                                    # floor planks along Z
        x = -W + k * .6
        items.append((98, cam.poly([(x, 0, Z0), (x + .6, 0, Z0), (x + .6, 0, Z1), (x, 0, Z1)], '#c4a083' if k % 2 else '#b8957a')))
    for z in (2.5, 4.5, 6.5, 8.5):                                                                          # roof beams
        items.append((97, cam.box(-W, W, H - .25, H, z, z + .2, '#6f5442', '#5e4636', '#7d5c40', side_dark='#5e4636')))
    items.append((97, cam.box(-W, -W + .3, 0, H, Z1 - .3, Z1, '#7a5b40', '#6f5442', '#8a6a50')))
    items.append((97, cam.box(W - .3, W, 0, H, Z1 - .3, Z1, '#7a5b40', '#6f5442', '#8a6a50')))
    # left wall: tank rack with tanks standing in a row
    items.append((90, cam.box(-W, -W + .6, .9, 1.0, 2.6, 8.2, '#6f5442', '#5e4636', '#8a6a50')))
    for i, z in enumerate([2.8 + k * .42 for k in range(13)]):
        items.append((z, cam.sprite(-W + .32, 0, z, tank(0, 0, ['#9aa6b8', '#b9c2d0'][i % 2], 1), 90)))
    # right wall: wetsuits on a rail, fins + masks on a shelf
    items.append((89, cam.line((W - .3, 2.2, 2.6), (W - .3, 2.2, 8.4), '#9aa1a8', 3)))
    for i, z in enumerate([2.8 + k * .5 for k in range(11)]):
        items.append((z, cam.sprite(W - .3, 2.2, z, wetsuit(0, 0, ['#1f2b46', '#2c3a54', '#3a2a40'][i % 3], ['#2fb3b8', '#d8655a', '#e88aa8', '#7fd3d6'][i % 4]), 70)))
    items.append((7.6, cam.box(W - .8, W - .2, 0, .6, 6.8, 8.6, '#8a6a50', '#6f5442', '#a8835f')))
    for k, z in enumerate((7.0, 7.4, 7.8, 8.2)):
        items.append((z - .01, cam.sprite(W - .5, .6, z, f'<path d="M -12,0 L 12,0 L 16,-40 L -16,-40 Z" fill="{["#2fb3b8", "#d8655a"][k % 2]}"/>', 90)))
    # schedule board facing the camera (back-left), hanging sign, bench
    board = ('<rect x="0" y="0" width="190" height="140" rx="6" fill="#f8f8f6" stroke="#9aa1a8" stroke-width="5"/>' + txt(95, 28, 'TODAY · วันนี้', 17, '#1a1626', 800)
             + ''.join(txt(14, 56 + k * 22, t, 12.5, c, 700, 'start', EN) for k, (t, c) in enumerate((('08:00 Open Water · SUN', '#2a7f86'), ('11:00 Fun Dive · LAE', '#d8655a'), ('14:00 Snorkel trip', '#3d6fb0'), ('Sea: calm · Wind: OK', '#5a5470')))))
    items.append((9.2, cam.face(-W + .4, 2.3, 9.19, board)))
    items.append((6.4, cam.face(-.9, 3.0, 6.4, '<path d="M 40,0 L 40,30 M 140,0 L 140,30" stroke="#5e4636" stroke-width="4"/><rect x="0" y="30" width="180" height="56" rx="8" fill="#2fb3b8"/>' + txt(90, 68, 'DIVE · ดำน้ำ', 26, '#ffffff', 800))))
    items.append((4.3, cam.box(-2.6, -1.0, 0, .45, 4.0, 4.5, '#8a6a50', '#6f5442', '#a8835f')))
    scene = ''.join(sv for _, sv in sorted(items, key=lambda t: -t[0]))
    lae = person(fid, cam, -.75, 3.3, (-200, 100), ISL['LAE_BODY'] + '<use href="#h_lae"/>', h=1.62)
    sun = person(fid, cam, .8, 3.1, (-200, 100), sun_now('smirktalk'), face='sun')
    thatch = ''.join(f'<path d="M {x},0 L {x + 18},0 L {x + 12},{60 + (x % 3) * 6} L {x + 4},{56 + (x % 3) * 6} Z" fill="{["#8f6a4a", "#a37c58", "#b58d68"][x % 3]}"/>' for x in range(-10, 560, 16))
    sh = contact(cam, -.75, 3.3, .42) + contact(cam, .8, 3.1, .45)
    light = CL.glow(270, 440, 300, '#ffffff', .22, core=False) + CL.shaft([(150, 440), (390, 440), (520, 960), (20, 960)], '#fff8ee', .1, src=(270, 450), end=(270, 900), dust_n=26, seed=7)
    return frame(fid, 'day', scene, sh, [lae, sun], '<rect width="540" height="30" fill="#6a4c34"/>' + thatch, light, defs=d)


# ================================================================ F. viewpoint over Koh Nang Yuan
def viewpoint():
    fid = 'F'
    cam = Cam(horizon=330, f=760, h=1.6)
    d = (G(f'{fid}sky', [(0, '#86a8d8'), (.6, '#ead4dc'), (1, '#f6e2d6')]) + G(f'{fid}sea', [(0, '#3f8fb2'), (.5, '#4aa8bc'), (1, '#2f7f9e')])
         + RG(f'{fid}shal', [(0, '#a9ece0'), (.6, '#6fd6cf'), (1, '#4fb0c0', 0)]))
    bg = (f'<rect width="540" height="340" fill="url(#{fid}sky)"/><circle cx="440" cy="300" r="36" fill="#fff2e6"/><circle cx="440" cy="300" r="90" fill="#fff2e6" opacity=".25"/>'
          + cumulus(130, 140, .8, .8) + cumulus(320, 210, .5, .7) + f'<rect y="330" width="540" height="630" fill="url(#{fid}sea)"/>'
          + '<path d="M 420,332 L 460,332 L 500,520 L 380,520 Z" fill="#fff2e6" opacity=".22"/>')
    # Koh Nang Yuan far below: three islands joined by a sandbar (sprite in metres)
    ny = (f'<ellipse cx="0" cy="0" rx="640" ry="120" fill="url(#{fid}shal)"/>'
          '<path d="M -300,0 C -200,-20 -80,-14 0,-8 C 80,-14 200,-20 300,0 C 200,10 80,8 0,6 C -80,8 -200,10 -300,0 Z" fill="#f6eee0"/>'
          '<path d="M -460,4 C -440,-90 -380,-140 -310,-140 C -250,-140 -210,-90 -200,4 Z" fill="#5f985e"/><path d="M -460,4 C -440,-90 -380,-140 -310,-140 C -350,-110 -380,-60 -386,4 Z" fill="#7fb07a"/>'
          '<path d="M -90,0 C -80,-60 -40,-90 0,-90 C 40,-90 76,-60 86,0 Z" fill="#5f985e"/><path d="M -90,0 C -80,-60 -40,-90 0,-90 C -30,-70 -50,-40 -54,0 Z" fill="#7fb07a"/>'
          '<path d="M 200,4 C 214,-80 270,-126 340,-126 C 410,-126 450,-80 470,4 Z" fill="#4f8a5e"/><path d="M 200,4 C 214,-80 270,-126 340,-126 C 290,-100 268,-60 262,4 Z" fill="#6fa46c"/>'
          + boulder(-470, 8, 70, 40) + boulder(420, 8, 70, 36, 1) + boulder(70, 6, 50, 26)
          + ''.join(f'<rect x="{x}" y="{y}" width="18" height="12" fill="#f4f1ec"/><path d="M {x - 2},{y} l 11,-8 l 11,8 Z" fill="#c87a5e"/>' for x, y in ((-330, -60), (320, -50), (-20, -40), (-250, -30))))
    bg += cam.sprite(-40, -160, 900, ny, 1)
    items = []
    # hillside dropping away + shrubs
    items.append((40, cam.poly([(-40, -20, 30), (40, -20, 30), (40, -4, 8), (-40, -4, 8)], '#4f8a5e')))
    items.append((39, cam.poly([(-40, -4, 8), (40, -4, 8), (40, 0, 5), (-40, 0, 5)], '#6aa477')))
    # timber viewing deck + rail
    for k in range(9):
        z = 1.2 + k * .5
        items.append((z + .5 + 10, cam.poly([(-3, 0, z), (3, 0, z), (3, 0, z + .5), (-3, 0, z + .5)], '#a8835f' if k % 2 else '#9a7656')))
    items.append((5.8, cam.box(-3, 3, .95, 1.05, 5.7, 5.8, '#7a5b40', '#6f5442', '#8a6a50')))
    items.append((5.8, cam.box(-3, 3, .5, .56, 5.72, 5.78, '#7a5b40', '#6f5442', '#8a6a50')))
    for x in (-3, -1.5, 0, 1.5, 3):
        items.append((5.75, cam.box(x - .06, x + .06, 0, 1.05, 5.7, 5.82, '#6f5442', '#5e4636', '#7a5b40')))
    for X, Z, w, h, t in ((-3.6, 3.0, 2.4, 1.6, 0), (3.2, 2.6, 2.6, 1.9, 1), (-2.4, 6.8, 1.6, .8, 1), (2.8, 7.4, 1.4, .7, 0)):
        x0, y0 = cam.p(X - w / 2, 0, Z); x1, _ = cam.p(X + w / 2, 0, Z)
        items.append((Z - .1, boulder(round(x0), round(y0 + cam.ppm(Z) * .2), round(x1 - x0), round(cam.ppm(Z) * h), t)))
    items.append((3.6, cam.sprite(-1.7, .55, 3.6, scooter(0, 0, 1, '#2fb3b8', True), 55)))
    scene = ''.join(sv for _, sv in sorted(items, key=lambda t: -t[0]))
    sun = person(fid, cam, .2, 3.1, (440, 300), sun_now('smirk'), face='sun')
    dog = person(fid, cam, .62, 2.8, (440, 300), ISL['DOG'], h=.6, units=(280, 175))
    sh = contact(cam, .2, 3.1, .45) + contact(cam, .62, 2.8, .38)
    light = CL.glow(440, 300, 300, '#ffd9b8', .34) + CL.shaft([(420, 300), (460, 300), (330, 960), (80, 960)], '#ffe2c8', .12, src=(440, 300), end=(220, 900), dust_n=28, seed=8)
    return frame(fid, 'day', bg + scene, sh, [sun, dog], '', light, defs=d)


# ================================================================ graphics: paper-craft explainers with real numbers
PAPER = '#f4efe6'


def gcard(x, y, w, h, title, lines, accent='#2fb3b8'):
    out = (f'<rect x="{x + 5}" y="{y + 7}" width="{w}" height="{h}" rx="14" fill="#000" opacity=".18"/><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{PAPER}"/>'
           f'<rect x="{x}" y="{y}" width="8" height="{h}" rx="4" fill="{accent}"/>' + txt(x + 22, y + 28, title, 15, '#1a1626', 800, 'start'))
    for i, l in enumerate(lines):
        out += txt(x + 22, y + 52 + i * 21, l, 12.5, '#4a4458', 500, 'start')
    return out


def gtitle(t, sub):
    return (f'<rect x="24" y="40" width="492" height="78" rx="18" fill="#1d2a3d"/>' + txt(270, 76, t, 24, '#ffffff', 800) + txt(270, 102, sub, 12.5, '#9ccbe0', 500))


def g_bg(fid, top='#2a6f9a', bot='#1d4f74'):
    return G(f'{fid}bg', [(0, top), (1, bot)]), f'<rect width="540" height="960" fill="url(#{fid}bg)"/>' + ''.join(f'<path d="M {x},{y} q 10,-4 20,0" stroke="#ffffff" stroke-opacity=".12" stroke-width="1.6" fill="none"/>' for x in range(20, 540, 70) for y in range(140, 940, 90))


def g_map():
    fid = 'G1'
    d, bg = g_bg(fid)
    land = '#e8dcc6'
    main = ('<path d="M -20,130 L 140,130 C 150,240 120,320 150,420 C 170,500 140,600 180,700 C 200,780 170,880 190,960 L -20,960 Z" fill="#000" opacity=".2" transform="translate(7,9)"/>'
            f'<path d="M -20,130 L 140,130 C 150,240 120,320 150,420 C 170,500 140,600 180,700 C 200,780 170,880 190,960 L -20,960 Z" fill="{land}"/>'
            '<path d="M -20,130 L 110,130 C 118,240 96,320 122,420 C 142,500 112,600 150,700 C 172,780 142,880 162,960 L -20,960 Z" fill="#9cc08e"/>')
    def island(cx, cy, s, label, col='#8fbf86'):
        return (f'<polygon points="{K.koh_tao_shape(cx + 6, cy + 8, s)}" fill="#000" opacity=".22"/><polygon points="{K.koh_tao_shape(cx, cy, s)}" fill="{land}"/>'
                f'<polygon points="{K.koh_tao_shape(cx, cy - 3, s * .82)}" fill="{col}"/>' + txt(cx, cy + 150 * s + 20, label, 13, '#ffffff', 700))
    tao = island(330, 260, .55, '')
    pg = f'<ellipse cx="420" cy="560" rx="54" ry="44" fill="{land}"/><ellipse cx="420" cy="556" rx="44" ry="34" fill="#8fbf86"/>' + txt(420, 626, 'เกาะพะงัน', 13, '#ffffff', 700)
    sm = f'<ellipse cx="400" cy="760" rx="84" ry="64" fill="{land}"/><ellipse cx="400" cy="754" rx="70" ry="52" fill="#8fbf86"/>' + txt(400, 850, 'เกาะสมุย', 13, '#ffffff', 700)
    routes = ('<path d="M 150,300 C 210,260 260,250 300,262" stroke="#ffd84a" stroke-width="5" fill="none" stroke-dasharray="10 8"/>'
              '<path d="M 180,860 C 260,820 330,700 400,620" stroke="#ffffff" stroke-width="3" fill="none" stroke-dasharray="6 7" opacity=".7"/>'
              '<path d="M 420,512 C 410,440 370,360 344,330" stroke="#ffffff" stroke-width="3" fill="none" stroke-dasharray="6 7" opacity=".7"/>'
              '<path d="M 400,696 C 430,660 440,630 430,604" stroke="#ffffff" stroke-width="3" fill="none" stroke-dasharray="6 7" opacity=".7"/>'
              '<circle cx="150" cy="300" r="7" fill="#d8655a" stroke="#fff" stroke-width="2"/><circle cx="180" cy="860" r="6" fill="#ffffff"/>'
              '<g transform="translate(232,262) rotate(-10)"><path d="M -20,0 L 20,0 L 14,9 L -15,9 Z" fill="#fff"/><rect x="-9" y="-9" width="18" height="9" fill="#f2eee6"/></g>')
    cards = (gcard(28, 160, 210, 96, 'ชุมพร → เกาะเต่า', ['เส้นหลัก นั่งเรือเร็วราว 1:45 ชม.', 'ขึ้นกับคลื่นลมและชนิดเรือ'], '#ffd84a')
             + gcard(28, 870 - 120, 150, 74, 'ดอนสัก สุราษฎร์ฯ', ['ไปทางเกาะสมุย พะงัน'], '#ffffff')
             + gcard(250, 360, 120, 70, 'ต่อเรือได้', ['สมุย · พะงัน'], '#7fd3d6'))
    noair = (f'<g transform="translate(400,440)"><rect x="-96" y="-26" width="192" height="52" rx="26" fill="{PAPER}"/>'
             '<circle cx="-62" cy="0" r="16" fill="none" stroke="#d8655a" stroke-width="3.4"/><path d="M -73,-11 L -51,11" stroke="#d8655a" stroke-width="3.4"/>'
             '<path d="M -74,3 L -60,-2 L -57,-11 L -54,-11 L -54,-3 L -45,-6 L -45,-3 L -54,1 L -54,8 L -51,10 L -51,12 L -57,9 L -63,11 L -63,9 L -60,7 L -60,2 L -72,6 Z" fill="#1a1626"/>'
             + txt(16, 6, 'เกาะเต่าไม่มีสนามบิน', 14, '#1a1626', 800) + '</g>')
    return CL.compose('day', bg=bg + main + sm + pg + tao + routes, chars=gtitle('เกาะเต่าอยู่ตรงไหน', 'กลางอ่าวไทย · เข้าออกได้ทางเรืออย่างเดียว') + cards + noair, extra_defs=d, prefix=fid, label=fid)


def g_island():
    fid = 'G2'
    d, bg = g_bg(fid, '#e9eef2', '#d6e0e8')
    d += G(f'{fid}sea', [(0, '#5ccbc9'), (1, '#2a8fbd')])
    cx, cy = 290, 470
    plate = (f'<ellipse cx="{cx}" cy="{cy + 120}" rx="230" ry="84" fill="#000" opacity=".12"/><ellipse cx="{cx}" cy="{cy + 100}" rx="230" ry="84" fill="url(#{fid}sea)"/>'
             f'<path d="M {cx - 230},{cy + 100} C {cx - 230},{cy + 146} {cx + 230},{cy + 146} {cx + 230},{cy + 100} L {cx + 230},{cy + 116} C {cx + 230},{cy + 162} {cx - 230},{cy + 162} {cx - 230},{cy + 116} Z" fill="#1f6f8e"/>')
    layers = ''.join(f'<ellipse cx="{cx - 10 + k * 4}" cy="{cy + dy + 8}" rx="{rx}" ry="{ry}" fill="#000" opacity=".12"/><ellipse cx="{cx - 10 + k * 4}" cy="{cy + dy}" rx="{rx}" ry="{ry}" fill="{c}"/>'
                     for k, (rx, ry, dy, c) in enumerate(((180, 68, 96, '#efe6d8'), (166, 62, 82, '#8fbf86'), (140, 52, 62, '#7fb07a'), (112, 42, 40, '#6fa46c'), (82, 30, 18, '#5f985e'), (50, 20, -4, '#4f8a5e'), (22, 9, -24, '#457c52'))))
    pins = ''
    for (x, y, t) in ((-150, 92, 'หาดทรายรี'), (-120, 120, 'ท่าเรือแม่หาด'), (40, 150, 'อ่าวโฉลกบ้านเก่า'), (150, 80, 'อ่าวโตนด')):
        pins += f'<circle cx="{cx + x}" cy="{cy + y}" r="5" fill="#d8655a" stroke="#fff" stroke-width="2"/>'
        pins += f'<rect x="{cx + x - 54}" y="{cy + y + 10}" width="108" height="22" rx="11" fill="{PAPER}"/>' + txt(cx + x, cy + y + 26, t, 11, '#1a1626', 700)
    road = f'<path d="M {cx - 120},{cy + 112} C {cx - 70},{cy + 96} {cx - 40},{cy + 90} {cx - 30},{cy + 64} C {cx - 20},{cy + 40} {cx - 70},{cy + 34} {cx - 40},{cy + 14} C {cx - 10},{cy} {cx + 30},{cy + 14} {cx + 10},{cy - 14}" stroke="#f6eee0" stroke-width="5" fill="none"/>'
    cards = (gcard(28, 150, 230, 94, '≈ 21 ตร.กม.', ['ทั้งเกาะ เดินรอบไม่ได้ในวันเดียว', 'เพราะส่วนใหญ่เป็นภูเขาและเนิน'], '#5f985e')
             + gcard(282, 150, 230, 94, 'คนอยู่ประจำหลักพัน', ['ตัวเลขทางการเก่าและต่างกัน', 'บวกแรงงานในธุรกิจท่องเที่ยว'], '#d8655a')
             + gcard(28, 700, 484, 120, 'ถนนบนเกาะ', ['ชันและแคบ หลายเส้นเป็นปูนหรือดินลูกรัง', 'มอเตอร์ไซค์คือพาหนะหลัก ต้องใส่หมวกกันน็อก',
                                                    'บ้านเช่าหลายหลังอยู่บนเนิน ขนของขึ้นบ้านคือเรื่องใหญ่'], '#ffd84a'))
    return CL.compose('day', bg=bg + plate + layers + road + pins, chars=gtitle('เกาะเต่ามีอะไรบ้าง', 'เกาะเล็ก แต่ทั้งชันทั้งคดเคี้ยว') + cards, extra_defs=d, prefix=fid, label=fid)


def g_parcel():
    fid = 'G3'
    d, bg = g_bg(fid, '#e9eef2', '#dfe6ec')
    steps = [('โกดังกรุงเทพ', 'ของออกจากร้าน', '#5a6c8e'), ('รถขนส่ง', 'ขึ้นรถลงใต้', '#d8655a'), ('ท่าเรือชุมพร', 'รอเรือรอบถัดไป', '#2fb3b8'),
             ('ข้ามทะเล', 'ถ้าคลื่นแรง เรืออาจงด', '#3d6fb0'), ('ท่าเรือแม่หาด', 'ถึงเกาะแล้ว', '#2fb3b8'), ('ถึงบ้าน', 'ส่งต่อด้วยรถกระบะหรือมอเตอร์ไซค์', '#7a5ab8')]
    out = '<path d="M 70,190 L 70,800" stroke="#1a1626" stroke-width="3" stroke-dasharray="6 7"/>'
    for i, (t, sub, c) in enumerate(steps):
        y = 200 + i * 118
        out += f'<circle cx="70" cy="{y}" r="22" fill="{c}"/>' + txt(70, y + 6, str(i + 1), 16, '#ffffff', 800)
        out += gcard(110, y - 40, 400, 82, t, [sub], c)
    storm = ('<g transform="translate(380,554)"><path d="M -40,10 C -40,-10 -20,-20 0,-14 C 10,-30 40,-28 44,-6 C 60,-4 62,14 46,18 L -36,18 C -50,18 -52,10 -40,10 Z" fill="#9aa6b8"/>'
             '<path d="M -10,22 L -18,40 M 6,22 L -2,40 M 22,22 L 14,40" stroke="#3d6fb0" stroke-width="3" stroke-linecap="round"/></g>')
    note = gcard(28, 870, 484, 66, 'ช่วงมรสุม (ราว พ.ย.–ธ.ค.)', ['เรืองดวิ่งเป็นช่วง ๆ ของบนเกาะจึงมาช้าหรือขาดได้'], '#d8655a')
    return CL.compose('day', bg=bg, chars=gtitle('พัสดุเดินทางมาเกาะยังไง', 'ทุกอย่างต้องนั่งเรือมาเหมือนคุณ') + out + storm + note, extra_defs=d, prefix=fid, label=fid)


def g_season():
    fid = 'G4'
    d, bg = g_bg(fid)
    months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    kind = ['g', 'g', 'g', 'g', 'o', 'o', 'g', 'g', 'o', 'o', 'r', 'r']
    col = {'g': '#7fb07a', 'o': '#f0b46a', 'r': '#d8655a'}
    out = ''
    for i, (m, k) in enumerate(zip(months, kind)):
        a = -90 + i * 30
        r0, r1 = 90, 190
        a0, a1 = math.radians(a - 14), math.radians(a + 14)
        cx, cy = 270, 400
        pts = [(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)), (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1)), (cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))]
        out += '<path d="M ' + ' L '.join(f'{x:.0f},{y:.0f}' for x, y in pts) + f' Z" fill="{col[k]}" stroke="#1d4f74" stroke-width="3"/>'
        am = math.radians(a)
        out += txt(cx + 140 * math.cos(am), cy + 140 * math.sin(am) + 5, m, 13, '#1a1626', 800)
    out += '<circle cx="270" cy="400" r="84" fill="#1d2a3d"/>' + txt(270, 394, 'ปฏิทิน', 18, '#ffffff', 800) + txt(270, 418, 'คลื่นลมเกาะเต่า', 12, '#9ccbe0', 500)
    cards = (gcard(28, 620, 484, 70, '● ช่วงทะเลสวย (ราว ม.ค.–เม.ย.)', ['แดดดี ทะเลเรียบ คนมาเที่ยวและเรียนดำน้ำเยอะ'], '#7fb07a')
             + gcard(28, 704, 484, 70, '● ช่วงกลาง ๆ', ['มีฝนเป็นพัก ๆ ยังเดินทางได้เกือบตลอด'], '#f0b46a')
             + gcard(28, 788, 484, 92, '● ช่วงมรสุม (ราว พ.ย.–ธ.ค.)', ['ฝนหนัก คลื่นแรง เรืออาจงดวิ่ง', 'แต่ละแหล่งระบุช่วงต่างกันเล็กน้อย'], '#d8655a'))
    return CL.compose('day', bg=bg, chars=gtitle('อยู่เกาะต้องดูฟ้าดูลม', 'ช่วงไหนทะเลสวย ช่วงไหนเรืองด') + out + cards, extra_defs=d, prefix=fid, label=fid)


def g_cost():
    fid = 'G5'
    d, bg = g_bg(fid, '#e9eef2', '#dfe6ec')
    rows = [('บังกะโลพัดลม', '~4,000 บาท/เดือน', 4), ('สตูดิโอแอร์', '12,000–18,000 บาท', 15), ('เช่ามอเตอร์ไซค์', '2,500–3,500 บาท/เดือน', 3),
            ('งบนักเรียนดำน้ำ', '15,000–20,000 บาท/เดือน', 17.5), ('งบอยู่สบาย ๆ', '35,000–60,000 บาท/เดือน', 47)]
    out = ''
    for i, (t, v, n) in enumerate(rows):
        y = 190 + i * 96
        w = 40 + n / 60 * 380
        out += txt(36, y, t, 15, '#1a1626', 800, 'start') + txt(504, y, v, 13, '#4a4458', 700, 'end')
        out += f'<rect x="36" y="{y + 12}" width="468" height="26" rx="13" fill="#d6dde4"/><rect x="36" y="{y + 12}" width="{w:.0f}" height="26" rx="13" fill="{["#2fb3b8", "#3d6fb0", "#7a5ab8", "#d8655a", "#c87a5e"][i]}"/>'
    cards = (gcard(28, 680, 484, 94, 'ทำไมแพงกว่าฝั่ง', ['ของเกือบทุกอย่างต้องขนมาทางเรือ', 'แต่ค่าแรงบนเกาะไม่ได้สูงตาม'], '#d8655a')
             + gcard(28, 790, 484, 120, 'คนที่อยู่ได้นาน มักจะ…', ['มีงานออนไลน์หรือมีเงินเก็บก่อนมา', 'หางานเสริมบนเกาะ ส่วนใหญ่เป็นงานบริการ', 'ตัวเลขจากรีวิวผู้ใช้ ต่างกันตามไลฟ์สไตล์'], '#2fb3b8'))
    return CL.compose('day', bg=bg, chars=gtitle('อยู่เกาะเต่าเดือนละเท่าไหร่', 'ค่าครองชีพแพง ค่าแรงไม่แพง') + out + cards, extra_defs=d, prefix=fid, label=fid)


def g_dive():
    fid = 'G6'
    d, bg = g_bg(fid, '#2a8fbd', '#123f5c')
    out = ''
    stats = [('25+', 'จุดดำน้ำรอบเกาะ'), ('หลายสิบ', 'ร้านและโรงเรียนสอนดำน้ำ'), ('~4 วัน', 'เรียนใบดำน้ำขั้นแรก')]
    for i, (n, t) in enumerate(stats):
        x = 28 + i * 164
        out += f'<rect x="{x + 4}" y="{150 + 6}" width="152" height="120" rx="16" fill="#000" opacity=".2"/><rect x="{x}" y="150" width="152" height="120" rx="16" fill="{PAPER}"/>'
        out += txt(x + 76, 206, n, 30, '#2a7f86', 800) + txt(x + 76, 238, t, 11.5, '#4a4458', 600)
    ladder = [('นักเรียนดำน้ำ', 'เรียนใบแรก ดำได้ไม่เกิน 18 ม.'), ('ผู้ช่วยครู', 'ฝึกงานกับร้านดำน้ำหลายเดือน'), ('ครูสอนดำน้ำ', 'สอบเป็นครู รับสอนนักเรียนเอง')]
    out += txt(270, 330, 'เส้นทางของซัน: จากนักเรียนสู่ครู', 17, '#ffffff', 800)
    for i, (t, s) in enumerate(ladder):
        y = 370 + i * 130
        out += gcard(110, y, 380, 86, t, [s], ['#7fd3d6', '#2fb3b8', '#ffd84a'][i])
        out += f'<circle cx="64" cy="{y + 43}" r="26" fill="{["#7fd3d6", "#2fb3b8", "#ffd84a"][i]}"/>' + txt(64, y + 50, str(i + 1), 20, '#1a1626', 800)
        if i < 2:
            out += f'<path d="M 64,{y + 72} L 64,{y + 128}" stroke="#ffffff" stroke-width="3" stroke-dasharray="5 6"/>'
    out += gcard(28, 790, 484, 96, 'เพื่อนบ้านจากทั่วโลก', ['คนมาเรียนและทำงานดำน้ำจากหลายประเทศ', 'ภาษาอังกฤษเลยกลายเป็นภาษาประจำวัน'], '#d8655a')
    return CL.compose('day', bg=bg, chars=gtitle('ทำไมเกาะเต่าถึงดังเรื่องดำน้ำ', 'และอาชีพใหม่ของซัน') + out, extra_defs=d, prefix=fid, label=fid)


SHOTS = [
    (road, 'ถนนชันเหนือท่าเรือแม่หาด · เช้า', 'มุมกล้องจริง ถนนไต่เนินขึ้นไป ห้องแถวขั้นบันไดตามความชันพร้อมกันสาด ป้ายยื่น ชัตเตอร์ แอร์ ร้านดำน้ำ มินิมาร์ท ร้านซักผ้า ร้านอาหาร ร้านเช่ามอเตอร์ไซค์ ร้านกาแฟ · มอเตอร์ไซค์จอดหันหน้าเข้าฟุตบาท · เสาไฟกับสายไฟพาดข้ามถนน · กำแพงกันดินกับเฟื่องฟ้า ลีลาวดี มะพร้าว โขดหิน'),
    (pier, 'ท่าเรือแม่หาด · วันย้ายบ้าน', 'ยืนบนสะพานท่าเรือหันกลับเข้าหาฝั่ง · พื้นไม้ หลักผูกเรือ เสาไฟ ซุ้มขายตั๋ว นักท่องเที่ยว · ร้านริมฝั่ง รถกระบะแท็กซี่ บ้านบนเนิน · เรือเฟอร์รี่จอดขวา เรือหางยาวซ้าย · ซันกับกองกล่องจริงแบบสามมิติ'),
    (K.bungalow, 'บ้านเช่าบนเนิน · คืนแรก', 'ฉากที่เจ้าของช่องบอกว่าเกือบโอเค เก็บไว้ตามเดิม'),
    (shop, 'ร้านโชห่วยบนเกาะ', 'ห้องจริงมีพื้น ผนัง เพดาน หลอดไฟ · ชั้นสินค้าผนังหลังกับผนังซ้าย ตู้แช่เครื่องดื่มผนังขวา · ขนมห้อย พัดลม เคาน์เตอร์มีเครื่องคิดเงิน กล้วย ป้าย "ของสดมาพรุ่งนี้ (ถ้าเรือมา)"'),
    (dive, 'ร้านดำน้ำริมหาดทรายรี', 'มองจากในร้านออกไปทะเล · ชั้นถังอากาศเรียงตามผนังซ้าย ราวชุดดำน้ำผนังขวา ตีนกบ ม้านั่ง คานหลังคา ป้ายแขวน กระดานตารางวันนี้'),
    (viewpoint, 'จุดชมวิวเกาะนางยวน · เย็น', 'ยืนบนลานไม้บนยอดเขา มองลงไปเห็นเกาะนางยวนสามเกาะกับสันทราย · ราวไม้ โขดหินแกรนิต มอเตอร์ไซค์ ซันกับหมา'),
    (g_map, 'กราฟิก 1 · เกาะเต่าอยู่ตรงไหน', 'ชุมพรไปเกาะเต่าเรือเร็วราว 1:45 ชม. · เส้นทางต่อเรือสมุย พะงัน · ไม่มีสนามบิน'),
    (g_island, 'กราฟิก 2 · เกาะเต่ามีอะไรบ้าง', '≈21 ตร.กม. · หาดทรายรี ท่าเรือแม่หาด อ่าวโฉลกบ้านเก่า อ่าวโตนด · ถนนชัน มอเตอร์ไซค์ บ้านบนเนิน'),
    (g_parcel, 'กราฟิก 3 · พัสดุเดินทางมาเกาะยังไง', '6 ขั้นจากโกดังถึงบ้าน · จุดที่เรืองดช่วงมรสุม'),
    (g_season, 'กราฟิก 4 · ปฏิทินคลื่นลม', 'วงล้อ 12 เดือน · ช่วงทะเลสวย ช่วงกลาง ช่วงมรสุม'),
    (g_cost, 'กราฟิก 5 · ค่าครองชีพ', 'ค่าเช่า มอเตอร์ไซค์ งบต่อเดือน · ทำไมแพงกว่าฝั่ง · คนที่อยู่ได้นานทำยังไง'),
    (g_dive, 'กราฟิก 6 · ทำไมดังเรื่องดำน้ำ', 'จุดดำน้ำ 25+ · ร้านดำน้ำหลายสิบร้าน · เส้นทางของซันจากนักเรียนสู่ครู'),
]


def build():
    figs = ''
    for i, (fn, t, note) in enumerate(SHOTS, 1):
        figs += f'<figure>{fn()}<figcaption><span class="n">{i:02d}</span> <b>{t}</b><span class="note">{note}</span></figcaption></figure>'
    page = open(os.path.join(HERE, 'locations.html')).read()
    head = page[:page.index('<div class="wrap">')]
    head = head.replace('</defs></svg>', '<filter id="kt-dof1" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.4"/></filter></defs></svg>', 1) if 'kt-dof1' not in head else head
    out = head + f'''<div class="wrap">
  <h1>ฉาก EP.01 เกาะเต่า รอบ 3<span>สร้างผ่านกล้องมุมมองจริงตัวเดียวทั้งฉาก · กราฟิก 6 แบบพร้อมข้อมูลจริง</span></h1>
  <div class="grid">{figs}</div>
</div>
'''
    open(os.path.join(HERE, 'locations.html'), 'w').write(out)
    print(len(out))


if __name__ == '__main__':
    build()
