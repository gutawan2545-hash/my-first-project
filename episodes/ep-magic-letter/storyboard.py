# สร้าง storyboard.html: ร่างสตอรี่บอร์ดฉากส่งจดหมาย (ช็อต 1-5) เฟรม 9:16 (540x960)
# ใช้ตัวละครจาก cast.html (ดึงบล็อก <defs> มาใช้ซ้ำ ไม่วาดหน้าใหม่)
import pathlib, re
HERE = pathlib.Path(__file__).parent
cast = (HERE / "cast.html").read_text()
DEFS = re.search(r'<svg width="0" height="0"[^>]*><defs>(.*?)</defs></svg>', cast, re.S).group(1)

SUB_TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif" font-weight="700" font-size="20" fill="#ffd84a" stroke="#1a1420" stroke-width="5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'
SUB_EN = 'font-family="Inter, sans-serif" font-weight="500" font-size="13" fill="#fff" stroke="#1a1420" stroke-width="3.5" paint-order="stroke" stroke-linejoin="round" text-anchor="middle"'

def subs(th, en):
    """ซับไทยกับอังกฤษ จัดกลางรอบ y 712"""
    n = len(th) + len(en)
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
    <text x="{w/2:.0f}" y="20" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-weight="600" font-size="14" fill="#e8e2f4">{t}</text></g>'''

EYE = '<g transform="translate(500,40)" opacity=".75"><path d="M -14,0 C -8,-8 8,-8 14,0 C 8,8 -8,8 -14,0 Z" fill="#b18cff"/><circle r="4" fill="#1b1f2b"/></g>'
GRAIN = '<rect width="540" height="960" filter="url(#grain)" opacity=".09"/>'

def dust(cx, cy, w, h, n=14, seed=1):
    import random
    r = random.Random(seed); out = ""
    for _ in range(n):
        x, y = cx + r.uniform(-w/2, w/2), cy + r.uniform(-h/2, h/2)
        if r.random() < .5:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.8,1.6):.1f}" fill="#fff4e0" opacity="{r.uniform(.5,.85):.2f}" filter="url(#glow)"/>'
        else:
            out += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(2,4):.1f}" fill="#fff4e0" opacity="{r.uniform(.12,.25):.2f}" filter="url(#soft)"/>'
    return out

def bedroom(sky="night"):
    """ห้องนอน: หน้าต่างวิวตึก ตู้เสื้อผ้า กรอบรูป เตียงด้านหลัง (เบลอเบาให้ระยะชัดตื้น)"""
    glass = '<rect x="40" y="150" width="190" height="250" fill="url(#night)"/>' if sky == "night" else '<rect x="40" y="150" width="190" height="250" fill="url(#dawn)"/>'
    lit = "#e8d9b0" if sky == "night" else "#cfd4e8"
    return f'''<g filter="url(#bgblur)">
    <rect width="540" height="960" fill="url(#wall)"/>
    <rect y="610" width="540" height="350" fill="#241e2a"/><rect y="610" width="540" height="6" fill="#2e2634"/>
    {glass}
    <g fill="#26305a" opacity=".9"><rect x="50" y="300" width="30" height="100"/><rect x="86" y="260" width="40" height="140"/><rect x="134" y="320" width="26" height="80"/><rect x="166" y="280" width="36" height="120"/><rect x="206" y="330" width="24" height="70"/></g>
    <g fill="{lit}" opacity=".7"><rect x="94" y="272" width="4" height="5"/><rect x="108" y="290" width="4" height="5"/><rect x="94" y="320" width="4" height="5"/><rect x="174" y="296" width="4" height="5"/><rect x="186" y="330" width="4" height="5"/><rect x="58" y="320" width="4" height="5"/></g>
    <path d="M 34,144 L 236,144 L 236,406 L 34,406 Z M 40,150 L 40,400 L 230,400 L 230,150 Z" fill="#4a3f52" fill-rule="evenodd"/>
    <rect x="132" y="150" width="6" height="250" fill="#4a3f52"/><rect x="28" y="404" width="214" height="12" fill="#55485e"/>
    <rect x="386" y="120" width="140" height="490" fill="#3e3238"/><rect x="386" y="120" width="70" height="490" fill="#46393f"/><rect x="455" y="120" width="2" height="490" fill="#2a2228"/>
    <rect x="444" y="340" width="4" height="40" rx="2" fill="#a89a8a"/><rect x="464" y="340" width="4" height="40" rx="2" fill="#8a7c6e"/>
    <rect x="276" y="170" width="70" height="88" fill="#5a4a3e"/><rect x="284" y="178" width="54" height="72" fill="#7a8fb0"/><path d="M 284,250 L 304,214 L 318,232 L 326,220 L 338,250 Z" fill="#4a5a7a"/>
    <rect x="250" y="440" width="290" height="70" rx="8" fill="#55424c"/><rect x="250" y="500" width="290" height="120" fill="#5e5070"/><rect x="250" y="500" width="290" height="16" fill="#6e6080"/>
    <rect x="300" y="470" width="110" height="38" rx="14" fill="#cfc6d8"/>
    </g>'''

DEFS_SB = '''
<filter id="grain"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="2" seed="4"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 1.4 -.5"/></filter>
<filter id="bgblur"><feGaussianBlur stdDeviation="1.6"/></filter>
<filter id="soft"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation=".7"/></filter>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2232"/><stop offset="1" stop-color="#3a3042"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16203e"/><stop offset="1" stop-color="#2c3c68"/></linearGradient>
<linearGradient id="dawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4a4c7a"/><stop offset=".7" stop-color="#b89ab8"/><stop offset="1" stop-color="#f0c8b0"/></linearGradient>
<radialGradient id="screenglow"><stop offset="0" stop-color="#9fc4ff" stop-opacity=".55"/><stop offset="1" stop-color="#9fc4ff" stop-opacity="0"/></radialGradient>
<linearGradient id="beam" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe6cc" stop-opacity=".28"/><stop offset="1" stop-color="#ffe6cc" stop-opacity="0"/></linearGradient>
'''

def frame(inner):
    return f'<svg viewBox="0 0 540 960" role="img"><defs><clipPath id="fr"><rect width="540" height="960"/></clipPath></defs><g clip-path="url(#fr)">{inner}{GRAIN}</g></svg>'

SK, SKS = "#fbe7d8", "#efc7b0"

# ---------- P1: ห้องนอนกลางคืน เจมจ้องมือถือ ----------
p1 = frame(f'''{bedroom("night")}
  <ellipse cx="290" cy="985" rx="150" ry="20" fill="#000" opacity=".35" filter="url(#shadow)"/>
  <use href="#j_full" transform="translate(270,1010) scale(1.55)"/>
  <path d="M 336,612 L 352,606 L 322,470 L 304,476 Z" fill="{SK}"/><path d="M 336,612 L 344,609 L 316,472 L 310,474 Z" fill="{SKS}"/>
  <rect x="286" y="408" width="40" height="72" rx="7" fill="#15161c" transform="rotate(-8 306 444)"/>
  <rect x="290" y="413" width="32" height="60" rx="4" fill="#9fc4ff" transform="rotate(-8 306 444)"/>
  <ellipse cx="312" cy="470" rx="16" ry="12" fill="{SK}"/>
  <circle cx="300" cy="300" r="150" fill="url(#screenglow)"/>
  <path d="M 240,150 L 330,610 L 40,610 L 34,406 Z" fill="url(#beam)" opacity=".5"/>
  {dust(150, 420, 180, 260, 14, 3)}
  {badge("วันประกาศผล · 23:59")}{EYE}
  {subs(["ถ้าคุณสอบมหาลัยไม่ติด", "แต่ได้จดหมายตอบรับจากฮอกวอตส์", "สาขาประเทศไทย คุณจะไปไหมครับ"], ["If you failed every university, but got into", "Hogwarts, Thailand branch, would you go?"])}''')

# ---------- P2: จอมือถือ ผลไม่ผ่านทุกคณะ ----------
rows = [("คณะแพทยศาสตร์", False), ("คณะวิศวกรรมศาสตร์", False), ("คณะนิเทศศาสตร์", False), ("คณะไหนก็ได้ที่รับ", True)]
rr = ""
for i, (name, last) in enumerate(rows):
    y = 250 + i * 70
    rr += f'''<rect x="150" y="{y}" width="240" height="56" rx="10" fill="{'#3a1e26' if last else '#1e2230'}" stroke="{'#e05a5a' if last else 'none'}" stroke-width="1.5"/>
    <text x="164" y="{y+34}" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" font-weight="{600 if last else 500}" fill="#e6e7ee">{name}</text>
    <rect x="316" y="{y+16}" width="62" height="24" rx="12" fill="#c43a3a"/><text x="347" y="{y+33}" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" font-weight="600" fill="#fff">ไม่ผ่าน</text>'''
