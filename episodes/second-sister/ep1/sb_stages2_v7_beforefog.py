# Round-2 stages for the EP1 storyboard (exec'd inside storyboard.py, uses its helpers).
# Every room is built once as a *_room() function so all camera angles of that room share
# the same walls, doors, windows and furniture.
import math as _m

def poly(pts, fill, op=None, extra=""):
    o = f' opacity="{op}"' if op is not None else ""
    return f'<polygon points="{pts}" fill="{fill}"{o} {extra}/>'

def stars(n, y1=420, seed=3):
    r = _rr.Random(seed)
    return "".join(f'<circle cx="{r.uniform(0, 540):.0f}" cy="{r.uniform(0, y1):.0f}" r="{r.uniform(.5, 1.4):.1f}" fill="#eef0ff" opacity="{r.uniform(.3, .9):.2f}"/>' for _ in range(n))

def moon(x, y, r=34):
    return (f'<circle cx="{x}" cy="{y}" r="{r * 3.2:.0f}" fill="url(#lg_c4d0ff)" opacity=".55"/><circle cx="{x}" cy="{y}" r="{r}" fill="#f2f2ff"/>'
            f'<circle cx="{x - r * .3:.0f}" cy="{y - r * .2:.0f}" r="{r * .22:.0f}" fill="#d8dcf0" opacity=".7"/><circle cx="{x + r * .32:.0f}" cy="{y + r * .25:.0f}" r="{r * .15:.0f}" fill="#d8dcf0" opacity=".6"/><circle cx="{x + r * .1:.0f}" cy="{y - r * .45:.0f}" r="{r * .1:.0f}" fill="#d8dcf0" opacity=".6"/>')

def cloud(x, y, w, h, body="#3a3c6a", rim="#9aa0d8", op=.9):
    """Varied lumpy cloud with a moonlit top rim."""
    r = _rr.Random(int(x * 7 + y))
    bumps = []
    n = r.randint(4, 7)
    for i in range(n):
        bx = x + w * (i + .5) / n + r.uniform(-w * .05, w * .05)
        br = h * r.uniform(.45, .85)
        bumps.append((bx, y - br * .3, br))
    o = f'<g opacity="{op}">'
    o += f'<rect x="{x}" y="{y - h * .2:.0f}" width="{w}" height="{h * .55:.0f}" rx="{h * .27:.0f}" fill="{body}"/>'
    for bx, by, br in bumps:
        o += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{br:.0f}" fill="{body}"/>'
    for bx, by, br in bumps:
        o += f'<path d="M {bx - br * .8:.0f},{by - br * .3:.0f} A {br:.0f},{br:.0f} 0 0 1 {bx + br * .6:.0f},{by - br * .6:.0f}" stroke="{rim}" stroke-width="2.2" fill="none" opacity=".7"/>'
    return o + '</g>'

def night_sky(moon_xy=(420, 120), seed=3):
    o = '<linearGradient id="nsky2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c1030"/><stop offset=".6" stop-color="#232a5c"/><stop offset="1" stop-color="#3e3e74"/></linearGradient>'
    o += '<rect width="540" height="960" fill="url(#nsky2)"/>' + stars(70, 460, seed) + moon(*moon_xy)
    o += cloud(-30, 210, 210, 34, op=.85) + cloud(300, 150, 170, 26, op=.75) + cloud(moon_xy[0] - 70, moon_xy[1] + 34, 140, 18, op=.6) + cloud(160, 300, 120, 20, op=.6)
    return o

def plaster_wear(x, y, w, h, seed, dark="#8a8098", brick="#9a6a60"):
    """Peeling patches showing brick, cracks and damp streaks over a wall area."""
    r = _rr.Random(seed); o = ""
    for _ in range(3):
        px, py = r.uniform(x, x + w - 20), r.uniform(y, y + h - 14)
        pw, ph = r.uniform(14, 30), r.uniform(8, 16)
        o += f'<path d="M {px:.0f},{py:.0f} l {pw * .3:.0f},{-ph * .4:.0f} l {pw * .7:.0f},{ph * .2:.0f} l {-pw * .1:.0f},{ph * .9:.0f} l {-pw * .8:.0f},{ph * .2:.0f} Z" fill="{brick}" opacity=".55"/>'
        o += "".join(f'<path d="M {px + 2:.0f},{py + k * 5:.0f} l {pw * .6:.0f},0" stroke="#7a4a44" stroke-width=".8" opacity=".5"/>' for k in range(1, 3))
    for _ in range(2):
        cx, cy = r.uniform(x, x + w), r.uniform(y, y + h * .6)
        d = f"M {cx:.0f},{cy:.0f}"
        for k in range(5):
            cx += r.uniform(-6, 6); cy += r.uniform(5, 12); d += f" L {cx:.0f},{cy:.0f}"
        o += f'<path d="{d}" fill="none" stroke="#4a4458" stroke-width="1"/>'
    for _ in range(3):
        sx = r.uniform(x, x + w)
        o += f'<rect x="{sx:.0f}" y="{y}" width="{r.uniform(3, 7):.1f}" height="{r.uniform(h * .2, h * .6):.0f}" fill="{dark}" opacity=".3"/>'
    return o

# ============================== 1. BELL TOWER ==============================
def bell_tower_old(swing=0):
    """Old Gothic bell tower, low angle: verticals converge upward. Bell clearly visible in the belfry."""
    o = ""
    # tower footprint at the base, converging toward the top (low camera)
    bx0, bx1, by = 160, 380, 900       # base
    tx0, tx1, ty = 200, 340, 210       # top of the shaft
    def X(u, y):  # u 0..1 across, interpolated by height
        t = (by - y) / (by - ty)
        return (bx0 + (tx0 - bx0) * t) + ((bx1 + (tx1 - bx1) * t) - (bx0 + (tx0 - bx0) * t)) * u
    lit, mid, shd = "#c8c4dc", "#a8a4c4", "#6e6a90"
    # moonlit left face / shadowed right face
    o += poly(f"{X(0, by):.0f},{by} {X(.62, by):.0f},{by} {X(.62, ty):.0f},{ty} {X(0, ty):.0f},{ty}", mid)
    o += poly(f"{X(0, by):.0f},{by} {X(.16, by):.0f},{by} {X(.16, ty):.0f},{ty} {X(0, ty):.0f},{ty}", lit)
    o += poly(f"{X(.62, by):.0f},{by} {X(1, by):.0f},{by} {X(1, ty):.0f},{ty} {X(.62, ty):.0f},{ty}", shd)
    # string courses (horizontal mouldings), get thinner as they rise
    for y in (760, 600, 440, 300):
        o += poly(f"{X(-.03, y):.0f},{y} {X(1.03, y):.0f},{y} {X(1.03, y - 10):.0f},{y - 10} {X(-.03, y - 10):.0f},{y - 10}", "#d8d4e8")
        o += poly(f"{X(.62, y):.0f},{y} {X(1.03, y):.0f},{y} {X(1.03, y - 10):.0f},{y - 10} {X(.62, y - 10):.0f},{y - 10}", "#7a769a")
        o += f'<rect x="{X(-.03, y):.0f}" y="{y}" width="{X(1.03, y) - X(-.03, y):.0f}" height="6" fill="#3a3658" opacity=".5"/>'
    # pointed door at the base
    dl, dr = X(.3, by), X(.56, by)
    o += f'<path d="M {dl:.0f},{by} L {dl:.0f},{by - 110} Q {(dl + dr) / 2:.0f},{by - 170} {dr:.0f},{by - 110} L {dr:.0f},{by} Z" fill="#1a1422"/><path d="M {dl - 8:.0f},{by} L {dl - 8:.0f},{by - 112} Q {(dl + dr) / 2:.0f},{by - 184} {dr + 8:.0f},{by - 112} L {dr + 8:.0f},{by}" stroke="#dcd8ec" stroke-width="5" fill="none"/>'
    o += f'<path d="M {(dl + dr) / 2:.0f},{by - 150} L {(dl + dr) / 2:.0f},{by}" stroke="#2a2232" stroke-width="2"/><path d="M {dl + 6:.0f},{by - 40} l 22,8 l 0,6 l -22,-8 Z" fill="#5a5060"/>'  # loose chain
    # lancet windows on the shaft, deep shadow inside
    for y in (690, 530):
        for u in (.2, .44):
            l, r_ = X(u, y), X(u + .12, y)
            o += f'<path d="M {l:.0f},{y} L {l:.0f},{y - 70} Q {(l + r_) / 2:.0f},{y - 98} {r_:.0f},{y - 70} L {r_:.0f},{y} Z" fill="#14101c"/><path d="M {l:.0f},{y - 70} Q {(l + r_) / 2:.0f},{y - 98} {r_:.0f},{y - 70}" stroke="#dcd8ec" stroke-width="2.4" fill="none"/>'
    # belfry: two tall open arches with the bell hanging from a timber headstock
    y0, y1 = 430, 300
    l, r_ = X(.12, y0), X(.88, y0)
    o += f'<path d="M {l:.0f},{y0} L {l:.0f},{y1 + 20} Q {(l + r_) / 2:.0f},{y1 - 60} {r_:.0f},{y1 + 20} L {r_:.0f},{y0} Z" fill="#0e0a16"/>'
    o += f'<path d="M {l - 6:.0f},{y1 + 20} Q {(l + r_) / 2:.0f},{y1 - 70} {r_ + 6:.0f},{y1 + 20}" stroke="#e0dcf0" stroke-width="4" fill="none"/>'
    cx = (l + r_) / 2
    o += f'<rect x="{l + 6:.0f}" y="{y1 + 6}" width="{r_ - l - 12:.0f}" height="10" fill="#3a2a22"/><rect x="{cx - 4:.0f}" y="{y1 + 14}" width="8" height="14" fill="#2a1e1a"/>'
    o += (f'<g transform="rotate({swing} {cx:.0f} {y1 + 26})"><path d="M {cx - 26:.0f},{y1 + 28} C {cx - 28:.0f},{y1 + 70} {cx - 40:.0f},{y1 + 96} {cx - 50:.0f},{y1 + 104} L {cx + 50:.0f},{y1 + 104} C {cx + 40:.0f},{y1 + 96} {cx + 28:.0f},{y1 + 70} {cx + 26:.0f},{y1 + 28} C {cx + 26:.0f},{y1 + 16} {cx - 26:.0f},{y1 + 16} {cx - 26:.0f},{y1 + 28} Z" fill="#c9952e"/>'
          f'<path d="M {cx - 26:.0f},{y1 + 28} C {cx - 28:.0f},{y1 + 70} {cx - 40:.0f},{y1 + 96} {cx - 50:.0f},{y1 + 104} L {cx - 22:.0f},{y1 + 104} C {cx - 16:.0f},{y1 + 80} {cx - 12:.0f},{y1 + 50} {cx - 8:.0f},{y1 + 18} Z" fill="#f2cf63"/>'
          f'<rect x="{cx - 52:.0f}" y="{y1 + 100}" width="104" height="7" rx="3" fill="#a8761f"/><path d="M {cx - 30:.0f},{y1 + 60} L {cx + 30:.0f},{y1 + 60}" stroke="#f6dc84" stroke-width="2"/>'
          f'<circle cx="{cx:.0f}" cy="{y1 + 108}" r="7" fill="#7a5418"/><path d="M {cx:.0f},{y1 + 112} L {cx + 4:.0f},{y1 + 180}" stroke="#a89a80" stroke-width="2"/></g>')
    o += f'<path d="M {l:.0f},{y0 - 30} L {r_:.0f},{y0 - 30}" stroke="#d8d4e8" stroke-width="5"/>' + "".join(f'<rect x="{l + k * (r_ - l) / 9:.0f}" y="{y0 - 28}" width="4" height="26" fill="#d8d4e8"/>' for k in range(1, 9))  # balustrade
    # crown: cornice, balustrade, corner pinnacles, drum, dome, cross
    yc = ty
    o += poly(f"{X(-.08, yc):.0f},{yc} {X(1.08, yc):.0f},{yc} {X(1.08, yc - 14):.0f},{yc - 14} {X(-.08, yc - 14):.0f},{yc - 14}", "#e4e0f0")
    o += "".join(f'<rect x="{X(k / 10, yc):.0f}" y="{yc - 34}" width="4" height="20" fill="#d0ccdc"/>' for k in range(0, 11))
    o += poly(f"{X(-.08, yc):.0f},{yc - 34} {X(1.08, yc):.0f},{yc - 34} {X(1.08, yc):.0f},{yc - 40} {X(-.08, yc):.0f},{yc - 40}", "#e4e0f0")
    for u in (-.04, 1.04):
        px = X(u, yc)
        o += f'<rect x="{px - 7:.0f}" y="{yc - 70}" width="14" height="32" fill="{lit if u < 0 else shd}"/><path d="M {px - 9:.0f},{yc - 68} L {px:.0f},{yc - 108} L {px + 9:.0f},{yc - 68} Z" fill="{lit if u < 0 else shd}"/><circle cx="{px:.0f}" cy="{yc - 110}" r="3" fill="#e4e0f0"/>'
    dx0, dx1 = X(.22, yc), X(.78, yc)
    o += f'<rect x="{dx0:.0f}" y="{yc - 100}" width="{dx1 - dx0:.0f}" height="60" fill="{mid}"/><rect x="{dx0:.0f}" y="{yc - 100}" width="{(dx1 - dx0) * .25:.0f}" height="60" fill="{lit}"/><rect x="{dx0 + (dx1 - dx0) * .7:.0f}" y="{yc - 100}" width="{(dx1 - dx0) * .3:.0f}" height="60" fill="{shd}"/>'
    o += "".join(f'<path d="M {dx0 + (dx1 - dx0) * u:.0f},{yc - 44} L {dx0 + (dx1 - dx0) * u:.0f},{yc - 76} Q {dx0 + (dx1 - dx0) * (u + .06):.0f},{yc - 88} {dx0 + (dx1 - dx0) * (u + .12):.0f},{yc - 76} L {dx0 + (dx1 - dx0) * (u + .12):.0f},{yc - 44} Z" fill="#14101c"/>' for u in (.14, .44, .74))
    o += f'<rect x="{dx0 - 6:.0f}" y="{yc - 106}" width="{dx1 - dx0 + 12:.0f}" height="8" fill="#e4e0f0"/>'
    o += f'<path d="M {dx0:.0f},{yc - 106} C {dx0:.0f},{yc - 160} {dx1:.0f},{yc - 160} {dx1:.0f},{yc - 106} Z" fill="{mid}"/><path d="M {dx0:.0f},{yc - 106} C {dx0:.0f},{yc - 150} {(dx0 + dx1) / 2 - 10:.0f},{yc - 158} {(dx0 + dx1) / 2:.0f},{yc - 158} C {(dx0 + dx1) / 2 - 16:.0f},{yc - 146} {(dx0 + dx1) / 2 - 22:.0f},{yc - 124} {(dx0 + dx1) / 2 - 20:.0f},{yc - 106} Z" fill="{lit}"/>'
    cxx = (dx0 + dx1) / 2
    o += f'<rect x="{cxx - 4:.0f}" y="{yc - 176}" width="8" height="20" fill="{lit}"/><rect x="{cxx - 2:.0f}" y="{yc - 214}" width="4" height="40" fill="#e4e0f0"/><rect x="{cxx - 12:.0f}" y="{yc - 204}" width="24" height="4" fill="#e4e0f0"/>'
    # pigeons on the cornices
    o += pigeon(X(.2, 600), 588, .7) + pigeon(X(.8, 440), 428, .6, -1)
    return o

def bell_ground(mek=True, body=True):
    o = '<path d="M 0,880 L 540,880 L 540,960 L 0,960 Z" fill="#2c2c3c"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#20202c" stroke-width="2"/>' for y in (900, 926, 952))
    o += poly("160,900 380,900 140,960 -120,960", "#0a0814", .45)   # tower shadow thrown toward the lower left (moon is upper right)
    o += "".join(tuft(x, 884, 1.3, "#3e5040") for x in (20, 60, 110, 420, 470, 520))
    o += haze(820, 110, "#b8bce0", .5)
    return o

