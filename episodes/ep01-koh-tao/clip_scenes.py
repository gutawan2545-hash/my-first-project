"""EP.01 full clip: the new locations the script needs (same approved look: warm medium shots, layered props,
light shafts with fine dust, soft contact shadows). Characters are passed in already rigged."""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'motion'))
import cinelight as CL
import omkit as M
import kt_scenes as K
import style5 as S5
import style6 as S6
from style3 import wood_planks
from style4 import beam_set, fine_dust, buoy, net, shell_chime, lifebuoy, driftwood_sign, char, compose, uid, wall_shadow
from scenes import palm

TH, EN = M.TH, M.EN


def _blob(cx, cy, r, c, n=9, seed=1):
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        rr = r * rnd.uniform(.75, 1.1)
        pts.append((cx + rr * math.cos(a), cy + rr * .8 * math.sin(a)))
    d = f'M {pts[0][0]:.0f},{pts[0][1]:.0f} ' + ' '.join(f'Q {(x0 + x1) / 2 + rnd.uniform(-6, 6):.0f},{(y0 + y1) / 2 - r * .25:.0f} {x1:.0f},{y1:.0f}' for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1])) + ' Z'
    return f'<path d="{d}" fill="{c}"/>'


def bush(cx, cy, w, seed=1, cols=('#2f5e44', '#3f7a52', '#5e9a62', '#7fb27a')):
    rnd = random.Random(seed)
    out = ''
    for layer, c in enumerate(cols):
        for k in range(5 - layer):
            out += _blob(cx + rnd.uniform(-w / 2, w / 2), cy - layer * w * .08 + rnd.uniform(-10, 10), w * rnd.uniform(.18, .3) * (1 - layer * .12), c, 9, seed * 31 + layer * 7 + k)
    return out


