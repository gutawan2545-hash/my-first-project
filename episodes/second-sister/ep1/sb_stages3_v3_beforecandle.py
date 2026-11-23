# Round-3 stages for the EP1 storyboard (master revision). exec'd inside storyboard.py right after the
# lighting block, so it can use every helper from storyboard.py and sb_stages2.py, and L() for lights.
# Each stage replaces or adds one set; rooms stay built from one function so every camera angle matches.

# ------------------------------------------------------------------ shared pieces
def cumulus(x, y, w, h, seed=1, op=.95, lit="#ffffff", mid="#f0ecf8", shade="#cfc6e4"):
    """Daytime cumulus: flat lavender-grey base, lit puffy tops, soft shade on the lower right of each puff."""
    r = _rr.Random(seed * 31 + int(x))
    n = r.randint(4, 6)
    o = f'<g opacity="{op}">'
    o += f'<rect x="{x}" y="{y - h * .25:.0f}" width="{w}" height="{h * .42:.0f}" rx="{h * .2:.0f}" fill="{shade}"/>'
    bumps = []
    for i in range(n):
        bx = x + w * (i + .5) / n + r.uniform(-w * .04, w * .04)
        br = h * r.uniform(.42, .78) * (1.15 if 0 < i < n - 1 else .85)
        bumps.append((bx, y - br * .55, br))
    for bx, by, br in bumps:
        o += f'<circle cx="{bx + br * .12:.0f}" cy="{by + br * .14:.0f}" r="{br:.0f}" fill="{shade}"/>'
    for bx, by, br in bumps:
        o += f'<circle cx="{bx:.0f}" cy="{by:.0f}" r="{br * .93:.0f}" fill="{mid}"/><circle cx="{bx - br * .18:.0f}" cy="{by - br * .2:.0f}" r="{br * .62:.0f}" fill="{lit}"/>'
    o += f'<rect x="{x + h * .2:.0f}" y="{y - h * .05:.0f}" width="{w - h * .4:.0f}" height="{h * .2:.0f}" rx="{h * .1:.0f}" fill="{shade}" opacity=".9"/>'
    return o + '</g>'

def day_sky(top="#7fa2e8", mid="#b9c4f0", low="#efe6f6", gid="dsky3"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".62" stop-color="{mid}"/><stop offset="1" stop-color="{low}"/></linearGradient>'
            f'<rect width="540" height="960" fill="url(#{gid})"/>')

def round_tree(x, base, h=300, w=220, c=("#5f8a5a", "#4e7650", "#3e6044"), trunk="#5a4a48", seed=5):
    """Rain tree: short forked trunk, wide layered canopy lit from the upper left."""
    r = _rr.Random(seed)
    o = f'<path d="M {x - 10},{base} C {x - 8},{base - h * .3} {x - 14},{base - h * .45} {x - 30},{base - h * .6} L {x - 22},{base - h * .62} C {x - 4},{base - h * .5} {x + 2},{base - h * .45} {x + 6},{base - h * .55} C {x + 16},{base - h * .5} {x + 30},{base - h * .58} {x + 40},{base - h * .64} L {x + 44},{base - h * .6} C {x + 26},{base - h * .5} {x + 14},{base - h * .4} {x + 12},{base} Z" fill="{trunk}"/>'
    o += f'<path d="M {x - 10},{base} C {x - 8},{base - h * .3} {x - 14},{base - h * .45} {x - 30},{base - h * .6} L {x - 24},{base - h * .62} C {x - 6},{base - h * .45} {x - 2},{base - h * .3} {x - 2},{base} Z" fill="#7a6a66"/>'
    cy = base - h * .72
    for k, (dx, dy, rr, col) in enumerate(((-w * .32, 10, w * .3, c[2]), (w * .3, 14, w * .3, c[2]), (0, -h * .12, w * .34, c[1]), (-w * .22, -6, w * .28, c[1]),
                                           (w * .2, -2, w * .3, c[1]), (-w * .12, -h * .16, w * .24, c[0]), (w * .12, -h * .1, w * .22, c[0]))):
        o += f'<ellipse cx="{x + dx:.0f}" cy="{cy + dy:.0f}" rx="{rr:.0f}" ry="{rr * .62:.0f}" fill="{col}"/>'
    o += "".join(f'<ellipse cx="{x + r.uniform(-w * .4, w * .4):.0f}" cy="{cy + r.uniform(-h * .15, h * .08):.0f}" rx="{r.uniform(8, 18):.0f}" ry="{r.uniform(5, 10):.0f}" fill="{c[0]}" opacity=".8"/>' for _ in range(6))
    o += f'<ellipse cx="{x + w * .08:.0f}" cy="{cy + h * .12:.0f}" rx="{w * .42:.0f}" ry="{h * .05:.0f}" fill="#24382c" opacity=".35"/>'   # dark underside
    return o

def soft_shadow(x, y, rx, ry, op=.3):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#2a2036" opacity="{op}" filter="url(#lsoft)"/>'

def frame_pic(x, y, w, h, inner, wood="#6a4a32", mat="#efe6d4"):
    return (f'<rect x="{x + 3}" y="{y + 4}" width="{w}" height="{h}" fill="#0a080c" opacity=".35"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{wood}"/>'
            f'<rect x="{x + 4}" y="{y + 4}" width="{w - 8}" height="{h - 8}" fill="{mat}"/><svg x="{x + 7}" y="{y + 7}" width="{w - 14}" height="{h - 14}" viewBox="0 0 100 100" preserveAspectRatio="none">{inner}</svg>'
            f'<path d="M {x},{y} L {x + w},{y}" stroke="#a88a5a" stroke-width="1.4" opacity=".7"/>')
PIC_PORTRAIT = '<rect width="100" height="100" fill="#4a3a3a"/><ellipse cx="50" cy="44" rx="18" ry="22" fill="#c8a88a"/><path d="M 22,100 C 24,70 40,64 50,64 C 60,64 76,70 78,100 Z" fill="#1a1418"/><path d="M 44,64 L 56,64 L 50,74 Z" fill="#efe8da"/><path d="M 32,40 C 32,18 68,18 68,40 C 62,28 38,28 32,40 Z" fill="#3a2a2a"/>'
PIC_SAINT = '<rect width="100" height="100" fill="#3a3456"/><circle cx="50" cy="36" r="24" fill="#d8b860" opacity=".6"/><ellipse cx="50" cy="40" rx="12" ry="15" fill="#e8c8a8"/><path d="M 24,100 C 26,62 38,54 50,54 C 62,54 74,62 76,100 Z" fill="#7a2a32"/><path d="M 30,100 C 34,74 42,66 50,66 L 50,100 Z" fill="#2a3a6a"/><path d="M 46,70 C 46,64 54,64 54,70 C 54,76 50,78 50,80 C 50,78 46,76 46,70 Z" fill="#e85a5a"/>'
PIC_LAND = '<rect width="100" height="100" fill="#9ab0c8"/><path d="M 0,60 C 20,46 40,56 60,44 C 76,36 90,44 100,40 L 100,100 L 0,100 Z" fill="#5a7a5a"/><path d="M 0,76 C 30,66 60,80 100,70 L 100,100 L 0,100 Z" fill="#46644a"/><rect x="62" y="36" width="10" height="14" fill="#efe8da"/><path d="M 60,36 L 67,28 L 74,36 Z" fill="#8a4a3a"/>'
PIC_GROUP = '<rect width="100" height="100" fill="#d8ccb4"/>' + "".join(f'<circle cx="{14 + i * 14}" cy="{40 + (i % 2) * 22}" r="5" fill="#5a4a3a"/><rect x="{9 + i * 14}" y="{45 + (i % 2) * 22}" width="10" height="14" fill="#efe8da"/>' for i in range(6)) + '<rect width="100" height="100" fill="#8a6a3a" opacity=".2"/>'

# ------------------------------------------------------------------ 1. CONVENT FRONT (gate): clouds, trees, kerb, paving
def gate_bg3():
    o = day_sky(gid="gsky3")
    o += cumulus(-50, 190, 270, 74, 1) + cumulus(250, 130, 250, 62, 2, .92) + cumulus(140, 320, 170, 40, 3, .75) + cumulus(390, 300, 190, 48, 4, .8) + cumulus(-20, 360, 130, 30, 5, .6)
    o += "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{480 - y}" fill="#9a90b8" opacity=".45"/>' for x, y, w in ((0, 300, 46), (40, 340, 30), (480, 280, 60)))   # far city, hazy
    o += f'<g opacity=".97">{church(310, 410, .62)}</g>' + haze(410, 80, "#e2d4ea", .28)
    o += round_tree(500, 560, 280, 210, seed=8) + round_tree(150, 540, 200, 150, ("#6a9460", "#58804f", "#466a44"), seed=9)
    # lawn strip behind the fence, clipped hedge along its foot
    o += '<path d="M 0,520 L 540,520 L 540,566 L 0,566 Z" fill="#7aa06a"/><path d="M 0,520 L 540,520 L 540,530 L 0,530 Z" fill="#8fb47a"/>'
    o += "".join(f'<ellipse cx="{x}" cy="560" rx="34" ry="18" fill="#4e7a4a"/><ellipse cx="{x - 8}" cy="553" rx="20" ry="10" fill="#6a9a5e"/>' for x in range(0, 560, 52))
    # paved forecourt in perspective, a stone kerb and a strip of road in the foreground
    o += '<path d="M 0,560 L 540,560 L 540,900 L 0,900 Z" fill="#a49cae"/>'
    o += "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#8a8296" stroke-width="1.3"/>' for y in (588, 622, 668, 728, 806))
    o += "".join(f'<path d="M {270 + (x - 270) * .25:.0f},560 L {x},900" stroke="#8a8296" stroke-width="1.1"/>' for x in range(-400, 940, 80))
    o += '<path d="M 0,900 L 540,900 L 540,914 L 0,914 Z" fill="#d8d2dc"/><path d="M 0,914 L 540,914 L 540,926 L 0,926 Z" fill="#8a8494"/>'   # kerb
    o += '<path d="M 0,926 L 540,926 L 540,960 L 0,960 Z" fill="#5a5666"/><path d="M 20,944 L 90,944 M 160,944 L 230,944 M 300,944 L 370,944 M 440,944 L 510,944" stroke="#e8e2ea" stroke-width="3"/>'   # road
    o += soft_shadow(470, 600, 140, 16, .35) + soft_shadow(160, 576, 90, 10, .3)   # tree shadows on the court
    o += fence(470, 640) + '<rect x="250" y="560" width="30" height="40" rx="4" fill="#2a2420"/><path d="M 256,560 C 256,546 274,546 274,560" fill="none" stroke="#2a2420" stroke-width="4"/>'
    o += '<g transform="translate(440,500)"><rect x="-3" y="0" width="4" height="60" fill="#16121a"/><rect x="-56" y="-30" width="112" height="34" rx="3" fill="#efe8da"/><rect x="-56" y="-30" width="112" height="7" fill="#8e1b24"/><text x="0" y="-10" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" font-weight="700" fill="#3a2a22">เขตพักซิสเตอร์</text><text x="0" y="0" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7" fill="#5a4a3a">ห้ามบุคคลภายนอก</text></g>'
    # lamp posts and big potted plants frame the court
    for x in (28, 512):
        o += f'<rect x="{x - 3}" y="620" width="6" height="220" fill="#2a2630"/><rect x="{x - 9}" y="834" width="18" height="8" fill="#2a2630"/><path d="M {x - 12},620 L {x + 12},620 L {x + 8},596 L {x - 8},596 Z" fill="#efe8f0"/><path d="M {x - 14},596 L {x + 14},596 L {x},584 Z" fill="#2a2630"/>'
    for x in (96, 444):
        o += f'<path d="M {x - 22},880 L {x + 22},880 L {x + 16},840 L {x - 16},840 Z" fill="#b88a6a"/><path d="M {x - 22},846 L {x + 22},846" stroke="#8a6a4e" stroke-width="3"/>' + clump(x, 820, 30, "#6a9a5e", "#4e7a4a", "#3e6040")
    o += frangipani(40, 470, 1.0) + "".join(flower5(RR.uniform(10, 520), RR.uniform(700, 880), 1.2) for _ in range(6))
    return o
ST["gate"] = gate_bg3() + C("daeng_hug", 120, 900, .92) + C("mek", 255, 910, .96) + C("cat_point", 420, 905, .94) + '<polygon points="120,900 240,900 300,940 150,946" fill="#2a2032" opacity=".25" filter="url(#lsoft)"/>'
L("gate", .12, holes=((120, 180, 300),), glows=((80, 160, 320, WARM, .4),),
  shadows=(("140,920 200,920 420,980 300,980", .4), ("360,900 420,900 560,960 480,970", .4)))

