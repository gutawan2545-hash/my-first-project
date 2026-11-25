#!/usr/bin/env python3
"""บ้านตรงข้าม: สตอรีบอร์ดพร้อมตัวละคร
ฉากจาก scenes.py · ตัวละครจาก characters/house-across (หน้า/หลังเท่านั้น) · ซับไทยเหลือง + อังกฤษขาวที่ y ~712
รัน: python3 storyboard.py -> storyboard.html"""
import os, runpy, html

HERE = os.path.dirname(os.path.abspath(__file__))
CHAR = os.path.join(HERE, '..', '..', 'characters', 'house-across')

os.chdir(HERE); SG = runpy.run_path('scenes.py')
SC = {sid: body for sid, _, _, body in SG['S']}
frame_svg_inner = SG['frame_svg']
os.chdir(CHAR); TG = runpy.run_path('turnaround.py'); OG = runpy.run_path('others.py')
os.chdir(HERE)
C, FH = TG['C'], TG['FRONT_HEAD']
front_view, back_view = TG['front_view'], TG['back_view']

# hero in uniform (before the accident): no cast, no crutches
C['hero_cop'] = dict(C['hero'], top='uniform', tc=('#8a6c4a', '#a38563', '#6a5136'), bot=('#7a5e40', '#92755a', '#5c452e'),
                     shoe='#15151a', cast=False, crutch=False)
FH['hero_cop'] = FH['hero']

def tfig(key, view='front'):
    c = C[key]
    body = front_view(key) if view == 'front' else back_view(key)
    grp = f'<g transform="translate(200,{c["ty"]}) scale({c["sc"]})">{body}</g>'
    return grp, c['ty'] + (c['foot'] + 16) * c['sc'], c['ty'] - 70 * c['sc']

def ofig(name):
    body, ty, sc, feet = {'dad': (OG['dd_body'], 176, 1.15, 482), 'mom': (OG['mm_body'], 182, 1.1, 484), 'friend': (OG['fr_body'], 170, 1.2, 482)}[name]
    return OG['figure'](body, ty, sc), ty + feet * sc, ty - 64 * sc

def put(fig, x, feet_y, height, sil=False, shadow=True):
    grp, f, t = fig
    k = height / (f - t)
    tr = f'translate({x - 200*k:.1f},{feet_y - f*k:.1f}) scale({k:.4f})'
    sh = f'<ellipse cx="{x:.0f}" cy="{feet_y:.0f}" rx="{height*.2:.0f}" ry="{height*.03:.0f}" fill="#120a14" opacity=".45" filter="url(#sbBlur)"/>' if shadow and not sil else ''
    return sh + f'<g transform="{tr}"{" filter=\"url(#sbSil)\"" if sil else ""}>{grp}</g>'

def P(key, x, y, h, view='front', **kw): return put(tfig(key, view), x, y, h, **kw)
def O(name, x, y, h, **kw): return put(ofig(name), x, y, h, **kw)

def clip(rect, inner):
    x0, y0, x1, y1 = rect
    i = f'sbc{abs(hash(inner)) % 10**8}'
    return f'<clipPath id="{i}"><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}"/></clipPath><g clip-path="url(#{i})">{inner}</g>'

def subs(th, en):
    if not th: return ''
    tl = th.split('\n'); el = en.split('\n') if en else []
    y = 700 - (len(tl) - 1) * 13
    o = ''.join(f'<text x="270" y="{y + i*26}" class="th">{html.escape(l)}</text>' for i, l in enumerate(tl))
    y2 = y + len(tl) * 26 - 4
    o += ''.join(f'<text x="270" y="{y2 + i*17}" class="en">{html.escape(l)}</text>' for i, l in enumerate(el))
    return o

def tag(t):
    w = 16 + len(t) * 10.5
    return f'<rect x="20" y="22" width="{w:.0f}" height="30" rx="15" fill="#1c1428" fill-opacity=".86" stroke="#9a7ad8" stroke-width="1.4"/><text x="{20+w/2:.0f}" y="42" class="tag">{html.escape(t)}</text>'

