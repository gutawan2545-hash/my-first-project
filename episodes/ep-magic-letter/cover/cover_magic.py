"""ปกตอนฮอกวอตส์สาขาไทย ตามแม่แบบปกของช่อง (cover/cover.py): ข้อความครึ่งบน ภาพเด่นครึ่งล่าง พื้นดำอมม่วง เม็ดฟิล์มบาง ๆ
ใช้ตัวละครจาก ../cast.html · ไม่เฉลยมุกในเรื่อง
usage: python3 cover_magic.py -> cover.html ; node render.js -> cover.png (1080x1920)"""
import re, random, pathlib
HERE = pathlib.Path(__file__).parent
cast = (HERE.parent / "cast.html").read_text()
CHAR = re.search(r'(<svg width="0" height="0"[^>]*><defs>.*?</defs></svg>)', cast, re.S).group(1)

EP = {
    'episode': 'ตอนที่ 2',
    'title1': 'ถ้าได้จดหมาย',
    'title2_before': 'จาก', 'title2_hl': 'ฮอกวอตส์', 'title2_after': '',
    'rule': 'สาขาประเทศไทย • 5 ขั้นตอนก่อนเข้าเรียน',
}
S = dict(margin_left=48, margin_right=48, logo=(70, 66), episode_y=152, title1_y=232, title2_y=306,
         title_size=62, episode_size=22, rule_y=338, rule_h=36, rule_size=17)

r = random.Random(7)
motes = ''.join(f'<circle cx="{r.uniform(60,480):.0f}" cy="{r.uniform(480,920):.0f}" r="{r.uniform(.7,1.9):.1f}" opacity="{r.uniform(.25,.8):.2f}" fill="#ffe9c8"{" filter=\"url(#soft)\"" if r.random() < .4 else ""}/>' for _ in range(30))
windows = ''.join(f'<rect x="{x}" y="{y}" width="7" height="10" fill="#ffd9a0" opacity=".45"/>' for x, y in [(30,690),(64,700),(98,684),(30,730),(98,726),(430,690),(466,706),(500,688),(466,740)])

ART = f'''
<rect width="540" height="960" fill="url(#bg)"/>
<!-- ฉากหลัง: ยอดวัดสีทองซ้าย ปราสาทเวทมนตร์ขวา ตึกแถวเก่า เบลอจาง ๆ -->
<g filter="url(#soft6)" opacity=".75">
  <path d="M 70,640 L 86,520 L 102,640 Z" fill="#c99a3a"/><path d="M 60,640 L 112,640 L 106,620 L 66,620 Z" fill="#8e1b24"/><path d="M 86,520 L 86,496" stroke="#c99a3a" stroke-width="3"/>
  <path d="M 410,640 L 410,560 L 400,560 L 425,500 L 450,560 L 440,560 L 440,640 Z M 455,640 L 455,580 L 446,580 L 468,530 L 490,580 L 481,580 L 481,640 Z" fill="#2a2148"/>
  <rect x="0" y="640" width="540" height="320" fill="#1a1024"/>
  <rect x="0" y="660" width="140" height="300" fill="#2a1a2e"/><rect x="400" y="660" width="140" height="300" fill="#22182e"/>
  {windows}
</g>
<ellipse cx="300" cy="700" rx="280" ry="260" fill="url(#halo)" style="mix-blend-mode:screen"/>
<!-- ซิ่ง ชุดคลุมดำ ยิ้มกวน (ครึ่งตัว) -->
<g transform="translate(300,1135) scale(1.36)"><use href="#c_sing_robe"/></g>
<!-- ไอ้เหลืองเกาะไหล่ ขันใส่ -->
<g transform="translate(150,590) scale(-.7,.7)"><use href="#c_rooster"/></g>
<!-- จดหมายเรืองแสง ตราครั่งแดง -->
<circle cx="384" cy="752" r="95" fill="url(#glow)" style="mix-blend-mode:screen"/>
<g transform="translate(384,758) rotate(-12) scale(.66)">
  <rect x="-92" y="-62" width="184" height="124" rx="6" fill="#05040a" opacity=".45" transform="translate(10,12)" filter="url(#soft6)"/>
  <rect x="-92" y="-62" width="184" height="124" rx="6" fill="#f4ecd8"/>
  <path d="M -92,-62 L 0,10 L 92,-62" fill="none" stroke="#d8ccb6" stroke-width="3"/>
  <circle cx="0" cy="8" r="20" fill="#8e1b24"/><circle cx="-4" cy="4" r="7" fill="#b8323e"/>
  <text x="0" y="48" text-anchor="middle" class="t" font-size="13" font-weight="600" fill="#5a3a2a">ฮอกวอตส์ สาขาประเทศไทย</text>
</g>
<g>{motes}</g>
<rect width="540" height="470" fill="url(#topfade)"/>
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".09" style="mix-blend-mode:screen"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:overlay"/>
'''