# ------------------------------------------------------------------ 2. PRIMARY SCHOOL (new, shot 87): afternoon, nearly empty
def school_bg():
    o = day_sky("#86a6e6", "#c2c8ee", "#f2e4ee", "ssky3")
    o += cumulus(-30, 150, 230, 60, 11) + cumulus(300, 110, 220, 54, 12, .9) + cumulus(170, 250, 150, 34, 13, .7)
    o += "".join(clump(x, 420, r, "#5e8a5a", "#4c7650", "#3c6044") for x, r in ((10, 70), (90, 56), (470, 70), (540, 60)))
    # two-storey white school: arcade on both floors, central gable with a cross and the name
    W, Li, D, S = "#e8e4ee", "#f6f2f8", "#bdb6cc", "#9a92ae"
    o += f'<path d="M 20,330 L 520,330 L 540,346 L 0,346 Z" fill="#6a6280"/>'   # roof eave
    o += f'<path d="M 30,250 L 510,250 L 530,330 L 10,330 Z" fill="#7a7290"/><path d="M 30,250 L 510,250 L 506,262 L 34,262 Z" fill="#8e86a4"/>'   # hipped roof
    o += f'<path d="M 200,330 L 270,214 L 340,330 Z" fill="{W}"/><path d="M 270,214 L 340,330 L 316,330 L 270,246 Z" fill="{D}"/><path d="M 190,334 L 270,204 L 350,334" fill="none" stroke="{Li}" stroke-width="6"/>'
    o += f'<rect x="266" y="176" width="8" height="34" fill="{Li}"/><rect x="256" y="186" width="28" height="7" fill="{Li}"/><circle cx="270" cy="280" r="18" fill="{D}"/><circle cx="270" cy="280" r="13" fill="#4a4a6a"/>'
    o += f'<rect x="30" y="346" width="480" height="270" fill="{W}"/><rect x="30" y="346" width="12" height="270" fill="{Li}"/><rect x="498" y="346" width="12" height="270" fill="{D}"/>'
    o += f'<rect x="30" y="470" width="480" height="12" fill="{Li}"/><rect x="30" y="482" width="480" height="4" fill="{S}"/>'   # floor band
    for floor_y, h in ((356, 104), (492, 116)):
        for i in range(8):
            x = 42 + i * 58
            o += f'<path d="M {x + 6},{floor_y + h} L {x + 6},{floor_y + 30} Q {x + 26},{floor_y + 4} {x + 46},{floor_y + 30} L {x + 46},{floor_y + h} Z" fill="#4a4660"/>'
            o += f'<path d="M {x + 6},{floor_y + 30} Q {x + 26},{floor_y + 4} {x + 46},{floor_y + 30}" fill="none" stroke="{Li}" stroke-width="3"/>'
            o += f'<path d="M {x + 30},{floor_y + h} L {x + 30},{floor_y + 34} L {x + 46},{floor_y + 40} L {x + 46},{floor_y + h} Z" fill="#5c5874"/>'   # depth inside the arch
            o += f'<rect x="{x - 2}" y="{floor_y + 8}" width="8" height="{h - 8}" fill="{Li}"/><rect x="{x + 4}" y="{floor_y + 8}" width="2" height="{h - 8}" fill="{D}"/>'
    o += f'<rect x="30" y="446" width="480" height="8" fill="{Li}"/>' + "".join(f'<rect x="{x}" y="454" width="4" height="16" fill="{D}"/>' for x in range(36, 508, 9))   # balcony balustrade
    o += f'<rect x="212" y="300" width="116" height="20" rx="3" fill="#2a3a6a"/><text x="270" y="314" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" font-weight="700" fill="#f2e6c8">โรงเรียนเซนต์เวโรนิกา</text>'
    o += f'<path d="M 30,616 L 510,616 L 520,626 L 20,626 Z" fill="{S}"/>'   # plinth
    # empty classrooms glimpsed through the upper arches: a desk row, a blackboard
    o += '<rect x="108" y="400" width="34" height="22" fill="#2e4a3e"/><rect x="340" y="400" width="34" height="22" fill="#2e4a3e"/>' + "".join(f'<rect x="{x}" y="430" width="16" height="6" fill="#8a6a4a"/>' for x in (58, 176, 290, 410))
    # flagpole with the national flag, lowered for the evening? no: still up, barely moving
    o += '<rect x="68" y="230" width="4" height="400" fill="#d8d4dc"/><circle cx="70" cy="228" r="4" fill="#e8c86a"/>'
    o += '<g transform="translate(72,240)">' + "".join(f'<rect x="0" y="{y}" width="46" height="{h}" fill="{c}"/>' for y, h, c in ((0, 5, "#c8323c"), (5, 5, "#f4f0f2"), (10, 10, "#2a3a7a"), (20, 5, "#f4f0f2"), (25, 5, "#c8323c"))) + '</g>'
    # field: sandy court, painted lines, a goal; long afternoon shadows fall to the lower right
    o += '<path d="M 0,626 L 540,626 L 540,960 L 0,960 Z" fill="#8aaa72"/><path d="M 0,626 L 540,626 L 540,640 L 0,640 Z" fill="#9aba80"/>'
    o += '<path d="M 140,660 L 520,660 L 560,860 L 120,860 Z" fill="#c8b48e"/><path d="M 150,668 L 512,668 L 548,852 L 130,852 Z" fill="none" stroke="#efe8da" stroke-width="2.4"/><path d="M 331,668 L 339,852" stroke="#efe8da" stroke-width="2.4"/><ellipse cx="335" cy="760" rx="44" ry="18" fill="none" stroke="#efe8da" stroke-width="2.4"/>'
    o += '<g transform="translate(470,700)"><path d="M 0,0 L 0,-60 L 50,-60 L 50,0" fill="none" stroke="#f2eef4" stroke-width="5"/><path d="M 0,-60 L 12,-48 L 62,-48 L 50,-60 M 62,-48 L 62,10" fill="none" stroke="#c8c4d0" stroke-width="2"/>' + "".join(f'<path d="M {x},-56 L {x + 8},-46 L {x + 8},6" stroke="#d8d4e0" stroke-width=".8" opacity=".7"/>' for x in range(4, 50, 8)) + '</g>'
    o += '<polygon points="70,630 76,630 220,700 200,704" fill="#3a3a4a" opacity=".25"/>'   # flagpole shadow
    # playground swing (empty, one seat still swaying), a bench with a forgotten school bag, the school bell on its post
    o += '<g transform="translate(70,860)"><path d="M -40,0 L -20,-130 L 0,0 M 80,0 L 100,-130 L 120,0" fill="none" stroke="#5a5a7a" stroke-width="6"/><rect x="-24" y="-134" width="128" height="8" fill="#6a6a8a"/>'
    o += '<g id="swingSeat"><path d="M 10,-126 L 10,-44 M 40,-126 L 40,-44" stroke="#3a3a4a" stroke-width="2"/><rect x="4" y="-46" width="42" height="7" rx="2" fill="#b84a3a"/></g>'
    o += '<path d="M 60,-126 L 60,-40 M 90,-126 L 90,-40" stroke="#3a3a4a" stroke-width="2"/><rect x="54" y="-42" width="42" height="7" rx="2" fill="#3a6aa8"/></g>'
    o += soft_shadow(120, 864, 90, 8, .35)
    o += '<g transform="translate(330,900)"><rect x="-60" y="-26" width="120" height="8" fill="#8a6a4a"/><rect x="-60" y="-44" width="120" height="6" fill="#9a7a5a"/><rect x="-54" y="-18" width="6" height="22" fill="#4a3a2a"/><rect x="48" y="-18" width="6" height="22" fill="#4a3a2a"/>'
    o += '<path d="M -30,-26 L -6,-26 L -8,-48 C -8,-54 -28,-54 -28,-48 Z" fill="#2a4a8a"/><rect x="-24" y="-42" width="12" height="8" rx="2" fill="#3a5aa0"/><path d="M -26,-48 C -24,-58 -12,-58 -10,-48" stroke="#1a2a5a" stroke-width="2" fill="none"/></g>'
    o += soft_shadow(350, 906, 80, 6, .35)
    o += '<g transform="translate(200,640)"><rect x="-3" y="-90" width="6" height="90" fill="#4a3a3a"/><rect x="-14" y="-96" width="28" height="6" fill="#4a3a3a"/><path d="M -10,-90 C -10,-104 10,-104 10,-90 L 12,-78 L -12,-78 Z" fill="#c8a858"/><circle cx="0" cy="-76" r="2.4" fill="#8a6a2a"/></g>'
    # two kids far away walking out of the gate, the last ones (small, backlit)
    for x, h, top in ((452, 34, "#f2f2f4"), (470, 30, "#f2f2f4")):
        o += f'<g transform="translate({x},640)"><circle cx="0" cy="{-h}" r="4" fill="#2a1e1a"/><rect x="-4" y="{-h + 4}" width="8" height="{h * .4:.0f}" fill="{top}"/><rect x="-4" y="{-h * .6 + 4:.0f}" width="8" height="{h * .3:.0f}" fill="#2a3a6a"/><path d="M -3,{-h * .3 + 4:.0f} L -3,0 M 3,{-h * .3 + 4:.0f} L 3,0" stroke="#e8c8a8" stroke-width="2"/></g>'
    o += "".join(tuft(RR.uniform(0, 540), RR.uniform(880, 950), 1.4, "#5a7a4a") for _ in range(10))
    return o
ST["school"] = school_bg()
L("school", .1, holes=((150, 300, 300),), glows=((40, 200, 340, WARM, .45),), motes=(40, 300, 500, 760, 10, "#fff4e0"),
  shadows=(("330,904 390,904 520,960 400,960", .3),))

