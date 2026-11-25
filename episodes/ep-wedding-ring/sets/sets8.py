# Odd Hours · ตอนงานแต่ง · รอบ 7: ห้องพิธีโทนงาช้าง-เงิน เพิ่มรายละเอียดให้ขลัง หรูแต่น่าขนลุก
# รัน: python3 sets7.py -> sets7.html
import math, random
import sets4 as S
import sets3 as T
from sets import Cam, fx, city
from sets5 import VARIANTS

V = VARIANTS['S']
for key in ('CRM_L', 'CRM', 'CRM_M', 'CRM_D', 'CRM_DD', 'GLD', 'GLD_L', 'GLD_D', 'RED', 'RED_L', 'RED_D', 'RED_DD'):
    setattr(S, key, V[key])
# เก้าอี้ชิวารีจาก sets3 เปลี่ยนเป็นเงินกับเบาะงาช้าง
T.GOLD, T.GOLD_L, T.GOLD_D = V['GLD'], V['GLD_L'], V['GLD_D']
T.CREAM, T.CREAM_D, T.SHADOW = '#f4eee4', '#c9bca8', '#3a3540'
SV, SV_L, SV_D = V['GLD'], V['GLD_L'], V['GLD_D']
rect, poly = S.rect, S.poly

def clock(cx, cy, r):
    """นาฬิกาเงินในโค้งหน้าต่าง เข็มหยุดที่ใกล้เที่ยงคืน"""
    o = [f'<circle cx="{cx}" cy="{cy}" r="{r + 7}" fill="{SV_D}"/>', f'<circle cx="{cx}" cy="{cy}" r="{r + 4}" fill="{SV}"/>',
         f'<path d="M{fx(cx - r - 4)},{cy} A{r + 4},{r + 4} 0 0,1 {fx(cx + r + 4)},{cy}" fill="none" stroke="{SV_L}" stroke-width="2"/>',
         f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f6f1e6"/>', f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#clockShade)"/>']
    for i in range(60):
        a = math.radians(i * 6 - 90); L = 6 if i % 5 == 0 else 2.5
        o.append(f'<path d="M{fx(cx + math.cos(a) * (r - 3))},{fx(cy + math.sin(a) * (r - 3))} L{fx(cx + math.cos(a) * (r - 3 - L))},{fx(cy + math.sin(a) * (r - 3 - L))}" stroke="#4a4650" stroke-width="{1.6 if i % 5 == 0 else .7}"/>')
    for i, a_deg in ((0, -90), (1, -150.5)):  # นาที 59 ชั่วโมงใกล้ 12
        pass
    mh = math.radians(354 - 90); hh = math.radians(358 - 90)
    o.append(f'<path d="M{cx},{cy} L{fx(cx + math.cos(hh) * r * .5)},{fx(cy + math.sin(hh) * r * .5)}" stroke="#2c2930" stroke-width="3" stroke-linecap="round"/>')
    o.append(f'<path d="M{cx},{cy} L{fx(cx + math.cos(mh) * r * .78)},{fx(cy + math.sin(mh) * r * .78)}" stroke="#2c2930" stroke-width="1.8" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="{SV_D}"/>')
    return ''.join(o)

def portrait(cx, cy, rx, ry, seed):
    """ภาพเหมือนเจ้าสาวในกรอบวงรีเงิน หน้าจมอยู่ในเงา เห็นแค่ผ้าคลุม"""
    o = [f'<ellipse cx="{cx + 3}" cy="{cy + 4}" rx="{rx + 6}" ry="{ry + 6}" fill="#3a3540" opacity=".3" filter="url(#sf4)"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 6}" ry="{ry + 6}" fill="{SV_D}"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="{rx + 4}" ry="{ry + 4}" fill="{SV}"/>',
         f'<path d="M{cx - rx - 4},{cy} A{rx + 4},{ry + 4} 0 0,1 {cx + rx + 4},{cy}" fill="none" stroke="{SV_L}" stroke-width="1.6"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#2e2a33"/>']
    cid = f'pt{seed}'
    o.append(f'<clipPath id="{cid}"><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}"/></clipPath><g clip-path="url(#{cid})">')
    o.append(f'<path d="M{cx - rx},{cy + ry} Q{cx - rx * .6},{cy - ry * .1} {cx},{cy - ry * .2} Q{cx + rx * .6},{cy - ry * .1} {cx + rx},{cy + ry}Z" fill="#4a4550"/>')
    o.append(f'<ellipse cx="{cx}" cy="{fx(cy - ry * .25)}" rx="{fx(rx * .34)}" ry="{fx(ry * .3)}" fill="#3a3640"/>')
    o.append(f'<path d="M{fx(cx - rx * .55)},{cy + ry} Q{fx(cx - rx * .6)},{fx(cy - ry * .7)} {cx},{fx(cy - ry * .62)} Q{fx(cx + rx * .6)},{fx(cy - ry * .7)} {fx(cx + rx * .55)},{cy + ry}" fill="#e9e4ec" opacity=".42"/>')
    o.append(f'<ellipse cx="{fx(cx - rx * .3)}" cy="{fx(cy - ry * .4)}" rx="{fx(rx * .3)}" ry="{fx(ry * .5)}" fill="#ffffff" opacity=".08"/></g>')
    return ''.join(o)

def pillar_candles(cx, base, seed, s=1.0):
    r = random.Random(seed); o = []
    items = sorted([(r.uniform(-1, 1), r.uniform(30, 78), r.uniform(7, 10)) for _ in range(6)], key=lambda t: -t[1])
    o.append(f'<ellipse cx="{fx(cx + 6)}" cy="{fx(base + 2)}" rx="{fx(38 * s)}" ry="{fx(6 * s)}" fill="#3a3540" opacity=".28" filter="url(#sf4)"/>')
    for dx, h, w in items:
        x = cx + dx * 26 * s; h *= s; w *= s; y = base + (dx + 1) * 2 * s
        o.append(rect(x - w, y - h, w * 2, h, '#f8f3ea'))
        o.append(rect(x + w * .25, y - h, w * .75, h, '#ddd2c2'))
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y - h)}" rx="{fx(w)}" ry="{fx(w * .3)}" fill="#fffaf2"/>')
        for k in range(2):
            dxp = r.uniform(-.7, .5) * w
            o.append(f'<path d="M{fx(x + dxp - 1.4)},{fx(y - h)} v{fx(r.uniform(6, 18) * s)} a1.4,1.4 0 0,0 2.8,0 v{fx(-r.uniform(6, 18) * s)}Z" fill="#fffaf2"/>')
        o.append(S.flame(x, y - h - 1, s * .9))
    return ''.join(o)

