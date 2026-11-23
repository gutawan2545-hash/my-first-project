# สร้าง storyboard.html: สตอรี่บอร์ดเต็มทั้งคลิป (ตาม script.md v7) เฟรม 9:16 (540x960)
# ใช้ตัวละครจาก cast.html (ดึงบล็อก <defs> มาใช้ซ้ำ ไม่วาดหน้าใหม่)
import pathlib, re, random
HERE = pathlib.Path(__file__).parent
cast = (HERE / "cast.html").read_text()
DEFS = re.search(r'<svg width="0" height="0"[^>]*><defs>(.*?)</defs></svg>', cast, re.S).group(1)

TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
SUB_TH = TH + ' font-weight="700" font-size="20" fill="#ffd84a" stroke="#1a1420" stroke-width="5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'
SUB_EN = 'font-family="Inter, sans-serif" font-weight="500" font-size="13" fill="#fff" stroke="#1a1420" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'
POP = TH + ' font-weight="700" fill="#fff4d0" stroke="#3a1e16" stroke-width="5" paint-order="stroke" stroke-linejoin="round"'

def subs(th, en):
    y = 712 - (len(th) * 27 + len(en) * 17) / 2 + 20
    out = ""
    for line in th:
        out += f'<text x="270" y="{y:.0f}" {SUB_TH}>{line}</text>'; y += 27
    y += 2
    for line in en:
        out += f'<text x="270" y="{y:.0f}" {SUB_EN}>{line}</text>'; y += 17
    return out

def badge(t):
    w = 22 + len(t) * 9.2
    return f'''<g transform="translate(22,26)"><rect width="{w:.0f}" height="30" rx="15" fill="#15121c" fill-opacity=".85" stroke="#8a6cd8" stroke-width="1.4"/>
    <text x="{w/2:.0f}" y="20" text-anchor="middle" {TH} font-weight="600" font-size="14" fill="#e8e2f4">{t}</text></g>'''

def card(x, y, w, t1, t2="", tx=None, ty=None):
    """กล่องคำอธิบายสีขาวนวล + เส้นประชี้จุด"""
    line = f'<path d="M {x + w/2:.0f},{y+ (56 if t2 else 40)} L {tx},{ty}" stroke="#f6f1e6" stroke-width="2" stroke-dasharray="5 4"/>' if tx is not None else ""
    h = 62 if t2 else 44
    sub = f'<text x="14" y="50" {TH} font-size="13" fill="#5a5260">{t2}</text>' if t2 else ""
    return f'{line}<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="10" fill="#f6f1e6"/><text x="14" y="28" {TH} font-size="15" font-weight="600" fill="#2a2430">{t1}</text>{sub}</g>'

EYE = '<g transform="translate(500,40)" opacity=".75"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="#b18cff"/><circle r="4" fill="#1b1f2b"/></g>'
GRAIN = '<rect width="540" height="960" filter="url(#grain)" opacity=".09"/>'

