#!/usr/bin/env python3
"""EP1 storyboard: every scene, key panels (9:16) + the full shot list under each panel.
Panels are crops of a per-scene 'stage' (one composed set with full-body characters), so the
camera framing (wide / medium / close) is just a different viewBox on the same stage.
Run: python3 storyboard.py -> storyboard.html"""
import os, re, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    so = sys.stdout; sys.stdout = open(os.devnull, "w")
    try: spec.loader.exec_module(m)
    finally: sys.stdout = so
    return m
v2 = load("v2", os.path.join(HERE, "scenes_v2.py"))      # posed(), put(), church(), fence(), frangipani(), pigeon()
v1 = load("v1", os.path.join(HERE, "scenes.py"))         # old_wing(), bell_tower(), stained_glass(), rules_board(), cross(), CAT, JAMES_DEFS
cf = v2.cf
posed, put, church, fence, frangipani, pigeon = v2.posed, v2.put, v2.church, v2.fence, v2.frangipani, v2.pigeon
old_wing, stained_glass, rules_board, cross = v1.old_wing, v1.stained_glass, v1.rules_board, v1.cross

# ---------- James full body (not in the cast rig yet) ----------
J_SKIN = ("#fbe7d8", "#efc7b0")
james = cf.figure("james", "",
    cf.leg("james", -1, ("#3a3d48", "#4a4e5c", "#2a2c36"), "#2a2a30") + cf.leg("james", 1, ("#3a3d48", "#4a4e5c", "#2a2c36"), "#22222a"),
    cf.torso_basic(("#2b3768", "#3d4b8a", "#1d2550")) + '<rect x="-14" y="96" width="28" height="12" rx="3" fill="#9fb0ff"/>',
    cf.arm("james", -1, ("#2b3768", "#3d4b8a", "#1d2550"), J_SKIN, short=True) + cf.arm("james", 1, ("#2b3768", "#3d4b8a", "#1d2550"), J_SKIN, short=True),
    '<g transform="translate(0,9) scale(.82)"><use href="#jhead"/></g>')
cf.F["james"] = james

# ---------- poses used in the boards ----------
P = {}
def pose(key, cid, **kw): P[key] = posed(cid, "sb_" + key, **kw)
pose("rosa", "rosa"); pose("rosa_pray", "rosa", aL=-40, aR=40); pose("rosa_point", "rosa", aR=-100)
pose("mek", "mek"); pose("mek_phone", "mek", aL=-30, aR=34); pose("mek_reach", "mek", aR=-70); pose("mek_torch", "mek", aL=-62, head=6)
pose("james", "james"); pose("james_turn", "james", aL=20, aR=-24)
pose("daeng", "daeng"); pose("daeng_hug", "daeng", aL=10, aR=-38); pose("daeng_whisper", "daeng", aL=-20, aR=-40)
pose("cat", "cat"); pose("cat_point", "cat", aR=-118)
pose("jos", "jos"); pose("jos_key", "jos", aR=-58); pose("jos_pray", "jos", aL=-40, aR=40)
pose("mariam", "mariam"); pose("mariam_piano", "mariam", aL=-30, aR=30)
pose("agnes", "agnes"); pose("agnes_tray", "agnes", aL=-40, aR=40); pose("agnes_left", "agnes", aR=-40)
pose("agnes_candle", "agnes", aR=-20, extraR='<g transform="translate(50,206)"><rect x="-2.5" y="-22" width="5" height="22" fill="#efe8da"/><path d="M 0,-33 C -3.5,-28 -3.5,-25 0,-23 C 3.5,-25 3.5,-28 0,-33 Z" fill="#fff6e6"/></g>')
pose("luc", "luc"); pose("thana", "thana"); pose("thana_bag", "thana", aR=-60)
for k in ("mkid", "jan", "twinM", "twinA"): pose(k, k)

def kid(key, x, feet, k):
    y = feet - 300 * k
    return f'<ellipse cx="{x + 8}" cy="{feet + 2}" rx="{40 * k:.0f}" ry="{6 * k:.0f}" fill="#000" opacity=".35"/><g transform="translate({x},{y:.0f}) scale({k})"><use href="#{P[key]}"/></g>'
def C(key, x, feet, k, light=1.0):
    # Agnes always reads greyed-out and dim, as in the approved chapel frame
    if key.startswith("agnes"): return put(P[key], x, feet, k, min(light, .78), .5)
    return put(P[key], x, feet, k, light)

# ---------- set primitives (rough, readable in grey) ----------
def room(wall="#8a8494", floor="#5a5460", hz=640, ceil=None):
    s = f'<rect width="540" height="960" fill="{wall}"/><rect y="{hz}" width="540" height="{960 - hz}" fill="{floor}"/><rect y="{hz}" width="540" height="6" fill="#3a3640"/>'
    if ceil: s += f'<rect width="540" height="{ceil}" fill="#4a4652"/>'
    return s
def window(x, y, w, h, night=True, inner=""):
    sky = "#2a2f5e" if night else "#b8c4e0"
    return (f'<rect x="{x - 8}" y="{y - 8}" width="{w + 16}" height="{h + 16}" fill="#3a3030"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{sky}"/>{inner}'
            f'<path d="M {x + w / 2},{y} L {x + w / 2},{y + h} M {x},{y + h / 2} L {x + w},{y + h / 2}" stroke="#3a3030" stroke-width="6"/>')
def door(x, y, w, h, open_=False):
    return f'<rect x="{x - 6}" y="{y - 6}" width="{w + 12}" height="{h + 6}" fill="#3a2a26"/><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{"#141014" if open_ else "#5a4234"}"/>' + ("" if open_ else f'<circle cx="{x + w - 12}" cy="{y + h / 2}" r="4" fill="#c8b07a"/>')
def table(x, y, w, h=20, legs=120):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#6a4a3a"/><rect x="{x + 8}" y="{y + h}" width="10" height="{legs}" fill="#3a2820"/><rect x="{x + w - 18}" y="{y + h}" width="10" height="{legs}" fill="#3a2820"/>'
def bed(x, y, w=200):
    return f'<rect x="{x}" y="{y}" width="{w}" height="60" fill="#d8d2dc"/><rect x="{x}" y="{y + 60}" width="{w}" height="20" fill="#5a5060"/><rect x="{x - 10}" y="{y - 70}" width="10" height="150" fill="#2a2630"/><rect x="{x + w}" y="{y - 30}" width="10" height="110" fill="#2a2630"/><rect x="{x + 10}" y="{y - 14}" width="60" height="20" rx="6" fill="#f0eaf2"/>'
def note(x, y, txt, w=None):
    w = w or (len(txt) * 8 + 20)
    return f'<g><rect x="{x}" y="{y}" width="{w}" height="22" rx="4" fill="#fffbe6" stroke="#c8a040"/><text x="{x + 8}" y="{y + 15}" font-family="IBM Plex Sans Thai, sans-serif" font-size="12" fill="#5a4010">{txt}</text></g>'
def candle(x, y, glow=True):
    s = f'<rect x="{x - 3}" y="{y - 22}" width="6" height="22" fill="#efe8da"/><path d="M {x},{y - 34} C {x - 4},{y - 29} {x - 4},{y - 25} {x},{y - 23} C {x + 4},{y - 25} {x + 4},{y - 29} {x},{y - 34} Z" fill="#fff6e6"/>'
    return s + (f'<circle cx="{x}" cy="{y - 28}" r="40" fill="#fff4dc" opacity=".25"/>' if glow else "")