def fog(seed, y0, y1, n, op=.18):
    r = random.Random(seed); o = []
    for i in range(n):
        x = r.uniform(-60, 600); y = r.uniform(y0, y1)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(80, 170):.0f}" ry="{r.uniform(10, 22):.0f}" fill="#eef0f6" opacity="{r.uniform(op * .5, op):.2f}" filter="url(#bl4)"/>')
    return ''.join(o)

# ---------------------------------------------------------------- ตัวละครในฉาก
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'characters'))
import supporting as SP
import wedding_chars as WC
import bride_v2 as B2

def place(inner, x, feet, s, local_feet, shadow_w=70):
    sh = f'<ellipse cx="{x + 10 * s:.1f}" cy="{feet + 2:.1f}" rx="{shadow_w * s:.1f}" ry="{9 * s:.1f}" fill="#3a3540" opacity=".32" filter="url(#sf4)"/>'
    return sh + f'<g transform="translate({x:.1f},{feet - local_feet * s:.1f}) scale({s:.3f})">{inner}</g>'

def sup(fn):
    name, note, kind, back, head, body = fn()
    return back + body + head, (460 if kind == 'f' else 488)

def cast():
    items = []
    for fn, x, feet, s in ((SP.c_woman_black, 40, 690, .42), (SP.c_staff, 150, 688, .40), (SP.c_guard, 474, 700, .42),
                           (SP.c_guest_w, 392, 702, .42), (SP.c_guest_m, 432, 706, .42), (SP.c_bridesmaid, 160, 748, .48),
                           (SP.c_mother, 380, 762, .50)):
        inner, lf = sup(fn)
        items.append((feet, place(inner, x, feet, s, lf, 40)))
    bride = '<use href="#b2back"/>' + WC.bride_body() + '<use href="#b2head"/>'
    groom = WC.groom_body() + '<use href="#ghead"/><path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="#d8d4ce" stroke-width="2"/>'
    items.append((845, place(bride, 228, 845, .58, 462, 110)))
    items.append((848, place(groom, 316, 848, .58, 488, 50)))
    items.sort(key=lambda t: t[0])
    back = ''.join(p for _, p in items)
    inner, lf = sup(SP.c_photographer)
    front = place(inner, 96, 912, .66, lf, 46)
    return back, front

