#!/usr/bin/env python3
"""Before / After ของระบบแสง cinelight 3 ฉาก: กลางคืน · ในห้องเปิดไฟ · ระยะใกล้ใบหน้า
รัน: python3 lighting_preview.py -> lighting_preview.html"""
import re, runpy, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline'))
import cinelight as cl

os.chdir(HERE)
G = runpy.run_path('scenes.py')
SC = {sid: body for sid, _, _, body in G['S']}
SCENE_DEFS = G['DEFS']

leads = open(os.path.join(HERE, '..', '..', 'characters', 'house-across', 'leads.html'), encoding='utf-8').read()
CHAR_DEFS = leads[leads.index('<defs>') + 6: leads.index('</defs>')]

def figure(start):
    i = leads.index(start); j = leads.index('</g>\n        </svg>', i)
    return leads[i:j + 4]
HERO = figure('<g transform="translate(200,140) scale(1.18)">')
HEROINE = figure('<g transform="translate(200,150) scale(1.2)">')

IDS = ['hface', 'heyeL', 'heyeR', 'hhead', 'hhair', 'gface', 'geyeL', 'geyeR', 'gback', 'ghead', 'skyBg']
def suffix(s, sfx='_a'):
    for k in IDS:
        s = s.replace(f'id="{k}"', f'id="{k}{sfx}"').replace(f'url(#{k})', f'url(#{k}{sfx})').replace(f'href="#{k}"', f'href="#{k}{sfx}"')
    return s

# ---- AFTER character defs: chin AO + soft form shading on the face itself ----
fH, fH_svg = cl.char_light((1, -.6), rim=1.2, shade=5, key_op=.6)     # hero face, key from the right
fG, fG_svg = cl.char_light((-1, -.45), rim=1.2, shade=5, key_op=.6)   # heroine face, key from the left
A = suffix(CHAR_DEFS)
A = A.replace('<path d="M -10,28 L 10,28 L 10.6,46 Q 0,40 -10.4,50 Z" fill="#c99a74"/>',
              '<path d="M -10,28 L 10,28 L 10.6,46 Q 0,40 -10.4,50 Z" fill="#c99a74"/>' + cl.chin_ao(0, 33, 15, .6))
A = A.replace('<path d="M -7.4,28 L 7.4,28 L 7.8,45 Q 0,39 -7.6,48 Z" fill="#d7a486"/>',
              '<path d="M -7.4,28 L 7.4,28 L 7.8,45 Q 0,39 -7.6,48 Z" fill="#d7a486"/>' + cl.chin_ao(0, 33, 12, .6))
def wrap_face(src, head_id, face_start, fid):
    h = src.index(f'id="{head_id}"'); i = src.index(face_start, h)
    j = src.index('\n    </g>', i) + len('\n    </g>')
    return src[:i] + f'<g filter="url(#{fid})">' + src[i:j] + '</g>' + src[j:]
A = wrap_face(A, 'hhead_a', '<path d="M -31,-12 C -32,-46', fH)
A = wrap_face(A, 'ghead_a', '<path d="M -30,-12 C -31,-45', fG)
HERO_A, HEROINE_A = suffix(HERO), suffix(HEROINE)

def place(fig, x, y, k, feet_y):   # put a 400x900 sheet figure with its feet at (x,y)
    return f'translate({x - 200*k:.1f},{y - feet_y*k:.1f}) scale({k})'

pairs = []

# ===== 1. night exterior (6A street, heroine under the street lamp) =====
k = .42; T = place(HEROINE, 170, 760, k, 762)
before = SC['6A'] + f'<g transform="{T}">{HEROINE}</g>'
lamp = (54, 312); L = (lamp[0] - 170, lamp[1] - 620)
f1, f1s = cl.char_light(L, rim=8, shade=24)
cone1 = '40,306 72,306 330,790 -60,790'
after = cl.compose(
    SC['6A'],
    shadow=cl.shadow_layer(cl.contact_shadow(170, 758, 70, L, .6)),
    character=cl.character(HEROINE_A, f1, T),
    env=cl.env_layer(cl.ambient(op=.32), cl.low_key(140, 560, 540, op=.66)),
    lighting=cl.lighting_layer(cl.cone(cone1, op=.42, axis=((56, 306), (130, 790))), cl.glow(lamp[0], lamp[1], 110, op=1),
                               cl.glow(495, 505, 90, op=.5), cl.glow(120, 120, 120, '#c9ccff', .55),
                               cl.glow(200, 320, 46, op=.55), cl.glow(290, 320, 46, op=.55), cl.glow(205, 430, 60, op=.6)),
) + cl.atmosphere_layer(cl.dust_in(cone1, 3, 46))
pairs.append(('ฉากกลางคืน', '6A · แฟนสาวยืนใต้ไฟถนน', 'แสงขอบส้มทองติดขอบผม ไหล่ และแขนด้านที่หันหาไฟถนนเท่านั้น ด้านไกลแสงไล่เข้าเงาเทาน้ำเงิน มีเงาสัมผัสใต้เท้า ฉากรอบนอกวงไฟถูกกดให้มืดแบบ low-key ฝุ่นเห็นเฉพาะในลำแสง', [f1s], before, after))