# ------------------------------------------------------------------ 3. GROTTO OF OUR LADY (new, shots 88-89): stone grotto by the canal, dusk
def grotto_bg():
    o = day_sky("#4a5a9a", "#9a92c8", "#e6c8d8", "gsky4")
    o += cumulus(-40, 140, 200, 46, 21, .7, "#f2e2ee", "#d8c8e2", "#a89ac4") + cumulus(330, 110, 220, 40, 22, .65, "#f2e2ee", "#d8c8e2", "#a89ac4")
    o += "".join(clump(x, y, r, "#3e5a4a", "#30483c", "#243a30") for x, y, r in ((-10, 260, 130), (560, 240, 140), (120, 160, 90), (440, 150, 100)))   # overhanging trees
    # the grotto: a big arch of stacked stones with a deep recess and a niche up high
    r = _rr.Random(44)
    o += '<path d="M 40,700 C 30,520 70,300 270,250 C 470,300 510,520 500,700 Z" fill="#6a6478"/>'
    for _ in range(90):   # stones: lighter on the upper left, darker to the right
        x = r.uniform(50, 490); y = r.uniform(270, 690)
        if (x - 270) ** 2 / 230 ** 2 + (y - 520) ** 2 / 270 ** 2 > 1: continue
        w = r.uniform(26, 54); h = r.uniform(18, 34)
        col = r.choice(("#8a84a0", "#7a7490", "#9a94ae", "#6e6884")) if x < 300 else r.choice(("#6e6884", "#5e5874", "#726c88"))
        o += f'<path d="M {x:.0f},{y:.0f} l {w * .5:.0f},{-h * .3:.0f} l {w * .5:.0f},{h * .2:.0f} l {-w * .1:.0f},{h * .8:.0f} l {-w * .8:.0f},{h * .1:.0f} Z" fill="{col}"/>'
        o += f'<path d="M {x:.0f},{y:.0f} l {w * .5:.0f},{-h * .3:.0f} l {w * .5:.0f},{h * .2:.0f}" stroke="#b4aec6" stroke-width="1.2" fill="none" opacity=".55"/>'
    o += '<path d="M 130,700 C 120,560 170,420 270,390 C 370,420 420,560 410,700 Z" fill="#2a2436"/><path d="M 300,400 C 380,440 420,560 410,700 L 360,700 C 370,580 350,470 300,400 Z" fill="#1e1a28"/>'   # deep recess
    # (no ivy or creeping leaves on the rock: user)
    # the statue niche with Our Lady: white veil and robe, blue sash, hands joined, gold halo
    o += '<path d="M 220,500 L 220,380 Q 270,330 320,380 L 320,500 Z" fill="#3a3448"/><path d="M 210,500 L 330,500 L 336,512 L 204,512 Z" fill="#a8a2b8"/>'
    o += '<g transform="translate(270,500)">'
    o += '<circle cx="0" cy="-118" r="20" fill="none" stroke="#e8cc7a" stroke-width="2.4"/>' + "".join(f'<circle cx="{20 * _m.cos(a):.1f}" cy="{-118 + 20 * _m.sin(a):.1f}" r="1.6" fill="#f2dc8a"/>' for a in [i * _m.pi / 6 for i in range(12)])
    o += '<path d="M -26,0 C -28,-40 -24,-80 -16,-100 C -10,-112 10,-112 16,-100 C 24,-80 28,-40 26,0 Z" fill="#f4f2f8"/><path d="M 4,-108 C 18,-100 26,-70 26,0 L 10,0 C 14,-50 12,-84 4,-108 Z" fill="#cfcadc"/>'
    o += '<ellipse cx="0" cy="-104" rx="9" ry="11" fill="#f2e6e0"/><path d="M -12,-106 C -12,-124 12,-124 12,-106 L 16,-60 L -16,-60 Z" fill="#f8f6fa"/><path d="M 4,-120 C 12,-114 16,-90 16,-60 L 8,-60 C 10,-86 8,-108 4,-120 Z" fill="#d8d4e4"/>'
    o += '<ellipse cx="0" cy="-104" rx="7.4" ry="9.4" fill="#f4eae4"/><path d="M -4,-106 l 2.6,.4 M 4,-106 l -2.6,.4" stroke="#8a7a7a" stroke-width=".9"/><path d="M -2,-99 Q 0,-98 2,-99" stroke="#b88a8a" stroke-width=".8" fill="none"/>'
    o += '<path d="M -18,-56 L 18,-56 L 14,-52 L -14,-52 Z" fill="#4a7ac8"/><path d="M -4,-52 C -6,-30 -2,-12 -6,0 L 2,0 C 0,-14 4,-32 4,-52 Z" fill="#4a7ac8"/>'
    o += '<path d="M -6,-80 L 6,-80 L 4,-66 L -4,-66 Z" fill="#efe4dc"/><path d="M -8,-2 C -4,4 4,4 8,-2" fill="#f2e6e0"/>'
    o += '<path d="M -12,4 C -4,0 4,0 12,4" stroke="#d8c870" stroke-width="2" fill="none"/></g>'
    o += '<g transform="translate(270,530)"><path d="M -60,0 C -30,-14 30,-14 60,0 C 40,6 -40,6 -60,0 Z" fill="#c8c2d6"/>' + "".join(f'<circle cx="{x}" cy="-6" r="5" fill="{c}"/>' for x, c in ((-40, "#f2f0f4"), (-28, "#e88a9a"), (28, "#f2f0f4"), (40, "#e8d070"))) + '</g>'   # flowers at her feet
    # candle rack and a mound of melted wax, flames lit
    o += '<path d="M 150,650 C 150,610 200,596 270,596 C 340,596 390,610 390,650 Z" fill="#efe6d8"/><path d="M 300,598 C 350,600 390,612 390,650 L 340,650 C 340,624 326,606 300,598 Z" fill="#d8ccba"/>'
    o += "".join(f'<path d="M {x},{y} c -4,10 4,14 0,24" stroke="#f6eee2" stroke-width="5" fill="none"/>' for x, y in ((170, 618), (226, 600), (318, 602), (372, 620)))   # wax drips
    for i, x in enumerate(range(170, 380, 18)):
        y = 600 + abs(x - 270) * .12 - (i % 3) * 6
        o += f'<rect x="{x - 3}" y="{y - 22:.0f}" width="6" height="22" fill="#f6f0e6"/><path d="M {x},{y - 34:.0f} C {x - 3.5},{y - 29:.0f} {x - 3.5},{y - 26:.0f} {x},{y - 24:.0f} C {x + 3.5},{y - 26:.0f} {x + 3.5},{y - 29:.0f} {x},{y - 34:.0f} Z" fill="#fff4ec"/>'
        o += f'<circle class="cflame" cx="{x}" cy="{y - 29:.0f}" r="16" fill="url(#lg_ffe6c4)" opacity=".7" style="mix-blend-mode:screen"/>'
    o += '<rect x="140" y="650" width="260" height="12" fill="#5a4a4a"/><rect x="150" y="662" width="8" height="40" fill="#3a2e2e"/><rect x="382" y="662" width="8" height="40" fill="#3a2e2e"/>'
    o += '<path d="M 100,760 L 200,760 L 196,774 L 104,774 Z" fill="#5a4234"/><rect x="104" y="774" width="6" height="26" fill="#3a2a22"/><rect x="190" y="774" width="6" height="26" fill="#3a2a22"/>'   # kneeler
    # stone steps down to the canal, black water with the flames reflected
    o += '<path d="M 0,700 L 540,700 L 540,800 L 0,800 Z" fill="#8a849a"/><path d="M 0,700 L 540,700 L 540,708 L 0,708 Z" fill="#b0aac2"/>'
    for k, y in enumerate((800, 830, 858)):
        o += f'<path d="M {-10 + k * 6},{y} L {550 - k * 6},{y} L {550 - k * 6},{y + 30} L {-10 + k * 6},{y + 30} Z" fill="{("#7a7490", "#6a6480", "#5a5470")[k]}"/><path d="M {-10 + k * 6},{y} L {550 - k * 6},{y}" stroke="#a8a2bc" stroke-width="2"/>'
    o += '<path d="M 0,884 L 540,884 L 540,960 L 0,960 Z" fill="#1e2232"/>' + "".join(f'<path d="M {x},{y} l {w},0" stroke="#4a5070" stroke-width="2" opacity=".7"/>' for x, y, w in ((40, 900, 60), (180, 912, 90), (330, 904, 70), (420, 930, 80), (90, 940, 70)))
    o += "".join(f'<path d="M {x},{892 + k * 9} l 8,0" stroke="#f4dcc8" stroke-width="2" opacity="{.6 - k * .12:.2f}"/>' for x in range(178, 372, 36) for k in range(4))
    o += '<rect x="0" y="790" width="540" height="8" fill="#c8c2d6"/>' + "".join(f'<rect x="{x}" y="740" width="6" height="52" fill="#b4aec6"/>' for x in range(10, 540, 46)) + '<rect x="0" y="736" width="540" height="6" fill="#d8d2e4"/>'   # railing
    return o
ST["grotto"] = grotto_bg()
L("grotto", .35, holes=((270, 430, 150), (270, 610, 140)), beams=(("200,0 330,0 330,520 210,520", "#f4e6f2", .32),),
  glows=((270, 410, 120, "#f4e6f2", .55), (270, 600, 150, CANDLE, .8)), motes=(200, 160, 340, 520, 18, "#fff4ec"))

# ------------------------------------------------------------------ 4. MUSIC ROOM: grand piano, Mek in the room, Agnes's doorway
def grand_piano():
    """Grand piano seen from its tail: closed lid, music desk at the far end, curved body, three carved legs, brass casters."""
    o = '<g>'
    top = "M 60,640 L 300,640 L 292,770 C 270,800 220,812 180,804 C 120,790 92,760 84,712 C 80,690 70,668 60,640 Z"
    o += f'<path d="{top}" fill="#120e14"/>'
    o += '<path d="M 84,712 C 92,760 120,790 180,804 C 220,812 270,800 292,770 L 292,806 C 270,836 220,848 180,840 C 120,826 92,796 84,748 Z" fill="#1e1820"/>'   # rim facing us
    o += '<path d="M 84,712 C 92,760 120,790 180,804 L 180,840 C 120,826 92,796 84,748 Z" fill="#2a2230"/>'
    o += '<path d="M 86,744 C 96,790 126,818 180,832 C 222,842 268,832 290,802" stroke="#c8a860" stroke-width="1.2" fill="none" opacity=".7"/>'   # thin gilt line on the rim
    # lacquer reflections on the lid: window light and the candles
    o += '<path d="M 96,660 C 130,656 200,654 262,660 L 250,676 C 196,670 140,672 104,678 Z" fill="#6a6280" opacity=".55"/>'
    o += '<path d="M 110,720 C 150,740 210,752 268,742" stroke="#8a84a4" stroke-width="5" fill="none" opacity=".35"/><path d="M 120,700 C 160,712 200,716 240,712" stroke="#e8e2f4" stroke-width="1.6" fill="none" opacity=".5"/>'
    o += '<ellipse cx="236" cy="700" rx="12" ry="4" fill="#ffe8d8" opacity=".55"/><ellipse cx="236" cy="700" rx="30" ry="9" fill="url(#lg_ffe6c4)" opacity=".5"/>'
    # music desk with open sheet music, fretwork
    o += '<path d="M 100,622 L 258,622 L 266,640 L 92,640 Z" fill="#1a1418"/><path d="M 108,624 L 250,624 L 256,638 L 102,638 Z" fill="#2c2228"/>'
    o += '<path d="M 116,625 L 176,624 L 177,637 L 114,638 Z" fill="#f2ece0"/><path d="M 180,624 L 240,625 L 242,638 L 178,637 Z" fill="#e8e0d2"/>' + "".join(f'<path d="M 120,{628 + k * 3} l 52,-.4 M 184,{627.6 + k * 3} l 52,.4" stroke="#6a6060" stroke-width=".6"/>' for k in range(3))
    # candelabra standing on the lid
    o += '<g transform="translate(236,690)"><path d="M -8,0 L 8,0 L 4,-6 L -4,-6 Z" fill="#c8a860"/><rect x="-1.6" y="-34" width="3.2" height="28" fill="#c8a860"/><path d="M -16,-30 C -16,-40 16,-40 16,-30" stroke="#c8a860" stroke-width="2.4" fill="none"/>'
    o += "".join(f'<rect x="{x - 2.5}" y="-52" width="5" height="18" fill="#f2ece2"/><path d="M {x},-62 C {x - 3},-57 {x - 3},-55 {x},-53 C {x + 3},-55 {x + 3},-57 {x},-62 Z" fill="#fff4ec"/>' for x in (-16, 0, 16)) + '</g>'
    # legs: tapered, with a carved collar and brass caster
    for x, y0, y1 in ((110, 790, 900), (270, 800, 914), (196, 836, 934)):
        o += f'<path d="M {x - 11},{y0} L {x + 11},{y0} L {x + 7},{y1} L {x - 7},{y1} Z" fill="#1a141c"/><path d="M {x - 11},{y0} L {x - 4},{y0} L {x - 3},{y1} L {x - 7},{y1} Z" fill="#3a3040"/>'
        o += f'<rect x="{x - 13}" y="{y0 + 8}" width="26" height="8" rx="3" fill="#2a2230"/><path d="M {x - 13},{y0 + 10} L {x + 13},{y0 + 10}" stroke="#c8a860" stroke-width="1" opacity=".7"/>'
        o += f'<rect x="{x - 8}" y="{y1}" width="16" height="6" rx="2" fill="#c8a860"/><circle cx="{x}" cy="{y1 + 9}" r="4" fill="#8a7040"/>'
    o += soft_shadow(190, 930, 160, 14, .45)
    return o + '</g>'

