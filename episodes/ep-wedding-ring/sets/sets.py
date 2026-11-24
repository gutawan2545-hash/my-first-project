# Odd Hours · ตอนงานแต่ง · ฉากโรงแรมหรู 5 ฉาก (พื้นหลังเปล่า ยังไม่มีตัวละคร)
# รัน: python3 sets.py  -> sets.html
# ทุกฉากใช้กล้องมุมมองจุดเดียว หน่วยโลกเป็นเซนติเมตร แล้วฉายลงเฟรม 540x960
import math, random

def fx(v): return f'{v:.1f}'

class Cam:
    def __init__(s, VX, VY, H, f):
        s.VX, s.VY, s.H, s.f = VX, VY, H, f
    def k(s, z): return s.f / z
    def p(s, X, Y, z):
        k = s.f / z
        return (s.VX + X * k, s.VY + (s.H - Y) * k)
    def poly(s, pts):
        return 'M' + ' L'.join('%.1f,%.1f' % s.p(*q) for q in pts) + 'Z'

def P(pts): return 'M' + ' L'.join('%.1f,%.1f' % q for q in pts) + 'Z'
def path(d, fill, extra=''): return f'<path d="{d}" fill="{fill}" {extra}/>'

def back(c, X0, X1, Y0, Y1, z): return c.poly([(X0, Y0, z), (X1, Y0, z), (X1, Y1, z), (X0, Y1, z)])
def side(c, X, z0, z1, Y0, Y1): return c.poly([(X, Y0, z0), (X, Y0, z1), (X, Y1, z1), (X, Y1, z0)])
def flat(c, X0, X1, z0, z1, Y): return c.poly([(X0, Y, z0), (X1, Y, z0), (X1, Y, z1), (X0, Y, z1)])

def box(c, X0, X1, Y0, Y1, z0, z1, top, front, sideC):
    o = ''
    if Y1 < c.H: o += path(flat(c, X0, X1, z0, z1, Y1), top)
    elif Y0 > c.H: o += path(flat(c, X0, X1, z0, z1, Y0), sideC)
    if X0 > 0: o += path(side(c, X0, z0, z1, Y0, Y1), sideC)
    elif X1 < 0: o += path(side(c, X1, z0, z1, Y0, Y1), sideC)
    o += path(back(c, X0, X1, Y0, Y1, z0), front)
    return o

def fshadow(c, X0, X1, z0, z1, sx=22, sz=18, op=.35):
    """เงาตกนุ่ม ๆ บนพื้น เยื้องไปทางขวาล่าง"""
    return f'<path d="{flat(c, X0 + sx, X1 + sx, z0 - sz, z1 - sz, 0)}" fill="#3a2a28" opacity="{op}" filter="url(#soft)"/>'

def softsh(d, dx=6, dy=8, op=.35):
    return f'<path d="{d}" fill="#3a2a28" opacity="{op}" transform="translate({dx},{dy})" filter="url(#soft)"/>'

def mix(a, b, t):
    a = [int(a[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join('%02x' % round(a[i] + (b[i] - a[i]) * t) for i in range(3))
def shade(c, t=.28): return mix(c, '#6a5250', t)
def light(c, t=.45): return mix(c, '#ffffff', t)

# ---------------------------------------------------------------- props
def bloom(x, y, s, c):
    d = shade(c, .3)
    return (f'<circle cx="{fx(x)}" cy="{fx(y + s * .22)}" r="{fx(s)}" fill="{d}"/>'
            f'<circle cx="{fx(x - s * .12)}" cy="{fx(y - s * .05)}" r="{fx(s * .86)}" fill="{c}"/>'
            f'<path d="M{fx(x - s * .5)},{fx(y)} a{fx(s * .42)},{fx(s * .42)} 0 1,1 {fx(s * .72)},{fx(s * .22)}" fill="none" stroke="{d}" stroke-width="{fx(max(.4, s * .13))}"/>'
            f'<circle cx="{fx(x - s * .05)}" cy="{fx(y)}" r="{fx(s * .2)}" fill="{d}"/>')

PAL_W = ('#fffaf7', '#fdf3f5', '#f7dbe4', '#f1e7f6', '#fffaf7', '#ffffff')
LEAF = ('#9fb8a2', '#87a592', '#b5cbb0', '#7c9888')

def flowers(cx, cy, rx, ry, seed, n=40, s=1.0, pal=PAL_W, leaf=True, trail=0):
    r = random.Random(seed); o = []
    if leaf:
        for i in range(int(n * .55)):
            a = r.uniform(0, 2 * math.pi); d = r.uniform(.7, 1.15)
            x = cx + math.cos(a) * rx * d; y = cy + math.sin(a) * ry * d
            o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(6 * s)}" ry="{fx(2.4 * s)}" transform="rotate({math.degrees(a):.0f} {fx(x)} {fx(y)})" fill="{r.choice(LEAF)}"/>')
    for i in range(trail):
        x = cx + r.uniform(-rx, rx) * .8; y0 = cy + ry * .5; L = r.uniform(.6, 1.4) * ry * 1.6
        o.append(f'<path d="M{fx(x)},{fx(y0)} q{fx(r.uniform(-8, 8) * s)},{fx(L * .5)} {fx(r.uniform(-6, 6) * s)},{fx(L)}" stroke="{r.choice(LEAF)}" stroke-width="{fx(1.4 * s)}" fill="none"/>')
        for j in range(4):
            o.append(f'<circle cx="{fx(x + r.uniform(-4, 4) * s)}" cy="{fx(y0 + L * (j + 1) / 5)}" r="{fx(1.8 * s)}" fill="{r.choice(LEAF)}"/>')
    bl = []
    for i in range(n):
        a = r.uniform(0, 2 * math.pi); d = math.sqrt(r.random())
        bl.append((cy + math.sin(a) * ry * d, cx + math.cos(a) * rx * d, r.uniform(3.4, 6.2) * s, r.choice(pal)))
    bl.sort()
    o += [bloom(x, y, ss, c) for y, x, ss, c in bl]
    # แสงจากซ้ายบน
    o.append(f'<ellipse cx="{fx(cx - rx * .3)}" cy="{fx(cy - ry * .35)}" rx="{fx(rx * .6)}" ry="{fx(ry * .5)}" fill="#fff" opacity=".18" filter="url(#soft)"/>')
    return ''.join(o)

def chandelier(cx, cy, s, seed, glow=True):
    r = random.Random(seed); o = []
    if glow:
        o.append(f'<circle cx="{fx(cx)}" cy="{fx(cy + 30 * s)}" r="{fx(150 * s)}" fill="url(#chGlow)"/>')
    o.append(f'<path d="M{fx(cx)},{fx(cy - 400)} L{fx(cx)},{fx(cy - 30 * s)}" stroke="#b79a6e" stroke-width="{fx(2 * s)}"/>')
    o.append(f'<path d="M{fx(cx - 9 * s)},{fx(cy - 30 * s)} L{fx(cx + 9 * s)},{fx(cy - 30 * s)} L{fx(cx + 4 * s)},{fx(cy - 16 * s)} L{fx(cx - 4 * s)},{fx(cy - 16 * s)}Z" fill="#e9d3a4"/>')
    tiers = [(26, -10, 9, 16), (46, 12, 13, 22), (64, 36, 17, 28), (42, 60, 11, 20)]
    items = []
    for w, yy, n, L in tiers:
        ry = w * .24
        for i in range(n):
            a = 2 * math.pi * i / n + r.uniform(-.1, .1)
            x = cx + math.cos(a) * w * s; y = cy + (yy + math.sin(a) * ry) * s
            items.append((math.sin(a), x, y, L * s * r.uniform(.8, 1.15)))
        items.append((0.0, ('ring', w, yy, ry), 0, 0))
    items.sort(key=lambda t: t[0])
    for depth, x, y, L in items:
        if isinstance(x, tuple):
            _, w, yy, ry = x
            o.append(f'<ellipse cx="{fx(cx)}" cy="{fx(cy + yy * s)}" rx="{fx(w * s)}" ry="{fx(ry * s)}" fill="none" stroke="#e8cf9c" stroke-width="{fx(2.6 * s)}"/>')
            o.append(f'<ellipse cx="{fx(cx)}" cy="{fx(cy + yy * s + .8 * s)}" rx="{fx(w * s)}" ry="{fx(ry * s)}" fill="none" stroke="#b6946a" stroke-width="{fx(1 * s)}" opacity=".7"/>')
            continue
        op = .55 + .45 * (depth + 1) / 2
        o.append(f'<path d="M{fx(x)},{fx(y)} L{fx(x)},{fx(y + L)}" stroke="#f4eefc" stroke-width="{fx(.9 * s)}" opacity="{op:.2f}" stroke-dasharray="{fx(2 * s)} {fx(1.2 * s)}"/>')
        o.append(f'<path d="M{fx(x)},{fx(y + L)} l{fx(2.4 * s)},{fx(3.5 * s)} l{fx(-2.4 * s)},{fx(4.5 * s)} l{fx(-2.4 * s)},{fx(-4.5 * s)}Z" fill="#fbf7ff" opacity="{op:.2f}"/>')
        o.append(f'<path d="M{fx(x)},{fx(y + L)} l{fx(2.4 * s)},{fx(3.5 * s)} l{fx(-2.4 * s)},{fx(4.5 * s)}Z" fill="#cbbbe8" opacity="{op:.2f}"/>')
    for w, yy in ((46, 12), (64, 36)):
        for i in range(7 if w < 60 else 9):
            a = math.pi * (i + .5) / (7 if w < 60 else 9)
            x = cx - math.cos(a) * w * s; y = cy + (yy - math.sin(a) * w * .24) * s
            o.append(f'<rect x="{fx(x - 1.6 * s)}" y="{fx(y - 9 * s)}" width="{fx(3.2 * s)}" height="{fx(9 * s)}" fill="#fff8ef"/>')
            o.append(f'<circle cx="{fx(x)}" cy="{fx(y - 11 * s)}" r="{fx(2.6 * s)}" fill="#fffaf0" filter="url(#glow)"/>')
    o.append(f'<path d="M{fx(cx)},{fx(cy + 68 * s)} l{fx(6 * s)},{fx(10 * s)} l{fx(-6 * s)},{fx(16 * s)} l{fx(-6 * s)},{fx(-16 * s)}Z" fill="#f6f0ff"/>')
    o.append(f'<path d="M{fx(cx)},{fx(cy + 68 * s)} l{fx(6 * s)},{fx(10 * s)} l{fx(-6 * s)},{fx(16 * s)}Z" fill="#c7b6e6"/>')
    return ''.join(o)

def sconce(x, y, s):
    o = [f'<circle cx="{fx(x)}" cy="{fx(y - 8 * s)}" r="{fx(46 * s)}" fill="url(#chGlow)"/>',
         f'<path d="M{fx(x - 4 * s)},{fx(y - 6 * s)} h{fx(8 * s)} v{fx(22 * s)} h{fx(-8 * s)}Z" fill="#e3c792"/>']
    for d in (-1, 1):
        o.append(f'<path d="M{fx(x)},{fx(y + 6 * s)} q{fx(d * 14 * s)},{fx(4 * s)} {fx(d * 15 * s)},{fx(-10 * s)}" stroke="#d7b983" stroke-width="{fx(2 * s)}" fill="none"/>')
        o.append(f'<path d="M{fx(x + d * 15 * s - 5 * s)},{fx(y - 4 * s)} h{fx(10 * s)} l{fx(-2 * s)},{fx(-10 * s)} h{fx(-6 * s)}Z" fill="#fff6ec"/>')
        o.append(f'<path d="M{fx(x + d * 15 * s)},{fx(y - 4 * s)} h{fx(5 * s)} l{fx(-2 * s)},{fx(-10 * s)} h{fx(-3 * s)}Z" fill="#e9d9e8"/>')
        o.append(f'<circle cx="{fx(x + d * 15 * s)}" cy="{fx(y - 9 * s)}" r="{fx(3 * s)}" fill="#fffaf2" filter="url(#glow)"/>')
    return ''.join(o)

def dust(seed, box_, n, col='#fff8f2'):
    r = random.Random(seed); x0, y0, x1, y1 = box_; near = far = ''
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if r.random() < .45: far += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.4, 2.6):.1f}" opacity="{r.uniform(.22, .42):.2f}"/>'
        else: near += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6, 1.4):.1f}" opacity="{r.uniform(.55, .95):.2f}"/>'
    return f'<g fill="{col}"><g filter="url(#moteBlur)">{far}</g><g filter="url(#moteGlow)">{near}</g></g>'

def beam(pts, gid, op=1):
    return f'<path d="{P(pts)}" fill="url(#{gid})" opacity="{op}" filter="url(#haze)" style="mix-blend-mode:screen"/>'

def veins(seed, n, box_, col='#ffffff', op=.35, w=1.0):
    r = random.Random(seed); x0, y0, x1, y1 = box_; o = []
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); L = r.uniform(60, 180)
        o.append(f'<path d="M{fx(x)},{fx(y)} c{fx(L * .3)},{fx(r.uniform(-12, 12))} {fx(L * .6)},{fx(r.uniform(-18, 18))} {fx(L)},{fx(r.uniform(-10, 24))}" stroke="{col}" stroke-width="{fx(r.uniform(.5, 1.6) * w)}" fill="none" opacity="{op}"/>')
    return ''.join(o)