def dust(cx, cy, w, h, n=14, seed=1, col="#fff4e0"):
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, y = cx + r.uniform(-w/2, w/2), cy + r.uniform(-h/2, h/2)
        if r.random() < .5:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.8,1.6):.1f}" fill="{col}" opacity="{r.uniform(.5,.85):.2f}" filter="url(#glow)"/>'
        else:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,4):.1f}" fill="{col}" opacity="{r.uniform(.12,.25):.2f}" filter="url(#soft)"/>'
    return out

def shadow(cx, cy, rx, ry=12, o=.4):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity="{o}" filter="url(#shadow)"/>'

def speed(x0, y0, x1, n=6, seed=2, col="#e8e2f4"):
    r = random.Random(seed)
    return "".join(f'<path d="M {x0},{y0 + i*r.uniform(16,26):.0f} L {x1 + r.uniform(-30,30):.0f},{y0 + i*r.uniform(16,26):.0f}" stroke="{col}" stroke-width="{r.uniform(1.5,3):.1f}" stroke-linecap="round" opacity=".55"/>' for i in range(n))

DEFS_SB = '''
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.4 -.5"/></filter>
<filter id="bgblur"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="bgblur2"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation=".7"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<linearGradient id="morning" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8a8cc0"/><stop offset=".6" stop-color="#d6b8c8"/><stop offset="1" stop-color="#f2d6c4"/></linearGradient>
<linearGradient id="roomwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4258"/><stop offset="1" stop-color="#5a5064"/></linearGradient>
<linearGradient id="shopwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5a2a32"/><stop offset="1" stop-color="#3e1e26"/></linearGradient>
<linearGradient id="nightsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#121a36"/><stop offset="1" stop-color="#2c3c68"/></linearGradient>
<linearGradient id="hall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1626"/><stop offset="1" stop-color="#3a2e3a"/></linearGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0e0" stop-opacity=".32"/><stop offset="1" stop-color="#fff0e0" stop-opacity="0"/></linearGradient>
<radialGradient id="portal"><stop offset="0" stop-color="#fff6e0"/><stop offset=".35" stop-color="#f4d6a0" stop-opacity=".9"/><stop offset="1" stop-color="#b18cff" stop-opacity="0"/></radialGradient>
<radialGradient id="pingpong"><stop offset="0" stop-color="#fff4dc"/><stop offset=".5" stop-color="#ffe2b8" stop-opacity=".6"/><stop offset="1" stop-color="#ffe2b8" stop-opacity="0"/></radialGradient>
<radialGradient id="candle"><stop offset="0" stop-color="#fff0d8" stop-opacity=".9"/><stop offset="1" stop-color="#fff0d8" stop-opacity="0"/></radialGradient>
'''

def frame(inner):
    return f'<svg viewBox="0 0 540 960" role="img"><defs><clipPath id="fr"><rect width="540" height="960"/></clipPath></defs><g clip-path="url(#fr)">{inner}{GRAIN}</g></svg>'

SK, SKS = "#e8b88e", "#cc9a70"   # ผิวซิ่ง

def bike_side(x, y, s=1.0, rot=0, body="#1c1b22", trim="#c8432e"):
    """มอเตอร์ไซค์ป๊อปแต่งซิ่ง หันข้างเต็ม หน้ารถไปทางซ้าย"""
    return f'''<g transform="translate({x},{y}) rotate({rot}) scale({s})">
    <circle cx="-70" cy="0" r="30" fill="#141318"/><circle cx="-70" cy="0" r="14" fill="#c4c8d4"/><circle cx="-70" cy="0" r="5" fill="#141318"/>
    <circle cx="70" cy="0" r="30" fill="#141318"/><circle cx="70" cy="0" r="14" fill="#c4c8d4"/><circle cx="70" cy="0" r="5" fill="#141318"/>
    <path d="M -70,0 L -50,-70 L -44,-70 L -62,0 Z" fill="#9aa0aa"/>
    <path d="M -58,-60 C -30,-40 20,-44 60,-40 L 76,-20 L 30,-14 L -30,-14 Z" fill="{body}"/>
    <path d="M -56,-62 C -30,-74 10,-70 40,-56 L 60,-40 C 20,-46 -20,-46 -56,-62 Z" fill="{trim}"/>
    <path d="M 0,-58 L 60,-54 C 66,-54 70,-50 68,-46 L 4,-46 Z" fill="#2a2830"/>
    <path d="M 20,-14 L 110,-30 L 114,-20 L 24,-6 Z" fill="#c4c8d4"/><ellipse cx="112" cy="-25" rx="6" ry="8" fill="#5a5e6a"/>
    <path d="M -54,-72 L -40,-92 L -34,-90 L -48,-70 Z" fill="#2a2830"/><circle cx="-62" cy="-56" r="8" fill="#f4e6b0"/>
    <path d="M -10,-20 L 10,-20 L 0,8 Z" fill="#3a3d48"/>
    <text x="-6" y="-26" font-family="Inter, sans-serif" font-size="11" font-weight="700" fill="#f0c050" transform="skewX(-12)">ZING</text>
    </g>'''

def shophouses(x0=0, w=540, horizon=600, sign=True, blur=True):
    """ตึกแถวเยาวราชสามชั้น ร้านทองชั้นล่าง"""
    g = []
    for i, (bx, col) in enumerate([(-40, "#8a6e72"), (140, "#7e6670"), (320, "#8c7268"), (500, "#74606c")]):
        g.append(f'<rect x="{bx}" y="{horizon-470}" width="180" height="470" fill="{col}"/>')
        for fy in (horizon-430, horizon-300):
            g.append(f'<rect x="{bx+24}" y="{fy}" width="132" height="90" fill="#3a3040"/>')
            g.append("".join(f'<rect x="{bx+24+k*22}" y="{fy}" width="3" height="90" fill="#9aa0aa" opacity=".7"/>' for k in range(7)))
            g.append(f'<rect x="{bx+14}" y="{fy+92}" width="152" height="8" fill="#5a4a50"/>')
        g.append(f'<rect x="{bx}" y="{horizon-160}" width="180" height="160" fill="#2a2228"/>')
    if sign:
        g.append(f'<rect x="150" y="{horizon-200}" width="160" height="44" fill="#7a1e24"/><rect x="154" y="{horizon-196}" width="152" height="36" fill="none" stroke="#e0b84a" stroke-width="2"/>')
        g.append(f'<text x="230" y="{horizon-170}" text-anchor="middle" {TH} font-size="20" font-weight="700" fill="#f0d070">ห้างทอง ซิ่งเฮง</text>')
        g.append(f'<rect x="150" y="{horizon-150}" width="160" height="150" fill="#5a2a32"/><rect x="160" y="{horizon-120}" width="140" height="70" fill="#d8b860" opacity=".55"/>')
        g.append("".join(f'<rect x="150" y="{horizon-150 + k*10}" width="160" height="2" fill="#3a2028" opacity=".6"/>' for k in range(3)))
    g.append(f'<path d="M -10,{horizon-480} C 120,{horizon-440} 300,{horizon-450} 560,{horizon-470} M -10,{horizon-450} C 160,{horizon-410} 360,{horizon-420} 560,{horizon-445}" fill="none" stroke="#1a1620" stroke-width="2"/>')
    return f'<g {"filter=\"url(#bgblur)\"" if blur else ""}>{"".join(g)}</g>'

# ---------- 1 หน้าตึกแถวเยาวราชตอนเช้า ----------
p1 = frame(f'''<rect width="540" height="960" fill="url(#morning)"/>
  {shophouses(horizon=640)}
  <rect y="640" width="540" height="320" fill="#4a4250"/><rect y="640" width="540" height="8" fill="#5a5260"/>
  <path d="M 540,0 L 540,260 L 120,960 L 0,960 L 0,700 Z" fill="url(#beam)" opacity=".7"/>
  {dust(330, 380, 300, 300, 18, 11)}
  <g transform="translate(232,330) scale(.5)"><use href="#c_sing"/></g>
  <rect x="140" y="300" width="200" height="8" fill="#5a4a50"/><g fill="#9aa0aa">{"".join(f'<rect x="{150+k*18}" y="262" width="3" height="40"/>' for k in range(11))}</g>
  <rect x="140" y="260" width="200" height="4" fill="#9aa0aa"/>
  {card(330, 110, 180, "ห้องซิ่ง ชั้นสาม", "บิดขี้เกียจรับแดดเช้า", 260, 200)}
  {badge("เยาวราช · 06:30")}{EYE}
  {subs(["ถ้าเด็กแว้นอย่างผม ได้จดหมายเชิญ", "ไปเรียนฮอกวอตส์ สาขาประเทศไทย", "คุณว่าผมจะรอดไหมครับ"], ["If a street racer like me got invited to", "Hogwarts, Thailand branch, think I’d survive?"])}''')

def room():
    return f'''<g filter="url(#bgblur)">
    <rect width="540" height="960" fill="url(#roomwall)"/>
    <rect x="300" y="120" width="200" height="250" fill="url(#morning)"/>
    <g fill="#3a3040">{"".join(f'<rect x="{300+k*25}" y="120" width="4" height="250"/>' for k in range(9))}{"".join(f'<rect x="300" y="{120+k*50}" width="200" height="4"/>' for k in range(6))}</g>
    <path d="M 294,114 L 506,114 L 506,376 L 294,376 Z M 300,120 L 300,370 L 500,370 L 500,120 Z" fill="#6a6070" fill-rule="evenodd"/>
    <rect x="40" y="140" width="150" height="200" fill="#1c1b22"/><rect x="48" y="148" width="134" height="184" fill="#c8432e"/>
    <path d="M 60,300 C 80,260 150,250 172,290 L 172,320 L 60,320 Z" fill="#1c1b22"/><circle cx="84" cy="318" r="14" fill="#1c1b22"/><circle cx="150" cy="318" r="14" fill="#1c1b22"/>
    <text x="115" y="200" text-anchor="middle" font-family="Inter, sans-serif" font-size="24" font-weight="800" fill="#f0c050" transform="skewX(-10)">SPEED</text>
    <rect y="640" width="540" height="320" fill="#3a3440"/><rect y="640" width="540" height="6" fill="#4a4250"/>
    </g>'''

# ---------- 2 ห้องนอน ไก่เกาะแฮนด์ขัน ซิ่งตกฟูก ----------
p2 = frame(f'''{room()}
  <path d="M 300,120 L 0,700 L 0,960 L 200,960 L 500,370 Z" fill="url(#beam)"/>
  {dust(260, 420, 280, 300, 16, 5)}
  {shadow(300, 640, 170)}
  {bike_side(310, 610, 1.3)}
  <g transform="translate(250,494) scale(1.25)"><use href="#c_rooster"/><path d="M -26,-145 L -42,-136 L -27,-140 Z" fill="#c4922a"/></g>
  <text x="34" y="120" font-size="40" transform="rotate(-8 34 120)" {POP}>เอ้กอี๊เอ้กกก!!</text>
  <path d="M 180,280 L 210,262 M 186,300 L 220,296 M 180,320 L 210,334" stroke="#fff4d0" stroke-width="3" stroke-linecap="round" opacity=".8"/>
  <rect x="300" y="680" width="260" height="60" rx="6" fill="#6a6080"/><rect x="300" y="680" width="260" height="12" fill="#7a7090"/>
  <g transform="translate(470,860) rotate(-64) scale(1.15)"><use href="#c_sing"/></g>
  <text x="440" y="560" font-size="34" {POP}>!?</text>
  {badge("06:31")}{EYE}
  {subs(["เช้านี้ไก่ชนมาเกาะแฮนด์รถผม", "แล้วขันใส่หน้า"], ["This morning a fighting rooster perched", "on my bike and crowed in my face."])}''')

# ---------- 3 Close-up ซิ่งอ่านจดหมาย ----------
p3 = frame(f'''{room()}
  <g transform="translate(90,380) scale(.8)" filter="url(#bgblur)"><use href="#c_rooster"/></g>
  <g transform="translate(270,320) scale(3.6)">
    <path d="M -54,72 C -52,58 -32,50 -12,49 L 12,49 C 32,50 52,58 54,72 L 58,120 L -58,120 Z" fill="#1c1b22"/>
    <path d="M -54,72 C -52,60 -36,52 -20,50 C -26,60 -28,90 -28,120 L -58,120 Z" fill="#2c2b35"/>
    <path d="M 24,50 C 38,53 52,60 54,72 L 58,120 L 32,120 C 32,90 30,56 24,50 Z" fill="#111016"/>
    <path d="M -12,49 C -8,61 8,61 12,49" fill="none" stroke="#2c2b35" stroke-width="4"/>
    <g transform="translate(0,2)"><use href="#c_sing" transform="translate(0,480)" visibility="hidden"/></g>
  </g>
  <g transform="translate(270,328) scale(3.6)">{re.search(r'SING_HEAD_PLACEHOLDER', 'SING_HEAD_PLACEHOLDER').group(0)}</g>
  {shadow(290, 600, 150, 16, .3)}
  <g transform="rotate(-4 270 500)">
    <rect x="120" y="420" width="300" height="170" rx="4" fill="#f4ecd8"/><rect x="120" y="420" width="300" height="10" fill="#e6dcc4"/>
    <circle cx="390" cy="560" r="14" fill="#8e1b24"/><circle cx="388" cy="558" r="5" fill="#b8323e"/>
    <text x="140" y="458" {TH} font-size="16" font-weight="700" fill="#3a2a22">ฮอกวอตส์ สาขาประเทศไทย</text>
    <g fill="#b8aa90"><rect x="140" y="472" width="230" height="4"/><rect x="140" y="484" width="200" height="4"/></g>
    <rect x="136" y="498" width="150" height="22" fill="#ffd84a" opacity=".55"/>
    <text x="142" y="514" {TH} font-size="14" font-weight="600" fill="#3a2a22">ไม่พิจารณาเกรด</text>
    <g fill="#b8aa90"><rect x="140" y="532" width="220" height="4"/><rect x="140" y="544" width="160" height="4"/></g>
    <path d="M 112,560 C 100,540 104,520 118,512 L 132,590 C 120,592 114,580 112,560 Z" fill="{SK}"/>
    <path d="M 428,560 C 440,540 436,520 422,512 L 408,590 C 420,592 426,580 428,560 Z" fill="{SKS}"/>
  </g>
  {card(340, 120, 170, "เกรดเฉลี่ย 1.50", "ผ่านแบบเฉียดฉิว", 330, 420)}
  {badge("06:33")}{EYE}
  {subs(["ฮอกวอตส์ สาขาประเทศไทย… ไม่ดูเกรด!", "เกรดผมหนึ่งจุดห้าเองนะ"], ["Hogwarts Thailand… grades don’t matter!", "Mine’s a 1.5."])}''')

# ---------- 4 ร้านทอง อาม้ากัดเหรียญ ----------
p4 = frame(f'''<g filter="url(#bgblur)">
  <rect width="540" height="960" fill="url(#shopwall)"/>
  <rect x="30" y="120" width="480" height="180" fill="#3a1a20"/>
  {"".join(f'<path d="M {60+k*44},140 C {70+k*44},200 {90+k*44},200 {100+k*44},140" fill="none" stroke="#e0b84a" stroke-width="4"/>' for k in range(10))}
  {"".join(f'<path d="M {50+k*48},210 C {62+k*48},270 {86+k*48},270 {98+k*48},210" fill="none" stroke="#c9a24a" stroke-width="3"/>' for k in range(9))}
  <rect x="200" y="60" width="140" height="40" fill="#7a1e24"/><text x="270" y="88" text-anchor="middle" {TH} font-size="18" font-weight="700" fill="#f0d070">ซิ่งเฮง</text>
  <rect y="640" width="540" height="320" fill="#2a1a1e"/>
  </g>
  {shadow(220, 640, 120)}
  <g transform="translate(220,700) scale(1.15)"><use href="#c_ama"/></g>
  <rect x="0" y="560" width="400" height="120" fill="#3a2028"/><rect x="0" y="560" width="400" height="10" fill="#c9a24a" opacity=".6"/>
  <rect x="20" y="572" width="360" height="60" fill="#d8b860" opacity=".35"/>
  {"".join(f'<rect x="{40+k*60}" y="590" width="40" height="22" rx="3" fill="#e8c24a"/>' for k in range(6))}
  <g transform="translate(232,302)"><circle r="12" fill="#e8c24a"/><circle r="8" fill="#f4d878"/></g>
  <path d="M 214,300 l -10,-8 M 214,312 l -12,2 M 250,296 l 10,-8" stroke="#fff4d0" stroke-width="2.4" stroke-linecap="round"/>
  {shadow(450, 690, 70)}
  <g transform="translate(450,760) scale(1.0)"><use href="#c_sing"/></g>
  <rect x="404" y="430" width="44" height="30" fill="#f4ecd8" transform="rotate(-10 426 445)"/>
  <text x="290" y="200" font-size="30" {POP}>งั่ม!</text>
  {card(30, 360, 170, "ม๊าเช็กทองแท้", "กัดก่อน ชั่งทีหลัง", 222, 304)}
  {badge("ร้านทองชั้นล่าง · 07:00")}{EYE}
  {subs(["จ่ายค่าเทอมเป็นเหรียญทองเหรอ", "เอามาให้ม๊าชั่งก่อน!"], ["Tuition in gold coins?", "Bring them here, Ma’s weighing them first!"])}''')

# ---------- 5 ซอย ล้อหน้าลอย ----------
p5 = frame(f'''<rect width="540" height="960" fill="url(#morning)"/>
  <g filter="url(#bgblur2)">{shophouses(horizon=600, sign=False, blur=False)}</g>
  <rect y="600" width="540" height="360" fill="#4a4250"/><path d="M 0,700 L 540,700" stroke="#e8e2f4" stroke-width="4" stroke-dasharray="40 30" opacity=".5"/>
  {speed(380, 300, 540, 10, 4)}
  {shadow(270, 640, 190, 14)}
  <g transform="translate(270,560) rotate(-18)">
    <g transform="translate(46,-40) scale(.62)"><use href="#c_giant"/></g>
    <g transform="translate(-14,-40) scale(.7)"><use href="#c_sing"/></g>
    {bike_side(0, 0, 1.3)}
  </g>
  <text x="34" y="200" font-size="34" transform="rotate(-10 34 200)" {POP}>ล้อหน้าลอย!</text>
  {card(330, 120, 180, "ไม่ได้ยกล้อ", "ลุงหนักเกิน 200 กก.", 330, 360)}
  {badge("ซอยเยาวราช")}{EYE}
  {subs(["ลุงโตมารับ ผมเลยขี่รถพาไป ล้อหน้าลอยทั้งทาง", "ไม่ได้ยกล้อนะ ลุงหนัก"], ["Uncle To came to get me, so I rode him there.", "Not a wheelie. He’s just heavy."])}''')

def spirit_house(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})">
    <rect x="-10" y="0" width="20" height="160" fill="#d8d0c4"/><rect x="-10" y="0" width="7" height="160" fill="#efe8dc"/>
    <rect x="-70" y="-6" width="140" height="10" fill="#c8bfb2"/>
    <rect x="-50" y="-90" width="100" height="86" fill="#efe8dc"/><rect x="-50" y="-90" width="34" height="86" fill="#fbf6ee"/><rect x="20" y="-90" width="30" height="86" fill="#d8d0c4"/>
    <path d="M -16,-4 L -16,-60 C -16,-72 16,-72 16,-60 L 16,-4 Z" fill="#7a1e24"/>
    <path d="M -64,-90 L 64,-90 L 40,-130 L -40,-130 Z" fill="#c8432e"/><path d="M -64,-90 L -40,-130 L -20,-130 L -40,-90 Z" fill="#e06a52"/>
    <path d="M -40,-130 L 40,-130 L 20,-170 L -20,-170 Z" fill="#c8432e"/><path d="M -20,-170 L 20,-170 L 0,-210 Z" fill="#e0b84a"/>
    <path d="M -64,-90 L -76,-104 M 64,-90 L 76,-104 M -40,-130 L -52,-144 M 40,-130 L 52,-144" stroke="#e0b84a" stroke-width="5" stroke-linecap="round"/>
    <path d="M -50,-90 L 50,-90 L 50,-84 L -50,-84 Z" fill="#e0b84a"/>
    </g>'''

def zebra(x, y, s=1.0, blink=False):
    eye = '<path d="M -10,-38 Q -7,-35 -4,-38" fill="none" stroke="#1a1a20" stroke-width="1.6"/>' if blink else '<circle cx="-7" cy="-38" r="2" fill="#1a1a20"/>'
    return f'''<g transform="translate({x},{y}) scale({s})">
    <rect x="-14" y="-20" width="5" height="20" fill="#f4f4f4"/><rect x="8" y="-20" width="5" height="20" fill="#e0e0e0"/>
    <path d="M -18,-34 L 18,-34 L 18,-18 L -18,-18 Z" fill="#f4f4f4"/><g fill="#1a1a20"><rect x="-12" y="-34" width="3" height="16"/><rect x="-2" y="-34" width="3" height="16"/><rect x="8" y="-34" width="3" height="16"/></g>
    <path d="M -18,-34 L -20,-50 L -8,-52 L -4,-34 Z" fill="#f4f4f4"/><path d="M -20,-50 L -16,-56 L -12,-50 Z" fill="#1a1a20"/>
    <path d="M -26,-44 L -18,-48 L -16,-40 L -24,-38 Z" fill="#f4f4f4"/>{eye}
    </g>'''

# ---------- 6 ศาลพระภูมิ ----------
p6 = frame(f'''<rect width="540" height="960" fill="url(#morning)"/>
  <g filter="url(#bgblur2)">{shophouses(horizon=620, sign=False, blur=False)}</g>
  <rect y="620" width="540" height="340" fill="#4a4250"/>
  {shadow(150, 640, 60, 10, .35)}
  {spirit_house(150, 470, 1.1)}
  {zebra(108, 470, 1.2)}{zebra(150, 470, 1.2)}{zebra(192, 470, 1.2)}
  <g transform="translate(206,420)"><rect x="-8" y="-40" width="16" height="40" rx="4" fill="#c8243a" opacity=".85"/><path d="M 2,-40 L 10,-62" stroke="#f4f4f4" stroke-width="2.4"/></g>
  {shadow(370, 650, 130)}
  <g transform="translate(380,940) scale(.98)"><use href="#c_giant"/></g>
  <g transform="translate(300,350)"><rect x="-10" y="-46" width="20" height="46" rx="5" fill="#c8243a"/><rect x="-10" y="-30" width="20" height="10" fill="#f4f4f4" opacity=".8"/><path d="M 2,-46 L 12,-70" stroke="#f4f4f4" stroke-width="3"/></g>
  {shadow(250, 660, 60, 10, .35)}
  <g transform="translate(252,700) scale(.9)"><use href="#c_sing"/></g>
  <path d="M 246,370 C 242,350 250,330 256,328 C 262,330 268,350 264,370 Z" fill="{SK}"/><path d="M 255,330 L 255,370" stroke="{SKS}" stroke-width="1.4"/>
  {card(20, 120, 190, "น้ำแดงเสียบหลอด", "ของไหว้ยอดนิยม", 205, 380)}
  {badge("ปากซอย")}{EYE}
  {subs(["ทางเข้าโลกเวทมนตร์ ต้องถวายน้ำแดง", "ศาลพระภูมิก่อนนะไอ้หนู"], ["To enter the magic world, first offer", "red soda to the spirit house, kid."])}''')

# ---------- 7 วูบ ประตูศาลเปิด ----------
rays = "".join(f'<path d="M 270,330 L {270 + 900*__import__("math").cos(a/24*6.283):.0f},{330 + 900*__import__("math").sin(a/24*6.283):.0f}" stroke="#fff0d0" stroke-width="{6 if a%2 else 2}" opacity=".25"/>' for a in range(24))
p7 = frame(f'''<rect width="540" height="960" fill="#2a2238"/>
  {rays}
  <circle cx="270" cy="330" r="260" fill="url(#portal)"/>
  {spirit_house(270, 470, 2.2)}
  <circle cx="270" cy="400" r="70" fill="url(#portal)"/>
  {zebra(150, 620, 2.6, True)}{zebra(270, 640, 2.6, True)}{zebra(390, 620, 2.6, True)}
  <g transform="translate(250,420) rotate(25) scale(.32)" opacity=".85"><use href="#c_sing"/></g>
  <g transform="translate(300,410) rotate(-30) scale(.3)" opacity=".85"><use href="#c_giant"/></g>
  <text x="40" y="150" font-size="44" transform="rotate(-6 40 150)" {POP}>วู้บบบ!!</text>
  {card(320, 690, 200, "ม้าลายกะพริบตา", "พร้อมกันทั้งสามตัว", 300, 580)}
  {EYE}''')

def pingpong(y0, n=9, seed=1):
    r = random.Random(seed); out = f'<path d="M -10,{y0} C 180,{y0+40} 360,{y0+40} 560,{y0}" fill="none" stroke="#1a1620" stroke-width="2"/>'
    for i in range(n):
        t = (i + .5) / n; x = -10 + 570 * t; y = y0 + 40 * 4 * t * (1 - t) * .75 + 8
        out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="18" fill="url(#pingpong)"/><circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#fff4dc"/>'
    return out

def market_bg():
    return f'''<rect width="540" height="960" fill="url(#nightsky)"/>
    <g filter="url(#bgblur2)">
      {"".join(f'<g transform="translate({x},420)"><path d="M -70,0 L 70,0 L 60,-40 L -60,-40 Z" fill="{c}"/>{"".join(f"<path d=\"M {-70+k*28},0 L {-56+k*28},0 L {-48+k*28},-40 L {-60+k*28},-40 Z\" fill=\"#f2ead8\" opacity=\".7\"/>" for k in range(5))}<rect x="-64" y="0" width="128" height="200" fill="#3a3040"/></g>' for x, c in [(60,"#8e1b24"),(220,"#2f5e8a"),(390,"#2f6b4a"),(540,"#7a4a8a")])}
      <path d="M 80,200 L 150,190 L 160,196 L 90,206 Z" fill="#9a7444"/><path d="M 380,240 L 450,228 L 460,234 L 390,246 Z" fill="#9a7444"/>
      <circle cx="460" cy="150" r="14" fill="#c8432e" opacity=".8"/><circle cx="110" cy="120" r="12" fill="#c8432e" opacity=".7"/>
    </g>
    {pingpong(250, 9, 3)}{pingpong(330, 8, 4)}
    <rect y="620" width="540" height="340" fill="#2a2430"/>'''

# ---------- 8 ป้าแต๋วตะโกน ----------
p8 = frame(f'''{market_bg()}
  {dust(270, 300, 500, 200, 16, 21, "#ffe8c8")}
  {shadow(230, 640, 110)}
  <g transform="translate(230,700) scale(1.15)"><use href="#c_vendor"/></g>
  <rect x="0" y="560" width="540" height="100" fill="#5a3e28"/><rect x="0" y="560" width="540" height="10" fill="#7a5638"/>
  {"".join(f'<path d="M {20+k*14},{570} L {40+k*14},{520 - (k%3)*10}" stroke="{["#6a4a2c","#8a6a44","#9a7650","#5a3a22"][k%4]}" stroke-width="4" stroke-linecap="round"/>' for k in range(30))}
  <rect x="380" y="500" width="130" height="50" rx="4" fill="#f2ead8"/><text x="445" y="532" text-anchor="middle" {TH} font-size="20" font-weight="700" fill="#c43a3a">3 อัน 100</text>
  <text x="300" y="200" font-size="34" transform="rotate(6 300 200)" {POP}>จ้าาา!</text>
  {badge("ตลาดนัดเวทมนตร์")}{EYE}
  {subs(["ไม้กายสิทธิ์ สามอันร้อยจ้า", "เลือกเลยจ้า!"], ["Magic wands, three for a hundred baht!", "Pick one!"])}''')

# ---------- 9 ไม้ลูกชิ้น ----------
p9 = frame(f'''{market_bg()}
  <g filter="url(#bgblur2)" opacity=".9"><g transform="translate(270,1200) scale(2.4)"><use href="#c_sing"/></g></g>
  <path d="M 250,700 C 236,640 246,560 270,540 L 320,540 C 330,580 330,650 320,700 Z" fill="{SK}"/>
  <path d="M 300,540 L 320,540 C 330,580 330,650 320,700 L 306,700 C 312,640 310,580 300,540 Z" fill="{SKS}"/>
  <path d="M 268,560 C 256,552 254,540 264,534 L 300,540 L 296,566 Z" fill="{SK}"/>
  <path d="M 282,550 L 300,180" stroke="#d8c09a" stroke-width="7" stroke-linecap="round"/><path d="M 280,550 L 296,190" stroke="#efe0c0" stroke-width="2"/>
  <circle cx="298" cy="230" r="30" fill="#9a5a3a"/><circle cx="290" cy="222" r="11" fill="#b8784e"/><path d="M 278,240 C 290,248 306,248 318,236" fill="none" stroke="#7a4228" stroke-width="3"/>
  <circle cx="298" cy="230" r="70" fill="url(#portal)" opacity=".55"/>
  <path d="M 340,190 C 360,170 380,180 372,200 M 236,260 C 220,250 214,270 230,276 M 330,290 C 350,296 352,316 334,316" fill="none" stroke="#e8dcff" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>
  {card(30, 120, 180, "ไม้มะขาม?", "ไม่ใช่ ไม้เสียบลูกชิ้น", 270, 230)}
  {badge("ร้านไม้กายสิทธิ์")}{EYE}
  {subs(["แต่ไม้ที่เลือกผม", "ดันเป็นไม้เสียบลูกชิ้น"], ["But the wand that chose me", "was a meatball skewer."])}''')

# ---------- 10 ต้นเดินเข้าเฟรม ----------
p10 = frame(f'''{market_bg()}
  {dust(270, 300, 500, 200, 12, 31, "#ffe8c8")}
  {shadow(180, 650, 100)}
  <g transform="translate(180,720) scale(1.12)"><use href="#c_ton"/></g>
  {speed(0, 360, 70, 6, 8)}
  <g transform="translate(70,300) rotate(-8)"><rect x="-26" y="-46" width="52" height="92" rx="8" fill="#15161c"/><rect x="-22" y="-40" width="44" height="80" rx="4" fill="#3a2e5a"/>
    <circle cx="0" cy="-6" r="12" fill="#c98f62"/><path d="M -14,20 L 14,20 L 10,34 L -10,34 Z" fill="#4f8a5a"/><text x="0" y="-26" text-anchor="middle" {TH} font-size="10" font-weight="700" fill="#ffd84a">หมอลำ</text></g>
  {shadow(440, 660, 80)}
  <g transform="translate(440,730) scale(1.0)"><use href="#c_sing_robe"/></g>
  <text x="200" y="170" font-size="32" {POP}>เสี่ยวว!</text>
  {card(330, 120, 180, "พอร์ตหมอลำ", "ยื่นไปอันเดียว ติดเลย", 110, 290)}
  {badge("ตลาดนัดเวทมนตร์")}{EYE}
  {subs(["เสี่ยว! ข้อยกะติดคือกัน", "ยื่นพอร์ตหมอลำไปอันเดียว"], ["Buddy! I got in too.", "My only portfolio was folk singing."])}''')

# ---------- 11 ไม้กวาดแต่งท่อ เหนือปราสาท ----------
castle = '''<g fill="#1a1830"><rect x="60" y="460" width="70" height="200"/><path d="M 52,460 L 95,390 L 138,460 Z"/><rect x="150" y="420" width="90" height="240"/><path d="M 142,420 L 195,330 L 248,420 Z"/>
  <rect x="260" y="480" width="60" height="180"/><path d="M 252,480 L 290,420 L 328,480 Z"/><rect x="340" y="440" width="80" height="220"/><path d="M 332,440 L 380,360 L 428,440 Z"/><rect x="430" y="500" width="70" height="160"/></g>
  <g fill="#f0d8a0" opacity=".7"><rect x="180" y="460" width="8" height="12"/><rect x="200" y="500" width="8" height="12"/><rect x="370" y="480" width="8" height="12"/><rect x="90" y="500" width="8" height="12"/></g>'''
p11 = frame(f'''<rect width="540" height="960" fill="url(#nightsky)"/>
  <circle cx="420" cy="140" r="54" fill="#e8e6f4"/><circle cx="440" cy="130" r="54" fill="#121a36" opacity=".25"/>
  <g filter="url(#bgblur)">{castle}</g>
  <rect y="640" width="540" height="320" fill="#141228"/>
  {speed(380, 330, 540, 8, 9)}
  <g transform="translate(270,420) rotate(-8)">
    <ellipse cx="0" cy="40" rx="190" ry="20" fill="#b18cff" opacity=".35" filter="url(#soft)"/>
    <g transform="translate(-20,30) scale(.62)"><g transform="translate(70,0)"><use href="#c_ton"/></g><use href="#c_sing_robe"/></g>
    <path d="M -200,20 L 160,20 L 160,30 L -200,30 Z" fill="#9a7444"/><path d="M 160,6 L 230,-10 L 240,60 L 160,44 Z" fill="#c9a26a"/>
    {"".join(f'<path d="M 166,{12+k*6} L 236,{-2+k*12}" stroke="#a8844e" stroke-width="2"/>' for k in range(5))}
    <path d="M -190,10 L -120,10 L -120,40 L -190,40 Z" fill="#c4c8d4"/><ellipse cx="-192" cy="25" rx="8" ry="15" fill="#5a5e6a"/>
    <circle cx="-214" cy="20" r="14" fill="#e8e2f4" opacity=".5"/><circle cx="-236" cy="10" r="18" fill="#e8e2f4" opacity=".35"/><circle cx="-262" cy="2" r="22" fill="#e8e2f4" opacity=".22"/>
    <text x="-60" y="-4" font-family="Inter, sans-serif" font-size="12" font-weight="800" fill="#f0c050" transform="skewX(-12)">ZING</text>
  </g>
  <text x="30" y="250" font-size="44" transform="rotate(-8 30 250)" {POP}>แว้นนนน!!</text>
  {card(300, 690, 210, "ท่อสูตร + ไฟใต้ท้อง", "ดังทั้งปราสาท", 120, 450)}
  {badge("คืนแรก · 23:00")}{EYE}
  {subs(["ไม้กวาดบินได้ ผมจับแต่งท่อซะเลย", "บินทีดังทั้งปราสาท"], ["I modded my flying broom with a racing exhaust.", "The whole castle hears me."])}''')

def hall_bg():
    c = "".join(f'<g transform="translate({x},{y})"><rect x="-3" y="0" width="6" height="18" fill="#efe8dc"/><circle cy="-4" r="16" fill="url(#candle)"/><path d="M 0,-8 C 3,-4 2,0 0,0 C -2,0 -3,-4 0,-8 Z" fill="#fff0c8"/></g>' for x, y in [(60,140),(150,110),(250,150),(340,100),(430,140),(500,200),(100,220),(390,230)])
    return f'''<rect width="540" height="960" fill="url(#hall)"/>
    <g filter="url(#bgblur2)">
      {"".join(f'<path d="M {x},60 L {x+50},60 L {x+50},300 L {x+25},280 L {x},300 Z" fill="{col}"/>' for x, col in [(20,"#4a2a5a"),(140,"#3a2a4a"),(350,"#4a2a5a"),(470,"#3a2a4a")])}
      <path d="M 0,560 L 540,560 L 540,620 L 0,620 Z" fill="#4a3428"/>
    </g>{c}
    <rect y="620" width="540" height="340" fill="#2a2028"/>'''

# ---------- 12 เดรโก ปะทะ ต้น ----------
p12 = frame(f'''{hall_bg()}
  <g filter="url(#bgblur2)" opacity=".8"><g transform="translate(200,600) scale(.7)"><use href="#c_harry"/></g><g transform="translate(270,600) scale(.7)"><use href="#c_ron"/></g><g transform="translate(340,600) scale(.7)"><use href="#c_hermione"/></g></g>
  {shadow(150, 680, 100)}
  <g transform="translate(150,760) scale(1.12)"><use href="#c_draco"/></g>
  {shadow(400, 680, 100)}
  <g transform="translate(400,760) scale(1.12)"><use href="#c_ton"/></g>
  <text x="250" y="190" font-size="26" {POP} text-anchor="middle">ฮึ!</text>
  <text x="440" y="200" font-size="22" {POP}>ฮ่าๆ</text>
  {card(30, 120, 180, "นาสามร้อยไร่", "เดรโกเงียบกริบ", 400, 300)}
  {badge("ห้องโถงใหญ่")}{EYE}
  {subs(["(เดรโก) เสียงดังชะมัด พวกบ้านนอก", "(ต้น) บ้านนอกแต่มีนาสามร้อยไร่เด้อ"], ["(Draco) So loud. Country bumpkins.", "(Ton) Bumpkins with a 300-acre rice farm."])}''')

# ---------- 13 คัดบ้าน ----------
p13 = frame(f'''{hall_bg()}
  {shadow(440, 690, 90)}
  <g transform="translate(440,770) scale(1.05)" filter="url(#bgblur)"><use href="#c_strict"/></g>
  <rect x="190" y="560" width="160" height="20" rx="4" fill="#5a3e28"/><rect x="200" y="580" width="14" height="80" fill="#4a3222"/><rect x="326" y="580" width="14" height="80" fill="#4a3222"/>
  <g transform="translate(270,980) scale(1.7)"><use href="#c_sing_robe"/></g>
  <g transform="translate(272,128) scale(1.15) rotate(-4)"><use href="#c_hat"/></g>
  <text x="40" y="200" font-size="30" {POP}>อืมมม…</text>
  {card(330, 230, 180, "ใจกล้า เจ้าเล่ห์", "แต่ซิ่งเกิน", 300, 90)}
  {badge("พิธีคัดบ้าน")}{EYE}
  {subs(["ต้นน่ะง่าย ฮัฟเฟิลพัฟ! ส่วนเด็กแว้นคนนี้…", "ใจกล้า เจ้าเล่ห์ แต่ซิ่งเกิน…", "ให้คนดูเลือกแล้วกัน"], ["Ton’s easy, Hufflepuff! This street racer…", "brave, cunning, way too fast… let the viewers decide."])}''')

# ---------- 14 การ์ดโหวต ----------
opts = [("A", "กริฟฟินดอร์", "#8e1b24", "#d9b24a", True), ("B", "สลิธีริน", "#2a5e40", "#c4c8d4", False), ("C", "เรเวนคลอ", "#2a3e6e", "#b8905a", False), ("D", "ฮัฟเฟิลพัฟ", "#c99a2a", "#1a1a20", False)]
oc = ""
for i, (k, name, c1, c2, on) in enumerate(opts):
    x, y = 60 + (i % 2) * 220, 250 + (i // 2) * 150
    oc += f'''<g transform="translate({x},{y})" opacity="{1 if on else .72}">
    {'<rect x="-6" y="-6" width="212" height="132" rx="18" fill="none" stroke="#ffd84a" stroke-width="4"/>' if on else ''}
    <rect width="200" height="120" rx="14" fill="{c1}"/><rect y="96" width="200" height="24" rx="0" fill="{c2}" opacity=".85"/>
    <circle cx="34" cy="40" r="20" fill="#15121c" opacity=".55"/><text x="34" y="48" text-anchor="middle" font-family="Inter, sans-serif" font-size="22" font-weight="800" fill="#fff">{k}</text>
    <text x="64" y="50" {TH} font-size="20" font-weight="700" fill="#fff">{name}</text></g>'''
p14 = frame(f'''<rect width="540" height="960" fill="#15121c"/>
  <circle cx="270" cy="360" r="320" fill="#b18cff" opacity=".08"/>
  <text x="270" y="190" text-anchor="middle" {TH} font-size="32" font-weight="700" fill="#fff">ซิ่งควรอยู่บ้านไหน?</text>
  {oc}
  <path d="M 250,350 l 0,30 l 8,-8 l 6,14 l 6,-3 l -6,-13 l 11,0 Z" fill="#fff" stroke="#15121c" stroke-width="1.5"/>
  <g transform="translate(270,578)"><rect x="-150" y="-20" width="300" height="38" rx="19" fill="#2a2440" stroke="#8a6cd8"/><text y="5" text-anchor="middle" {TH} font-size="15" font-weight="600" fill="#e8e2f4">พิมพ์ A B C หรือ D ในคอมเมนต์</text></g>
  {subs(["ผมควรอยู่บ้านไหนดีครับ", "โหวตในคอมเมนต์เลย"], ["Which house should I be in?", "Vote in the comments."])}''')

# แทรกหัวของซิ่งจาก cast.html ในช็อต 3 (Close-up) ด้วยการใช้ทั้งตัวแล้วตัดเฉพาะส่วนบน
p3 = p3.replace('<g transform="translate(270,328) scale(3.6)">SING_HEAD_PLACEHOLDER</g>', '<g transform="translate(270,328) scale(3.6)"><clipPath id="hc"><rect x="-80" y="-90" width="160" height="140"/></clipPath><g clip-path="url(#hc)"><use href="#c_sing" transform="translate(0,478)"/></g></g>')

PANELS = [
  ("1", "4", p1, "Wide · หน้าตึกแถวเยาวราชตอนเช้า", "แสงเช้าส่องเฉียง ร้านทองชั้นล่างเพิ่งเปิด ซิ่งบิดขี้เกียจที่ระเบียงชั้นสาม · กล้องค่อย ๆ ซูมเข้าหาระเบียง", "เสียงเมืองตอนเช้า รถเข็นขายโจ๊ก · ดนตรีขี้เล่นเริ่ม · เสียงบรรยายซิ่ง"),
  ("2", "3.5", p2, "Medium Wide · ห้องนอนชั้นสาม", "รถจอดในห้อง ไอ้เหลืองเกาะแฮนด์แล้วขันใส่ ซิ่งตกฟูกหงายหลัง · กล้องสั่นสั้น ๆ ตอนขัน", "ดนตรีหยุดหนึ่งจังหวะ → เสียงไก่ขันดังลั่น + เสียงตุ้บ"),
  ("3", "3.5", p3, "Close-up · ซิ่งอ่านจดหมาย", "ซิ่งยกคิ้วข้างเดียว ยิ้มโชว์ฟันทอง · ไอ้เหลืองเบลอด้านหลัง · กล่องคำอธิบายเกรด 1.50", "ปากซิ่งขยับ (ซิ่งพูดเอง) · เสียง 'ติ๊ง' ตอนกล่องเด้ง"),
  ("4", "4", p4, "Medium · ร้านทองชั้นล่าง", "อาม้าในชุดนอน โรลม้วนผม กัดเหรียญเช็กทอง · ซิ่งยืนถือจดหมายข้างตู้ทอง", "ปากอาม้าขยับ · เสียง 'งั่ม' ตอนกัดเหรียญ"),
  ("5", "4", p5, "Wide · ซอยเยาวราช", "รถวิ่งล้อหน้าลอยทั้งคัน ลุงโตซ้อนท้ายตัวใหญ่กว่ารถ · กล้องแพนตาม", "เสียงท่อแว้น + เสียงลุงโตหัวเราะทุ้ม ๆ · เสียงบรรยายซิ่ง"),
  ("6", "3.5", p6, "Medium · ศาลพระภูมิปากซอย", "ลุงโตยื่นน้ำแดงเสียบหลอด ซิ่งพนมมือไหว้จริงจัง · ตุ๊กตาม้าลายสามตัวหน้าศาล", "ปากลุงโตขยับ · ดนตรีเบาลง ลึกลับนิด ๆ"),
  ("7", "3", p7, "Close-up → ซูมเบลอ", "ม้าลายกะพริบตาพร้อมกัน ประตูศาลเปิด แสงพุ่ง ทั้งสองคนหดตัวถูกดูดเข้าไป", "เงียบหนึ่งจังหวะ → เสียงวูบ (ใช้ครั้งเดียวทั้งคลิป)"),
  ("8", "4", p8, "Medium · ตลาดนัดเวทมนตร์", "ไฟปิงปอง ไม้กวาดบินผ่าน โคมลอย · ป้าแต๋วตะโกนหน้าแผง ป้าย '3 อัน 100'", "เสียงตลาดคึกคัก · ปากป้าแต๋วขยับ · ดนตรีตื่นตา"),
  ("9", "3", p9, "Close-up มือ · ร้านไม้กายสิทธิ์", "ไม้เสียบลูกชิ้นเหลือลูกเดียว มีแสงเวทมนตร์วูบวาบ · ซิ่งเบลออยู่ด้านหลัง หน้านิ่ง", "เสียงเวทมนตร์ใส ๆ แล้วตัดเงียบ · เสียงบรรยายซิ่ง"),
  ("10", "4", p10, "Medium · ต้นเดินเข้าเฟรมจากซ้าย", "ต้นเดินเข้าเฟรม ชูมือถือโชว์คลิปหมอลำ ผ้าขาวม้าพาดคอ ถือกระติบ · ซิ่งหันไปมอง", "เสียงแคนสั้น ๆ ตอนต้นเข้าเฟรม · ปากต้นขยับ"),
  ("11", "4", p11, "Wide · ฟ้าเหนือปราสาท", "ไม้กวาดติดท่อ ไฟใต้ท้องสีม่วง ควันพ่นเป็นวง ซิ่งขี่ ต้นซ้อนกอดกระติบ", "เสียงท่อแว้นยาว ๆ ก้องทั้งปราสาท · เสียงบรรยายซิ่ง"),
  ("12", "4.5", p12, "Medium · ห้องโถงใหญ่ (ตัดสลับ)", "เดรโกยิ้มเยาะ → ตัดไปต้นยิ้มแป้นตอบ เดรโกหน้าเหวอ · แฮร์รี่ รอน เฮอร์ไมโอนี่แอบขำด้านหลัง", "ปากเดรโกขยับก่อน แล้วปากต้น · กล้องตามคนพูด"),
  ("13", "4.5", p13, "Medium Close-up · พิธีคัดบ้าน", "หมวกบนหัวซิ่ง ครูมาลัยเบลอด้านข้าง · ซูมเข้าช้า ๆ · หมวกหันมองกล้อง ภาพหยุด", "ปากหมวกขยับ · ดนตรีลุ้นค่อย ๆ ดังขึ้นแล้วหยุด"),
  ("14", "4", p14, "การ์ดโหวต", "ไฮไลต์เลื่อนวน A → B → C → D ช้าพอให้อ่าน ตัวที่ถูกเลือกสว่างขึ้น · ไม่เฉลย", "เสียงคลิก UI ทุกครั้งที่สลับ · เสียงบรรยายซิ่ง · ต่อด้วยโลโก้ปิดท้าย 2.6 วิ"),
]
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
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:18px 16px; }}
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
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{DEFS}{DEFS_SB}</defs></svg>
<div class="wrap">
  <h1>สตอรี่บอร์ดเต็ม · ซิ่งไปฮอกวอตส์ สาขาประเทศไทย<span>{len(PANELS)} ช็อต · {total:g} วิ + โลโก้ปิดท้าย 2.6 วิ ≈ {total+2.6:.0f} วิ · เฟรม 9:16 ซับอยู่ช่วง 74% ของความสูง · ร่าง v1</span></h1>
  <div class="grid">{cards}</div>
  <p class="note">ภาพร่างนี้ใช้ตรวจองค์ประกอบ มุมกล้อง และจังหวะมุก ท่าทางพิเศษ (ขี่รถ ขี่ไม้กวาด ตกฟูก พนมมือ นั่งเก้าอี้) ยังใช้ท่ายืนแทน จะวาดท่าจริงในขั้นทำภาพนิ่ง</p>
</div>'''
(HERE / "storyboard.html").write_text(page)
print(len(PANELS), "panels", total, "sec")
