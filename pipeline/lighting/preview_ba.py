"""Before/After lighting preview on three shots from storyboard2 (EP ตอนโอนตีสี่).

  night    = shot 7 (dark hallway, both characters, door-gap light)
  interior = shot 4 (bedroom, desk lamp on)
  closeup  = shot 2 cropped to James's face (monitor light + warm rim from behind-left)

Run:  python3 preview_ba.py   ->  ../../out/lighting_preview.html
"""
import os, re, sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cinelight as CL

ROOT = os.path.join(HERE, '..', '..')
SB = open(os.path.join(ROOT, 'episodes', 'ep-4am-transfer', 'storyboard2.html')).read()
NS = 'http://www.w3.org/2000/svg'
ET.register_namespace('', NS)

HIDDEN = re.findall(r'<svg width="0" height="0".*?</svg>', SB, re.S)
SHOTS = re.findall(r'<svg viewBox="0 0 540 960".*?</svg>', SB, re.S)


def children(svg):
    root = ET.fromstring(svg.replace('<svg ', f'<svg xmlns="{NS}" ', 1))
    return list(root)


def tostr(el):
    return ET.tostring(el, encoding='unicode').replace(f' xmlns="{NS}"', '')


def split(svg):
    """Classify the shot's top-level elements into layers."""
    bg, chars, fg, oldlight, motes = [], [], [], [], []
    seen_char = False
    for el in children(svg):
        cls = el.get('class', '')
        filt = el.get('filter', '') or ''
        style = el.get('style', '') or ''
        fill = el.get('fill', '') or ''
        txt = tostr(el)
        if cls in ('info', 'subs', 'guide'):
            continue
        if fill == 'url(#gVig)' or filt in ('url(#stipple)', 'url(#grain)'):
            continue                                     # replaced by the kit's vignette + grain
        if 'tint' in filt and re.search(r'href="#(jbody|tbody|jbodyS|tbodyS)', txt):
            chars.append(el); seen_char = True; continue
        if not seen_char:
            bg.append(txt); continue
        if el.tag.endswith('g') and 'moteBlur' in txt and 'moteGlow' in txt:
            motes.append(txt); continue
        if 'mix-blend-mode' in style:
            oldlight.append(txt); continue
        fg.append(txt)
    return bg, chars, fg, oldlight, motes


def before(svg):
    """Current look, UI stripped so only the lighting differs."""
    out = svg
    out = re.sub(r'<g class="(info|subs|guide)".*?</g></g>|<g class="(subs|guide)".*?</g>', '', out, flags=re.S)
    return out


def strip_ui(svg):
    root = ET.fromstring(svg.replace('<svg ', f'<svg xmlns="{NS}" ', 1))
    for el in list(root):
        if el.get('class', '') in ('info', 'subs', 'guide'):
            root.remove(el)
    return tostr(root)


def char_parts(el):
    """(tint filter, use href, transform) for every character <use> inside a tint group."""
    out = []
    for u in el.iter(f'{{{NS}}}use'):
        out.append((el.get('filter'), u.get('href'), u.get('transform', '')))
    return out


def head_of(href):
    return 'james' if href.startswith('#j') else 'tawan'


def after(svg, rig, lights, shadow='', light='', atmos='', frame_transform='', scale=1.0,
          char_light=None, prefix='cl', label=''):
    bg, chars, fg, oldlight, motes = split(svg)
    fdefs, cmk = [], []
    for el in chars:
        for i, (tint, href, tr) in enumerate(char_parts(el)):
            m = re.search(r'translate\(([-\d.]+),([-\d.]+)\)\s*scale\(([-\d.]+)\)', tr)
            tx, ty, sc = float(m.group(1)), float(m.group(2)), float(m.group(3))
            centre = (tx, ty + 200 * sc)                 # torso centre in frame space
            lp = (char_light or {}).get(href, lights)
            d = CL.aim(centre, lp)
            uid = f'{prefix}-{href[1:]}'
            f, mk = CL.character(uid, f'<g filter="{tint}"><use href="{href}"/></g>', d, rig,
                                 transform=tr, heads=[(head_of(href), '')], scale=scale, prefix=prefix)
            fdefs.append(f); cmk.append(mk)
    return CL.compose(rig, bg=''.join(bg), shadow=shadow,
                      chars=''.join(cmk) + ''.join(fg),
                      light=''.join(oldlight) + light, atmos=''.join(motes) + atmos,
                      extra_defs=''.join(fdefs), frame_transform=frame_transform, label=label, prefix=prefix)


# ---------------------------------------------------------------- scene 1: night hallway (shot 7)
s7 = SHOTS[6]
WARM_SRC = (-90, 470)          # James's room door, off-frame left: warm spill
night_after = after(
    s7, 'night', WARM_SRC, prefix='n', label='หลัง: ฉากกลางคืน',
    shadow=(CL.contact_shadow(112, 868, 58, strength=1.1) + CL.contact_shadow(430, 878, 52, strength=1.1)
            + CL.ao_line(0, 760, 540, 760, 22, .55) + CL.ao_line(183, 140, 183, 760, 16, .45)
            + CL.ao_line(357, 140, 357, 760, 16, .45) + CL.ao_line(195, 752, 345, 752, 10, .35)),
    light=(CL.falloff(170, 640, 560, .55) + CL.shaft([(0, 380), (0, 600), (360, 960), (140, 960)], '#ffbe82', .30, src=(0, 470), end=(320, 900),
                    dust_n=40, seed=7)
           + CL.shaft([(0, 300), (0, 420), (175, 520), (175, 420)], '#ffc890', .16, src=(0, 360), end=(175, 470))
           + CL.glow(270, 758, 110, '#cfe0ff', .38, core=False) + CL.glow(270, 470, 210, '#9fb4ff', .10, core=False)
           + CL.glow(50, 568, 34, '#9fb4ff', .55, core=False) + CL.glow(488, 592, 34, '#9fb4ff', .55, core=False)
           + CL.glow(-20, 470, 200, '#ffb877', .30, core=False)),
    atmos=CL.shaft([(195, 760), (345, 760), (420, 900), (130, 900)], '#dfe9ff', .18, src=(270, 760), end=(270, 900),
                   dust_n=18, seed=3),
)