p2 = frame(f'''<rect width="540" height="960" fill="#1a1620"/>
  <rect width="540" height="960" fill="url(#wall)" opacity=".6" filter="url(#bgblur)"/>
  <ellipse cx="290" cy="560" rx="170" ry="40" fill="#000" opacity=".4" filter="url(#shadow)"/>
  <rect x="128" y="110" width="284" height="470" rx="34" fill="#15161c"/>
  <rect x="138" y="120" width="264" height="450" rx="26" fill="#101420"/>
  <rect x="236" y="130" width="68" height="16" rx="8" fill="#15161c"/>
  <text x="270" y="200" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" font-weight="600" fill="#e6e7ee">ผลการสมัครเรียน</text>
  <text x="270" y="226" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="12" fill="#80849a">ประกาศเมื่อ 23:59</text>
  {rr}
  <path d="M 96,620 C 90,560 110,500 140,470 L 150,560 C 150,600 140,640 130,660 Z" fill="{SK}"/><path d="M 444,620 C 450,560 430,500 400,470 L 390,560 C 390,600 400,640 410,660 Z" fill="{SKS}"/>
  <path d="M 140,470 C 160,460 176,470 172,490 L 150,500 Z" fill="{SK}"/><path d="M 400,470 C 380,460 364,470 368,490 L 390,500 Z" fill="{SKS}"/>
  <rect x="0" y="600" width="540" height="360" fill="#1a1620" opacity=".55"/>
  {badge("วันประกาศผล · 23:59")}{EYE}
  {subs(["ผลออกพร้อมกันทุกคณะ ไม่ติดสักที่", "ขนาดคณะไหนก็ได้ยังไม่รับ"], ["Rejected everywhere. Even “any faculty", "that’ll take me” said no."])}''')