# ================================================================ Bangkok restaurant kitchen (flashback)
def kitchen(james, face_id, light_pt=(330, 120)):
    fid = 'KC'
    tiles = '<rect width="540" height="660" fill="#cbc2b6"/>' + ''.join(
        f'<rect x="{(c * 40 + (r % 2) * 20) - 20}" y="{150 + r * 20}" width="38" height="18" rx="1.5" fill="#d8d0c4" opacity=".75"/>' for r in range(26) for c in range(15))
    grime = '<ellipse cx="380" cy="560" rx="220" ry="140" fill="#6a5040" opacity=".22" filter="url(#s4soft)"/>'
    hood = ('<path d="M -10,0 L 550,0 L 550,120 L 500,170 L 40,170 L -10,120 Z" fill="#8c919b"/><path d="M -10,0 L 550,0 L 550,26 L -10,26 Z" fill="#6e737d"/>'
            '<path d="M 40,170 L 500,170 L 496,178 L 44,178 Z" fill="#5a5f69"/><path d="M -10,120 L 40,170 L 52,170 L 4,120 Z" fill="#b9bec8"/>'
            '<rect x="70" y="160" width="400" height="9" rx="4" fill="#fff4e0"/>' + ''.join(f'<rect x="{x}" y="60" width="44" height="70" rx="3" fill="#7a7f89" opacity=".8"/>' for x in range(60, 500, 60))
            + ''.join(f'<path d="M {x},64 L {x},126" stroke="#a5aab4" stroke-width="1.4"/>' for x in range(66, 500, 10)))
    rail = '<rect x="18" y="212" width="250" height="7" rx="3" fill="#9aa0aa"/>' + ''.join(
        f'<g transform="translate({30 + i * 34},219) rotate({(-4, 3, -2, 5, -3, 2, -5)[i]})"><rect x="0" y="0" width="28" height="{46 + (i % 3) * 8}" fill="#fbf8f0"/>'
        + ''.join(f'<rect x="4" y="{8 + j * 7}" width="{12 + (j * 7 + i) % 9}" height="2" fill="#8a8494"/>' for j in range(5)) + '<rect x="4" y="2" width="20" height="3" fill="#c4463d"/></g>' for i in range(7))
    shelf = ('<rect x="300" y="250" width="240" height="8" fill="#9aa0aa"/>'
             + ''.join(f'<g transform="translate({318 + i * 26},250)"><rect x="-8" y="-38" width="16" height="38" rx="3" fill="{c}"/><rect x="-4" y="-48" width="8" height="12" fill="{c}"/><rect x="-8" y="-26" width="16" height="12" fill="#f2eee6" opacity=".85"/></g>'
                       for i, c in enumerate(('#6a3a26', '#3a2a22', '#8a5a26', '#c4463d', '#3a5a2e', '#6a3a26', '#d8a03a', '#3a2a22')))
             + ''.join(f'<g transform="translate({330 + i * 40},300)"><path d="M 0,0 L 0,{60 + i % 2 * 14}" stroke="#a5aab4" stroke-width="3"/><ellipse cx="0" cy="{66 + i % 2 * 14}" rx="{9 + i % 3 * 2}" ry="5" fill="#8c919b"/></g>' for i in range(5)))
    pic = ('<g transform="translate(150,330)"><rect x="-42" y="-30" width="84" height="60" fill="#2c2f38"/><rect x="-38" y="-26" width="76" height="52" fill="#f2eee6"/>'
           f'<text x="0" y="-6" {TH} font-size="12" font-weight="800" fill="#c4463d" text-anchor="middle">ออเดอร์ด่วน!</text><text x="0" y="12" {TH} font-size="10" font-weight="700" fill="#2c2f38" text-anchor="middle">กะเพรา x 12</text></g>')
    back = f'<g filter="url(#s4dof)">{tiles}{grime}{shelf}{pic}</g>' + hood + rail
    counter = ('<rect x="-10" y="660" width="560" height="310" fill="#9aa0aa"/><rect x="-10" y="660" width="560" height="14" fill="#c9ced8"/><rect x="-10" y="674" width="560" height="8" fill="#6e737d" opacity=".6"/>'
               + ''.join(f'<rect x="{x}" y="700" width="160" height="240" rx="4" fill="none" stroke="#7a7f89" stroke-width="3"/><rect x="{x + 66}" y="716" width="28" height="6" rx="3" fill="#6e737d"/>' for x in (10, 190, 370)))
    wok = ('<g transform="translate(372,664)"><ellipse cx="0" cy="0" rx="84" ry="14" fill="#2a2c34"/>'
           '<path d="M -80,-6 C -60,40 60,40 80,-6 Z" fill="#1b1d24"/><path d="M -80,-6 C -62,22 -30,30 0,30 C -30,20 -56,10 -66,-6 Z" fill="#3a3d48"/>'
           '<path d="M 76,-10 L 150,-34" stroke="#3a2a22" stroke-width="9" stroke-linecap="round"/>'
           '<g class="om-beam" opacity=".95">' + ''.join(f'<path d="M {x},14 C {x - 12},-20 {x + 4},-40 {x + 2},-66 C {x + 16},-40 {x + 18},-14 {x + 8},14 Z" fill="{c}"/>' for x, c in ((-50, '#ff9a4a'), (-20, '#ffb45e'), (10, '#ff8a3a'), (34, '#ffc070'), (-64, '#ff7a3a')))
           + '</g><g class="om-beam" opacity=".9">' + ''.join(f'<path d="M {x},14 C {x - 6},-6 {x + 2},-22 {x + 1},-34 C {x + 9},-20 {x + 9},-6 {x + 5},14 Z" fill="#fff0c0"/>' for x in (-40, -10, 18)) + '</g>'
           '<path d="M -60,-8 C -40,-20 30,-22 60,-10" stroke="#5e9a3a" stroke-width="6" fill="none"/><circle cx="-20" cy="-14" r="5" fill="#c4463d"/><circle cx="16" cy="-16" r="4" fill="#c4463d"/></g>')
    steam = ''.join(f'<g class="om-cloud"><path d="M {x},560 C {x - 20},500 {x + 24},470 {x},420 C {x - 18},380 {x + 10},350 {x - 4},320" stroke="#ffffff" stroke-opacity=".22" stroke-width="{14 - i * 2}" fill="none" stroke-linecap="round" filter="url(#s4soft)"/></g>' for i, x in enumerate((340, 380, 410)))
    plates = ('<g transform="translate(92,668)"><ellipse cx="0" cy="0" rx="60" ry="13" fill="#f8f6f0"/><ellipse cx="0" cy="-3" rx="38" ry="9" fill="#f2eee6"/>'
              '<path d="M -30,-4 C -20,-20 20,-20 30,-4 Z" fill="#fbf8f0"/><path d="M 4,-10 C 14,-22 34,-16 36,-6 Z" fill="#6a8a3a"/><ellipse cx="-6" cy="-12" rx="14" ry="6" fill="#fff8ea"/><circle cx="-6" cy="-12" r="5" fill="#f2b23a"/></g>'
              '<g transform="translate(200,668)"><rect x="-40" y="-8" width="80" height="10" rx="3" fill="#c8a07a"/><path d="M -10,-8 L 30,-8 L 26,-14 L -4,-14 Z" fill="#d6dae2"/></g>')
    james_tr = 'translate(176,300) scale(1.46)'
    ch = [char(fid, james, james_tr, light_pt, (176, 480), 'warm', 'sun')]
    bd, bs, bc = beam_set(fid, [[(80 + k * 70, 170), (120 + k * 70, 170), (150 + k * 70, 900), (100 + k * 70, 900)] for k in range(6)], '#fff4e2', .14)
    light = (bs + CL.glow(372, 640, 200, '#ffb46a', .36) + CL.glow(270, 165, 260, '#fff4e0', .2, core=False)
             + fine_dust((40, 170, 520, 900), 260, 71, '#fff4e2', clip=bc) + fine_dust((280, 420, 480, 660), 60, 72, '#ffd9a8'))
    sh = CL.contact_shadow(372, 676, 90, 8, .5) + CL.ao_line(0, 660, 540, 660, 14, .45)
    return compose(fid, 'warm', back, sh, ch, counter + wok + plates + steam, light, '', '', bd)


