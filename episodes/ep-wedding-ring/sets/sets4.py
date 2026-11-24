# Odd Hours · ตอนงานแต่ง · รอบ 4: สว่าง อบอุ่น เป็นธรรมชาติ แต่ยังน่าค้นหา
# อิงหลักการจัดองค์ประกอบจาก ref-tone-7/8 (สมมาตร หน้าต่างสูง ม่านกรอบภาพ โคมกลางบน บันไดพรมแดง)
# และความนุ่มของแสงจาก ref-tone-9/10 โดยออกแบบใหม่เป็นโรงแรมของเราเอง
# รัน: python3 sets4.py -> sets4.html
import math, random
from sets import fx, P
from sets3 import rose, leaf

# ---------------------------------------------------------------- palette (อุ่น สว่าง)
CRM = '#f7e2c0'; CRM_L = '#fff3dc'; CRM_M = '#ecc99c'; CRM_D = '#cf9c6e'; CRM_DD = '#a8714c'
GLD = '#efbe68'; GLD_L = '#fff0bf'; GLD_D = '#b8803e'
RED = '#b8383a'; RED_L = '#dd5a4e'; RED_D = '#7c1f28'; RED_DD = '#5a141e'
BLU = '#3c5fae'; BLU_L = '#6f96d8'; BLU_D = '#253f84'
WD = '#9a5a3a'; WD_L = '#c4805a'; WD_D = '#6a3824'
FLAME = '#fff4cf'

def poly(pts, fill, extra=''):
    return f'<path d="{P(pts)}" fill="{fill}" {extra}/>'
def rect(x, y, w, h, fill, extra=''):
    return f'<rect x="{fx(x)}" y="{fx(y)}" width="{fx(w)}" height="{fx(h)}" fill="{fill}" {extra}/>'

ROSES_B = [('#fff6e6', '#ffffff', '#e2c4a4'), ('#f8d4c8', '#ffe8de', '#d9a294'), ('#fde9d2', '#fffaf0', '#e0bc98'), ('#d9605e', '#f08070', '#9a3436')]
LEAVES_B = (('#6f9a5e', '#9cc27a', '#4a7244'), ('#7faa68', '#acd08a', '#557e4a'))
def leafB(x, y, L, ang, pal): return leaf(x, y, L, ang, pal)
def bouquetB(cx, cy, rx, ry, seed, s=1.0, n=26, trail=4, red=.12):
    r = random.Random(seed); o = []
    for i in range(int(n * 1.1)):
        a = r.uniform(0, 2 * math.pi)
        x = cx + math.cos(a) * rx * r.uniform(.75, 1.05); y = cy + math.sin(a) * ry * r.uniform(.75, 1.05)
        o.append(leafB(x, y, r.uniform(9, 15) * s, math.degrees(a) + r.uniform(-25, 25), r.choice(LEAVES_B)))
    for i in range(trail):
        x = cx + r.uniform(-rx, rx) * .7; y = cy + ry * .6
        for j in range(5):
            o.append(leafB(x + r.uniform(-4, 4) * s, y + j * 9 * s, r.uniform(7, 11) * s, 90 + r.uniform(-50, 50), r.choice(LEAVES_B)))
    fl = []
    for i in range(n):
        a = r.uniform(0, 2 * math.pi); d = math.sqrt(r.random())
        pal = ROSES_B[3] if r.random() < red else r.choice(ROSES_B[:3])
        fl.append((cy + math.sin(a) * ry * d, cx + math.cos(a) * rx * d, r.uniform(5.5, 8.5) * s, pal, r.uniform(-40, 40)))
    fl.sort()
    o += [rose(x, y, rr, *pal, rot=rot) for y, x, rr, pal, rot in fl]
    for i in range(int(n * .8)):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(.6, 1.1)
        o.append(f'<circle cx="{fx(cx + math.cos(a) * rx * d)}" cy="{fx(cy + math.sin(a) * ry * d)}" r="{fx(1.4 * s)}" fill="#ffffff"/>')
    return ''.join(o)

def flame(x, y, s=1):
    return (f'<circle cx="{fx(x)}" cy="{fx(y - 3 * s)}" r="{fx(16 * s)}" fill="url(#flameGlow)"/>'
            f'<path d="M{fx(x)},{fx(y - 9 * s)} q{fx(3.2 * s)},{fx(5 * s)} 0,{fx(8.5 * s)} q{fx(-3.2 * s)},{fx(-3.5 * s)} 0,{fx(-8.5 * s)}Z" fill="{FLAME}"/>')
def candle(x, y, s=1, h=22):
    return (rect(x - 2.6 * s, y - h * s, 5.2 * s, h * s, '#fffaf0') + rect(x + .4 * s, y - h * s, 2.2 * s, h * s, '#ead6bc')
            + flame(x, y - h * s, s))

def arch(x0, x1, top, bot):
    r = (x1 - x0) / 2
    return f'M{fx(x0)},{fx(bot)} L{fx(x0)},{fx(top + r)} A{fx(r)},{fx(r)} 0 0,1 {fx(x1)},{fx(top + r)} L{fx(x1)},{fx(bot)}Z'

