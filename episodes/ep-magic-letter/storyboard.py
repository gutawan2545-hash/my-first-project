# สร้าง storyboard.html: สตอรี่บอร์ดเต็มทั้งคลิป (ตาม script.md v12e) เฟรม 9:16 (540x960)
# ฉากละเอียด มีเฟอร์นิเจอร์และของประกอบเยอะ · กรุงเทพโทนสว่างพาสเทล · โลกเวทมนตร์กลางคืน
# เม็ดฟิล์มละเอียดเฉพาะพื้นหลัง เห็นชัดขึ้นในบริเวณสีเข้ม (blend แบบ screen)
# ใช้ตัวละครจาก cast.html (ดึงบล็อก <defs> มาใช้ซ้ำ ไม่วาดหน้าใหม่)
import pathlib, re, random, math
HERE = pathlib.Path(__file__).parent
cast = (HERE / "cast.html").read_text()
DEFS = re.search(r'<svg width="0" height="0"[^>]*><defs>(.*?)</defs></svg>', cast, re.S).group(1)

TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
SUB_TH = TH + ' font-weight="700" font-size="20" fill="#ffd84a" stroke="#1a1420" stroke-width="5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'
SUB_EN = 'font-family="Inter, sans-serif" font-weight="500" font-size="13" fill="#fff" stroke="#1a1420" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'
POP = TH + ' font-weight="700" fill="#fff4d0" stroke="#3a1e16" stroke-width="5" paint-order="stroke" stroke-linejoin="round"'

# ---------------- UI ----------------
def subs(th, en):
    y = 712 - (len(th) * 27 + len(en) * 17) / 2 + 20
    out = ""
    for line in th:
        out += f'<text x="270" y="{y:.0f}" {SUB_TH}>{line}</text>'; y += 27
    y += 2
    for line in en:
        out += f'<text x="270" y="{y:.0f}" {SUB_EN}>{line}</text>'; y += 17
    return f'<g data-ui="1">{out}</g>'

def badge(t):
    w = 22 + len(t) * 9.2
    return f'''<g data-ui="1" transform="translate(22,26)"><rect width="{w:.0f}" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8a6cd8" stroke-width="1.4"/>
    <text x="{w/2:.0f}" y="20" text-anchor="middle" {TH} font-weight="600" font-size="14" fill="#e8e2f4">{t}</text></g>'''

def card(x, y, w, t1, t2="", tx=None, ty=None):
    h = 62 if t2 else 44
    line = f'<path d="M {x + w/2:.0f},{y + h} L {tx},{ty}" stroke="#8a76b8" stroke-width="2" stroke-dasharray="5 4"/>' if tx is not None else ""
    sub = f'<text x="14" y="50" {TH} font-size="13" fill="#5a5260">{t2}</text>' if t2 else ""
    return f'<g data-ui="1">{line}<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="10" fill="#f6f1e6" stroke="#9a86c8" stroke-width="1.6"/><text x="14" y="28" {TH} font-size="15" font-weight="600" fill="#2a2430">{t1}</text>{sub}</g></g>'

def Z(svg, k, ay=600, ax=270):
    """ขยายพื้นหลังรอบแนวพื้น ให้ของในฉากใหญ่สมจริงเทียบกับคน"""
    return f'<g transform="translate({ax},{ay}) scale({k}) translate({-ax},{-ay})">{svg}</g>'

def pop(x, y, t, size=34, rot=-8):
    return f'<g data-ui="1"><text x="{x}" y="{y}" font-size="{size}" transform="rotate({rot} {x} {y})" {POP}>{t}</text></g>'

EYE = '<g transform="translate(500,40)" opacity=".75"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="#b18cff"/><circle r="4" fill="#1b1f2b"/></g>'
VIGN = '<rect width="540" height="960" fill="url(#vign)"/>'
BGGRAIN = VIGN + '<rect width="540" height="960" filter="url(#fgrain)" style="mix-blend-mode:screen" opacity=".22"/>'

def dust(cx, cy, w, h, n=14, seed=1, col="#fff8f0"):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, y = cx + r.uniform(-w/2, w/2), cy + r.uniform(-h/2, h/2)
        if r.random() < .5:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.8,1.6):.1f}" fill="{col}" opacity="{r.uniform(.55,.9):.2f}" filter="url(#glow)"/>'
        else:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,4):.1f}" fill="{col}" opacity="{r.uniform(.15,.3):.2f}" filter="url(#soft)"/>'
    return out

def shadow(cx, cy, rx, ry=12, o=.3):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#5a4a7a" opacity="{o}" filter="url(#shadow)"/>'

def speed(x0, y0, x1, n=6, seed=2, col="#ffffff"):
    r = random.Random(seed)
    return "".join(f'<path d="M {x0},{y0 + i*22} L {x1 + r.uniform(-30,30):.0f},{y0 + i*22}" stroke="{col}" stroke-width="{r.uniform(1.5,3):.1f}" stroke-linecap="round" opacity=".6"/>' for i in range(n))

def shafts(xs, top=0, h=760, o=.55):
    return "".join(f'<path d="M {x-40},{top} L {x+40},{top} L {x+120},{top+h} L {x-10},{top+h} Z" fill="url(#shaft)" opacity="{o*.45:.2f}"/>' for x in xs)

def clouds(seed=1, n=4, y0=40, y1=200, x0=0, x1=540):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, y, w = r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(70, 140)
        out += "".join(f'<ellipse cx="{x+dx*w:.0f}" cy="{y+dy*w*.3:.0f}" rx="{w*.5:.0f}" ry="{w*.28:.0f}" fill="url(#cloud)"/>' for dx, dy in [(-.4,.2),(0,0),(.4,.15)])
    return out

DEFS_SB = '''
<filter id="fgrain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="2" seed="7"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.8 -.95"/></filter>
<filter id="bgblur"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="bgblur2"><feGaussianBlur stdDeviation="2.4"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation=".7"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="7"/></filter>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2f8ee0"/><stop offset=".6" stop-color="#7cc0f0"/><stop offset="1" stop-color="#cfe8fa"/></linearGradient>
<linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".8"/><stop offset=".5" stop-color="#fff2fa" stop-opacity=".35"/><stop offset="1" stop-color="#e8f4ff" stop-opacity="0"/></linearGradient>
<radialGradient id="cloud"><stop offset=".55" stop-color="#ffffff" stop-opacity=".95"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<linearGradient id="roomwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d9c2a6"/><stop offset="1" stop-color="#ecdcc4"/></linearGradient>
<linearGradient id="shopwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8e1620"/><stop offset="1" stop-color="#a82430"/></linearGradient>
<linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121a36"/><stop offset="1" stop-color="#34447a"/></linearGradient>
<linearGradient id="hall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1e1a2c"/><stop offset="1" stop-color="#3e3240"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".6"/><stop offset="1" stop-color="#fff4fa" stop-opacity="0"/></linearGradient>
<radialGradient id="portal"><stop offset="0" stop-color="#fff6e0"/><stop offset=".35" stop-color="#f4d6a0" stop-opacity=".9"/><stop offset="1" stop-color="#b18cff" stop-opacity="0"/></radialGradient>
<radialGradient id="warm"><stop offset="0" stop-color="#fff4dc"/><stop offset=".5" stop-color="#ffe2b8" stop-opacity=".55"/><stop offset="1" stop-color="#ffe2b8" stop-opacity="0"/></radialGradient>
<linearGradient id="wallshade" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#5a3a2a" stop-opacity=".18"/><stop offset=".35" stop-color="#5a3a2a" stop-opacity="0"/><stop offset=".75" stop-color="#5a3a2a" stop-opacity="0"/><stop offset="1" stop-color="#5a3a2a" stop-opacity=".2"/></linearGradient>
<radialGradient id="vign" cx=".5" cy=".45" r=".75"><stop offset=".55" stop-color="#1a1220" stop-opacity="0"/><stop offset="1" stop-color="#1a1220" stop-opacity=".35"/></radialGradient>
<pattern id="tiles" width="40" height="40" patternUnits="userSpaceOnUse"><rect width="40" height="40" fill="#e2d8c8"/><rect width="20" height="20" fill="#c8baa4"/><rect x="20" y="20" width="20" height="20" fill="#c8baa4"/><rect width="40" height="1" fill="#a89a86"/><rect width="1" height="40" fill="#a89a86"/></pattern>
<pattern id="terrazzo" width="30" height="30" patternUnits="userSpaceOnUse"><rect width="30" height="30" fill="#e2d6c8"/><circle cx="6" cy="8" r="1.6" fill="#c8b0bc"/><circle cx="20" cy="4" r="1.2" fill="#b8c4d8"/><circle cx="14" cy="20" r="1.8" fill="#d0a8b0"/><circle cx="26" cy="24" r="1.2" fill="#c8b0bc"/></pattern>
<pattern id="stone" width="60" height="34" patternUnits="userSpaceOnUse"><rect width="60" height="34" fill="#3a3346"/><rect x="1" y="1" width="58" height="15" fill="#443c52"/><rect x="-29" y="18" width="58" height="15" fill="#40384e"/><rect x="31" y="18" width="58" height="15" fill="#40384e"/></pattern>
'''

def frame(inner):
    return f'<svg viewBox="0 0 540 960" role="img"><defs><clipPath id="fr"><rect width="540" height="960"/></clipPath></defs><g clip-path="url(#fr)">{inner}</g></svg>'

SK, SKS = "#fbe9dc", "#efcab4"     # ผิวซิ่ง

# ---------------- ห้องนอน ----------------
def fan(x, y, s=1.0):
    spokes = "".join(f'<path d="M 0,-160 L {36*math.cos(a/12*6.283):.1f},{-160+36*math.sin(a/12*6.283):.1f}" stroke="#e8f0f8" stroke-width="1"/>' for a in range(12))
    return f'''<g transform="translate({x},{y}) scale({s})">
    <ellipse cx="0" cy="0" rx="30" ry="6" fill="#c8c0d8"/><rect x="-4" y="-130" width="8" height="130" fill="#e8e4f0"/><rect x="-4" y="-130" width="3" height="130" fill="#fff"/>
    <rect x="-10" y="-60" width="20" height="14" rx="4" fill="#d8d2e4"/><circle cx="-4" cy="-53" r="2" fill="#8ac8a0"/><circle cx="3" cy="-53" r="2" fill="#c8c0d8"/>
    <circle cx="0" cy="-160" r="36" fill="#bfe0f4" opacity=".55"/>{spokes}<circle cx="0" cy="-160" r="36" fill="none" stroke="#e8f0f8" stroke-width="3"/>
    <path d="M 0,-160 C 10,-180 26,-176 22,-164 Z M 0,-160 C -18,-150 -24,-136 -12,-136 Z M 0,-160 C 8,-142 22,-140 24,-150 Z" fill="#8ab8e0"/><circle cx="0" cy="-160" r="6" fill="#6a9ac8"/>
    <rect x="-10" y="-200" width="20" height="10" rx="4" fill="#d8d2e4"/></g>'''

def clock(x, y, r=22, h=6, m=30):
    ha, ma = (h % 12 + m/60) / 12 * 6.283 - 1.5708, m / 60 * 6.283 - 1.5708
    ticks = "".join(f'<circle cx="{(r-4)*math.cos(k/12*6.283):.1f}" cy="{(r-4)*math.sin(k/12*6.283):.1f}" r="1.2" fill="#8a7a9a"/>' for k in range(12))
    return f'''<g transform="translate({x},{y})"><circle r="{r+3}" fill="#e88aa8"/><circle r="{r}" fill="#fffaf6"/>{ticks}
    <path d="M 0,0 L {r*.5*math.cos(ha):.1f},{r*.5*math.sin(ha):.1f}" stroke="#3a2a40" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M 0,0 L {r*.8*math.cos(ma):.1f},{r*.8*math.sin(ma):.1f}" stroke="#3a2a40" stroke-width="1.6" stroke-linecap="round"/><circle r="2" fill="#c43a3a"/></g>'''

def poster(x, y, w, h, kind="idol"):
    inner = {
      "idol": f'<rect x="4" y="4" width="{w-8}" height="{h-8}" fill="#f4c8d8"/><circle cx="{w/2}" cy="{h*.42}" r="{w*.2}" fill="#fbe2d0"/><path d="M {w*.28},{h*.38} C {w*.3},{h*.16} {w*.7},{h*.16} {w*.72},{h*.38} Z" fill="#2a2030"/><rect x="{w*.22}" y="{h*.62}" width="{w*.56}" height="{h*.3}" fill="#8ab8e0"/><text x="{w/2}" y="{h*.95}" text-anchor="middle" font-family="Inter" font-size="{w*.12:.0f}" font-weight="800" fill="#c0306a">TOUR</text>',
      "game": f'<rect x="4" y="4" width="{w-8}" height="{h-8}" fill="#1e2a40"/><path d="M {w*.2},{h*.7} L {w*.5},{h*.25} L {w*.8},{h*.7} Z" fill="#7d74e6"/><circle cx="{w/2}" cy="{h*.55}" r="{w*.1}" fill="#ffd84a"/><text x="{w/2}" y="{h*.9}" text-anchor="middle" font-family="Inter" font-size="{w*.13:.0f}" font-weight="800" fill="#8fd19e">LEVEL UP</text>',
    }[kind]
    return f'<g transform="translate({x},{y}) rotate({random.Random(x).uniform(-3,3):.1f})"><rect width="{w}" height="{h}" fill="#fff"/>{inner}<circle cx="{w/2}" cy="3" r="2.4" fill="#c43a3a"/></g>'

def calendar_cn(x, y):
    return f'''<g transform="translate({x},{y})"><rect width="58" height="86" fill="#c8323a"/><rect x="4" y="18" width="50" height="62" fill="#fff6ee"/>
    <text x="29" y="14" text-anchor="middle" font-family="serif" font-size="11" font-weight="700" fill="#f0d070">福</text>
    <text x="29" y="54" text-anchor="middle" font-family="Inter" font-size="28" font-weight="800" fill="#c8323a">23</text><text x="29" y="72" text-anchor="middle" {TH} font-size="9" fill="#8a4a4a">พฤหัส</text></g>'''

def window_view(x, y, w, h, grille=True, curtain=True):
    """หน้าต่างตึกแถว เห็นตึกฝั่งตรงข้าม ป้าย แอร์ สายไฟ ฟ้าอ่อน"""
    g = [f'<clipPath id="wv{x}_{y}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#wv{x}_{y})">',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sky)"/>', clouds(x, 2, y + 10, y + 50, x, x + w),
         f'<rect x="{x-10}" y="{y+h*.35:.0f}" width="{w*.55:.0f}" height="{h}" fill="#d98f7a"/><rect x="{x+w*.5:.0f}" y="{y+h*.25:.0f}" width="{w*.6:.0f}" height="{h}" fill="#e9d8b8"/>',
         "".join(f'<rect x="{x+6+k*30}" y="{y+h*.45:.0f}" width="18" height="24" fill="#5f8cbc"/>' for k in range(int(w*.5/30))),
         "".join(f'<rect x="{x+w*.55+k*30:.0f}" y="{y+h*.35:.0f}" width="18" height="24" fill="#5f8cbc"/>' for k in range(int(w*.5/30))),
         f'<rect x="{x+w*.56:.0f}" y="{y+h*.6:.0f}" width="34" height="22" fill="#f4f4f6"/><circle cx="{x+w*.56+12:.0f}" cy="{y+h*.6+11:.0f}" r="8" fill="#c8ccd6"/>',
         f'<rect x="{x+8}" y="{y+h*.62:.0f}" width="20" height="54" fill="#c8323a"/><text x="{x+18}" y="{y+h*.62+22:.0f}" text-anchor="middle" font-family="serif" font-size="12" fill="#f0d070">金</text>',
         f'<path d="M {x},{y+h*.3:.0f} C {x+w*.4:.0f},{y+h*.4:.0f} {x+w*.7:.0f},{y+h*.36:.0f} {x+w},{y+h*.3:.0f}" stroke="#6a6280" stroke-width="1.5" fill="none"/>',
         '</g>']
    if grille:
        bars = "".join(f'<rect x="{x+k*w/8:.0f}" y="{y}" width="3" height="{h}"/>' for k in range(1, 8)) + "".join(f'<rect x="{x}" y="{y+k*h/5:.0f}" width="{w}" height="3"/>' for k in range(1, 5))
        g.append(f'<g fill="#ffffff">{bars}</g>')
    g.append(f'<path d="M {x-8},{y-8} L {x+w+8},{y-8} L {x+w+8},{y+h+8} L {x-8},{y+h+8} Z M {x},{y} L {x},{y+h} L {x+w},{y+h} L {x+w},{y} Z" fill="#ffffff" fill-rule="evenodd"/>')
    g.append(f'<rect x="{x-14}" y="{y+h+6}" width="{w+28}" height="10" fill="#f2ece2"/><rect x="{x-14}" y="{y+h+14}" width="{w+28}" height="4" fill="#b8a488"/>')
    if curtain:
        g.append(f'<path d="M {x-24},{y-14} L {x+30},{y-14} C {x+20},{y+h*.4:.0f} {x+10},{y+h*.7:.0f} {x+2},{y+h+10} L {x-24},{y+h+10} Z" fill="#d8566e" opacity=".95"/><path d="M {x-24},{y-14} L {x-6},{y-14} L {x-10},{y+h+10} L {x-24},{y+h+10} Z" fill="#e8748a"/>')
        g.append(f'<path d="M {x+w+24},{y-14} L {x+w-30},{y-14} C {x+w-20},{y+h*.4:.0f} {x+w-10},{y+h*.7:.0f} {x+w-2},{y+h+10} L {x+w+24},{y+h+10} Z" fill="#b8405a" opacity=".95"/>')
        g.append(f'<rect x="{x-30}" y="{y-20}" width="{w+60}" height="6" rx="3" fill="#b8a8c8"/>')
    return "".join(g)