# ---------- P3: ตีห้า ไก่ชนขันที่หน้าต่าง เจมตกเตียง ----------
p3 = frame(f'''{bedroom("dawn")}
  <path d="M 230,150 L 540,560 L 540,700 L 40,404 Z" fill="url(#beam)"/>
  {dust(300, 420, 300, 260, 18, 7)}
  <ellipse cx="150" cy="412" rx="70" ry="8" fill="#000" opacity=".35" filter="url(#soft)"/>
  <g transform="translate(150,406) scale(1.45)"><use href="#c_rooster"/>
    <path d="M -26,-145 L -42,-136 L -27,-140 Z" fill="#c4922a"/></g>
  <g font-family="IBM Plex Sans Thai, sans-serif" font-weight="700" fill="#fff4d0" stroke="#3a1e16" stroke-width="5" paint-order="stroke" stroke-linejoin="round">
    <text x="30" y="120" font-size="38" transform="rotate(-8 30 120)">เอ้กอี๊เอ้กกก!!</text></g>
  <path d="M 60,170 L 40,160 M 70,190 L 44,190 M 64,210 L 42,220" stroke="#fff4d0" stroke-width="3" stroke-linecap="round" opacity=".8"/>
  <rect x="250" y="560" width="300" height="80" fill="#5e5070"/><rect x="250" y="560" width="300" height="14" fill="#6e6080"/>
  <g transform="translate(420,700) rotate(-62) scale(1.25)"><use href="#j_full"/></g>
  <path d="M 470,440 l 6,-18 l 6,18 z M 500,470 l 5,-14 l 5,14 z" fill="#9fd0ff"/>
  <text x="478" y="420" font-family="IBM Plex Sans Thai, sans-serif" font-size="30" font-weight="700" fill="#fff4d0" stroke="#3a1e16" stroke-width="4" paint-order="stroke">!?</text>
  {badge("ตีห้า · 05:00")}{EYE}
  {subs(["นกฮูกที่อังกฤษงานล้น", "สาขาไทยเลยใช้ไก่ชนส่งจดหมายแทน"], ["The owls in England are overbooked,", "so the Thai branch uses fighting roosters."])}''')

