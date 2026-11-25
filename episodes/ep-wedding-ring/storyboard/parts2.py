# Odd Hours · ตอนงานแต่ง · ชิ้นส่วนสตอรีบอร์ดรอบ 2
# สีหน้าใหม่ (นางเอกกังวล/ตกใจกลัว, เจ้าบ่าวยิ้มร้าย) · ลิฟต์หรู · ห้องพักหรู · ประตูห้องพัก · ช็อตมือถือแบบตอนแรก (มือถือเข้ามาจากล่าง ฉากหลังเบลอ)
import re, math, random
import bride_v2 as B2
import wedding_chars as WC

def fx(v): return f'{v:.1f}'

# ---------------------------------------------------------------- สีหน้า
_b2head = re.search(r'<g id="b2head">.*?\n</g>', B2.HEAD, re.S).group(0)

def _swap(head, start, end, new):
    i = head.index(start); j = head.index(end)
    return head[:i] + new + head[j:]

def bride_expr(name, brows, mouth, iris_r=4.7, extra=''):
    h = _b2head.replace('<g id="b2head">', f'<g id="b2head_{name}">')
    h = _swap(h, '  <!-- soft straight brows -->', '  <path d="M -21.4,-3', '  <!-- brows -->\n' + brows + '\n')
    h = _swap(h, '  <!-- lips:', '  <!-- crown:', mouth + '\n')
    h = h.replace('r="4.7" fill="#5a3426"', f'r="{iris_r}" fill="#5a3426"').replace('A4.7,4.7', f'A{iris_r},{iris_r}')
    h = h.replace('M -17.7,-1.2', f'M {-13 - iris_r:.1f},-1.2').replace('M 8.3,-1.2', f'M {13 - iris_r:.1f},-1.2')
    h = h.replace('r="2.1" fill="#120808"', f'r="{max(1.4, iris_r * .45):.1f}" fill="#120808"')
    return h.replace('\n</g>', extra + '\n</g>')

H = B2.H
BROW_WORRY = (f'<path d="M -22.6,-11.8 C -17,-13.6 -10.6,-15.6 -5.4,-15 L -5.8,-13 C -10.6,-13.4 -16.6,-11.6 -22,-9.8 Z" fill="{H}"/>'
              f'<path d="M 22.6,-11.8 C 17,-13.6 10.6,-15.6 5.4,-15 L 5.8,-13 C 10.6,-13.4 16.6,-11.6 22,-9.8 Z" fill="{H}"/>')
BROW_SCARED = (f'<path d="M -22.6,-11 C -17,-14 -10.6,-18 -5.4,-17.6 L -5.8,-15.6 C -10.6,-15.8 -16.6,-12.6 -22,-9 Z" fill="{H}"/>'
               f'<path d="M 22.6,-11 C 17,-14 10.6,-18 5.4,-17.6 L 5.8,-15.6 C 10.6,-15.8 16.6,-12.6 22,-9 Z" fill="{H}"/>')
MOUTH_WORRY = ('<path d="M -5,23.4 Q 0,22.4 5,23.4 Q 0,25.6 -5,23.4 Z" fill="#cf6f7a"/>'
               '<path d="M -5,23.4 Q 0,22.6 5,23.4" fill="none" stroke="#9a4052" stroke-width=".9"/>')
MOUTH_SCARED = ('<ellipse cx="0" cy="24.4" rx="4" ry="3.8" fill="#6e2632"/><path d="M -3,22.2 Q 0,21.6 3,22.2 L 2.6,23.2 Q 0,22.8 -2.6,23.2 Z" fill="#fff"/>'
                '<path d="M -4.4,22.6 Q 0,20.4 4.4,22.6" fill="none" stroke="#c25c6a" stroke-width="1.6" stroke-linecap="round"/>'
                '<path d="M -3.8,26.4 Q 0,29 3.8,26.4" fill="none" stroke="#d97884" stroke-width="1.8" stroke-linecap="round"/>')
