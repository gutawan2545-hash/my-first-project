"""ช่วงทดลองแอนิเมชัน (ช็อต 3-9 ฉากผู้หญิงชุดดำเปิดประตูเข้ามา)
ตัวละครมีชีวิต: กะพริบตา ขยับปากตามเสียงคนพูด หัวขยับ เดินเข้าฉาก ชี้มือ เปลี่ยนสีหน้า ตัวสั่น
เพิ่มช็อตปฏิกิริยานางเอก (คนฟังต้องมีปฏิกิริยา) · เสียงพากย์ใส่อารมณ์ · ดนตรีและเสียงประกอบสังเคราะห์
รัน: python3 anim_test.py -> anim_test.html + out/test_audio.wav แล้ว node render_anim.js แล้ว ffmpeg รวม"""
import os, sys, re, json, math, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'storyboard'))
import storyboard as SB                      # ฉาก ตัวละคร และ defs ที่ทำไว้แล้ว
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'pipeline'))
import cinelight as CL
LIGHT = not os.environ.get('NOLIGHT')
BGDIR = 'bg_lit' if LIGHT else 'bg'
if LIGHT:   # ตัวละครที่อยู่ในฉากหลังนิ่ง (แขกในห้องพิธี) ได้แสงขอบด้วย
    _put0 = SB.put
    def _put_lit(key, x, feet, s, shadow=True): return f'<g filter="url(#clRim_bg)">' + _put0(key, x, feet, s, shadow) + '</g>'
    SB.put = _put_lit
import audiolib as A
import supporting as SP
import wedding_chars as WC
sys.path.insert(0, HERE)
from subs import thai_lines, EN
os.chdir(HERE)
FPS = 24

# ---------------------------------------------------------------- หัวเจ้าบ่าวตอนโกรธ + ตัวที่แยกแขนขวาออกมาขยับได้
gh = re.search(r'<g id="ghead">.*?\n  </g>', WC.GROOM_HEAD, re.S).group(0).replace('<g id="ghead">', '<g id="ghead_angry">')
gh = gh.replace('<path d="M -23,-14.5 L -7,-11.6 L -7.4,-8.8 L -22,-11.2 Z" fill="#141218"/>', '<path d="M -23,-16.5 L -6.6,-9.4 L -7.4,-6.4 L -22,-13 Z" fill="#141218"/>')
gh = gh.replace('<path d="M 23,-14.5 L 7,-11.6 L 7.4,-8.8 L 22,-11.2 Z" fill="#141218"/>', '<path d="M 23,-16.5 L 6.6,-9.4 L 7.4,-6.4 L 22,-13 Z" fill="#141218"/>')
i = gh.index('    <!-- thin closed-mouth smirk'); j = gh.index('    <!-- neat comma hair')
gh = gh[:i] + ('    <path d="M -8,21 Q 0,19 8,21 Q 7,30 0,30 Q -7,30 -8,21 Z" fill="#5a1a22"/><path d="M -7,21.4 Q 0,19.8 7,21.4 L 6.4,23.6 Q 0,22.4 -6.4,23.6 Z" fill="#fff"/>'
               '<path d="M -8,21 Q 0,19 8,21" fill="none" stroke="#8a4a46" stroke-width="1.4"/>\n') + gh[j:]
gp = re.search(r'<g id="ghead">.*?\n  </g>', WC.GROOM_HEAD, re.S).group(0).replace('<g id="ghead">', '<g id="ghead_panic">')
gp = gp.replace('<path d="M -23,-14.5 L -7,-11.6 L -7.4,-8.8 L -22,-11.2 Z" fill="#141218"/>', '<path d="M -23,-11.5 L -7,-17.6 L -6.4,-14.6 L -22,-8.6 Z" fill="#141218"/>')
gp = gp.replace('<path d="M 23,-14.5 L 7,-11.6 L 7.4,-8.8 L 22,-11.2 Z" fill="#141218"/>', '<path d="M 23,-11.5 L 7,-17.6 L 6.4,-14.6 L 22,-8.6 Z" fill="#141218"/>')
gp = gp.replace('\n  </g>', '<path d="M 27,-24 C 31,-17 32,-13 28.5,-11 C 25,-13 25.5,-18 27,-24 Z" fill="#cfe6ff" stroke="#9cc4ee" stroke-width=".6"/>'
                '<path d="M -29,-14 C -26,-9 -26,-6 -28.5,-4.8 C -31,-6 -31,-9.5 -29,-14 Z" fill="#cfe6ff" stroke="#9cc4ee" stroke-width=".6"/>\n  </g>')
gb = WC.groom_body()
ARM_PARTS = [p for p in re.findall(r'<[^>]+/>', gb) if any(k in p for k in ('-58,226', '-59,229', 'x="-59"', 'cx="-51.5"', '-58,96'))]
for p in ARM_PARTS: gb = gb.replace(p, '', 1)
GROOM_ARM = ''.join(ARM_PARTS)