def music_room3():
    o = '<rect width="540" height="960" fill="#6a5c70"/>'
    o += '<rect width="540" height="70" fill="#4e4258"/><rect y="66" width="540" height="12" fill="#8a7e92"/><path d="M 0,78 L 540,78" stroke="#a89cae" stroke-width="2"/>'   # cornice
    o += "".join(f'<rect x="{x}" y="96" width="{w}" height="360" fill="none" stroke="#7a6c80" stroke-width="3"/>' for x, w in ((196, 110), (316, 110)))   # wall panels
    o += '<rect y="470" width="540" height="140" fill="#5a4c60"/><rect y="466" width="540" height="8" fill="#8a7e92"/>' + "".join(f'<rect x="{x}" y="488" width="76" height="104" fill="none" stroke="#4a3e50" stroke-width="3"/>' for x in range(12, 540, 90))   # wainscot
    # tall arched window, evening sky, curtains
    o += '<path d="M 28,470 L 28,190 Q 98,110 168,190 L 168,470 Z" fill="#2c3466"/>'
    o += '<path d="M 98,140 L 98,470 M 28,320 L 168,320" stroke="#3a3040" stroke-width="7"/><path d="M 20,192 Q 98,100 176,192" stroke="#9a8ea4" stroke-width="7" fill="none"/><rect x="18" y="466" width="160" height="10" fill="#8a7e92"/>'
    o += curtains(10, 120, 186, 600, ("#6a3a4e", "#86506a", "#4e2a3a"))
    # portraits on the wall, a small chandelier
    o += frame_pic(208, 130, 86, 110, PIC_PORTRAIT, "#7a5a3a") + frame_pic(330, 150, 84, 64, PIC_LAND, "#6a4a32") + frame_pic(338, 236, 68, 84, PIC_SAINT, "#7a5a3a")
    o += '<path d="M 270,78 L 270,120" stroke="#2a2228" stroke-width="2"/><g transform="translate(270,130)"><ellipse cx="0" cy="0" rx="34" ry="6" fill="#c8a860"/><path d="M -34,0 C -34,14 34,14 34,0" fill="#a88a4a"/>'
    o += "".join(f'<rect x="{x - 2}" y="-14" width="4" height="12" fill="#f2ece2"/><circle cx="{x}" cy="-17" r="2.6" fill="#fff4ec"/>' for x in (-28, -14, 0, 14, 28)) + "".join(f'<path d="M {x},6 l 0,10" stroke="#e8e2f0" stroke-width="2" opacity=".8"/>' for x in (-24, -8, 8, 24)) + '</g>'
    # doorway on the right (dark corridor beyond) with a carved frame
    o += '<rect x="440" y="250" width="100" height="360" fill="#3a2a2a"/><rect x="452" y="262" width="88" height="348" fill="#100c12"/><path d="M 436,250 L 540,250 L 540,240 L 432,240 Z" fill="#8a6a4a"/>'
    o += '<path d="M 452,610 L 540,610 L 540,480 C 510,500 480,560 452,610 Z" fill="#1c1620" opacity=".9"/>'
    # sheet-music cabinet and a chair against the wall
    o += '<g transform="translate(350,500)"><rect x="0" y="0" width="76" height="110" fill="#4a3428"/><rect x="0" y="0" width="76" height="6" fill="#6a4a38"/>' + "".join(f'<rect x="{6 + k * 11}" y="{14 + (k % 2) * 6}" width="9" height="{88 - (k % 2) * 6}" fill="{c}"/>' for k, c in enumerate(("#6a2a32", "#2a3a5a", "#efe8da", "#3a4a3a", "#5a2a4a", "#efe8da"))) + '</g>'
    o += '<g transform="translate(330,560)"><rect x="-4" y="-30" width="4" height="80" fill="#3a2a22"/><rect x="-4" y="10" width="36" height="6" fill="#5a3e30"/><rect x="28" y="16" width="4" height="34" fill="#3a2a22"/><rect x="-4" y="-30" width="30" height="34" rx="3" fill="#6a3a4e"/></g>'
    # floor: herringbone boards and a faded rug
    o += '<path d="M 0,610 L 540,610 L 540,960 L 0,960 Z" fill="#5a4038"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#4a3430" stroke-width="2"/>' for y in (640, 680, 730, 800, 880))
    o += "".join(f'<path d="M {270 + (x - 270) * .3:.0f},610 L {x},960" stroke="#4a3430" stroke-width="1.6"/>' for x in range(-300, 860, 70))
    o += '<path d="M 30,820 L 510,820 L 540,950 L 0,950 Z" fill="#6a3e4a"/><path d="M 48,830 L 492,830 L 518,940 L 22,940 Z" fill="none" stroke="#b08a6a" stroke-width="3"/><path d="M 70,846 L 470,846 L 492,926 L 48,926 Z" fill="none" stroke="#8a5a5a" stroke-width="2"/>'
    return o
_mu3 = music_room3() + C("agnes", 494, 614, .6)
_mu3 += C("mariam_piano", 180, 866, .78)
_mu3 += grand_piano()
_mu3 += '<path d="M 120,820 L 240,820 L 236,834 L 124,834 Z" fill="#3a2a2c" opacity="0"/>'
_mu3 += C("mek", 372, 912, .92)
ST["music"] = _mu3
L("music", .38, holes=((180, 560, 170), (372, 600, 140), (98, 300, 120)), beams=(("40,190 160,190 330,960 60,960", "#c8c4f0", .3),),
  glows=((236, 640, 120, CANDLE, .7), (270, 120, 120, WARM, .55)), motes=(60, 200, 320, 780, 22, "#f4eef8"),
  shadows=(("372,912 430,912 520,960 420,960", .35),))

# ------------------------------------------------------------------ 5. VERANDA: hanging plant -> small chandelier
_veg = ST["veranda"]
_plant0 = _veg.index('<path d="M 300,150 L 300,220" stroke="#2a2024" stroke-width="2"/><g transform="translate(300,232)">')
_plant1 = _veg.index('</g>', _plant0) + 4
CHANDELIER = ('<path d="M 300,150 L 300,196" stroke="#2a2024" stroke-width="2"/>'
              '<g transform="translate(300,206)"><path d="M -4,-10 L 4,-10 L 6,0 L -6,0 Z" fill="#b8985a"/>'
              '<path d="M -30,8 C -30,0 -10,2 0,0 C 10,2 30,0 30,8" stroke="#c8a860" stroke-width="2.4" fill="none"/><path d="M -18,10 C -18,4 18,4 18,10" stroke="#c8a860" stroke-width="2" fill="none"/>'
              + "".join(f'<rect x="{x - 2.4}" y="{y - 12}" width="4.8" height="12" fill="#f2ece2"/><path d="M {x},{y - 20} C {x - 2.6},{y - 16} {x - 2.6},{y - 14} {x},{y - 13} C {x + 2.6},{y - 14} {x + 2.6},{y - 16} {x},{y - 20} Z" fill="#fff4ec"/><circle cx="{x}" cy="{y - 16}" r="12" fill="url(#lg_ffe6c4)" opacity=".6" style="mix-blend-mode:screen"/>' for x, y in ((-30, 8), (30, 8), (-18, 10), (18, 10), (0, 2)))
              + '<path d="M 0,0 L 0,22" stroke="#c8a860" stroke-width="2"/>' + "".join(f'<path d="M {x},10 l 0,9" stroke="#e8e2f0" stroke-width="1.6" opacity=".85"/><circle cx="{x}" cy="21" r="1.6" fill="#f4f0fa"/>' for x in (-24, -10, 10, 24))
              + '<circle cx="0" cy="25" r="3" fill="#e8e2f0"/></g>')
ST["veranda"] = _veg[:_plant0] + CHANDELIER + _veg[_plant1:]
GLOWCOLS.add("#ffe6c4")

# ------------------------------------------------------------------ 6. KITCHEN: no rice bag; more real kitchen things
_rice = '<g transform="translate(470,700)"><path d="M -36,0 C -42,-46 -26,-72 0,-74 C 26,-72 42,-46 36,0 Z" fill="#d8c8a8"/><text x="0" y="-30" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" font-weight="700" fill="#6a4a34">ข้าวหอม</text></g>'
KITCHEN_EXTRA = (
    '<g transform="translate(330,140)"><circle r="20" fill="#efe8da" stroke="#3a3030" stroke-width="3"/><path d="M 0,0 L 0,-13 M 0,0 L 9,4" stroke="#2a2228" stroke-width="2"/></g>'   # wall clock
    '<path d="M 230,236 C 236,262 230,290 236,316" stroke="#7a6a4a" stroke-width="3" fill="none"/>' + "".join(f'<ellipse cx="{232 + (k % 2) * 6}" cy="{246 + k * 12}" rx="6" ry="5" fill="#efe6d4"/>' for k in range(6)) +   # garlic braid
    '<rect x="150" y="452" width="56" height="18" rx="2" fill="#b8946a"/><path d="M 160,452 l 10,-10 l 14,0 l -4,10 Z" fill="#6a9a4a"/><ellipse cx="190" cy="448" rx="7" ry="5" fill="#c84a3a"/>'   # chopping board, greens, chilli
    '<rect x="260" y="458" width="10" height="14" rx="2" fill="#6a4a2a"/><rect x="274" y="456" width="9" height="16" rx="2" fill="#2a4a2a"/><rect x="287" y="460" width="8" height="12" rx="2" fill="#e8e0d0"/>'   # sauce bottles
    '<path d="M 0,560 L 20,560" stroke="#c8c0b0" stroke-width="0"/>'
    '<g transform="translate(470,600)"><rect x="-30" y="-120" width="60" height="120" fill="#e8e2d8"/><rect x="-30" y="-120" width="60" height="6" fill="#c8c0b0"/><rect x="-26" y="-60" width="52" height="4" fill="#c8c0b0"/><rect x="18" y="-100" width="4" height="22" fill="#9a9aa4"/><rect x="18" y="-48" width="4" height="22" fill="#9a9aa4"/></g>'   # old fridge by the back door
    '<rect x="452" y="470" width="36" height="6" fill="#8a7a68" opacity="0"/>'
    '<path d="M 20,640 L 120,640 L 116,650 L 24,650 Z" fill="#4a3a30" opacity=".5"/>')
_kroom = kitchen_room()
def kitchen_table3():
    """Plain wooden kitchen table standing on the floor at mid-depth: top in perspective, apron, four legs, two chairs, soup bowls."""
    o = soft_shadow(270, 806, 190, 12, .4)
    o += '<g transform="translate(150,700)"><rect x="-4" y="-60" width="6" height="106" fill="#3a2a20"/><rect x="34" y="-60" width="6" height="106" fill="#2e2018"/><rect x="-4" y="-62" width="44" height="8" fill="#5a4030"/><rect x="-4" y="-40" width="44" height="5" fill="#4a3428"/></g>'   # chair back, far side
    o += '<path d="M 128,700 L 412,700 L 440,726 L 100,726 Z" fill="#9a7458"/><path d="M 128,700 L 412,700 L 416,704 L 124,704 Z" fill="#b08a6a"/>'   # top
    o += '<path d="M 100,726 L 440,726 L 440,740 L 100,740 Z" fill="#6a4a36"/>'   # apron
    o += '<rect x="108" y="740" width="12" height="66" fill="#4a3428"/><rect x="420" y="740" width="12" height="66" fill="#3a281e"/>'   # front legs
    o += '<rect x="136" y="726" width="8" height="54" fill="#3a281e"/><rect x="398" y="726" width="8" height="54" fill="#2e2018"/>'   # back legs (shorter: further away)
    o += '<path d="M 0,0" fill="none"/>'
    o += '<ellipse cx="200" cy="710" rx="26" ry="6" fill="#efe8dc"/><ellipse cx="200" cy="708" rx="19" ry="3.6" fill="#d8c48e"/><ellipse cx="300" cy="712" rx="34" ry="7" fill="#9a9aa4"/><ellipse cx="300" cy="709" rx="28" ry="4.6" fill="#d8c48e"/>'
    o += '<path d="M 226,712 l 22,-3" stroke="#d8d4dc" stroke-width="2.4"/><rect x="356" y="700" width="10" height="12" rx="2" fill="#e8e2ea"/>'
    o += '<g transform="translate(400,740)"><rect x="-4" y="-56" width="6" height="96" fill="#3a2a20"/><rect x="30" y="-20" width="6" height="60" fill="#2e2018"/><rect x="-4" y="-22" width="40" height="7" fill="#5a4030"/><rect x="-4" y="-58" width="8" height="10" fill="#5a4030"/></g>'   # chair pulled out, near side
    return o
_kt_old = kitchen_table()
_kd = C("daeng_whisper", 250, 900, .98)
assert _kt_old in ST["kitchen"] and _kd in ST["kitchen"]
ST["kitchen"] = ST["kitchen"].replace(_kroom, _kroom.replace(_rice, "") + KITCHEN_EXTRA).replace(_kt_old, "").replace(_kd, kitchen_table3() + _kd)