def mattress(x, y, w=300):
    return f'''<g transform="translate({x},{y})">
    <rect x="0" y="0" width="{w}" height="40" rx="10" fill="#f4f0fa"/><rect x="0" y="28" width="{w}" height="14" rx="6" fill="#d8d0e6"/>
    <rect x="12" y="-14" width="80" height="26" rx="12" fill="#ffffff"/><rect x="12" y="-4" width="80" height="16" rx="8" fill="#e8e2f2"/></g>'''

def blanket(x, y, w=210):
    dots = "".join(f'<circle cx="{x+20+k*28}" cy="{y+8 - (k%2)*10}" r="3"/>' for k in range(int(w/28)))
    return f'''<path d="M {x},{y} C {x+40},{y-26} {x+w-40},{y-30} {x+w},{y-8} L {x+w+10},{y+34} L {x-6},{y+34} Z" fill="#8ab8e0"/>
    <path d="M {x},{y} C {x+40},{y-26} {x+w*.5},{y-28} {x+w*.6},{y-24} C {x+w*.4},{y-10} {x+20},{y+6} {x-6},{y+34} Z" fill="#a8cdec"/>
    <g fill="#ffffff" opacity=".7">{dots}</g>'''

def shelf(x, y, w=150, items="trophy"):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="8" fill="#c8a8b8"/><rect x="{x}" y="{y+8}" width="{w}" height="3" fill="#a88898"/>'
    if items == "trophy":
        for k, c in enumerate(["#e8c24a", "#c8ccd6", "#d9a05a", "#e8c24a"]):
            cx = x + 18 + k * 36
            out += f'<path d="M {cx-8},{y-30} L {cx+8},{y-30} C {cx+8},{y-18} {cx+4},{y-14} {cx},{y-14} C {cx-4},{y-14} {cx-8},{y-18} {cx-8},{y-30} Z" fill="{c}"/><rect x="{cx-2}" y="{y-14}" width="4" height="6" fill="{c}"/><rect x="{cx-7}" y="{y-8}" width="14" height="8" fill="#5a4a5a"/>'
    else:
        cols = ["#e86a7a", "#6a9ad8", "#8fd19e", "#f0c050", "#b18cff", "#e8a0b0", "#6ac8c0"]
        for k in range(int(w / 12)):
            hh = 22 + (k * 7) % 12
            out += f'<rect x="{x + 4 + k*12}" y="{y - hh}" width="10" height="{hh}" fill="{cols[k % len(cols)]}"/>'
    return out

def string_lights(x0, x1, y, sag=20, n=10):
    out = f'<path d="M {x0},{y} Q {(x0+x1)/2},{y+sag*2} {x1},{y}" fill="none" stroke="#8a7a9a" stroke-width="1.2"/>'
    for i in range(n):
        t = (i + .5) / n; px = x0 + (x1 - x0) * t; py = y + sag * 4 * t * (1 - t)
        out += f'<circle cx="{px:.0f}" cy="{py+4:.0f}" r="7" fill="url(#warm)"/><circle cx="{px:.0f}" cy="{py+4:.0f}" r="2.4" fill="#fff4dc"/>'
    return out

def plant(x, y, s=1.0, pot="#e88aa8"):
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M -14,0 L 14,0 L 10,26 L -10,26 Z" fill="{pot}"/><rect x="-16" y="-4" width="32" height="6" rx="2" fill="{pot}"/>
    <path d="M 0,-2 C -20,-20 -26,-40 -10,-50 C -6,-30 -2,-16 0,-2 Z" fill="#6aa878"/><path d="M 0,-2 C 18,-24 28,-38 16,-54 C 8,-34 4,-18 0,-2 Z" fill="#5a9868"/><path d="M 0,-2 C -2,-30 2,-48 8,-60 C 10,-40 6,-20 0,-2 Z" fill="#7ab888"/></g>'''

def clothes_rack(x, y):
    shirts = [("#f4f4f6", "#d8d8e0"), ("#8ab8e0", "#6a98c0"), ("#2a2a32", "#1a1a20"), ("#e8a0b0", "#c8808f")]
    out = f'<rect x="{x}" y="{y}" width="4" height="170" fill="#c8c0d8"/><rect x="{x+116}" y="{y}" width="4" height="170" fill="#b8b0c8"/><rect x="{x}" y="{y}" width="120" height="4" fill="#d8d2e4"/>'
    for k, (c1, c2) in enumerate(shirts):
        sx = x + 10 + k * 27
        out += f'<path d="M {sx+10},{y+4} L {sx+14},{y+10} L {sx+24},{y+16} L {sx+22},{y+70} L {sx-2},{y+70} L {sx-4},{y+16} L {sx+6},{y+10} Z" fill="{c1}"/><path d="M {sx+14},{y+10} L {sx+24},{y+16} L {sx+22},{y+70} L {sx+14},{y+70} Z" fill="{c2}"/>'
    out += f'<path d="M {x+10},{y+150} L {x+50},{y+150} L {x+46},{y+170} L {x+12},{y+170} Z" fill="#c8a8b8"/>'
    return out

def tv_cabinet(x, y):
    return f'''<g transform="translate({x},{y})"><rect x="0" y="0" width="150" height="56" fill="#e8d8e0"/><rect x="0" y="0" width="150" height="8" fill="#f4e8ee"/>
    <rect x="8" y="16" width="64" height="32" fill="#d8c4cc"/><rect x="78" y="16" width="64" height="32" fill="#d8c4cc"/><circle cx="66" cy="32" r="2" fill="#a88898"/><circle cx="84" cy="32" r="2" fill="#a88898"/>
    <rect x="18" y="-74" width="114" height="70" rx="4" fill="#1a1a22"/><rect x="24" y="-68" width="102" height="58" fill="#3a4a6a"/><path d="M 24,-68 L 80,-68 L 24,-26 Z" fill="#4a5c80"/>
    <rect x="68" y="-6" width="14" height="6" fill="#1a1a22"/><rect x="96" y="-14" width="40" height="10" rx="3" fill="#f4f4f6"/><rect x="100" y="-12" width="10" height="4" rx="2" fill="#7d74e6"/></g>'''

def mini_fridge(x, y):
    return f'''<g transform="translate({x},{y})"><rect width="70" height="96" rx="6" fill="#bfe0f4"/><rect width="18" height="96" rx="6" fill="#d6ecf8"/><rect x="0" y="34" width="70" height="3" fill="#9cc4e0"/>
    <rect x="58" y="12" width="4" height="16" rx="2" fill="#8aa8c8"/><rect x="58" y="44" width="4" height="22" rx="2" fill="#8aa8c8"/>
    <circle cx="26" cy="58" r="8" fill="#ffd84a"/><rect x="34" y="70" width="18" height="12" fill="#e86a7a" transform="rotate(10 43 76)"/><circle cx="46" cy="18" r="6" fill="#8fd19e"/></g>'''

def snacks(x, y):
    return f'''<g transform="translate({x},{y})"><path d="M 0,0 L 26,0 L 22,-34 L 4,-34 Z" fill="#f0c050"/><rect x="4" y="-30" width="18" height="8" fill="#c8432e"/>
    <rect x="32" y="-24" width="14" height="24" rx="3" fill="#c8243a"/><rect x="32" y="-16" width="14" height="6" fill="#f4f4f6"/>
    <rect x="50" y="-20" width="12" height="20" rx="3" fill="#6ac8a0"/><path d="M 68,-4 L 92,-4 L 88,-18 L 72,-18 Z" fill="#f4f4f6"/><rect x="72" y="-14" width="16" height="4" fill="#e86a5a"/></g>'''

def floor(y, kind="tiles"):
    fill = {"tiles": "url(#tiles)", "terrazzo": "url(#terrazzo)"}[kind]
    return f'<rect y="{y}" width="540" height="{960-y}" fill="{fill}"/><rect y="{y}" width="540" height="6" fill="#8a7a66"/><rect y="{y}" width="540" height="300" fill="url(#beam)" opacity=".1"/>'

def bedroom(blur="bgblur"):
    """ห้องนอนชั้นสามของซิ่ง: หน้าต่างเหล็กดัด ม่าน โปสเตอร์ ชั้นถ้วยรางวัล นาฬิกา ปฏิทินจีน ราวเสื้อ ทีวี ตู้เย็นเล็ก ไฟประดับ ต้นไม้"""
    stripes = '<rect width="540" height="600" fill="url(#wallshade)"/>'
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#roomwall)"/>{stripes}
    <rect y="560" width="540" height="40" fill="#b89a7a"/><rect y="560" width="540" height="4" fill="#d8c0a0"/>
    {window_view(300, 110, 190, 240)}
    {string_lights(20, 520, 70, 26, 12)}
    {poster(30, 120, 90, 120, "idol")}{poster(140, 150, 80, 100, "game")}
    {calendar_cn(236, 150)}{clock(260, 300)}
    {shelf(28, 300, 160, "trophy")}{shelf(28, 370, 160, "books")}
    {clothes_rack(30, 420)}{tv_cabinet(180, 520)}{plant(500, 360, .9, "#8ab8e0")}
    {floor(600, "tiles")}{mini_fridge(440, 504)}
    </g>'''

# ---------------- ร้านทอง ----------------
def gold_chains(x, y, w, h, n=8):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b8323e"/><rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" fill="#c8434e"/>'
    for k in range(n):
        cx = x + 14 + k * (w - 28) / (n - 1)
        out += f'<path d="M {cx-10:.0f},{y+12} C {cx-10:.0f},{y+h*.75:.0f} {cx+10:.0f},{y+h*.75:.0f} {cx+10:.0f},{y+12}" fill="none" stroke="#f0cc60" stroke-width="3"/><circle cx="{cx:.0f}" cy="{y+h*.72:.0f}" r="4" fill="#f4d878"/>'
    return out

def counter(x, y, w):
    trays = ""
    for k in range(int((w - 20) / 58)):
        trays += f'<rect x="{x+14+k*58}" y="{y+22}" width="48" height="26" rx="3" fill="#2a2030"/>' + "".join(f'<path d="M {x+18+k*58+j*10},{y+28} C {x+18+k*58+j*10},{y+44} {x+26+k*58+j*10},{y+44} {x+26+k*58+j*10},{y+28}" fill="none" stroke="#f0cc60" stroke-width="2"/>' for j in range(4))
    return f'''<rect x="{x}" y="{y}" width="{w}" height="70" fill="#e8f0f4" opacity=".45"/><rect x="{x}" y="{y}" width="{w}" height="4" fill="#ffffff"/>
    {trays}<rect x="{x}" y="{y+70}" width="{w}" height="90" fill="#6a2a1e"/><rect x="{x}" y="{y+70}" width="{w}" height="10" fill="#8a4030"/><rect x="{x}" y="{y+150}" width="{w}" height="10" fill="#4a1a12"/>'''

def lucky_cat(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})"><ellipse cx="0" cy="0" rx="20" ry="6" fill="#c8a8b8"/><path d="M -18,0 C -20,-30 20,-30 18,0 Z" fill="#fffaf6"/>
    <circle cx="0" cy="-34" r="16" fill="#fffaf6"/><path d="M -14,-44 L -10,-56 L -4,-46 Z M 14,-44 L 10,-56 L 4,-46 Z" fill="#fffaf6"/><path d="M -12,-46 L -10,-52 L -7,-46 Z" fill="#f4a8b8"/>
    <path d="M -8,-36 Q -5,-33 -2,-36 M 2,-36 Q 5,-33 8,-36" fill="none" stroke="#2a2030" stroke-width="1.4"/><circle cx="0" cy="-30" r="1.6" fill="#f08a9a"/>
    <path d="M 14,-30 C 22,-38 24,-52 18,-58 C 12,-54 12,-42 12,-34 Z" fill="#fffaf6"/><rect x="-10" y="-20" width="20" height="5" fill="#c8323a"/><circle cx="0" cy="-14" r="4" fill="#f0cc60"/>
    <ellipse cx="0" cy="-8" rx="8" ry="6" fill="#f0cc60"/></g>'''

def abacus(x, y):
    rods = "".join(f'<path d="M {x+10+k*9},{y+2} L {x+10+k*9},{y+32}" stroke="#6a3a2a" stroke-width="1"/>' for k in range(9))
    beads = "".join(f'<circle cx="{x+10+k*9}" cy="{y+8+r*9}" r="3.4" fill="{["#8a3a3a","#c8a060"][r%2]}"/>' for k in range(9) for r in range(3))
    return f'<rect x="{x}" y="{y}" width="96" height="34" rx="3" fill="none" stroke="#6a3a2a" stroke-width="4"/>{rods}{beads}'

def price_board(x, y):
    return f'''<g transform="translate({x},{y})"><rect width="150" height="96" rx="6" fill="#1e1a26"/><text x="75" y="22" text-anchor="middle" {TH} font-size="13" font-weight="700" fill="#f0cc60">ราคาทองวันนี้</text>
    <text x="12" y="46" {TH} font-size="11" fill="#e8e2f4">ทองแท่ง</text><text x="138" y="46" text-anchor="end" font-family="Inter" font-size="13" font-weight="700" fill="#ff8a7a">41,250</text>
    <text x="12" y="66" {TH} font-size="11" fill="#e8e2f4">รูปพรรณ</text><text x="138" y="66" text-anchor="end" font-family="Inter" font-size="13" font-weight="700" fill="#ff8a7a">41,750</text>
    <text x="12" y="86" {TH} font-size="11" fill="#e8e2f4">เหรียญเวทมนตร์</text><text x="138" y="86" text-anchor="end" font-family="Inter" font-size="13" font-weight="700" fill="#8fd19e">???</text></g>'''

def lantern(x, y, s=1.0, c="#d8323e"):
    return f'''<g transform="translate({x:.0f},{y:.0f}) scale({s})"><path d="M 0,-30 L 0,-16" stroke="#6a4a3a" stroke-width="1.4"/><rect x="-10" y="-18" width="20" height="5" fill="#f0cc60"/>
    <ellipse cx="0" cy="0" rx="20" ry="16" fill="{c}"/><path d="M -10,-14 C -14,-4 -14,4 -10,14 M 0,-16 L 0,16 M 10,-14 C 14,-4 14,4 10,14" fill="none" stroke="#a8222e" stroke-width="1.2"/>
    <ellipse cx="-6" cy="-4" rx="5" ry="8" fill="#ff8a8a" opacity=".5"/><rect x="-10" y="13" width="20" height="5" fill="#f0cc60"/><path d="M -4,18 L -4,30 M 0,18 L 0,32 M 4,18 L 4,30" stroke="#f0cc60" stroke-width="1.4"/></g>'''

def shrine(x, y):
    return f'''<g transform="translate({x},{y})"><rect x="-50" y="0" width="100" height="10" fill="#a8222e"/><rect x="-44" y="-70" width="88" height="70" fill="#c8323a"/><rect x="-36" y="-62" width="72" height="54" fill="#8a1a24"/>
    <path d="M -54,-70 L 54,-70 L 40,-90 L -40,-90 Z" fill="#e0a040"/><circle cx="-24" cy="-36" r="6" fill="url(#warm)"/><circle cx="24" cy="-36" r="6" fill="url(#warm)"/>
    <rect x="-8" y="-50" width="16" height="30" rx="6" fill="#f0cc60" opacity=".85"/><rect x="-20" y="-14" width="40" height="8" fill="#e0a040"/></g>'''

def shutter_door(x, y, w, h, open_frac=.6):
    oh = h * (1 - open_frac)
    slats = "".join(f'<rect x="{x}" y="{y+k*8}" width="{w}" height="2" fill="#a8a4b8"/>' for k in range(int(oh/8)))
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#sky)"/><rect x="{x}" y="{y+h*.5:.0f}" width="{w}" height="{h*.5:.0f}" fill="#7a7a84"/>
    <rect x="{x+20}" y="{y+h*.3:.0f}" width="50" height="{h*.4:.0f}" fill="#d98f7a"/><rect x="{x+w-80}" y="{y+h*.25:.0f}" width="60" height="{h*.45:.0f}" fill="#e9d8b8"/>
    <rect x="{x}" y="{y}" width="{w}" height="{oh:.0f}" fill="#a9a6a0"/>{slats}
    <rect x="{x-6}" y="{y}" width="6" height="{h}" fill="#a8a4b8"/><rect x="{x+w}" y="{y}" width="6" height="{h}" fill="#a8a4b8"/>'''