# ---------------------------------------------------------------- ชิ้นส่วนขยับได้
def blink(p, skin, ex=13, ey=-1.6, rx=10, ry=7, scale=None):
    g = (f'<g id="{p}B" display="none">' + ''.join(
        f'<ellipse cx="{s * ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="{skin}"/><path d="M {s * (ex + 9)},{ey + .5} Q {s * ex},{ey + 4} {s * (ex - 9)},{ey + .5}" fill="none" stroke="#1c1214" stroke-width="1.6" stroke-linecap="round"/>'
        for s in (-1, 1)) + '</g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
def mouth(p, skin, lip, scale=None):
    g = (f'<g id="{p}M" display="none"><ellipse cx="0" cy="24.2" rx="8.8" ry="5" fill="{skin}"/>'
         f'<ellipse id="{p}Mo" cx="0" cy="24.4" rx="4.6" ry="2" fill="#4a1420" stroke="{lip}" stroke-width="1.8"/>'
         f'<rect id="{p}Mt" x="-3" y="22.6" width="6" height="1.4" rx=".6" fill="#ffffff"/></g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
TEARS = lambda p: (f'<g id="{p}T" display="none"><path d="M -14,4 C -15,12 -13,20 -15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/>'
                   f'<path d="M 14,4 C 15,12 13,20 15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/><circle cx="-15" cy="31" r="1.8" fill="#e6f0ff"/></g>')

def bride_rig(p, heads=('b2head', 'b2head_worry', 'b2head_scared')):
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    return (f'<g id="{p}"><use href="#b2back"/>{WC.bride_body()}<g id="{p}H">{hs}{blink(p, "#fbe2cf")}{TEARS(p)}</g></g>', 462)
def woman_rig(p):
    n, nt, kind, back, head, body = SP.c_woman_black()
    sc = 'scale(.87 1.03)'
    return (f'<g id="{p}">{back}{body}<g id="{p}H">{head}{blink(p, "#f1d8cc", scale=sc)}{mouth(p, "#f1d8cc", "#8e2236", scale=sc)}</g></g>', 460)
def groom_rig(p, heads=('ghead', 'ghead_angry')):
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    return (f'<g id="{p}">{gb}<g id="{p}A">{GROOM_ARM}</g><g id="{p}H">{hs}{blink(p, "#f6dcc8", 12, -1.6, 9.6, 5.4)}'
            f'<path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="#d8d4ce" stroke-width="2"/></g></g>', 488)
def guard_rig(p):
    n, nt, kind, back, head, body = SP.c_guard()
    return (f'<g id="{p}">{back}{body}<g id="{p}H">{head}{blink(p, "#ecc4a2", 12, -1.6, 9.6, 5.4, scale="scale(.88 1.03)")}</g></g>', 488)

from rigs import bride_rig, woman_rig as _woman_rig, groom_rig, guard_rig
def woman_rig(p):
    body, lf = _woman_rig(p)
    if p in ('w22', 'w23'): body = body.replace(f'<g id="{p}H">', f'<g id="{p}H">' + PHONE_EAR, 1)
    return body, lf
PHONE_EAR = '<g transform="translate(30,6) rotate(10)"><rect x="-6" y="-20" width="14" height="34" rx="3" fill="#15131c"/><rect x="-4.4" y="-18" width="10.8" height="28" rx="2" fill="#6f7cff" opacity=".4"/></g>'

def placed(rig, x, feet, s):
    body, lf = rig
    if LIGHT: body = body.replace('class="place"', '')
    cs = CL.contact_shadow(0, lf, 1) if LIGHT else ''
    return f'<g data-lf="{lf}" data-x="{x}" data-feet="{feet}" data-s="{s}" class="place">{cs}{body}</g>'

CAST_NO = lambda *ks: {k: v for k, v in SB.CAST.items() if k not in ks}
BX, BY = SB.bx, SB.by; GX, GY = SB.gx, SB.gy
WF = SB.WB_FACE

# ---------------------------------------------------------------- เสียงพากย์และไทม์ไลน์
VO = {k: A.load_voice(os.path.join(HERE, 'vo', f'{k}.mp3')) for k in ('01c', '03c', '04c', '05c', '06e', '07g', '08c', '09e') + tuple(f'{n}f' for n in range(10, 26))}
VO['02a'] = A.load_voice(os.path.join(HERE, 'vo', '02a_t1.mp3'))
D = {k: len(v) / A.SR for k, v in VO.items()}
TB = .3 + D['04c'] - .35                  # เสียงปังตรงคำว่า "เปิดออก"
S7_SPLIT = .3 + D['07g'] + .35          # เจ้าบ่าวพูดจบในช็อตตัวเองก่อน แล้วค่อยตัดไป รปภ. เดินเข้ามา
G7_POINT = .3 + 7.9                       # เสียงตะคอก "เจ้าหน้าที่!" เริ่มที่ 7.9 วิ (ดูจากช่วงเงียบในไฟล์เสียง)            # ชี้ตอนพูดว่า "เจ้าหน้าที่ครับ"
SHOTS = [
    ('s1', .5 + D['01c'] + .9), ('s2', .4 + D['02a'] + .5), ('s3', .4 + D['03c'] + .5), ('s4', TB + 2.3), ('s4r', 1.8), ('s5', .4 + D['05c'] + .6), ('s6', .4 + D['06e'] + .5),
    ('s6r', 2.3), ('s7a', S7_SPLIT), ('s7b', 3.0), ('s8', .4 + D['08c'] + .4), ('s9', .4 + D['09e'] + .6), ('s9r', 2.6),
    ('s10', .5 + D['10f'] + .5), ('s11', .4 + D['11f'] + .5), ('s12', .4 + D['12f'] + .5), ('s13', .4 + D['13f'] + .6), ('s14', .4 + D['14f'] + .6),
    ('s15', .6 + D['15f'] + .4), ('s16', .4 + D['16f'] + .5), ('s17', .4 + D['17f'] + .9), ('s18', .4 + D['18f'] + .4), ('s19', .4 + D['19f'] + 1.0),
    ('s20', .7 + D['20f'] + 1.6), ('s21', .4 + D['21f'] + .8), ('s22', .4 + D['22f'] + .5), ('s23', .4 + D['23f'] + .7),
    ('s24', .5 + D['24f'] + 2.4), ('s25', .3 + D['25f'] + .9), ('s26', 3.6), ('s27', 9.0)]
T0 = {}; t = 0
for k, d in SHOTS: T0[k] = t; t += d
TOTAL = t
VOICE_AT = {'01c': T0['s1'] + .5, '02a': T0['s2'] + .4, **{f'{n}f': T0[f's{n}'] + (.5 if n in (10, 24) else .6 if n == 15 else .7 if n == 20 else .3 if n == 25 else .4) for n in range(10, 26)}, '03c': T0['s3'] + .4, '04c': T0['s4'] + .3, '05c': T0['s5'] + .4, '06e': T0['s6'] + .4, '07g': T0['s7a'] + .3, '08c': T0['s8'] + .4, '09e': T0['s9'] + .4}
SPEAKER = {'06e': 'w6', '09e': 'w9', '07g': 'g7', '22f': 'w22', '23f': 'w23', '25f': 'g25'}
ENV = {k: A.envelope_fps(VO[k], FPS) for k in SPEAKER}

# ---------------------------------------------------------------- ฉากแต่ละช็อต
HALL_L = CL.Light(dir=(-.55, -.8), glows=[(270, 30, 150, '#ffd2a0', .35), (85, 400, 80, '#ffb36b', .55), (440, 400, 80, '#ffb36b', .55), (300, 290, 110, '#a9bcff', .25)])
DOOR_L = CL.Light(dir=(-.75, -.5), ambient_op=.26, glows=[(175, 600, 60, '#ffb36b', .6), (365, 600, 60, '#ffb36b', .6), (270, 330, 150, '#b7c6ff', .3)])
LIGHTS = {**{k: HALL_L for k in ('s1', 's2', 's3', 's4r', 's6r', 's7a', 's9r', 's10', 's11', 's12', 's13', 's14')},
          **{k: DOOR_L for k in ('s4', 's5', 's6', 's7b', 's8', 's9')},
          **{k: CL.Light(dir=(-.3, -.4), ambient='#5a6596', ambient_op=.18, glows=[(270, 420, 150, '#9fb4ff', .35), (440, 200, 90, '#ffe0c0', .2)]) for k in ('s15', 's16', 's17', 's18', 's19')},
          's20': CL.Light(dir=(0, -1), ambient_op=.28, lowkey=.35, glows=[(270, 40, 160, '#ffd2a0', .5), (270, 800, 120, '#b7a6ff', .25)], pools=[(270, 120, 260), (270, 820, 160)]),
          's21': CL.Light(dir=(0, -1), ambient='#3a4478', ambient_op=.3, lowkey=.4, glows=[(270, 400, 170, '#9fb4ff', .4)], pools=[(270, 420, 260)]),
          **{k: CL.Light(dir=(-.8, -.3), rim_op=.85, ambient='#3a4478', ambient_op=.3, lowkey=.55, char_exp=.9, glows=[(150, 330, 120, '#ffb36b', .3), (270, 300, 200, '#7f90d0', .2)], pools=[(230, 340, 260)]) for k in ('s22', 's23')},
          's24': CL.Light(dir=(-.6, -.6), ambient='#3a4478', ambient_op=.3, lowkey=.55, glows=[(80, 270, 70, '#ffb36b', .6), (460, 270, 70, '#ffb36b', .6), (270, 742, 120, '#ffcf96', .45)], pools=[(80, 270, 160), (460, 270, 160), (270, 760, 180)]),
          's25': CL.Light(dir=(.8, -.4), ambient='#3a4478', ambient_op=.3, lowkey=.55, char_exp=.88, glows=[(90, 340, 70, '#ffb36b', .7), (450, 340, 70, '#ffb36b', .75)], pools=[(90, 340, 200), (450, 340, 220)]),
          's26': CL.Light(dir=(-.6, -.2), char_exp=.92, ambient='#3c4678', ambient_op=.28, lowkey=.45, glows=[(230, 560, 90, '#ffb36b', .55), (420, 200, 150, '#a9bcff', .35)], pools=[(230, 560, 220), (420, 230, 220)])}
BG_L = CL.Light(dir=(-.55, -.8), rim_w=1.6, shade_w=6, rim_op=.7)
def light_chars(sid, content):
    # ฟิลเตอร์แสงขอบ/เงานุ่มต่อชิ้นส่วน (ตัว หัว แขน) แสงติดไปกับตัวละครทุกท่า
    a = CL.char_attr(sid)
    content = re.sub(r'<g id="(\w+?)(Body|LU|RU)"', lambda m: f'<g id="{m.group(1)}{m.group(2)}" {a}', content)
    content = re.sub(r'<g id="(\w+?)H">', lambda m: CL.AO_NECK + f'<g id="{m.group(1)}H" {a}>', content)
    return content
def shot_svg(sid, content):
    if LIGHT and sid in LIGHTS:   # ชั้นเงาแวดล้อมใต้ตัวละคร (ต่อจากภาพฉากหลัง) · ตัวละครมีแสงของตัวเอง · ชั้นแสงเรืองบนสุด
        L_ = LIGHTS[sid]; content = light_chars(sid, content)
        tag = 'preserveAspectRatio="none"/>'
        content = content.replace(tag, tag + CL.shadow_layer(sid, L_), 1) if tag in content else CL.shadow_layer(sid, L_) + content
        content += CL.light_layer(sid, L_)
    return f'<svg id="{sid}" class="shot" viewBox="0 0 540 960" display="none"><g id="{sid}c">{content}</g><rect id="{sid}f" width="540" height="960" fill="#ffffff" opacity="0"/><rect id="{sid}k" width="540" height="960" fill="#000" opacity="0"/></svg>'
# ฉากหลังที่ไม่ขยับ เรนเดอร์เป็นภาพครั้งเดียว (render_bg.js) แล้วใช้เป็น <image> ทำให้เรนเดอร์ทีละเฟรมเร็วขึ้นมาก
BG = {'hall_nbg': SB.hall(CAST_NO('bride', 'groom')), 'hall_nb': SB.hall(CAST_NO('bride')), 'hall_ng': SB.hall(CAST_NO('groom')),
      'hall_nb_cool': SB.hall(CAST_NO('bride'), cool=.15), 'door_closed': SB.doors('closed'), 'door_half': SB.doors('half'), 'door_open': SB.doors('open')}
P2 = SB.P2
THUMB_OLD = '<path d="M 300,630 C 320,580 340,540 352,510 C 362,496 382,500 380,520 C 372,560 360,610 340,660 Z" fill="#fbe2cf"/><ellipse cx="366" cy="512" rx="12" ry="9" fill="#ffffff" opacity=".5"/>'
THUMB = ('<path d="M 286,880 C 296,760 322,590 352,510 C 362,496 382,500 380,520 C 374,580 362,700 350,880 Z" fill="#fbe2cf"/>'
         '<path d="M 352,520 C 356,560 352,620 344,700" stroke="#efc3a8" stroke-width="3" fill="none" opacity=".6"/><ellipse cx="366" cy="512" rx="12" ry="9" fill="#ffffff" opacity=".5"/>')
def phone_bg(bg):
    o = P2.phone_hand('', bg); assert THUMB_OLD in o; return o.replace(THUMB_OLD, '')
FTP = 'font-family="IBM Plex Sans Thai, sans-serif"'
def scr_lock():
    keys = ''.join(f'<g id="k15_{d}"><circle cx="{200 + (i % 3) * 70}" cy="{420 + (i // 3) * 52}" r="20" fill="#2a2e44"/><text x="{200 + (i % 3) * 70}" y="{427 + (i // 3) * 52}" text-anchor="middle" {FTP} font-size="18" fill="#eef0f6">{d}</text></g>'
                   for i, d in enumerate('123456789') ) + f'<circle cx="270" cy="576" r="20" fill="#2a2e44"/><text x="270" y="583" text-anchor="middle" {FTP} font-size="18" fill="#eef0f6">0</text>'
    dots = ''.join(f'<circle id="pd15_{i}" cx="{240 + i * 20}" cy="350" r="6" fill="none" stroke="#c9a8ff" stroke-width="2"/>' for i in range(4))
    return (f'<rect x="156" y="156" width="228" height="488" fill="#141826"/><text x="270" y="250" text-anchor="middle" {FTP} font-size="44" font-weight="300" fill="#eef0f6">21:41</text>'
            f'<text x="270" y="275" text-anchor="middle" {FTP} font-size="11" fill="#9aa2b8">มือถือของเขา · ใส่รหัสผ่าน</text>{dots}{keys}')
def scr_album_long(n=15, scroll_id='al'):
    hairs = ['#3a2620', '#141017', '#6a4a3c', '#2a1c18', '#141017', '#5a3a2a', '#0e0b10', '#3a2a24', '#7a5848', '#2c1e1a', '#4a3028', '#141017', '#6a4a3c', '#3a2620', '#141017']
    cells = ''
    for i in range(n):
        x = 162 + (i % 3) * 74; y = 206 + (i // 3) * 132
        cells += SB.mini_couple(x, y, 68, 104, hairs[i], i + 3) + f'<text x="{x + 34}" y="{y + 120}" text-anchor="middle" font-size="10" fill="#9aa2b8" {FTP}>{2011 + i}</text>'
    hl = f'<rect id="{scroll_id}HL" x="{162 + 2 * 74}" y="{206 + 4 * 132}" width="68" height="104" fill="none" stroke="#c9a8ff" stroke-width="3" opacity="0"/>'
    return (f'<rect x="156" y="156" width="228" height="488" fill="#1a1c28"/><g id="{scroll_id}">{cells}{hl}</g>'
            f'<rect x="156" y="156" width="228" height="40" fill="#2a2c3c"/><text x="170" y="182" font-size="13" font-weight="600" fill="#e8ecf4" {FTP}>อัลบั้ม · งานแต่ง</text>')
def scr_type():
    rows = ''.join(f'<g id="r18_{i}" opacity="0"><rect x="166" y="{254 + i * 72}" width="208" height="60" rx="8" fill="#22263a"/><rect x="176" y="{264 + i * 72}" width="40" height="40" rx="4" fill="#3a3f58"/>'
                   f'<rect x="226" y="{268 + i * 72}" width="{120 - i * 8}" height="8" rx="4" fill="#8a94b4"/><rect x="226" y="{286 + i * 72}" width="{90 + i * 6}" height="6" rx="3" fill="#4e5674"/></g>' for i in range(5))
    kb = ('<g id="kb18"><rect x="156" y="470" width="228" height="174" fill="#262a3a"/>' +
          ''.join(f'<rect x="{162 + c * 22.4}" y="{480 + r * 40}" width="19" height="32" rx="4" fill="#3c4258"/>' for r in range(3) for c in range(10)) +
          '<rect x="200" y="600" width="140" height="30" rx="5" fill="#3c4258"/></g>')
    return (f'<rect x="156" y="156" width="228" height="488" fill="#1a1c28"/><rect x="156" y="156" width="228" height="40" fill="#2a2c3c"/>'
            f'<rect x="166" y="206" width="208" height="30" rx="15" fill="#2c3044"/><text id="q18" x="182" y="226" font-size="12" fill="#e8ecf4" {FTP}></text>'
            f'<rect id="cur18" x="182" y="214" width="1.6" height="15" fill="#c9a8ff"/>{rows}{kb}')
def scr_missing_live():
    s = SB.scr_missing(); parts = s.split('<rect x="')
    return s
def phone_live(n, screen):
    return (f'<g transform="rotate(-4 270 420)"><clipPath id="sc{n}"><rect x="152" y="140" width="236" height="520" rx="24"/></clipPath>'
            f'<g clip-path="url(#sc{n})"><g transform="translate(152,140) scale({236 / 228:.4f},{520 / 488:.4f}) translate(-156,-156)">{screen}'
            f'<circle id="rp{n}" r="10" fill="none" stroke="#ffffff" stroke-width="3" opacity="0"/></g></g></g><g id="th{n}">{THUMB}</g>')
LAST = f'<g id="ly17" opacity="0">{SB.scr_lastyear()}</g>'
MISS = SB.scr_missing()
# แยกโปสเตอร์ตามหาคนหายเป็นชิ้น ให้ขึ้นทีละใบ
_m = re.split(r'(?=<rect x="\d+" y="\d+" width="102" height="136")', MISS)
MISS_LIVE = _m[0] + '<g id="ms19">' + ''.join(f'<g id="ms19_{i}" opacity="0">{p}</g>' for i, p in enumerate(_m[1:])) + '</g>'
BG.update({'hall_all': SB.hall(), 'hall_cool': SB.hall(cool=.12), 'hall_nmom': SB.hall(CAST_NO('mom'), cool=.12), 'hall_nph': SB.hall(CAST_NO('ph'), cool=.12),
           'hall_nstaff': SB.hall(CAST_NO('staff', 'ph', 'bm'), cool=.12), 'hall_nb_cool2': SB.hall(CAST_NO('bride'), cool=.12),
           'phb_bridal': phone_bg(P2.bridal_room_bg()), 'phb_suite': phone_bg('<g filter="url(#blurBG)">' + P2.suite_room() + '</g>'),
           'ph17': P2.phone_hand(SB.scr_lastyear(), P2.bridal_room_bg()), 'ph18': P2.phone_hand(SB.scr_search(), P2.bridal_room_bg()),
           'ph19': P2.phone_hand(SB.scr_missing(), P2.bridal_room_bg()), 'ph21': P2.phone_hand(SB.scr_call(), '<g filter="url(#blurBG)">' + P2.suite_room() + '</g>'),
           'elev': P2.elevator_lux(''), 'sdoor': P2.suite_door_lux(True), 'suite': P2.suite_room(''),
           'darkbg': '<rect width="540" height="960" fill="#0e0d16"/><ellipse cx="270" cy="360" rx="200" ry="260" fill="#3a3a5a" opacity=".35" filter="url(#bl4)"/>',
           'corr': SB.corridor_groom().split(SB.put('groom_sin', 270, 330 + 492 * 1.7, 1.7, shadow=False))[0]})
def sup_rig(p, f):
    n, nt, kind, back, head, body = f()
    return (f'<g id="{p}">{back}<g id="{p}Body">{body}</g><g id="{p}H">{head}</g></g>', 460 if kind == 'f' else 488)
def fxy(key):
    x, feet, sc = SB.CAST[key]; return x, feet - (sup_rig('_', {'mom': SP.c_mother, 'ph': SP.c_photographer, 'staff': SP.c_staff}[key])[1] + 4) * sc
MX, MY = fxy('mom'); PX, PY = fxy('ph'); SX, SY = fxy('staff')
DARK_TOP = '<rect width="540" height="960" fill="#1a1a30" opacity=".35" style="mix-blend-mode:multiply"/><rect width="540" height="960" fill="url(#vigD)"/>'
PHONE = '<g transform="translate(38,4) rotate(8)"><rect x="-6" y="-18" width="13" height="30" rx="3" fill="#15131c"/><rect x="-4.6" y="-16" width="10" height="25" rx="2" fill="#6f7cff" opacity=".35"/></g>'
CARD_Q = ('คุณคิดว่าผู้หญิงคนนั้นเข้ามาเพื่อ', 'ช่วยคุณ หรือกำลังหาคน', 'มาตายแทนตัวเอง?')
def card_svg():
    q = (f'<text x="270" y="300" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#fff">{CARD_Q[0]}</text>'
         f'<text x="270" y="338" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#fff"><tspan fill="#c04dff">ช่วยคุณ</tspan> หรือกำลังหาคน</text>'
         f'<text x="270" y="376" text-anchor="middle" {FT0} font-size="26" font-weight="700" fill="#ff3b4e">มาตายแทนตัวเอง?</text>')
    opt = lambda k, y, txt: (f'<g id="opt{k}" transform="translate(270,{y})"><rect id="opt{k}R" x="-190" y="-34" width="380" height="68" rx="34" fill="#120e1c" stroke="#9a86ff" stroke-width="2"/>'
                             f'<circle cx="-150" cy="0" r="20" fill="#7a1fff"/><text x="-150" y="8" text-anchor="middle" {FT0} font-size="22" font-weight="700" fill="#fff">{k}</text>'
                             f'<text x="-116" y="9" {FT0} font-size="22" font-weight="600" fill="#f2eefa">{txt}</text></g>')
    return ('<rect width="540" height="960" fill="#0b0912"/><rect width="540" height="960" fill="url(#vigD)"/>' + q + opt('A', 470, 'เข้ามาช่วยคุณ') + opt('B', 560, 'หาคนมาตายแทนตัวเอง')
            + f'<text x="270" y="660" text-anchor="middle" {FT0} font-size="16" fill="#a79fc0">ตอบในคอมเมนต์ A หรือ B</text>')
FT0 = 'font-family="IBM Plex Sans Thai, sans-serif"'
import base64 as _b64
_GRAIN = _b64.b64encode(open('grain256.png', 'rb').read()).decode()
GRADE = ('<svg id="grade" viewBox="0 0 540 960"><defs><pattern id="grainP" width="256" height="256" patternUnits="userSpaceOnUse">'
         f'<image href="data:image/png;base64,{_GRAIN}" width="256" height="256"/></pattern>'
         '<filter id="dGlow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="1.1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<filter id="dSoft" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="2.6"/></filter>'
         '<radialGradient id="gVig" cx=".5" cy=".46" r=".72"><stop offset=".55" stop-color="#05040a" stop-opacity="0"/><stop offset="1" stop-color="#05040a" stop-opacity=".42"/></radialGradient></defs>'
         '<rect id="grRect" width="540" height="960" fill="#4a5d96" opacity="0"/>'
         '<g id="dustS" filter="url(#dGlow)">' + ''.join(f'<circle id="ds{i}" r="1.4" fill="#fff6ea" opacity="0"/>' for i in range(22)) + '</g>'
         '<g id="dustB" filter="url(#dSoft)">' + ''.join(f'<circle id="db{i}" r="4" fill="#fff2e2" opacity="0"/>' for i in range(10)) + '</g>'
         '<rect id="grVig" width="540" height="960" fill="url(#gVig)"/><rect id="grGrain" width="540" height="960" fill="url(#grainP)" opacity=".16"/></svg>')
def img(name): return f'<image href="{BGDIR}/{name}.jpg" width="540" height="960" preserveAspectRatio="none"/>'
door_open = img('door_open')
SVGS = [
    shot_svg('s1', img('hall_nbg') + placed(bride_rig('b1'), *SB.CAST['bride']) + placed(groom_rig('g1'), *SB.CAST['groom'])),
    shot_svg('s2', img('hall_all')),
    shot_svg('s3', img('hall_nbg') + placed(bride_rig('b3'), *SB.CAST['bride']) + placed(groom_rig('g3'), *SB.CAST['groom'])),
    shot_svg('s4', f'<g id="d4c">{img("door_closed")}</g><g id="d4h" display="none">{img("door_half")}</g><g id="d4o" display="none">{door_open}</g>'),
    shot_svg('s4r', img('hall_nb') + placed(bride_rig('b4'), *SB.CAST['bride'])),
    shot_svg('s5', door_open + placed(woman_rig('w5'), 270, SB.DOOR_FEET, SB.DOOR_S) + f'<g id="ring5" display="none">{SB.inset_ring()}</g>'),
    shot_svg('s6', door_open + placed(woman_rig('w6'), 270, SB.DOOR_FEET, SB.DOOR_S)),
    shot_svg('s6r', img('hall_nb') + placed(bride_rig('b6'), *SB.CAST['bride'])),
    shot_svg('s7a', img('hall_ng') + placed(groom_rig('g7', heads=('ghead', 'ghead_angry', 'ghead_sin', 'ghead_panic')), *SB.CAST['groom'])),
    shot_svg('s7b', door_open + placed(woman_rig('w7'), 246, SB.DOOR_FEET, SB.DOOR_S) + placed(guard_rig('k7'), 600, SB.DOOR_FEET + 4, SB.DOOR_S)),
    shot_svg('s8', door_open + placed(woman_rig('w8'), 246, SB.DOOR_FEET, SB.DOOR_S) + placed(guard_rig('k8'), 312, SB.DOOR_FEET + 4, SB.DOOR_S)),
    shot_svg('s9', door_open + placed(woman_rig('w9'), 270, SB.DOOR_FEET, SB.DOOR_S)),
    shot_svg('s9r', img('hall_nb_cool') + placed(bride_rig('b9'), *SB.CAST['bride'])),
    shot_svg('s10', img('hall_nb_cool2') + placed(bride_rig('b10'), *SB.CAST['bride'])),
    shot_svg('s11', img('hall_cool')),
    shot_svg('s12', img('hall_nmom') + placed(sup_rig('m12', SP.c_mother), *SB.CAST['mom'])),
    shot_svg('s13', img('hall_nph') + placed(sup_rig('p13', SP.c_photographer), *SB.CAST['ph'])),
    shot_svg('s14', img('hall_nstaff') + placed(sup_rig('t14', SP.c_staff), *SB.CAST['staff'])),
    shot_svg('s15', img('phb_bridal') + phone_live(15, scr_lock() + f'<g id="al15" opacity="0">{scr_album_long(15, "a15")}</g>')),
    shot_svg('s16', img('phb_bridal') + phone_live(16, scr_album_long(15, 'a16'))),
    shot_svg('s17', img('phb_bridal') + phone_live(17, scr_album_long(15, 'a17') + LAST)),
    shot_svg('s18', img('phb_bridal') + phone_live(18, scr_type())),
    shot_svg('s19', img('phb_bridal') + phone_live(19, MISS_LIVE)),
    shot_svg('s20', img('elev') + placed(bride_rig('b20'), 270, 905, .64)),
    shot_svg('s21', img('phb_suite') + phone_live(21, SB.scr_call() + '<circle id="ring21" cx="270" cy="300" r="44" fill="none" stroke="#9aa8ff" stroke-width="2"/>')),
    shot_svg('s22', img('darkbg') + placed(woman_rig('w22'), 270, 330 + 464 * 1.7, 1.7) + DARK_TOP),
    shot_svg('s23', img('darkbg') + placed(woman_rig('w23'), 270, 330 + 464 * 1.7, 1.7) + DARK_TOP),
    shot_svg('s24', img('sdoor')),
    shot_svg('s25', img('corr') + placed(groom_rig('g25'), 270, 330 + 492 * 1.7, 1.7) + '<rect width="540" height="960" fill="url(#vigD)"/>'),
    shot_svg('s26', img('suite') + placed(bride_rig('b26'), 300, 330 + 466 * 1.8, 1.8)),
    shot_svg('s27', f'<g id="s27in" opacity="0">{card_svg()}</g>'),
]

# ---------------------------------------------------------------- ซับแบบตั้งเวลา (ไทย + อังกฤษ)
# คำเน้นในซับ (ผู้ใช้สั่ง: ตัวหนังสือขาว คำเน้นสีม่วง จังหวะตกใจสีแดง)
EMPH = {1: [('วันแต่งงาน', 'p'), ('ภรรยา', 'r'), ('คุณจะทำยังไงคะ?', 'p')], 3: [('สามปี', 'p'), ('สมบูรณ์แบบ', 'p')],
        4: [('ประตูห้องจัดเลี้ยง', 'p'), ('เปิดออก', 'r')], 5: [('ชุดเดรสสีดำ', 'p'), ('แบบเดียวกับคุณทุกประการ', 'r')],
        6: [('สามีของฉัน', 'r')], 7: [('แฟนเก่า', 'p'), ('ป่วยทางจิต', 'r'), ('เจ้าหน้าที่!', 'r')], 8: [('ประโยคเดียว', 'p')],
        9: [('อย่าให้เขาถอดแหวน', 'r'), ('เด็ดขาด', 'r')], 2: [('โรงแรมหรู', 'p')], 10: [('ความผิดปกติ', 'p')],
        11: [('ไม่มีใครถ่ายรูป', 'p')], 12: [('ผิดชื่อ', 'r')], 13: [('ครั้งที่แล้ว', 'r')], 14: [('สายตาสงสาร', 'p')], 15: [('โทรศัพท์ของเจ้าบ่าว', 'p')],
        16: [('โรงแรมเดียวกัน', 'p'), ('เจ้าบ่าวคนเดียวกัน', 'p'), ('ไม่เคยซ้ำหน้า', 'r')], 17: [('เจ้าสาวของปีที่แล้ว', 'r')], 18: [('ชื่อเจ้าสาว', 'p')],
        19: [('ประกาศตามหาคนหาย', 'r'), ('หนึ่งวัน', 'r')], 20: [('จุดเดิม', 'p'), ('ซ้ำแล้วซ้ำเล่า', 'r')], 21: [('เบอร์ไม่ทราบชื่อ', 'p'), ('ผู้หญิงชุดดำ', 'r')],
        22: [('ไม่ใช่สามี', 'r'), ('เจ้าสาว', 'p')], 23: [('อยากรอด', 'p'), ('ผู้หญิงคนต่อไป', 'r')], 24: [('สามครั้ง', 'p')], 25: [('ถอดแหวน', 'r')]}
def colorize(full, lines, n):
    col = [''] * len(full)
    for ph, c in EMPH.get(n, []):
        i = full.find(ph)
        while i >= 0:
            for k in range(i, i + len(ph)): col[k] = c
            i = full.find(ph, i + len(ph))
    out = []; cur = 0
    for l in lines:
        i = full.find(l, cur); i = cur if i < 0 else i; cur = i + len(l)
        segs = []; run = ''; rc = None
        for k, ch in enumerate(l):
            c = col[i + k] if i + k < len(col) else ''
            if c != rc and run: segs.append((run, rc)); run = ''
            run += ch; rc = c
        if run: segs.append((run, rc))
        out.append(''.join(f'<tspan class="h{c}">{t}</tspan>' if c else t for t, c in segs))
    return out
SUB_Y = 780   # ผู้ใช้สั่ง: ขยับซับลงมา (เดิม 712)
SUB_TXT = {**{f'{n}f': n for n in range(10, 26)}, '02a': 2, '01c': 1, '03c': 3, '04c': 4, '05c': 5, '06e': 6, '07g': 7, '08c': 8, '09e': 9}
subs = []; sub_svg = []
script = {int(m.group(1)): m.group(2) for m in (re.match(r'^(\d+)\. (.*)$', l.strip()) for l in open('../script.md')) if m}
def clean(t): return re.sub(r'\s*\([^)]*\)\s*', ' ', re.sub(r'\[[^\]]*\]\s*', '', t)).replace('"', '').strip()
for key, n in SUB_TXT.items():
    full = clean(script[n]); ls0 = thai_lines(full); ls = colorize(full, ls0, n); groups = [ls[i:i + 2] for i in range(0, len(ls), 2)]
    plain = [ls0[i:i + 2] for i in range(0, len(ls0), 2)]
    words = EN[n].split(' '); tot = sum(len(''.join(g)) for g in plain); acc = 0; wi = 0
    for gi, g in enumerate(groups):
        a0 = VOICE_AT[key] + D[key] * acc / tot - .1; acc += len(''.join(plain[gi])); a1 = VOICE_AT[key] + D[key] * acc / tot + (.4 if gi == len(groups) - 1 else 0)
        upto = len(words) if gi == len(groups) - 1 else round(len(words) * acc / tot); en = ' '.join(words[wi:upto]); wi = upto
        el = []; cur = ''
        for w in en.split(' '):
            if len(cur) + len(w) > 44 and cur: el.append(cur); cur = w
            else: cur = (cur + ' ' + w).strip()
        if cur: el.append(cur)
        block = len(g) * 27 + 6 + len(el) * 17; y0 = SUB_Y - block / 2 + 20
        th = ''.join(f'<text x="270" y="{y0 + i * 27:.0f}" class="th">{l}</text>' for i, l in enumerate(g))
        ye = y0 + (len(g) - 1) * 27 + 23
        enx = ''.join(f'<text x="270" y="{ye + i * 17:.0f}" class="en">{l}</text>' for i, l in enumerate(el[:3]))
        sid = f'sub{len(subs)}'; subs.append((round(a0, 3), round(a1, 3), sid)); sub_svg.append(f'<g id="{sid}" display="none">{th}{enx}</g>')

# ---------------------------------------------------------------- กราฟิกทับภาพ: ป้ายเวลา + มาตรความไว้ใจ + กราฟิกชี้แหวน
FT = 'font-family="IBM Plex Sans Thai, sans-serif"'
def mini_ring(skin, sleeve, label, cx, cy, gid):
    hand = (SB.inset_ring().replace('#141218"/><path', '#26222e"/><path', 1)
            .replace('fill="#141218"/>\n', '').replace('d="M 380,240 C 400,214 460,214 482,240 L 486,270 L 376,270 Z" fill="#141218"', f'd="M 380,240 C 400,214 460,214 482,240 L 486,270 L 376,270 Z" fill="{skin}"')
            .replace('stroke="#2c2a34"', f'stroke="{sleeve}"'))
    return (f'<g id="{gid}" opacity="0" transform="translate({cx},{cy})"><g transform="scale(.74) translate(-430,-230)">{hand}</g>'
            f'<rect x="-46" y="66" width="92" height="28" rx="14" fill="#f6f2fb"/><text x="0" y="86" text-anchor="middle" {FT} font-size="15" font-weight="600" fill="#1a1626">{label}</text></g>')
EYE = ('<g id="wm" transform="translate(500,48)" opacity=".85"><ellipse cx="0" cy="0" rx="20" ry="15" fill="#7a1fff"/>'
       '<path d="M -15,0 C -8,-8.5 8,-8.5 15,0 C 8,8.5 -8,8.5 -15,0 Z" fill="#05040a"/><circle cx="0" cy="0" r="4.2" fill="#d6b0ff"/></g>')   # ลายน้ำดวงตาของช่อง (จาก ep-4am-transfer)
RINGS = ('<g id="ringBlack"><path d="M -70,-14 L 70,-16 C 80,-15 80,15 70,16 L -70,14 Z" fill="#1d1a24"/><path d="M -70,-14 L 70,-16 L 70,-8 L -70,-6 Z" fill="#34303f"/>'
         '<path d="M -9,-17 L 9,-17 L 9,17 L -9,17 Z" fill="#cfd5df"/><path d="M -9,-17 L -3,-17 L -3,17 L -9,17 Z" fill="#f4f7fb"/><path d="M 5,-17 L 9,-17 L 9,17 L 5,17 Z" fill="#9aa3b2"/>'
         '<path d="M 0,-34 L 11,-22 L 0,-14 L -11,-22 Z" fill="#e6f0ff"/><path d="M 0,-34 L -11,-22 L 0,-22 Z" fill="#ffffff"/><path d="M 0,-22 L 11,-22 L 0,-14 Z" fill="#a9c4ea"/></g>'
         '<g id="ringSkin"><path d="M -70,-14 L 70,-16 C 80,-15 80,15 70,16 L -70,14 Z" fill="#f6d6c2"/><path d="M -70,6 L 70,8 L 70,16 L -70,14 Z" fill="#e8bea6"/>'
         '<path d="M -9,-17 L 9,-17 L 9,17 L -9,17 Z" fill="#cfd5df"/><path d="M -9,-17 L -3,-17 L -3,17 L -9,17 Z" fill="#f4f7fb"/><path d="M 5,-17 L 9,-17 L 9,17 L 5,17 Z" fill="#9aa3b2"/>'
         '<path d="M 0,-34 L 11,-22 L 0,-14 L -11,-22 Z" fill="#e6f0ff"/><path d="M 0,-34 L -11,-22 L 0,-22 Z" fill="#ffffff"/><path d="M 0,-22 L 11,-22 L 0,-14 Z" fill="#a9c4ea"/></g>'
         '<clipPath id="lensSm"><circle r="44"/></clipPath>')
MONO = 'font-family="IBM Plex Mono, monospace"'
WARN = '<path d="M 0,-7 L 7,6 L -7,6 Z" fill="#ff3b4e"/><rect x="-.9" y="-3" width="1.8" height="5" fill="#fff"/><circle cx="0" cy="3.8" r=".9" fill="#fff"/>'
# ป้ายสถานะแบบ C (ผู้ใช้เลือก): แคปซูลเวลาแบบตอนแรก · ป้ายเหตุการณ์แดงขึ้นตอนมีเรื่อง · ตัวเลขความไว้ใจขึ้นกลางบนแว้บเดียวตอนลดลง
OVL = EYE + (f'<defs>{RINGS}</defs><g id="hud" {FT}><rect x="20" y="22" width="112" height="38" rx="19" fill="#120e1c" fill-opacity=".82" stroke="#9a86ff" stroke-opacity=".7"/>'
       f'<circle id="hudDot" cx="39" cy="41" r="5" fill="#9a86ff"/><text id="hudTxt" x="52" y="47" font-size="17" font-weight="600" fill="#f2eefa" {MONO}>19:00</text>'
       f'<g id="evt" opacity="0"><rect id="evtR" x="20" y="68" width="150" height="30" rx="15" fill="#3a0f1a" fill-opacity=".85" stroke="#ff3b4e" stroke-opacity=".7"/>'
       f'<g transform="translate(38,83)">{WARN}</g><text id="evtTxt" x="52" y="88" font-size="13" font-weight="600" fill="#ffd2d7">มีคนบุกงานแต่ง</text></g>'
       f'<g id="trustT" opacity="0" text-anchor="middle"><rect x="178" y="24" width="184" height="34" rx="17" fill="#120e1c" fill-opacity=".8" stroke="#ff3b4e" stroke-opacity=".5"/>'
       f'<text x="270" y="47" font-size="14" fill="#f2eefa">ความไว้ใจ <tspan id="trustPct" fill="#ff3b4e" font-weight="700">100%</tspan> <tspan id="trustDel" fill="#ff3b4e" font-size="12">▼ 30</tspan></text></g></g>'
       # กราฟิกชี้แหวนแบบ 3 (ผู้ใช้เลือก): มุมกรอบม่วงล็อกแหวน → เส้นประหักมุม → การ์ดเทียบแหวน MATCH
       f'<g id="callout" opacity="0"><g id="coBr" stroke="#c9a8ff" stroke-width="3" fill="none" stroke-linecap="round">'
       f'<path d="M -22,-11 V -21 H -12"/><path d="M 12,-21 H 22 V -11"/><path d="M 22,11 V 21 H 12"/><path d="M -12,21 H -22 V 11"/></g>'
       f'<circle id="coDot" r="4" fill="#c9a8ff"/><path id="coLine" d="M 0,0" fill="none" stroke="#c9a8ff" stroke-width="2.4" stroke-dasharray="6 5"/>'
       f'<g id="coCard" opacity="0"><rect x="150" y="236" width="300" height="188" rx="16" fill="#120e1c" fill-opacity=".9" stroke="#9a86ff" stroke-opacity=".8" stroke-width="1.5"/>'
       f'<circle cx="172" cy="260" r="5" fill="#9a86ff"/><text x="184" y="266" font-size="15" font-weight="500" fill="#d9d2ee">ตรวจพบแหวนวงเดียวกัน</text>'
       f'<g id="coA" opacity="0"><circle r="44" fill="#2a2433" stroke="#9a86ff" stroke-width="1.5"/><g clip-path="url(#lensSm)"><use href="#ringBlack" transform="scale(.85) translate(0,10)"/></g>'
       f'<text y="70" text-anchor="middle" font-size="14" fill="#f2eefa">ของเธอ</text></g>'
       f'<g id="coB" opacity="0"><circle r="44" fill="#efe6dc" stroke="#9a86ff" stroke-width="1.5"/><g clip-path="url(#lensSm)"><use href="#ringSkin" transform="scale(.85) translate(0,10)"/></g>'
       f'<text y="70" text-anchor="middle" font-size="14" fill="#f2eefa">ของคุณ</text></g>'
       f'<text id="coEq" x="300" y="342" text-anchor="middle" font-size="30" font-weight="700" fill="#c9a8ff" opacity="0">=</text>'
       f'<text id="coM" x="300" y="414" text-anchor="middle" font-size="12" fill="#a79fc0" {MONO}>MATCH 0%</text></g></g>')
TRUST = [(T0['s6'] + .4 + D['06e'] * .85, 100, 70), (T0['s7a'] + G7_POINT - 3.2, 70, 45), (T0['s9'] + .4 + D['09e'] * .7, 45, 20),
         (T0['s12'] + .4 + D['12f'] * .7, 20, 12), (T0['s13'] + .4 + D['13f'] * .8, 12, 5), (T0['s17'] + .4 + D['17f'] * .6, 5, 0)]
ZB_T = [T0[k] for k in ('s4', 's15', 's20', 's22', 's24', 's27')]
TW22 = T0['s22'] + .4 + D['22f'] * .82
SHAKES = [(T0['s6r'], .45, 9), (TW22, .5, 8), (T0['s26'] + .02, .55, 9)]
KNOCKS = [.5 + D['24f'] + .45 + k * .55 for k in range(3)]
EVT = [(T0['s4'] + TB + .6, 'มีคนบุกงานแต่ง'), (T0['s10'], 'มีบางอย่างผิดปกติ'), (T0['s15'], 'แอบค้นมือถือเจ้าบ่าว'), (T0['s17'], 'เจ้าสาวปีที่แล้ว'),
       (T0['s19'], 'เจ้าสาวทุกคนหายตัว'), (T0['s20'], 'หนีออกไปไม่ได้'), (T0['s21'], 'สายเข้า · ผู้หญิงชุดดำ'), (T0['s24'], 'มีคนเคาะประตู')]

# ---------------------------------------------------------------- JS ขับการเคลื่อนไหวทุกเฟรม
JS = r'''
const VD = %(vd)s, KNOCKS = %(knocks)s, EVT = %(evt)s;
const TRUST = %(trust)s, BANG = %(bang)s, RT5 = %(ringt)s;
const SH = %(shots)s, T0 = %(t0)s, ENV = %(env)s, VAT = %(vat)s, SUBS = %(subs)s, FPS = %(fps)s;
const $ = id => document.getElementById(id);
function place(el, dx, dfeet, ds, rot) {
  const lf = +el.dataset.lf, x = +el.dataset.x + (dx||0), feet = +el.dataset.feet + (dfeet||0), s = +el.dataset.s * (ds||1);
  el.setAttribute('transform', `translate(${x},${feet - lf * s}) scale(${s}) rotate(${rot||0} 0 ${lf})`);
}
function P(rig) { return $(rig).parentNode; }
function head(rig, ang, dy) { $(rig + 'H').setAttribute('transform', `translate(0,${dy||0}) rotate(${ang||0} 0 40)`); }
function blinkAt(rig, t, per, off, force) { const c = force || ((t + off) %% per) < .13; $(rig + 'B').setAttribute('display', c ? 'inline' : 'none'); }
function face(rig, k, n) { for (let i = 0; i < n; i++) { const u = $(rig + 'H' + i); if (u) u.setAttribute('display', i === k ? 'inline' : 'none'); } }
function talk(rig, key, gt) {
  const e = ENV[key], i = Math.floor((gt - VAT[key]) * FPS), m = $(rig + 'M');
  if (!e || i < 0 || i >= e.length) { m.setAttribute('display', 'none'); return; }
  const a = e[i];
  if (a < .1) { m.setAttribute('display', 'none'); return; }
  m.setAttribute('display', 'inline'); $(rig + 'Mo').setAttribute('ry', (1.1 + a * 4.4).toFixed(2)); $(rig + 'Mo').setAttribute('rx', (4 + a * 1.4).toFixed(2));
  $(rig + 'Mt').setAttribute('display', a > .35 ? 'inline' : 'none');
}
function cam(sid, z, cx, cy, ty, sx, sy) { let X = 270 - cx * z + (sx||0), Y = (ty||400) - cy * z + (sy||0);
  if (z >= 1) { X = Math.min(0, Math.max(540 - 540 * z, X)); Y = Math.min(0, Math.max(960 - 960 * z, Y)); }
  $(sid + 'c').setAttribute('transform', `translate(${X},${Y}) scale(${z})`); }
const ease = x => x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x);
const lerp = (a, b, x) => a + (b - a) * x;
function shake(t, t0, d, amp) { if (t < t0 || t > t0 + d) return [0, 0]; const q = 1 - (t - t0) / d; return [Math.sin(t * 90) * amp * q, Math.cos(t * 77) * amp * q]; }
function flash(sid, t, list) { let o = 0; for (const [a, d] of list) if (t >= a && t < a + d) o = Math.max(o, .85 * (1 - (t - a) / d)); $(sid + 'f').setAttribute('opacity', o.toFixed(3)); }
function arm(p, side, a, b) { const u = $(p + side + 'U'); if (!u) return; u.setAttribute('transform', `rotate(${a} ${u.dataset.sx} ${u.dataset.sy})`);
  const f = $(p + side + 'F'); f.setAttribute('transform', `rotate(${b} ${f.dataset.ex} ${f.dataset.ey})`); }
const backOut = x => { x = Math.min(1, Math.max(0, x)); const c = 1.6; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
function pose(p, from, to, k) { const e = backOut(k); arm(p, 'L', lerp(from[0], to[0], e), lerp(from[1], to[1], e)); arm(p, 'R', lerp(from[2], to[2], e), lerp(from[3], to[3], e)); }
function idleArms(p, t, ph) { arm(p, 'L', 1.6 * Math.sin(t * .9 + ph), -5 - 2.5 * Math.sin(t * 1.1 + ph)); arm(p, 'R', -1.6 * Math.sin(t * .8 + ph), 5 + 2.5 * Math.sin(t * 1.2 + ph)); }
function env(key, gt) { const e = ENV[key]; if (!e) return 0; const i = Math.floor((gt - VAT[key]) * FPS); return (i >= 0 && i < e.length) ? e[i] : 0; }
function breathe(p, t, amp, rate, sway) { place(P(p), 0, 0, 1 + amp * Math.sin(t * rate), sway * Math.sin(t * .45)); }
const CLASP = [-12, -18, 12, 18], SHOCK = [-28, -138, 10, 140], RELAX = [0, -5, 0, 5], RINGUP = [0, -5, 15, 122], CHEST = [0, -5, 12, 128];

function scrXY(cx, cy) { const px = 152 + (cx - 156) * 236 / 228, py = 140 + (cy - 156) * 520 / 488, a = -4 * Math.PI / 180, dx = px - 270, dy = py - 420;
  return [270 + dx * Math.cos(a) - dy * Math.sin(a), 420 + dx * Math.sin(a) + dy * Math.cos(a)]; }
function thumb(n, kf, t) {   // kf = [[เวลา, x จอ, y จอ, กด(0/1)], ...] นิ้วโป้งเคลื่อนนุ่ม ๆ ระหว่างจุด กดแล้วจุ่มลงนิดหนึ่งพร้อมวงคลื่นบนจอ
  let i = 0; while (i < kf.length - 1 && t > kf[i + 1][0]) i++;
  const A = kf[i], B = kf[Math.min(i + 1, kf.length - 1)], k = B[0] > A[0] ? ease((t - A[0]) / (B[0] - A[0])) : 0;
  const cx = lerp(A[1], B[1], k), cy = lerp(A[2], B[2], k); let press = 0, rp = null;
  for (const K of kf) if (K[3]) { const u = t - K[0]; if (u >= 0 && u < .16) press = Math.sin(u / .16 * Math.PI); if (u >= 0 && u < .45) rp = [K[1], K[2], u]; }
  const [x, y] = scrXY(cx, cy), dx = x - 366, dy = y - 512 + press * 5;
  $('th' + n).setAttribute('transform', `translate(${dx.toFixed(1)},${dy.toFixed(1)}) rotate(${(dx * .04).toFixed(2)} 330 880)`);
  const r = $('rp' + n); if (rp) { r.setAttribute('cx', rp[0]); r.setAttribute('cy', rp[1]); r.setAttribute('r', (8 + 40 * rp[2]).toFixed(1)); r.setAttribute('opacity', (.8 * (1 - rp[2] / .45)).toFixed(2)); } else r.setAttribute('opacity', 0);
}
const KEYXY = d => [200 + ((d - 1) %% 3) * 70, 420 + Math.floor((d - 1) / 3) * 52];

// ---- เอฟเฟกต์แบบหนัง
const ZB = %(zb)s, SHAKES = %(shakes)s;
const GRADES = [[0, '#ffe3d4', .16, 'contrast(1.04) saturate(1.02)'], [BANG + .1, '#4a5d96', .32, 'contrast(1.08) saturate(.88)'],
  [T0.s10, '#56689a', .28, 'contrast(1.06) saturate(.86) brightness(.99)'], [T0.s15, '#3d5f84', .30, 'contrast(1.08) saturate(.9)'],
  [T0.s20, '#2e3e74', .38, 'contrast(1.1) saturate(.86) brightness(.98)'], [T0.s27, '#000000', 0, 'none']];
const HALLZ = [[270, 250, 190, 170]], DOORZ = [[270, 470, 110, 250]];
const DUSTZ = { s1: HALLZ, s2: HALLZ, s3: HALLZ, s4: DOORZ, s4r: HALLZ, s5: DOORZ, s6: DOORZ, s6r: HALLZ, s7a: HALLZ, s7b: DOORZ, s8: DOORZ, s9: DOORZ, s9r: HALLZ,
  s10: HALLZ, s11: HALLZ, s12: HALLZ, s13: HALLZ, s14: HALLZ, s20: [[270, 190, 150, 110]], s22: [[270, 330, 160, 200]], s23: [[270, 330, 160, 200]],
  s24: [[270, 300, 210, 150]], s25: [[270, 330, 230, 110]], s26: [[390, 330, 110, 210]] };
const hsh = i => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
function filmFX(cur, gt) {
  // คุมสีตามช่วงเรื่อง ช่วงหลังเสียงปังค่อย ๆ เย็นลง
  let g = GRADES[0]; for (const G of GRADES) if (gt >= G[0]) g = G;
  let op = g[2]; if (g === GRADES[1]) op *= Math.min(1, (gt - BANG - .1) / .6);
  $('grRect').setAttribute('fill', g[1]); $('grRect').setAttribute('opacity', op.toFixed(3));
  $('grGrain').setAttribute('opacity', cur === 's27' ? .1 : .16); $('grVig').setAttribute('opacity', cur === 's27' ? 0 : 1);
  $('grain' + 'P') && $('grainP').setAttribute('patternTransform', `translate(${Math.floor(hsh(Math.floor(gt * 24)) * 256)},${Math.floor(hsh(Math.floor(gt * 24) + 7) * 256)})`);
  // ซูมเบลอตอนตัดเปลี่ยนสถานที่
  let zk = 0; for (const B of ZB) { if (gt > B - .22 && gt < B) zk = Math.max(zk, (gt - (B - .22)) / .22); if (gt >= B && gt < B + .3) zk = Math.max(zk, 1 - (gt - B) / .3); }
  // กล้องสั่นตอนหักมุม
  let sx = 0, sy = 0; for (const [a, d, amp] of SHAKES) if (gt >= a && gt < a + d) { const q = 1 - (gt - a) / d; sx += Math.sin(gt * 93) * amp * q; sy += Math.cos(gt * 71) * amp * q; }
  const el = $(cur); el.style.transform = `translate(${sx.toFixed(1)}px,${sy.toFixed(1)}px) scale(${(1 + .22 * zk + (sx || sy ? .02 : 0)).toFixed(3)})`;
  el.style.filter = (g[3] === 'none' ? '' : g[3]) + (zk > .01 ? ` blur(${(7 * zk).toFixed(1)}px) brightness(${(1 + .25 * zk).toFixed(2)})` : '');
  // ฝุ่นลอยในลำแสง: จุดคมเรืองนิด ๆ กับจุดเบลอไกล ลอยขึ้นช้า ๆ กะพริบเบา ๆ
  const Z = DUSTZ[cur] || [], nS = 22, nB = 10;
  for (let i = 0; i < nS + nB; i++) {
    const c = i < nS ? $('ds' + i) : $('db' + (i - nS)); if (!Z.length) { c.setAttribute('opacity', 0); continue; }
    const [zx, zy, rx, ry] = Z[i %% Z.length], u = hsh(i + 1), v = hsh(i + 50), ph = hsh(i + 90) * 6.28;
    const x = zx + rx * (u * 2 - 1) + 10 * Math.sin(gt * .25 + ph), yy = (v * 2 * ry + gt * (i < nS ? 7 : 4)) %% (2 * ry), y = zy + ry - yy;
    const dd = Math.pow((x - zx) / rx, 2) + Math.pow((y - zy) / ry, 2), fall = Math.max(0, 1 - dd);
    const tw = .55 + .45 * Math.sin(gt * (1.3 + u) + ph);
    c.setAttribute('cx', x.toFixed(1)); c.setAttribute('cy', y.toFixed(1)); c.setAttribute('r', (i < nS ? 1 + 1.1 * u : 3 + 2.5 * u).toFixed(2));
    c.setAttribute('opacity', ((i < nS ? .75 : .28) * fall * tw).toFixed(2));
  }
}
const R = { // การแสดงของแต่ละช็อต: t = เวลาในช็อต, gt = เวลารวม
  s1(t, gt) { cam('s1', lerp(1.0, 1.75, ease(t / SH.s1)), lerp(270, %(cx3)s, ease(t / SH.s1)), lerp(520, %(cy3)s, ease(t / SH.s1)), lerp(480, 380, ease(t / SH.s1)));
    blinkAt('b1', t, 3.4, .7); blinkAt('g1', t, 3.9, 2.1); breathe('b1', t, .005, 2.0, .6); breathe('g1', t, .004, 1.8, -.4);
    const k = (t - 2.0) / .9; if (t < 2.0) pose('b1', CLASP, CLASP, 1); else pose('b1', CLASP, [-12, -18, 26, 96], k);
    head('b1', 3 + 1.5 * Math.sin(t * 1.0), 0); idleArms('g1', t, .5); head('g1', -2 - Math.sin(t * .8), 0);
    if (t > SH.s1 - 3) { face('b1', 1, 3); head('b1', lerp(3, -5, ease((t - SH.s1 + 3) / .8)), 0); } else face('b1', 0, 3); },
  s3(t, gt) { cam('s3', lerp(2.0, 2.25, t / SH.s3), %(cx3)s, %(cy3)s, 360); blinkAt('b3', t, 3.1, .4); blinkAt('g3', t, 3.7, 1.6);
    breathe('b3', t, .005, 2.2, .7); breathe('g3', t, .004, 1.9, -.5);
    pose('b3', CLASP, CLASP, 1); arm('b3', 'L', -12 + 1.5 * Math.sin(t * 1.3), -18 - 3 * Math.sin(t * 1.3)); arm('b3', 'R', 12 - 1.5 * Math.sin(t * 1.3), 18 + 3 * Math.sin(t * 1.3));
    head('b3', 3.5 + 1.8 * Math.sin(t * 1.1), 0); idleArms('g3', t, 1); head('g3', -2.5 - 1.2 * Math.sin(t * .9 + 1), 0);
    face('g3', t > SH.s3 - 2 ? 2 : 0, 3); },
  s4(t, gt) { const tb = %(tb)s; $('d4c').setAttribute('display', t < tb ? 'inline' : 'none'); $('d4h').setAttribute('display', t >= tb && t < tb + .12 ? 'inline' : 'none'); $('d4o').setAttribute('display', t >= tb + .12 ? 'inline' : 'none');
    const [sx, sy] = shake(t, tb, .7, 26); cam('s4', lerp(1.0, 1.08, t / SH.s4), 270, 480, 480, sx, sy); flash('s4', t, [[tb + .75, .2], [tb + 1.05, .14]]); },
  s4r(t, gt) { cam('s4r', lerp(2.6, 2.9, t / SH.s4r), %(bx)s, %(by)s + 40, 400); face('b4', t < .12 ? 0 : 2, 3); $('b4B').setAttribute('display', t < .1 ? 'inline' : 'none');
    pose('b4', CLASP, SHOCK, (t - .05) / .28); head('b4', -1.5 + (Math.random() - .5) * 1.2, -3.5 * ease(t / .2)); breathe('b4', t, .012, 10, 0); },
  s5(t, gt) { const p = ease(t / 3.6), ph = t * Math.PI * 1.7, walking = 1 - ease((t - 3.4) / .3), step = Math.abs(Math.sin(ph)) * walking;
    const el = P('w5'); el.dataset.feet = lerp(610, %(df)s, p); el.dataset.s = lerp(.30, %(ds)s, p);
    place(el, 1.5 * Math.sin(ph) * walking, -6 * step, 1, 1.6 * Math.sin(ph) * walking);
    $('w5Body').setAttribute('transform', `skewX(${1.8 * Math.sin(ph + .6) * walking})`);
    head('w5', -1.4 * Math.sin(ph) * walking, 0); blinkAt('w5', t, 3.3, 1.2); $('w5M').setAttribute('display', 'none');
    const rt = %(ringt)s;
    if (t < rt - .3) { arm('w5', 'L', 7 * Math.sin(ph) * walking, -8); arm('w5', 'R', 7 * Math.sin(ph) * walking, 8); }
    else pose('w5', RELAX, RINGUP, (t - rt + .3) / .45);
 cam('s5', lerp(1.0, 1.12, t / SH.s5), 270, 560, 560); },
  s6(t, gt) { cam('s6', lerp(2.6, 2.95, t / SH.s6), %(wfx)s, %(wfy)s + 70, 400); blinkAt('w6', t, 3.4, .9); const e = env('06e', gt);
    head('w6', 1.2 * Math.sin(t * .8) + 3 * e, -1.6 * e); talk('w6', '06e', gt); breathe('w6', t, .004, 1.7, .5);
    const k0 = SH.s6 * .58; if (t < k0) idleArms('w6', t, 0); else pose('w6', RELAX, CHEST, (t - k0) / .4); },
  s6r(t, gt) { cam('s6r', lerp(2.8, 3.2, t / SH.s6r), %(bx)s, %(by)s + 40, 400); face('b6', t < .9 ? 2 : 1, 3); blinkAt('b6', t, .9, .5, t > 1.0 && t < 1.25);
    if (t < 1.1) pose('b6', SHOCK, SHOCK, 1); else pose('b6', SHOCK, CLASP, (t - 1.1) / .7);
    head('b6', (Math.random() - .5) * (t < .9 ? 1.6 : .5) + (t > .9 ? -3 * ease((t - .9) / .6) : 0), 0); breathe('b6', t, t < 1 ? .012 : .007, t < 1 ? 9 : 4, 0); },
  s7a(t, gt) { const tp = %(gpt)s, v = t - .3; blinkAt('g7', t, 2.6, 1.2); const e = env('07g', gt); talk('g7', '07g', gt);
    const z = lerp(2.1, 2.4, ease(t / tp)) + (t > tp ? .35 * backOut((t - tp) / .3) : 0); const [sx, sy] = shake(t, tp, .45, 7);
    cam('s7a', z, %(gx)s, %(gy)s + 110, 420, sx, sy);
    let ph;
    if (v < 3.0) { ph = 'panic'; face('g7', 3, 4);   // ลนลาน: ยกสองมือขึ้นห้าม มือสั่น หัวส่าย ตัวเอนหลัง
      const c = backOut((t - .15) / .35), j = 3 * Math.sin(t * 17);
      arm('g7', 'L', lerp(0, 65, c) + j, lerp(0, -205, c) + j); arm('g7', 'R', lerp(-6, -65, c) - j, lerp(22, 205, c) - j);
      head('g7', 5 * Math.sin(t * 6.5) + 3 * e, -2 * e); place(P('g7'), 0, 0, 1 + .006 * Math.sin(t * 9), 2.4); }
    else if (v < 4.0) { ph = 'laugh'; face('g7', 2, 4);   // หัวเราะกลบเกลื่อน: ลดมือลง ถูมือ หัวเอียง ไหล่ขยับ
      const c = ease((v - 3.0) / .4), j = 4 * Math.sin(t * 14);
      arm('g7', 'L', lerp(65, 15, c) + j, lerp(-205, -70, c)); arm('g7', 'R', lerp(-65, -15, c) - j, lerp(205, 70, c));
      head('g7', -6 + 2 * Math.sin(t * 12), -1.5 + Math.abs(Math.sin(t * 12)) * -1.5); place(P('g7'), 0, Math.abs(Math.sin(t * 12)) * -2, 1, -1); }
    else if (t < tp - .35) { ph = 'explain'; face('g7', 0, 4);   // อธิบาย: มือขวาผายไปทางประตูเป็นจังหวะตามเสียง มือซ้ายถูกับมือ
      const c = ease((v - 4.0) / .4), beat = 8 * e;
      arm('g7', 'L', 15 + 2 * Math.sin(t * 3), -70); arm('g7', 'R', lerp(-15, -34, c) - beat, lerp(70, 34, c) - beat * 1.5);
      head('g7', lerp(-6, 3, c) + 3 * e + 1.2 * Math.sin(t * 2), -1.5 * e); place(P('g7'), 0, 0, 1, lerp(-1, .8, c)); }
    else { ph = 'rage'; face('g7', 1, 4);   // โกรธ: ง้างแล้วชี้ไล่แรง ตัวพุ่งไปข้างหน้า หัวกระแทกตามคำ
      const wind = -16 * Math.sin(Math.PI * Math.min(1, Math.max(0, (t - tp + .35) / .25)));
      const a = t < tp ? wind : lerp(0, 76, backOut((t - tp) / .3)) + (t > tp + .35 ? 3 * Math.sin(t * 15) : 0);
      arm('g7', 'L', a, t < tp ? -38 : -4); arm('g7', 'R', lerp(-34, -10, ease((t - tp + .35) / .3)), lerp(34, 40, ease((t - tp + .35) / .3)) + 6 * e);
      head('g7', 4 * e + 2 * Math.sin(t * 11) * e, -3 * e - 1.5); place(P('g7'), 0, 0, 1 + .01 * e, -3.2); }
  },
  s7b(t, gt) { cam('s7b', lerp(1.35, 1.45, t / SH.s7b), 270, 590, 480); const p = ease(t / 2.2), ph = t * Math.PI * 2, step = Math.abs(Math.sin(ph)) * (1 - p);
    const el = P('k7'); el.dataset.x = lerp(600, 316, p); place(el, 0, -5 * step, 1, 1.2 * Math.sin(ph) * (1 - p));
    if (t < 2.2) { arm('k7', 'L', 8 * Math.sin(ph) * (1 - p), -6); arm('k7', 'R', -8 * Math.sin(ph) * (1 - p), 6); } else pose('k7', RELAX, [38, -24, 0, 5], (t - 2.2) / .4);
    blinkAt('w7', t, 3.1, .3); blinkAt('k7', t, 4.2, 1.1); head('w7', -4 * ease((t - 1.8) / .5), 0); $('w7M').setAttribute('display', 'none');
    if (t < 2.3) idleArms('w7', t, 2); else pose('w7', RELAX, [-6, -40, 4, 20], (t - 2.3) / .35); place(P('w7'), 0, 0, 1, t > 2.3 ? -1.2 : 0); },
  s8(t, gt) { cam('s8', lerp(1.7, 1.95, t / SH.s8), 270, 600, 430); head('w8', lerp(-5, 1, ease((t - 1.2) / 1.6)), 0); blinkAt('w8', t, 3.6, 2.4); blinkAt('k8', t, 4.0, .6);
    $('w8M').setAttribute('display', 'none'); pose('k8', [38, -24, 0, 5], [38, -24, 0, 5], 1); pose('w8', [-6, -40, 4, 20], [-6, -40, 4, 20], 1); breathe('w8', t, .004, 1.6, .4); },
  s9(t, gt) { cam('s9', lerp(4.6, 5.1, t / SH.s9), %(wfx)s, %(wfy)s + 6, 380); blinkAt('w9', t, 3.9, 2.8); const e = env('09e', gt);
    head('w9', .8 * Math.sin(t * .7) + 2.5 * e, -1.4 * e); talk('w9', '09e', gt); flash('s9', t, [[2.1, .18]]); },
  s9r(t, gt) { cam('s9r', lerp(3.0, 3.6, t / SH.s9r), %(bx)s, %(by)s + 40, 400); face('b9', 1, 3); blinkAt('b9', t, 1.3, .9);
    pose('b9', CLASP, [-26, -132, 10, 140], (t - .4) / .5); head('b9', -2 + (Math.random() - .5) * .8, Math.sin(t * 7) * .8);
    breathe('b9', t, .01, 7, 0); $('b9T').setAttribute('display', t > .8 ? 'inline' : 'none');
  },
  s2(t, gt) { const k = ease(t / SH.s2); cam('s2', lerp(1.55, 1.08, k), 270, lerp(230, 560, k), lerp(330, 470, k)); },
  s10(t, gt) { cam('s10', lerp(2.2, 2.7, ease(t / SH.s10)), %(bx)s, %(by)s + 40, 380); face('b10', 1, 3); blinkAt('b10', t, 2.8, .6);
    pose('b10', CLASP, CLASP, 1); arm('b10', 'L', -12 + 1.5 * Math.sin(t * 2), -18 - 4 * Math.sin(t * 2)); arm('b10', 'R', 12 - 1.5 * Math.sin(t * 2), 18 + 4 * Math.sin(t * 2));
    head('b10', t < 2 ? 4 * ease(t / .6) : t < 4 ? lerp(4, -5, ease((t - 2) / .5)) : lerp(-5, 1, ease((t - 4) / .6)), 0); breathe('b10', t, .008, 4, 0); },
  s11(t, gt) { cam('s11', lerp(1.9, 2.05, t / SH.s11), lerp(400, 450, ease(t / SH.s11)), 640, 420); },
  s12(t, gt) { cam('s12', lerp(3.0, 3.4, t / SH.s12), %(mx)s, %(my)s + 20, 380); head('m12', 2 * Math.sin(t * 1.4) + (t > 1 && t < 2.4 ? 3 * Math.sin((t - 1) * 9) : 0), 0); breathe('m12', t, .004, 1.6, .4); },
  s13(t, gt) { cam('s13', lerp(1.85, 2.05, t / SH.s13), %(px)s, %(py)s + 70, 380); head('p13', t < 1.6 ? 2 * Math.sin(t * 2) : lerp(0, -7, ease((t - 1.6) / .4)) + 1.5 * Math.sin(t * 7), t > 1.6 ? -2 : 0);
    breathe('p13', t, .006, 3, -.6); },
  s14(t, gt) { cam('s14', lerp(3.2, 3.6, t / SH.s14), %(sx)s, %(sy)s + 20, 380); head('t14', t < SH.s14 * .55 ? -2 + Math.sin(t * 1.2) : lerp(-2, 8, ease((t - SH.s14 * .55) / .6)), t > SH.s14 * .55 ? 1.5 : 0);
    breathe('t14', t, .004, 1.5, .3); },
  s15(t, gt) { cam('s15', lerp(1.0, 1.06, t / SH.s15), 270 + 3 * Math.sin(t * .9), 470 + 4 * Math.sin(t * 1.3), 470);
    const pin = [2, 5, 8, 0], tt = [.9, 1.45, 2.0, 2.55], KF = [[0, 330, 600, 0]];   // พิมพ์รหัสสี่ตัว แล้วปลดล็อกเข้าอัลบั้ม
    pin.forEach((d, i) => { const [x, y] = d ? KEYXY(d) : [270, 576]; KF.push([tt[i] - .25, x, y, 0], [tt[i], x, y, 1]); }); KF.push([3.2, 340, 610, 0], [SH.s15, 330, 610, 0]);
    thumb(15, KF, t); for (let i = 0; i < 4; i++) $('pd15_' + i).setAttribute('fill', t > tt[i] ? (t > 2.8 ? '#6fe0a0' : '#c9a8ff') : 'none');
    $('al15').setAttribute('opacity', Math.max(0, Math.min(1, (t - 3.0) / .35)).toFixed(2)); },
  s16(t, gt) { cam('s16', lerp(1.02, 1.12, ease(t / SH.s16)), 270 + 2 * Math.sin(t * .8), 450 + 3 * Math.sin(t * 1.1), 470);
    const sw = [[.8, 1.3, 0, -110], [3.0, 3.5, -110, -222]];   // ปัดขึ้นสองครั้ง จอเลื่อนตามแบบมีแรงเหวี่ยง
    let sy = 0; for (const [a, b, f, to] of sw) { if (t >= a) sy = lerp(f, to, 1 - Math.pow(1 - Math.min(1, (t - a) / (b - a + .5)), 3)); }
    $('a16').setAttribute('transform', `translate(0,${sy.toFixed(1)})`);
    thumb(16, [[0, 330, 600, 0], [.6, 300, 600, 0], [.8, 300, 600, 0], [1.25, 300, 470, 0], [1.6, 330, 600, 0], [2.8, 300, 600, 0], [3.0, 300, 600, 0], [3.45, 300, 470, 0], [3.9, 335, 605, 0], [SH.s16, 335, 605, 0]], t);
    $('a16HL').setAttribute('opacity', t > SH.s16 - 2.2 ? (.6 + .4 * Math.sin(t * 6)).toFixed(2) : 0); },
  s17(t, gt) { const tp = .4 + VD['17f'] * .55, [sx, sy] = shake(t, tp, .4, 9); cam('s17', 1.04 + (t > tp ? .14 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy); flash('s17', t, [[tp, .12]]);
    $('a17').setAttribute('transform', 'translate(0,-222)'); $('a17HL').setAttribute('opacity', .9);
    thumb(17, [[0, 335, 605, 0], [.35, 344, 566, 0], [.55, 344, 566, 1], [1.0, 330, 640, 0], [SH.s17, 330, 640, 0]], t);   // แตะรูปปี 2025 แล้วรูปขยายเต็มจอ
    const o = ease((t - .65) / .35); $('ly17').setAttribute('opacity', o.toFixed(2));
    $('ly17').setAttribute('transform', `translate(${lerp(344, 270, o).toFixed(1)},${lerp(566, 400, o).toFixed(1)}) scale(${lerp(.3, 1, o).toFixed(3)}) translate(-270,-400)`); },
  s18(t, gt) { cam('s18', lerp(1.0, 1.05, t / SH.s18), 270 + 3 * Math.sin(t), 470 + 3 * Math.sin(t * 1.4), 470);
    const W = ['ชื่อ', 'เจ้าสาว', ' ', '2025', ' ', 'หาย'], t0 = .35, dt = .22, nT = W.length, done = t0 + nT * dt;   // พิมพ์ค้นหาทีละคำ นิ้วกดคีย์บอร์ดตามจังหวะ
    $('q18').textContent = W.slice(0, Math.max(0, Math.min(nT, Math.floor((t - t0) / dt) + 1))).join('').trim();
    $('cur18').setAttribute('x', (183 + $('q18').getComputedTextLength()).toFixed(1)); $('cur18').setAttribute('opacity', (t * 2) %% 1 < .6 ? 1 : 0);
    const KF = [[0, 330, 610, 0]]; for (let i = 0; i < nT; i++) { const x = 175 + ((i * 97) %% 200), y = 496 + ((i * 53) %% 3) * 40; KF.push([t0 + i * dt - .14, x, y, 0], [t0 + i * dt, x, y, 1]); }
    KF.push([done + .2, 270, 615, 0], [done + .45, 270, 615, 1], [done + 1, 330, 640, 0], [SH.s18, 330, 640, 0]); thumb(18, KF, t);
    const kd = ease((t - done - .55) / .35); $('kb18').setAttribute('transform', `translate(0,${(190 * kd).toFixed(1)})`);
    for (let i = 0; i < 5; i++) $('r18_' + i).setAttribute('opacity', Math.max(0, Math.min(1, (t - done - .7 - i * .15) / .25)).toFixed(2)); },
  s19(t, gt) { const tp = .4 + VD['19f'] * .25, [sx, sy] = shake(t, tp, .45, 10); cam('s19', 1.03 + (t > tp ? .16 * backOut((t - tp) / .3) : 0), 270, 420, 470, sx, sy);
    for (let i = 0; i < 6; i++) { const u = (t - .25 - i * .28) / .3, e = Math.max(0, Math.min(1, u)); const g = $('ms19_' + i); if (!g) continue;   // โปสเตอร์คนหายขึ้นทีละใบ
      g.setAttribute('opacity', e.toFixed(2)); }
    const sy2 = -70 * ease((t - 2.6) / .8); $('ms19').setAttribute('transform', `translate(0,${sy2.toFixed(1)})`);
    thumb(19, [[0, 330, 620, 0], [2.4, 300, 610, 0], [2.6, 300, 610, 0], [3.2, 300, 520, 0], [3.7, 335, 625, 0], [SH.s19, 335, 625, 0]], t);
    $('s19k').setAttribute('opacity', Math.max(0, (t - SH.s19 + .5) / .5).toFixed(2)); },
  s20(t, gt) { const dings = [.5, .5 + (SH.s20 - 1.2) / 2.4, .5 + (SH.s20 - 1.2) / 1.2]; let bump = 0, look = 0;
    for (const d of dings) { if (t > d && t < d + .5) { bump = 4 * Math.sin((t - d) * 20) * (1 - (t - d) / .5); } if (t > d) look = Math.max(look, 1 - Math.min(1, (t - d) / 1.4)); }
    cam('s20', lerp(1.0, 1.12, ease(t / SH.s20)), 270, 640, 520, 0, bump); face('b20', 1, 3); blinkAt('b20', t, 2.4, .3);
    pose('b20', CLASP, CLASP, 1); arm('b20', 'L', -12 + 2 * Math.sin(t * 3), -18 - 4 * Math.sin(t * 3)); arm('b20', 'R', 12, 18 + 4 * Math.sin(t * 3));
    head('b20', 3 * Math.sin(t * 1.7), -4 * look); breathe('b20', t, .01, 6, 0); },
  s21(t, gt) { const vib = t > .2 && t < SH.s21 - .5 && (t * 1.25) %% 1 < .45; cam('s21', 1.02, 270 + (vib ? 2.5 * Math.sin(t * 90) : 0), 470, 470);
    const pr = (t * .8) %% 1; $('ring21').setAttribute('r', (44 + 26 * pr).toFixed(1)); $('ring21').setAttribute('opacity', (1 - pr).toFixed(2));
    const tr = 1.5 * Math.sin(t * 23);   // นิ้วโป้งสั่นลังเล แล้วค่อย ๆ เลื่อนไปกดรับสาย
    thumb(21, [[0, 300, 630, 0], [SH.s21 - 1.1, 310 + tr, 610, 0], [SH.s21 - .55, 330, 560, 0], [SH.s21 - .4, 330, 560, 1], [SH.s21, 330, 575, 0]], t); },
  s22(t, gt) { cam('s22', lerp(1.0, 1.12, t / SH.s22), 270, 470, 480); blinkAt('w22', t, 3.6, 1.0); const e = env('22f', gt); talk('w22', '22f', gt);
    head('w22', -3 + 1.2 * Math.sin(t * .7) + 2 * e, -1.2 * e); arm('w22', 'L', 1.5 * Math.sin(t), -5); arm('w22', 'R', -100, 219); breathe('w22', t, .004, 1.5, .3); },
  s23(t, gt) { cam('s23', lerp(1.55, 1.75, t / SH.s23), 270, 400, 440); blinkAt('w23', t, 4.1, 2.2); const e = env('23f', gt); talk('w23', '23f', gt);
    head('w23', -2 + .8 * Math.sin(t * .6) + 1.5 * e, -1 * e); arm('w23', 'L', 1.5 * Math.sin(t), -5); arm('w23', 'R', -100, 219); breathe('w23', t, .003, 1.4, .2); },
  s24(t, gt) { let j = 0; for (const k of KNOCKS) if (t > k && t < k + .12) j = 3 * (1 - (t - k) / .12); cam('s24', 1.0, 270, 480, 480, 0, j); },
  s25(t, gt) { cam('s25', lerp(1.0, 1.18, ease(t / SH.s25)), 270, 420, 440); face('g25', 2, 3); blinkAt('g25', t, 4.4, 1.6); const e = env('25f', gt); talk('g25', '25f', gt);
    head('g25', 3 + 2 * e + .8 * Math.sin(t * .6), -1.2 * e); arm('g25', 'L', 0, -5); arm('g25', 'R', 0, 5); place(P('g25'), 0, 0, 1, .8 * Math.sin(t * .5));
    flash('s25', t, [[SH.s25 - .35, .3]]); },
  s26(t, gt) { cam('s26', lerp(1.0, 1.15, ease(t / SH.s26)), 300, 440, 440); face('b26', 2, 3); blinkAt('b26', t, 9, .2); flash('s26', t, [[.02, .25], [.42, .14]]);
    pose('b26', CLASP, CHEST, t / .4); head('b26', -2 + (Math.random() - .5) * .8, Math.sin(t * 9) * .8); breathe('b26', t, .012, 9, 0);
    place(P('b26'), 0, -14 * ease(t / 1.2), 1 - .04 * ease(t / 1.2), 0); $('s26k').setAttribute('opacity', Math.max(0, (t - SH.s26 + .6) / .6).toFixed(2)); },
  s27(t, gt) { const k = Math.floor(Math.max(0, t - 1.0) / 1.4), a = t < 1.0 ? -1 : k %% 2;
    for (const [i, id] of [[0, 'optA'], [1, 'optB']]) { const on = a === i; $(id).setAttribute('transform', `translate(270,${i ? 560 : 470}) scale(${on ? 1.04 : 1})`);
      $(id + 'R').setAttribute('fill', on ? '#2a1f44' : '#120e1c'); $(id + 'R').setAttribute('stroke', on ? '#e2d2ff' : '#6a5aaa'); $(id + 'R').setAttribute('stroke-width', on ? 3 : 1.5); }
    $('s27in').setAttribute('opacity', Math.min(1, t / .6).toFixed(2)); },
};
window.renderAt = function (gt) {
  let cur = null;
  for (const k of Object.keys(SH)) { if (gt >= T0[k] && gt < T0[k] + SH[k]) cur = k; }
  if (!cur) cur = Object.keys(SH).pop();
  document.querySelectorAll('svg.shot').forEach(s => s.setAttribute('display', s.id === cur ? 'inline' : 'none'));
  document.querySelectorAll('.place').forEach(el => { if (!el.dataset.init) { el.dataset.init = 1; place(el); } });
  R[cur](gt - T0[cur], gt); filmFX(cur, gt);
  for (const [a, b, id] of SUBS) $(id).setAttribute('display', gt >= a && gt < b ? 'inline' : 'none');
  // ป้ายเวลาแบบตอนแรก: นาฬิกาเดิน หลังประตูเปิดจุดเป็นสีแดงกะพริบ และป้ายเหตุการณ์แดงเลื่อนเข้ามา
  let mins = gt < T0.s15 ? Math.floor(gt / 3.2) : gt < T0.s20 ? 160 + Math.floor((gt - T0.s15) / 3) : gt < T0.s24 ? 281 + Math.min(17, Math.floor((gt - T0.s20) / 2.5)) : 299;
  const hh = 19 + Math.floor(mins / 60), mm = mins %% 60;
  $('hudTxt').textContent = hh + ':' + String(mm).padStart(2, '0');
  const card = cur === 's27'; $('hud').setAttribute('display', card ? 'none' : 'inline'); $('wm').setAttribute('opacity', card ? Math.max(0, .85 - (gt - T0.s27) / .5).toFixed(2) : .85);
  let et = null; for (const E of EVT) if (gt >= E[0]) et = E;
  if (et) { if ($('evtTxt').textContent !== et[1]) { $('evtTxt').textContent = et[1]; $('evtR').setAttribute('width', ($('evtTxt').getComputedTextLength() + 44).toFixed(0)); } }
  $('hudDot').setAttribute('fill', gt < BANG ? '#9a86ff' : ((gt * 2) %% 1 < .5 ? '#ff3b4e' : '#5a1520'));
  const ev = et ? ease((gt - et[0]) / .4) : 0; $('evt').setAttribute('opacity', ev.toFixed(2)); $('evt').setAttribute('transform', `translate(${(-14 * (1 - ev)).toFixed(1)},0)`);
  // ความไว้ใจ: ขึ้นกลางบนแว้บเดียวตอนลดลง ตัวเลขนับลง แล้วจางหาย
  let tr = null; for (const T of TRUST) if (gt >= T[0] && gt < T[0] + 2.6) tr = T;
  if (tr) { const u = gt - tr[0], o = Math.min(1, u / .25) * Math.min(1, (2.6 - u) / .4), pct = tr[1] + (tr[2] - tr[1]) * ease((u - .3) / .7);
    $('trustT').setAttribute('opacity', o.toFixed(2)); $('trustT').setAttribute('transform', `translate(0,${(-8 * (1 - Math.min(1, u / .3))).toFixed(1)})`);
    $('trustPct').textContent = Math.round(pct) + '%%'; $('trustDel').textContent = '▼ ' + (tr[1] - tr[2]); }
  else $('trustT').setAttribute('opacity', 0);
  // กราฟิกชี้แหวน (ช็อต 5): มุมกรอบหุบเข้าล็อกแหวน → เส้นประหักมุมค่อย ๆ ลากขึ้น → การ์ด → แหวนของเธอ = แหวนของคุณ → MATCH นับถึงร้อย
  const tt = gt - T0.s5 - RT5;
  if (cur !== 's5' || tt < .1) $('callout').setAttribute('opacity', 0);
  else {
    const fo = Math.max(0, Math.min(1, (SH.s5 - RT5 - tt) / .35)); $('callout').setAttribute('opacity', (Math.min(1, (tt - .1) / .15) * fo).toFixed(2));
    const rr = $('w5Ring').getBoundingClientRect(), st = $('stage').getBoundingClientRect(), x0 = rr.x + rr.width / 2 - st.x, y0 = rr.y + rr.height / 2 - st.y;
    const sc = 1 + 1.2 * (1 - backOut((tt - .1) / .35)); $('coBr').setAttribute('transform', `translate(${x0.toFixed(1)},${y0.toFixed(1)}) scale(${sc.toFixed(3)})`);
    $('coDot').setAttribute('cx', x0.toFixed(1)); $('coDot').setAttribute('cy', y0.toFixed(1));
    const P = [[x0 + 22, y0 - 21], [330, y0 - 89], [330, 424]], seg = [Math.hypot(P[1][0] - P[0][0], P[1][1] - P[0][1]), Math.hypot(P[2][0] - P[1][0], P[2][1] - P[1][1])];
    let d = (seg[0] + seg[1]) * ease((tt - .45) / .55), path = `M ${P[0][0].toFixed(1)},${P[0][1].toFixed(1)}`;
    if (d > 0) { const k = Math.min(1, d / seg[0]); path += ` L ${(P[0][0] + (P[1][0] - P[0][0]) * k).toFixed(1)},${(P[0][1] + (P[1][1] - P[0][1]) * k).toFixed(1)}`;
      if (d > seg[0]) { const k2 = Math.min(1, (d - seg[0]) / seg[1]); path += ` L 330,${(P[1][1] + (424 - P[1][1]) * k2).toFixed(1)}`; } }
    $('coLine').setAttribute('d', path);
    const c = Math.max(0, Math.min(1, (tt - .95) / .25)); $('coCard').setAttribute('opacity', c.toFixed(2)); $('coCard').setAttribute('transform', `translate(300,424) scale(${(.9 + .1 * backOut((tt - .95) / .3)).toFixed(3)}) translate(-300,-424)`);
    const pop = (id, t0, cx) => { const o = Math.max(0, Math.min(1, (tt - t0) / .2)), e = Math.max(.01, backOut((tt - t0) / .35));
      $(id).setAttribute('opacity', o.toFixed(2)); $(id).setAttribute('transform', `translate(${cx},330) scale(${e.toFixed(3)})`); };
    pop('coA', 1.25, 222); pop('coB', 1.7, 378);
    $('coEq').setAttribute('opacity', Math.max(0, Math.min(1, (tt - 1.55) / .2)).toFixed(2));
    $('coM').textContent = 'MATCH ' + Math.round(100 * ease((tt - 1.9) / .6)) + '%%';
  }
};
'''
js = JS % dict(shots=json.dumps(dict(SHOTS)), t0=json.dumps(T0), env=json.dumps(ENV), vat=json.dumps(VOICE_AT), subs=json.dumps(subs), fps=FPS,
               cx3=(BX + GX) / 2, cy3=BY + 60, tb=TB, bx=BX, by=BY + 40, gx=GX, gy=GY, df=SB.DOOR_FEET, ds=SB.DOOR_S, ringt=.4 + D['05c'] * .55,
               wfx=WF[0], wfy=WF[1], gpt=G7_POINT, zb=json.dumps(ZB_T), shakes=json.dumps(SHAKES), mx=MX, my=MY, px=PX, py=PY, sx=SX, sy=SY, vd=json.dumps(D), knocks=json.dumps(KNOCKS), evt=json.dumps(EVT, ensure_ascii=False), trust=json.dumps(TRUST), bang=T0['s4'] + TB)

base = SB.N9.H8.S.DEFS
for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
    base = re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=re.S)
DEFS = ((CL.defs({**LIGHTS, 'bg': BG_L}) if LIGHT else '') + base + SB.H8.DEFS_EXTRA + SB.N9.EXTRA_DEFS + WC.DEFS + SB.B2.DEFS + SP.DEFS + SB.P2.DEFS2 + SB.EXTRA_DEFS + SB.CHAR_DEFS
        + f'<svg width="0" height="0" style="position:absolute"><defs>{gh}{gp}</defs></svg>')
html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@600&family=IBM+Plex+Mono:wght@500&display=swap">'
        '<style>html,body{margin:0;background:#000}#stage{position:relative;width:540px;height:960px;overflow:hidden}#stage svg{position:absolute;inset:0;width:540px;height:960px;transform-origin:50% 50%}#grRect,#grGrain{mix-blend-mode:soft-light}'
        '.th{font-family:"IBM Plex Sans Thai";font-weight:700;font-size:20px;fill:#ffffff;stroke:#12081c;stroke-width:5px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}'
        '.hp{fill:#ffd84a}.hr{fill:#ffd84a}.en{font-family:Inter,sans-serif;font-weight:600;font-size:13px;fill:#fff;stroke:#14121a;stroke-width:3.4px;paint-order:stroke;stroke-linejoin:round;text-anchor:middle}</style>'
        + DEFS + '<div id="stage">' + ''.join(SVGS) + GRADE + f'<svg viewBox="0 0 540 960">{OVL}{"".join(sub_svg)}</svg></div><script>{js}</script>')
open('anim_full.html', 'w').write(html)
os.makedirs('bg', exist_ok=True)
bg_html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600&family=IBM+Plex+Mono:wght@500&display=swap"><style>html,body{margin:0}svg{display:block}</style>'
           + DEFS + ''.join(f'<svg id="{k}" viewBox="0 0 540 960" width="540" height="960">{v}</svg>' for k, v in BG.items()))