PALE = ('<ellipse cx="0" cy="0" rx="30" ry="40" fill="#c8d4f0" opacity=".14"/>'
        '<path d="M 27,-18 q 2.4,4 0,6.4 q -2.4,-2.4 0,-6.4 Z" fill="#dfeaff" opacity=".9"/>')

GROOM_SIN = re.search(r'<g id="ghead">.*?\n  </g>', WC.GROOM_HEAD, re.S).group(0).replace('<g id="ghead">', '<g id="ghead_sin">')
GROOM_SIN = _swap(GROOM_SIN, '    <!-- thin closed-mouth smirk', '    <!-- neat comma hair',
                  '    <path d="M -8,22 Q 0,28 9.4,20 Q 0,24.6 -8,22 Z" fill="#f4f0ea"/><path d="M -8,22 Q 0,28 9.4,20" fill="none" stroke="#8a4a46" stroke-width="1.6" stroke-linecap="round"/>'
                  '<path d="M 9.4,20 L 11,18.6" stroke="#8a4a46" stroke-width="1.4" stroke-linecap="round"/>\n')

HEAD_DEFS = (bride_expr('worry', BROW_WORRY, MOUTH_WORRY, 4.5) + bride_expr('scared', BROW_SCARED, MOUTH_SCARED, 3.2, PALE) + GROOM_SIN)

def bride_with(head):
    return '<use href="#b2back"/>' + WC.bride_body() + f'<use href="#{head}"/>'

# มือกำไว้ที่อก (ใช้กับภาพใกล้ช่วงบน)
CLUTCH = ('<path d="M -14,92 C -20,84 -10,76 -2,82 L 4,90 C 6,98 -6,102 -14,92 Z" fill="#fbe2cf"/>'
          '<path d="M 14,94 C 22,86 12,78 4,84 L -2,92 C -4,100 8,104 14,94 Z" fill="#efc3a8"/>'
          '<path d="M -8,86 L -4,90 M -4,83 L 0,87" stroke="#d9a089" stroke-width="1"/>'
          '<rect x="4" y="86" width="6" height="2.4" rx="1.2" fill="#f4f6f9" transform="rotate(30 7 87)"/>')

# ---------------------------------------------------------------- วิวคืนพระจันทร์เต็มดวง (ใช้ซ้ำในหน้าต่าง)
def moon_view(x0, y0, w, h, seed=3, moon=True):
    r = random.Random(seed); o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="url(#nightSky)"/>']
    if moon:
        mx, my = x0 + w * .66, y0 + h * .26
        o.append(f'<circle cx="{fx(mx)}" cy="{fx(my)}" r="{fx(w * .28)}" fill="#9fb0e0" opacity=".10"/><circle cx="{fx(mx)}" cy="{fx(my)}" r="{fx(w * .12)}" fill="#eef2fb"/><circle cx="{fx(mx - w * .03)}" cy="{fx(my - w * .02)}" r="{fx(w * .022)}" fill="#d6dcec"/>')
    for _ in range(10):
        o.append(f'<circle cx="{fx(r.uniform(x0, x0 + w))}" cy="{fx(r.uniform(y0, y0 + h * .5))}" r="{r.uniform(.5, 1.1):.1f}" fill="#dfe6ff" opacity=".7"/>')
    for layer, col in enumerate(('#1a2350', '#141b40', '#0e1430')):
        x = x0 - 6
        while x < x0 + w:
            bw = r.uniform(12, 28); bh = r.uniform(.25, .7) * h * (1 - layer * .15)
            o.append(f'<rect x="{fx(x)}" y="{fx(y0 + h - bh)}" width="{fx(bw)}" height="{fx(bh)}" fill="{col}"/>')
            if layer == 2:
                for yy in range(int(y0 + h - bh + 5), int(y0 + h - 3), 7):
                    for xx in range(int(x + 3), int(x + bw - 3), 6):
                        if r.random() < .25: o.append(f'<rect x="{xx}" y="{yy}" width="2.2" height="3" fill="{r.choice(("#ffe6c4", "#cfe0ff"))}" opacity=".85"/>')
            x += bw + r.uniform(1, 5)
    return ''.join(o)