CAST_BACK, CAST_FRONT = cast()

def scene():
    o = []
    H = 640
    o.append(rect(0, 0, 540, H, 'url(#wall7)'))
    # บัวเพดานโค้งพร้อมลายฟันปลา
    o.append(f'<path d="M0,0 H540 V70 Q270,10 0,70Z" fill="#cfc6b6"/>')
    o.append(f'<path d="M0,70 Q270,10 540,70" stroke="{SV}" stroke-width="4" fill="none"/>')
    for i in range(41):
        t = i / 40; x = t * 540; y = 70 - 60 * 4 * t * (1 - t) * .5 * 2 + 6
        o.append(rect(x - 3, y, 6, 6, S.CRM_M))
    o.append(f'<path d="M0,82 Q270,22 540,82" stroke="{S.CRM_L}" stroke-width="2" fill="none"/>')
    # หน้าต่าง
    def win_city(x0, x1, top, seed, maxh):
        w = S.window(x0, x1, top, H - 8, seed)
        mark = 'filter="url(#mottle4)" opacity=".16" style="mix-blend-mode:screen"/>'
        i = w.index(mark) + len(mark)
        sky = f'<g filter="url(#blur7)">{city(x0, x1, H - 8, seed, maxh=maxh)}</g>'
        return w[:i] + sky + w[i:]
    o.append(win_city(178, 362, 110, 71, 230))
    o.append(win_city(-60, 112, 178, 72, 170))
    o.append(win_city(428, 600, 178, 73, 170))
    # ในหน้าต่างกลาง
    o.append(f'<clipPath id="moonC"><path d="{S.arch(178, 362, 110, H - 8)}"/></clipPath><g clip-path="url(#moonC)">')
    o.append('</g>')
    o.append(clock(270, 178, 40))
    # เสา + ภาพเจ้าสาวในกรอบวงรี
    o.append(S.pilaster(122, 168, 236, H))
    o.append(S.pilaster(372, 418, 236, H))
    o.append(portrait(145, 150, 19, 26, 1))
    o.append(portrait(395, 150, 19, 26, 2))
    for x in (145, 395):
        o.append(f'<path d="M{x - 10},118 Q{x},106 {x + 10},118" stroke="{SV}" stroke-width="2" fill="none"/><circle cx="{x}" cy="110" r="3" fill="{SV}"/>')
    # ไฟผนังเงินบนเสา
    for x in (145, 395):
        y = 360
        o.append(f'<circle cx="{x}" cy="{y - 18}" r="40" fill="url(#chGlow4)"/>')
        o.append(rect(x - 3, y - 8, 6, 26, SV)); o.append(rect(x, y - 8, 3, 26, SV_D))
        for d in (-1, 1):
            o.append(f'<path d="M{x},{y + 10} q{d * 14},4 {d * 15},-12" stroke="{SV}" stroke-width="2.4" fill="none"/>')
            o.append(rect(x + d * 15 - 5, y - 4, 10, 3, SV_L)); o.append(S.candle(x + d * 15, y - 4, .8, 16))
    o.append(rect(0, H - 22, 540, 22, S.CRM_M)); o.append(rect(0, H - 22, 540, 4, S.CRM_L)); o.append(rect(0, H - 4, 540, 4, S.CRM_DD))
    # พื้นหินอ่อน
    o.append(rect(0, H, 540, 320, 'url(#floor7)'))
    r = random.Random(4)
    for i in range(50):
        x = r.uniform(-40, 540); y = r.uniform(650, 950); L = r.uniform(60, 170)
        o.append(f'<path d="M{x:.0f},{y:.0f} c{L * .3:.0f},{r.uniform(-8, 8):.0f} {L * .6:.0f},{r.uniform(-14, 14):.0f} {L:.0f},{r.uniform(-6, 18):.0f}" stroke="#a8a2a0" stroke-width="{r.uniform(.5, 1.4):.1f}" fill="none" opacity=".4"/>')
    VX, VY = 270, 430
    for xb in range(-600, 1141, 70):
        o.append(f'<path d="M{fx(VX + (xb - VX) * (H - VY) / (960 - VY))},{H} L{xb},960" stroke="{S.CRM_D}" stroke-width="1.1" opacity=".35"/>')
    for yy in (668, 706, 760, 836, 940):
        o.append(f'<path d="M0,{yy} H540" stroke="{S.CRM_D}" stroke-width="1.1" opacity=".3"/>')
    for x0, x1 in ((178, 362), (0, 112), (428, 540)):
        o.append(f'<path d="M{x0},{H} L{x1},{H} L{x1 + (x1 - 270) * .5},960 L{x0 + (x0 - 270) * .5},960Z" fill="url(#reflDusk)" opacity=".5"/>')
    # ลายพื้นกลาง: แหวนสองวงคล้องกัน ล้อมด้วยวงลาย
    mc = (270, 800)
    o.append(f'<ellipse cx="270" cy="800" rx="232" ry="72" fill="none" stroke="{SV_D}" stroke-width="4" opacity=".75"/>')
    o.append(f'<ellipse cx="270" cy="800" rx="218" ry="67" fill="none" stroke="{SV}" stroke-width="1.4" opacity=".8"/>')
    for i in range(24):
        a = 2 * math.pi * i / 24
        o.append(f'<circle cx="{fx(270 + math.cos(a) * 196)}" cy="{fx(800 + math.sin(a) * 60)}" r="2.6" fill="{SV_D}" opacity=".7"/>')
    for i in range(12):
        a = 2 * math.pi * i / 12
        o.append(f'<path d="M{fx(270 + math.cos(a) * 150)},{fx(800 + math.sin(a) * 46)} L{fx(270 + math.cos(a) * 182)},{fx(800 + math.sin(a) * 56)}" stroke="{SV_D}" stroke-width="1.6" opacity=".55"/>')
    for dx in (-30, 30):
        o.append(f'<ellipse cx="{270 + dx}" cy="800" rx="62" ry="20" fill="none" stroke="{SV_D}" stroke-width="5" opacity=".7"/>')
        o.append(f'<ellipse cx="{270 + dx}" cy="799" rx="62" ry="20" fill="none" stroke="{SV_L}" stroke-width="1.6" opacity=".8"/>')
    # แสงจันทร์จากหน้าต่างตกบนลายพื้น (เย็น)
    o.append(f'<path d="M210,340 L330,340 L430,860 L110,860Z" fill="url(#moonShaft)" opacity=".55" filter="url(#bl4)" style="mix-blend-mode:screen"/>')
    o.append(f'<ellipse cx="270" cy="800" rx="150" ry="40" fill="#f4e6f2" opacity=".22" filter="url(#bl4)"/>')
    # แท่นดอกไม้
    for x in (196, 344):
        o.append(f'<ellipse cx="{x + 10}" cy="{H + 6}" rx="34" ry="6" fill="#3a3540" opacity=".3" filter="url(#sf4)"/>')
        o.append(poly([(x - 18, H + 4), (x + 18, H + 4), (x + 12, H - 60), (x + 22, H - 70), (x - 22, H - 70), (x - 12, H - 60)], S.CRM_L))
        o.append(poly([(x + 2, H + 4), (x + 18, H + 4), (x + 12, H - 60), (x + 22, H - 70), (x + 2, H - 70)], S.CRM_D))
        o.append(rect(x - 24, H - 76, 48, 7, SV)); o.append(rect(x - 24, H - 76, 48, 2.4, SV_L))
        o.append(S.bouquetB(x, H - 104, 44, 34, 30 + x, 1.0, 34, 9, red=0))
    # เชิงเทียนตั้งพื้น
    o.append(S.floor_candelabra(92, H + 18, 210, 1.1))
    o.append(S.floor_candelabra(448, H + 18, 210, 1.1))
    # เก้าอี้แขกว่างเปล่าสองแถว
    c = Cam(270, 430, 160, 600)
    for z in ():
        for sgn in (-1, 1):
            X = 132
            while True:
                x, _ = c.p(sgn * X, 0, z)
                if x < -40 or x > 580: break
                o.append(T.chair(c, sgn * X, z)); X += 58
    # เทียนแท่งหลายขนาดรอบลายพื้น
    o.append(pillar_candles(118, 760, 3, 1.0))
    o.append(pillar_candles(422, 762, 4, 1.0))
    # กลีบดอกที่ร่วงและกุหลาบหนึ่งดอกบนพื้น
    rr = random.Random(9)
    for i in range(40):
        x = rr.gauss(270, 120); y = rr.uniform(740, 900)
        col = rr.choice(('#fbf8f2', '#f6efe4', '#efe4d6', '#ffffff'))
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(rr.uniform(3, 5))}" ry="{fx(rr.uniform(1.4, 2.4))}" transform="rotate({rr.uniform(-50, 50):.0f} {fx(x)} {fx(y)})" fill="{col}" opacity=".9"/>')
    o.append(f'<path d="M300,862 q20,-4 40,6" stroke="#4a6a44" stroke-width="2.4" fill="none"/>')
    o.append(T.rose(296, 862, 7.5, '#f4efe6', '#ffffff', '#c9bfb2', 20))
    # หมอกจาง ๆ เลียดพื้น
    o.append(fog(5, 650, 800, 18, .4))
    o.append(CAST_BACK)
    # ม่านงาช้าง
    o.append(S.drape(-1, -40, 120, 12, 600, -40, 40, n=5))
    o.append(S.drape(1, 420, 580, 528, 600, 500, 580, n=5))
    o.append(f'<path d="M-20,-10 H560 V40 Q405,96 270,62 Q135,96 -20,40Z" fill="{S.RED}"/>')
    o.append(f'<path d="M-20,30 Q135,86 270,52 Q405,86 560,30 V40 Q405,96 270,62 Q135,96 -20,40Z" fill="{S.RED_D}"/>')
    o.append(f'<path d="M-20,-10 H560 V8 Q405,60 270,30 Q135,60 -20,8Z" fill="{S.RED_L}" opacity=".7"/>')
    # ผ้าโปร่งห้อยจากเพดานสองข้าง
    for x, d in ((60, 1), (480, -1)):
        o.append(f'<path d="M{x - 30},40 Q{x + d * 20},300 {x - d * 10},640 L{x + d * 30},640 Q{x + d * 40},300 {x + 30},40Z" fill="#fbf8f2" opacity=".22"/>')
    # โคมระย้าเงิน
    o.append(f'<circle cx="270" cy="70" r="120" fill="url(#chGlow4)"/>')
    o.append(S.chandelier_arms(270, -96, .7))
    # สายคริสตัลห้อยจากโคม
    rc = random.Random(2)
    for i in range(22):
        x = 270 + rc.uniform(-100, 100); y0 = 66 + rc.uniform(-6, 12); L = rc.uniform(14, 30)
        o.append(f'<path d="M{fx(x)},{fx(y0)} V{fx(y0 + L)}" stroke="#f4f6fa" stroke-width=".8" opacity=".7" stroke-dasharray="2 1.4"/><path d="M{fx(x)},{fx(y0 + L)} l2.2,3.4 l-2.2,4.2 l-2.2,-4.2Z" fill="#f6f8fc"/>')
    o.append(S.motes(5, (120, 240, 420, 760), 24))
    # ขอบภาพเย็นและมืดลง ให้ขลัง
    o.append(rect(0, 0, 540, 960, 'url(#eerie7)', 'style="mix-blend-mode:multiply"'))
    o.append(CAST_FRONT)
    o.append(f'<g filter="url(#dof4)">{S.bouquetB(10, 930, 80, 60, 91, 2.3, 24, 4, red=0)}{S.bouquetB(530, 940, 80, 60, 92, 2.3, 24, 4, red=0)}</g>')
    return ''.join(o)

