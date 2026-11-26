"""EP.01 round 6: protagonist renamed James (subtitles say "เจม"), better tropical islands everywhere,
a rough-sea viewpoint (big curling waves, whitecaps, spray on granite), smaller scooter.
Run: python3 style6.py -> scenes_v6.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
import kt_scenes as K
import style5 as S5
from style3 import wood_planks
from style4 import beam_set, fine_dust, buoy, lifebuoy, flipflops_rack, tag, step, callout, subs, char, compose, uid, EYE
from scenes import palm, boulder
ISL = K.ISL
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'


def mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join(f'{round(x + (y - x) * t):02x}' for x, y in zip(a, b))


# ================================================================ tropical island (Koh Tao look: jungle canopy, granite boulders, white sand)
def tropical_island(cx, base, w, h, seed=1, haze=0.0, haze_col='#c8d8e4', sun_left=True, beach=True, houses=0):
    """cx/base = centre and waterline in px; w/h = size; haze 0..1 pushes colours toward the sky for distance."""
    rnd = random.Random(seed)
    col = lambda c: mix(c, haze_col, haze)
    dark, mid, light, lit = col('#2f5e46'), col('#3f7a52'), col('#5a9a5e'), col('#86bc72')
    # ridgeline: two or three summits, irregular
    n = 16
    peaks = [(rnd.uniform(.25, .4), rnd.uniform(.85, 1)), (rnd.uniform(.55, .75), rnd.uniform(.6, .85))]
    pts = []
    for i in range(n + 1):
        t = i / n
        hgt = max(p[1] * math.exp(-((t - p[0]) / .2) ** 2) for p in peaks)
        hgt *= min(1, t * 6, (1 - t) * 6)
        pts.append((cx - w / 2 + w * t, base - h * hgt * rnd.uniform(.93, 1.04)))
    ridge = 'M ' + ' L '.join(f'{x:.0f},{y:.0f}' for x, y in pts) + f' L {cx + w / 2:.0f},{base} L {cx - w / 2:.0f},{base} Z'
    out = f'<path d="{ridge}" fill="{dark}"/>'
    # canopy: overlapping tree crowns, darker low, lit on the sun side
    crowns = ''
    for i in range(int(w * h / 220)):
        t = rnd.random()
        x = cx - w / 2 + w * t
        top_y = min(y for (px, y) in pts if abs(px - x) < w / n + 1) if True else base
        y = rnd.uniform(top_y + 4, base - 2)
        r = rnd.uniform(.035, .07) * w * (1 - .4 * (base - y) / max(h, 1))
        c = rnd.choice([mid, mid, light, dark])
        crowns += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{c}"/>'
        if (sun_left and rnd.random() < .5) or (not sun_left and rnd.random() < .5):
            crowns += f'<circle cx="{x + (-r * .35 if sun_left else r * .35):.0f}" cy="{y - r * .35:.0f}" r="{r * .55:.1f}" fill="{lit}" opacity=".85"/>'
    clip = uid('isl')
    out += f'<clipPath id="{clip}"><path d="{ridge}"/></clipPath><g clip-path="url(#{clip})">{crowns}</g>'
    # ridge rim light
    half = pts[: n // 2 + 1] if sun_left else pts[n // 2:]
    out += f'<path d="M ' + ' L '.join(f'{x:.0f},{y:.0f}' for x, y in half) + f'" stroke="{col("#c8e0a0")}" stroke-width="{max(1, w / 260):.1f}" fill="none" opacity=".7"/>'
    # palms poking over the ridge
    for i in range(3):
        px, py = pts[rnd.randint(3, n - 3)]
        out += f'<g transform="translate({px:.0f},{py + 4:.0f}) scale({w / 1400:.3f})">{palm(0, 0, 1, rnd.random() < .5, 1).replace("#2f6b5a", dark).replace("#3f8a6e", mid).replace("#4fa07c", light)}</g>'
    # houses tucked in the trees
    for i in range(houses):
        hx = cx - w * .3 + rnd.uniform(0, w * .6)
        hy = base - rnd.uniform(.12, .45) * h
        s = w / 260
        out += f'<rect x="{hx:.0f}" y="{hy:.0f}" width="{7 * s:.1f}" height="{5 * s:.1f}" fill="{col("#f4efe4")}"/><path d="M {hx - s:.1f},{hy:.0f} l {4.5 * s:.1f},{-3.5 * s:.1f} l {4.5 * s:.1f},{3.5 * s:.1f} Z" fill="{col("#c87a5e")}"/>'
    # white sand + granite boulders at the waterline
    if beach:
        bw = w * rnd.uniform(.25, .4)
        bx = cx - w / 2 + w * rnd.uniform(.1, .5)
        out += f'<path d="M {bx:.0f},{base} C {bx + bw * .2:.0f},{base - h * .05:.0f} {bx + bw * .8:.0f},{base - h * .05:.0f} {bx + bw:.0f},{base} Z" fill="{col("#f6ecd8")}"/>'
    for i in range(int(w / 40) + 2):
        bx = cx - w / 2 + rnd.uniform(0, w)
        bw, bh = rnd.uniform(.03, .07) * w, rnd.uniform(.02, .05) * w
        out += boulder(round(bx), round(base + 1), round(bw), round(bh), rnd.randint(0, 1)).replace('#a9a5a9', col('#b2aca8')).replace('#86828a', col('#8a8488')).replace('#c9c5c8', col('#d6d0cc'))
    # turquoise shallows halo
    halo = f'<ellipse cx="{cx:.0f}" cy="{base + 3:.0f}" rx="{w * .58:.0f}" ry="{max(4, h * .09):.0f}" fill="{col("#7fdcd0")}" opacity="{.75 * (1 - haze):.2f}"/>'
    return halo + out


# ================================================================ waves
def whitecaps(y0, y1, n, seed=1, col='#f4f8fa'):
    rnd = random.Random(seed)
    out = ''
    for i in range(n):
        t = (rnd.random()) ** 1.5
        y = y0 + t * (y1 - y0)
        w = 6 + t * 70
        x = rnd.uniform(-30, 560)
        out += (f'<path d="M {x:.0f},{y:.0f} q {w * .3:.0f},{-2 - t * 5:.1f} {w * .6:.0f},{-1 - t * 2:.1f} q {w * .25:.0f},{1 + t * 3:.1f} {w * .4:.0f},{1 + t * 2:.1f}" '
                f'stroke="{col}" stroke-width="{1 + t * 3.5:.1f}" fill="none" stroke-linecap="round" opacity="{.45 + t * .45:.2f}"/>')
    return out


def big_wave(x, y, w, h, body='#1f6a7c', face='#2f8a96', seed=2):
    """A rolling wave seen from the side-front: dark face, curling lip, foam crest and spray."""
    rnd = random.Random(seed)
    face_d = (f'M {x},{y} C {x + w * .2:.0f},{y - h * .2:.0f} {x + w * .45:.0f},{y - h * .9:.0f} {x + w * .62:.0f},{y - h:.0f} '
              f'C {x + w * .74:.0f},{y - h * 1.04:.0f} {x + w * .8:.0f},{y - h * .78:.0f} {x + w * .72:.0f},{y - h * .6:.0f} '
              f'C {x + w * .86:.0f},{y - h * .62:.0f} {x + w * .95:.0f},{y - h * .25:.0f} {x + w},{y} Z')
    g = uid('wv')
    out = (f'<defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{face}"/><stop offset="1" stop-color="{body}"/></linearGradient></defs>'
           f'<path d="{face_d}" fill="url(#{g})"/>'
           f'<path d="M {x + w * .3:.0f},{y - h * .45:.0f} C {x + w * .42:.0f},{y - h * .7:.0f} {x + w * .52:.0f},{y - h * .86:.0f} {x + w * .6:.0f},{y - h * .92:.0f}" stroke="#7fc8cc" stroke-width="3" fill="none" opacity=".5"/>')
    # foam on the lip and pouring down the face
    foam = ''
    for i in range(26):
        t = rnd.random()
        fx = x + w * (.55 + .4 * t)
        fy = y - h * (1 - .9 * t ** 1.4) + rnd.uniform(-6, 6)
        foam += f'<circle cx="{fx:.0f}" cy="{fy:.0f}" r="{rnd.uniform(4, 12):.1f}" fill="#f4f8fa" opacity="{rnd.uniform(.7, 1):.2f}"/>'
    out += f'<g filter="url(#s6foam)">{foam}</g>'
    out += ''.join(f'<path d="M {x + w * rnd.uniform(.1, .6):.0f},{y - h * rnd.uniform(.05, .4):.0f} q 14,-4 28,0" stroke="#d8eef0" stroke-width="2" fill="none" opacity=".55"/>' for _ in range(8))
    return out


def spray(cx, cy, r, seed=3):
    rnd = random.Random(seed)
    blobs = ''.join(f'<circle cx="{cx + rnd.uniform(-r, r):.0f}" cy="{cy - rnd.uniform(0, r * 1.4):.0f}" r="{rnd.uniform(r * .12, r * .3):.1f}" fill="#f8fbfc" opacity="{rnd.uniform(.5, .95):.2f}"/>' for _ in range(28))
    drops = ''.join(f'<circle cx="{cx + rnd.uniform(-r * 1.6, r * 1.6):.0f}" cy="{cy - rnd.uniform(0, r * 2):.0f}" r="{rnd.uniform(.8, 2.4):.1f}" fill="#ffffff" opacity="{rnd.uniform(.5, .9):.2f}"/>' for _ in range(80))
    return f'<g filter="url(#s6foam)">{blobs}</g><g>{drops}</g>'


S6DEFS = ('<filter id="s6foam" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4"/></filter>'
          '<linearGradient id="s6storm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4064"/><stop offset=".45" stop-color="#6a6488"/><stop offset=".75" stop-color="#c890a0"/><stop offset="1" stop-color="#f2b89c"/></linearGradient>'
          '<linearGradient id="s6sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5e7896"/><stop offset=".2" stop-color="#2f5f78"/><stop offset="1" stop-color="#173c50"/></linearGradient>')


# ================================================================ rough-sea viewpoint
def rough_sea():
    fid = 'X1'
    sunx, suny, hz = 410, 400, 430
    sky = (f'<rect width="540" height="{hz + 6}" fill="url(#s6storm)"/>'
           + S5.wisps(80, 240, '#8a86a8', 8, 51)
           + S5.cloud_bank(-60, 170, 420, 90, '#c8a8c0', '#7a7098', '#4a4a6a', 51, False)
           + S5.cloud_bank(200, 120, 400, 80, '#d8b0c0', '#807698', '#4a4a6a', 52, True)
           + f'<circle cx="{sunx}" cy="{suny}" r="170" fill="url(#s5sunglow)" opacity=".8"/><circle cx="{sunx}" cy="{suny}" r="20" fill="#fff4e4"/>'
           + S5.cloud_bank(40, 330, 300, 46, '#f0b8a8', '#a88aa8', '#6e6488', 53, False)
           + S5.cloud_bank(330, 360, 260, 34, '#f8c8b0', '#b494b0', '#7a6c90', 54, True)
           + ''.join(f'<path d="M {x},{suny + 30} L {x - 40},{hz}" stroke="#ffe0c8" stroke-width="10" opacity=".08" filter="url(#s5wisp)"/>' for x in (380, 410, 440)))
    islands = (tropical_island(110, hz + 2, 220, 34, 5, .65, '#b8a0b8', False, True, 2)
               + tropical_island(470, hz + 2, 170, 26, 6, .7, '#b8a0b8', False, False, 1))
    sea = f'<rect y="{hz}" width="540" height="{960 - hz}" fill="url(#s6sea)"/>' + f'<rect y="{hz - 4}" width="540" height="14" fill="#e8b8b0" opacity=".45" filter="url(#s5haze)"/>'
    rnd = random.Random(7)
    for i in range(80):                                        # broken light path
        t = rnd.random() ** 1.4
        y = hz + 4 + t * 300
        spread = 10 + t * 100
        sea += f'<rect x="{sunx + rnd.uniform(-spread, spread):.0f}" y="{y:.0f}" width="{4 + t * 20:.0f}" height="{1 + t * 2:.1f}" rx="1" fill="#ffe4cc" opacity="{.25 + (1 - t) * .45:.2f}"/>'
    sea += '<g class="om-caps">' + whitecaps(hz + 6, 800, 160, 8) + '</g>'
    waves = big_wave(-40, 690, 380, 120, '#18485c', '#2f7f8e', 3) + big_wave(250, 640, 330, 80, '#1c5266', '#3a8a96', 4)
    waves = f'<g class="om-wave">{waves}</g>'
    rocks = (boulder(-120, 980, 330, 280, 1) + boulder(120, 990, 160, 110, 0))
    ledge = boulder(250, 1000, 340, 250, 1) + '<path d="M 290,790 C 360,770 470,770 560,786 L 560,800 C 470,790 360,790 290,806 Z" fill="#c9c5c8" opacity=".6"/>'
    crash = '<g class="om-spray">' + spray(150, 830, 110, 5) + spray(330, 860, 70, 6) + '</g>'
    foam_band = '<path d="M -20,850 C 80,820 200,860 300,840 C 400,820 480,850 560,836 L 560,880 L -20,880 Z" fill="#f2f8fa" opacity=".75" filter="url(#s6foam)"/>'
    back = sky + f'<g filter="url(#s4dof)">{islands}</g>' + sea + waves
    j_tr = 'translate(446,508) scale(.58)'
    dog_tr = 'translate(360,738) scale(.3)'
    wind = ''.join(f'<path d="M {x},{y} q 40,-8 80,0" stroke="#ffffff" stroke-opacity=".35" stroke-width="2" fill="none" stroke-linecap="round"/>' for x, y in ((40, 260), (300, 300), (120, 520), (380, 470), (20, 600)))
    light = CL.glow(sunx, suny, 240, '#ffcfb0', .22, core=False) + fine_dust((0, 500, 540, 960), 260, 61, '#ffffff', density_far=.7)
    chars = [char(fid, S5.sun_island('dead'), j_tr, (sunx, suny), (446, 640), 'dusk', 'sun'), char(fid, ISL['DOG'], dog_tr, (sunx, suny), (360, 780), 'dusk', None)]
    sh = ''
    ui = tag('สองปีต่อมา · หน้าผาริมทะเล') + subs('วันนี้คลื่นแรง…/ของคงไม่มาอีกแล้ว', 'Rough sea today…/my parcel isn’t coming again.')
    back += foam_band + rocks + crash + ledge + CL.contact_shadow(446, 794, 34) + CL.contact_shadow(360, 790, 26, 5)
    return compose(fid, 'dusk', back, sh, chars, '', light, wind, ui, S5.S5DEFS + S6DEFS)


# ================================================================ islands applied to other views
def street():
    svg = S5.street()
    old_hill_start = svg.find('<path d="M -20,400 C 80,330 200,320 300,350')
    if old_hill_start >= 0:
        end = svg.find('</g>', old_hill_start)
        hill = svg[old_hill_start:end]
        svg = svg.replace(hill, tropical_island(150, 400, 360, 90, 11, .35, '#d6ecf4', False, True, 3) + tropical_island(470, 400, 220, 60, 12, .45, '#d6ecf4', False, False, 1))
    return svg


def vista_calm():
    """Calm sunset over Koh Nang Yuan with the new island renderer (the earlier 'skull' islands replaced)."""
    svg = S5.vista()
    a = svg.find('<g transform="translate(250,606) scale(1.25)">')
    if a >= 0:
        depth, i = 0, a
        while True:
            o, c = svg.find('<g', i + 1), svg.find('</g>', i + 1)
            if o != -1 and o < c:
                depth += 1; i = o
            else:
                if depth == 0:
                    end = c + 4; break
                depth -= 1; i = c
        ny = ('<ellipse cx="250" cy="612" rx="300" ry="50" fill="url(#s5shal)" opacity=".8"/>'
              '<path d="M 100,610 C 160,598 220,600 250,604 C 280,600 340,598 400,610 C 340,616 280,614 250,612 C 220,614 160,616 100,610 Z" fill="#fbefe0"/>'
              + tropical_island(120, 612, 180, 92, 21, .25, '#e8b8c0', False, False, 1)
              + tropical_island(250, 610, 110, 58, 22, .25, '#e8b8c0', False, False, 0)
              + tropical_island(390, 612, 170, 82, 23, .25, '#e8b8c0', False, False, 1))
        svg = svg[:a] + ny + svg[end:]
    return svg


RENAMES = [('ผู้ชายคนนี้ชื่อซัน', 'ผู้ชายคนนี้ชื่อเจม'), ('This is Sun,', 'This is James,'), ('Open Water · SUN', 'Open Water · JAMES'),
           ('ถึง: ซัน', 'ถึง: เจม'), ('aria-label="ชุดซัน"', 'aria-label="ชุดเจม"')]


def renamed(svg):
    for a, b in RENAMES:
        svg = svg.replace(a, b)
    return svg


SHOTS = [
    (lambda: renamed(S5.outfit_card()), 'เจม · ชุดกรุงเทพกับชุดชาวเกาะ', 'เปลี่ยนชื่อตัวเอกเป็นเจมส์ (ซับไทยและเสียงพากย์ใช้ "เจม" ตามกฎช่อง)'),
    (lambda: renamed(street()), 'ถนนหน้าร้านดำน้ำ · เช้า', 'มอเตอร์ไซค์ถอยไปจอดไกลขึ้น ตัวเล็กลง · เนินเขาหลังทะเลเปลี่ยนเป็นเกาะแบบใหม่'),
    (rough_sea, 'หน้าผาริมทะเล · คลื่นแรง', 'ทำใหม่ทั้งหมด · คลื่นลูกใหญ่ม้วนเข้าฝั่ง ฟองขาวทั่วทะเล คลื่นซัดโขดหินแกรนิตแตกเป็นละออง · ฟ้าครึ้มมีแสงเย็นลอด · เกาะไกล ๆ ในหมอก · เจมยืนนิ่งกับหมา'),
    (lambda: renamed(vista_calm()), 'จุดชมวิวเกาะนางยวน · เย็น (ทะเลสงบ)', 'เกาะสามเกาะวาดใหม่: ป่าเป็นพุ่มไม้ซ้อนชั้นรับแสง โขดหินแกรนิตที่ชายฝั่ง น้ำตื้นสีฟ้าใส หมอกตามระยะ · ใช้ได้ถ้าอยากมีช็อตทะเลสงบ'),
    (lambda: renamed(S5.g_parcel()), 'กราฟิก · กล่องพัสดุ', 'เปลี่ยนชื่อบนฉลากเป็น "ถึง: เจม"'),
]


def build():
    figs = ''.join(f'<figure>{fn()}<figcaption><span class="n">{i:02d}</span> <b>{t}</b><span class="note">{n}</span></figcaption></figure>' for i, (fn, t, n) in enumerate(SHOTS, 1))
    page = open(os.path.join(HERE, 'scenes_v5.html')).read()
    head = page[:page.index('<div class="wrap">')].replace('รอบ 5</title>', 'รอบ 6</title>')
    out = head + f'''<div class="wrap">
  <h1>ฉาก EP.01 เกาะเต่า · รอบ 6<span>ตัวเอกชื่อเจม · เกาะแบบใหม่ · ฉากคลื่นแรง · มอเตอร์ไซค์เล็กลง</span></h1>
  <div class="grid">{figs}</div>
</div>
'''
    open(os.path.join(HERE, 'scenes_v6.html'), 'w').write(out)
    print(len(out))


if __name__ == '__main__':
    build()
