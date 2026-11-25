# Odd Hours · ตอนงานแต่ง · สตอรีบอร์ด 30 ช็อต (ห้องพิธีวิวพระจันทร์เต็มดวง)
# ฉากห้องพิธีและตัวละครใช้ของจริงที่ทำไว้ ส่วนประตู มือถือ ลิฟต์ และห้องพักเป็นแบบร่างโทนเดียวกัน
# รัน: python3 storyboard.py -> storyboard.html
import os, sys, re, math, random
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'sets'))
sys.path.insert(0, os.path.join(HERE, '..', 'characters'))
os.chdir(os.path.join(HERE, '..', 'sets'))
import sets9 as N9
import sets8 as H8
import supporting as SP
import wedding_chars as WC
import bride_v2 as B2

def fx(v): return f'{v:.1f}'

# ---------------------------------------------------------------- ห้องพิธี (วิวพระจันทร์เต็มดวง) เป็นชิ้นใช้ซ้ำ
name, note, fn, sky, refl, shaft = N9.VARIANTS[0]
_hall = N9.variant_svg(0, name, fn, sky, refl, shaft)
HALL_INNER = _hall[_hall.index('>') + 1:_hall.index('<g class="guide">')]

# ---------------------------------------------------------------- ตัวละครเป็นชิ้นใช้ซ้ำ
def sup_parts(f):
    n, nt, kind, back, head, body = f()
    return back, head, body, (460 if kind == 'f' else 488)
CH = {}
for key, f in (('wb', SP.c_woman_black), ('mom', SP.c_mother), ('ph', SP.c_photographer), ('staff', SP.c_staff), ('guard', SP.c_guard),
               ('nb', SP.c_new_bride), ('bm', SP.c_bridesmaid), ('gw', SP.c_guest_w), ('gm', SP.c_guest_m)):
    b, h, bd, lf = sup_parts(f)
    CH[key] = (b + bd + h, lf)
CH['bride'] = ('<use href="#b2back"/>' + WC.bride_body() + '<use href="#b2head"/>', 462)
CH['groom'] = (WC.groom_body() + '<use href="#ghead"/><path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="#d8d4ce" stroke-width="2"/>', 488)
# เจ้าบ่าวกับแขกฝั่งเจ้าบ่าว: แขนปรบมือไม่มี ใช้ท่ายืนตรงเหมือนแผ่นตัวละคร
# เจ้าสาวในชุดดำ (ฉากจบ): หัวเจ้าสาว + ชุดผู้หญิงชุดดำ ไม่มีผ้าคลุม
_wb_back, _wb_head, _wb_body, _ = sup_parts(SP.c_woman_black)
_b2back = re.search(r'<g id="b2back">(.*?)</g>', B2.HEAD, re.S).group(1)
_b2back_nv = '\n'.join(l for l in _b2back.split('\n') if '#ffffff' not in l)
CH['bride_black'] = (f'<g>{_b2back_nv}</g>' + _wb_body + '<use href="#b2head"/>', 460)
# รูปงานแต่งปีที่แล้วในมือถือ: หัวผู้หญิงชุดดำ + ชุดเจ้าสาว
CH['wb_white'] = (_wb_back + WC.bride_body() + _wb_head, 462)

CHAR_DEFS = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + \
    ''.join(f'<g id="ch_{k}">{v[0]}</g>' for k, v in CH.items()) + f'<g id="hallbg">{HALL_INNER}</g></defs></svg>'

def put(key, x, feet, s, shadow=True):
    lf = CH[key][1]
    sh = f'<ellipse cx="{fx(x + 10 * s)}" cy="{fx(feet + 2)}" rx="{fx(60 * s)}" ry="{fx(8 * s)}" fill="#20202c" opacity=".3" filter="url(#sf4)"/>' if shadow else ''
    return sh + f'<g transform="translate({fx(x)},{fx(feet - lf * s)}) scale({s:.3f})"><use href="#ch_{key}"/></g>'

def face_xy(key, x, feet, s):
    lf = CH[key][1]
    return x, feet - (lf + 4) * s

# ตำแหน่งตัวละครในห้องพิธี (เหมือน sets8)
CAST = {'staff': (150, 688, .40), 'guard': (474, 700, .42), 'gw': (392, 702, .42), 'gm': (432, 706, .42),
        'bm': (160, 748, .48), 'mom': (380, 762, .50), 'bride': (228, 845, .58), 'groom': (316, 848, .58), 'ph': (96, 912, .66)}

def hall(cast=CAST, extra_back='', cool=0.0):
    items = sorted(((v[1], put(k, *v)) for k, v in cast.items()), key=lambda t: t[0])
    o = '<use href="#hallbg"/>' + extra_back + ''.join(p for _, p in items)
    if cool: o += f'<rect width="540" height="960" fill="#28305a" opacity="{cool}" style="mix-blend-mode:multiply"/>'
    return o

def cam(content, cx, cy, z, ty=400):
    """ซูมเข้าหาจุด (cx, cy) ให้ไปอยู่ราวกลางเฟรม"""
    tx = 270 - cx * z; tyy = ty - cy * z
    return f'<g transform="translate({fx(tx)},{fx(tyy)}) scale({z})">{content}</g>'