def city(x0, x1, ybase, seed, cols=('#8a80bd', '#7a70ae', '#6c63a0'), lit='#ffeedd', maxh=120):
    r = random.Random(seed); o = []
    for layer, col in enumerate(cols):
        x = x0 - 10
        while x < x1:
            w = r.uniform(14, 34); h = r.uniform(.25, 1.0) * maxh * (1 - layer * .18)
            o.append(f'<rect x="{fx(x)}" y="{fx(ybase - h)}" width="{fx(w)}" height="{fx(h + 2)}" fill="{col}"/>')
            if layer == len(cols) - 1 or r.random() < .5:
                for yy in range(int(ybase - h + 6), int(ybase - 4), 7):
                    for xx in range(int(x + 3), int(x + w - 4), 6):
                        if r.random() < .35:
                            o.append(f'<rect x="{xx}" y="{yy}" width="2.4" height="3.2" fill="{lit}" opacity="{r.uniform(.45, .95):.2f}"/>')
            x += w + r.uniform(1, 6)
    return ''.join(o)

def drape(x, ytop, ybot, w, col, side_=1, tie=.62, folds=5):
    """ผ้าม่านหนาแบบรวบ side_=1 รวบไปทางขวา"""
    yt = ytop + (ybot - ytop) * tie
    if side_ == 1:
        d = f'M{fx(x)},{fx(ytop)} L{fx(x + w)},{fx(ytop)} C{fx(x + w * .55)},{fx(yt - 40)} {fx(x + w * .25)},{fx(yt - 6)} {fx(x + w * .22)},{fx(yt)} C{fx(x + w * .12)},{fx(yt + 40)} {fx(x + w * .5)},{fx(ybot - 30)} {fx(x + w * .7)},{fx(ybot)} L{fx(x)},{fx(ybot)}Z'
    else:
        d = f'M{fx(x + w)},{fx(ytop)} L{fx(x)},{fx(ytop)} C{fx(x + w * .45)},{fx(yt - 40)} {fx(x + w * .75)},{fx(yt - 6)} {fx(x + w * .78)},{fx(yt)} C{fx(x + w * .88)},{fx(yt + 40)} {fx(x + w * .5)},{fx(ybot - 30)} {fx(x + w * .3)},{fx(ybot)} L{fx(x + w)},{fx(ybot)}Z'
    o = [softsh(d, 5, 6, .3), path(d, col)]
    cid = f'dr{abs(hash((x, ytop, w))) % 99999}'
    o.append(f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">')
    for i in range(folds):
        t = (i + .5) / folds
        xx = x + w * t if side_ == 1 else x + w * (1 - t)
        o.append(f'<path d="M{fx(xx)},{fx(ytop)} C{fx(xx - (xx - x - w * .22) * .5 if side_ == 1 else xx)},{fx(yt - 20)} {fx(x + w * .22 if side_ == 1 else x + w * .78)},{fx(yt)} {fx(x + w * .22 if side_ == 1 else x + w * .78)},{fx(yt)} L{fx(xx + 200 * side_ * 0)},{fx(ybot + 10)}" stroke="{shade(col, .3)}" stroke-width="{fx(w / folds * .35)}" fill="none" opacity=".55"/>')
    # ขอบรับแสงด้านซ้าย
    o.append(f'<rect x="{fx(x if side_ == 1 else x)}" y="{fx(ytop)}" width="{fx(w * .14)}" height="{fx(ybot - ytop)}" fill="{light(col, .35)}" opacity=".55"/></g>')
    o.append(f'<rect x="{fx((x + w * .22 if side_ == 1 else x + w * .78) - 7)}" y="{fx(yt - 4)}" width="14" height="8" rx="3" fill="#e8cf9c"/>')
    return ''.join(o)

def sheer(x, y0, y1, w, op=.35):
    o = [f'<rect x="{fx(x)}" y="{fx(y0)}" width="{fx(w)}" height="{fx(y1 - y0)}" fill="#fbf5ff" opacity="{op}"/>']
    for i in range(int(w // 9)):
        o.append(f'<rect x="{fx(x + i * 9 + 3)}" y="{fx(y0)}" width="3" height="{fx(y1 - y0)}" fill="#ffffff" opacity="{op * .6:.2f}"/>')
    return ''.join(o)

def arch_d(x0, x1, ytop, ybot):
    w = x1 - x0; r = w / 2
    return f'M{fx(x0)},{fx(ybot)} L{fx(x0)},{fx(ytop + r)} A{fx(r)},{fx(r)} 0 0,1 {fx(x1)},{fx(ytop + r)} L{fx(x1)},{fx(ybot)}Z'

def arch_window(uid, x0, x1, ytop, ybot, seed, sky='skyDusk', frame='#f7f1f6', citymax=110, bars=True):
    w = x1 - x0; o = []
    o.append(softsh(arch_d(x0 - 8, x1 + 8, ytop - 8, ybot + 4), 6, 8, .3))
    o.append(path(arch_d(x0 - 8, x1 + 8, ytop - 8, ybot + 4), frame))
    o.append(path(arch_d(x0 - 8, x1 + 8, ytop - 8, ybot + 4), '#e8cf9c', 'opacity=".0"'))
    o.append(f'<clipPath id="{uid}"><path d="{arch_d(x0, x1, ytop, ybot)}"/></clipPath>')
    o.append(f'<g clip-path="url(#{uid})"><rect x="{fx(x0)}" y="{fx(ytop)}" width="{fx(w)}" height="{fx(ybot - ytop)}" fill="url(#{sky})"/>')
    o.append(f'<g filter="url(#blur1)">{city(x0, x1, ybot, seed, maxh=citymax)}</g>')
    o.append(f'<path d="M{fx(x0)},{fx(ybot)} L{fx(x0 + w * .55)},{fx(ytop)} L{fx(x0 + w * .75)},{fx(ytop)} L{fx(x0 + w * .2)},{fx(ybot)}Z" fill="#fff" opacity=".10"/></g>')
    if bars:
        r = w / 2; cx = (x0 + x1) / 2; cyA = ytop + r
        for i in (1, 2):
            xx = x0 + w * i / 3
            o.append(f'<rect x="{fx(xx - 1.5)}" y="{fx(cyA - math.sqrt(max(0, r * r - (xx - cx) ** 2)))}" width="3" height="{fx(ybot - cyA + math.sqrt(max(0, r * r - (xx - cx) ** 2)))}" fill="{frame}"/>')
        yy = cyA
        while yy < ybot - 10:
            o.append(f'<rect x="{fx(x0)}" y="{fx(yy - 1.5)}" width="{fx(w)}" height="3" fill="{frame}"/>')
            yy += (ybot - cyA) / 3
        o.append(f'<path d="{arch_d(x0, x1, ytop, ybot)}" fill="none" stroke="{shade(frame, .25)}" stroke-width="2"/>')
    return ''.join(o)

def texture(op_st=.17):
    return (f'<rect width="540" height="960" filter="url(#stipple)" opacity="{op_st}" style="mix-blend-mode:overlay"/>'
            f'<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:screen"/>'
            '<rect width="540" height="960" fill="url(#vig)"/>')

def petals(seed, n, c, X0, X1, z0, z1, cols=('#f4bccb', '#fbe3ea', '#e9a4b8', '#ffffff')):
    r = random.Random(seed); o = []
    for i in range(n):
        z = r.uniform(z0, z1); X = r.uniform(X0, X1); x, y = c.p(X, 0, z); k = c.k(z)
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(3.4 * k)}" ry="{fx(1.5 * k)}" transform="rotate({r.uniform(-40, 40):.0f} {fx(x)} {fx(y)})" fill="{r.choice(cols)}" opacity=".95"/>')
    return ''.join(o)

def wainscot(c, X0, X1, z, Y1, col, n):
    """แผงไม้บุผนังล่าง (ผนังหลัง)"""
    o = [path(back(c, X0, X1, 0, Y1, z), col),
         path(back(c, X0, X1, Y1 - 6, Y1, z), light(col, .4)),
         path(back(c, X0, X1, 0, 12, z), shade(col, .2))]
    w = (X1 - X0) / n
    for i in range(n):
        a = X0 + i * w + w * .12; b = X0 + (i + 1) * w - w * .12
        o.append(path(back(c, a, b, 22, Y1 - 18, z), shade(col, .1)))
        o.append(path(back(c, a + 3, b - 3, 25, Y1 - 21, z), col))
        o.append(path(back(c, a, b, Y1 - 21, Y1 - 18, z), light(col, .5)))
    return ''.join(o)

FRN=[0]
def frame_svg(content, label, lc=(.5, .38), dark=.62):
    FRN[0] += 1; g = f'lm{FRN[0]}'
    lm = (f'<radialGradient id="{g}" cx="{lc[0]}" cy="{lc[1]}" r=".85"><stop offset="0" stop-color="#ffffff"/><stop offset=".45" stop-color="#e6d8cc"/><stop offset="1" stop-color="#2e2226"/></radialGradient>'
          f'<rect width="540" height="960" fill="url(#{g})" opacity="{dark}" style="mix-blend-mode:multiply"/>')
    return (f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
            f'<g filter="url(#grade)">{content}</g>{lm}{texture()}<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".75" stroke-dasharray="6 5" stroke-width="1.5"/>'
            f'<text x="270" y="652" text-anchor="middle" font-size="13" fill="#fff" fill-opacity=".8" font-family="IBM Plex Sans Thai, sans-serif">พื้นที่ซับ</text></g></svg>')

# ================================================================ ฉาก 1: โถงหน้าห้องจัดเลี้ยง
def scene_lobby():
    c = Cam(270, 440, 160, 660); ZB = 1000; XL, XR, YC = -380, 380, 540
    o = []
    WALL = '#d2b8a6'; CEIL = '#c4ab98'
    # เพดาน
    o.append(path(c.poly([(XL, YC, ZB), (XR, YC, ZB), (XR, YC, 120), (XL, YC, 120)]), CEIL))
    for X in (-380, -190, 0, 190, 380):
        o.append(f'<path d="{c.poly([(X - 6, YC, ZB), (X + 6, YC, ZB), (X + 6, YC, 150), (X - 6, YC, 150)])}" fill="#efe4d6"/>')
    for z in (1000, 820, 660, 540, 440, 360):
        o.append(f'<path d="{c.poly([(XL, YC, z), (XR, YC, z), (XR, YC, z - 14), (XL, YC, z - 14)])}" fill="#efe6f5"/>')
        o.append(f'<path d="{c.poly([(XL, YC, z - 14), (XR, YC, z - 14), (XR, YC, z - 17), (XL, YC, z - 17)])}" fill="#e3cd9e" opacity=".8"/>')
    mx, my = c.p(0, YC, 470)
    o.append(f'<ellipse cx="{fx(mx)}" cy="{fx(my)}" rx="70" ry="18" fill="#f3ecf8"/><ellipse cx="{fx(mx)}" cy="{fx(my)}" rx="54" ry="13" fill="none" stroke="#e3cd9e" stroke-width="2"/><ellipse cx="{fx(mx)}" cy="{fx(my)}" rx="30" ry="7" fill="#e9dff2"/>')
    # ผนังข้าง
    o.append(path(side(c, XL, ZB, 120, 0, YC), '#bfa391'))
    o.append(path(side(c, XR, ZB, 120, 0, YC), '#ad917f'))
    for X, col in ((XL, '#6e4a3a'), (XR, '#62402f')):
        o.append(path(side(c, X, ZB, 120, 0, 95), col))
        o.append(path(side(c, X, ZB, 120, 95, 102), '#efe5f5'))
        o.append(path(side(c, X, ZB, 120, YC - 30, YC), '#efe6f5'))
    # ผนังหลัง
    o.append(path(back(c, XL, XR, 0, YC, ZB), WALL))
    o.append(f'<path d="{back(c, XL, XR, 110, YC - 30, ZB)}" fill="url(#damask)"/>')
    o.append(wainscot(c, XL, XR, ZB, 105, '#7a4e3c', 8))
    o.append(path(back(c, XL, XR, YC - 32, YC, ZB), '#f6eff8'))
    o.append(path(back(c, XL, XR, YC - 36, YC - 32, ZB), '#e3cd9e'))
    for X in (-330, -200, 200, 330):
        o.append(path(back(c, X - 18, X + 18, 0, YC - 36, ZB), '#f4eef6'))
        o.append(path(back(c, X + 8, X + 18, 0, YC - 36, ZB), '#ddd0e8'))
        o.append(path(back(c, X - 22, X + 22, YC - 60, YC - 36, ZB), '#f8f3fa'))
        o.append(path(back(c, X - 22, X + 22, 0, 18, ZB), '#e8dcee'))
    # ประตูใหญ่ห้องจัดเลี้ยง
    x0, yb = c.p(-150, 0, ZB); x1, yt = c.p(150, 290, ZB)
    ax0, _ = c.p(-176, 0, ZB); ax1, at = c.p(176, 316, ZB)
    o.append(softsh(arch_d(ax0, ax1, at - (ax1 - ax0) / 2 + 0, yb), 6, 8, .35))
    o.append(path(arch_d(ax0, ax1, at - (ax1 - ax0) / 2, yb), '#f8f2f8'))
    o.append(path(arch_d(ax0 + 4, ax1 - 4, at - (ax1 - ax0) / 2 + 4, yb), '#e6cf9f'))
    o.append(path(arch_d(x0, x1, yt - (x1 - x0) / 2, yb), '#bfa9cf'))
    tr_top = yt - (x1 - x0) / 2
    o.append(f'<clipPath id="lbT"><path d="{arch_d(x0, x1, tr_top, yt)}"/></clipPath><g clip-path="url(#lbT)"><rect x="{fx(x0)}" y="{fx(tr_top)}" width="{fx(x1 - x0)}" height="{fx(yt - tr_top)}" fill="#fff4ec"/>')
    cxT = (x0 + x1) / 2
    for i in range(9):
        a = math.pi * (i + 1) / 10
        o.append(f'<path d="M{fx(cxT)},{fx(yt)} L{fx(cxT - math.cos(a) * 120)},{fx(yt - math.sin(a) * 120)}" stroke="#e3cd9e" stroke-width="2"/>')
    o.append(f'<circle cx="{fx(cxT)}" cy="{fx(yt)}" r="16" fill="#e8d2a4"/></g>')
    o.append(f'<circle cx="{fx(cxT)}" cy="{fx(yt - 10)}" r="70" fill="url(#chGlow)"/>')
    dw = (x1 - x0) / 2
    for i, (lx, col, sh) in enumerate(((x0, '#fbf6fa', '#e3d6ea'), (x0 + dw, '#f4edf6', '#ddd0e6'))):
        o.append(f'<rect x="{fx(lx + 1)}" y="{fx(yt)}" width="{fx(dw - 2)}" height="{fx(yb - yt)}" fill="{col}"/>')
        for (py0, py1) in ((yt + 10, yt + (yb - yt) * .45), (yt + (yb - yt) * .5, yb - 10)):
            o.append(f'<rect x="{fx(lx + 10)}" y="{fx(py0)}" width="{fx(dw - 20)}" height="{fx(py1 - py0)}" fill="{sh}"/>')
            o.append(f'<rect x="{fx(lx + 12)}" y="{fx(py0 + 2)}" width="{fx(dw - 24)}" height="{fx(py1 - py0 - 4)}" fill="{col}" stroke="#e3cd9e" stroke-width="1.4"/>')
        hx = lx + dw - 8 if i == 0 else lx + 8
        o.append(f'<rect x="{fx(hx - 2)}" y="{fx(yt + (yb - yt) * .4)}" width="4" height="34" rx="2" fill="#d9bb82"/>')
    o.append(f'<rect x="{fx(x0 + dw - 1)}" y="{fx(yt)}" width="2" height="{fx(yb - yt)}" fill="#fff7ea"/>')
    o.append(f'<rect x="{fx(x0)}" y="{fx(yb - 2)}" width="{fx(x1 - x0)}" height="3" fill="#fff6e8" filter="url(#glow)"/>')
    sx, sy = c.p(0, 486, ZB)
    o.append(f'<rect x="{fx(sx - 62)}" y="{fx(sy - 9)}" width="124" height="18" rx="2" fill="#f8f2f8" stroke="#e3cd9e"/><text x="{fx(sx)}" y="{fx(sy + 4)}" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="11" letter-spacing="3" fill="#a88a5c">GRAND BALLROOM</text>')
    # ไฟผนัง
    for X in (-265, 265):
        x, y = c.p(X, 250, ZB); o.append(sconce(x, y, .8))
    # แท่นดอกไม้สองข้างประตู
    for X in (-255, 255):
        z0, z1 = 950, 990
        o.append(fshadow(c, X - 22, X + 22, z0, z1))
        o.append(box(c, X - 22, X + 22, 0, 110, z0, z1, '#fbf7fb', '#efe7f3', '#ddd0e7'))
        o.append(box(c, X - 28, X + 28, 104, 116, z0 - 4, z1 + 4, '#ffffff', '#f6f0f8', '#e3d8ec'))
        x, y = c.p(X, 140, z0); k = c.k(z0)
        o.append(flowers(x, y, 42 * k, 30 * k, 11 + X, 70, .95, trail=7))
    # กระจกและโต๊ะคอนโซลผนังซ้าย
    o.append(path(side(c, XL, 900, 640, 120, 320), '#e3cd9e'))
    o.append(path(side(c, XL + .1, 890, 650, 130, 310), '#c7bcdc'))
    o.append(path(c.poly([(XL, 140, 870), (XL, 300, 760), (XL, 300, 730), (XL, 140, 840)]), '#ffffff', 'opacity=".25"'))
    o.append(fshadow(c, XL, XL + 45, 660, 880, 18, 10))
    o.append(box(c, XL, XL + 45, 80, 88, 660, 880, '#f8f3f8', '#efe5f2', '#e0d3ea'))
    for zz in (680, 860):
        o.append(box(c, XL + 30, XL + 38, 0, 80, zz - 6, zz, '#e3cd9e', '#d6b985', '#c7a874'))
    for zz in (700, 840):
        x, y = c.p(XL + 22, 88, zz); k = c.k(zz)
        o.append(f'<rect x="{fx(x - 2 * k)}" y="{fx(y - 34 * k)}" width="{fx(4 * k)}" height="{fx(34 * k)}" fill="#d9bb82"/><rect x="{fx(x - 2.5 * k)}" y="{fx(y - 52 * k)}" width="{fx(5 * k)}" height="{fx(18 * k)}" fill="#fff8f0"/><circle cx="{fx(x)}" cy="{fx(y - 56 * k)}" r="{fx(3 * k)}" fill="#fffaf0" filter="url(#glow)"/><circle cx="{fx(x)}" cy="{fx(y - 56 * k)}" r="{fx(22 * k)}" fill="url(#chGlow)"/>')
    x, y = c.p(XL + 22, 88, 770); k = c.k(770)
    o.append(f'<path d="M{fx(x - 8 * k)},{fx(y)} l{fx(-3 * k)},{fx(-26 * k)} h{fx(22 * k)} l{fx(-3 * k)},{fx(26 * k)}Z" fill="#f2edf6"/>')
    o.append(flowers(x, y - 38 * k, 20 * k, 15 * k, 77, 26, .8 * k))
    # ม้านั่งกำมะหยี่ผนังขวา
    o.append(fshadow(c, XR - 60, XR, 640, 860, 14, 10))
    o.append(box(c, XR - 60, XR, 0, 46, 640, 860, '#8e3e4e', '#7a3242', '#682a38'))
    for zz in (660, 750, 840):
        x, y = c.p(XR - 30, 46, zz); k = c.k(zz)
        o.append(f'<circle cx="{fx(x)}" cy="{fx(y)}" r="{fx(1.6 * k)}" fill="#8e76aa"/>')
    # ขาตั้งป้ายต้อนรับ
    X, z = 165, 760
    o.append(fshadow(c, X - 30, X + 30, z - 20, z + 10, 24, 20, .3))
    ax, ay = c.p(X, 0, z); k = c.k(z)
    o.append(f'<path d="M{fx(ax - 22 * k)},{fx(ay)} L{fx(ax)},{fx(ay - 160 * k)} L{fx(ax + 22 * k)},{fx(ay)}" stroke="#cfae78" stroke-width="{fx(3 * k)}" fill="none"/>')
    bx0, by0 = ax - 34 * k, ay - 150 * k
    o.append(f'<rect x="{fx(bx0 + 3)}" y="{fx(by0 + 4)}" width="{fx(68 * k)}" height="{fx(90 * k)}" fill="#3a2a28" opacity=".25" filter="url(#soft)"/>')
    o.append(f'<rect x="{fx(bx0)}" y="{fx(by0)}" width="{fx(68 * k)}" height="{fx(90 * k)}" fill="#fffbf8" stroke="#e3cd9e" stroke-width="{fx(1.4 * k)}"/>')
    o.append(f'<rect x="{fx(bx0 + 5 * k)}" y="{fx(by0 + 5 * k)}" width="{fx(58 * k)}" height="{fx(80 * k)}" fill="none" stroke="#ead8b2" stroke-width="{fx(.7 * k)}"/>')
    o.append(f'<text x="{fx(ax)}" y="{fx(by0 + 34 * k)}" text-anchor="middle" font-family="Cormorant Garamond, serif" font-style="italic" font-size="{fx(11 * k)}" fill="#8f7aa8">Welcome</text>')
    o.append(f'<text x="{fx(ax)}" y="{fx(by0 + 48 * k)}" text-anchor="middle" font-family="Cormorant Garamond, serif" font-size="{fx(5.2 * k)}" letter-spacing="1.5" fill="#a88a5c">TO OUR WEDDING</text>')
    o.append(f'<path d="M{fx(ax - 14 * k)},{fx(by0 + 58 * k)} h{fx(28 * k)}" stroke="#e3cd9e" stroke-width="{fx(.7 * k)}"/>')
    o.append(flowers(bx0 + 6 * k, by0 + 4 * k, 12 * k, 8 * k, 91, 14, .55 * k, trail=3))
    # พื้นหินอ่อนลายตาราง
    T = 80; tiles = []
    zs = [ZB]
    while zs[-1] > 140: zs.append(zs[-1] - T)
    for j in range(len(zs) - 1):
        for i, X in enumerate(range(XL, XR, T)):
            col = '#f0e6da' if (i + j) % 2 == 0 else '#4a3532'
            tiles.append(path(flat(c, X, X + T, zs[j + 1], zs[j], 0), col))
    o.insert(0, '')
    floor_d = flat(c, XL, XR, 120, ZB, 0)
    o.append(f'<clipPath id="lbF"><path d="{floor_d}"/></clipPath><g clip-path="url(#lbF)">{"".join(tiles)}{veins(5, 60, (0, 480, 540, 960), "#ffffff", .45)}{veins(6, 30, (0, 480, 540, 960), "#bfaed0", .35)}')
    # พรมทางเดิน
    o.append(path(flat(c, -112, 112, 120, ZB, 0), '#9c3f5e'))
    o.append(path(flat(c, -100, 100, 120, ZB, 0), '#bf5a78'))
    o.append(path(flat(c, -112, -104, 120, ZB, 0), '#e3cd9e'))
    o.append(path(flat(c, 104, 112, 120, ZB, 0), '#e3cd9e'))
    o.append(f'<path d="{flat(c, -150, 150, 900, ZB, 0)}" fill="#fff4ea" opacity=".45" filter="url(#haze)"/>')
    # สะท้อนบนพื้น
    o.append(f'<ellipse cx="{fx(c.p(0, 0, 700)[0])}" cy="{fx(c.p(0, 0, 700)[1])}" rx="120" ry="30" fill="#ffffff" opacity=".18" filter="url(#haze)"/></g>')
    # โคมระย้ากลางโถง
    x, y = c.p(0, 400, 470); o.append(chandelier(x, y, c.k(470) * 1.0, 3))
    o.append(beam([(x - 30, y + 60), (x + 30, y + 60), (x + 180, 900), (x - 180, 900)], 'beamW', .55))
    o.append(dust(31, (x - 160, y + 80, x + 160, 860), 34))
    # ฉากหน้าเบลอ: แจกันดอกไม้มุมซ้ายล่าง
    o.append(f'<g filter="url(#blur3)">{flowers(30, 900, 90, 70, 401, 70, 2.4, trail=6)}</g>')
    o.append(f'<path d="M0,0 L540,0 L540,200 L0,260Z" fill="#3a2a55" opacity=".10"/>')
    return frame_svg(''.join(o), 'โถงหน้าห้องจัดเลี้ยงของโรงแรมหรู ประตูบานคู่สีขาวขอบทอง แท่นดอกไม้สองข้าง ป้ายต้อนรับ โคมระย้า พื้นหินอ่อนลายตาราง และพรมทางเดินสีกุหลาบเข้ม', (.5, .36))

# ================================================================ ฉาก 2: ห้องจัดเลี้ยง พิธีแต่งงาน
def chair_back(c, X, z, sash=True):
    x, y = c.p(X, 0, z); k = c.k(z)
    W, S, T = 44 * k, 46 * k, 94 * k
    o = [f'<ellipse cx="{fx(x + 8 * k)}" cy="{fx(y + 2 * k)}" rx="{fx(W * .7)}" ry="{fx(5 * k)}" fill="#3a2a28" opacity=".22" filter="url(#soft)"/>']
    L = x - W / 2; R = x + W / 2
    o.append(f'<rect x="{fx(L + 1 * k)}" y="{fx(y - S)}" width="{fx(W - 2 * k)}" height="{fx(4 * k)}" fill="#f6efe6"/>')
    for lx in (L, R - 3.4 * k):
        o.append(f'<rect x="{fx(lx)}" y="{fx(y - T)}" width="{fx(3.4 * k)}" height="{fx(T)}" fill="#e4c690"/>')
    o.append(f'<rect x="{fx(R - 3.4 * k)}" y="{fx(y - T)}" width="{fx(1.4 * k)}" height="{fx(T)}" fill="#b8955e"/>')
    for yy in (T, T - 22 * k, S + 12 * k):
        o.append(f'<rect x="{fx(L)}" y="{fx(y - yy)}" width="{fx(W)}" height="{fx(3 * k)}" fill="#e4c690"/>')
    for i in range(1, 5):
        sx = L + W * i / 5
        o.append(f'<rect x="{fx(sx - .8 * k)}" y="{fx(y - T + 22 * k)}" width="{fx(1.6 * k)}" height="{fx(T - S - 34 * k)}" fill="#d6b67c"/>')
    o.append(f'<rect x="{fx(L + 6 * k)}" y="{fx(y - S + 4 * k)}" width="{fx(2 * k)}" height="{fx(S - 4 * k)}" fill="#c9a76c"/><rect x="{fx(R - 8 * k)}" y="{fx(y - S + 4 * k)}" width="{fx(2 * k)}" height="{fx(S - 4 * k)}" fill="#b8955e"/>')
    if sash:
        by = y - T + 30 * k
        o.append(f'<path d="M{fx(L)},{fx(by)} Q{fx(x)},{fx(by + 6 * k)} {fx(R)},{fx(by)} L{fx(R)},{fx(by + 7 * k)} Q{fx(x)},{fx(by + 13 * k)} {fx(L)},{fx(by + 7 * k)}Z" fill="#f2cbd8"/>')
        o.append(f'<path d="M{fx(x)},{fx(by + 7 * k)} l{fx(-9 * k)},{fx(-6 * k)} l{fx(-2 * k)},{fx(10 * k)}Z M{fx(x)},{fx(by + 7 * k)} l{fx(9 * k)},{fx(-6 * k)} l{fx(2 * k)},{fx(10 * k)}Z" fill="#eab6c7"/>')
        o.append(f'<path d="M{fx(x - 1 * k)},{fx(by + 8 * k)} q{fx(-4 * k)},{fx(20 * k)} {fx(-7 * k)},{fx(44 * k)} l{fx(5 * k)},{fx(1 * k)} q{fx(2 * k)},{fx(-24 * k)} {fx(4 * k)},{fx(-44 * k)}Z M{fx(x + 1 * k)},{fx(by + 8 * k)} q{fx(5 * k)},{fx(20 * k)} {fx(9 * k)},{fx(40 * k)} l{fx(-5 * k)},{fx(2 * k)} q{fx(-3 * k)},{fx(-22 * k)} {fx(-6 * k)},{fx(-41 * k)}Z" fill="#f4d3de"/>')
        o.append(f'<circle cx="{fx(x)}" cy="{fx(by + 7 * k)}" r="{fx(2.6 * k)}" fill="#e2a9bc"/>')
    return ''.join(o)

def scene_ballroom():
    c = Cam(270, 362, 160, 660); ZB = 1200; YC = 600
    o = []
    WALL = '#d6bcaa'
    # เพดานลายช่อง
    o.append(path(c.poly([(-1400, YC, ZB), (1400, YC, ZB), (1400, YC, 500), (-1400, YC, 500)]), '#c2a894'))
    for X in range(-1400, 1401, 200):
        o.append(f'<path d="{c.poly([(X - 10, YC, ZB), (X + 10, YC, ZB), (X + 10, YC, 500), (X - 10, YC, 500)])}" fill="#efe7f6"/>')
    for z in (1200, 1050, 920, 810):
        o.append(f'<path d="{c.poly([(-1400, YC, z), (1400, YC, z), (1400, YC, z - 22), (-1400, YC, z - 22)])}" fill="#efe7f6"/>')
        o.append(f'<path d="{c.poly([(-1400, YC, z - 22), (1400, YC, z - 22), (1400, YC, z - 26), (-1400, YC, z - 26)])}" fill="#e3cd9e" opacity=".8"/>')
    # ผนังหลัง
    o.append(path(back(c, -1400, 1400, 0, YC, ZB), WALL))
    o.append(f'<path d="{back(c, -1400, 1400, 100, YC - 50, ZB)}" fill="url(#damask)"/>')
    o.append(path(back(c, -1400, 1400, YC - 50, YC, ZB), '#f6f0f8'))
    o.append(path(back(c, -1400, 1400, YC - 56, YC - 50, ZB), '#e3cd9e'))
    o.append(path(back(c, -1400, 1400, YC - 12, YC - 6, ZB), '#e3cd9e'))
    o.append(wainscot(c, -1400, 1400, ZB, 95, '#7a4e3c', 14))
    # หน้าต่างโค้ง
    win = [(-150, 150, 70, 530), (-430, -300, 90, 480), (300, 430, 90, 480)]
    for idx, (a, b, y0, y1) in enumerate(win):
        xa, yb_ = c.p(a, y0, ZB); xb, yt_ = c.p(b, y1, ZB)
        o.append(arch_window(f'bw{idx}', xa, xb, yt_, yb_, 20 + idx, citymax=60 if idx else 90))
        o.append(sheer(xa, yt_ + (xb - xa) / 2 - 10, yb_, xb - xa, .22))
        w = (xb - xa)
        o.append(drape(xa - w * .18, yt_ + w * .25, yb_ + 6, w * .42, '#a84a6c', 1))
        o.append(drape(xb - w * .24, yt_ + w * .25, yb_ + 6, w * .42, '#a84a6c', -1))
        o.append(f'<path d="M{fx(xa - w * .2)},{fx(yt_ + w * .22)} Q{fx((xa + xb) / 2)},{fx(yt_ + w * .42)} {fx(xb + w * .2)},{fx(yt_ + w * .22)} L{fx(xb + w * .2)},{fx(yt_ + w * .12)} Q{fx((xa + xb) / 2)},{fx(yt_ + w * .3)} {fx(xa - w * .2)},{fx(yt_ + w * .12)}Z" fill="#b9587a"/>')
    for X in (-235, 235, -490, 490):
        o.append(path(back(c, X - 22, X + 22, 0, YC - 56, ZB), '#f5f0f8'))
        o.append(path(back(c, X + 10, X + 22, 0, YC - 56, ZB), '#dfd2ea'))
        o.append(path(back(c, X - 26, X + 26, YC - 86, YC - 56, ZB), '#f9f5fb'))
        x, y = c.p(X, 330, ZB); o.append(sconce(x, y, .62))
    # เวที
    o.append(box(c, -420, 420, 0, 36, 1020, ZB, '#f8f2f6', '#efe5ef', '#e2d6e9'))
    o.append(path(back(c, -420, 420, 30, 36, 1020), '#e3cd9e'))
    o.append(box(c, -130, 130, 0, 18, 975, 1020, '#f6eff5', '#ebe0ec', '#ddd1e6'))
    # ซุ้มดอกไม้
    zA = 1110; R_ = 165; base = 36
    pts = []
    for i in range(46):
        t = math.pi * i / 45
        X = -math.cos(t) * R_; Y = base + 200 + math.sin(t) * R_
        if t < .02 or t > math.pi - .02: pass
        pts.append(c.p(X, Y, zA))
    for X in (-R_, R_):
        for Y in range(base, base + 200, 20):
            pts.append(c.p(X, Y, zA))
    xL, yL = c.p(-R_, base, zA); xR, yR = c.p(R_, base, zA)
    _, yTop = c.p(0, base + 200 + R_, zA)
    for X in (-R_, R_):
        x0, y0 = c.p(X - 4, base, zA); x1, y1 = c.p(X + 4, base + 360, zA)
        o.append(f'<rect x="{fx(x0)}" y="{fx(y1)}" width="{fx(x1 - x0)}" height="{fx(y0 - y1)}" fill="#efe6f0"/>')
    # ผ้าชีฟองห้อย
    o.append(f'<path d="M{fx(xL)},{fx(yTop + 60)} Q{fx((xL + xR) / 2)},{fx(yTop + 110)} {fx(xR)},{fx(yTop + 60)} L{fx(xR + 6)},{fx(yL)} Q{fx(xR - 10)},{fx(yTop + 140)} {fx(xR - 20)},{fx(yTop + 90)} Q{fx((xL + xR) / 2)},{fx(yTop + 130)} {fx(xL + 20)},{fx(yTop + 90)} Q{fx(xL + 10)},{fx(yTop + 140)} {fx(xL - 6)},{fx(yL)}Z" fill="#fbf4fa" opacity=".75"/>')
    k = c.k(zA)
    r = random.Random(4)
    for i, (x, y) in enumerate(pts):
        if i % 2 == 0:
            o.append(flowers(x, y, 13 * k * 1.7, 10 * k * 1.7, 300 + i, 9, .55, trail=1 if r.random() < .25 else 0))
    for X in (-R_, R_):
        x, y = c.p(X, base + 30, zA)
        o.append(flowers(x, y, 60 * k, 40 * k, 500 + X, 46, .75, trail=6))
    # เชิงเทียนบนเวที
    for X in (-300, 300):
        x, y = c.p(X, 36, 1100); kk = c.k(1100)
        o.append(f'<path d="M{fx(x - 10 * kk)},{fx(y)} h{fx(20 * kk)} l{fx(-7 * kk)},{fx(-12 * kk)} v{fx(-120 * kk)} h{fx(-6 * kk)} v{fx(120 * kk)}Z" fill="#dcbf8a"/>')
        for d in (-1, 0, 1):
            cx_ = x + d * 22 * kk; cy_ = y - 140 * kk - (8 * kk if d == 0 else 0)
            o.append(f'<path d="M{fx(x)},{fx(y - 120 * kk)} Q{fx(cx_)},{fx(y - 122 * kk)} {fx(cx_)},{fx(cy_ + 14 * kk)}" stroke="#dcbf8a" stroke-width="{fx(2 * kk)}" fill="none"/>')
            o.append(f'<rect x="{fx(cx_ - 2.5 * kk)}" y="{fx(cy_)}" width="{fx(5 * kk)}" height="{fx(16 * kk)}" fill="#fff8ef"/><circle cx="{fx(cx_)}" cy="{fx(cy_ - 3 * kk)}" r="{fx(2.4 * kk)}" fill="#fffaf0" filter="url(#glow)"/>')
        o.append(f'<circle cx="{fx(x)}" cy="{fx(y - 140 * kk)}" r="{fx(60 * kk)}" fill="url(#chGlow)"/>')
    # พื้นหินอ่อน + พรมทางเดิน
    floor_d = flat(c, -1400, 1400, 150, 1020, 0)
    o.append(path(floor_d, '#dccbbd'))
    o.append(f'<clipPath id="brF"><path d="{floor_d}"/></clipPath><g clip-path="url(#brF)">')
    for X in range(-1400, 1401, 120):
        o.append(f'<path d="{c.poly([(X - 1, 0, 1020), (X + 1, 0, 1020), (X + 1, 0, 150), (X - 1, 0, 150)])}" fill="#c8b4a2"/>')
    for z in (1020, 880, 760, 655, 565, 488, 420, 360, 310, 268, 230, 198, 170):
        o.append(f'<path d="{c.poly([(-1400, 0, z), (1400, 0, z), (1400, 0, z - 2), (-1400, 0, z - 2)])}" fill="#c8b4a2"/>')
    o.append(veins(8, 70, (0, 450, 540, 960), '#ffffff', .5))
    o.append(veins(9, 30, (0, 450, 540, 960), '#b49c88', .3))
    o.append(path(flat(c, -92, 92, 150, 1020, 0), '#9c3f5e'))
    o.append(path(flat(c, -82, 82, 150, 1020, 0), '#c25f7d'))
    o.append(f'<path d="{flat(c, -82, 0, 150, 1020, 0)}" fill="#d9809a" opacity=".45"/>')
    o.append(petals(12, 160, c, -80, 80, 160, 1000))
    o.append(f'<ellipse cx="270" cy="470" rx="140" ry="22" fill="#fff" opacity=".22" filter="url(#haze)"/></g>')
    # เก้าอี้แขก (มองจากด้านหลัง)
    rows = [960, 880, 800, 725, 655, 590, 530, 475, 425, 380, 340]
    pedestals = []
    for zi, z in enumerate(rows):
        row = []
        for side_ in (-1, 1):
            X = 150
            while True:
                x, _ = c.p(side_ * X, 0, z)
                if x < -60 or x > 600: break
                row.append(chair_back(c, side_ * X, z))
                X += 58
        o.append(''.join(row))
        if zi % 2 == 0:
            for side_ in (-1, 1):
                X = side_ * 108
                x, y = c.p(X, 0, z - 20); kk = c.k(z - 20)
                o.append(f'<ellipse cx="{fx(x + 8 * kk)}" cy="{fx(y + 2 * kk)}" rx="{fx(14 * kk)}" ry="{fx(4 * kk)}" fill="#3a2a28" opacity=".25" filter="url(#soft)"/>')
                o.append(f'<path d="M{fx(x - 9 * kk)},{fx(y)} h{fx(18 * kk)} l{fx(-4 * kk)},{fx(-10 * kk)} v{fx(-62 * kk)} l{fx(5 * kk)},{fx(-8 * kk)} h{fx(-20 * kk)} l{fx(5 * kk)},{fx(8 * kk)} v{fx(62 * kk)}Z" fill="#f6f0f8"/>')
                o.append(f'<path d="M{fx(x + 1 * kk)},{fx(y - 10 * kk)} v{fx(-62 * kk)} h{fx(4 * kk)} v{fx(62 * kk)}Z" fill="#ddd0e8"/>')
                o.append(flowers(x, y - 88 * kk, 22 * kk, 17 * kk, 700 + zi * 3 + side_, 22, .55 * kk, trail=3))
    # โคมระย้า
    for X, z, s, Y in ((-430, 1000, .85, 500), (430, 1000, .85, 500), (0, 640, 1.2, 470)):
        x, y = c.p(X, Y, z)
        o.append(chandelier(x, y, c.k(z) * s, 7 + X))
    x, y = c.p(0, 470, 640)
    o.append(beam([(x - 34, y + 70), (x + 34, y + 70), (x + 210, 860), (x - 210, 860)], 'beamW', .5))
    # แสงสนธยาจากหน้าต่างกลาง
    xa, ya = c.p(-150, 300, ZB); xb, _ = c.p(150, 300, ZB)
    o.append(beam([(xa, ya - 80), (xb, ya - 80), (xb + 160, 760), (xa - 40, 760)], 'beamP', .45))
    o.append(dust(41, (100, 260, 460, 760), 46))
    # ฉากหน้าเบลอ
    o.append(f'<g filter="url(#blur3)">{flowers(-10, 880, 80, 90, 801, 60, 2.6, trail=6)}{flowers(555, 900, 80, 90, 802, 60, 2.6, trail=6)}</g>')
    return frame_svg(''.join(o), 'ห้องจัดเลี้ยงในโรงแรมหรู ซุ้มดอกไม้สีขาวบนเวที หน้าต่างโค้งเห็นฟ้าสนธยาสีม่วงชมพู โคมระย้าคริสตัล เก้าอี้แขกสีขาวผูกโบว์ชมพู และพรมทางเดินโรยกลีบกุหลาบ')

# ================================================================ ฉาก 3: ห้องแต่งตัวเจ้าสาว
def scene_dressing():
    c = Cam(260, 330, 160, 700); ZB = 350; YC = 290
    o = []
    WALL = '#dcbcae'
    o.append(path(c.poly([(-300, YC, ZB), (300, YC, ZB), (300, YC, 90), (-300, YC, 90)]), '#cdb0a0'))
    o.append(path(c.poly([(-300, YC, ZB), (300, YC, ZB), (300, YC, ZB - 30), (-300, YC, ZB - 30)]), '#f7eef4'))
    o.append(path(c.poly([(-300, YC, ZB - 30), (300, YC, ZB - 30), (300, YC, ZB - 34), (-300, YC, ZB - 34)]), '#e3cd9e'))
    o.append(path(back(c, -300, 300, 0, YC, ZB), WALL))
    o.append(f'<path d="{back(c, -300, 300, 92, YC - 22, ZB)}" fill="url(#damask)"/>')
    o.append(path(back(c, -300, 300, YC - 22, YC, ZB), '#f9f1f6'))
    o.append(path(back(c, -300, 300, YC - 25, YC - 22, ZB), '#e3cd9e'))
    o.append(wainscot(c, -300, 300, ZB, 88, '#f1e4d8', 5))
    # หน้าต่าง
    xa, yb_ = c.p(25, 70, ZB); xb, yt_ = c.p(140, 250, ZB)
    o.append(f'<rect x="{fx(xa - 10)}" y="{fx(yt_ - 10)}" width="{fx(xb - xa + 20)}" height="{fx(yb_ - yt_ + 22)}" fill="#fbf6f8"/>')
    o.append(f'<rect x="{fx(xa - 14)}" y="{fx(yb_ + 8)}" width="{fx(xb - xa + 28)}" height="8" fill="#f2e6ee"/>')
    o.append(f'<rect x="{fx(xa)}" y="{fx(yt_)}" width="{fx(xb - xa)}" height="{fx(yb_ - yt_)}" fill="url(#skyDusk)"/>')
    o.append(f'<clipPath id="drW"><rect x="{fx(xa)}" y="{fx(yt_)}" width="{fx(xb - xa)}" height="{fx(yb_ - yt_)}"/></clipPath><g clip-path="url(#drW)" filter="url(#blur1)">{city(xa, xb, yb_, 61, maxh=150)}</g>')
    o.append(f'<path d="M{fx(xa)},{fx(yb_)} L{fx(xa + 90)},{fx(yt_)} L{fx(xa + 130)},{fx(yt_)} L{fx(xa + 30)},{fx(yb_)}Z" fill="#fff" opacity=".12"/>')
    for t in (1 / 3, 2 / 3):
        o.append(f'<rect x="{fx(xa + (xb - xa) * t - 2)}" y="{fx(yt_)}" width="4" height="{fx(yb_ - yt_)}" fill="#fbf6f8"/>')
    for t in (.25, .5, .75):
        o.append(f'<rect x="{fx(xa)}" y="{fx(yt_ + (yb_ - yt_) * t - 2)}" width="{fx(xb - xa)}" height="4" fill="#fbf6f8"/>')
    o.append(sheer(xa - 6, yt_ - 30, yb_ + 30, 46, .38))
    o.append(drape(xa - 70, yt_ - 40, yb_ + 140, 90, '#8e3e4e', 1, .55))
    o.append(drape(xb - 30, yt_ - 40, yb_ + 140, 90, '#8e3e4e', -1, .55))
    o.append(f'<rect x="{fx(xa - 80)}" y="{fx(yt_ - 46)}" width="{fx(xb - xa + 170)}" height="8" rx="4" fill="#e3cd9e"/>')
    # พื้นพรมกับพรมวงรี
    floor_d = flat(c, -300, 300, 120, ZB, 0)
    o.append(path(floor_d, '#9c8072'))
    o.append(f'<clipPath id="drF"><path d="{floor_d}"/></clipPath><g clip-path="url(#drF)">')
    for X in range(-300, 301, 18):
        o.append(f'<path d="{c.poly([(X, 0, ZB), (X + 9, 0, ZB), (X + 9, 0, 120), (X, 0, 120)])}" fill="#8f7466" opacity=".6"/>')
    ex, ey = c.p(-30, 0, 230); kk = c.k(230)
    o.append(f'<ellipse cx="{fx(ex)}" cy="{fx(ey)}" rx="{fx(150 * kk)}" ry="{fx(42 * kk)}" fill="#ead2c4"/><ellipse cx="{fx(ex)}" cy="{fx(ey)}" rx="{fx(136 * kk)}" ry="{fx(36 * kk)}" fill="none" stroke="#e7c6d6" stroke-width="{fx(5 * kk)}"/><ellipse cx="{fx(ex)}" cy="{fx(ey)}" rx="{fx(110 * kk)}" ry="{fx(28 * kk)}" fill="none" stroke="#efd6e2" stroke-width="{fx(2 * kk)}" stroke-dasharray="6 5"/>')
    o.append('</g>')
    # โต๊ะเครื่องแป้ง
    VX0, VX1, VZ0, VZ1 = -140, -15, 305, ZB
    mx0, my0 = c.p(-132, 225, ZB); mx1, my1 = c.p(-23, 100, ZB)
    o.append(softsh(P([(mx0 - 12, my0 - 12), (mx1 + 12, my0 - 12), (mx1 + 12, my1 + 6), (mx0 - 12, my1 + 6)]), 6, 8, .3))
    o.append(f'<rect x="{fx(mx0 - 12)}" y="{fx(my0 - 12)}" width="{fx(mx1 - mx0 + 24)}" height="{fx(my1 - my0 + 18)}" rx="8" fill="#f9f3f6"/>')
    o.append(f'<rect x="{fx(mx0)}" y="{fx(my0)}" width="{fx(mx1 - mx0)}" height="{fx(my1 - my0)}" rx="4" fill="url(#mirror)"/>')
    o.append(f'<g opacity=".55" filter="url(#blur1)"><rect x="{fx(mx0 + 10)}" y="{fx(my0 + 20)}" width="{fx((mx1 - mx0) * .5)}" height="{fx((my1 - my0) * .8)}" fill="#e8d2e2"/><rect x="{fx(mx0 + (mx1 - mx0) * .55)}" y="{fx(my0 + 30)}" width="30" height="60" fill="#c9a8d0"/></g>')
    o.append(f'<path d="M{fx(mx0)},{fx(my1)} L{fx(mx0 + 40)},{fx(my0)} L{fx(mx0 + 66)},{fx(my0)} L{fx(mx0 + 22)},{fx(my1)}Z" fill="#fff" opacity=".22"/>')
    n = 7
    for i in range(n):
        for (bx, by) in ((mx0 - 6 + (mx1 - mx0 + 12) * i / (n - 1), my0 - 6),):
            o.append(f'<circle cx="{fx(bx)}" cy="{fx(by)}" r="5" fill="#fffaf0" filter="url(#glow)"/><circle cx="{fx(bx)}" cy="{fx(by)}" r="18" fill="url(#chGlow)"/>')
    for i in range(1, 6):
        for bx in (mx0 - 6, mx1 + 6):
            by = my0 - 6 + (my1 - my0 + 6) * i / 5
            o.append(f'<circle cx="{fx(bx)}" cy="{fx(by)}" r="5" fill="#fffaf0" filter="url(#glow)"/><circle cx="{fx(bx)}" cy="{fx(by)}" r="18" fill="url(#chGlow)"/>')
    o.append(fshadow(c, VX0, VX1, VZ0, VZ1, 14, 10, .3))
    for X in (VX0 + 4, VX1 - 8):
        o.append(box(c, X, X + 5, 0, 70, VZ0, VZ0 + 5, '#e3cd9e', '#f3ebf2', '#e0d0e4'))
    o.append(box(c, VX0, VX1, 58, 76, VZ0, VZ1, '#fbf6fa', '#f4eaf2', '#e3d3e7'))
    o.append(path(back(c, VX0, VX1, 58, 60, VZ0), '#e3cd9e'))
    for i in range(3):
        a = VX0 + 6 + i * (VX1 - VX0 - 12) / 3; b = a + (VX1 - VX0 - 12) / 3 - 4
        o.append(path(back(c, a, b, 62, 73, VZ0), '#efe3ed'))
        hx, hy = c.p((a + b) / 2, 67, VZ0)
        o.append(f'<circle cx="{fx(hx)}" cy="{fx(hy)}" r="2" fill="#d9bb82"/>')
    # ของบนโต๊ะ
    def on_table(X, z): return c.p(X, 76, z), c.k(z)
    (x, y), kk = on_table(-125, 330)
    o.append(f'<path d="M{fx(x - 6 * kk)},{fx(y)} l{fx(-2 * kk)},{fx(-22 * kk)} h{fx(16 * kk)} l{fx(-2 * kk)},{fx(22 * kk)}Z" fill="#f2e9f5"/>')
    o.append(flowers(x, y - 30 * kk, 15 * kk, 12 * kk, 66, 20, .7, trail=2))
    for i, (X, h, col) in enumerate(((-100, 14, '#e6c3d9'), (-92, 10, '#c9b6e6'), (-85, 16, '#f2d0dc'))):
        (x, y), kk = on_table(X, 322)
        o.append(f'<rect x="{fx(x - 3 * kk)}" y="{fx(y - h * kk)}" width="{fx(6 * kk)}" height="{fx(h * kk)}" rx="{fx(1.5 * kk)}" fill="{col}"/><rect x="{fx(x - 1.5 * kk)}" y="{fx(y - h * kk - 4 * kk)}" width="{fx(3 * kk)}" height="{fx(4 * kk)}" fill="#e3cd9e"/><rect x="{fx(x - 2.5 * kk)}" y="{fx(y - h * kk + 2 * kk)}" width="{fx(1.4 * kk)}" height="{fx(h * kk - 4 * kk)}" fill="#fff" opacity=".5"/>')
    (x, y), kk = on_table(-62, 326)
    o.append(f'<rect x="{fx(x - 12 * kk)}" y="{fx(y - 9 * kk)}" width="{fx(24 * kk)}" height="{fx(9 * kk)}" rx="{fx(1.5 * kk)}" fill="#f6eef5" stroke="#e3cd9e" stroke-width="1"/><path d="M{fx(x - 12 * kk)},{fx(y - 9 * kk)} l{fx(3 * kk)},{fx(-6 * kk)} h{fx(18 * kk)} l{fx(3 * kk)},{fx(6 * kk)}Z" fill="#fbf6fa"/>')
    (x, y), kk = on_table(-40, 316)
    o.append(f'<path d="M{fx(x - 9 * kk)},{fx(y - 1 * kk)} l{fx(15 * kk)},{fx(-4 * kk)} l{fx(5 * kk)},{fx(3 * kk)} l{fx(-15 * kk)},{fx(4 * kk)}Z" fill="#2c2840"/><path d="M{fx(x - 8 * kk)},{fx(y - 1.6 * kk)} l{fx(13 * kk)},{fx(-3.4 * kk)}" stroke="#58507a" stroke-width="1"/>')
    (x, y), kk = on_table(-30, 334)
    o.append(f'<rect x="{fx(x - 4 * kk)}" y="{fx(y - 12 * kk)}" width="{fx(8 * kk)}" height="{fx(12 * kk)}" fill="#e7dcef"/>' + ''.join(f'<path d="M{fx(x + d * kk)},{fx(y - 12 * kk)} l{fx(d * .6 * kk)},{fx(-10 * kk)}" stroke="#a88a5c" stroke-width="{fx(1.4 * kk)}"/>' for d in (-3, -1, 1, 3)))
    # เก้าอี้สตูลหน้าโต๊ะ
    o.append(fshadow(c, -110, -50, 255, 290, 14, 10, .3))
    for X in (-106, -58):
        o.append(box(c, X, X + 4, 0, 40, 258, 262, '#e3cd9e', '#d9bb82', '#c9a874'))
    o.append(box(c, -112, -48, 38, 50, 255, 292, '#b8606e', '#a0505e', '#8a4350'))
    # หุ่นชุดเจ้าสาว หน้าหน้าต่าง
    bx, by = c.p(82, 0, 290); kk = c.k(290)
    o.append(f'<ellipse cx="{fx(bx + 30 * kk)}" cy="{fx(by + 4 * kk)}" rx="{fx(75 * kk)}" ry="{fx(12 * kk)}" fill="#3a2a28" opacity=".3" filter="url(#soft)"/>')
    sk = f'M{fx(bx - 8 * kk)},{fx(by - 100 * kk)} C{fx(bx - 30 * kk)},{fx(by - 60 * kk)} {fx(bx - 62 * kk)},{fx(by - 20 * kk)} {fx(bx - 70 * kk)},{fx(by)} L{fx(bx + 70 * kk)},{fx(by)} C{fx(bx + 62 * kk)},{fx(by - 20 * kk)} {fx(bx + 30 * kk)},{fx(by - 60 * kk)} {fx(bx + 8 * kk)},{fx(by - 100 * kk)}Z'
    o.append(path(sk, '#fbf7fb'))
    o.append(f'<path d="M{fx(bx + 2 * kk)},{fx(by - 100 * kk)} C{fx(bx + 26 * kk)},{fx(by - 60 * kk)} {fx(bx + 52 * kk)},{fx(by - 24 * kk)} {fx(bx + 70 * kk)},{fx(by)} L{fx(bx + 26 * kk)},{fx(by)} C{fx(bx + 22 * kk)},{fx(by - 40 * kk)} {fx(bx + 10 * kk)},{fx(by - 70 * kk)} {fx(bx + 2 * kk)},{fx(by - 100 * kk)}Z" fill="#e7dcee"/>')
    for i in range(5):
        t = (i + 1) / 6
        o.append(f'<path d="M{fx(bx - 70 * kk * t)},{fx(by - 100 * kk * (1 - t) )} q{fx(-4 * kk)},{fx(60 * kk * t)} {fx(-6 * kk * t)},{fx(100 * kk * t)}" stroke="#ece2f2" stroke-width="{fx(2 * kk)}" fill="none" opacity=".8"/>')
    o.append(f'<path d="M{fx(bx - 70 * kk)},{fx(by)} q{fx(17 * kk)},{fx(-5 * kk)} {fx(35 * kk)},0 t{fx(35 * kk)},0 t{fx(35 * kk)},0 t{fx(35 * kk)},0" stroke="#ffffff" stroke-width="{fx(2 * kk)}" fill="none"/>')
    bd = f'M{fx(bx - 15 * kk)},{fx(by - 160 * kk)} C{fx(bx - 17 * kk)},{fx(by - 130 * kk)} {fx(bx - 10 * kk)},{fx(by - 110 * kk)} {fx(bx - 10 * kk)},{fx(by - 100 * kk)} L{fx(bx + 10 * kk)},{fx(by - 100 * kk)} C{fx(bx + 10 * kk)},{fx(by - 110 * kk)} {fx(bx + 17 * kk)},{fx(by - 130 * kk)} {fx(bx + 15 * kk)},{fx(by - 160 * kk)} Q{fx(bx)},{fx(by - 150 * kk)} {fx(bx - 15 * kk)},{fx(by - 160 * kk)}Z'
    o.append(path(bd, '#fffbfd'))
    o.append(f'<path d="M{fx(bx + 3 * kk)},{fx(by - 155 * kk)} L{fx(bx + 15 * kk)},{fx(by - 160 * kk)} C{fx(bx + 17 * kk)},{fx(by - 130 * kk)} {fx(bx + 10 * kk)},{fx(by - 110 * kk)} {fx(bx + 10 * kk)},{fx(by - 100 * kk)} L{fx(bx + 3 * kk)},{fx(by - 100 * kk)}Z" fill="#ebe0f0"/>')
    o.append(f'<path d="M{fx(bx - 11 * kk)},{fx(by - 101 * kk)} h{fx(22 * kk)}" stroke="#e3cd9e" stroke-width="{fx(1.6 * kk)}"/>')
    o.append(f'<path d="M{fx(bx - 15 * kk)},{fx(by - 160 * kk)} Q{fx(bx)},{fx(by - 172 * kk)} {fx(bx + 15 * kk)},{fx(by - 160 * kk)} Q{fx(bx)},{fx(by - 152 * kk)} {fx(bx - 15 * kk)},{fx(by - 160 * kk)}Z" fill="#e3d4c4"/>')
    o.append(f'<rect x="{fx(bx - 1.5 * kk)}" y="{fx(by - 186 * kk)}" width="{fx(3 * kk)}" height="{fx(18 * kk)}" fill="#d9bb82"/><circle cx="{fx(bx)}" cy="{fx(by - 188 * kk)}" r="{fx(3 * kk)}" fill="#e3cd9e"/>')
    o.append(f'<path d="{sk}" fill="none" stroke="#ffffff" stroke-width="2.4" opacity=".9" filter="url(#glow)"/>')
    # อาร์มแชร์กำมะหยี่ฉากหน้าซ้าย + โต๊ะข้าง
    o.append(fshadow(c, -170, -90, 160, 220, 20, 12, .35))
    o.append(box(c, -175, -165, 0, 95, 165, 225, '#9a4656', '#843a4a', '#70303e'))
    o.append(box(c, -175, -90, 0, 42, 165, 225, '#a84e5e', '#904252', '#7a3646'))
    o.append(box(c, -170, -95, 42, 52, 168, 222, '#bc6a78', '#a45a68', '#8e4c5a'))
    o.append(box(c, -100, -88, 0, 64, 165, 225, '#a84e5e', '#904252', '#7a3646'))
    x, y = c.p(-95, 64, 165); kk = c.k(165)
    o.append(f'<path d="M{fx(x - 4 * kk)},{fx(y)} q{fx(6 * kk)},{fx(-8 * kk)} {fx(14 * kk)},0" stroke="#efd5e5" stroke-width="{fx(4 * kk)}" fill="none"/>')
    # ผ้าคลุมหน้าบนแขนเก้าอี้
    o.append(f'<path d="M{fx(x - 18 * kk)},{fx(y - 46 * kk)} q{fx(10 * kk)},{fx(-6 * kk)} {fx(24 * kk)},{fx(2 * kk)} q{fx(-4 * kk)},{fx(30 * kk)} {fx(6 * kk)},{fx(64 * kk)} q{fx(-18 * kk)},{fx(6 * kk)} {fx(-36 * kk)},0 q{fx(8 * kk)},{fx(-30 * kk)} {fx(6 * kk)},{fx(-66 * kk)}Z" fill="#fdf9ff" opacity=".7"/>')
    # โคมระย้าเล็ก
    x, y = c.p(-60, 250, 150); o.append(chandelier(x, y, c.k(150) * .32, 17))
    # ลำแสงจากหน้าต่างลงพื้น
    o.append(beam([(xa, yt_), (xb, yt_), (xb - 40, 900), (xa - 260, 900)], 'beamP', .65))
    o.append(dust(51, (xa - 220, yt_ + 40, xb, 860), 50))
    return frame_svg(''.join(o), 'ห้องแต่งตัวเจ้าสาวในโรงแรม โต๊ะเครื่องแป้งกระจกล้อมไฟ ชุดเจ้าสาวบนหุ่นหน้าหน้าต่าง แสงสนธยาส่องเป็นลำลงพื้น อาร์มแชร์กำมะหยี่ และโคมระย้าเล็ก', (.45, .3))

# ================================================================ ฉาก 4: ห้องพักคืนเข้าหอ
def scene_suite():
    c = Cam(230, 360, 160, 560); ZB = 420; XL, XR, YC = -190, 200, 300
    o = []
    WALL = '#66708c'
    o.append(path(c.poly([(XL, YC, ZB), (XR, YC, ZB), (XR, YC, 80), (XL, YC, 80)]), '#4a5168'))
    o.append(path(c.poly([(XL, YC, ZB), (XR, YC, ZB), (XR, YC, ZB - 26), (XL, YC, ZB - 26)]), '#cbbfb2'))
    o.append(path(c.poly([(XL, YC, ZB - 26), (XR, YC, ZB - 26), (XR, YC, ZB - 29), (XL, YC, ZB - 29)]), '#d9c49a'))
    o.append(path(side(c, XR, ZB, 60, 0, YC), '#535c78'))
    o.append(path(side(c, XL, ZB, 60, 0, YC), '#5c6682'))
    # หน้าต่างผนังขวา วิวเมืองกลางคืน
    o.append(path(side(c, XR, 380, 120, 40, 270), '#cfc6e2'))
    wq = side(c, XR, 372, 128, 48, 262)
    o.append(f'<clipPath id="stW"><path d="{wq}"/></clipPath><g clip-path="url(#stW)"><rect x="380" y="0" width="200" height="700" fill="url(#skyNight)"/><g filter="url(#blur1)">{city(400, 560, 520, 81, ("#3b3f78", "#323569", "#2a2c5c"), "#cfe0ff", 260)}</g><circle cx="500" cy="190" r="16" fill="#eef0ff" filter="url(#glow)"/></g>')
    for zz in (290, 200):
        o.append(path(side(c, XR, zz + 3, zz - 3, 48, 262), '#cfc6e2'))
    o.append(path(side(c, XR - .1, 395, 330, 0, 285), '#8f84b5'))
    o.append(path(side(c, XR - .1, 140, 70, 0, 285), '#8f84b5'))
    # ผนังหลัง
    o.append(path(back(c, XL, XR, 0, YC, ZB), WALL))
    o.append(f'<path d="{back(c, XL, XR, 90, YC - 24, ZB)}" fill="url(#damask)" opacity=".7"/>')
    o.append(path(back(c, XL, XR, YC - 24, YC, ZB), '#cdc2e0'))
    o.append(wainscot(c, XL, XR, ZB, 86, '#5a4038', 5))
    # ประตูทางเข้าห้อง
    o.append(path(back(c, -186, -96, 0, 222, ZB), '#d8cfe8'))
    o.append(path(back(c, -180, -102, 0, 216, ZB), '#6a4a3c'))
    o.append(path(back(c, -174, -108, 20, 110, ZB), '#5a3e32'))
    o.append(path(back(c, -174, -108, 122, 204, ZB), '#5a3e32'))
    hx, hy = c.p(-112, 105, ZB)
    o.append(f'<rect x="{fx(hx - 9)}" y="{fx(hy - 3)}" width="12" height="4" rx="2" fill="#e0c995"/><rect x="{fx(hx - 3)}" y="{fx(hy - 22)}" width="6" height="16" rx="1.5" fill="#463f62"/><circle cx="{fx(hx)}" cy="{fx(hy - 18)}" r="1.4" fill="#9effc8"/>')
    px, py = c.p(-141, 160, ZB)
    o.append(f'<circle cx="{fx(px)}" cy="{fx(py)}" r="3" fill="#e0c995"/><circle cx="{fx(px)}" cy="{fx(py)}" r="1.4" fill="#2a2440"/>')
    cx1, cy1 = c.p(-108, 140, ZB)
    o.append(f'<path d="M{fx(cx1)},{fx(cy1)} q-14,10 -24,2" stroke="#e0c995" stroke-width="1.6" fill="none" stroke-dasharray="3 1.4"/>')
    lx0, ly = c.p(-180, 0, ZB); lx1, _ = c.p(-102, 0, ZB)
    o.append(f'<rect x="{fx(lx0)}" y="{fx(ly - 2)}" width="{fx(lx1 - lx0)}" height="3" fill="#fff1dd" filter="url(#glow)"/>')
    # ภาพแขวนเหนือเตียง
    a0, a1 = c.p(-10, 250, ZB), c.p(150, 160, ZB)
    o.append(softsh(P([(a0[0], a0[1]), (a1[0], a0[1]), (a1[0], a1[1]), (a0[0], a1[1])]), 5, 6, .35))
    o.append(f'<rect x="{fx(a0[0])}" y="{fx(a0[1])}" width="{fx(a1[0] - a0[0])}" height="{fx(a1[1] - a0[1])}" fill="#e2cd9c"/><rect x="{fx(a0[0] + 6)}" y="{fx(a0[1] + 6)}" width="{fx(a1[0] - a0[0] - 12)}" height="{fx(a1[1] - a0[1] - 12)}" fill="#ece2d6"/>')
    o.append(f'<path d="M{fx(a0[0] + 6)},{fx(a1[1] - 6)} C{fx(a0[0] + 50)},{fx(a1[1] - 50)} {fx(a1[0] - 60)},{fx(a0[1] + 50)} {fx(a1[0] - 6)},{fx(a0[1] + 20)} L{fx(a1[0] - 6)},{fx(a1[1] - 6)}Z" fill="#b9a08e"/><circle cx="{fx(a1[0] - 40)}" cy="{fx(a0[1] + 28)}" r="10" fill="#f1d3dd"/>')
    # พื้นพรม
    floor_d = flat(c, XL, XR, 60, ZB, 0)
    o.append(path(floor_d, '#3e3a44'))
    o.append(f'<clipPath id="stF"><path d="{floor_d}"/></clipPath><g clip-path="url(#stF)">')
    for X in range(XL, XR, 14):
        o.append(f'<path d="{c.poly([(X, 0, ZB), (X + 7, 0, ZB), (X + 7, 0, 60), (X, 0, 60)])}" fill="#38343e" opacity=".7"/>')
    o.append(path(flat(c, -150, 180, 90, 300, 0), '#7a5a52'))
    o.append(path(flat(c, -140, 170, 98, 292, 0), '#8a6a60'))
    o.append(f'<path d="{flat(c, -140, 170, 98, 292, 0)}" fill="none" stroke="#d9c49a" stroke-width="2" stroke-dasharray="5 4"/>')
    o.append(f'<path d="{flat(c, -186, -96, 380, 420, 0)}" fill="#fff1dd" opacity=".35" filter="url(#haze)"/>')
    o.append('</g>')
    # โต๊ะข้างเตียง + โคมไฟ
    def nightstand(X0, X1):
        s = fshadow(c, X0, X1, 375, 415, 14, 10, .4)
        s += box(c, X0, X1, 0, 58, 375, 418, '#e5ddef', '#d6cbe6', '#c8bcdb')
        s += path(back(c, X0 + 4, X1 - 4, 30, 52, 375), '#cdc1df')
        hx_, hy_ = c.p((X0 + X1) / 2, 41, 375); s += f'<circle cx="{fx(hx_)}" cy="{fx(hy_)}" r="1.8" fill="#e0c995"/>'
        x_, y_ = c.p((X0 + X1) / 2, 58, 395); k_ = c.k(395)
        s += f'<circle cx="{fx(x_)}" cy="{fx(y_ - 44 * k_)}" r="{fx(70 * k_)}" fill="url(#lampGlow)"/>'
        s += f'<path d="M{fx(x_ - 7 * k_)},{fx(y_)} q{fx(-8 * k_)},{fx(-14 * k_)} {fx(0)},{fx(-24 * k_)} h{fx(14 * k_)} q{fx(8 * k_)},{fx(10 * k_)} 0,{fx(24 * k_)}Z" fill="#e8dcf0"/>'
        s += f'<path d="M{fx(x_ - 15 * k_)},{fx(y_ - 24 * k_)} l{fx(5 * k_)},{fx(-26 * k_)} h{fx(20 * k_)} l{fx(5 * k_)},{fx(26 * k_)}Z" fill="#fff6ea"/>'
        s += f'<path d="M{fx(x_ + 3 * k_)},{fx(y_ - 24 * k_)} l{fx(2 * k_)},{fx(-26 * k_)} h{fx(5 * k_)} l{fx(5 * k_)},{fx(26 * k_)}Z" fill="#efe0d8"/>'
        s += beam([(x_ - 15 * k_, y_ - 24 * k_), (x_ + 15 * k_, y_ - 24 * k_), (x_ + 40 * k_, y_ + 20 * k_), (x_ - 40 * k_, y_ + 20 * k_)], 'beamW', .8)
        return s
    o.append(nightstand(-88, -42))
    o.append(nightstand(164, 198))
    # เตียง
    o.append(fshadow(c, -36, 160, 210, 415, 26, 18, .45))
    o.append(box(c, -40, 162, 0, 150, 408, 418, '#c9b4a2', '#b49e8c', '#9e8878'))
    for i in range(4):
        for j in range(3):
            tx, ty = c.p(-25 + i * 52 + (26 if j % 2 else 0), 70 + j * 26, 408)
            if tx < c.p(150, 0, 408)[0]:
                o.append(f'<circle cx="{fx(tx)}" cy="{fx(ty)}" r="1.6" fill="#8e7866"/>')
    o.append(box(c, -32, 154, 0, 30, 215, 408, '#6a4a40', '#5a3e36', '#4c342e'))
    o.append(box(c, -34, 156, 30, 58, 212, 406, '#fbf8fe', '#efe9f6', '#e2daee'))
    # หมอน
    for X in (-22, 64):
        x0_, y0_ = c.p(X, 58, 395); x1_, y1_ = c.p(X + 80, 88, 395)
        o.append(f'<rect x="{fx(x0_)}" y="{fx(y1_)}" width="{fx(x1_ - x0_)}" height="{fx(y0_ - y1_)}" rx="10" fill="#ffffff"/><rect x="{fx(x0_ + 6)}" y="{fx(y1_ + (y0_ - y1_) * .55)}" width="{fx(x1_ - x0_ - 12)}" height="{fx((y0_ - y1_) * .4)}" rx="6" fill="#e9e2f2"/>')
    x0_, y0_ = c.p(30, 58, 370); x1_, y1_ = c.p(100, 82, 370)
    o.append(f'<rect x="{fx(x0_)}" y="{fx(y1_)}" width="{fx(x1_ - x0_)}" height="{fx(y0_ - y1_)}" rx="8" fill="#d8b9d6"/>')
    # ผ้าห่มพับ + ผ้าพาดปลายเตียง
    o.append(path(flat(c, -34, 156, 212, 330, 58.5), '#f5f1fa'))
    o.append(path(flat(c, -34, 156, 318, 330, 58.6), '#ffffff'))
    o.append(path(flat(c, -34, 156, 230, 270, 58.7), '#8e3e4e'))
    o.append(path(back(c, -34, 156, 30, 58, 212), '#ebe4f3'))
    o.append(path(back(c, -34, 156, 18, 58, 212), '#a995c8', 'opacity=".0"'))
    o.append(path(c.poly([(-34, 58.7, 230), (156, 58.7, 230), (156, 26, 228), (-34, 26, 228)]), '#7a3242'))
    # กลีบกุหลาบรูปหัวใจบนเตียง
    r = random.Random(14)
    hcx, hcz = 60, 290
    for i in range(70):
        t = r.uniform(0, 2 * math.pi)
        hxw = 16 * math.sin(t) ** 3; hzw = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        X = hcx + hxw * 2.4 + r.uniform(-3, 3); z = hcz + hzw * 2.2 + r.uniform(-3, 3)
        x, y = c.p(X, 59, z); kk = c.k(z)
        o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(3.2 * kk)}" ry="{fx(1.6 * kk)}" transform="rotate({r.uniform(-50, 50):.0f} {fx(x)} {fx(y)})" fill="{r.choice(("#e88aa6", "#f2a9bd", "#d9718f"))}"/>')
    # ม้านั่งปลายเตียง
    o.append(fshadow(c, -10, 130, 176, 200, 18, 12, .4))
    for X in (-6, 122):
        o.append(box(c, X, X + 4, 0, 30, 178, 182, '#d9c49a', '#cbb282', '#bca273'))
    o.append(box(c, -10, 130, 30, 44, 176, 200, '#8e3e4e', '#7a3242', '#682a38'))
    for X in (10, 40, 70, 100):
        tx, ty = c.p(X, 44, 188); o.append(f'<circle cx="{fx(tx)}" cy="{fx(ty)}" r="2" fill="#5a2430"/>')
    # ถังแชมเปญข้างหน้าต่าง
    x, y = c.p(178, 0, 230); kk = c.k(230)
    o.append(f'<ellipse cx="{fx(x + 10 * kk)}" cy="{fx(y + 2 * kk)}" rx="{fx(16 * kk)}" ry="{fx(4 * kk)}" fill="#20183a" opacity=".4" filter="url(#soft)"/>')
    o.append(f'<path d="M{fx(x - 10 * kk)},{fx(y)} L{fx(x)},{fx(y - 70 * kk)} L{fx(x + 10 * kk)},{fx(y)}" stroke="#d9c49a" stroke-width="{fx(2 * kk)}" fill="none"/>')
    o.append(f'<path d="M{fx(x - 13 * kk)},{fx(y - 92 * kk)} h{fx(26 * kk)} l{fx(-3 * kk)},{fx(24 * kk)} h{fx(-20 * kk)}Z" fill="#e6d3a6"/><rect x="{fx(x - 2 * kk)}" y="{fx(y - 116 * kk)}" width="{fx(5 * kk)}" height="{fx(26 * kk)}" fill="#3c5a4a"/><rect x="{fx(x - 1.5 * kk)}" y="{fx(y - 118 * kk)}" width="{fx(4 * kk)}" height="{fx(6 * kk)}" fill="#e3cd9e"/>')
    # โคมเพดาน
    x, y = c.p(60, 250, 230); o.append(chandelier(x, y, c.k(230) * .5, 23, glow=False))
    o.append(f'<circle cx="{fx(x)}" cy="{fx(y + 20)}" r="70" fill="url(#chGlow)" opacity=".5"/>')
    # แสงจันทร์จากหน้าต่าง
    o.append(beam([(470, 140), (540, 100), (540, 640), (230, 860)], 'beamB', .5))
    o.append(dust(61, (300, 300, 540, 820), 30, '#e6ecff'))
    o.append(dust(62, (0, 380, 200, 600), 12))
    o.append(f'<rect width="540" height="960" fill="#1b1838" opacity=".14"/>')
    return frame_svg(''.join(o), 'ห้องพักหรูคืนเข้าหอ เตียงหัวเตียงบุนวม กลีบกุหลาบรูปหัวใจ โคมไฟข้างเตียงแสงอุ่น หน้าต่างเห็นเมืองยามค่ำ และประตูทางเข้าที่มีตาแมว', (.55, .42), .75)

# ================================================================ ฉาก 5: ในลิฟต์
def scene_elevator():
    c = Cam(270, 380, 160, 440); ZB = 200; XL, XR, YC = -95, 95, 250
    o = []
    # ทางเดินด้านนอกประตู (ลึกเข้าไป)
    o.append(f'<rect width="540" height="960" fill="#3b3157"/>')
    cz = 1300
    o.append(path(c.poly([(-120, 0, ZB), (120, 0, ZB), (120, 0, cz), (-120, 0, cz)]), '#5a3f62'))
    o.append(path(c.poly([(-60, 0, ZB), (60, 0, ZB), (60, 0, cz), (-60, 0, cz)]), '#704a6e'))
    o.append(path(side(c, -120, ZB, cz, 0, 260), '#4d4270'))
    o.append(path(side(c, 120, ZB, cz, 0, 260), '#443a66'))
    o.append(path(c.poly([(-120, 260, ZB), (120, 260, ZB), (120, 260, cz), (-120, 260, cz)]), '#3a3058'))
    o.append(path(back(c, -120, 120, 0, 260, cz), '#5b4e80'))
    for z in (420, 700, 1000):
        o.append(path(side(c, 120, z + 50, z - 50, 0, 210), '#6d5f92'))
        o.append(path(side(c, 120, z + 44, z - 44, 6, 204), '#5f5185'))
        x, y = c.p(-120, 180, z)
        o.append(f'<circle cx="{fx(x)}" cy="{fx(y)}" r="{fx(60 * c.k(z))}" fill="url(#chGlow)"/><rect x="{fx(x)}" y="{fx(y - 8 * c.k(z))}" width="{fx(5 * c.k(z))}" height="{fx(14 * c.k(z))}" fill="#fff4e4"/>')
    nx, ny = c.p(118, 160, 640)
    o.append(f'<text x="{fx(nx - 2)}" y="{fx(ny)}" text-anchor="end" font-family="Cormorant Garamond, serif" font-size="9" fill="#d9c49a" transform="skewY(18 )">1208</text>')
    o.append(f'<path d="M0,0" />')
    # ผนังหน้า (ประตูลิฟต์)
    W1 = '#b58c7c'
    face = back(c, XL, XR, 0, YC, ZB)
    gap = 26
    o.append(path(back(c, XL, -54, 0, YC, ZB), W1))
    o.append(path(back(c, 54, XR, 0, YC, ZB), W1))
    o.append(path(back(c, -54, 54, 216, YC, ZB), W1))
    o.append(path(back(c, -58, -52, 0, 220, ZB), '#bfa07a'))
    o.append(path(back(c, 52, 58, 0, 220, ZB), '#a88a66'))
    o.append(path(back(c, -58, 58, 214, 220, ZB), '#d8bf98'))
    o.append(f'<clipPath id="elO"><path d="{back(c, -52, 52, 0, 214, ZB)}"/></clipPath>')
    # บานประตูแง้มออกข้างละครึ่ง
    o.append(f'<g clip-path="url(#elO)">')
    o.append(path(back(c, -52, -gap, 0, 214, ZB - 1), '#a57a6c'))
    o.append(path(back(c, gap, 52, 0, 214, ZB - 1), '#946a5e'))
    o.append(path(back(c, -gap - 1, -gap, 0, 214, ZB - 1), '#efe0c0'))
    o.append(path(back(c, gap, gap + 1, 0, 214, ZB - 1), '#9e8a68'))
    o.append('</g>')
    # ป้ายบอกชั้น
    ix0, iy0 = c.p(-30, 238, ZB); ix1, iy1 = c.p(30, 224, ZB)
    o.append(f'<rect x="{fx(ix0)}" y="{fx(iy0)}" width="{fx(ix1 - ix0)}" height="{fx(iy1 - iy0)}" rx="3" fill="#221b33"/><text x="{fx((ix0 + ix1) / 2 + 6)}" y="{fx(iy1 - 6)}" text-anchor="middle" font-family="IBM Plex Mono, monospace" font-size="20" fill="#cbb2ff" filter="url(#glow)">12</text><path d="M{fx(ix0 + 12)},{fx(iy1 - 9)} l6,-9 l6,9Z" fill="#cbb2ff" opacity=".9"/>')
    o.append(f'<circle cx="{fx((ix0 + ix1) / 2)}" cy="{fx((iy0 + iy1) / 2)}" r="60" fill="#b392ff" opacity=".12" filter="url(#haze)"/>')
    # ผนังข้าง: แผงทองแชมเปญ + กระจก
    for X, base, sh in ((XL, '#a87e72', '#8e665c'), (XR, '#9a7266', '#825c52')):
        o.append(path(side(c, X, ZB, 40, 0, YC), base))
        for (z0, z1) in ((ZB - 8, 150), (142, 96), (88, 50)):
            o.append(path(side(c, X, z0, z1, 12, YC - 12), sh))
            o.append(path(side(c, X, z0 - 2, z1 + 2, 14, YC - 14), base))
        o.append(path(side(c, X, 140, 98, 100, YC - 20), '#8f89ad'))
        o.append(f'<path d="{side(c, X, 140, 98, 100, YC - 20)}" fill="url(#mirror)" opacity=".6"/>')
        o.append(path(side(c, X, ZB, 40, 86, 92), '#efdcb6'))
        o.append(path(side(c, X, ZB, 40, 84, 86), '#a38c64'))
    # แผงปุ่มกด ผนังขวาใกล้ประตู
    o.append(path(side(c, XR, 192, 164, 96, 158), '#2a2338'))
    for j in range(5):
        for i in range(2):
            z = 186 - i * 12; Y = 150 - j * 11
            x, y = c.p(XR, Y, z); kk = c.k(z)
            lit = (j == 1 and i == 0)
            o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(2.2 * kk * .7)}" ry="{fx(3 * kk)}" fill="{"#cbb2ff" if lit else "#d9c49a"}" {"filter=\"url(#glow)\"" if lit else ""}/>')
    # เพดาน: แผงไฟดาวน์ไลต์
    o.append(path(c.poly([(XL, YC, ZB), (XR, YC, ZB), (XR, YC, 40), (XL, YC, 40)]), '#8f7466'))
    o.append(path(c.poly([(XL + 10, YC, ZB - 8), (XR - 10, YC, ZB - 8), (XR - 10, YC, 50), (XL + 10, YC, 50)]), '#a38878'))
    for z in (175, 130, 95):
        for X in (-45, 0, 45):
            x, y = c.p(X, YC, z); kk = c.k(z)
            o.append(f'<ellipse cx="{fx(x)}" cy="{fx(y)}" rx="{fx(7 * kk)}" ry="{fx(2.2 * kk)}" fill="#fffdf6" filter="url(#glow)"/>')
    # พื้นหินอ่อนลายฝัง
    fl = flat(c, XL, XR, 40, ZB, 0)
    o.append(path(fl, '#c4b2a4'))
    o.append(f'<clipPath id="elF"><path d="{fl}"/></clipPath><g clip-path="url(#elF)">{veins(71, 30, (0, 700, 540, 960), "#ffffff", .5)}')
    o.append(path(c.poly([(0, 0, 175), (60, 0, 120), (0, 0, 75), (-60, 0, 120)]), '#cdb6c9'))
    o.append(path(c.poly([(0, 0, 165), (48, 0, 120), (0, 0, 85), (-48, 0, 120)]), '#e2cdd9'))
    o.append(path(c.poly([(0, 0, 150), (26, 0, 120), (0, 0, 100), (-26, 0, 120)]), '#d9c49a'))
    o.append(path(flat(c, -52, 52, ZB - 8, ZB, 0), '#a38c64'))
    o.append('</g>')
    # ลำแสงดาวน์ไลต์ลงพื้น
    for X in (-45, 45):
        x, y = c.p(X, YC, 130)
        o.append(beam([(x - 10, y), (x + 10, y), (x + 60, 940), (x - 60, 940)], 'beamW', .4))
    o.append(dust(81, (80, 160, 460, 900), 34))
    # ทางเดินมืดลงเล็กน้อย ให้ดูผิดปกติ
    o.append(f'<path d="{back(c, -52, 52, 0, 214, ZB)}" fill="#1c1430" opacity=".18"/>')
    o.append(f'<rect width="540" height="960" fill="#2a2450" opacity=".08"/>')
    return frame_svg(''.join(o), 'ภายในลิฟต์โรงแรมหรู ผนังทองแชมเปญกับกระจก ราวจับทองเหลือง ป้ายบอกชั้น 12 ประตูแง้มเห็นทางเดินพรมสีม่วงเข้ม และดาวน์ไลต์ส่องลงพื้นหินอ่อน', (.5, .3), .6)