def gold_shop(blur="bgblur"):
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#shopwall)"/>
    {gold_chains(20, 100, 230, 150, 9)}{gold_chains(290, 100, 230, 150, 9)}
    <rect x="160" y="20" width="220" height="56" fill="#a8222e"/><rect x="166" y="26" width="208" height="44" fill="none" stroke="#f0cc60" stroke-width="2"/>
    <text x="270" y="58" text-anchor="middle" {TH} font-size="26" font-weight="700" fill="#f4d878">ห้างทอง ซิ่งเฮง</text>
    {lantern(120, 60)}{lantern(420, 60)}
    {shrine(450, 340)}{price_board(30, 270)}{clock(300, 300, 20, 7, 0)}{calendar_cn(200, 268)}
    {shutter_door(196, 360, 150, 200, .7)}
    <rect x="20" y="380" width="160" height="12" fill="#5a2a1e"/>{plant(60, 380, .8, "#c8323a")}{lucky_cat(140, 380, .9)}
    {floor(600, "terrazzo")}
    </g>'''

# ---------------- ถนนเยาวราช ----------------
def vsign(x, y, w, h, text, bg="#c8323a", fg="#f4d878"):
    chars = "".join(f'<text x="{x+w/2}" y="{y+18+i*18}" text-anchor="middle" {TH} font-size="14" font-weight="700" fill="{fg}">{c}</text>' for i, c in enumerate(text))
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{bg}"/><rect x="{x+3}" y="{y+3}" width="{w-6}" height="{h-6}" rx="2" fill="none" stroke="{fg}" stroke-width="1" opacity=".6"/>{chars}'

def street_facades(horizon=640, seed=5):
    r = random.Random(seed)
    cols = ["#e9d8b8", "#d98f7a", "#7fb4b0", "#c9c3b8", "#e6a88e"]
    awn = ["#c8323a", "#1f5fbf", "#2f8a5a", "#e8743a", "#7a3aa8"]
    g = []
    for i, bx in enumerate(range(-60, 600, 130)):
        top = horizon - 520 + r.randint(-30, 30)
        g.append(f'<rect x="{bx}" y="{top}" width="130" height="{horizon-top}" fill="{cols[i % 5]}"/><rect x="{bx}" y="{top}" width="130" height="10" fill="#ffffff" opacity=".6"/>')
        for fy in range(top + 40, horizon - 200, 110):
            g.append(f'<rect x="{bx+16}" y="{fy}" width="98" height="70" fill="#5f8cbc"/><rect x="{bx+16}" y="{fy}" width="40" height="70" fill="#8ab4dc"/>')
            g.append("".join(f'<rect x="{bx+16+k*14}" y="{fy}" width="2" height="70" fill="#ffffff"/>' for k in range(8)))
            g.append(f'<rect x="{bx+10}" y="{fy+72}" width="110" height="6" fill="#ffffff" opacity=".8"/>')
            if r.random() < .5:
                g.append(f'<rect x="{bx+80}" y="{fy+40}" width="30" height="20" fill="#f4f4f6"/><circle cx="{bx+91}" cy="{fy+50}" r="7" fill="#c8ccd6"/>')
            if r.random() < .5:
                g.append(f'<path d="M {bx+18},{fy+20} L {bx+70},{fy+20}" stroke="#8a7a9a" stroke-width="1"/>' + "".join(f'<rect x="{bx+22+k*14}" y="{fy+20}" width="10" height="{14+(k%2)*6}" fill="{["#f4a8b8","#8ab8e0","#f4f4f6","#8fd19e"][k%4]}"/>' for k in range(4)))
        g.append(f'<rect x="{bx}" y="{horizon-190}" width="130" height="190" fill="#a9a6a0"/>' + "".join(f'<rect x="{bx}" y="{horizon-190+k*12}" width="130" height="2" fill="#8a8780"/>' for k in range(8)))
        g.append(f'<rect x="{bx+10}" y="{horizon-92}" width="110" height="92" fill="#5a4a4a"/><rect x="{bx+20}" y="{horizon-80}" width="90" height="40" fill="#f0c860" opacity=".75"/>')
        g.append(f'<path d="M {bx},{horizon-196} L {bx+130},{horizon-196} L {bx+120},{horizon-170} L {bx+10},{horizon-170} Z" fill="{awn[i % 5]}"/>')
    for k, (t, bgc) in enumerate([("ห้างทอง", "#c8323a"), ("ยาจีน", "#2f6b4a"), ("โจ๊ก", "#c8432e"), ("ขนมเปี๊ยะ", "#a8222e"), ("ข้าวมันไก่", "#2a3a6a")]):
        g.append(vsign(20 + k * 108, horizon - 470 + (k % 2) * 40, 34, 22 + 18 * len(t), t, bgc))
    g.append(f'<path d="M -10,{horizon-500} C 160,{horizon-460} 380,{horizon-470} 560,{horizon-500} M -10,{horizon-480} C 180,{horizon-440} 360,{horizon-445} 560,{horizon-478} M -10,{horizon-460} C 200,{horizon-430} 340,{horizon-430} 560,{horizon-455}" fill="none" stroke="#6a6280" stroke-width="1.6"/>')
    g.append("".join(lantern(40 + k * 92, horizon - 430 + 18 * math.sin(k), .8) for k in range(6)))
    return "".join(g)

def pole(x, horizon):
    return f'<rect x="{x}" y="{horizon-560}" width="12" height="560" fill="#c8c4d4"/><rect x="{x}" y="{horizon-560}" width="4" height="560" fill="#e8e4f0"/><rect x="{x-20}" y="{horizon-540}" width="52" height="6" fill="#a8a4b8"/><rect x="{x-10}" y="{horizon-480}" width="32" height="40" rx="4" fill="#a8a4b8"/>'

def food_cart(x, y, s=1.0, label="ลูกชิ้นปิ้ง"):
    stripes = "".join(f'<path d="M {-80+k*32},-140 L {-64+k*32},-140 L {-56+k*32},-160 L {-70+k*32},-160 Z" fill="#ffffff"/>' for k in range(5))
    pots = "".join(f'<rect x="{-50+k*16}" y="-50" width="10" height="22" rx="3" fill="#c87a4a"/>' for k in range(7))
    return f'''<g transform="translate({x},{y}) scale({s})">
    <rect x="-60" y="-70" width="120" height="70" fill="#f4f4f6"/><rect x="-60" y="-70" width="120" height="12" fill="#e86a7a"/>
    <rect x="-54" y="-54" width="108" height="30" fill="#bfe0f4" opacity=".7"/>{pots}
    <rect x="-62" y="-140" width="4" height="70" fill="#c8c4d4"/><rect x="58" y="-140" width="4" height="70" fill="#c8c4d4"/>
    <path d="M -80,-140 L 80,-140 L 70,-160 L -70,-160 Z" fill="#f08a9a"/>{stripes}
    <text x="0" y="-8" text-anchor="middle" {TH} font-size="14" font-weight="700" fill="#c8432e">{label}</text>
    <circle cx="-40" cy="8" r="12" fill="#3a3a44"/><circle cx="40" cy="8" r="12" fill="#3a3a44"/><circle cx="-40" cy="8" r="5" fill="#c8ccd6"/><circle cx="40" cy="8" r="5" fill="#c8ccd6"/>
    <path d="M -20,-80 C -26,-100 -14,-110 -20,-130 M 10,-80 C 4,-100 16,-110 10,-130" fill="none" stroke="#ffffff" stroke-width="5" stroke-linecap="round" opacity=".55"/></g>'''

def stools(x, y, n=3):
    cols = ["#e86a7a", "#6a9ad8", "#8fd19e"]
    return "".join(f'<g transform="translate({x+k*34},{y})"><rect x="-14" y="-26" width="28" height="6" rx="3" fill="{cols[k%3]}"/><path d="M -12,-20 L -14,0 M 12,-20 L 14,0" stroke="{cols[k%3]}" stroke-width="4"/></g>' for k in range(n))

def tuktuk(x, y, s=1.0, rot=0):
    """ตุ๊กตุ๊กไทย หันข้างเต็ม หน้ารถไปทางซ้าย: จมูกรถไฟหน้าดวงเดียว กระจกหน้าเอียง หลังคายาวขอบโครเมียม ป้าย TAXI ราวโครเมียมข้างเบาะ เบาะแดง ล้อหลังมีบังโคลนโครเมียม"""
    stripes = "".join(f'<rect x="{-6+k*14}" y="-34" width="8" height="3" fill="#f4d878"/>' for k in range(8))
    return f'''<g transform="translate({x},{y}) rotate({rot}) scale({s})">
    <path d="M 76,-4 L 132,-4 L 132,4 L 76,4 Z" fill="#9aa0aa"/><circle cx="136" cy="0" r="4" fill="#5a5e6a"/>
    <circle cx="-118" cy="0" r="20" fill="#16161c"/><circle cx="-118" cy="0" r="9" fill="#d8dde6"/><circle cx="-118" cy="0" r="3" fill="#16161c"/>
    <circle cx="84" cy="0" r="24" fill="#16161c"/><circle cx="84" cy="0" r="11" fill="#d8dde6"/><circle cx="84" cy="0" r="4" fill="#16161c"/>
    <path d="M -144,-8 C -146,-30 -138,-52 -122,-66 L -100,-66 L -100,-14 L -134,-14 C -140,-14 -144,-12 -144,-8 Z" fill="#1f5fbf"/>
    <path d="M -144,-8 C -146,-28 -140,-46 -128,-60 L -120,-60 C -130,-46 -134,-28 -132,-14 L -134,-14 C -140,-14 -144,-12 -144,-8 Z" fill="#4a86e0"/>
    <circle cx="-138" cy="-38" r="9" fill="#d8dde6"/><circle cx="-138" cy="-38" r="6" fill="#fff6d0"/>
    <path d="M -146,-20 L -130,-20 M -146,-14 L -132,-14" stroke="#d8dde6" stroke-width="2"/>
    <path d="M -142,-16 C -142,-34 -94,-34 -94,-16" fill="none" stroke="#d8dde6" stroke-width="5"/>
    <path d="M -122,-66 L -102,-150 L -94,-150 L -112,-66 Z" fill="#d8dde6"/><path d="M -116,-68 L -98,-146 L -78,-146 L -78,-70 Z" fill="#a8d4f0" opacity=".75"/>
    <path d="M -100,-66 L 60,-66 L 64,-14 L -100,-14 Z" fill="#1f5fbf"/><path d="M 0,-66 L 60,-66 L 64,-14 L 10,-14 Z" fill="#174a98"/>
    <path d="M -100,-48 L 62,-48" stroke="#d8dde6" stroke-width="2.4"/>
    <path d="M 60,-74 C 80,-80 110,-76 118,-56 L 120,-14 L 60,-14 Z" fill="#1f5fbf"/><path d="M 96,-76 C 108,-72 116,-66 118,-56 L 120,-14 L 100,-14 Z" fill="#174a98"/>
    <path d="M 58,-20 C 58,-46 112,-46 112,-20" fill="none" stroke="#d8dde6" stroke-width="6"/>
    {stripes}<rect x="70" y="-34" width="40" height="3" fill="#f4d878"/>
    <circle cx="116" cy="-44" r="4" fill="#e8323e"/>
    <path d="M -96,-66 L -96,-110 L -80,-110 L -80,-66 Z" fill="#2a2a32"/>
    <path d="M -10,-66 L -10,-118 C -10,-124 0,-126 6,-124 L 6,-66 Z" fill="#c8243a"/><path d="M 6,-104 L 58,-104 L 58,-66 L 6,-66 Z" fill="#c8243a"/><path d="M 6,-104 L 58,-104 L 58,-98 L 6,-98 Z" fill="#e8434e"/>
    <path d="M -100,-158 L 122,-158 C 126,-158 128,-154 126,-150 L 120,-140 L -104,-140 L -108,-150 C -108,-155 -104,-158 -100,-158 Z" fill="#14264a"/>
    <path d="M -108,-150 L 126,-150 L 124,-146 L -108,-146 Z" fill="#d8dde6"/><path d="M -104,-140 L 120,-140 L 120,-136 L -104,-136 Z" fill="#d8dde6"/>
    <rect x="-34" y="-176" width="56" height="18" rx="3" fill="#f4f4f6"/><text x="-6" y="-162" text-anchor="middle" font-family="Inter" font-size="12" font-weight="800" fill="#c8243a">TAXI</text>
    <path d="M -12,-136 L -12,-66 M 116,-136 L 116,-74" stroke="#d8dde6" stroke-width="4"/>
    <path d="M 6,-84 L 60,-84 M 6,-74 L 60,-74" stroke="#d8dde6" stroke-width="2.4"/>
    <path d="M -94,-128 L -14,-128" stroke="#f4d878" stroke-width="2" stroke-dasharray="4 3"/>
    <text x="-40" y="-24" text-anchor="middle" font-family="Inter" font-size="10" font-weight="800" fill="#f4d878">BANGKOK</text>
    </g>'''

def driver(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M -18,0 L 18,0 L 16,-40 C 10,-48 -10,-48 -16,-40 Z" fill="#e88a3a"/>
    <rect x="-5" y="-54" width="10" height="10" fill="#d9a57c"/><circle cx="0" cy="-64" r="14" fill="#d9a57c"/><path d="M -15,-66 C -14,-82 14,-82 15,-66 Z" fill="#2a3a5c"/><path d="M -4,-70 L -22,-68 L -15,-64 Z" fill="#2a3a5c"/>
    <circle cx="-5" cy="-62" r="3.4" fill="#fff"/><circle cx="5" cy="-62" r="3.4" fill="#fff"/><circle cx="-5" cy="-62" r="1.4" fill="#1a1a20"/><circle cx="5" cy="-62" r="1.4" fill="#1a1a20"/><ellipse cx="0" cy="-54" rx="3" ry="2.6" fill="#7a2e2a"/></g>'''

