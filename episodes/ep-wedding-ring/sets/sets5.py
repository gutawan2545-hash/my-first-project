# Odd Hours · ตอนงานแต่ง · รอบ 5: ห้องพิธีเดิม 4 โทนสีหรู ให้เจ้าของช่องเลือก
# รัน: python3 sets5.py -> sets5.html
import re
import sets4 as S

VARIANTS = {
    'A': dict(name='งาช้างกับแชมเปญโกลด์', note='ผนังงาช้าง ม่านซาตินสีแชมเปญ พื้นหินอ่อนขาว ทองด้าน แบบโรงแรมห้าดาวคลาสสิก',
              CRM_L='#fffaf2', CRM='#f2ebdf', CRM_M='#e2d7c6', CRM_D='#bfb09a', CRM_DD='#8f8170',
              GLD='#d4b06a', GLD_L='#f6e3b0', GLD_D='#9c7a3e',
              RED='#e3d5bc', RED_L='#f8efde', RED_D='#c2ad8c', RED_DD='#9e8a6c',
              wall=('#e6dccb', '#f6f0e6', '#ece3d4'), floor=('#f4efe8', '#e9e2d8', '#d6ccbf'),
              glass=('#1a2650', '#2c4176', '#4c679e'), ceil='#dcd0bd', med='#fbf7f0', vig='#3a3028', shadow='#6e5e48'),
    'B': dict(name='เขียวมรกตกับทอง', note='ผนังเขียวมรกตเข้ม ม่านกำมะหยี่เขียว ทองเงา พื้นหินอ่อนขาว แบบอาร์ตเดโค',
              CRM_L='#6f9482', CRM='#47695a', CRM_M='#3a5a4c', CRM_D='#26402f', CRM_DD='#182a22',
              GLD='#e2bb6a', GLD_L='#fbe6ad', GLD_D='#a07a36',
              RED='#2e4d3f', RED_L='#4f7562', RED_D='#1d3429', RED_DD='#12221b',
              wall=('#2c463b', '#3e5f50', '#35533f'), floor=('#efe9df', '#ddd5c8', '#c2b7a8'),
              glass=('#141d3c', '#233466', '#3b528c'), ceil='#22382d', med='#f6f1e8', vig='#0b130f', shadow='#0f1a14'),
    'C': dict(name='กรมท่ากับทอง', note='ผนังน้ำเงินกรมท่า ม่านกำมะหยี่กรมท่า ทองเงา พื้นหินอ่อนงาช้าง เรียบหรูแบบงานกลางคืน',
              CRM_L='#56679a', CRM='#3a4874', CRM_M='#2f3c62', CRM_D='#1f2946', CRM_DD='#131b30',
              GLD='#e0b968', GLD_L='#fbe6ae', GLD_D='#9e7834',
              RED='#28365c', RED_L='#435688', RED_D='#19223e', RED_DD='#10162a',
              wall=('#27345a', '#38487a', '#303f6a'), floor=('#f2ede5', '#e2dbd0', '#c9c0b2'),
              glass=('#3a4f8e', '#5a78b8', '#8aa6d8'), ceil='#212c4c', med='#f7f2ea', vig='#090d1a', shadow='#10162a'),
    'D': dict(name='ชมพูหม่นกับทอง', note='ผนังชมพูนู้ด ม่านกำมะหยี่ชมพูหม่น ทองด้าน พื้นหินอ่อนขาว หวานแบบผู้ใหญ่ ไม่สดจัด',
              CRM_L='#fbf1ec', CRM='#efdcd4', CRM_M='#e2c6bb', CRM_D='#c49e92', CRM_DD='#9a7468',
              GLD='#d6b06a', GLD_L='#f6e2b0', GLD_D='#9c783c',
              RED='#b07a80', RED_L='#cf9ea2', RED_D='#87545c', RED_DD='#663e46',
              wall=('#e6cdc3', '#f5e6df', '#eedad1'), floor=('#f6f0ea', '#eae1d9', '#d8cbbf'),
              glass=('#24345c', '#3a5490', '#6884ba'), ceil='#ddc3b8', med='#fbf6f2', vig='#3a2626', shadow='#6e4a44'),
}
VARIANTS['S'] = dict(VARIANTS['A'], name='งาช้างกับเงิน', note='แบบ A แต่เปลี่ยนทองเป็นเงินทั้งหมด: โคมระย้า เชิงเทียน หัวเสา กรอบหน้าต่าง ขอบลายพื้น และสายรวบม่าน',
                     GLD='#c3c8cf', GLD_L='#f4f6f9', GLD_D='#868d97', med='#fbfaf8')
