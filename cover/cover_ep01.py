"""Odd Hours cover template (1080x1920). Fixed slots: eye logo top-left, episode label, two-line title with one
highlighted word, small dark-red rule tag. Only the art layer and the texts change per episode.
EP.01 Koh Tao cover (same fixed slots as cover.py). usage: python3 cover_ep01.py ; node render_cover.js cover_ep01.html ../out/cover_ep01.png"""
import json, random

EP = {
    'episode': 'EP.01',
    'title1': 'กรุงเทพเนทีฟ',
    'title2_before': 'ย้ายไป', 'title2_hl': 'เกาะเต่า', 'title2_after': '',
    'rule': 'เกาะนี้ไม่มีสนามบิน • ทุกอย่างต้องนั่งเรือ',
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
<!-- hero: present-day James at the Koh Nang Yuan viewpoint (rendered from the episode scenes: ep01_art.png) -->
<image href="ep01_art.png" x="0" y="0" width="540" height="960" preserveAspectRatio="xMidYMid slice"/>
<rect width="540" height="520" fill="url(#topfade)"/>
<rect width="540" height="960" fill="url(#vig)"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".08" style="mix-blend-mode:screen"/>
<rect width="540" height="960" filter="url(#grain)" opacity=".05" style="mix-blend-mode:overlay"/>
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
<linearGradient id="topfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0612" stop-opacity=".96"/><stop offset=".6" stop-color="#140c22" stop-opacity=".72"/><stop offset="1" stop-color="#05030a" stop-opacity="0"/></linearGradient>
<radialGradient id="vig" cx="50%" cy="58%" r="75%"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".7"/></radialGradient>
<filter id="lilac" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.92 0 0 0 0.02  0 0.84 0 0 0.01  0 0 1.0 0 0.06  0 0 0 1 0"/></filter>
<filter id="soft" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="1.2"/></filter>
<filter id="soft6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="8"/></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.9" numOctaves="1" seed="4"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>'''

CHAR = open('char_defs.svg.html').read()
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
open('cover_ep01.html', 'w').write(html)

print('cover_ep01.html built')