# ---------- stages ----------
ST = {}
ST["tower_fog"] = ('<rect width="540" height="960" fill="#3a3c52"/>' + v1.bell_tower(270, 300, 1.3) +
    '<rect y="700" width="540" height="260" fill="#2a2a36"/><rect y="560" width="540" height="240" fill="#9a9ab0" opacity=".35"/>' +
    "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{700 - y}" fill="#4a4c66" opacity=".7"/>' for x, y, w in ((0, 420, 60), (470, 380, 70))))
ST["rosa_room"] = (room("#6a6478", "#4a4452", 700) + window(40, 160, 220, 320, inner=old_wing(56, 300, .8, lit=6)) +
    '<path d="M 400,150 L 410,150 L 410,230 L 400,230 Z M 380,175 L 430,175 L 430,183 L 380,183 Z" fill="#2a2630"/>' + bed(300, 640) +
    '<rect x="270" y="620" width="30" height="80" fill="#5a4234"/><rect x="274" y="604" width="22" height="14" rx="2" fill="#2a2a30"/><text x="285" y="615" text-anchor="middle" font-size="8" fill="#9fdcff" font-family="monospace">03:00</text>' +
    C("rosa", 330, 900, 1.15))
ST["rosa_bed"] = (room("#6a6478", "#4a4452", 700) + window(40, 160, 220, 320) + bed(160, 640, 300) +
    '<rect x="120" y="620" width="30" height="80" fill="#5a4234"/><rect x="124" y="604" width="22" height="14" rx="2" fill="#2a2a30"/>' +
    C("rosa_pray", 300, 870, 1.0) + '<rect x="160" y="700" width="300" height="60" fill="#d8d2dc"/>')
ST["oldwing"] = ('<rect width="540" height="960" fill="#2a2f5e"/>' + old_wing(-60, 120, 2.6, lit=6) + '<rect y="700" width="540" height="260" fill="#1a1a24"/>')
ST["path_dawn"] = ('<rect width="540" height="960" fill="#7d8cab"/><rect x="140" y="180" width="260" height="260" fill="#3a3046"/><rect x="230" y="300" width="80" height="140" fill="#1c1622"/>'
    '<path d="M 0,440 L 540,440 L 540,960 L 0,960 Z" fill="#4a4c5e"/><path d="M 200,440 L 340,440 L 560,960 L -20,960 Z" fill="#5d6074"/>' +
    "".join(f'<ellipse cx="{x}" cy="{y}" rx="{5 * s}" ry="{9 * s}" fill="#1d2232"/>' for x, y, s in ((300, 900, 2.2), (250, 800, 1.9), (286, 712, 1.6), (252, 640, 1.35), (278, 580, 1.15), (256, 532, 1), (272, 494, .85))))
ST["refectory"] = (room("#8a8494", "#5a5460", 600) + window(60, 140, 120, 180, night=False) + window(360, 140, 120, 180, night=False) +
    C("cat", 270, 700, .7) + C("mariam", 120, 760, .78, .95) + C("rosa", 420, 760, .78) + C("daeng", 500, 720, .72) + C("agnes", 40, 740, .74, .9) +
    '<path d="M 20,700 L 520,700 L 540,760 L 0,760 Z" fill="#6a4a3a"/><rect x="0" y="760" width="540" height="24" fill="#3a2820"/>' +
    "".join(f'<ellipse cx="{x}" cy="722" rx="22" ry="6" fill="#e8e0d4"/>' for x in (80, 180, 270, 360, 460)))
ST["condo"] = ('<rect width="540" height="960" fill="#2a2648"/>' + window(40, 100, 220, 300, inner="".join(f'<rect x="{x}" y="{y}" width="{w}" height="{400 - y}" fill="#1a2250"/>' for x, y, w in ((50, 220, 40), (100, 170, 50), (170, 240, 36), (214, 140, 46)))) +
    '<rect x="300" y="160" width="200" height="8" fill="#9a86ff"/>' + C("james_turn", 400, 820, 1.0) +
    '<path d="M 300,560 C 300,520 490,520 490,560 L 494,760 L 296,760 Z" fill="#15132b" opacity=".0"/>' +
    '<path d="M 0,620 L 260,620 L 270,840 L 0,840 Z" fill="#3a3466"/>' + C("mek_phone", 130, 880, .95) +
    '<path d="M 0,760 L 280,760 L 290,960 L 0,960 Z" fill="#2a2648"/>' + f'<g transform="translate(40,330) scale(1.2)">{v1.CAT}</g>')
ST["gate"] = ('<rect width="540" height="960" fill="#9a8aae"/>' + church(300, 380, .72) + fence(520, 700) +
    '<rect x="232" y="580" width="36" height="46" rx="4" fill="#2a2420"/><path d="M 0,700 L 540,700 L 540,960 L 0,960 Z" fill="#8a8494"/>' +
    frangipani(60, 540, 1.1) + C("daeng_hug", 180, 640, .5, .8) + C("cat_point", 360, 900, .95) + C("mek", 140, 920, 1.0))
ST["guestroom"] = (room("#7a6e78", "#4a3e44", 640) + window(150, 110, 250, 330, night=False, inner=old_wing(170, 230, .9)) +
    '<rect x="400" y="470" width="140" height="130" fill="#d8d2dc"/><rect x="400" y="440" width="10" height="160" fill="#2a2630"/>' +
    C("jos_key", 160, 900, 1.0) + C("mek", 390, 910, 1.02) + '<g transform="translate(244,560)"><circle r="7" fill="none" stroke="#c9ad66" stroke-width="3"/><path d="M 5,4 L 20,18" stroke="#c9ad66" stroke-width="3"/></g>')
ST["cemetery"] = ('<rect width="540" height="960" fill="#8a7a9e"/>' + old_wing(270, 220, 1.0) + "".join(cross(x, 500, .5) for x in range(30, 540, 60)) +
    '<path d="M 0,520 L 540,520 L 540,960 L 0,960 Z" fill="#3a4034"/>' + C("rosa_point", 160, 760, .85) + C("mek", 400, 770, .88) +
    cross(130, 880, 1.4, "มาร์ธา") + cross(270, 900, 1.4, "นภา") + cross(410, 880, 1.4))
ST["music"] = (room("#6a5e6e", "#3e3440", 620) + door(380, 260, 120, 360, open_=True) + C("agnes_tray", 440, 620, .72, .8) +
    '<rect x="20" y="520" width="300" height="120" fill="#1c1418"/><rect x="20" y="500" width="300" height="24" fill="#2c2024"/><rect x="26" y="504" width="288" height="12" fill="#f1ece2"/>' +
    C("mariam_piano", 180, 840, .95) + '<rect x="20" y="640" width="300" height="200" fill="#1e1619"/>' +
    "".join(f'<rect x="{x}" y="504" width="6" height="8" fill="#141014"/>' for x in range(30, 314, 14)))
ST["veranda"] = ('<rect width="540" height="960" fill="#1e2244"/>' + old_wing(160, 240, .9) + '<rect y="480" width="540" height="480" fill="#2a2228"/>' +
    '<rect x="0" y="100" width="20" height="560" fill="#3a3034"/><rect x="520" y="100" width="20" height="560" fill="#3a3034"/>' +
    C("jos", 140, 860, .95, .9) + C("mek", 400, 870, .97, .9) +
    '<path d="M 40,640 L 500,640 L 520,680 L 20,680 Z" fill="#5a4234"/>' + candle(270, 636) + '<rect x="256" y="580" width="28" height="60" fill="none" stroke="#3a3030" stroke-width="3"/>')
ST["dawn_walk"] = ('<rect width="540" height="960" fill="#7d8cab"/><rect y="240" width="540" height="320" fill="#4a4a62"/>' +
    "".join(f'<rect x="{x}" y="300" width="50" height="70" fill="#2a2a40"/>' for x in (30, 130, 230, 330, 430)) +
    '<path d="M 0,560 L 540,560 L 540,960 L 0,960 Z" fill="#5a5c6e"/>' + C("agnes", 380, 900, .95, .9) + C("mariam", 220, 920, 1.0, .95))
ST["mass"] = ('<rect width="540" height="960" fill="#5a5466"/>' + stained_glass(190, 120, 160, 260, bright=.9) +
    '<rect x="160" y="420" width="220" height="60" fill="#d8d2dc"/>' + C("jos", 270, 470, .5) +
    "".join(f'<g transform="translate({x},{y}) scale(.42)"><use href="#{P["mariam"]}"/></g>' for x, y in ((90, 520), (170, 520), (250, 520), (330, 520), (410, 520), (130, 560), (210, 560), (290, 560), (370, 560), (450, 560), (60, 560), (480, 520))) +
    '<rect y="760" width="540" height="200" fill="#2a1e22"/>' + C("mek", 270, 1040, 1.0, .85))
ST["garden"] = ('<rect width="540" height="960" fill="#5a6a5a"/><circle cx="120" cy="160" r="170" fill="#3e5a3e"/><circle cx="400" cy="120" r="190" fill="#34503a"/><rect x="250" y="180" width="30" height="420" fill="#3a3030"/>' +
    '<path d="M 0,560 L 540,560 L 540,960 L 0,960 Z" fill="#4a5a44"/>' + C("luc", 200, 860, .95) + C("agnes_left", 360, 860, .95, .95) + C("mek", 500, 900, .9))
ST["archive"] = ('<rect width="540" height="960" fill="#5a4a44"/><path d="M 0,0 L 540,0 L 540,240 L 270,60 L 0,240 Z" fill="#3a2a26"/><circle cx="270" cy="170" r="46" fill="#c8d0e8"/>' +
    "".join(f'<rect x="10" y="{y}" width="190" height="6" fill="#3a2820"/><rect x="340" y="{y}" width="190" height="6" fill="#3a2820"/>' for y in (380, 470, 560)) +
    "".join(f'<rect x="{x}" y="{y - 40}" width="34" height="40" fill="#a88a64"/>' for x in (20, 60, 100, 150, 350, 400, 450) for y in (380, 470, 560)) +
    '<rect y="700" width="540" height="260" fill="#3a2a24"/>' + C("mek_reach", 290, 880, 1.0) + table(140, 640, 330) +
    '<rect x="220" y="626" width="160" height="16" fill="#e8dfcc"/><polygon points="230,140 310,140 460,960 120,960" fill="#fff4dc" opacity=".12"/>')
ST["flash_dorm"] = ('<rect width="540" height="960" fill="#7a6e66"/>' + "".join(bed(x, 520, 130) for x in (20, 210, 400)) + '<rect y="660" width="540" height="300" fill="#5a4e46"/>' +
    kid("mkid", 120, 900, 1.1) + kid("jan", 230, 900, .9) + kid("twinM", 340, 890, 1.0) + kid("twinA", 450, 880, 1.0))
ST["steps"] = ('<rect width="540" height="960" fill="#4a4458"/><rect x="60" y="60" width="420" height="520" fill="#3a3440"/><rect x="200" y="200" width="140" height="380" fill="#1a1418"/>' +
    C("agnes_left", 270, 600, .95, .85) + '<rect y="600" width="540" height="100" fill="#5a5060"/><rect y="700" width="540" height="260" fill="#4a4250"/>' +
    '<g transform="translate(270,820) scale(1.8)"><path d="M -18,0 L 18,0 L 24,32 L -24,32 Z" fill="#e8e0d4"/><path d="M 4,0 L 18,0 L 24,32 L 8,32 Z" fill="#3a2a24"/><circle cx="0" cy="-12" r="14" fill="#f0d8c0"/><path d="M 2,-26 C 14,-24 16,-12 12,-2 L 4,-6 Z" fill="#2a1a16"/></g>' + C("mek", 470, 960, .8))
ST["kitchen"] = (room("#bab4aa", "#6a5a50", 640, 80) + '<rect y="420" width="540" height="24" fill="#8aa08a"/>' + window(400, 120, 110, 140) +
    '<rect x="20" y="200" width="200" height="8" fill="#5a4234"/><rect x="0" y="470" width="400" height="170" fill="#7a6a5a"/><rect x="0" y="470" width="400" height="22" fill="#e8e2d8"/>' +
    '<rect x="408" y="300" width="112" height="340" fill="#141014"/>' + C("agnes", 456, 640, .66, .8) +
    C("daeng_whisper", 250, 900, 1.0) + C("mek", 100, 940, .98) + '<path d="M 30,740 L 430,740 L 450,780 L 10,780 Z" fill="#7a5a44"/>' +
    '<path d="M 270,0 L 270,120" stroke="#1a1418" stroke-width="2"/><circle cx="270" cy="140" r="8" fill="#fff4e0"/>')
ST["call"] = ('<rect width="540" height="960" fill="#0e0c14"/><svg x="0" y="0" width="540" height="470" viewBox="0 0 540 470"><rect width="540" height="470" fill="#2a2648"/>' +
    put(P["james_turn"], 270, 600, 1.1) + f'<g transform="translate(190,-190) scale(1.1)">{v1.CAT}</g></svg><rect y="466" width="540" height="8" fill="#0e0c14"/>' +
    '<svg x="0" y="474" width="540" height="486" viewBox="0 0 540 486"><rect width="540" height="486" fill="#2a2430"/>' + put(P["mek_phone"], 200, 600, 1.1, .8) +
    '<g transform="translate(450,400)"><ellipse rx="34" ry="12" fill="#3a3a40"/><path d="M -24,0 L 24,0 M -18,-6 L 18,-6 M -18,6 L 18,6" stroke="#141418" stroke-width="3"/></g></svg>')
ST["dream"] = ('<rect width="540" height="960" fill="#6a6268"/><rect x="0" y="0" width="540" height="960" fill="#9a9aa0" opacity=".3"/><rect x="170" y="140" width="200" height="200" fill="#c8d0e8"/>' +
    '<rect x="160" y="130" width="220" height="10" fill="#3a3030"/>' + kid("twinA", 270, 520, .9) + '<rect y="640" width="540" height="320" fill="#4a4448"/><rect x="40" y="560" width="160" height="40" fill="#e8e2ea"/>' + kid("mkid", 120, 880, .9) +
    '<rect y="700" width="540" height="260" fill="#8a8890" opacity=".35"/>')
ST["tower_night"] = ('<rect width="540" height="960" fill="#1e2244"/><circle cx="430" cy="110" r="28" fill="#e8ecff"/>' + church(300, 690, 1.15, night=True) +
    '<path d="M 0,690 L 540,690 L 540,960 L 0,960 Z" fill="#2a2a36"/>' + C("mek_torch", 130, 900, 1.05, .85) +
    '<polygon points="206,646 222,638 520,850 470,940" fill="#fff4dc" opacity=".22"/>' +
    '<g transform="translate(380,862)"><path d="M -110,0 C -100,-18 70,-22 100,-6 L 102,14 C 50,22 -70,22 -110,12 Z" fill="#6c2b30"/><path d="M -40,-14 L 64,-16 L 68,14 L -38,16 Z" fill="#748894"/><ellipse cx="-124" cy="2" rx="18" ry="14" fill="#a9a4a6"/><path d="M -20,14 L -60,36 L -54,42 L -12,20 Z" fill="#c98f69"/><rect x="-74" y="36" width="10" height="7" fill="#fbf8f2"/></g>')
ST["police"] = ('<rect width="540" height="960" fill="#7d8cab"/>' + "".join(f'<g transform="translate({x},330) scale(.55)"><use href="#{P["mariam"]}"/></g>' for x in (60, 130, 410, 480)) +
    '<rect y="470" width="540" height="10" fill="#e8c84a"/><rect y="640" width="540" height="320" fill="#4a4a54"/>' + C("cat", 110, 900, .9) + C("thana", 300, 900, 1.05) + C("mek", 470, 910, .9))
ST["thana_night"] = (room("#3a3440", "#2a2430", 640) + '<rect x="0" y="560" width="540" height="20" fill="#5a4234"/>' + C("thana_bag", 170, 900, 1.0, .85) + C("mek", 390, 910, 1.0, .85) + '<circle cx="270" cy="120" r="10" fill="#fff4e0"/>')
ST["chapel_sisters"] = ('<rect width="540" height="960" fill="#1e1822"/>' + '<rect x="0" y="0" width="70" height="620" fill="#120f16"/><rect x="470" y="0" width="70" height="620" fill="#120f16"/>' +
    stained_glass(196, 40, 148, 230) + '<rect x="112" y="120" width="6" height="66" fill="#0d0b11"/><rect x="98" y="138" width="34" height="6" fill="#0d0b11"/>' +
    '<path d="M 0,470 L 150,486 L 150,560 L 0,560 Z" fill="#2c2026"/><rect x="414" y="510" width="124" height="90" fill="#2a1e1e"/>' + "".join(f'<rect x="{424 + i * 16}" y="{494 + (i % 2) * 4}" width="7" height="14" fill="#efe6d6"/>' for i in range(7)) +
    '<rect y="600" width="540" height="360" fill="#18131a"/>' + C("agnes_candle", 132, 760, 1.25) + C("mariam_piano", 384, 940, 1.6))
ST["chapel_night"] = ('<rect width="540" height="960" fill="#2a2630"/>' + stained_glass(330, 80, 150, 250, bright=.9) +
    "".join(f'<path d="M 0,{y} L 540,{y - 20} L 540,{y + 30} L 0,{y + 50} Z" fill="#3a2a2c"/>' for y in (500, 600, 700)) +
    C("mek", 250, 760, .7, .7) + '<path d="M -20,800 L 560,800 L 560,960 L -20,960 Z" fill="#0e0c10"/>' + candle(440, 790, glow=False) + '<polygon points="330,180 480,180 300,960 0,960" fill="#c8d4ff" opacity=".12"/>')



# ================= detailed exteriors: cemetery + garden (layered depth, haze, painted sky) =================
import random as _rr
RR = _rr.Random(7)
def sky(top, mid, low, clouds=()):
    o = f'<linearGradient id="sk{top[1:]}{low[1:]}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{top}"/><stop offset=".6" stop-color="{mid}"/><stop offset="1" stop-color="{low}"/></linearGradient>'
    o += f'<rect width="540" height="960" fill="url(#sk{top[1:]}{low[1:]})"/>'
    for (x, y, w, c, op) in clouds:
        o += f'<path d="M {x},{y} C {x + w * .2},{y - 10} {x + w * .5},{y - 14} {x + w * .7},{y - 6} C {x + w * .85},{y - 12} {x + w},{y - 4} {x + w},{y + 4} L {x},{y + 4} Z" fill="{c}" opacity="{op}"/>'
        o += f'<rect x="{x + w * .1:.0f}" y="{y + 3}" width="{w * .8:.0f}" height="3" rx="1.5" fill="{c}" opacity="{op * .7:.2f}"/>'
    return o
def haze(y, h, col, op):
    return f'<rect x="-20" y="{y}" width="580" height="{h}" fill="{col}" opacity="{op}" filter="url(#lhaze)"/>'
def clump(x, y, r, c1, c2, c3):
    return (f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r * .75:.0f}" fill="{c2}"/><ellipse cx="{x - r * .35:.0f}" cy="{y - r * .25:.0f}" rx="{r * .6:.0f}" ry="{r * .45:.0f}" fill="{c1}"/>'
            f'<ellipse cx="{x + r * .4:.0f}" cy="{y + r * .2:.0f}" rx="{r * .55:.0f}" ry="{r * .4:.0f}" fill="{c3}"/>')
def cypress(x, y, h, c1="#3e4a44", c2="#2c3632"):
    return f'<path d="M {x},{y - h} C {x + h * .16},{y - h * .7} {x + h * .14},{y - h * .2} {x + h * .1},{y} L {x - h * .1},{y} C {x - h * .14},{y - h * .2} {x - h * .16},{y - h * .7} {x},{y - h} Z" fill="{c2}"/><path d="M {x},{y - h} C {x - h * .16},{y - h * .7} {x - h * .14},{y - h * .2} {x - h * .1},{y} L {x},{y} Z" fill="{c1}"/>'
