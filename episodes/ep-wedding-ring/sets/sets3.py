# Odd Hours · ตอนงานแต่ง · ทดลองโทนใหม่ (รอบ 3) เริ่มจากห้องจัดเลี้ยงฉากเดียว
# แนวภาพ: ref-tone-3..6 ผนังเข้ม แสงเทียนอำพัน แสงเงาเป็นก้อนสีขอบคม ไม่ใช้แสงฟุ้ง
# รัน: python3 sets3.py -> sets3.html
import math, random
from sets import Cam, P, path, back, side, flat, box, mix, fx, city, arch_d

# ---------------------------------------------------------------- palette
WALL = '#4a3b38'; WALL_D = '#3a2e2d'; WALL_L = '#6b5246'
PIL = '#574540'; PIL_L = '#8f6c55'; PIL_D = '#3a2c2a'
GOLD = '#b48a4e'; GOLD_L = '#e8c07a'; GOLD_D = '#6e4f2c'
WINE = '#6a1d2b'; WINE_L = '#9a3242'; WINE_D = '#43121c'
WOOD = '#4a3024'; WOOD_L = '#6e4836'; WOOD_D = '#2e1d16'
CREAM = '#ead8b8'; CREAM_L = '#fff0d2'; CREAM_D = '#a88e72'
AMBER = '#ffcf8a'
NIGHT = '#2a3352'
SHADOW = '#1c1316'

def poly(pts, fill, op=None):
    o = f' opacity="{op}"' if op is not None else ''
    return f'<path d="{P(pts)}" fill="{fill}"{o}/>'

# ---------------------------------------------------------------- props (ตัดแสงเงาเป็นก้อนสี)
def rose(x, y, r, base, lt, dk, rot=0):
    """กุหลาบแบบชิ้นส่วน: สีกลาง + ฝั่งรับแสงซ้ายบน + ฝั่งเงาขวาล่าง + กลีบวน"""
    o = [f'<g transform="rotate({rot:.0f} {fx(x)} {fx(y)})">',
         f'<circle cx="{fx(x)}" cy="{fx(y)}" r="{fx(r)}" fill="{base}"/>',
         f'<path d="M{fx(x - r)},{fx(y)} A{fx(r)},{fx(r)} 0 0,1 {fx(x + r * .2)},{fx(y - r * .98)} A{fx(r * 1.1)},{fx(r * 1.1)} 0 0,0 {fx(x - r)},{fx(y)}Z" fill="{lt}"/>'.replace('A' + fx(r * 1.1), 'A' + fx(r * .9)),
         f'<path d="M{fx(x + r)},{fx(y)} A{fx(r)},{fx(r)} 0 0,1 {fx(x - r * .3)},{fx(y + r * .95)} A{fx(r * .8)},{fx(r * .8)} 0 0,0 {fx(x + r)},{fx(y)}Z" fill="{dk}"/>',
         f'<path d="M{fx(x - r * .55)},{fx(y + r * .1)} A{fx(r * .55)},{fx(r * .5)} 0 1,1 {fx(x + r * .45)},{fx(y + r * .3)}" fill="none" stroke="{dk}" stroke-width="{fx(max(.6, r * .16))}"/>',
         f'<path d="M{fx(x - r * .2)},{fx(y + r * .05)} A{fx(r * .26)},{fx(r * .24)} 0 1,1 {fx(x + r * .18)},{fx(y + r * .14)}" fill="none" stroke="{dk}" stroke-width="{fx(max(.5, r * .13))}"/>',
         '</g>']
    return ''.join(o)

LEAVES = (('#3f5a3e', '#5f7d55', '#273a28'), ('#4a6447', '#6d8a60', '#2e4130'))
def leaf(x, y, L, ang, pal):
    base, lt, dk = pal
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    tip = (x + ca * L, y + sa * L); w = L * .34
    nx, ny = -sa * w, ca * w
    m1 = (x + ca * L * .45 + nx, y + sa * L * .45 + ny); m2 = (x + ca * L * .45 - nx, y + sa * L * .45 - ny)
    d1 = f'M{fx(x)},{fx(y)} Q{fx(m1[0])},{fx(m1[1])} {fx(tip[0])},{fx(tip[1])}Z'
    d2 = f'M{fx(x)},{fx(y)} Q{fx(m2[0])},{fx(m2[1])} {fx(tip[0])},{fx(tip[1])}Z'
    return f'<path d="{d1}" fill="{lt if ny < 0 else dk}"/><path d="{d2}" fill="{dk if ny < 0 else lt}"/>'