DEFS_EXTRA = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="wall7" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d6ccbb"/><stop offset=".45" stop-color="#f3ede2"/><stop offset="1" stop-color="#e8dfd0"/></linearGradient>
<linearGradient id="floor7" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f1ede7"/><stop offset=".5" stop-color="#e4ded5"/><stop offset="1" stop-color="#cdc5ba"/></linearGradient>
<linearGradient id="moonShaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3e2f2" stop-opacity=".6"/><stop offset="1" stop-color="#f3e2f2" stop-opacity="0"/></linearGradient>
<linearGradient id="reflDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9a6d6" stop-opacity=".5"/><stop offset="1" stop-color="#c9a6d6" stop-opacity="0"/></linearGradient><radialGradient id="clockShade" cx=".35" cy=".3" r=".8"><stop offset=".6" stop-color="#ffffff" stop-opacity="0"/><stop offset="1" stop-color="#8a8494" stop-opacity=".35"/></radialGradient>
<radialGradient id="eerie7" cx=".5" cy=".5" r=".75"><stop offset=".45" stop-color="#ffffff"/><stop offset=".8" stop-color="#b9bccb"/><stop offset="1" stop-color="#6e6c80"/></radialGradient>
<linearGradient id="drapeShadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{V['RED_DD']}" stop-opacity=".6"/><stop offset="1" stop-color="{V['RED_DD']}" stop-opacity="0"/></linearGradient>
<linearGradient id="drapeShadeR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{V['RED_DD']}" stop-opacity=".6"/><stop offset="1" stop-color="{V['RED_DD']}" stop-opacity="0"/></linearGradient>
<linearGradient id="glass4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8b84c9"/><stop offset=".55" stop-color="#c9a6d6"/><stop offset="1" stop-color="#f4c4cf"/></linearGradient><filter id="blur7" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.1"/></filter>
<radialGradient id="vig4" cx=".5" cy=".45" r=".8"><stop offset=".55" stop-color="#2a2833" stop-opacity="0"/><stop offset="1" stop-color="#2a2833" stop-opacity=".5"/></radialGradient>
</defs></svg>'''

def build():
    # ลบ gradient เดิมที่ id ชนกัน แล้วใช้ชุดใหม่
    import re
    base = S.DEFS
    for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
        base = re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=re.S)
    svg = S.frame(scene(), 'ห้องพิธีแต่งงานโทนงาช้างกับเงิน นาฬิกาเงินในโค้งหน้าต่างหยุดใกล้เที่ยงคืน ภาพเจ้าสาวในกรอบวงรีบนเสา เทียนแท่ง กลีบดอกร่วง หมอกเลียดพื้น วิวเมืองยามสนธยาสีม่วงชมพูนอกหน้าต่าง')
    css = S.CSS.replace('<title>ฉากงานแต่งโทนอบอุ่น</title>', '<title>ห้องพิธีพร้อมตัวละคร</title>').replace('repeat(auto-fit,minmax(260px,1fr))', 'minmax(0,480px)').replace('.grid{display:grid;', '.grid{display:grid;justify-content:center;')
    notes = ''.join(f'<li>{t}</li>' for t in [
        'นาฬิกาเงินในโค้งหน้าต่างกลาง เข็มหยุดที่ 11:59 เป็นลางเรื่องเวลาที่วนซ้ำ',
        'ภาพเจ้าสาวในกรอบวงรีเงินบนหัวเสาสองข้าง หน้าจมอยู่ในเงา เห็นแค่ผ้าคลุม',
        'เทียนแท่งหลายขนาดรอบลายพื้น มีน้ำตาเทียนไหล',
        'ลายกลางพื้นเป็นแหวนสองวงคล้องกัน แสงสนธยาจากหน้าต่างตกลงตรงจุดนั้น',
        'กลีบดอกร่วงบนพื้น มีกลีบแดงเข้มปนนิดหน่อย กับกุหลาบแดงหนึ่งดอก',
        'หมอกจางเลียดพื้น ขอบภาพเย็นและมืดลง ตรงกลางยังสว่างและหรู',
    ])
    page = css + base + DEFS_EXTRA + WC.DEFS + B2.DEFS + SP.DEFS + f'''<div class="wrap" id="wrap"><header><h1>ห้องพิธี · ใส่ตัวละคร<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ทดลองวางตัวละครทุกคนในฉาก</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid"><figure>{svg}<figcaption><b>สิ่งที่เพิ่ม</b><small><ul style="margin:6px 0 0;padding-left:18px;display:flex;flex-direction:column;gap:4px">{notes}</ul></small></figcaption></figure></div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets8.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