ST["tower_fog"] = night_sky() + '<g opacity=".8">' + "".join(clump(x, 840, r, "#2a3048", "#222840", "#1a2034") for x, r in ((30, 90), (120, 70), (470, 100), (540, 80))) + '</g>' + bell_tower_old(swing=8) + bell_ground() + haze(700, 200, "#b0b4dc", .35)
_tn = night_sky() + bell_tower_old(swing=4) + bell_ground()
_tn += C("mek_torch", 110, 940, .62, .85)
_tn += '<g transform="translate(330,936) scale(.7)"><path d="M -110,0 C -100,-18 70,-22 100,-6 L 102,14 C 50,22 -70,22 -110,12 Z" fill="#6c2b30"/><path d="M -40,-14 L 64,-16 L 68,14 L -38,16 Z" fill="#748894"/><ellipse cx="-124" cy="2" rx="18" ry="14" fill="#a9a4a6"/><path d="M -20,14 L -60,36 L -54,42 L -12,20 Z" fill="#c98f69"/><rect x="-74" y="36" width="10" height="7" fill="#fbf8f2"/></g>'
_tn += '<g transform="translate(250,950)"><circle r="6" fill="none" stroke="#b49a5a" stroke-width="2"/><path d="M 4,4 l 7,8 M -4,4 l -5,9" stroke="#c9ad66" stroke-width="2"/></g>'
ST["tower_night"] = _tn

# ============================== 2. ROSA'S ROOM ==============================
def curtains(x0, y0, x1, y1, col=("#6a5a7a", "#8a7a9a", "#4a3e5a")):
    """Heavy curtains with folds, gathered with tie-backs on both sides."""
    m, l, d = col
    o = f'<rect x="{x0 - 20}" y="{y0 - 18}" width="{x1 - x0 + 40}" height="8" rx="4" fill="#3a2a22"/>'
    for side in (-1, 1):
        xa = x0 - 16 if side < 0 else x1 + 16
        xb = x0 + 56 if side < 0 else x1 - 56
        tie = y0 + (y1 - y0) * .55
        o += f'<path d="M {xa},{y0 - 12} L {xb},{y0 - 12} C {xb - side * 4},{tie - 40} {xa + side * 26},{tie - 10} {xa + side * 22},{tie} C {xa + side * 30},{tie + 40} {xa + side * 40},{y1 + 40} {xa + side * 46},{y1 + 70} L {xa},{y1 + 70} Z" fill="{m}"/>'
        for k, c in ((.25, l), (.55, d), (.8, l)):
            fx = xa + (xb - xa) * k
            o += f'<path d="M {fx:.0f},{y0 - 10} C {fx - side * 6:.0f},{tie - 40} {xa + side * (8 + 16 * k):.0f},{tie - 8} {xa + side * (8 + 16 * k):.0f},{tie} C {xa + side * (12 + 30 * k):.0f},{tie + 40} {xa + side * (16 + 30 * k):.0f},{y1 + 40} {xa + side * (16 + 30 * k):.0f},{y1 + 66}" stroke="{c}" stroke-width="5" fill="none" opacity=".8"/>'
        o += f'<rect x="{xa + side * 10 - 8:.0f}" y="{tie - 5:.0f}" width="34" height="10" rx="5" fill="#c8a868" transform="rotate({side * -14} {xa + side * 20:.0f} {tie:.0f})"/>'
    return o

def room_rosa():
    o = '<rect width="540" height="960" fill="#3e3448"/>'
    o += '<rect width="540" height="120" fill="#2e2638"/><rect y="118" width="540" height="10" fill="#5a4e64"/>'   # ceiling + cornice
    o += '<rect y="610" width="540" height="12" fill="#5a4e64"/><rect y="622" width="540" height="40" fill="#2e2638"/>'   # dado rail + skirting
    o += '<path d="M 0,660 L 540,660 L 540,960 L 0,960 Z" fill="#4a3c3a"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#3a2e2c" stroke-width="2"/>' for y in (700, 750, 810, 880))
    # window with night view of the old wing
    o += f'<svg x="56" y="190" width="200" height="300" viewBox="0 0 200 300"><rect width="200" height="300" fill="#1c2250"/>{stars(14, 140, 8)}' + old_wing(-10, 110, .9, lit=6) + '<rect y="290" width="200" height="10" fill="#141018"/></svg>'
    o += '<rect x="48" y="182" width="216" height="316" fill="none" stroke="#3a2a26" stroke-width="10"/><path d="M 156,190 L 156,490 M 56,330 L 256,330" stroke="#3a2a26" stroke-width="7"/><rect x="40" y="494" width="232" height="12" fill="#5a4234"/>'
    o += curtains(56, 190, 256, 490)
    # moonlight patch on the floor + window-frame shadow
    o += '<polygon points="70,662 250,662 400,900 150,900" fill="#9aa4e0" opacity=".16"/><path d="M 160,662 L 275,900 M 108,770 L 330,770" stroke="#2a2232" stroke-width="7" opacity=".35"/>'
    # wall: crucifix, framed Mary, wall clock, shelf with a small statue and a candle
    o += '<rect x="402" y="200" width="6" height="56" fill="#2a1e1c"/><rect x="390" y="214" width="30" height="6" fill="#2a1e1c"/>'
    o += '<rect x="440" y="300" width="64" height="80" fill="#6a5034"/><rect x="446" y="306" width="52" height="68" fill="#2a3058"/><ellipse cx="472" cy="336" rx="10" ry="13" fill="#e0d4c8"/><path d="M 456,374 C 458,350 486,350 488,374 Z" fill="#5a7ab0"/>'
    o += '<g transform="translate(330,200)"><circle r="26" fill="#3a2a22"/><circle r="21" fill="#efe8da"/><path d="M 0,0 L 0,-15 M 0,0 L 11,0" stroke="#1a1418" stroke-width="2.4"/></g>'
    o += '<rect x="290" y="420" width="90" height="6" fill="#5a4234"/><path d="M 312,420 L 314,396 C 314,388 324,388 324,396 L 326,420 Z" fill="#e8e2ea"/><rect x="350" y="404" width="5" height="16" fill="#efe8da"/>'
    # wardrobe at the right edge, bed with headboard, blanket, pillow; nightstand; slippers
    o += '<rect x="470" y="300" width="80" height="360" fill="#4a3428"/><rect x="474" y="304" width="72" height="352" fill="#5a4030"/><circle cx="482" cy="480" r="3" fill="#c8b07a"/>'
    o += '<rect x="250" y="520" width="16" height="200" fill="#3a2a22"/><path d="M 250,520 C 250,490 450,490 450,520 L 450,560 L 250,560 Z" fill="#4a3428"/>'
    o += '<rect x="250" y="640" width="220" height="70" fill="#e4dee8"/><rect x="250" y="700" width="220" height="40" fill="#8a7aa0"/><rect x="266" y="610" width="80" height="34" rx="12" fill="#f4f0f6"/>'
    o += '<path d="M 230,640 L 230,760 L 250,760 L 250,640 Z" fill="#3a2a22"/><rect x="196" y="650" width="48" height="60" fill="#5a4234"/><rect x="200" y="660" width="40" height="4" fill="#3a2a26"/>'
    o += '<ellipse cx="250" cy="800" rx="16" ry="6" fill="#8a7a9a"/><ellipse cx="280" cy="806" rx="16" ry="6" fill="#7a6a8a"/>'
    o += '<path d="M 458,560 C 470,600 460,640 466,680" stroke="#4a3328" stroke-width="2" stroke-dasharray="2 1.6" fill="none"/>'  # rosary on the bedpost
    return o

FLASH = '<g transform="translate(-50,216) rotate(-20)"><rect x="-5" y="-26" width="10" height="28" rx="3" fill="#2a2a30"/><rect x="-6.5" y="-32" width="13" height="8" rx="2" fill="#8a8a94"/><ellipse cx="0" cy="-33" rx="5.5" ry="2" fill="#fff6e6"/></g>'
BIBLE = '<g transform="translate(50,212) rotate(14)"><path d="M -24,-6 L 0,-10 L 24,-6 L 24,14 L 0,10 L -24,14 Z" fill="#3a2028"/><path d="M -21,-6 L 0,-9 L 21,-6 L 21,11 L 0,8 L -21,11 Z" fill="#f2ece0"/><path d="M -17,-3 L -4,-5 M -17,1 L -4,-1 M -17,5 L -4,3 M 4,-5 L 17,-3 M 4,-1 L 17,1 M 4,3 L 17,5" stroke="#9a9080" stroke-width=".9"/><path d="M 0,-9 L 0,9" stroke="#c8b07a" stroke-width="1"/></g>'
pose("rosa_read", "rosa", aL=-48, aR=52, extraL=FLASH, extraR=BIBLE)
pose("rosa_curtain", "rosa", aL=-150, aR=10, extraR='<g transform="translate(50,214) rotate(70)"><rect x="-5" y="-26" width="10" height="28" rx="3" fill="#2a2a30"/><rect x="-6.5" y="-32" width="13" height="8" rx="2" fill="#8a8a94"/></g>')
_rb = room_rosa() + C("rosa_read", 330, 860, 1.05)
_rb += '<path d="M 230,700 C 260,690 420,690 470,700 L 470,780 L 230,780 Z" fill="#8a7aa0"/><path d="M 230,700 C 260,690 420,690 470,700" stroke="#a89ac0" stroke-width="5" fill="none"/>' + "".join(f'<path d="M {x},704 C {x + 6},730 {x - 4},756 {x + 2},780" stroke="#6a5a84" stroke-width="2" fill="none"/>' for x in (270, 330, 400, 440))
_rb += '<polygon points="270,672 282,664 390,690 350,720" fill="#fff4dc" opacity=".35" filter="url(#lhaze)"/>'    # torch cone onto the open Bible
ST["rosa_bed"] = _rb
ST["rosa_room"] = room_rosa() + C("rosa_curtain", 200, 900, 1.08)