def chandelier_arms(cx, top, s, seed=1):
    """โคมระย้าทองแบบแขนโค้งถือเทียน"""
    o = [rect(cx - 2 * s, top, 4 * s, 120 * s, GLD_D)]
    stem = [(120, 10, 14), (165, 14, 10), (200, 9, 18), (240, 16, 12), (270, 36, 14)]
    for yy, rx, ry in stem:
        y = top + yy * s
        o.append(f'<ellipse cx="{fx(cx)}" cy="{fx(y)}" rx="{fx(rx * s)}" ry="{fx(ry * s)}" fill="{GLD}"/>')
        o.append(f'<path d="M{fx(cx - rx * s)},{fx(y)} A{fx(rx * s)},{fx(ry * s)} 0 0,1 {fx(cx - rx * s * .1)},{fx(y - ry * s)} A{fx(rx * s * .9)},{fx(ry * s)} 0 0,0 {fx(cx - rx * s)},{fx(y)}Z" fill="{GLD_L}"/>')
        o.append(f'<path d="M{fx(cx + rx * s)},{fx(y)} A{fx(rx * s)},{fx(ry * s)} 0 0,1 {fx(cx)},{fx(y + ry * s)} A{fx(rx * s * .8)},{fx(ry * s * .8)} 0 0,0 {fx(cx + rx * s)},{fx(y)}Z" fill="{GLD_D}"/>')
    o.insert(1, rect(cx - 3 * s, top + 120 * s, 6 * s, 160 * s, GLD))
    o.insert(2, rect(cx, top + 120 * s, 3 * s, 160 * s, GLD_D))
    tiers = [(180, 128, (34, 68, 102)), (270, 212, (46, 92, 138, 180))]
    for y0, cupy, xs in tiers:
        for side in (-1, 1):
            for dx in xs:
                ex = cx + side * dx * s; ey = top + cupy * s
                d = f'M{fx(cx)},{fx(top + y0 * s)} C{fx(cx + side * dx * s * .35)},{fx(top + (y0 + 40) * s)} {fx(ex)},{fx(top + (y0 + 40) * s)} {fx(ex)},{fx(ey + 8 * s)}'
                o.append(f'<path d="{d}" stroke="{GLD_D}" stroke-width="{fx(4.6 * s)}" fill="none"/>')
                o.append(f'<path d="{d}" stroke="{GLD}" stroke-width="{fx(3 * s)}" fill="none"/>')
                o.append(f'<path d="{d}" stroke="{GLD_L}" stroke-width="{fx(1 * s)}" fill="none" transform="translate({fx(-1 * s)},{fx(-1 * s)})"/>')
                o.append(f'<path d="M{fx(ex - 9 * s)},{fx(ey + 2 * s)} h{fx(18 * s)} l{fx(-4 * s)},{fx(7 * s)} h{fx(-10 * s)}Z" fill="{GLD}"/>')
                o.append(f'<path d="M{fx(ex)},{fx(ey + 2 * s)} h{fx(9 * s)} l{fx(-4 * s)},{fx(7 * s)} h{fx(-5 * s)}Z" fill="{GLD_D}"/>')
                o.append(candle(ex, ey + 2 * s, s, 26))
    o.append(f'<path d="M{fx(cx)},{fx(top + 284 * s)} l{fx(7 * s)},{fx(12 * s)} l{fx(-7 * s)},{fx(20 * s)} l{fx(-7 * s)},{fx(-20 * s)}Z" fill="{GLD}"/><path d="M{fx(cx)},{fx(top + 284 * s)} l{fx(7 * s)},{fx(12 * s)} l{fx(-7 * s)},{fx(20 * s)}Z" fill="{GLD_D}"/>')
    return ''.join(o)

def floor_candelabra(x, base, h, s=1):
    o = [f'<ellipse cx="{fx(x + 8)}" cy="{fx(base + 2)}" rx="{fx(26 * s)}" ry="{fx(5 * s)}" fill="#7a4a30" opacity=".3" filter="url(#sf4)"/>',
         poly([(x - 18 * s, base), (x + 18 * s, base), (x + 6 * s, base - 16 * s), (x - 6 * s, base - 16 * s)], GLD),
         poly([(x, base), (x + 18 * s, base), (x + 6 * s, base - 16 * s), (x, base - 16 * s)], GLD_D),
         rect(x - 3 * s, base - h, 6 * s, h - 14 * s, GLD), rect(x, base - h, 3 * s, h - 14 * s, GLD_D), rect(x - 3 * s, base - h, 1.4 * s, h - 14 * s, GLD_L)]
    for yy in (.35, .7):
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(base - h * yy)}" rx="{fx(7 * s)}" ry="{fx(5 * s)}" fill="{GLD}"/><path d="M{fx(x)},{fx(base - h * yy - 5 * s)} a{fx(7 * s)},{fx(5 * s)} 0 0,1 0,{fx(10 * s)}Z" fill="{GLD_D}"/>')
    for d in (-1, 1):
        o.append(f'<path d="M{fx(x)},{fx(base - h + 10 * s)} Q{fx(x + d * 26 * s)},{fx(base - h + 12 * s)} {fx(x + d * 28 * s)},{fx(base - h - 14 * s)}" stroke="{GLD}" stroke-width="{fx(3 * s)}" fill="none"/>')
        o.append(rect(x + d * 28 * s - 6 * s, base - h - 16 * s, 12 * s, 4 * s, GLD_L))
        o.append(candle(x + d * 28 * s, base - h - 16 * s, s, 30))
    o.append(rect(x - 6 * s, base - h - 4 * s, 12 * s, 4 * s, GLD_L))
    o.append(candle(x, base - h - 4 * s, s, 40))
    return ''.join(o)