def watermark():
    return '<g transform="translate(508,36)" opacity=".7"><ellipse rx="13" ry="8" fill="none" stroke="#c9a8ff" stroke-width="1.6"/><circle r="4" fill="#c9a8ff"/></g>'

def bag(x, y, k=1):
    return f'<g transform="translate({x},{y}) scale({k})"><path d="M -16,0 C -22,-20 -10,-34 0,-34 C 12,-34 22,-20 16,0 Z" fill="#141016"/><path d="M -4,-34 L 0,-42 L 4,-34" fill="#141016"/></g>'

def hooded_back(x, y, h):
    k = h / 560
    return (f'<g transform="translate({x - 200*k:.0f},{y - 900*k + 0:.0f}) scale({k:.3f})"><g transform="translate(200,210) scale(1.25)">'
            '<path d="M -64,100 C -70,70 -66,40 -48,30 L 48,30 C 66,40 70,70 64,100 L 70,330 L -70,330 Z" fill="#2c2650"/>'
            '<path d="M -48,40 C -70,40 -86,30 -88,6 C -88,-14 -76,-24 -62,-24 L -40,-6 Z M 48,40 C 70,40 86,30 88,6 C 88,-14 76,-24 62,-24 L 40,-6 Z" fill="#2c2650"/>'
            '<rect x="-50" y="-34" width="18" height="20" rx="5" fill="#0a0818"/><rect x="32" y="-34" width="18" height="20" rx="5" fill="#0a0818"/>'
            '<path d="M -44,32 C -54,0 -48,-46 -22,-62 C -8,-70 8,-70 22,-62 C 48,-46 54,0 44,32 C 28,42 -28,42 -44,32 Z" fill="#241f44"/>'
            '<path d="M 22,-62 C 48,-46 54,0 44,32" fill="none" stroke="#a8a2f0" stroke-width="2.4" opacity=".75"/>'
            '<path d="M 62,-24 C 76,-24 88,-14 88,6 C 86,30 70,40 48,40" fill="none" stroke="#8e88d8" stroke-width="2" opacity=".6"/>'
            '<rect x="-40" y="330" width="34" height="140" fill="#1e1a3a"/><rect x="6" y="330" width="34" height="140" fill="#1e1a3a"/></g></g>')

def ab_card():
    o = ['<rect width="540" height="960" fill="#140f22"/>', '<rect width="540" height="960" fill="url(#vig)"/>']
    o.append('<text x="270" y="300" class="q">คนที่แอบส่องอยู่คือใคร?</text><text x="270" y="334" class="qe">Who is watching from the window?</text>')
    for i, (lt, th, en) in enumerate((('A', 'คนร้ายตัวจริง', 'The real criminal'), ('B', 'อีกหนึ่งเซอร์ไพรส์', 'Another surprise'))):
        y = 420 + i * 130; on = i == 0
        o.append(f'<rect x="70" y="{y}" width="400" height="100" rx="18" fill="{"#3a2a5e" if on else "#221a36"}" stroke="{"#c9a8ff" if on else "#5a4a7a"}" stroke-width="{3 if on else 1.5}"/>'
                 f'<circle cx="124" cy="{y+50}" r="26" fill="{"#c9a8ff" if on else "#4a3a6a"}"/><text x="124" y="{y+60}" class="abl">{lt}</text>'
                 f'<text x="172" y="{y+46}" class="abt">{th}</text><text x="172" y="{y+72}" class="abe">{en}</text>')
    o.append('<text x="270" y="760" class="qe">ตอบในคอมเมนต์ · Answer in the comments</text>')
    return ''.join(o)