# ================================================================ taxi back seat in Bangkok traffic (flashback, night)
def taxi(james, fare_at, fare_out):
    fid = 'TX'
    rnd = random.Random(8)
    city = '<rect width="540" height="700" fill="#1b2442"/><rect y="300" width="540" height="400" fill="#2a3560"/>'
    for i in range(14):
        x, w, h = rnd.uniform(-20, 520), rnd.uniform(40, 90), rnd.uniform(160, 380)
        city += f'<rect x="{x:.0f}" y="{460 - h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{rnd.choice(["#22305a", "#2a3a6a", "#1e2a50"])}"/>'
        for r in range(int(h // 22)):
            for c in range(int(w // 16)):
                if rnd.random() < .35:
                    city += f'<rect x="{x + 5 + c * 16:.0f}" y="{466 - h + r * 22:.0f}" width="7" height="9" fill="{rnd.choice(["#ffd9a8", "#cfe0ff", "#ffeccc"])}" opacity="{rnd.uniform(.4, .9):.2f}"/>'
    road = '<rect y="460" width="540" height="240" fill="#232a44"/>'
    for row, (y, s) in enumerate(((480, .5), (520, .75), (575, 1.0))):
        for k in range(7):
            x = (k * 92 + row * 37) % 600 - 30
            road += (f'<rect x="{x - 34 * s:.0f}" y="{y - 22 * s:.0f}" width="{68 * s:.0f}" height="{30 * s:.0f}" rx="{8 * s:.0f}" fill="#3a3550"/>'
                     f'<circle cx="{x - 24 * s:.0f}" cy="{y - 6 * s:.0f}" r="{6 * s:.1f}" fill="#ff5a4a"/><circle cx="{x + 24 * s:.0f}" cy="{y - 6 * s:.0f}" r="{6 * s:.1f}" fill="#ff5a4a"/>'
                     f'<circle cx="{x - 24 * s:.0f}" cy="{y - 6 * s:.0f}" r="{16 * s:.1f}" fill="#ff5a4a" opacity=".25"/><circle cx="{x + 24 * s:.0f}" cy="{y - 6 * s:.0f}" r="{16 * s:.1f}" fill="#ff5a4a" opacity=".25"/>')
    sign = f'<g transform="translate(400,250)"><rect x="-60" y="-20" width="120" height="40" rx="4" fill="#2f8f5a"/><text x="0" y="6" {TH} font-size="14" font-weight="800" fill="#fff" text-anchor="middle">สุขุมวิท</text></g>'
    outside = f'<g filter="url(#s4dof2)">{city}{road}{sign}</g>'
    drops = ''.join(f'<circle cx="{rnd.uniform(40, 500):.0f}" cy="{rnd.uniform(130, 560):.0f}" r="{rnd.uniform(1.2, 3.2):.1f}" fill="#cfe0ff" opacity="{rnd.uniform(.3, .7):.2f}"/>' for _ in range(90))
    frame = ('<path d="M 0,0 L 540,0 L 540,960 L 0,960 Z M 34,130 C 34,112 46,100 64,100 L 470,100 C 494,100 506,112 506,136 L 506,560 L 34,560 Z" fill="#1d1b22" fill-rule="evenodd"/>'
             '<path d="M 34,560 L 506,560 L 506,572 L 34,572 Z" fill="#2c2a32"/><path d="M 64,100 L 470,100" stroke="#3a3842" stroke-width="3"/>'
             '<rect x="0" y="572" width="540" height="400" fill="#24222a"/><path d="M 0,600 L 540,600" stroke="#2f2d36" stroke-width="2"/>')
    seat_back = ('<path d="M -10,720 C 60,690 220,686 300,700 L 300,970 L -10,970 Z" fill="#2c2a32"/><path d="M -10,720 C 60,690 220,686 300,700 L 300,712 C 220,700 60,704 -10,734 Z" fill="#3a3842"/>'
                 '<rect x="120" y="640" width="90" height="70" rx="16" fill="#2c2a32"/><rect x="150" y="700" width="10" height="20" fill="#5a5862"/>')
    meter = ('<g transform="translate(150,780)"><rect x="-86" y="-34" width="172" height="68" rx="8" fill="#0e0e12"/><rect x="-78" y="-26" width="156" height="40" rx="4" fill="#1a0c0c"/>'
             f'<text x="-70" y="28" {EN} font-size="10" font-weight="700" fill="#8a8494">TAXI-METER</text></g>'
             + M.counter(150, 788, 287, '฿ {n}', fare_at, fare_out, 30, '#ff5a4a', frm=35) + M.reveal(f'<text x="150" y="812" {TH} font-size="10" font-weight="700" fill="#ff9a8a" text-anchor="middle">รถติด · ขยับ 2 เมตร</text>', fare_at + 1.2, fare_out, 'fade', .5))
    james_tr = 'translate(330,320) scale(1.34)'
    ch = [char(fid, james, james_tr, (60, 300), (330, 500), 'night', 'sun')]
    light = (CL.glow(100, 480, 260, '#ff6a5a', .12, core=False) + CL.glow(280, 300, 300, '#9fb8ff', .14, core=False) + CL.falloff(150, 360, 600, .35)
             + fine_dust((40, 120, 500, 560), 90, 81, '#cfe0ff'))
    return compose(fid, 'night', outside + drops, '', ch, frame + seat_back + meter, light, '', '', '')


# ================================================================ steps up the hill (agent at the foot / James climbing)
def stairs(chars_in, light_pt=(560, -40), sign=True):
    fid = 'ST'
    sky = '<rect width="540" height="420" fill="#a9d0ec"/><rect y="200" width="540" height="220" fill="#d6ecf4"/>' + S5.cloud_bank(260, 160, 260, 46, '#ffffff', '#eef3f8', '#c9d4e4', 3)
    house = ('<g transform="translate(410,214)"><path d="M -60,0 L 60,0 L 50,-36 L -50,-36 Z" fill="#2f6fb5"/><path d="M -60,0 L 0,-46 L 60,0 Z" fill="#2c5a96"/>'
             '<rect x="-46" y="0" width="92" height="56" fill="#c9a87a"/><rect x="-20" y="14" width="22" height="42" fill="#6f5442"/><rect x="14" y="12" width="24" height="18" fill="#9ad7e3"/>'
             '<path d="M -50,56 L 50,56" stroke="#8a6a50" stroke-width="4"/></g>')
    hill = '<path d="M -20,420 C 120,300 260,200 380,170 C 460,150 520,170 560,180 L 560,960 L -20,960 Z" fill="#4f8a5a"/>'
    jungle = (bush(80, 380, 260, 2) + bush(470, 300, 200, 3) + bush(240, 300, 180, 4) + palm(60, 420, .7) + palm(500, 330, .6, True, 1)
              + K.bougainvillea(-20, 300, 160, 100, 6))
    steps = ''
    for i in range(16):
        q = i / 16
        y = 940 - q * 700
        w = 300 * (1 - q * .72)
        x = 300 + q * 110
        h = 44 * (1 - q * .7)
        steps += (f'<path d="M {x - w / 2:.0f},{y:.0f} L {x + w / 2:.0f},{y:.0f} L {x + w / 2 - 4:.0f},{y - h:.0f} L {x - w / 2 + 4:.0f},{y - h:.0f} Z" fill="#b9b2a6"/>'
                  f'<path d="M {x - w / 2 + 4:.0f},{y - h:.0f} L {x + w / 2 - 4:.0f},{y - h:.0f} L {x + w / 2 - 10 * (1 - q):.0f},{y - h - 10 * (1 - q * .7):.0f} L {x - w / 2 + 10 * (1 - q):.0f},{y - h - 10 * (1 - q * .7):.0f} Z" fill="#d6d0c4"/>')
    rail = ('<path d="M 160,940 C 220,700 300,450 370,250" stroke="#8a857e" stroke-width="5" fill="none"/>'
            + ''.join(f'<path d="M {160 + k * 21},{940 - k * 70} l 0,-46" stroke="#8a857e" stroke-width="4"/>' for k in range(10)))
    pots = ('<g transform="translate(470,820)"><path d="M -30,0 L 30,0 L 24,50 L -24,50 Z" fill="#c87a5e"/>' + bush(0, -10, 80, 9) + '</g>'
            + buoy(110, 880, 16, '#e8735f') + buoy(140, 892, 13, '#f4efe6'))
    sg = driftwood_sign(80, 640, 150, 'บ้านเช่า ↑', '128 ขั้น', -6, '#2a7f86') if sign else ''
    back = f'<g filter="url(#s4dof2)">{sky}{house}</g><g filter="url(#s4dof)">{hill}{jungle}</g>' + steps + rail
    ch = [char(fid, inner, tr, light_pt, foot, 'warm', face) for inner, tr, foot, face in chars_in]
    bd, bs, bc = beam_set(fid, [[(420 + k * 40, 0), (446 + k * 40, 0), (120 + k * 40, 960), (90 + k * 40, 960)] for k in range(5)], '#fff6e4', .15)
    leaves = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .45:.0f}" fill="#fff6e4" opacity=".26" filter="url(#s4soft)"/>' for x, y, rx in ((160, 760, 50), (330, 820, 60), (280, 600, 40), (400, 900, 50)))
    light = bs + leaves + CL.glow(560, -40, 380, '#fff6e4', .2, core=False) + fine_dust((60, 0, 540, 960), 240, 91, '#fffaf0', clip=bc)
    sh = ''.join(CL.contact_shadow(f[0], f[1], 70) for _, _, f, _ in chars_in)
    return compose(fid, 'warm', back, sh, ch, pots + sg, light, '', '', bd + S5.S5DEFS)


# ================================================================ Koh Tao seen from the ferry deck (21 km2, mostly hills)
def island_view(t0, t1):
    fid = 'IV'
    sky = S5.day_sky(470)
    sea = '<rect y="470" width="540" height="490" fill="url(#s5sea)"/>' + S6.whitecaps(480, 900, 70, 4)
    isl = S6.tropical_island(270, 560, 600, 270, 31, 0.1, '#d6ecf4', False, True, 9)
    deck = ('<rect x="-10" y="800" width="560" height="170" fill="#e9e4dc"/><rect x="-10" y="800" width="560" height="12" fill="#ffffff"/>'
            + ''.join(f'<rect x="{x}" y="740" width="8" height="64" fill="#d6d0c4"/>' for x in range(10, 560, 60))
            + '<path d="M -10,744 L 550,744" stroke="#f4f1ec" stroke-width="7"/><path d="M -10,772 L 550,772" stroke="#d6d0c4" stroke-width="4"/>'
            + lifebuoy(450, 860, 40) + '<path d="M 60,900 C 120,880 200,930 260,900" stroke="#c9b08a" stroke-width="7" fill="none"/>')
    back = sky + sea + isl                                 # island kept sharp (owner: the hills must read clearly)
    light = CL.glow(500, 60, 300, '#fff6e4', .2, core=False) + fine_dust((0, 300, 540, 960), 220, 101, '#ffffff', density_far=.7)
    ui = (M.reveal(f'<g transform="translate(150,236)"><rect x="-96" y="-34" width="192" height="68" rx="12" fill="#f8f3ea"/><rect x="-96" y="-34" width="8" height="68" rx="4" fill="#9a86ff"/>'
                   f'<text x="6" y="-8" {TH} font-size="12" font-weight="700" fill="#8a7fa0" text-anchor="middle">พื้นที่ทั้งเกาะ</text></g>', t0 + .3, t1 - .3, 'mask-right', .6)
          + M.counter(156, 258, 21, 'ราว {n} ตร.กม.', t0 + .6, t1 - .3, 22, '#1d1626', 0)
          + M.callout(330, 96, 180, ['ส่วนใหญ่', 'เป็นภูเขา'], 300, 400, t0 + 1.6, t1 - .5, '#2a7f86')
          + M.arrow('M 120,520 C 150,480 190,460 226,470', t0 + 2.6, t1 - .4, '#ffffff', 3.4)
          + M.reveal(f'<g transform="translate(96,546)"><rect x="-64" y="-16" width="128" height="32" rx="16" fill="#120e1c" fill-opacity=".85" stroke="#9a86ff"/><text x="0" y="5" {TH} font-size="13" font-weight="700" fill="#f2eefa" text-anchor="middle">บ้านอยู่บนเนิน</text></g>', t0 + 3.0, t1 - .3, 'fade-up', .5))
    return compose(fid, 'day', back, '', [], deck, light, '', '', S5.S5DEFS + S6.S6DEFS), ui


# ================================================================ dive shop pinboard: neighbours from all over the world
def pinboard(t0, t1):
    fid = 'PB'
    wall = wood_planks(0, 0, 540, 700, '#9c6e52', '#ad7f60', '#8a5e44', seed=5)
    cork = ('<rect x="46" y="150" width="456" height="380" fill="#000" opacity=".25" filter="url(#s4soft)"/><rect x="40" y="140" width="460" height="380" fill="#6f5442"/><rect x="52" y="152" width="436" height="356" fill="#c49a6c"/>'
            + ''.join(f'<circle cx="{random.Random(i).uniform(56, 484):.0f}" cy="{random.Random(i + 99).uniform(156, 504):.0f}" r="1.3" fill="#a07a50"/>' for i in range(160))
            + '<rect x="70" y="170" width="400" height="250" fill="#f3e8d2"/><rect x="70" y="170" width="400" height="250" fill="#a9c8d4" opacity=".55"/>')
    land = '#8fae86'
    cont = (f'<path d="M 90,200 C 110,186 150,190 160,210 C 168,230 150,250 156,270 C 160,290 176,300 170,330 C 164,360 150,380 140,400 C 132,380 128,350 120,330 C 108,300 96,280 92,250 Z" fill="{land}"/>'
            f'<path d="M 230,196 C 250,184 280,186 286,200 C 290,214 270,220 268,236 C 290,240 300,260 296,290 C 292,330 270,360 258,380 C 248,350 246,320 236,300 C 226,280 218,256 224,236 C 214,224 216,206 230,196 Z" fill="{land}"/>'
            f'<path d="M 290,192 C 330,180 400,184 440,200 C 456,214 446,236 424,244 C 410,262 396,270 380,268 C 372,280 360,286 352,276 C 340,262 330,250 312,246 C 296,236 284,214 290,192 Z" fill="{land}"/>'
            f'<path d="M 410,330 C 430,322 456,326 462,342 C 466,358 446,368 426,364 C 412,360 404,342 410,330 Z" fill="{land}"/>')
    kt = (378, 268)
    pins = [(110, 230, '#2f6fb5', 'แคนาดา'), (140, 330, '#2fb3b8', 'บราซิล'), (250, 210, '#e8735f', 'อังกฤษ'), (270, 220, '#7a5ab8', 'เยอรมนี'),
            (262, 330, '#d8a03a', 'แอฟริกาใต้'), (330, 210, '#e88aa8', 'รัสเซีย'), (420, 216, '#2f8f5a', 'ญี่ปุ่น'), (436, 342, '#c4463d', 'ออสเตรเลีย'), (300, 238, '#5a6c8e', 'ฝรั่งเศส')]
    strings, heads = '', ''
    for i, (x, y, c, n) in enumerate(pins):
        a = t0 + .5 + i * .22
        mx, my = (x + kt[0]) / 2, min(y, kt[1]) - 30
        strings += f'<path data-in="draw" data-at="{a:.2f}" data-dur=".7" data-out="fade" data-out-at="{t1 - .4:.2f}" d="M {x},{y} Q {mx:.0f},{my:.0f} {kt[0]},{kt[1]}" stroke="#c4463d" stroke-width="1.8" fill="none"/>'
        heads += M.pop(f'<circle cx="{x}" cy="{y + 2}" r="7" fill="#000" opacity=".25"/><circle cx="{x}" cy="{y}" r="6.5" fill="{c}"/><circle cx="{x - 2}" cy="{y - 2}" r="2" fill="#fff" opacity=".7"/>', a - .15, t1 - .3, .4)
    ktpin = M.pop(f'<circle cx="{kt[0]}" cy="{kt[1]}" r="11" fill="#c4463d"/><circle cx="{kt[0] - 3}" cy="{kt[1] - 3}" r="3.4" fill="#fff" opacity=".8"/>'
                  f'<g transform="translate({kt[0] + 6},{kt[1] + 22})"><rect x="-40" y="-13" width="80" height="26" rx="13" fill="#120e1c" stroke="#9a86ff"/><text x="0" y="5" {TH} font-size="13" font-weight="800" fill="#f2eefa" text-anchor="middle">เกาะเต่า</text></g>', t0 + .2, t1 - .3, .5)
    polas = ''.join(f'<g transform="translate({x},{y}) rotate({r})"><rect x="-34" y="-30" width="68" height="76" fill="#fbf8f0"/><rect x="-28" y="-24" width="56" height="50" fill="{c}"/>'
                    f'<path d="M -28,14 q 14,-10 28,0 q 14,10 28,0 L 28,26 L -28,26 Z" fill="#1f6f8e"/><circle cx="{4 - r % 5}" cy="-6" r="8" fill="#22303f"/><rect x="-6" y="0" width="20" height="10" rx="3" fill="#22303f"/></g>'
                    for x, y, r, c in ((110, 470, -6, '#3f93b4'), (200, 474, 4, '#2fb3b8'), (360, 470, -3, '#5fa8c4'), (448, 470, 7, '#3f93b4')))
    flags = '<path d="M 40,110 C 160,138 380,138 500,110" stroke="#c9b08a" stroke-width="2" fill="none"/>' + ''.join(
        f'<path d="M {60 + k * 40},{114 + 16 * math.sin(math.pi * k / 11):.0f} l 26,0 l -13,24 Z" fill="{c}"/>' for k, c in enumerate(('#c4463d', '#f4efe6', '#2f6fb5', '#2fb3b8', '#e8735f', '#7a5ab8', '#d8a03a', '#2f8f5a', '#e88aa8', '#5a6c8e', '#c4463d')))
    counter = ('<rect x="-10" y="690" width="560" height="280" fill="#6e4a34"/><rect x="-10" y="690" width="560" height="14" fill="#8a5e44"/>'
               '<g transform="translate(130,690)"><rect x="-26" y="-20" width="52" height="20" rx="7" fill="#22303f"/><rect x="-21" y="-16" width="42" height="12" rx="5" fill="#9ad7e3"/></g>'
               '<g transform="translate(400,690)"><path d="M -40,0 L 0,0 L 6,-50 L -46,-50 Z" fill="#2fb3b8"/><path d="M 4,0 L 44,0 L 50,-50 L -2,-50 Z" fill="#e8735f"/></g>')
    deco = shell_chime(500, 40, 5, 60) + lifebuoy(30, 620, 30) + buoy(500, 600, 14, '#e8735f')
    bd, bs, bc = beam_set(fid, [[(-20 + k * 46, 0), (6 + k * 46, 0), (300 + k * 46, 960), (270 + k * 46, 960)] for k in range(5)], '#fff4e2', .14)
    light = bs + fine_dust((0, 0, 540, 960), 220, 111, '#fff4e2', clip=bc)
    sh = CL.ao_line(0, 690, 540, 690, 14, .45)
    return compose(fid, 'warm', wall + flags + deco, sh, [], cork + cont + polas + strings + heads + ktpin + counter, light, '', '', bd)


# ================================================================ close-up: the phone on speaker in James's hand
def phone_screen(key, t0, t1):
    fid = 'PH'
    rnd = random.Random(12)
    room = ('<rect width="540" height="960" fill="#2a3048"/><rect x="40" y="60" width="460" height="520" fill="#3a4a70"/>'
            + ''.join(f'<circle cx="{rnd.uniform(40, 500):.0f}" cy="{rnd.uniform(60, 580):.0f}" r="{rnd.uniform(10, 34):.0f}" fill="{rnd.choice(["#ffd9a8", "#9fb8ff", "#cfe0ff"])}" opacity="{rnd.uniform(.08, .22):.2f}"/>' for _ in range(26))
            + '<rect x="40" y="580" width="460" height="20" fill="#4a3428"/>')
    rain = '<g class="om-rain">' + ''.join(f'<path d="M {rnd.uniform(40, 500):.0f},{rnd.uniform(0, 600):.0f} l -4,22" stroke="#cfe0ff" stroke-opacity="{rnd.uniform(.2, .5):.2f}" stroke-width="1.4"/>' for _ in range(120)) + '</g>'
    back = f'<g filter="url(#s4dof2)">{room}</g>' + rain
    SKp, SKSp = '#fbe7d8', '#efc7b0'
    hand = (f'<path d="M 330,960 L 300,700 L 400,690 L 470,960 Z" fill="{SKSp}"/>'
            f'<path d="M 190,620 C 186,560 230,540 270,546 L 380,560 C 420,566 430,640 410,700 L 300,720 C 240,720 196,680 190,620 Z" fill="{SKp}"/>'
            f'<path d="M 170,520 C 150,520 140,560 168,580 L 220,600 L 230,540 Z" fill="{SKp}"/>')
    phone = ('<g transform="translate(276,410) rotate(-6)"><rect x="-128" y="-250" width="256" height="500" rx="34" fill="#16161c"/><rect x="-118" y="-240" width="236" height="480" rx="28" fill="#0e1424"/>'
             '<rect x="-118" y="-240" width="236" height="480" rx="28" fill="url(#PHscr)"/><rect x="-30" y="-232" width="60" height="16" rx="8" fill="#000"/>'
             '<circle cx="0" cy="-130" r="44" fill="#2a3a5c"/><path d="M -24,-122 L -24,-142 L 8,-142 L 8,-122 Z M 8,-136 L 20,-136 L 26,-128 L 26,-122 L 8,-122 Z" fill="#9ad7e3"/><circle cx="-14" cy="-118" r="6" fill="#9ad7e3"/><circle cx="16" cy="-118" r="6" fill="#9ad7e3"/>'
             f'<text x="0" y="-62" {TH} font-size="19" font-weight="800" fill="#f2eefa" text-anchor="middle">ขนส่งด่วน</text>'
             f'<text x="0" y="-38" {TH} font-size="13" font-weight="600" fill="#9aa6c8" text-anchor="middle">สาขาชุมพร</text>'
             + ''.join(f'<rect class="om-envbar" data-key="{key}" data-t0="{t0:.3f}" data-i="{i}" x="{-90 + i * 12}" y="-14" width="7" height="28" rx="3.5" fill="#9a86ff"/>' for i in range(16))
             + f'<text x="0" y="56" {EN} font-size="14" font-weight="600" fill="#9aa6c8" text-anchor="middle">00:12 · ลำโพง</text>'
             '<circle cx="-60" cy="170" r="26" fill="#2a3048"/><circle cx="0" cy="170" r="26" fill="#7a5ab8"/><circle cx="60" cy="170" r="26" fill="#c4463d"/>'
             '<path d="M -8,164 L 0,158 L 8,164 L 8,178 L -8,178 Z" fill="#fff"/><path d="M 48,170 C 52,162 68,162 72,170" stroke="#fff" stroke-width="4" fill="none"/><path d="M -70,162 L -50,178 M -50,162 L -70,178" stroke="#9aa6c8" stroke-width="3"/></g>')
    thumb = f'<path d="M 410,520 C 440,500 470,520 460,560 L 420,640 L 380,600 Z" fill="{SKSp}"/>'
    defs = '<linearGradient id="PHscr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2a50"/><stop offset="1" stop-color="#0e1424"/></linearGradient>'
    light = CL.glow(276, 410, 300, '#9fb8ff', .22, core=False) + fine_dust((40, 60, 500, 600), 80, 121, '#cfe0ff')
    return compose(fid, 'night', back, '', [], hand + phone + thumb, light, '', '', defs)


# ================================================================ closing A/B question card
def ab_card(t0, t1, toggles):
    fid = 'AB'
    bg = ('<rect width="540" height="960" fill="#120e1c"/><circle cx="270" cy="420" r="380" fill="#3a2a5c" opacity=".55" filter="url(#s4soft)"/>'
          '<circle cx="270" cy="420" r="220" fill="#5a3a8c" opacity=".25" filter="url(#s4soft)"/>')
    eye = ('<g transform="translate(270,150)"><path d="M -34,0 Q 0,-26 34,0 Q 0,26 -34,0 Z" fill="none" stroke="#b18cff" stroke-width="3.4"/><circle r="10" fill="#b18cff"/><circle cx="3" cy="-3" r="3" fill="#fff"/></g>')
    q = (M.reveal(f'<text x="270" y="236" {TH} font-size="28" font-weight="800" fill="#ffffff" text-anchor="middle">ถ้าต้องย้ายมาเป็น<tspan fill="#c9a8ff">ชาวเกาะ</tspan></text>', t0 + .2, t1, 'fade-up', .6)
         + M.reveal(f'<text x="270" y="276" {TH} font-size="28" font-weight="800" fill="#ffffff" text-anchor="middle">คุณจะไหวไหม?</text>', t0 + .45, t1, 'fade-up', .6))

    def opt(y, letter, line1, line2, at):
        return M.reveal(f'<g transform="translate(270,{y})"><rect x="-210" y="-48" width="420" height="96" rx="18" fill="#1e1830" stroke="#4a3a6c" stroke-width="2"/>'
                        f'<rect x="-190" y="-30" width="60" height="60" rx="14" fill="#7a5ab8"/><text x="-160" y="12" {EN} font-size="30" font-weight="800" fill="#fff" text-anchor="middle">{letter}</text>'
                        f'<text x="-110" y="-6" {TH} font-size="20" font-weight="800" fill="#f2eefa">{line1}</text><text x="-110" y="20" {TH} font-size="14" font-weight="600" fill="#a99cc8">{line2}</text></g>', at, t1, 'fade-left', .6)
    opts = opt(370, 'A', 'ย้ายเลย ขอเป็นชาวเกาะ', 'มอไซค์ คลื่น ตุ๊กแก ไหวหมด', t0 + .8) + opt(490, 'B', 'ขออยู่กรุงเทพกับรถติดต่อ', 'ของส่งถึงบ้าน ไฟไม่ดับ', t0 + 1.05)
    hl = ''
    for i, (a, b) in enumerate(toggles):
        y = 370 if i % 2 == 0 else 490
        hl += (f'<g data-in="fade" data-at="{a:.2f}" data-dur=".18" data-out="fade" data-out-at="{b:.2f}" data-out-dur=".18">'
               f'<rect x="54" y="{y - 52}" width="432" height="104" rx="21" fill="none" stroke="#c9a8ff" stroke-width="4"/>'
               f'<rect x="60" y="{y - 48}" width="420" height="96" rx="18" fill="#c9a8ff" opacity=".12"/></g>')
    foot = M.reveal(f'<text x="270" y="590" {TH} font-size="15" font-weight="700" fill="#a99cc8" text-anchor="middle">ตอบในคอมเมนต์ได้เลย</text>', t0 + 1.6, t1, 'fade', .6)
    light = fine_dust((0, 0, 540, 960), 120, 131, '#c9a8ff')
    return compose(fid, 'night', bg, '', [], eye + q + opts + hl + foot, light, '', '', '')


# ================================================================ Mae Haad pier, true scale (people stand ON the deck, full figures)
def pier2(chars_in):
    """chars_in: [(inner, transform, foot_xy, face)]. Horizon y=360; James scale 1.0 = 320 px/m at feet y=905."""
    fid = 'PR'
    from style4 import fine_dust as FD
    sky = '<rect width="540" height="380" fill="#8ec4e8"/><rect y="230" width="540" height="150" fill="#d6ecf4"/>' + S5.cloud_bank(-20, 170, 280, 50, '#ffffff', '#eef3f8', '#c9d4e4', 3) + S5.cloud_bank(300, 120, 260, 40, '#ffffff', '#eef3f8', '#c9d4e4', 6)
    isl = S6.tropical_island(430, 372, 260, 70, 41, .4, '#d6ecf4', False, True, 2)
    sea = ('<rect y="360" width="540" height="140" fill="url(#s5sea)"/>' + S6.whitecaps(366, 480, 40, 5)
           + f'<g transform="translate(330,402) scale(.62)">{K.ferry(0, 0, 1)}</g>' + K.longtail(90, 430, .42))
    # deck in perspective: vanishing point (270,360)
    deck = '<path d="M -10,480 L 550,480 L 550,970 L -10,970 Z" fill="#b89a7a"/>'
    for i in range(-9, 11):
        x = 270 + i * 60
        deck += f'<path d="M {270 + (x - 270) * .22:.0f},480 L {x},970" stroke="#9a7c5e" stroke-width="2"/>'
    for k in range(9):
        y = 480 + (k / 8) ** 1.7 * 490
        deck += f'<path d="M -10,{y:.0f} L 550,{y:.0f}" stroke="#a68866" stroke-width="{1 + k * .35:.1f}" opacity=".7"/>'
    deck += '<rect x="-10" y="474" width="560" height="8" fill="#7d6450"/>'
    posts = ''.join(f'<rect x="{x}" y="436" width="9" height="44" rx="2" fill="#7d553c"/>' for x in (20, 140, 260, 380, 500)) + '<path d="M 24,446 Q 84,462 144,446 Q 204,462 264,446 Q 324,462 384,446 Q 444,462 504,446" stroke="#c9b08a" stroke-width="2.4" fill="none"/>'
    bollard = '<g transform="translate(470,940)"><rect x="-26" y="-60" width="52" height="60" rx="8" fill="#3a3d48"/><rect x="-32" y="-66" width="64" height="12" rx="5" fill="#4a4e5a"/></g>'
    # the move: boxes ~45 cm, fan, rice cooker, wok on top (320 px/m at y~900)
    stack = (K.cardboard(330, 760, 150, 140, 'ครัว') + K.cardboard(344, 626, 130, 134, 'มีด') + K.cardboard(354, 506, 116, 120)
             + '<g transform="translate(412,506)"><rect x="-34" y="-70" width="68" height="70" rx="8" fill="#f4efe6"/><rect x="-34" y="-70" width="68" height="18" rx="8" fill="#d6d0c4"/><rect x="18" y="-60" width="5" height="12" fill="#9aa1b0"/></g>'
             + '<g transform="translate(410,436)"><ellipse cx="0" cy="0" rx="50" ry="10" fill="#2a2c34"/><path d="M 46,-2 L 96,-14" stroke="#2a2c34" stroke-width="7" stroke-linecap="round"/></g>'
             + '<g transform="translate(292,905)"><rect x="-6" y="-120" width="12" height="120" fill="#d6d0c4"/><ellipse cx="0" cy="0" rx="40" ry="10" fill="#c9c3b8"/>'
             '<circle cx="0" cy="-160" r="48" fill="none" stroke="#e8e4dc" stroke-width="4"/><circle cx="0" cy="-160" r="48" fill="#7fb3c4" opacity=".25"/>'
             + ''.join(f'<ellipse cx="0" cy="-186" rx="12" ry="26" fill="#9ccbd6" transform="rotate({a} 0 -160)"/>' for a in (0, 120, 240)) + '<circle cx="0" cy="-160" r="9" fill="#e8e4dc"/></g>')
    ch = [char(fid, inner, tr, (-40, -40), foot, 'warm', face) for inner, tr, foot, face in chars_in]
    sh = ''.join(CL.contact_shadow(f[0], f[1], 60 * (f[1] - 360) / 545) for _, _, f, _ in chars_in) + CL.contact_shadow(405, 902, 90, 8) + CL.contact_shadow(292, 906, 46, 6)
    back = f'<g filter="url(#s4dof2)">{sky}{isl}</g><g filter="url(#s4dof)">{sea}</g>' + deck + posts
    light = CL.glow(-40, -40, 420, '#fffaf0', .2, core=False) + FD((0, 340, 540, 760), 140, 22, '#ffffff', density_far=.75)
    return compose(fid, 'warm', back, sh, ch, stack + bollard, light, '', '', S5.S5DEFS + S6.S6DEFS)