# ---------------------------------------------------------------- ฉากประตูห้องจัดเลี้ยง (มองจากในห้อง ประตูบานคู่สูงสองชั้น)
SV = H8.S
DOOR_FEET = 760        # เท้าคนที่ยืนตรงกรอบประตู
DOOR_S = .52           # ขนาดคนที่ระยะประตู
def doors(state='closed', figures=()):
    o = []
    o.append('<rect width="540" height="960" fill="url(#wall7)"/>')
    o.append('<path d="M 0,0 H 540 V 70 Q 270,20 0,70 Z" fill="#cfc6b6"/><path d="M 0,70 Q 270,20 540,70" stroke="#c3c8cf" stroke-width="5" fill="none"/>')
    o.append(''.join(f'<rect x="{x - 3}" y="{70 - 50 * 4 * (x / 540) * (1 - x / 540) + 6:.1f}" width="6" height="6" fill="#e2d7c6"/>' for x in range(0, 541, 14)))
    # ทางเดินด้านนอก (เห็นเมื่อเปิด)
    ox0, ox1, top, bot = 150, 390, 196, DOOR_FEET
    r_ = (ox1 - ox0) / 2
    arch = f'M {ox0},{bot} L {ox0},{top + r_} A {r_},{r_} 0 0,1 {ox1},{top + r_} L {ox1},{bot} Z'
    o.append(f'<clipPath id="dopen"><path d="{arch}"/></clipPath><g clip-path="url(#dopen)">')
    o.append(f'<rect x="{ox0}" y="{top}" width="{ox1 - ox0}" height="{bot - top}" fill="#141228"/>')
    o.append(f'<path d="M {ox0},{bot} L 236,560 L 304,560 L {ox1},{bot} Z" fill="#2c2444"/><rect x="236" y="380" width="68" height="180" fill="#1e1a34"/>')
    o.append('<rect x="250" y="400" width="40" height="70" fill="#4a5a94"/><circle cx="270" cy="424" r="9" fill="#e8eefc"/>')
    for k in range(3):
        y = 430 + k * 34; dx = 18 + k * 26
        o.append(f'<circle cx="{236 - dx * .6:.0f}" cy="{y}" r="{8 - k * 2}" fill="#fff0d8" opacity=".55"/><circle cx="{304 + dx * .6:.0f}" cy="{y}" r="{8 - k * 2}" fill="#fff0d8" opacity=".55"/>')
    o.append('<ellipse cx="270" cy="560" rx="120" ry="200" fill="#9fb2e8" opacity=".22" filter="url(#bl4)"/>')
    o.append('</g>')
    # ประตูบานคู่: closed / half / open (บานเปิดเข้าหากล้อง)
    if state == 'closed':
        lw = (ox1 - ox0) / 2
        for k, (x0, col, sh) in enumerate(((ox0, '#f8f3ea', '#e2d8c8'), (ox0 + lw, '#f0e9dd', '#d8cebe'))):
            o.append(f'<path d="M {x0},{bot} L {x0},{top + r_} A {r_},{r_} 0 0,1 {ox1},{top + r_} L {ox1},{bot} Z" fill="{col}" clip-path="url(#dopen)"/>' if False else f'<rect x="{x0}" y="{top + r_ - 10}" width="{lw}" height="{bot - top - r_ + 10}" fill="{col}"/>')
            for (py0, py1) in ((top + r_ + 6, 470), (486, bot - 14)):
                o.append(f'<rect x="{x0 + 12}" y="{py0}" width="{lw - 24}" height="{py1 - py0}" fill="{sh}"/><rect x="{x0 + 15}" y="{py0 + 3}" width="{lw - 30}" height="{py1 - py0 - 6}" fill="{col}" stroke="#c3c8cf" stroke-width="2"/>')
                o.append(f'<rect x="{x0 + 26}" y="{py0 + 14}" width="{lw - 52}" height="{py1 - py0 - 28}" fill="none" stroke="#dcd2c2" stroke-width="1.2"/>')
            hx = x0 + lw - 12 if k == 0 else x0 + 6
            o.append(f'<rect x="{hx}" y="450" width="6" height="64" rx="3" fill="#c3c8cf"/><rect x="{hx}" y="450" width="2" height="64" fill="#f4f6f9"/>')
        o.append(f'<rect x="{ox0 + (ox1 - ox0) / 2 - 1}" y="{top + r_ - 10}" width="2" height="{bot - top - r_ + 10}" fill="#fff6e6"/>')
    else:
        fe = {'half': (112, 286, 806), 'open': (44, 250, 862)}[state]
        fx_, ft, fb = fe
        for side in (-1, 1):
            hxg = ox0 if side < 0 else ox1
            ex = fx_ if side < 0 else 540 - fx_
            pts = f'{hxg},{top + r_ - 10} {ex},{ft} {ex},{fb} {hxg},{bot}'
            o.append(f'<polygon points="{pts}" fill="{"#f4eee4" if side < 0 else "#e6dfd2"}"/>')
            # แผงลวดลายบนบาน
            def lerp(a, b, t): return a + (b - a) * t
            for (t0, t1) in ((.08, .42), (.5, .92)):
                p = []
                for (u, v) in ((.15, t0), (.85, t0), (.85, t1), (.15, t1)):
                    xx = lerp(hxg, ex, u)
                    ytop = lerp(top + r_ - 10, ft, u); ybot = lerp(bot, fb, u)
                    p.append(f'{xx:.1f},{lerp(ytop, ybot, v):.1f}')
                o.append(f'<polygon points="{" ".join(p)}" fill="none" stroke="#c3c8cf" stroke-width="2.2"/>')
            o.append(f'<line x1="{ex}" y1="{ft}" x2="{ex}" y2="{fb}" stroke="{"#ffffff" if side < 0 else "#c9bfb0"}" stroke-width="3"/>')
    # กรอบประตูใหญ่: เสา ซุ้มโค้ง ช่องแสงรูปพัด
    o.append(SV.pilaster(92, 138, 210, bot))
    o.append(SV.pilaster(402, 448, 210, bot))
    o.append(f'<path d="M {ox0 - 22},{top + r_} A {r_ + 22},{r_ + 22} 0 0,1 {ox1 + 22},{top + r_}" fill="none" stroke="#e2d7c6" stroke-width="16"/>')
    o.append(f'<path d="M {ox0 - 30},{top + r_} A {r_ + 30},{r_ + 30} 0 0,1 {ox1 + 30},{top + r_}" fill="none" stroke="#c3c8cf" stroke-width="3"/>')
    o.append(f'<path d="M {ox0 - 13},{top + r_} A {r_ + 13},{r_ + 13} 0 0,1 {ox1 + 13},{top + r_}" fill="none" stroke="#c3c8cf" stroke-width="2"/>')
    o.append(f'<path d="M 258,{top - 34} L 282,{top - 34} L 288,{top - 8} L 252,{top - 8} Z" fill="#f6f1e8" stroke="#c3c8cf" stroke-width="2"/>')
    if state == 'closed':
        o.append(f'<path d="M {ox0},{top + r_ - 10} L {ox0},{top + r_} A {r_},{r_} 0 0,1 {ox1},{top + r_} L {ox1},{top + r_ - 10} Z" fill="#3a4a7c"/>')
        o.append(f'<path d="M {ox0},{top + r_} A {r_},{r_} 0 0,1 {ox1},{top + r_} Z" fill="#46588e"/>')
        for k in range(11):
            a = math.pi * (k + 1) / 12
            o.append(f'<path d="M 270,{top + r_} L {270 - math.cos(a) * r_:.1f},{top + r_ - math.sin(a) * r_:.1f}" stroke="#c3c8cf" stroke-width="2.4"/>')
        o.append(f'<circle cx="270" cy="{top + r_}" r="20" fill="#c3c8cf"/><rect x="{ox0}" y="{top + r_ - 4}" width="{ox1 - ox0}" height="8" fill="#c3c8cf"/>')
    # พื้นหินอ่อน + พรมทางเดินพุ่งไปที่ประตู
    o.append(f'<rect x="0" y="{bot}" width="540" height="{960 - bot}" fill="url(#floor7)"/>')
    for x in range(-200, 760, 60):
        o.append(f'<path d="M {270 + (x - 270) * .22:.1f},{bot} L {x},960" stroke="#cfc6b8" stroke-width="1.1" opacity=".55"/>')
    o.append(f'<path d="M {ox0 + 30},{bot} L {ox1 - 30},{bot} L 470,960 L 70,960 Z" fill="#f4f0ea"/>')
    o.append(f'<path d="M {ox0 + 30},{bot} L {ox0 + 36},{bot} L 82,960 L 70,960 Z M {ox1 - 30},{bot} L {ox1 - 36},{bot} L 458,960 L 470,960 Z" fill="#c3c8cf"/>')
    # ลำแสงจันทร์จากประตูเปิด + เงายาวของคน
    if state != 'closed':
        w = 70 if state == 'half' else 120
        o.append(f'<path d="M {270 - w},{bot} L {270 + w},{bot} L {270 + w * 2.4},960 L {270 - w * 2.4},960 Z" fill="#d6e2ff" opacity=".42"/>')
        o.append(f'<path d="M {ox0 + 10},{top + r_} L {ox1 - 10},{top + r_} L {270 + w * 2.6},960 L {270 - w * 2.6},960 Z" fill="url(#doorBeam)" opacity=".55" filter="url(#bl4)" style="mix-blend-mode:screen"/>')
        for key, x, feet, sc in figures:
            o.append(f'<path d="M {x - 16},{feet} L {x + 16},{feet} L {x + 50 + (x - 270) * 1.2},960 L {x - 50 + (x - 270) * 1.2},960 Z" fill="#14121e" opacity=".42" filter="url(#sf4)"/>')
    # คนในกรอบประตู + แสงขอบด้านหลัง
    for key, x, feet, sc in figures:
        o.append(f'<ellipse cx="{x}" cy="{feet - 130 * sc}" rx="{110 * sc:.0f}" ry="{300 * sc:.0f}" fill="#b8c8ff" opacity=".28" filter="url(#bl4)"/>')
        o.append(put(key, x, feet, sc, shadow=False))
    # แท่นดอกไม้ เชิงเทียน
    for x in (60, 480):
        o.append(f'<path d="M {x - 22},{bot + 30} L {x + 22},{bot + 30} L {x + 14},{bot - 60} L {x + 26},{bot - 72} L {x - 26},{bot - 72} L {x - 14},{bot - 60} Z" fill="#f6f1e8"/><path d="M {x + 2},{bot + 30} L {x + 22},{bot + 30} L {x + 14},{bot - 60} L {x + 26},{bot - 72} L {x + 2},{bot - 72} Z" fill="#d6ccbe"/>')
        o.append(SV.bouquetB(x, bot - 104, 50, 38, 300 + x, 1.1, 36, 8, red=0))
    o.append(SV.floor_candelabra(168, bot + 22, 150, .8))
    o.append(SV.floor_candelabra(372, bot + 22, 150, .8))
    # ม่านงาช้างกรอบภาพ + โคมระย้าด้านหน้า
    o.append(SV.drape(-1, -40, 70, 0, 560, -40, 20, n=4))
    o.append(SV.drape(1, 470, 580, 540, 560, 520, 580, n=4))
    o.append(f'<circle cx="270" cy="40" r="110" fill="url(#chGlow4)"/>')
    o.append(SV.chandelier_arms(270, -150, .62))
    o.append('<rect width="540" height="960" fill="#1a2040" opacity=".14" style="mix-blend-mode:multiply"/>')
    o.append('<rect width="540" height="960" filter="url(#stip4)" opacity=".12" style="mix-blend-mode:overlay"/><rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

WB = ('wb', 270, DOOR_FEET, DOOR_S)
WB_FACE = (270, DOOR_FEET - 464 * DOOR_S)

# ---------------------------------------------------------------- มือถือในมือ
def phone(screen, bg='#3a3448', glow='#aac0ff'):
    o = [f'<rect width="540" height="960" fill="{bg}"/>',
         '<rect width="540" height="960" fill="url(#dimV)"/>',
         f'<ellipse cx="270" cy="420" rx="230" ry="300" fill="{glow}" opacity=".12" filter="url(#bl4)"/>',
         # ผ้าชุดเจ้าสาวด้านล่างเบลอ
         '<path d="M -20,820 C 120,760 420,760 560,820 L 560,960 L -20,960 Z" fill="#f2ede4" opacity=".9" filter="url(#dof4)"/>',
         '<rect x="140" y="140" width="260" height="520" rx="34" fill="#16161c"/><rect x="150" y="150" width="240" height="500" rx="26" fill="#0c0c12"/>']
    o.append(f'<clipPath id="scr{abs(hash(screen)) % 99999}"><rect x="156" y="156" width="228" height="488" rx="22"/></clipPath><g clip-path="url(#scr{abs(hash(screen)) % 99999})">{screen}</g>')
    o.append('<rect x="240" y="164" width="60" height="12" rx="6" fill="#0c0c12"/>')
    # มือ (ผิวเจ้าสาว) จับสองข้าง
    sk, sks = '#fbe2cf', '#efc3a8'
    o.append(f'<path d="M 100,700 C 110,600 130,520 150,470 L 176,480 C 168,540 168,600 172,660 L 150,760 L 90,760 Z" fill="{sk}"/>')
    o.append(f'<path d="M 440,700 C 430,600 410,520 390,470 L 364,480 C 372,540 372,600 368,660 L 390,760 L 450,760 Z" fill="{sks}"/>')
    o.append(f'<path d="M 150,470 C 160,450 176,452 178,470 L 176,490 Z M 390,470 C 380,450 364,452 362,470 L 364,490 Z" fill="{sk}"/>')
    o.append('<rect x="152" y="560" width="18" height="6" rx="3" fill="#f4f6f9" transform="rotate(-8 161 563)"/>')
    return ''.join(o)

def scr_bg(c1='#1a1c28', c2='#2a2c3c'):
    return f'<rect x="156" y="156" width="228" height="488" fill="{c1}"/><rect x="156" y="156" width="228" height="40" fill="{c2}"/>'

def mini_couple(x, y, w, h, hair, seed, highlight=False):
    r = random.Random(seed)
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e8e1d6"/>', f'<rect x="{x}" y="{y}" width="{w}" height="{h * .45}" fill="#c9a6d6" opacity=".6"/>']
    bx, gx = x + w * .38, x + w * .64
    o.append(f'<path d="M {bx - 9},{y + h} L {bx - 4},{y + h * .5} L {bx + 4},{y + h * .5} L {bx + 9},{y + h} Z" fill="#fffdf9"/>')
    o.append(f'<circle cx="{bx}" cy="{y + h * .38}" r="5" fill="#fbe2cf"/><path d="M {bx - 6},{y + h * .38} C {bx - 6},{y + h * .2} {bx + 6},{y + h * .2} {bx + 6},{y + h * .38} L {bx + 6},{y + h * .55} L {bx - 6},{y + h * .55} Z" fill="{hair}"/><circle cx="{bx}" cy="{y + h * .4}" r="4" fill="#fbe2cf"/>')
    o.append(f'<rect x="{gx - 6}" y="{y + h * .5}" width="12" height="{h * .5}" fill="#24252e"/><circle cx="{gx}" cy="{y + h * .4}" r="5" fill="#f6dcc8"/><path d="M {gx - 5},{y + h * .38} C {gx - 5},{y + h * .26} {gx + 5},{y + h * .26} {gx + 5},{y + h * .36} Z" fill="#121118"/>')
    o.append(f'<circle cx="{x + 8}" cy="{y + h - 8}" r="4" fill="#f7dbe4"/><circle cx="{x + w - 8}" cy="{y + h - 8}" r="4" fill="#fffaf7"/>')
    if highlight: o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="#ffd84a" stroke-width="3"/>')
    return ''.join(o)

def scr_album():
    o = [scr_bg(), '<text x="170" y="182" font-size="13" font-weight="600" fill="#e8ecf4" font-family="IBM Plex Sans Thai">อัลบั้ม · งานแต่ง</text>']
    hairs = ['#3a2620', '#141017', '#6a4a3c', '#2a1c18', '#141017', '#5a3a2a', '#0e0b10', '#3a2a24', '#7a5848']
    years = ['2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025']
    for i in range(9):
        x = 162 + (i % 3) * 74; y = 206 + (i // 3) * 132
        o.append(mini_couple(x, y, 68, 104, hairs[i], i, highlight=(i == 8)))
        o.append(f'<text x="{x + 34}" y="{y + 120}" text-anchor="middle" font-size="10" fill="#9aa2b8" font-family="IBM Plex Sans Thai">{years[i]}</text>')
    return ''.join(o)

def scr_lastyear():
    o = [scr_bg(), '<text x="170" y="182" font-size="13" font-weight="600" fill="#e8ecf4" font-family="IBM Plex Sans Thai">2025</text>',
         '<rect x="162" y="206" width="216" height="330" fill="#e8e1d6"/><rect x="162" y="206" width="216" height="140" fill="#c9a6d6" opacity=".6"/>',
         '<clipPath id="lyC"><rect x="162" y="206" width="216" height="330"/></clipPath><g clip-path="url(#lyC)">',
         put('wb_white', 236, 600, .62, shadow=False), put('groom', 318, 600, .6, shadow=False), '</g>',
         '<text x="270" y="568" text-anchor="middle" font-size="12" fill="#c8cede" font-family="IBM Plex Sans Thai">โรงแรมเดิม · ดอกไม้แบบเดิม</text>']
    return ''.join(o)

def scr_search():
    o = [scr_bg(), '<rect x="166" y="206" width="208" height="30" rx="15" fill="#2c3044"/><text x="182" y="226" font-size="12" fill="#e8ecf4" font-family="IBM Plex Sans Thai">ชื่อเจ้าสาว 2025</text>']
    for i in range(5):
        y = 254 + i * 72
        o.append(f'<rect x="166" y="{y}" width="208" height="60" rx="8" fill="#22263a"/><rect x="176" y="{y + 10}" width="40" height="40" rx="4" fill="#3a3f58"/>')
        o.append(f'<rect x="226" y="{y + 14}" width="{120 - i * 8}" height="8" rx="4" fill="#8a94b4"/><rect x="226" y="{y + 32}" width="{90 + i * 6}" height="6" rx="3" fill="#4e5674"/>')
    return ''.join(o)

def scr_missing():
    o = [scr_bg('#1e1416', '#2a1c1e'), '<text x="170" y="182" font-size="13" font-weight="600" fill="#f0e2e2" font-family="IBM Plex Sans Thai">ผลการค้นหา</text>']
    hairs = ['#3a2620', '#141017', '#6a4a3c', '#2a1c18', '#141017', '#5a3a2a']
    for i in range(6):
        x = 164 + (i % 2) * 110; y = 204 + (i // 2) * 144
        o.append(f'<rect x="{x}" y="{y}" width="102" height="136" fill="#f4efe6"/><rect x="{x}" y="{y}" width="102" height="22" fill="#a8222c"/>')
        o.append(f'<text x="{x + 51}" y="{y + 16}" text-anchor="middle" font-size="10" font-weight="600" fill="#fff" font-family="IBM Plex Sans Thai">ตามหาคนหาย</text>')
        o.append(f'<rect x="{x + 26}" y="{y + 30}" width="50" height="60" fill="#d8d0c4"/><circle cx="{x + 51}" cy="{y + 54}" r="12" fill="#fbe2cf"/><path d="M {x + 38},{y + 54} C {x + 38},{y + 34} {x + 64},{y + 34} {x + 64},{y + 54} L {x + 66},{y + 80} L {x + 36},{y + 80} Z" fill="{hairs[i]}"/><circle cx="{x + 51}" cy="{y + 57}" r="10" fill="#fbe2cf"/>')
        o.append(f'<rect x="{x + 12}" y="{y + 100}" width="78" height="6" rx="3" fill="#8a8078"/><rect x="{x + 18}" y="{y + 114}" width="66" height="5" rx="2.5" fill="#b8aea4"/>')
    return ''.join(o)

def scr_call():
    return ''.join([scr_bg('#141826', '#141826'), '<circle cx="270" cy="300" r="44" fill="#2c3248"/><circle cx="270" cy="290" r="16" fill="#4a5270"/><path d="M 244,330 C 248,312 292,312 296,330 Z" fill="#4a5270"/>',
                    '<text x="270" y="390" text-anchor="middle" font-size="16" font-weight="600" fill="#eef0f6" font-family="IBM Plex Sans Thai">ไม่ทราบชื่อ</text>',
                    '<text x="270" y="414" text-anchor="middle" font-size="12" fill="#9aa2b8" font-family="IBM Plex Sans Thai">กำลังโทรเข้า…</text>',
                    '<circle cx="210" cy="560" r="26" fill="#d6404a"/><circle cx="330" cy="560" r="26" fill="#3aa86a"/>',
                    '<path d="M 198,562 q 12,-8 24,0" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/><path d="M 318,566 q 12,-14 24,0" stroke="#fff" stroke-width="5" fill="none" stroke-linecap="round"/>'])

# ---------------------------------------------------------------- ลิฟต์ (แบบร่างโทนเงิน)
def elevator():
    return ''.join([
        '<rect width="540" height="960" fill="#2c2a3c"/>',
        '<path d="M 0,0 L 540,0 L 440,170 L 100,170 Z" fill="#d8dae0"/>' + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="16" ry="5" fill="#fffdf6"/>' for x, y in ((170, 60), (270, 60), (370, 60), (200, 130), (270, 130), (340, 130))),
        '<path d="M 0,0 L 100,170 L 100,760 L 0,960 Z" fill="#b8bcc6"/><path d="M 540,0 L 440,170 L 440,760 L 540,960 Z" fill="#a8acb8"/>',
        '<path d="M 0,560 L 100,520 L 100,530 L 0,572 Z M 540,560 L 440,520 L 440,530 L 540,572 Z" fill="#e8ecf2"/>',
        '<rect x="100" y="170" width="340" height="590" fill="#c8ccd4"/>',
        '<rect x="150" y="250" width="240" height="510" fill="#a8acb6"/>',
        # ประตูเปิดเห็นทางเดินเดิม
        '<rect x="200" y="250" width="140" height="510" fill="#2a2440"/><path d="M 200,760 L 240,560 L 300,560 L 340,760 Z" fill="#4a3a5a"/><rect x="240" y="400" width="60" height="160" fill="#3a3452"/>',
        '<circle cx="216" cy="440" r="10" fill="#fff0d8" opacity=".5" filter="url(#bl4)"/><circle cx="324" cy="440" r="10" fill="#fff0d8" opacity=".5" filter="url(#bl4)"/>',
        '<rect x="150" y="250" width="50" height="510" fill="#b8bcc6"/><rect x="340" y="250" width="50" height="510" fill="#a2a6b0"/>',
        '<rect x="226" y="196" width="88" height="36" rx="4" fill="#16141e"/><text x="282" y="223" text-anchor="middle" font-size="26" font-weight="600" fill="#cbb2ff" font-family="IBM Plex Mono, monospace">12</text><path d="M 236,222 l 8,-12 l 8,12 Z" fill="#cbb2ff"/>',
        '<rect x="408" y="400" width="22" height="70" rx="3" fill="#24222e"/>' + ''.join(f'<circle cx="{414 + (i % 2) * 10}" cy="{410 + (i // 2) * 12}" r="3" fill="{"#cbb2ff" if i == 3 else "#c3c8cf"}"/>' for i in range(10)),
        '<path d="M 100,760 L 440,760 L 540,960 L 0,960 Z" fill="#d8d4d8"/>',
        put('bride', 270, 900, .62)])

# ---------------------------------------------------------------- ห้องพัก (แบบร่าง กลางคืนเย็น)
def suite_door(feet_shadow=False):
    o = ['<rect width="540" height="960" fill="#3c4258"/>', '<rect x="0" y="0" width="540" height="90" fill="#2e3346"/>',
         '<rect x="0" y="700" width="540" height="260" fill="#2a2c3a"/>',
         '<rect x="150" y="190" width="240" height="510" fill="#c3c8cf"/><rect x="160" y="200" width="220" height="500" fill="#5a4038"/>',
         '<rect x="176" y="220" width="188" height="200" fill="none" stroke="#6e5248" stroke-width="3"/><rect x="176" y="440" width="188" height="240" fill="none" stroke="#6e5248" stroke-width="3"/>',
         '<circle cx="270" cy="330" r="5" fill="#c3c8cf"/><circle cx="270" cy="330" r="2.2" fill="#14141a"/>',
         '<rect x="350" y="450" width="18" height="6" rx="3" fill="#c3c8cf"/><path d="M 362,420 q -24,16 -40,4" stroke="#c3c8cf" stroke-width="2" fill="none" stroke-dasharray="4 2"/>',
         '<rect x="160" y="696" width="220" height="5" fill="#fff1dd" filter="url(#glow)"/>',
         '<path d="M 160,701 L 380,701 L 470,820 L 70,820 Z" fill="#fff1dd" opacity=".12"/>']
    if feet_shadow:
        o.append('<rect x="226" y="695" width="26" height="7" fill="#0c0c12"/><rect x="290" y="695" width="26" height="7" fill="#0c0c12"/>')
    # ขอบเตียงฉากหน้า
    o.append('<path d="M -20,860 C 120,820 300,830 560,800 L 560,960 L -20,960 Z" fill="#e8e6ee" filter="url(#dof4)"/>')
    o.append('<rect width="540" height="960" fill="url(#vigD)"/>')
    return ''.join(o)

def corridor_groom():
    return ''.join(['<rect width="540" height="960" fill="#221e30"/>',
                    '<path d="M 0,0 L 540,0 L 360,380 L 180,380 Z" fill="#1a1726"/><path d="M 0,960 L 180,620 L 360,620 L 540,960 Z" fill="#3a2a40"/>',
                    '<path d="M 0,0 L 180,380 L 180,620 L 0,960 Z" fill="#2c2840"/><path d="M 540,0 L 360,380 L 360,620 L 540,960 Z" fill="#262238"/>',
                    '<circle cx="90" cy="340" r="40" fill="#fff0d8" opacity=".25" filter="url(#bl4)"/><circle cx="450" cy="340" r="40" fill="#fff0d8" opacity=".25" filter="url(#bl4)"/>',
                    put('groom', 270, 330 + 492 * 1.7, 1.7, shadow=False),
                    '<rect width="540" height="960" fill="url(#vigD)"/>'])

def dark_wb(s=1.7):
    return ''.join(['<rect width="540" height="960" fill="#0e0d16"/>',
                    '<ellipse cx="270" cy="360" rx="200" ry="260" fill="#3a3a5a" opacity=".35" filter="url(#bl4)"/>',
                    put('wb', 270, 330 + 464 * s, s, shadow=False),
                    '<rect width="540" height="960" fill="#1a1a30" opacity=".35" style="mix-blend-mode:multiply"/>',
                    '<rect width="540" height="960" fill="url(#vigD)"/>'])

def card():
    return ''.join(['<rect width="540" height="960" fill="#0a090f"/>',
                    '<text x="270" y="300" text-anchor="middle" font-size="22" font-weight="600" fill="#ffffff" font-family="IBM Plex Sans Thai">คุณคิดว่าผู้หญิงคนนั้น</text>',
                    '<text x="270" y="334" text-anchor="middle" font-size="22" font-weight="600" fill="#ffffff" font-family="IBM Plex Sans Thai">เข้ามาเพื่อช่วยคุณ</text>',
                    '<text x="270" y="368" text-anchor="middle" font-size="22" font-weight="600" fill="#ffffff" font-family="IBM Plex Sans Thai">หรือกำลังหาคนมาตายแทนตัวเอง?</text>',
                    '<rect x="70" y="430" width="400" height="64" rx="14" fill="#2a2440" stroke="#c9a8ff" stroke-width="2.5"/><text x="96" y="470" font-size="19" font-weight="600" fill="#ffffff" font-family="IBM Plex Sans Thai">A · เข้ามาช่วยคุณ</text>',
                    '<rect x="70" y="512" width="400" height="64" rx="14" fill="#16141f" stroke="#4a4466" stroke-width="2"/><text x="96" y="552" font-size="19" font-weight="600" fill="#b8b2cc" font-family="IBM Plex Sans Thai">B · หาคนมาตายแทนตัวเอง</text>',
                    '<text x="270" y="630" text-anchor="middle" font-size="14" fill="#9a94b0" font-family="IBM Plex Sans Thai">คอมเมนต์บอกหน่อย</text>'])

def label(text):
    w = 18 + len(text) * 13
    return f'<rect x="24" y="24" width="{w}" height="34" rx="17" fill="#16141f" stroke="#9a7cff" stroke-width="1.6"/><text x="{24 + w / 2}" y="47" text-anchor="middle" font-size="15" font-weight="600" fill="#ffffff" font-family="IBM Plex Sans Thai">{text}</text>'

def inset_ring():
    return ('<circle cx="430" cy="230" r="78" fill="#141218" stroke="#ffffff" stroke-width="4"/>'
            '<path d="M 380,240 C 400,214 460,214 482,240 L 486,270 L 376,270 Z" fill="#141218"/>'
            '<path d="M 392,250 L 470,250" stroke="#2c2a34" stroke-width="18" stroke-linecap="round"/>'
            '<ellipse cx="430" cy="248" rx="14" ry="5" fill="none" stroke="#f4f6f9" stroke-width="4"/><circle cx="430" cy="242" r="4" fill="#e8f0ff"/>')

# ---------------------------------------------------------------- ซับไทย
def wrap_thai(text, n=19):
    words = text.split(' '); lines = []; cur = ''
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= n or not cur:
            cur = (cur + ' ' + w).strip()
        else:
            lines.append(cur); cur = w
        while len(cur) > n + 6:
            lines.append(cur[:n]); cur = cur[n:]
    if cur: lines.append(cur)
    return lines[:4]

def subtitle(text):
    lines = wrap_thai(text)
    lh = 27; y0 = 712 - (len(lines) - 1) * lh / 2
    return ''.join(f'<text x="270" y="{y0 + i * lh:.0f}" text-anchor="middle" font-size="20" font-weight="700" fill="#ffd84a" stroke="#1a1410" stroke-width="5" paint-order="stroke" stroke-linejoin="round" font-family="IBM Plex Sans Thai">{l}</text>' for i, l in enumerate(lines))

# ---------------------------------------------------------------- 30 ช็อต
def script_lines():
    out = {}
    for line in open(os.path.join(HERE, '..', 'script.md')):
        m = re.match(r'^(\d+)\. (.*)$', line.strip())
        if m: out[int(m.group(1))] = m.group(2)
    return out

def clean_sub(t):
    t = re.sub(r'^\(.*?\)\s*', '', t)
    t = re.sub(r'\[[^\]]*\]\s*', '', t)
    return t.replace('"', '').strip()

bx, by = face_xy('bride', *CAST['bride']); gx, gy = face_xy('groom', *CAST['groom'])
mx, my = face_xy('mom', *CAST['mom']); px, py = face_xy('ph', *CAST['ph'])
sx, sy = face_xy('staff', *CAST['staff'])

SHOTS = {
    1: ('WS · ซูมเข้าช้า ๆ', 'ผู้บรรยาย', 'ภาพกว้างห้องพิธีคืนพระจันทร์เต็มดวง คู่บ่าวสาวยืนกลางลายแหวน แขกยืนสองข้าง กล้องค่อย ๆ ดันเข้าหาคู่บ่าวสาว', hall()),
    2: ('WS · แพนลงจากโคม', 'ผู้บรรยาย', 'เริ่มที่โคมระย้ากับนาฬิกา แล้วแพนลงมาเห็นดอกไม้และแขกที่กำลังปรบมือ', cam(hall(), 270, 330, 1.25, 330)),
    3: ('MS · คู่บ่าวสาว', 'ผู้บรรยาย', 'ภาพสองคน เจ้าสาวยิ้ม เจ้าบ่าวยิ้มมุมปาก ดูสมบูรณ์แบบ', cam(hall(), (bx + gx) / 2, by + 60, 2.2, 360)),
    4: ('WS · ประตู · กล้องนิ่ง', 'ผู้บรรยาย', 'ประตูบานคู่สูงสองชั้นที่ปิดอยู่ค่อย ๆ แง้มออกเข้าหากล้อง แสงจันทร์เย็นจากทางเดินพาดยาวลงพรม เงียบหนึ่งจังหวะ', doors('half')),
    5: ('MS · ประตู + อินเสิร์ตแหวน', 'ผู้บรรยาย', 'ผู้หญิงชุดดำยืนครึ่งตัวในเงาตรงกรอบประตู หยุดนิ่งสั้น ๆ แล้วก้าวเข้ามา ตัดอินเสิร์ตแหวนเงินบนถุงมือดำ', doors('open', [WB]) + inset_ring()),
    6: ('CU · ผู้หญิงชุดดำ', 'ผู้หญิงชุดดำ', 'กล้องอยู่ที่ผู้พูด หน้าเธอนิ่ง พูดเบาแต่ชัด', cam(doors('open', [WB]), WB_FACE[0], WB_FACE[1] + 40, 3.2, 380)),
    7: ('MS · ประตู', 'ผู้บรรยาย', 'รปภ. เดินเข้ามาประกบผู้หญิงชุดดำ เจ้าบ่าวพูดกับแขก (เสียงบรรยาย ไม่ขยับปากใคร)', doors('open', [('wb', 246, DOOR_FEET, DOOR_S), ('guard', 312, DOOR_FEET + 4, DOOR_S)])),
    8: ('MS · หันกลับมา', 'ผู้บรรยาย', 'ก่อนพ้นประตู เธอหยุดแล้วหันกลับมามองตรงกล้อง (มุมมองเจ้าสาว)', cam(doors('open', [('wb', 246, DOOR_FEET, DOOR_S), ('guard', 312, DOOR_FEET + 4, DOOR_S)]), 270, 600, 1.7, 430)),
    9: ('ECU · ผู้หญิงชุดดำ', 'ผู้หญิงชุดดำ', 'ใกล้มากที่ตาและปาก เสียงกระซิบเบา ๆ ไม่ตะโกน', cam(doors('open', [WB]), WB_FACE[0], WB_FACE[1] + 4, 5.2, 380)),
    10: ('MS · เจ้าสาว · ซูมเข้าช้า', 'ผู้บรรยาย', 'กลับมาที่ห้องพิธี เจ้าสาวยังยิ้มแต่ตาเริ่มสงสัย ภาพเย็นลงเล็กน้อย กล้องค่อย ๆ ดันเข้าหาหน้า', cam(hall(cool=.12), bx, by + 40, 2.4, 380)),
    11: ('MS · แขกฝั่งเจ้าบ่าว', 'ผู้บรรยาย', 'แขกฝั่งเจ้าบ่าวยืนนิ่ง ยิ้มแข็ง ไม่มีใครยกมือถือ ตัดกับเพื่อนเจ้าสาวที่ถ่ายรูปอยู่ขอบเฟรม', cam(hall(cool=.12), 420, 640, 1.9, 420)),
    12: ('CU · แม่เจ้าบ่าว', 'ผู้บรรยาย', 'แม่เจ้าบ่าวยิ้มสุภาพแต่ตาไม่ยิ้มตาม', cam(hall(cool=.12), mx, my + 20, 3.2, 380)),
    13: ('MS · ช่างภาพ', 'ผู้บรรยาย', 'ช่างภาพยิ้มเจื่อนเหมือนเพิ่งพูดอะไรผิด มือยังจับกล้อง', cam(hall(cool=.12), px, py + 70, 1.9, 380)),
    14: ('CU · พนักงานโรงแรม', 'ผู้บรรยาย', 'พนักงานมองมาที่กล้องด้วยสายตาสงสาร แล้วหลบตา', cam(hall(cool=.12), sx, sy + 20, 3.4, 380)),
    15: ('CU · มือถือ', 'ผู้บรรยาย', 'มือเจ้าสาวถือมือถือเจ้าบ่าวในห้องพักเจ้าสาว แสงจอส่องหน้า', phone(scr_search().replace('ชื่อเจ้าสาว 2025', 'รหัสผ่าน ••••'))),
    16: ('ECU · จอมือถือ', 'ผู้บรรยาย', 'อัลบั้มงานแต่งเก้าปี เจ้าบ่าวคนเดิมทุกรูป เจ้าสาวไม่ซ้ำหน้า', phone(scr_album())),
    17: ('ECU · รูปปีที่แล้ว', 'ผู้บรรยาย', 'ซูมเข้ารูปปี 2025 เจ้าสาวในรูปคือผู้หญิงชุดดำ', phone(scr_lastyear())),
    18: ('ECU · ค้นหา', 'ผู้บรรยาย', 'พิมพ์ชื่อเจ้าสาวทีละคน', phone(scr_search())),
    19: ('ECU · ประกาศคนหาย', 'ผู้บรรยาย', 'ผลค้นหาเป็นประกาศตามหาคนหายทั้งหมด เสียงทุ้มกระแทกเบา ๆ', phone(scr_missing(), '#2a1c22', '#ffb0b0')),
    20: ('WS · ลิฟต์', 'ผู้บรรยาย', 'เจ้าสาวในลิฟต์ ประตูเปิดออกที่ชั้น 12 ทางเดินเดิมซ้ำแล้วซ้ำเล่า (ตัดซ้ำสามครั้ง)', elevator()),
    21: ('CU · สายเข้า', 'ผู้บรรยาย', 'มือถือเจ้าสาวมีสายเข้าจากเบอร์ที่ไม่รู้จัก ในห้องพักมืด ๆ', phone(scr_call(), '#1e2234')),
    22: ('CU · ผู้หญิงชุดดำ (ทางโทรศัพท์)', 'ผู้หญิงชุดดำ', 'กล้องอยู่ที่ผู้พูดแม้คุยทางโทรศัพท์ เธอยืนในความมืด แสงอ่อนจากด้านหน้า', dark_wb()),
    23: ('ECU · ผู้หญิงชุดดำ', 'ผู้หญิงชุดดำ', 'ใกล้ขึ้นอีก น้ำเสียงเรียบ ไม่ข่มขู่', dark_wb(2.5)),
    24: ('MS · ประตูห้องพัก · กล้องนิ่ง', 'ผู้บรรยาย', 'เงียบ แล้วเสียงเคาะสามครั้ง เห็นเงาเท้าสองข้างลอดใต้ประตู', suite_door(True)),
    25: ('CU · เจ้าบ่าวหลังประตู', 'เจ้าบ่าว', 'กล้องอยู่ที่ผู้พูด เจ้าบ่าวยืนในทางเดินมืด ยิ้มมุมปาก พูดนุ่ม ๆ', corridor_groom()),
    26: ('WS · หนึ่งปีต่อมา', 'ผู้บรรยาย', 'ห้องพิธีเดิม เจ้าบ่าวคนเดิมยืนยิ้มข้างเจ้าสาวคนใหม่ ป้ายเวลาที่มุมบน',
         hall({k: v for k, v in CAST.items() if k not in ('bride', 'staff', 'ph')} | {'nb': (228, 845, .58)}) + label('หนึ่งปีต่อมา')),
    27: ('WS · ประตู · กล้องนิ่ง', 'ผู้บรรยาย', 'ประตูห้องจัดเลี้ยงค่อย ๆ เปิดออกอีกครั้ง จังหวะเดียวกับช็อต 4', doors('half')),
    28: ('MS · ประตู', 'ผู้บรรยาย', 'ผู้หญิงชุดดำที่ยืนในกรอบประตูคราวนี้คือเจ้าสาวคนแรก (หน้าเจ้าสาว ชุดดำ แหวนเงินบนถุงมือ)', doors('open', [('bride_black', 270, DOOR_FEET, DOOR_S)])),
    29: ('CU · เจ้าสาวในชุดดำ', 'เจ้าสาว (ชุดดำ)', 'กล้องอยู่ที่ผู้พูด ประโยคเดียวกับช็อต 6 คำต่อคำ', cam(doors('open', [('bride_black', 270, DOOR_FEET, DOOR_S)]), WB_FACE[0], WB_FACE[1] + 40, 3.2, 380)),
    30: ('การ์ดคำถาม', '—', 'ตัดดำ แล้วขึ้นการ์ด A/B ไฮไลต์สลับไปมาพร้อมเสียงคลิก', card()),
}

EXTRA_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="dimV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".5" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".25"/></linearGradient>
<linearGradient id="doorBeam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dfe8ff" stop-opacity=".6"/><stop offset="1" stop-color="#dfe8ff" stop-opacity="0"/></linearGradient>
<radialGradient id="vigD" cx=".5" cy=".45" r=".75"><stop offset=".5" stop-color="#0a0a14" stop-opacity="0"/><stop offset="1" stop-color="#0a0a14" stop-opacity=".6"/></radialGradient>
</defs></svg>'''

CSS = '''<title>สตอรีบอร์ดงานแต่ง</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=IBM+Plex+Mono:wght@500&display=swap">
<style>
/* Layout: storyboard grid of 9:16 frames grouped by scene, captions under each frame. Single dark look by choice. */
:root{--stage:#101018;--ink:#e6e4ee;--muted:#9a96ac;--line:#2a2838;--accent:#c9a8ff;--font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;color-scheme:dark}
html,body{background:var(--stage);color:var(--ink)}
body{font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 48px}
.wrap{max-width:1240px;margin:0 auto;display:flex;flex-direction:column;gap:22px}
h1{margin:0;font-size:22px;font-weight:600;text-wrap:balance}
h1 span{display:block;font-size:13px;font-weight:400;color:var(--muted);margin-top:4px}
h2{margin:8px 0 0;font-size:16px;font-weight:600;color:var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:18px}
figure{margin:0;display:flex;flex-direction:column;gap:8px;min-width:0}
figure svg{display:block;width:100%;height:auto;aspect-ratio:9/16;border-radius:4px;box-shadow:0 0 0 1px var(--line)}
figcaption{display:flex;flex-direction:column;gap:3px;font-size:12.5px;line-height:1.55}
.num{display:flex;gap:8px;align-items:baseline}
.num b{font-size:15px;color:#fff;font-variant-numeric:tabular-nums}
.num span{color:var(--accent);font-size:12px}
.who{color:#ffd84a;font-size:12px}
small{color:var(--muted);font-size:12px}
.note{font-size:13px;color:var(--muted);line-height:1.6;max-width:75ch}
</style>'''

SCENES = [('เปิดเรื่อง', [1]), ('ฉากที่ 1 · วันที่มีความสุขที่สุด', [2, 3, 4, 5, 6]), ('ฉากที่ 2 · ผู้หญิงปริศนา', [7, 8, 9, 10, 11, 12, 13, 14]),
          ('ฉากที่ 3 · ความจริงในห้องพักเจ้าสาว', [15, 16, 17, 18, 19]), ('ฉากที่ 4 · คืนเข้าหอ', [20, 21, 22, 23, 24, 25]), ('ฉากจบ · หนึ่งปีต่อมา', [26, 27, 28, 29, 30])]

def build():
    lines = script_lines()
    html_scenes = ''
    for title, nums in SCENES:
        cards = ''
        for n in nums:
            camtxt, who, desc, content = SHOTS[n]
            sub = '' if n == 30 else subtitle(clean_sub(lines[n]))
            svg = (f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="ช็อต {n}">'
                   f'<clipPath id="fr{n}"><rect width="540" height="960"/></clipPath><g clip-path="url(#fr{n})">{content}{sub}</g></svg>')
            cards += f'<figure>{svg}<figcaption><div class="num"><b>{n:02d}</b><span>{camtxt}</span></div><div class="who">เสียง: {who}</div><small>{desc}</small></figcaption></figure>'
        html_scenes += f'<h2>{title}</h2><div class="grid">{cards}</div>'
    base = N9.H8.S.DEFS
    for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
        base = re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=re.S)
    page = (CSS + base + H8.DEFS_EXTRA + N9.EXTRA_DEFS + WC.DEFS + B2.DEFS + SP.DEFS + EXTRA_DEFS + CHAR_DEFS +
            f'''<div class="wrap"><h1>สตอรีบอร์ด · ถ้าวันนี้เป็นวันแต่งงานของคุณ<span>Odd Hours · 30 ช็อตตามบท · ห้องพิธีวิวพระจันทร์เต็มดวง</span></h1>
<p class="note">ห้องพิธีกับตัวละครใช้ของที่ทำไว้แล้ว ส่วนประตูห้องจัดเลี้ยง หน้าจอมือถือ ลิฟต์ ห้องพัก และทางเดิน เป็นแบบร่างในโทนเดียวกัน ไว้ดูจังหวะและมุมกล้องก่อน ตัวละครยังยืนท่าตรงแบบแผ่นตัวละคร ท่าทางจริงจะทำตอนภาพนิ่ง ซับไทยวางที่ราว 74% ของความสูงเฟรมตามมาตรฐานช่อง</p>
{html_scenes}</div>''')
    out = os.path.join(HERE, 'storyboard.html')
    open(out, 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