open('bg_full_lit.html' if LIGHT else 'bg_full.html', 'w').write(bg_html)

# ---------------------------------------------------------------- เสียง
N = int((TOTAL + 1) * A.SR)
voice = np.zeros(N, np.float32)
for k, at in VOICE_AT.items(): A.add(voice, at, VO[k])
bang_t = T0['s4'] + TB
SH_D = dict(SHOTS)
music_w = A.bridal_chorus(N, 0.0, bang_t)
cl = A.claps(N, T0['s3'] + .1, T0['s3'] + 2.6)
sfx = np.zeros(N, np.float32)
A.add(sfx, bang_t, A.door_bang()); A.add(sfx, bang_t + .75, A.thunder(5.0, 1.0)); A.add(sfx, T0['s9'] + 2.1, A.thunder(4.0, 1.4), .8)
A.add(sfx, T0['s6r'] + .05, A.sting(), .8); A.add(sfx, T0['s9r'] + .2, A.boom(2.6, 46), .5)
steps = A.footsteps(N, T0['s5'] + .1, T0['s5'] + 3.5, 1.7, .55) + A.footsteps(N, T0['s7b'] + .05, T0['s7b'] + 2.2, 2.0, .45)
rn = A.rain(N, bang_t + .9)
# เสียงจริงจาก sfx/*.mp3 (gen_sfx.py) ถ้ามี ใช้แทนเสียงสังเคราะห์
def real(name): f = f'sfx/{name}.mp3'; return A.load_voice(f, .1) if os.path.exists(f) else None
def fit(x, n, fo=.4): x = x[:n].copy(); k = min(len(x), int(fo * A.SR)); x[-k:] *= np.linspace(1, 0, k); return x
R_ = {k: real(k) for k in ('applause', 'door_bang', 'thunder', 'rain', 'heels', 'guard_steps')}
if R_['applause'] is not None: cl = np.zeros(N, np.float32); A.add(cl, T0['s3'] + .1, fit(R_['applause'], int(2.6 * A.SR), .8))
if R_['door_bang'] is not None or R_['thunder'] is not None:
    sfx = np.zeros(N, np.float32)
    A.add(sfx, bang_t, R_['door_bang'] * 3 if R_['door_bang'] is not None else A.door_bang())
    th = R_['thunder'] * 3 if R_['thunder'] is not None else None
    A.add(sfx, bang_t + .75, th if th is not None else A.thunder(5.0, 1.0)); A.add(sfx, T0['s9'] + 2.1, th if th is not None else A.thunder(4.0, 1.4), .8)
    A.add(sfx, T0['s6r'] + .05, A.sting(), .8); A.add(sfx, T0['s9r'] + .2, A.boom(2.6, 46), .5)