def headstone(x, y, k, kind, shade="#b8b2c0", lit="#dcd6e4", dark="#8a8494"):
    sh = f'<path d="M {x + 10 * k},{y} L {x + 60 * k},{y + 10 * k} L {x + 40 * k},{y + 14 * k} L {x - 6 * k},{y + 4 * k} Z" fill="#20182a" opacity=".35"/>'  # long shadow to the right
    if kind == "arch":
        g = f'<path d="M {x - 14 * k},{y} L {x - 14 * k},{y - 30 * k} C {x - 14 * k},{y - 46 * k} {x + 14 * k},{y - 46 * k} {x + 14 * k},{y - 30 * k} L {x + 14 * k},{y} Z" fill="{shade}"/><path d="M {x - 14 * k},{y} L {x - 14 * k},{y - 30 * k} C {x - 14 * k},{y - 40 * k} {x - 6 * k},{y - 44 * k} {x},{y - 45 * k} L {x - 2 * k},{y} Z" fill="{lit}"/><path d="M {x - 6 * k},{y - 26 * k} L {x + 6 * k},{y - 26 * k} M {x - 7 * k},{y - 18 * k} L {x + 7 * k},{y - 18 * k}" stroke="{dark}" stroke-width="{1.2 * k:.1f}"/>'
    elif kind == "cross":
        g = f'<rect x="{x - 3 * k}" y="{y - 50 * k}" width="{6 * k}" height="{50 * k}" fill="{shade}"/><rect x="{x - 14 * k}" y="{y - 38 * k}" width="{28 * k}" height="{6 * k}" fill="{shade}"/><rect x="{x - 3 * k}" y="{y - 50 * k}" width="{3 * k}" height="{50 * k}" fill="{lit}"/><rect x="{x - 10 * k}" y="{y - 2 * k}" width="{20 * k}" height="{6 * k}" fill="{dark}"/>'
    elif kind == "celtic":
        g = f'<rect x="{x - 3 * k}" y="{y - 56 * k}" width="{6 * k}" height="{56 * k}" fill="{shade}"/><rect x="{x - 15 * k}" y="{y - 44 * k}" width="{30 * k}" height="{6 * k}" fill="{shade}"/><circle cx="{x}" cy="{y - 41 * k}" r="{9 * k:.1f}" fill="none" stroke="{shade}" stroke-width="{3 * k:.1f}"/><rect x="{x - 3 * k}" y="{y - 56 * k}" width="{3 * k}" height="{56 * k}" fill="{lit}"/>'
    elif kind == "obelisk":
        g = f'<path d="M {x - 8 * k},{y} L {x - 5 * k},{y - 64 * k} L {x},{y - 72 * k} L {x + 5 * k},{y - 64 * k} L {x + 8 * k},{y} Z" fill="{shade}"/><path d="M {x - 8 * k},{y} L {x - 5 * k},{y - 64 * k} L {x},{y - 72 * k} L {x},{y} Z" fill="{lit}"/><rect x="{x - 12 * k}" y="{y - 4 * k}" width="{24 * k}" height="{6 * k}" fill="{dark}"/>'
    else:  # angel
        g = (f'<rect x="{x - 12 * k}" y="{y - 20 * k}" width="{24 * k}" height="{20 * k}" fill="{dark}"/><path d="M {x - 9 * k},{y - 20 * k} L {x - 6 * k},{y - 58 * k} L {x + 6 * k},{y - 58 * k} L {x + 9 * k},{y - 20 * k} Z" fill="{shade}"/>'
             f'<circle cx="{x}" cy="{y - 64 * k}" r="{6 * k:.1f}" fill="{lit}"/><path d="M {x - 5 * k},{y - 54 * k} C {x - 26 * k},{y - 66 * k} {x - 28 * k},{y - 40 * k} {x - 8 * k},{y - 34 * k} Z M {x + 5 * k},{y - 54 * k} C {x + 26 * k},{y - 66 * k} {x + 28 * k},{y - 40 * k} {x + 8 * k},{y - 34 * k} Z" fill="{lit}"/>'
             f'<path d="M {x - 4 * k},{y - 44 * k} L {x + 4 * k},{y - 44 * k} L {x + 2 * k},{y - 36 * k} L {x - 2 * k},{y - 36 * k} Z" fill="{dark}"/>')
    return sh + g
def lamppost(x, y, h, lit=True):
    o = f'<rect x="{x - 3}" y="{y - h}" width="6" height="{h}" fill="#2a2630"/><rect x="{x - 8}" y="{y - 6}" width="16" height="6" fill="#2a2630"/><path d="M {x - 12},{y - h} L {x + 12},{y - h} L {x + 8},{y - h - 26} L {x - 8},{y - h - 26} Z" fill="{"#fff1d6" if lit else "#4a4652"}"/><path d="M {x - 14},{y - h - 26} L {x + 14},{y - h - 26} L {x},{y - h - 38} Z" fill="#2a2630"/>'
    if lit:
        o += f'<circle cx="{x}" cy="{y - h - 13}" r="70" fill="url(#lg_fff0dc)" opacity=".7" style="mix-blend-mode:screen"/>'
        GLOWCOLS.add("#fff0dc") if "GLOWCOLS" in globals() else None
    return o
def tuft(x, y, k=1, c="#4e6a48"):
    return f'<path d="M {x},{y} l {-4 * k},{-14 * k} M {x + 3 * k},{y} l {1 * k},{-18 * k} M {x + 6 * k},{y} l {5 * k},{-13 * k} M {x - 3 * k},{y} l {-8 * k},{-9 * k}" stroke="{c}" stroke-width="{1.8 * k:.1f}" stroke-linecap="round"/>'