# ============================== 3. WALL CLOCK ==============================
INS2 = {}
INS2["clock"] = ('<rect width="540" height="960" fill="#2e2638"/>' + "".join(f'<rect x="{x}" y="0" width="24" height="960" fill="#342a3e"/>' for x in range(0, 540, 48)) +
  '<polygon points="-40,120 160,0 600,700 400,960" fill="#aab4f0" opacity=".1" filter="url(#lhaze)"/>' +
  '<ellipse cx="282" cy="440" rx="190" ry="190" fill="#0a0810" opacity=".45" filter="url(#lsoft)"/>' +
  '<g transform="translate(270,420)">'
  '<circle r="178" fill="#3a2418"/><circle r="168" fill="#5a3a26"/><circle r="168" fill="none" stroke="#7a5236" stroke-width="6" stroke-dasharray="3 9"/><circle r="152" fill="#8a6a3e"/><circle r="146" fill="#efe6d0"/>'
  '<circle r="146" fill="url(#lg_ffe6c4)" opacity=".25"/><path d="M -146,0 A 146,146 0 0 1 60,-133 A 130,130 0 0 0 -146,0 Z" fill="#d8ccb0" opacity=".5"/>'
  + "".join(f'<rect x="-1.2" y="-140" width="2.4" height="{12 if k % 5 == 0 else 6}" fill="#3a2a22" transform="rotate({k * 6})"/>' for k in range(60))
  + "".join(f'<text x="{112 * _m.sin(_m.radians(i * 30)):.0f}" y="{-112 * _m.cos(_m.radians(i * 30)) + 9:.0f}" text-anchor="middle" font-family="Georgia, serif" font-size="26" fill="#2a1e1a">{n}</text>' for i, n in enumerate(["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]))
  + '<text x="0" y="52" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#6a5a44" letter-spacing="2">ST. VERONICA 1926</text>'
  '<path d="M -6,8 L 0,-118 L 6,8 Z" fill="#1a1418"/><path d="M -8,6 L 82,-2 L 82,2 L -8,10 Z" fill="#1a1418"/><path d="M 0,26 L 0,-130" stroke="#8e1b24" stroke-width="1.6"/><circle r="9" fill="#1a1418"/><circle r="3" fill="#c8b07a"/>'
  '<path d="M -120,-80 C -100,-110 -70,-130 -40,-138" stroke="#fff" stroke-width="5" opacity=".25" fill="none"/>'
  '<path d="M -150,-60 C -140,-30 -146,10 -136,40" stroke="#c8c4d0" stroke-width=".6" fill="none" opacity=".5"/><path d="M -168,-40 L -110,-20 M -168,-40 L -120,-60" stroke="#c8c4d0" stroke-width=".6" opacity=".4"/>'
  '</g>'
  '<g transform="translate(270,610)"><rect x="-40" y="0" width="80" height="150" fill="#3a2418"/><rect x="-32" y="8" width="64" height="134" fill="#140e10"/><path d="M 0,10 L 6,110" stroke="#c8b07a" stroke-width="2"/><circle cx="6" cy="118" r="14" fill="#c8a868"/><circle cx="2" cy="114" r="5" fill="#f0dcaa"/></g>' +
  note(170, 800, "02:59 → 03:00 เข็มยาวกระดิกไปที่ XII"))

# ============================== 4. SISTERS' BUILDING AT NIGHT ==============================
def sisters_building():
    o = night_sky((110, 110), seed=5)
    o += "".join(clump(x, 470, r, "#1e2440", "#182038", "#141a30") for x, r in ((420, 80), (520, 90)))
    # three-storey colonial block, slightly low angle
    W, L_, D = "#c4c0d8", "#dcd8ec", "#8e8aac"
    o += poly("40,300 500,320 500,800 40,800", W) + poly("40,300 120,304 120,800 40,800", L_) + poly("420,316 500,320 500,800 420,800", D)
    o += poly("20,300 270,200 520,320", "#3a3448") + poly("20,300 270,200 270,214 34,306", "#4a4458")
    o += '<path d="M 270,200 L 270,160 M 258,172 L 282,172" stroke="#dcd8ec" stroke-width="4"/>'
    for i, y in enumerate((330, 470, 620)):
        o += poly(f"30,{y + 110} 510,{y + 120} 510,{y + 130} 30,{y + 120}", "#e4e0f0")   # floor slab / cornice
        if i < 2:   # upper verandas with balustrade
            o += "".join(f'<rect x="{x}" y="{y + 92}" width="4" height="22" fill="#e4e0f0"/>' for x in range(40, 500, 12)) + f'<rect x="36" y="{y + 88}" width="470" height="5" fill="#e4e0f0"/>'
        for k in range(7):
            x = 66 + k * 64
            lit = (i == 1 and k == 4)
            o += f'<path d="M {x},{y + 86} L {x},{y + 30} Q {x + 18},{y + 6} {x + 36},{y + 30} L {x + 36},{y + 86} Z" fill="{"#f4dca0" if lit else "#d4d0e2"}"/>'
            if not lit: o += f'<path d="M {x + 18},{y + 14} L {x + 18},{y + 86} M {x},{y + 54} L {x + 36},{y + 54}" stroke="#a9a4c0" stroke-width="2"/>'
            o += f'<path d="M {x - 4},{y + 30} Q {x + 18},{y + 0} {x + 40},{y + 30}" stroke="#e8e4f4" stroke-width="2.4" fill="none"/>'
            o += f'<rect x="{x - 9}" y="{y + 30}" width="8" height="56" fill="#3e4e48"/><rect x="{x + 37}" y="{y + 30}" width="8" height="56" fill="#3e4e48"/>'
            if lit:
                o += f'<circle cx="{x + 18}" cy="{y + 58}" r="60" fill="url(#lg_ffe6c4)" opacity=".8"/><path d="M {x + 10},{y + 86} L {x + 11},{y + 50} C {x + 11},{y + 42} {x + 25},{y + 42} {x + 25},{y + 50} L {x + 26},{y + 86} Z" fill="#7a5a48" opacity=".6"/>'
    # ground-floor arcade walkway
    o += "".join(f'<path d="M {x},800 L {x},716 Q {x + 26},686 {x + 52},716 L {x + 52},800 Z" fill="#bab5cc"/><rect x="{x + 52}" y="700" width="12" height="100" fill="#d8d4e8"/>' for x in range(46, 500, 64))
    # tree shadows thrown on the façade by the moon (upper left)
    o += '<g opacity=".38" fill="#0a0814"><path d="M 300,330 C 340,360 380,350 420,400 C 440,430 470,440 500,430 L 500,470 C 460,470 430,450 400,420 C 370,390 330,390 300,350 Z"/><path d="M 360,500 C 390,520 430,540 470,530 L 470,546 C 430,556 390,540 356,516 Z"/><circle cx="440" cy="380" r="40"/><circle cx="480" cy="520" r="30"/></g>'
    # big rain tree silhouette on the right
    o += '<path d="M 470,960 C 474,820 466,700 480,600 L 510,600 C 516,700 520,820 524,960 Z" fill="#14101c"/>' + "".join(clump(x, y, r, "#1e2240", "#181c36", "#12162c") for x, y, r in ((430, 520, 90), (530, 470, 110), (480, 400, 80)))
    # ground, path, frangipani, fog
    o += '<path d="M 0,800 L 540,800 L 540,960 L 0,960 Z" fill="#26283a"/><path d="M 200,800 L 340,800 L 420,960 L 120,960 Z" fill="#3a3a50"/>'
    o += haze(760, 140, "#b8bce0", .55) + haze(860, 120, "#b8bce0", .35)
    return o
ST["sisters_ext"] = sisters_building()

# ============================== 5. REFECTORY ==============================
def refectory_room():
    o = '<rect width="540" height="960" fill="#d8d0c8"/>'
    o += '<rect width="540" height="150" fill="#5a4234"/>' + "".join(f'<rect x="{x}" y="0" width="22" height="150" fill="#3e2c22"/>' for x in range(-6, 560, 108))   # beamed ceiling
    o += '<rect y="150" width="540" height="14" fill="#efe8de"/><rect y="164" width="540" height="6" fill="#a89a8a"/>'   # cornice
    for x in (40, 200, 360):   # tall arched windows with morning light
        o += f'<path d="M {x},470 L {x},250 Q {x + 70},190 {x + 140},250 L {x + 140},470 Z" fill="#a8bcd8"/><path d="M {x + 70},215 L {x + 70},470 M {x},360 L {x + 140},360" stroke="#5a4234" stroke-width="6"/><path d="M {x - 8},252 Q {x + 70},180 {x + 148},252" stroke="#efe8de" stroke-width="6" fill="none"/><rect x="{x - 10}" y="468" width="160" height="10" fill="#efe8de"/>'
    o += '<rect y="490" width="540" height="10" fill="#8a6a50"/><rect y="500" width="540" height="110" fill="#7a5a40"/>' + "".join(f'<rect x="{x}" y="510" width="80" height="90" fill="#8a6a4e"/>' for x in range(10, 540, 90))   # wainscot
    o += '<rect x="250" y="176" width="40" height="60" fill="#6a5034"/><rect x="256" y="182" width="28" height="48" fill="#3a3048"/><rect x="262" y="190" width="16" height="30" fill="#c8b8a8"/>'   # small painting
    o += '<path d="M 0,610 L 540,610 L 540,960 L 0,960 Z" fill="#8a7a6a"/>' + "".join(f'<path d="M {270 + (x - 270) * .3:.0f},610 L {x},960" stroke="#7a6a5a" stroke-width="1.6"/>' for x in range(-300, 860, 80)) + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#7a6a5a" stroke-width="1.6"/>' for y in (650, 700, 770, 860))
    for x in (130, 410):   # pendant lamps
        o += f'<path d="M {x},150 L {x},230" stroke="#2a2024" stroke-width="2"/><path d="M {x - 26},250 C {x - 26},226 {x + 26},226 {x + 26},250 Z" fill="#3a3a30"/><ellipse cx="{x}" cy="250" rx="26" ry="5" fill="#fff4dc"/>'
    o += '<g transform="translate(470,610)"><rect x="-40" y="-110" width="80" height="110" fill="#5a4030"/><rect x="-36" y="-104" width="76" height="40" fill="#3e2c22"/>' + "".join(f'<ellipse cx="{-24 + i * 16}" cy="-84" rx="6" ry="12" fill="#efe8f0"/>' for i in range(4)) + '<rect x="-36" y="-60" width="72" height="4" fill="#3e2c22"/></g>'   # sideboard with plates
    o += '<g transform="translate(60,610)"><rect x="-3" y="-80" width="6" height="80" fill="#3a2a22"/><path d="M -20,-100 L 20,-100 L 14,-80 L -14,-80 Z" fill="#5a4234"/><path d="M -16,-104 L 16,-104 L 0,-110 Z" fill="#efe8da"/></g>'   # reading lectern
    return o

def refectory_table():
    o = '<path d="M 10,700 L 530,700 L 540,746 L 0,746 Z" fill="#f4f0e8"/><path d="M 0,746 L 540,746 L 540,770 L 0,770 Z" fill="#e2dcd0"/>'   # tablecloth top + drop
    o += "".join(f'<path d="M {x},770 L {x + 6},792" stroke="#d4ccc0" stroke-width="1.4"/>' for x in range(4, 540, 14))
    o += '<rect x="20" y="770" width="12" height="150" fill="#4a3428"/><rect x="508" y="770" width="12" height="150" fill="#4a3428"/><rect x="262" y="770" width="12" height="150" fill="#3a2820"/>'
    for x in (70, 170, 270, 370, 470):
        o += f'<ellipse cx="{x}" cy="722" rx="24" ry="7" fill="#e8e2ea"/><ellipse cx="{x}" cy="719" rx="17" ry="4" fill="#d8c8a8"/><path d="M {x + 28},716 l 2,14" stroke="#a8a4ac" stroke-width="2"/>'
    o += '<g transform="translate(220,708)"><path d="M -12,0 C -14,-18 14,-18 12,0 Z" fill="#e8e2ea"/><path d="M 12,-8 L 22,-14 L 20,-8 Z" fill="#e8e2ea"/><rect x="-4" y="-22" width="8" height="5" fill="#c8c4cc"/></g>'
    o += '<g transform="translate(320,712)"><path d="M -18,0 L 18,0 L 14,-10 L -14,-10 Z" fill="#a8845a"/>' + "".join(f'<ellipse cx="{-8 + i * 8}" cy="-12" rx="5" ry="3" fill="#d8b888"/>' for i in range(3)) + '</g>'
    o += '<g transform="translate(120,706)"><path d="M -6,0 L -7,-22 L 7,-22 L 6,0 Z" fill="#c8d4e0" opacity=".85"/><rect x="-7" y="-24" width="14" height="3" fill="#e8eef4"/></g><g transform="translate(420,706)"><path d="M -6,0 L -7,-22 L 7,-22 L 6,0 Z" fill="#c8d4e0" opacity=".85"/></g>'
    return o

ST["refectory"] = (refectory_room() + C("cat", 270, 790, .66) + C("mariam", 120, 820, .7, .95) + C("rosa", 420, 820, .7) + C("daeng", 506, 800, .68) + C("agnes", 40, 810, .68, .9)
                   + refectory_table() + '<polygon points="200,250 340,250 400,700 140,700" fill="#fff4e0" opacity=".14" filter="url(#lhaze)"/>')

# ============================== 6. JAMES'S CONDO ==============================
TAW = v1.tf[v1.tf.index('<clipPath id="tface"'):v1.tf.index('<!-- background treatment')]
def photo_frame(x, y, w, h, r=0):
    """Framed photo on the wall: James, Tawan and the orange cat, a natural snapshot."""
    s = w / 120
    return (f'<g transform="translate({x},{y}) rotate({r})"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" fill="#2a2420"/><rect x="{-w / 2 + 5}" y="{-h / 2 + 5}" width="{w - 10}" height="{h - 10}" fill="#c8d8e8"/>'
            f'<rect x="{-w / 2 + 5}" y="{h * .1:.0f}" width="{w - 10}" height="{h * .4 - 5:.0f}" fill="#a8b0a0"/>'
            f'<g transform="translate({-w * .18:.0f},{h * .02:.0f}) scale({.3 * s:.2f})"><use href="#jhead"/></g>'
            f'<g transform="translate({w * .16:.0f},{h * .04:.0f}) scale({.28 * s:.2f})"><use href="#tback"/><use href="#thead"/></g>'
            f'<g transform="translate({-w * .02:.0f},{h * .3:.0f}) scale({.16 * s:.2f})"><circle r="40" fill="#e79a4a"/><circle cx="-14" cy="-6" r="6" fill="#3a2a22"/><circle cx="14" cy="-6" r="6" fill="#3a2a22"/><ellipse cx="0" cy="16" rx="18" ry="12" fill="#f7e3c4"/></g></g>')

def condo_room():
    o = '<rect width="540" height="960" fill="#3a3466"/><rect width="540" height="100" fill="#2a2650"/><rect y="98" width="540" height="6" fill="#4a4480"/>'
    # balcony door + window with the city at night, curtains
    o += f'<svg x="20" y="150" width="210" height="430" viewBox="0 0 210 430"><rect width="210" height="430" fill="#141a44"/>{stars(10, 120, 4)}' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{430 - y}" fill="#1e2656"/>' for x, y, w in ((0, 200, 40), (46, 140, 46), (100, 230, 34), (140, 120, 56), (196, 250, 20))) + "".join(f'<rect x="{x}" y="{y}" width="4" height="5" fill="#ffe6b8" opacity=".75"/>' for x, y in ((10, 230), (22, 270), (58, 170), (70, 210), (60, 260), (112, 260), (150, 150), (168, 190), (156, 240), (176, 300))) + '<rect y="330" width="210" height="8" fill="#5a5a70"/>' + "".join(f'<rect x="{x}" y="338" width="4" height="60" fill="#5a5a70"/>' for x in range(4, 210, 16)) + '<rect y="396" width="210" height="34" fill="#2a2a40"/></svg>'
    o += '<rect x="14" y="144" width="222" height="442" fill="none" stroke="#1e1a3a" stroke-width="10"/><path d="M 125,150 L 125,580" stroke="#1e1a3a" stroke-width="8"/><rect x="108" y="350" width="6" height="34" rx="3" fill="#8a8aa4"/>'
    o += curtains(20, 150, 230, 580, ("#4a4a7a", "#5e5e90", "#363664"))
    # wall: shelf with figures + controller, framed photos of James, Tawan and the cat, LED strip
    o += '<rect x="250" y="120" width="290" height="5" fill="#9a86ff"/><rect x="250" y="125" width="290" height="18" fill="#5a4ea8" opacity=".5"/>'
    o += photo_frame(300, 230, 90, 70, -3) + photo_frame(380, 210, 60, 76, 4)
    o += '<rect x="430" y="270" width="100" height="6" fill="#2a2440"/>' + '<rect x="440" y="246" width="10" height="24" fill="#c86a8a"/><circle cx="445" cy="242" r="6" fill="#c86a8a"/><rect x="460" y="254" width="16" height="16" fill="#6ad0ff"/><path d="M 488,262 c 0,-8 18,-8 18,0 c 0,6 -18,6 -18,0 Z" fill="#2a2a34"/>'
    # floor + rug
    o += '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#2c2848"/>' + "".join(f'<path d="M {270 + (x - 270) * .4:.0f},640 L {x},960" stroke="#24203e" stroke-width="2"/>' for x in range(-200, 760, 70))
    o += '<path d="M 40,780 L 500,780 L 540,930 L 0,930 Z" fill="#5a5088"/><path d="M 60,790 L 480,790 L 514,920 L 26,920 Z" fill="none" stroke="#7a70a8" stroke-width="4"/>'
    # bed at the back right with bedding
    o += '<rect x="400" y="520" width="140" height="120" fill="#3a3460"/><rect x="400" y="560" width="140" height="80" fill="#c8c4e0"/><rect x="410" y="540" width="60" height="26" rx="10" fill="#e8e4f4"/><path d="M 400,600 C 440,590 500,600 540,594 L 540,640 L 400,640 Z" fill="#6a6aa8"/>'
    # computer desk with two monitors + PC tower, gaming chair, floor lamp
    o += '<rect x="250" y="500" width="160" height="12" fill="#2a2440"/><rect x="258" y="512" width="8" height="128" fill="#1e1a30"/><rect x="394" y="512" width="8" height="128" fill="#1e1a30"/>'
    o += '<rect x="262" y="420" width="80" height="54" rx="3" fill="#0e0c1c"/><rect x="266" y="424" width="72" height="44" fill="#6a5ae0"/><path d="M 270,460 l 14,-12 l 10,8 l 14,-16 l 16,20" stroke="#c8f0ff" stroke-width="2" fill="none"/><rect x="298" y="474" width="8" height="26" fill="#1e1a30"/>'
    o += '<rect x="346" y="430" width="56" height="40" rx="3" fill="#0e0c1c"/><rect x="349" y="433" width="50" height="34" fill="#3a8ae0"/>' + "".join(f'<rect x="352" y="{437 + k * 7}" width="{20 + (k * 13) % 24}" height="4" fill="{c}"/>' for k, c in enumerate(("#ff7ab0", "#7affc8", "#ffe07a", "#ff7ab0"))) + '<rect x="370" y="470" width="6" height="30" fill="#1e1a30"/>'
    o += '<rect x="372" y="560" width="30" height="72" fill="#16142a"/><rect x="376" y="566" width="4" height="60" fill="#ff5aa0"/>'
    o += '<rect x="276" y="490" width="66" height="8" rx="2" fill="#14122a"/><rect x="278" y="496" width="62" height="1.6" fill="#8a7bff"/><ellipse cx="356" cy="494" rx="6" ry="3.5" fill="#14122a"/><path d="M 236,500 L 248,500 L 246,488 L 238,488 Z" fill="#e8e4dc"/>'
    o += '<path d="M 520,640 L 520,400" stroke="#2a2440" stroke-width="4"/><path d="M 500,400 L 540,400 L 530,370 L 510,370 Z" fill="#e8d8c0"/>'
    return o

def condo_front():
    # sofa (left), coffee table with snacks and controllers (front)
    o = '<path d="M 0,700 L 250,700 L 260,800 L 0,800 Z" fill="#4a4280"/><path d="M 0,660 C 0,640 240,640 244,662 L 250,710 L 0,710 Z" fill="#5a52a0"/><rect x="0" y="790" width="262" height="40" fill="#3a3466"/>'
    o += '<rect x="30" y="680" width="50" height="36" rx="10" fill="#c88ab0"/>'
    o += '<path d="M 170,850 L 420,850 L 440,880 L 150,880 Z" fill="#6a5a8a"/><rect x="160" y="880" width="270" height="10" fill="#4a3e66"/><rect x="172" y="890" width="8" height="40" fill="#2a2440"/><rect x="412" y="890" width="8" height="40" fill="#2a2440"/>'
    o += '<path d="M 220,858 c 0,-6 22,-6 22,0 c 0,5 -22,5 -22,0 Z" fill="#2a2a34"/><rect x="270" y="852" width="20" height="14" fill="#e85a6a"/><rect x="300" y="848" width="10" height="18" rx="3" fill="#7ae0a0"/><path d="M 340,862 l 30,-4 l 2,6 l -30,4 Z" fill="#efe8da"/>'
    return o

pose("james_desk", "james", aL=-24, aR=20, head=-6)
ST["condo"] = condo_room() + '<path d="M 290,560 C 290,520 380,520 380,560 L 386,700 L 284,700 Z" fill="#1e1a3a"/><rect x="296" y="564" width="6" height="134" fill="#9a86ff"/>' + C("james_desk", 336, 830, .82) + C("mek_phone", 120, 880, .82) + condo_front() + f'<g transform="translate(220,640) scale(.9)">{v1.CAT}</g>'

# ============================== 12. VIDEO CALL (phone POV) ==============================
def call_screen():
    o = '<rect width="540" height="960" fill="#05040a"/>'
    # James full-screen, front camera: close, slightly below eye level, his room behind (same room as the condo)
    o += '<svg x="0" y="0" width="540" height="960" viewBox="230 300 260 462" preserveAspectRatio="xMidYMid slice">' + condo_room() + '</svg>'
    o += '<rect width="540" height="960" fill="#1a1440" opacity=".35"/>'
    o += C("james_desk", 280, 1460, 2.4)
    o += '<circle cx="380" cy="300" r="320" fill="url(#lg_b4a8ff)" opacity=".6" style="mix-blend-mode:screen"/>'
    # picture-in-picture: Mek in his dark guest room, top-right, clear of James's face
    o += '<g transform="translate(372,96)"><rect width="140" height="210" rx="14" fill="#141018"/><svg x="0" y="0" width="140" height="210" viewBox="0 0 140 210"><rect width="140" height="210" fill="#2a2430"/>' + put(P["mek_phone"], 70, 520, 1.15, .75) + '<circle cx="70" cy="80" r="70" fill="url(#lg_cfe0ff)" opacity=".6"/></svg><rect width="140" height="210" rx="14" fill="none" stroke="#fff" stroke-opacity=".6" stroke-width="2"/></g>'
    # phone UI: status bar, name + call timer, call buttons at the very bottom (below the subtitle area)
    o += '<text x="40" y="44" font-family="Inter, sans-serif" font-size="17" font-weight="600" fill="#fff">02:59</text><rect x="470" y="32" width="34" height="15" rx="4" fill="none" stroke="#fff" stroke-width="1.6"/><rect x="473" y="35" width="20" height="9" rx="2" fill="#fff"/>'
    o += '<text x="40" y="96" font-family="IBM Plex Sans Thai, sans-serif" font-size="20" font-weight="700" fill="#fff">เจมส์</text><text x="40" y="120" font-family="Inter, sans-serif" font-size="14" fill="#e0e0ee">12:48</text>'
    for i, (col, icon) in enumerate((("#3a3a48", "M -8,-4 L 8,-4 M 0,-12 L 0,4"), ("#3a3a48", "M -10,-6 L 4,-6 L 4,6 L -10,6 Z M 4,-2 L 12,-7 L 12,7 L 4,2"), ("#e5484d", "M -12,2 C -6,-6 6,-6 12,2"), ("#3a3a48", "M -6,-10 L -6,10 M 6,-10 L 6,10"))):
        x = 110 + i * 107
        o += f'<circle cx="{x}" cy="880" r="30" fill="{col}" opacity=".92"/><path d="{icon}" transform="translate({x},880)" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return o
ST["call"] = call_screen()

# ============================== 7. ARRIVAL: three people on one ground plane ==============================
def gate_bg():
    o = '<rect width="540" height="960" fill="#9a8aae"/>' + sky("#86a8e6", "#b8c2ee", "#ece4f4", clouds=((30, 120, 170, "#ffffff", .7), (300, 90, 200, "#ffffff", .6)))
    o += "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{480 - y}" fill="#8a7ea8" opacity=".55"/>' for x, y, w in ((0, 260, 50), (470, 240, 60)))
    o += f'<g opacity=".95">{church(310, 410, .62)}</g>' + haze(400, 90, "#d8c4dc", .3)
    o += '<path d="M 0,560 L 540,560 L 540,960 L 0,960 Z" fill="#8a8494"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#6e6878" stroke-width="1.4"/>' for y in (600, 660, 740, 840, 940)) + "".join(f'<path d="M {270 + (x - 270) * .25:.0f},560 L {x},960" stroke="#6e6878" stroke-width="1.2"/>' for x in range(-400, 940, 90))
    o += fence(470, 640) + '<rect x="250" y="560" width="30" height="40" rx="4" fill="#2a2420"/><path d="M 256,560 C 256,546 274,546 274,560" fill="none" stroke="#2a2420" stroke-width="4"/>'
    o += '<g transform="translate(440,500)"><rect x="-3" y="0" width="4" height="60" fill="#16121a"/><rect x="-56" y="-30" width="112" height="34" rx="3" fill="#efe8da"/><rect x="-56" y="-30" width="112" height="7" fill="#8e1b24"/><text x="0" y="-10" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" font-weight="700" fill="#3a2a22">เขตพักซิสเตอร์</text><text x="0" y="0" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7" fill="#5a4a3a">ห้ามบุคคลภายนอก</text></g>'
    o += frangipani(40, 470, 1.0) + "".join(flower5(RR.uniform(10, 520), RR.uniform(700, 940), 1.3) for _ in range(8))
    return o
# all three stand on the same paving, feet within the same depth band, scaled by that depth
ST["gate"] = gate_bg() + C("daeng_hug", 120, 900, .92) + C("mek", 255, 910, .96) + C("cat_point", 420, 905, .94) + '<polygon points="120,900 240,900 300,940 150,946" fill="#2a2032" opacity=".25" filter="url(#lsoft)"/>'

# ============================== 8. GUEST HOUSE (Father Joseph) ==============================
def guest_room():
    o = '<rect width="540" height="960" fill="#c8b8a8"/><rect width="540" height="110" fill="#6a5040"/><rect y="108" width="540" height="10" fill="#efe4d8"/>'
    o += '<rect y="560" width="540" height="8" fill="#8a6a50"/><rect y="568" width="540" height="72" fill="#7a5a44"/>' + "".join(f'<rect x="{x}" y="576" width="60" height="56" fill="#8a6a4e"/>' for x in range(10, 540, 70))
    # window to the old wing at dusk
    o += f'<svg x="170" y="150" width="200" height="270" viewBox="0 0 200 270"><rect width="200" height="270" fill="#8a7aa8"/>' + old_wing(-10, 100, .85) + '</svg><rect x="164" y="144" width="212" height="282" fill="none" stroke="#5a4234" stroke-width="10"/><path d="M 270,150 L 270,420 M 170,280 L 370,280" stroke="#5a4234" stroke-width="6"/><rect x="156" y="420" width="228" height="10" fill="#efe4d8"/>'
    o += curtains(170, 150, 370, 420, ("#8a6a5a", "#a88a78", "#6a4e42"))
    # wall: crucifix, framed print, wall lamp; bookshelf (left) + filing cabinet
    o += '<rect x="436" y="170" width="6" height="56" fill="#3a2a22"/><rect x="424" y="184" width="30" height="6" fill="#3a2a22"/>'
    o += '<rect x="420" y="250" width="74" height="96" fill="#6a5034"/><rect x="426" y="256" width="62" height="84" fill="#5a6a8a"/><path d="M 432,334 L 456,290 L 470,312 L 482,300 L 482,334 Z" fill="#8a9ab8"/>'
    o += '<path d="M 510,300 L 520,300 L 520,330" stroke="#3a2a22" stroke-width="3" fill="none"/><path d="M 508,330 L 532,330 L 526,350 L 514,350 Z" fill="#efe0c0"/>'
    o += '<rect x="10" y="150" width="130" height="410" fill="#5a4030"/>' + "".join(f'<rect x="10" y="{y}" width="130" height="6" fill="#3e2c22"/>' for y in (230, 320, 410, 500)) + "".join(f'<rect x="{14 + (k * 17) % 116}" y="{y - 52 + (k % 3) * 4}" width="{10 + k % 4 * 2}" height="{48 - (k % 3) * 4}" fill="{c}"/>' for y in (230, 320, 410, 500) for k, c in enumerate(("#6a2a32", "#2a3a5a", "#3a4a3a", "#8a6a3a", "#5a2a4a", "#2a4a5a", "#7a5a2a")))
    o += '<rect x="80" y="440" width="56" height="120" fill="#7a7a84"/>' + "".join(f'<rect x="84" y="{450 + k * 36}" width="48" height="30" fill="#8a8a94"/><rect x="100" y="{462 + k * 36}" width="16" height="4" fill="#3a3a40"/>' for k in range(3))
    # floor
    o += '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#7a5a44"/>' + "".join(f'<path d="M {270 + (x - 270) * .35:.0f},640 L {x},960" stroke="#6a4a36" stroke-width="2"/>' for x in range(-300, 860, 70))
    o += '<path d="M 70,760 L 470,760 L 520,920 L 20,920 Z" fill="#8a3a3e" opacity=".85"/><path d="M 90,772 L 450,772 L 494,906 L 46,906 Z" fill="none" stroke="#c8a868" stroke-width="3"/>'
    # Father's desk (right) with lamp, papers, Bible; chair
    o += '<rect x="390" y="560" width="150" height="14" fill="#4a3428"/><rect x="396" y="574" width="140" height="90" fill="#3a2820"/><rect x="404" y="590" width="58" height="66" fill="#4a3428"/><circle cx="455" cy="622" r="2.5" fill="#c8b07a"/>'
    o += '<path d="M 500,560 L 504,520 L 492,500" stroke="#2a2024" stroke-width="3" fill="none"/><path d="M 478,494 L 506,504 L 500,516 L 474,506 Z" fill="#2a4a3a"/><rect x="420" y="552" width="40" height="8" fill="#efe8da" transform="rotate(-4 440 556)"/><rect x="466" y="550" width="18" height="10" fill="#5a2a2e"/>'
    o += '<path d="M 440,600 C 440,580 480,580 480,600 L 484,700 L 436,700 Z" fill="#5a3a2a" opacity=".0"/>'
    return o

def guest_front():
    # armchair (left), coffee table with teapot and cups (front)
    o = '<path d="M 0,700 L 90,700 L 96,820 L 0,820 Z" fill="#6a4a3a"/><path d="M 0,660 C 0,640 86,640 90,662 L 94,712 L 0,712 Z" fill="#7a5a48"/><rect x="0" y="812" width="100" height="30" fill="#4a3428"/>'
    o += '<path d="M 180,850 L 380,850 L 396,876 L 164,876 Z" fill="#5a4030"/><rect x="172" y="876" width="216" height="10" fill="#3e2c22"/><rect x="180" y="886" width="8" height="44" fill="#2a1e18"/><rect x="372" y="886" width="8" height="44" fill="#2a1e18"/>'
    o += '<g transform="translate(250,852)"><path d="M -12,0 C -14,-18 14,-18 12,0 Z" fill="#efe8f0"/><path d="M 12,-8 L 22,-14 L 20,-8 Z" fill="#efe8f0"/></g><ellipse cx="300" cy="856" rx="12" ry="4" fill="#efe8f0"/><ellipse cx="330" cy="858" rx="12" ry="4" fill="#efe8f0"/>'
    return o

KEY = '<g transform="translate(50,226)"><circle cx="0" cy="-2" r="5.5" fill="none" stroke="#d8bc70" stroke-width="2.4"/><path d="M 4,2 L 16,14 L 13,17 L 10,14 L 8,16 L 6,14" fill="none" stroke="#d8bc70" stroke-width="2.4"/></g>'
pose("jos_give", "jos", aR=-20, extraR=KEY)
pose("mek_take", "mek", aL=19)
ST["guestroom"] = guest_room() + C("jos_give", 180, 900, .95) + C("mek_take", 360, 908, .97) + guest_front()

# ============================== 9. PIANO (side view) ==============================
def mariam_profile_seated():
    """Mariam seen in full profile, seated on a piano bench, hands on the keys (facing right)."""
    o = '<g>'
    o += '<path d="M -40,-150 C -48,-200 -10,-226 18,-214 C 30,-208 34,-196 32,-180 L 26,-60 L -60,-40 C -66,-90 -54,-130 -40,-150 Z" fill="#1a1520"/>'   # veil falling down the back
    o += '<path d="M -34,-40 C -36,-90 -10,-110 20,-104 L 40,-40 C 44,0 40,30 30,46 L -44,46 C -50,10 -44,-16 -34,-40 Z" fill="#e6e0d5"/><path d="M -34,-40 C -36,-80 -20,-100 0,-104 L -6,46 L -44,46 C -50,10 -44,-16 -34,-40 Z" fill="#f6f1e8"/>'   # robe torso
    o += '<path d="M -44,46 L 70,46 C 80,46 84,56 82,66 L 78,74 L -46,74 Z" fill="#e6e0d5"/><path d="M -44,46 L 70,46 L 70,56 L -44,56 Z" fill="#f6f1e8"/>'   # lap / thighs forward
    o += '<path d="M 64,70 L 80,70 L 86,150 L 70,150 Z" fill="#d8d0c4"/><path d="M 66,148 L 96,148 C 100,152 100,158 96,160 L 64,160 Z" fill="#1d1a20"/>'   # shin + shoe
    o += '<path d="M 10,-80 C 26,-70 40,-50 58,-34 L 80,-30 L 80,-20 L 54,-22 C 34,-38 16,-54 2,-66 Z" fill="#f2ece2"/><ellipse cx="84" cy="-25" rx="9" ry="5" fill="#f6dcc4"/><path d="M 80,-29 C 86,-32 92,-30 92,-26" stroke="#d98f86" stroke-width="2" fill="none"/>'   # arm + hand on keys (scar)
    # head in profile inside the wimple
    o += '<path d="M -10,-196 C -10,-232 40,-238 46,-200 C 50,-176 46,-160 30,-150 L -2,-146 C -12,-160 -12,-178 -10,-196 Z" fill="#ece6dc"/>'   # wimple
    o += '<path d="M 18,-206 C 30,-210 42,-202 44,-188 L 48,-178 L 44,-176 L 46,-168 C 44,-160 38,-156 30,-158 C 22,-160 16,-170 16,-186 Z" fill="#f6dcc4"/>'   # face profile
    o += '<path d="M 36,-190 C 38,-192 41,-191 42,-189" stroke="#1d1418" stroke-width="2" fill="none" stroke-linecap="round"/><path d="M 30,-196 C 34,-199 40,-199 43,-196" stroke="#3a2a26" stroke-width="1.6" fill="none"/>'
    o += '<path d="M 40,-166 L 45,-166" stroke="#b5767a" stroke-width="1.8" stroke-linecap="round"/><ellipse cx="32" cy="-174" rx="5" ry="2.6" fill="#ec948c" opacity=".45"/>'
    o += '<path d="M -14,-210 C -16,-240 30,-250 48,-214 L 46,-204 C 32,-232 0,-230 -6,-200 Z" fill="#f3eee6"/><path d="M -20,-200 C -24,-246 34,-260 54,-214 L 48,-208 C 30,-244 -6,-236 -12,-196 Z" fill="#1a1520"/>'
    return o + '</g>'

def upright_piano():
    """Upright piano in three-quarter side view: case, music desk, keyboard shelf, keys, pedals."""
    o = '<g>'
    o += '<path d="M 0,0 L 150,-20 L 150,240 L 0,250 Z" fill="#1e1418"/><path d="M 150,-20 L 200,-6 L 200,250 L 150,240 Z" fill="#2c1e22"/>'   # side + front of the case
    o += '<path d="M -6,-6 L 150,-28 L 206,-12 L 50,10 Z" fill="#3a2a2c"/>'   # lid
    o += '<path d="M 150,30 L 200,40 L 200,110 L 150,100 Z" fill="#3a2a2e"/><path d="M 156,46 L 194,54 L 194,96 L 156,88 Z" fill="#f2ece0"/><path d="M 160,56 l 30,6 M 160,64 l 30,6 M 160,72 l 30,6 M 160,80 l 30,6" stroke="#5a5050" stroke-width=".8"/>'   # music desk with sheet music
    o += '<path d="M 150,120 L 240,138 L 240,150 L 150,134 Z" fill="#2a1c20"/><path d="M 150,134 L 240,150 L 240,170 L 150,154 Z" fill="#1a1216"/>'   # keyboard shelf
    o += '<path d="M 152,122 L 238,139 L 238,146 L 152,130 Z" fill="#f4f0e6"/>' + "".join(f'<path d="M {152 + k * 8.6:.1f},{122 + k * 1.7:.1f} L {152 + k * 8.6:.1f},{130 + k * 1.6:.1f}" stroke="#8a8478" stroke-width=".8"/>' for k in range(1, 10))
    o += "".join(f'<path d="M {155 + k * 8.6:.1f},{122 + k * 1.7:.1f} L {160 + k * 8.6:.1f},{123 + k * 1.7:.1f} L {160 + k * 8.6:.1f},{127 + k * 1.7:.1f} L {155 + k * 8.6:.1f},{126 + k * 1.7:.1f} Z" fill="#141014"/>' for k in (0, 1, 3, 4, 5, 7, 8))
    o += '<path d="M 160,180 L 160,240 M 194,186 L 194,244" stroke="#3a2a2e" stroke-width="6"/><circle cx="170" cy="244" r="3" fill="#c8b07a"/><circle cx="182" cy="246" r="3" fill="#c8b07a"/>'   # legs + pedals
    o += '<rect x="166" y="-50" width="5" height="26" fill="#efe8da"/><path d="M 168.5,-62 C 165,-56 165,-53 168.5,-51 C 172,-53 172,-56 168.5,-62 Z" fill="#fff6e6"/><rect x="160" y="-26" width="18" height="4" fill="#a8945e"/>'   # candle on the piano
    o += '<path d="M 40,40 C 70,30 100,34 120,30" stroke="#c8b07a" stroke-width="2" fill="none" opacity=".6"/>'   # fretwork
    return o + '</g>'

def music_room():
    o = '<rect width="540" height="960" fill="#5a4e62"/><rect width="540" height="120" fill="#3e3448"/><rect y="118" width="540" height="10" fill="#7a6e84"/>'
    o += '<path d="M 300,460 L 300,220 Q 380,160 460,220 L 460,460 Z" fill="#2a3060"/><path d="M 380,190 L 380,460 M 300,340 L 460,340" stroke="#3a3040" stroke-width="7"/><path d="M 292,222 Q 380,148 468,222" stroke="#8a7e94" stroke-width="6" fill="none"/>'   # evening window
    o += '<rect x="20" y="160" width="160" height="110" fill="#6a5034"/><rect x="26" y="166" width="148" height="98" fill="#f2ece0"/>' + "".join(f'<path d="M 34,{180 + k * 14} L 166,{180 + k * 14}" stroke="#3a3a3a" stroke-width="1"/>' for k in range(5)) + '<path d="M 50,186 l 0,-12 M 80,200 l 0,-14 M 120,190 l 0,-12" stroke="#1a1a1a" stroke-width="2"/>'   # music chalkboard
    o += '<rect y="600" width="540" height="10" fill="#7a6e84"/><path d="M 0,610 L 540,610 L 540,960 L 0,960 Z" fill="#4a3c40"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#3e3236" stroke-width="2"/>' for y in (650, 700, 770, 860))
    o += '<rect x="470" y="250" width="70" height="360" fill="#2a2228"/><rect x="476" y="256" width="64" height="354" fill="#141014"/>'   # door at the right (Agnes)
    o += '<g transform="translate(40,520)"><rect x="0" y="0" width="60" height="90" fill="#3a2a22"/>' + "".join(f'<rect x="{4 + k * 9}" y="{6 + (k % 2) * 6}" width="7" height="{78 - (k % 2) * 6}" fill="{c}"/>' for k, c in enumerate(("#6a2a32", "#2a3a5a", "#efe8da", "#3a4a3a", "#5a2a4a", "#efe8da"))) + '</g>'   # sheet-music cabinet
    o += '<g transform="translate(450,610)"><path d="M -6,0 L 0,-60 L 6,0 Z" fill="#2a2228"/><path d="M -16,-60 L 16,-60 L 12,-50 L -12,-50 Z" fill="#3a2a2c"/></g>'   # music stand
    return o
_mu = music_room() + C("agnes", 506, 610, .6, .8)
_mu += '<g transform="translate(250,450)">' + upright_piano() + '</g>'
_mu += '<g transform="translate(176,640) scale(1.15)">' + mariam_profile_seated() + '</g>'
_mu += '<path d="M 150,690 L 260,690 L 256,704 L 154,704 Z" fill="#3a2a2c"/><path d="M 160,704 L 160,780 M 248,704 L 248,780" stroke="#2a1c20" stroke-width="6"/>'   # piano bench
_mu += '<polygon points="300,230 460,230 520,900 240,900" fill="#9aa4e0" opacity=".1" filter="url(#lhaze)"/>'
ST["music"] = _mu

# ============================== 10. VERANDA ==============================
def veranda():
    o = night_sky((420, 140), seed=9)
    o += "".join(clump(x, y, r, "#1e2440", "#182038", "#141a30") for x, y, r in ((40, 470, 90), (150, 500, 70), (500, 460, 100)))
    o += f'<g opacity=".9">{old_wing(250, 330, .7)}</g>'
    # house wall on the left with a door spilling warm light, verandah floor, columns, waist-high balustrade
    o += '<path d="M 0,120 L 70,150 L 70,960 L 0,960 Z" fill="#c8bca8"/><path d="M 10,520 L 54,530 L 54,800 L 10,800 Z" fill="#f2d8a8"/><path d="M 10,520 L 54,530 L 54,800 L 10,800 Z" fill="none" stroke="#5a4234" stroke-width="5"/>'
    o += '<polygon points="54,800 54,530 260,900 120,960" fill="#fff0d0" opacity=".12" filter="url(#lhaze)"/>'
    o += '<path d="M 0,90 L 540,120 L 540,150 L 0,124 Z" fill="#5a4234"/><path d="M 0,124 L 540,150 L 540,160 L 0,134 Z" fill="#3e2c22"/>'   # roof edge / fascia
    o += '<path d="M 0,700 L 540,700 L 540,960 L 0,960 Z" fill="#9a7a6a"/>' + "".join(f'<path d="M {270 + (x - 270) * .3:.0f},700 L {x},960" stroke="#8a6a5a" stroke-width="1.6"/>' for x in range(-300, 860, 60)) + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#8a6a5a" stroke-width="1.6"/>' for y in (730, 770, 830, 910))
    for x in (110, 520):   # columns
        o += f'<rect x="{x - 12}" y="150" width="24" height="550" fill="#e4dcd0"/><rect x="{x - 12}" y="150" width="8" height="550" fill="#f4ece2"/><rect x="{x - 18}" y="150" width="36" height="14" fill="#efe4d8"/><rect x="{x - 16}" y="686" width="32" height="14" fill="#d8ccc0"/>'
    o += '<rect x="70" y="590" width="470" height="12" fill="#e4dcd0"/>' + "".join(f'<path d="M {x},602 C {x - 5},616 {x + 5},632 {x},646 L {x},690" stroke="#d8ccc0" stroke-width="7"/>' for x in range(90, 540, 22)) + '<rect x="70" y="690" width="470" height="10" fill="#c8bcb0"/>'
    o += '<path d="M 300,150 L 300,220" stroke="#2a2024" stroke-width="2"/>'   # hook for a hanging plant
    o += '<g transform="translate(300,232)"><path d="M -18,0 L 18,0 L 12,18 L -12,18 Z" fill="#8a604a"/>' + "".join(f'<path d="M {dx},6 C {dx * 2},20 {dx * 2.4},40 {dx * 2.2},60" stroke="#3e5a3e" stroke-width="3" fill="none"/>' for dx in (-10, -4, 4, 10)) + '</g>'
    return o
_ve = veranda() + C("jos", 160, 880, .92, .9) + C("mek", 380, 890, .94, .9)
_ve += '<path d="M 90,760 L 460,760 L 480,790 L 70,790 Z" fill="#5a4234"/><rect x="70" y="790" width="410" height="12" fill="#3e2c22"/>' + "".join(f'<rect x="{x}" y="802" width="10" height="120" fill="#2a1e18"/>' for x in (84, 456)) + '<rect x="260" y="802" width="10" height="120" fill="#2a1e18" opacity=".0"/>'
_ve += '<ellipse cx="200" cy="772" rx="34" ry="8" fill="#e8e0d4"/><ellipse cx="200" cy="769" rx="24" ry="4" fill="#5e8a4a"/><ellipse cx="350" cy="772" rx="34" ry="8" fill="#e8e0d4"/><ellipse cx="350" cy="769" rx="24" ry="4" fill="#5e8a4a"/>'
_ve += '<g transform="translate(275,770)"><rect x="-14" y="-50" width="28" height="50" fill="none" stroke="#3a3030" stroke-width="3"/><path d="M -16,-50 L 0,-62 L 16,-50 Z" fill="#3a3030"/>' + candle(0, 0) + '</g>'
_ve += '<path d="M 70,822 L 120,822 L 124,900 L 66,900 Z M 420,822 L 470,822 L 474,900 L 416,900 Z" fill="#4a3428"/>'   # chairs
ST["veranda"] = _ve

# ============================== 11. KITCHEN (table fixed) ==============================
def kitchen_room():
    o = '<rect width="540" height="960" fill="#d6d2c8"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#b8b2a6" stroke-width="1"/>' for y in range(100, 640, 22)) + "".join(f'<path d="M {x},80 L {x},640" stroke="#b8b2a6" stroke-width="1"/>' for x in range(0, 541, 22))
    o += '<rect width="540" height="80" fill="#3a3030"/><rect y="420" width="540" height="24" fill="#8aa08a"/>'
    o += f'<svg x="400" y="130" width="110" height="140" viewBox="0 0 110 140"><rect width="110" height="140" fill="#1e2244"/>{stars(8, 60, 6)}<circle cx="80" cy="30" r="9" fill="#eef0ff"/></svg><rect x="394" y="124" width="122" height="152" fill="none" stroke="#3a3030" stroke-width="8"/><path d="M 455,130 L 455,270" stroke="#3a3030" stroke-width="5"/>'
    o += '<rect x="20" y="200" width="200" height="8" fill="#5a4234"/><rect x="20" y="300" width="200" height="8" fill="#5a4234"/>'
    for (x, y, w, h, c) in ((30, 168, 40, 32, "#9a9aa4"), (78, 160, 46, 40, "#b8b8c0"), (132, 172, 34, 28, "#8a8a94"), (172, 166, 40, 34, "#a8604a"), (32, 266, 30, 34, "#e8e0d0"), (68, 272, 30, 28, "#e8e0d0"), (106, 258, 50, 42, "#7a7a86"), (164, 270, 46, 30, "#c8b890")):
        o += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{c}"/>'
    o += '<rect x="236" y="210" width="140" height="4" fill="#3a3030"/>' + "".join(f'<path d="M {x},214 L {x},{214 + h}" stroke="#8a8a94" stroke-width="2.4"/><ellipse cx="{x}" cy="{216 + h}" rx="{r}" ry="{r * .6:.1f}" fill="#9a9aa4"/>' for x, h, r in ((250, 50, 7), (272, 60, 5), (294, 44, 8), (316, 56, 5), (338, 48, 6), (360, 40, 9)))
    o += '<g transform="translate(236,110)"><rect x="0" y="0" width="56" height="74" fill="#efe8da"/><rect x="0" y="0" width="56" height="12" fill="#8e1b24"/><rect x="6" y="16" width="44" height="26" fill="#6a7aa8"/><ellipse cx="28" cy="29" rx="8" ry="10" fill="#e8e0d0"/></g>'
    # counter run with cabinets, stove + pots, sink + tap + dish rack, rice cooker
    o += '<rect x="0" y="470" width="400" height="22" fill="#e8e2d8"/><rect x="0" y="492" width="400" height="148" fill="#7a6a5a"/>' + "".join(f'<rect x="{x}" y="502" width="88" height="128" fill="#8a7a68"/><rect x="{x + 76}" y="560" width="6" height="16" fill="#c8b07a"/>' for x in (10, 108, 206, 304))
    o += '<rect x="20" y="452" width="120" height="18" fill="#2a2a30"/><path d="M 28,452 L 72,452 L 70,414 L 30,414 Z" fill="#9a9aa4"/><ellipse cx="50" cy="414" rx="21" ry="5" fill="#b8b8c0"/><path d="M 90,452 L 130,452 L 128,424 L 92,424 Z" fill="#7a7a86"/>'
    o += '<g fill="#ece8f2" opacity=".35" filter="url(#lsoft)"><ellipse cx="50" cy="380" rx="16" ry="26"/><ellipse cx="60" cy="330" rx="12" ry="22"/></g>'
    o += '<rect x="170" y="456" width="80" height="16" fill="#c8c4cc"/><path d="M 210,456 L 210,430 L 226,430" stroke="#8a8a94" stroke-width="4" fill="none"/><g transform="translate(270,430)"><rect x="0" y="0" width="60" height="40" fill="none" stroke="#8a8a94" stroke-width="2"/>' + "".join(f'<ellipse cx="{8 + i * 9}" cy="18" rx="3" ry="16" fill="#efe8f0"/>' for i in range(6)) + '</g>'
    o += '<g transform="translate(350,436)"><rect x="0" y="0" width="34" height="34" rx="8" fill="#e8e2ea"/><ellipse cx="17" cy="0" rx="16" ry="5" fill="#c8c4cc"/></g>'
    o += '<rect x="400" y="300" width="120" height="340" fill="#2a2024"/><rect x="408" y="308" width="104" height="332" fill="#141014"/>'   # back door (Agnes)
    o += '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#6a5a50"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#5a4a40" stroke-width="2"/>' for y in (680, 730, 800, 880)) + "".join(f'<path d="M {270 + (x - 270) * .3:.0f},640 L {x},960" stroke="#5a4a40" stroke-width="2"/>' for x in range(-300, 860, 60))
    o += '<g transform="translate(470,700)"><path d="M -36,0 C -42,-46 -26,-72 0,-74 C 26,-72 42,-46 36,0 Z" fill="#d8c8a8"/><text x="0" y="-30" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" font-weight="700" fill="#6a4a34">ข้าวหอม</text></g>'
    return o

