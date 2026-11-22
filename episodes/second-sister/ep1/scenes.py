#!/usr/bin/env python3
"""EP1 key frames: one still per scene (18 scenes), 540x960, house style.
Characters come from the approved sheets:
  - Mariam / Agnes: ../frames/nuns-test-frame.html
  - supporting cast: ../characters/build_cast.py
  - James + cat: ../../../scenes/ep-partner-not-same-test-frame.html
Run: python3 scenes.py  ->  scenes.html
"""
import os, sys, random, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))

# ---------- borrow approved art ----------
spec = importlib.util.spec_from_file_location("bc", os.path.join(HERE, "..", "characters", "build_cast.py"))
bc = importlib.util.module_from_spec(spec)
_stdout = sys.stdout; sys.stdout = open(os.devnull, "w"); spec.loader.exec_module(bc); sys.stdout = _stdout
CAST = {c[0]: c[4] for c in bc.cards}

nuns = open(os.path.join(HERE, "..", "frames", "nuns-test-frame.html")).read()
NUN_DEFS = nuns[nuns.index('<clipPath id="face">'):nuns.index('<filter id="dof"')]
# Agnes without the candle (for day scenes); her raised hand stays
a0 = NUN_DEFS.index('<g id="agnes">'); a1 = NUN_DEFS.index('<filter', a0) if '<filter' in NUN_DEFS[a0:] else len(NUN_DEFS)
agnes = NUN_DEFS[a0:a1]
c0 = agnes.index('<!-- brass holder + taper -->'); c1 = agnes.index('<!-- left hand around the holder')
AGNES_NC = agnes[:c0].replace('<g id="agnes">', '<g id="agnesNC">') + agnes[c1:]

tf = open(os.path.join(ROOT, "scenes", "ep-partner-not-same-test-frame.html")).read()
JAMES_DEFS = tf[tf.index('<clipPath id="jface"'):tf.index('<clipPath id="tface"')]
CAT = tf[tf.index('<!-- orange cat curled beside the desk -->'):tf.index('<!-- ============ TAWAN ROOM')]

JAMES_BODY = '''<g id="jamesBody">
  <path d="M -16,52 C -32,54 -46,60 -52,74 L -58,260 L 58,260 L 52,74 C 46,60 32,54 16,52 Z" fill="#2b3768"/>
  <path d="M -52,74 C -46,60 -32,54 -18,53 C -24,90 -28,170 -30,260 L -58,260 Z" fill="#3d4b8a"/>
  <path d="M 24,55 C 38,58 48,64 52,74 L 58,260 L 34,260 C 34,170 32,100 24,55 Z" fill="#1d2550"/>
  <path d="M -15,52 C -10,60 10,60 15,52" fill="none" stroke="#1a2147" stroke-width="4"/>
  <g fill="#9fb0ff"><rect x="-14" y="96" width="28" height="12" rx="3"/></g>
  <g fill="#2b3768"><rect x="-10" y="100" width="2" height="4"/><rect x="-12" y="101" width="6" height="2"/><circle cx="7" cy="101" r="1.4"/><circle cx="10" cy="103.6" r="1.4"/></g>
</g>'''

SHARED_DEFS = f'''
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
{NUN_DEFS}
{AGNES_NC}
{JAMES_DEFS}
{JAMES_BODY}
<g id="james"><use href="#jamesBody"/><g transform="translate(0,9) scale(.82)"><use href="#jhead"/></g></g>
{''.join(f'<g id="c-{k}">{v}</g>' for k, v in CAST.items())}
<filter id="dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.6"/></filter>
<filter id="dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="bokeh" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="moteFar" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation=".6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="5" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="drop" x="-20%" y="-20%" width="150%" height="150%"><feGaussianBlur in="SourceAlpha" stdDeviation="6"/><feOffset dx="8" dy="10"/><feComponentTransfer><feFuncA type="linear" slope=".42"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="subStroke" x="-10%" y="-30%" width="120%" height="160%"><feMorphology in="SourceAlpha" operator="dilate" radius="2.2" result="d"/><feFlood flood-color="#120e18"/><feComposite in2="d" operator="in" result="o"/><feMerge><feMergeNode in="o"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="vig" cx="50%" cy="45%" r="70%"><stop offset=".5" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".82"/></radialGradient>
<radialGradient id="glowW" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#fff1dc" stop-opacity=".6"/><stop offset=".4" stop-color="#f3cfb8" stop-opacity=".22"/><stop offset="1" stop-color="#d9a9a0" stop-opacity="0"/></radialGradient>
<radialGradient id="glowB" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#b9b2ff" stop-opacity=".6"/><stop offset=".45" stop-color="#7d6ff0" stop-opacity=".22"/><stop offset="1" stop-color="#5a4fd0" stop-opacity="0"/></radialGradient>
<radialGradient id="glowC" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#a9c4ff" stop-opacity=".55"/><stop offset=".5" stop-color="#6f86d8" stop-opacity=".18"/><stop offset="1" stop-color="#4a5aa8" stop-opacity="0"/></radialGradient>
<radialGradient id="glowR" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#7f9cff" stop-opacity=".55"/><stop offset=".5" stop-color="#3f5ad8" stop-opacity=".2"/><stop offset="1" stop-color="#2a3a98" stop-opacity="0"/></radialGradient>
<linearGradient id="beamC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b4c0ff" stop-opacity=".32"/><stop offset="1" stop-color="#7f88d8" stop-opacity="0"/></linearGradient>
<linearGradient id="beamW" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0dc" stop-opacity=".34"/><stop offset="1" stop-color="#f3cfb8" stop-opacity="0"/></linearGradient>
<linearGradient id="nightSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121733"/><stop offset="1" stop-color="#2a2f5e"/></linearGradient>
<linearGradient id="duskSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3560"/><stop offset=".7" stop-color="#7a6a8e"/><stop offset="1" stop-color="#b59aa6"/></linearGradient>
<linearGradient id="dawnSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a3354"/><stop offset="1" stop-color="#7d8cab"/></linearGradient>
</defs></svg>'''

# ---------- helpers ----------
def fig(cid, x, y, k=1.0, light=1.0, sat=1.0, extra=""):
    st = f' style="filter:brightness({light}) saturate({sat})"' if (light != 1 or sat != 1) else ""
    return f'<g filter="url(#drop)"><g{st}><g transform="translate({x},{y}) scale({k})"><use href="#{cid}"/>{extra}</g></g></g>'

def glow(x, y, r, g="glowW", op=1):
    return f'<ellipse cx="{x}" cy="{y}" rx="{r}" ry="{r}" fill="url(#{g})" opacity="{op}" style="mix-blend-mode:screen"/>'

def beam(pts, g="beamC", op=1):
    return f'<polygon points="{pts}" fill="url(#{g})" opacity="{op}" filter="url(#haze)" style="mix-blend-mode:screen"/>'

