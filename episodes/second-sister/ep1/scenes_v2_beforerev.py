#!/usr/bin/env python3
"""EP1 key frames, round 2: dense props, full-body posed characters, white ornate convent.
Four scenes for review first: 5 (arrival / church exterior), 12 (archive), 14 (kitchen), 16 (bell tower).
Run: python3 scenes_v2.py -> scenes_v2.html"""
import os, re, random, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("cf", os.path.join(HERE, "..", "characters", "build_cast_full.py"))
cf = importlib.util.module_from_spec(spec); spec.loader.exec_module(cf)

POSES = []
def posed(cid, name, aL=0, aR=0, extraL="", extraR="", head=0):
    """Copy a full-body figure as a new <g id=name> with arms rotated at the shoulder (degrees, SVG sense)."""
    s = cf.F[cid].replace(f'id="fb-{cid}"', f'id="{name}"', 1)
    for side, ang, extra in (("L", aL, extraL), ("R", aR, extraR)):
        m = re.search(rf'<g id="{cid}-arm{side}" data-pivot="([-\d.]+),([-\d.]+)">', s)
        if not m: continue
        px, py = m.group(1), m.group(2)
        start = m.start(); end = s.index("</g>", m.end())
        inner = s[m.end():end]
        s = s[:start] + f'<g transform="rotate({ang} {px} {py})">' + inner + extra + "</g>" + s[end + 4:]
    if head:
        s = s.replace(f'<g id="{cid}-head" data-pivot="0,52">', f'<g transform="rotate({head} 0 52)">', 1)
    POSES.append(s)
    return name

def put(name, x, feet, k, light=1.0, sat=1.0, shadow=True):
    y = feet - 372 * k
    st = f' style="filter:brightness({light}) saturate({sat})"' if (light != 1 or sat != 1) else ""
    sh = f'<ellipse cx="{x + 10 * k:.0f}" cy="{feet + 3:.0f}" rx="{58 * k:.0f}" ry="{8 * k:.0f}" fill="#0a080c" opacity=".5"/>' if shadow else ""
    return f'{sh}<g filter="url(#drop)"><g{st}><g transform="translate({x},{y:.0f}) scale({k})"><use href="#{name}"/></g></g></g>'

