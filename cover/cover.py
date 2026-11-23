"""Odd Hours cover template (1080x1920). Fixed slots: eye logo top-left, episode label, two-line title with one
highlighted word, small dark-red rule tag. Only the art layer and the texts change per episode.
usage: python3 cover.py  -> cover.html ; then node render_cover.js -> ../out/cover.png"""
import json, random

# per-episode: texts + which art to use. Earlier cover (ตีสี่ EP1) is kept in cover_v2_4am_ep1.py
SERIES = 'second-sister'
EP = {
    'episode': 'ตอนที่ 1 · ระฆังตีสาม',
    'title1': 'แม่ชี',
    'title2_before': '', 'title2_hl': 'คนที่สอง', 'title2_after': '',
    'rule': 'กฎข้อที่ 1 • ระฆังดังตอนตีสาม ห้ามออกจากห้อง',
}

# ---- fixed template slots (540x960 design units, rendered x2) ----
SLOT = dict(margin_left=48, margin_right=48, logo=(48 + 22, 66), episode_y=152, title1_y=232, title2_y=306,
            title_size=62, episode_size=22, rule_y=338, rule_h=36, rule_size=17)

r = random.Random(5)
motes = ''.join(f'<circle cx="{r.uniform(80,360):.0f}" cy="{r.uniform(600,900):.0f}" r="{r.uniform(0.7,1.8):.1f}" '
                f'opacity="{r.uniform(.25,.85):.2f}" fill="#e9dcff"{" filter=\"url(#soft)\"" if r.random() < .4 else ""}/>' for _ in range(26))
planks = ''.join(f'<line x1="{x}" y1="420" x2="{x - 60}" y2="960" stroke="#120a18" stroke-opacity=".55" stroke-width="2"/>' for x in range(0, 640, 52))

ART = f'''
<rect width="540" height="960" fill="url(#bg)"/>
<!-- back wall: dim bedroom, a window of city lights at the right edge, blurred -->
<g filter="url(#soft6)" opacity=".8">
  <rect x="402" y="380" width="150" height="230" fill="#110c1c"/><rect x="410" y="388" width="134" height="214" fill="#1b1838"/>
  {''.join(f'<rect x="{410+(k*37)%120}" y="{430+(k*53)%150}" width="5" height="7" fill="#ffd9a0" opacity=".5"/>' for k in range(14))}
  <rect x="-10" y="430" width="120" height="330" fill="#1a1222"/>
</g>
<!-- James behind the desk, lit from below by the phone -->
<g filter="url(#lilac)"><use href="#jbodySNHL" transform="translate(372,600) scale(1.78)"/></g>
<ellipse cx="300" cy="720" rx="260" ry="220" fill="url(#halo)" style="mix-blend-mode:screen"/>
<!-- desk -->
<path d="M0,760 L540,748 L540,960 L0,960 Z" fill="url(#desk)"/><path d="M0,760 L540,748 L540,758 L0,770 Z" fill="#3a2a48"/>
<g opacity=".8"><g transform="translate(470,800) rotate(8)"><rect x="-80" y="-14" width="160" height="30" rx="6" fill="#17121f"/><rect x="-80" y="12" width="160" height="3" fill="#7d5cff" opacity=".6"/></g></g>
<ellipse cx="200" cy="860" rx="210" ry="90" fill="url(#pool)" style="mix-blend-mode:screen"/>
<!-- the phone: hero, lying on the desk tilted toward camera -->
<g transform="translate(205,800) rotate(-12) scale(1,0.9)">
  <rect x="-104" y="-200" width="208" height="400" rx="30" fill="#05040a" opacity=".55" transform="translate(14,18)" filter="url(#soft6)"/>
  <rect x="-104" y="-200" width="208" height="400" rx="30" fill="#0b0a12"/>
  <rect x="-104" y="-200" width="208" height="400" rx="30" fill="none" stroke="#6a6590" stroke-width="2"/>
  <rect x="-96" y="-192" width="192" height="384" rx="24" fill="url(#scr)"/>
  <text x="0" y="-104" text-anchor="middle" class="t" font-size="54" font-weight="600" fill="#f4f1ff">04:00</text>
  <text x="0" y="-78" text-anchor="middle" class="t" font-size="12" fill="#b8b0de">วันพฤหัสบดี</text>
  <rect x="-80" y="-52" width="160" height="66" rx="13" fill="#f2effa" fill-opacity=".96"/>
  <circle cx="-62" cy="-30" r="9" fill="#7a1fff"/><path d="M-66,-30 l3,3 l6,-6" stroke="#fff" stroke-width="2" fill="none"/>
  <text x="-46" y="-26" class="t" font-size="10" fill="#4a4670">ธนาคาร · ตอนนี้</text>
  <text x="-68" y="-6" class="t" font-size="15" font-weight="600" fill="#14111f">เงินเข้า +333.07 บาท</text>
  <text x="-68" y="8" class="t" font-size="9.5" fill="#5a5578">จากบัญชีที่ไม่รู้จัก</text>
  <path d="M -96,80 L 96,-10 L 96,40 L -96,130 Z" fill="#ffffff" opacity=".05"/>
</g>
<circle cx="205" cy="760" r="150" fill="url(#halo)" style="mix-blend-mode:screen"/>
<g>{motes}</g>
<rect width="540" height="470" fill="url(#topfade)"/>
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".09" style="mix-blend-mode:screen"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".06" style="mix-blend-mode:overlay"/>
'''