def drape(side, x_top0, x_top1, tie_x, tie_y, bot_x0, bot_x1, ybot=990, n=6, top=-10):
    """ม่านกำมะหยี่แดง พับเป็นแถบ ไล่แสงเงาแบบนุ่มผสมตัดคม"""
    o = []
    tones = [RED, RED_L, RED, RED_D, RED, RED_DD]
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        a = x_top0 + (x_top1 - x_top0) * t0; b = x_top0 + (x_top1 - x_top0) * t1
        ta = tie_x + (t0 - .5) * 30; tb = tie_x + (t1 - .5) * 30
        ba = bot_x0 + (bot_x1 - bot_x0) * t0; bb = bot_x0 + (bot_x1 - bot_x0) * t1
        d = (f'M{fx(a)},{top} L{fx(b)},{top} C{fx(b)},{fx(tie_y * .45)} {fx(tb + side * 10)},{fx(tie_y * .8)} {fx(tb)},{fx(tie_y)} '
             f'C{fx(tb - side * 6)},{fx(tie_y + 80)} {fx(bb)},{fx(ybot - 140)} {fx(bb)},{fx(ybot)} L{fx(ba)},{fx(ybot)} '
             f'C{fx(ba)},{fx(ybot - 140)} {fx(ta - side * 6)},{fx(tie_y + 80)} {fx(ta)},{fx(tie_y)} C{fx(ta + side * 10)},{fx(tie_y * .8)} {fx(a)},{fx(tie_y * .45)} {fx(a)},{top}Z')
        o.append(f'<path d="{d}" fill="{tones[i % len(tones)]}"/>')
    o.append(f'<path d="M{fx(x_top0)},{top} L{fx(x_top1)},{top} L{fx(x_top1)},{fx(top + 600)} L{fx(x_top0)},{fx(top + 600)}Z" fill="url(#drapeShade{"L" if side < 0 else "R"})" opacity=".55" style="mix-blend-mode:multiply"/>')
    # สายรวบทอง
    o.append(f'<path d="M{fx(tie_x - 22)},{fx(tie_y - 4)} Q{fx(tie_x)},{fx(tie_y + 8)} {fx(tie_x + 22)},{fx(tie_y - 4)}" stroke="{GLD_D}" stroke-width="7" fill="none"/>')
    o.append(f'<path d="M{fx(tie_x - 22)},{fx(tie_y - 6)} Q{fx(tie_x)},{fx(tie_y + 6)} {fx(tie_x + 22)},{fx(tie_y - 6)}" stroke="{GLD}" stroke-width="4" fill="none"/>')
    tx = tie_x + side * 18
    o.append(f'<path d="M{fx(tx)},{fx(tie_y)} l-7,30 h14Z" fill="{GLD}"/><path d="M{fx(tx)},{fx(tie_y)} l0,30 h7Z" fill="{GLD_D}"/>')
    return ''.join(o)

def window(x0, x1, top, bot, seed):
    o = []
    o.append(f'<path d="{arch(x0 - 14, x1 + 14, top - 14, bot)}" fill="{CRM_M}"/>')
    o.append(f'<path d="{arch(x0 - 8, x1 + 8, top - 8, bot)}" fill="{CRM_L}"/>')
    o.append(f'<path d="{arch(x0 - 3, x1 + 3, top - 3, bot)}" fill="{GLD_D}"/>')
    cid = f'win{seed}'
    o.append(f'<clipPath id="{cid}"><path d="{arch(x0, x1, top, bot)}"/></clipPath><g clip-path="url(#{cid})">')
    o.append(rect(x0, top, x1 - x0, bot - top, 'url(#glass4)'))
    o.append(rect(x0, top, x1 - x0, bot - top, '#ffffff', 'filter="url(#mottle4)" opacity=".16" style="mix-blend-mode:screen"'))
    o.append(poly([(x0, bot), (x0 + (x1 - x0) * .5, top), (x0 + (x1 - x0) * .78, top), (x0 + (x1 - x0) * .25, bot)], '#cfe0ff', 'opacity=".10"'))
    w = x1 - x0; n = max(3, round(w / 26))
    for i in range(1, n):
        xx = x0 + w * i / n
        o.append(rect(xx - 1.6, top, 3.2, bot - top, GLD))
        o.append(rect(xx - 1.6, top, 1.1, bot - top, GLD_L))
    yy = top + (x1 - x0) / 2 + 30
    while yy < bot - 20:
        o.append(rect(x0, yy - 1.6, w, 3.2, GLD)); o.append(rect(x0, yy - 1.6, w, 1.1, GLD_L))
        yy += 68
    o.append('</g>')
    return ''.join(o)