def kitchen_table():
    """A real table in perspective: top, apron, four legs, all on the floor plane."""
    o = '<path d="M 40,744 L 430,744 L 470,792 L 0,792 Z" fill="#8a6a50"/><path d="M 40,744 L 230,744 L 222,792 L 0,792 Z" fill="#9a7a5a"/>'   # top (receding edge is shorter)
    o += '<path d="M 0,792 L 470,792 L 470,808 L 0,808 Z" fill="#5a4030"/>'   # front apron
    o += '<rect x="8" y="808" width="14" height="140" fill="#4a3428"/><rect x="450" y="808" width="14" height="140" fill="#3a281e"/>'   # front legs (reach the floor)
    o += '<rect x="48" y="752" width="10" height="150" fill="#3a281e"/><rect x="414" y="752" width="10" height="150" fill="#2e2018"/>'   # back legs, shorter because further away
    o += '<ellipse cx="236" cy="950" rx="250" ry="10" fill="#1a1214" opacity=".35"/>'
    o += '<ellipse cx="140" cy="760" rx="34" ry="8" fill="#e8e0d4"/><ellipse cx="140" cy="757" rx="26" ry="5" fill="#d8c8a0"/><ellipse cx="290" cy="762" rx="44" ry="10" fill="#9a9aa4"/><ellipse cx="290" cy="758" rx="38" ry="7" fill="#d8c8a0"/>'
    o += '<rect x="350" y="746" width="12" height="16" rx="2" fill="#e8e2ea"/><rect x="368" y="748" width="12" height="14" rx="2" fill="#c8d8c0"/><path d="M 190,760 l 24,-4 M 194,764 l 24,-4" stroke="#c8c4cc" stroke-width="2"/>'
    return o