TEXT = f'''
<g id="logo" transform="translate({S['logo'][0]},{S['logo'][1]})"><ellipse rx="22" ry="16.5" fill="#7a1fff"/>
  <path d="M -16.5,0 C -9,-9.5 9,-9.5 16.5,0 C 9,9.5 -9,9.5 -16.5,0 Z" fill="#05040a"/><circle r="4.6" fill="#d6b0ff"/></g>
<text id="episode" x="{S['margin_left']}" y="{S['episode_y']}" class="t" font-size="{S['episode_size']}" font-weight="500" fill="#c9b8ec" letter-spacing=".5">{EP['episode']}</text>
<g class="t" font-weight="700" font-size="{S['title_size']}" fill="#ffffff" stroke="#07050c" stroke-width="3" paint-order="stroke">
  <text id="title1" x="{S['margin_left']}" y="{S['title1_y']}">{EP['title1']}</text>
  <text id="title2" x="{S['margin_left']}" y="{S['title2_y']}">{EP['title2_before']}<tspan fill="#c9a8ff">{EP['title2_hl']}</tspan>{EP['title2_after']}</text>
</g>
<g id="rule" transform="translate({S['margin_left']},{S['rule_y']})">
  <rect width="0" height="{S['rule_h']}" rx="7" fill="#8e1b24"/>
  <text x="14" y="{S['rule_h']/2 + S['rule_size']*0.36:.1f}" class="t" font-size="{S['rule_size']}" font-weight="600" fill="#fff4f2">{EP['rule']}</text>
</g>'''

DEFS = '''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07050c"/><stop offset=".45" stop-color="#140c20"/><stop offset="1" stop-color="#22142e"/></linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#ffd9a8" stop-opacity=".26"/><stop offset=".6" stop-color="#c9a8ff" stop-opacity=".08"/><stop offset="1" stop-color="#c9a8ff" stop-opacity="0"/></radialGradient>
<radialGradient id="glow"><stop offset="0" stop-color="#fff2c8" stop-opacity=".7"/><stop offset=".5" stop-color="#ffd88a" stop-opacity=".2"/><stop offset="1" stop-color="#ffd88a" stop-opacity="0"/></radialGradient>
<linearGradient id="topfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05030a" stop-opacity=".92"/><stop offset=".7" stop-color="#05030a" stop-opacity=".45"/><stop offset="1" stop-color="#05030a" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx="50%" cy="58%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<filter id="soft" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="soft6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.9" numOctaves="1" seed="4"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>'''

CHAR = re.sub(r'(<g id="c_sing_robe">.*?<g transform="translate\(60,206\)">)<path d="M 2,4 L 6,4 L 4,-62 L 1,-62 Z"[^>]*/><circle[^>]*/><circle[^>]*/>', r'\1', CHAR, count=1, flags=re.S)
CHAR = CHAR.replace('class="an-mouth-rooster" display="none"', 'class="an-mouth-rooster" display="inline"')   # ไก่อ้าปากขัน
html = f'''<!doctype html><meta charset="utf-8"><title>Odd Hours cover</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap">
<style>html,body{{margin:0;background:#000}}#cover{{display:block;width:540px;height:960px}}.t{{font-family:"IBM Plex Sans Thai","Noto Sans Thai",sans-serif}}</style>
{CHAR}<svg id="cover" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">{DEFS}<clipPath id="cv"><rect width="540" height="960"/></clipPath><g clip-path="url(#cv)">{ART}{TEXT}</g></svg>
<script>
document.fonts.ready.then(() => {{
  const g = document.querySelector('#rule'), t = g.querySelector('text');
  g.querySelector('rect').setAttribute('width', (t.getBBox().width + 28).toFixed(1));
  const maxR = 540 - {S['margin_right']};
  for (const id of ['title1', 'title2', 'rule']) {{ const b = document.getElementById(id).getBBox(); const x0 = id === 'rule' ? {S['margin_left']} : b.x; if (x0 + b.width > maxR) document.body.dataset.overflow = (document.body.dataset.overflow || '') + id + ' '; }}
  document.body.dataset.ready = '1';
}});
</script>'''
(HERE / "cover.html").write_text(html)
print("cover.html built")