# ------------------------------------------------------------------ 7. FOYER where Mek finds the doll (shots 182-189): furnished, dim, door light
def staircase():
    """Wooden staircase against the left wall, seen from the side: a wide bottom step, then eight steps rising to the
    upper left; each tread shows its top face going back into the room, closed side panel underneath, newel post,
    handrail parallel to the slope, one baluster per step."""
    o = ""
    steps = [(230, 640, 60, 36)] + [(170 - k * 20, 604 - k * 38, 20, 38) for k in range(8)]   # (right x, bottom y, run, rise)
    prof = [(232, 640)]
    for (xr, yb, run, rise) in steps:
        prof += [(xr, yb - rise), (xr - run, yb - rise)]
    prof += [(0, prof[-1][1]), (0, 640)]
    o += '<path d="M ' + " L ".join(f"{x},{y}" for x, y in prof) + ' Z" fill="#4e362c"/>'   # closed side panel under the stairs
    o += '<path d="M 0,300 L 18,300 L 230,640 L 0,640 Z" fill="#46302a" opacity=".0"/>'
    o += "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#3e2a22" stroke-width="2"/>' for x, y, w, h in ((14, 470, 60, 150), (90, 540, 60, 84), (160, 590, 50, 40)))   # panelling on the side
    D = 14   # depth of each tread going back into the room (drawn up and to the right)
    for (xr, yb, run, rise) in steps:
        yt = yb - rise
        o += f'<path d="M {xr - run},{yt} L {xr},{yt} L {xr + D},{yt - D * .6:.1f} L {xr - run + D},{yt - D * .6:.1f} Z" fill="#8a6650"/>'   # tread top
        o += f'<path d="M {xr - run},{yt} L {xr},{yt}" stroke="#a88068" stroke-width="2.4"/>'                                       # rounded nosing catches the light
        o += f'<path d="M {xr},{yt} L {xr + D},{yt - D * .6:.1f} L {xr + D},{yb - D * .6:.1f} L {xr},{yb} Z" fill="#5e4234"/>'      # end of the step
    # newel post, handrail parallel to the slope, balusters
    o += '<rect x="214" y="560" width="16" height="80" fill="#3a281e"/><rect x="210" y="552" width="24" height="10" rx="2" fill="#5a3e2a"/><circle cx="222" cy="546" r="9" fill="#5a3e2a"/>'
    o += '<path d="M 222,556 L 168,522 L 10,222" stroke="#4a3428" stroke-width="9" stroke-linecap="round" fill="none"/><path d="M 222,553 L 168,519 L 10,219" stroke="#7a5a44" stroke-width="2" fill="none"/>'
    for (xr, yb, run, rise) in steps[1:]:
        x = xr - run / 2; yt = yb - rise
        yr = 522 + (x - 168) * (522 - 222) / (168 - 10)   # rail height above this tread
        o += f'<rect x="{x - 2}" y="{yr:.0f}" width="4" height="{yt - yr:.0f}" fill="#3a281e"/>'
    o += '<rect x="196" y="533" width="4" height="71" fill="#3a281e"/><rect x="178" y="523" width="4" height="81" fill="#3a281e"/>'
    return o

def foyer_room():
    o = '<rect width="540" height="960" fill="#8a7e80"/>'
    o += '<rect width="540" height="60" fill="#5a4e52"/><rect y="56" width="540" height="10" fill="#a89a98"/>'
    o += '<rect y="470" width="540" height="170" fill="#6a5652"/><rect y="466" width="540" height="8" fill="#a89a98"/>' + "".join(f'<rect x="{x}" y="490" width="70" height="130" fill="none" stroke="#5a4642" stroke-width="3"/>' for x in range(150, 540, 84))
    # pictures on the wall (several, different sizes), all a little crooked
    o += frame_pic(176, 130, 70, 90, PIC_PORTRAIT, "#5a3e2a") + frame_pic(256, 120, 96, 70, PIC_GROUP, "#6a4a32") + frame_pic(262, 206, 50, 64, PIC_SAINT, "#6a4a32")
    o += frame_pic(322, 210, 60, 46, PIC_LAND, "#5a3e2a") + frame_pic(200, 240, 46, 58, PIC_GROUP, "#4a3428")
    o += '<g transform="translate(366,150)"><rect x="-2" y="0" width="4" height="40" fill="#3a2a22"/><rect x="-12" y="10" width="24" height="4" fill="#3a2a22"/></g>'   # wooden crucifix
    # tall glass-front cabinet with crockery and old books
    o += '<g transform="translate(150,330)"><rect x="0" y="0" width="0" height="0"/></g>'
    o += '<rect x="390" y="300" width="0" height="0"/>'
    # front door on the right, open: dusk outside, light spills in a long wedge across the tiles
    o += '<rect x="410" y="250" width="130" height="392" fill="#3a2a24"/><rect x="424" y="262" width="116" height="380" fill="#6a72a8"/><rect x="424" y="262" width="116" height="200" fill="#8a8ec0"/>'
    o += '<path d="M 424,560 L 540,540 L 540,642 L 424,642 Z" fill="#3a4a3a"/><path d="M 424,262 L 470,280 L 470,642 L 424,642 Z" fill="#4a3428"/><path d="M 470,280 L 470,642" stroke="#2a1e18" stroke-width="2"/><circle cx="462" cy="460" r="3" fill="#c8a860"/>'   # door leaf swung in
    # tiled floor (old patterned cement tiles) in perspective
    o += '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#8a7a72"/>'
    o += "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#6a5a54" stroke-width="2"/>' for y in (664, 694, 732, 782, 846, 926))
    o += "".join(f'<path d="M {270 + (x - 270) * .3:.0f},640 L {x},960" stroke="#6a5a54" stroke-width="2"/>' for x in range(-330, 900, 66))
    o += "".join(f'<rect x="{270 + (x - 270) * .55:.0f}" y="{y}" width="10" height="5" fill="#a8968a" transform="rotate(45 {270 + (x - 270) * .55:.0f} {y})" opacity=".55"/>' for x in range(-200, 760, 66) for y in (712, 812))
    o += staircase()
    # side table with a little lamp (lit, peach-white), a chair, an umbrella stand, a coat rack with a hat
    o += '<g transform="translate(300,640)"><rect x="-44" y="-96" width="88" height="10" fill="#5a3e2e"/><rect x="-40" y="-86" width="6" height="86" fill="#3a281e"/><rect x="34" y="-86" width="6" height="86" fill="#3a281e"/><rect x="-36" y="-60" width="72" height="5" fill="#4a3428"/>'
    o += '<rect x="-4" y="-130" width="8" height="34" fill="#c8a860"/><path d="M -22,-130 L 22,-130 L 14,-160 L -14,-160 Z" fill="#f2e2d6"/><path d="M -2,-130 L 22,-130 L 14,-160 L 4,-160 Z" fill="#dcc8bc"/>'
    o += '<rect x="20" y="-104" width="16" height="8" fill="#6a2a32"/><rect x="22" y="-110" width="14" height="6" fill="#2a3a5a"/></g>'
    o += '<g transform="translate(376,640)"><rect x="-18" y="-50" width="36" height="6" fill="#5a3e2e"/><rect x="-18" y="-96" width="6" height="96" fill="#3a281e"/><rect x="12" y="-44" width="6" height="44" fill="#3a281e"/><rect x="-18" y="-96" width="30" height="40" fill="#6a4a3a"/></g>'
    o += '<g transform="translate(396,646)"><path d="M -10,0 L 10,0 L 8,-40 L -8,-40 Z" fill="#4a4a5a"/><path d="M -4,-40 L -6,-74 M 2,-40 L 6,-70" stroke="#2a2a34" stroke-width="3"/><path d="M -6,-74 c -6,0 -6,6 -2,8" stroke="#2a2a34" stroke-width="2" fill="none"/></g>'
    o += '<g transform="translate(230,470)"><rect x="-2" y="0" width="0" height="0"/></g>'
    # long cabinet with glass doors under the pictures (crockery, a candle, a rosary hanging on the key)
    o += '<g transform="translate(180,540)"><rect x="0" y="0" width="0" height="0"/></g>'
    return o
FOYER_CAB = ('<g transform="translate(214,510)"><rect x="0" y="0" width="60" height="132" fill="#4a3226"/><rect x="0" y="0" width="60" height="6" fill="#6a4a36"/>'
             '<rect x="5" y="10" width="23" height="70" fill="#2a2a3a"/><rect x="32" y="10" width="23" height="70" fill="#2a2a3a"/>'
             + "".join(f'<ellipse cx="{x}" cy="{y}" rx="7" ry="3" fill="#efe8da"/>' for x, y in ((12, 30), (22, 30), (40, 30), (48, 30))) + "".join(f'<rect x="{x}" y="{y}" width="5" height="18" fill="{c}"/>' for x, y, c in ((8, 58, "#6a2a32"), (14, 60, "#2a3a5a"), (36, 58, "#5a4a2a"), (42, 56, "#3a4a3a"), (48, 60, "#6a2a32")))
             + '<path d="M 6,12 L 26,12 L 6,40 Z M 34,12 L 52,12 L 34,38 Z" fill="#ffffff" opacity=".12"/><rect x="4" y="90" width="52" height="36" fill="#3a2820"/><circle cx="30" cy="98" r="2.4" fill="#c8a860"/>'
             '<path d="M 30,100 C 26,108 28,116 30,120 C 32,116 34,108 30,100" stroke="#8a2a32" stroke-width="1" fill="none"/></g>')
ST["steps"] = (foyer_room() + FOYER_CAB + C("agnes_left", 470, 646, .64) + C("mek", 300, 916, .94)
               + '<g transform="translate(200,560) scale(.42)">' + ragdoll() + '</g>')
L("steps", .4, holes=((470, 420, 150), (300, 640, 160), (130, 760, 90)), beams=(("424,300 540,280 540,960 150,960", "#c8ccf0", .38),),
  glows=((300, 490, 90, WARM, .6),), motes=(200, 420, 540, 880, 20, "#eef0ff"), shadows=(("300,916 360,916 440,960 330,960", .4),))

# ------------------------------------------------------------------ 8. MARIAM AT DAWN: nightgown with mud on the hem, sleeves, legs, bare muddy feet
NIGHTGOWN = ("#ebe8ee", "#f8f6fa", "#c4c0cc")
MUD, MUD2 = "#6a4e3a", "#8a6a4e"
def _mud_robe():
    r = _rr.Random(77); o = ""
    for _ in range(14):   # heavier at the hem, lighter going up
        x = r.uniform(-48, 48); y = r.uniform(300, 356); w = r.uniform(8, 20); h = r.uniform(5, 14)
        o += f'<path d="M {x:.0f},{y:.0f} c {w * .4:.0f},{-h * .6:.0f} {w:.0f},{-h * .2:.0f} {w * .9:.0f},{h * .4:.0f} c {-w * .3:.0f},{h * .6:.0f} {-w * .8:.0f},{h * .5:.0f} {-w * .9:.0f},{-h * .4:.0f} Z" fill="{r.choice((MUD, MUD2))}" opacity="{r.uniform(.55, .9):.2f}"/>'
    for _ in range(6):
        x = r.uniform(-34, 34); y = r.uniform(240, 300)
        o += f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{r.uniform(3, 7):.1f}" ry="{r.uniform(2, 4):.1f}" fill="{MUD2}" opacity="{r.uniform(.35, .6):.2f}"/>'
    o += f'<path d="M -50,350 C -30,344 -10,352 10,346 C 26,342 40,350 50,348 L 50,358 L -50,358 Z" fill="{MUD}" opacity=".85"/>'   # soaked hem line
    o += f'<path d="M -20,232 c 4,-6 12,-4 10,4 c -2,6 -10,4 -10,-4 Z M 14,262 c 3,-5 10,-3 8,3" fill="{MUD2}" opacity=".5"/>'   # knee marks where she knelt
    return o
def _mud_sleeve(side):
    s = side
    return (f'<path d="M {s * 46 - 6},180 c 4,-4 12,-2 10,6 c -3,5 -10,4 -10,-6 Z" fill="{MUD2}" opacity=".6"/>'
            f'<path d="M {s * 50 - 10},206 L {s * 50 + 10},206 L {s * 50 + 12},214 L {s * 50 - 12},214 Z" fill="{MUD}" opacity=".7"/>'
            f'<ellipse cx="{s * 50}" cy="226" rx="6" ry="4" fill="{MUD}" opacity=".55"/>')   # dirt on the cuff and the hand
_ms = cf.MAR_SKIN
_feet = ("#a07a5e", "#8a644a")
mariam_night = cf.figure("mariam_night", cf.hs(cf.bc.habit_back("#1a1520")),
    cf.leg("mariam", -1, NIGHTGOWN, _feet[0], "#6a4a36", pants_to=0) + cf.leg("mariam", 1, NIGHTGOWN, _feet[1], "#5a3e2e", pants_to=0),
    cf.robe(NIGHTGOWN) + _mud_robe(),
    cf.arm("mariam", -1, NIGHTGOWN, _ms, wide=True, hand_extra=_mud_sleeve(-1)) + cf.arm("mariam", 1, NIGHTGOWN, _ms, wide=True, hand_extra=_mud_sleeve(1) + cf.SCAR),
    cf.hs(cf.bc.habit_over("#2c2532", "#120e16") + cf.MARIAM_HEAD))