_ki = kitchen_room() + C("agnes", 456, 640, .64, .8) + C("daeng_whisper", 250, 900, .98) + C("mek", 100, 940, .96) + kitchen_table()
_ki += '<path d="M 270,0 L 270,120" stroke="#1a1418" stroke-width="2"/><path d="M 258,120 L 282,120 L 276,136 L 264,136 Z" fill="#2a2228"/><circle cx="270" cy="141" r="7" fill="#fff4e0"/>'
ST["kitchen"] = _ki

# ============================== 13. SCRATCHED PHOTO (clue close-up) ==============================
def old_photo_twins(scratched=True):
    o = '<g>'
    o += '<path d="M -150,-200 L 150,-196 L 154,206 L -152,202 Z" fill="#e4d6b4"/>'   # paper with a white border, slightly skewed
    o += '<path d="M -150,-200 L 150,-196 L 154,206 L -152,202 Z" fill="url(#paperAge)"/>'
    o += '<rect x="-128" y="-174" width="258" height="300" fill="#9a8e76"/>'   # sepia print area
    # chapel doorway behind the girls
    o += '<path d="M -40,126 L -40,-40 Q 0,-110 40,-40 L 40,126 Z" fill="#6a604e"/><rect x="-128" y="70" width="258" height="56" fill="#847862"/>'
    for gx, scratched_face in ((-58, scratched), (58, False)):
        o += f'<g transform="translate({gx},0)">'
        o += '<path d="M -34,126 L -26,10 C -24,-6 24,-6 26,10 L 34,126 Z" fill="#e8e0cc"/><path d="M -26,10 C -24,-6 -6,-8 -4,-6 L -10,126 L -34,126 Z" fill="#f4eedc"/>'   # nightgown
        o += '<rect x="-20" y="22" width="16" height="7" fill="#fbf8f2"/>'   # name tag
        o += '<circle cx="0" cy="-30" r="22" fill="#d8c8a8"/><path d="M -24,-30 C -26,-60 26,-60 24,-30 L 24,-12 L 18,-24 L -18,-24 L -24,-12 Z" fill="#3a3028"/><path d="M -22,-36 L 22,-36 L 22,-30 L -22,-30 Z" fill="#3a3028"/>'   # face + bob with bangs
        if not scratched_face:
            o += '<circle cx="-7" cy="-28" r="2.2" fill="#2a2420"/><circle cx="7" cy="-28" r="2.2" fill="#2a2420"/><path d="M -6,-18 Q 0,-13 6,-18" stroke="#5a4a40" stroke-width="1.6" fill="none"/>'
            o += '<g transform="translate(26,40)"><circle cx="0" cy="-8" r="6" fill="#d8c0c0"/><path d="M -6,0 L 6,0 L 8,16 L -8,16 Z" fill="#c8a8a8"/></g>'   # Mariam holds her doll
        else:
            o += '<g transform="translate(-30,38)"><rect x="-2" y="-18" width="4" height="18" fill="#f4eedc"/><path d="M 0,-26 C -3,-22 -3,-20 0,-18 C 3,-20 3,-22 0,-26 Z" fill="#fff6e0"/></g>'   # candle in her LEFT hand
            # scratched out: dense, angry pen strokes pressed into the paper, only over her face
            r = _rr.Random(5)
            o += '<g stroke="#1a1414" stroke-linecap="round" fill="none">'
            for k in range(26):
                a = r.uniform(-1, 1)
                x0, y0 = r.uniform(-22, -6), r.uniform(-50, -12)
                o += f'<path d="M {x0:.1f},{y0:.1f} l {r.uniform(18, 30):.1f},{a * 18:.1f}" stroke-width="{r.uniform(1.6, 3.2):.1f}" opacity="{r.uniform(.7, 1):.2f}"/>'
            o += '</g><g stroke="#f8f2e0" stroke-width="1" opacity=".6" fill="none">' + "".join(f'<path d="M {r.uniform(-20, 0):.1f},{r.uniform(-48, -14):.1f} l {r.uniform(10, 22):.1f},{r.uniform(-8, 8):.1f}"/>' for _ in range(10)) + '</g>'   # paper torn shiny where the pen dug in
        o += '</g>'
    o += '<text x="0" y="160" text-anchor="middle" font-family="Georgia, serif" font-size="13" fill="#6a5a40" font-style="italic">มาร์ธา · มาเรียม  2549</text>'
    o += '<path d="M -152,20 L 154,26" stroke="#c8b890" stroke-width="2" opacity=".7"/><path d="M -152,22 L 154,28" stroke="#f4ead0" stroke-width="1" opacity=".7"/>'   # fold crease
    o += '<path d="M 120,-196 L 150,-196 L 150,-168 Z" fill="#c8b48a"/><path d="M -152,180 L -152,202 L -128,202 Z" fill="#bca880"/>'   # worn corners
    o += '<circle cx="90" cy="-120" r="26" fill="#c8a868" opacity=".2"/><circle cx="-100" cy="140" r="18" fill="#b8985a" opacity=".2"/>'   # foxing stains
    return o + '</g>'