if R_['heels'] is not None or R_['guard_steps'] is not None:
    steps = np.zeros(N, np.float32)
    A.add(steps, T0['s5'] + .1, fit(R_['heels'], int(3.4 * A.SR)) if R_['heels'] is not None else A.footsteps(N, 0, 3.4, 1.7, .55)[:int(3.4 * A.SR)])
    A.add(steps, T0['s7b'] + .05, fit(R_['guard_steps'], int(2.2 * A.SR)) if R_['guard_steps'] is not None else A.footsteps(N, 0, 2.2, 2.0, .45)[:int(2.2 * A.SR)])
if R_['rain'] is not None:
    r = R_['rain']; x = r[int(.5 * A.SR):]; k = int(1.0 * A.SR)  # วนลูปแบบเฟดซ้อน
    loop = np.zeros(N, np.float32); t = int((bang_t + .9) * A.SR); w = np.linspace(0, 1, k)
    while t < N: seg = x.copy(); seg[:k] *= w; seg[-k:] *= w[::-1]; n = min(len(seg), N - t); loop[t:t + n] += seg[:n]; t += len(seg) - k
    rn = loop
import score
thr = score.build(N, dict(bang=bang_t, s5=T0['s5'], s6=T0['s6'], s6r=T0['s6r'], s7a=T0['s7a'], s7b=T0['s7b'], s8=T0['s8'], s9=T0['s9'], s9r=T0['s9r'], end=TOTAL))
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
v = rms(voice[np.abs(voice) > 1e-4])
def lvl(x, a, b, db): i0, i1 = int(a * A.SR), int(b * A.SR); return x * (v * 10 ** (-db / 20) / rms(x[i0:i1]))
music_w = lvl(music_w, .3, bang_t - .1, 8); thr = lvl(thr, bang_t + 1.5, TOTAL - 1, 8)
# เพลงจริงจาก ElevenLabs Music (gen_music.py) ถ้ามี ใช้แทนเพลงสังเคราะห์ ท่อนเพลงตั้งความยาวตามไทม์ไลน์ไว้แล้ว
def load_raw(f):
    import subprocess
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', f, '-f', 's16le', '-ac', '1', '-ar', str(A.SR), '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
# ผู้ใช้สั่ง: ช่วงเปิดเรื่องถึงงานแต่งต้องเป็นทำนอง Bridal Chorus (Here Comes the Bride) จึงใช้ออร์แกนที่เรียบเรียงเองแทน A_wedding
if os.environ.get('AI_WEDDING') and os.path.exists('music/A_wedding.mp3'):
    w = load_raw('music/A_wedding.mp3'); music_w = np.zeros(N, np.float32); A.add(music_w, 0, w)
    k = int(.06 * A.SR); i = int(bang_t * A.SR); music_w[i:i + k] *= np.linspace(1, 0, k); music_w[i + k:] = 0   # ตัดฉับตรงเสียงปัง
    music_w = lvl(music_w, .5, bang_t - .2, 8)