cf.F["mariam_night"] = mariam_night
pose("mariam_night", "mariam_night")
_dw = ST["dawn_walk"]
_mi = _dw.index(C("mariam", 220, 920, 1.0, .95))
ST["dawn_walk"] = _dw.replace(C("mariam", 220, 920, 1.0, .95), C("mariam_night", 220, 920, 1.0, .95)
    + '<path d="M 150,924 c 10,-4 22,-2 30,4 M 250,930 c 8,-3 18,-2 24,3" stroke="#6a4e3a" stroke-width="5" stroke-linecap="round" opacity=".5"/>')   # muddy footprints behind her

# ------------------------------------------------------------------ 9. JAMES'S CONDO: gamer + video-editor room, Dean asleep by the desk
DEAN_DEFS = ""
_cat = open(os.path.join(HERE, "..", "..", "..", "characters", "cat.html")).read()
_c0 = _cat.index('<clipPath id="chead">'); _c1 = _cat.index('</defs>', _c0)
DEAN_DEFS = _cat[_c0:_c1]
for _i in ("chead", "cside", "headBase", "eyesSleepy", "eyesAlert", "headSide", "sitBody"):
    DEAN_DEFS = DEAN_DEFS.replace(f'id="{_i}"', f'id="dn_{_i}"').replace(f'url(#{_i})', f'url(#dn_{_i})').replace(f'href="#{_i}"', f'href="#dn_{_i}"')
_l0 = _cat.index('<!-- tail tucked along the ground -->'); _l1 = _cat.index('<!-- head turned to camera, sleepy -->')
DEAN_LIE = _cat[_l0:_l1]
for _i in ("headBase", "eyesSleepy"):
    DEAN_LIE = DEAN_LIE.replace(f'href="#{_i}"', f'href="#dn_{_i}"')
def dean_lying(x, y, k):
    """Dean (approved design, pose 3) lying stretched out, head toward the camera, sleepy eyes. Tail group id dnTail moves in the player."""
    body = DEAN_LIE.replace('<!-- tail tucked along the ground -->', '<!-- tail --><g id="dnTail">', 1)
    body = body.replace('<!-- low loaf body -->', '</g><!-- low loaf body -->', 1)
    return (f'<ellipse cx="{x + 10 * k:.0f}" cy="{y + 96 * k:.0f}" rx="{170 * k:.0f}" ry="{11 * k:.0f}" fill="#0a080c" opacity=".45"/>'
            f'<g transform="translate({x},{y}) scale({k})"><g transform="translate(-30,40)">{body}<g id="dnHead" transform="translate(66,-30) scale(0.95)"><use href="#dn_headBase"/><g id="dnEyes"><use href="#dn_eyesSleepy"/></g></g></g></g>')
CONDO_EXTRA = (
    # editing timeline on the right monitor, a third vertical screen, mic on a boom arm, a webcam + ring light, LED strip under the desk, acoustic panels, posters
    '<rect x="406" y="408" width="30" height="62" rx="3" fill="#0e0c1c"/><rect x="409" y="411" width="24" height="56" fill="#2a2a4a"/>' + "".join(f'<rect x="411" y="{415 + k * 7}" width="{8 + (k * 7) % 12}" height="3" fill="{c}"/>' for k, c in enumerate(("#9a86ff", "#ff7ab0", "#7affc8", "#9a86ff", "#ffe07a", "#7ac8ff", "#ff7ab0")))
    + '<path d="M 250,400 L 236,360 L 262,330" stroke="#2a2440" stroke-width="4" fill="none"/><rect x="254" y="314" width="16" height="28" rx="8" fill="#1a1828"/><path d="M 256,322 L 268,322 M 256,328 L 268,328" stroke="#4a4870" stroke-width="1.4"/>'
    + '<circle cx="300" cy="408" r="5" fill="#1a1828"/><circle cx="300" cy="408" r="2" fill="#6a5ae0"/>'
    + '<g transform="translate(480,470)"><circle cx="0" cy="-60" r="22" fill="none" stroke="#efeaff" stroke-width="5"/><circle cx="0" cy="-60" r="22" fill="none" stroke="#c8c0ff" stroke-width="1.4" opacity=".7"/><path d="M 0,-38 L 0,170 M -16,170 L 0,140 L 16,170" stroke="#2a2440" stroke-width="3" fill="none"/></g>'
    + '<rect x="250" y="512" width="160" height="3" fill="#ff5aa0" opacity=".9"/><rect x="250" y="515" width="160" height="10" fill="#ff5aa0" opacity=".18"/>'
    + "".join(f'<rect x="{x}" y="{y}" width="26" height="26" fill="#2c2850"/><path d="M {x},{y + 8} L {x + 26},{y + 8} M {x},{y + 17} L {x + 26},{y + 17}" stroke="#3a3466" stroke-width="2"/>' for x, y in ((420, 150), (448, 150), (420, 178), (448, 178)))
    + '<g transform="translate(300,150)"><rect x="0" y="0" width="60" height="70" fill="#1e1a3a"/><rect x="4" y="4" width="52" height="62" fill="#5a3aa8"/><path d="M 10,50 L 30,14 L 50,50 Z" fill="#ffb05a"/><text x="30" y="62" text-anchor="middle" font-family="Inter, sans-serif" font-size="7" font-weight="700" fill="#fff">LEVEL 99</text></g>'
    + '<g transform="translate(232,480)"><path d="M -8,20 L 8,20 L 4,0 L -4,0 Z" fill="#2a2440"/><path d="M -10,-2 C -10,-18 10,-18 10,-2" stroke="#1a1828" stroke-width="4" fill="none"/><rect x="-12" y="-6" width="6" height="10" rx="2" fill="#1a1828"/><rect x="6" y="-6" width="6" height="10" rx="2" fill="#1a1828"/></g>'   # headphone stand
)
_cr_old = condo_room()
def photo_frame(x, y, w, h, r=0):
    """Framed snapshot: James and Tawan from the waist up (shoulders, shirts, arms), the cat in front."""
    s_ = w / 120
    jx, tx = -w * .18, w * .16
    o = f'<g transform="translate({x},{y}) rotate({r})"><rect x="{-w / 2}" y="{-h / 2}" width="{w}" height="{h}" fill="#2a2420"/>'
    o += f'<clipPath id="pf{int(x)}{int(y)}"><rect x="{-w / 2 + 5}" y="{-h / 2 + 5}" width="{w - 10}" height="{h - 10}"/></clipPath><g clip-path="url(#pf{int(x)}{int(y)})">'
    o += f'<rect x="{-w / 2 + 5}" y="{-h / 2 + 5}" width="{w - 10}" height="{h - 10}" fill="#c8d8e8"/><rect x="{-w / 2 + 5}" y="{h * .1:.0f}" width="{w - 10}" height="{h * .4:.0f}" fill="#a8b0a0"/>'
    for cx, top, cols in ((jx, h * .02, ("#2b3768", "#3d4b8a")), (tx, h * .04, ("#ecdcc0", "#f6ecd8"))):
        y0 = top + 9 * s_
        o += (f'<path d="M {cx - 6 * s_:.1f},{y0:.1f} L {cx + 6 * s_:.1f},{y0:.1f} L {cx + 20 * s_:.1f},{y0 + 8 * s_:.1f} L {cx + 22 * s_:.1f},{h / 2:.1f} L {cx - 22 * s_:.1f},{h / 2:.1f} L {cx - 20 * s_:.1f},{y0 + 8 * s_:.1f} Z" fill="{cols[0]}"/>'
              f'<path d="M {cx - 20 * s_:.1f},{y0 + 8 * s_:.1f} L {cx - 12 * s_:.1f},{y0 + 4 * s_:.1f} L {cx - 12 * s_:.1f},{h / 2:.1f} L {cx - 22 * s_:.1f},{h / 2:.1f} Z" fill="{cols[1]}"/>'
              f'<rect x="{cx - 3 * s_:.1f}" y="{y0 - 3 * s_:.1f}" width="{6 * s_:.1f}" height="{5 * s_:.1f}" fill="#efc7b0"/>')
    o += f'<path d="M {jx + 18 * s_:.1f},{h * .02 + 20 * s_:.1f} L {tx - 14 * s_:.1f},{h * .04 + 22 * s_:.1f}" stroke="#2b3768" stroke-width="{5 * s_:.1f}" stroke-linecap="round"/>'   # his arm round her shoulders
    o += f'<g transform="translate({jx:.0f},{h * .02:.0f}) scale({.3 * s_:.2f})"><use href="#jhead"/></g>'
    o += f'<g transform="translate({tx:.0f},{h * .04:.0f}) scale({.28 * s_:.2f})"><use href="#tback"/><use href="#thead"/></g>'
    o += f'<g transform="translate({-w * .02:.0f},{h * .32:.0f}) scale({.16 * s_:.2f})"><ellipse cx="0" cy="34" rx="46" ry="30" fill="#e79a4a"/><circle r="40" fill="#e79a4a"/><circle cx="-14" cy="-6" r="6" fill="#3a2a22"/><circle cx="14" cy="-6" r="6" fill="#3a2a22"/><ellipse cx="0" cy="16" rx="18" ry="12" fill="#f7e3c4"/></g>'
    return o + '</g></g>'
_cr = condo_room()
ST["call"] = ST["call"].replace(_cr_old, _cr)
_oldcat = f'<g transform="translate(220,640) scale(.9)">{v1.CAT}</g>'
ST["condo"] = ST["condo"].replace(_cr_old, _cr + CONDO_EXTRA).replace(_oldcat, dean_lying(424, 784, .34))

# ------------------------------------------------------------------ 10. VIDEO CALL: no floating light blobs; Mek-speaking variant
CALL_BLOBS = ('<circle cx="380" cy="300" r="320" fill="url(#lg_b4a8ff)" opacity=".6" style="mix-blend-mode:screen"/>',)
_call = ST["call"]
for _b in CALL_BLOBS: _call = _call.replace(_b, '<rect width="540" height="960" fill="#8a7aff" opacity=".06" style="mix-blend-mode:screen"/>')
_lc = _call.find('<circle cx="460" cy="150" r="260" fill="url(#lg_b4a8ff)"')
if _lc > 0: _call = _call[:_lc] + '<rect width="540" height="960" fill="#06050c" opacity=".2"/>'   # drop the old glow/blob overlay block from L("call")
_call = _call.replace('<circle cx="70" cy="80" r="70" fill="url(#lg_cfe0ff)" opacity=".6"/>', '')
ST["call"] = _call
def call_mek_screen():
    """Same call, Mek's camera big (he is talking), James small top-right: the shot follows whoever speaks."""
    o = '<rect width="540" height="960" fill="#05040a"/>'
    o += '<svg x="0" y="0" width="540" height="960" viewBox="0 0 540 960" preserveAspectRatio="xMidYMid slice">' + guest_room() + '</svg>'
    o += '<rect width="540" height="960" fill="#0c0a18" opacity=".55"/>'
    o += put(P["mek_phone"], 280, 1460, 2.4, .9)
    o += '<rect width="540" height="960" fill="#cfe0ff" opacity=".06" style="mix-blend-mode:screen"/>'
    o += ('<g transform="translate(372,96)"><rect width="140" height="210" rx="14" fill="#141018"/><svg x="0" y="0" width="140" height="210" viewBox="0 0 140 210">'
          '<svg x="0" y="0" width="140" height="210" viewBox="230 300 260 390" preserveAspectRatio="xMidYMid slice">' + condo_room() + '</svg>'
          + put(P["james_desk"], 70, 470, 1.05) + '</svg><rect width="140" height="210" rx="14" fill="none" stroke="#ffffff" stroke-opacity=".5" stroke-width="2"/></g>')
    o += '<text x="40" y="44" font-family="Inter, sans-serif" font-size="17" font-weight="600" fill="#fff">02:59</text><rect x="470" y="32" width="34" height="15" rx="4" fill="none" stroke="#fff" stroke-width="1.6"/><rect x="473" y="35" width="20" height="9" rx="2" fill="#fff"/>'
    o += '<text x="40" y="96" font-family="IBM Plex Sans Thai, sans-serif" font-size="20" font-weight="700" fill="#fff">เจม</text><text x="40" y="120" font-family="Inter, sans-serif" font-size="14" fill="#e0e0ee">12:48</text>'
    for i, (col, icon) in enumerate((("#3a3a48", "M -8,-4 L 8,-4 M 0,-12 L 0,4"), ("#3a3a48", "M -10,-6 L 4,-6 L 4,6 L -10,6 Z M 4,-2 L 12,-7 L 12,7 L 4,2"), ("#e5484d", "M -12,2 C -6,-6 6,-6 12,2"), ("#3a3a48", "M -6,-10 L -6,10 M 6,-10 L 6,10"))):
        x = 110 + i * 107
        o += f'<circle cx="{x}" cy="880" r="30" fill="{col}" opacity=".92"/><path d="{icon}" transform="translate({x},880)" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return o