R = random.Random(11)
def motes(x0, y0, x1, y1, n, col="#e8e2ff"):
    o = []
    for i in range(n):
        x = R.uniform(x0, x1); y = R.uniform(y0, y1)
        if R.random() < .6:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(.6, 1.3):.1f}" fill="{col}" opacity="{R.uniform(.4, .85):.2f}" filter="url(#moteGlow)"/>')
        else:
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{R.uniform(1.3, 2.2):.1f}" fill="{col}" opacity="{R.uniform(.18, .32):.2f}" filter="url(#moteFar)"/>')
    return "".join(o)

def glow(x, y, r, g="glowW", op=1.0):
    return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r}" fill="url(#{g})" opacity="{op}" style="mix-blend-mode:screen"/>'

def frame(body, chip, th, en, label):
    s = f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">{body}'
    s += '<rect width="540" height="960" filter="url(#paint)" opacity=".2" style="mix-blend-mode:soft-light"/>'
    s += '<rect width="540" height="960" fill="url(#vig)"/>'
    s += '<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:screen"/><rect width="540" height="960" filter="url(#grain)" opacity=".045" style="mix-blend-mode:overlay"/>'
    w = 14 + len(chip) * 7.4
    s += f'<rect x="24" y="28" width="{w:.0f}" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8f74d8" stroke-width="1.4"/><text x="{24 + w / 2:.0f}" y="48" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="500" fill="#e6e0f4">{chip}</text>'
    s += '<g transform="translate(500,44)" opacity=".8"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="none" stroke="#b18cff" stroke-width="1.6"/><circle r="3.6" fill="#b18cff"/></g>'
    lines = th.split("|"); el = en.split("|")
    y = 712 - (len(lines) * 27 + len(el) * 17) / 2 + 20
    s += '<g class="subs" font-family="IBM Plex Sans Thai, sans-serif" text-anchor="middle" filter="url(#subStroke)">'
    for L in lines: s += f'<text x="270" y="{y:.0f}" font-size="20" font-weight="700" fill="#ffd84a">{L}</text>'; y += 27
    for L in el: s += f'<text x="270" y="{y:.0f}" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#fff">{L}</text>'; y += 17
    return s + '</g></svg>'

# ---------------- reusable architecture ----------------
def church(x, y, k=1.0, night=False):
    """White Gothic church with one tall central tower, dome + cross, pinnacles, balustrades, pointed arches."""
    W, L, D = ("#d8d4e0", "#eeeaf2", "#a6a0b4") if not night else ("#7a7898", "#9a98b8", "#4a4868")
    G = "#2a2836" if not night else "#141420"
    o = f'<g transform="translate({x},{y}) scale({k})">'
    # nave block with side aisles
    o += f'<rect x="-150" y="80" width="300" height="230" fill="{W}"/><rect x="-150" y="80" width="80" height="230" fill="{L}"/><rect x="90" y="80" width="60" height="230" fill="{D}"/>'
    o += f'<rect x="-156" y="72" width="312" height="10" fill="{L}"/>' + "".join(f'<rect x="{bx}" y="60" width="5" height="12" fill="{W}"/>' for bx in range(-152, 152, 9)) + f'<rect x="-156" y="56" width="312" height="5" fill="{L}"/>'
    for px in (-150, -90, 90, 150):  # buttress pinnacles
        o += f'<rect x="{px - 6}" y="20" width="12" height="290" fill="{L if px < 0 else D}"/><path d="M {px - 8},22 L {px},-14 L {px + 8},22 Z" fill="{L if px < 0 else D}"/><circle cx="{px}" cy="-16" r="2.5" fill="{L}"/>'
    # side doors + windows (pointed arches)
    for dx in (-120, 120):
        o += f'<path d="M {dx - 18},310 L {dx - 18},230 Q {dx},196 {dx + 18},230 L {dx + 18},310 Z" fill="{G}"/><path d="M {dx - 24},310 L {dx - 24},228 Q {dx},186 {dx + 24},228" fill="none" stroke="{L}" stroke-width="3"/>'
        o += f'<path d="M {dx - 10},160 L {dx - 10},120 Q {dx},102 {dx + 10},120 L {dx + 10},160 Z" fill="{G}"/>'
    # tower
    o += f'<rect x="-50" y="-150" width="100" height="460" fill="{W}"/><rect x="-50" y="-150" width="30" height="460" fill="{L}"/><rect x="26" y="-150" width="24" height="460" fill="{D}"/>'
    o += f'<path d="M -34,310 L -34,200 Q 0,140 34,200 L 34,310 Z" fill="{G}"/><path d="M -42,310 L -42,198 Q 0,124 42,198" fill="none" stroke="{L}" stroke-width="4"/>'
    o += f'<path d="M -22,300 L -22,210 Q 0,170 22,210 L 22,300 Z" fill="{"#3a2a26" if not night else "#1a1214"}"/><path d="M 0,186 L 0,300" stroke="{G}" stroke-width="2"/>'
    o += f'<circle cx="0" cy="110" r="22" fill="{G}"/><circle cx="0" cy="110" r="16" fill="{"#4c4f8c" if not night else "#2a2c5c"}"/><path d="M 0,94 L 0,126 M -16,110 L 16,110" stroke="{G}" stroke-width="2"/>'
    for ty in (40, -40):
        o += f'<path d="M -18,{ty + 40} L -18,{ty} Q -9,{ty - 16} 0,{ty} L 0,{ty + 40} Z M 2,{ty + 40} L 2,{ty} Q 11,{ty - 16} 20,{ty} L 20,{ty + 40} Z" fill="{G}"/>'
    o += f'<rect x="-56" y="-158" width="112" height="9" fill="{L}"/>' + "".join(f'<rect x="{bx}" y="-172" width="4" height="14" fill="{W}"/>' for bx in range(-54, 56, 8)) + f'<rect x="-56" y="-176" width="112" height="5" fill="{L}"/>'
    for px in (-50, 50):
        o += f'<rect x="{px - 5}" y="-200" width="10" height="44" fill="{L if px < 0 else D}"/><path d="M {px - 6},-198 L {px},-224 L {px + 6},-198 Z" fill="{L if px < 0 else D}"/>'
    # belfry (octagonal drum) + dome + cross
    o += f'<rect x="-32" y="-250" width="64" height="76" fill="{W}"/><rect x="-32" y="-250" width="18" height="76" fill="{L}"/><rect x="16" y="-250" width="16" height="76" fill="{D}"/>'
    o += f'<path d="M -18,-180 L -18,-226 Q -9,-240 0,-226 L 0,-180 Z M 2,-180 L 2,-226 Q 11,-240 20,-226 L 20,-180 Z" fill="{G}"/>'
    o += f'<rect x="-38" y="-256" width="76" height="8" fill="{L}"/>'
    o += f'<path d="M -34,-256 C -34,-300 34,-300 34,-256 Z" fill="{W}"/><path d="M -34,-256 C -34,-292 -8,-298 0,-298 C -12,-290 -16,-272 -14,-256 Z" fill="{L}"/><path d="M 14,-256 C 16,-276 10,-292 0,-298 C 20,-296 34,-286 34,-256 Z" fill="{D}"/>'
    o += f'<rect x="-4" y="-312" width="8" height="16" fill="{W}"/><rect x="-2" y="-340" width="4" height="30" fill="{L}"/><rect x="-10" y="-332" width="20" height="4" fill="{L}"/>'
    # grime streaks
    o += ''.join(f'<path d="M {sx},{sy} L {sx + 1},{sy + R.randint(30, 90)}" stroke="{D}" stroke-width="{R.uniform(2, 5):.1f}" opacity=".35"/>' for sx, sy in ((-140, 82), (-60, 84), (70, 86), (-40, -146), (30, -146), (-20, -170)))
    return o + '</g>'

def fence(y0, y1, x0=-10, x1=560, gap=None):
    o = ""
    for x in range(x0, x1, 22):
        if gap and gap[0] < x < gap[1]: continue
        o += f'<rect x="{x}" y="{y0}" width="5" height="{y1 - y0}" fill="#16121a"/><path d="M {x - 3},{y0} L {x + 2.5},{y0 - 14} L {x + 8},{y0} Z" fill="#16121a"/>'
    o += f'<rect x="{x0}" y="{y0 + 16}" width="{x1 - x0}" height="6" fill="#16121a"/><rect x="{x0}" y="{y1 - 30}" width="{x1 - x0}" height="6" fill="#16121a"/>'
    o += "".join(f'<circle cx="{x + 13}" cy="{y0 + 40}" r="6" fill="none" stroke="#16121a" stroke-width="2.4"/>' for x in range(x0, x1, 22) if not (gap and gap[0] < x < gap[1]))
    return o

def frangipani(x, y, k=1.0, dim=1.0):
    o = f'<g transform="translate({x},{y}) scale({k})" opacity="{dim}">'
    o += '<path d="M -6,200 C -8,140 -4,100 0,60 L 8,60 C 6,110 10,150 10,200 Z" fill="#6a5a58"/><path d="M 2,90 C -20,70 -40,60 -60,56 L -58,50 C -36,52 -16,62 4,80 Z M 6,70 C 24,46 40,36 60,30 L 62,36 C 44,42 28,54 10,76 Z" fill="#6a5a58"/>'
    for (cx, cy, r) in ((-60, 40, 34), (60, 20, 38), (0, 30, 40), (-30, 10, 30), (30, -6, 28)):
        o += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * .6:.0f}" fill="#3e5a3e"/><ellipse cx="{cx - r * .3:.0f}" cy="{cy - r * .2:.0f}" rx="{r * .6:.0f}" ry="{r * .35:.0f}" fill="#4e6e4a"/>'
        for j in range(5):
            fx, fy = cx + R.uniform(-r * .7, r * .7), cy + R.uniform(-r * .4, r * .2)
            o += f'<g transform="translate({fx:.0f},{fy:.0f})">' + "".join(f'<ellipse cx="0" cy="-3" rx="2" ry="3.4" fill="#f6f0e6" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288)) + '<circle r="1.4" fill="#f2d880"/></g>'
    return o + '</g>'

def pigeon(x, y, k=1.0, flip=1):
    return (f'<g transform="translate({x},{y}) scale({k * flip},{k})"><ellipse cx="0" cy="0" rx="9" ry="6" fill="#9a98a8"/><circle cx="7" cy="-5" r="4" fill="#a8a6b6"/>'
            f'<path d="M 10,-5 l 4,1 l -4,1 Z" fill="#c8a080"/><path d="M -4,-2 C -10,-4 -14,0 -16,4 L -6,3 Z" fill="#7a7888"/><path d="M -8,4 L -16,6 L -10,2 Z" fill="#6a6878"/></g>')

def drop_shadow_rect(x, y, w, h, op=.35):
    return f'<rect x="{x + 6}" y="{y + 8}" width="{w}" height="{h}" fill="#0a080c" opacity="{op}" filter="url(#soft)"/>'

SCENES = []

# =============== SCENE 5: arrival, church exterior, Catarina at the iron fence ===============
cat_folder = '<g transform="translate(-52,224)"><rect x="-12" y="-6" width="24" height="32" rx="2" fill="#3b3f4a"/><rect x="-12" y="-6" width="6" height="32" fill="#535866"/><rect x="-6" y="-2" width="14" height="4" fill="#e8e0d0"/></g>'
posed("cat", "cat_point", aL=-6, aR=-118, extraL=cat_folder)          # right arm (viewer-right) raised, pointing at the fence
mek_bag = '<g transform="translate(50,214)"><path d="M -6,-150 L 4,-150 L 2,0 L -8,0 Z" fill="#3a3238" opacity="0"/></g>'
posed("mek", "mek_listen", aL=4, aR=-4)
posed("daeng", "daeng_wave", aL=150, aR=-4)

b = []
B = b.append
B('<rect width="540" height="960" fill="url(#duskSky)"/>')
# Bangkok beyond the wall: condo towers, power lines
B('<g filter="url(#dof2)" opacity=".85">' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{520 - y}" fill="{c}"/>' for x, y, w, c in ((0, 150, 70, "#6a6488"), (60, 210, 50, "#5e587c"), (430, 120, 80, "#6a6488"), (500, 200, 60, "#5e587c"), (380, 230, 50, "#7a7498")))
  + "".join(f'<rect x="{x}" y="{y}" width="5" height="4" fill="#f4e8d8" opacity=".6"/>' for x, y in ((12, 180), (30, 220), (48, 260), (446, 150), (470, 190), (490, 240), (450, 300), (396, 260))) + '</g>')
B('<path d="M -10,250 Q 140,290 300,260 T 560,240 M -10,262 Q 150,300 310,272 T 560,254" stroke="#2a2434" stroke-width="1.2" fill="none" opacity=".7"/>')
# the church (behind the sisters' fence, in the cloister)
B('<g filter="url(#dof)">' + church(285, 360, .78) + '</g>')
B(pigeon(258, 108, .8) + pigeon(290, 114, .7, -1) + pigeon(214, 254, .7) + pigeon(360, 252, .7, -1))
# white convent wing left with dark shutters, flowering vine
B('<g filter="url(#dof)"><rect x="-10" y="330" width="170" height="250" fill="#ddd8e2"/><rect x="-10" y="330" width="170" height="14" fill="#efeaf2"/>'
  + "".join(f'<path d="M {x},{y + 50} L {x},{y + 10} Q {x + 14},{y - 6} {x + 28},{y + 10} L {x + 28},{y + 50} Z" fill="#2a2632"/><rect x="{x - 9}" y="{y + 6}" width="8" height="46" fill="#4a5a52"/><rect x="{x + 29}" y="{y + 6}" width="8" height="46" fill="#4a5a52"/>' for x in (20, 100) for y in (370, 470))
  + '<path d="M 150,340 C 130,380 160,420 140,470 C 126,500 150,540 140,580" stroke="#3e5a3e" stroke-width="5" fill="none"/>'
  + "".join(f'<circle cx="{140 + R.uniform(-14, 14):.0f}" cy="{R.uniform(350, 570):.0f}" r="3" fill="#c88aa8"/>' for _ in range(16)) + '</g>')
# cloister lawn, path, grotto with Mary statue and candles
B('<rect x="0" y="560" width="540" height="40" fill="#5a6a52"/>')
B('<g filter="url(#dof)"><path d="M 400,600 C 400,520 470,500 500,520 C 530,540 540,600 540,600 Z" fill="#5a5660"/><path d="M 430,600 C 432,560 470,544 490,560 C 504,572 506,600 506,600 Z" fill="#2a2632"/>'
  '<path d="M 464,596 L 464,572 C 464,562 476,562 476,572 L 476,596 Z" fill="#eeeaf2"/><circle cx="470" cy="566" r="5" fill="#eeeaf2"/>' + "".join(f'<rect x="{440 + i * 7}" y="590" width="3" height="7" fill="#f4ecd8"/>' for i in range(8)) + '</g>')
B(glow(470, 590, 50, "glowW", .7))
# iron fence with padlocked gate and a warning sign
B(fence(500, 690, gap=None))
B('<rect x="232" y="560" width="36" height="46" rx="4" fill="#2a2420"/><path d="M 240,560 C 240,542 260,542 260,560" fill="none" stroke="#2a2420" stroke-width="5"/><rect x="246" y="574" width="8" height="12" fill="#5a4a3a"/>')
B('<path d="M 210,600 L 300,600" stroke="#3a3430" stroke-width="3"/>')
B('<g transform="translate(240,520)"><rect x="-4" y="0" width="4" height="40" fill="#16121a"/><rect x="-60" y="-34" width="120" height="38" rx="3" fill="#efe8da"/><rect x="-60" y="-34" width="120" height="8" fill="#8e1b24"/>'
  '<text x="0" y="-12" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9.5" font-weight="700" fill="#3a2a22">เขตพักซิสเตอร์</text><text x="0" y="0" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7.5" fill="#5a4a3a">ห้ามบุคคลภายนอกเข้า หลัง 18.00 น.</text></g>')
# foreground: courtyard paving, frangipani, bench, bicycle, notice board, potted plants
B('<path d="M 0,690 L 540,690 L 540,960 L 0,960 Z" fill="#8a8494"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#6e6878" stroke-width="1.4"/>' for y in (720, 760, 810, 870, 940)) + "".join(f'<path d="M {x},690 L {x * 1.6 - 160:.0f},960" stroke="#6e6878" stroke-width="1.2"/>' for x in range(0, 560, 60)))
B('<path d="M 0,690 L 540,690 L 540,708 L 0,708 Z" fill="#a6a0b0"/>')
B(frangipani(70, 520, 1.25))
B("".join(f'<g transform="translate({R.uniform(20, 200):.0f},{R.uniform(720, 900):.0f}) rotate({R.uniform(0, 360):.0f})">' + "".join(f'<ellipse cx="0" cy="-3" rx="2.2" ry="3.6" fill="#f6f0e6" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288)) + '<circle r="1.4" fill="#f2d880"/></g>' for _ in range(9)))
B('<g transform="translate(455,770)">' + drop_shadow_rect(-60, -20, 120, 14) + '<rect x="-60" y="-34" width="120" height="8" fill="#5a4234"/><rect x="-60" y="-20" width="120" height="8" fill="#4a3428"/><rect x="-56" y="-12" width="6" height="30" fill="#2a2024"/><rect x="50" y="-12" width="6" height="30" fill="#2a2024"/>'
  '<rect x="-30" y="-40" width="26" height="6" fill="#2a3a5a"/><rect x="-26" y="-46" width="20" height="6" fill="#6a2a32"/></g>')
B('<g transform="translate(20,860)" stroke="#2a2830" stroke-width="3" fill="none"><circle cx="0" cy="0" r="30"/><circle cx="96" cy="0" r="30"/><path d="M 0,0 L 36,-40 L 80,-40 L 96,0 M 36,-40 L 48,0 L 80,-40 M 30,-52 L 44,-52 M 80,-40 L 76,-58 L 90,-60"/><path d="M 44,-56 L 56,-56" stroke-width="6" stroke="#4a3a3a"/></g>'
  '<path d="M 70,824 L 106,824 L 104,846 L 72,846 Z" fill="#8a6a4a" opacity=".9"/>')
B('<g transform="translate(240,760)"><rect x="-4" y="0" width="5" height="60" fill="#3a2a22"/><rect x="45" y="0" width="5" height="60" fill="#3a2a22"/><rect x="-10" y="-60" width="66" height="62" fill="#5a4234"/><rect x="-6" y="-56" width="58" height="54" fill="#8a7458"/>'
  '<rect x="-2" y="-52" width="22" height="26" fill="#efe8da" transform="rotate(-3 9 -39)"/><rect x="24" y="-50" width="24" height="18" fill="#c8d8e8"/><rect x="26" y="-30" width="20" height="24" fill="#f4dcc8" transform="rotate(4 36 -18)"/><rect x="0" y="-24" width="20" height="18" fill="#e8e0b8"/>'
  '<circle cx="9" cy="-50" r="1.6" fill="#b33a3a"/><circle cx="36" cy="-49" r="1.6" fill="#2a5a8a"/><path d="M 2,-44 L 16,-44 M 2,-40 L 14,-40 M 2,-36 L 16,-36" stroke="#8a8070" stroke-width="1"/></g>')
for (px, py, sc) in ((180, 700, 1.0), (520, 700, 1.1)):
    B(f'<g transform="translate({px},{py}) scale({sc})"><path d="M -14,0 L 14,0 L 10,26 L -10,26 Z" fill="#a8604a"/><path d="M -16,-4 L 16,-4 L 14,2 L -14,2 Z" fill="#8a4a38"/>' + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="8" ry="4" fill="#4e6e4a" transform="rotate({dx * 3} {dx} {dy})"/>' for dx, dy in ((-8, -10), (8, -12), (0, -18), (-12, -18), (12, -22))) + '</g>')
# characters: Catarina points at the fence, Mek listens with his camera bag, Daeng waves from far behind the fence
B(put("daeng_wave", 150, 610, .52, .78, .8))
B(put("cat_point", 360, 900, .96, .97))
B(put("mek_listen", 130, 924, 1.0, .95))
B(glow(110, 180, 260, "glowW", .35) + motes(60, 120, 500, 700, 26, "#fff4e6"))
SCENES.append(("ฉาก 5 · มาถึงคอนแวนต์", "โบสถ์ขาวหอระฆังกลาง ยอดโดม มีรั้วเหล็กกั้นเขตซิสเตอร์ มาเธอร์คาทารีนาชี้รั้ว ป้าแดงโบกมือจากอีกฝั่ง",
  frame("".join(b), "20 พ.ย. · 16:30", "หลังรั้วนั้นคือที่พักของซิสเตอร์|ห้ามเข้าเด็ดขาด", "Behind that fence is the sisters' house. Never go in.", "มาถึงคอนแวนต์")))

# =============== SCENE 12: archive attic ===============
photo = '<g transform="translate(46,212) rotate(-20)"><rect x="-10" y="-14" width="20" height="24" fill="#efe8da"/><rect x="-8" y="-12" width="16" height="16" fill="#8a8070"/><circle cx="-3" cy="-6" r="3" fill="#f4f0e6"/><circle cx="3" cy="-6" r="3" fill="#c7bdab"/></g>'
posed("mek", "mek_photo", aL=-28, aR=-34, extraR=photo)
b = []; B = b.append
B('<rect width="540" height="960" fill="#2a2124"/>')
# roof: sloped plank ceiling with heavy beams, round window
B('<path d="M 0,0 L 540,0 L 540,240 L 270,60 L 0,240 Z" fill="#3a2a26"/>' + "".join(f'<path d="M {270 + (x - 270) * .2:.0f},{60 + abs(x - 270) * .1:.0f} L {x},{240 if x in (0, 540) else 0}" stroke="#2a1c1a" stroke-width="2"/>' for x in range(0, 541, 45)))
B('<path d="M 0,240 L 270,60 L 540,240 L 540,262 L 270,82 L 0,262 Z" fill="#5a4234"/><path d="M 0,262 L 270,82 L 540,262" stroke="#2a1c1a" stroke-width="3" fill="none"/>')
B('<rect x="130" y="40" width="14" height="230" fill="#4a3428" transform="skewX(-12)"/><rect x="400" y="40" width="14" height="230" fill="#3a2820" transform="skewX(12)"/>')
B('<circle cx="270" cy="170" r="54" fill="#1e1618"/><circle cx="270" cy="170" r="46" fill="#c8d0e8"/><circle cx="270" cy="170" r="46" fill="url(#skyDay)"/><path d="M 270,124 L 270,216 M 224,170 L 316,170 M 238,138 L 302,202 M 302,138 L 238,202" stroke="#1e1618" stroke-width="4"/>')
# walls: plaster with stains, shelves loaded with archive boxes by year
B('<rect x="0" y="262" width="540" height="440" fill="#c8bfb8"/><rect x="0" y="262" width="540" height="440" fill="url(#atticWash)"/>')
B('<path d="M 60,262 C 70,300 50,330 64,380 L 40,380 C 30,330 44,300 40,262 Z" fill="#8a7a70" opacity=".35"/><path d="M 470,262 C 480,320 462,360 476,420 L 452,420 C 440,360 456,320 450,262 Z" fill="#8a7a70" opacity=".3"/>')
def shelf(x0, x1, y, labels):
    o = f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="7" fill="#5a4234"/><rect x="{x0}" y="{y + 7}" width="{x1 - x0}" height="4" fill="#2a1c1a" opacity=".5"/>'
    x = x0 + 4
    for i, lab in enumerate(labels):
        w = 36 if lab else 14; h = 40 if lab else 46
        c = ("#a88a64", "#8a7050", "#b89a74", "#7a6448")[i % 4]
        if lab:
            o += f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{c}"/><rect x="{x}" y="{y - h}" width="{w * .3:.0f}" height="{h}" fill="#000" opacity=".12"/><rect x="{x + 6}" y="{y - h + 12}" width="{w - 12}" height="12" fill="#efe6d4"/><text x="{x + w / 2:.0f}" y="{y - h + 21}" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7.5" fill="#3a2a22">{lab}</text>'
        else:
            o += f'<rect x="{x}" y="{y - h}" width="{w}" height="{h}" fill="{("#5a2a2e", "#2a3a5a", "#3a4a3a")[i % 3]}"/><rect x="{x}" y="{y - h + 6}" width="{w}" height="2" fill="#c8b07a"/>'
        x += w + 3
        if x > x1 - 20: break
    return o
B(shelf(10, 200, 380, ["2469", "", "", "2485", "2501", "", "2520"]) + shelf(10, 200, 470, ["", "", "2530", "2540", "", "2549", ""]) + shelf(10, 200, 560, ["ทะเบียน", "", "", "รูปถ่าย", "", ""]))
B(shelf(340, 530, 380, ["", "จดหมาย", "", "", "ใบเสร็จ", ""]) + shelf(340, 530, 470, ["2552", "", "2560", "", "", "2568"]) + shelf(340, 530, 560, ["", "", "โรงเรียน", "", "แผนผัง", ""]))
# pinned children's drawings, a crucifix, hanging bulb
for (dx, dy, r, c) in ((226, 300, -6, "#f4ecd8"), (262, 296, 4, "#efe6e0"), (298, 302, -3, "#f4ecd8")):
    B(f'<g transform="translate({dx},{dy}) rotate({r})"><rect x="-14" y="-18" width="28" height="34" fill="{c}"/><circle cx="0" cy="-17" r="1.6" fill="#b33a3a"/><path d="M -8,8 L -8,-2 L 0,-8 L 8,-2 L 8,8 Z" fill="none" stroke="#5a7aa8" stroke-width="1.4"/><circle cx="6" cy="-10" r="3" fill="none" stroke="#d8a040" stroke-width="1.2"/><path d="M -6,12 l 2,-5 l 2,5 M 2,12 l 2,-5 l 2,5" stroke="#3a3a3a" stroke-width="1"/></g>')
B('<path d="M 270,250 L 270,330" stroke="#1e1618" stroke-width="1.4"/><path d="M 262,330 L 278,330 L 274,342 L 266,342 Z" fill="#3a3030"/><circle cx="270" cy="346" r="6" fill="#fff4e0"/>')
# floor and clutter: dress form with an old habit, rocking horse, globe, typewriter, ledgers, film tins, tripod
B('<path d="M 0,700 L 540,700 L 540,960 L 0,960 Z" fill="#4a3630"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#3a2824" stroke-width="2"/>' for y in (740, 790, 850, 920)))
B('<g transform="translate(470,700)"><rect x="-2" y="-30" width="4" height="30" fill="#2a2024"/><ellipse cx="0" cy="0" rx="18" ry="4" fill="#2a2024"/>'
  '<path d="M -22,-130 C -24,-160 24,-160 22,-130 L 26,-30 L -26,-30 Z" fill="#d8d0c4"/><path d="M -22,-130 C -24,-160 -6,-160 0,-160 L -6,-30 L -26,-30 Z" fill="#e8e2d8"/>'
  '<path d="M -18,-176 C -18,-196 18,-196 18,-176 L 22,-130 L -22,-130 Z" fill="#1a1520"/><ellipse cx="0" cy="-160" rx="10" ry="4" fill="#ece6dc"/></g>')
B('<g transform="translate(70,770)"><path d="M -40,20 C -30,30 30,30 40,20" stroke="#6a4a34" stroke-width="5" fill="none"/><path d="M -24,-16 L 26,-16 L 22,8 L -20,8 Z" fill="#c8a080"/><path d="M -24,-16 L 0,-16 L -2,8 L -20,8 Z" fill="#d8b090"/>'
  '<path d="M 22,-16 C 34,-30 40,-40 36,-52 L 26,-48 C 28,-38 24,-30 16,-20 Z" fill="#c8a080"/><path d="M 30,-50 L 40,-58 L 38,-46 Z" fill="#6a4a34"/><circle cx="33" cy="-46" r="1.6" fill="#1a1216"/>'
  '<path d="M -16,8 L -22,22 M 16,8 L 22,22 M -6,8 L -8,22 M 8,8 L 10,22" stroke="#8a6a4a" stroke-width="3"/><path d="M -26,-16 L -34,-4" stroke="#6a4a34" stroke-width="3"/></g>')
B('<g transform="translate(420,830)"><circle cx="0" cy="-30" r="20" fill="#7a8a6a"/><path d="M -12,-40 C -4,-44 4,-36 10,-42 M -14,-24 C -4,-20 6,-30 14,-22" stroke="#c8b07a" stroke-width="2" fill="none"/><path d="M -22,-30 A 22,22 0 0 0 22,-30" stroke="#6a5a3a" stroke-width="2.4" fill="none"/><rect x="-2" y="-8" width="4" height="10" fill="#5a4234"/><ellipse cx="0" cy="4" rx="12" ry="3" fill="#5a4234"/></g>')
B('<g transform="translate(150,900)"><rect x="-30" y="-20" width="60" height="20" rx="3" fill="#2a2a30"/><rect x="-24" y="-34" width="48" height="16" fill="#3a3a40"/><rect x="-20" y="-46" width="40" height="14" fill="#efe8da"/>' + "".join(f'<circle cx="{-22 + i * 6}" cy="-8" r="2" fill="#c8c4b8"/>' for i in range(8)) + '</g>')
B('<g transform="translate(350,920)">' + "".join(f'<rect x="-22" y="{-10 - i * 8}" width="44" height="8" fill="{c}" transform="rotate({r} 0 {-6 - i * 8})"/>' for i, (c, r) in enumerate((("#5a2a2e", 0), ("#2a3a5a", 3), ("#3a4a3a", -2), ("#6a4a34", 4)))) + '</g>')
B('<g transform="translate(240,930)">' + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="9" ry="3" fill="#8a8a92"/><ellipse cx="{dx}" cy="{dy - 2}" rx="9" ry="3" fill="#b8b8c0"/>' for dx, dy in ((-12, 0), (8, 2), (-2, -6))) + '</g>')
B('<g stroke="#1e1a1e" stroke-width="3"><path d="M 300,520 L 290,700 M 300,520 L 312,700 M 300,520 L 300,700"/></g><rect x="290" y="502" width="22" height="16" rx="2" fill="#2b2b30"/><circle cx="312" cy="510" r="6" fill="#16161a"/>')
B('<path d="M 0,0 L 70,30 M 0,0 L 40,60 M 22,10 Q 18,22 12,26 M 44,20 Q 34,40 24,46" stroke="#e8e2ea" stroke-width=".7" fill="none" opacity=".35"/>')
# Mek at the table holding an old photo; the table with the 2549 album
B(put("mek_photo", 300, 880, 1.04, .92))
B('<path d="M 150,640 L 460,640 L 480,680 L 130,680 Z" fill="#6a4a3a"/><rect x="130" y="680" width="350" height="20" fill="#3a2820"/><rect x="140" y="700" width="10" height="120" fill="#2a1c18"/><rect x="460" y="700" width="10" height="120" fill="#2a1c18"/>')
B('<g transform="translate(300,654)"><path d="M -80,-6 L 0,-12 L 0,16 L -82,20 Z" fill="#5a3a2a"/><path d="M 80,-6 L 0,-12 L 0,16 L 82,20 Z" fill="#4a2e22"/><path d="M -72,-6 L -4,-10 L -4,14 L -74,18 Z" fill="#e8dfcc"/><path d="M 72,-6 L 4,-10 L 4,14 L 74,18 Z" fill="#ddd2bc"/>'
  '<rect x="-64" y="-6" width="24" height="18" fill="#8a8070"/><circle cx="-58" cy="0" r="3.4" fill="#f4f0e6"/><circle cx="-46" cy="0" r="3.4" fill="#c7bdab"/><rect x="-34" y="-6" width="24" height="18" fill="#8a8070"/><circle cx="-28" cy="0" r="3.4" fill="#f4f0e6"/><circle cx="-16" cy="0" r="3.4" fill="#c7bdab"/>'
  '<rect x="14" y="-6" width="24" height="18" fill="#8a8070"/><circle cx="20" cy="0" r="3.4" fill="#c7bdab"/><circle cx="32" cy="0" r="3.4" fill="#f4f0e6"/><rect x="44" y="-6" width="24" height="18" fill="#8a8070"/><circle cx="50" cy="0" r="3.4" fill="#c7bdab"/><circle cx="62" cy="0" r="3.4" fill="#f4f0e6"/></g>')
B('<rect x="400" y="626" width="34" height="14" rx="2" fill="#efe8da" transform="rotate(8 417 633)"/><rect x="170" y="630" width="20" height="10" fill="#c8b07a"/><path d="M 196,636 l 16,-2" stroke="#2a2420" stroke-width="2"/>')
# light: oculus beam with dust
B('<polygon points="230,140 310,140 460,960 120,960" fill="url(#beamW)" filter="url(#haze)" style="mix-blend-mode:screen"/>' + glow(270, 346, 140, "glowW", .6) + motes(130, 200, 440, 760, 40, "#fff0dc"))
SCENES.append(("ฉาก 12 · ห้องเก็บเอกสาร", "ห้องใต้หลังคา ลังเอกสารร้อยปีตามปี ม้าโยกของเด็กกำพร้า หุ่นใส่ชุดซิสเตอร์เก่า เมฆถือรูปที่หน้าถูกขูด",
  frame("".join(b), "21 พ.ย. · 10:20", "ทุกรูป… หน้าของมาร์ธา|ถูกขูดออกทุกใบ", "Every photo. Martha's face, scratched out of every one.", "ห้องเก็บเอกสาร")))

# =============== SCENE 14: kitchen ===============
ladle = '<g transform="translate(50,226) rotate(12)"><rect x="-1.6" y="-40" width="3.2" height="40" fill="#8a8a94"/><ellipse cx="0" cy="2" rx="7" ry="4" fill="#9a9aa4"/></g>'
posed("daeng", "daeng_ladle", aL=-26, aR=-38, extraR=ladle)
kettle = '<g transform="translate(-52,226)"><path d="M -14,4 C -14,-10 14,-10 14,4 L 15,20 L -15,20 Z" fill="#7a7a86"/><path d="M -15,6 L -26,-2 L -24,4 L -16,14 Z" fill="#6a6a76"/><path d="M -10,-6 C -8,-18 8,-18 10,-6" fill="none" stroke="#3a3a44" stroke-width="3"/></g>'
posed("agnes", "agnes_kettle", aL=-8, aR=4, extraL="")
cf.F["agnes"]  # keep
posed("agnes", "agnes_kettleR", aL=4, aR=-14, extraR=kettle.replace("-52,226", "52,226").replace("-26,-2", "26,-2").replace("-24,4", "24,4").replace("-16,14", "16,14").replace("-15,6", "15,6"))
posed("mek", "mek_sit", aL=-30, aR=30)
b = []; B = b.append
B('<rect width="540" height="960" fill="#2a2228"/>')
# tiled wall (white + sage band), shelves of pots, hanging utensils, calendar, radio, window to the night
B('<rect x="0" y="80" width="540" height="560" fill="#d6d2c8"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#b8b2a6" stroke-width="1"/>' for y in range(100, 640, 22)) + "".join(f'<path d="M {x},80 L {x},640" stroke="#b8b2a6" stroke-width="1"/>' for x in range(0, 541, 22)))
B('<rect x="0" y="420" width="540" height="24" fill="#8aa08a"/><rect x="0" y="80" width="540" height="560" fill="url(#kitchenWash)"/>')
B('<rect x="0" y="0" width="540" height="80" fill="#3a3030"/>')
B('<g transform="translate(400,120)"><rect x="0" y="0" width="120" height="150" fill="#3a3030"/><rect x="6" y="6" width="108" height="138" fill="url(#nightSky)"/>' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{144 - y}" fill="#1e2244"/>' for x, y, w in ((10, 80, 20), (34, 60, 26), (66, 90, 18), (88, 70, 22))) + '<path d="M 60,6 L 60,144 M 6,74 L 114,74" stroke="#3a3030" stroke-width="5"/><circle cx="96" cy="26" r="7" fill="#e8ecff" opacity=".8"/></g>')
B('<rect x="20" y="200" width="200" height="8" fill="#5a4234"/><rect x="20" y="300" width="200" height="8" fill="#5a4234"/>')
for (x, y, w, h, c) in ((30, 168, 40, 32, "#9a9aa4"), (78, 160, 46, 40, "#b8b8c0"), (132, 172, 34, 28, "#8a8a94"), (172, 166, 40, 34, "#a8604a"), (32, 266, 30, 34, "#e8e0d0"), (68, 272, 30, 28, "#e8e0d0"), (106, 258, 50, 42, "#7a7a86"), (164, 270, 46, 30, "#c8b890")):
    B(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{c}"/><rect x="{x}" y="{y}" width="{w * .3:.0f}" height="{h}" rx="3" fill="#fff" opacity=".18"/><rect x="{x - 3}" y="{y}" width="{w + 6}" height="4" rx="2" fill="#000" opacity=".2"/>')
B('<rect x="236" y="210" width="140" height="4" fill="#3a3030"/>' + "".join(f'<path d="M {x},214 L {x},{214 + h}" stroke="#8a8a94" stroke-width="2.4"/><ellipse cx="{x}" cy="{216 + h}" rx="{r}" ry="{r * .6:.1f}" fill="#9a9aa4"/>' for x, h, r in ((250, 50, 7), (272, 60, 5), (294, 44, 8), (316, 56, 5), (338, 48, 6), (360, 40, 9))))
B('<g transform="translate(236,110)"><rect x="0" y="0" width="56" height="74" fill="#efe8da"/><rect x="0" y="0" width="56" height="12" fill="#8e1b24"/><rect x="6" y="16" width="44" height="26" fill="#6a7aa8"/><ellipse cx="28" cy="29" rx="8" ry="10" fill="#e8e0d0"/><circle cx="28" cy="22" r="4" fill="#f0d8c0"/>' + "".join(f'<rect x="{6 + (i % 7) * 6.4:.1f}" y="{48 + (i // 7) * 6}" width="5" height="4" fill="{"#b33a3a" if i == 20 else "#c8c0b0"}"/>' for i in range(28)) + '</g>')
B('<g transform="translate(320,170)"><rect x="0" y="0" width="54" height="30" rx="5" fill="#8a6a4a"/><circle cx="14" cy="15" r="9" fill="#3a2a22"/><rect x="28" y="7" width="20" height="8" fill="#e8d8a8"/><path d="M 48,0 L 60,-26" stroke="#2a2a30" stroke-width="2"/></g>')
# counter, stove with steaming pots, sink, dish rack, rice cooker, sacks, crates of vegetables
B('<rect x="0" y="470" width="400" height="22" fill="#e8e2d8"/><rect x="0" y="492" width="400" height="148" fill="#7a6a5a"/>' + "".join(f'<rect x="{x}" y="502" width="88" height="128" fill="#8a7a68"/><rect x="{x + 76}" y="560" width="6" height="16" fill="#c8b07a"/>' for x in (10, 108, 206, 304)))
B('<rect x="20" y="452" width="120" height="18" fill="#2a2a30"/><g fill="#3a3a44"><ellipse cx="50" cy="452" rx="20" ry="4"/><ellipse cx="110" cy="452" rx="20" ry="4"/></g>'
  '<path d="M 28,452 L 72,452 L 70,414 L 30,414 Z" fill="#9a9aa4"/><ellipse cx="50" cy="414" rx="21" ry="5" fill="#b8b8c0"/><path d="M 90,452 L 130,452 L 128,424 L 92,424 Z" fill="#7a7a86"/><ellipse cx="110" cy="424" rx="19" ry="4" fill="#8a8a94"/>')
B('<g fill="#ece8f2" opacity=".35" filter="url(#soft)"><ellipse cx="50" cy="380" rx="16" ry="26"/><ellipse cx="60" cy="330" rx="12" ry="22"/><ellipse cx="112" cy="392" rx="12" ry="20"/></g>')
B('<rect x="170" y="456" width="80" height="16" fill="#c8c4cc"/><path d="M 210,456 L 210,430 L 226,430" stroke="#8a8a94" stroke-width="4" fill="none"/>'
  '<g transform="translate(270,430)"><rect x="0" y="0" width="60" height="40" fill="none" stroke="#8a8a94" stroke-width="2"/>' + "".join(f'<ellipse cx="{8 + i * 9}" cy="18" rx="3" ry="16" fill="#efe8f0" stroke="#c8c4cc" stroke-width=".6"/>' for i in range(6)) + '</g>'
  '<g transform="translate(350,436)"><rect x="0" y="0" width="34" height="34" rx="8" fill="#e8e2ea"/><rect x="0" y="0" width="12" height="34" rx="6" fill="#fff" opacity=".4"/><ellipse cx="17" cy="0" rx="16" ry="5" fill="#c8c4cc"/><rect x="12" y="16" width="10" height="6" fill="#6a8a6a"/></g>')
B('<g transform="translate(460,690)"><path d="M -40,0 C -46,-50 -30,-80 0,-82 C 30,-80 46,-50 40,0 Z" fill="#d8c8a8"/><path d="M -40,0 C -46,-50 -30,-80 -6,-82 C -18,-60 -22,-30 -20,0 Z" fill="#e8dcc0"/><text x="0" y="-36" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="10" font-weight="700" fill="#6a4a34">ข้าวหอม</text></g>')
B('<g transform="translate(470,760)"><rect x="-50" y="-40" width="100" height="40" fill="#5a7a5a"/>' + "".join(f'<rect x="{-48 + i * 12}" y="-40" width="3" height="40" fill="#3e5a3e"/>' for i in range(8)) + '<circle cx="-30" cy="-46" r="10" fill="#7a5aa0"/><circle cx="-12" cy="-48" r="9" fill="#e8d8b8"/><circle cx="8" cy="-46" r="10" fill="#7a5aa0"/><ellipse cx="28" cy="-46" rx="14" ry="6" fill="#5e8a4a"/></g>')
# door at the back right (Agnes)
B('<rect x="400" y="300" width="120" height="340" fill="#2a2024"/><rect x="408" y="308" width="104" height="332" fill="#141014"/>')
B(put("agnes_kettleR", 456, 640, .7, .72, .8, shadow=False))
# floor tiles
B('<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#6a5a50"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#5a4a40" stroke-width="2"/>' for y in (680, 730, 800, 880)) + "".join(f'<path d="M {x},640 L {x * 1.5 - 135:.0f},960" stroke="#5a4a40" stroke-width="2"/>' for x in range(0, 560, 54)))
# Daeng ladling soup, Mek at the table
B(put("daeng_ladle", 250, 900, 1.05, .95))
B(put("mek_sit", 96, 950, 1.0, .88))
B('<path d="M 30,740 L 430,740 L 450,780 L 10,780 Z" fill="#7a5a44"/><path d="M 30,740 L 230,740 L 222,780 L 10,780 Z" fill="#8a6a50"/><rect x="10" y="780" width="440" height="20" fill="#4a3428"/><rect x="24" y="800" width="10" height="160" fill="#3a281e"/><rect x="420" y="800" width="10" height="160" fill="#3a281e"/>')
B('<ellipse cx="140" cy="756" rx="34" ry="8" fill="#e8e0d4"/><ellipse cx="140" cy="753" rx="26" ry="5" fill="#d8c8a0"/><ellipse cx="290" cy="758" rx="44" ry="10" fill="#9a9aa4"/><ellipse cx="290" cy="754" rx="38" ry="7" fill="#d8c8a0"/>'
  '<rect x="350" y="742" width="12" height="16" rx="2" fill="#e8e2ea"/><rect x="368" y="744" width="12" height="14" rx="2" fill="#c8d8c0"/><path d="M 190,756 l 24,-4 M 194,760 l 24,-4" stroke="#c8c4cc" stroke-width="2"/>')
# single bulb and its light
B('<path d="M 270,0 L 270,120" stroke="#1a1418" stroke-width="2"/><path d="M 258,120 L 282,120 L 276,136 L 264,136 Z" fill="#2a2228"/><circle cx="270" cy="141" r="7" fill="#fff4e0"/>')
B(glow(270, 150, 330, "glowW", .85) + '<polygon points="262,140 278,140 460,960 80,960" fill="url(#beamW)" filter="url(#haze)" opacity=".45" style="mix-blend-mode:screen"/>' + motes(120, 180, 420, 700, 26, "#fff4e0"))
SCENES.append(("ฉาก 14 · ป้าแดงในครัว", "ครัวกลางเก่า กระเบื้องขาวแถบเขียว หม้อเดือด ปฏิทินแม่พระ วิทยุ ป้าแดงตักแกง อักเนสยืนที่ประตูถือกาด้วยมือซ้าย",
  frame("".join(b), "21 พ.ย. · 18:30", "ป้าได้ยินเพลงของป้า|เพลงที่ไม่มีใครในโลกนี้รู้จักอีกแล้ว", "I heard my song. A song no one else alive should know.", "ครัว")))

# =============== SCENE 16: bell tower at night ===============
torch = '<g transform="translate(-50,226) rotate(-60)"><rect x="-4" y="-22" width="8" height="24" rx="2" fill="#2a2a30"/><rect x="-5" y="-26" width="10" height="6" fill="#8a8a94"/><ellipse cx="0" cy="-27" rx="4" ry="1.6" fill="#fff6e6"/></g>'
posed("mek", "mek_torch", aL=-62, aR=10, extraL=torch, head=6)
b = []; B = b.append
B('<rect width="540" height="960" fill="url(#nightSky)"/>')
B("".join(f'<circle cx="{R.uniform(0, 540):.0f}" cy="{R.uniform(0, 300):.0f}" r=".8" fill="#e8ecff" opacity="{R.uniform(.2, .6):.2f}"/>' for _ in range(30)))
B('<circle cx="430" cy="110" r="28" fill="#e8ecff" opacity=".9"/><circle cx="430" cy="110" r="70" fill="url(#glowC)" opacity=".7"/>')
B('<g filter="url(#dof2)" opacity=".8">' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{560 - y}" fill="#141834"/>' for x, y, w in ((0, 330, 60), (470, 300, 70), (60, 380, 40))) + '</g>')
# the tower, low angle, white Gothic with dome
B(church(300, 690, 1.15, night=True))
B('<path d="M 300,270 L 320,300 L 300,330" stroke="#c8c4d8" stroke-width="1" fill="none" opacity=".5"/>')  # bell rope swaying out of the belfry
B(pigeon(240, 330, .9) + pigeon(380, 280, .8, -1) + pigeon(170, 250, .7))
B('<g fill="#7a7898" opacity=".85"><path d="M 120,200 l 10,-6 l 6,6 l 6,-6 l 10,6 l -10,-2 l -6,4 l -6,-4 Z"/><path d="M 400,240 l 8,-5 l 5,5 l 5,-5 l 8,5 l -8,-2 l -5,3 l -5,-3 Z"/></g>')
# ground: paving, overgrown grass, fallen leaves, iron bench, dead lamp post, scattered keys, Daeng
B('<path d="M 0,690 L 540,690 L 540,960 L 0,960 Z" fill="#2a2a36"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#1e1e28" stroke-width="2"/>' for y in (730, 780, 850, 930)) + "".join(f'<path d="M {x},690 L {x * 1.6 - 160:.0f},960" stroke="#1e1e28" stroke-width="1.6"/>' for x in range(0, 560, 60)))
B("".join(f'<path d="M {x},{y} l -2,-10 M {x + 3},{y} l 2,-12 M {x + 6},{y} l 0,-8" stroke="#3a4a3a" stroke-width="1.6"/>' for x, y in ((20, 694), (80, 692), (500, 694), (460, 692), (150, 693))))
B("".join(f'<ellipse cx="{R.uniform(0, 540):.0f}" cy="{R.uniform(700, 950):.0f}" rx="5" ry="2.4" fill="{R.choice(("#5a4a3a", "#6a5a42", "#4a3a2e"))}" transform="rotate({R.uniform(0, 180):.0f} 0 0)" opacity=".8"/>' for _ in range(26)))
B('<g transform="translate(470,760)"><rect x="-50" y="-36" width="100" height="6" fill="#1e1a22"/><rect x="-50" y="-22" width="100" height="6" fill="#1e1a22"/><path d="M -48,-16 L -50,20 M 48,-16 L 50,20 M -48,-40 L -48,-16 M 48,-40 L 48,-16" stroke="#1e1a22" stroke-width="4"/></g>')
B('<path d="M 40,690 L 40,500" stroke="#1e1a22" stroke-width="6"/><path d="M 28,500 L 52,500 L 48,480 L 32,480 Z" fill="#2a2630"/><path d="M 40,480 L 40,470" stroke="#1e1a22" stroke-width="3"/>')
# Mek with the torch, recoiling
B(put("mek_torch", 130, 900, 1.12, .78, .85))
# torch beam to the body
B('<polygon points="206,646 222,638 520,850 470,940" fill="url(#beamW)" filter="url(#haze)" style="mix-blend-mode:screen"/>')
B('<g transform="translate(380,862)"><ellipse cx="0" cy="22" rx="130" ry="15" fill="#0a090e" opacity=".6"/>'
  '<path d="M -110,0 C -100,-18 70,-22 100,-6 L 102,14 C 50,22 -70,22 -110,12 Z" fill="#6c2b30"/><path d="M -110,0 C -100,-18 -60,-20 -40,-18 L -46,16 C -70,18 -96,16 -110,12 Z" fill="#7a3438"/>'
  '<path d="M -40,-14 L 64,-16 L 68,14 L -38,16 Z" fill="#748894"/><path d="M 100,-6 L 140,-4 L 142,16 L 102,14 Z" fill="#4a3a4a"/>'
  '<ellipse cx="-124" cy="2" rx="18" ry="14" fill="#a9a4a6"/><circle cx="-128" cy="-6" r="5" fill="#b9b4b6"/><circle cx="-118" cy="-8" r="4.5" fill="#b9b4b6"/>'
  '<path d="M -20,14 L -60,36 L -54,42 L -12,20 Z" fill="#c98f69"/><ellipse cx="-62" cy="40" rx="8" ry="6" fill="#c98f69"/><rect x="-74" y="36" width="10" height="7" fill="#fbf8f2"/>'
  '<path d="M 142,2 l 12,2 l -2,8 l -10,0 Z" fill="#6a4a3a"/></g>')
B('<g transform="translate(232,904)"><circle r="9" fill="none" stroke="#b49a5a" stroke-width="2.4"/><path d="M 6,6 l 10,12 l 3,-2 M -6,6 l -8,14 l 3,1 M 0,9 l 0,14 l 3,0" stroke="#c9ad66" stroke-width="2.4" fill="none"/></g>')
B('<path d="M 300,690 C 304,720 296,740 302,760" stroke="#c8c4d8" stroke-width="1.6" fill="none" opacity=".7"/><path d="M 296,760 l 12,4" stroke="#c8c4d8" stroke-width="1.6" opacity=".7"/>')
B(motes(150, 690, 520, 930, 18, "#fff4e0") + glow(470, 900, 120, "glowW", .45))
SCENES.append(("ฉาก 16 · หอระฆัง", "หอระฆังขาวยอดโดมมุมต่ำ คืนพระจันทร์ เชือกระฆังขาดห้อย เมฆถือไฟฉายถอยหลัง ร่างป้าแดงและพวงกุญแจกระจาย",
  frame("".join(b), "22 พ.ย. · 03:01", "แล้วผมก็เห็นป้าแดง", "Then I saw Auntie Daeng.", "หอระฆัง")))

# ---------------- page ----------------
DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{cf.NUN_DEFS}{"".join(POSES)}
<filter id="dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="moteFar" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation=".6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="5" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="paint" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency=".012 .02" numOctaves="4" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .52  0 0 0 0 .62  0 0 0 1.4 -.25"/></filter>
<filter id="drop" x="-20%" y="-20%" width="150%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dx="8" dy="10"/><feComponentTransfer><feFuncA type="linear" slope=".4"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="subStroke" x="-10%" y="-30%" width="120%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="2.2" result="d"/><feFlood flood-color="#120e18"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset=".5" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".8"/></radialGradient>
<radialGradient id="glowW" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff1dc" stop-opacity=".6"/><stop offset=".4" stop-color="#f3cfb8" stop-opacity=".22"/><stop offset="1" stop-color="#d9a9a0" stop-opacity="0"/></radialGradient>
<radialGradient id="glowC" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#a9c4ff" stop-opacity=".55"/><stop offset=".5" stop-color="#6f86d8" stop-opacity=".18"/><stop offset="1" stop-color="#4a5aa8" stop-opacity="0"/></radialGradient>
<linearGradient id="beamW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0dc" stop-opacity=".4"/><stop offset="1" stop-color="#f3cfb8" stop-opacity="0"/></linearGradient>
<linearGradient id="nightSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0e1230"/><stop offset="1" stop-color="#2a2f5e"/></linearGradient>
<linearGradient id="duskSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4470"/><stop offset=".6" stop-color="#8a7a9e"/><stop offset="1" stop-color="#c8aab4"/></linearGradient>
<linearGradient id="skyDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#a8b8e0"/><stop offset="1" stop-color="#e8e0e8"/></linearGradient>
<linearGradient id="atticWash" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a1c1a" stop-opacity=".55"/><stop offset=".5" stop-color="#2a1c1a" stop-opacity="0"/><stop offset="1" stop-color="#2a1c1a" stop-opacity=".6"/></linearGradient>
<radialGradient id="kitchenWash" cx="50%" cy="15%" r="80%"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#1a1418" stop-opacity=".7"/></radialGradient>
</defs></svg>'''

cards = "\n".join(f'<figure><div class="fr">{svg}</div><figcaption><b>{t}</b><br>{d}</figcaption></figure>' for t, d, svg in SCENES)
html = f'''<title>EP1 ภาพฉากรอบ 2</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: 2-up grid of 9:16 frames (1 column on phones). Single dark look by choice, matching the other sheets. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#8f86ff;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); margin:0; }}
body {{ font-family:var(--font); padding:24px max(16px, env(safe-area-inset-right,0px)) 40px max(16px, env(safe-area-inset-left,0px)); }}
.wrap {{ max-width:1000px; margin:0 auto; display:grid; gap:16px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
.bar {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; font-size:13px; color:var(--muted); }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:6px; padding:6px 12px; cursor:pointer; }}
button:hover {{ border-color:var(--muted); }} button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
button[aria-pressed="true"] {{ border-color:var(--accent); color:#fff; }}
.grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:20px; }}
@media (max-width:620px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
.fr {{ aspect-ratio:9/16; box-shadow:0 0 0 1px var(--line); border-radius:6px; overflow:hidden; }}
.fr svg {{ display:block; width:100%; height:100%; }}
body.nosubs .subs {{ display:none; }}
figcaption {{ font-size:13px; color:var(--muted); line-height:1.6; }} figcaption b {{ color:var(--ink); font-weight:500; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@500&display=swap">
{DEFS}
<div class="wrap">
  <h1>แม่ชีคนที่สอง EP1 · ภาพฉากรอบ 2<span>4 ฉากตัวอย่าง · ของในฉากจัดเต็ม ตัวละครเต็มตัวมีท่าทาง</span></h1>
  <div class="bar"><span>ถ้าระดับนี้ผ่าน จะทำอีก 13 ฉากที่เหลือแบบเดียวกัน (โบสถ์รอแก้ตามภาพตัวอย่าง)</span><button id="t" type="button" aria-pressed="true">ซับ</button></div>
  <div class="grid">
{cards}
  </div>
</div>
<script>
const b = document.getElementById('t');
b.addEventListener('click', () => {{ const on = b.getAttribute('aria-pressed') !== 'true'; b.setAttribute('aria-pressed', String(on)); document.body.classList.toggle('nosubs', !on); }});
</script>'''
open(os.path.join(HERE, "scenes_v2.html"), "w").write(html)
print("wrote scenes_v2.html", len(html) // 1024, "KB")
