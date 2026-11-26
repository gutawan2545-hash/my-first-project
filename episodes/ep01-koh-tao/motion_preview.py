"""EP.01 animated preview: three scenes running on the reusable motion engine before the full render.
Run: python3 motion_preview.py -> motion_preview.html (plays live) and motion_frame.html (one scene, for frame render)"""
import os, sys, re, random

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'lighting'))
sys.path.insert(0, os.path.join(ROOT, 'pipeline', 'motion'))
import omkit as M
import sunrig as R
import kt_scenes as K
import style4 as S4
import style5 as S5
import style6 as S6
from style3 import wood_planks
from style4 import beam_set, fine_dust, compose, EYE
ISL = K.ISL
TH = M.TH
ENGINE = open(os.path.join(ROOT, 'pipeline', 'motion', 'oddmotion.js')).read()

# animated heads: James (pale = past, tan = present), the auntie
TAN_DEAD = R.tanify(M.group(R.HEAD_DEFS, 'sh_dead_t'))
HEADS = (M.anim_head(R.HEAD_DEFS, 'sh_annoy', 'jamA', '#efc7b0')
         + M.anim_head(R.HEAD_DEFS, 'sh_dead_t', 'jamT', '#d29e78')
         + M.anim_head(ISL['AUNT_HEAD'], 'h_aunt', 'auntA', '#e4ae86', 'tawan', ('teyeL', 'teyeR')))


def strip_ui(svg, ui):
    a = svg.rindex('<g id="L-ui">')
    return svg[:a] + f'<g id="L-ui">{ui}{EYE}</g></svg>'


def animate_scene(svg, cam):
    svg = svg.replace('<g id="L-graded"', f'<g id="L-graded" data-cam="{cam}"', 1)
    svg = re.sub(r'(<g class="cl-char"[^>]*>)<g transform="', r'\1<g data-breath="1.1,3.8" transform="', svg)
    return svg


# ---------------------------------------------------------------- scene 1: wooden shop, narration + step card + callout
def shop():
    svg = S4.shop().replace('href="#sh_annoy"', 'href="#jamA"').replace('href="#h_aunt"', 'href="#auntA"')
    ui = (M.tag('ปีแรกบนเกาะ', .2, 7.2)
          + M.step(1, 'ของบนเกาะแพงกว่าฝั่ง', 'EVERYTHING ARRIVES BY BOAT', .5, 7.0)
          + M.callout(34, 540, 220, ['ค่าเรือ', 'รวมอยู่ในราคา'], 120, 618, 3.0, 6.6, '#c4463d')
          + M.subs('ของบางอย่างแพงกว่าฝั่งนิดหน่อย/เพราะค่าเรือรวมอยู่ในนั้นแล้ว', 'Some things cost a bit more here,/the boat ride is in the price.', 1.4, 7.1, line_gap=1.6))
    return animate_scene(strip_ui(svg, ui), '1,1.05,10,-10'), {'dur': 8, 'faces': [
        {'id': 'jamA', 'glance': [[2.4, -2.6, .6], [5.6, 0, 0]], 'seed': 3},
        {'id': 'auntA', 'glance': [[3.2, 2, 0], [6.2, 0, 0]], 'seed': 9, 'blinkEvery': 2.8}]}