ST["call_mek"] = call_mek_screen()

# ------------------------------------------------------------------ 11. DAENG AT THE FOOT OF THE TOWER: a real body lying on the ground (no wound shown)
def daeng_fallen():
    """Lying on her side, seen across the ground: head turned away into the grass, one arm thrown out toward the keys,
    the other folded under, knees bent, sarong and apron following the body. Local origin = ground under her hips."""
    SK, SKS = "#e3b088", "#c99070"
    o = '<g>'
    o += '<ellipse cx="0" cy="14" rx="190" ry="14" fill="#05040a" opacity=".55" filter="url(#lsoft)"/>'
    # legs: sarong wraps both, knees bent toward the camera, bare shins, one sandal off
    o += '<path d="M 20,-6 C 60,-30 110,-26 130,-10 C 140,0 136,10 124,12 L 30,12 C 18,10 14,2 20,-6 Z" fill="#4a3a4a"/><path d="M 30,-14 C 70,-30 110,-26 128,-12" stroke="#5e4c5e" stroke-width="6" fill="none"/>'
    o += '<path d="M 60,-4 C 80,-12 104,-12 120,-6" stroke="#3a2c3a" stroke-width="2" fill="none"/>'
    o += f'<path d="M 124,-2 C 142,-6 160,-2 176,6 L 172,14 C 156,8 140,6 124,10 Z" fill="{SK}"/><path d="M 120,6 C 140,8 158,12 170,18 L 166,24 C 152,18 138,16 120,14 Z" fill="{SKS}"/>'
    o += '<path d="M 174,2 C 184,2 190,8 188,14 L 172,16 Z" fill="#6a4a3a"/>'   # sandal still on
    o += f'<ellipse cx="172" cy="22" rx="7" ry="4" fill="{SKS}"/>'   # the other bare foot
    o += '<g transform="translate(204,20) rotate(18)"><path d="M -12,-4 L 12,-4 C 16,0 14,6 10,6 L -12,6 Z" fill="#5a3e30"/><path d="M -6,-4 C -2,-10 4,-10 6,-4" stroke="#3a2a22" stroke-width="2" fill="none"/></g>'   # lost sandal
    # torso on its side, floral blouse, apron twisted around the hips
    o += '<path d="M -96,-16 C -80,-40 -20,-44 20,-30 C 36,-24 40,-6 30,8 L -90,12 C -104,8 -106,-6 -96,-16 Z" fill="#8a3a3e"/><path d="M -90,-24 C -70,-40 -20,-42 16,-32" stroke="#a54a4e" stroke-width="7" fill="none"/>'
    o += "".join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="#e8b0a0" opacity=".8"/>' for x, y in ((-70, -18), (-40, -24), (-10, -20), (-56, -2), (-24, -6), (6, -10)))
    o += '<path d="M -20,-30 C 0,-36 26,-30 36,-14 C 44,0 36,10 20,12 L -30,12 C -20,0 -26,-18 -20,-30 Z" fill="#748894"/><path d="M -20,-30 C 0,-36 26,-30 36,-14" stroke="#8a9eaa" stroke-width="4" fill="none"/><path d="M 30,-20 c 14,-10 22,0 14,8" stroke="#748894" stroke-width="5" fill="none"/>'
    # arm folded under the chest (only the hand shows), arm thrown out toward the keys
    o += f'<path d="M -60,8 C -52,14 -40,14 -34,10 L -36,4 C -42,8 -52,8 -58,4 Z" fill="{SKS}"/>'
    o += '<path d="M -86,-26 C -100,-40 -120,-50 -150,-50 L -152,-38 C -124,-38 -104,-28 -92,-14 Z" fill="#6c2b30"/>'
    o += f'<path d="M -150,-50 C -170,-50 -186,-44 -200,-34 L -196,-26 C -184,-34 -168,-40 -152,-38 Z" fill="{SK}"/><ellipse cx="-204" cy="-28" rx="9" ry="6" fill="{SK}"/><path d="M -212,-30 l -6,-2 M -212,-26 l -7,0 M -210,-22 l -6,2" stroke="{SKS}" stroke-width="2.4" stroke-linecap="round"/>'
    # head: lying on the grass, face turned away from us (we see the grey bun and an ear), a hairpin fallen out
    o += f'<ellipse cx="-118" cy="-6" rx="24" ry="20" fill="{SKS}"/><path d="M -140,-16 C -140,-34 -100,-36 -96,-14 C -94,0 -104,12 -118,14 C -134,14 -142,2 -140,-16 Z" fill="#a9a4a6"/>'
    o += '<ellipse cx="-104" cy="-24" rx="11" ry="9" fill="#bdb8ba"/><path d="M -110,-30 C -104,-34 -96,-30 -98,-22" stroke="#d8d4d6" stroke-width="2" fill="none"/><ellipse cx="-126" cy="0" rx="4" ry="6" fill="#d9a07c"/>'
    o += '<path d="M -150,10 l 16,-4" stroke="#8a8488" stroke-width="2"/>'
    return o + '</g>'
_tn3 = ST["tower_night"]
_old_body = '<g transform="translate(330,936) scale(.7)"><path d="M -110,0 C -100,-18 70,-22 100,-6 L 102,14 C 50,22 -70,22 -110,12 Z" fill="#6c2b30"/><path d="M -40,-14 L 64,-16 L 68,14 L -38,16 Z" fill="#748894"/><ellipse cx="-124" cy="2" rx="18" ry="14" fill="#a9a4a6"/><path d="M -20,14 L -60,36 L -54,42 L -12,20 Z" fill="#c98f69"/><rect x="-74" y="36" width="10" height="7" fill="#fbf8f2"/></g>'
assert _old_body in _tn3, "tower body not found"
ST["tower_night"] = _tn3.replace(_old_body, '<g transform="translate(340,934) scale(.66)">' + daeng_fallen() + '</g>'
    + '<path d="M 206,938 c 10,-2 18,2 16,8" stroke="#f2f0ee" stroke-width="2" fill="none" opacity=".6"/>')   # corner of white cloth near her hand

# ------------------------------------------------------------------ 12. POLICE ARRIVE (shots 256-264): building, road, police car, clouds, dawn
def police_car(x, y, k=1.0, flip=False):
    s = -1 if flip else 1
    o = f'<g transform="translate({x},{y}) scale({k * s},{k})">'
    o += '<ellipse cx="0" cy="4" rx="150" ry="10" fill="#05040a" opacity=".45" filter="url(#lsoft)"/>'
    o += '<path d="M -140,-10 L -140,-46 C -140,-54 -132,-58 -120,-58 L -60,-60 L -36,-96 C -32,-102 -26,-104 -18,-104 L 50,-104 C 60,-104 66,-100 70,-92 L 86,-60 L 128,-56 C 140,-54 146,-46 146,-36 L 146,-10 Z" fill="#f2f0f4"/>'
    o += '<path d="M -140,-36 L 146,-36 L 146,-22 L -140,-22 Z" fill="#1e2a5a"/><path d="M -140,-22 L 146,-22 L 146,-18 L -140,-18 Z" fill="#c8323c"/>'
    o += '<path d="M -30,-94 L -10,-94 L -10,-62 L -52,-62 Z" fill="#3a4a6a"/><path d="M -2,-94 L 46,-94 C 52,-94 56,-90 58,-86 L 70,-62 L -2,-62 Z" fill="#3a4a6a"/><path d="M 6,-90 L 30,-90 L 18,-66 L 0,-66 Z" fill="#8a9ac8" opacity=".5"/>'
    o += '<rect x="-30" y="-112" width="70" height="8" rx="3" fill="#2a2a34"/><rect x="-28" y="-112" width="32" height="7" rx="3" fill="#e5484d"/><rect x="6" y="-112" width="32" height="7" rx="3" fill="#3a6aff"/>'
    o += '<text x="40" y="-42" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="11" font-weight="700" fill="#1e2a5a">ตำรวจ</text>'
    o += '<rect x="132" y="-50" width="12" height="8" rx="2" fill="#fff4dc"/><rect x="-140" y="-50" width="8" height="8" rx="2" fill="#c83a3a"/>'
    for wx in (-92, 92):
        o += f'<circle cx="{wx}" cy="-8" r="22" fill="#1a1a20"/><circle cx="{wx}" cy="-8" r="11" fill="#a8a8b4"/><circle cx="{wx}" cy="-8" r="4" fill="#5a5a66"/>'
    o += '<path d="M -120,-10 L -64,-10 C -66,-30 -84,-36 -92,-36 C -102,-36 -118,-30 -120,-10 Z M 64,-10 L 120,-10 C 118,-30 102,-36 92,-36 C 84,-36 66,-30 64,-10 Z" fill="#d8d6dc" opacity=".0"/>'
    return o + '</g>'
def police_bg3():
    o = day_sky("#5a6aa0", "#a8a8d0", "#efd8e2", "psky3")
    o += cumulus(-40, 170, 230, 56, 31, .85, "#fbf2f6", "#e2d6ea", "#a89ac8") + cumulus(260, 120, 260, 60, 32, .8, "#fbf2f6", "#e2d6ea", "#a89ac8") + cumulus(140, 290, 160, 32, 33, .6, "#fbf2f6", "#e2d6ea", "#a89ac8")
    o += '<g transform="translate(330,40) scale(.5)">' + bell_tower_old() + '</g>'
    # sisters' dorm building (clean, simple, light-grey windows) behind the lawn
    o += '<rect x="-10" y="330" width="330" height="230" fill="#e2dee8"/><path d="M -20,330 L 330,330 L 300,296 L 10,296 Z" fill="#7a7290"/><rect x="-10" y="440" width="330" height="8" fill="#f2eef6"/>'
    o += "".join(f'<rect x="{x}" y="{y}" width="34" height="56" fill="#b8b6c4"/><path d="M {x},{y} L {x + 34},{y}" stroke="#f6f2f8" stroke-width="3"/><path d="M {x + 17},{y} L {x + 17},{y + 56}" stroke="#a6a2b4" stroke-width="2"/>' for x in range(14, 300, 58) for y in (360, 470))
    o += "".join(clump(x, 556, r, "#5e8a5a", "#4c7650", "#3c6044") for x, r in ((340, 40), (380, 34), (520, 46)))
    o += '<path d="M 0,556 L 540,556 L 540,612 L 0,612 Z" fill="#7a9a6a"/>'
    # road in front with a kerb, the police car parked on it, light from the siren washing the road
    o += '<path d="M 0,612 L 540,612 L 540,622 L 0,622 Z" fill="#d8d2dc"/><path d="M 0,622 L 540,622 L 540,720 L 0,720 Z" fill="#5a5666"/><path d="M 30,672 L 100,672 M 170,672 L 240,672 M 310,672 L 380,672 M 450,672 L 520,672" stroke="#e8e2ea" stroke-width="3"/>'
    o += police_car(150, 700, .9)
    o += '<polygon points="120,620 200,620 320,720 40,720" fill="#3a6aff" opacity=".12" filter="url(#lhaze)"/><polygon points="60,620 130,620 150,720 -40,720" fill="#e5484d" opacity=".1" filter="url(#lhaze)"/>'
    # paved court where everyone stands, tape across it
    o += '<path d="M 0,720 L 540,720 L 540,960 L 0,960 Z" fill="#8a8494"/>' + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#76707e" stroke-width="1.4"/>' for y in (750, 800, 870, 950))
    o += '<path d="M 0,736 L 540,756" stroke="#e8c84a" stroke-width="7"/><path d="M 0,736 L 540,756" stroke="#1a1a20" stroke-width="7" stroke-dasharray="18 18"/>' + "".join(f'<rect x="{x}" y="{728 + x * .037:.0f}" width="5" height="50" fill="#e8e0d0"/>' for x in (16, 270, 520))
    # a second officer by the car with a radio
    return o
_pol = ("".join(C("mariam", x, 760, .5) if False else f'<g transform="translate({x},560) scale(.5)"><use href="#{P["nunx"]}"/></g>' for x in (380, 440, 490))
        + C("thana", 300, 905, 1.05) + C("cat", 110, 905, .9) + C("mek", 470, 912, .9))