VARIANTS['A'] = dict(VARIANTS['A'], name='งาช้างกับทอง (แบบ A เดิม)', note='ไว้เทียบกับแบบเงิน')
SHOW = ['S', 'A']
KEYS = ['CRM_L', 'CRM', 'CRM_M', 'CRM_D', 'CRM_DD', 'GLD', 'GLD_L', 'GLD_D', 'RED', 'RED_L', 'RED_D', 'RED_DD']

def variant_svg(k, v):
    for key in KEYS: setattr(S, key, v[key])
    svg = S.frame(S.scene_hall(), f'ห้องพิธีแต่งงาน โทน{v["name"]}')
    rep = {'#e2b282': v['ceil'], '#f5cfa2': v['med'], '#8a5434': v['shadow'], '#7a4a30': v['shadow']}
    for a, b in rep.items(): svg = svg.replace(a, b)
    for gid in ('wall4', 'floor4', 'glass4', 'vig4', 'drapeShadeL', 'drapeShadeR'):
        svg = svg.replace(f'url(#{gid})', f'url(#{gid}{k})')
    svg = re.sub(r'clipPath id="win(\d)"', lambda m: f'clipPath id="win{m.group(1)}{k}"', svg)
    svg = re.sub(r'url\(#win(\d)\)', lambda m: f'url(#win{m.group(1)}{k})', svg)
    w, f_, g = v['wall'], v['floor'], v['glass']
    defs = (f'<defs><linearGradient id="wall4{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{w[0]}"/><stop offset=".45" stop-color="{w[1]}"/><stop offset="1" stop-color="{w[2]}"/></linearGradient>'
            f'<linearGradient id="floor4{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{f_[0]}"/><stop offset=".5" stop-color="{f_[1]}"/><stop offset="1" stop-color="{f_[2]}"/></linearGradient>'
            f'<linearGradient id="glass4{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{g[0]}"/><stop offset=".55" stop-color="{g[1]}"/><stop offset="1" stop-color="{g[2]}"/></linearGradient>'
            f'<radialGradient id="vig4{k}" cx=".5" cy=".45" r=".8"><stop offset=".55" stop-color="{v["vig"]}" stop-opacity="0"/><stop offset="1" stop-color="{v["vig"]}" stop-opacity=".45"/></radialGradient>'
            f'<linearGradient id="drapeShadeL{k}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{v["RED_DD"]}" stop-opacity=".6"/><stop offset="1" stop-color="{v["RED_DD"]}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="drapeShadeR{k}" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{v["RED_DD"]}" stop-opacity=".6"/><stop offset="1" stop-color="{v["RED_DD"]}" stop-opacity="0"/></linearGradient></defs>')
    # หินอ่อน: เพิ่มลายเส้นบนพื้น
    import random
    r = random.Random(ord(k)); veins = []
    for i in range(46):
        x = r.uniform(-40, 540); y = r.uniform(650, 950); L = r.uniform(60, 170)
        veins.append(f'<path d="M{x:.0f},{y:.0f} c{L * .3:.0f},{r.uniform(-8, 8):.0f} {L * .6:.0f},{r.uniform(-14, 14):.0f} {L:.0f},{r.uniform(-6, 18):.0f}" stroke="{v["CRM_DD"] if k in "BC" else "#b8ad9e"}" stroke-width="{r.uniform(.5, 1.4):.1f}" fill="none" opacity=".35"/>')
    floor_marker = '<rect x="0.0" y="640.0" width="540.0" height="320.0"'
    i = svg.index(floor_marker); j = svg.index('/>', i) + 2
    svg = svg[:j] + ''.join(veins) + svg[j:]
    return svg.replace('role="img"', 'role="img"', 1).replace('>', '>' + defs, 1)

CSS = S.CSS.replace('<title>ฉากงานแต่งโทนอบอุ่น</title>', '<title>ห้องพิธีโทนเงิน</title>').replace('repeat(auto-fit,minmax(260px,1fr))', 'repeat(auto-fit,minmax(220px,1fr))').replace('max-width:1000px', 'max-width:1240px')

def build():
    cards = ''.join(f'<figure>{variant_svg(k, v)}<figcaption><b>{k} · {v["name"]}</b><small>{v["note"]}</small></figcaption></figure>' for k, v in ((k, VARIANTS[k]) for k in SHOW))
    page = CSS + S.DEFS + f'''<div class="wrap" id="wrap"><header><h1>ห้องพิธีโทนงาช้าง · เงินเทียบทอง<span>Odd Hours · ถ้าวันนี้เป็นวันแต่งงานของคุณ · ซ้ายคือแบบเงิน ขวาคือแบบ A เดิม</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
    open('sets6.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
