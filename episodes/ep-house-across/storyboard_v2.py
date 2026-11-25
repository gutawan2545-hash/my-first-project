#!/usr/bin/env python3
"""บ้านตรงข้าม: สตอรีบอร์ดพร้อมตัวละคร v2
ทุกตัวละครวางด้วยความสูงจริง (เมตร) ตามเปอร์สเปกทีฟของห้อง ห้องและเฟอร์นิเจอร์ใช้หน่วยเดียวกัน
ฉากจาก scenes.py · ตัวละครจาก characters/house-across (หน้า/หลังเท่านั้น) · ซับไทยเหลือง + อังกฤษขาวที่ y ~712
รัน: python3 storyboard.py -> storyboard.html"""
import os, runpy, html, math

HERE = os.path.dirname(os.path.abspath(__file__))
CHAR = os.path.join(HERE, '..', '..', 'characters', 'house-across')

os.chdir(HERE); SG = runpy.run_path('scenes.py')
SC = {sid: body for sid, _, _, body in SG['S']}
frame_svg_inner, Room, sil = SG['frame_svg'], SG['Room'], SG['sil']
os.chdir(CHAR); TG = runpy.run_path('turnaround.py'); OG = runpy.run_path('others.py')
os.chdir(HERE)
C, FH = TG['C'], TG['FRONT_HEAD']
front_view, back_view = TG['front_view'], TG['back_view']

C['hero_cop'] = dict(C['hero'], top='uniform', tc=('#8a6c4a', '#a38563', '#6a5136'), bot=('#7a5e40', '#92755a', '#5c452e'),
                     shoe='#15151a', cast=False, crutch=False)
C['hero_sit'] = dict(C['hero'], crutch=False)
FH['hero_cop'] = FH['hero_sit'] = FH['hero']

# real heights (m)
HM = dict(hero=1.78, hero_cop=1.78, hero_sit=1.78, heroine=1.62, moo=1.66, ton=1.85, husband=1.78, wife=1.60, dad=1.70, mom=1.57, friend=1.70)

def tfig(key, view='front'):
    c = C[key]
    body = front_view(key) if view == 'front' else back_view(key)
    grp = f'<g transform="translate(200,{c["ty"]}) scale({c["sc"]})">{body}</g>'
    return grp, c['ty'] + (c['foot'] + 16) * c['sc'], c['ty'] - 70 * c['sc']

def ofig(name):
    body, ty, sc, feet = {'dad': (OG['dd_body'], 176, 1.15, 482), 'mom': (OG['mm_body'], 182, 1.1, 484), 'friend': (OG['fr_body'], 170, 1.2, 482)}[name]
    return OG['figure'](body, ty, sc), ty + feet * sc, ty - 64 * sc

_n = [0]
def put(fig, x, feet_y, height, shadow=True, clip_y=None, clip_x=None):
    grp, f, t = fig
    k = height / (f - t)
    tr = f'translate({x - 200*k:.1f},{feet_y - f*k:.1f}) scale({k:.4f})'
    sh = f'<ellipse cx="{x:.0f}" cy="{feet_y:.0f}" rx="{height*.17:.0f}" ry="{height*.025:.0f}" fill="#120a14" opacity=".5" filter="url(#sbBlur)"/>' if shadow and clip_y is None else ''
    g = f'<g transform="{tr}">{grp}</g>'
    if clip_y is not None or clip_x is not None:
        _n[0] += 1; i = f'sbk{_n[0]}'
        x0, x1 = clip_x or (-200, 800)
        g = f'<clipPath id="{i}"><rect x="{x0}" y="-200" width="{x1-x0}" height="{(clip_y if clip_y is not None else 1200)+200}"/></clipPath><g clip-path="url(#{i})">{g}</g>'
    return sh + g

def fig_of(key, view):
    return ofig(key) if key in ('dad', 'mom', 'friend') else tfig(key, view)