# ---------------- shots ----------------
WIN = (92, 230, 448, 560)
SHOTS = [
 ('1A', 'ฉาก 1 · สถานี', P('ton', 420, 650, 230) + P('moo', 120, 670, 210) + P('hero_cop', 270, 830, 380),
  'เดิมทีผมเป็นตำรวจสายสืบ\nชีวิตของผมแทบไม่เคยมีวันหยุด', 'I used to be a detective.\nMy life had almost no days off.', 'เปิดเรื่องที่ห้องนักสืบ พระเอกในเครื่องแบบ หมูกับต้นทำงานอยู่ด้านหลัง กล้องค่อย ๆ ดันเข้า'),
 ('1B', 'ฉาก 1 · ย้อนอดีต', P('hero_cop', 260, 760, 300, 'back'),
  'จนกระทั่งวันหนึ่ง ผมประสบอุบัติเหตุ\nระหว่างไล่จับคนร้าย', 'Until one day, I had an accident\nwhile chasing a suspect.', 'หันหลังวิ่งไล่เข้าซอย โทนอุ่นซีดแบบความทรงจำ ตัดด้วยซูมเบลอพร้อมเสียงวูบ'),
 ('1C', 'ฉาก 1 · โรงพยาบาล', P('heroine', 150, 820, 330) + P('hero', 330, 840, 370),
  'ทำให้ขาหักและต้องพักรักษาตัว\nอยู่บ้านเป็นเวลาสองเดือน', 'I broke my leg and had to rest\nat home for two months.', 'พระเอกเข้าเฝือกถือไม้ค้ำยัน แฟนมาเยี่ยม ดอกไม้กับการ์ดบนโต๊ะข้างเตียง'),
 ('1D', 'ฉาก 1 · บ้าน', P('hero', 130, 840, 360) + P('heroine', 340, 880, 430),
  'ก็ดีแล้วไง จะได้พักบ้าง\nทำแต่งานอยู่นั่นแหละ', '"Good. You finally get to rest.\nAll you ever do is work."', 'แฟนพูด กล้องอยู่ที่แฟน ระยะใกล้กว่า พระเอกฟังอยู่ด้านซ้าย ทำหน้าเบื่อ'),
 ('2A', 'ฉาก 2 · ห้องนั่งเล่นชั้นสอง', P('hero', 300, 760, 300),
  'ตอนแรกผมก็คิดแบบนั้นเหมือนกัน…\nแต่ผมคิดผิด', 'At first, I thought so too...\nbut I was wrong.', 'พระเอกยืนกลางห้อง เว้นจังหวะเงียบก่อน "แต่ผมคิดผิด"'),
 ('2A', 'ฉาก 2 · ห้องนั่งเล่นชั้นสอง', P('hero', 300, 640, 220, 'back'),
  'สำหรับคนอย่างผม\nมันแทบจะเป็นการลงโทษ', 'For someone like me,\nit felt like a punishment.', 'หันหลังมองออกหน้าต่าง ถือแก้วกาแฟ'),
 ('2B', 'ฉาก 2 · หน้าต่าง', P('husband', 236, 612, 92) + P('wife', 288, 612, 84),
  'รถขนของคันหนึ่ง\nก็เข้ามาจอดที่บ้านตรงข้าม', 'A moving truck pulled up\nat the house across the street.', 'มุมมองพระเอก สามีภรรยาตัวเล็กยืนหน้าบ้าน'),
 ('3A', 'ฉาก 3 · เช้า', P('wife', 120, 606, 96),
  'ภรรยาชอบออกมารดน้ำต้นไม้ทุกเช้า\nส่วนสามีมักจะกลับบ้านตอนสองทุ่ม', 'The wife watered the plants every morning.\nThe husband came home at eight.', 'ภรรยารดน้ำพุ่มกุหลาบ ป้าย "วันที่ 3 · 07:00"'),
 ('3B', 'ฉาก 3 · คืนวันศุกร์', '',
  'แต่ในคืนวันศุกร์\nผมเห็นทั้งคู่ทะเลาะกันอย่างรุนแรง', 'But on Friday night,\nI saw them fight violently.', 'มุมกว้างจากหน้าต่างก่อนซูมเข้า'),
 ('3C', 'ฉาก 3 · ระยะใกล้', clip(WIN, P('wife', 190, 600, 300, sil=True) + P('husband', 360, 610, 330, sil=True)),
  '', '', 'ละครเงา: ภรรยาปาแก้วไวน์ลงพื้น สามีเดินมาปิดม่าน เสียงแก้วแตกโดยไม่มี VO'),
 ('3D', 'ฉาก 3 · ไฟดับ', '',
  'นับตั้งแต่คืนนั้น\nผมก็ไม่เคยเห็นภรรยาของเขาอีกเลย', 'Since that night,\nI never saw his wife again.', 'ไฟดับ เงียบสั้น ๆ แล้ว VO'),
 ('4', 'ฉาก 4 · 02:00', P('husband', 380, 612, 96) + bag(410, 612, 1.1),
  'ตีสอง ผมเห็นผู้ชายบ้านตรงข้าม\nลากถุงดำขนาดใหญ่ขึ้นท้ายรถ', 'At 2 a.m., I saw the man across the street\ndrag a huge black bag into his car.', 'ไฟถนนวงเดียว สามีลากถุงไปท้ายรถ'),
 ('1D', 'ฉาก 4 · บ้าน', P('ton', 120, 840, 420) + P('moo', 320, 890, 400),
  'กูเช็กให้แล้ว ไม่มีอะไรหรอกมึง\nพักผ่อนบ้างเหอะ', '"I checked. It\'s nothing, man.\nGet some rest."', 'หมูพูด เคี้ยวหมูปิ้ง ต้นยืนยักคิ้วข้างหลัง'),
 ('4', 'ฉาก 4 · หน้าต่าง', P('husband', 300, 622, 120),
  'ผู้ชายคนนั้นเงยหน้าขึ้นมามองผม\nแล้วค่อย ๆ ยิ้มให้', 'The man looked up at me...\nand slowly smiled.', 'ซูมช้าเข้าหาสามี ดนตรีเงียบ แล้วกล้องสั่นเบา ๆ'),
 ('5A', 'ฉาก 5 · ห้องสืบสวน', P('hero', 300, 800, 340),
  'ห้องนั่งเล่นชั้นสองของผม\nเริ่มกลายเป็นห้องสืบสวนขนาดย่อม', 'My upstairs living room\nturned into a small investigation room.', 'บอร์ดรูปโยงด้ายแดง กล้องบนขาตั้ง'),
 ('5B', 'ฉาก 5 · 02:47', '',
  'จนกระทั่งคืนหนึ่ง ผมได้รับข้อความ\nจากเบอร์ที่ไม่รู้จัก', 'Then one night, I got a message\nfrom an unknown number.', 'มองจากบนลงโต๊ะ ข้อความขึ้นทีละบรรทัด'),
 ('5C', 'ฉาก 5 · ระยะใกล้', '',
  'ผมเห็นเงาผู้หญิงคนหนึ่ง\nกำลังทุบกระจกหน้าต่าง', 'I saw a woman\'s shadow\npounding on the window.', 'มือจากความมืดดึงเธอกลับ กล้องสั่นพร้อมเสียงทุ้ม'),
 ('5A', 'ฉาก 6 · ห้องสืบสวน', P('heroine', 140, 800, 320) + P('hero', 340, 880, 430),
  'เธอ ฟังเค้าก่อนดิ\nเค้าว่ามันมีคนโดนฆ่าจริง ๆ นะ', '"Babe, listen to me.\nI think someone really got killed."', 'พระเอกพูด กล้องอยู่ที่พระเอก แฟนกอดอก'),
 ('5A', 'ฉาก 6 · ห้องสืบสวน', P('heroine', 300, 840, 420) + P('hero', 90, 1010, 560, 'back', shadow=False),
  'อะ งั้นเดี๋ยวเค้าไปถามให้\nจะได้เลิกคิดมากสักที', '"Fine, I\'ll go ask them myself.\nThen you can stop overthinking."', 'แฟนพูด ข้ามไหล่พระเอก'),
 ('6A', 'ฉาก 6 · ถนน', P('heroine', 260, 742, 170, 'back'),
  'ผมมองเธอเดินข้ามถนน\nไปยังบ้านหลังนั้น', 'I watched her cross the street\nto that house.', 'แฟนเดินออกจากเฟรมไปทางบ้านตรงข้าม'),
 ('6C', 'ฉาก 6 · ระยะใกล้', clip(WIN, P('heroine', 210, 590, 290, sil=True) + P('husband', 340, 600, 320, sil=True)),
  'เงาของทั้งคู่\nดูเหมือนกำลังต่อสู้กัน', 'Their shadows looked like\nthey were struggling.', 'ละครเงาบนผ้าม่าน เงาแฟนล้มลง เสียงร้อง แล้วตัดไปไฟดับ'),
 ('7A', 'ฉาก 7 · บันได', P('hero', 270, 760, 340, 'back'),
  'ผมรีบคว้าไม้ค้ำยัน\nพยายามเดินลงบันได', 'I grabbed my crutches\nand struggled down the stairs.', 'มองจากหัวบันได พระเอกหันหลังลงไปในความมืด'),
 ('7B', 'ฉาก 7 · ประตู', P('hero', 270, 980, 520, 'back', shadow=False),
  'ประตูหน้าบ้านเปิดแง้มอยู่\nภายในมืดสนิท', 'The front door was ajar.\nIt was pitch black inside.', 'ข้ามไหล่พระเอก เว้นจังหวะเงียบก่อนผลักประตู'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', O('dad', 70, 700, 260) + O('mom', 130, 712, 240) + P('ton', 420, 700, 300) + P('moo', 470, 716, 250)
  + P('husband', 190, 690, 270) + P('wife', 360, 690, 250) + O('friend', 300, 740, 280) + P('heroine', 250, 820, 340),
  'เซอร์ไพรส์!!!', '"SURPRISE!!!"', 'ไฟเปิดพร้อมกัน ทุกคนพูดพร้อมกัน แฟนยืนหน้าสุดถือเค้ก'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', P('hero', 270, 900, 470),
  'เชี่ย… อะไรวะเนี่ย!', '"What the... what is this?!"', 'พระเอกพูด หน้าตกใจ ระยะใกล้'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', P('heroine', 270, 880, 450),
  'ก็เห็นบ่นทุกวันว่าเบื่อ\nเค้าเลยหาคดีมาให้ทำไง', '"You kept saying you were bored,\nso I found you a case."', 'แฟนพูด หัวเราะ'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', P('hero', 270, 900, 470),
  'ทีหลังซื้อหนังสือเกมจับผิดภาพให้ก็พอนะ\nขอร้อง', '"Next time, just buy me\na spot-the-difference book. Please."', 'พระเอกพูด ทุกคนหัวเราะ'),
 ('8A', 'ฉาก 8 · ผู้เฝ้ามอง', '',
  'ตลอดชีวิตการทำงาน\nผมภูมิใจมาตลอดว่าตัวเองเป็นคนช่างสังเกต', 'All my career, I was proud\nof how observant I was.', 'กล้องถอยออกจากหน้าต่างงานเลี้ยง เสียงหัวเราะจางลง'),
 ('8B', 'ฉาก 8 · ผู้เฝ้ามอง', hooded_back(270, 920, 560),
  'ในขณะที่ผมกำลังเฝ้ามองคนอื่น\nมีใครกำลังเฝ้ามองผมอยู่เหมือนกันหรือเปล่า?', 'While I was watching others...\nwas someone watching me too?', 'บุคคลปริศนาหันหลังใส่ฮู้ดยกกล้องส่องทางไกล แล้วตัดดำทันที'),
 ('AB', 'การ์ดคำถาม', '', '', '', 'ไฮไลต์สลับ A/B พร้อมเสียงคลิก ไม่เฉลย แล้วต่อด้วยโลโก้ปิดท้าย'),
]