def pilaster(x0, x1, top, bot):
    w = x1 - x0
    return ''.join([rect(x0, top, w, bot - top, CRM),
                    rect(x0, top, w * .22, bot - top, CRM_L),
                    rect(x1 - w * .26, top, w * .26, bot - top, CRM_D),
                    rect(x0 + w * .3, top + 40, w * .38, bot - top - 80, CRM_M),
                    rect(x0 + w * .3, top + 40, w * .1, bot - top - 80, CRM_L),
                    rect(x0 - 6, top - 26, w + 12, 26, GLD), rect(x0 - 6, top - 26, w + 12, 6, GLD_L), rect(x0 - 6, top - 6, w + 12, 6, GLD_D),
                    rect(x0 - 10, top - 36, w + 20, 10, CRM_L), rect(x0 - 10, top - 28, w + 20, 3, CRM_D),
                    rect(x0 - 6, bot - 30, w + 12, 30, CRM_M), rect(x0 - 6, bot - 30, w + 12, 5, CRM_L), rect(x1 - 4, bot - 30, 10, 30, CRM_D)])

def motes(seed, box_, n):
    r = random.Random(seed); x0, y0, x1, y1 = box_; o = []
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if r.random() < .4: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.4, 2.4):.1f}" fill="#fff4dc" opacity="{r.uniform(.25, .4):.2f}" filter="url(#mb4)"/>')
        else: o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6, 1.2):.1f}" fill="#fffaf0" opacity="{r.uniform(.6, .9):.2f}"/>')
    return ''.join(o)

# ================================================================ ฉาก 1: ห้องพิธีแต่งงาน
def scene_hall():
    o = []
    H = 640  # เส้นต่อผนังกับพื้น
    o.append(rect(0, 0, 540, H, 'url(#wall4)'))
    # เพดานโค้งด้านบน
    o.append(f'<path d="M0,0 H540 V70 Q270,10 0,70Z" fill="#e2b282"/>')
    o.append(f'<path d="M0,70 Q270,10 540,70" stroke="{GLD}" stroke-width="4" fill="none"/>')
    o.append(f'<path d="M0,78 Q270,18 540,78" stroke="{CRM_L}" stroke-width="2" fill="none"/>')
    # หน้าต่างโค้งสามบาน
    o.append(window(178, 362, 110, H - 8, 1))
    o.append(window(-60, 112, 178, H - 8, 2))
    o.append(window(428, 600, 178, H - 8, 3))
    # เสาระหว่างหน้าต่าง
    o.append(pilaster(122, 168, 236, H))
    o.append(pilaster(372, 418, 236, H))
    # วงกลมประดับเหนือเสา
    for x in (145, 395):
        o.append(f'<circle cx="{x}" cy="150" r="20" fill="{CRM_M}"/><circle cx="{x}" cy="150" r="14" fill="{CRM_L}"/><circle cx="{x}" cy="150" r="7" fill="{GLD}"/>')
    # บัวล่างผนัง
    o.append(rect(0, H - 22, 540, 22, CRM_M)); o.append(rect(0, H - 22, 540, 4, CRM_L)); o.append(rect(0, H - 4, 540, 4, CRM_DD))
    # พื้นหินอ่อนอุ่น
    o.append(rect(0, H, 540, 960 - H, 'url(#floor4)'))
    VX, VY = 270, 430
    for xb in range(-600, 1141, 70):
        o.append(f'<path d="M{fx(VX + (xb - VX) * (H - VY) / (960 - VY))},{H} L{xb},960" stroke="{CRM_D}" stroke-width="1.2" opacity=".35"/>')
    for yy in (668, 706, 760, 836, 940):
        o.append(f'<path d="M0,{yy} H540" stroke="{CRM_D}" stroke-width="1.2" opacity=".3"/>')
    # เงาสะท้อนหน้าต่างบนพื้น (ฟ้าเย็น)
    for x0, x1 in ((178, 362), (0, 112), (428, 540)):
        o.append(f'<path d="M{x0},{H} L{x1},{H} L{x1 + (x1 - 270) * .5},960 L{x0 + (x0 - 270) * .5},960Z" fill="url(#reflBlue)" opacity=".55"/>')
    # ลายวงกลมกลางพื้น (จุดยืนพิธี)
    mc, mr = (270, 800), (232, 72)
    o.append(f'<ellipse cx="{mc[0]}" cy="{mc[1]}" rx="{mr[0]}" ry="{mr[1]}" fill="none" stroke="{CRM_D}" stroke-width="5" opacity=".7"/>')
    o.append(f'<ellipse cx="{mc[0]}" cy="{mc[1]}" rx="{mr[0] - 14}" ry="{mr[1] - 5}" fill="none" stroke="{GLD_D}" stroke-width="1.6" opacity=".7"/>')
    o.append(f'<ellipse cx="{mc[0]}" cy="{mc[1]}" rx="160" ry="48" fill="#f5cfa2" opacity=".55"/>')
    for i in range(16):
        a = 2 * math.pi * i / 16
        x1_, y1_ = mc[0] + math.cos(a) * 160, mc[1] + math.sin(a) * 48
        x2_, y2_ = mc[0] + math.cos(a) * 214, mc[1] + math.sin(a) * 66
        o.append(f'<path d="M{fx(x1_)},{fx(y1_)} L{fx(x2_)},{fx(y2_)}" stroke="{CRM_D}" stroke-width="2" opacity=".55"/>')
        xm, ym = mc[0] + math.cos(a + .2) * 190, mc[1] + math.sin(a + .2) * 58
        o.append(f'<circle cx="{fx(xm)}" cy="{fx(ym)}" r="3" fill="{GLD_D}" opacity=".6"/>')
    o.append(f'<ellipse cx="{mc[0]}" cy="{mc[1]}" rx="84" ry="25" fill="none" stroke="{GLD_D}" stroke-width="2.4" opacity=".6"/>')
    o.append(f'<ellipse cx="{mc[0]}" cy="{mc[1] - 4}" rx="160" ry="40" fill="#fff4dc" opacity=".35" filter="url(#bl4)"/>')
    # แท่นดอกไม้สองข้างหน้าต่างกลาง
    for x in (196, 344):
        o.append(f'<ellipse cx="{x + 10}" cy="{H + 6}" rx="34" ry="6" fill="#8a5434" opacity=".3" filter="url(#sf4)"/>')
        o.append(poly([(x - 18, H + 4), (x + 18, H + 4), (x + 12, H - 60), (x + 22, H - 70), (x - 22, H - 70), (x - 12, H - 60)], CRM_L))
        o.append(poly([(x + 2, H + 4), (x + 18, H + 4), (x + 12, H - 60), (x + 22, H - 70), (x + 2, H - 70)], CRM_D))
        o.append(rect(x - 24, H - 76, 48, 7, GLD)); o.append(rect(x - 24, H - 76, 48, 2.4, GLD_L))
        o.append(bouquetB(x, H - 104, 44, 34, 30 + x, 1.0, 34, 6))
    # เชิงเทียนตั้งพื้น
    o.append(floor_candelabra(92, H + 18, 210, 1.1))
    o.append(floor_candelabra(448, H + 18, 210, 1.1))
    # ม่านแดง
    o.append(drape(-1, -40, 120, 12, 600, -40, 40, n=5))
    o.append(drape(1, 420, 580, 528, 600, 500, 580, n=5))
    # ระบายบนสุดเชื่อมม่าน
    o.append(f'<path d="M-20,-10 H560 V40 Q405,96 270,62 Q135,96 -20,40Z" fill="{RED}"/>')
    o.append(f'<path d="M-20,30 Q135,86 270,52 Q405,86 560,30 V40 Q405,96 270,62 Q135,96 -20,40Z" fill="{RED_D}"/>')
    o.append(f'<path d="M-20,-10 H560 V8 Q405,60 270,30 Q135,60 -20,8Z" fill="{RED_L}" opacity=".7"/>')
    # โคมระย้า
    o.append(f'<circle cx="270" cy="190" r="140" fill="url(#chGlow4)"/>')
    o.append(chandelier_arms(270, -24, .8))
    # แสงอุ่นจากโคมกับฟ้าเย็นจากหน้าต่าง
    o.append(f'<path d="M190,250 L350,250 L470,900 L70,900Z" fill="url(#shaft4)" opacity=".5" filter="url(#bl4)" style="mix-blend-mode:screen"/>')
    o.append(motes(5, (120, 220, 420, 760), 30))
    # ฉากหน้าเบลอ
    o.append(f'<g filter="url(#dof4)">{bouquetB(10, 930, 80, 60, 91, 2.3, 24, 4)}{bouquetB(530, 940, 80, 60, 92, 2.3, 24, 4)}</g>')
    return ''.join(o)