if os.path.exists('music/B_thriller.mp3'):
    b = load_raw('music/B_thriller.mp3'); thr = np.zeros(N, np.float32); A.add(thr, bang_t + 1.4, b)
    i1 = int(T0['s10'] * A.SR); k = int(1.2 * A.SR); thr[i1 - k // 2:i1 + k // 2] *= np.linspace(1, 0, k); thr[i1 + k // 2:] = 0
    thr = lvl(thr, bang_t + 2, T0['s10'] - 1, 8); rn = lvl(rn, bang_t + 2, T0['s10'] - 1, 22); cl = lvl(cl, T0['s3'] + .4, T0['s3'] + 2.3, 16)
steps = lvl(steps, T0['s5'] + .2, T0['s5'] + 3.3, 10)
SR = A.SR
def knock():
    n = int(.25 * SR); x = np.arange(n) / SR
    s_ = np.sin(2 * np.pi * 150 * x) * np.exp(-x * 38) + .5 * np.sin(2 * np.pi * 360 * x) * np.exp(-x * 55)
    s_ = s_ + A.bp(A.rng.standard_normal(n).astype(np.float32), 300, 2500) * np.exp(-x * 70) * .7
    return A.reverb(s_.astype(np.float32), .5, .2)
def ding(f=1318.5):
    n = int(1.6 * SR); x = np.arange(n) / SR
    return ((np.sin(2 * np.pi * f * x) + .4 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 4)) * np.exp(-x * 2.5) * .22).astype(np.float32)