def motes(x0, y0, x1, y1, n, col="#e8e2ff", seed=1):
    r = random.Random(seed); out = []
    for i in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if r.random() < .6:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6,1.3):.1f}" fill="{col}" opacity="{r.uniform(.4,.8):.2f}" filter="url(#moteGlow)"/>')
        else:
            out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.2,2):.1f}" fill="{col}" opacity="{r.uniform(.2,.35):.2f}" filter="url(#moteFar)"/>')
    return "".join(out)

def frame(body, chip=None, th=None, en=None, label=""):
    s = f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">'
    s += body
    s += '<rect width="540" height="960" fill="url(#vig)"/>'
    s += '<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:screen"/>'
    s += '<rect width="540" height="960" filter="url(#grain)" opacity=".045" style="mix-blend-mode:overlay"/>'
    if chip:
        w = 14 + len(chip) * 7.4
        s += f'<rect x="24" y="28" width="{w:.0f}" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8f74d8" stroke-width="1.4"/>'
        s += f'<text x="{24 + w/2:.0f}" y="48" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="500" fill="#e6e0f4">{chip}</text>'
    s += '<g transform="translate(500,44)" opacity=".8"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="none" stroke="#b18cff" stroke-width="1.6"/><circle r="3.6" fill="#b18cff"/></g>'
    if th:
        lines = th.split("|"); el = en.split("|") if en else []
        n = len(lines) + len(el)
        y = 712 - (len(lines) * 27 + len(el) * 17) / 2 + 20
        s += '<g class="subs" font-family="IBM Plex Sans Thai, sans-serif" text-anchor="middle" filter="url(#subStroke)">'
        for L in lines:
            s += f'<text x="270" y="{y:.0f}" font-size="20" font-weight="700" fill="#ffd84a">{L}</text>'; y += 27
        for L in el:
            s += f'<text x="270" y="{y:.0f}" font-family="Inter, sans-serif" font-size="13" font-weight="500" fill="#fff">{L}</text>'; y += 17
        s += '</g>'
    s += '</svg>'
    return s

# ---------- reusable set pieces ----------
def old_wing(x, y, k=1.0, lit=None, op=1):
    """Burnt two-storey brick dorm. lit = index of window with a candle."""
    s = f'<g transform="translate({x},{y}) scale({k})" opacity="{op}">'
    s += '<path d="M 0,40 L 120,0 L 240,40 L 240,220 L 0,220 Z" fill="#1c1418"/>'
    s += '<path d="M 0,40 L 120,0 L 120,8 L 6,46 Z" fill="#2a1e22"/>'
    s += '<path d="M 0,40 L 60,40 L 60,220 L 0,220 Z" fill="#160f13"/>'
    for i, (wx, wy) in enumerate([(24,70),(74,70),(124,70),(174,70),(24,140),(74,140),(124,140),(174,140)]):
        col = "#0b080b"
        s += f'<path d="M {wx},{wy} L {wx+28},{wy} L {wx+28},{wy+44} L {wx},{wy+44} Z" fill="{col}"/>'
        s += f'<path d="M {wx+4},{wy+30} L {wx+12},{wy+20} L {wx+18},{wy+34} L {wx+24},{wy+24} L {wx+28},{wy+44} L {wx},{wy+44} Z" fill="#100b0e"/>'
        if lit == i:
            s += f'<rect x="{wx+2}" y="{wy+2}" width="24" height="40" fill="#3a2a24"/>'
            s += f'<ellipse cx="{wx+14}" cy="{wy+24}" rx="9" ry="12" fill="#ffe9cc" opacity=".5" filter="url(#soft)"/>'
            s += f'<path d="M {wx+8},{wy+44} L {wx+9},{wy+22} C {wx+9},{wy+14} {wx+19},{wy+14} {wx+19},{wy+22} L {wx+20},{wy+44} Z" fill="#0d090b"/>'
            s += f'<circle cx="{wx+14}" cy="{wy+12}" r="5" fill="#0d090b"/>'
            s += f'<circle cx="{wx+21}" cy="{wy+26}" r="1.6" fill="#fff4dc"/>'
    s += '<path d="M 60,40 L 70,20 L 82,44 L 96,10 L 110,40 L 60,40 Z" fill="#0f0a0d"/>'
    s += '</g>'
    return s

def bell_tower(x, y, k=1.0, swing=0):
    return f'''<g transform="translate({x},{y}) scale({k})">
      <path d="M -40,0 L 40,0 L 46,420 L -46,420 Z" fill="#3a2226"/>
      <path d="M -40,0 L -14,0 L -16,420 L -46,420 Z" fill="#4a2c30"/>
      <path d="M 18,0 L 40,0 L 46,420 L 20,420 Z" fill="#2a181c"/>
      <path d="M -52,-70 L 0,-130 L 52,-70 Z" fill="#241418"/>
      <rect x="-48" y="-70" width="96" height="70" fill="#2e1a1e"/>
      <path d="M -30,-60 C -30,-20 30,-20 30,-60 L 30,-6 L -30,-6 Z" fill="#0c080b"/>
      <g transform="rotate({swing} 0 -56)"><path d="M -14,-50 C -14,-34 -18,-22 -22,-18 L 22,-18 C 18,-22 14,-34 14,-50 C 14,-58 -14,-58 -14,-50 Z" fill="#5b6a5a"/><path d="M -14,-50 C -14,-34 -18,-22 -22,-18 L -8,-18 C -8,-30 -6,-44 -2,-56 C -10,-56 -14,-54 -14,-50 Z" fill="#7d8f7a"/></g>
      <g fill="#2a181c"><rect x="-40" y="60" width="80" height="4"/><rect x="-42" y="180" width="84" height="4"/><rect x="-44" y="300" width="88" height="4"/></g>
      <path d="M -12,330 L 12,330 L 12,420 L -12,420 Z" fill="#120b0e"/>
    </g>'''

def stained_glass(x, y, w, h, broken=True, bright=1.0):
    cx = x + w/2
    return f'''<g opacity="{bright}">
      <path d="M {x-8},{y+h+8} L {x-8},{y+h*0.42} C {x-8},{y+h*0.12} {cx-w*0.3},{y-10} {cx},{y-14} C {cx+w*0.3},{y-10} {x+w+8},{y+h*0.12} {x+w+8},{y+h*0.42} L {x+w+8},{y+h+8} Z" fill="#0d0b11"/>
      <clipPath id="sg{x}{y}"><path d="M {x},{y+h} L {x},{y+h*0.42} C {x},{y+h*0.14} {cx-w*0.28},{y-2} {cx},{y-6} C {cx+w*0.28},{y-2} {x+w},{y+h*0.14} {x+w},{y+h*0.42} L {x+w},{y+h} Z"/></clipPath>
      <g clip-path="url(#sg{x}{y})">
        <rect x="{x}" y="{y-10}" width="{w}" height="{h+20}" fill="#2b2f5c"/>
        <rect x="{x}" y="{y-10}" width="{w/2}" height="{h+20}" fill="#33386e"/>
        <rect x="{x}" y="{y+h*0.55}" width="{w}" height="{h*0.45}" fill="#3c2f52"/>
        <circle cx="{cx}" cy="{y+h*0.2}" r="{w*0.16}" fill="#4c4f8c"/><circle cx="{cx}" cy="{y+h*0.2}" r="{w*0.07}" fill="#8f7ab8"/>
        <path d="M {x+w*0.1},{y+h} L {x+w*0.14},{y+h*0.55} C {x+w*0.16},{y+h*0.48} {x+w*0.36},{y+h*0.48} {x+w*0.38},{y+h*0.55} L {x+w*0.42},{y+h} Z" fill="#5a2f45"/>
        <circle cx="{x+w*0.26}" cy="{y+h*0.44}" r="{w*0.1}" fill="#b8a46e" opacity=".55"/>
        <ellipse cx="{x+w*0.26}" cy="{y+h*0.45}" rx="{w*0.065}" ry="{w*0.07}" fill="{'#07060a' if broken else '#d9c9c0'}"/>
        <path d="M {x+w*0.58},{y+h} L {x+w*0.62},{y+h*0.55} C {x+w*0.64},{y+h*0.48} {x+w*0.84},{y+h*0.48} {x+w*0.86},{y+h*0.55} L {x+w*0.9},{y+h} Z" fill="#2f4f86"/>
        <circle cx="{x+w*0.74}" cy="{y+h*0.44}" r="{w*0.1}" fill="#b8a46e" opacity=".55"/>
        <ellipse cx="{x+w*0.74}" cy="{y+h*0.45}" rx="{w*0.065}" ry="{w*0.07}" fill="#d9c9c0"/>
        <g stroke="#0d0b11" stroke-width="3" fill="none"><line x1="{cx}" y1="{y-10}" x2="{cx}" y2="{y+h}"/><line x1="{x}" y1="{y+h*0.38}" x2="{x+w}" y2="{y+h*0.38}"/><line x1="{x}" y1="{y+h*0.7}" x2="{x+w}" y2="{y+h*0.7}"/></g>
      </g></g>'''

def rules_board(x, y, k=1.0, hl=None):
    rules = ["1 ระฆังตีสาม ห้ามออกจากห้อง", "2 เสียงเคาะห้องสารภาพบาป อย่าเปิดม่าน", "3 ห้ามเข้าปีกเก่าหลังสามทุ่ม", "4 ห้ามจุดเทียนในหอเด็ก",
             "5 ก่อนนอนต้องขานชื่อตัวเอง", "6 นับซิสเตอร์ได้สิบสาม อย่าทัก", "7 ห้ามเอ่ยชื่อ มาร์ธา"]
    s = f'<g transform="translate({x},{y}) scale({k})"><rect x="0" y="0" width="200" height="190" rx="4" fill="#3a2a20"/><rect x="6" y="6" width="188" height="178" fill="#5a4030"/><rect x="6" y="6" width="80" height="178" fill="#664a38"/>'
    s += '<text x="100" y="30" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" font-weight="700" fill="#efe2c8">กฎของโบสถ์น้อย</text>'
    for i, r in enumerate(rules):
        col = "#ffd84a" if hl == i else "#e4d3b4"
        s += f'<text x="14" y="{54 + i*19}" font-family="IBM Plex Sans Thai, sans-serif" font-size="10.5" fill="{col}">{r}</text>'
    return s + '</g>'

# ================== SCENES ==================
S = []

# 1. Rosa at the window, 03:00
S.append(("ฉาก 1 · เปิดเรื่อง", "ซิสเตอร์โรซาแง้มม่าน เห็นเงาเด็กถือเทียนในปีกเก่า", frame(
  '<rect width="540" height="960" fill="#1a1520"/>'
  '<g filter="url(#dof)">'
  '<rect x="30" y="110" width="290" height="440" fill="url(#nightSky)"/>'
  + old_wing(40, 250, 1.12, lit=6) +
  '<rect x="30" y="500" width="290" height="50" fill="#0e1018"/>'
  '<path d="M 400,120 L 410,120 L 410,200 L 400,200 Z M 380,145 L 430,145 L 430,153 L 380,153 Z" fill="#0d0a10"/>'
  '</g>'
  '<path d="M 18,96 L 334,96 L 334,564 L 18,564 Z M 30,110 L 30,550 L 320,550 L 320,110 Z" fill="#2c2228" fill-rule="evenodd"/>'
  '<rect x="170" y="110" width="8" height="440" fill="#2c2228"/><rect x="30" y="320" width="290" height="8" fill="#2c2228"/>'
  '<path d="M 230,100 C 250,240 236,420 262,570 L 338,570 L 338,96 Z" fill="#3a2f3e"/><path d="M 300,96 L 338,96 L 338,570 L 312,570 C 300,420 310,240 300,96 Z" fill="#2a2130"/>'
  + beam("40,120 320,120 520,900 160,900", "beamC", .9) + motes(150, 300, 470, 640, 18, "#d6dcff", 3) +
  fig("c-rosa", 400, 430, 1.75, .78, .9) +
  glow(400, 400, 160, "glowC", .45),
  "18 พ.ย. · 03:00", "ฝั่งตรงข้ามคือปีกเก่า|ที่ปิดตายมายี่สิบปี", "Across the lawn: the old wing, sealed for twenty years.", "โรซามองปีกเก่า")))

# 2. Wet footprints, dawn
fp = "".join(f'<g transform="translate({x},{y}) scale({s}) rotate({r})"><ellipse cx="0" cy="0" rx="5" ry="9" fill="#1d2232"/><circle cx="-3" cy="-11" r="1.6" fill="#1d2232"/><circle cx="0" cy="-12" r="1.6" fill="#1d2232"/><circle cx="3" cy="-11" r="1.5" fill="#1d2232"/><ellipse cx="-1" cy="-2" rx="2" ry="4" fill="#8fa0c8" opacity=".35"/></g>'
             for x, y, s, r in [(300,900,2.2,8),(250,800,1.9,-6),(286,712,1.6,8),(252,640,1.35,-6),(278,580,1.15,8),(256,532,1.0,-6),(272,494,.85,8),(260,466,.72,-6)])
S.append(("ฉาก 2 · เช้าหลังคืนนั้น", "รอยเท้าเด็กเปียก ๆ จากปีกเก่าไปหยุดหน้าตึกซิสเตอร์", frame(
  '<rect width="540" height="960" fill="url(#dawnSky)"/>'
  '<g filter="url(#dof2)"><path d="M 140,180 L 400,180 L 400,440 L 140,440 Z" fill="#3a3046"/><path d="M 140,180 L 270,120 L 400,180 Z" fill="#2c2438"/>'
  '<path d="M 230,300 L 310,300 L 310,440 L 230,440 Z" fill="#1c1622"/><path d="M 234,304 L 270,304 L 270,440 L 234,440 Z" fill="#241c2a"/>'
  '<g fill="#544866"><rect x="160" y="220" width="40" height="50"/><rect x="340" y="220" width="40" height="50"/></g>'
  '<g stroke="#1a1520" stroke-width="5"><line x1="0" y1="430" x2="540" y2="430"/>' + "".join(f'<line x1="{x}" y1="360" x2="{x}" y2="440"/>' for x in range(10, 540, 36)) + '</g></g>'
  '<path d="M 0,440 L 540,440 L 540,960 L 0,960 Z" fill="#4a4c5e"/>'
  '<path d="M 200,440 L 340,440 L 560,960 L -20,960 Z" fill="#5d6074"/>'
  '<g stroke="#3a3c4c" stroke-width="2" fill="none"><path d="M 200,520 L 350,520 M 160,620 L 390,620 M 110,760 L 440,760 M 40,920 L 500,920"/><path d="M 270,440 L 270,960 M 230,440 L 170,960 M 310,440 L 370,960"/></g>'
  + fp + '<rect x="0" y="380" width="540" height="200" fill="#8a96b8" opacity=".25" filter="url(#haze)"/>'
  + motes(60, 300, 480, 700, 14, "#e6ecff", 5),
  "18 พ.ย. · 06:15", "รอยเท้าเด็กเปียก ๆ|เดินมาจากทางปีกเก่า", "Small wet footprints, coming from the old wing.", "รอยเท้าเปียก")))

# 3. Title
S.append(("ฉาก 3 · ชื่อเรื่อง", "หน้าต่างกระจกสีที่ใบหน้ามาร์ธาแตกหายไป", frame(
  '<rect width="540" height="960" fill="#120e16"/>'
  + stained_glass(150, 380, 240, 400) +
  beam("150,520 390,520 520,960 20,960", "beamC", .8) + motes(80, 520, 460, 900, 20, "#d6dcff", 7) +
  '<text x="270" y="190" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="22" fill="#cdbfff">ODD HOURS · EP1</text>'
  '<text x="270" y="268" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="64" font-weight="700" fill="#fff">แม่ชี<tspan fill="#c9a8ff">คนที่สอง</tspan></text>'
  '<text x="270" y="318" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="22" fill="#e6e0f4">ระฆังตีสาม</text>',
  None, None, None, "ชื่อเรื่อง")))

# 4. James's condo
S.append(("ฉาก 4 · คอนโดเจมส์", "เมฆเล่าเรื่องไฟไหม้ให้เจมส์ฟังเป็นครั้งแรก", frame(
  '<rect width="540" height="960" fill="#181633"/>'
  '<g filter="url(#dof)"><rect x="40" y="90" width="230" height="300" fill="#0e1430"/>'
  + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1a2250"/>' for x, y, w, h in [(50,200,40,190),(100,150,50,240),(160,230,36,160),(206,120,54,270)]) +
  "".join(f'<rect x="{x}" y="{y}" width="4" height="5" fill="#7f9cff" opacity=".7"/>' for x, y in [(60,220),(70,260),(112,180),(130,220),(120,300),(172,250),(220,150),(240,200),(230,280)]) +
  '<circle cx="232" cy="118" r="2.4" fill="#ff5a6a"/><path d="M 30,80 L 280,80 L 280,400 L 30,400 Z M 40,90 L 40,390 L 270,390 L 270,90 Z" fill="#22204a" fill-rule="evenodd"/>'
  '<rect x="300" y="160" width="200" height="8" fill="#9a86ff"/></g>'
  '<path d="M 300,330 C 300,290 480,290 480,330 L 490,620 L 290,620 Z" fill="#15132b"/><rect x="306" y="334" width="8" height="280" fill="#6a52e0"/>'
  + fig("james", 392, 420, 1.55, .92) +
  '<path d="M 0,560 L 250,560 L 270,960 L 0,960 Z" fill="#2a2648"/><path d="M 0,520 L 230,520 L 236,580 L 0,580 Z" fill="#3a3466"/>'
  + fig("c-mek", 130, 520, 1.45, .85) +
  '<path d="M 0,640 L 280,640 L 300,960 L 0,960 Z" fill="#2a2648"/><path d="M 0,640 L 280,640 L 282,664 L 0,664 Z" fill="#3a3466"/>'
  '<rect x="150" y="610" width="34" height="56" rx="5" fill="#0e0c1c"/><rect x="153" y="614" width="28" height="46" rx="3" fill="#cdd8ff"/>'
  + glow(166, 600, 90, "glowC", .7) + glow(520, 420, 260, "glowB", .7) +
  f'<g transform="translate(10,250) scale(1.2)">{CAT}</g>',
  "19 พ.ย. · 04:10", "คืนสุดท้ายที่กูอยู่ที่นั่น|หอนอนมันไหม้", "The last night I was there, the dorm burned.", "คอนโดเจมส์")))

# 5. Catarina at the iron fence
fence = "".join(f'<rect x="{x}" y="300" width="6" height="320" fill="#141016"/><path d="M {x-4},300 L {x+3},282 L {x+10},300 Z" fill="#141016"/>' for x in range(-10, 560, 30))
S.append(("ฉาก 5 · กติกาของแขกผู้ชาย", "มาเธอร์คาทารีนาชี้รั้วเหล็ก: หลังรั้วคือเขตซิสเตอร์ ห้ามเข้า", frame(
  '<rect width="540" height="960" fill="url(#duskSky)"/>'
  '<g filter="url(#dof2)">' + bell_tower(440, 150, .7) +
  '<path d="M 0,260 L 380,260 L 380,620 L 0,620 Z" fill="#6a3a3c"/><path d="M 0,230 L 190,180 L 380,230 L 380,260 L 0,260 Z" fill="#4a2a30"/>'
  + "".join(f'<rect x="{x}" y="{y}" width="34" height="56" fill="#3a2a3a"/><rect x="{x}" y="{y}" width="34" height="8" fill="#e8d8c8" opacity=".4"/>' for x in (30,110,190,270) for y in (300,400)) +
  '</g>' + fence + '<rect x="0" y="420" width="540" height="10" fill="#141016"/><rect x="0" y="330" width="540" height="8" fill="#141016"/>'
  '<rect x="236" y="400" width="26" height="40" rx="4" fill="#2a2420"/><path d="M 242,400 C 242,386 256,386 256,400" fill="none" stroke="#2a2420" stroke-width="4"/>'
  '<path d="M 0,620 L 540,620 L 540,960 L 0,960 Z" fill="#3a3a3c"/>'
  + fig("c-cat", 160, 470, 1.65, .95) + fig("c-mek", 400, 480, 1.7, .95) +
  glow(100, 200, 260, "glowW", .35),
  "20 พ.ย. · 16:30", "หลังรั้วนั้นคือที่พักของซิสเตอร์|ห้ามเข้าเด็ดขาด", "Behind that fence is the sisters' house. Never go in.", "คาทารีนาที่รั้ว")))

# 6. Guest room, Father Joseph with the key
S.append(("ฉาก 6 · เรือนรับรอง", "คุณพ่อยอแซฟให้กุญแจประตูข้างโบสถ์ หน้าต่างหันไปทางปีกเก่าพอดี", frame(
  '<rect width="540" height="960" fill="#241c26"/>'
  '<g filter="url(#dof)"><rect x="150" y="110" width="250" height="330" fill="url(#duskSky)"/>' + old_wing(170, 230, .9) +
  '<path d="M 138,98 L 412,98 L 412,452 L 138,452 Z M 150,110 L 150,440 L 400,440 L 400,110 Z" fill="#3a2c2a" fill-rule="evenodd"/><rect x="270" y="110" width="8" height="330" fill="#3a2c2a"/>'
  '<path d="M 0,560 L 540,560 L 540,620 L 0,620 Z" fill="#1c161c"/>'
  '<path d="M 400,470 L 540,470 L 540,600 L 400,600 Z" fill="#2c2228"/><path d="M 400,440 L 410,440 L 410,600 L 400,600 Z M 530,440 L 540,440 L 540,600 Z" fill="#141016"/><rect x="400" y="470" width="140" height="30" fill="#e8e0d4" opacity=".7"/></g>'
  + beam("150,110 400,110 300,960 -40,960", "beamW", .55) + motes(80, 300, 400, 700, 14, "#fff0dc", 9) +
  fig("c-jos", 150, 450, 1.7, .9) + fig("c-mek", 390, 470, 1.7, .88) +
  '<g transform="translate(262,640)"><circle r="7" fill="none" stroke="#c9ad66" stroke-width="3"/><path d="M 5,4 L 22,20 L 18,24 L 14,20 L 11,23 L 8,20" fill="none" stroke="#c9ad66" stroke-width="3"/></g>'
  + glow(262, 640, 40, "glowW", .7),
  "20 พ.ย. · 17:05", "โบสถ์เปิดให้สวดมนต์ทั้งคืน|ถ้านอนไม่หลับ ไปนั่งในนั้นได้", "The chapel stays open all night, if you can't sleep.", "คุณพ่อให้กุญแจ")))

# 7. Cemetery with three graves
def cross(x, y, k, label=None):
    s = f'<g transform="translate({x},{y}) scale({k})"><rect x="-4" y="-60" width="8" height="70" fill="#e4dfd6"/><rect x="-20" y="-44" width="40" height="8" fill="#e4dfd6"/><rect x="0" y="-60" width="4" height="70" fill="#b9b2a6"/><ellipse cx="0" cy="12" rx="26" ry="6" fill="#1a1820" opacity=".6"/>'
    if label:
        s += f'<rect x="-22" y="-26" width="44" height="18" rx="2" fill="#c9c2b6"/><text x="0" y="-13" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="9" fill="#3a3238">{label}</text>'
    return s + '</g>'
S.append(("ฉาก 7 · ทัวร์กับโรซา", "สุสานเด็กสามหลุม ทั้งที่ข่าวบอกว่าตายสองคน หลุมหนึ่งไม่มีชื่อ", frame(
  '<rect width="540" height="960" fill="url(#duskSky)"/>'
  '<g filter="url(#dof2)">' + old_wing(260, 200, 1.1) + "".join(cross(x, 470, .55) for x in range(30, 540, 60)) + '</g>'
  '<path d="M 0,480 L 540,480 L 540,960 L 0,960 Z" fill="#2c3028"/><path d="M 0,480 L 540,480 L 540,520 L 0,520 Z" fill="#3a4034"/>'
  + fig("c-rosa", 150, 440, 1.55, .9) + fig("c-mek", 400, 450, 1.6, .9) +
  cross(120, 840, 1.5, "มาร์ธา") + cross(270, 860, 1.5, "นภา") + cross(420, 840, 1.5) +
  glow(270, 160, 280, "glowW", .3),
  "20 พ.ย. · 17:40", "ผมนับได้สามหลุม|ทั้งที่ข่าวบอกว่าเด็กตายแค่สองคน", "I counted three graves. The news said two.", "สุสานเด็ก")))

# 8. Music room: Mariam + Agnes with thermos
thermos = '<g transform="translate(24,60)"><rect x="0" y="0" width="20" height="52" rx="4" fill="#5a6a7a"/><rect x="0" y="0" width="7" height="52" rx="3" fill="#7a8a9a"/><rect x="2" y="-8" width="16" height="10" rx="2" fill="#3a4450"/></g>'
S.append(("ฉาก 8 · มาเรียมกับเปียโน", "มาเรียมพูดถึงกฎข้อห้า อักเนสเข้ามาพร้อมกระติกชา", frame(
  '<rect width="540" height="960" fill="#2a2230"/>'
  '<g filter="url(#dof)"><rect x="0" y="120" width="540" height="10" fill="#3a2e36"/>'
  '<rect x="370" y="140" width="130" height="420" fill="#1a141c"/><rect x="376" y="146" width="118" height="414" fill="#2e2430"/><circle cx="382" cy="360" r="3" fill="#c9ad66"/>'
  '<rect x="40" y="170" width="120" height="90" fill="#3a3046"/><g stroke="#2a2230" stroke-width="2"><line x1="60" y1="190" x2="140" y2="190"/><line x1="60" y1="210" x2="140" y2="210"/><line x1="60" y1="230" x2="140" y2="230"/></g></g>'
  + fig("agnesNC", 430, 400, 1.25, .78, .9, thermos) +
  '<path d="M 10,470 L 330,470 L 330,700 L 10,700 Z" fill="#1c1418"/><path d="M 10,470 L 330,470 L 330,486 L 10,486 Z" fill="#3a2a2c"/>'
  + fig("mariam", 180, 360, 1.42) +
  '<path d="M 0,540 L 360,540 L 370,960 L 0,960 Z" fill="#1e1619"/><path d="M 0,520 L 360,520 L 362,546 L 0,546 Z" fill="#2c2024"/>'
  '<rect x="10" y="526" width="340" height="16" fill="#f1ece2"/>' + "".join(f'<rect x="{x}" y="526" width="7" height="10" fill="#141014"/>' for x in range(22, 340, 17)) +
  glow(180, 120, 260, "glowW", .45) + beam("120,0 260,0 360,700 40,700", "beamW", .5) + motes(60, 150, 360, 560, 16, "#fff0dc", 11),
  "20 พ.ย. · 17:55", "คนที่เคยอยู่ที่นี่|ไม่มีใครถูกลืมหรอก", "No one who lived here is ever forgotten.", "ห้องดนตรี")))

# 9. Veranda dinner
S.append(("ฉาก 9 · มื้อค่ำกับคุณพ่อ", "คุณพ่อพูดหลุดว่า 'เด็กคนนั้น' ไม่ใช่ 'เด็กสองคน'", frame(
  '<rect width="540" height="960" fill="#120f18"/>'
  '<g filter="url(#dof2)"><rect width="540" height="420" fill="url(#nightSky)"/>' + old_wing(150, 200, 1.0) +
  '<path d="M 0,380 C 80,330 140,360 200,340 C 300,320 380,360 540,330 L 540,520 L 0,520 Z" fill="#0c0e14"/></g>'
  '<rect x="0" y="100" width="20" height="560" fill="#2a2024"/><rect x="520" y="100" width="20" height="560" fill="#2a2024"/><rect x="0" y="90" width="540" height="18" fill="#2a2024"/>'
  + fig("c-jos", 130, 420, 1.6, .82) + fig("c-mek", 410, 430, 1.62, .82) +
  '<path d="M 40,580 L 500,580 L 520,620 L 20,620 Z" fill="#4a362e"/><rect x="20" y="620" width="500" height="20" fill="#2c201c"/>'
  '<rect x="258" y="520" width="24" height="56" rx="3" fill="#2a2420"/><rect x="262" y="528" width="16" height="36" fill="#fff1dc"/><rect x="254" y="514" width="32" height="8" fill="#2a2420"/>'
  '<ellipse cx="200" cy="584" rx="34" ry="8" fill="#e8e0d4"/><ellipse cx="340" cy="584" rx="34" ry="8" fill="#e8e0d4"/>'
  + glow(270, 548, 220, "glowW", .9) + motes(170, 420, 370, 560, 12, "#fff4e0", 13) +
  '<g fill="#d8cfc0" opacity=".7"><path d="M 300,470 l 6,-3 l 2,4 Z"/><path d="M 236,500 l -6,-2 l 0,5 Z"/></g>',
  "20 พ.ย. · 19:40", "บางเรื่องพ่อรู้|แต่พ่อพูดไม่ได้", "Some things I know, but I cannot say.", "มื้อค่ำที่ระเบียง")))

# 10. Dawn: Mariam sleepwalking, Agnes with blanket
blanket = '<path d="M -60,40 C -50,20 50,20 60,40 L 66,180 L -66,180 Z" fill="#8a8aa6" opacity=".95"/><path d="M -60,40 C -54,30 -40,26 -26,24 L -30,180 L -66,180 Z" fill="#a6a6c0"/>'
S.append(("ฉาก 10 · คืนแรก", "ตีห้า มาเรียมเดินเท้าเปล่าออกมาจากห้องดนตรี อักเนสตามมาห่มผ้าให้", frame(
  '<rect width="540" height="960" fill="url(#dawnSky)"/>'
  '<g filter="url(#dof2)"><path d="M 0,240 L 540,240 L 540,560 L 0,560 Z" fill="#3a3a52"/>'
  + "".join(f'<rect x="{x}" y="300" width="50" height="70" fill="#22223a"/>' for x in (30, 130, 230, 330, 430)) +
  '<rect x="0" y="230" width="540" height="14" fill="#2a2a40"/></g>'
  '<path d="M 0,560 L 540,560 L 540,960 L 0,960 Z" fill="#4a4c5e"/>'
  + fig("agnesNC", 380, 420, 1.35, .85, .9) + fig("mariam", 220, 440, 1.5, .9, .9, blanket) +
  '<rect x="0" y="420" width="540" height="200" fill="#9aa6c8" opacity=".2" filter="url(#haze)"/>' + motes(60, 300, 480, 640, 14, "#e6ecff", 15),
  "21 พ.ย. · 05:02", "หนูเล่นเพลงของป้าแดง…", "I played Auntie Daeng's song...", "มาเรียมละเมอ")))

# 11. Garden: Mother Lucia
spoon = '<g transform="translate(30,96) rotate(-30)"><rect x="-1.2" y="-22" width="2.4" height="22" fill="#c8c8d0"/><ellipse cx="0" cy="-24" rx="4" ry="5" fill="#d8d8e0"/></g>'
S.append(("ฉาก 11 · มาเธอร์ลูเซีย", "'น้องจันทร์เขาฝากบอกว่าคิดถึงนะ เขารออยู่ตรงนั้น'", frame(
  '<rect width="540" height="960" fill="#3a4250"/>'
  '<g filter="url(#dof2)"><circle cx="120" cy="140" r="170" fill="#2a3a30"/><circle cx="380" cy="100" r="190" fill="#24342c"/><rect x="250" y="160" width="30" height="420" fill="#2a2024"/>'
  '<path d="M 0,520 L 540,520 L 540,960 L 0,960 Z" fill="#3a4a3a"/></g>'
  '<path d="M 0,560 L 540,560 L 540,960 L 0,960 Z" fill="#344234"/>'
  + fig("c-luc", 190, 470, 1.55, .9) + fig("agnesNC", 360, 440, 1.4, .92, .9, spoon) +
  beam("200,0 360,0 300,700 120,700", "beamW", .5) + motes(100, 120, 420, 560, 16, "#fff4e0", 17),
  "21 พ.ย. · 06:45", "น้องจันทร์เขาฝากบอกว่าคิดถึงนะ|เขารออยู่ตรงนั้น", "Little Jan says she misses you. She's waiting there.", "ลูเซียในสวน")))

# 12. Archive
S.append(("ฉาก 12 · ห้องเก็บเอกสาร", "อัลบั้มปี 2549 หน้าของมาร์ธาถูกขูดออกทุกใบ", frame(
  '<rect width="540" height="960" fill="#2a2024"/>'
  '<path d="M 0,0 L 540,0 L 540,120 L 0,300 Z" fill="#1e171a"/>'
  '<g filter="url(#dof)"><path d="M 380,60 L 480,30 L 480,170 L 380,200 Z" fill="#c9c4d8"/><path d="M 428,46 L 432,45 L 432,186 L 428,187 Z" fill="#2a2024"/>'
  + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="40" fill="{c}"/>' for x, y, w, c in [(20,320,90,"#4a3a30"),(20,360,90,"#3e3028"),(30,280,70,"#5a4638"),(430,330,90,"#4a3a30"),(440,370,80,"#3e3028")]) + '</g>'
  + beam("380,60 480,30 300,960 40,960", "beamW", .85) + motes(80, 200, 460, 680, 30, "#fff0dc", 19) +
  fig("c-mek", 270, 430, 1.6, .9) +
  '<path d="M 40,560 L 500,560 L 520,600 L 20,600 Z" fill="#5a4234"/><rect x="20" y="600" width="500" height="24" fill="#3a2a22"/>'
  '<g transform="translate(270,572)"><path d="M -110,-6 L 0,-14 L 0,20 L -112,24 Z" fill="#5a3a2a"/><path d="M 110,-6 L 0,-14 L 0,20 L 112,24 Z" fill="#4a2e22"/>'
  '<path d="M -100,-6 L -6,-12 L -6,16 L -102,20 Z" fill="#e8dfcc"/><path d="M 100,-6 L 6,-12 L 6,16 L 102,20 Z" fill="#ddd2bc"/>'
  '<rect x="-84" y="-8" width="30" height="22" fill="#8a8070"/><circle cx="-76" cy="0" r="4" fill="#f4f0e6"/><circle cx="-62" cy="0" r="4" fill="#c7bdab"/>'
  '<rect x="24" y="-8" width="30" height="22" fill="#8a8070"/><circle cx="32" cy="0" r="4" fill="#f4f0e6"/><circle cx="46" cy="0" r="4" fill="#f4f0e6"/></g>',
  "21 พ.ย. · 10:20", "ทุกรูป… หน้าของมาร์ธา|ถูกขูดออกทุกใบ", "Every photo. Martha's face, scratched out of every one.", "ห้องเก็บเอกสาร")))

# 13. Burnt doll on the steps
doll = '''<g transform="translate(270,800) scale(1.6)">
  <ellipse cx="0" cy="34" rx="40" ry="6" fill="#0c0a0e" opacity=".6"/>
  <path d="M -18,0 L 18,0 L 24,32 L -24,32 Z" fill="#e8e0d4"/><path d="M 4,0 L 18,0 L 24,32 L 8,32 Z" fill="#3a2a24"/>
  <path d="M 6,6 L 14,4 L 18,14 L 10,18 Z" fill="#1a1210"/>
  <circle cx="0" cy="-12" r="14" fill="#f0d8c0"/><path d="M 2,-26 C 14,-24 16,-12 12,-2 L 4,-6 Z" fill="#2a1a16"/>
  <path d="M -14,-14 C -16,-28 4,-30 10,-24 C 2,-26 -8,-22 -10,-12 Z" fill="#3a2a22"/>
  <circle cx="-5" cy="-12" r="1.6" fill="#1a1216"/><circle cx="4" cy="-12" r="1.6" fill="#1a1216"/>
  <rect x="-14" y="10" width="14" height="6" fill="#fbf8f2"/>
</g>'''
S.append(("ฉาก 13 · ตุ๊กตาไหม้", "ตุ๊กตาไหม้บนบันได อักเนสมาเก็บด้วยมือซ้าย เธอเดินได้ทั้งคืน", frame(
  '<rect width="540" height="960" fill="#3a3448"/>'
  '<g filter="url(#dof2)"><rect x="60" y="60" width="420" height="500" fill="#2e2830"/><rect x="200" y="200" width="140" height="360" fill="#1a1418"/></g>'
  + fig("agnesNC", 270, 360, 1.55, .78, .85) +
  '<path d="M 0,600 L 540,600 L 540,700 L 0,700 Z" fill="#4a4048"/><path d="M 0,600 L 540,600 L 540,612 L 0,612 Z" fill="#5a5058"/>'
  '<path d="M 0,700 L 540,700 L 540,960 L 0,960 Z" fill="#3e3640"/><path d="M 0,700 L 540,700 L 540,712 L 0,712 Z" fill="#544a56"/>'
  + doll + glow(270, 300, 300, "glowW", .25),
  "21 พ.ย. · 17:45", "เด็กนักเรียนเล่นแรงไปหน่อยค่ะ", "The students played a little too rough.", "ตุ๊กตาไหม้")))

# 14. Kitchen
kettle = '<g transform="translate(20,84)"><path d="M 0,10 C 0,-4 30,-4 30,10 L 32,30 L -2,30 Z" fill="#7a7a86"/><path d="M 30,12 L 42,4 L 40,10 L 32,20 Z" fill="#6a6a76"/><path d="M 4,0 C 6,-10 24,-10 26,0" fill="none" stroke="#3a3a44" stroke-width="3"/></g>'
S.append(("ฉาก 14 · ป้าแดงในครัว", "ป้าแดงกำลังจะเล่าความลับ แล้วอักเนสก็เดินเข้ามาพร้อมกาน้ำชา", frame(
  '<rect width="540" height="960" fill="#2a2228"/>'
  '<g filter="url(#dof)"><rect x="370" y="160" width="140" height="440" fill="#141014"/><rect x="40" y="200" width="200" height="16" fill="#4a3a30"/><circle cx="80" cy="190" r="16" fill="#5a5060"/><circle cx="130" cy="186" r="20" fill="#4a4250"/><circle cx="190" cy="192" r="14" fill="#5a5060"/></g>'
  + fig("agnesNC", 440, 380, 1.15, .7, .85, kettle) +
  fig("c-daeng", 230, 410, 1.6, .95) + fig("c-mek", 80, 480, 1.55, .85) +
  '<path d="M 0,580 L 540,580 L 540,960 L 0,960 Z" fill="#4a3a30"/><path d="M 0,580 L 540,580 L 540,600 L 0,600 Z" fill="#6a5240"/>'
  '<ellipse cx="200" cy="592" rx="40" ry="10" fill="#e8e0d4"/><ellipse cx="200" cy="588" rx="30" ry="6" fill="#d8c8a0"/>'
  '<path d="M 300,100 L 300,150" stroke="#1a1418" stroke-width="2"/><path d="M 288,150 L 312,150 L 306,166 L 294,166 Z" fill="#2a2228"/><circle cx="300" cy="170" r="7" fill="#fff4e0"/>'
  + glow(300, 175, 300, "glowW", .8) + beam("292,170 308,170 420,700 180,700", "beamW", .5) +
  '<g fill="#e8e4ee" opacity=".3" filter="url(#soft)"><ellipse cx="110" cy="150" rx="20" ry="30"/><ellipse cx="130" cy="110" rx="16" ry="24"/></g>' + motes(180, 200, 420, 560, 18, "#fff4e0", 21),
  "21 พ.ย. · 18:30", "ป้าได้ยินเพลงของป้า|เพลงที่ไม่มีใครในโลกนี้รู้จักอีกแล้ว", "I heard my song. A song no one else alive should know.", "ครัว")))

# 15. Video call split screen
S.append(("ฉาก 15 · วิดีโอคอลตีสาม", "เจมส์ได้ยินเสียงเด็กร้องเพลงในสายของเมฆ ก่อนระฆังจะดัง", frame(
  '<rect width="540" height="960" fill="#0e0c14"/>'
  '<svg x="0" y="0" width="540" height="470" viewBox="0 0 540 470"><rect width="540" height="470" fill="#181633"/>'
  + glow(500, 200, 300, "glowB", .8) + fig("james", 270, 210, 1.5, .95) +
  f'<g transform="translate(190,-190) scale(1.1)">{CAT}</g></svg>'
  '<rect x="0" y="466" width="540" height="8" fill="#0e0c14"/>'
  '<svg x="0" y="474" width="540" height="486" viewBox="0 0 540 486"><rect width="540" height="486" fill="#141018"/>'
  '<g filter="url(#dof)"><rect x="330" y="40" width="160" height="200" fill="#1a1e36"/>' + old_wing(345, 110, .55) + '</g>'
  + fig("c-mek", 200, 120, 1.45, .7, .85) +
  '<g transform="translate(450,380)"><ellipse cx="0" cy="0" rx="34" ry="12" fill="#2a2a30"/><g stroke="#141418" stroke-width="3"><line x1="-24" y1="0" x2="24" y2="0"/><line x1="-18" y1="-6" x2="18" y2="-6"/><line x1="-18" y1="6" x2="18" y2="6"/></g></g>'
  + glow(200, 260, 140, "glowC", .5) + '</svg>'
  '<rect x="400" y="490" width="120" height="30" rx="15" fill="#15121c" fill-opacity=".85"/><text x="460" y="511" text-anchor="middle" font-family="ui-monospace, monospace" font-size="15" fill="#e6e0f4">02:59</text>',
  "22 พ.ย. · 02:59", "มีเสียงเด็กร้องเพลงในสายมึง…|ชัดเลย", "There's a kid singing on your end. Clear as day.", "วิดีโอคอล")))

# 16. Bell tower, body found
S.append(("ฉาก 16 · หอระฆัง", "เมฆพบป้าแดงที่ฐานหอระฆัง มือกำบางอย่างไว้แน่น", frame(
  '<rect width="540" height="960" fill="#0e0d16"/>'
  '<rect width="540" height="600" fill="url(#nightSky)"/>'
  + bell_tower(320, 120, 1.0, swing=8) +
  '<path d="M 0,540 L 540,540 L 540,960 L 0,960 Z" fill="#1c1c24"/>'
  + fig("c-mek", 140, 470, 1.55, .72, .85) +
  beam("150,540 190,540 520,900 340,920", "beamW", .9) +
  '<g transform="translate(380,840)"><ellipse cx="0" cy="20" rx="120" ry="14" fill="#0a090e" opacity=".6"/>'
  '<path d="M -100,0 C -90,-16 60,-20 90,-4 L 92,14 C 40,20 -60,20 -100,12 Z" fill="#6c2b30"/><path d="M -40,-12 L 60,-14 L 64,12 L -38,14 Z" fill="#748894"/>'
  '<ellipse cx="108" cy="2" rx="18" ry="14" fill="#a9a4a6"/><path d="M -20,14 L -60,34 L -54,40 L -12,20 Z" fill="#c98f69"/><ellipse cx="-62" cy="38" rx="8" ry="6" fill="#c98f69"/>'
  '<rect x="-74" y="34" width="10" height="7" fill="#fbf8f2"/></g>'
  '<g transform="translate(220,880)"><circle r="9" fill="none" stroke="#b49a5a" stroke-width="2.4"/><path d="M 6,6 l 10,12 l 3,-2 M -6,6 l -8,14 l 3,1" stroke="#c9ad66" stroke-width="2.4" fill="none"/></g>'
  + motes(200, 560, 500, 900, 14, "#fff4e0", 23),
  "22 พ.ย. · 03:01", "แล้วผมก็เห็นป้าแดง", "Then I saw Auntie Daeng.", "หอระฆัง")))

# 17. Police at dawn
nunline = "".join(f'<g transform="translate({x},330) scale(.6)"><use href="#{c}"/></g>' for x, c in ((60,"mariam"),(130,"c-rosa"),(200,"agnesNC"),(410,"mariam"),(480,"agnesNC")))
S.append(("ฉาก 17 · ตำรวจ", "ธนา: 'ที่นี่ใส่ผ้าคลุมดำทุกคนครับคุณ'", frame(
  '<rect width="540" height="960" fill="url(#dawnSky)"/>'
  '<g filter="url(#dof2)" style="filter:brightness(.7)">' + nunline + '</g>'
  '<g filter="url(#dof2)"><rect x="0" y="470" width="540" height="10" fill="#e8c84a" opacity=".8"/><rect x="0" y="480" width="540" height="10" fill="#1a1a20" opacity=".8"/></g>'
  + fig("c-cat", 110, 470, 1.4, .85) + fig("c-thana", 300, 440, 1.7, .9) + fig("c-mek", 470, 500, 1.4, .82) +
  '<path d="M 0,640 L 540,640 L 540,960 L 0,960 Z" fill="#3a3a44"/>'
  + glow(40, 300, 300, "glowR", .8) + glow(520, 260, 200, "glowR", .5),
  "22 พ.ย. · 05:40", "ที่นี่ใส่ผ้าคลุมดำทุกคนครับคุณ", "Everyone here wears a black veil, sir.", "ตำรวจ")))

# 18. Chapel, ending
S.append(("ฉาก 18 · ทิ้งท้าย", "เมฆกระซิบชื่อมาร์ธาในโบสถ์มืด แล้วมีเสียงเด็กตอบว่า 'ค่ะ'", frame(
  '<rect width="540" height="960" fill="#0e0c12"/>'
  '<g filter="url(#dof)">' + stained_glass(330, 80, 150, 250, bright=.9) +
  "".join(f'<path d="M 0,{y} L 540,{y-20} L 540,{y-6} L 0,{y+14} Z" fill="#2a1e22"/><path d="M 0,{y+14} L 540,{y-6} L 540,{y+30} L 0,{y+50} Z" fill="#1a1216"/>' for y in (420, 500)) + '</g>'
  + beam("330,180 480,180 300,960 0,960", "beamC", .9) + motes(60, 300, 460, 700, 22, "#d6dcff", 25) +
  fig("c-mek", 250, 450, 1.35, .62, .85) +
  '<path d="M 0,560 L 540,540 L 540,600 L 0,620 Z" fill="#3a2a2c"/><path d="M 0,620 L 540,600 L 540,660 L 0,680 Z" fill="#221a1c"/>'
  '<path d="M -20,760 L 560,760 L 560,960 L -20,960 Z" fill="#08070a"/><path d="M -20,740 L 560,740 L 560,770 L -20,770 Z" fill="#1a1216"/>'
  '<rect x="430" y="690" width="10" height="50" fill="#e8e0d0"/><path d="M 435,690 C 430,670 444,650 436,628" fill="none" stroke="#c8c4d0" stroke-width="2" opacity=".5" filter="url(#moteFar)"/>',
  "22 พ.ย. · 23:58", "(เสียงเด็กผู้หญิงจากความมืด)|ค่ะ", "(a little girl's voice, from the dark) Yes?", "โบสถ์มืด")))

# ---------- page ----------
cards = "\n".join(f'<figure><div class="fr">{svg}</div><figcaption><b>{t}</b><br>{d}</figcaption></figure>' for t, d, svg in S)
html = f'''<title>EP1 ภาพฉาก</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: grid of 9:16 key frames (3 / 2 / 1 columns) with a caption under each. Single dark look by choice, matching the other sheets. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#8f86ff;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); margin:0; }}
body {{ font-family:var(--font); padding:24px max(16px, env(safe-area-inset-right,0px)) 40px max(16px, env(safe-area-inset-left,0px)); }}
.wrap {{ max-width:1100px; margin:0 auto; display:grid; gap:16px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
.bar {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; font-size:13px; color:var(--muted); }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:6px; padding:6px 12px; cursor:pointer; }}
button:hover {{ border-color:var(--muted); }} button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
button[aria-pressed="true"] {{ border-color:var(--accent); color:#fff; }}
.grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
@media (max-width:900px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
.fr {{ aspect-ratio:9/16; box-shadow:0 0 0 1px var(--line); border-radius:6px; overflow:hidden; }}
.fr svg {{ display:block; width:100%; height:100%; }}
body.nosubs .subs {{ display:none; }}
figcaption {{ font-size:13px; color:var(--muted); line-height:1.6; }} figcaption b {{ color:var(--ink); font-weight:500; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@500&display=swap">
{SHARED_DEFS}
<div class="wrap">
  <h1>แม่ชีคนที่สอง EP1 · ภาพฉาก<span>ฉากละหนึ่งภาพหลัก ทั้งหมด 18 ฉาก · 9:16</span></h1>
  <div class="bar"><span>ซับในภาพคือประโยคเด่นของฉากนั้น</span><button id="t" type="button" aria-pressed="true">ซับ</button></div>
  <div class="grid">
{cards}
  </div>
</div>
<script>
const b = document.getElementById('t');
b.addEventListener('click', () => {{
  const on = b.getAttribute('aria-pressed') !== 'true';
  b.setAttribute('aria-pressed', String(on));
  document.body.classList.toggle('nosubs', !on);
}});
</script>'''
open(os.path.join(HERE, "scenes.html"), "w").write(html)
print("wrote scenes.html", len(html) // 1024, "KB")