ROSES = [(CREAM, CREAM_L, '#b89a7c'), ('#e9c3b8', '#fbe0d4', '#b48a82'), ('#f3e6d0', '#fffaf0', '#bca88e'), ('#b4485a', '#d86a78', '#6e2232')]
def bouquet(cx, cy, rx, ry, seed, s=1.0, n=26, trail=4, wine=.12):
    r = random.Random(seed); o = []
    for i in range(int(n * 1.1)):
        a = r.uniform(0, 2 * math.pi)
        x = cx + math.cos(a) * rx * r.uniform(.75, 1.05); y = cy + math.sin(a) * ry * r.uniform(.75, 1.05)
        o.append(leaf(x, y, r.uniform(9, 15) * s, math.degrees(a) + r.uniform(-25, 25), r.choice(LEAVES)))
    for i in range(trail):
        x = cx + r.uniform(-rx, rx) * .7; y = cy + ry * .6
        for j in range(5):
            o.append(leaf(x + r.uniform(-4, 4) * s, y + j * 9 * s, r.uniform(7, 11) * s, 90 + r.uniform(-50, 50), r.choice(LEAVES)))
    fl = []
    for i in range(n):
        a = r.uniform(0, 2 * math.pi); d = math.sqrt(r.random())
        pal = ROSES[3] if r.random() < wine else r.choice(ROSES[:3])
        fl.append((cy + math.sin(a) * ry * d, cx + math.cos(a) * rx * d, r.uniform(5.5, 8.5) * s, pal, r.uniform(-40, 40)))
    fl.sort()
    for y, x, rr, pal, rot in fl:
        o.append(rose(x, y, rr, *pal, rot=rot))
    # เบบี้บลูธเล็ก ๆ
    for i in range(int(n * .8)):
        a = r.uniform(0, 2 * math.pi); d = r.uniform(.6, 1.1)
        o.append(f'<circle cx="{fx(cx + math.cos(a) * rx * d)}" cy="{fx(cy + math.sin(a) * ry * d)}" r="{fx(1.4 * s)}" fill="{CREAM_L}"/>')
    return ''.join(o)

def chandelier(cx, cy, s, seed):
    r = random.Random(seed); o = []
    o.append(f'<path d="M{fx(cx)},{fx(cy - 500)} V{fx(cy - 34 * s)}" stroke="{GOLD_D}" stroke-width="{fx(2.4 * s)}"/>')
    o.append(poly([(cx - 10 * s, cy - 34 * s), (cx + 10 * s, cy - 34 * s), (cx + 5 * s, cy - 18 * s), (cx - 5 * s, cy - 18 * s)], GOLD))
    tiers = [(30, -6, 9), (52, 18, 13), (72, 42, 17)]
    for w, yy, n in tiers:
        ry = w * .22
        # สายคริสตัลด้านหลัง
        for i in range(n):
            a = 2 * math.pi * i / n
            if math.sin(a) > 0: continue
            x = cx + math.cos(a) * w * s; y = cy + (yy + math.sin(a) * ry) * s; L = r.uniform(14, 24) * s
            o.append(f'<path d="M{fx(x)},{fx(y)} V{fx(y + L)}" stroke="#f5dcae" stroke-width="{fx(.9 * s)}" opacity=".55" stroke-dasharray="{fx(2 * s)} {fx(1.4 * s)}"/>')
        # วงทอง: ด้านบนรับแสง ด้านล่างเงา
        o.append(f'<ellipse cx="{fx(cx)}" cy="{fx(cy + yy * s)}" rx="{fx(w * s)}" ry="{fx(ry * s)}" fill="none" stroke="{GOLD_D}" stroke-width="{fx(3.4 * s)}"/>')
        o.append(f'<path d="M{fx(cx - w * s)},{fx(cy + yy * s)} A{fx(w * s)},{fx(ry * s)} 0 0,1 {fx(cx + w * s)},{fx(cy + yy * s)}" fill="none" stroke="{GOLD_L}" stroke-width="{fx(2.2 * s)}"/>')
        for i in range(n):
            a = 2 * math.pi * i / n
            if math.sin(a) <= 0: continue
            x = cx + math.cos(a) * w * s; y = cy + (yy + math.sin(a) * ry) * s; L = r.uniform(14, 24) * s
            o.append(f'<path d="M{fx(x)},{fx(y)} V{fx(y + L)}" stroke="#ffe8bc" stroke-width="{fx(1 * s)}" stroke-dasharray="{fx(2 * s)} {fx(1.4 * s)}"/>')
            o.append(f'<path d="M{fx(x)},{fx(y + L)} l{fx(2.6 * s)},{fx(4 * s)} l{fx(-2.6 * s)},{fx(5 * s)} l{fx(-2.6 * s)},{fx(-5 * s)}Z" fill="#fff1d2"/>')
            o.append(f'<path d="M{fx(x)},{fx(y + L)} l{fx(2.6 * s)},{fx(4 * s)} l{fx(-2.6 * s)},{fx(5 * s)}Z" fill="#c9965a"/>')
        # เทียน
        m = 7 if w < 60 else 9
        for i in range(m):
            a = math.pi * (i + .5) / m
            x = cx - math.cos(a) * w * s; y = cy + (yy - math.sin(a) * ry) * s
            o.append(f'<rect x="{fx(x - 1.8 * s)}" y="{fx(y - 10 * s)}" width="{fx(3.6 * s)}" height="{fx(10 * s)}" fill="{CREAM_L}"/><rect x="{fx(x)}" y="{fx(y - 10 * s)}" width="{fx(1.8 * s)}" height="{fx(10 * s)}" fill="{CREAM_D}"/>')
            o.append(f'<path d="M{fx(x)},{fx(y - 18 * s)} q{fx(2.6 * s)},{fx(4 * s)} 0,{fx(6.5 * s)} q{fx(-2.6 * s)},{fx(-2.5 * s)} 0,{fx(-6.5 * s)}Z" fill="#fff4d0"/>')
    o.append(f'<path d="M{fx(cx)},{fx(cy + 66 * s)} l{fx(7 * s)},{fx(11 * s)} l{fx(-7 * s)},{fx(18 * s)} l{fx(-7 * s)},{fx(-18 * s)}Z" fill="#fff1d2"/><path d="M{fx(cx)},{fx(cy + 66 * s)} l{fx(7 * s)},{fx(11 * s)} l{fx(-7 * s)},{fx(18 * s)}Z" fill="#c9965a"/>')
    return ''.join(o)