INS2["album"] = ('<rect width="540" height="960" fill="#3a2a24"/><path d="M 20,250 L 270,230 L 270,760 L 10,780 Z" fill="#e8dfcc"/><path d="M 520,250 L 270,230 L 270,760 L 530,780 Z" fill="#ddd2bc"/>'
                '<linearGradient id="paperAge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff8e0" stop-opacity=".0"/><stop offset=".7" stop-color="#c8a868" stop-opacity=".25"/><stop offset="1" stop-color="#a8844a" stop-opacity=".45"/></linearGradient>'
                '<g transform="translate(270,480) rotate(-3) scale(1.1)">' + old_photo_twins() + '</g>'
                '<ellipse cx="270" cy="440" rx="240" ry="220" fill="url(#lg_fff0dc)" opacity=".35" style="mix-blend-mode:screen"/>'
                + note(150, 830, "เด็กซ้าย (มาร์ธา) หน้าถูกขีดฆ่า ถือเทียนมือซ้าย · ขวาคือมาเรียมกอดตุ๊กตา"))
INS2["lefthand"] = ('<rect width="540" height="960" fill="#3a2a24"/><linearGradient id="paperAge2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff8e0" stop-opacity="0"/><stop offset="1" stop-color="#a8844a" stop-opacity=".45"/></linearGradient>'
                   '<g transform="translate(330,520) rotate(-3) scale(2.4)">' + old_photo_twins().replace("paperAge", "paperAge2") + '</g>' + note(80, 830, "ซูมเข้า: มือซ้ายของเด็กที่ถูกขีดหน้าถือเทียน"))

# ============================== 14. BODY UNDER A SHEET ==============================
def body_sheet():
    """White sheet over a body lying on its back: head, shoulders, chest, hips, legs, feet read through the cloth."""
    o = '<g>'
    o += '<ellipse cx="0" cy="34" rx="210" ry="22" fill="#0a080c" opacity=".45" filter="url(#lsoft)"/>'
    o += ('<path d="M -200,10 C -204,-20 -186,-36 -166,-38 C -150,-40 -140,-30 -130,-30 C -110,-44 -60,-46 -40,-40 C -10,-34 20,-34 40,-30 C 80,-26 110,-24 140,-20 '
          'C 160,-18 170,-36 186,-34 C 200,-32 206,-14 204,6 C 202,22 190,30 170,30 L -170,30 C -190,30 -198,24 -200,10 Z" fill="#ece8ee"/>')
    o += '<path d="M -200,10 C -204,-20 -186,-36 -166,-38 C -150,-40 -140,-30 -130,-30 C -110,-44 -60,-46 -40,-40 L -40,30 L -170,30 C -190,30 -198,24 -200,10 Z" fill="#f6f4f8"/>'
    o += '<path d="M 20,-32 C 60,-28 100,-24 140,-20 C 160,-18 170,-36 186,-34 C 200,-32 206,-14 204,6 C 202,22 190,30 170,30 L 20,30 Z" fill="#d4d0dc"/>'
    # folds that follow the shape: around the head, across the chest, between the legs, at the feet
    o += '<g fill="none" stroke="#b8b4c4" stroke-width="2" stroke-linecap="round">'
    o += '<path d="M -150,-34 C -152,-10 -146,10 -150,28"/><path d="M -126,-30 C -118,-12 -120,10 -112,28"/>'
    o += '<path d="M -90,-42 C -80,-20 -84,6 -78,28"/><path d="M -40,-40 C -46,-16 -40,8 -46,28"/><path d="M 0,-34 C 6,-10 0,10 6,28"/>'
    o += '<path d="M 40,-30 C 60,-14 100,-10 150,-6" stroke-width="2.4"/><path d="M 60,-6 C 90,4 130,6 170,8"/>'
    o += '<path d="M 160,-30 C 168,-14 166,6 172,26"/><path d="M 186,-32 C 194,-14 196,6 192,24"/></g>'
    o += '<path d="M -170,30 C -150,40 -120,44 -100,40 M 60,30 C 90,38 140,40 170,34" stroke="#d4d0dc" stroke-width="5" fill="none"/>'   # hem pooling on the ground
    o += '<path d="M -180,-16 C -172,-24 -160,-26 -150,-20" stroke="#fff" stroke-width="3" fill="none" opacity=".7"/>'   # highlight on the head
    o += '<path d="M -40,28 C -60,36 -70,46 -76,52 L -64,54 C -58,46 -50,38 -40,32 Z" fill="#c98f69"/><ellipse cx="-72" cy="54" rx="8" ry="5" fill="#c98f69"/>'   # her hand slipping out from under the sheet
    return o + '</g>'
def police_dawn_bg():
    o = '<rect width="540" height="960" fill="#7d8cab"/>' + sky("#4a5a8a", "#8a98c0", "#c8c4d8", clouds=((40, 140, 160, "#e8e4f0", .4), (300, 100, 180, "#e8e4f0", .35)))
    o += '<g transform="translate(40,0) scale(.62)">' + bell_tower_old() + '</g>'
    o += '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#4a4a5a"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#3a3a48" stroke-width="2"/>' for y in (680, 740, 820, 920))
    o += '<path d="M 0,610 L 540,640" stroke="#e8c84a" stroke-width="7"/><path d="M 0,610 L 540,640" stroke="#1a1a20" stroke-width="7" stroke-dasharray="18 18"/>' + "".join(f'<rect x="{x}" y="{600 + x * .055:.0f}" width="6" height="60" fill="#e8e0d0"/>' for x in (20, 260, 500))
    return o
ST["body_sheet"] = (police_dawn_bg() + "".join(f'<g transform="translate({x},420) scale(.5)"><use href="#{P["mariam"]}"/></g>' for x in (380, 450)) +
    C("agnes", 330, 760, .78) + C("mariam", 200, 770, .8) + '<g transform="translate(290,860) scale(1.15)">' + body_sheet() + '</g>')

# carved stone plaque on Martha's grave (replaces the plain label)
def stone_plaque(name="MARTHA", th="มาร์ธา", years="2540 – 2549"):
    return ('<g><path d="M -96,-62 L 96,-62 L 104,-54 L 104,62 L -104,62 L -104,-54 Z" fill="#7a7488"/><path d="M -96,-62 L 96,-62 L 96,54 L -96,54 Z" fill="#b4aec0"/>'
            '<path d="M -96,-62 L 96,-62 L 90,-56 L -90,-56 Z" fill="#d4cedc"/><path d="M -96,-62 L -90,-56 L -90,48 L -96,54 Z" fill="#c8c2d0"/><path d="M 96,-62 L 90,-56 L 90,48 L 96,54 Z" fill="#8a8494"/>'
            '<rect x="-80" y="-44" width="160" height="84" fill="none" stroke="#8a8494" stroke-width="2"/>'
            f'<text x="0" y="-6" text-anchor="middle" font-family="Georgia, serif" font-size="30" font-weight="700" letter-spacing="4" fill="#5a5466">{name}</text>'
            f'<text x="0" y="-7" text-anchor="middle" font-family="Georgia, serif" font-size="30" font-weight="700" letter-spacing="4" fill="#e4e0ea" opacity=".35" transform="translate(-1,-1)">{name}</text>'
            f'<text x="0" y="18" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#5a5466">{th}</text><text x="0" y="34" text-anchor="middle" font-family="Georgia, serif" font-size="11" fill="#5a5466">{years}</text>'
            '<path d="M 60,-62 L 52,-40 L 58,-28 L 50,-10" stroke="#5a5466" stroke-width="1.4" fill="none"/>'
            '<path d="M -96,30 C -80,20 -60,40 -40,30 C -20,22 -10,46 10,40 L 10,54 L -96,54 Z" fill="#5e7a54" opacity=".75"/><ellipse cx="70" cy="44" rx="20" ry="8" fill="#6a8a5a" opacity=".6"/>'
            '<path d="M -104,62 L 104,62" stroke="#3a3446" stroke-width="3"/></g>')

# ============================== 16. CEMETERY: more age, a big tree, ivy, steps, iron fence ==============================
def cemetery_extra():
    o = ""
    # big old tree on the left, branches reaching into the frame
    o += '<path d="M -40,960 C -20,800 -30,640 10,520 C 30,460 20,400 40,340 L 70,350 C 54,410 64,470 46,530 C 20,640 40,800 30,960 Z" fill="#3a2e30"/><path d="M -40,960 C -20,800 -30,640 10,520 L 24,524 C -6,640 6,800 -4,960 Z" fill="#4a3c3c"/>'
    o += '<path d="M 40,360 C 120,300 220,260 330,250 L 330,262 C 224,272 128,312 50,372 Z M 30,430 C 80,410 140,420 190,400 L 190,410 C 140,432 84,422 36,442 Z M 60,320 C 70,250 120,190 200,150 L 204,160 C 128,200 82,258 70,326 Z" fill="#3a2e30"/>'
    o += "".join(clump(x, y, r, "#4e5e48", "#3e4e3a", "#2e3c2c") for x, y, r in ((60, 220, 90), (180, 150, 80), (300, 200, 70), (120, 320, 60)))
    o += "".join(f'<path d="M {x},{y} C {x + 4},{y + 30} {x - 4},{y + 60} {x + 2},{y + 90}" stroke="#4e6048" stroke-width="2" fill="none"/>' for x, y in ((210, 250), (250, 246), (300, 250), (150, 290)))   # hanging moss
    # stone chest tombs of different heights in the midground, with moss + ivy
    for (x, y, w, h) in ((400, 640, 90, 40), (360, 700, 110, 52), (470, 740, 70, 60)):
        o += f'<path d="M {x},{y} L {x + w},{y} L {x + w},{y + h} L {x},{y + h} Z" fill="#b4aec0"/><path d="M {x - 6},{y - 8} L {x + w + 6},{y - 8} L {x + w + 6},{y} L {x - 6},{y} Z" fill="#d0cad8"/><path d="M {x + w * .7:.0f},{y} L {x + w},{y} L {x + w},{y + h} L {x + w * .7:.0f},{y + h} Z" fill="#8a8494"/>'
        o += f'<path d="M {x},{y + h} C {x + 10},{y + h - 16} {x + 4},{y + h - 30} {x + 16},{y}" stroke="#3e5a3e" stroke-width="3" fill="none"/>' + "".join(f'<ellipse cx="{x + 6 + k * 4}" cy="{y + h - k * 7}" rx="5" ry="3" fill="#4e6e4a"/>' for k in range(5))
        o += f'<ellipse cx="{x + w * .3:.0f}" cy="{y - 6}" rx="{w * .25:.0f}" ry="3" fill="#6a8a5a" opacity=".7"/>'
    # stone steps in the path + rusty iron railing in the foreground right
    for i, (x, y, w) in enumerate(((236, 640, 70), (226, 664, 90), (214, 692, 114))):
        o += f'<rect x="{x}" y="{y}" width="{w}" height="10" fill="#c8c2d0"/><rect x="{x}" y="{y + 10}" width="{w}" height="12" fill="#8a8494"/>'
    o += '<g opacity=".95">' + "".join(f'<rect x="{x}" y="{760 + (x - 380) * .1:.0f}" width="5" height="190" fill="#2a2226"/><path d="M {x - 4},{760 + (x - 380) * .1:.0f} L {x + 2.5},{744 + (x - 380) * .1:.0f} L {x + 9},{760 + (x - 380) * .1:.0f} Z" fill="#2a2226"/>' for x in range(380, 560, 20)) + '<path d="M 376,790 L 560,808 M 376,900 L 560,918" stroke="#2a2226" stroke-width="5"/><path d="M 390,800 C 420,780 440,820 470,800" stroke="#6a3a2a" stroke-width="2" fill="none" opacity=".7"/></g>'
    o += haze(560, 90, "#d8cce0", .35) + haze(860, 100, "#d8cce0", .3)   # ground mist
    return o
_old_cg = child_graves()
def child_graves2():
    return _old_cg + '<g transform="translate(132,912) scale(.42)">' + stone_plaque() + '</g>'
ST["cemetery"] = ST["cemetery"].replace(_old_cg, "") + cemetery_extra() + child_graves2()
ST["cemetery_wide"] = cemetery_bg() + cemetery_extra() + child_graves2() + C("rosa", 380, 700, .6) + C("mek_back", 250, 960, 1.05)

# ============================== 17. MARTHA NAME TAG (embroidered, in an evidence bag) ==============================
INS2["tag"] = ('<rect width="540" height="960" fill="#1e1c24"/><ellipse cx="270" cy="470" rx="260" ry="240" fill="url(#lg_fff0dc)" opacity=".35"/>'
  '<g transform="translate(270,470) rotate(-4)">'
  '<rect x="-170" y="-230" width="340" height="440" rx="10" fill="#dce2ee" opacity=".18"/><rect x="-170" y="-230" width="340" height="30" rx="6" fill="#c84040" opacity=".55"/><path d="M -170,-200 L 170,-200" stroke="#e8e8f0" stroke-width="3" opacity=".5"/>'
  '<text x="-150" y="-176" font-family="Inter, sans-serif" font-size="12" fill="#e8e8f0" opacity=".7">EVIDENCE · สน.บางกอกน้อย · 22/11/69</text>'
  '<path d="M -150,-120 L 140,-160 M -120,180 L 150,120" stroke="#fff" stroke-width="2" opacity=".2"/>'   # plastic sheen
  # the cloth tag: thickness, stitched border, embroidered letters in red thread
  '<rect x="-128" y="-48" width="256" height="112" rx="8" fill="#b8b0a0"/><rect x="-124" y="-56" width="256" height="112" rx="8" fill="#f6f2e8"/>'
  '<rect x="-112" y="-44" width="232" height="88" rx="4" fill="none" stroke="#c84040" stroke-width="2.4" stroke-dasharray="5 3"/>'
  '<g stroke="#e8e0cc" stroke-width=".6" opacity=".7">' + "".join(f'<path d="M {-124 + k * 6},-56 L {-124 + k * 6},56"/>' for k in range(43)) + '</g>'   # weave
  '<text x="4" y="4" text-anchor="middle" font-family="Georgia, serif" font-size="48" font-weight="700" letter-spacing="6" fill="#a8302e">MARTHA</text>'
  '<text x="4" y="4" text-anchor="middle" font-family="Georgia, serif" font-size="48" font-weight="700" letter-spacing="6" fill="none" stroke="#7a1e1e" stroke-width="1" stroke-dasharray="2 1.4"/>'
  '<text x="4" y="36" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" font-weight="700" fill="#a8302e">มาร์ธา</text>'
  '<path d="M 124,-20 l 10,-4 l -4,10 l 12,0" stroke="#e8e0cc" stroke-width="1.6" fill="none"/>'   # loose thread end
  '</g>' + note(130, 800, "ป้ายชื่อผ้าปักด้ายแดง ใหม่เอี่ยม ไม่มีรอยไหม้ ในถุงหลักฐาน"))