# ================================================================ ฉาก 2: โถงบันไดใหญ่หน้าห้องจัดเลี้ยง
def baluster(x, ybot, ytop, s=1):
    h = ybot - ytop; w = 7 * s
    return ''.join([rect(x - w / 2, ytop, w, h, WD_L),
                    rect(x, ytop, w / 2, h, WD),
                    f'<ellipse cx="{fx(x)}" cy="{fx(ytop + h * .62)}" rx="{fx(w * .9)}" ry="{fx(h * .14)}" fill="{WD_L}"/>',
                    f'<path d="M{fx(x)},{fx(ytop + h * .48)} a{fx(w * .9)},{fx(h * .14)} 0 0,1 0,{fx(h * .28)}Z" fill="{WD}"/>',
                    rect(x - w * .7, ybot - 6 * s, w * 1.4, 6 * s, WD_D)])

def scene_stair():
    o = []
    LAND = 352
    # ผนังชั้นบน
    o.append(rect(0, 0, 540, LAND, 'url(#wall4b)'))
    o.append(f'<path d="M0,0 H540 V50 Q270,0 0,50Z" fill="#e3b88c"/><path d="M0,50 Q270,0 540,50" stroke="{GLD}" stroke-width="4" fill="none"/>')
    # ประตูบานคู่ชั้นบน (ทางเข้าห้องจัดเลี้ยง)
    dx0, dx1, dt = 196, 344, 130
    o.append(f'<path d="{arch(dx0 - 22, dx1 + 22, dt - 72, LAND)}" fill="{CRM_M}"/>')
    o.append(f'<path d="{arch(dx0 - 14, dx1 + 14, dt - 64, LAND)}" fill="{CRM_L}"/>')
    o.append(f'<path d="{arch(dx0 - 4, dx1 + 4, dt - 54, LAND)}" fill="{GLD_D}"/>')
    o.append(f'<path d="{arch(dx0, dx1, dt - 50, dt + 24)}" fill="#ffe9c4"/>')
    for i in range(7):
        a = math.pi * (i + 1) / 8
        o.append(f'<path d="M270,{dt + 24} L{fx(270 - math.cos(a) * 80)},{fx(dt + 24 - math.sin(a) * 80)}" stroke="{GLD}" stroke-width="2.4"/>')
    o.append(rect(dx0, dt + 20, dx1 - dx0, 6, GLD))
    dw = (dx1 - dx0) / 2
    for i, (lx, base, sh) in enumerate(((dx0, '#fbecd2', '#e9cfac'), (dx0 + dw, '#f3dfc0', '#ddbf98'))):
        o.append(rect(lx + 1, dt + 26, dw - 2, LAND - dt - 26, base))
        for (py0, py1) in ((dt + 38, dt + 120), (dt + 132, LAND - 14)):
            o.append(rect(lx + 10, py0, dw - 20, py1 - py0, sh))
            o.append(rect(lx + 12, py0 + 2, dw - 24, py1 - py0 - 4, base, f'stroke="{GLD}" stroke-width="1.4"'))
        hx = lx + dw - 9 if i == 0 else lx + 7
        o.append(rect(hx - 1, dt + 120, 4, 34, GLD_D)); o.append(rect(hx - 1, dt + 120, 2, 34, GLD_L))
    o.append(rect(269, dt + 26, 2, LAND - dt - 26, '#fff4dc'))
    # ช่องโค้งผนังพร้อมไฟผนังชั้นบน
    def niche_sconce(x, top, bot, w):
        s_ = [f'<path d="{arch(x - w / 2, x + w / 2, top, bot)}" fill="{CRM_M}"/>',
              f'<path d="{arch(x - w / 2 + 6, x + w / 2 - 6, top + 6, bot)}" fill="#e8bf90"/>',
              f'<path d="{arch(x - w / 2 + 6, x - w / 2 + 16, top + 30, bot)}" fill="#f3d3a8"/>',
              f'<ellipse cx="{x}" cy="{fx(top + (bot - top) * .42)}" rx="{fx(w * .55)}" ry="{fx(w * .6)}" fill="url(#chGlow4)"/>']
        yy = top + (bot - top) * .48
        s_.append(rect(x - 4, yy - 6, 8, 34, GLD)); s_.append(rect(x, yy - 6, 4, 34, GLD_D))
        for d in (-1, 0, 1):
            ex = x + d * 18; ey = yy - 6 - (10 if d == 0 else 0)
            if d: s_.append(f'<path d="M{x},{fx(yy + 16)} Q{fx(ex)},{fx(yy + 18)} {fx(ex)},{fx(ey + 4)}" stroke="{GLD}" stroke-width="3" fill="none"/>')
            s_.append(rect(ex - 6, ey, 12, 4, GLD_L)); s_.append(candle(ex, ey, 1, 20))
        return ''.join(s_)
    o.append(niche_sconce(70, 90, 300, 96))
    o.append(niche_sconce(470, 90, 300, 96))
    # พื้นชั้นบนและราวระเบียง
    o.append(rect(0, LAND - 6, 540, 6, CRM_DD))
    o.append(rect(0, LAND, 540, 26, WD)); o.append(rect(0, LAND, 540, 6, WD_L)); o.append(rect(0, LAND + 22, 540, 4, WD_D))
    for side, (a, b) in ((-1, (0, 196)), (1, (344, 540))):
        x = a + 10
        while x < b - 6:
            o.append(baluster(x, LAND, LAND - 64, .9)); x += 17
        o.append(rect(a, LAND - 74, b - a, 12, WD_L)); o.append(rect(a, LAND - 66, b - a, 4, WD)); o.append(rect(a, LAND - 74, b - a, 3, '#e0a07a'))
    # ผนังชั้นล่างสองข้างบันได
    o.append(rect(0, LAND + 26, 540, 960 - LAND - 26, 'url(#wall4c)'))
    o.append(niche_sconce(54, 470, 720, 84))
    o.append(niche_sconce(486, 470, 720, 84))
    # บันได (กว้างขึ้นเมื่อลงมา)
    N = 15; ytop, ybot = LAND + 26, 900
    hw0, hw1 = 84, 176
    steps = []
    for k in range(N):
        t0, t1 = k / N, (k + 1) / N
        y0 = ytop + (ybot - ytop) * t0; y1 = ytop + (ybot - ytop) * t1
        w0 = hw0 + (hw1 - hw0) * t0; w1 = hw0 + (hw1 - hw0) * t1
        steps.append((y0, y1, w0, w1))
        tread = y0 + (y1 - y0) * .32
        o.append(poly([(270 - w0, y0), (270 + w0, y0), (270 + w1, tread), (270 - w1, tread)], '#f6dcb6'))
        o.append(poly([(270 - w1, tread), (270 + w1, tread), (270 + w1, y1), (270 - w1, y1)], '#dcae80'))
        o.append(rect(270 - w1, tread - 1, 2 * w1, 2, CRM_L))
        rw0, rw1 = w0 * .56, w1 * .56
        o.append(poly([(270 - rw0, y0), (270 + rw0, y0), (270 + rw1, tread), (270 - rw1, tread)], RED_L))
        o.append(poly([(270 - rw1, tread), (270 + rw1, tread), (270 + rw1, y1), (270 - rw1, y1)], RED))
        o.append(poly([(270 + rw1 * .5, tread), (270 + rw1, tread), (270 + rw1, y1), (270 + rw1 * .5, y1)], RED_D, 'opacity=".55"'))
        o.append(rect(270 - rw1 - 3, y1 - 3, 2 * rw1 + 6, 3, GLD))
        o.append(rect(270 - rw1 - 3, y1 - 3, 2 * rw1 + 6, 1, GLD_L))
    o.append(poly([(270 + hw0 * .1, ytop), (270 + hw0 + 6, ytop), (270 + hw1 + 6, ybot), (270 + hw1 * .35, ybot)], '#7a3a24', 'opacity=".16"'))
    # ราวบันไดสองข้าง
    for side in (-1, 1):
        rail = []
        for (y0, y1, w0, w1) in steps:
            x = 270 + side * (w1 + 6)
            o.append(baluster(x, y1 - (y1 - y0) * .6, y1 - (y1 - y0) * .6 - 70, 1 + (y1 - ytop) / 900))
            rail.append((x, y1 - (y1 - y0) * .6 - 74))
        xs, ys = rail[0]; xe, ye = rail[-1]
        nx = 270 + side * (hw1 + 40)
        d = f'M{fx(270 + side * (hw0 + 6))},{fx(ytop - 74)} L{fx(xe)},{fx(ye)} Q{fx(xe + side * 12)},{fx(ye + 6)} {fx(nx)},{fx(ye + 6)}'
        o.append(f'<path d="{d}" stroke="{WD_D}" stroke-width="16" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="{d}" stroke="{WD_L}" stroke-width="11" fill="none" stroke-linecap="round"/>')
        o.append(f'<path d="{d}" stroke="#e8aa80" stroke-width="3" fill="none" transform="translate(0,-3)" stroke-linecap="round"/>')
        # เสาหัวบันไดพร้อมแจกันดอกไม้
        o.append(rect(nx - 15, ye + 4, 30, 960 - ye, WD)); o.append(rect(nx - 15, ye + 4, 10, 960 - ye, WD_L)); o.append(rect(nx + 6, ye + 4, 9, 960 - ye, WD_D))
        o.append(rect(nx - 20, ye - 4, 40, 12, WD_L)); o.append(rect(nx - 20, ye + 4, 40, 4, WD_D))
        o.append(bouquetB(nx, ye - 26, 34, 26, 70 + side, .95, 26, 5))
    # พื้นโถงล่าง
    o.append(rect(0, 900, 540, 60, '#e8b888')); o.append(rect(0, 900, 540, 4, CRM_DD))
    o.append(f'<ellipse cx="270" cy="930" rx="230" ry="26" fill="#fff0d0" opacity=".35" filter="url(#bl4)"/>')
    # ม่านแดงกรอบภาพ + ระบายบน
    o.append(drape(-1, -40, 70, -4, 520, -40, 14, n=4))
    o.append(drape(1, 470, 580, 544, 520, 526, 580, n=4))
    o.append(f'<path d="M-20,-10 H560 V30 Q405,80 270,46 Q135,80 -20,30Z" fill="{RED}"/><path d="M-20,22 Q135,72 270,38 Q405,72 560,22 V30 Q405,80 270,46 Q135,80 -20,30Z" fill="{RED_D}"/>')
    # โคมระย้าเหนือบันได
    o.append(f'<circle cx="270" cy="80" r="100" fill="url(#chGlow4)"/>')
    o.append(chandelier_arms(270, -110, .5))
    o.append(f'<path d="M200,170 L340,170 L420,880 L120,880Z" fill="url(#shaft4)" opacity=".4" filter="url(#bl4)" style="mix-blend-mode:screen"/>')
    o.append(motes(8, (130, 160, 410, 700), 26))
    o.append(f'<g filter="url(#dof4)">{bouquetB(20, 940, 70, 50, 93, 2.1, 20, 3)}{bouquetB(520, 945, 70, 50, 94, 2.1, 20, 3)}</g>')
    return ''.join(o)

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stip4" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="paint4" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency=".02 .06" numOctaves="3" seed="6"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="mottle4" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".05" numOctaves="3" seed="11"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="dof4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4.5"/></filter>
<filter id="bl4" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="sf4" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="mb4" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<linearGradient id="wall4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#eebf8e"/><stop offset=".45" stop-color="#f7dcb6"/><stop offset="1" stop-color="#f1cc9e"/></linearGradient>
<linearGradient id="wall4b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#efc796"/><stop offset="1" stop-color="#f8e2c0"/></linearGradient>
<linearGradient id="wall4c" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ecc898"/><stop offset="1" stop-color="#e2b183"/></linearGradient>
<linearGradient id="floor4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f5d2a6"/><stop offset=".5" stop-color="#efbf8e"/><stop offset="1" stop-color="#e2a676"/></linearGradient>
<linearGradient id="glass4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22397c"/><stop offset=".55" stop-color="#3c5fae"/><stop offset="1" stop-color="#6c90d4"/></linearGradient>
<linearGradient id="reflBlue" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f9fdc" stop-opacity=".55"/><stop offset="1" stop-color="#7f9fdc" stop-opacity="0"/></linearGradient>
<linearGradient id="shaft4" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2d6" stop-opacity=".6"/><stop offset="1" stop-color="#fff2d6" stop-opacity="0"/></linearGradient>
<linearGradient id="drapeShadeL" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a141e" stop-opacity=".6"/><stop offset="1" stop-color="#5a141e" stop-opacity="0"/></linearGradient>
<linearGradient id="drapeShadeR" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="#5a141e" stop-opacity=".6"/><stop offset="1" stop-color="#5a141e" stop-opacity="0"/></linearGradient>
<radialGradient id="chGlow4"><stop offset="0" stop-color="#fff6dc" stop-opacity=".75"/><stop offset=".5" stop-color="#ffe6bc" stop-opacity=".25"/><stop offset="1" stop-color="#ffe6bc" stop-opacity="0"/></radialGradient>
<radialGradient id="flameGlow"><stop offset="0" stop-color="#fff2c8" stop-opacity=".7"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></radialGradient>
<radialGradient id="vig4" cx=".5" cy=".45" r=".8"><stop offset=".6" stop-color="#6a3020" stop-opacity="0"/><stop offset="1" stop-color="#5a2418" stop-opacity=".35"/></radialGradient>
</defs></svg>'''

def frame(content, label):
    tex = ('<rect width="540" height="960" filter="url(#paint4)" opacity=".08" style="mix-blend-mode:overlay"/>'
           '<rect width="540" height="960" filter="url(#stip4)" opacity=".13" style="mix-blend-mode:overlay"/>'
           '<rect width="540" height="960" fill="url(#vig4)"/>')
    return (f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">{content}{tex}'
            '<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".8" stroke-dasharray="6 5" stroke-width="1.5"/>'
            '<text x="270" y="652" text-anchor="middle" font-size="13" fill="#fff" font-family="IBM Plex Sans Thai, sans-serif">พื้นที่ซับ</text></g></svg>')

CSS = '''<title>ฉากงานแต่งโทนอบอุ่น</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&display=swap">
<style>
/* Layout: two 9:16 frames side by side with captions, stacking on phones. Single warm-dark stage by choice. */
:root{--stage:#1a1210;--ink:#f3e6d6;--muted:#b9a08c;--line:#3a2a24;--accent:#efbe68;--font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;color-scheme:dark}
html,body{background:var(--stage);color:var(--ink)}
body{font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 40px}
.wrap{max-width:1000px;margin:0 auto;display:flex;flex-direction:column;gap:20px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:end;justify-content:space-between}
h1{margin:0;font-size:22px;font-weight:600;text-wrap:balance}
h1 span{display:block;font-size:13px;font-weight:400;color:var(--muted);margin-top:4px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
figure{margin:0;display:flex;flex-direction:column;gap:10px;min-width:0}
figure svg{display:block;width:100%;height:auto;aspect-ratio:9/16;border-radius:4px;box-shadow:0 0 0 1px var(--line),0 18px 44px rgba(0,0,0,.5)}
figcaption{display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:1.6}
figcaption b{font-weight:600;color:#fff}
figcaption small{color:var(--muted);font-size:12.5px}
button{font:inherit;font-size:13px;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:6px;padding:7px 12px;cursor:pointer}
button:hover{border-color:var(--muted)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button[aria-pressed="true"]{border-color:var(--accent);color:#fff}
.guide{display:none}.show-guide .guide{display:inline}
</style>'''

def build():
    figs = [
        ('ห้องพิธีแต่งงาน', 'ฉากหลักของเรื่อง หน้าต่างโค้งสูงเห็นฟ้ากลางคืน ม่านแดงกรอบภาพ โคมทองแขนโค้งถือเทียนอยู่กลางบน ลายวงกลมกลางพื้นเป็นจุดยืนของคู่บ่าวสาว', frame(scene_hall(), 'ห้องพิธีแต่งงานในโรงแรม โทนอบอุ่น หน้าต่างโค้งสูงสีน้ำเงินกลางคืน ม่านแดง โคมระย้าทองถือเทียน เชิงเทียนตั้งพื้น แท่นดอกกุหลาบ และพื้นหินอ่อนมีลายวงกลม')),
        ('โถงบันไดหน้าห้องจัดเลี้ยง', 'ประตูบานคู่อยู่บนชั้นลอยเหนือบันไดพรมแดง ใช้กับช็อตที่ประตูเปิดแล้วผู้หญิงชุดดำปรากฏตัวด้านบน ก่อนค่อย ๆ เดินลงมา', frame(scene_stair(), 'โถงบันไดใหญ่ในโรงแรม ประตูบานคู่สีครีมขอบทองบนชั้นลอย บันไดพรมแดงพร้อมราวไม้ ช่องโค้งผนังมีไฟเทียน ม่านแดง และโคมระย้าทอง')),
    ]
    cards = ''.join(f'<figure>{svg}<figcaption><b>{t}</b><small>{n}</small></figcaption></figure>' for t, n, svg in figs)
    page = CSS + DEFS + f'''<div class="wrap" id="wrap"><header><h1>ฉากงานแต่ง · โทนสว่างอบอุ่น<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ยังไม่ใส่ตัวละคร</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets4.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
