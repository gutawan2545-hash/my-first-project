"""EP.01 round 5: islander outfit (Hawaiian shirt), the earlier bedroom restored, true-scale scooters,
a grand sunset vista with layered clouds and a proper sea, new clouds everywhere, and explainer graphics
rebuilt as real objects in the story world (map on a table, parcel with route stickers, wall calendar, cost notepad).
Run: python3 style5.py -> scenes_v5.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
import kt_scenes as K
import style4 as S4
from style3 import wood_planks, jar
from style4 import (beam_set, fine_dust, wall_shadow, buoy, net, shell_chime, lifebuoy, driftwood_sign, flipflops_rack, coconut,
                    tag, step, callout, subs, char, compose, sun_then, uid, DEFS, EYE)
from scenes import palm, boulder
ISL = K.ISL
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'

# ================================================================ Sun's islander outfit: open hibiscus shirt over a white tank
HAWAII = ('<pattern id="hawaii" width="44" height="44" patternUnits="userSpaceOnUse">'
          '<rect width="44" height="44" fill="#1f4f7e"/>'
          '<path d="M 4,30 q 10,-16 22,-6 q -10,6 -22,6 Z" fill="#2f8f6a"/><path d="M 26,8 q 14,-6 16,8 q -10,-2 -16,-8 Z" fill="#2f8f6a"/>'
          + ''.join(f'<ellipse cx="14" cy="14" rx="4.4" ry="7" fill="#f0846e" transform="rotate({a} 14 14)"/>' for a in (0, 72, 144, 216, 288))
          + '<circle cx="14" cy="14" r="2.4" fill="#ffe2a6"/>'
          + ''.join(f'<ellipse cx="34" cy="34" rx="3.4" ry="5.4" fill="#f8efe2" transform="rotate({a} 34 34)"/>' for a in (0, 72, 144, 216, 288))
          + '<circle cx="34" cy="34" r="1.8" fill="#f0846e"/></pattern>')
SK, SKS, SKH = '#fbe7d8', '#efc7b0', '#fff5ee'
SHORTS_PRINT = ''.join(f'<path d="M {x},{y} q 7,-5 14,0 q 7,5 14,0" stroke="#bfe8ea" stroke-width="2" fill="none" opacity=".7"/>' for x, y in ((-40, 262), (-30, 300), (6, 270), (12, 310), (-20, 324)))
SUN_ISLAND2 = (ISL['shorts']('#2a7f86', '#3a9aa0', '#1f6268', SK, SKS, SHORTS_PRINT)
               + '<path d="M -48,236 L -44,336 M 48,236 L 44,336" stroke="#f4efe6" stroke-width="4"/>'
               + ISL['flipflops']('#e8735f', '#e9e4dc', SK, SKS)
               + ISL['arms'](SK, SKS, SKH)
               + ISL['tank']('#f4f1ec', '#ffffff', '#ddd8ce')
               # open shirt panels + short sleeves, patterned, block-shaded
               + '<path d="M -12,49 C -28,51 -42,56 -47,66 L -58,118 L -40,124 L -42,240 L -16,240 L -10,110 C -12,90 -14,70 -12,49 Z" fill="url(#hawaii)"/>'
               + '<path d="M 12,49 C 28,51 42,56 47,66 L 58,118 L 40,124 L 42,240 L 16,240 L 10,110 C 12,90 14,70 12,49 Z" fill="url(#hawaii)"/>'
               + '<path d="M 12,49 C 28,51 42,56 47,66 L 58,118 L 40,124 L 42,240 L 26,240 C 28,180 26,100 20,52 Z" fill="#0b1a2c" opacity=".28"/>'
               + '<path d="M -47,66 C -42,56 -30,52 -20,50 C -26,74 -30,110 -30,240 L -42,240 L -40,124 L -58,118 Z" fill="#ffffff" opacity=".1"/>'
               + '<path d="M -58,112 L -40,118 L -40,124 L -58,118 Z M 58,112 L 40,118 L 40,124 L 58,118 Z" fill="#163b5e"/>'
               + '<path d="M -12,49 L -24,54 L -16,80 L -9,62 Z" fill="#2a6596"/><path d="M 12,49 L 24,54 L 16,80 L 9,62 Z" fill="#163b5e"/>'
               # shell + bead necklace, rope bracelet
               + '<path d="M -10,52 C -6,66 6,66 10,52" stroke="#c9b08a" stroke-width="1.4" fill="none"/>'
               + ''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="{c}"/>' for x, y, c in ((-8, 57, '#2fb3b8'), (-4, 61, '#f4efe6'), (4, 61, '#e8735f'), (8, 57, '#2fb3b8')))
               + '<path d="M -3,63 C -3,58 3,58 3,63 L 0,70 Z" fill="#f6eadb"/>'
               + '<path d="M -56,226 L -41,226" stroke="#a07a58" stroke-width="5"/>')
NECK = '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'


def sun_island(head='smirk'):
    return R.tanify(SUN_ISLAND2) + f'<use href="#{R.HEADS[head]}_t"/>' + NECK


# ================================================================ skies + sea (painterly, layered)
def cloud_bank(x, y, w, h, lit, mid, shade, seed=1, sun_left=False):
    """Long soft cloud bank: bumpy lit top, soft underside, vertical gradient, rim light on the sun side."""
    rnd = random.Random(seed)
    g = uid('cg')
    n = max(6, int(w / 26))
    pts = []
    for i in range(n + 1):
        t = i / n
        bump = h * (.35 + .65 * math.sin(math.pi * t) ** .8) * rnd.uniform(.7, 1.0)
        pts.append((x + w * t, y - bump))
    top = f'M {x},{y} ' + ' '.join(f'Q {(x0 + x1) / 2:.0f},{min(y0, y1) - h * rnd.uniform(.15, .35):.0f} {x1:.0f},{y1:.0f}' for (x0, y0), (x1, y1) in zip([(x, y)] + pts[:-1], pts))
    shape = top + f' L {x + w},{y} C {x + w * .7:.0f},{y + h * .22:.0f} {x + w * .3:.0f},{y + h * .26:.0f} {x},{y} Z'
    gx1, gx2 = (0, 1) if sun_left else (1, 0)
    defs = (f'<linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lit}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{shade}"/></linearGradient>'
            f'<linearGradient id="{g}r" x1="{gx2}" y1="0" x2="{gx1}" y2="0"><stop offset="0" stop-color="{lit}" stop-opacity=".9"/><stop offset=".6" stop-color="{lit}" stop-opacity="0"/></linearGradient>')
    return (f'<defs>{defs}</defs><g filter="url(#s5cloud)"><path d="{shape}" fill="url(#{g})"/>'
            f'<path d="{top}" fill="none" stroke="url(#{g}r)" stroke-width="3" opacity=".8"/></g>')


def wisps(y0, y1, color, n=7, seed=3):
    rnd = random.Random(seed)
    return ''.join(f'<ellipse cx="{rnd.uniform(-40, 580):.0f}" cy="{rnd.uniform(y0, y1):.0f}" rx="{rnd.uniform(80, 200):.0f}" ry="{rnd.uniform(3, 8):.0f}" fill="{color}" opacity="{rnd.uniform(.35, .7):.2f}" filter="url(#s5wisp)"/>' for _ in range(n))


def day_sky(h=430):
    return (f'<rect width="540" height="{h}" fill="url(#s5dayg)"/>' + wisps(40, 180, '#f4f8fc', 6, 4)
            + cloud_bank(-30, 230, 260, 60, '#ffffff', '#eef3f8', '#c9d4e4', 2) + cloud_bank(330, 190, 240, 52, '#ffffff', '#eef3f8', '#c9d4e4', 5)
            + cloud_bank(150, 300, 200, 34, '#ffffff', '#e8eef6', '#cbd5e4', 8))


def sea_band(y0, y1, sunx=None, seed=5):
    rnd = random.Random(seed)
    out = f'<rect y="{y0}" width="540" height="{y1 - y0}" fill="url(#s5sea)"/><rect y="{y0}" width="540" height="10" fill="#e9f2f2" opacity=".55" filter="url(#s5wisp)"/>'
    for i in range(70):
        t = (i / 70) ** 1.6
        y = y0 + 6 + t * (y1 - y0 - 8)
        w = 6 + t * 60
        x = rnd.uniform(-20, 560)
        out += f'<path d="M {x:.0f},{y:.0f} q {w / 2:.0f},{-1 - t * 3:.1f} {w:.0f},0" stroke="#ffffff" stroke-opacity="{.18 + t * .25:.2f}" stroke-width="{.8 + t * 1.6:.1f}" fill="none"/>'
    if sunx is not None:                                       # soft broken path of reflected light
        for i in range(60):
            t = rnd.random() ** 1.3
            y = y0 + 4 + t * (y1 - y0) * .8
            spread = 14 + t * 110
            x = sunx + rnd.uniform(-spread, spread)
            out += f'<rect x="{x:.0f}" y="{y:.0f}" width="{4 + t * 22:.0f}" height="{1 + t * 2:.1f}" rx="1" fill="#fff2de" opacity="{.35 + (1 - t) * .4:.2f}"/>'
    return out


S5DEFS = (HAWAII
          + '<filter id="s5cloud" x="-20%" y="-40%" width="140%" height="180%"><feGaussianBlur stdDeviation="1.6"/></filter>'
          + '<filter id="s5wisp" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="4"/></filter>'
          + '<filter id="s5haze" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="8"/></filter>'
          + '<linearGradient id="s5dayg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5f9fd6"/><stop offset=".6" stop-color="#a9d0ec"/><stop offset="1" stop-color="#e6f1f6"/></linearGradient>'
          + '<linearGradient id="s5sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7fb8cc"/><stop offset=".25" stop-color="#3f93b4"/><stop offset="1" stop-color="#1f6a90"/></linearGradient>'
          + '<linearGradient id="s5dusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3e4f8e"/><stop offset=".35" stop-color="#8a7ab8"/><stop offset=".62" stop-color="#e6a6b0"/><stop offset=".82" stop-color="#f8c8a8"/><stop offset="1" stop-color="#fde2c6"/></linearGradient>'
          + '<linearGradient id="s5duskSea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d8a8b8"/><stop offset=".15" stop-color="#8a8ab8"/><stop offset=".6" stop-color="#3e5f8e"/><stop offset="1" stop-color="#28466e"/></linearGradient>'
          + '<radialGradient id="s5sunglow"><stop offset="0" stop-color="#fff4e2"/><stop offset=".25" stop-color="#ffe0c0" stop-opacity=".8"/><stop offset="1" stop-color="#ffc8a8" stop-opacity="0"/></radialGradient>'
          + '<radialGradient id="s5shal"><stop offset="0" stop-color="#b8f0e2"/><stop offset=".55" stop-color="#6fd0cc" stop-opacity=".9"/><stop offset="1" stop-color="#3f93b4" stop-opacity="0"/></radialGradient>')


# ================================================================ 1. street in front of the dive shop (new sky, true-scale scooter, islander outfit)
def street():
    fid = 'V1'
    PPM = 1.38 * 560 / 1.75                                            # Sun's pixels per metre in this shot
    sky = day_sky(420)
    sea = sea_band(330, 400)[0:0] + '<rect x="0" y="330" width="540" height="70" fill="url(#s5sea)"/>' + K.longtail(120, 360, .26) + K.longtail(330, 352, .2, '#7fd3d6')
    hill = '<path d="M -20,400 C 80,330 200,320 300,350 C 380,372 460,340 560,320 L 560,420 L -20,420 Z" fill="#6aa477"/>' + palm(60, 410, .55) + palm(480, 404, .5, True, 1)
    shopfront = (f'<rect x="0" y="230" width="540" height="430" fill="#f2ebe0"/><rect x="0" y="230" width="540" height="14" fill="#cfc6b8"/>'
                 '<rect x="20" y="300" width="230" height="300" fill="#4a3c36"/><rect x="290" y="300" width="230" height="300" fill="#4a3c36"/>'
                 + ''.join(K.tank(30 + i * 30, 590, '#9aa6b8' if i % 2 else '#b9c2d0', 1.0) for i in range(7))
                 + ''.join(K.wetsuit(318 + i * 34, 330, ['#1f2b46', '#2c3a54', '#3a2a40'][i % 3], ['#2fb3b8', '#e8735f', '#e88aa8'][i % 3]) for i in range(6))
                 + '<path d="M 0,276 L 540,276 L 528,300 L 12,300 Z" fill="#2fb3b8"/>' + ''.join(f'<path d="M {12 + k * 24},300 l 12,10 l 12,-10" fill="#2fb3b8"/>' for k in range(22))
                 + '<rect x="120" y="244" width="300" height="30" rx="4" fill="#1d2a3d"/>' + f'<text x="270" y="266" {EN} font-size="18" font-weight="800" fill="#fff" text-anchor="middle">TAO REEF DIVERS · ดำน้ำ</text>'
                 + lifebuoy(470, 360, 28) + flipflops_rack(30, 330) + buoy(250, 330, 12) + buoy(272, 344, 10, '#2fb3b8'))
    wires = ''.join(f'<path d="M -10,{150 + i * 7} Q 270,{210 + i * 9} 560,{120 + i * 6}" stroke="#2a2c34" stroke-width="{1.7 - i * .2:.1f}" fill="none" opacity=".85"/>' for i in range(5))
    pole = '<rect x="500" y="0" width="16" height="640" fill="#b9b4ae"/><rect x="500" y="0" width="6" height="640" fill="#d6d1ca"/><rect x="470" y="130" width="76" height="8" fill="#8a857e"/>'
    bouga = K.bougainvillea(-20, 200, 140, 90, 4) + K.bougainvillea(420, 210, 140, 70, 8)
    back = f'<g filter="url(#s4dof2)">{sky}{sea}{hill}</g><g filter="url(#s4dof)">{shopfront}{bouga}</g>' + wires + pole
    road = '<rect y="640" width="540" height="320" fill="#c9c2b6"/><path d="M 0,640 L 540,640" stroke="#a69e94" stroke-width="5"/><rect y="640" width="540" height="40" fill="#d8d2c6"/>'
    # scooter ~1.8 m long, parked a step behind Sun (depth factor .78), so it is cropped by the frame
    sc_scale = PPM * .78 / 55
    scoot = f'<g transform="translate(470,{1006 - 70:.0f}) scale({-sc_scale:.2f},{sc_scale:.2f})">{K.scooter(0, -15, 1, "#2fb3b8")}</g>'
    dog_tr = 'translate(96,742) scale(.66)'
    s_tr = 'translate(232,330) scale(1.38)'
    leaves = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .45:.0f}" fill="#fff6e4" opacity=".28" filter="url(#s4soft)" style="mix-blend-mode:screen"/>' for x, y, rx in ((90, 700, 50), (230, 760, 60), (420, 720, 44), (330, 880, 56), (60, 900, 40)))
    bd, bs, bc = beam_set(fid, [[(380 + k * 36, 0), (404 + k * 36, 0), (120 + k * 36, 960), (96 + k * 36, 960)] for k in range(5)], '#fff6e4', .14)
    light = bs + leaves + CL.glow(560, -40, 380, '#fff6e4', .22, core=False) + fine_dust((60, 0, 540, 960), 220, 12, '#fffaf0', clip=bc)
    chars = [char(fid, ISL['DOG'], dog_tr, (560, -40), (96, 840), 'warm', None), char(fid, sun_island('smirk'), s_tr, (560, -40), (232, 500), 'warm', 'sun')]
    sh = CL.contact_shadow(232, 1006, 80) + CL.contact_shadow(96, 860, 62, 10) + CL.contact_shadow(470, 940, 150, 14, .7)
    ui = tag('ปัจจุบัน · เกาะเต่า') + subs('ผู้ชายคนนี้ชื่อซัน/ครูสอนดำน้ำบนเกาะเต่า', 'This is Sun,/a dive instructor on Koh Tao.')
    return compose(fid, 'warm', back + road, sh, [chars[0]] + [(chars[1][0], scoot + chars[1][1])], '', light, '', ui, bd + S5DEFS)


# ================================================================ 2. the earlier bedroom (owner preferred it), with fine dust + new labels
def bedroom():
    svg = K.bungalow()
    dust = fine_dust((260, 120, 540, 960), 200, 5, '#dfe8ff') + fine_dust((150, 300, 460, 700), 90, 6, '#fff0d8')
    ui = tag('คืนแรกในบ้านเช่า') + callout(250, 60, 'รูมเมทคนแรก', 226, 168, 150, '#7a5ab8') + subs('รูมเมทคนแรก/มาเองไม่ต้องหา', 'The first roommate/moved in on its own.') + EYE
    svg = svg.replace('<g id="L-post"', f'<g id="L-dust">{dust}</g><g id="L-post"', 1)
    return svg.replace('<g id="L-ui"></g>', f'<g id="L-ui">{ui}</g>', 1)


# ================================================================ 3. the grand vista: Koh Nang Yuan at sunset
def vista():
    fid = 'V3'
    sunx, suny, hz = 400, 430, 470
    sky = (f'<rect width="540" height="{hz + 4}" fill="url(#s5dusk)"/>'
           + wisps(60, 200, '#c8b8e8', 8, 11) + wisps(200, 330, '#f8c8c0', 6, 12)
           + f'<circle cx="{sunx}" cy="{suny}" r="190" fill="url(#s5sunglow)"/><circle cx="{sunx}" cy="{suny}" r="26" fill="#fff8ec"/>'
           + cloud_bank(-60, 210, 330, 70, '#ffd8c4', '#c49ac0', '#8a7aa8', 21, False)
           + cloud_bank(250, 150, 360, 80, '#ffe0c8', '#d0a0c0', '#8a7aa8', 22, True)
           + cloud_bank(60, 330, 260, 40, '#ffd0b8', '#d8a8bc', '#a088b0', 23, False)
           + cloud_bank(330, 380, 240, 30, '#ffe4cc', '#e8b4bc', '#b894b4', 24, True))
    far = (f'<path d="M -20,{hz} C 40,{hz - 18} 110,{hz - 22} 170,{hz - 8} L 190,{hz} Z" fill="#8a80a8" opacity=".85" filter="url(#s5cloud)"/>'
           f'<path d="M 470,{hz} C 500,{hz - 14} 540,{hz - 16} 560,{hz - 10} L 560,{hz} Z" fill="#8a80a8" opacity=".8"/>')
    sea = (f'<rect y="{hz}" width="540" height="{960 - hz}" fill="url(#s5duskSea)"/>' + f'<rect y="{hz - 6}" width="540" height="16" fill="#f8d0c0" opacity=".55" filter="url(#s5haze)"/>')
    rnd = random.Random(9)
    for i in range(90):
        t = (i / 90) ** 1.6
        y = hz + 6 + t * 420
        w = 8 + t * 70
        x = rnd.uniform(-20, 560)
        sea += f'<path d="M {x:.0f},{y:.0f} q {w / 2:.0f},{-1 - t * 3:.1f} {w:.0f},0" stroke="#f8d8d8" stroke-opacity="{.12 + t * .2:.2f}" stroke-width="{.8 + t * 1.4:.1f}" fill="none"/>'
    for i in range(110):
        t = rnd.random() ** 1.4
        y = hz + 3 + t * 380
        spread = 10 + t * 120
        x = sunx + rnd.uniform(-spread, spread)
        sea += f'<rect x="{x:.0f}" y="{y:.0f}" width="{4 + t * 26:.0f}" height="{1 + t * 2.2:.1f}" rx="1" fill="#fff0dc" opacity="{.3 + (1 - t) * .5:.2f}"/>'
    def peak(x0, x1, top, seed):
        r2 = random.Random(seed)
        n = 7
        pts = [(x0, 6)]
        for i in range(1, n):
            t = i / n
            pts.append((x0 + (x1 - x0) * t, 6 - top * (math.sin(math.pi * t) ** .7) * r2.uniform(.78, 1.05)))
        pts.append((x1, 6))
        d = 'M ' + ' L '.join(f'{px:.0f},{py:.0f}' for px, py in pts) + ' Z'
        rim = 'M ' + ' L '.join(f'{px:.0f},{py:.0f}' for px, py in pts[len(pts) // 2:-1])
        return f'<path d="{d}" fill="#2e4a50"/><path d="{rim}" stroke="#f0b49a" stroke-width="2.4" fill="none" opacity=".75"/>'
    ny = ('<g transform="translate(250,606) scale(1.25)">'
          '<ellipse cx="0" cy="6" rx="250" ry="44" fill="url(#s5shal)" opacity=".8"/>'
          '<path d="M -120,4 C -80,-6 -34,-4 0,-1 C 34,-4 80,-6 120,4 C 80,9 34,7 0,6 C -34,7 -80,9 -120,4 Z" fill="#fbefe0"/>'
          + peak(-196, -64, 76, 1) + peak(-44, 40, 50, 2) + peak(76, 204, 66, 3)
          + ''.join(f'<rect x="{x}" y="{y}" width="8" height="5" fill="#ffe2b8"/>' for x, y in ((-130, -20), (132, -16), (-6, -10)))
          + '</g>')
    hills = ('<path d="M -20,640 C 30,600 70,586 110,600 C 150,614 180,660 200,720 L -20,720 Z" fill="#22303a"/>'
             '<path d="M 560,628 C 510,598 470,594 440,612 C 410,630 390,670 380,720 L 560,720 Z" fill="#1f2c36"/>'
             + palm(70, 610, .5, False) .replace('#2f6b5a', '#1a2830').replace('#3f8a6e', '#1f2f38').replace('#4fa07c', '#24343e').replace('#8a7462', '#1a2228').replace('#6c5a4c', '#151c22').replace('#5e4c40', '#151c22')
             + palm(500, 600, .45, True).replace('#2f6b5a', '#1a2830').replace('#3f8a6e', '#1f2f38').replace('#4fa07c', '#24343e').replace('#8a7462', '#1a2228').replace('#6c5a4c', '#151c22').replace('#5e4c40', '#151c22'))
    ground = ('<path d="M -20,760 C 120,720 300,712 560,740 L 560,960 L -20,960 Z" fill="#2e3e3a"/>'
              '<path d="M -20,760 C 120,720 300,712 560,740 L 560,756 C 300,730 120,740 -20,780 Z" fill="#e8a890" opacity=".3"/>'
              + ''.join(f'<path d="M {x},{y} q 4,-16 8,0 M {x + 6},{y} q 5,-20 10,0" stroke="#4e6a52" stroke-width="2" fill="none"/>' for x, y in ((30, 800), (130, 780), (300, 790), (420, 806), (490, 830), (80, 880), (230, 860))))
    rocks = boulder(-80, 1000, 330, 240, 1) + boulder(360, 1000, 260, 180, 1)
    back = sky + far + sea + f'<g filter="url(#s4dof)">{ny}</g>' + hills + ground
    s_tr = 'translate(450,606) scale(.6)'
    dog_tr = 'translate(372,850) scale(.3)'
    bd, bs, bc = beam_set(fid, [[(sunx - 8, suny), (sunx + 8, suny), (200 - k * 60, 960), (150 - k * 60, 960)] for k in range(4)], '#ffe2c8', .12)
    light = bs + CL.glow(sunx, suny, 260, '#ffcfb0', .25, core=False) + fine_dust((0, suny, 540, 960), 240, 31, '#fff0e0', clip=bc) + fine_dust((0, 300, 540, 900), 60, 32, '#fff0e0')
    chars = [char(fid, sun_island('smirk'), s_tr, (sunx, suny), (450, 700), 'dusk', 'sun'), char(fid, ISL['DOG'], dog_tr, (sunx, suny), (372, 890), 'dusk', None)]
    sh = CL.contact_shadow(450, 900, 36) + CL.contact_shadow(372, 902, 28, 5)
    ui = tag('สองปีต่อมา · จุดชมวิวเกาะนางยวน') + subs('วันนี้คลื่นแรง…/ของคงไม่มาอีกแล้ว', 'Rough sea today…/my parcel isn’t coming again.')
    return compose(fid, 'dusk', back, sh, chars, rocks, light, '', ui, bd + S5DEFS)


# ================================================================ explainer graphics as story-world objects
def table_top(fid, light_from=(540, 0)):
    top = wood_planks(0, 0, 540, 960, '#a8805e', '#b88e6a', '#946e50', 80, 41)
    bd, bs, bc = beam_set(fid, [[(380 + k * 50, 0), (420 + k * 50, 0), (60 + k * 50, 960), (20 + k * 50, 960)] for k in range(4)], '#fff2d8', .2)
    return top, bd, bs, bc


def g_map():
    fid = 'GX1'
    top, bd, bs, bc = table_top(fid)
    paper = ('<g transform="translate(270,430) rotate(-4)"><rect x="-206" y="-262" width="420" height="530" fill="#000" opacity=".25" filter="url(#s4soft)"/>'
             '<rect x="-210" y="-270" width="420" height="530" fill="#f3e8d2"/><rect x="-210" y="-270" width="420" height="530" fill="none" stroke="#e0d2b8" stroke-width="2"/>'
             '<path d="M -210,-270 L -210,260 L -110,260 C -100,140 -130,40 -96,-60 C -76,-140 -120,-210 -100,-270 Z" fill="#d6c8a8"/>'
             '<path d="M -210,-270 L -210,260 L -134,260 C -124,140 -152,40 -120,-60 C -100,-140 -142,-210 -124,-270 Z" fill="#a9c08e" opacity=".8"/>'
             + ''.join(f'<path d="M {-60 + i * 40},{-200 + (i % 3) * 120} q 10,-4 20,0" stroke="#9ab8c4" stroke-width="2" fill="none"/>' for i in range(7))
             + f'<polygon points="{K.koh_tao_shape(90, -60, .62)}" fill="#a9c08e" stroke="#7a9a6a" stroke-width="2"/>'
             + '<path d="M -100,-40 C -40,-80 20,-90 56,-70" stroke="#c4463d" stroke-width="4" fill="none" stroke-dasharray="10 8"/>'
             + '<circle cx="-100" cy="-40" r="8" fill="#c4463d"/><path d="M 90,-150 L 90,-180 L 112,-170 L 90,-160" fill="#c4463d"/>'
             + f'<text x="-150" y="-10" {TH} font-size="18" font-weight="800" fill="#4a3a2a" text-anchor="middle" transform="rotate(-90 -150 -10)">ชุมพร</text>'
             + f'<text x="160" y="40" {TH} font-size="20" font-weight="800" fill="#2a5a4a">เกาะเต่า</text>'
             + f'<text x="10" y="150" {TH} font-size="16" font-weight="700" fill="#5a7a8a" font-style="italic">อ่าวไทย</text>'
             + '<path d="M 60,110 C 80,140 120,150 150,140" stroke="#5a7a8a" stroke-width="2" fill="none" stroke-dasharray="4 5"/>'
             + f'<text x="150" y="170" {TH} font-size="13" font-weight="700" fill="#5a7a8a" text-anchor="middle">ต่อสมุย · พะงัน</text>'
             + '<rect x="-30" y="-290" width="60" height="26" fill="#f6efe0" opacity=".75" transform="rotate(6)"/><rect x="150" y="230" width="60" height="26" fill="#f6efe0" opacity=".75" transform="rotate(-8)"/></g>')
    ticket = ('<g transform="translate(120,856) rotate(9)"><rect x="-96" y="-44" width="192" height="88" rx="6" fill="#000" opacity=".25" filter="url(#s4soft)"/><rect x="-100" y="-48" width="192" height="88" rx="6" fill="#f8f4ea"/>'
              '<rect x="-100" y="-48" width="192" height="24" rx="6" fill="#2a7f86"/>' + f'<text x="-4" y="-31" {TH} font-size="12" font-weight="800" fill="#fff" text-anchor="middle">ตั๋วเรือ · FERRY</text>'
              + f'<text x="-4" y="0" {TH} font-size="15" font-weight="800" fill="#1a1626" text-anchor="middle">ชุมพร → เกาะเต่า</text>'
              + f'<text x="-4" y="24" {TH} font-size="12" font-weight="700" fill="#5a5470" text-anchor="middle">เรือเร็วราว 1 ชม. 45 นาที</text>'
              + '<path d="M 58,-48 L 58,40" stroke="#c9c1b2" stroke-width="2" stroke-dasharray="4 4"/></g>')
    props = ('<g transform="translate(440,820)"><circle r="54" fill="#000" opacity=".25" filter="url(#s4soft)"/><circle r="50" fill="#f4efe6"/><circle r="38" fill="#6a4632"/><circle r="38" fill="#8a5e40" opacity=".5"/><ellipse cx="-10" cy="-12" rx="14" ry="6" fill="#c89a72" opacity=".6"/></g>'
             '<g transform="translate(460,150)"><circle r="38" fill="#c9a86a"/><circle r="31" fill="#f4efe6"/><path d="M 0,-26 L 6,0 L 0,26 L -6,0 Z" fill="#c4463d"/><path d="M 0,0 L 6,0 L 0,26 L -6,0 Z" fill="#2a2c34"/></g>'
             + ''.join(f'<path d="M {x},{y} q 8,-14 16,0 q -8,6 -16,0 Z" fill="#f6eadb" transform="rotate({r} {x} {y})"/>' for x, y, r in ((60, 130, 20), (90, 160, -30), (420, 620, 40)))
             + '<g transform="translate(70,560) rotate(-30)"><path d="M -24,-8 L -4,-8 L -5,0 C -6,4 -10,6 -14,6 C -20,6 -24,3 -24,-1 Z M 24,-8 L 4,-8 L 5,0 C 6,4 10,6 14,6 C 20,6 24,3 24,-1 Z" fill="#141218"/></g>')
    noair = ('<g transform="translate(270,600)"><rect x="-110" y="-26" width="220" height="52" rx="26" fill="#120e1c" fill-opacity=".85" stroke="#9a86ff"/>'
             '<circle cx="-78" cy="0" r="14" fill="none" stroke="#e8735f" stroke-width="3"/><path d="M -88,-10 L -68,10" stroke="#e8735f" stroke-width="3"/>'
             f'<text x="16" y="6" {TH} font-size="15" font-weight="800" fill="#f2eefa" text-anchor="middle">เกาะเต่าไม่มีสนามบิน</text></g>')
    light = bs + fine_dust((0, 0, 540, 960), 220, 41, '#fff4e2', clip=bc)
    ui = step(1, 'เกาะเต่าอยู่ตรงไหน', 'GULF OF THAILAND · BY BOAT ONLY') + subs('เกาะเต่าไม่มีสนามบิน/ย้ายบ้านทีต้องขนทั้งชีวิตลงเรือ', 'No airport on Koh Tao:/moving means shipping your whole life.')
    return compose(fid, 'warm', top, '', [], paper + ticket + props + noair, light, '', ui, bd + S5DEFS)


def g_parcel():
    fid = 'GX2'
    floor = wood_planks(0, 0, 540, 960, '#8a6a52', '#9a7860', '#7a5c46', 70, 51, vertical=False)
    bd, bs, bc = beam_set(fid, [[(380 + k * 50, 0), (420 + k * 50, 0), (60 + k * 50, 960), (20 + k * 50, 960)] for k in range(4)], '#fff2d8', .18)
    box = ('<g transform="translate(270,470)"><rect x="-150" y="-110" width="310" height="240" fill="#000" opacity=".28" filter="url(#s4soft)"/>'
           '<rect x="-160" y="-120" width="320" height="240" fill="#c49a6c"/><rect x="-160" y="-120" width="320" height="240" fill="none" stroke="#a97f55" stroke-width="3"/>'
           '<rect x="-24" y="-120" width="48" height="240" fill="#e6d2b0" opacity=".85"/>'
           '<rect x="-140" y="-96" width="110" height="78" fill="#f8f4ea"/>' + f'<text x="-85" y="-74" {TH} font-size="11" font-weight="800" fill="#1a1626" text-anchor="middle">ถึง: ซัน</text>'
           + f'<text x="-85" y="-56" {TH} font-size="10" fill="#5a5470" text-anchor="middle">บ้านบนเนิน เกาะเต่า</text>' + ''.join(f'<rect x="{-130 + k * 6}" y="-44" width="{2 + k % 3}" height="20" fill="#1a1626"/>' for k in range(14))
           + '<g transform="translate(90,40) rotate(-10)"><rect x="-50" y="-22" width="100" height="44" rx="6" fill="#c4463d"/>' + f'<text x="0" y="6" {TH} font-size="14" font-weight="800" fill="#fff" text-anchor="middle">ระวังแตก</text></g></g>')
    steps = [('โกดัง', 'กรุงเทพ', '#5a6c8e', 90, 170), ('รถขนส่ง', 'ลงใต้', '#e8735f', 270, 130), ('ท่าเรือ', 'ชุมพร', '#2fb3b8', 450, 170),
             ('ข้ามทะเล', 'คลื่นแรง = งด', '#3d6fb0', 470, 760), ('แม่หาด', 'ถึงเกาะ', '#2fb3b8', 270, 800), ('ถึงบ้าน', 'กระบะ/มอไซค์', '#7a5ab8', 70, 760)]
    path = '<path d="M 90,170 Q 180,100 270,130 Q 360,100 450,170 Q 560,470 470,760 Q 370,840 270,800 Q 170,840 70,760 Q 0,470 90,170" stroke="#f8f4ea" stroke-width="3" fill="none" stroke-dasharray="8 7" opacity=".85"/>'
    stickers = ''.join(f'<g transform="translate({x},{y})"><circle r="46" fill="#000" opacity=".25" filter="url(#s4soft)"/><circle r="44" fill="#f8f4ea"/><circle r="38" fill="{c}"/>'
                       f'<text x="0" y="-2" {TH} font-size="14" font-weight="800" fill="#fff" text-anchor="middle">{t}</text><text x="0" y="16" {TH} font-size="10.5" font-weight="700" fill="#ffffff" text-anchor="middle" opacity=".9">{s}</text>'
                       f'<circle cx="30" cy="-30" r="12" fill="#120e1c"/><text x="30" y="-25" {TH} font-size="12" font-weight="800" fill="#f2eefa" text-anchor="middle">{i + 1}</text></g>' for i, (t, s, c, x, y) in enumerate(steps))
    storm = '<g transform="translate(500,690)"><path d="M -30,8 C -30,-8 -14,-16 0,-11 C 8,-24 30,-22 33,-4 C 46,-3 47,11 35,14 L -26,14 C -37,14 -39,8 -30,8 Z" fill="#9aa6b8"/><path d="M -6,18 L -12,32 M 8,18 L 2,32" stroke="#3d6fb0" stroke-width="3"/></g>'
    light = bs + fine_dust((0, 0, 540, 960), 200, 51, '#fff4e2', clip=bc)
    ui = step(2, 'พัสดุเดินทางมาเกาะยังไง', 'SIX STOPS FROM WAREHOUSE TO DOOR', 880 - 74 - 6) + subs('ของหลายอย่างต้องมาทางเรือ/คลื่นแรงเมื่อไหร่ เรืองด ของก็มาช้า', 'Most things come by boat;/rough seas mean late parcels.', 668)
    return compose(fid, 'warm', floor, '', [], path + box + stickers + storm, light, '', ui, bd + S5DEFS)


def g_calendar():
    fid = 'GX3'
    wall = wood_planks(0, 0, 540, 960, '#8a6a52', '#9a7860', '#7a5c46', 54, 61)
    win = ('<rect x="380" y="120" width="160" height="300" fill="#5a6a86"/>' + ''.join(f'<path d="M {x},{y} l -6,18" stroke="#c8d8f0" stroke-width="2" opacity=".6"/>' for x, y in ((400, 140), (430, 200), (460, 160), (500, 240), (420, 300), (470, 340), (510, 180)))
           + '<rect x="372" y="112" width="176" height="10" fill="#5e3e2c"/><rect x="372" y="420" width="176" height="14" fill="#5e3e2c"/><rect x="372" y="112" width="10" height="320" fill="#5e3e2c"/>')
    months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']
    kind = ['g', 'g', 'g', 'g', 'o', 'o', 'g', 'g', 'o', 'o', 'r', 'r']
    cal = '<g transform="translate(60,170) rotate(-2)"><rect x="6" y="10" width="330" height="440" fill="#000" opacity=".3" filter="url(#s4soft)"/><rect x="0" y="0" width="330" height="440" fill="#fbf6ee"/>'
    cal += '<rect x="0" y="0" width="330" height="54" fill="#2a7f86"/>' + f'<text x="165" y="36" {TH} font-size="22" font-weight="800" fill="#fff" text-anchor="middle">ปฏิทินชาวเกาะ</text>'
    cal += '<circle cx="165" cy="-14" r="6" fill="#8a857e"/><path d="M 165,-14 L 120,0 M 165,-14 L 210,0" stroke="#8a857e" stroke-width="2"/>'
    icon = {'g': ('#7fb07a', '☀'), 'o': ('#f0b46a', '⛅'), 'r': ('#e8735f', '⛈')}
    for i, (m, k) in enumerate(zip(months, kind)):
        cx, cy = 18 + (i % 3) * 104, 70 + (i // 3) * 90
        c, ic = icon[k]
        cal += f'<rect x="{cx}" y="{cy}" width="92" height="80" rx="6" fill="{c}" opacity=".9"/><text x="{cx + 46}" y="{cy + 28}" {TH} font-size="16" font-weight="800" fill="#1a1626" text-anchor="middle">{m}</text>'
        cal += f'<text x="{cx + 46}" y="{cy + 62}" font-size="24" text-anchor="middle">{ic}</text>'
        if k == 'r':
            cal += f'<path d="M {cx + 8},{cy + 8} L {cx + 84},{cy + 72} M {cx + 84},{cy + 8} L {cx + 8},{cy + 72}" stroke="#7a1a1a" stroke-width="4" opacity=".7"/>'
    cal += f'<g transform="translate(210,400) rotate(-6)"><rect x="-6" y="-18" width="130" height="34" fill="#fff4a8"/><text x="58" y="5" {TH} font-size="13" font-weight="800" fill="#7a1a1a" text-anchor="middle">พ.ย.–ธ.ค. เรืองด!</text></g></g>'
    notes = (driftwood_sign(60, 680, 200, 'ม.ค.–เม.ย. ทะเลสวย', 'BEST SEA', -3, '#2f6b5a') + driftwood_sign(290, 690, 200, 'พ.ย.–ธ.ค. มรสุม', 'MONSOON', 3, '#b0463c')
             + shell_chime(470, 440, 5, 80) + buoy(420, 600, 14) + buoy(470, 620, 12, '#2fb3b8'))
    bd, bs, bc = beam_set(fid, [[(386 + k * 30, 122), (406 + k * 30, 122), (180 + k * 30, 960), (156 + k * 30, 960)] for k in range(5)], '#c8d8f0', .1)
    light = bs + fine_dust((0, 120, 540, 960), 160, 61, '#e8f0ff', clip=bc)
    ui = step(3, 'อยู่เกาะต้องดูฟ้าดูลม', 'WHEN THE SEA IS KIND · WHEN BOATS STOP') + subs('ช่วงมรสุม ราว พ.ย.–ธ.ค./ฝนหนัก คลื่นแรง เรืออาจงดวิ่ง', 'Monsoon, around Nov–Dec:/heavy rain, rough sea, ferries may stop.', 880)
    return compose(fid, 'warm', wall + win, '', [], cal + notes, light, '', ui, bd + S5DEFS)


def g_cost():
    fid = 'GX4'
    top, bd, bs, bc = table_top(fid)
    pad = ('<g transform="translate(250,450) rotate(3)"><rect x="-176" y="-286" width="360" height="560" fill="#000" opacity=".25" filter="url(#s4soft)"/><rect x="-180" y="-290" width="360" height="560" fill="#fbf6ea"/>'
           + ''.join(f'<path d="M -180,{-240 + k * 34} L 180,{-240 + k * 34}" stroke="#bcd0e0" stroke-width="1.2"/>' for k in range(16))
           + '<path d="M -140,-290 L -140,270" stroke="#e8a0a0" stroke-width="1.6"/>' + ''.join(f'<circle cx="{-150 + k * 34}" cy="-296" r="6" fill="#9aa1a8"/>' for k in range(10))
           + f'<text x="0" y="-250" {TH} font-size="22" font-weight="800" fill="#2a2a4a" text-anchor="middle">ค่าใช้จ่ายต่อเดือน</text>')
    rows = [('บังกะโลพัดลม', '~4,000'), ('สตูดิโอแอร์', '12,000–18,000'), ('เช่ามอไซค์', '2,500–3,500'), ('งบนักเรียนดำน้ำ', '15,000–20,000'), ('งบอยู่สบาย ๆ', '35,000–60,000')]
    for i, (t, v) in enumerate(rows):
        y = -196 + i * 68
        pad += f'<text x="-126" y="{y}" {TH} font-size="17" font-weight="700" fill="#2a2a4a">{t}</text><text x="166" y="{y}" {TH} font-size="17" font-weight="800" fill="#c4463d" text-anchor="end">{v} ฿</text>'
    pad += f'<path d="M -126,150 L 166,150" stroke="#2a2a4a" stroke-width="2"/><text x="20" y="190" {TH} font-size="16" font-weight="800" fill="#2a2a4a" text-anchor="middle">แพงกว่าฝั่ง เพราะของมาทางเรือ</text>'
    pad += f'<text x="20" y="222" {TH} font-size="13" font-weight="600" fill="#6a6478" text-anchor="middle">ตัวเลขจากรีวิวคนที่อยู่จริง ต่างกันตามไลฟ์สไตล์</text></g>'
    props = ('<g transform="translate(450,190) rotate(14)"><rect x="-44" y="-70" width="88" height="140" rx="10" fill="#000" opacity=".25" filter="url(#s4soft)"/><rect x="-46" y="-72" width="88" height="140" rx="10" fill="#2a2c34"/><rect x="-36" y="-60" width="68" height="30" fill="#bfe3c4"/>'
             + ''.join(f'<rect x="{-36 + (k % 4) * 18}" y="{-20 + (k // 4) * 20}" width="14" height="14" rx="3" fill="#5e6270"/>' for k in range(16)) + '</g>'
             + ''.join(f'<circle cx="{x}" cy="{y}" r="16" fill="#d9b25e"/><circle cx="{x}" cy="{y}" r="11" fill="none" stroke="#b08a3e" stroke-width="2"/>' for x, y in ((80, 840), (110, 860), (96, 820)))
             + '<g transform="translate(470,820) rotate(-20)"><rect x="-6" y="-70" width="12" height="130" rx="3" fill="#2f6fb5"/><path d="M -6,60 L 0,76 L 6,60 Z" fill="#f4efe6"/></g>' + coconut(80, 200, 1.2))
    light = bs + fine_dust((0, 0, 540, 960), 200, 71, '#fff4e2', clip=bc)
    ui = step(4, 'อยู่เกาะเต่าเดือนละเท่าไหร่', 'HIGH COST OF LIVING · MODEST WAGES', 22) + subs('ค่าครองชีพแพง/แต่ค่าแรงไม่ได้แพงตาม', 'Living costs are high,/wages are not.', 900)
    return compose(fid, 'warm', top, '', [], pad + props, light, '', ui, bd + S5DEFS)


def outfit_card():
    """Islander outfit on the house character-sheet background, beside the Bangkok look."""
    out = '<rect width="540" height="960" fill="#1b1f2b"/><rect y="830" width="540" height="130" fill="#161a24"/>'
    out += f'<g transform="translate(150,190) scale(1.3)">{R.body(head="smirk")}</g>'
    out += f'<g transform="translate(390,190) scale(1.3)">{sun_island("smirk")}</g>'
    out += f'<text x="150" y="930" {TH} font-size="16" font-weight="700" fill="#d4d6e0" text-anchor="middle">กรุงเทพ (อดีต)</text><text x="390" y="930" {TH} font-size="16" font-weight="700" fill="#d4d6e0" text-anchor="middle">ชาวเกาะ (ปัจจุบัน)</text>'
    return f'<svg viewBox="0 0 540 960" role="img" aria-label="ชุดซัน"><defs>{S5DEFS}</defs>{out}</svg>'


SHOTS = [
    (outfit_card, 'ชุดชาวเกาะใหม่ของซัน', 'เสื้อฮาวายลายดอกชบาสีกรมสด เปิดหน้า ทับเสื้อกล้ามขาว · บอร์ดชอร์ตสีเขียวทะเลลายคลื่น แถบข้างขาว · รองเท้าแตะสายส้ม · สร้อยลูกปัดกับเปลือกหอย กำไลเชือก · ผิวแทน'),
    (street, 'ถนนหน้าร้านดำน้ำ · เช้า', 'เมฆใหม่เป็นแนวหลายชั้น · มอเตอร์ไซค์ขนาดจริงจอดอยู่ข้างหลังซัน (ยาวราว 1.8 ม. เลยล้นกรอบ) · ชุดชาวเกาะใหม่'),
    (bedroom, 'บ้านเช่า · คืนแรก', 'กลับไปใช้ห้องฉบับก่อนที่เจ้าของช่องบอกว่าดีกว่า · เติมฝุ่นละเอียดในแสงจันทร์กับแสงโคม และป้ายแบบใหม่'),
    (vista, 'จุดชมวิวเกาะนางยวน · พระอาทิตย์ตก', 'ทำใหม่ทั้งหมด · ฟ้าไล่ม่วงชมพูพีช เมฆเป็นแนวยาวหลายชั้นมีแสงทาบขอบ · ทะเลมีหมอกที่ขอบฟ้า ระลอกคลื่นเล็กลงตามระยะ แดดสะท้อนเป็นทาง · เกาะสามเกาะกับสันทราย เนินเขาเงาดำสองข้าง · ซันกับหมาตัวเล็กลงให้วิวเด่น'),
    (g_map, 'กราฟิก 1 · แผนที่บนโต๊ะ', 'แผนที่กระดาษติดเทปบนโต๊ะไม้ เส้นเรือจากชุมพร · ตั๋วเรือ "เรือเร็วราว 1 ชม. 45 นาที" · เข็มทิศ กาแฟ เปลือกหอย แว่นกันแดด · ป้ายไม่มีสนามบิน'),
    (g_parcel, 'กราฟิก 2 · กล่องพัสดุกับสติกเกอร์เส้นทาง', 'กล่องพัสดุบนพื้นไม้ สติกเกอร์ 6 จุดจากโกดังถึงบ้าน · ไอคอนพายุตรงช่วงข้ามทะเล'),
    (g_calendar, 'กราฟิก 3 · ปฏิทินชาวเกาะบนผนัง', 'ปฏิทิน 12 เดือนสีตามคลื่นลม พ.ย.–ธ.ค. กากบาท "เรืองด!" · หน้าต่างฝนตก · ป้ายไม้ทะเลบอกช่วงทะเลสวยกับมรสุม'),
    (g_cost, 'กราฟิก 4 · กระดาษจดค่าใช้จ่าย', 'สมุดจดบนโต๊ะไม้ ค่าเช่า มอเตอร์ไซค์ งบต่อเดือน · เครื่องคิดเลข เหรียญ ปากกา มะพร้าว'),
]


def build():
    figs = ''.join(f'<figure>{fn()}<figcaption><span class="n">{i:02d}</span> <b>{t}</b><span class="note">{n}</span></figcaption></figure>' for i, (fn, t, n) in enumerate(SHOTS, 1))
    page = open(os.path.join(HERE, 'scenes_v4.html')).read()
    head = page[:page.index('<div class="wrap">')].replace('<title>Odd Hours ฉาก EP.01</title>', '<title>Odd Hours ฉาก EP.01 รอบ 5</title>')
    head = head.replace('</defs></svg>', f'{ISL["UNCLE_HEAD"] if "h_uncle" not in head else ""}</defs></svg>', 1)
    out = head + f'''<div class="wrap">
  <h1>ฉาก EP.01 เกาะเต่า · รอบ 5<span>ชุดชาวเกาะใหม่ · ห้องนอนฉบับเดิม · มอเตอร์ไซค์ขนาดจริง · วิวพระอาทิตย์ตกทำใหม่ · กราฟิกเป็นของจริงในเรื่อง</span></h1>
  <div class="grid">{figs}</div>
</div>
'''
    open(os.path.join(HERE, 'scenes_v5.html'), 'w').write(out)
    print(len(out))


if __name__ == '__main__':
    build()