# ======================= ROUND 3 FIXES (only what was asked) =======================
ST["sisters_ext"] = sisters_building()   # rebuilt without stains or cracks; age comes from light and shadow

# ---- engraved Thai lettering on stone ----
def carved(x, y, text, size, anchor="middle", weight=700, latin=False):
    fam = "Georgia, 'Times New Roman', serif" if latin else "IBM Plex Sans Thai, sans-serif"
    f = f'font-family="{fam}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{1.2 if latin else 1.5}"'
    return (f'<text x="{x + 1.1:.1f}" y="{y + 1.3:.1f}" {f} fill="#eeeaf4" opacity=".55">{text}</text>'   # light catching the lower lip of the groove
            f'<text x="{x:.1f}" y="{y:.1f}" {f} fill="#4a4456">{text}</text>'                              # the cut itself
            f'<text x="{x - .6:.1f}" y="{y - .7:.1f}" {f} fill="#2e2a38" opacity=".55">{text}</text>')      # shadow inside the top of the groove

def big_stone(x, y, w, h, shape, lines=(), k=1.0, seed=1):
    """Large, thick Western headstone standing on the earth: face, side thickness, top, plinth, contact shadow, moss."""
    w, h = w * k, h * k; t = 9 * k
    r = _rr.Random(seed)
    face, side, top_, edge = "#c4bece", "#8a8496", "#dcd6e4", "#a8a2b4"
    if shape == "round":
        f = f"M {x - w / 2:.1f},{y:.1f} L {x - w / 2:.1f},{y - h + w / 2:.1f} A {w / 2:.1f},{w / 2:.1f} 0 0 1 {x + w / 2:.1f},{y - h + w / 2:.1f} L {x + w / 2:.1f},{y:.1f} Z"
    elif shape == "ogee":
        f = f"M {x - w / 2:.1f},{y:.1f} L {x - w / 2:.1f},{y - h * .78:.1f} C {x - w / 2:.1f},{y - h * .95:.1f} {x - w * .1:.1f},{y - h * .9:.1f} {x:.1f},{y - h:.1f} C {x + w * .1:.1f},{y - h * .9:.1f} {x + w / 2:.1f},{y - h * .95:.1f} {x + w / 2:.1f},{y - h * .78:.1f} L {x + w / 2:.1f},{y:.1f} Z"
    else:  # gable
        f = f"M {x - w / 2:.1f},{y:.1f} L {x - w / 2:.1f},{y - h * .82:.1f} L {x:.1f},{y - h:.1f} L {x + w / 2:.1f},{y - h * .82:.1f} L {x + w / 2:.1f},{y:.1f} Z"
    o = f'<ellipse cx="{x + w * .25:.1f}" cy="{y + 4 * k:.1f}" rx="{w * .85:.1f}" ry="{7 * k:.1f}" fill="#120e18" opacity=".55" filter="url(#lsoft)"/>'   # contact shadow
    o += f'<path d="{f}" fill="{side}" transform="translate({t:.1f},{-t * .5:.1f})"/>'   # thickness (back slab)
    o += f'<path d="{f}" fill="{face}"/>'
    o += f'<path d="{f}" fill="none" stroke="{top_}" stroke-width="{2.2 * k:.1f}" stroke-dasharray="{w * 1.4:.0f} 2000"/>'   # lit top edge
    o += f'<path d="M {x - w / 2 + 6 * k:.1f},{y:.1f} L {x - w / 2 + 6 * k:.1f},{y - h * .6:.1f}" stroke="{edge}" stroke-width="{1.4 * k:.1f}" opacity=".6"/>'
    o += f'<rect x="{x - w / 2 - 8 * k:.1f}" y="{y - 4 * k:.1f}" width="{w + 16 * k + t:.1f}" height="{12 * k:.1f}" fill="#9a94a6"/><rect x="{x - w / 2 - 8 * k:.1f}" y="{y - 4 * k:.1f}" width="{w + 16 * k + t:.1f}" height="{3 * k:.1f}" fill="#d0cad8"/>'   # plinth
    # carved cross near the top
    cy = y - h * .74
    o += f'<path d="M {x:.1f},{cy - 12 * k:.1f} L {x:.1f},{cy + 12 * k:.1f} M {x - 8 * k:.1f},{cy - 4 * k:.1f} L {x + 8 * k:.1f},{cy - 4 * k:.1f}" stroke="#4a4456" stroke-width="{3 * k:.1f}"/><path d="M {x + 1 * k:.1f},{cy - 11 * k:.1f} L {x + 1 * k:.1f},{cy + 13 * k:.1f}" stroke="#eeeaf4" stroke-width="{1 * k:.1f}" opacity=".5"/>'
    yy = y - h * .46
    for ln in lines:
        txt, size = ln[0], ln[1]; latin = len(ln) > 2 and ln[2]
        o += carved(x, yy, txt, size * k, weight=600 if latin else 700, latin=latin); yy += size * k * 1.6
    # moss and lichen, a small chip on the edge
    o += f'<path d="M {x - w / 2:.1f},{y - 2:.1f} C {x - w * .3:.1f},{y - 16 * k:.1f} {x - w * .1:.1f},{y - 4 * k:.1f} {x + w * .05:.1f},{y - 12 * k:.1f} L {x + w * .1:.1f},{y:.1f} Z" fill="#5e7a54" opacity=".8"/>'
    o += "".join(f'<ellipse cx="{x + r.uniform(-w * .4, w * .4):.1f}" cy="{y - r.uniform(h * .1, h * .9):.1f}" rx="{r.uniform(3, 7) * k:.1f}" ry="{r.uniform(2, 4) * k:.1f}" fill="#8a9a6a" opacity=".45"/>' for _ in range(3))
    o += f'<path d="M {x + w / 2:.1f},{y - h * .55:.1f} l {-6 * k:.1f},{4 * k:.1f} l {6 * k:.1f},{5 * k:.1f} Z" fill="{side}"/>'
    return o

def child_graves3():
    o = big_stone(130, 912, 92, 150, "round", (("มาร์ธา", 21), ("1997 – 2006", 11, True), ("REST IN PEACE", 6, True)), seed=1)
    o += big_stone(275, 930, 98, 138, "ogee", (("นภา", 21), ("DEC 14, 2006", 11, True), ("REST IN PEACE", 6, True)), seed=2)
    o += big_stone(420, 912, 86, 128, "gable", (), seed=3)   # the nameless grave: only a carved cross
    # offerings stay as they were
    o += '<g transform="translate(176,918)"><circle cx="0" cy="-10" r="9" fill="#a88a6a"/><circle cx="-6" cy="-18" r="3.5" fill="#a88a6a"/><circle cx="6" cy="-18" r="3.5" fill="#a88a6a"/><ellipse cx="0" cy="4" rx="11" ry="9" fill="#9a7a5a"/></g>'
    o += '<g transform="translate(316,940)"><rect x="-12" y="-8" width="24" height="9" rx="3" fill="#5a7aa8"/><rect x="-7" y="-14" width="14" height="7" rx="2" fill="#7a9ac8"/><circle cx="-7" cy="2" r="3.5" fill="#2a2a30"/><circle cx="7" cy="2" r="3.5" fill="#2a2a30"/></g>'
    for (x, y) in ((92, 918), (236, 936), (380, 918), (462, 920)):
        o += f'<rect x="{x - 5}" y="{y - 12}" width="10" height="13" rx="2" fill="#c8d0e0" opacity=".7"/><rect x="{x - 2}" y="{y - 10}" width="4" height="7" fill="#efe8da"/><circle cx="{x}" cy="{y - 13}" r="10" fill="url(#lg_ffe6c4)" opacity=".8" style="mix-blend-mode:screen"/>'
    o += '<path d="M 424,868 c 6,-4 10,0 6,4 c 6,2 4,8 -2,6 l -2,10 l -2,-10 c -6,2 -8,-4 -2,-6 c -4,-4 0,-8 6,-4 Z" fill="#f2eee8"/>'   # white ribbon on the nameless stone
    return o

def tree_natural(x, base, h=620, flip=1):
    """Old cemetery tree: flared roots, tapering trunk, forked limbs, twigs, layered canopy with a dark underside."""
    s_ = flip
    o = f'<g transform="translate({x},{base}) scale({s_},1)">'
    o += '<path d="M -70,0 C -40,-10 -30,-30 -24,-60 C -18,-160 -30,-260 -10,-360 L 26,-360 C 34,-260 26,-160 34,-60 C 40,-30 56,-10 90,0 Z" fill="#3e3236"/>'
    o += '<path d="M -70,0 C -40,-10 -30,-30 -24,-60 C -18,-160 -30,-260 -10,-360 L 2,-360 C -10,-260 -2,-160 -4,-60 C -6,-30 -20,-10 -40,0 Z" fill="#54464a"/>'
    o += "".join(f'<path d="M {bx},{by} C {bx + 4},{by - 30} {bx - 3},{by - 60} {bx + 2},{by - 90}" stroke="#2e2428" stroke-width="2" fill="none" opacity=".7"/>' for bx, by in ((-8, -40), (8, -80), (16, -150), (-2, -220), (12, -280)))   # bark
    # limbs forking out of the trunk
    o += '<path d="M -6,-340 C -40,-400 -110,-430 -180,-440 L -176,-428 C -110,-416 -46,-386 -14,-326 Z" fill="#3e3236"/>'
    o += '<path d="M 18,-350 C 60,-420 140,-460 260,-470 L 258,-458 C 144,-446 70,-406 30,-338 Z" fill="#3e3236"/>'
    o += '<path d="M 6,-360 C 4,-440 20,-520 50,-580 L 60,-574 C 34,-514 20,-440 22,-356 Z" fill="#3e3236"/>'
    o += '<path d="M 120,-440 C 150,-470 170,-500 176,-530 M 200,-460 C 230,-470 260,-480 300,-478 M -110,-420 C -140,-450 -150,-480 -146,-510" stroke="#3e3236" stroke-width="5" fill="none"/>'
    # canopy: back (dark), mid, front (lit) leaf masses
    for (cx, cy, r, c1, c2, c3) in ((-160, -470, 80, "#344430", "#2c3a28", "#222e20"), (60, -580, 110, "#344430", "#2c3a28", "#222e20"), (240, -500, 90, "#344430", "#2c3a28", "#222e20"),
                                     (-90, -500, 90, "#4e6446", "#40543a", "#33452e"), (150, -540, 100, "#4e6446", "#40543a", "#33452e"), (10, -470, 80, "#4e6446", "#40543a", "#33452e"),
                                     (-150, -440, 60, "#6a8258", "#5a7048", "#4a5e3c"), (80, -500, 70, "#6a8258", "#5a7048", "#4a5e3c"), (260, -470, 60, "#6a8258", "#5a7048", "#4a5e3c")):
        o += clump(cx, cy, r, c1, c2, c3)
    o += "".join(f'<path d="M {px},{py} C {px + 3},{py + 20} {px - 3},{py + 44} {px + 1},{py + 64}" stroke="#5a6a4e" stroke-width="1.6" fill="none" opacity=".75"/>' for px, py in ((-120, -420), (-60, -440), (40, -430), (120, -460), (200, -440)))   # hanging moss
    o += '<path d="M -70,0 C -90,4 -110,2 -130,8 M 90,0 C 110,4 130,6 150,12" stroke="#3e3236" stroke-width="6" fill="none"/>'   # surface roots
    return o + '</g>'

def cemetery_extra2():
    o = tree_natural(30, 700, flip=1)
    # big stone headstones of varied height and shape in the midground (no paving, standing in grass)
    for (x, y, w, h, sh, sd) in ((360, 660, 60, 92, "gable", 11), (440, 690, 66, 110, "round", 12), (510, 700, 58, 88, "ogee", 13), (390, 750, 70, 118, "round", 14)):
        o += big_stone(x, y, w, h, sh, (), k=.9, seed=sd)
    o += '<g opacity=".95">' + "".join(f'<rect x="{x}" y="{790 + (x - 380) * .1:.0f}" width="5" height="170" fill="#2a2226"/><path d="M {x - 4},{790 + (x - 380) * .1:.0f} L {x + 2.5},{774 + (x - 380) * .1:.0f} L {x + 9},{790 + (x - 380) * .1:.0f} Z" fill="#2a2226"/>' for x in range(380, 560, 20)) + '<path d="M 376,820 L 560,838 M 376,920 L 560,938" stroke="#2a2226" stroke-width="5"/></g>'
    o += "".join(tuft(RR.uniform(300, 540), RR.uniform(700, 800), 1.3) for _ in range(10))
    o += haze(560, 90, "#d8cce0", .35) + haze(860, 100, "#d8cce0", .3)
    return o

ST["cemetery"] = cemetery_bg() + cemetery_extra2() + C("rosa_point", 160, 780, .85) + C("mek", 400, 790, .88) + child_graves3()
ST["cemetery_wide"] = cemetery_bg() + cemetery_extra2() + child_graves3() + C("rosa", 380, 700, .6) + C("mek_back", 250, 960, 1.05)

# ---- piano: original front-facing Mariam, keyboard clearly separate in the foreground ----
def keyboard_fg(y=712):
    """Seen from the piano's side: keys run toward her, black keys nearest us, dark key slip and cheek blocks frame them."""
    o = f'<path d="M 96,{y - 6} L 444,{y - 6} L 452,{y + 40} L 88,{y + 40} Z" fill="#1a1216"/>'   # dark wood behind the keys = clean edge against her white robe
    o += f'<path d="M 104,{y} L 436,{y} L 442,{y + 34} L 98,{y + 34} Z" fill="#f4f0e6"/>'
    o += "".join(f'<path d="M {104 + k * 15.1:.1f},{y} L {98 + k * 15.4:.1f},{y + 34}" stroke="#a8a294" stroke-width="1"/>' for k in range(1, 22))
    o += "".join(f'<path d="M {106 + k * 15.1:.1f},{y + 14} L {115 + k * 15.1:.1f},{y + 14} L {115 + k * 15.3:.1f},{y + 34} L {104 + k * 15.3:.1f},{y + 34} Z" fill="#141014"/>' for k in range(22) if k % 7 not in (2, 6))
    o += f'<path d="M 80,{y + 34} L 460,{y + 34} L 470,{y + 90} L 70,{y + 90} Z" fill="#2a1c20"/><path d="M 80,{y + 34} L 460,{y + 34} L 462,{y + 42} L 78,{y + 42} Z" fill="#4a3236"/>'   # key slip
    o += f'<rect x="70" y="{y - 20}" width="34" height="110" fill="#2a1c20"/><rect x="436" y="{y - 20}" width="34" height="110" fill="#22161a"/>'   # cheek blocks
    o += f'<path d="M 104,{y - 6} L 436,{y - 6}" stroke="#c8b07a" stroke-width="1.4" opacity=".6"/>'
    return o
def hands_on_keys(xl, xr, y):
    o = ""
    for x, col, scar in ((xl, "#f6dcc4", False), (xr, "#e4b89c", True)):
        o += f'<path d="M {x - 12},{y - 4} C {x - 12},{y - 14} {x + 12},{y - 14} {x + 12},{y - 4} L {x + 13},{y + 8} L {x - 13},{y + 8} Z" fill="{col}"/>'
        o += "".join(f'<rect x="{x - 12 + i * 6:.0f}" y="{y + 4}" width="4.6" height="9" rx="2.2" fill="{col}"/>' for i in range(4))
        if scar: o += f'<path d="M {x - 6},{y - 8} C {x},{y - 11} {x + 6},{y - 8} {x + 5},{y - 3} C {x},{y - 1} {x - 5},{y - 3} {x - 6},{y - 8} Z" fill="#d98f86" opacity=".85"/>'
    return o