def yaowarat_street(blur="bgblur", horizon=640):
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#sky)"/>{clouds(2, 4, 20, 140)}
    {street_facades(horizon)}{pole(470, horizon)}
    <rect y="{horizon}" width="540" height="{960-horizon}" fill="#7a7a84"/><rect y="{horizon}" width="540" height="40" fill="#c8c0b0"/><rect y="{horizon+40}" width="540" height="4" fill="#9a948a"/>
    <path d="M 0,{horizon+150} L 540,{horizon+150}" stroke="#ffffff" stroke-width="5" stroke-dasharray="44 28"/>
    {food_cart(70, horizon+30, .8, "โจ๊ก")}{stools(140, horizon+36, 3)}
    </g>'''

# ---------------- ศาลพระภูมิ ----------------
def spirit_house(x, y, s=1.0, door_open=False):
    door = '<path d="M -16,-4 L -16,-60 C -16,-72 16,-72 16,-60 L 16,-4 Z" fill="url(#portal)"/>' if door_open else '<path d="M -16,-4 L -16,-60 C -16,-72 16,-72 16,-60 L 16,-4 Z" fill="#7a1e24"/><path d="M 0,-4 L 0,-66" stroke="#e0b84a" stroke-width="1.4"/>'
    return f'''<g transform="translate({x},{y}) scale({s})">
    <rect x="-10" y="0" width="20" height="160" fill="#e8e0d4"/><rect x="-10" y="0" width="7" height="160" fill="#f8f2ea"/>
    <rect x="-74" y="-8" width="148" height="12" fill="#d8cfc2"/><rect x="-74" y="-8" width="148" height="4" fill="#f0e8dc"/>
    <rect x="-50" y="-90" width="100" height="84" fill="#f4eee4"/><rect x="-50" y="-90" width="34" height="84" fill="#fffaf2"/><rect x="20" y="-90" width="30" height="84" fill="#ddd4c6"/>
    {door}
    <path d="M -64,-90 L 64,-90 L 40,-130 L -40,-130 Z" fill="#d8434e"/><path d="M -64,-90 L -40,-130 L -20,-130 L -40,-90 Z" fill="#ec6a72"/>
    <path d="M -40,-130 L 40,-130 L 20,-170 L -20,-170 Z" fill="#d8434e"/><path d="M -20,-170 L 20,-170 L 0,-214 Z" fill="#f0cc60"/>
    <path d="M -64,-90 L -78,-106 M 64,-90 L 78,-106 M -40,-130 L -54,-146 M 40,-130 L 54,-146" stroke="#f0cc60" stroke-width="5" stroke-linecap="round"/>
    <path d="M -50,-90 L 50,-90 L 50,-84 L -50,-84 Z" fill="#f0cc60"/></g>'''

def garland(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
    <path d="M -20,0 C -20,30 20,30 20,0" fill="none" stroke="#ffffff" stroke-width="7"/><path d="M -20,0 C -20,30 20,30 20,0" fill="none" stroke="#f0e8d8" stroke-width="7" stroke-dasharray="3 3"/>
    <circle cx="0" cy="24" r="6" fill="#e86a7a"/><circle cx="0" cy="24" r="3" fill="#f0cc60"/>
    <path d="M -4,30 L -6,46 M 0,30 L 0,48 M 4,30 L 6,46" stroke="#e86a7a" stroke-width="2.4"/></g>'''

def zebra(x, y, s=1.0, blink=False):
    eye = '<path d="M -10,-38 Q -7,-35 -4,-38" fill="none" stroke="#1a1a20" stroke-width="1.6"/>' if blink else '<circle cx="-7" cy="-38" r="2" fill="#1a1a20"/>'
    return f'''<g transform="translate({x},{y}) scale({s})">
    <rect x="-14" y="-20" width="5" height="20" fill="#f8f8f8"/><rect x="8" y="-20" width="5" height="20" fill="#e4e4e4"/>
    <path d="M -18,-34 L 18,-34 L 18,-18 L -18,-18 Z" fill="#f8f8f8"/><g fill="#1a1a20"><rect x="-12" y="-34" width="3" height="16"/><rect x="-2" y="-34" width="3" height="16"/><rect x="8" y="-34" width="3" height="16"/></g>
    <path d="M -18,-34 L -20,-50 L -8,-52 L -4,-34 Z" fill="#f8f8f8"/><path d="M -20,-50 L -16,-56 L -12,-50 Z" fill="#1a1a20"/>
    <path d="M -26,-44 L -18,-48 L -16,-40 L -24,-38 Z" fill="#f8f8f8"/>{eye}</g>'''

def incense(x, y):
    return f'''<g transform="translate({x},{y})"><path d="M -14,0 L 14,0 L 10,14 L -10,14 Z" fill="#c8a060"/>
    <path d="M -4,0 L -8,-40 M 0,0 L 0,-44 M 4,0 L 8,-40" stroke="#a8323a" stroke-width="1.6"/><circle cx="-8" cy="-40" r="1.6" fill="#ff8a5a"/><circle cx="0" cy="-44" r="1.6" fill="#ff8a5a"/><circle cx="8" cy="-40" r="1.6" fill="#ff8a5a"/>
    <path d="M 0,-46 C -8,-60 8,-70 0,-86 C -6,-96 4,-104 0,-114" fill="none" stroke="#ffffff" stroke-width="3" opacity=".6"/></g>'''

def win_riders(x, y):
    out = f'<rect x="{x-30}" y="{y-112}" width="170" height="26" rx="4" fill="#f08a3a"/><text x="{x+55}" y="{y-94}" text-anchor="middle" {TH} font-size="13" font-weight="700" fill="#fff">วินมอเตอร์ไซค์</text>'
    for k in range(3):
        cx = x + k * 46
        out += f'<g transform="translate({cx},{y})"><path d="M -16,0 L 16,0 L 14,-50 C 8,-58 -8,-58 -14,-50 Z" fill="#f08a3a"/><text x="0" y="-26" text-anchor="middle" font-family="Inter" font-size="10" font-weight="800" fill="#fff">{k+11}</text>'
        out += '<rect x="-5" y="-64" width="10" height="10" fill="#d9a57c"/><circle cx="0" cy="-74" r="12" fill="#d9a57c"/><path d="M -12,-76 C -12,-90 12,-90 12,-76 Z" fill="#1d1a1e"/><circle cx="-4" cy="-72" r="1.6" fill="#1a1a20"/><circle cx="4" cy="-72" r="1.6" fill="#1a1a20"/></g>'
    return out