def candle(x, y, s, h=16):
    return (f'<rect x="{fx(x - 2.4 * s)}" y="{fx(y - h * s)}" width="{fx(4.8 * s)}" height="{fx(h * s)}" fill="{CREAM_L}"/>'
            f'<rect x="{fx(x + .2 * s)}" y="{fx(y - h * s)}" width="{fx(2.2 * s)}" height="{fx(h * s)}" fill="{CREAM_D}"/>'
            f'<path d="M{fx(x)},{fx(y - (h + 9) * s)} q{fx(3 * s)},{fx(5 * s)} 0,{fx(8 * s)} q{fx(-3 * s)},{fx(-3 * s)} 0,{fx(-8 * s)}Z" fill="#fff2c8"/>')

def candelabra(x, y, s):
    o = [poly([(x - 14 * s, y), (x + 14 * s, y), (x + 5 * s, y - 14 * s), (x - 5 * s, y - 14 * s)], GOLD),
         poly([(x, y), (x + 14 * s, y), (x + 5 * s, y - 14 * s), (x, y - 14 * s)], GOLD_D),
         f'<rect x="{fx(x - 3 * s)}" y="{fx(y - 150 * s)}" width="{fx(6 * s)}" height="{fx(136 * s)}" fill="{GOLD}"/>',
         f'<rect x="{fx(x)}" y="{fx(y - 150 * s)}" width="{fx(3 * s)}" height="{fx(136 * s)}" fill="{GOLD_D}"/>',
         f'<rect x="{fx(x - 3 * s)}" y="{fx(y - 150 * s)}" width="{fx(1.4 * s)}" height="{fx(136 * s)}" fill="{GOLD_L}"/>']
    for d in (-2, -1, 1, 2):
        ex = x + d * 16 * s; ey = y - 150 * s - (abs(d) == 1) * 14 * s
        o.append(f'<path d="M{fx(x)},{fx(y - 128 * s)} Q{fx(ex)},{fx(y - 132 * s)} {fx(ex)},{fx(ey + 4 * s)}" stroke="{GOLD}" stroke-width="{fx(2.4 * s)}" fill="none"/>')
        o.append(f'<rect x="{fx(ex - 4 * s)}" y="{fx(ey)}" width="{fx(8 * s)}" height="{fx(3 * s)}" fill="{GOLD_L}"/>')
        o.append(candle(ex, ey, s, 18))
    o.append(f'<rect x="{fx(x - 4 * s)}" y="{fx(y - 168 * s)}" width="{fx(8 * s)}" height="{fx(3 * s)}" fill="{GOLD_L}"/>')
    o.append(candle(x, y - 168 * s, s, 22))
    return ''.join(o)

def chair(c, X, z):
    """เก้าอี้ชิวารีทอง มองจากหลัง ด้านที่หันเข้าหาแสงกลางห้องสว่าง อีกด้านเป็นเงา"""
    x, y = c.p(X, 0, z); k = c.k(z)
    W, S, T = 44 * k, 46 * k, 94 * k
    L = x - W / 2; R = x + W / 2
    lit_left = X > 0   # แสงมาจากกลางห้อง
    sgn = 1 if X > 0 else -1
    o = []
    # เงาตกขอบคมบนพื้น ยื่นออกจากแสง
    sx0, sy0 = c.p(X - 22, 0, z - 4); sx1, _ = c.p(X + 22, 0, z - 4)
    sx2, sy2 = c.p(X + 22 + sgn * 36, 0, z - 34); sx3, _ = c.p(X - 22 + sgn * 36, 0, z - 34)
    o.append(poly([(sx0, sy0), (sx1, sy0), (sx2, sy2), (sx3, sy2)], SHADOW, .45))
    o.append(f'<rect x="{fx(L + 2 * k)}" y="{fx(y - S)}" width="{fx(W - 4 * k)}" height="{fx(5 * k)}" fill="{CREAM}"/>')
    o.append(f'<rect x="{fx(L + 2 * k)}" y="{fx(y - S + 3.4 * k)}" width="{fx(W - 4 * k)}" height="{fx(1.8 * k)}" fill="{CREAM_D}"/>')
    for lx, is_lit in ((L, not lit_left), (R - 3.6 * k, lit_left)):
        o.append(f'<rect x="{fx(lx)}" y="{fx(y - T)}" width="{fx(3.6 * k)}" height="{fx(T)}" fill="{GOLD_L if is_lit else GOLD_D}"/>')
    for yy in (T, T - 22 * k, S + 12 * k):
        o.append(f'<rect x="{fx(L)}" y="{fx(y - yy)}" width="{fx(W)}" height="{fx(3.2 * k)}" fill="{GOLD}"/>')
        o.append(f'<rect x="{fx(L)}" y="{fx(y - yy)}" width="{fx(W)}" height="{fx(1.2 * k)}" fill="{GOLD_L}"/>')
    for i in range(1, 5):
        sx = L + W * i / 5
        o.append(f'<rect x="{fx(sx - .9 * k)}" y="{fx(y - T + 22 * k)}" width="{fx(1.8 * k)}" height="{fx(T - S - 34 * k)}" fill="{GOLD if i % 2 else GOLD_D}"/>')
    return ''.join(o)