def sconce(x, y, s=1):
    return (f'<circle cx="{x}" cy="{y - 6 * s}" r="{40 * s}" fill="url(#chGlow4)"/><rect x="{x - 3 * s}" y="{y - 6 * s}" width="{6 * s}" height="{24 * s}" fill="#c3c8cf"/>'
            + ''.join(f'<path d="M {x},{y + 8 * s} q {d * 14 * s},{4 * s} {d * 15 * s},{-12 * s}" stroke="#c3c8cf" stroke-width="{2.4 * s}" fill="none"/><rect x="{x + d * 15 * s - 5 * s}" y="{y - 18 * s}" width="{10 * s}" height="{14 * s}" rx="{2 * s}" fill="#fff8ee"/>' for d in (-1, 1)))

def wall_panels(x0, x1, y0, y1, n, col='#ece5d8', trim='#c3c8cf'):
    w = (x1 - x0) / n; o = []
    for i in range(n):
        a = x0 + i * w + 8; b = a + w - 16
        o.append(f'<rect x="{fx(a)}" y="{y0}" width="{fx(b - a)}" height="{y1 - y0}" fill="{col}" stroke="{trim}" stroke-width="1.6"/><rect x="{fx(a + 6)}" y="{y0 + 6}" width="{fx(b - a - 12)}" height="{y1 - y0 - 12}" fill="none" stroke="#dcd2c2" stroke-width="1"/>')
    return ''.join(o)

