"""EP.01 style test 3: warm cinematic medium shot (island wooden shop) + on-scene title graphics.
Technique only from the owner's references: medium framing, counter as foreground, wall close behind,
strong window light beams with dust, the character's shadow cast on the wall, soft background blur.
Run: python3 style3.py -> style3.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R
import kt_scenes as K
ISL = K.ISL
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'

# warm golden-hour rig for these shots (owner's references are warm)
CL.RIGS['golden'] = dict(rim='#ffcf96', rim_op=.95, rim_soft_op=.3, rim_w=2.4, bloom=.4,
                         amb='#6a4a5a', shade_op=.34, shade_k=14, shade_blur=10, face_shade=.18, chin_ao=.4,
                         sat=1.0, lift=(.02, .012, .02), gamma=(1.0, 1.02, 1.06), gain=(1.0, .97, .9), vig=.45, grain=.075)


def wood_planks(x, y, w, h, base='#a9785a', light='#bb8a68', dark='#946548', plank=46, seed=1, vertical=True):
    rnd = random.Random(seed)
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base}"/>'
    n = int(w / plank) + 1 if vertical else int(h / plank) + 1
    for i in range(n):
        if vertical:
            px = x + i * plank
            c = rnd.choice([base, light, base, dark])
            out += f'<rect x="{px}" y="{y}" width="{plank - 3}" height="{h}" fill="{c}"/><rect x="{px + plank - 3}" y="{y}" width="3" height="{h}" fill="#5e3e2c" opacity=".55"/>'
            for k in range(5):                                 # grain
                gx = px + rnd.uniform(4, plank - 8)
                out += f'<path d="M {gx:.0f},{y} C {gx + rnd.uniform(-6, 6):.0f},{y + h * .3:.0f} {gx + rnd.uniform(-6, 6):.0f},{y + h * .7:.0f} {gx + rnd.uniform(-4, 4):.0f},{y + h}" stroke="#6e4a34" stroke-width="1" fill="none" opacity=".18"/>'
            if rnd.random() < .4:
                ky = y + rnd.uniform(.1, .9) * h
                out += f'<ellipse cx="{px + plank / 2:.0f}" cy="{ky:.0f}" rx="4" ry="7" fill="#6e4a34" opacity=".35"/>'
        else:
            py = y + i * plank
            c = rnd.choice([base, light, base, dark])
            out += f'<rect x="{x}" y="{py}" width="{w}" height="{plank - 3}" fill="{c}"/><rect x="{x}" y="{py + plank - 3}" width="{w}" height="3" fill="#5e3e2c" opacity=".55"/>'
            for k in range(4):
                gy = py + rnd.uniform(4, plank - 8)
                out += f'<path d="M {x},{gy:.0f} C {x + w * .3:.0f},{gy + rnd.uniform(-4, 4):.0f} {x + w * .7:.0f},{gy + rnd.uniform(-4, 4):.0f} {x + w},{gy:.0f}" stroke="#6e4a34" stroke-width="1" fill="none" opacity=".16"/>'
    return out


def jar(x, y, w, h, fill, lid='#d8655a'):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w * .18:.1f}" fill="#eaf2f2" opacity=".55"/>'
            f'<rect x="{x + 2}" y="{y + h * .35:.0f}" width="{w - 4}" height="{h * .6:.0f}" rx="{w * .14:.1f}" fill="{fill}" opacity=".9"/>'
            f'<rect x="{x - 1}" y="{y - 6}" width="{w + 2}" height="8" rx="3" fill="{lid}"/>'
            f'<rect x="{x + 3}" y="{y + 4}" width="{w * .18:.1f}" height="{h - 10}" rx="2" fill="#fff" opacity=".45"/>')


def wall_props():
    rnd = random.Random(7)
    out = ''
    # left shelf: jars of sweets, instant noodles, bottles
    for sy in (330, 452):
        out += f'<rect x="-10" y="{sy}" width="180" height="10" fill="#7d553c"/><rect x="-10" y="{sy + 10}" width="180" height="5" fill="#5e3e2c" opacity=".6"/>'
        x = 0
        while x < 160:
            k = rnd.random()
            if k < .45:
                w, h = 26, rnd.randint(34, 46)
                out += jar(x, sy - h, w, h, rnd.choice(['#e88aa8', '#f0b46a', '#7fb07a', '#d8655a', '#c9a2e0']), rnd.choice(['#d8655a', '#2fb3b8', '#e8c35e']))
                x += w + 6
            elif k < .75:
                w, h = 22, 30
                c = rnd.choice(['#d8655a', '#2f6fb5', '#e8a43a', '#3fa06a'])
                out += f'<rect x="{x}" y="{sy - h}" width="{w}" height="{h}" rx="3" fill="{c}"/><rect x="{x}" y="{sy - h + 8}" width="{w}" height="6" fill="#fff" opacity=".7"/>'
                x += w + 4
            else:
                out += f'<path d="M {x + 6},{sy} L {x + 6},{sy - 30} C {x + 6},{sy - 40} {x + 3},{sy - 42} {x + 3},{sy - 50} L {x + 11},{sy - 50} C {x + 11},{sy - 42} {x + 8},{sy - 40} {x + 8},{sy - 30} L {x + 8},{sy} Z" fill="{rnd.choice(["#3fa06a", "#9fd6dc", "#c87a5e"])}" opacity=".9"/>'
                x += 16
    # right: clock, calendar, framed old photo of the pier, tin sign
    out += ('<g transform="translate(470,250)"><circle r="30" fill="#f4ede0" stroke="#5e3e2c" stroke-width="5"/>'
            + ''.join(f'<path d="M {22 * math.cos(a):.1f},{22 * math.sin(a):.1f} L {26 * math.cos(a):.1f},{26 * math.sin(a):.1f}" stroke="#5e3e2c" stroke-width="2"/>' for a in [i * math.pi / 6 for i in range(12)])
            + '<path d="M 0,0 L 0,-18 M 0,0 L 12,6" stroke="#2a1c18" stroke-width="3" stroke-linecap="round"/><circle r="3" fill="#2a1c18"/></g>'
            '<g transform="translate(410,330)"><rect x="0" y="0" width="74" height="96" fill="#fbf6ee"/><rect x="0" y="0" width="74" height="26" fill="#d8655a"/>'
            f'<text x="37" y="18" {TH} font-size="12" font-weight="700" fill="#fff" text-anchor="middle">ธันวาคม</text>'
            f'<text x="37" y="74" {EN} font-size="40" font-weight="800" fill="#d8655a" text-anchor="middle">14</text></g>'
            '<g transform="translate(430,450)"><rect x="-4" y="-4" width="96" height="76" fill="#5e3e2c"/><rect x="0" y="0" width="88" height="68" fill="#d9c8a8"/>'
            '<path d="M 0,44 L 88,44 L 88,68 L 0,68 Z" fill="#8fb5b8"/><path d="M 10,44 L 50,30 L 80,44 Z" fill="#9a8a70"/><rect x="40" y="38" width="30" height="8" fill="#6e5a48"/>'
            f'<text x="44" y="62" {TH} font-size="8" fill="#3a2a22" text-anchor="middle">ท่าเรือ ๒๕๒๙</text></g>'
            '<g transform="translate(60,520) rotate(-2)"><rect x="0" y="0" width="120" height="44" rx="4" fill="#2f6fb5"/>'
            f'<text x="60" y="20" {TH} font-size="13" font-weight="800" fill="#fff" text-anchor="middle">น้ำแข็งหลอด</text>'
            f'<text x="60" y="36" {TH} font-size="10" fill="#cfe3ff" text-anchor="middle">มีขาย</text></g>')
    return out


def window():
    # wooden window with bars, sea and sky beyond, shutters pushed open
    sky = ('<rect x="200" y="210" width="210" height="190" fill="#ffd9b0"/><rect x="200" y="300" width="210" height="100" fill="#f6c69a"/>'
           '<rect x="200" y="330" width="210" height="70" fill="#7fb8c4"/><path d="M 200,330 L 410,330 L 410,336 L 200,338 Z" fill="#ffe8cc"/>'
           '<path d="M 200,332 C 260,312 320,318 360,326 L 410,330 Z" fill="#6f9a7a" opacity=".85"/><circle cx="330" cy="292" r="22" fill="#fff4e4"/>')
    frame = ('<rect x="190" y="200" width="230" height="10" fill="#6e4a34"/><rect x="190" y="400" width="230" height="16" fill="#6e4a34"/>'
             '<rect x="190" y="200" width="10" height="210" fill="#6e4a34"/><rect x="410" y="200" width="10" height="210" fill="#6e4a34"/>'
             + ''.join(f'<rect x="{x}" y="210" width="7" height="190" fill="#7d553c"/><rect x="{x}" y="210" width="2" height="190" fill="#b88a64"/>' for x in range(228, 410, 30))
             + '<path d="M 190,204 L 160,214 L 160,404 L 190,414 Z" fill="#8a5e40"/>' + ''.join(f'<path d="M 162,{226 + k * 16} L 188,{220 + k * 16}" stroke="#6e4a34" stroke-width="3"/>' for k in range(11)))
    return sky + frame


def beams(x0, x1, angle_dx, top, bottom, n=4, op=.22, seed=3):
    rnd = random.Random(seed)
    out = ''
    for i in range(n):
        a = x0 + (x1 - x0) * i / n + rnd.uniform(-6, 6)
        w = rnd.uniform(18, 34)
        o = op * rnd.uniform(.6, 1.0)
        out += (f'<polygon points="{a:.0f},{top} {a + w:.0f},{top} {a + w + angle_dx:.0f},{bottom} {a + angle_dx:.0f},{bottom}" fill="url(#s3beam)" opacity="{o:.2f}" '
                'filter="url(#s3soft)" style="mix-blend-mode:screen"/>')
    return out


def shop_frame():
    fid = 'S3'
    defs = ('<linearGradient id="s3beam" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2d8" stop-opacity="1"/><stop offset="1" stop-color="#ffe2b8" stop-opacity="0"/></linearGradient>'
            '<filter id="s3soft" x="-30%" y="-10%" width="160%" height="120%"><feGaussianBlur stdDeviation="5"/></filter>'
            '<filter id="s3dof" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="1.3"/></filter>'
            '<filter id="s3sil" x="-20%" y="-20%" width="140%" height="140%"><feFlood flood-color="#3a2230"/><feComposite in2="SourceAlpha" operator="in"/><feGaussianBlur stdDeviation="6"/></filter>'
            '<radialGradient id="s3bulb"><stop offset="0" stop-color="#fff2d0" stop-opacity=".9"/><stop offset="1" stop-color="#ffcf96" stop-opacity="0"/></radialGradient>')
    wall = wood_planks(0, 0, 540, 640, seed=2)
    ceiling = '<rect x="0" y="0" width="540" height="70" fill="#6e4a34"/>' + ''.join(f'<rect x="{x}" y="0" width="22" height="80" fill="#5e3e2c"/>' for x in (40, 250, 470))
    bulbs = ''.join(f'<path d="M {x},70 L {x},120" stroke="#2a1c18" stroke-width="2"/><path d="M {x - 18},120 L {x + 18},120 L {x + 10},106 L {x - 10},106 Z" fill="#c4463d"/><circle cx="{x}" cy="128" r="7" fill="#fff4dc"/><circle cx="{x}" cy="128" r="46" fill="url(#s3bulb)" style="mix-blend-mode:screen"/>' for x in (130, 410))
    back = f'<g filter="url(#s3dof)">{wall}{ceiling}{window()}{wall_props()}</g>' + bulbs
    # window light patch on the wall + beams
    patch = ('<g opacity=".55" style="mix-blend-mode:screen" filter="url(#s3soft)">' + ''.join(f'<polygon points="{230 + k * 30},420 {252 + k * 30},420 {300 + k * 30},640 {276 + k * 30},640" fill="#fff0d0"/>' for k in range(5)) + '</g>')
    light = beams(200, 400, 170, 205, 960, 7, .4) + CL.glow(320, 300, 260, '#ffd9a8', .32) + CL.dust((180, 220, 520, 860), 60, 4, '#fff4e0')
    # foreground counter: wooden top across the frame, front panel, goods
    counter = (wood_planks(-10, 640, 560, 26, '#b8865f', '#c99872', '#a07250', 560, 5, vertical=False)
               + '<rect x="-10" y="664" width="560" height="10" fill="#5e3e2c" opacity=".7"/>'
               + wood_planks(-10, 674, 560, 300, '#8a5e40', '#9a6c4c', '#7a5236', 60, 9)
               + '<rect x="-10" y="674" width="560" height="22" fill="#3a2418" opacity=".35"/>')
    goods = (jar(30, 580, 46, 62, '#f0b46a', '#d8655a') + jar(84, 594, 40, 48, '#e88aa8', '#2fb3b8')
             + '<g transform="translate(150,640)">' + ''.join(f'<path d="M {k * 12 - 22},0 C {k * 12 - 30},-34 {k * 12 - 8},-48 {k * 12 + 4},-44" stroke="#e8c35e" stroke-width="10" fill="none" stroke-linecap="round"/>' for k in range(5)) + '<path d="M -26,-4 C -10,-14 26,-14 40,-4" stroke="#6e5a2a" stroke-width="5" fill="none"/></g>'
             + '<g transform="translate(430,640)"><rect x="-42" y="-34" width="84" height="34" rx="4" fill="#d6d1c8"/><rect x="-42" y="-34" width="84" height="8" fill="#eeeae2"/><rect x="-12" y="-62" width="24" height="28" rx="3" fill="#9aa1a8"/><ellipse cx="0" cy="-64" rx="30" ry="6" fill="#c9ced8"/></g>'
             + '<g transform="translate(330,640)"><rect x="-30" y="-56" width="60" height="56" rx="6" fill="#2f6fb5"/><rect x="-30" y="-56" width="60" height="14" rx="5" fill="#2c5a96"/>'
             f'<text x="0" y="-18" {TH} font-size="11" font-weight="800" fill="#fff" text-anchor="middle">น้ำแข็ง</text></g>'
             + '<g transform="translate(240,652) rotate(-4)"><rect x="-56" y="-20" width="112" height="40" rx="4" fill="#fffaf0"/>'
             f'<text x="0" y="-3" {TH} font-size="12" font-weight="800" fill="#1a1626" text-anchor="middle">ของสดมาพรุ่งนี้</text>'
             f'<text x="0" y="13" {TH} font-size="10" font-weight="700" fill="#c4463d" text-anchor="middle">(ถ้าเรือมา)</text></g>')
    # characters: the auntie behind the counter (medium), Sun at the right edge (past, city look)
    aunt_in = ISL['AUNT_BODY'] + '<use href="#h_aunt"/>'
    sun_in = R.body(head='annoy', tote=True, camera=False)
    a_tr = 'translate(250,250) scale(1.5)'
    s_tr = 'translate(470,392) scale(1.62)'
    shadow_wall = (f'<g filter="url(#s3sil)" opacity=".32" style="mix-blend-mode:multiply"><g transform="translate(-70,-18) {a_tr} skewX(-8)">{aunt_in}</g></g>'
                   f'<g filter="url(#s3sil)" opacity=".28" style="mix-blend-mode:multiply"><g transform="translate(-60,-10) {s_tr} skewX(-8)">{sun_in}</g></g>')
    fa, ma = CL.character(f'{fid}-aunt', aunt_in, CL.aim((250, 400), (320, 260)), 'golden', transform=a_tr, heads=[('tawan', '')], prefix=fid)
    fs, ms = CL.character(f'{fid}-sun', sun_in, CL.aim((478, 450), (320, 260)), 'golden', transform=s_tr, heads=[('sun', '')], prefix=fid)
    ui = (step_card(1, 'ของบนเกาะแพงกว่าฝั่ง', 'STEP 1 · EVERYTHING COMES BY BOAT')
          + '<g transform="translate(36,770)"><rect x="0" y="0" width="200" height="44" rx="10" fill="#c4463d"/>'
          f'<text x="100" y="29" {TH} font-size="17" font-weight="800" fill="#fff" text-anchor="middle">ค่าเรือรวมอยู่ในราคา</text></g>'
          '<path d="M 120,768 C 110,720 130,690 160,660" stroke="#ffffff" stroke-width="4" fill="none" stroke-linecap="round"/><path d="M 148,656 L 164,654 L 160,670" stroke="#ffffff" stroke-width="4" fill="none" stroke-linecap="round"/>'
          + subs('ของบางอย่างแพงกว่าฝั่งนิดหน่อย', 'Some things cost a bit more here.'))
    return CL.compose('golden', bg=back, shadow=patch + shadow_wall, chars=ma + counter + goods + ms, light=light, atmos='', ui=ui,
                      extra_defs=defs + fa + fs, prefix=fid, label='ร้านโชห่วยไม้บนเกาะ')


def step_card(n, title, sub):
    return (f'<g {TH}><rect x="22" y="46" width="496" height="92" rx="16" fill="#f6efe4" opacity=".95"/><rect x="22" y="46" width="496" height="92" rx="16" fill="none" stroke="#e3d6c2" stroke-width="2"/>'
            f'<circle cx="74" cy="92" r="30" fill="#2f8f4e"/><text x="74" y="104" font-size="32" font-weight="800" fill="#fff" text-anchor="middle">{n}</text>'
            f'<text x="120" y="96" font-size="27" font-weight="800" fill="#2a2430">{title}</text>'
            f'<text x="120" y="122" {EN} font-size="11.5" font-weight="700" fill="#8a8094" letter-spacing="1">{sub}</text></g>')


def subs(th, en):
    return (f'<g {TH} font-weight="800" font-size="30" text-anchor="middle" fill="#ffffff" stroke="#1a1218" stroke-width="7" paint-order="stroke" stroke-linejoin="round">'
            f'<text x="270" y="712">{th}</text></g>'
            f'<rect x="{270 - len(en) * 4.2:.0f}" y="728" width="{len(en) * 8.4:.0f}" height="30" rx="8" fill="#1a1218" opacity=".78"/>'
            f'<text x="270" y="749" {EN} font-size="14" font-weight="700" fill="#ffffff" text-anchor="middle">{en}</text>')


if __name__ == '__main__':
    svg = shop_frame()
    page = f'''<title>Odd Hours ทดลองสไตล์ใหม่</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one 9:16 test frame centred, notes beside it on desktop, below on phones. Single dark look by choice. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:900px; margin:0 auto; display:grid; grid-template-columns:minmax(0,420px) 1fr; gap:24px; align-items:start; }}
@media (max-width:700px) {{ .wrap {{ grid-template-columns:1fr; }} }}
svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:8px; box-shadow:0 0 0 1px var(--line); }}
h1 {{ font-size:18px; font-weight:500; margin:0 0 10px; }} p, li {{ font-size:14px; color:var(--muted); line-height:1.7; }} b {{ color:var(--ink); font-weight:500; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700;800&family=Inter:wght@600;700;800&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{R.HEAD_DEFS}{ISL["CLIPS"]}{ISL["AUNT_HEAD"]}</defs></svg>
<div class="wrap">
  <div>{svg}</div>
  <div><h1>ทดลองสไตล์ใหม่ · ร้านโชห่วยไม้บนเกาะ</h1>
  <ul>
    <li><b>มุมกล้องระยะกลาง:</b> ป้าครึ่งตัวหลังเคาน์เตอร์ไม้ เคาน์เตอร์เป็นฉากหน้า ผนังไม้อยู่ใกล้หลังตัวละคร</li>
    <li><b>แสง:</b> ลำแสงเย็นอุ่นส่องผ่านหน้าต่างลูกกรงเป็นแนวเฉียง มีฝุ่นลอย เงาลูกกรงตกบนผนัง เงาตัวละครทาบผนัง หลอดไฟห้อยเรืองแสง</li>
    <li><b>ร้านไม้บ้าน ๆ:</b> ผนังไม้มีลายไม้ ชั้นโหลขนม บะหมี่ ขวด นาฬิกา ปฏิทิน รูปเก่าท่าเรือ ป้ายน้ำแข็งหลอด กล้วย ถังน้ำแข็ง ตาชั่ง ป้ายลายมือ</li>
    <li><b>กราฟิกแบบใหม่:</b> การ์ดหัวข้อมีเลขขั้นตอนซ้อนบนฉาก ป้ายแดงพร้อมลูกศรชี้ ซับตัวขาวขอบเข้มกับป้ายอังกฤษ</li>
  </ul></div>
</div>
'''
    open(os.path.join(HERE, 'style3.html'), 'w').write(page)
    print(len(page))
