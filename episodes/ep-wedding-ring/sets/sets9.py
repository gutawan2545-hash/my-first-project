# Odd Hours · ตอนงานแต่ง · วิวนอกหน้าต่างกลางคืน 3 แบบ (ห้องพิธีเดิม ไม่ใส่ตัวละคร)
# รัน: python3 sets9.py -> sets9.html
import random, re
import sets8 as H8
from sets import fx

H8.CAST_BACK = H8.CAST_FRONT = ''
ORIG_CITY = H8.city

def towers(x0, x1, ybase, seed, cols, lit, maxh, lit_p=.35):
    r = random.Random(seed); o = []
    for layer, col in enumerate(cols):
        x = x0 - 10
        while x < x1:
            w = r.uniform(14, 34); h = r.uniform(.3, 1.0) * maxh * (1 - layer * .16)
            o.append(f'<rect x="{fx(x)}" y="{fx(ybase - h)}" width="{fx(w)}" height="{fx(h + 2)}" fill="{col}"/>')
            if layer == len(cols) - 1:
                for yy in range(int(ybase - h + 6), int(ybase - 4), 7):
                    for xx in range(int(x + 3), int(x + w - 4), 6):
                        if r.random() < lit_p:
                            o.append(f'<rect x="{xx}" y="{yy}" width="2.4" height="3.2" fill="{r.choice(lit)}" opacity="{r.uniform(.4, .95):.2f}"/>')
            x += w + r.uniform(1, 6)
    return ''.join(o)

def view_moon(x0, x1, ybase, seed, maxh):
    o = ''
    if seed == 71:
        o += ('<circle cx="300" cy="290" r="70" fill="#9fb0e0" opacity=".10"/><circle cx="300" cy="290" r="44" fill="#c4d0f0" opacity=".14"/>'
              '<circle cx="300" cy="290" r="28" fill="#eef2fb"/><circle cx="292" cy="284" r="5" fill="#d6dcec"/><circle cx="308" cy="298" r="3.6" fill="#d6dcec"/><circle cx="304" cy="280" r="2.4" fill="#d6dcec"/>'
              '<ellipse cx="270" cy="306" rx="70" ry="6" fill="#2a3666" opacity=".7"/><ellipse cx="330" cy="318" rx="56" ry="5" fill="#2a3666" opacity=".6"/>')
    r = random.Random(seed)
    o += ''.join(f'<circle cx="{fx(r.uniform(x0, x1))}" cy="{fx(r.uniform(ybase - 520, ybase - 260))}" r="{r.uniform(.5, 1.1):.1f}" fill="#dfe6ff" opacity="{r.uniform(.4, .9):.2f}"/>' for _ in range(14))
    o += f'<g filter="url(#blur7)">{towers(x0, x1, ybase, seed, ("#1a2350", "#141b40", "#0e1430"), ("#ffe6c4", "#cfe0ff", "#ffd8a0"), maxh, .28)}</g>'
    return o

def view_rain(x0, x1, ybase, seed, maxh):
    r = random.Random(seed); o = ''
    o += f'<g filter="url(#blur7)">{towers(x0, x1, ybase, seed, ("#2e3848", "#262f3e", "#1e2633"), ("#ffd9a8", "#e8eef8"), maxh, .3)}</g>'
    o += ''.join(f'<circle cx="{fx(r.uniform(x0, x1))}" cy="{fx(r.uniform(ybase - 140, ybase - 10))}" r="{r.uniform(3, 8):.1f}" fill="{r.choice(("#ffcf8a", "#ffe6c4", "#c8d8f0", "#ff9a7a"))}" opacity="{r.uniform(.25, .55):.2f}" filter="url(#bokeh9)"/>' for _ in range(16))
    o += ''.join(f'<path d="M {fx(x)},{fx(y)} l -5,22" stroke="#c8d4e8" stroke-width=".8" opacity="{r.uniform(.25, .55):.2f}"/>'
                 for x, y in ((r.uniform(x0, x1 + 20), r.uniform(ybase - 540, ybase)) for _ in range(70)))
    for _ in range(22):
        x = r.uniform(x0, x1); y = r.uniform(ybase - 520, ybase - 10); L = r.uniform(4, 14)
        o += f'<path d="M {fx(x)},{fx(y)} q 1,{fx(L * .5)} 0,{fx(L)}" stroke="#dfe8f6" stroke-width="1.4" opacity=".55" fill="none"/><circle cx="{fx(x)}" cy="{fx(y + L)}" r="1.6" fill="#eef3fb" opacity=".7"/>'
    return o

def view_fog(x0, x1, ybase, seed, maxh):
    r = random.Random(seed); o = ''
    if seed == 71:
        o += '<circle cx="232" cy="270" r="16" fill="#e6e0f0"/><circle cx="239" cy="266" r="15" fill="#1c1828"/><circle cx="232" cy="270" r="40" fill="#b8a8d8" opacity=".08"/>'
    o += f'<g filter="url(#blur7)">{towers(x0, x1, ybase, seed, ("#1e1a2c", "#16131f", "#0f0d16"), ("#d8c8a8",), maxh * 1.15, .03)}</g>'
    for _ in range(3):
        x = r.uniform(x0 + 10, x1 - 10); y = ybase - r.uniform(maxh * .7, maxh * 1.1)
        o += f'<circle cx="{fx(x)}" cy="{fx(y)}" r="2" fill="#ff4a4a"/><circle cx="{fx(x)}" cy="{fx(y)}" r="7" fill="#ff4a4a" opacity=".25" filter="url(#bokeh9)"/>'
    for k in range(6):
        y = ybase - 40 - k * 48
        o += f'<ellipse cx="{fx((x0 + x1) / 2 + r.uniform(-30, 30))}" cy="{fx(y)}" rx="{fx((x1 - x0) * .95)}" ry="{fx(r.uniform(18, 30))}" fill="#9a90b4" opacity="{.55 - k * .07:.2f}" filter="url(#fog9)"/>'
    return o