# ---- placement by real size ----
ROOM = {  # (vp, x0, y0, x1, y1, ceiling metres)
    '1A': ((270, 420), 110, 220, 430, 560, 3.0), '1C': ((290, 430), 130, 230, 450, 560, 2.8),
    '2A': ((280, 430), 120, 220, 440, 570, 3.2), '5A': ((280, 430), 120, 220, 440, 570, 3.2),
    '7C': ((280, 440), 110, 250, 450, 590, 3.0), '1B': ((270, 470), 208, 300, 332, 552, 11.7),
    '7B': ((270, 470), 120, 170, 420, 760, 2.34),
}
def RP(key, sid, s, u, view='front', **kw):
    vp, x0, y0, x1, y1, ceil = ROOM[sid]
    R = Room(vp, x0, y0, x1, y1)
    x, y = R.P('F', s, u)
    return put(fig_of(key, view), x, y, HM[key] / ceil * (y1 - y0) * s, **kw)

def room_y(sid, s, h_frac):
    """screen y of a point h_frac of the ceiling height above the floor at depth s (for clipping behind furniture)"""
    vp, x0, y0, x1, y1, ceil = ROOM[sid]
    R = Room(vp, x0, y0, x1, y1)
    return R.P('F', s, .5)[1] - (y1 - y0) * s * h_frac

def EP(key, x, y, view='front', **kw):     # 1D entry hall: door 2.2 m = 600 px at y 820, floor vanishes at y 664
    ppm = 272 * (y - 664.4) / 155.6
    return put(fig_of(key, view), x, y, HM[key] * ppm, **kw)

def WP(key, x, y, view='front', hor=484, ref=(548, 40), **kw):   # street seen through the window: 40 px/m at the house
    ppm = ref[1] * (y - hor) / (ref[0] - hor)
    return put(fig_of(key, view), x, y, HM[key] * ppm, **kw)

def seated_back(key, x, hip_y, ppm):
    """character seen from behind sitting on a bench: body clipped just below the hips"""
    h = HM[key] * ppm
    grp, f, t = tfig(key, 'back')
    k = h / (f - t)
    feet_y = hip_y + .47 * h
    return put((grp, f, t), x, feet_y, h, shadow=False, clip_y=hip_y + .03 * h) + \
        f'<ellipse cx="{x}" cy="{hip_y+.03*h:.0f}" rx="{.16*h:.0f}" ry="{.02*h:.0f}" fill="#120a14" opacity=".45" filter="url(#sbBlur)"/>'

def zoom(cx, cy, z, inner):
    return f'<g transform="translate({cx},{cy}) scale({z}) translate({-cx},{-cy})">{inner}</g>'

# ---- silhouettes for the shadow play ----
WIFE = dict(h=1.60, fem=True, dress=True, hair='half')
HUSB = dict(h=1.78, hair='slick')
GIRL = dict(h=1.62, fem=True, hair='bob')

def sw_sil(x, sp, ppm=275):
    X0, Y0, X1, Y1 = SG['SHADOW_WIN']
    return sil(x, Y1 + .9 * 250, ppm, sp)

def hand_pos(x, y, ppm, sp, side):
    """screen position of a silhouette's hand (same maths as sil) for the glass cracks"""
    k = sp.get('h', 1.7) / 1.7; sw = .19 if sp.get('fem') else .235; sx = -1 if side == 'L' else 1
    a1, a2 = sp[side]; r1, r2 = math.radians(a1), math.radians(a2)
    hx = sx * (sw - .035) + .29 * math.sin(r1) + .26 * math.sin(r2) + .05 * math.sin(r2)
    hy = -.47 + .29 * math.cos(r1) + .26 * math.cos(r2) + .1 * math.cos(r2)
    L = math.radians(sp.get('lean', 0)); rx = hx * math.cos(L) - hy * math.sin(L); ry = hx * math.sin(L) + hy * math.cos(L)
    s = ppm * k
    return (x + rx * s, y - .88 * ppm * k + ry * s)