# ---------------------------------------------------------------- scene 2: lamp-lit room (shot 4)
s4 = SHOTS[3]
LAMP = (476, 574)
interior_after = after(
    s4, 'interior', LAMP, prefix='i', label='หลัง: ฉากในห้องเปิดไฟ',
    shadow=(CL.ao_line(0, 692, 540, 692, 20, .5) + CL.ao_line(330, 420, 540, 420, 12, .35)
            + CL.ao_corner('M0,90 L150,90 L150,110 L0,110 Z', .4)
            + CL.contact_shadow(484, 690, 34, 6, 1.0)),
    light=(CL.falloff(320, 380, 560, .42, inner=.42) + CL.glow(476, 572, 180, '#ffcf96', .30, core=False) + CL.glow(476, 572, 46, '#fff0dc', .35, core=False)
           + CL.shaft([(452, 580), (500, 568), (330, 700), (120, 700)], '#ffd6a6', .30, src=(476, 574), end=(260, 700),
                      dust_n=34, seed=5)
           + CL.glow(430, 270, 190, '#9fb8ff', .14, core=False)
           ),
)

# ---------------------------------------------------------------- scene 3: face close-up (shot 2, cropped)
s2 = SHOTS[1]
ZOOM = 2.35
FT = f'translate(270,420) scale({ZOOM}) translate(-262,-322)'
REAR_WARM = (-160, 330)          # bedside lamp behind-left, off-frame: warm rim
closeup_after = after(
    s2, 'closeup', REAR_WARM, prefix='c', label='หลัง: ระยะใกล้ใบหน้า', frame_transform=FT, scale=1 / ZOOM * 1.4,
    shadow=CL.ao_line(150, 90, 150, 690, 14, .4),
    light=(CL.falloff(262, 380, 330, .5, inner=.45) + CL.glow(10, 300, 220, '#ffb877', .24, core=False)
           + CL.shaft([(0, 230), (0, 380), (300, 470), (300, 360)], '#ffc58c', .18, src=(0, 300), end=(300, 420),
                      dust_n=30, seed=9)),
)

closeup_before_inner = strip_ui(s2)
closeup_before = re.sub(r'(<svg[^>]*>)', r'\1<g transform="%s">' % FT, closeup_before_inner, count=1).replace('</svg>', '</g></svg>')


def fig(svg, cap):
    return f'<figure>{svg}<figcaption>{cap}</figcaption></figure>'


ROWS = [
    ('ฉากกลางคืน · ทางเดินมืด', 'Low-key · แสงส้มทองจากห้องซ้ายนอกเฟรมทำ rim ฝั่งซ้ายของทั้งสองคน · เงาเย็นเทาอมน้ำเงิน · แสงลอดใต้ประตูมีฝุ่น · เงาสัมผัสใต้เท้า',
     strip_ui(s7), night_after),
    ('ฉากในห้องที่เปิดไฟ', 'โคมโต๊ะขวาล่างเป็นแหล่งแสงหลัก · rim ส้มทองฝั่งขวาของผมและไหล่ · เงานุ่มฝั่งซ้าย · หน้าต่างให้แสงฟ้าเย็นจาง ๆ · AO ตามขอบโต๊ะและมุมตู้',
     strip_ui(s4), interior_after),
    ('ระยะใกล้ใบหน้า', 'แสงจอฟ้าเย็นด้านหน้า + rim ส้มทองจากโคมหลังซ้าย ตามขอบผม หน้า และไหล่ · ไล่เฉดนุ่มบนหน้าและใต้คาง · หน้าตาและลายเส้นเดิมทั้งหมด',
     closeup_before, closeup_after),
]

rows = ''.join(f'''<section>
  <h2>{t}</h2><p class="note">{n}</p>
  <div class="pair">{fig(b, '<b>Before</b> · ระบบปัจจุบัน')}{fig(a, '<b>After</b> · Cinematic 2D Lighting')}</div>
</section>''' for t, n, b, a in ROWS)

PAGE = f'''<title>Odd Hours แสงเงา Before/After</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one section per scene, before/after side by side (stack on phones). Single dark look by choice, like the other Odd Hours sheets. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#ffbf7a;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:900px; margin:0 auto; display:grid; gap:28px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }}
h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
h2 {{ font-size:15px; font-weight:500; margin:0 0 4px; }}
.note {{ font-size:13px; color:var(--muted); margin:0 0 10px; line-height:1.6; }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }}
@media (max-width:560px) {{ .pair {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:6px; }}
figure svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:6px; box-shadow:0 0 0 1px var(--line); overflow:hidden; }}
figcaption {{ font-size:12px; color:var(--muted); }}
figcaption b {{ color:var(--accent); font-weight:500; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">
{''.join(HIDDEN)}
<div class="wrap">
  <h1>Cinematic 2D Lighting<span>Before / After · 3 ฉากจากตอนโอนตีสี่ · ลายเส้นและหน้าตัวละครไม่เปลี่ยน</span></h1>
  {rows}
</div>
'''
out = os.path.join(ROOT, 'out', 'lighting_preview.html')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w').write(PAGE)
print(out, len(PAGE))