def buzz(dur=.45):
    n = int(dur * SR); x = np.arange(n) / SR
    s_ = (np.sign(np.sin(2 * np.pi * 150 * x)) * .5 + np.sin(2 * np.pi * 300 * x)).astype(np.float32)
    return (A.bp(s_, 120, 1500) * A.env_adsr(n, .02, .05) * .12).astype(np.float32)
def click():
    n = int(.04 * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * x) * np.exp(-x * 160) * .35).astype(np.float32)
def whoosh(dur=.6):
    n = int(dur * SR); x = np.arange(n) / SR
    return (A.bp(A.rng.standard_normal(n).astype(np.float32), 300, 2500) * np.sin(np.pi * x / dur) ** 2 * .5).astype(np.float32)
sfx2 = np.zeros(N, np.float32)
for b in ZB_T: A.add(sfx2, b - .3, whoosh(.65), .9)
A.add(sfx2, T0['s6r'], A.boom(2.4, 50), .6); A.add(sfx2, TW22, A.boom(2.6, 46), .8)
A.add(sfx2, T0['s17'] + .4 + D['17f'] * .55, A.boom(2.6, 48), .9); A.add(sfx2, T0['s19'] + .4 + D['19f'] * .25, A.boom(2.8, 44), 1.0)
for k in range(3): A.add(sfx2, T0['s20'] + .5 + k * (SH_D['s20'] - 1.2) / 2.4, ding(), 1.0)
for k in range(4): A.add(sfx2, T0['s21'] + .2 + k * .8, buzz(), 1.0)
for kt in KNOCKS: A.add(sfx2, T0['s24'] + kt, knock(), 1.3)
th2 = R_['thunder'] * 3 if R_['thunder'] is not None else A.thunder(5.0, .9)
A.add(sfx2, T0['s25'] + SH_D['s25'] - .35, th2, 1.0)                      # ผู้ใช้สั่ง: ฟ้าผ่าอีกครั้งหลังสามีเรียกจบประโยค
A.add(sfx2, T0['s26'] + .3, A.boom(3.0, 42), .5)
for k in range(5): A.add(sfx2, T0['s27'] + 1.0 + k * 1.4, click(), 1.0)
if os.path.exists('music/C_night.mp3'):
    c_ = load_raw('music/C_night.mp3'); mc = np.zeros(N, np.float32)
    O = json.load(open('music/C_night_timeline.json'))['t0']   # ไทม์ไลน์ตอนแต่งเพลง: ตัดเป็นท่อนแล้ววางตามเวลาใหม่ ท่อนลิฟต์-สายเข้ายืดหดให้พอดี
    cut = lambda a, b: c_[int((O[a] - O['s10']) * A.SR):int((O[b] - O['s10']) * A.SR)] if b else c_[int((O[a] - O['s10']) * A.SR):]
    def stretch(x, n):
        import subprocess, tempfile
        f = len(x) / n
        if abs(f - 1) < .01: return x
        if f < .9:   # ยาวขึ้นมาก: วนท่อนกลางซ้ำแบบเฟดซ้อน แทนการยืดจนเสียงยาน
            k = int(.6 * A.SR); body = x[len(x) // 4:]; out = x.copy()
            while len(out) < n:
                w = np.linspace(0, 1, k); out = np.concatenate([out[:-k], out[-k:] * (1 - w) + body[:k] * w, body[k:]])
            return out[:n]
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-f', 'f32le', '-ar', str(A.SR), '-ac', '1', '-i', '-', '-filter:a', f'atempo={f:.4f}', '-f', 'f32le', '-'], input=x.astype(np.float32).tobytes(), capture_output=True).stdout
        return np.frombuffer(raw, np.float32)
    def put_xf(x, at):
        k = int(.25 * A.SR); x = x.copy(); x[:k] *= np.linspace(0, 1, k); x[-k:] *= np.linspace(1, 0, k); A.add(mc, at - .12, x)
    put_xf(cut('s10', 's20'), T0['s10']); put_xf(stretch(cut('s20', 's22'), int((T0['s22'] - T0['s20']) * A.SR)), T0['s20']); put_xf(cut('s22', None), T0['s22'])
    mc = lvl(mc, T0['s10'] + 1, T0['s26'], 9); thr = thr + mc
rn = A.lp(rn, 1200) * (10 ** (-12 / 20)) * 2.2   # ตัดเสียงแหลมแบบสังกะสีออก เหลือฝนทุ้ม ๆ ไกล ๆ เบากว่าเดิมราว 5 dB
venv = A.lp(np.abs(voice), 4); duck = 1 - .3 * np.clip(venv / (venv.max() * .25 + 1e-6), 0, 1)
mix = voice + (music_w + thr) * duck + cl + rn + steps + sfx * .35 + sfx2 * .35
fade = int(.7 * A.SR); end = int(TOTAL * A.SR); mix[end - fade:end] *= np.linspace(1, 0, fade); mix[end:] = 0
mix = np.tanh(mix * 1.3) / 1.3; mix = mix / (np.abs(mix).max() + 1e-6) * .9
os.makedirs('out', exist_ok=True)
with wave.open('out/full_audio.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(A.SR)
    w.writeframes(np.repeat((mix[:end] * 32767).astype(np.int16)[:, None], 2, axis=1).tobytes())
json.dump(dict(total=TOTAL, fps=FPS, shots=SHOTS, t0=T0, bang=bang_t), open('out/full_timeline.json', 'w'))
print(f'total {TOTAL:.1f}s · frames {int(TOTAL * FPS)} · arm parts {len(ARM_PARTS)}')