cards = []
for n, (sid, tg, chars, th, en, note) in enumerate(SHOTS, 1):
    if sid == 'AB':
        inner = ab_card() + watermark()
        svg = f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
    else:
        body = SC[sid] + chars
        svg = frame_svg_inner(body).replace('</svg>', tag(tg) + watermark() + subs(th, en) + '</svg>')
    cards.append(f'<figure><div class="fr">{svg}</div><figcaption><b>{n:02d}</b> <i>{sid}</i> {html.escape(note)}</figcaption></figure>')

page = f'''<title>บ้านตรงข้าม สตอรีบอร์ด</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: shot grid in story order, 4 per row on desktop, 2 on phones. Dark page so the low-key frames read true. */
:root {{ --bg:#120e1c; --ink:#e6e0f2; --muted:#9a90b8; --line:#2a2440; --accent:#c9a8ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }} header p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.6; max-width:85ch; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:18px; }}
figure {{ margin:0; display:grid; gap:6px; min-width:0; }}
.fr {{ border-radius:6px; overflow:hidden; box-shadow:0 0 0 1px var(--line); }}
.fr svg {{ display:block; width:100%; height:auto; }}
figcaption {{ font-size:12px; color:var(--muted); line-height:1.5; }} figcaption b {{ color:var(--accent); font-weight:500; }} figcaption i {{ font-style:normal; color:var(--ink); margin:0 4px; }}
.th {{ font-family:"IBM Plex Sans Thai",sans-serif; font-weight:700; font-size:20px; fill:#ffd84a; stroke:#1a1020; stroke-width:4.5px; paint-order:stroke; text-anchor:middle; }}
.en {{ font-family:Inter,sans-serif; font-size:13px; fill:#ffffff; stroke:#1a1020; stroke-width:3px; paint-order:stroke; text-anchor:middle; }}
.tag {{ font-family:"IBM Plex Sans Thai",sans-serif; font-size:14px; fill:#efe6ff; text-anchor:middle; }}
.q {{ font-family:"IBM Plex Sans Thai",sans-serif; font-weight:700; font-size:30px; fill:#ffffff; text-anchor:middle; }}
.qe {{ font-family:Inter,sans-serif; font-size:14px; fill:#b8acd8; text-anchor:middle; }}
.abl {{ font-family:Inter,sans-serif; font-weight:700; font-size:26px; fill:#140f22; text-anchor:middle; }}
.abt {{ font-family:"IBM Plex Sans Thai",sans-serif; font-weight:700; font-size:24px; fill:#ffffff; }}
.abe {{ font-family:Inter,sans-serif; font-size:13px; fill:#b8acd8; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&family=Inter:wght@400;700&display=swap">
{SG["DEFS"]}
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="sbBlur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="sbSil" x="-10%" y="-10%" width="120%" height="120%"><feFlood flood-color="#1e1216"/><feComposite in2="SourceAlpha" operator="in"/><feGaussianBlur stdDeviation="2.5"/></filter>
{TG["HEAD_DEFS"]}{OG["DEFS"]}
</defs></svg>
<div class="wrap"><header><h1>บ้านตรงข้าม · สตอรีบอร์ด ({len(SHOTS)} ช็อต)</h1>
<p>เรียงตามบท · ตัวละครใช้มุมหน้าและมุมหลังเท่านั้น · ช็อตที่มีบทพูด กล้องอยู่ที่คนพูด · ช็อตหน้าต่างเป็นละครเงา · ซับไทยสีเหลืองกับซับอังกฤษอยู่ช่วง 74% ของความสูง · ใต้ภาพแต่ละช็อตคือหมายเหตุการกำกับ</p></header>
<div class="grid">{"".join(cards)}</div></div>'''
open('storyboard.html', 'w', encoding='utf-8').write(page)
print('shots', len(SHOTS))