# ---------- P4: Close-up เจมอ่านจดหมาย ----------
p4 = frame(f'''{bedroom("dawn")}
  <g transform="translate(70,330) scale(.9)" filter="url(#bgblur)"><use href="#c_rooster"/></g>
  <g transform="translate(270,320) scale(3.6)">
    <path d="M -50,72 C -48,58 -30,50 -12,49 L 12,49 C 30,50 48,58 50,72 L 54,120 L -54,120 Z" fill="#2b3768"/>
    <path d="M -50,72 C -48,60 -34,52 -20,50 C -24,58 -26,90 -26,120 L -54,120 Z" fill="#3e4d8e"/>
    <path d="M 22,50 C 36,53 48,60 50,72 L 54,120 L 30,120 C 30,90 28,56 22,50 Z" fill="#1c2448"/>
    <use href="#j_jhead"/>
    <path d="M -9,56 L 9,56 L 9,60 L -9,60 Z" fill="#2b3768"/><path d="M -12,49 C -8,61 8,61 12,49" fill="none" stroke="#1a2147" stroke-width="4"/>
  </g>
  <ellipse cx="290" cy="600" rx="150" ry="16" fill="#000" opacity=".3" filter="url(#shadow)"/>
  <g transform="rotate(-4 270 500)">
    <rect x="120" y="420" width="300" height="170" rx="4" fill="#f4ecd8"/><rect x="120" y="420" width="300" height="10" fill="#e6dcc4"/>
    <circle cx="390" cy="560" r="14" fill="#8e1b24"/><circle cx="388" cy="558" r="5" fill="#b8323e"/>
    <text x="140" y="458" font-family="IBM Plex Sans Thai, sans-serif" font-size="16" font-weight="700" fill="#3a2a22">ฮอกวอตส์ สาขาประเทศไทย</text>
    <g fill="#b8aa90"><rect x="140" y="472" width="230" height="4"/><rect x="140" y="484" width="200" height="4"/></g>
    <rect x="136" y="498" width="180" height="22" fill="#ffd84a" opacity=".55"/>
    <text x="142" y="514" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="600" fill="#3a2a22">ไม่ต้องยื่นพอร์ต ไม่ต้องสอบ</text>
    <g fill="#b8aa90"><rect x="140" y="532" width="220" height="4"/><rect x="140" y="544" width="160" height="4"/></g>
    <path d="M 112,560 C 100,540 104,520 118,512 L 132,590 C 120,592 114,580 112,560 Z" fill="{SK}"/>
    <path d="M 428,560 C 440,540 436,520 422,512 L 408,590 C 420,592 426,580 428,560 Z" fill="{SKS}"/>
  </g>
  <path d="M 318,500 L 400,400" stroke="#f6f1e6" stroke-width="2" stroke-dasharray="5 4"/>
  <g transform="translate(330,330)"><rect width="190" height="70" rx="10" fill="#f6f1e6"/><text x="14" y="30" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" font-weight="600" fill="#2a2430">ไม่ต้องยื่นพอร์ต</text><text x="14" y="54" font-family="IBM Plex Sans Thai, sans-serif" font-size="13" fill="#5a5260">ไม่ต้องสอบ ไม่ต้องสัมภาษณ์</text></g>
  {badge("ตีห้า · 05:02")}{EYE}
  {subs(["ฮอกวอตส์ สาขาประเทศไทย…", "ไม่ต้องยื่นพอร์ต ไม่ต้องสอบอะไรเลย"], ["Hogwarts, Thailand branch…", "no portfolio, no exams at all."])}''')