# ---- the watcher: seated in a wooden chair, back to camera, hood up, binoculars raised (no face, hair or hands) ----
def watcher(x, seat_y, ppm):
    hood, hood_dk, rim, chair, chair_dk = '#2e2852', '#1e1a38', '#9a94e0', '#5a3a28', '#3e261a'
    b = (f'<ellipse cx="0" cy=".46" rx=".42" ry=".05" fill="#05030a" opacity=".6"/>'
         # arms raised to the binoculars: upper arms out to the elbows, forearms in behind the hood
         f'<path d="M -.2,-.54 L -.36,-.66 L -.12,-.8" fill="none" stroke="{hood}" stroke-width=".14" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="M .2,-.54 L .36,-.66 L .12,-.8" fill="none" stroke="{hood}" stroke-width=".14" stroke-linecap="round" stroke-linejoin="round"/>'
         f'<path d="M -.42,-.7 L -.36,-.6 M .42,-.7 L .36,-.6" stroke="{rim}" stroke-width=".018" opacity=".7"/>'
         f'<rect x="-.17" y="-.88" width=".07" height=".1" rx=".02" fill="#0c0a12"/><rect x=".1" y="-.88" width=".07" height=".1" rx=".02" fill="#0c0a12"/>'
         # torso (baggy hoodie), hem band, seat of the trousers
         f'<path d="M -.27,0 C -.3,-.28 -.29,-.48 -.22,-.58 C -.12,-.65 .12,-.65 .22,-.58 C .29,-.48 .3,-.28 .27,0 Z" fill="{hood}"/>'
         f'<path d="M .22,-.58 C .29,-.48 .3,-.28 .27,0 L .17,0 C .2,-.28 .2,-.46 .16,-.56 Z" fill="{hood_dk}"/>'
         f'<rect x="-.27" y="-.06" width=".54" height=".07" rx=".02" fill="{hood_dk}"/>'
         f'<path d="M -.04,-.6 C -.06,-.4 -.05,-.2 -.04,0" fill="none" stroke="{hood_dk}" stroke-width=".012"/>'
         # hood up
         f'<path d="M -.16,-.58 C -.22,-.74 -.17,-.93 0,-.96 C .17,-.93 .22,-.74 .16,-.58 C .08,-.55 -.08,-.55 -.16,-.58 Z" fill="{hood}"/>'
         f'<path d="M .0,-.96 C .17,-.93 .22,-.74 .16,-.58 C .12,-.57 .1,-.57 .08,-.57 C .13,-.7 .1,-.88 0,-.96 Z" fill="{hood_dk}"/>'
         f'<path d="M 0,-.95 C -.01,-.82 -.01,-.68 0,-.57" fill="none" stroke="{hood_dk}" stroke-width=".012"/>'
         f'<path d="M -.17,-.62 C -.21,-.76 -.16,-.92 0,-.95 C .16,-.92 .21,-.76 .17,-.62" fill="none" stroke="{rim}" stroke-width=".02" opacity=".8"/>'
         f'<path d="M -.22,-.58 C -.27,-.52 -.29,-.4 -.29,-.3 M .22,-.58 C .27,-.52 .29,-.4 .29,-.3" fill="none" stroke="{rim}" stroke-width=".016" opacity=".55"/>'
         # wooden chair in front of the body: seat edge, back posts, two rails, legs
         f'<rect x="-.25" y="0" width=".5" height=".05" rx=".01" fill="{chair}"/><rect x="-.25" y=".05" width=".5" height=".02" fill="{chair_dk}"/>'
         f'<rect x="-.24" y="-.44" width=".04" height=".9" fill="{chair}"/><rect x=".2" y="-.44" width=".04" height=".9" fill="{chair_dk}"/>'
         f'<path d="M -.25,-.44 C -.1,-.48 .1,-.48 .25,-.44 L .25,-.37 C .1,-.41 -.1,-.41 -.25,-.37 Z" fill="{chair}"/>'
         f'<rect x="-.22" y="-.22" width=".44" height=".035" fill="{chair_dk}"/>'
         f'<rect x="-.19" y=".07" width=".03" height=".38" fill="{chair_dk}"/><rect x=".16" y=".07" width=".03" height=".38" fill="{chair_dk}"/>'
         f'<path d="M -.25,-.44 C -.1,-.48 .1,-.48 .25,-.44" fill="none" stroke="#a07a5a" stroke-width=".01"/>')
    return f'<g transform="translate({x},{seat_y}) scale({ppm})">{b}</g>'