if SERIES == 'second-sister':   # art from episodes/second-sister/cover/make_art_ep1.py (the chapel frame, current cast)
    ART = '''
<rect width="540" height="960" fill="url(#bg)"/>
<g transform="translate(-95,150) scale(1.35)"><use href="#chapelArt"/></g>
<rect width="540" height="520" fill="url(#topfade)"/>
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".07" style="mix-blend-mode:screen"/>
'''

S = SLOT
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
</g>
'''

DEFS = '''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07050c"/><stop offset=".45" stop-color="#120a1c"/><stop offset="1" stop-color="#1c1028"/></linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#241830"/><stop offset=".6" stop-color="#1a1124"/><stop offset="1" stop-color="#0e0814"/></linearGradient>
<radialGradient id="pool"><stop offset="0" stop-color="#b9a8ff" stop-opacity=".55"/><stop offset=".55" stop-color="#8f7bff" stop-opacity=".18"/><stop offset="1" stop-color="#8f7bff" stop-opacity="0"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#cfc4ff" stop-opacity=".22"/><stop offset="1" stop-color="#cfc4ff" stop-opacity="0"/></radialGradient>
<linearGradient id="scr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4a3fa0"/><stop offset=".55" stop-color="#2a2370"/><stop offset=".56" stop-color="#332a80"/><stop offset="1" stop-color="#1b1650"/></linearGradient>
<linearGradient id="topfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#05030a" stop-opacity=".9"/><stop offset=".7" stop-color="#05030a" stop-opacity=".45"/><stop offset="1" stop-color="#05030a" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx="50%" cy="58%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<filter id="lilac" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.92 0 0 0 0.02  0 0.84 0 0 0.01  0 0 1.0 0 0.06  0 0 0 1 0"/></filter>
<filter id="soft" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="soft6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.9" numOctaves="1" seed="4"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>'''

CHAR = open('char_defs.svg.html').read()
if SERIES == 'second-sister': CHAR += open('../episodes/second-sister/cover/art_ep1.svg.html').read()
for c in ('blinkJ', 'blinkT', 'blinkC', 'mouthJ', 'mouthT'):          # stills: eyes open, mouths at rest
    CHAR = CHAR.replace(f'<g class="{c}">', f'<g class="{c}" display="none">')
html = f'''<!doctype html><meta charset="utf-8"><title>Odd Hours cover</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap">
<style>html,body{{margin:0;background:#000}}svg{{display:block;width:540px;height:960px}}.t{{font-family:"IBM Plex Sans Thai","Noto Sans Thai",sans-serif}}</style>
{CHAR}<svg id="cover" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">{DEFS}{ART}{TEXT}</svg>
<script>
// size the red rule tag to its text, and check the title fits inside the right margin
document.fonts.ready.then(() => {{
  const g = document.querySelector('#rule'), t = g.querySelector('text');
  g.querySelector('rect').setAttribute('width', (t.getBBox().width + 28).toFixed(1));
  const maxR = 540 - {S['margin_right']};
  for (const id of ['title1', 'title2']) {{ const b = document.getElementById(id).getBBox(); if (b.x + b.width > maxR) document.body.dataset.overflow = id; }}
  document.body.dataset.ready = '1';
}});
</script>'''
open('cover.html', 'w').write(html)
json.dump(dict(slots=SLOT, episode=EP), open('cover_template.json', 'w'), ensure_ascii=False, indent=1)
print('cover.html built')