# ---------------------------------------------------------------- ลิฟต์หรู
def elevator_lux(figure):
    o = ['<rect width="540" height="960" fill="#1e1a2a"/>']
    # เพดานลายช่อง + โคมคริสตัล
    o.append('<path d="M 0,0 H 540 L 430,160 L 110,160 Z" fill="#e6e0d4"/>')
    o.append('<path d="M 60,0 L 140,120 L 400,120 L 480,0 Z" fill="#f2ece2" stroke="#c3c8cf" stroke-width="2"/><path d="M 140,120 L 400,120" stroke="#c3c8cf" stroke-width="3"/>')
    o.append('<circle cx="270" cy="70" r="70" fill="url(#chGlow4)"/>')
    for i, x in enumerate(range(222, 320, 12)):
        L = 30 + (12 - abs(x - 270) / 4)
        o.append(f'<path d="M {x},40 V {40 + L}" stroke="#f4f6fa" stroke-width="1" stroke-dasharray="2 1.4"/><path d="M {x},{40 + L} l 2.6,4 l -2.6,5 l -2.6,-5 Z" fill="#f8faff"/>')
    o.append('<ellipse cx="270" cy="40" rx="54" ry="10" fill="none" stroke="#c3c8cf" stroke-width="3"/>')
    # ผนังข้างกระจกกรอบเงิน
    o.append('<path d="M 0,0 L 110,160 L 110,780 L 0,960 Z" fill="#d6cfc2"/><path d="M 540,0 L 430,160 L 430,780 L 540,960 Z" fill="#c8c0b2"/>')
    o.append('<path d="M 14,100 L 96,210 L 96,520 L 14,560 Z" fill="#8a8aa6"/><path d="M 14,100 L 96,210 L 96,520 L 14,560 Z" fill="url(#mirror)" opacity=".55"/><path d="M 14,100 L 96,210 L 96,520 L 14,560 Z" fill="none" stroke="#c3c8cf" stroke-width="4"/>')
    o.append('<path d="M 526,100 L 444,210 L 444,520 L 526,560 Z" fill="#7e7e9a"/><path d="M 526,100 L 444,210 L 444,520 L 526,560 Z" fill="url(#mirror)" opacity=".45"/><path d="M 526,100 L 444,210 L 444,520 L 526,560 Z" fill="none" stroke="#c3c8cf" stroke-width="4"/>')
    o.append('<path d="M 30,600 L 96,570 M 510,600 L 444,570" stroke="#eef0f4" stroke-width="7" stroke-linecap="round"/><path d="M 30,606 L 96,576 M 510,606 L 444,576" stroke="#9aa0aa" stroke-width="2"/>')
    o.append('<path d="M 14,620 L 96,590 L 96,760 L 14,840 Z M 526,620 L 444,590 L 444,760 L 526,840 Z" fill="#cbc2b2" stroke="#c3c8cf" stroke-width="2"/>')
    # ผนังประตูด้านหน้า
    o.append('<rect x="110" y="160" width="320" height="620" fill="#ece5d8"/>')
    o.append(wall_panels(110, 430, 640, 776, 2))
    # หน้าปัดบอกชั้นแบบเข็มครึ่งวงกลม
    cx, cy = 270, 236
    o.append(f'<path d="M {cx - 70},{cy} A 70,70 0 0,1 {cx + 70},{cy} Z" fill="#c3c8cf"/><path d="M {cx - 62},{cy} A 62,62 0 0,1 {cx + 62},{cy} Z" fill="#1c1a26"/>')
    for k in range(12):
        a = math.pi - math.pi * k / 11
        o.append(f'<text x="{fx(cx + math.cos(a) * 50)}" y="{fx(cy - math.sin(a) * 50 + 4)}" text-anchor="middle" font-size="9" fill="{"#cbb2ff" if k == 11 else "#c3c8cf"}" font-family="IBM Plex Mono, monospace">{k + 1}</text>')
    o.append(f'<path d="M {cx},{cy} L {cx + 40},{cy - 18}" stroke="#cbb2ff" stroke-width="3" stroke-linecap="round"/><circle cx="{cx}" cy="{cy}" r="6" fill="#c3c8cf"/>')
    # ประตูเปิด เห็นทางเดินเดิม
    o.append('<rect x="170" y="290" width="200" height="490" fill="#c3c8cf"/>')
    o.append('<rect x="180" y="300" width="180" height="480" fill="#2a2440"/>')
    o.append('<path d="M 180,780 L 236,560 L 304,560 L 360,780 Z" fill="#3c3050"/><rect x="236" y="400" width="68" height="160" fill="#4a4060"/>')
    o.append(f'<rect x="246" y="410" width="48" height="60" fill="#c3c8cf"/>{moon_view(250, 414, 40, 52, 7)}')
    o.append('<rect x="250" y="520" width="40" height="30" fill="#5a4e70"/><circle cx="270" cy="508" r="12" fill="#e8e0ec" opacity=".8"/>')
    o.append('<circle cx="206" cy="440" r="10" fill="#fff0d8" opacity=".6"/><circle cx="334" cy="440" r="10" fill="#fff0d8" opacity=".6"/>')
    o.append('<path d="M 180,300 L 196,300 L 196,780 L 180,780 Z M 344,300 L 360,300 L 360,780 L 344,780 Z" fill="#d8d2c6"/>')
    o.append('<text x="270" y="378" text-anchor="middle" font-size="12" fill="#c3c8cf" font-family="IBM Plex Sans Thai" letter-spacing="2">ชั้น 12</text>')
    # พื้นหินอ่อนลายฝัง
    o.append('<path d="M 110,780 L 430,780 L 540,960 L 0,960 Z" fill="#ece7e2"/><path d="M 270,800 L 380,870 L 270,940 L 160,870 Z" fill="#d6ccd4"/><path d="M 270,820 L 348,870 L 270,920 L 192,870 Z" fill="#c3c8cf"/>')
    if figure: o.append(figure)
    o.append('<rect width="540" height="960" fill="#2a2a50" opacity=".12" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

# ---------------------------------------------------------------- ห้องพักหรู (กลางคืน)
def suite_room(figure=''):
    o = ['<rect width="540" height="960" fill="#d8d0c2"/>', '<rect width="540" height="960" fill="url(#damask)" opacity=".35"/>',
         '<path d="M 0,0 H 540 V 60 Q 270,20 0,60 Z" fill="#c4baa8"/><path d="M 0,60 Q 270,20 540,60" stroke="#c3c8cf" stroke-width="4" fill="none"/>']
    # หน้าต่างใหญ่วิวพระจันทร์
    o.append('<rect x="250" y="120" width="260" height="440" fill="#c3c8cf"/>' + moon_view(260, 130, 240, 420, 11))
    o.append('<path d="M 380,130 V 550 M 260,330 H 500" stroke="#c3c8cf" stroke-width="4"/>')
    o.append('<path d="M 240,100 C 250,300 236,480 250,600 L 300,600 C 290,460 300,300 290,100 Z" fill="#efe8dc"/><path d="M 520,100 C 510,300 526,480 512,600 L 470,600 C 480,460 470,300 480,100 Z" fill="#e2dacc"/>')
    o.append('<path d="M 230,96 H 530 V 116 Q 380,150 230,116 Z" fill="#f2ece2"/><rect x="230" y="92" width="300" height="6" fill="#c3c8cf"/>')
    # แสงจันทร์ลงพื้น
    o.append('<path d="M 260,560 L 500,560 L 460,960 L 120,960 Z" fill="#cfdcff" opacity=".2"/>')
    # หัวเตียงบุนวมสูง + เตียง
    o.append('<rect x="0" y="300" width="230" height="300" rx="10" fill="#efe9de" stroke="#c3c8cf" stroke-width="4"/>')
    o.append(''.join(f'<circle cx="{x}" cy="{y}" r="2" fill="#cfc4b2"/>' for x in range(20, 220, 24) for y in range(326, 590, 26)))
    o.append('<path d="M -20,560 L 240,560 L 300,800 L -20,800 Z" fill="#faf8f4"/><path d="M -20,620 L 270,620 L 300,800 L -20,800 Z" fill="#f0ece6"/>')
    o.append('<rect x="10" y="520" width="90" height="46" rx="14" fill="#ffffff"/><rect x="110" y="520" width="90" height="46" rx="14" fill="#f8f6f2"/>')
    o.append('<path d="M -20,680 L 285,680 L 292,720 L -20,720 Z" fill="#c9cfdc"/>')
    o.append(''.join(f'<ellipse cx="{x}" cy="{y}" rx="4" ry="2" fill="#ffffff" transform="rotate({a} {x} {y})"/>' for x, y, a in ((80, 640, 20), (120, 650, -30), (150, 636, 40), (100, 660, 10), (170, 652, -20), (60, 655, 50))))
    # โต๊ะข้างเตียง + โคม
    o.append('<rect x="210" y="580" width="60" height="70" fill="#ece5d8" stroke="#c3c8cf" stroke-width="2"/><circle cx="240" cy="520" r="60" fill="url(#lampGlow)"/><path d="M 222,560 L 258,560 L 250,530 L 230,530 Z" fill="#fff6ea"/><rect x="237" y="560" width="6" height="20" fill="#c3c8cf"/>')
    # พรมและพื้น
    o.append('<rect x="0" y="800" width="540" height="160" fill="#b8b0a6"/><rect x="40" y="820" width="460" height="140" fill="#cfc8c2"/><rect x="52" y="830" width="436" height="130" fill="none" stroke="#c3c8cf" stroke-width="2"/>')
    o.append('<circle cx="390" cy="20" r="80" fill="url(#chGlow4)" opacity=".7"/>')
    o.append(figure)
    o.append('<rect width="540" height="960" fill="#1e2448" opacity=".28" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

def suite_door_lux(feet=True):
    o = ['<rect width="540" height="960" fill="#d6cebf"/>', '<rect width="540" height="960" fill="url(#damask)" opacity=".35"/>',
         '<path d="M 0,0 H 540 V 60 Q 270,20 0,60 Z" fill="#c4baa8"/><path d="M 0,60 Q 270,20 540,60" stroke="#c3c8cf" stroke-width="4" fill="none"/>',
         wall_panels(0, 540, 620, 780, 4, '#e6dfd2')]
    o.append('<rect x="140" y="150" width="260" height="640" fill="#c3c8cf"/><rect x="150" y="160" width="240" height="630" fill="#efe9de"/>')
    o.append('<rect x="172" y="190" width="196" height="250" fill="none" stroke="#c3c8cf" stroke-width="3"/><rect x="180" y="198" width="180" height="234" fill="none" stroke="#dcd2c2" stroke-width="1.4"/>')
    o.append('<rect x="172" y="470" width="196" height="290" fill="none" stroke="#c3c8cf" stroke-width="3"/><rect x="180" y="478" width="180" height="274" fill="none" stroke="#dcd2c2" stroke-width="1.4"/>')
    o.append('<circle cx="270" cy="300" r="7" fill="#c3c8cf"/><circle cx="270" cy="300" r="3.4" fill="#14141a"/>')
    o.append('<rect x="340" y="470" width="34" height="8" rx="4" fill="#c3c8cf"/><rect x="340" y="470" width="34" height="2.6" rx="1.3" fill="#f4f6f9"/><rect x="352" y="488" width="12" height="22" rx="2" fill="#2a2834"/>')
    o.append('<path d="M 372,420 q -40,26 -70,6" stroke="#c3c8cf" stroke-width="2.6" fill="none" stroke-dasharray="5 2.4"/>')
    o.append('<rect x="150" y="786" width="240" height="6" fill="#dfe8ff"/><path d="M 150,792 L 390,792 L 480,960 L 60,960 Z" fill="#cfdcff" opacity=".25"/>')
    if feet:
        o.append('<rect x="214" y="784" width="34" height="9" fill="#0c0c14"/><rect x="292" y="784" width="34" height="9" fill="#0c0c14"/>')
        o.append('<path d="M 214,792 L 248,792 L 230,900 L 196,900 Z M 292,792 L 326,792 L 344,900 L 310,900 Z" fill="#0c0c14" opacity=".35"/>')
    o.append(sconce(80, 320, 1.1) + sconce(460, 320, 1.1))
    o.append('<rect x="0" y="790" width="540" height="170" fill="#b8b0a6" opacity=".9"/>')
    o.append('<rect width="540" height="960" fill="#1e2448" opacity=".3" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

# ---------------------------------------------------------------- ห้องเจ้าสาว (ฉากหลังเบลอของช็อตมือถือ)
def bridal_room_bg():
    o = ['<rect width="540" height="960" fill="#e6ddd0"/>', '<rect x="60" y="120" width="200" height="300" rx="8" fill="#f4efe6" stroke="#c3c8cf" stroke-width="6"/>',
         '<rect x="76" y="136" width="168" height="268" fill="url(#mirror)"/>']
    for k in range(8):
        o.append(f'<circle cx="{60 + k * 28}" cy="112" r="10" fill="#fff6e0"/><circle cx="{60 + k * 28}" cy="112" r="26" fill="url(#chGlow4)"/>')
    o.append('<rect x="320" y="90" width="200" height="380" fill="#c3c8cf"/>' + moon_view(330, 100, 180, 360, 21))
    o.append('<path d="M 300,80 C 310,260 296,420 312,520 L 350,520 C 340,400 350,250 340,80 Z" fill="#efe8dc"/>')
    o.append('<path d="M 380,460 C 360,560 330,700 320,960 L 540,960 L 540,520 C 500,480 430,460 380,460 Z" fill="#fbf8f2"/>')
    o.append('<rect x="40" y="440" width="260" height="30" fill="#f2ece2"/><rect x="40" y="470" width="260" height="200" fill="#e8e0d2"/>')
    return f'<g filter="url(#blurBG)">{"".join(o)}</g><rect width="540" height="960" fill="#2a2440" opacity=".25"/>'

# ---------------------------------------------------------------- มือถือในมือ แบบคลิปตอนแรก
def phone_hand(screen, bg):
    o = [bg]
    o.append('<g transform="rotate(-4 270 420)">')
    o.append('<rect x="132" y="120" width="276" height="560" rx="38" fill="#1a1a22"/><rect x="138" y="126" width="264" height="548" rx="34" fill="#2c2c38"/>')
    o.append('<rect x="146" y="134" width="248" height="532" rx="28" fill="#0c0c12"/>')
    # จอเดิมพิกัด 156..384 x 156..644 → ขยายให้เต็มกรอบใหม่
    o.append(f'<clipPath id="phc{abs(hash(screen)) % 99999}"><rect x="152" y="140" width="236" height="520" rx="24"/></clipPath>'
             f'<g clip-path="url(#phc{abs(hash(screen)) % 99999})"><g transform="translate(152,140) scale({236 / 228:.4f},{520 / 488:.4f}) translate(-156,-156)">{screen}</g></g>')
    o.append('<rect x="240" y="148" width="60" height="14" rx="7" fill="#0c0c12"/>')
    o.append('<path d="M 160,150 L 210,150 L 152,330 Z" fill="#ffffff" opacity=".05"/>')
    o.append('</g>')
    # มือซ้ายจับ: นิ้วสี่นิ้วรอบขอบซ้าย ฝ่ามือกับนิ้วโป้งจากด้านล่าง
    sk, sks, skd = '#fbe2cf', '#efc3a8', '#d9a089'
    for k, y in enumerate((420, 470, 520, 570)):
        o.append(f'<rect x="{104 + k * 2}" y="{y}" width="44" height="40" rx="18" fill="{sk if k % 2 == 0 else sks}"/><path d="M {108 + k * 2},{y + 30} h 30" stroke="{skd}" stroke-width="1.4" opacity=".6"/>')
    o.append(f'<path d="M 150,600 C 200,640 330,620 400,600 C 430,680 440,780 420,960 L 210,960 C 220,860 160,760 150,600 Z" fill="{sk}"/>')
    o.append(f'<path d="M 360,610 C 400,604 420,640 430,700 C 440,780 434,880 420,960 L 380,960 C 396,860 396,740 360,610 Z" fill="{sks}"/>')
    o.append(f'<path d="M 300,630 C 320,580 340,540 352,510 C 362,496 382,500 380,520 C 372,560 360,610 340,660 Z" fill="{sk}"/><ellipse cx="366" cy="512" rx="12" ry="9" fill="#ffffff" opacity=".5"/>')
    o.append(f'<path d="M 120,980 C 160,900 200,860 220,840 L 300,960 Z" fill="{sks}"/>')
    o.append('<rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

DEFS2 = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="nightSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b1e"/><stop offset=".55" stop-color="#121c44"/><stop offset="1" stop-color="#26346c"/></linearGradient>
<filter id="blurBG" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="9"/></filter>
<pattern id="damask" width="34" height="44" patternUnits="userSpaceOnUse"><g fill="#ffffff" opacity=".35"><path d="M17,6 C21,12 25,14 25,20 C25,26 20,28 17,34 C14,28 9,26 9,20 C9,14 13,12 17,6Z"/></g></pattern>
<linearGradient id="mirror" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f4f2ef"/><stop offset=".5" stop-color="#cfd2d8"/><stop offset="1" stop-color="#eeebe6"/></linearGradient>
<radialGradient id="lampGlow"><stop offset="0" stop-color="#fff1e2" stop-opacity=".75"/><stop offset=".5" stop-color="#ffe6dc" stop-opacity=".25"/><stop offset="1" stop-color="#ffe6dc" stop-opacity="0"/></radialGradient>
{HEAD_DEFS}
</defs></svg>'''