# ---- overlay helpers ----
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

def ab_card():
    o = ['<rect width="540" height="960" fill="#140f22"/>']
    o.append('<text x="270" y="300" class="q">คนที่แอบส่องอยู่คือใคร?</text><text x="270" y="334" class="qe">Who is watching from the window?</text>')
    for i, (lt, th, en) in enumerate((('A', 'คนร้ายตัวจริง', 'The real criminal'), ('B', 'อีกหนึ่งเซอร์ไพรส์', 'Another surprise'))):
        y = 420 + i * 130; on = i == 0
        o.append(f'<rect x="70" y="{y}" width="400" height="100" rx="18" fill="{"#3a2a5e" if on else "#221a36"}" stroke="{"#c9a8ff" if on else "#5a4a7a"}" stroke-width="{3 if on else 1.5}"/>'
                 f'<circle cx="124" cy="{y+50}" r="26" fill="{"#c9a8ff" if on else "#4a3a6a"}"/><text x="124" y="{y+60}" class="abl">{lt}</text>'
                 f'<text x="172" y="{y+46}" class="abt">{th}</text><text x="172" y="{y+72}" class="abe">{en}</text>')
    o.append('<text x="270" y="760" class="qe">ตอบในคอมเมนต์ · Answer in the comments</text>')
    return ''.join(o)