# ---------------------------------------------------------------- ประกอบหน้า
DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stipple" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.15" numOctaves="1" seed="5"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="9"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="blur1" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="blur3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="moteBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grade" color-interpolation-filters="sRGB"><feComponentTransfer><feFuncR type="gamma" exponent="1.22" amplitude="1"/><feFuncG type="gamma" exponent="1.25" amplitude="1"/><feFuncB type="gamma" exponent="1.3" amplitude="1"/></feComponentTransfer><feColorMatrix type="saturate" values="1.08"/></filter>
<radialGradient id="chGlow"><stop offset="0" stop-color="#fff6ea" stop-opacity=".6"/><stop offset=".4" stop-color="#fbeadc" stop-opacity=".24"/><stop offset="1" stop-color="#f5dccb" stop-opacity="0"/></radialGradient>
<radialGradient id="lampGlow"><stop offset="0" stop-color="#fff1e2" stop-opacity=".75"/><stop offset=".5" stop-color="#ffe6dc" stop-opacity=".25"/><stop offset="1" stop-color="#ffe6dc" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx=".5" cy=".46" r=".75"><stop offset=".55" stop-color="#2a1e20" stop-opacity="0"/><stop offset="1" stop-color="#2a1e20" stop-opacity=".42"/></radialGradient>
<linearGradient id="skyDusk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5d6aa6"/><stop offset=".55" stop-color="#b394bf"/><stop offset="1" stop-color="#f4bfa8"/></linearGradient>
<linearGradient id="skyNight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1c2050"/><stop offset="1" stop-color="#3d4282"/></linearGradient>
<linearGradient id="mirror" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f2ef"/><stop offset=".5" stop-color="#cfd2d8"/><stop offset="1" stop-color="#eeebe6"/></linearGradient>
<linearGradient id="beamW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff6ee" stop-opacity=".55"/><stop offset="1" stop-color="#fff6ee" stop-opacity="0"/></linearGradient>
<linearGradient id="beamP" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe9dc" stop-opacity=".6"/><stop offset="1" stop-color="#f8dccc" stop-opacity="0"/></linearGradient>
<linearGradient id="beamB" x1="1" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfdcff" stop-opacity=".5"/><stop offset="1" stop-color="#cfdcff" stop-opacity="0"/></linearGradient>
<pattern id="damask" width="34" height="44" patternUnits="userSpaceOnUse"><g fill="#ffffff" opacity=".28"><path d="M17,6 C21,12 25,14 25,20 C25,26 20,28 17,34 C14,28 9,26 9,20 C9,14 13,12 17,6Z"/><circle cx="17" cy="40" r="1.6"/><circle cx="0" cy="18" r="1.6"/><circle cx="34" cy="18" r="1.6"/></g><path d="M17,12 L17,30" stroke="#b8a08a" stroke-width=".8" opacity=".35"/></pattern>
</defs></svg>'''

SCENES = [
    ('ฉาก A · โถงหน้าห้องจัดเลี้ยง', 'ใช้กับช็อต 4 ตอนประตูเปิด (มองจากด้านนอก), ช็อต 7–8 ตอน รปภ. พาผู้หญิงชุดดำออกไป และช็อต 27 ตอนประตูเปิดหนึ่งปีต่อมา', scene_lobby),
    ('ฉาก B · ห้องจัดเลี้ยง พิธีแต่งงาน', 'ฉากหลักของเรื่อง ใช้กับช็อต 2–6, 9–14 และ 26–29 ตอนนี้ยังเป็นฉากเปล่า แขกกับคู่บ่าวสาวจะใส่ทีหลังเมื่อเลือกตัวละครแล้ว', scene_ballroom),
    ('ฉาก C · ห้องแต่งตัวเจ้าสาว', 'ใช้กับช็อต 15–19 ตอนแอบค้นมือถือเจ้าบ่าว บนโต๊ะเครื่องแป้งวางมือถือคว่ำไว้แล้ว แสงสนธยาส่องผ่านหน้าต่าง', scene_dressing),
    ('ฉาก D · ห้องพัก คืนเข้าหอ', 'ใช้กับช็อต 21–25 ตอนโทรศัพท์ดังและเสียงเคาะประตู โทนกลางคืนเย็นลง ประตูทางเข้ามีตาแมว โซ่คล้อง และแสงลอดใต้ประตู', scene_suite),
    ('ฉาก E · ในลิฟต์', 'ใช้กับช็อต 20 ตอนลิฟต์พากลับมาชั้นเดิม ป้ายบอกชั้นขึ้นเลข 12 ประตูแง้มเห็นทางเดินที่มืดกว่าลิฟต์', scene_elevator),
]

CSS = '''<title>ฉากโรงแรมงานแต่ง</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Cormorant+Garamond:ital,wght@0,500;1,500&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: dark stage, responsive grid of 9:16 frames with captions. Single dark look by choice (matches the channel's sheets). */
:root{--stage:#14111d;--ink:#e6e0ef;--muted:#9a92ad;--line:#2d2740;--accent:#c9a8ff;--font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;color-scheme:dark}
html,body{background:var(--stage);color:var(--ink)}
body{font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 40px}
.wrap{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:20px}
header{display:flex;flex-wrap:wrap;gap:12px;align-items:end;justify-content:space-between}
h1{margin:0;font-size:22px;font-weight:600;text-wrap:balance}
h1 span{display:block;font-size:13px;font-weight:400;color:var(--muted);margin-top:4px}
button{font:inherit;font-size:13px;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:6px;padding:7px 12px;cursor:pointer}
button:hover{border-color:var(--muted)}
button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button[aria-pressed="true"]{border-color:var(--accent);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:22px}
figure{margin:0;display:flex;flex-direction:column;gap:10px;min-width:0}
figure svg{display:block;width:100%;max-width:100%;aspect-ratio:9/16;height:auto;border-radius:4px;box-shadow:0 0 0 1px var(--line),0 16px 40px rgba(0,0,0,.45)}
figcaption{display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:1.55}
figcaption b{font-weight:600;color:#fff}
figcaption small{color:var(--muted);font-size:12.5px}
.guide{display:none}
.show-guide .guide{display:inline}
.note{font-size:13px;color:var(--muted);line-height:1.6;max-width:70ch}
</style>'''

def build():
    figs = ''.join(f'<figure>{fn()}<figcaption><b>{t}</b><small>{n}</small></figcaption></figure>' for t, n, fn in SCENES)
    page = CSS + DEFS + f'''<div class="wrap" id="wrap"><header><h1>ฉากโรงแรมหรู ตอนงานแต่ง<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ฉากเปล่า 5 ฉาก ยังไม่ใส่ตัวละคร</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">{figs}</div>
<p class="note">โทนแชมเปญอมกุหลาบ ไม้เข้ม ทอง และผ้ากุหลาบเข้มตามภาพตัวอย่างที่ส่งมา ใช้แสงขาวอุ่นกับทองอ่อน ไม่ให้ออกเหลือง ฉากห้องพักกับลิฟต์กดให้เย็นลงตามจังหวะเรื่อง ทุกฉากมีเม็ดเกรน ลำแสงพร้อมฝุ่นลอย และเงาตกเยื้องไปทางขวาล่าง</p></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets.html', 'w').write(page)
    print('ok', len(page))

if __name__ == '__main__':
    build()