def drape(x0, x1, ytop, ybot, n, lit_side=-1, tie=None):
    """ม่านหนา ไหล่ผ้าเป็นแถบสว่าง-เข้มสลับกันขอบคม"""
    o = []; w = (x1 - x0) / n
    for i in range(n):
        a = x0 + i * w; b = a + w
        sway = (i - n / 2) * 2
        o.append(poly([(a, ytop), (b, ytop), (b + sway, ybot), (a + sway, ybot)], WINE))
        o.append(poly([(a + w * .1, ytop), (a + w * .42, ytop), (a + w * .42 + sway, ybot), (a + w * .1 + sway, ybot)], WINE_L if (i % 2 == 0) else '#7e2636'))
        o.append(poly([(a + w * .72, ytop), (b, ytop), (b + sway, ybot), (a + w * .72 + sway, ybot)], WINE_D))
    return ''.join(o)

def sconce_light(x, y, s, wall_col):
    """ไฟผนังส่องเป็นรูปตัววีขึ้นลงบนผนัง ขอบคม 2 ชั้น"""
    o = []
    for (k, op) in ((1.0, .08), (.62, .1)):
        o.append(poly([(x - 8 * s, y - 6 * s), (x + 8 * s, y - 6 * s), (x + 46 * s * k, y - 120 * s * k), (x - 46 * s * k, y - 120 * s * k)], AMBER, op))
        o.append(poly([(x - 6 * s, y + 10 * s), (x + 6 * s, y + 10 * s), (x + 30 * s * k, y + 80 * s * k), (x - 30 * s * k, y + 80 * s * k)], AMBER, op))
    o.append(f'<path d="M{fx(x - 5 * s)},{fx(y - 4 * s)} h{fx(10 * s)} v{fx(26 * s)} h{fx(-10 * s)}Z" fill="{GOLD}"/><path d="M{fx(x)},{fx(y - 4 * s)} h{fx(5 * s)} v{fx(26 * s)} h{fx(-5 * s)}Z" fill="{GOLD_D}"/>')
    for d in (-1, 1):
        o.append(f'<path d="M{fx(x)},{fx(y + 8 * s)} q{fx(d * 16 * s)},{fx(4 * s)} {fx(d * 17 * s)},{fx(-12 * s)}" stroke="{GOLD}" stroke-width="{fx(2.2 * s)}" fill="none"/>')
        o.append(poly([(x + d * 17 * s - 7 * s, y - 4 * s), (x + d * 17 * s + 7 * s, y - 4 * s), (x + d * 17 * s + 4 * s, y - 16 * s), (x + d * 17 * s - 4 * s, y - 16 * s)], '#ffe3b0'))
        o.append(poly([(x + d * 17 * s, y - 4 * s), (x + d * 17 * s + 7 * s, y - 4 * s), (x + d * 17 * s + 4 * s, y - 16 * s), (x + d * 17 * s, y - 16 * s)], '#e8b878'))
    return ''.join(o)

def mote(seed, box_, n):
    r = random.Random(seed); x0, y0, x1, y1 = box_; o = []
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if r.random() < .4:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.4, 2.4):.1f}" fill="#ffe2b0" opacity="{r.uniform(.2, .35):.2f}" filter="url(#mBlur)"/>')
        else:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6, 1.2):.1f}" fill="#fff0d0" opacity="{r.uniform(.5, .85):.2f}"/>')
    return ''.join(o)