# ---------------- custom bodies ----------------
SEAT = SG['WATCH_SEAT_Y']
# 3C: wife hurls the wine glass, husband points at her
s3c = (sw_sil(185, dict(WIFE, lean=7, tilt=6, L=(-158, -172), handL='glass', R=(35, 75))) +
       sw_sil(360, dict(HUSB, lean=-6, tilt=-4, L=(-82, -88), handL='point', R=(28, -35))) +
       ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#24121a"/>' for x, y, r in ((128, 268, 4), (114, 290, 3), (140, 252, 2.5), (106, 312, 2))))
# 6C: the husband grabs her shoulders, she pushes him off
s6c = (sw_sil(205, dict(GIRL, lean=-14, tilt=-12, L=(-140, -168), handL='open', R=(72, 92), handR='open')) +
       sw_sil(345, dict(HUSB, lean=-9, L=(-62, -92), R=(-48, -80))))
# 5C: woman presses both palms on the glass, an arm from the dark grabs her shoulder
X0, Y0, X1, Y1 = SG['POUND_WIN']
PW = dict(WIFE, lean=-3, tilt=8, L=(-152, -176), handL='open', R=(154, 178), handR='open')
pw_feet, pw_ppm = (262, 905), 300
s5c = sil(pw_feet[0], pw_feet[1], pw_ppm, PW) + f'<path d="M {X1+10},{Y0+170} C {X1-50},{Y0+190} 360,{Y0+250} 318,{Y0+262} L 322,{Y0+284} C 368,{Y0+276} {X1-40},{Y0+226} {X1+10},{Y0+222} Z" fill="#0c0608"/>'
cracks = [hand_pos(*pw_feet, pw_ppm, PW, 'L')]
SC['3C*'] = SG['shadow_window']('closed', s3c)
SC['6C*'] = SG['shadow_window']('closed', s6c)
SC['5C*'] = SG['pound_window2'](s5c, cracks)

pj = SG['stairs_pj']
ft, hd = pj(0, 1.62, 2.3), pj(0, 1.62 + 1.78, 2.3)
hero_stairs = put(tfig('hero', 'front'), ft[0], ft[1], ft[1] - hd[1])

# ---------------- shots ----------------
SHOTS = [
 ('1A', 'ฉาก 1 · สถานี', RP('ton', '1A', 1.15, .2, clip_y=room_y('1A', 1.51, .21)) + RP('moo', '1A', 1.15, .8, clip_y=room_y('1A', 1.51, .21)) + RP('hero_cop', '1A', 2.6, .5),
  'เดิมทีผมเป็นตำรวจสายสืบ\nชีวิตของผมแทบไม่เคยมีวันหยุด', 'I used to be a detective.\nMy life had almost no days off.', 'เปิดเรื่องที่ห้องนักสืบ พระเอกยืนในทางเดินกลางห้อง หมูกับต้นยืนหลังโต๊ะแถวหลัง กล้องค่อย ๆ ดันเข้า'),
 ('1B', 'ฉาก 1 · ย้อนอดีต', RP('hero_cop', '1B', 3.3, .45, 'back'),
  'จนกระทั่งวันหนึ่ง ผมประสบอุบัติเหตุ\nระหว่างไล่จับคนร้าย', 'Until one day, I had an accident\nwhile chasing a suspect.', 'หันหลังวิ่งไล่เข้าซอย ตัวขนาดจริงเทียบกับตึกแถว โทนอุ่นซีดแบบความทรงจำ ตัดด้วยซูมเบลอพร้อมเสียงวูบ'),
 ('1C', 'ฉาก 1 · โรงพยาบาล', RP('heroine', '1C', 2.3, .76) + RP('hero', '1C', 2.45, .36),
  'ทำให้ขาหักและต้องพักรักษาตัว\nอยู่บ้านเป็นเวลาสองเดือน', 'I broke my leg and had to rest\nat home for two months.', 'พระเอกเข้าเฝือกยืนปลายเตียง แฟนมาเยี่ยมยืนหน้าเก้าอี้เยี่ยม'),
 ('1D', 'ฉาก 1 · บ้าน', EP('hero', 140, 846) + EP('heroine', 370, 884),
  'ก็ดีแล้วไง จะได้พักบ้าง\nทำแต่งานอยู่นั่นแหละ', '"Good. You finally get to rest.\nAll you ever do is work."', 'แฟนพูด กล้องอยู่ที่แฟน ยืนใกล้กล้องกว่า พระเอกฟังอยู่ข้างประตู ทำหน้าเบื่อ'),
 ('2A', 'ฉาก 2 · ห้องนั่งเล่นชั้นสอง', RP('hero', '2A', 2.15, .3),
  'ตอนแรกผมก็คิดแบบนั้นเหมือนกัน…\nแต่ผมคิดผิด', 'At first, I thought so too...\nbut I was wrong.', 'พระเอกยืนข้างโต๊ะกลาง เว้นจังหวะเงียบก่อน "แต่ผมคิดผิด"'),
 ('2A', 'ฉาก 2 · ห้องนั่งเล่นชั้นสอง', RP('hero', '2A', 1.2, .5, 'back'),
  'สำหรับคนอย่างผม\nมันแทบจะเป็นการลงโทษ', 'For someone like me,\nit felt like a punishment.', 'หันหลังยืนหน้าหน้าต่าง มองออกไปข้างนอก'),
 ('2B', 'ฉาก 2 · หน้าต่าง', WP('husband', 262, 548) + WP('wife', 345, 548) + seated_back('hero_sit', 440, SEAT - 6, 270),
  'รถขนของคันหนึ่ง\nก็เข้ามาจอดที่บ้านตรงข้าม', 'A moving truck pulled up\nat the house across the street.', 'ข้ามไหล่: พระเอกนั่งบนเบาะริมหน้าต่างหันหลัง มองสามีภรรยาที่เพิ่งย้ายเข้า'),
 ('3A', 'ฉาก 3 · เช้า', WP('wife', 120, 552),
  'ภรรยาชอบออกมารดน้ำต้นไม้ทุกเช้า\nส่วนสามีมักจะกลับบ้านตอนสองทุ่ม', 'The wife watered the plants every morning.\nThe husband came home at eight.', 'มุมมองพระเอกผ่านกระจกใส ภรรยารดน้ำแปลงดอกไม้ ป้าย "วันที่ 3 · 07:00"'),
 ('3B', 'ฉาก 3 · คืนวันศุกร์', '',
  'แต่ในคืนวันศุกร์\nผมเห็นทั้งคู่ทะเลาะกันอย่างรุนแรง', 'But on Friday night,\nI saw them fight violently.', 'มุมกว้างจากหน้าต่าง ไฟห้องนั่งเล่นบ้านตรงข้ามเปิด แล้วซูมเข้า'),
 ('3C*', 'ฉาก 3 · ระยะใกล้', '',
  '', '', 'ละครเงาบนผ้าม่าน: ภรรยาเงื้อแก้วไวน์จะปา สามีชี้หน้า แล้วเสียงแก้วแตก ไม่มี VO'),
 ('3D', 'ฉาก 3 · ไฟดับ', '',
  'นับตั้งแต่คืนนั้น\nผมก็ไม่เคยเห็นภรรยาของเขาอีกเลย', 'Since that night,\nI never saw his wife again.', 'ไฟดับ เงียบสั้น ๆ แล้ว VO'),
 ('4', 'ฉาก 4 · 02:00', WP('husband', 350, 556) + bag(384, 556, 1.25) + seated_back('hero_sit', 90, SEAT - 6, 270),
  'ตีสอง ผมเห็นผู้ชายบ้านตรงข้าม\nลากถุงดำขนาดใหญ่ขึ้นท้ายรถ', 'At 2 a.m., I saw the man across the street\ndrag a huge black bag into his car.', 'ข้ามไหล่พระเอกที่นั่งเฝ้าริมหน้าต่าง ไฟถนนวงเดียว สามีลากถุงไปท้ายรถ'),
 ('1D', 'ฉาก 4 · บ้าน', EP('ton', 130, 846) + EP('moo', 372, 888),
  'กูเช็กให้แล้ว ไม่มีอะไรหรอกมึง\nพักผ่อนบ้างเหอะ', '"I checked. It\'s nothing, man.\nGet some rest."', 'หมูพูด เคี้ยวหมูปิ้ง ต้นยืนยักคิ้วข้างหลัง'),
 ('4', 'ฉาก 4 · หน้าต่าง', '@zoom', 'ผู้ชายคนนั้นเงยหน้าขึ้นมามองผม\nแล้วค่อย ๆ ยิ้มให้', 'The man looked up at me...\nand slowly smiled.', 'ซูมช้าเข้าหาสามี (ทั้งภาพขยาย ขนาดตัวกับบ้านคงสัดส่วน) ดนตรีเงียบ แล้วกล้องสั่นเบา ๆ'),
 ('5A', 'ฉาก 5 · ห้องสืบสวน', RP('hero', '5A', 2.2, .38),
  'ห้องนั่งเล่นชั้นสองของผม\nเริ่มกลายเป็นห้องสืบสวนขนาดย่อม', 'My upstairs living room\nturned into a small investigation room.', 'บอร์ดรูปโยงด้ายแดง กล้องบนขาตั้ง กระดาษเต็มพื้น'),
 ('5B', 'ฉาก 5 · 02:47', '',
  'จนกระทั่งคืนหนึ่ง ผมได้รับข้อความ\nจากเบอร์ที่ไม่รู้จัก', 'Then one night, I got a message\nfrom an unknown number.', 'มองจากบนลงโต๊ะ ข้อความขึ้นทีละบรรทัด'),
 ('5C*', 'ฉาก 5 · ระยะใกล้', '',
  'ผมเห็นเงาผู้หญิงคนหนึ่ง\nกำลังทุบกระจกหน้าต่าง', 'I saw a woman\'s shadow\npounding on the window.', 'หน้าต่างบานสูงชั้นล่าง ฝ่ามือแนบกระจกจนร้าว แขนจากความมืดดึงเธอกลับ กล้องสั่นพร้อมเสียงทุ้ม'),
 ('5A', 'ฉาก 6 · ห้องสืบสวน', RP('heroine', '5A', 1.75, .2) + RP('hero', '5A', 2.4, .66),
  'เธอ ฟังเค้าก่อนดิ\nเค้าว่ามันมีคนโดนฆ่าจริง ๆ นะ', '"Babe, listen to me.\nI think someone really got killed."', 'พระเอกพูด กล้องอยู่ที่พระเอก แฟนกอดอกฟังอยู่หลังห้อง'),
 ('5A', 'ฉาก 6 · ห้องสืบสวน', RP('heroine', '5A', 2.05, .36) + RP('hero', '5A', 3.6, .72, 'back', shadow=False),
  'อะ งั้นเดี๋ยวเค้าไปถามให้\nจะได้เลิกคิดมากสักที', '"Fine, I\'ll go ask them myself.\nThen you can stop overthinking."', 'แฟนพูด ข้ามไหล่พระเอก'),
 ('6A', 'ฉาก 6 · ถนน', WP('heroine', 262, 690, 'back', hor=495, ref=(548, 33)),
  'ผมมองเธอเดินข้ามถนน\nไปยังบ้านหลังนั้น', 'I watched her cross the street\nto that house.', 'แฟนเดินออกจากเฟรมไปทางบ้านตรงข้าม ตัวเล็กลงตามระยะ'),
 ('6C*', 'ฉาก 6 · ระยะใกล้', '',
  'เงาของทั้งคู่\nดูเหมือนกำลังต่อสู้กัน', 'Their shadows looked like\nthey were struggling.', 'ละครเงาบนผ้าม่าน สามีคว้าไหล่ แฟนดิ้นผลักออก แล้วตัดไปไฟดับ'),
 ('7A', 'ฉาก 7 · บันได', hero_stairs,
  'ผมรีบคว้าไม้ค้ำยัน\nพยายามเดินลงบันได', 'I grabbed my crutches\nand struggled down the stairs.', 'มองจากเชิงบันไดขึ้นไป พระเอกหันหน้าค่อย ๆ ลงบันไดด้วยไม้ค้ำยัน แสงจากห้องชั้นบนส่องจากด้านหลัง'),
 ('7B', 'ฉาก 7 · ประตู', RP('hero', '7B', 1.62, .8, 'back', shadow=False),
  'ประตูหน้าบ้านเปิดแง้มอยู่\nภายในมืดสนิท', 'The front door was ajar.\nIt was pitch black inside.', 'ข้ามไหล่พระเอก เว้นจังหวะเงียบก่อนผลักประตู'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', '@party',
  'เซอร์ไพรส์!!!', '"SURPRISE!!!"', 'ไฟเปิดพร้อมกัน ทุกคนยืนหลังโต๊ะเค้ก แฟนยืนหน้าสุด'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', RP('hero', '7C', 2.75, .5),
  'เชี่ย… อะไรวะเนี่ย!', '"What the... what is this?!"', 'พระเอกพูด หน้าตกใจ ระยะใกล้'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', RP('heroine', '7C', 2.75, .5),
  'ก็เห็นบ่นทุกวันว่าเบื่อ\nเค้าเลยหาคดีมาให้ทำไง', '"You kept saying you were bored,\nso I found you a case."', 'แฟนพูด หัวเราะ'),
 ('7C', 'ฉาก 7 · เซอร์ไพรส์', RP('hero', '7C', 2.75, .5),
  'ทีหลังซื้อหนังสือเกมจับผิดภาพให้ก็พอนะ\nขอร้อง', '"Next time, just buy me\na spot-the-difference book. Please."', 'พระเอกพูด ทุกคนหัวเราะ'),
 ('8A', 'ฉาก 8 · ผู้เฝ้ามอง', '',
  'ตลอดชีวิตการทำงาน\nผมภูมิใจมาตลอดว่าตัวเองเป็นคนช่างสังเกต', 'All my career, I was proud\nof how observant I was.', 'กล้องถอยออกจากหน้าต่างงานเลี้ยง เสียงหัวเราะจางลง'),
 ('8B', 'ฉาก 8 · ผู้เฝ้ามอง', watcher(270, 690, 330),
  'ในขณะที่ผมกำลังเฝ้ามองคนอื่น\nมีใครกำลังเฝ้ามองผมอยู่เหมือนกันหรือเปล่า?', 'While I was watching others...\nwas someone watching me too?', 'ห้องมืดอีกหลัง บุคคลปริศนานั่งหันหลังบนเก้าอี้ไม้ ใส่ฮู้ด ยกกล้องส่องทางไกลมองบ้านพระเอก แล้วตัดดำ'),
 ('AB', 'การ์ดคำถาม', '', '', '', 'ไฮไลต์สลับ A/B พร้อมเสียงคลิก ไม่เฉลย แล้วต่อด้วยโลโก้ปิดท้าย'),
]

# party crowd behind the cake table (clipped at the table top), heroine in front
tt = room_y('7C', 1.8, 1.5 * 52 / 160 / 3.0 * 1.0)   # table top ~ .75 m at s 1.8
tt = Room((280, 440), 110, 250, 450, 590).P('F', 1.8, .5)[1] - 52 * (1.8 * 340 / 3.0 * 1.5 / 160)
party = (RP('dad', '7C', 1.4, .2) + RP('mom', '7C', 1.4, .32) + RP('ton', '7C', 1.42, .82) + RP('moo', '7C', 1.45, .7)
         + RP('husband', '7C', 1.5, .4, clip_y=tt) + RP('wife', '7C', 1.5, .6, clip_y=tt) + RP('friend', '7C', 1.55, .5, clip_y=tt)
         + RP('heroine', '7C', 2.2, .28))

cards = []
for n, (sid, tg, chars, th, en, note) in enumerate(SHOTS, 1):
    if sid == 'AB':
        svg = f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">{ab_card() + watermark()}</svg>'
    else:
        if chars == '@zoom':
            body = zoom(350, 520, 2.2, SC['4'] + WP('husband', 350, 556))
        elif chars == '@party':
            body = SC['7C'] + party
        else:
            body = SC[sid] + chars
        svg = frame_svg_inner(body).replace('</svg>', tag(tg) + watermark() + subs(th, en) + '</svg>')
    cards.append(f'<figure><div class="fr">{svg}</div><figcaption><b>{n:02d}</b> <i>{sid.rstrip("*")}</i> {html.escape(note)}</figcaption></figure>')

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
{TG["HEAD_DEFS"]}{OG["DEFS"]}
</defs></svg>
<div class="wrap"><header><h1>บ้านตรงข้าม · สตอรีบอร์ด v2 ({len(SHOTS)} ช็อต)</h1>
<p>สเกลใหม่: ตัวละครวางด้วยความสูงจริง (พระเอก 1.78 ม. นางเอก 1.62 ม. หมู 1.66 ม. ต้น 1.85 ม.) ตามเปอร์สเปกทีฟของแต่ละห้อง เฟอร์นิเจอร์ใช้ขนาดจริงชุดเดียวกัน คนที่ยืนหลังโต๊ะถูกโต๊ะบังจริง ·
หน้าต่างพระเอกเป็นกระจกบานใหญ่ไม่มีเสากลาง มีเบาะนั่งริมหน้าต่าง · ละครเงาเป็นเงาท่าทางชัด (ปาแก้ว ชี้หน้า ดึงไหล่ ฝ่ามือแนบกระจก) · บันไดวาดใหม่แบบสามมิติ ไม่มีรูปแขวน · ป้ายร้านในซอยทำใหม่ · บุคคลปริศนานั่งหันหลังบนเก้าอี้ เห็นร่างชัด · ใต้ภาพคือหมายเหตุการกำกับ</p></header>
<div class="grid">{"".join(cards)}</div></div>'''
open('storyboard.html', 'w', encoding='utf-8').write(page)
print('shots', len(SHOTS))