# ---------------------------------------------------------------- scene 2: parcel route graphic, staggered stickers + draw-on route + counter
def parcel():
    fid = 'MP2'
    floor = wood_planks(0, 0, 540, 960, '#8a6a52', '#9a7860', '#7a5c46', 70, 51, vertical=False)
    bd, bs, bc = beam_set(fid, [[(380 + k * 50, 0), (420 + k * 50, 0), (60 + k * 50, 960), (20 + k * 50, 960)] for k in range(4)], '#fff2d8', .18)
    box = ('<g transform="translate(270,430)"><rect x="-150" y="-110" width="310" height="240" fill="#000" opacity=".28" filter="url(#s4soft)"/>'
           '<rect x="-160" y="-120" width="320" height="240" fill="#c49a6c"/><rect x="-160" y="-120" width="320" height="240" fill="none" stroke="#a97f55" stroke-width="3"/>'
           '<rect x="-24" y="-120" width="48" height="240" fill="#e6d2b0" opacity=".85"/>'
           '<rect x="-140" y="-96" width="110" height="78" fill="#f8f4ea"/>' + f'<text x="-85" y="-74" {TH} font-size="11" font-weight="800" fill="#1a1626" text-anchor="middle">ถึง: เจม</text>'
           + f'<text x="-85" y="-56" {TH} font-size="10" fill="#5a5470" text-anchor="middle">บ้านบนเนิน เกาะเต่า</text>' + ''.join(f'<rect x="{-130 + k * 6}" y="-44" width="{2 + k % 3}" height="20" fill="#1a1626"/>' for k in range(14)) + '</g>')
    stamp = M.pop('<g transform="translate(360,470) rotate(-10)"><rect x="-50" y="-22" width="100" height="44" rx="6" fill="#c4463d"/>' + f'<text x="0" y="6" {TH} font-size="14" font-weight="800" fill="#fff" text-anchor="middle">ระวังแตก</text></g>', 1.0, 7.3)
    steps = [('โกดัง', 'กรุงเทพ', '#5a6c8e', 90, 170), ('รถขนส่ง', 'ลงใต้', '#e8735f', 270, 130), ('ท่าเรือ', 'ชุมพร', '#2fb3b8', 450, 170),
             ('ข้ามทะเล', 'คลื่นแรง = งด', '#3d6fb0', 470, 720), ('แม่หาด', 'ถึงเกาะ', '#2fb3b8', 270, 750), ('ถึงบ้าน', 'กระบะ/มอไซค์', '#7a5ab8', 70, 720)]
    route = ('<path data-in="draw" data-at="1.4" data-dur="3.6" data-out="draw-back" data-out-at="6.9" data-out-dur=".6" data-dash="8 7" '
             'd="M 90,170 Q 180,100 270,130 Q 360,100 450,170 Q 560,450 470,720 Q 370,790 270,750 Q 170,790 70,720" stroke="#f8f4ea" stroke-width="3.4" fill="none" opacity=".9"/>')
    stickers = ''
    for i, (t, s, c, x, y) in enumerate(steps):
        at = 1.4 + i * .62
        stickers += M.pop(f'<g transform="translate({x},{y})"><circle r="46" fill="#000" opacity=".25" filter="url(#s4soft)"/><circle r="44" fill="#f8f4ea"/><circle r="38" fill="{c}"/>'
                          f'<text x="0" y="-2" {TH} font-size="14" font-weight="800" fill="#fff" text-anchor="middle">{t}</text><text x="0" y="16" {TH} font-size="10.5" font-weight="700" fill="#fff" text-anchor="middle" opacity=".9">{s}</text>'
                          f'<circle cx="30" cy="-30" r="12" fill="#120e1c"/><text x="30" y="-25" {TH} font-size="12" font-weight="800" fill="#f2eefa" text-anchor="middle">{i + 1}</text></g>', at, 6.4 + i * .08)
    storm = M.pop('<g transform="translate(500,650)" data-float="2.5,2.2"><path d="M -30,8 C -30,-8 -14,-16 0,-11 C 8,-24 30,-22 33,-4 C 46,-3 47,11 35,14 L -26,14 C -37,14 -39,8 -30,8 Z" fill="#9aa6b8"/><path d="M -6,18 L -12,32 M 8,18 L 2,32" stroke="#3d6fb0" stroke-width="3"/></g>', 3.5, 6.6)
    count = M.reveal(f'<g transform="translate(270,268)"><rect x="-96" y="-30" width="192" height="46" rx="23" fill="#120e1c" fill-opacity=".85" stroke="#9a86ff"/></g>', 4.6, 6.8, 'grow', .5) + M.counter(270, 246, 6, 'ผ่าน {n} จุดกว่าจะถึงบ้าน', 4.7, 6.8, 16, '#f2eefa')
    light = bs + fine_dust((0, 0, 540, 960), 200, 51, '#fff4e2', clip=bc)
    ui = (M.step(2, 'พัสดุเดินทางมาเกาะยังไง', 'SIX STOPS FROM WAREHOUSE TO DOOR', .3, 7.1, 852)
          + M.subs('ของหลายอย่างต้องมาทางเรือ/คลื่นแรงเมื่อไหร่ เรืองด ของก็มาช้า', 'Most things come by boat;/rough seas mean late parcels.', 1.2, 7.2, 610, 2.0))
    svg = compose(fid, 'warm', floor, '', [], f'<g data-par="-.4">{box}</g>' + stamp + route + stickers + storm + count, light, '', ui, bd + S5.S5DEFS)
    return animate_scene(svg, '1.02,1.06,0,6'), {'dur': 8}


# ---------------------------------------------------------------- scene 3: rough sea, James speaks, waves alive, push-in
def rough():
    svg = S6.rough_sea().replace('href="#sh_dead_t"', 'href="#jamT"')
    ui = (M.tag('สองปีต่อมา · หน้าผาริมทะเล', .2, 7.2)
          + M.subs('วันนี้คลื่นแรง…/ของคงไม่มาอีกแล้ว', 'Rough sea today…/my parcel isn’t coming again.', 1.5, 7.0, line_gap=2.0)
          + M.callout(40, 470, 190, ['คลื่นแรง', 'เรืองดวิ่ง'], 200, 690, 4.4, 6.8, '#3d6fb0'))
    return animate_scene(strip_ui(svg, ui), '1,1.08,-30,-30'), {'dur': 8, 'faces': [
        {'id': 'jamT', 'talk': [[1.55, 2.75], [3.55, 5.1]], 'glance': [[.6, -2.4, .8], [3.2, 0, 0], [5.6, -2.4, .8]], 'seed': 5}]}