def tree(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M -10,0 L 10,0 L 6,-140 L -6,-140 Z" fill="#9a7a6a"/>
    <circle cx="0" cy="-170" r="60" fill="#8ac898"/><circle cx="-44" cy="-140" r="42" fill="#7ab888"/><circle cx="44" cy="-146" r="46" fill="#6aa878"/><circle cx="-16" cy="-196" r="34" fill="#a8dcb4"/></g>'''

def soi_entrance(blur="bgblur", horizon=660):
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#sky)"/>{clouds(3, 4, 20, 160)}
    {street_facades(horizon, 9)}
    <rect x="300" y="{horizon-150}" width="200" height="40" rx="4" fill="#2a5aa8"/><text x="400" y="{horizon-123}" text-anchor="middle" {TH} font-size="16" font-weight="700" fill="#fff">ซอยเยาวราช 6</text>
    {tree(500, horizon, .9)}
    <rect y="{horizon}" width="540" height="{960-horizon}" fill="#7a7a84"/><rect y="{horizon}" width="540" height="30" fill="#c8c0b0"/>
    {win_riders(330, horizon+10)}
    </g>'''

# ---------------- โลกเวทมนตร์ ----------------
def pingpong(y0, n=9, sag=40):
    out = f'<path d="M -10,{y0} Q 270,{y0+sag*2} 560,{y0}" fill="none" stroke="#1a1620" stroke-width="2"/>'
    for i in range(n):
        t = (i + .5) / n; x = -10 + 570 * t; y = y0 + sag * 4 * t * (1 - t) + 8
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="url(#warm)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff4dc"/>'
    return out

def stall(x, y, w, awning, goods="wands", label=""):
    stripes = "".join(f'<path d="M {x-w/2+k*w/6:.0f},{y} L {x-w/2+(k+1)*w/6:.0f},{y} L {x-w/2+(k+1)*w/6+4:.0f},{y-36} L {x-w/2+k*w/6+4:.0f},{y-36} Z" fill="{awning if k%2 else "#f2ead8"}"/>' for k in range(6))
    if goods == "potions":
        g = "".join(f'<g transform="translate({x-w/2+18+k*22:.0f},{y+96})"><rect x="-6" y="-24" width="12" height="24" rx="4" fill="{["#8fd19e","#b18cff","#ff8aa8","#6ac8e0"][k%4]}"/><rect x="-3" y="-30" width="6" height="7" fill="#c8a060"/></g>' for k in range(int((w-20)/22)))
    elif goods == "meatball":
        g = "".join(f'<g transform="translate({x-w/2+16+k*14:.0f},{y+98})"><path d="M 0,0 L 0,-40" stroke="#d8c09a" stroke-width="2.4"/><circle cy="-34" r="5" fill="#9a5a3a"/><circle cy="-22" r="5" fill="#a8683e"/><circle cy="-10" r="5" fill="#9a5a3a"/></g>' for k in range(int((w-20)/14)))
        g += f'<path d="M {x-20},{y+50} C {x-26},{y+30} {x-14},{y+20} {x-20},{y}" fill="none" stroke="#ffffff" stroke-width="5" opacity=".4"/>'
    else:
        g = "".join(f'<g transform="translate({x-w/2+20+k*26:.0f},{y+100}) rotate(-8)"><rect x="-2" y="-90" width="4" height="70" fill="#9a7444"/><path d="M -8,-20 L 8,-20 L 12,0 L -12,0 Z" fill="#c9a26a"/></g>' for k in range(int((w-20)/26)))
    lab = f'<rect x="{x-50}" y="{y+6}" width="100" height="24" rx="4" fill="#f2ead8"/><text x="{x}" y="{y+23}" text-anchor="middle" {TH} font-size="13" font-weight="700" fill="#8e1b24">{label}</text>' if label else ""
    return f'''<rect x="{x-w/2+4:.0f}" y="{y}" width="4" height="120" fill="#5a4a5a"/><rect x="{x+w/2-8:.0f}" y="{y}" width="4" height="120" fill="#5a4a5a"/>
    {stripes}<rect x="{x-w/2:.0f}" y="{y+100}" width="{w}" height="40" fill="#6a4a32"/><rect x="{x-w/2:.0f}" y="{y+100}" width="{w}" height="6" fill="#84603f"/>{g}{lab}'''

def crowd(y, n=10, seed=4):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, s = r.uniform(0, 540), r.uniform(.6, 1)
        c = r.choice(["#2a2440", "#342a50", "#3a2e4a"])
        out += f'<g transform="translate({x:.0f},{y}) scale({s:.2f})"><path d="M -18,0 L 18,0 L 14,-50 L -14,-50 Z" fill="{c}"/><circle cy="-60" r="12" fill="{c}"/><path d="M -16,-64 L 16,-64 L 4,-100 Z" fill="{c}"/></g>'
    return out

def magic_market(blur="bgblur2"):
    lanterns = "".join(f'<ellipse cx="{x}" cy="{y}" rx="9" ry="12" fill="#ff9a6a" opacity=".85"/><ellipse cx="{x}" cy="{y}" rx="22" ry="26" fill="url(#warm)"/>' for x, y in [(80,90),(200,60),(330,110),(460,70),(500,170),(140,180)])
    broom = lambda x, y, r, c: f'<g transform="translate({x},{y}) rotate({r})"><rect x="-40" y="-2" width="80" height="4" fill="#9a7444"/><path d="M 40,-6 L 58,0 L 40,6 Z" fill="#c9a26a"/><path d="M -10,-4 L 0,-24 L 10,-4 Z" fill="{c}"/></g>'
    return f'''<rect width="540" height="960" fill="url(#nightsky)"/>
    <g filter="url(#{blur})">{lanterns}{broom(120,220,-6,"#2a2440")}{broom(410,250,8,"#342a50")}
      {crowd(470, 9, 2)}
      {stall(90, 330, 170, "#2f5e8a", "potions", "ยาปรุงสำเร็จ")}{stall(450, 330, 170, "#2f6b4a", "brooms", "ไม้กวาดมือสอง")}
    </g>
    {pingpong(250, 9)}{pingpong(330, 8, 30)}
    <rect y="620" width="540" height="340" fill="#2e2638"/><rect y="620" width="540" height="6" fill="#3a3046"/>
    {BGGRAIN}'''

def castle(x, y, s=1.0):
    lights = "".join(f'<rect x="{wx}" y="{wy}" width="6" height="10"/>' for wx, wy in [(-150,-140),(-130,-110),(-56,-200),(-30,-160),(-60,-120),(40,-160),(60,-120),(130,-120),(-180,-50),(-100,-50),(70,-50),(150,-50)])
    return f'''<g transform="translate({x},{y}) scale({s})" fill="#1c1a34">
    <rect x="-200" y="-80" width="400" height="80"/><rect x="-170" y="-170" width="60" height="170"/><path d="M -178,-170 L -140,-240 L -102,-170 Z"/>
    <rect x="-80" y="-230" width="80" height="230"/><path d="M -90,-230 L -40,-330 L 10,-230 Z"/><rect x="20" y="-190" width="70" height="190"/><path d="M 12,-190 L 55,-270 L 98,-190 Z"/>
    <rect x="110" y="-150" width="60" height="150"/><path d="M 102,-150 L 140,-210 L 178,-150 Z"/>
    <g fill="#f4d8a0" opacity=".85">{lights}</g></g>'''

def songthaew(x, y, s=1.0, rot=0):
    """รถสองแถวแดง หันข้างเต็ม หน้ารถไปทางซ้าย"""
    bars = "".join(f'<rect x="{-30+k*34}" y="-120" width="4" height="50" fill="#d8323e"/>' for k in range(6))
    return f'''<g transform="translate({x},{y}) rotate({rot}) scale({s})">
    <circle cx="-100" cy="0" r="24" fill="#1a1a22"/><circle cx="-100" cy="0" r="11" fill="#c8ccd6"/><circle cx="90" cy="0" r="24" fill="#1a1a22"/><circle cx="90" cy="0" r="11" fill="#c8ccd6"/>
    <path d="M -150,-16 C -150,-46 -140,-60 -120,-64 L -70,-90 L -40,-90 L -40,-10 L -140,-10 C -148,-10 -150,-12 -150,-16 Z" fill="#d8323e"/>
    <path d="M -110,-64 L -76,-84 L -50,-84 L -50,-62 Z" fill="#bfe0f4"/><circle cx="-142" cy="-30" r="7" fill="#fff4c8"/>
    <path d="M -40,-130 L 150,-130 L 150,-10 L -40,-10 Z" fill="#d8323e"/><path d="M 40,-130 L 150,-130 L 150,-10 L 60,-10 Z" fill="#b8222e"/>
    <path d="M -46,-140 L 156,-140 L 156,-128 L -46,-128 Z" fill="#a8222e"/>
    <path d="M -30,-120 L 140,-120 L 140,-70 L -30,-70 Z" fill="#1e1a2a"/>{bars}
    <rect x="-40" y="-64" width="190" height="10" fill="#a8222e"/><rect x="146" y="-20" width="24" height="6" fill="#c8ccd6"/>
    <text x="50" y="-26" text-anchor="middle" {TH} font-size="14" font-weight="700" fill="#f4d878">กรุงเทพ - ฮอกวอตส์</text>
    <ellipse cx="0" cy="18" rx="170" ry="10" fill="#b18cff" opacity=".4" filter="url(#soft)"/></g>'''

def rice_fields(y):
    out = f'<rect y="{y}" width="540" height="{960-y}" fill="#1a2440"/>'
    for k in range(7):
        yy = y + 14 + k * (26 + k * 6)
        out += f'<path d="M -20,{yy} L 560,{yy-6}" stroke="#2c3c66" stroke-width="{3+k}"/>'
    out += f'<ellipse cx="420" cy="{y+60}" rx="40" ry="6" fill="#e8e6f4" opacity=".4"/>'
    out += "".join(f'<path d="M {x},{y+20+i*30} l -3,-10 M {x},{y+20+i*30} l 3,-12" stroke="#3a5a6a" stroke-width="2"/>' for i in range(6) for x in range(20, 540, 60))
    return out

def great_hall(blur="bgblur2"):
    cand = "".join(f'<g transform="translate({x},{y})"><rect x="-3" y="0" width="6" height="18" fill="#efe8dc"/><circle cy="-4" r="18" fill="url(#warm)"/><path d="M 0,-8 C 3,-4 2,0 0,0 C -2,0 -3,-4 0,-8 Z" fill="#fff0c8"/></g>' for x, y in [(60,150),(150,120),(250,160),(340,110),(430,150),(500,210),(100,230),(390,240),(200,250),(300,200)])
    wins = "".join(f'<path d="M {x},460 L {x},140 C {x},100 {x+60},100 {x+60},140 L {x+60},460 Z" fill="#2a3a6a"/><path d="M {x+6},456 L {x+6},142 C {x+6},110 {x+54},110 {x+54},142 L {x+54},456 Z" fill="#3a5088"/><path d="M {x+30},110 L {x+30},456 M {x+6},280 L {x+54},280" stroke="#2a3a6a" stroke-width="3"/>' for x in (30, 170, 310, 450))
    flags = "".join(f'<path d="M {x},60 L {x+44},60 L {x+44},300 L {x+22},280 L {x},300 Z" fill="{c}"/><path d="M {x+16},120 L {x+28},120 L {x+28},140 L {x+16},140 Z" fill="#f0cc60" opacity=".7"/>' for x, c in [(110,"#6a2a4a"),(250,"#2a4a6a"),(390,"#4a2a6a")])
    plates = "".join(f'<circle cx="{x}" cy="512" r="9" fill="#e8dcc8"/><circle cx="{x}" cy="512" r="5" fill="#c87a4a"/>' for x in range(30, 540, 52))
    cups = "".join(f'<path d="M {x},512 L {x+6},494 L {x+12},512 Z" fill="#c8a060"/>' for x in range(50, 540, 70))
    return f'''<rect width="540" height="960" fill="url(#hall)"/>
    <g filter="url(#{blur})">
      <rect width="540" height="560" fill="url(#stone)"/>{wins}{flags}
      <rect y="460" width="540" height="100" fill="#4a3a36"/>
      <path d="M 0,520 L 540,520 L 540,560 L 0,560 Z" fill="#6a4a3a"/><path d="M 0,520 L 540,520" stroke="#8a6a4a" stroke-width="4"/>{plates}{cups}
      {crowd(560, 12, 7)}
    </g>{cand}
    <rect y="620" width="540" height="340" fill="#2e2430"/>
    {BGGRAIN}'''

# =================== ช็อต (บท v9) ===================
exec((HERE / "sb_thai.py").read_text())   # ฉากไทยย่านพระนคร + ตุ๊กตุ๊กไทย
WARMGRAIN = BGGRAIN

p1 = frame(f'''{phranakhon_street()}
  {WARMGRAIN}
  {dust(420, 300, 220, 400, 18, 11, "#fff2d8")}
  {card(30, 400, 200, "บ้านซิ่ง ชั้นบนร้านทอง", "ตึกแถวเก่าย่านพระนคร", 200, 300)}
  {badge("พระนคร · 05:00")}{EYE}
  {subs(["ถ้าฮอกวอตส์มาเปิดสาขาที่ไทย", "มันจะเป็นแบบนี้ครับ"], ["If Hogwarts opened a branch in Thailand,", "this is how it’d go."])}''')

p2 = frame(f'''{bedroom2()}
  {WARMGRAIN}
  {dust(360, 520, 300, 400, 22, 12, "#fff2d8")}
  {mattress2(60, 660, 330)}
  {axe_pillow(70, 664, .9)}
  {thai_blanket(170, 676, 210)}
  {old_fan(470, 800, .9)}{slippers(60, 830)}
  {pop(24, 130, "เอ้กอี๊เอ้กกก!!", 40)}
  <g data-ui="1"><path d="M 300,270 L 270,256 M 296,290 L 262,290 M 300,310 L 270,322" stroke="#fff4d0" stroke-width="3.4" stroke-linecap="round"/></g>
  <g data-anim="fall" transform="translate(470,560) rotate(-118) scale(.72)"><use href="#c_sing"/></g>
  <g data-anim="rooster" transform="translate(340,374) scale(.62)"><use href="#c_rooster"/><path d="M -26,-145 L -42,-136 L -27,-140 Z" fill="#c4922a"/></g>
  <g transform="translate(110,560) rotate(-24)">{axe_pillow(0, 0, .7)}</g>
  <g transform="translate(240,440) rotate(16)"><rect x="-26" y="-18" width="52" height="36" fill="#f4ecd8"/><path d="M -26,-18 L 0,4 L 26,-18" fill="none" stroke="#d8ccb6" stroke-width="2"/><circle cx="0" cy="2" r="6" fill="#8e1b24"/></g>
  {card(330, 120, 190, "ที่อังกฤษ: นกฮูก", "ที่ไทย: ไก่ชน ตีห้าตรง", 350, 290)}
  {badge("05:00")}{EYE}
  {subs(["ที่อังกฤษ จดหมายมากับนกฮูก…", "ที่ไทย มากับไก่ชน ตีห้า!"], ["In England, letters come by owl.", "In Thailand, by fighting rooster. At 5 a.m.!"])}''')

coins = "".join(f'<g transform="translate({x},{y}) rotate({r})"><ellipse rx="13" ry="12" fill="#e8c24a"/><ellipse rx="9" ry="8" fill="#f4d878"/><text y="4" text-anchor="middle" font-family="serif" font-size="10" font-weight="700" fill="#c49a2a">H</text></g>' for x, y, r in [(410,600,10),(436,626,-20),(392,640,30),(450,580,-10),(420,666,15)])
p3 = frame(f'''{bedroom2("bgblur2")}
  {WARMGRAIN}
  <g transform="translate(400,372) scale(.5)" filter="url(#bgblur)"><use href="#c_rooster"/></g>
  <g transform="translate(270,320) scale(3.6)">
    <path d="M -54,72 C -52,58 -32,50 -12,49 L 12,49 C 32,50 52,58 54,72 L 58,120 L -58,120 Z" fill="#eeeef2"/>
    <path d="M -54,72 C -52,60 -36,52 -20,50 C -26,60 -28,90 -28,120 L -58,120 Z" fill="#fbfbfd"/>
    <path d="M 24,50 C 38,53 52,60 54,72 L 58,120 L 32,120 C 32,90 30,56 24,50 Z" fill="#d4d4dc"/>
    <clipPath id="hc"><rect x="-80" y="-90" width="160" height="150"/></clipPath><g clip-path="url(#hc)"><use href="#c_sing" transform="translate(0,480)"/></g>
  </g>
  {sunpoly([(0,300),(200,180),(260,960),(0,960)], .35)}
  {shadow(290, 600, 150, 16, .25)}
  <g transform="rotate(-4 270 500)">
    <rect x="120" y="420" width="300" height="170" rx="4" fill="#f4ecd8"/><rect x="120" y="420" width="300" height="10" fill="#e6dcc4"/>
    <circle cx="390" cy="560" r="14" fill="#8e1b24"/><circle cx="388" cy="558" r="5" fill="#b8323e"/>
    <text x="140" y="458" {TH} font-size="16" font-weight="700" fill="#3a2a22">ฮอกวอตส์ สาขาประเทศไทย</text>
    <rect x="140" y="472" width="230" height="4" fill="#b8aa90"/>
    <rect x="136" y="484" width="150" height="22" fill="#ffd84a" opacity=".55"/><text x="142" y="500" {TH} font-size="14" font-weight="600" fill="#3a2a22">ไม่พิจารณาเกรด</text>
    <text x="142" y="526" {TH} font-size="12" fill="#5a4a3a">แนบทุนการศึกษา: เหรียญทอง 10 เหรียญ</text>
    <path d="M 112,560 C 100,540 104,520 118,512 L 132,590 C 120,592 114,580 112,560 Z" fill="#d9a47a"/>
    <path d="M 428,560 C 440,540 436,520 422,512 L 408,590 C 420,592 426,580 428,560 Z" fill="#bf8a62"/>
  </g>
  {coins}
  {card(340, 110, 170, "เกรดเฉลี่ย 1.50", "ผ่านแบบเฉียดฉิว", 330, 230)}
  {badge("05:02")}{EYE}
  {subs(["ไม่ดูเกรดด้วย!", "เกรดผมหนึ่งจุดห้าเองนะเว้ย"], ["And they don’t check grades!", "Mine’s a 1.5!"])}''')

p4 = frame(f'''{Z(gold_shop2(), 1.6, 600)}
  {WARMGRAIN}
  {shadow(220, 640, 110)}
  <g transform="translate(220,700) scale(.95)"><use href="#c_ama"/></g>
  {counter(0, 520, 400)}
  {abacus(30, 486)}<g transform="translate(300,500)"><rect x="-30" y="-6" width="60" height="22" rx="3" fill="#e8e4f0"/><rect x="-24" y="-2" width="30" height="12" fill="#8fd19e"/><text x="-9" y="8" text-anchor="middle" font-family="Inter" font-size="9" fill="#1a3a20">15.2g</text><rect x="-20" y="-14" width="40" height="8" rx="2" fill="#c8c4d4"/></g>
  <path d="M 230,330 l -10,-8 M 230,342 l -12,2 M 262,326 l 10,-8" stroke="#fff4d0" stroke-width="2.4" stroke-linecap="round"/>
  {shadow(460, 700, 70)}
  <g transform="translate(460,770)"><use href="#c_sing"/></g>
  {pop(290, 250, "แท้!", 32, -6)}
  {card(20, 360, 180, "ทอง 96.5%", "มาตรฐานทองไทย", 250, 336)}
  {badge("ร้านทองชั้นล่าง · 07:00")}{EYE}
  {subs(["(ซิ่ง) ที่อังกฤษ เหรียญทองเอาไปฝากธนาคาร…", "ที่ไทย อาม้าขอกัดก่อน", "(อาม้า) แท้! ทองเก้าสิบหกจุดห้า!"], ["In England, gold goes to the bank. In Thailand,", "Ma bites it first. (Ma) Real! 96.5% gold!"])}''')

p5 = frame(f'''{Z(phranakhon_street(), 2.0, 640)}
  {WARMGRAIN}
  {speed(420, 380, 540, 9, 4, "#fff4e0")}
  {shadow(290, 650, 200, 14)}
  <g data-anim="tuk" data-x="300" data-y="620" transform="translate(300,620) rotate(-14)">
    {tuktuk_thai(0, 0, 1.15)}
    <clipPath id="tkc"><rect x="-220" y="-420" width="440" height="335"/></clipPath>
    <g clip-path="url(#tkc)"><g transform="translate(70,-24) scale(.34)"><use href="#c_giant"/></g><g transform="translate(22,-34) scale(.34)"><use href="#c_sing"/></g><g transform="translate(-72,-40) scale(.32)"><use href="#c_tukdriver"/></g></g>
  </g>
  {pop(26, 220, "หัวรถลอย!", 34, -10)}
  {card(320, 110, 190, "ที่อังกฤษ: รถไฟ", "ที่ไทย: ตุ๊กตุ๊ก + ลุงโต", 300, 420)}
  {badge("ย่านพระนคร · 08:00")}{EYE}
  {subs(["ที่อังกฤษ ไปโรงเรียนด้วยรถไฟ… ที่ไทย", "ลุงโตมารับด้วยตุ๊กตุ๊ก หัวรถลอยทั้งทาง"], ["In England, you take a train. In Thailand,", "Uncle To brings a tuk-tuk. Front wheel up all the way."])}''')

p6 = frame(f'''{Z(soi2(), 2.0, 660)}
  {WARMGRAIN}
  {shadow(130, 760, 80, 10)}
  {spirit_house(130, 600, 1.15)}
  {garland(90, 510, .9)}{garland(170, 510, .9)}
  {zebra(86, 594, 1.2)}{zebra(128, 594, 1.2)}{zebra(170, 594, 1.2)}
  {incense(50, 594)}
  <g transform="translate(204,592)"><rect x="-8" y="-40" width="16" height="40" rx="4" fill="#c8243a" opacity=".85"/><path d="M 2,-40 L 10,-62" stroke="#f4f4f4" stroke-width="2.4"/></g>
  {shadow(400, 790, 80)}
  <g transform="translate(400,800) scale(.72)"><use href="#c_giant"/></g>
  {shadow(270, 790, 50, 10)}
  <g transform="translate(270,800) scale(.72)"><use href="#c_sing"/></g>
  <path d="M 265,540 C 262,524 268,508 272,506 C 277,508 282,524 279,540 Z" fill="#d9a47a"/><path d="M 272,508 L 272,540" stroke="#bf8a62" stroke-width="1.2"/>
  {card(20, 110, 210, "ที่อังกฤษ: วิ่งชนกำแพง", "ที่ไทย: ถวายน้ำแดง", 204, 550)}
  {badge("ปากซอย")}{EYE}
  {subs(["ที่อังกฤษ ต้องวิ่งชนกำแพงชานชาลา…", "ที่ไทย ต้องถวายน้ำแดงศาลพระภูมิ"], ["In England, you run through a wall.", "In Thailand, you offer red soda to the spirit house."])}''')

rays = "".join(f'<path d="M 270,330 L {270 + 900*math.cos(a/24*6.283):.0f},{330 + 900*math.sin(a/24*6.283):.0f}" stroke="#fff4d8" stroke-width="{8 if a%2 else 3}" opacity=".5"/>' for a in range(24))
p7 = frame(f'''<rect width="540" height="960" fill="#f4dcb0"/>
  {rays}<circle cx="270" cy="330" r="280" fill="url(#portal)"/>
  {WARMGRAIN}
  {spirit_house(270, 470, 2.2, True)}
  {garland(190, 300, 1.6)}{garland(350, 300, 1.6)}
  {zebra(150, 640, 2.6, True)}{zebra(270, 660, 2.6, True)}{zebra(390, 640, 2.6, True)}
  <g transform="translate(250,420) rotate(25) scale(.3)" opacity=".85"><use href="#c_sing"/></g>
  <g transform="translate(300,410) rotate(-30) scale(.3)" opacity=".85"><use href="#c_giant"/></g>
  {pop(40, 150, "วู้บบบ!!", 44, -6)}
  {card(320, 700, 200, "ม้าลายกะพริบตา", "พร้อมกันทั้งสามตัว", 300, 590)}
  {EYE}''')

wandpile = "".join(f'<path d="M {236+k*10},570 L {252+k*10},{520-(k%3)*10}" stroke="{["#6a4a2c","#8a6a44","#9a7650","#5a3a22"][k%4]}" stroke-width="4" stroke-linecap="round"/>' for k in range(26))
p8 = frame(f'''{Z(magic_market(), 1.7, 620)}
  {dust(270, 300, 500, 200, 16, 21, "#ffe8c8")}
  {Z(stall(100, 440, 200, "#8e1b24", "meatball", "ลูกชิ้นปิ้ง"), 1.5, 620)}
  {shadow(330, 650, 110)}
  <g transform="translate(330,720) scale(.92)"><use href="#c_vendor"/></g>
  <rect x="220" y="560" width="320" height="100" fill="#5a3e28"/><rect x="220" y="560" width="320" height="10" fill="#7a5638"/>{wandpile}
  <rect x="400" y="500" width="120" height="48" rx="4" fill="#f2ead8"/><text x="460" y="532" text-anchor="middle" {TH} font-size="20" font-weight="700" fill="#c43a3a">3 อัน 100</text>
  {pop(380, 200, "จ้าาา!", 34, 6)}
  {card(20, 110, 200, "ที่อังกฤษ: ไม้ราคาแพง", "ที่ไทย: สามอันร้อย", 330, 330)}
  {badge("ตลาดนัดเวทมนตร์")}{EYE}
  {subs(["(ซิ่ง) ที่อังกฤษ ไม้กายสิทธิ์ราคาแพง…", "(ป้าแต๋ว) สามอันร้อยจ้า!"], ["(Sing) In England, wands are expensive…", "(Vendor) Three for a hundred!"])}''')

fallen = "".join(f'<path d="M {x},{y} L {x+60*math.cos(a):.0f},{y+60*math.sin(a):.0f}" stroke="#8a6a44" stroke-width="5" stroke-linecap="round"/>' for x, y, a in [(150,780,-.3),(240,820,.4),(380,800,-.8)])
p9 = frame(f'''{Z(magic_market(), 1.7, 620)}
  <g filter="url(#bgblur2)">{stall(120, 420, 220, "#8e1b24", "meatball", "ลูกชิ้นปิ้ง")}<g transform="translate(330,1120) scale(2.2)"><use href="#c_sing"/></g></g>
  <path d="M 250,700 C 236,640 246,560 270,540 L 320,540 C 330,580 330,650 320,700 Z" fill="#d9a47a"/>
  <path d="M 300,540 L 320,540 C 330,580 330,650 320,700 L 306,700 C 312,640 310,580 300,540 Z" fill="#bf8a62"/>
  <path d="M 268,560 C 256,552 254,540 264,534 L 300,540 L 296,566 Z" fill="#d9a47a"/>
  <path d="M 282,550 L 300,180" stroke="#d8c09a" stroke-width="7" stroke-linecap="round"/><path d="M 280,550 L 296,190" stroke="#efe0c0" stroke-width="2"/>
  <circle cx="298" cy="230" r="30" fill="#9a5a3a"/><circle cx="290" cy="222" r="11" fill="#b8784e"/><path d="M 278,240 C 290,248 306,248 318,236" fill="none" stroke="#7a4228" stroke-width="3"/>
  <circle cx="298" cy="230" r="80" fill="url(#portal)" opacity=".5"/>
  <path d="M 120,250 C 180,240 220,220 260,236" fill="none" stroke="#e8dcff" stroke-width="3" stroke-dasharray="6 6" opacity=".8"/>
  {fallen}{pop(380, 860, "ร่วง…", 22, 0)}
  {card(30, 110, 200, "ไม้มะขาม?", "ไม่ใช่ ไม้ลูกชิ้นร้านข้าง ๆ", 270, 230)}
  {badge("ร้านไม้กายสิทธิ์")}{EYE}
  {subs(["แต่ไม้ที่เลือกผม…", "ดันเป็นไม้ลูกชิ้น"], ["But the wand that chose me…", "was a meatball skewer."])}''')

p10 = frame(f'''{Z(magic_market(), 1.7, 620)}
  {dust(270, 300, 500, 200, 12, 31, "#ffe8c8")}
  {shadow(180, 735, 80)}
  <g transform="translate(180,740) scale(.9)"><use href="#c_ton"/></g>
  {speed(0, 380, 70, 6, 8)}
  <g data-anim="carry" data-dx="-504" data-t="1.1" data-base="translate(124,420) rotate(-12)" transform="translate(124,420) rotate(-12)"><path d="M 0,80 L 0,-40" stroke="#d8c09a" stroke-width="5" stroke-linecap="round"/><rect x="-14" y="-60" width="28" height="56" rx="12" fill="#e8d4a8"/><rect x="-14" y="-60" width="28" height="56" rx="12" fill="none" stroke="#a8743a" stroke-width="3"/><path d="M -10,-50 L 10,-44 M -10,-34 L 10,-28 M -10,-20 L 10,-14" stroke="#b8844a" stroke-width="3"/><circle cy="-32" r="50" fill="url(#portal)" opacity=".45"/></g>
  {shadow(430, 745, 64)}
  <g transform="translate(430,750) scale(.84)"><use href="#c_sing"/></g>
  <path d="M 470,548 L 482,400" stroke="#d8c09a" stroke-width="4" stroke-linecap="round"/><circle cx="481" cy="414" r="8" fill="#9a5a3a"/>
  {pop(200, 180, "เสี่ยวว!", 32, -6)}
  {card(300, 110, 210, "ไม้ข้าวเหนียวปิ้ง", "ไม้กายสิทธิ์ของต้น", 130, 260)}
  {badge("ตลาดนัดเวทมนตร์")}{EYE}
  {subs(["เสี่ยว! ของข้อยได้", "ไม้ข้าวเหนียวปิ้ง!"], ["Buddy! Mine’s a", "grilled sticky-rice stick!"])}''')

p11 = frame(f'''{Z(great_hall(), 1.5, 620)}
  <g filter="url(#bgblur2)" opacity=".85"><g transform="translate(220,640) scale(.58)"><use href="#c_harry"/></g><g transform="translate(280,640) scale(.58)"><use href="#c_ron"/></g><g transform="translate(340,640) scale(.58)"><use href="#c_hermione"/></g></g>
  {shadow(150, 690, 100)}
  <g transform="translate(140,790) scale(.96)"><use href="#c_draco"/></g>
  {shadow(400, 690, 100)}
  <g transform="translate(410,790) scale(.96)"><use href="#c_ton"/></g>
  {pop(230, 190, "ฮึ!", 28, 0)}{pop(440, 200, "ฮ่าๆ", 22, 0)}
  {card(20, 110, 190, "โลว์ = ดูไม่มีระดับ", "ศัพท์วัยรุ่นตอนนี้", 160, 300)}
  {badge("ห้องโถงใหญ่")}{EYE}
  {subs(["(เดรโก) มาโรงเรียนด้วยตุ๊กตุ๊กเนี่ยนะ โลว์ชะมัด", "(ต้น) โลว์แต่มีนาสามร้อยไร่เด้อ"], ["(Draco) You came in a tuk-tuk? So low.", "(Ton) Low, with a 300-acre rice farm."])}''')

p12 = frame(f'''{Z(great_hall(), 1.5, 620)}
  {shadow(450, 700, 90)}
  <g transform="translate(450,780) scale(1.05)" filter="url(#bgblur)"><use href="#c_strict"/></g>
  <rect x="190" y="570" width="160" height="20" rx="4" fill="#6a4a32"/><rect x="200" y="590" width="14" height="80" fill="#4a3222"/><rect x="326" y="590" width="14" height="80" fill="#4a3222"/>
  <g transform="translate(270,980) scale(1.7)"><use href="#c_sing_robe"/></g>
  <g transform="translate(272,128) scale(1.15) rotate(-4)"><use href="#c_hat"/></g>
  {pop(30, 210, "อืมมม…", 30, -6)}
  {card(330, 230, 190, "ที่อังกฤษ: หมวกเลือกให้", "ที่ไทย: โยนให้คนดู", 300, 90)}
  {badge("พิธีคัดบ้าน")}{EYE}
  {subs(["(ซิ่ง) ที่อังกฤษ หมวกเลือกบ้านให้…", "(หมวก) อืม… กวนขนาดนี้", "ให้คนดูเลือกเองแล้วกัน!"], ["(Sing) In England, the hat picks your house…", "(Hat) Hmm… this cheeky? Let the viewers pick!"])}''')

opts = [("A", "กริฟฟินดอร์", "#8e1b24", "#d9b24a", True), ("B", "สลิธีริน", "#2a5e40", "#c4c8d4", False), ("C", "เรเวนคลอ", "#2a3e6e", "#b8905a", False), ("D", "ฮัฟเฟิลพัฟ", "#c99a2a", "#1a1a20", False)]
oc = ""
for i, (k, name, c1, c2, on) in enumerate(opts):
    x, y = 60 + (i % 2) * 220, 250 + (i // 2) * 150
    f1, f2, tc = (c1, c2, "#fff") if on else ("#3c3c46", c1, "#b8b8c4")
    oc += f'''<g transform="translate({x},{y})">
    <rect width="200" height="120" rx="14" fill="{f1}"/><rect y="100" width="200" height="20" fill="{f2}" opacity="{.9 if on else .55}"/>
    <circle cx="34" cy="40" r="20" fill="#15121c" opacity=".45"/><text x="34" y="48" text-anchor="middle" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="{tc}">{k}</text>
    <text x="64" y="50" {TH} font-size="20" font-weight="700" fill="{tc}">{name}</text></g>'''
p13 = frame(f'''<g opacity=".6">{great_hall("bgblur2")}</g><rect width="540" height="960" fill="#15121c" opacity=".55"/>
  <text x="270" y="190" text-anchor="middle" {TH} font-size="32" font-weight="700" fill="#fff">ซิ่งควรอยู่บ้านไหน?</text>
  {oc}
  <path d="M 250,350 l 0,30 l 8,-8 l 6,14 l 6,-3 l -6,-13 l 11,0 Z" fill="#fff" stroke="#15121c" stroke-width="1.5"/>
  <g transform="translate(270,578)"><rect x="-150" y="-20" width="300" height="38" rx="19" fill="#2a2440" stroke="#8a6cd8"/><text y="5" text-anchor="middle" {TH} font-size="15" font-weight="600" fill="#e8e2f4">พิมพ์ A B C หรือ D ในคอมเมนต์</text></g>
  {subs(["ผมควรอยู่บ้านไหน", "คอมเมนต์มาเลยครับ"], ["Which house should I be in?", "Tell me in the comments."])}''')

PANELS = [
  ("1", "3.5", p1, "Wide · ตึกแถวเก่าย่านพระนครตอนเช้า", "ตึกแถวชิโน-โปรตุกีส หน้าต่างโค้งบานไม้สีเขียว บานเฟี้ยม ป้ายร้านภาษาไทย สายไฟ ยอดวัดสีทองไกล ๆ · แดดเช้าเฉียง เงาอมฟ้า · ซูมเข้าหน้าต่างชั้นบนร้านทอง", "เสียงเมืองตอนเช้า ระฆังวัดไกล ๆ · ดนตรีขี้เล่น · เสียงบรรยายซิ่ง"),
  ("2", "4", p2, "Medium Wide · ห้องนอนชั้นบน", "ผนังเขียวหัวเป็ด ไม้บุผนัง พื้นไม้กระดาน ตู้ไม้มีกระจก โปสเตอร์มวยไทย รูปอากง วิทยุเก่า พัดลมตั้งพื้น · ไอ้เหลืองเกาะหน้าต่างบานเกล็ดขันใส่ ซิ่งตกฟูก หมอนขวานกระเด็น · กล้องสั่นสั้น ๆ", "ไก่ขันลั่น ซิ่งล้ม ไก่กระโดดลงมาทับ + เสียงตุ้บ"),
  ("3", "3.5", p3, "Close-up · ซิ่งอ่านจดหมาย", "ตาตี๋ยิ้มกวน คิ้วยก · เหรียญทองไหลออกจากซอง · ไอ้เหลืองเบลอด้านหลัง", "ปากซิ่งขยับ · เสียงเหรียญกรุ๊งกริ๊ง"),
  ("4", "5", p4, "Medium · ร้านทองชั้นล่าง", "ผนังแดง กระเบื้องเก่าครึ่งล่าง โปสเตอร์กระดาษแปะเต็มผนัง ตู้ทอง พัดลมเพดาน นาฬิกาลูกตุ้ม ศาลเจ้า แมวกวัก บานเฟี้ยมเปิดรับแดด · อาม้ากัดเหรียญแล้วชูขึ้นตาวาว", "เสียงบรรยายซิ่ง → ปากอาม้าขยับ · เสียง 'งั่ม' แล้ว 'วิ้ง'"),
  ("5", "4", p5, "Wide · ถนนย่านพระนคร", "ตุ๊กตุ๊กไทยหน้ากากขาวแถบน้ำเงิน ไฟกลมโครเมียม ล้อหน้าขอบแดง หลังคาผ้าระบายเงิน ป้าย TAXI · หัวรถลอย ลุงโตเบียดเบาะหลัง ลุงเปี๊ยกคนขับเกาะแฮนด์แน่น", "เสียงตุ๊กตุ๊ก 'ปั๊ด ๆ ๆ' + แตร · เสียงบรรยายซิ่ง"),
  ("6", "4", p6, "Medium · ศาลพระภูมิปากซอย", "พวงมาลัย ธูป ม้าลาย น้ำแดงเสียบหลอด ป้ายซอย ต้นไม้ วินมอไซค์ · ลุงโตวางน้ำแดง ซิ่งพนมมือไหว้", "ดนตรีเบาลง ลึกลับนิด ๆ · เสียงบรรยายซิ่ง"),
  ("7", "3", p7, "Close-up → ซูมเบลอ", "ม้าลายกะพริบตาพร้อมกัน ประตูศาลเปิด แสงทองพุ่ง ดูดทั้งสองคนเข้าไป", "เงียบหนึ่งจังหวะ → เสียงวูบ (ใช้ครั้งเดียว)"),
  ("8", "4", p8, "Medium · ตลาดนัดเวทมนตร์", "ไฟปิงปอง โคมลอย ไม้กวาดบิน ร้านลูกชิ้นปิ้งข้าง ๆ · ป้าแต๋วตะโกน ป้าย '3 อัน 100'", "เสียงบรรยายซิ่ง → ปากป้าแต๋วขยับ · เสียงตลาด"),
  ("9", "3.5", p9, "Close-up มือ", "ไม้ลูกชิ้นลอยเข้ามือซิ่งเองพร้อมแสงวูบ · ไม้สามอันที่ซื้อร่วงพื้น", "เสียงเวทมนตร์ใส ๆ แล้วเสียงไม้ร่วง 'ก๊อก ๆ'"),
  ("10", "4", p10, "Medium · ต้นเดินเข้าเฟรมจากซ้าย", "ต้นชูไม้ข้าวเหนียวปิ้งเรืองแสง ผ้าขาวม้าพาดคอ ถือกระติบ · ซิ่งหันไปมอง", "เสียงแคนสั้น ๆ · ปากต้นขยับ"),
  ("11", "4.5", p11, "Medium · ห้องโถงใหญ่ (ตัดสลับ)", "เดรโกแซะเรื่องตุ๊กตุ๊ก (โยงกลับช็อต 5) → ต้นยิ้มแป้นตอบ เดรโกหน้าเหวอ · แฮร์รี่ รอน เฮอร์ไมโอนี่แอบขำ", "ปากเดรโกขยับก่อน แล้วปากต้น"),
  ("12", "5", p12, "Medium Close-up · พิธีคัดบ้าน", "หมวกบนหัวซิ่ง ครูมาลัยเบลอด้านข้าง · ซูมเข้าช้า ๆ · หมวกหันมองกล้อง ภาพหยุด", "เสียงบรรยายซิ่ง → ปากหมวกขยับ · ดนตรีลุ้นแล้วหยุด"),
  ("13", "4", p13, "การ์ดโหวต", "ไฮไลต์วน A → B → C → D ตัวที่เลือกขึ้นสีบ้าน ตัวอื่นสีเทา · ไม่เฉลย", "เสียงคลิกทุกครั้งที่สลับ · ต่อด้วยโลโก้ปิดท้าย 2.6 วิ"),
]


# ===== บท v10: ปรับซับและเพิ่มช็อตใหม่ =====
def swap_subs(svg, old_first, th, en):
    a = svg.index(old_first); a = svg.rindex('<text', 0, a)
    b = svg.rindex('</g></svg>')
    return svg[:a] + subs(th, en) + svg[b:]

p5 = swap_subs(p5, "ที่อังกฤษ ไปโรงเรียนด้วยรถไฟ", ["ลุงโตภารโรงโรงเรียนมารับด้วยตุ๊กตุ๊ก", "ลุงนั่งปุ๊บ หัวรถลอยปั๊บ"], ["Uncle To came in a tuk-tuk.", "He sat down, and the front wheel went up."])
p5 = p5.replace('ที่อังกฤษ: รถไฟ', 'ลุงโตนั่งปุ๊บ').replace('ที่ไทย: ตุ๊กตุ๊ก + ลุงโต', 'หัวรถลอยปั๊บ')

p6d = frame(f'''{Z(phranakhon_street("bgblur2"), 2.0, 640)}
  {WARMGRAIN}
  <g transform="translate(150,960) scale(1.1)" filter="url(#bgblur)"><use href="#c_giant"/></g>
  <g transform="translate(310,1150) scale(2.0)"><use href="#c_tukdriver"/></g>
  <g transform="translate(110,250)"><path d="M -14,40 L 14,40 L 16,0 L -16,0 Z" fill="#b8805a"/><rect x="-14" y="-40" width="8" height="42" rx="4" fill="#b8805a"/><rect x="-4" y="-46" width="8" height="48" rx="4" fill="#b8805a"/><rect x="6" y="-40" width="8" height="42" rx="4" fill="#9a6644"/></g>
  {pop(170, 190, "สามร้อย!", 40, -6)}
  {card(320, 110, 190, "คนตัวใหญ่", "คิดสองที่", 330, 330)}
  {badge("ย่านพระนคร · 08:01")}{EYE}
  {subs(["สามร้อย!", "คนตัวใหญ่คิดสองที่!"], ["Three hundred!", "Big guys pay for two seats!"])}''')

p6 = swap_subs(p6, "ที่อังกฤษ ต้องวิ่งชนกำแพงชานชาลา", ["ทางเข้าโลกเวทมนตร์", "ต้องถวายน้ำแดงก่อนนะไอ้หนู"], ["To enter the magic world,", "first offer red soda, kid."])
p6 = p6.replace('"ที่อังกฤษ: วิ่งชนกำแพง"', '"น้ำแดงเสียบหลอด"').replace('ที่อังกฤษ: วิ่งชนกำแพง', 'น้ำแดงเสียบหลอด').replace('ที่ไทย: ถวายน้ำแดง', 'ของไหว้ยอดนิยม')

p11 = swap_subs(p11, "(เดรโก) มาโรงเรียนด้วยตุ๊กตุ๊ก", ["(เดรโก) รู้ไหมพ่อฉันเป็นใคร… พ่อมดใหญ่!", "(ต้น) พ่อข้อยกะใหญ่คือกัน… ผู้ใหญ่บ้าน!"], ["(Draco) Know who my father is? A great wizard!", "(Ton) Mine’s great too… the village headman!"])
p11 = p11.replace("โลว์ = ดูไม่มีระดับ", "ผู้ใหญ่บ้าน").replace("ศัพท์วัยรุ่นตอนนี้", "ใหญ่ไม่แพ้พ่อมด").replace('ฮ่าๆ', 'ใหญ่!')

p13t = frame(f'''{Z(great_hall(), 1.5, 620)}
  {shadow(450, 700, 90)}
  <g transform="translate(450,780) scale(1.05)" filter="url(#bgblur)"><use href="#c_strict"/></g>
  <rect x="190" y="570" width="160" height="20" rx="4" fill="#6a4a32"/><rect x="200" y="590" width="14" height="80" fill="#4a3222"/><rect x="326" y="590" width="14" height="80" fill="#4a3222"/>
  <g transform="translate(270,980) scale(1.7)"><use href="#c_ton"/></g>
  <g transform="translate(272,130) scale(1.15) rotate(4)"><use href="#c_hat"/></g>
  {pop(30, 210, "ฮัฟเฟิลพัฟ!", 30, -6)}
  {card(320, 230, 200, "ตำปลาแดก", "บ่แม่นตำไทยเด้อ", 290, 400)}
  {badge("พิธีคัดบ้าน")}{EYE}
  {subs(["(หมวก) หัวนี้มีแต่ส้มตำ… ฮัฟเฟิลพัฟ!", "(ต้น) ตำปลาแดกเด้อหมวก บ่แม่นตำไทย!"], ["(Hat) All papaya salad… Hufflepuff!", "(Ton) Fermented-fish style, hat, not Bangkok style!"])}''')

p12 = swap_subs(p12, "(ซิ่ง) ที่อังกฤษ หมวกเลือกบ้านให้", ["(หมวก) อืมม… บ้านไหนดี", "(ซิ่ง) ลุงหมวก เร็ว ๆ ดิ ช้ากว่าเน็ตบ้านผมอีก", "(หมวก) มาเช็กเกลียวฉันเหรอ? ให้คนดูเลือกไปเลย!"], ["(Hat) Hmm… (Sing) Hurry up, slower than my wifi.", "(Hat) Testing me? Fine, the viewers pick!"])
p12 = p12.replace('ที่อังกฤษ: หมวกเลือกให้', 'เช็กเกลียว = ลองเชิง').replace('ที่ไทย: โยนให้คนดู', 'หมวกงอน โยนให้คนดู').replace('อืมมม…', 'งอนแล้ว!')

# ===== บท v11: ตัดมุก "ที่อังกฤษ" · เปิดเรื่องแบบเดิม =====
p1 = swap_subs(p1, "ถ้าฮอกวอตส์มาเปิดสาขาที่ไทย", ["ถ้าวันหนึ่งคุณได้จดหมายเข้าเรียน", "จากฮอกวอตส์ คุณจะไปไหมครับ"], ["If one day you got a letter from Hogwarts,", "would you go?"])
p2 = swap_subs(p2, "ที่อังกฤษ จดหมายมากับนกฮูก", ["จดหมายของผมมากับไก่ชน…", "ตอนตีห้า!"], ["My letter came by fighting rooster\u2026", "at 5 a.m.!"])
p2 = p2.replace("ที่อังกฤษ: นกฮูก", "ไปรษณีย์สาขาไทย").replace("ที่ไทย: ไก่ชน ตีห้าตรง", "ไก่ชน ส่งตีห้าตรง")
p3 = swap_subs(p3, "ไม่ดูเกรดด้วย!", ["ฮอกวอตส์ สาขาประเทศไทย… ไม่ดูเกรดด้วย!", "เกรดผมหนึ่งจุดห้าเองนะเว้ย"], ["Hogwarts, Thailand branch\u2026 no grades needed!", "Mine\u2019s a 1.5!"])
p4 = swap_subs(p4, "(ซิ่ง) ที่อังกฤษ เหรียญทอง", ["(ซิ่ง) ในซองมีเหรียญทองมาด้วย อาม้าเลยขอกัดก่อน", "(อาม้า) แท้! ทองเก้าสิบหกจุดห้า!"], ["(Sing) The letter came with gold coins, so Ma bit one.", "(Ma) Real! 96.5% gold!"])
p8 = swap_subs(p8, "(ซิ่ง) ที่อังกฤษ ไม้กายสิทธิ์", ["ไม้กายสิทธิ์จ้า สามอันร้อย", "เลือกเลยจ้า!"], ["Magic wands, three for a hundred!", "Pick one!"])
p8 = p8.replace("ที่อังกฤษ: ไม้ราคาแพง", "ไม้กายสิทธิ์").replace("ที่ไทย: สามอันร้อย", "สามอันร้อย ถูกสุดในตลาด")

PANELS = [
  ("1", "3.5", p1, "Wide · ตึกแถวเก่าย่านพระนครตอนเช้า", "แดดเช้าเฉียง ยอดวัดไกล ๆ · ซูมเข้าหน้าต่างชั้นบนร้านทอง", "เสียงเมืองตอนเช้า ระฆังวัดไกล ๆ · เสียงบรรยายซิ่ง"),
  ("2", "4", p2, "Medium Wide · ห้องนอนชั้นบน", "ไอ้เหลืองเกาะหน้าต่างขันใส่ ซิ่งตกฟูก หมอนขวานกระเด็น · กล้องสั่นสั้น ๆ", "ไก่ขันลั่น ซิ่งล้ม ไก่กระโดดลงมาทับ + เสียงตุ้บ"),
  ("3", "3.5", p3, "Close-up · ซิ่งอ่านจดหมาย", "ตาตี๋ยิ้มกวน คิ้วยก · เหรียญทองไหลออกจากซอง", "ปากซิ่งขยับ · เหรียญกรุ๊งกริ๊ง"),
  ("4", "4.5", p4, "Medium · ร้านทองชั้นล่าง", "ซิ่งเดินเข้าร้าน อาม้ากัดเหรียญ แล้วชูขึ้นตาวาว", "เสียงบรรยายซิ่ง → ปากอาม้าขยับ · 'งั่ม' แล้ว 'วิ้ง'"),
  ("5", "3", p5, "Wide · ถนนย่านพระนคร", "ลุงโตนั่งปุ๊บ หัวตุ๊กตุ๊กลอยปั๊บ · ลุงเปี๊ยกเกาะแฮนด์แน่น", "เสียงสปริงยุบ 'โบ๋ง' + ตุ๊กตุ๊ก 'ปั๊ด ๆ' · เสียงบรรยายซิ่ง"),
  ("6", "2.5", p6d, "Medium · ลุงเปี๊ยกหันมา", "ลุงเปี๊ยกชูสามนิ้ว ฟันทองวิ้ง · ลุงโตเบลอด้านหลังหน้าเหวอ", "ปากลุงเปี๊ยกขยับ · เสียง 'ติ๊ง' ตอนฟันทองวิ้ง"),
  ("7", "3.5", p6, "Medium · ศาลพระภูมิปากซอย", "ลุงโตวางน้ำแดงเสียบหลอด ซิ่งพนมมือไหว้ · ม้าลายสามตัว", "ปากลุงโตขยับ · ดนตรีเบาลง ลึกลับนิด ๆ"),
  ("8", "2.5", p7, "Close-up → ซูมเบลอ", "ม้าลายกะพริบตาพร้อมกัน ประตูศาลเปิด ดูดทั้งสองคนเข้าไป", "เงียบหนึ่งจังหวะ → เสียงวูบ"),
  ("9", "3.5", p8, "Medium · ตลาดนัดเวทมนตร์", "ไฟปิงปอง โคมลอย ร้านลูกชิ้นข้าง ๆ · ป้าแต๋วตะโกน '3 อัน 100'", "ปากป้าแต๋วขยับ · เสียงตลาด"),
  ("10", "3", p9, "Close-up มือ", "ไม้ลูกชิ้นลอยเข้ามือซิ่งเอง · ไม้สามอันที่ซื้อร่วงพื้น", "เสียงเวทมนตร์ แล้วไม้ร่วง 'ก๊อก ๆ'"),
  ("11", "3.5", p10, "Medium · ต้นเดินเข้าเฟรมจากซ้าย", "ต้นชูไม้ข้าวเหนียวปิ้งเรืองแสง · ซิ่งหันไปมอง", "เสียงแคนสั้น ๆ · ปากต้นขยับ"),
  ("12", "4.5", p11, "Medium · ห้องโถงใหญ่ (ตัดสลับ)", "เดรโกเชิดหน้าอวดพ่อ → ตัดไปต้นยืดอกภูมิใจ · แฮร์รี่ รอน เฮอร์ไมโอนี่กลั้นขำ", "ปากเดรโกขยับก่อน แล้วปากต้น · เว้นจังหวะก่อน 'ผู้ใหญ่บ้าน'"),
  ("13", "4", p13t, "Medium Close-up · ต้นคัดบ้าน", "หมวกบนหัวต้น · ต้นชี้นิ้วแก้หมวกจริงจัง", "ปากหมวกขยับก่อน แล้วปากต้น"),
  ("14", "5.5", p12, "Medium Close-up · ซิ่งคัดบ้าน", "ซิ่งเคาะหมวกเร่ง · หมวกขมวดคิ้วงอน หันมองกล้อง ภาพหยุด", "ปากหมวก → ปากซิ่ง → ปากหมวก · ดนตรีหยุดตอน 'เช็กเกลียว'"),
  ("15", "3.5", p13, "การ์ดโหวต", "ไฮไลต์วน A → B → C → D ตัวที่เลือกขึ้นสีบ้าน ตัวอื่นสีเทา · ไม่เฉลย", "เสียงคลิกทุกครั้งที่สลับ · ต่อด้วยโลโก้ปิดท้าย 2.6 วิ"),
]

# ===== บท v12e: 5 ขั้นตอน · ตัดอาม้าและเดรโก · ฉากหมอลำ =====
STEPS = ["รับจดหมาย", "เดินทางเข้าโลกเวทมนตร์", "ซื้อไม้กายสิทธิ์", "หาเพื่อนใหม่", "คัดบ้าน"]
def set_badge(svg, text):
    return re.sub(r'<g data-ui="1" transform="translate\(22,26\)">.*?</text></g>', badge(text).replace("\n", ""), svg, count=1, flags=re.S)
def stepb(k): return f"ขั้นที่ {k}/5 · {STEPS[k-1]}"

p1 = swap_subs(p1, "ถ้าวันหนึ่งคุณได้จดหมายเข้าเรียน", ["ถ้าวันหนึ่งคุณได้จดหมายเข้าเรียน", "จากฮอกวอตส์ ต้องผ่านห้าขั้นนี้ครับ"], ["If one day you got a letter from Hogwarts,", "here are the five steps."])
p2 = swap_subs(p2, "จดหมายของผมมากับไก่ชน", ["ขั้นแรก รับจดหมาย", "จดหมายของผมมากับไก่ชน… ตอนตีห้า!"], ["Step one: get the letter.", "Mine came by fighting rooster\u2026 at 5 a.m.!"])
p2 = set_badge(p2, stepb(1)); p3 = set_badge(p3, stepb(1))
p5 = swap_subs(p5, "ลุงโตภารโรงโรงเรียนมารับด้วยตุ๊กตุ๊ก", ["ขั้นที่สอง เดินทางเข้าโลกเวทมนตร์", "ลุงโตมารับด้วยตุ๊กตุ๊ก", "ลุงนั่งปุ๊บ หัวรถลอยปั๊บ"], ["Step two: travel to the magic world. Uncle To", "came in a tuk-tuk. He sat, the front went up."])
for v in ("p5", "p6d", "p6"):
    globals()[v] = set_badge(globals()[v], stepb(2))
p8 = swap_subs(p8, "ไม้กายสิทธิ์จ้า สามอันร้อย", ["ขั้นที่สาม ซื้อไม้กายสิทธิ์", "(ป้าแต๋ว) ไม้กายสิทธิ์จ้า สามอันร้อย", "เลือกเลยจ้า!"], ["Step three: buy a wand.", "(Vendor) Magic wands, three for a hundred!"])
p8 = set_badge(p8, stepb(3)); p9 = set_badge(p9, stepb(3))
p10 = swap_subs(p10, "เสี่ยว! ของข้อยได้", ["ขั้นที่สี่ หาเพื่อนใหม่", "(ต้น) ครั้งแรกของโลก… ครั้งแรกของโลกใบนี้", "สิพ้อเหตุการณ์แนวนี้ ขนคิงลุกยาบ ๆ!", "เสี่ยว! ของข้อยได้ไม้ข้าวเหนียวปิ้ง!"], ["Step four: make a friend. (Ton) First time on this earth", "seeing this, goosebumps! Mine\u2019s a sticky-rice stick!"])
p10 = set_badge(p10, stepb(4)).replace("เสี่ยวว!", "ขนคิงลุก!").replace("ไม้ข้าวเหนียวปิ้ง\", \"ไม้กายสิทธิ์ของต้น", "ครั้งแรกของโลก!\", \"สิพ้อ = จะได้เจอ")
p10 = p10.replace('{EYE}', '{EYE}') 
goose = '<g data-ui="1">' + "".join(f'<path d="M {x},{y} l {dx},{dy}" stroke="#fff4d0" stroke-width="3" stroke-linecap="round"/>' for x, y, dx, dy in [(120,330,-14,-10),(116,360,-18,0),(124,390,-14,10),(240,330,14,-10),(244,360,18,0),(236,390,14,10)]) + '</g>'
broom_fly = '<g transform="translate(250,190) rotate(-10)"><rect x="-60" y="-3" width="120" height="6" fill="#9a7444"/><path d="M 60,-10 L 92,0 L 60,10 Z" fill="#c9a26a"/><path d="M -20,-4 L -8,-34 L 4,-4 Z" fill="#2a2440"/><circle cx="-8" cy="-40" r="8" fill="#2a2440"/><path d="M -18,-42 L 2,-42 L -6,-62 Z" fill="#2a2440"/></g>'
p10 = p10.replace('<g data-ui="1" transform="translate(22,26)">', goose + broom_fly + '<g data-ui="1" transform="translate(22,26)">', 1)

beams = "".join(f'<path data-anim="beam" data-ph="{i}" d="M {x},-20 L {x-60},960 L {x+60},960 Z" fill="{c}" opacity=".22" style="mix-blend-mode:screen"/>' for i, (x, c) in enumerate([(90, "#ff5aa8"), (200, "#b18cff"), (340, "#5ad8ff"), (450, "#ff5aa8")]))
balls = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity=".85"/><circle cx="{x}" cy="{y}" r="{r*2.4}" fill="{c}" opacity=".18"/>' for x, y, r, c in [(70,150,7,"#ff5aa8"),(170,110,6,"#5ad8ff"),(270,160,8,"#ffd84a"),(370,105,6,"#b18cff"),(470,150,7,"#5ad8ff"),(120,240,5,"#ffd84a"),(420,240,5,"#ff5aa8")])
pmor = frame(f'''{Z(great_hall(), 1.5, 620)}
  <rect width="540" height="960" fill="#2a0a3a" opacity=".35"/>
  {balls}{beams}
  <g transform="translate(270,300)"><path d="M -170,0 L 170,0 L 160,46 L -160,46 Z" fill="#c8243a"/><path d="M -170,0 L 170,0 L 170,8 L -170,8 Z" fill="#f0cc60"/>
    <text y="34" text-anchor="middle" {TH} font-size="24" font-weight="700" fill="#ffe08a">หมอลำซิ่ง · คืนแรก</text></g>
  <rect x="0" y="690" width="540" height="40" fill="#3a2030"/><rect x="0" y="690" width="540" height="6" fill="#f0cc60"/>
  <g transform="translate(36,690)"><rect x="-26" y="-120" width="52" height="120" rx="4" fill="#1a1a20"/><circle cy="-80" r="16" fill="#3a3a44"/><circle cy="-34" r="20" fill="#3a3a44"/></g>
  <g transform="translate(504,690)"><rect x="-26" y="-120" width="52" height="120" rx="4" fill="#1a1a20"/><circle cy="-80" r="16" fill="#3a3a44"/><circle cy="-34" r="20" fill="#3a3a44"/></g>
  <g transform="translate(120,690) scale(.62)"><use href="#c_harry"/></g><g transform="translate(420,690) scale(.62)"><use href="#c_hermione"/></g><g transform="translate(470,700) scale(.62)"><use href="#c_ron"/></g>
  {shadow(270, 780, 80)}
  <g transform="translate(270,790) scale(.95)"><use href="#c_ton"/></g>
  <g transform="translate(232,520) rotate(-30)"><path d="M 0,60 L 0,-20" stroke="#d8c09a" stroke-width="5" stroke-linecap="round"/><rect x="-12" y="-44" width="24" height="44" rx="10" fill="#e8d4a8"/><path d="M -8,-36 L 8,-32 M -8,-24 L 8,-20" stroke="#b8844a" stroke-width="3"/><circle cy="-22" r="36" fill="url(#portal)" opacity=".5"/></g>
  {pop(30, 210, "ม่วนอีหลี!", 36, -8)}
  {badge(stepb(4))}{EYE}
  {subs(["(ซิ่ง) คืนแรก เพื่อนใหม่ผมเสกห้องโถง", "ให้กลายเป็นเวทีหมอลำ", "(ต้น) โอ้ละหนอ… ม่วนอีหลีเด้อพี่น้อง!"], ["(Sing) First night, my friend turned the hall into a mor lam stage.", "(Ton) Oh la nor\u2026 let\u2019s party, everyone!"])}''')

p13t = swap_subs(p13t, "(หมวก) หัวนี้มีแต่ส้มตำ", ["ขั้นสุดท้าย คัดบ้าน", "(หมวก) หัวนี้มีแต่ส้มตำ… ฮัฟเฟิลพัฟ!", "(ต้น) ตำปลาแดกเด้อหมวก บ่แม่นตำไทย!"], ["Final step: the sorting. (Hat) All papaya salad\u2026 Hufflepuff!", "(Ton) Fermented-fish style, hat, not Bangkok style!"])
p13t = set_badge(p13t, stepb(5))
p12 = swap_subs(p12, "(หมวก) อืมม", ["(หมวก) อืมม… หัวคนนี้มีแต่เพลงหมอลำ", "ฟังอะไรไม่ออกเลย…", "ให้คนดูช่วยเลือกแล้วกัน!"], ["(Hat) Hmm\u2026 this head is full of mor lam,", "I can\u2019t hear a thing\u2026 let the viewers decide!"])
p12 = set_badge(p12, stepb(5)).replace("เช็กเกลียว = ลองเชิง", "หัวมีแต่เพลงหมอลำ").replace("หมวกงอน โยนให้คนดู", "คัดไม่ได้ โยนให้คนดู").replace("งอนแล้ว!", "ฟังไม่ออก!")

PANELS = [
  ("1", "3.5", p1, "Wide · ตึกแถวเก่าย่านพระนครตอนเช้า", "แดดเช้าเฉียง ยอดวัดไกล ๆ · ซูมเข้าหน้าต่างชั้นบนร้านทอง", "ซิ่งบรรยายเปิดเรื่อง"),
  ("2", "5", p2, "ขั้นที่ 1 · ห้องนอน", "การ์ด 'ขั้นที่ 1 รับจดหมาย' เด้งกลางจอ · ไก่ขัน ซิ่งล้ม ไก่กระโดดทับ", "ซิ่งบรรยายบอกขั้น · ไก่ขัน + ตุ้บ"),
  ("3", "3.5", p3, "Close-up · ซิ่งอ่านจดหมาย", "ตาตี๋ยิ้มกวน · เหรียญทองไหลออกจากซอง", "ปากซิ่งขยับ"),
  ("4", "4.5", p5, "ขั้นที่ 2 · ถนนย่านพระนคร", "การ์ด 'ขั้นที่ 2' · ตุ๊กตุ๊กหัวลอย ลุงโตเบียดเบาะหลัง", "ซิ่งบรรยายบอกขั้น · ตุ๊กตุ๊ก 'ปั๊ด ๆ'"),
  ("5", "2.5", p6d, "Medium · ลุงเปี๊ยกหันมา", "ชูสามนิ้ว ฟันทองวิ้ง", "ปากลุงเปี๊ยกขยับ"),
  ("6", "3.5", p6, "Medium · ศาลพระภูมิปากซอย", "ลุงโตวางน้ำแดง ซิ่งพนมมือไหว้", "ปากลุงโตขยับ"),
  ("7", "2.5", p7, "ซูมเบลอ", "ม้าลายกะพริบตา ประตูศาลเปิด ดูดทั้งสองคนหมุนเข้าไป", "เสียงวูบ"),
  ("8", "4", p8, "ขั้นที่ 3 · ตลาดนัดเวทมนตร์", "การ์ด 'ขั้นที่ 3' · ป้าแต๋วตะโกน '3 อัน 100'", "ซิ่งบรรยายบอกขั้น → ปากป้าแต๋วขยับ"),
  ("9", "3", p9, "Close-up มือ", "ไม้ลูกชิ้นลอยเข้ามือซิ่ง ไม้สามอันร่วง", "เสียงเวทมนตร์ + ไม้ร่วง"),
  ("10", "5.5", p10, "ขั้นที่ 4 · ต้นเดินเข้าเฟรม", "การ์ด 'ขั้นที่ 4' · ต้นตาโต ไม้กวาดบินผ่านหัว ขนลุกซู่ 'ครั้งแรกของโลก…' แล้วชูไม้ข้าวเหนียวปิ้ง", "แคน · ปากต้นขยับ · เพลงอีสานเริ่ม"),
  ("11", "5", pmor, "Wide · ห้องโถงกลายเป็นเวทีหมอลำ", "ไฟเวทีชมพูม่วงกวาด ลูกบอลดิสโก้ ลำโพง ป้าย 'หมอลำซิ่ง' · ต้นร้องใช้ไม้ข้าวเหนียวปิ้งเป็นไมค์ · แฮร์รี่ รอน เฮอร์ไมโอนี่เซิ้ง", "ซิ่งบรรยาย → ต้นร้อง · ลายอีสานเต็มวง"),
  ("12", "4.5", p13t, "ขั้นที่ 5 · ต้นคัดบ้าน", "การ์ด 'ขั้นที่ 5' · ต้นชี้นิ้วแก้หมวก", "ซิ่งบรรยายบอกขั้น → ปากหมวก → ปากต้น"),
  ("13", "5", p12, "Medium Close-up · ซิ่งคัดบ้าน", "หมวกโยกหัวตามเพลงหมอลำในหัวซิ่ง แล้วหันมองกล้อง ภาพหยุด", "ปากหมวกขยับ · เพลงหมอลำแว่ว ๆ แล้วหยุด"),
  ("14", "3.5", p13, "การ์ดโหวต", "ไฮไลต์วน A → B → C → D ตัวที่เลือกขึ้นสีบ้าน ตัวอื่นสีเทา · ไม่เฉลย", "เสียงคลิก · ต่อโลโก้ปิดท้าย"),
]

# การ์ดขั้นตอนกลางจอ (ชั้นโปร่งใส) สำหรับทำคลิป
def step_card(k):
    return f'''<svg viewBox="0 0 540 960" role="img"><g data-ui="1" transform="translate(270,400)">
    <rect x="-200" y="-70" width="400" height="140" rx="26" fill="#1e1630" fill-opacity=".92" stroke="#b18cff" stroke-width="3"/>
    <circle cx="-150" cy="0" r="40" fill="#b18cff"/><text x="-150" y="16" text-anchor="middle" font-family="Inter, sans-serif" font-size="44" font-weight="800" fill="#1e1630">{k}</text>
    <text x="-92" y="-16" {TH} font-size="20" font-weight="600" fill="#c9a8ff">ขั้นที่ {k} จาก 5</text>
    <text x="-92" y="30" {TH} font-size="{30 if len(STEPS[k-1]) < 12 else 24}" font-weight="700" fill="#ffffff">{STEPS[k-1]}</text></g></svg>'''

total = sum(float(d) for _, d, *_ in PANELS)

cards = "".join(f'''<figure class="panel">
  <div class="frame">{svg}</div>
  <figcaption><div class="row"><span class="num">ช็อต {n}</span><span class="dur">{d} วิ</span></div><div class="cam">{cam}</div>
  <p><b>ภาพ</b> {act}</p><p><b>เสียง</b> {snd}</p></figcaption>
</figure>''' for n, d, svg, cam, act, snd in PANELS)

page = f'''<title>สตอรี่บอร์ดซิ่งไปฮอกวอตส์</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@400;500;700;800&display=swap">
<style>
/* Layout: แถวเฟรม 9:16 ตามลำดับช็อต พร้อมโน้ตภาพและเสียงใต้แต่ละเฟรม · โทนมืดของช่อง */
:root {{ --bg:#0d0f14; --panel:#1b1f2b; --ink:#e6e7ee; --muted:#80849a; --line:#2a2e3a; --accent:#c9a8ff;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1200px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:20px; margin:0; font-weight:600; text-wrap:balance; }}
h1 span {{ display:block; font-size:14px; font-weight:400; color:var(--muted); margin-top:4px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:18px 16px; }}
.panel {{ margin:0; display:grid; gap:8px; align-content:start; min-width:0; }}
.frame svg {{ display:block; width:100%; height:auto; border-radius:8px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:13px; line-height:1.55; display:grid; gap:4px; }}
figcaption p {{ margin:0; color:var(--muted); }}
figcaption b {{ color:var(--ink); font-weight:500; margin-right:4px; }}
.row {{ display:flex; gap:8px; align-items:center; }}
.num {{ background:#2a2440; color:var(--accent); border:1px solid #4a3f72; border-radius:99px; padding:0 9px; font-weight:600; }}
.dur {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
.cam {{ color:var(--ink); font-weight:500; }}
.note {{ font-size:13px; color:var(--muted); max-width:72ch; line-height:1.6; margin:0; }}
</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{DEFS}{DEFS_SB}{DEFS_THAI}</defs></svg>
<div class="wrap">
  <h1>สตอรี่บอร์ดเต็ม · ซิ่งไปฮอกวอตส์ สาขาประเทศไทย<span>{len(PANELS)} ช็อต · {total:g} วิ + โลโก้ปิดท้าย 2.6 วิ ≈ {total+2.6:.0f} วิ · เฟรม 9:16 ซับอยู่ช่วง 74% ของความสูง · ร่าง v8 · บท v12e · 5 ขั้นตอน</span></h1>
  <div class="grid">{cards}</div>
  <p class="note">ท่าทางพิเศษ (ตกฟูก นั่งตุ๊กตุ๊ก พนมมือ นั่งเก้าอี้) ยังใช้ท่ายืนหมุนแทน จะวาดท่าจริงในขั้นทำภาพนิ่ง</p>
</div>'''
(HERE / "storyboard.html").write_text(page)
print(len(PANELS), "panels", total, "sec")

# ===== การ์ดโหวต 4 แบบ (ไฮไลต์ A/B/C/D) สำหรับทำคลิป =====
def vote_svg(on_idx):
    oc2 = ""
    for i, (k, name, c1, c2, _) in enumerate(opts):
        x, y = 60 + (i % 2) * 220, 250 + (i // 2) * 150
        on = i == on_idx
        f1, f2, tc = (c1, c2, "#fff") if on else ("#3c3c46", c1, "#b8b8c4")
        oc2 += f'''<g transform="translate({x},{y})">
    <rect width="200" height="120" rx="14" fill="{f1}"/><rect y="100" width="200" height="20" fill="{f2}" opacity="{.9 if on else .55}"/>
    <circle cx="34" cy="40" r="20" fill="#15121c" opacity=".45"/><text x="34" y="48" text-anchor="middle" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="{tc}">{k}</text>
    <text x="64" y="50" {TH} font-size="20" font-weight="700" fill="{tc}">{name}</text></g>'''
    return frame(f'''<g opacity=".6">{great_hall("bgblur2")}</g><rect width="540" height="960" fill="#15121c" opacity=".55"/>
  <text x="270" y="190" text-anchor="middle" {TH} font-size="32" font-weight="700" fill="#fff">ซิ่งควรอยู่บ้านไหน?</text>
  {oc2}
  <g transform="translate(270,578)"><rect x="-150" y="-20" width="300" height="38" rx="19" fill="#2a2440" stroke="#8a6cd8"/><text y="5" text-anchor="middle" {TH} font-size="15" font-weight="600" fill="#e8e2f4">พิมพ์ A B C หรือ D ในคอมเมนต์</text></g>''')

vote_page = page.split('<div class="wrap">')[0] + '<div class="wrap"><div class="grid">' + "".join(f'<figure class="panel"><div class="frame">{vote_svg(i)}</div></figure>' for i in range(4)) + '</div></div>'
(HERE / "vote.html").write_text(vote_page)

step_page = page.split('<div class="wrap">')[0] + '<style>html,body{background:transparent}</style><div class="wrap"><div class="grid">' + "".join(f'<figure class="panel"><div class="frame">{step_card(k)}</div></figure>' for k in range(1, 6)) + '</div></div>'
(HERE / "steps.html").write_text(step_page)