def flower5(x, y, k=1, c="#f6f0e6", ctr="#f2d880"):
    return f'<g transform="translate({x},{y}) scale({k})">' + "".join(f'<ellipse cx="0" cy="-3" rx="2.2" ry="3.6" fill="{c}" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288)) + f'<circle r="1.4" fill="{ctr}"/></g>'

# --- back view of Mek (he looks into the scene, like the reference) ---
mek_back_head = ('<g transform="translate(0,9) scale(.82)"><rect x="-8" y="16" width="16" height="40" fill="#d9a27e"/>'
                 '<ellipse cx="-31" cy="2" rx="5" ry="8" fill="#e2b393"/><ellipse cx="31" cy="2" rx="5" ry="8" fill="#c99272"/>'
                 '<path d="M -36,-6 C -42,-44 -24,-64 0,-65 C 24,-64 42,-44 36,-6 L 34,16 C 22,26 -22,26 -34,16 Z" fill="#1a1619"/>'
                 '<path d="M -30,-40 C -22,-56 -8,-62 4,-62 C -8,-56 -18,-48 -24,-34 Z" fill="#3a3238"/><path d="M -10,8 L -6,22 M 4,10 L 6,22 M 16,6 L 18,18" stroke="#2b2428" stroke-width="2"/></g>')
cf.F["mek_back"] = cf.figure("mek_back", "",
    cf.leg("mek_back", -1, ("#2e3448", "#3e4660", "#232838"), "#e8e4dc", "#8a8690") + cf.leg("mek_back", 1, ("#2e3448", "#3e4660", "#232838"), "#d4d0c8", "#7a7680"),
    cf.torso_basic(("#5d6f8a", "#7889a6", "#45546c"), hip=200) + '<path d="M -30,120 L 30,120 M 0,60 L 0,200" stroke="#45546c" stroke-width="2"/><path d="M -30,62 L 30,176" stroke="#2a2420" stroke-width="4"/>',
    cf.arm("mek_back", -1, ("#5d6f8a", "#7889a6", "#45546c"), ("#eec4a2", "#d9a27e")) + cf.arm("mek_back", 1, ("#5d6f8a", "#7889a6", "#45546c"), ("#eec4a2", "#d9a27e")),
    mek_back_head)
pose("mek_back", "mek_back")

def cemetery_bg():
    o = sky("#4a4478", "#9a86b4", "#e8b8b4", clouds=((20, 120, 160, "#f4d0c4", .55), (260, 90, 220, "#f8dcd0", .5), (360, 190, 150, "#f0c8c0", .45), (60, 230, 120, "#e8c0c0", .35)))
    # far: Bangkok towers, the church tower, tree line, all in lavender haze
    o += "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{420 - y}" fill="#8a7ea8" opacity=".55"/>' for x, y, w in ((0, 250, 46), (40, 290, 34), (470, 230, 60), (430, 300, 40)))
    o += f'<g opacity=".8">{church(330, 330, .5)}</g>'
    o += "".join(clump(x, 400, r, "#8a88a4", "#7a7896", "#6a6888") for x, r in ((40, 60), (130, 50), (220, 44), (430, 56), (520, 64)))
    o += haze(330, 120, "#c8b4d4", .55)
    # mid: lawn with mowing stripes in perspective
    o += '<path d="M 0,420 L 540,420 L 540,960 L 0,960 Z" fill="#5a6e5a"/>'
    for i in range(-6, 8):
        x0 = 270 + i * 40; x1 = 270 + i * 260
        o += f'<path d="M {x0},420 L {x0 + 40},420 L {x1 + 260},960 L {x1},960 Z" fill="{"#647a62" if i % 2 else "#566a54"}"/>'
    o += haze(410, 70, "#c8b4d4", .45)
    # rows of graves receding (back rows small and hazy, front rows bigger)
    kinds = ("arch", "cross", "celtic", "arch", "obelisk", "cross", "angel")
    for row, (yy, k, op) in enumerate(((450, .42, .6), (500, .58, .75), (565, .78, .9))):
        for j in range(9):
            x = 20 + j * 64 + (row % 2) * 28 + RR.uniform(-6, 6)
            if 190 < x < 350 and row == 2: continue   # keep the path clear
            o += f'<g opacity="{op}">{headstone(x, yy + RR.uniform(-4, 4), k, kinds[(j + row) % 7])}</g>'
            if RR.random() < .4: o += flower5(x + 8 * k, yy + 2, k * .9, "#e8d8f0")
    o += cypress(70, 540, 150) + cypress(470, 530, 170) + cypress(505, 520, 120, "#465248", "#323c36")
    o += haze(470, 60, "#d4c0dc", .25)
    # worn grass-and-earth trail instead of paving
    o += '<path d="M 262,560 C 250,640 300,700 268,780 C 240,850 300,900 290,960 L 230,960 C 236,900 190,850 220,780 C 250,700 220,640 248,560 Z" fill="#7a6a54" opacity=".55"/>'
    o += '<path d="M 262,560 C 250,640 300,700 268,780 C 240,850 300,900 290,960" stroke="#5a7050" stroke-width="6" fill="none" opacity=".6"/>' 
    # family plot with a little iron railing, lamp post lit at dusk, wreath on the cross
    o += '<g opacity=".95">' + "".join(f'<rect x="{x}" y="560" width="2.5" height="22" fill="#2a2630"/>' for x in range(372, 452, 8)) + '<rect x="370" y="562" width="84" height="2.5" fill="#2a2630"/><rect x="370" y="574" width="84" height="2" fill="#2a2630"/></g>'
    o += lamppost(170, 640, 190)
    # wilted wreath on a stand and jars with candles
    o += '<g transform="translate(450,640)"><path d="M -12,30 L 0,0 L 12,30" stroke="#3a3030" stroke-width="2.4" fill="none"/><circle cx="0" cy="-6" r="16" fill="none" stroke="#5a6a4e" stroke-width="7"/>' + "".join(f'<circle cx="{16 * __import__("math").cos(a / 3):.1f}" cy="{-6 + 16 * __import__("math").sin(a / 3):.1f}" r="2.6" fill="#e8d8e0"/>' for a in range(0, 19, 2)) + '<path d="M -4,6 l -4,14 M 4,6 l 5,14" stroke="#8a4a5a" stroke-width="3"/></g>'
    # foreground: tall grass tufts, fallen frangipani, a big out-of-focus iron gate post at the left edge
    o += "".join(tuft(RR.uniform(0, 540), RR.uniform(700, 950), RR.uniform(1, 1.8)) for _ in range(30))
    o += "".join(flower5(RR.uniform(20, 520), RR.uniform(720, 940), RR.uniform(1.1, 1.7)) for _ in range(10))
    return o

def child_graves():
    o = cross(130, 880, 1.4, "มาร์ธา") + cross(270, 900, 1.4, "นภา") + cross(410, 880, 1.4)
    # small offerings: teddy bear, toy car, a hair ribbon, glass candle jars
    o += '<g transform="translate(160,900)"><circle cx="0" cy="-10" r="9" fill="#a88a6a"/><circle cx="-6" cy="-18" r="3.5" fill="#a88a6a"/><circle cx="6" cy="-18" r="3.5" fill="#a88a6a"/><ellipse cx="0" cy="4" rx="11" ry="9" fill="#9a7a5a"/><circle cx="-3" cy="-11" r="1" fill="#1a1216"/><circle cx="3" cy="-11" r="1" fill="#1a1216"/></g>'
    o += '<g transform="translate(300,918)"><rect x="-12" y="-8" width="24" height="9" rx="3" fill="#5a7aa8"/><rect x="-7" y="-14" width="14" height="7" rx="2" fill="#7a9ac8"/><circle cx="-7" cy="2" r="3.5" fill="#2a2a30"/><circle cx="7" cy="2" r="3.5" fill="#2a2a30"/></g>'
    for (x, y) in ((100, 900), (240, 918), (382, 900), (440, 902)):
        o += f'<rect x="{x - 5}" y="{y - 12}" width="10" height="13" rx="2" fill="#c8d0e0" opacity=".7"/><rect x="{x - 2}" y="{y - 10}" width="4" height="7" fill="#efe8da"/><circle cx="{x}" cy="{y - 13}" r="10" fill="url(#lg_ffe6c4)" opacity=".8" style="mix-blend-mode:screen"/>'
    o += '<path d="M 412,904 c 6,-4 10,0 6,4 c 6,2 4,8 -2,6 l -2,10 l -2,-10 c -6,2 -8,-4 -2,-6 c -4,-4 0,-8 6,-4 Z" fill="#f2eee8"/>'  # white ribbon on the nameless grave
    return o

ST["cemetery"] = cemetery_bg() + C("rosa_point", 160, 780, .85) + C("mek", 400, 790, .88) + child_graves()
ST["cemetery_wide"] = cemetery_bg() + child_graves() + C("rosa", 380, 700, .6) + C("mek_back", 250, 960, 1.05)

def garden_bg():
    o = sky("#9ab0d4", "#d8dce8", "#f2e8e0", clouds=((40, 90, 180, "#ffffff", .6), (300, 60, 200, "#ffffff", .5)))
    # far: white cloister arcade + church tower in morning haze
    o += f'<g opacity=".85">{church(410, 300, .48)}</g>'
    o += '<rect x="-10" y="300" width="560" height="150" fill="#e4e0e8"/><rect x="-10" y="300" width="560" height="12" fill="#f4f0f6"/>'
    o += "".join(f'<path d="M {x},450 L {x},350 Q {x + 22},322 {x + 44},350 L {x + 44},450 Z" fill="#8a8698"/><rect x="{x + 44}" y="330" width="10" height="120" fill="#f0ecf2"/>' for x in range(-6, 560, 56))
    o += "".join(f'<rect x="{x}" y="372" width="10" height="34" fill="#f6f2ea"/>' for x in (24, 30, 140, 146, 152))   # habits drying on a line inside the arcade
    o += '<path d="M 10,370 Q 90,380 170,368" stroke="#5a5660" stroke-width="1" fill="none"/>'
    o += haze(290, 170, "#e8e4f0", .45)
    # lawn + brick paths
    o += '<path d="M 0,450 L 540,450 L 540,960 L 0,960 Z" fill="#5e7a58"/>'
    for i in range(-5, 7):
        x0 = 270 + i * 46; x1 = 270 + i * 220
        o += f'<path d="M {x0},450 L {x0 + 46},450 L {x1 + 220},960 L {x1},960 Z" fill="{"#68845e" if i % 2 else "#5a7454"}"/>'
    o += '<path d="M 230,450 L 310,450 L 420,960 L 120,960 Z" fill="#a88a7a"/>' + "".join(f'<path d="M {230 - (y - 450) * .21:.0f},{y} L {310 + (y - 450) * .21:.0f},{y}" stroke="#8a6e60" stroke-width="1.6"/>' for y in range(470, 960, 26))
    # flower beds, bougainvillea on the arcade, Mary statue, birdbath, bench, watering can, pots
    o += "".join(clump(x, 470, r, "#c88aa8", "#a86a88", "#8a5a74") for x, r in ((70, 40), (480, 44)))
    o += "".join(clump(x, 520, 30, "#5e8a58", "#4e7448", "#3e5e3a") + "".join(f'<circle cx="{x + RR.uniform(-22, 22):.0f}" cy="{520 + RR.uniform(-16, 8):.0f}" r="3.4" fill="{c}"/>' for c in ("#e88a8a", "#f4d080", "#e8e0f0", "#e88a8a")) for x in (40, 120, 430, 510))
    o += '<g transform="translate(470,600)"><rect x="-14" y="-6" width="28" height="40" fill="#d8d4dc"/><path d="M -9,-6 L -7,-58 L 7,-58 L 9,-6 Z" fill="#f2eef4"/><circle cx="0" cy="-64" r="7" fill="#f2eef4"/><path d="M -10,-62 C -10,-74 10,-74 10,-62 L 12,-30 L -12,-30 Z" fill="#9aaad8" opacity=".9"/><circle cx="0" cy="-70" r="11" fill="none" stroke="#e8d890" stroke-width="1.4" opacity=".8"/></g>'
    o += '<g transform="translate(90,640)"><path d="M -24,0 C -24,-10 24,-10 24,0 C 24,6 -24,6 -24,0 Z" fill="#c8c4cc"/><ellipse cx="0" cy="-3" rx="20" ry="4" fill="#8aa0c8"/><rect x="-5" y="0" width="10" height="34" fill="#b8b4bc"/><rect x="-12" y="34" width="24" height="5" fill="#a8a4ac"/>' + pigeon(10, -12, .55) + '</g>'
    o += '<g transform="translate(400,690)"><rect x="-56" y="-26" width="112" height="7" fill="#e4e0e8"/><rect x="-56" y="-14" width="112" height="7" fill="#d8d4dc"/><rect x="-50" y="-7" width="8" height="26" fill="#b8b4bc"/><rect x="42" y="-7" width="8" height="26" fill="#b8b4bc"/></g>'
    o += '<g transform="translate(340,740)"><path d="M -12,0 L 12,0 L 10,-20 L -10,-20 Z" fill="#6a8a6a"/><path d="M 10,-16 L 26,-28 L 28,-24 L 12,-12 Z" fill="#6a8a6a"/><path d="M -10,-20 C -10,-30 10,-30 10,-20" fill="none" stroke="#4a6a4a" stroke-width="2.4"/></g>'
    for (x, y, k) in ((200, 700, 1.0), (150, 760, 1.2)):
        o += f'<g transform="translate({x},{y}) scale({k})"><path d="M -14,0 L 14,0 L 10,26 L -10,26 Z" fill="#a8604a"/>' + "".join(f'<ellipse cx="{dx}" cy="{dy}" rx="8" ry="4" fill="#4e6e4a" transform="rotate({dx * 3} {dx} {dy})"/>' for dx, dy in ((-8, -10), (8, -12), (0, -18), (-12, -18), (12, -22))) + '</g>'
    # the great rain tree: trunk + layered canopy filling the top
    o += '<path d="M 230,620 C 236,520 228,420 240,300 L 286,300 C 292,420 296,520 304,620 Z" fill="#4a3c38"/><path d="M 230,620 C 236,520 228,420 240,300 L 256,300 C 252,420 252,520 254,620 Z" fill="#5c4a44"/>'
    o += '<path d="M 250,330 C 200,260 120,240 40,240 L 40,250 C 120,252 196,276 246,344 Z M 276,320 C 330,250 420,220 520,220 L 520,232 C 420,234 336,262 282,334 Z" fill="#4a3c38"/>'
    for (x, y, r) in ((20, 120, 120), (140, 60, 120), (280, 40, 140), (420, 70, 130), (540, 140, 120), (80, 230, 90), (460, 230, 90), (270, 170, 110)):
        o += clump(x, y, r, "#6a8a5a", "#4e6e48", "#3a5438")
    o += "".join(f'<circle cx="{RR.uniform(0, 540):.0f}" cy="{RR.uniform(0, 280):.0f}" r="{RR.uniform(2, 5):.0f}" fill="#e8b0c8" opacity=".75"/>' for _ in range(40))   # pink rain-tree blossoms
    # dappled light on the lawn
    o += "".join(f'<ellipse cx="{RR.uniform(0, 540):.0f}" cy="{RR.uniform(640, 950):.0f}" rx="{RR.uniform(14, 34):.0f}" ry="{RR.uniform(4, 9):.0f}" fill="#f8f0d0" opacity=".22"/>' for _ in range(18))
    o += "".join(tuft(RR.uniform(0, 540), RR.uniform(760, 950), RR.uniform(1, 1.6), "#4a6644") for _ in range(16))
    return o

ST["garden"] = garden_bg() + C("luc", 200, 860, .95) + C("agnes_left", 360, 860, .95) + C("mek", 500, 900, .9) + \
    '<g filter="url(#lsoft)" opacity=".9"><path d="M -40,820 C 20,780 80,800 110,860 C 60,880 0,900 -40,900 Z" fill="#2e4a2c"/><path d="M -20,960 C 30,880 90,890 120,960 Z" fill="#26402a"/><path d="M 560,0 C 480,30 470,90 500,140 C 530,110 560,60 560,0 Z" fill="#3a5a36"/></g>'


# --- evidence wall in Mek's guest room (shot 216), lit by one hanging lamp ---
def evidence_wall():
    R2 = _rr.Random(99)
    o = '<rect width="540" height="960" fill="#1e3a42"/><rect y="0" width="540" height="960" fill="url(#wallTeal)"/>'
    o += '<linearGradient id="wallTeal" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#14282e"/><stop offset=".5" stop-color="#2a4e56"/><stop offset="1" stop-color="#1a3238"/></linearGradient>'
    # a dense field of pinned papers and photos
    items = []
    for i in range(130):
        x = R2.uniform(-20, 540); y = R2.uniform(-10, 700); w = R2.uniform(34, 60); h = w * R2.uniform(1.1, 1.4); r = R2.uniform(-9, 9)
        items.append((y, x, w, h, r, R2.random()))
    for (y, x, w, h, r, t) in sorted(items):
        if t < .45:   # portrait photo
            o += (f'<g transform="translate({x:.0f},{y:.0f}) rotate({r:.1f})"><rect x="{-w / 2:.0f}" y="{-h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#d8dcd4"/>'
                  f'<rect x="{-w / 2 + 4:.0f}" y="{-h / 2 + 4:.0f}" width="{w - 8:.0f}" height="{h - 14:.0f}" fill="#4a5a5e"/><circle cx="0" cy="{-h * .12:.0f}" r="{w * .16:.0f}" fill="#9aa4a4"/><path d="M {-w * .28:.0f},{h * .3:.0f} C {-w * .2:.0f},{h * .02:.0f} {w * .2:.0f},{h * .02:.0f} {w * .28:.0f},{h * .3:.0f} Z" fill="#2a3436"/></g>')
        else:         # note / document with scribbles
            o += f'<g transform="translate({x:.0f},{y:.0f}) rotate({r:.1f})"><rect x="{-w / 2:.0f}" y="{-h / 2:.0f}" width="{w:.0f}" height="{h:.0f}" fill="#e8e4d4"/>' + "".join(f'<path d="M {-w * .38:.0f},{-h * .35 + k * h * .14:.0f} L {w * (.1 + R2.random() * .28):.0f},{-h * .35 + k * h * .14:.0f}" stroke="{"#b8382e" if R2.random() < .25 else "#8a8a80"}" stroke-width="1.6"/>' for k in range(5)) + '</g>'
        o += f'<circle cx="{x:.0f}" cy="{y - h / 2 + 4:.0f}" r="2.4" fill="#c83a32"/>'
    # the key items, near the lamp
    def pin_photo(x, y, r, inner, cap=""):
        return (f'<g transform="translate({x},{y}) rotate({r})"><rect x="-34" y="-42" width="68" height="84" fill="#f2efe4"/><rect x="-30" y="-38" width="60" height="62" fill="#5a5c58"/>{inner}'
                + (f'<text x="0" y="36" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" fill="#3a3030">{cap}</text>' if cap else "") + '<circle cx="0" cy="-38" r="3.4" fill="#d8443a"/></g>')
    twins = '<circle cx="-12" cy="-12" r="9" fill="#f4f0e6"/><circle cx="12" cy="-12" r="9" fill="#c8c2b4"/><path d="M -20,-20 l 16,16 M -4,-22 l -16,18" stroke="#fff" stroke-width="3"/><path d="M -24,20 C -20,4 -4,4 -2,20 Z M 2,20 C 4,4 20,4 24,20 Z" fill="#e8e4dc"/>'
    jan = '<circle cx="0" cy="-10" r="11" fill="#e8d4c0"/><path d="M -12,-14 C -12,-26 12,-26 12,-14 Z" fill="#1a1619"/><path d="M 6,-22 A 4,4 0 1 0 10,-17 A 3,3 0 1 1 6,-22 Z" fill="#f2d36a"/><path d="M -16,20 C -12,4 12,4 16,20 Z" fill="#f3e4e0"/>'
    tower = '<rect x="-6" y="-30" width="12" height="50" fill="#e4e0e8"/><path d="M -8,-30 C -8,-40 8,-40 8,-30 Z" fill="#e4e0e8"/><rect x="-1" y="-46" width="2" height="10" fill="#e4e0e8"/>'
    luc = '<circle cx="0" cy="-8" r="10" fill="#e8d8cc"/><path d="M -14,-6 C -14,-28 14,-28 14,-6 L 16,22 L -16,22 Z" fill="#1a1520" opacity=".9"/><circle cx="0" cy="-8" r="8" fill="#efd6c6"/>'
    o += pin_photo(200, 330, -4, twins, "แฝด 2549") + pin_photo(330, 310, 5, jan, "จันทร์เจ้า") + pin_photo(120, 450, 3, tower, "หอระฆัง") + pin_photo(420, 440, -6, luc, "ม.ลูเซีย")
    o += ('<g transform="translate(270,430) rotate(-2)"><rect x="-58" y="-40" width="116" height="80" fill="#efe8d4"/><text x="0" y="-22" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="10" font-weight="700" fill="#2a2420">ไฟไหม้สถานรับเลี้ยง</text>'
          '<text x="0" y="-9" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" fill="#2a2420">เด็กเสียชีวิต 2 ราย</text><path d="M -48,4 L 48,4 M -48,14 L 40,14 M -48,24 L 44,24" stroke="#9a9488" stroke-width="1.6"/><circle cx="16" cy="-9" r="16" fill="none" stroke="#c83a32" stroke-width="2.4"/><circle cx="0" cy="-38" r="3.4" fill="#d8443a"/></g>')
    for (x, y, r, t) in ((150, 560, 6, "จับช้อน?"), (380, 560, -5, "เด็กคนที่ 3?"), (270, 230, 3, "มือซ้าย?"), (460, 300, -8, "14 ธ.ค. 03:00")):
        o += f'<g transform="translate({x},{y}) rotate({r})"><rect x="-38" y="-16" width="76" height="32" fill="#f4e8a8"/><text x="0" y="5" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="12" font-weight="700" fill="#5a2a22">{t}</text><circle cx="0" cy="-12" r="3" fill="#d8443a"/></g>'
    # red strings linking the clues
    for (a, b) in (((200, 292), (330, 272)), ((200, 292), (270, 392)), ((330, 272), (380, 546)), ((270, 392), (150, 546)), ((120, 412), (270, 392)), ((420, 402), (270, 392)), ((270, 216), (200, 292)), ((460, 286), (420, 402))):
        mx = (a[0] + b[0]) / 2; my = (a[1] + b[1]) / 2 + 14
        o += f'<path d="M {a[0]},{a[1]} Q {mx},{my} {b[0]},{b[1]}" stroke="#c83a32" stroke-width="1.8" fill="none"/>'
    # desk with clutter, chair, stacks
    o += '<rect x="40" y="720" width="460" height="18" fill="#3a2a24"/><rect x="40" y="738" width="460" height="10" fill="#22181a"/><rect x="330" y="748" width="150" height="160" fill="#2a1e1c"/><rect x="340" y="770" width="130" height="4" fill="#3a2a26"/><circle cx="405" cy="820" r="3" fill="#8a7a5a"/><rect x="60" y="748" width="12" height="170" fill="#22181a"/>'
    o += '<g transform="translate(110,720)"><rect x="-26" y="-14" width="52" height="14" rx="2" fill="#2b2b30"/><circle cx="8" cy="-7" r="7" fill="#16161a"/><circle cx="8" cy="-7" r="4" fill="#3a4a66"/></g>'
    o += '<g transform="translate(170,720)"><path d="M -9,0 L -8,-20 L 8,-20 L 9,0 Z" fill="#e8e4dc"/><path d="M 9,-16 C 16,-16 16,-6 9,-6" fill="none" stroke="#e8e4dc" stroke-width="2.4"/></g>'
    o += '<g transform="translate(420,720)">' + "".join(f'<rect x="-36" y="{-6 - i * 6}" width="72" height="6" fill="{c}" transform="rotate({rr} 0 {-3 - i * 6})"/>' for i, (c, rr) in enumerate((("#e8e4d4", 0), ("#d8d4c4", 3), ("#e8e4d4", -2), ("#c8c4b4", 4), ("#e8e4d4", -3)))) + '</g>'
    o += '<g transform="translate(230,720)"><rect x="-30" y="-6" width="60" height="6" fill="#5a3a2a"/><path d="M -28,-6 L 0,-10 L 0,-4 L -28,-2 Z M 28,-6 L 0,-10 L 0,-4 L 28,-2 Z" fill="#e8dfcc"/></g>'
    o += '<path d="M -10,760 C 30,740 80,746 90,790 L 96,880 L -10,890 Z" fill="#2a1e1c"/><path d="M -10,880 L 100,870 L 104,890 L -10,900 Z" fill="#3a2a26"/><path d="M 40,900 L 30,960 M 70,896 L 80,960" stroke="#1a1214" stroke-width="5"/>'
    o += '<rect y="900" width="540" height="60" fill="#14100f"/>'
    # Mek from behind, hand on his hip, facing the wall
    o += C("mek_back", 270, 935, 1.08)
    # the pendant lamp
    o += '<path d="M 270,0 L 270,170" stroke="#0e1416" stroke-width="2.4"/><path d="M 230,214 C 230,180 310,180 310,214 Z" fill="#141c1e"/><ellipse cx="270" cy="214" rx="40" ry="7" fill="#fff4dc"/>'
    return o
ST["evidence_wall"] = evidence_wall()

exec(open(os.path.join(HERE, 'sb_stages2.py')).read())

# ---------- lighting & atmosphere per stage ----------
import random as _r
_R = _r.Random(21)
def L(key, dark=.5, tint="#120c16", holes=(), glows=(), beams=(), fog=(), motes=None, shadows=(), extra=""):
    """dark: how much of the frame falls into darkness; holes: (x,y,r) where light keeps it open;
    glows: (x,y,r,color,op); beams: (points,color,op); fog: (y,h,op); motes: (x0,y0,x1,y1,n,color);
    shadows: cast-shadow polygons (points, op)."""
    dark *= .42
    o = ""
    for pts, op in shadows:
        o += f'<polygon points="{pts}" fill="#05040a" opacity="{op}" filter="url(#lsoft)"/>'
    o += f'<mask id="lm_{key}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="940" height="1360"><rect x="-200" y="-200" width="940" height="1360" fill="#fff"/>'
    for (x, y, r) in holes:
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#000" filter="url(#lhole)"/>'
    o += '</mask>'
    o += f'<rect x="-200" y="-200" width="940" height="1360" fill="{tint}" opacity="{dark}" mask="url(#lm_{key})"/>'
    for (pts, col, op) in beams:
        o += f'<polygon points="{pts}" fill="{col}" opacity="{op * .6:.2f}" filter="url(#lhaze)" style="mix-blend-mode:screen"/>'
    for (y, h, op) in fog:
        o += f'<rect x="-100" y="{y}" width="740" height="{h}" fill="#c8ccdc" opacity="{op * .55:.2f}" filter="url(#lhaze)"/>'
    for (x, y, r, col, op) in glows:
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#lg_{col.strip("#")})" opacity="{op * .7:.2f}" style="mix-blend-mode:screen"/>'
        GLOWCOLS.add(col)
    LIGHTS[key] = [(x, y, r) for (x, y, r) in holes] + [(x, y, r) for (x, y, r, c_, o_) in glows]
    if motes:
        o += '<g class="lmotes">'
        x0, y0, x1, y1, n, col = motes
        for i in range(max(4, n // 3)):
            x = _R.uniform(x0, x1); y = _R.uniform(y0, y1)
            if _R.random() < .6:
                o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{_R.uniform(.8, 1.6):.1f}" fill="{col}" opacity="{_R.uniform(.45, .9):.2f}"/>'
            else:
                o += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{_R.uniform(1.6, 2.6):.1f}" fill="{col}" opacity="{_R.uniform(.2, .35):.2f}" filter="url(#lfar)"/>'
        o += '</g>'
    ST[key] += o + extra
GLOWCOLS = set()
LIGHTS = {}
MOON, WARM, CANDLE, SCREEN, PHONE, SIREN = "#c4d0ff", "#fff0dc", "#ffe6c4", "#b4a8ff", "#cfe0ff", "#6a8cff"

L("tower_fog", .45, holes=((270, 200, 160),), glows=((270, 190, 220, MOON, .5),), fog=((560, 160, .45),), motes=(40, 300, 500, 760, 26, "#e4e8ff"))
L("rosa_room", .62, holes=((150, 320, 150), (330, 560, 110), (285, 610, 40)),
  beams=(("40,160 260,160 520,920 200,940", MOON, .4),), glows=((285, 610, 50, "#9fdcff", .6), (150, 320, 200, MOON, .45)), motes=(150, 300, 470, 860, 26, "#dfe4ff"),
  shadows=(("330,900 380,900 520,960 440,960", .5),))
L("rosa_bed", .7, holes=((300, 560, 130),), glows=((300, 600, 120, WARM, .7),), motes=(220, 520, 400, 700, 14, "#fff4e0"))
L("oldwing", .45, holes=((205, 405, 70),), glows=((205, 400, 110, CANDLE, .85),), motes=(120, 300, 300, 520, 14, "#fff0d8"))
L("path_dawn", .25, holes=((270, 300, 280),), fog=((400, 200, .45),), glows=((270, 120, 300, MOON, .35),), motes=(60, 300, 480, 760, 20, "#eef2ff"))
L("refectory", .28, holes=((120, 230, 140), (420, 230, 140), (270, 560, 200)),
   motes=(60, 160, 520, 760, 28, "#fff4e0"))
L("condo", .58, holes=((420, 420, 180), (166, 640, 90)), glows=((520, 420, 300, SCREEN, .75), (166, 640, 110, PHONE, .7), (150, 250, 140, "#7f9cff", .3)), motes=(280, 300, 520, 700, 16, "#d8d0ff"))
L("gate", .14, holes=((120, 180, 300),), glows=((80, 160, 320, WARM, .45),),
  shadows=(("140,920 200,920 420,980 300,980", .45), ("360,900 420,900 560,960 480,970", .45), ("150,640 190,640 260,690 200,700", .35)),
  motes=None)
L("guestroom", .38, holes=((275, 280, 200), (160, 560, 120)), beams=(("150,110 400,110 330,960 -40,960", WARM, .38),), motes=(60, 200, 420, 820, 22, "#fff0dc"),
  shadows=(("160,900 220,900 330,960 240,960", .4),))
L("cemetery", .3, holes=((270, 300, 300), (170, 440, 120)), glows=((120, 200, 260, "#f8d0c8", .35),), motes=(40, 300, 500, 760, 14, "#f4eef8"))
L("cemetery_wide", .3, holes=((270, 300, 300), (170, 440, 120)), glows=((120, 200, 260, "#f8d0c8", .35),), motes=(40, 300, 500, 760, 14, "#f4eef8"))
L("music", .42, holes=((180, 380, 180), (440, 380, 90)), glows=((180, 120, 260, WARM, .55),), motes=(60, 150, 360, 600, 18, "#fff0dc"))
L("veranda", .66, holes=((270, 600, 170),), glows=((270, 610, 200, CANDLE, .9),), motes=(170, 460, 370, 640, 16, "#fff4e0"),
  shadows=(("140,860 200,860 120,960 40,960", .45), ("400,870 460,870 560,960 480,960", .45)))
L("dawn_walk", .3, holes=((270, 400, 280),), fog=((420, 200, .45),), glows=((300, 200, 300, MOON, .35),), motes=(40, 300, 500, 760, 20, "#eef2ff"))
L("mass", .45, holes=((270, 250, 170), (270, 500, 200)),
  beams=(("190,200 350,200 470,960 90,960", "#b8a8ff", .32),), glows=((270, 220, 160, "#b8a8ff", .5),), motes=(120, 260, 440, 800, 26, "#e8e2ff"))
L("garden", .12, holes=((270, 600, 300),), beams=(("120,0 220,0 300,820 140,820", WARM, .3),), motes=(100, 120, 460, 700, 14, "#fff4e0"))
L("archive", .5, holes=((270, 170, 70), (290, 560, 170)), beams=(("230,140 310,140 460,960 120,960", WARM, .5),), glows=((270, 170, 110, "#e8ecff", .6),), motes=(130, 220, 440, 800, 38, "#fff0dc"))
L("flash_dorm", .5, tint="#120a04", holes=((450, 560, 120), (270, 600, 260)), glows=((410, 650, 110, CANDLE, .75),), motes=(150, 500, 520, 800, 16, "#fff0d8"))
L("steps", .42, holes=((270, 420, 200), (270, 820, 100)), motes=(80, 200, 460, 700, 14, "#f4eef8"))
L("kitchen", .55, holes=((270, 300, 220), (200, 640, 160)), glows=((270, 145, 300, WARM, .85),), motes=(120, 180, 420, 700, 24, "#fff4e0"), shadows=(("250,900 310,900 380,960 300,960", .4),))
L("call", .0, extra='<circle cx="460" cy="150" r="260" fill="url(#lg_b4a8ff)" opacity=".8" style="mix-blend-mode:screen"/><rect x="0" y="474" width="540" height="486" fill="#06050c" opacity=".45"/><circle cx="200" cy="700" r="140" fill="url(#lg_cfe0ff)" opacity=".7" style="mix-blend-mode:screen"/><circle cx="450" cy="874" r="80" fill="#06050c" opacity=".0"/>')
GLOWCOLS.update({SCREEN, PHONE})
L("evidence_wall", .62, tint="#03121a", holes=((270, 470, 230), (270, 214, 60)), glows=((270, 220, 120, WARM, .9),),
  beams=(("232,214 308,214 470,900 70,900", WARM, .55),), motes=(140, 230, 400, 700, 14, "#fff4e0"), shadows=(("250,935 300,935 380,960 230,960", .5),))
L("dream", .3, tint="#1a1418", holes=((270, 240, 160),), glows=((270, 240, 200, "#f0f0ff", .55),), fog=((420, 420, .35),), motes=(60, 200, 480, 860, 30, "#e8e8f0"))
L("tower_night", .55, holes=((430, 110, 90), (380, 860, 150), (180, 640, 90)), glows=((430, 110, 160, MOON, .7),),
  beams=(("206,646 222,638 520,850 470,940", WARM, .5),), motes=(200, 640, 520, 940, 20, "#fff4e0"))
L("police", .25, holes=((270, 600, 260),), glows=((40, 300, 300, SIREN, .75),), motes=(40, 300, 500, 760, 14, "#e4e8ff"))
L("thana_night", .6, holes=((270, 300, 180), (280, 600, 180)), glows=((270, 125, 220, WARM, .8),), motes=(120, 160, 420, 640, 16, "#fff4e0"))
L("chapel_sisters", .5, holes=((261, 500, 90), (384, 345, 160), (270, 160, 120)), glows=((261, 510, 95, CANDLE, .9), (270, 150, 140, "#b8a8ff", .55), (470, 500, 90, WARM, .5)), motes=(120, 200, 460, 640, 18, "#dfe4ff"))
L("chapel_night", .66, holes=((405, 210, 120), (250, 560, 110)), beams=(("330,180 480,180 300,960 0,960", MOON, .42),), glows=((405, 200, 150, "#b8a8ff", .5),),
  motes=(80, 300, 440, 800, 30, "#dfe4ff"), extra='<path d="M 440,760 C 432,730 452,700 440,670 C 432,650 448,630 440,610" stroke="#c8c4d0" stroke-width="2" fill="none" opacity=".5" filter="url(#lfar)"/>')

# ---------- inserts (drawn whole, not cropped) ----------
INS = {}
def phone(lines, title="", glow=True):
    s = '<rect width="540" height="960" fill="#1a1828"/><rect x="120" y="120" width="300" height="600" rx="34" fill="#0e0c18"/><rect x="134" y="150" width="272" height="540" rx="10" fill="#e8ecf8"/>'
    if title: s += f'<rect x="134" y="150" width="272" height="44" fill="#4a5aa8"/><text x="270" y="178" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" fill="#fff">{title}</text>'
    for i, L in enumerate(lines):
        s += f'<text x="150" y="{230 + i * 26}" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#2a2a3a">{L}</text>'
    return s + ('<circle cx="270" cy="420" r="300" fill="#cdd8ff" opacity=".1"/>' if glow else "")
INS["clock"] = '<rect width="540" height="960" fill="#2a2630"/><rect x="120" y="360" width="300" height="160" rx="16" fill="#141218"/><text x="270" y="470" text-anchor="middle" font-family="ui-monospace, monospace" font-size="84" fill="#9fdcff">03:00</text><text x="270" y="560" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="16" fill="#c8c4d8">02:59 → 03:00</text>'
INS["rules1"] = '<rect width="540" height="960" fill="#3a3030"/>' + rules_board(70, 260, 2.0, hl=0)
INS["rules7"] = '<rect width="540" height="960" fill="#3a3030"/>' + rules_board(70, 260, 2.0, hl=6)
INS["title"] = '<rect width="540" height="960" fill="#120e16"/>' + stained_glass(150, 380, 240, 400) + '<text x="270" y="268" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="60" font-weight="700" fill="#fff">แม่ชีคนที่สอง</text><text x="270" y="318" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="22" fill="#e6e0f4">EP1 ระฆังตีสาม</text>'
INS["email"] = phone(["เรียนเชิญถ่ายภาพจดหมายเหตุ", "ครบรอบ 100 ปี", "คอนแวนต์เซนต์เวโรนิกา", "", "ระยะเวลา 3 สัปดาห์", "", "ผู้เสนอชื่อ: คุณแดง", "หัวหน้าแม่ครัว"], "อีเมลใหม่")
INS["album"] = ('<rect width="540" height="960" fill="#3a2a24"/><path d="M 40,300 L 270,280 L 270,700 L 30,720 Z" fill="#e8dfcc"/><path d="M 500,300 L 270,280 L 270,700 L 510,720 Z" fill="#ddd2bc"/>' +
    "".join(f'<rect x="{x}" y="{y}" width="90" height="70" fill="#8a8070"/><circle cx="{x + 30}" cy="{y + 30}" r="14" fill="#f4f0e6"/><circle cx="{x + 62}" cy="{y + 30}" r="14" fill="#f4f0e6"/><path d="M {x + 20},{y + 20} l 20,20 M {x + 40},{y + 18} l -20,24" stroke="#fff" stroke-width="3"/>' for x, y in ((70, 330), (160, 460), (300, 330), (390, 470))) +
    note(160, 760, "หน้าของมาร์ธาถูกขูดออกทุกใบ"))
INS["lefthand"] = ('<rect width="540" height="960" fill="#3a2a24"/><rect x="90" y="260" width="360" height="300" fill="#8a8070"/><circle cx="270" cy="360" r="60" fill="#f4f0e6"/><path d="M 230,330 l 80,60 M 300,320 l -70,70" stroke="#fff" stroke-width="10"/>' +
    '<path d="M 150,500 L 230,520 L 236,540 L 156,520 Z" fill="#f4f0e6"/><rect x="190" y="460" width="8" height="70" fill="#c8b07a" transform="rotate(-30 194 495)"/>' + note(130, 640, "เด็กถือดินสอด้วยมือซ้าย (เบาะแส ไม่เน้น)"))
INS["note"] = '<rect width="540" height="960" fill="#3a2a24"/><rect x="110" y="320" width="320" height="220" fill="#f4efe0" transform="rotate(-4 270 430)"/><text x="270" y="450" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="34" fill="#4a4040" transform="rotate(-8 270 430)">หนูยังอยู่ตรงนี้</text>' + note(140, 640, "ลายมือเด็กเอียงซ้าย กระดาษใหม่")
INS["tag"] = ('<rect width="540" height="960" fill="#1e1c24"/><rect x="100" y="260" width="340" height="420" rx="10" fill="#d8dce8" opacity=".25"/><rect x="100" y="260" width="340" height="40" fill="#b33a3a" opacity=".6"/>' +
    '<rect x="160" y="400" width="220" height="90" rx="6" fill="#fbf8f2"/><text x="270" y="460" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="40" font-weight="700" fill="#b33a3a">มาร์ธา</text>' + note(150, 720, "ป้ายชื่อผ้าปัก ใหม่เอี่ยม ไม่มีรอยไหม้"))
INS["drain"] = '<rect width="540" height="960" fill="#2a2430"/><ellipse cx="270" cy="520" rx="200" ry="70" fill="#3a3a40"/>' + "".join(f'<path d="M 110,{520 + d} L 430,{520 + d}" stroke="#141418" stroke-width="10"/>' for d in (-30, 0, 30)) + note(130, 680, "เสียงฮัม 'หลับเถิดนะ ลูกนกน้อย' ลอยออกมา")
INS["hand"] = ('<rect width="540" height="960" fill="#2a2228"/><rect x="0" y="500" width="540" height="80" fill="#f1ece2"/>' + "".join(f'<rect x="{x}" y="500" width="22" height="50" fill="#141014"/>' for x in range(20, 540, 54)) +
    '<ellipse cx="300" cy="470" rx="90" ry="60" fill="#f6dcc4"/><path d="M 260,440 C 290,430 320,450 316,470 C 300,490 270,480 260,460 Z" fill="#d98f86"/>' + note(150, 680, "แผลไฟไหม้หลังมือซ้ายของมาเรียม"))
INS["count"] = ('<rect width="540" height="960" fill="#4a4456"/>' + "".join(f'<g transform="translate({60 + i * 84},{420 + (i % 2) * 40})"><path d="M -30,0 C -30,-50 30,-50 30,0 L 34,200 L -34,200 Z" fill="#1a1520"/><text x="0" y="-60" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="22" font-weight="700" fill="#ffd84a">{n}</text></g>' for i, n in enumerate(("1", "2", "…", "11", "12", "")) if n) +
    note(130, 760, "นับได้ 12 คนพอดี ไม่มีอักเนส"))
INS["doll"] = '<rect width="540" height="960" fill="#3a3448"/><g transform="translate(270,480) scale(5)"><path d="M -18,0 L 18,0 L 24,32 L -24,32 Z" fill="#e8e0d4"/><path d="M 4,0 L 18,0 L 24,32 L 8,32 Z" fill="#3a2a24"/><circle cx="0" cy="-12" r="14" fill="#f0d8c0"/><path d="M 2,-26 C 14,-24 16,-12 12,-2 L 4,-6 Z" fill="#2a1a16"/><circle cx="-5" cy="-12" r="1.6" fill="#1a1216"/><circle cx="4" cy="-12" r="1.6" fill="#1a1216"/></g>'
INS["question"] = '<rect width="540" height="960" fill="#15121c"/><text x="270" y="320" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="28" font-weight="700" fill="#fff">ป้าแดงตกเอง หรือถูกผลัก?</text><rect x="90" y="400" width="360" height="80" rx="14" fill="#2a2440" stroke="#8f74d8"/><text x="270" y="452" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="26" fill="#ffd84a">A · ตกเอง</text><rect x="90" y="510" width="360" height="80" rx="14" fill="#2a2440" stroke="#8f74d8"/><text x="270" y="562" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="26" fill="#ffd84a">B · ถูกผลัก</text><text x="270" y="680" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" fill="#c8c4d8">EP2 ห้องสารภาพบาป</text>'


INS.update(INS2)
TAW_DEFS = TAW

# ---------- shots 31-32: the approved frame, used exactly as it is (nuns-test-frame_v1.html) ----------
_v1 = open(os.path.join(HERE, "..", "frames", "nuns-test-frame_v1.html")).read()
_d0 = _v1.index("<defs>"); _d1 = _v1.index("</defs>")
_v1defs = _v1[_d0 + 6:_d1]
_f0 = _v1.index('<svg viewBox="0 0 540 960"'); _f1 = _v1.index("</svg>", _f0)
_v1frame = _v1[_v1.index(">", _f0) + 1:_f1]
_v1frame = re.sub(r'<g id="guide">.*?</g>', '', _v1frame, flags=re.S)
def _ns(txt, ids):
    for i in sorted(ids, key=len, reverse=True):
        txt = txt.replace(f'id="{i}"', f'id="v1_{i}"').replace(f'url(#{i})', f'url(#v1_{i})').replace(f'href="#{i}"', f'href="#v1_{i}"')
    return txt
_ids = set(re.findall(r'id="([^"]+)"', _v1defs + _v1frame))
V1_DEFS = _ns(_v1defs, _ids)
# the picture you approved shows Agnes a cool lavender grey; match it with a colour matrix instead of the CSS brightness filter
_fr = _ns(_v1frame, _ids).replace('<g style="filter:brightness(.6) saturate(.85)">', '<g filter="url(#v1_agT)">')
V1_DEFS += '<filter id="v1_agT" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.64 0 0 0 0  0 0.63 0 0 0  0 0 0.81 0 0  0 0 0 1 0"/></filter>'
INS_EXACT = {"chapel_v1": _fr}

# ---------- panels: (shots, stage-or-insert, crop(cx,cy,h) or None, size, move, note) ----------
F_ = None
PANELS = {
 1: [("1-2", "tower_fog", F_, "ภาพกว้าง มุมต่ำ", "tilt-u", "หอระฆังเก่าในหมอก พระจันทร์เต็มดวงหลังเมฆ ระฆังในช่องหอแกว่งเองหนึ่งครั้ง"),
     ("3", "sisters_ext", F_, "ภาพกว้าง", "in", "ตึกพักซิสเตอร์ตอนกลางคืน หน้าต่างมืดทุกบาน ยกเว้นบานเดียวที่มีแสงเทียน"),
     ("4", "rosa_bed", (320, 560, 560), "ภาพปานกลาง", "static", "โรซานั่งบนเตียง มือหนึ่งถือไฟฉาย อีกมือเปิดพระคัมภีร์ แสงไฟฉายตกบนหน้ากระดาษ"),
     ("5-7", "clock", F_, "แทรก", "static", "นาฬิกาเปลี่ยนเป็น 03:00 ระฆังดัง โรซาสะดุ้ง"),
     ("8", "rules1", F_, "แทรก", "in", "ป้ายกฎข้อ 1 ไฟฉายส่อง"),
     ("9-12", "rosa_room", F_, "ภาพกว้าง", "in", "โรซาเดินไปที่หน้าต่าง มือหนึ่งแหวกผ้าม่าน อีกมือถือไฟฉายห้อยลง"),
     ("13-16", "oldwing", (200, 420, 420), "ภาพใกล้ (ผ่านหน้าต่าง)", "in", "แสงเทียนวาบ เงาเด็กชุดนอนเดินผ่าน หยุด แล้วหันมา"),
     ("17-19", "rosa_room", (200, 500, 420), "ภาพใกล้หน้าโรซา", "static", "โรซาน้ำตาคลอ เทียนในหน้าต่างดับ เธอปล่อยม่านแล้วคุกเข่าสวด")],
 2: [("20-22", "path_dawn", F_, "ภาพกว้าง มุมต่ำระดับพื้น", "tilt-u", "รอยเท้าเด็กเปียกเรียงจากสนามไปหยุดหน้าประตูตึกซิสเตอร์"),
     ("23-26", "refectory", F_, "ภาพกว้าง", "static", "ห้องอาหาร โรซาเล่า คาทารีนาวางแก้วเสียงดัง"),
     ("27-28", "refectory", (270, 560, 420), "ภาพปานกลาง", "in", "คาทารีนาลุกขึ้น 'เป็นลมพัด แค่นั้น'"),
     ("29-30", "refectory", (470, 560, 360), "ภาพใกล้", "in", "ป้าแดงยืนนิ่งปลายโต๊ะ มองไปทางปีกเก่าผ่านหน้าต่าง")],
 3: [("31", "chapel_v1", F_, "ภาพปานกลาง สองคน", "static", "ฉากที่ผ่านแล้ว: มาเรียมหน้า อักเนสหลังในเงาถือเทียน 'เมื่อยี่สิบปีก่อน มีเด็กฝาแฝดคนหนึ่งตายในกองเพลิง'"),
     ("32", "chapel_v1", (270, 300, 600), "ดันกล้องผ่านไหล่", "in", "ดันกล้องผ่านสองซิสเตอร์ไปที่กระจกสี หน้ามาร์ธาแตกหาย"),
     ("33", "title", F_, "การ์ดชื่อเรื่อง", "static", "ชื่อเรื่องขึ้น ระฆังหนึ่งครั้ง")],
 4: [("34-37", "condo", F_, "ภาพกว้าง", "static", "เจมส์เล่นเกม ดีนนอนขด เมฆนอนบนโซฟา ดีนเดินมาขึ้นตัก"),
     ("38-39", "email", F_, "แทรก", "in", "อีเมลเชิญจากคอนแวนต์"),
     ("40-45", "condo", (380, 620, 520), "ภาพปานกลาง", "static", "เจมส์ถอดหูฟัง หมุนเก้าอี้หา 'มึงไม่เคยเล่าเรื่องที่นั่นเลยนะ'"),
     ("46-48", "condo", (130, 680, 460), "ภาพใกล้", "in", "เมฆมองวิวตึก 'หอนอนมันไหม้ เด็กตายสองคน'"),
     ("49-53", "flash_dorm", (240, 700, 520), "ย้อนอดีต ภาพปานกลาง", "static", "เมฆตอนเด็กกับจันทร์เจ้า ครอบครัวมารับเมฆไปคนเดียว"),
     ("54-58", "email", (270, 420, 520), "แทรกใกล้", "in", "'ผู้เสนอชื่อ: คุณแดง' เมฆกดตอบรับ")],
 5: [("59-62", "gate", F_, "ภาพกว้างมาก", "pan-r", "ถนนริมคลองรถติด เดินผ่านประตู เสียงเมืองหาย เห็นโบสถ์ขาวหอระฆังกลาง"),
     ("63-64", "rules7", F_, "แทรก", "in", "ป้ายกฎ 7 ข้อ กล้องไล่อ่าน หยุดที่ข้อ 7"),
     ("65-68", "gate", (190, 640, 520), "ภาพปานกลาง สองคน", "static", "ป้าแดงเข้ามากอดเมฆ ร้องไห้ ยืนพื้นเดียวกัน"),
     ("69-74", "gate", (380, 640, 520), "ภาพปานกลาง", "static", "คาทารีนาบอกกติกาแขกผู้ชาย ชี้รั้วเหล็กด้านหลัง"),
     ("75-76", "gate", (270, 600, 760), "ภาพกว้าง", "out", "ป้าแดงเดินจาก หันกลับมามองเมฆ")],
 6: [("77-78", "guestroom", (190, 620, 520), "ภาพปานกลาง", "static", "คุณพ่อยอแซฟต้อนรับเมฆในเรือนรับรอง มือเย็นและสั่น"),
     ("79-80", "guestroom", F_, "ภาพกว้าง", "pan-r", "เรือนรับรอง: ชั้นหนังสือ ตู้เอกสาร โต๊ะทำงานคุณพ่อ ชุดรับแขก หน้าต่างหันไปทางปีกเก่า"),
     ("81-82", "guestroom", (270, 745, 300), "ภาพใกล้มือ", "in", "คุณพ่อยื่นกุญแจทองเหลืองในมือ เมฆยื่นมือรับ มือทั้งสองเจอกันกลางเฟรม"),
     ("83-85", "guestroom", (170, 560, 380), "ภาพใกล้", "static", "'กฎเจ็ดข้อที่ป้ายนั่น เชื่อพ่อเถอะ ทำตามมัน'")],
 7: [("86-87", "cemetery", (160, 650, 500), "ภาพปานกลาง", "static", "โรซาพูดเร็ว พาเดินดูก่อนมืด"),
     ("88-91", "cemetery_wide", F_, "ภาพกว้าง", "pan-l", "ถ้ำแม่พระ หอระฆังมีโซ่คล้อง โรซาเล่าว่าระฆังดังจริง"),
     ("92-96", "cemetery", (175, 860, 340), "ภาพใกล้ หลุมศพ", "in", "หลุมเด็กสามหลุม หลุมหนึ่งไม่มีชื่อ ป้าย 'มาร์ธา'"),
     ("97-102", "cemetery", (400, 640, 460), "ภาพปานกลาง", "static", "โรซาถามว่าเคยมีเด็กถือเทียนเดินไหม เมฆนิ่ง"),
     ("103-106", "cemetery_wide", F_, "ภาพกว้าง", "out", "ระฆังหกโมง โรซารีบกลับหลังรั้ว เมฆยืนคนเดียว")],
 8: [("107-110", "music", F_, "ภาพกว้าง มุมข้าง", "in", "มาเรียมนั่งบนม้านั่งเปียโน มองจากด้านข้าง มือวางบนคีย์ เทียนบนเปียโน"),
     ("109", "hand", F_, "แทรกใกล้มือ", "static", "แผลไฟไหม้หลังมือซ้ายบนคีย์เปียโน"),
     ("111-116", "music", (240, 520, 520), "ภาพปานกลาง มุมข้าง", "static", "มาเรียมหยุดเล่น คุยกับเมฆเรื่องความจำและการพูดชื่อตัวเองทุกคืน"),
     ("117-122", "music", (444, 450, 360), "ภาพใกล้", "in", "อักเนสโผล่ที่ประตูมืด ถือกระติกชา รู้ชื่อเมฆ"),
     ("123", "music", F_, "ภาพกว้าง", "static", "สองซิสเตอร์เดินจากไปคู่กัน")],
 9: [("124-126", "veranda", F_, "ภาพกว้าง", "static", "มื้อค่ำที่ระเบียง ตะเกียง แมลงเม่า ปีกเก่ามืดด้านหลัง"),
     ("127-131", "veranda", (170, 600, 440), "ภาพใกล้", "in", "คุณพ่อมือสั่น 'บางเรื่องพ่อรู้ แต่พ่อพูดไม่ได้'"),
     ("132-133", "veranda", (400, 600, 440), "ภาพปานกลาง", "static", "เมฆนั่งคนเดียว จำคำว่า 'เด็กคนนั้น'")],
 10: [("134-138", "guestroom", (270, 300, 560), "ภาพกว้างผ่านหน้าต่าง", "static", "ตีสาม เปียโนดังห้าโน้ตจากห้องดนตรีที่มืด เมฆไม่ออกไป"),
      ("139-142", "dawn_walk", F_, "ภาพกว้าง", "static", "ตีห้า มาเรียมเดินเท้าเปล่าเปื้อนดิน อักเนสห่มผ้า 'หนูเล่นเพลงของป้าแดง'")],
 11: [("143-145", "mass", F_, "ภาพกว้างจากแถวหลัง", "static", "มิสซาเช้า คุณพ่อที่แท่น เมฆนั่งแถวหลัง"),
      ("146-148", "count", F_, "มุมมองเมฆ", "pan-r", "นับผ้าคลุม 1…12 ไม่มีอักเนส"),
      ("149-153", "garden", F_, "ภาพกว้าง", "static", "ลูเซียบนรถเข็น อักเนสป้อนยามือซ้าย 'เมฆ… เด็กดื้อ'"),
      ("154-156", "garden", (200, 620, 420), "ภาพใกล้", "in", "'น้องจันทร์เขาฝากบอกว่าคิดถึงนะ' 'ฉันเขียนไว้แล้ว'"),
      ("157-158", "garden", (360, 620, 420), "ภาพใกล้", "static", "อักเนสเช็ดปากลูเซีย มองเมฆแวบหนึ่ง")],
 12: [("159-161", "archive", F_, "ภาพกว้าง", "static", "ห้องใต้หลังคา แสงจากหน้าต่างกลม เมฆถ่ายเอกสาร"),
      ("162-164", "album", F_, "แทรก", "in", "อัลบั้ม 2549 รูปหมู่เด็กสี่สิบคน จันทร์เจ้าติดกิ๊บพระจันทร์"),
      ("165-171", "flash_dorm", F_, "ย้อนอดีต ภาพกว้าง", "pan-r", "หอนอนเด็ก จันทร์เจ้าวิ่งเล่น แฝดสองคน ป้าแดงร้องเพลงกล่อม"),
      ("172-174", "album", (270, 500, 600), "แทรกใกล้", "in", "หน้ามาร์ธาถูกขูดออกทุกใบ"),
      ("175", "lefthand", F_, "แทรกใกล้", "static", "เด็กถือดินสอมือซ้าย"),
      ("176-179", "note", F_, "แทรก", "in", "แชตเจมส์ และกระดาษ 'หนูยังอยู่ตรงนี้'"),
      ("180-181", "archive", (290, 560, 520), "ภาพปานกลาง", "static", "ประตูแง้ม เสียงฝีเท้าเปล่าวิ่งหนี กลิ่นเทียน")],
 13: [("182-184", "doll", F_, "แทรกใกล้", "in", "ตุ๊กตาไหม้บนบันไดหน้าเรือนรับรอง"),
      ("185-189", "steps", F_, "ภาพกว้าง มุมต่ำ", "static", "มือซ้ายอักเนสหยิบตุ๊กตา 'ห้องพยาบาลอยู่นอกรั้ว เดินได้ทั้งคืน'")],
 14: [("190-193", "kitchen", F_, "ภาพกว้าง", "static", "ครัวกลาง หลอดไฟดวงเดียว ป้าแดงตักแกงให้เมฆ"),
      ("194-203", "kitchen", (180, 640, 440), "ภาพปานกลาง สองคน", "in", "ป้าแดงเล่าเรื่องระฆัง แยกแฝดตอนจับช้อน และได้ยินเพลงของป้า"),
      ("204-208", "kitchen", (456, 470, 300), "ภาพใกล้ที่ประตู", "in", "อักเนสโผล่ที่ประตูพร้อมกาน้ำชา ฮัมเพลง มือป้าแดงสั่น"),
      ("209-213", "kitchen", (250, 620, 460), "ภาพปานกลาง", "static", "อักเนสรินชามือซ้าย ยื่นให้ป้าแดง ป้าเทชาทิ้ง"),
      ("214-215", "kitchen", (250, 560, 320), "ภาพใกล้", "in", "'พรุ่งนี้เช้าป้าจะเล่าทั้งหมด' ยัดของใส่กระเป๋าผ้ากันเปื้อน")],
 15: [("216", "evidence_wall", F_, "ภาพกว้าง จากหลังตัวละคร", "in", "เมฆยืนหน้าผนังเบาะแสในห้องพัก รูปจากห้องเก็บเอกสาร เชือกแดง โคมไฟดวงเดียว"),
      ("217-221", "dream", F_, "ฝัน ภาพกว้าง", "static", "ห้องน้ำหอเด็ก ควัน เด็กผู้หญิงปีนหน้าต่าง หน้ามืด"),
      ("222-227", "call", F_, "มุมมองจอโทรศัพท์", "static", "เห็นเจมส์เต็มจอแบบกล้องหน้า ห้องเจมส์ด้านหลัง เมฆอยู่ในกรอบเล็กมุมขวาบน"),
      ("228-234", "drain", F_, "แทรก", "in", "เจมส์ได้ยินเสียงเด็กร้องเพลง ฝาท่อในห้อง"),
      ("235-239", "clock", F_, "แทรก", "shake", "เงียบ 2 วินาที แล้วระฆังดังตอน 03:00 ป้ายกฎข้อ 1"),
      ("240-243", "call", F_, "มุมมองจอโทรศัพท์", "shake", "เจมส์ตะโกนห้าม ภาพในสายสั่นเพราะเมฆลุกคว้าไฟฉาย")],
 16: [("244-246", "tower_night", F_, "ภาพกว้าง มุมต่ำ", "tilt-u", "หอระฆังขาวยอดโดม โซ่ประตูถูกปลด ระฆังยังแกว่ง"),
      ("247-248", "tower_night", (170, 820, 420), "ภาพปานกลาง", "pan-l", "ชายผ้าคลุมดำแวบหาย รอยเท้าเปียกไปทางห้องพยาบาล"),
      ("249-253", "tower_night", (300, 870, 320), "ภาพใกล้", "in", "ร่างป้าแดงที่ฐานหอ พวงกุญแจกระจาย เจมส์ตะโกนในสาย"),
      ("254-255", "tower_night", (270, 330, 600), "มุมเงยขึ้นยอดหอ", "tilt-u", "เมฆเงยมองช่องระฆังที่มืด มีคนมองลงมา")],
 17: [("256-262", "police", F_, "ภาพกว้าง", "static", "ไฟไซเรน แถบกั้น ธนาสอบปากคำ 'ที่นี่ใส่ผ้าคลุมดำทุกคนครับคุณ'"),
      ("263-264", "police", (130, 700, 420), "ภาพปานกลาง", "static", "คาทารีนาขอให้จบเงียบ ๆ"),
      ("265-269", "body_sheet", F_, "ภาพปานกลาง", "in", "ร่างป้าแดงใต้ผ้าขาว มาเรียมทรุด อักเนสยืนข้างหลัง")],
 18: [("270-276", "thana_night", F_, "ภาพปานกลาง", "static", "ธนากลับมาคนเดียว ยื่นถุงหลักฐาน กุญแจหอระฆังหายจากพวง"),
      ("272-274", "tag", F_, "แทรกใกล้", "in", "ผ้าเช็ดหน้าปักชื่อ Martha ด้วยลายมือ ผ้าสะอาด ด้ายใหม่"),
      ("277-281", "chapel_night", F_, "ภาพกว้าง", "in", "เมฆไขประตูข้างโบสถ์ นั่งแถวหน้า กระซิบ 'มาร์ธา…'"),
      ("282-285", "chapel_night", (270, 560, 600), "ภาพกว้าง จากหลังแท่นบูชา", "static", "เทียนดับ เงียบ 2 วิ เสียงเด็กจากความมืด 'ค่ะ'"),
      ("286-287", "question", F_, "การ์ดคำถาม", "static", "A/B แล้วต่อฉากโลโก้ปิดท้าย")],
}

# ---------- script parsing ----------
SCRIPT = open(os.path.join(HERE, "script.md")).read()
ROWS = {}
TITLES = {}
cur = None
for line in SCRIPT.splitlines():
    m = re.match(r"## ฉาก (\d+): (.+)", line)
    if m: cur = int(m.group(1)); TITLES[cur] = m.group(2); continue
    m = re.match(r"\| (\d+) \| (.*?) \|(.*)\|$", line)
    if m and cur: ROWS[int(m.group(1))] = (cur, m.group(2), m.group(3).strip())
CHIPS = {}
for m in re.finditer(r"## ฉาก (\d+):.*?\n(?:ป้าย: \*\*(.+?)\*\*)?", SCRIPT):
    if m.group(2): CHIPS[int(m.group(1))] = m.group(2)

def md(s):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\*(.+?)\*", r"<i>\1</i>", s)
    return s

def shots(rng):
    a, _, b = rng.partition("-"); a = int(a); b = int(b or a)
    return [n for n in range(a, b + 1) if n in ROWS]

def dur(ns):
    t = 0.0
    for n in ns:
        audio = re.sub(r"\*\*[^*]*:\*\*|\*[^*]*\*|\([^)]*\)", "", ROWS[n][2])
        c = len(re.sub(r"\s", "", audio))
        t += c / 14 + (1.2 if c else 2.2)
    return t

MOVES = {"static": "กล้องนิ่ง", "in": "ดันกล้องเข้าช้า ๆ", "out": "ถอยกล้องออก", "pan-l": "แพนซ้าย", "pan-r": "แพนขวา", "tilt-u": "เงยกล้องขึ้น", "tilt-d": "ก้มกล้องลง", "shake": "กล้องสั่นสั้น ๆ"}
def move_overlay(mv):
    c = "#ff5a6a"; o = ""
    if mv == "in": o = f'<g stroke="{c}" stroke-width="3" fill="none"><path d="M 60,120 L 60,60 L 120,60 M 480,120 L 480,60 L 420,60 M 60,840 L 60,900 L 120,900 M 480,840 L 480,900 L 420,900"/><path d="M 120,180 L 160,220 M 420,180 L 380,220 M 120,780 L 160,740 M 420,780 L 380,740" stroke-width="2.4"/></g>'
    elif mv == "out": o = f'<g stroke="{c}" stroke-width="3" fill="none"><path d="M 160,220 L 120,180 M 380,220 L 420,180 M 160,740 L 120,780 M 380,740 L 420,780"/><rect x="40" y="40" width="460" height="880" stroke-dasharray="10 8"/></g>'
    elif mv in ("pan-l", "pan-r"):
        d = -1 if mv == "pan-l" else 1
        o = f'<g stroke="{c}" stroke-width="4" fill="{c}"><path d="M {270 - 160 * d},880 L {270 + 150 * d},880" fill="none"/><path d="M {270 + 170 * d},880 L {270 + 140 * d},864 L {270 + 140 * d},896 Z"/></g>'
    elif mv in ("tilt-u", "tilt-d"):
        d = -1 if mv == "tilt-u" else 1
        o = f'<g stroke="{c}" stroke-width="4" fill="{c}"><path d="M 500,{480 - 300 * d} L 500,{480 + 280 * d}" fill="none"/><path d="M 500,{480 + 310 * d} L 484,{480 + 270 * d} L 516,{480 + 270 * d} Z"/></g>'
    elif mv == "shake": o = f'<path d="M 40,100 l 20,-12 l 20,12 l 20,-12 l 20,12" stroke="{c}" stroke-width="3" fill="none"/>'
    return o

def panel_svg(stage, crop, mv):
    if stage in INS_EXACT:   # approved frame: no grade, no vignette, no colour boost
        cx, cy, h = crop if crop else (270, 480, 960); w = h * 9 / 16
        return (f'<svg viewBox="0 0 540 960" role="img"><svg x="0" y="0" width="540" height="960" viewBox="{cx - w / 2:.1f} {cy - h / 2:.1f} {w:.1f} {h:.1f}" preserveAspectRatio="xMidYMid slice">{INS_EXACT[stage]}</svg>'
                f'<rect x="1" y="1" width="538" height="958" fill="none" stroke="#000" stroke-width="2"/>{move_overlay(mv)}</svg>')
    body = INS.get(stage) or f'<use href="#st_{stage}"/>'
    if crop:
        cx, cy, h = crop; w = h * 9 / 16
        vb = f"{cx - w / 2:.1f} {cy - h / 2:.1f} {w:.1f} {h:.1f}"
    else:
        vb = "0 0 540 960"
    return (f'<svg viewBox="0 0 540 960" role="img"><svg x="0" y="0" width="540" height="960" viewBox="{vb}" preserveAspectRatio="xMidYMid slice">'
            f'<g class="bw">{body}</g></svg>'
            f'<rect width="540" height="960" fill="url(#pvig)"/><rect class="grade" width="540" height="960" fill="#5a3a6a" opacity=".1" style="mix-blend-mode:soft-light"/>'
            f'<rect x="1" y="1" width="538" height="958" fill="none" stroke="#000" stroke-width="2"/>'
            f'<rect x="24" y="576" width="492" height="144" fill="none" stroke="#5aa0ff" stroke-width="2" stroke-dasharray="8 6" opacity=".7"/>'
            f'{move_overlay(mv)}</svg>')

exec(open(os.path.join(HERE, 'sb_anim.py')).read())

def anim_html(rng):
    a = ANIM.get(rng)
    if not a: return ""
    rows = [("สีหน้า", a[0]), ("ท่าทาง", a[1]), ("ฉากเคลื่อนไหว", a[2]), ("เสียง", a[3])]
    return '<dl class="anim">' + "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows if v and v != "-") + '</dl>'

# ---------- page ----------
sections = []
total = 0.0
for sc in sorted(PANELS):
    cards = []
    sc_dur = 0.0
    for (rng, stage, crop, size, mv, desc) in PANELS[sc]:
        ns = shots(rng); d = dur(ns); sc_dur += d
        lines = "".join(f'<li><span class="n">#{n}</span> <span class="vis">{md(ROWS[n][1])}</span><br><span class="aud">{md(ROWS[n][2])}</span></li>' for n in ns)
        cards.append(f'''<article class="panel">
  <div class="pic">{panel_svg(stage, crop, mv)}</div>
  <div class="meta"><div class="hd"><b>ช็อต {rng.replace("-", "–")}</b><span>{size}</span><span>{MOVES[mv]}</span><span>≈ {d:.0f} วิ</span></div>
  <p class="desc">{desc}</p>
  {anim_html(rng)}
  <details><summary>ทุกช็อตในช่วงนี้ ({len(ns)})</summary><ol>{lines}</ol></details></div>
</article>''')
    total += sc_dur
    chip = CHIPS.get(sc, "")
    sections.append(f'<section><h2>ฉาก {sc} · {TITLES.get(sc, "")}<span>{chip} · ≈ {sc_dur / 60:.1f} นาที</span></h2><div class="grid">{"".join(cards)}</div></section>')

DEFS = (f'<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{V1_DEFS}{TAW_DEFS}{cf.NUN_DEFS}{v1.JAMES_DEFS}{"".join(v2.POSES)}'
        + "".join(f'<g id="st_{k}">{v}</g>' for k, v in ST.items())
        + '<filter id="drop" x="-20%" y="-20%" width="150%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="5"/><feOffset dx="6" dy="8"/><feComponentTransfer><feFuncA type="linear" slope=".35"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        + '<filter id="dof" x="0" y="0" width="100%" height="100%"><feGaussianBlur stdDeviation="0"/></filter><filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>'
        + '<radialGradient id="pvig" cx="50%" cy="45%" r="72%"><stop offset=".55" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".42"/></radialGradient>'
        + '<filter id="lhole" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="40"/></filter><filter id="lhaze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="12"/></filter><filter id="lsoft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter><filter id="lfar" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.2"/></filter>'
        + ''.join(f'<radialGradient id="lg_{c.strip("#")}"><stop offset="0" stop-color="{c}" stop-opacity=".75"/><stop offset=".4" stop-color="{c}" stop-opacity=".25"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>' for c in GLOWCOLS)
        + '</defs></svg>')

html = f'''<title>EP1 สตอรี่บอร์ด</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one section per scene; panel cards in a grid (3 / 2 / 1 columns), each card = 9:16 board + shot meta + collapsible shot list. Single light "paper" look by choice: storyboards read best as grey sketches on white. */
:root {{ --paper:#f4f2ee; --ink:#1e1c22; --muted:#6a6670; --line:#d6d2cc; --accent:#ff5a6a; --blue:#3a7ad8;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:light; }}
html,body {{ background:var(--paper); color:var(--ink); margin:0; }}
body {{ font-family:var(--font); padding:24px max(16px, env(safe-area-inset-right,0px)) 48px max(16px, env(safe-area-inset-left,0px)); }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:28px; }}
header h1 {{ font-size:20px; margin:0 0 6px; font-weight:700; }}
header p {{ margin:0; color:var(--muted); font-size:13.5px; line-height:1.7; }}
.legend {{ display:flex; flex-wrap:wrap; gap:8px 18px; font-size:12.5px; color:var(--muted); margin-top:10px; }}
.legend i {{ display:inline-block; width:22px; height:0; border-top:3px solid var(--accent); vertical-align:middle; margin-right:6px; }}
.legend i.b {{ border-top:2px dashed var(--blue); }}
section h2 {{ font-size:17px; margin:0 0 12px; padding-bottom:8px; border-bottom:2px solid var(--ink); display:flex; flex-wrap:wrap; gap:4px 12px; align-items:baseline; }}
section h2 span {{ font-size:13px; color:var(--muted); font-weight:400; }}
.grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
@media (max-width:960px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:560px) {{ .grid {{ grid-template-columns:1fr; }} }}
.panel {{ background:#fff; border:1px solid var(--line); border-radius:8px; padding:10px; display:grid; gap:10px; align-content:start; min-width:0; }}
.pic svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; background:#ddd; }}
.bw {{ filter:saturate(1.35) brightness(1.1) contrast(1.04); }}
body.gray .bw {{ filter:grayscale(1) contrast(1.08) brightness(1.12); }}
body.gray .grade {{ display:none; }}
.bar {{ display:flex; gap:10px; align-items:center; flex-wrap:wrap; margin-top:12px; font-size:13px; color:var(--muted); }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:#fff; border:1px solid var(--line); border-radius:6px; padding:6px 12px; cursor:pointer; }}
button:hover {{ border-color:var(--muted); }} button:focus-visible {{ outline:2px solid var(--blue); outline-offset:2px; }}
button[aria-pressed="true"] {{ border-color:var(--ink); background:var(--ink); color:#fff; }}
.hd {{ display:flex; flex-wrap:wrap; gap:4px 10px; font-size:12.5px; color:var(--muted); align-items:baseline; }}
.hd b {{ color:var(--ink); font-size:14px; }}
.desc {{ margin:0; font-size:13.5px; line-height:1.6; }}
dl.anim {{ display:grid; grid-template-columns:auto 1fr; gap:3px 10px; margin:0; font-size:12.5px; line-height:1.5; background:#f6f4f0; border-radius:6px; padding:8px 10px; }}
dl.anim dt {{ color:var(--muted); white-space:nowrap; }} dl.anim dd {{ margin:0; }}
details summary {{ cursor:pointer; font-size:12.5px; color:var(--blue); }}
details summary:focus-visible {{ outline:2px solid var(--blue); outline-offset:2px; }}
ol {{ list-style:none; margin:8px 0 0; padding:0; display:grid; gap:8px; }}
li {{ font-size:12.5px; line-height:1.55; border-left:3px solid var(--line); padding-left:8px; }}
.n {{ font-weight:700; }} .vis {{ color:var(--muted); }} .aud {{ color:var(--ink); }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Noto+Serif+Thai:wght@500;700&family=Dancing+Script:wght@600;700&display=swap">
{DEFS}
<div class="wrap">
<header>
  <h1>แม่ชีคนที่สอง EP1 · สตอรี่บอร์ด</h1>
  <p>18 ฉาก · {sum(len(v) for v in PANELS.values())} ภาพหลัก · ครอบคลุมทั้ง 287 ช็อตของบท (กด "ทุกช็อตในช่วงนี้" ใต้ภาพเพื่อดูภาพและเสียงของทุกช็อต) · ความยาวรวมประมาณ {total / 60:.0f} นาที (คิดจากความยาวบทพากย์)</p>
  <p>ภาพสีสด บอกมุมกล้อง ขนาดภาพ ตำแหน่งตัวละคร และแสงเงาของแต่ละฉาก กดปุ่ม "โทนเทา" เพื่อดูแบบสตอรี่บอร์ดดั้งเดิม</p>
  <div class="legend"><span><i></i>ลูกศรแดง = การเคลื่อนกล้อง</span><span><i class="b"></i>กรอบประฟ้า = พื้นที่ซับ (60–75% ของความสูง)</span></div>
  <div class="bar"><span>มุมมอง</span><button id="bm" type="button" aria-pressed="false">โทนเทา</button><span>กดเพื่อดูแบบสตอรี่บอร์ดโทนเทา กดอีกครั้งกลับเป็นภาพสี</span></div>
</header>
{"".join(sections)}
</div>
<script>
const bm = document.getElementById('bm');
bm.addEventListener('click', () => {{ const on = bm.getAttribute('aria-pressed') !== 'true'; bm.setAttribute('aria-pressed', String(on)); document.body.classList.toggle('gray', on); }});
</script>'''
open(os.path.join(HERE, "storyboard.html"), "w").write(html)
print("wrote storyboard.html", len(html) // 1024, "KB,", sum(len(v) for v in PANELS.values()), "panels,", f"{total / 60:.1f} min")
missing = [n for n in range(1, 288) if not any(n in shots(p[0]) for v in PANELS.values() for p in v)]
print("shots not covered:", missing)