VARIANTS = [
    ('คืนพระจันทร์เต็มดวง', 'ฟ้าน้ำเงินเข้มเกือบดำ พระจันทร์เต็มดวงมีวงแสงรอบ เมฆบางพาดผ่าน ดาวเล็ก ๆ ไม่กี่ดวง ตึกเงาน้ำเงินเข้มมีไฟหน้าต่างขาวอุ่นกับฟ้าประปราย แสงที่ส่องเข้ามาเป็นแสงจันทร์สีฟ้าเย็น',
     view_moon, ('#070b1e', '#121c44', '#26346c'), '#9fb2e8', '#cfdcff'),
    ('ฝนตกกลางคืน', 'ฟ้าเทาอมฟ้าเข้ม ฝนตกเป็นสายเฉียง มีหยดน้ำไหลบนกระจก ตึกเทาฟ้า ไฟเมืองข้างล่างเบลอเป็นดวงสีอำพัน ขาว และส้มแดง ให้ความรู้สึกเหงาและอึดอัด',
     view_rain, ('#0e131c', '#1e2634', '#34405a'), '#8ea0bc', '#d6e0ee'),
    ('หมอกเที่ยงคืน', 'ฟ้าดำอมม่วง จันทร์เสี้ยว หมอกหนาคลุมเมืองหลายชั้น ตึกเกือบทั้งหมดมืดสนิท มีไฟติดแค่ไม่กี่ห้อง กับไฟแดงกะพริบบนยอดตึก เป็นแบบที่น่าขนลุกที่สุดในสามแบบ',
     view_fog, ('#06050c', '#14111f', '#2a2338'), '#7a6c98', '#c8bce0'),
]

def variant_svg(k, name, fn, sky, refl, shaft):
    H8.city = fn
    svg = H8.S.frame(H8.scene(), f'ห้องพิธี วิวนอกหน้าต่าง{name}')
    H8.city = ORIG_CITY
    defs = (f'<defs><linearGradient id="glass9{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky[0]}"/><stop offset=".55" stop-color="{sky[1]}"/><stop offset="1" stop-color="{sky[2]}"/></linearGradient>'
            f'<linearGradient id="refl9{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{refl}" stop-opacity=".45"/><stop offset="1" stop-color="{refl}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="shaft9{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{shaft}" stop-opacity=".55"/><stop offset="1" stop-color="{shaft}" stop-opacity="0"/></linearGradient></defs>')
    svg = svg.replace('url(#glass4)', f'url(#glass9{k})').replace('url(#reflDusk)', f'url(#refl9{k})').replace('url(#moonShaft)', f'url(#shaft9{k})')
    svg = re.sub(r'clipPath id="(win7\d|moonC)"', lambda m: f'clipPath id="{m.group(1)}_{k}"', svg)
    svg = re.sub(r'url\(#(win7\d|moonC)\)', lambda m: f'url(#{m.group(1)}_{k})', svg)
    # the window mottle lightens a night sky too much: soften it
    svg = svg.replace('filter="url(#mottle4)" opacity=".16"', 'filter="url(#mottle4)" opacity=".06"')
    # night inside as well: cool, slightly darker room
    svg = svg.replace('<g class="guide">', '<rect width="540" height="960" fill="#1a2040" opacity=".16" style="mix-blend-mode:multiply"/><g class="guide">', 1)
    return svg.replace('>', '>' + defs, 1)

EXTRA_DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="bokeh9" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.6"/></filter>
<filter id="fog9" x="-30%" y="-100%" width="160%" height="300%"><feGaussianBlur stdDeviation="9"/></filter>
</defs></svg>'''

def build():
    src = open('sets8.py').read()
    cards = ''.join(f'<figure>{variant_svg(i, n, fn, sky, rf, sh)}<figcaption><b>แบบ {i + 1} · {n}</b><small>{note}</small></figcaption></figure>'
                    for i, (n, note, fn, sky, rf, sh) in enumerate(VARIANTS))
    css = H8.S.CSS.replace('<title>ฉากงานแต่งโทนอบอุ่น</title>', '<title>วิวหน้าต่างกลางคืน</title>').replace('repeat(auto-fit,minmax(260px,1fr))', 'repeat(auto-fit,minmax(240px,1fr))').replace('max-width:1000px', 'max-width:1200px')
    import re as _re
    base = H8.S.DEFS
    for gid in ('drapeShadeL', 'drapeShadeR', 'glass4', 'vig4'):
        base = _re.sub(rf'<(linear|radial)Gradient id="{gid}".*?</\1Gradient>', '', base, flags=_re.S)
    page = css + base + H8.DEFS_EXTRA + EXTRA_DEFS + f'''<div class="wrap" id="wrap"><header><h1>วิวนอกหน้าต่าง · กลางคืน 3 แบบ<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ห้องพิธีเดิม ยังไม่ใส่ตัวละคร</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets9.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