ST["police"] = police_bg3() + _pol
L("police", .18, holes=((270, 600, 280),), glows=((150, 600, 220, SIREN, .6),), motes=None)
GLOWCOLS.add(SIREN)

# ------------------------------------------------------------------ 13. ENDING CHOICE: horror-game choice screen (animated in the player)
INS2["question"] = (
    '<rect width="540" height="960" fill="#0c0a12"/><radialGradient id="qv" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#2a1e3a"/><stop offset="1" stop-color="#05040a"/></radialGradient><rect width="540" height="960" fill="url(#qv)"/>'
    + "".join(f'<path d="M 0,{y} L 540,{y}" stroke="#ffffff" stroke-opacity=".025" stroke-width="1"/>' for y in range(0, 960, 4))   # faint scanlines
    + '<g transform="translate(270,200)"><path d="M -18,0 C -10,-10 10,-10 18,0 C 10,10 -10,10 -18,0 Z" fill="none" stroke="#b18cff" stroke-width="2"/><circle r="4.6" fill="#b18cff"/></g>'
    + '<text x="270" y="270" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" font-weight="500" fill="#a89cc8" letter-spacing="3">คุณคิดว่า…</text>'
    + '<text x="270" y="318" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="32" font-weight="700" fill="#ffffff">ป้าแดงตกเอง หรือถูกผลัก?</text>'
    + '<g id="optA"><rect id="optAbox" x="70" y="380" width="400" height="86" rx="12" fill="#1a1426" stroke="#6a5a9a" stroke-width="2"/><rect id="optAglow" x="66" y="376" width="408" height="94" rx="15" fill="none" stroke="#c9a8ff" stroke-width="3" opacity="0" filter="url(#lsoft)"/>'
    + '<text x="112" y="435" font-family="Inter, sans-serif" font-size="26" font-weight="700" fill="#c9a8ff">A</text><text x="150" y="434" font-family="IBM Plex Sans Thai, sans-serif" font-size="26" font-weight="700" fill="#f2eef8">ตกลงมาเอง</text><path id="optAarrow" d="M 86,413 L 98,423 L 86,433 Z" fill="#ffffff" opacity="0"/></g>'
    + '<g id="optB"><rect id="optBbox" x="70" y="490" width="400" height="86" rx="12" fill="#1a1426" stroke="#6a5a9a" stroke-width="2"/><rect id="optBglow" x="66" y="486" width="408" height="94" rx="15" fill="none" stroke="#c9a8ff" stroke-width="3" opacity="0" filter="url(#lsoft)"/>'
    + '<text x="112" y="545" font-family="Inter, sans-serif" font-size="26" font-weight="700" fill="#c9a8ff">B</text><text x="150" y="544" font-family="IBM Plex Sans Thai, sans-serif" font-size="26" font-weight="700" fill="#f2eef8">มีคนผลัก</text><path id="optBarrow" d="M 86,523 L 98,533 L 86,543 Z" fill="#ffffff" opacity="0"/></g>'
    + '<text id="qCta" x="270" y="636" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" font-weight="500" fill="#d8d0ec">เลือกคำตอบในคอมเมนต์ · A หรือ B</text>'
    + '<text x="270" y="900" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#8a80a8">ตอนต่อไป · EP2 ห้องสารภาพบาป</text>'
)

# ------------------------------------------------------------------ 14. CEMETERY: Mek next to Rosa, nobody standing on a grave
_cbg = cemetery_bg() if False else None
ST["cemetery"] = ST["cemetery"].replace(C("mek", 400, 790, .88), C("mek", 330, 792, .88))
_cw = ST["cemetery_wide"]
_r_old, _m_old = C("rosa", 380, 700, .6), C("mek_back", 250, 960, 1.05)
assert _r_old in _cw and _m_old in _cw
_cw = _cw.replace(_r_old, "").replace(_m_old, "")
_g3 = child_graves3()
_ins = _cw.index(_g3) + len(_g3) if _g3 in _cw else None
_pair = C("rosa_point", 352, 952, .9) + C("mek_back", 236, 958, .96)   # both in front of the first row of stones, on the grass, side by side
ST["cemetery_wide"] = (_cw[:_ins] + _pair + _cw[_ins:]) if _ins else _cw + _pair

# ------------------------------------------------------------------ 15. THE FIGURE IN THE BELFRY (shots 254-255): a black shape
# beside the bell that slides away into the dark. Hidden by default; the player fades it in, holds, then slides it off.
SHADE = ('<clipPath id="belfryClip"><path d="M 207,430 L 207,320 Q 270,240 333,320 L 333,430 Z"/></clipPath>'
         '<g id="towerShade" opacity="0"><g clip-path="url(#belfryClip)">'
         '<ellipse cx="300" cy="372" rx="56" ry="74" fill="#3a3460" opacity=".55" filter="url(#lsoft)"/>'   # faint light behind it, so the black reads
         '<g id="towerShadeFig"><path d="M 300,332 C 300,316 324,314 326,330 C 328,342 326,350 324,356 C 338,362 346,378 350,404 L 352,440 L 288,440 L 290,404 C 292,380 300,364 312,356 C 304,350 300,342 300,332 Z" fill="#040307"/>'
         '<path d="M 300,332 C 300,316 312,314 318,318 M 312,356 C 300,364 292,380 290,404" stroke="#a8a4d8" stroke-width="1.2" fill="none" opacity=".55"/></g>'
         '</g></g>')
_bt = bell_tower_old(swing=4)
assert _bt in ST["tower_night"]
ST["tower_night"] = ST["tower_night"].replace(_bt, _bt + SHADE, 1)

# ------------------------------------------------------------------ 16. CLUE CARD before the question (shot 305): the three things Mek knows
def _clue(y, num, th, sub):
    return (f'<g transform="translate(70,{y})"><rect width="400" height="96" rx="12" fill="#1a1426" stroke="#6a5a9a" stroke-width="2"/>'
            f'<circle cx="44" cy="48" r="22" fill="#2a2040" stroke="#c9a8ff" stroke-width="2"/><text x="44" y="57" text-anchor="middle" font-family="Inter, sans-serif" font-size="22" font-weight="700" fill="#c9a8ff">{num}</text>'
            f'<text x="86" y="44" font-family="IBM Plex Sans Thai, sans-serif" font-size="20" font-weight="700" fill="#f2eef8">{th}</text>'
            f'<text x="86" y="72" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#a89cc8">{sub}</text></g>')
INS2["clues"] = ('<rect width="540" height="960" fill="#0c0a12"/><radialGradient id="cv" cx="50%" cy="40%" r="70%"><stop offset="0" stop-color="#2a1e3a"/><stop offset="1" stop-color="#05040a"/></radialGradient><rect width="540" height="960" fill="url(#cv)"/>'
    + '<text x="270" y="190" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="16" fill="#a89cc8" letter-spacing="3">เบาะแสที่เมฆมี</text>'
    + '<g id="clue1">' + _clue(230, 1, "แฝดแยกกันได้ตอนจับช้อน", "มาเรียมถนัดขวา · มาร์ธาถนัดซ้าย") + '</g>'
    + '<g id="clue2">' + _clue(346, 2, "อักเนสใช้มือซ้ายทุกครั้ง", "รินชา ป้อนยา หยิบตุ๊กตา") + '</g>'
    + '<g id="clue3">' + _clue(462, 3, "ผ้าเช็ดหน้า \"Martha\" ผืนใหม่", "อยู่ในมือป้าแดงตอนตาย ไม่มีรอยไหม้") + '</g>')

# ------------------------------------------------------------------ 17. HOOK BOARD (shots 301-303): the seven rules on an old wooden board,
# nailed to the plaster, lit by a torch; one rule lights up at a time. Fills the frame (user: open straight on the board).
HOOK_RULES = ["ถ้าระฆังดังตอนตีสาม ห้ามออกจากห้อง", "ได้ยินเสียงเคาะห้องสารภาพบาป อย่าเปิดม่าน", "ห้ามเข้าปีกเก่าหลังสามทุ่ม",
              "ห้ามจุดเทียนในหอเด็ก", "ก่อนนอน ต้องขานชื่อตัวเองดัง ๆ", "นับซิสเตอร์ได้สิบสาม อย่าทัก", "ห้ามเอ่ยชื่อ “มาร์ธา” เด็ดขาด"]
def hook_board(hl=None):
    r = _rr.Random(17)
    o = '<rect width="540" height="960" fill="#2a2330"/>'
    o += "".join(f'<rect x="{x}" y="0" width="{w}" height="960" fill="#2f2836" opacity=".8"/>' for x, w in ((0, 40), (500, 40)))
    o += '<path d="M 60,0 C 70,200 40,420 64,960" stroke="#3a3242" stroke-width="30" fill="none" opacity=".35"/>'   # damp streak on the plaster
    ly = 260 + (hl if hl is not None else 3) * 66
    o += f'<ellipse cx="270" cy="{ly}" rx="330" ry="260" fill="url(#lg_fff0dc)" opacity=".55" style="mix-blend-mode:screen"/>'   # torch pool on the wall
    GLOWCOLS.add("#fff0dc")
    # the board: horizontal planks, grain, dark frame, four nails
    o += '<rect x="44" y="96" width="452" height="752" rx="6" fill="#24170f"/><rect x="58" y="110" width="424" height="724" fill="#5a3e2c"/>'
    for k in range(9):
        y = 110 + k * 80.4
        o += f'<rect x="58" y="{y:.0f}" width="424" height="80" fill="{("#5a3e2c", "#523826", "#5e422e")[k % 3]}"/><path d="M 58,{y:.0f} L 482,{y:.0f}" stroke="#3a2618" stroke-width="2"/>'
        o += "".join(f'<path d="M {r.uniform(60, 300):.0f},{y + r.uniform(10, 70):.0f} c 40,{r.uniform(-4, 4):.0f} 80,{r.uniform(-4, 4):.0f} {r.uniform(90, 160):.0f},{r.uniform(-3, 3):.0f}" stroke="#4a3020" stroke-width="1" fill="none" opacity=".7"/>' for _ in range(3))
    o += "".join(f'<circle cx="{x}" cy="{y}" r="6" fill="#1a120c"/><circle cx="{x - 1.5}" cy="{y - 1.5}" r="2" fill="#8a7a6a"/>' for x, y in ((76, 128), (464, 128), (76, 816), (464, 816)))
    o += "".join(f'<path d="M {x},{y} l {r.uniform(20, 60):.0f},{r.uniform(-8, 8):.0f}" stroke="#c8b08a" stroke-width=".8" opacity=".35"/>' for x, y in ((120, 700), (300, 180), (380, 560), (150, 430)))   # scratches
    o += '<text x="270" y="182" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="34" font-weight="700" fill="#efe0c0">กฎเจ็ดข้อ</text>'
    o += '<text x="270" y="216" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#cdb894" letter-spacing="2">คอนแวนต์เซนต์เวโรนิกา</text>'
    o += '<path d="M 140,232 L 400,232" stroke="#c8a878" stroke-width="1.2" opacity=".6"/>'
    for i, t in enumerate(HOOK_RULES):
        y = 260 + i * 66; on = hl == i; dim = hl is not None and not on
        col = "#fff3cf" if on else ("#9c8a6c" if dim else "#e6d4b2")
        if i == 6: col = "#ff9a8a" if on else ("#9a5a50" if dim else "#d8786a")   # rule 7 painted over in red, a little crooked
        if on: o += f'<rect x="70" y="{y - 30}" width="400" height="52" rx="10" fill="#ffe2a0" opacity=".16" filter="url(#lsoft)"/>'
        tr = ' transform="rotate(-1.5 270 ' + str(y) + ')"' if i == 6 else ""
        o += f'<g{tr}><circle cx="96" cy="{y - 6}" r="17" fill="none" stroke="{col}" stroke-width="2"/><text x="96" y="{y + 1}" text-anchor="middle" font-family="Inter, sans-serif" font-size="18" font-weight="700" fill="{col}">{i + 1}</text>'
        o += f'<text x="126" y="{y + 1}" font-family="IBM Plex Sans Thai, sans-serif" font-size="{19 if len(t) > 30 else 20}" font-weight="{700 if on or i == 6 else 500}" fill="{col}">{t}</text></g>'
    o += '<path d="M 300,720 c 2,20 -2,40 1,60" stroke="#6a2a22" stroke-width="3" fill="none" opacity=".7"/>'   # a drip from the red paint
    return o
INS2["rules_all"], INS2["rules_h1"], INS2["rules_h7"] = hook_board(None), hook_board(0), hook_board(6)