# ===== 2. interior, lamps on (5A investigation room, hero standing) =====
k = .5; T = place(HERO, 230, 820, k, 804)
before = SC['5A'] + f'<g transform="{T}">{HERO}</g>'
key = (416, 464); L = (key[0] - 230, key[1] - 610)
f2, f2s = cl.char_light(L, rim=7, shade=22)
cone2 = '398,470 434,470 540,880 300,880'
after = cl.compose(
    SC['5A'],
    shadow=cl.shadow_layer(cl.contact_shadow(230, 818, 92, L, .6), cl.ao_corner('150,553 440,553 440,568 150,568', .5),
                           cl.ao_corner('150,230 150,560 162,560 162,230', .35), cl.ao_corner('428,230 428,560 440,560 440,230', .35)),
    character=cl.character(HERO_A, f2, T),
    env=cl.env_layer(cl.ambient(op=.3), cl.low_key(390, 500, 560, op=.62)),
    lighting=cl.lighting_layer(cl.cone(cone2, op=.44, axis=((416, 470), (420, 880))), cl.glow(key[0], key[1], 120, op=1),
                               cl.glow(310, 477, 100, op=.55)),
) + cl.atmosphere_layer(cl.dust_in(cone2, 5, 40))
pairs.append(('ฉากภายในห้องที่เปิดไฟ', '5A · พระเอกในห้องสืบสวน โคมโต๊ะเป็นแสงหลัก', 'โคมโต๊ะด้านขวาเป็นแสงหลัก แสงขอบส้มทองติดขอบด้านขวาของผม ไหล่ แขน และไม้ค้ำยัน ด้านซ้ายไล่เงาเย็น มี AO ตามมุมผนังกับพื้น และเงาสัมผัสใต้เท้า มุมห้องไกลโคมมืดลง', [f2s], before, after))

# ===== 3. face close-up (heroine, warm lamp off-frame left) =====
k = 2.3; T = f'translate({270 - 200*k:.1f},{372 - 137*k:.1f}) scale({k})'
bg = f'<g filter="url(#dof2)" transform="translate(270,480) scale(1.35) translate(-270,-480)">{SC["5A"]}</g><rect width="540" height="960" fill="#1a1436" opacity=".35"/>'
before = bg + f'<g transform="{T}">{HEROINE}</g>'
L = (-1, -.4)
f3, f3s = cl.char_light(L, rim=2, shade=14, key_op=.55)
after = cl.compose(
    bg,
    character=cl.character(HEROINE_A, f3, T),
    env=cl.env_layer(cl.ambient(op=.3), cl.low_key(120, 360, 560, op=.6)),
    lighting=cl.lighting_layer(cl.glow(-60, 300, 240, '#ff9a4a', .3)),
) + cl.atmosphere_layer(cl.dust_in('0,120 230,120 330,760 0,760', 9, 34))
pairs.append(('ฉากระยะใกล้ใบหน้า', 'ใบหน้าแฟนสาว โคมไฟอยู่นอกเฟรมด้านซ้าย', 'แสงขอบบางติดแก้ม คาง และขอบผมด้านซ้าย ใบหน้าด้านขวาไล่เงานุ่มเป็นเทาน้ำเงิน มี AO ใต้คางบนลำคอ หน้าตาและสัดส่วนเดิมไม่เปลี่ยน', [f3s], before, after))

# ---------------- page ----------------
def svg(body, defs=''):
    return f'<svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">{defs}{body}</svg>'

rows = ''
for title, sub, note, fdefs, b, a in pairs:
    rows += f'''<section><h2>{title}<span>{sub}</span></h2><div class="pair">
<figure><div class="fr">{svg(b)}</div><figcaption>Before · ระบบเดิม</figcaption></figure>
<figure><div class="fr">{svg(a, "<defs>" + "".join(fdefs) + "</defs>")}</div><figcaption>After · Cinematic Lighting</figcaption></figure>
</div><p>{note}</p></section>'''

page = f'''<title>Odd Hours แสงเงา Before/After</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one row per test scene, before and after side by side (stacks on phones). Dark page so the low-key frames read true. */
:root {{ --bg:#11131c; --ink:#e3e6f0; --muted:#8f97ad; --line:#272c3d; --accent:#ffb36b; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--bg); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:900px; margin:0 auto; display:grid; gap:34px; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }}
header p, section p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.65; max-width:80ch; }}
h2 {{ font-size:17px; font-weight:500; margin:0 0 10px; }} h2 span {{ color:var(--muted); font-weight:400; font-size:13px; margin-left:8px; }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
figure {{ margin:0; display:grid; gap:6px; min-width:0; }}
.fr {{ border-radius:6px; overflow:hidden; box-shadow:0 0 0 1px var(--line); }}
.fr svg {{ display:block; width:100%; height:auto; }}
figcaption {{ font-size:12px; color:var(--muted); }} figure:last-child figcaption {{ color:var(--accent); }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&family=Inter:wght@700&display=swap">
{SCENE_DEFS}
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{cl.defs()}{CHAR_DEFS}{A}{fH_svg}{fG_svg}</defs></svg>
<div class="wrap"><header><h1>Odd Hours · Cinematic 2D Lighting · ภาพเทียบ Before / After</h1>
<p>ระบบแสงใหม่ <code>pipeline/cinelight.py</code> แยกเป็นเลเยอร์ฉากหลัง เงา ตัวละคร แสง และบรรยากาศ แสงขอบกับเงาบนตัวละครคำนวณจากขอบตัวละครเอง จึงตามตัวละครไปทุกเฟรมเวลาเคลื่อนไหว ลายเส้น หน้าตา และสัดส่วนเดิมไม่เปลี่ยน</p></header>
{rows}</div>'''
open('lighting_preview.html', 'w', encoding='utf-8').write(page)
print('ok')