# ---------- P5: แชตแม่ ----------
def bubble(y, text, w):
    return f'<rect x="96" y="{y}" width="{w}" height="40" rx="18" fill="#2a2f40"/><text x="114" y="{y+26}" font-family="IBM Plex Sans Thai, sans-serif" font-size="15" fill="#e6e7ee">{text}</text>'
p5 = frame(f'''<rect width="540" height="960" fill="#121620"/>
  <rect x="0" y="0" width="540" height="96" fill="#1a1f2c"/>
  <circle cx="74" cy="56" r="22" fill="#e88aa8"/><circle cx="74" cy="56" r="10" fill="#f6c0d0"/>
  <text x="108" y="52" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" font-weight="600" fill="#e6e7ee">แม่</text>
  <text x="108" y="74" font-family="IBM Plex Sans Thai, sans-serif" font-size="12" fill="#80849a">ออนไลน์</text>
  <rect x="200" y="118" width="140" height="24" rx="12" fill="#232838"/><text x="270" y="135" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="12" fill="#a0a4b8">วันพฤหัสบดี</text>
  <circle cx="66" cy="182" r="16" fill="#e88aa8"/>
  {bubble(162, "ลูก แม่ได้ข่าวว่าติดโรงเรียนเวทมนตร์", 330)}
  {bubble(212, "จบมาเป็นข้าราชการได้ไหมลูก", 250)}
  <g transform="translate(96,268)">
    <rect width="190" height="170" rx="16" fill="#fff4f6"/>
    <g fill="#e05a7a"><circle cx="70" cy="70" r="26"/><circle cx="120" cy="64" r="22"/><circle cx="96" cy="100" r="24"/></g>
    <g fill="#f08aa4"><circle cx="66" cy="64" r="12"/><circle cx="118" cy="58" r="10"/><circle cx="94" cy="94" r="11"/></g>
    <path d="M 60,110 L 50,150 M 96,124 L 96,156 M 128,86 L 140,140" stroke="#5a9a5a" stroke-width="4"/>
    <text x="95" y="38" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="18" font-weight="700" fill="#c0306a">สวัสดีวันจันทร์</text>
  </g>
  <path d="M 300,330 L 360,250" stroke="#f6f1e6" stroke-width="2" stroke-dasharray="5 4"/>
  <g transform="translate(330,200)"><rect width="180" height="52" rx="10" fill="#f6f1e6"/><text x="14" y="32" font-family="IBM Plex Sans Thai, sans-serif" font-size="14" font-weight="600" fill="#2a2430">วันนี้วันพฤหัสนะแม่</text></g>
  <rect x="0" y="880" width="540" height="80" fill="#1a1f2c"/><rect x="24" y="900" width="430" height="40" rx="20" fill="#232838"/>
  {EYE}
  {subs(["แม่ทักไลน์มาคำเดียว", "จบมาเป็นข้าราชการได้ไหมลูก"], ["Mom texted one question:", "“Can you become a civil servant after?”"])}''')