SCENES = [(shop, 'ร้านโชห่วย · บรรยาย', 'กล้องค่อย ๆ ดันเข้า · การ์ดขั้นตอนเผยจากซ้าย เลขป๊อปขึ้น หัวข้อเลื่อนเข้า · ซับทยอยขึ้นทีละบรรทัดตามจังหวะบรรยาย · ป้ายชี้: จุดเน้น → เส้นวาดตัวเอง → กล่องขยายจากปลายเส้น → ตัวอักษรทยอยขึ้น → ค้างให้อ่าน → ออกย้อนกลับ · เจมกลอกตามองราคา ป้ากะพริบตา หายใจเบา ๆ · ลำแสงไหว ฝุ่นลอย'),
          (parcel, 'กราฟิก · เส้นทางพัสดุ', 'สติกเกอร์ 6 จุดทยอยป๊อปตามเส้นทางที่ค่อย ๆ วาดเป็นเส้นประ · ตราประทับ "ระวังแตก" · ไอคอนพายุลอยเบา ๆ · ตัวเลขนับขึ้น · กล่องขยับ parallax ช้ากว่ากล้อง · ทุกชิ้นออกก่อนจบ'),
          (rough, 'ฉากคลื่นแรง · เจมพูด', 'ปากเจมขยับเฉพาะช่วงพูดตรงกับซับสองบรรทัด กะพริบตาเอง มองทะเลแล้วหันกลับ · คลื่นซัด ฟองไหล ละอองพุ่งเป็นจังหวะ เมฆเลื่อน · กล้องดันเข้าหาเจมช้า ๆ · ป้ายชี้คลื่นขึ้นหลังพูดจบ')]


def page(body, title, autoplay=True):
    return f'''<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: animated 9:16 previews, 3 across on desktop, 1 on phone; notes under each. Single dark look by choice, like the other Odd Hours boards. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#9a86ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; margin:0; }}
.wrap {{ max-width:1100px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:18px; }}
@media (max-width:860px) {{ .grid {{ grid-template-columns:1fr; max-width:420px; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:8px; box-shadow:0 0 0 1px var(--line); overflow:hidden; }}
figcaption {{ display:grid; gap:3px; font-size:13px; line-height:1.55; }} figcaption b {{ font-weight:500; }} .note {{ color:var(--muted); font-size:12px; }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:8px; padding:6px 12px; cursor:pointer; justify-self:start; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700;800&family=Inter:wght@500;700;800&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{R.HEAD_DEFS}{ISL["CLIPS"]}{ISL["AUNT_HEAD"]}{HEADS}</defs></svg>
{body}
<script>{ENGINE}</script>
'''


def build():
    figs, confs = '', []
    for i, (fn, t, n) in enumerate(SCENES):
        svg, conf = fn()
        svg = svg.replace('<svg ', f'<svg data-scene="{i}" ', 1)
        figs += f'<figure>{svg}<figcaption><b>{t}</b><span class="note">{n}</span></figcaption></figure>'
        confs.append(conf)
    import json
    body = f'''<div class="wrap"><h1>Animated Preview · EP.01<span>ทดสอบการเคลื่อนไหวก่อนเรนเดอร์คลิปเต็ม · วนซ้ำทุก 8 วินาที · ยังไม่มีเสียง</span></h1>
<button id="replay">เล่นใหม่</button><div class="grid">{figs}</div></div>'''
    body += f'''<script>window.addEventListener('load', () => {{
  const confs = {json.dumps(confs)};
  document.querySelectorAll('svg[data-scene]').forEach((s, i) => OM.mount(s, confs[i]));
  OM.play(true);
  document.getElementById('replay').onclick = () => location.reload();
}});</script>'''
    open(os.path.join(HERE, 'motion_preview.html'), 'w').write(page(body, 'Odd Hours Motion Preview'))
    # single-scene page for frame-exact rendering (no autoplay; render script calls OM.seek)
    svg, conf = rough()
    svg = svg.replace('<svg ', '<svg data-scene="0" width="540" height="960" ', 1)
    sbody = (f'<div style="width:540px;height:960px">{svg}</div>'
             f'<script>window.addEventListener("load", () => {{ window.S = OM.mount(document.querySelector("svg[data-scene]"), {json.dumps(conf)}); window.READY = true; }});</script>')
    open(os.path.join(HERE, 'motion_frame.html'), 'w').write(page(sbody, 'Odd Hours frame render').replace('padding-block:24px 40px;', 'padding:0;'))
    print('ok')


if __name__ == '__main__':
    build()
