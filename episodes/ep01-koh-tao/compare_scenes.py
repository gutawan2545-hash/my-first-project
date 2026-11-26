"""Before/after of the scene-art upgrade (shots 1, 4, 16) -> scene_upgrade.html"""
import re, os
H = os.path.dirname(os.path.abspath(__file__))
old = open(os.path.join(H, 'storyboard_v1.html')).read()
new = open(os.path.join(H, 'storyboard.html')).read()
figs = lambda s: re.findall(r'<figure>(<svg viewBox.*?</svg>)', s, re.S)
fo, fn = figs(old), figs(new)
head = new[:new.index('<div class="wrap"')]
head = head.replace('<title>Odd Hours EP.01 เกาะเต่า</title>', '<title>Odd Hours ฉากใหม่ EP.01</title>')
names = {1: 'ห้องคอนโดกรุงเทพ', 4: 'บนเรือไปเกาะเต่า', 16: 'คาเฟ่ริมทะเล'}
rows = ''.join(f'<section><h2>ช็อต {i} · {t}</h2><div class="pair"><figure>{fo[i-1]}<figcaption><b>ก่อน</b> · สตอรี่บอร์ดฉบับแรก</figcaption></figure>'
               f'<figure>{fn[i-1]}<figcaption><b class="new">หลัง</b> · ฉากแบบใหม่</figcaption></figure></div></section>' for i, t in names.items())
css = '<style>.pair{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media (max-width:560px){.pair{grid-template-columns:1fr}} h2{font-size:15px;font-weight:500;margin:0 0 8px} section{display:grid;gap:4px} b.new{color:#ffd84a}</style>'
page = head + css + f'''<div class="wrap" id="board"><header><h1>ยกระดับฉาก EP.01<span>ก่อน / หลัง · 3 ช็อตตัวอย่าง · ถ้าผ่านจะใช้แนวนี้กับทุกช็อต</span></h1></header>{rows}</div>'''
open(os.path.join(H, 'scene_upgrade.html'), 'w').write(page)
print(len(page))