_mu = music_room() + C("agnes", 506, 610, .6, .8)
_mu += C("mariam_piano", 270, 880, .95)
_mu += keyboard_fg(712) + hands_on_keys(242, 298, 716)
_mu += '<rect x="160" y="600" width="6" height="22" fill="#efe8da"/><path d="M 163,588 C 160,594 160,597 163,599 C 166,597 166,594 163,588 Z" fill="#fff6e6"/><circle cx="163" cy="594" r="30" fill="url(#lg_ffe6c4)" opacity=".8"/>'   # candle at the end of the keyboard
ST["music"] = _mu

# ---- veranda: lawn between the veranda and the old wing; the building stands on the ground ----
def veranda2():
    o = night_sky((420, 140), seed=9)
    o += '<path d="M 0,500 L 540,500 L 540,620 L 0,620 Z" fill="#2c3a34"/>'                       # far lawn up to the horizon
    o += "".join(clump(x, y, r, "#22303a", "#1c2832", "#16202a") for x, y, r in ((40, 470, 70), (140, 488, 46), (470, 470, 80), (540, 480, 60)))   # trees at the edge of the lawn
    o += f'<g opacity=".88">{old_wing(220, 395, .5)}</g>'                                           # old wing, base on the lawn
    o += '<polygon points="220,505 340,505 300,532 170,532" fill="#0a0e14" opacity=".45" filter="url(#lsoft)"/>'   # its shadow on the grass (moon upper right)
    o += haze(470, 50, "#9aa0c8", .35)                                                             # distance haze softens it
    o += '<path d="M 0,540 L 540,540" stroke="#34443c" stroke-width="2" opacity=".6"/>' + "".join(f'<path d="M {x},{y} l -2,-8 M {x + 3},{y} l 1,-10 M {x + 6},{y} l 3,-7" stroke="#3e5048" stroke-width="1.4"/>' for x, y in ((60, 560), (180, 576), (300, 566), (420, 580), (500, 556)))
    o += '<path d="M 250,505 C 240,540 300,560 270,620" stroke="#4a5650" stroke-width="10" fill="none" opacity=".6"/>'   # garden path leading to the old wing
    o += '<g transform="translate(380,520)"><rect x="-2" y="-40" width="4" height="40" fill="#1a1e24"/><circle cx="0" cy="-44" r="4" fill="#3a3e48"/></g>'   # unlit garden lamp
    o += "".join(clump(x, 600, 36, "#30443a", "#283a30", "#203026") for x in (80, 200, 460))       # shrubs just beyond the balustrade
    # the veranda itself, unchanged
    o += '<path d="M 0,120 L 70,150 L 70,960 L 0,960 Z" fill="#c8bca8"/><path d="M 10,520 L 54,530 L 54,800 L 10,800 Z" fill="#f2d8a8"/><path d="M 10,520 L 54,530 L 54,800 L 10,800 Z" fill="none" stroke="#5a4234" stroke-width="5"/>'
    o += '<polygon points="54,800 54,530 260,900 120,960" fill="#fff0d0" opacity=".12" filter="url(#lhaze)"/>'
    o += '<path d="M 0,90 L 540,120 L 540,150 L 0,124 Z" fill="#5a4234"/><path d="M 0,124 L 540,150 L 540,160 L 0,134 Z" fill="#3e2c22"/>'
    o += '<path d="M 0,700 L 540,700 L 540,960 L 0,960 Z" fill="#9a7a6a"/>' + "".join(f'<path d="M {270 + (x - 270) * .3:.0f},700 L {x},960" stroke="#8a6a5a" stroke-width="1.6"/>' for x in range(-300, 860, 60)) + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#8a6a5a" stroke-width="1.6"/>' for y in (730, 770, 830, 910))
    for x in (110, 520):
        o += f'<rect x="{x - 12}" y="150" width="24" height="550" fill="#e4dcd0"/><rect x="{x - 12}" y="150" width="8" height="550" fill="#f4ece2"/><rect x="{x - 18}" y="150" width="36" height="14" fill="#efe4d8"/><rect x="{x - 16}" y="686" width="32" height="14" fill="#d8ccc0"/>'
    o += '<rect x="70" y="590" width="470" height="12" fill="#e4dcd0"/>' + "".join(f'<path d="M {x},602 C {x - 5},616 {x + 5},632 {x},646 L {x},690" stroke="#d8ccc0" stroke-width="7"/>' for x in range(90, 540, 22)) + '<rect x="70" y="690" width="470" height="10" fill="#c8bcb0"/>'
    o += '<path d="M 300,150 L 300,220" stroke="#2a2024" stroke-width="2"/><g transform="translate(300,232)"><path d="M -18,0 L 18,0 L 12,18 L -12,18 Z" fill="#8a604a"/>' + "".join(f'<path d="M {dx},6 C {dx * 2},20 {dx * 2.4},40 {dx * 2.2},60" stroke="#3e5a3e" stroke-width="3" fill="none"/>' for dx in (-10, -4, 4, 10)) + '</g>'
    return o
ST["veranda"] = ST["veranda"].replace(veranda(), veranda2())

# ---- burnt rag doll: cloth girl, yarn braids, button eyes, stitches; the right half charred ----
def ragdoll():
    o = '<g>'
    o += '<ellipse cx="4" cy="104" rx="70" ry="10" fill="#0a080c" opacity=".55" filter="url(#lsoft)"/>'
    # legs + arms (cloth tubes with stitch lines)
    o += '<path d="M -22,70 L -12,70 L -14,104 L -26,104 Z" fill="#e8dcc8"/><path d="M 10,70 L 22,70 L 26,102 L 12,102 Z" fill="#2a1e1a"/>'
    o += '<path d="M -34,8 C -52,20 -58,40 -54,58 L -44,58 C -46,42 -40,28 -28,18 Z" fill="#e8dcc8"/><path d="M 34,8 C 50,22 54,40 50,54 L 42,54 C 44,40 38,26 28,18 Z" fill="#3a2a22"/>'
    o += '<path d="M -50,40 l 6,2 M -51,48 l 6,2 M -24,80 l 8,0 M -24,90 l 8,0" stroke="#8a7a68" stroke-width="1.4"/>'
    # old-fashioned dress with collar and small print; the right side scorched with a ragged edge
    o += '<path d="M -30,0 L 30,0 L 44,76 L -44,76 Z" fill="#16121a"/><path d="M -30,0 L -8,0 L -16,76 L -44,76 Z" fill="#241e2a"/>'
    o += "".join(f'<circle cx="{dx}" cy="{dy}" r="1.4" fill="#3a3240"/>' for dx, dy in ((-24, 20), (-14, 40), (-30, 58), (-6, 64), (-20, 70)))
    o += '<path d="M -18,0 C -12,10 12,10 18,0 L 14,-4 L -14,-4 Z" fill="#f0e8dc"/>'
    o += '<path d="M 4,0 L 30,0 L 44,76 L 12,76 L 16,62 L 6,54 L 14,40 L 4,30 L 10,16 Z" fill="#1e1614"/><path d="M 4,0 L 10,16 L 4,30 L 14,40 L 6,54 L 16,62 L 12,76" stroke="#8a4a2a" stroke-width="2" fill="none" opacity=".8"/>'
    o += '<path d="M 10,30 c 4,-3 8,0 6,4 M 22,56 c 4,-3 8,1 5,5" stroke="#3a2a22" stroke-width="2" fill="none"/>'   # holes burnt through
    o += "".join(f'<circle cx="-4" cy="{y}" r="2.6" fill="#050406"/><circle cx="-4.8" cy="{y - .8}" r=".6" fill="#fff" opacity=".3"/>' for y in (10, 24, 38, 52))
    # head: cloth face with a seam down the middle, stitched mouth, button eyes; right half blackened
    o += '<circle cx="0" cy="-28" r="26" fill="#efe2cc"/>'
    o += '<path d="M 0,-54 A 26,26 0 0 1 0,-2 C 6,-10 2,-18 8,-26 C 2,-34 6,-44 0,-54 Z" fill="#241a16"/><path d="M 0,-54 C 6,-44 2,-34 8,-26 C 2,-18 6,-10 0,-2" stroke="#9a5a32" stroke-width="2" fill="none" opacity=".8"/>'
    o += '<path d="M -2,-52 L -2,-4" stroke="#a8988a" stroke-width="1" stroke-dasharray="3 2"/>'
    o += '<circle cx="-11" cy="-32" r="5.6" fill="#050406"/><circle cx="-11" cy="-32" r="5.6" fill="none" stroke="#1e1a22" stroke-width="1"/><circle cx="-12.6" cy="-33.6" r=".7" fill="#3a3440"/><circle cx="-9.4" cy="-33.6" r=".7" fill="#3a3440"/><circle cx="-12.6" cy="-30.4" r=".7" fill="#3a3440"/><circle cx="-9.4" cy="-30.4" r=".7" fill="#3a3440"/><circle cx="-13" cy="-34.5" r="1" fill="#ffffff" opacity=".35"/>'
    o += '<ellipse cx="12" cy="-31" rx="5.5" ry="4" fill="#050406" transform="rotate(20 12 -31)"/><path d="M 8,-29 C 11,-27 15,-28 17,-31" stroke="#6a5a52" stroke-width="1.4" fill="none"/>'   # melted button
    o += '<path d="M -14,-16 l 4,2 l 4,-2 l 4,2 l 4,-2" stroke="#4a1a1e" stroke-width="1.6" fill="none"/><path d="M -12,-18 l 0,4 M -6,-18 l 0,4 M 0,-18 l 0,4" stroke="#4a1a1e" stroke-width="1"/>'
    o += ''
    # yarn hair: two braids on the unburnt side, a singed curled stub on the burnt side
    o += '<path d="M -26,-36 C -30,-58 -6,-62 0,-56 C 6,-60 26,-58 26,-40 C 18,-50 6,-52 0,-50 C -8,-52 -18,-50 -26,-36 Z" fill="#7a4a2a"/><path d="M 0,-56 C 6,-60 26,-58 26,-40 C 18,-50 6,-52 0,-50 Z" fill="#2a1a12"/>'
    o += "".join(f'<path d="M {-22 + k * 4},-56 C {-24 + k * 4},-52 {-24 + k * 4},-46 {-22 + k * 4},-42" stroke="#9a6a3a" stroke-width="1.2" fill="none"/>' for k in range(5))
    o += '<g>' + "".join(f'<ellipse cx="-30" cy="{-30 + k * 9}" rx="5" ry="5.5" fill="{"#7a4a2a" if k % 2 else "#8a5a32"}"/>' for k in range(6)) + '<path d="M -34,24 l 4,10 M -30,24 l 0,12 M -26,24 l -3,10" stroke="#8a5a32" stroke-width="1.6"/><rect x="-35" y="18" width="10" height="5" fill="#c84848"/></g>'
    o += '<path d="M 26,-36 C 34,-34 36,-28 32,-24 C 38,-22 36,-14 30,-16 C 34,-10 28,-6 26,-12" stroke="#1a120e" stroke-width="4" fill="none"/><path d="M 28,-30 c 3,-2 6,0 4,3 M 30,-18 c 3,-2 5,1 3,3" stroke="#5a3a22" stroke-width="1.4" fill="none"/>'
    o += '<path d="M 6,-8 C 12,-14 20,-10 26,-16" stroke="#6a6060" stroke-width="1" fill="none" opacity=".6"/>'   # soot smudge
    return o + '</g>'
INS2["doll"] = ('<rect width="540" height="960" fill="#3a3448"/><rect y="640" width="540" height="320" fill="#4a4250"/><rect y="640" width="540" height="10" fill="#5a5060"/>'
                '<polygon points="380,0 540,0 540,700 300,700" fill="#d8d0e8" opacity=".08" filter="url(#lhaze)"/>'
                '<g transform="translate(270,520) scale(3.6)">' + ragdoll() + '</g>' + note(150, 840, "ตุ๊กตาผ้าโบราณ ชุดดำ ไหม้ครึ่งตัว ตากระดุมดำ"))
ST["steps"] = ST["steps"].replace(ST["steps"][ST["steps"].index('<g transform="translate(270,820) scale(1.8)">'):ST["steps"].index('</g>', ST["steps"].index('<g transform="translate(270,820) scale(1.8)">')) + 4], '<g transform="translate(300,880) scale(.5)">' + ragdoll() + '</g>')

# ---- final scene: embroidered handkerchief "Martha" (replaces the name tag) ----
INS2["tag"] = ('<rect width="540" height="960" fill="#1e1c24"/><ellipse cx="270" cy="460" rx="270" ry="250" fill="url(#lg_fff0dc)" opacity=".4"/>'
  '<linearGradient id="hkShade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fbf6ea"/><stop offset=".55" stop-color="#efe6d2"/><stop offset="1" stop-color="#d8cbb0"/></linearGradient>'
  '<g transform="translate(270,470) rotate(-6)">'
  '<ellipse cx="14" cy="200" rx="230" ry="26" fill="#0a080c" opacity=".5" filter="url(#lsoft)"/>'
  # cloth draped and folded: main square with soft folds, a turned-back corner
  '<path d="M -200,-150 C -120,-170 80,-176 196,-150 C 214,-60 210,60 200,150 C 90,176 -110,172 -204,150 C -216,60 -214,-60 -200,-150 Z" fill="url(#hkShade)"/>'
  '<path d="M -200,-150 C -120,-170 80,-176 196,-150 C 214,-60 210,60 200,150 C 90,176 -110,172 -204,150 C -216,60 -214,-60 -200,-150 Z" fill="none" stroke="#e8dcc4" stroke-width="12" stroke-dasharray="6 5"/>'   # lace / scalloped hem
  '<path d="M -200,-150 C -120,-170 80,-176 196,-150 C 214,-60 210,60 200,150 C 90,176 -110,172 -204,150 C -216,60 -214,-60 -200,-150 Z" fill="none" stroke="#c8b898" stroke-width="1.6" stroke-dasharray="2 3" transform="scale(.9)"/>'   # hand-stitched hem line
  '<path d="M -150,-140 C -100,-40 -120,60 -160,150" stroke="#d8ccb2" stroke-width="10" fill="none" opacity=".7"/><path d="M -146,-140 C -96,-40 -116,60 -156,150" stroke="#fffaf0" stroke-width="3" fill="none" opacity=".8"/>'
  '<path d="M 60,-160 C 90,-60 110,60 90,160" stroke="#d4c6aa" stroke-width="12" fill="none" opacity=".6"/><path d="M 66,-160 C 96,-60 116,60 96,160" stroke="#fffaf0" stroke-width="3" fill="none" opacity=".7"/>'
  '<path d="M 196,150 L 120,150 C 140,120 170,96 200,80 Z" fill="#e2d6bc"/><path d="M 120,150 C 140,120 170,96 200,80" stroke="#c8b898" stroke-width="2" fill="none"/>'   # folded-over corner
  '<circle cx="-120" cy="90" r="22" fill="#c8a868" opacity=".18"/><circle cx="150" cy="-100" r="14" fill="#b8985a" opacity=".2"/>'   # age spots
  # embroidered name: cursive, satin-stitch look (thick thread + stitch texture + highlight)
  '<text x="-6" y="18" text-anchor="middle" font-family="Dancing Script, cursive" font-size="96" font-weight="700" fill="#7a2a2a">Martha</text>'
  '<text x="-6" y="18" text-anchor="middle" font-family="Dancing Script, cursive" font-size="96" font-weight="700" fill="none" stroke="#5a1a1c" stroke-width="1.4" stroke-dasharray="1.6 1.4"/>'
  '<text x="-7.5" y="16.5" text-anchor="middle" font-family="Dancing Script, cursive" font-size="96" font-weight="700" fill="none" stroke="#c87a72" stroke-width=".8" opacity=".6" stroke-dasharray="3 3"/>'
  '<path d="M 112,30 c 10,2 16,8 24,4 c 6,-3 10,4 16,2" stroke="#7a2a2a" stroke-width="1.6" fill="none"/>'   # loose thread tail
  '<g transform="translate(-140,-96)">' + "".join(f'<ellipse cx="0" cy="-6" rx="3.4" ry="6" fill="#9a5a5a" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288)) + '<circle r="2.4" fill="#c8a868"/><path d="M 0,6 C 2,16 8,22 14,24" stroke="#5a7050" stroke-width="2" fill="none"/></g>'   # tiny embroidered flower
  '</g>' + note(140, 820, "ผ้าเช็ดหน้าปักชื่อ Martha ด้วยลายมือ ด้ายใหม่ ไม่มีรอยไหม้"))