# ================================================================ ห้องจัดเลี้ยง
def scene_ballroom():
    c = Cam(270, 430, 160, 600); ZB = 1000; YC = 700
    o = []
    # เพดานมืด + ผ้าโค้งระบาย
    o.append('<rect width="540" height="200" fill="#211819"/>')
    # ผนังหลัง
    o.append(path(back(c, -900, 900, 0, YC, ZB), WALL))
    o.append(f'<path d="{back(c, -900, 900, 110, YC - 70, ZB)}" fill="url(#damask3)"/>')
    # บัวผนังบนแบบทอง
    o.append(path(back(c, -900, 900, YC - 70, YC - 58, ZB), GOLD_D))
    o.append(path(back(c, -900, 900, YC - 70, YC - 66, ZB), GOLD))
    o.append(path(back(c, -900, 900, YC - 58, YC, ZB), WALL_D))
    # แผงไม้ผนังล่าง
    o.append(path(back(c, -900, 900, 0, 105, ZB), WOOD))
    o.append(path(back(c, -900, 900, 98, 105, ZB), WOOD_L))
    for X in range(-900, 900, 120):
        o.append(path(back(c, X + 14, X + 106, 18, 86, ZB), WOOD_D))
        o.append(path(back(c, X + 14, X + 106, 80, 86, ZB), WOOD_L))
    # เสาประดับ + กรอบกระจกทองระหว่างเสา
    for X in (-470, -250, 250, 470):
        o.append(path(back(c, X - 26, X + 26, 0, YC - 70, ZB), PIL))
        lit = -1 if X > 0 else 1
        if lit > 0: o.append(path(back(c, X + 14, X + 26, 0, YC - 70, ZB), PIL_L))
        else: o.append(path(back(c, X - 26, X - 14, 0, YC - 70, ZB), PIL_L))
        o.append(path(back(c, X - 32, X + 32, YC - 110, YC - 70, ZB), PIL_L))
        o.append(path(back(c, X - 32, X + 32, YC - 110, YC - 102, ZB), PIL_D))
        o.append(path(back(c, X - 32, X + 32, 0, 22, ZB), PIL_D))
    for (a, b) in ((-430, -290), (290, 430)):
        x0, y1 = c.p(a, 150, ZB); x1, y0 = c.p(b, 520, ZB)
        o.append(f'<rect x="{fx(x0)}" y="{fx(y0)}" width="{fx(x1 - x0)}" height="{fx(y1 - y0)}" fill="{GOLD_D}"/>')
        o.append(f'<rect x="{fx(x0 + 4)}" y="{fx(y0 + 4)}" width="{fx(x1 - x0 - 8)}" height="{fx(y1 - y0 - 8)}" fill="#5a4a4a"/>')
        o.append(poly([(x0 + 4, y1 - 4), (x0 + 4, y1 - 60), (x1 - 4, y0 + 30), (x1 - 4, y0 + 70)], '#6e5c58'))
        o.append(f'<rect x="{fx(x0)}" y="{fx(y0)}" width="{fx(x1 - x0)}" height="3" fill="{GOLD_L}"/>')
    # หน้าต่างโค้งใหญ่กลางผนัง (กลางคืน เย็นตัดกับแสงเทียนอุ่น)
    wx0, wyb = c.p(-175, 120, ZB); wx1, wyt = c.p(175, 600, ZB)
    o.append(path(arch_d(wx0 - 12, wx1 + 12, wyt - 12, wyb + 6), GOLD_D))
    o.append(path(arch_d(wx0 - 8, wx1 + 8, wyt - 8, wyb + 6), '#7a5a3c'))
    o.append(f'<clipPath id="w3"><path d="{arch_d(wx0, wx1, wyt, wyb)}"/></clipPath><g clip-path="url(#w3)">')
    o.append(f'<rect x="{fx(wx0)}" y="{fx(wyt)}" width="{fx(wx1 - wx0)}" height="{fx(wyb - wyt)}" fill="{NIGHT}"/>')
    o.append(f'<rect x="{fx(wx0)}" y="{fx(wyt + (wyb - wyt) * .55)}" width="{fx(wx1 - wx0)}" height="{fx((wyb - wyt) * .45)}" fill="#34406a"/>')
    o.append(city(wx0, wx1, wyb, 33, ('#1f2744', '#19203a', '#141a30'), '#ffcf8a', 120))
    o.append(f'<circle cx="{fx(wx1 - 40)}" cy="{fx(wyt + 70)}" r="11" fill="#e8ecf6"/><circle cx="{fx(wx1 - 36)}" cy="{fx(wyt + 67)}" r="10" fill="{NIGHT}"/>')
    o.append(poly([(wx0, wyb), (wx0 + 70, wyt), (wx0 + 110, wyt), (wx0 + 40, wyb)], '#ffffff', .06))
    o.append('</g>')
    cxw = (wx0 + wx1) / 2; rw = (wx1 - wx0) / 2
    for t in (1 / 3, 2 / 3):
        xx = wx0 + (wx1 - wx0) * t
        top = wyt + rw - math.sqrt(max(0, rw * rw - (xx - cxw) ** 2))
        o.append(f'<rect x="{fx(xx - 2)}" y="{fx(top)}" width="4" height="{fx(wyb - top)}" fill="#7a5a3c"/>')
    for t in (.42, .64, .84):
        yy = wyt + (wyb - wyt) * t
        o.append(f'<rect x="{fx(wx0)}" y="{fx(yy - 2)}" width="{fx(wx1 - wx0)}" height="4" fill="#7a5a3c"/>')
    # ม่านแดงไวน์สองข้างหน้าต่าง + ระบายบน
    o.append(drape(wx0 - 52, wx0 + 18, wyt + 30, wyb + 10, 4))
    o.append(drape(wx1 - 18, wx1 + 52, wyt + 30, wyb + 10, 4))
    for d in (-1, 1):
        tx = wx0 + 6 if d < 0 else wx1 - 6
        o.append(f'<rect x="{fx(tx - 10)}" y="{fx(wyb - 110)}" width="20" height="7" fill="{GOLD}"/><rect x="{fx(tx - 10)}" y="{fx(wyb - 110)}" width="20" height="2.4" fill="{GOLD_L}"/>')
    sw = f'M{fx(wx0 - 60)},{fx(wyt + 20)} Q{fx(cxw)},{fx(wyt + 120)} {fx(wx1 + 60)},{fx(wyt + 20)} L{fx(wx1 + 60)},{fx(wyt + 46)} Q{fx(cxw)},{fx(wyt + 150)} {fx(wx0 - 60)},{fx(wyt + 46)}Z'
    o.append(path(sw, WINE))
    o.append(f'<path d="M{fx(wx0 - 60)},{fx(wyt + 20)} Q{fx(cxw)},{fx(wyt + 120)} {fx(wx1 + 60)},{fx(wyt + 20)} L{fx(wx1 + 60)},{fx(wyt + 28)} Q{fx(cxw)},{fx(wyt + 130)} {fx(wx0 - 60)},{fx(wyt + 28)}Z" fill="{WINE_L}"/>')
    o.append(f'<path d="M{fx(wx0 - 60)},{fx(wyt + 40)} Q{fx(cxw)},{fx(wyt + 142)} {fx(wx1 + 60)},{fx(wyt + 40)} L{fx(wx1 + 60)},{fx(wyt + 46)} Q{fx(cxw)},{fx(wyt + 150)} {fx(wx0 - 60)},{fx(wyt + 46)}Z" fill="{WINE_D}"/>')
    # ไฟผนัง
    for X in (-250, 250, -470, 470):
        x, y = c.p(X, 360, ZB); o.append(sconce_light(x, y, .62, WALL))
    # แสงเทียนบนผนังหลังแท่นพิธี (ก้อนแสงขอบคม 2 ชั้น)
    ax, ay = c.p(0, 150, ZB)
    o.append(f'<ellipse cx="{fx(ax)}" cy="{fx(ay + 30)}" rx="120" ry="34" fill="{AMBER}" opacity=".10"/>')
    # พื้นไม้ขัดเงา
    fl = flat(c, -900, 900, 140, ZB, 0)
    o.append(path(fl, WOOD))
    o.append(f'<clipPath id="f3"><path d="{fl}"/></clipPath><g clip-path="url(#f3)">')
    r = random.Random(3)
    for X in range(-900, 900, 26):
        o.append(f'<path d="{c.poly([(X, 0, ZB), (X + 1.2, 0, ZB), (X + 1.2, 0, 140), (X, 0, 140)])}" fill="{WOOD_D}"/>')
        z = ZB
        while z > 160:
            z -= r.uniform(90, 200)
            o.append(f'<path d="{c.poly([(X, 0, z), (X + 26, 0, z), (X + 26, 0, z - 2), (X, 0, z - 2)])}" fill="{WOOD_D}"/>')
        if r.random() < .3:
            o.append(f'<path d="{c.poly([(X + 2, 0, ZB), (X + 24, 0, ZB), (X + 24, 0, 140), (X + 2, 0, 140)])}" fill="#553828" opacity=".6"/>')
    # แสงสะท้อนบนพื้นใต้โคมระย้าและแท่นพิธี ขอบคม
    for (X, z, rx, ry, op) in ((0, 560, 230, 52, .07), (0, 560, 140, 32, .09), (0, 900, 200, 24, .08)):
        x, y = c.p(X, 0, z)
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{rx}" ry="{ry}" fill="{AMBER}" opacity="{op}"/>')
    o.append('</g>')
    # แท่นพิธี
    o.append(box(c, -340, 340, 0, 34, 880, ZB, '#5a3c2c', '#3e2a20', '#33231b'))
    o.append(path(back(c, -340, 340, 28, 34, 880), GOLD))
    o.append(box(c, -150, 150, 0, 17, 845, 880, '#5a3c2c', '#3e2a20', '#33231b'))
    o.append(path(back(c, -150, 150, 13, 17, 845), GOLD_D))
    # พรมทางเดินแดงไวน์
    o.append(path(flat(c, -84, 84, 140, 845, 0), WINE_D))
    o.append(path(flat(c, -76, 76, 140, 845, 0), WINE))
    o.append(path(flat(c, -76, 0, 140, 845, 0), '#7a2434'))
    o.append(path(flat(c, -84, -78, 140, 845, 0), GOLD))
    o.append(path(flat(c, 78, 84, 140, 845, 0), GOLD))
    lx, ly = c.p(0, 0, 560)
    o.append(f'<ellipse cx="{fx(lx)}" cy="{fx(ly)}" rx="80" ry="20" fill="{WINE_L}" opacity=".45"/>')
    rr = random.Random(7)
    for i in range(110):
        z = rr.uniform(160, 840); X = rr.uniform(-72, 72); x, y = c.p(X, 0, z); k = c.k(z)
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(3.4 * k)}" ry="{fx(1.6 * k)}" transform="rotate({rr.uniform(-40, 40):.0f} {fx(x)} {fx(y)})" fill="{rr.choice((CREAM, CREAM_L, "#e9c3b8"))}"/>')
    # โต๊ะพิธีคลุมผ้า
    o.append(box(c, -95, 95, 34, 120, 930, 975, CREAM_L, CREAM, CREAM_D))
    tx0, ty0 = c.p(-95, 120, 930); tx1, ty1 = c.p(95, 34, 930)
    for i in range(7):
        a = tx0 + (tx1 - tx0) * i / 7; b = a + (tx1 - tx0) / 7
        o.append(poly([(a + (b - a) * .55, ty0), (b, ty0), (b + 1, ty1), (a + (b - a) * .55 + 1, ty1)], '#cdb592'))
    o.append(poly([(tx0, ty0), (tx1, ty0), (tx1, ty0 + 8), (tx0, ty0 + 8)], '#d9c3a0'))
    # ผ้าห้อยหน้าโต๊ะ + พวงดอกไม้
    gl = f'M{fx(tx0)},{fx(ty0 + 6)} Q{fx((tx0 + tx1) / 2)},{fx(ty0 + 40)} {fx(tx1)},{fx(ty0 + 6)}'
    o.append(f'<path d="{gl}" stroke="{WINE}" stroke-width="6" fill="none"/>')
    for i in range(11):
        t = i / 10; gx = tx0 + (tx1 - tx0) * t; gy = ty0 + 6 + 34 * 4 * t * (1 - t) * .5 * 2
        o.append(bouquet(gx, gy, 8, 6, 900 + i, .55, 5, 0, .2))
    # เชิงเทียนบนโต๊ะและบนแท่น
    for X in (-60, 60):
        x, y = c.p(X, 120, 950); o.append(candelabra(x, y, c.k(950) * .55))
    for X in (-250, 250):
        x, y = c.p(X, 34, 960); o.append(candelabra(x, y, c.k(960) * 1.05))
    # แจกันดอกไม้ใหญ่สองข้างแท่น
    for X in (-160, 160):
        x, y = c.p(X, 34, 905); k = c.k(905)
        o.append(poly([(x - 18 * k, y), (x + 18 * k, y), (x + 12 * k, y - 70 * k), (x + 26 * k, y - 90 * k), (x - 26 * k, y - 90 * k), (x - 12 * k, y - 70 * k)], GOLD))
        o.append(poly([(x, y), (x + 18 * k, y), (x + 12 * k, y - 70 * k), (x + 26 * k, y - 90 * k), (x, y - 90 * k)], GOLD_D))
        o.append(bouquet(x, y - 118 * k, 52 * k, 38 * k, 50 + X, 1.05, 34, 6))
    # เก้าอี้แขก
    rows = [800, 730, 660, 595, 535, 480, 430, 385, 345]
    for zi, z in enumerate(rows):
        for sgn in (-1, 1):
            X = 128
            while True:
                x, _ = c.p(sgn * X, 0, z)
                if x < -60 or x > 600: break
                o.append(chair(c, sgn * X, z)); X += 56
        if zi % 2 == 0:
            for sgn in (-1, 1):
                x, y = c.p(sgn * 128, 66, z + 2); k = c.k(z)
                o.append(bouquet(x, y, 12 * k, 9 * k, 400 + zi * 2 + sgn, .5 * k, 9, 2))
                o.append(f'<path d="M{fx(x - 2 * k)},{fx(y + 6 * k)} q{fx(-3 * k)},{fx(20 * k)} {fx(-6 * k)},{fx(34 * k)} M{fx(x + 2 * k)},{fx(y + 6 * k)} q{fx(3 * k)},{fx(18 * k)} {fx(7 * k)},{fx(30 * k)}" stroke="{CREAM}" stroke-width="{fx(2.4 * k)}" fill="none"/>')
    # ผ้าระบายเพดาน
    for (yy, sag, col, colL, colD, n) in ((150, 30, '#d7c2a0', CREAM_L, '#8e7658', 3), (40, 46, '#cdb592', '#f6e4c4', '#7e6648', 2)):
        w = 540 / n
        for i in range(n):
            a = i * w - 10; b = a + w + 20; m = (a + b) / 2
            d = f'M{fx(a)},{fx(yy - 30)} Q{fx(m)},{fx(yy + sag * 2)} {fx(b)},{fx(yy - 30)} L{fx(b)},{fx(yy - 50)} Q{fx(m)},{fx(yy + sag * 1.2)} {fx(a)},{fx(yy - 50)}Z'
            o.append(path(d, col))
            o.append(f'<path d="M{fx(a)},{fx(yy - 30)} Q{fx(m)},{fx(yy + sag * 2)} {fx(b)},{fx(yy - 30)} L{fx(b)},{fx(yy - 36)} Q{fx(m)},{fx(yy + sag * 1.8)} {fx(a)},{fx(yy - 36)}Z" fill="{colL}"/>')
            o.append(f'<path d="M{fx(a)},{fx(yy - 50)} Q{fx(m)},{fx(yy + sag * 1.2)} {fx(b)},{fx(yy - 50)} L{fx(b)},{fx(yy - 44)} Q{fx(m)},{fx(yy + sag * 1.4)} {fx(a)},{fx(yy - 44)}Z" fill="{colD}"/>')
        for i in range(n + 1):
            o.append(bouquet(i * w, yy - 40, 16, 12, 600 + i + yy, .7, 10, 2))
    # โคมระย้า
    x, y = c.p(0, 520, 520); o.append(chandelier(x, y - 10, c.k(520) * 1.0, 1))
    for X in (-340, 340):
        x, y = c.p(X, 520, 860); o.append(chandelier(x, y, c.k(860) * .9, 2 + X))
    o.append(mote(9, (120, 120, 420, 640), 26))
    # ฉากหน้ามืดเบลอ: พนักเก้าอี้แถวหน้าสุด + ดอกไม้
    o.append(f'<g filter="url(#dof3)" opacity=".95">{chair(c, -150, 190)}{chair(c, 150, 190)}{bouquet(30, 880, 70, 60, 77, 2.2, 22, 4)}{bouquet(520, 900, 70, 60, 78, 2.2, 22, 4)}</g>')
    o.append(f'<rect x="0" y="700" width="540" height="260" fill="url(#fgDark)"/>')
    return ''.join(o)

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stip3" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.2" numOctaves="1" seed="4"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="brush3" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency=".012 .05" numOctaves="3" seed="2"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="dof3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="mBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<radialGradient id="vig3" cx=".5" cy=".42" r=".78"><stop offset=".5" stop-color="#140c0e" stop-opacity="0"/><stop offset="1" stop-color="#140c0e" stop-opacity=".6"/></radialGradient>
<linearGradient id="fgDark" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#140c0e" stop-opacity="0"/><stop offset="1" stop-color="#140c0e" stop-opacity=".45"/></linearGradient>
<pattern id="damask3" width="40" height="52" patternUnits="userSpaceOnUse"><g fill="#3d302e"><path d="M20,6 C25,13 30,16 30,24 C30,31 24,34 20,42 C16,34 10,31 10,24 C10,16 15,13 20,6Z"/><path d="M20,14 C17,20 17,28 20,34 C23,28 23,20 20,14Z" fill="#4a3b38"/><circle cx="0" cy="24" r="2.4"/><circle cx="40" cy="24" r="2.4"/><circle cx="20" cy="49" r="2"/></g></pattern>
</defs></svg>'''

def frame(content, label):
    tex = ('<rect width="540" height="960" filter="url(#brush3)" opacity=".10" style="mix-blend-mode:overlay"/>'
           '<rect width="540" height="960" filter="url(#stip3)" opacity=".16" style="mix-blend-mode:overlay"/>'
           '<rect width="540" height="960" fill="url(#vig3)"/>')
    return (f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">{content}{tex}'
            '<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".75" stroke-dasharray="6 5" stroke-width="1.5"/>'
            '<text x="270" y="652" text-anchor="middle" font-size="13" fill="#fff" fill-opacity=".8" font-family="IBM Plex Sans Thai, sans-serif">พื้นที่ซับ</text></g></svg>')

CSS = '''<title>ห้องจัดเลี้ยงโทนใหม่</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&display=swap">
<style>
/* Layout: one 9:16 frame on a dark stage with notes beside it (stacks on phones). Single dark look by choice. */
:root{--stage:#120d0e;--ink:#eadfd2;--muted:#a8978a;--line:#33282a;--accent:#e8c07a;--font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;color-scheme:dark}
html,body{background:var(--stage);color:var(--ink)}
body{font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 40px}
.wrap{max-width:980px;margin:0 auto;display:flex;flex-wrap:wrap;gap:28px;align-items:flex-start;justify-content:center}
.frame{flex:0 1 460px;min-width:0;max-width:100%}
.frame svg{display:block;width:100%;height:auto;aspect-ratio:9/16;border-radius:4px;box-shadow:0 0 0 1px var(--line),0 18px 44px rgba(0,0,0,.5)}
.side{flex:1 1 280px;min-width:0;display:flex;flex-direction:column;gap:14px;font-size:14px;line-height:1.65}
h1{margin:0;font-size:21px;font-weight:600;text-wrap:balance}
h1 span{display:block;font-size:13px;font-weight:400;color:var(--muted);margin-top:4px}
ul{margin:0;padding-left:18px;display:flex;flex-direction:column;gap:6px}
li{color:var(--ink)}
li b{color:var(--accent);font-weight:500}
p{margin:0;color:var(--muted)}
button{align-self:flex-start;font:inherit;font-size:13px;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:6px;padding:7px 12px;cursor:pointer}
button:hover{border-color:var(--muted)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button[aria-pressed="true"]{border-color:var(--accent);color:#fff}
.guide{display:none}.show-guide .guide{display:inline}
</style>'''

def build():
    svg = frame(scene_ballroom(), 'ห้องจัดเลี้ยงโทนใหม่ ผนังลายดามัสก์สีเข้ม หน้าต่างโค้งเห็นเมืองกลางคืน ม่านแดงไวน์ แท่นพิธีมีเชิงเทียนและแจกันดอกกุหลาบ เก้าอี้ทอง พื้นไม้ขัดเงา และพรมแดงไวน์')
    page = CSS + DEFS + f'''<div class="wrap" id="wrap"><div class="frame">{svg}</div>
<div class="side"><h1>ห้องจัดเลี้ยง · โทนใหม่<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ฉากทดลองก่อนทำอีก 4 ฉาก</span></h1>
<ul>
<li><b>แสงเงา</b> ตัดเป็นก้อนสีเข้มอ่อนขอบคม ไม่ใช้แสงฟุ้ง ไฟผนังส่องเป็นรูปตัววี เก้าอี้มีเงาตกขอบคม</li>
<li><b>สี</b> ผนังน้ำตาลเข้มลายดามัสก์ ไม้เข้ม ทอง แดงไวน์ ครีม แสงเทียนอำพัน หน้าต่างเป็นฟ้ากลางคืนเย็นตัดกับแสงอุ่น</li>
<li><b>เพดาน</b> เปลี่ยนจากฝ้าลายตารางเป็นเพดานมืดกับผ้าระบายครีมห้อยเป็นโค้ง มีช่อดอกไม้ตรงจุดผูก</li>
<li><b>พื้น</b> เปลี่ยนจากหินอ่อนเป็นไม้ขัดเงาสีเข้ม มีแสงสะท้อนเป็นก้อนใต้โคมและหน้าแท่น</li>
<li><b>ดอกไม้</b> เลิกใช้ซุ้มโค้ง เปลี่ยนเป็นแท่นพิธีมีโต๊ะคลุมผ้า เชิงเทียน และแจกันทองใส่กุหลาบครีม ชมพู และแดงไวน์ กลีบตัดแสงเงาเป็นชิ้น</li>
</ul>
<p>ยังไม่มีตัวละคร ถ้าทางนี้ใช่ ผมจะทำโถงหน้าห้อง ห้องแต่งตัว ห้องพัก และลิฟต์ตามแนวเดียวกัน</p>
<button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets3.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