PANELS = [
  ("1", "4 วิ", p1, "Medium Shot · ห้องนอนกลางคืน", "เจมยืนข้างเตียง ยกมือถือจ้อง แสงจอฟ้าส่องหน้า · กล้องซูมเข้าช้า ๆ", "ดนตรีเบา ๆ ขี้เล่น · เสียงบรรยายเจม"),
  ("2", "3 วิ", p2, "Close-up จอมือถือ (มุมมองเจม)", "รายการขึ้นทีละบรรทัด บรรทัดสุดท้ายขอบแดงเด้งขึ้นช้ากว่านิด เป็นจังหวะมุก", "เสียงแจ้งเตือน 'ติ๊ง' ทีละบรรทัด · บรรทัดสุดท้ายเสียง 'ตึ่ง' แบบเกมโชว์ตอบผิด"),
  ("3", "4 วิ", p3, "Medium Wide · ห้องนอนตอนตีห้า", "ไอ้เหลืองโผล่ขอบหน้าต่างแล้วขันใส่ · กล้องสั่นสั้น ๆ ตอนขัน · เจมตกเตียงหงายหลัง ขาชี้ฟ้า", "เสียงไก่ขันดังลั่น + เสียงตุ้บตกเตียง · ดนตรีหยุดหนึ่งจังหวะก่อนขัน"),
  ("4", "3.5 วิ", p4, "Close-up · เจมนั่งพื้นอ่านจดหมาย", "เจมยกคิ้วข้างเดียว ยิ้มมุมปาก · กล่องคำอธิบายชี้บรรทัดที่ไฮไลต์ · ไอ้เหลืองเบลออยู่ด้านหลัง", "ดนตรีกลับมาแบบตื่นเต้นขึ้นนิด · ปากเจมขยับ (เจมพูดเอง)"),
  ("5", "3 วิ", p5, "Close-up จอแชต", "ข้อความแม่เด้งทีละอัน ตามด้วยสติกเกอร์สวัสดีวันจันทร์ · กล่องคำอธิบายแซวว่าวันนี้วันพฤหัส", "เสียงแจ้งเตือนแชตสามครั้งติดกัน · เสียงบรรยายเจม"),
]

cards = "".join(f'''<figure class="panel">
  <div class="frame">{svg}</div>
  <figcaption><div class="row"><span class="num">ช็อต {n}</span><span class="dur">{d}</span><span class="cam">{cam}</span></div>
  <p><b>ภาพ</b> {act}</p><p><b>เสียง</b> {snd}</p></figcaption>
</figure>''' for n, d, svg, cam, act, snd in PANELS)

page = f'''<title>สตอรี่บอร์ดฉากส่งจดหมาย</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@400;500&display=swap">
<style>
/* Layout: แถวเฟรม 9:16 ตามลำดับช็อต พร้อมโน้ตภาพและเสียงใต้แต่ละเฟรม · โทนมืดของช่อง */
:root {{ --bg:#0d0f14; --panel:#1b1f2b; --ink:#e6e7ee; --muted:#80849a; --line:#2a2e3a; --accent:#c9a8ff;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1200px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:20px; margin:0; font-weight:600; text-wrap:balance; }}
h1 span {{ display:block; font-size:14px; font-weight:400; color:var(--muted); margin-top:4px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(210px,1fr)); gap:16px; }}
.panel {{ margin:0; display:grid; gap:8px; align-content:start; min-width:0; }}
.frame svg {{ display:block; width:100%; height:auto; border-radius:8px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:13px; line-height:1.55; display:grid; gap:4px; }}
figcaption p {{ margin:0; color:var(--muted); }}
figcaption b {{ color:var(--ink); font-weight:500; margin-right:4px; }}
.row {{ display:flex; flex-wrap:wrap; gap:6px 8px; align-items:center; }}
.num {{ background:#2a2440; color:var(--accent); border:1px solid #4a3f72; border-radius:99px; padding:0 9px; font-weight:600; }}
.dur {{ color:var(--muted); font-variant-numeric:tabular-nums; }}
.cam {{ color:var(--ink); font-weight:500; }}
.note {{ font-size:13px; color:var(--muted); max-width:72ch; line-height:1.6; margin:0; }}
</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{DEFS}{DEFS_SB}</defs></svg>
<div class="wrap">
  <h1>สตอรี่บอร์ดฉากส่งจดหมาย · ร่าง v1<span>ฮอกวอตส์ สาขาประเทศไทย · ช็อต 1–5 · ยาว 17.5 วิ · เฟรม 9:16 ซับอยู่ช่วง 74% ของความสูง</span></h1>
  <div class="grid">{cards}</div>
  <p class="note">ภาพร่างนี้ใช้ดูองค์ประกอบ มุมกล้อง และจังหวะมุก ยังไม่ได้ลงรายละเอียดฉากเต็ม ท่าทางตัวละคร (ยกมือถือ ตกเตียง นั่งพื้น) จะวาดท่าจริงในขั้นทำภาพนิ่ง</p>
</div>'''
(HERE / "storyboard.html").write_text(page)
print("ok")
