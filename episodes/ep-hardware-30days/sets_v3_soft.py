# ฉากร้านวัสดุ (อิงร้านจริงจาก ref/) -> sets.html
# เฟรม 540x960 แนวตั้ง เว้นช่วง y 576-720 ไว้วางซับ
import random
from interior import frame_int2, EXTRA_DEFS

FONT = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'

DEFS = '''
<filter id="dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2"/></filter>
<filter id="dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.4"/></filter>
<filter id="haze" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="dsh" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="9" dy="13" stdDeviation="6" flood-color="#6a3418" flood-opacity=".38"/></filter>
<filter id="dshS" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="4" dy="6" stdDeviation="3" flood-color="#6a3418" flood-opacity=".34"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%" filterUnits="userSpaceOnUse"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="stipple" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="moteBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<radialGradient id="gVig" gradientUnits="userSpaceOnUse" cx="270" cy="420" r="640"><stop offset=".55" stop-color="#5a2a10" stop-opacity="0"/><stop offset="1" stop-color="#5a2a10" stop-opacity=".42"/></radialGradient>
<!-- exterior -->
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8ec6e0"/><stop offset="1" stop-color="#f4dcae"/></linearGradient>
<linearGradient id="ground" gradientUnits="userSpaceOnUse" x1="0" y1="590" x2="0" y2="960"><stop offset="0" stop-color="#b89a7c"/><stop offset="1" stop-color="#e6c79a"/></linearGradient>
<linearGradient id="spill" gradientUnits="userSpaceOnUse" x1="0" y1="580" x2="0" y2="900"><stop offset="0" stop-color="#ffeedd" stop-opacity=".5"/><stop offset="1" stop-color="#f6cdb8" stop-opacity="0"/></linearGradient>
<linearGradient id="doorBeam" gradientUnits="userSpaceOnUse" x1="280" y1="420" x2="220" y2="860"><stop offset="0" stop-color="#fff2e6" stop-opacity=".30"/><stop offset="1" stop-color="#fff2e6" stop-opacity="0"/></linearGradient>
<radialGradient id="doorGlow" gradientUnits="userSpaceOnUse" cx="282" cy="470" r="230"><stop offset="0" stop-color="#fff0e2" stop-opacity=".55"/><stop offset=".5" stop-color="#f3cbb8" stop-opacity=".18"/><stop offset="1" stop-color="#f3cbb8" stop-opacity="0"/></radialGradient>
<radialGradient id="lampGlow" gradientUnits="userSpaceOnUse" cx="30" cy="150" r="200"><stop offset="0" stop-color="#cfd8ff" stop-opacity=".45"/><stop offset="1" stop-color="#9fb0ff" stop-opacity="0"/></radialGradient>
<linearGradient id="lampBeam" gradientUnits="userSpaceOnUse" x1="30" y1="150" x2="120" y2="600"><stop offset="0" stop-color="#d8dfff" stop-opacity=".22"/><stop offset="1" stop-color="#d8dfff" stop-opacity="0"/></linearGradient>
<radialGradient id="tubeGlow" gradientUnits="userSpaceOnUse" cx="400" cy="300" r="110"><stop offset="0" stop-color="#eef0ff" stop-opacity=".5"/><stop offset="1" stop-color="#cfd8ff" stop-opacity="0"/></radialGradient>
<linearGradient id="sunRay" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="300" y2="960"><stop offset="0" stop-color="#fff0c8" stop-opacity=".34"/><stop offset=".6" stop-color="#ffd890" stop-opacity=".12"/><stop offset="1" stop-color="#ffd890" stop-opacity="0"/></linearGradient>
<radialGradient id="sunPatch" gradientUnits="userSpaceOnUse" cx="200" cy="820" r="420"><stop offset="0" stop-color="#fff2d0" stop-opacity=".55"/><stop offset="1" stop-color="#ffe0a8" stop-opacity=".1"/></radialGradient>
<linearGradient id="winBeam" gradientUnits="userSpaceOnUse" x1="0" y1="200" x2="360" y2="900"><stop offset="0" stop-color="#ffeec4" stop-opacity=".36"/><stop offset=".55" stop-color="#ffd48a" stop-opacity=".12"/><stop offset="1" stop-color="#ffd48a" stop-opacity="0"/></linearGradient>
<!-- interior -->'''+EXTRA_DEFS+'''
<linearGradient id="inWall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e2c9a4"/><stop offset="1" stop-color="#f0dcba"/></linearGradient>
<linearGradient id="floor" gradientUnits="userSpaceOnUse" x1="0" y1="470" x2="0" y2="960"><stop offset="0" stop-color="#e2cba8"/><stop offset="1" stop-color="#c9a47a"/></linearGradient>
<linearGradient id="ftBeam" gradientUnits="userSpaceOnUse" x1="450" y1="120" x2="230" y2="760"><stop offset="0" stop-color="#fff3ea" stop-opacity=".30"/><stop offset=".6" stop-color="#ffe9dc" stop-opacity=".10"/><stop offset="1" stop-color="#ffe9dc" stop-opacity="0"/></linearGradient>
<radialGradient id="ftGlow" gradientUnits="userSpaceOnUse" cx="452" cy="112" r="200"><stop offset="0" stop-color="#fff4ec" stop-opacity=".6"/><stop offset=".5" stop-color="#f4d6c8" stop-opacity=".18"/><stop offset="1" stop-color="#f4d6c8" stop-opacity="0"/></radialGradient>
<radialGradient id="floorPool" gradientUnits="userSpaceOnUse" cx="300" cy="720" r="260"><stop offset="0" stop-color="#f6e2d8" stop-opacity=".35"/><stop offset="1" stop-color="#f6e2d8" stop-opacity="0"/></radialGradient>
<linearGradient id="dustFilm" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff4e0" stop-opacity=".25"/><stop offset="1" stop-color="#fff4e0" stop-opacity="0"/></linearGradient>
'''

TEX = ('<rect width="540" height="960" filter="url(#stipple)" opacity=".10" style="mix-blend-mode:overlay"/>'
       '<rect width="540" height="960" filter="url(#grain)" opacity=".055" style="mix-blend-mode:screen"/>'
       '<rect width="540" height="960" filter="url(#grain)" opacity=".04" style="mix-blend-mode:overlay"/>')
VIG = '<rect width="540" height="960" fill="url(#gVig)"/>'


def dust(seed, box, n, col='#fff4ea'):
    r = random.Random(seed); x0, y0, x1, y1 = box; near = far = ''
    for _ in range(n):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if r.random() < .45:
            far += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.3,2.3):.1f}" opacity="{r.uniform(.22,.42):.2f}"/>'
        else:
            near += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6,1.4):.1f}" opacity="{r.uniform(.5,.9):.2f}"/>'
    return f'<g fill="{col}"><g filter="url(#moteBlur)">{far}</g><g filter="url(#moteGlow)">{near}</g></g>'


def box3(x, y, w, h, c):
    """block-shaded box: light / mid / shadow"""
    lt, md, dk = c
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{md}"/>'
            f'<rect x="{x}" y="{y}" width="{w*.28:.1f}" height="{h}" fill="{lt}"/>'
            f'<rect x="{x+w*.8:.1f}" y="{y}" width="{w*.2:.1f}" height="{h}" fill="{dk}"/>')


# ================= FRAME 1: storefront at dusk =================
def shutter(x, y, w, h, base='#8fb2ac', dark='#739690'):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{base}"/>'
    s += ''.join(f'<rect x="{x}" y="{yy}" width="{w}" height="2" fill="{dark}"/>' for yy in range(int(y)+6, int(y+h), 7))
    s += f'<rect x="{x}" y="{y}" width="{w}" height="10" fill="#8e7c6a"/>'
    s += f'<rect x="{x+w-14}" y="{y}" width="14" height="{h}" fill="#000" opacity=".12"/>'
    return s


def brooms(x, y, n=4, seed=1):
    r = random.Random(seed); s = ''
    for i in range(n):
        bx = x + i*9 + r.uniform(-2, 2); top = y + r.uniform(-8, 6)
        s += f'<rect x="{bx}" y="{top}" width="3" height="70" fill="#a98a6a"/>'
        s += f'<path d="M{bx+1.5},{top-4} l-16,-46 l34,0 Z" fill="#9c7a52"/><path d="M{bx+1.5},{top-4} l-16,-46 l10,0 Z" fill="#b8956a"/><path d="M{bx+1.5},{top-4} l8,-46 l10,0 Z" fill="#7a5c3e"/>'
    return s


def wheelbarrow(tx, ty, sc, tray, trayL, trayD, flip=False):
    f = ' scale(-1,1)' if flip else ''
    return f'''<g transform="translate({tx},{ty}) scale({sc}){f}" filter="url(#dsh)">
<path d="M-6,-58 L-150,-118" stroke="#2c2a36" stroke-width="6" stroke-linecap="round"/>
<path d="M-150,-118 l-22,-6" stroke="#1e1c26" stroke-width="9" stroke-linecap="round"/>
<path d="M-96,-80 L-110,0" stroke="#2c2a36" stroke-width="5"/><path d="M-118,0 l18,0" stroke="#2c2a36" stroke-width="5"/>
<path d="M-128,-128 L60,-128 L20,-56 L-96,-56 Z" fill="{tray}"/>
<path d="M-128,-128 L60,-128 L54,-116 L-122,-116 Z" fill="{trayL}"/>
<path d="M20,-56 L60,-128 L60,-118 L26,-56 Z" fill="{trayD}"/>
<path d="M-80,-56 L-80,-70 L10,-70 L10,-56" fill="none" stroke="{trayD}" stroke-width="3" opacity=".6"/>
<path d="M0,-56 L22,-26" stroke="#2c2a36" stroke-width="5"/>
<circle cx="22" cy="-22" r="24" fill="#1e1c26"/><circle cx="22" cy="-22" r="11" fill="#c43a3a"/><circle cx="19" cy="-25" r="4" fill="#e26a6a"/>
</g>'''


def frame_ext():
    s = '<rect width="540" height="960" fill="#e8d2ae"/>'
    # sky + upper floor (blurred background)
    s += '<g filter="url(#dof)">'
    s += '<rect x="0" y="0" width="540" height="90" fill="url(#sky)"/>'
    s += '<rect x="20" y="40" width="440" height="190" fill="#f2e4c8"/><rect x="20" y="40" width="70" height="190" fill="#fff4dc"/><rect x="380" y="40" width="80" height="190" fill="#d9c09c"/>'
    for x in (40, 360):  # framed windows
        s += f'<rect x="{x}" y="70" width="80" height="120" fill="#cdb08a"/><rect x="{x+12}" y="84" width="56" height="80" fill="#6fa6c4"/><path d="M{x+12},150 L{x+68},100 L{x+68},120 L{x+12},164 Z" fill="#bfe2f0" opacity=".7"/><rect x="{x+38}" y="84" width="3" height="80" fill="#cdb08a"/>'
    s += ''  # upstairs light on
    for x in (150, 250):  # vertical slat windows
        s += f'<rect x="{x}" y="60" width="86" height="160" fill="#5a4436"/>' + ''.join(f'<rect x="{x+4+i*10}" y="64" width="5" height="152" fill="#a8825e"/>' for i in range(8))
    s += '<rect x="460" y="0" width="80" height="250" fill="#d2443a"/><rect x="470" y="30" width="60" height="70" fill="#ffd36a" opacity=".85"/>'  # neighbour sign, out of focus
    s += '</g>'
    # awning underside
    s += '<path d="M0,226 L540,226 L540,300 L0,300 Z" fill="#8a6a54"/>'
    s += ''.join(f'<path d="M{x},226 L{270+(x-270)*1.25:.0f},300" stroke="#6a4e3e" stroke-width="4"/>' for x in range(-40, 600, 60))
    s += '<rect x="0" y="292" width="540" height="10" fill="#5e4434"/><rect x="0" y="222" width="540" height="6" fill="#b48c6a"/>'
    # wall below awning
    s += '<rect x="0" y="302" width="540" height="290" fill="#c9ad8c"/>'
    s += '<rect x="0" y="302" width="540" height="40" fill="#a98c70"/>'
    # pillars
    for x in (128, 406):
        s += f'<rect x="{x}" y="302" width="26" height="290" fill="#dcc3a0"/><rect x="{x}" y="302" width="8" height="290" fill="#f0dcbc"/><rect x="{x+20}" y="302" width="6" height="290" fill="#b49474"/>'
    # neighbours: closed shutters + for-rent sign
    s += shutter(0, 380, 128, 212)
    s += shutter(432, 380, 108, 212)
    s += f'<g transform="translate(26,440)" filter="url(#dshS)"><rect width="52" height="64" fill="#f1ece4"/><rect width="52" height="18" fill="#c7454a"/><text x="26" y="14" text-anchor="middle" {FONT} font-size="11" font-weight="600" fill="#fff">ให้เช่า</text><rect x="8" y="28" width="36" height="3" fill="#a9a2a8"/><rect x="8" y="38" width="30" height="3" fill="#a9a2a8"/><rect x="8" y="48" width="34" height="3" fill="#a9a2a8"/></g>'
    s += '<text x="40" y="374" ' + FONT + ' font-size="9" fill="#6a5040" opacity=".8">15/16</text><text x="452" y="374" ' + FONT + ' font-size="9" fill="#6a5040" opacity=".8">15/14</text>'
    # meter boxes + CCTV
    s += '<rect x="410" y="330" width="16" height="24" rx="2" fill="#cfcad6"/><rect x="412" y="358" width="16" height="24" rx="2" fill="#bfbac6"/>'
    s += '<g transform="translate(372,320)"><rect x="-2" y="0" width="4" height="14" fill="#d8d4de"/><rect x="-10" y="12" width="20" height="12" rx="5" fill="#ecebf0"/><circle cx="-6" cy="18" r="3" fill="#22202c"/></g>'
    # ---- the shop opening ----
    ox, oy, ow, oh = 154, 376, 252, 216
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#e2cfb4"/>'
    # interior back wall + shelves (blurred)
    s += f'<g filter="url(#dof)"><rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="#ecdcc2"/>'
    for i, yy in enumerate((440, 478, 516)):
        s += f'<rect x="{ox+30}" y="{yy}" width="190" height="4" fill="#a8866a"/>'
        r = random.Random(i)
        xx = ox + 32
        while xx < ox + 214:
            w = r.choice((10, 12, 14)); c = r.choice(('#e8e4ea', '#5a8a6a', '#c45a50', '#e0d6b0', '#4a6aa0', '#f0eef2'))
            s += f'<rect x="{xx}" y="{yy-22}" width="{w}" height="22" fill="{c}"/>'
            xx += w + 2
    s += '</g>'
    # hanging goods at top of opening
    r = random.Random(5); hx = ox + 8
    while hx < ox + ow - 10:
        c = r.choice(('#5aa6d6', '#5aa6d6', '#e86a8a', '#f0f0f4', '#4ac0b0', '#f0a050', '#7a6ad0'))
        h = r.uniform(22, 44); w = r.uniform(10, 18)
        s += f'<rect x="{hx:.0f}" y="{oy+8}" width="1.5" height="{h*.4:.0f}" fill="#555"/>'
        s += f'<rect x="{hx-w/2+1:.0f}" y="{oy+8+h*.4:.0f}" width="{w:.0f}" height="{h:.0f}" rx="4" fill="{c}"/><rect x="{hx-w/2+1:.0f}" y="{oy+8+h*.4:.0f}" width="{w*.35:.0f}" height="{h:.0f}" rx="3" fill="#fff" opacity=".25"/>'
        hx += w + r.uniform(2, 6)
    # rolling shutter rolled up
    s += f'<rect x="{ox}" y="{oy-2}" width="{ow}" height="12" fill="#9a8270"/><rect x="{ox}" y="{oy-2}" width="{ow}" height="3" fill="#c2a88e"/>'
    # counter + display stand in doorway
    s += f'<g filter="url(#dshS)"><rect x="{ox+24}" y="520" width="70" height="72" fill="#d8c4a6"/><rect x="{ox+24}" y="520" width="70" height="8" fill="#f4e6cc"/>'
    s += f'<rect x="{ox+30}" y="500" width="34" height="22" rx="2" fill="#2a2834"/><rect x="{ox+33}" y="503" width="28" height="15" fill="#6f7ab8"/></g>'
    s += f'<g filter="url(#dshS)"><rect x="318" y="460" width="64" height="132" fill="#2c3c86"/><rect x="318" y="460" width="64" height="16" fill="#3a4ca0"/><text x="350" y="472" text-anchor="middle" {FONT} font-size="8" fill="#e8ecff">ก๊อก · ฝักบัว</text>'
    s += ''.join(f'<rect x="{324+(i%3)*19}" y="{482+(i//3)*24}" width="15" height="20" rx="2" fill="#dfe4f0"/><circle cx="{331.5+(i%3)*19}" cy="{492+(i//3)*24}" r="4" fill="none" stroke="#8a93a8" stroke-width="1.6"/>' for i in range(12))
    s += '<rect x="318" y="460" width="10" height="132" fill="#000" opacity=".15"/></g>'
    # rack of seed/sundry packs left of door
    s += f'<g filter="url(#dshS)"><rect x="160" y="526" width="40" height="66" fill="#b0a08e"/>' + ''.join(f'<rect x="{163+(i%3)*12}" y="{530+(i//3)*15}" width="10" height="12" fill="{c}"/>' for i, c in enumerate(['#6ab07a', '#e8d88a', '#6ab07a', '#d86a6a', '#6ab07a', '#e8d88a', '#6aa0c0', '#6ab07a', '#d86a6a', '#e8d88a', '#6ab07a', '#6aa0c0'])) + '</g>'
    # door glow
    s += f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="url(#doorGlow)" style="mix-blend-mode:screen"/>'
    # shop sign (muted cream-yellow, no phone number)
    s += f'<g transform="translate(188,316)" filter="url(#dshS)"><rect width="122" height="48" fill="#e6d48a"/><rect width="122" height="48" fill="none" stroke="#c9b468" stroke-width="2"/><text x="61" y="20" text-anchor="middle" {FONT} font-size="13.5" font-weight="700" fill="#b02a2a">ร้านรุ่งเจริญฮาร์ดแวร์</text><text x="61" y="34" text-anchor="middle" {FONT} font-size="7.5" fill="#2a2a6a">ขายอุปกรณ์ก่อสร้างทุกชนิด</text><rect x="20" y="39" width="82" height="3" fill="#2a2a6a" opacity=".5"/></g>'
    s += f'<text x="280" y="372" {FONT} font-size="9" fill="#6a5040" opacity=".85">15/15</text>'
    # fluorescent tube under awning
    s += '<rect x="360" y="304" width="70" height="5" rx="2" fill="#f4f6ff"/><circle cx="395" cy="306" r="110" fill="url(#tubeGlow)" style="mix-blend-mode:screen"/>'
    # banner: faded paint-shop banner, torn strips (generic, no brand logo)
    s += '<g filter="url(#dsh)">'
    s += f'<path d="M102,196 L388,200 L386,272 L104,266 Z" fill="#e2d39a"/>'
    s += f'<path d="M102,196 L388,200 L388,210 L102,206 Z" fill="#c9524e"/>'
    s += f'<path d="M110,212 L176,213 L176,260 L110,258 Z" fill="#2a3f86"/><text x="143" y="242" text-anchor="middle" {FONT} font-size="17" font-weight="700" fill="#f2efe4">สี</text>'
    s += f'<text x="186" y="232" {FONT} font-size="15" font-weight="700" fill="#3a2a2a">ร้านนี้ขายสี</text><text x="186" y="252" {FONT} font-size="10" fill="#5a3a3a">สีทาไม้ · สีทาปูน · สีทาเหล็ก</text>'
    s += f'<rect x="300" y="216" width="78" height="44" fill="#d6c486"/>' + ''.join(f'<rect x="{304+i*12}" y="222" width="9" height="13" fill="{c}"/>' for i, c in enumerate(['#3a5aa0', '#c44a4a', '#3a5aa0', '#4a8a5a', '#c44a4a', '#3a5aa0']))
    # torn strips hanging off bottom edge
    for i, x in enumerate(range(116, 384, 14)):
        if i % 3 == 0: continue
        L = 10 + (i * 7) % 22
        s += f'<path d="M{x},{266+(x-104)*0.02:.0f} l10,0 l-1,{L} l-8,0 Z" fill="#d8c88e"/>'
    s += '</g>'
    s += '<path d="M240,198 L246,270" stroke="#b8a878" stroke-width="2"/>'  # seam
    # grey faded cloth hanging at left
    s += '<path d="M60,206 L102,204 L150,420 L118,436 Z" fill="#d4c6b4" filter="url(#dshS)"/><path d="M60,206 L76,206 L124,432 L118,436 Z" fill="#ece0ce"/>'
    # step / sidewalk tiles
    s += '<rect x="0" y="592" width="540" height="18" fill="#e4d4bc"/><rect x="0" y="592" width="540" height="4" fill="#fff2dc"/>'
    s += ''.join(f'<rect x="{x}" y="596" width="2" height="14" fill="#bca486"/>' for x in range(30, 540, 64))
    # concrete forecourt
    s += '<rect x="0" y="610" width="540" height="350" fill="url(#ground)"/>'
    s += '<path d="M0,690 L540,700" stroke="#a48868" stroke-width="2" opacity=".6"/><path d="M0,820 L540,836" stroke="#b8946c" stroke-width="2" opacity=".6"/>'
    s += '<ellipse cx="250" cy="830" rx="120" ry="34" fill="#9a7a5a" opacity=".35" filter="url(#soft)"/>'  # old stain
    s += '<path d="M60,760 q40,-10 80,6 q30,12 60,-4" fill="none" stroke="#a07e5c" stroke-width="3" opacity=".6"/>'
    # awning shade on forecourt, sunlit beyond
    s += '<path d="M0,610 L540,610 L540,690 L0,668 Z" fill="#7a5238" opacity=".28"/>'
    s += '<path d="M0,668 L540,690 L540,960 L0,960 Z" fill="url(#sunPatch)" style="mix-blend-mode:screen"/>'
    s += '<path d="M0,302 L540,302 L540,360 L0,420 Z" fill="#6a3a20" opacity=".16"/>'
    s += '<path d="M154,376 L250,376 L190,592 L154,592 Z" fill="#6a3a20" opacity=".14"/>'
    # stone table + benches (left)
    s += '<g filter="url(#dsh)">'
    s += '<path d="M36,600 L150,600 L156,612 L30,612 Z" fill="#fbf2e2"/><rect x="30" y="612" width="126" height="6" fill="#d2bfa4"/><rect x="82" y="618" width="22" height="46" fill="#e6d6be"/><rect x="82" y="618" width="7" height="46" fill="#fbf2e2"/>'
    s += '<rect x="0" y="640" width="70" height="10" fill="#fbf2e2"/><rect x="0" y="650" width="70" height="4" fill="#cdb698"/><rect x="10" y="654" width="12" height="26" fill="#e2d0b6"/><rect x="48" y="654" width="12" height="26" fill="#d4c0a2"/>'
    s += '<rect x="120" y="646" width="78" height="10" fill="#fbf2e2"/><rect x="120" y="656" width="78" height="4" fill="#cdb698"/><rect x="130" y="660" width="12" height="28" fill="#e2d0b6"/><rect x="176" y="660" width="12" height="28" fill="#d4c0a2"/>'
    s += '</g>'
    # broom stand right of door
    s += '<g filter="url(#dshS)">' + brooms(414, 520, 4, 3) + '<rect x="408" y="560" width="44" height="40" fill="#3e5a9a" opacity=".9"/><rect x="408" y="560" width="44" height="5" fill="#5a78b8"/></g>'
    # ladders wrapped in plastic (right edge)
    s += '<g filter="url(#dsh)"><rect x="492" y="430" width="44" height="300" fill="#ece2d2"/><rect x="492" y="430" width="12" height="300" fill="#fff8ec"/>'
    s += ''.join(f'<rect x="496" y="{y}" width="36" height="4" fill="#9a96a6"/>' for y in range(450, 720, 34))
    s += '<rect x="492" y="500" width="44" height="22" fill="#c8484a" opacity=".85"/><rect x="492" y="610" width="44" height="22" fill="#c8484a" opacity=".85"/><rect x="492" y="430" width="44" height="300" fill="#fff" opacity=".18"/></g>'
    # wheelbarrows (foreground, blue + orange)
    s += wheelbarrow(500, 800, 1.0, '#2f6fd0', '#5a92ea', '#1f4fa0')
    s += wheelbarrow(420, 930, 1.2, '#e2683a', '#f08c5a', '#b44a24')
    # afternoon sun from upper left: slanted rays + dust
    s += '<path d="M-40,0 L120,0 L420,960 L160,960 Z" fill="url(#sunRay)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
    s += '<path d="M150,0 L210,0 L560,800 L470,860 Z" fill="url(#sunRay)" opacity=".6" filter="url(#haze)" style="mix-blend-mode:screen"/>'
    s += dust(31, (40, 120, 360, 560), 26, '#fff4dc')
    s += '<rect width="540" height="960" fill="#ffa850" opacity=".10" style="mix-blend-mode:multiply"/>'
    s += VIG + TEX
    return s


# ================= FRAME 2: interior aisle =================
VPX, VPY = 340, 372


def lerp(a, b, t): return a + (b - a) * t


def persp(t):  # depth 0 near .. 1 far, non-linear
    return 1 - 1 / (1 + 4 * t) * (1) if False else (t * 1.0) / (t + (1 - t) * 0.28)


def shelf_pt(t, h):
    s = persp(t)
    x = lerp(566, 432, s)
    ytop = lerp(150, 300, s); ybot = lerp(900, 478, s)
    return x, lerp(ybot, ytop, h)


def quad(p, c, extra=''):
    return f'<path d="M{p[0][0]:.1f},{p[0][1]:.1f} L{p[1][0]:.1f},{p[1][1]:.1f} L{p[2][0]:.1f},{p[2][1]:.1f} L{p[3][0]:.1f},{p[3][1]:.1f} Z" fill="{c}"{extra}/>'


def frame_int():
    s = '<rect width="540" height="960" fill="url(#inWall)"/>'
    # ceiling
    s += '<path d="M0,0 L540,0 L540,110 L432,300 L250,300 L0,110 Z" fill="#94684a"/>'
    # back area (far, blurred): back wall with paint shelves
    s += '<g filter="url(#dof2)">'
    s += '<rect x="250" y="300" width="182" height="178" fill="#d8bb94"/>'
    for yy in (340, 380, 420, 460):
        s += f'<rect x="256" y="{yy}" width="170" height="3" fill="#8a6a50"/>'
        r = random.Random(yy); xx = 258
        while xx < 420:
            c = r.choice(('#c94a4a', '#e8e2e8', '#3a6aa8', '#e0c070', '#4a8a5a', '#2a2a30'))
            s += f'<rect x="{xx}" y="{yy-18}" width="9" height="18" fill="{c}"/>'
            xx += 11
    s += '</g>'
    # upper loft shelf on far-left wall with boxes (blurred)
    s += '<g filter="url(#dof)"><path d="M0,40 L250,150 L250,300 L0,260 Z" fill="#d2b48e"/>'
    s += '<path d="M0,120 L250,198 L250,204 L0,128 Z" fill="#8a6a50"/><path d="M0,250 L250,296 L250,302 L0,258 Z" fill="#8a6a50"/>'
    r = random.Random(9)
    for i in range(6):
        x0 = i * 40; x1 = x0 + 36
        y0b = lerp(250, 296, x0/250); y1b = lerp(250, 296, x1/250)
        hb = 46 - i*3
        s += quad(((x0, y0b), (x1, y1b), (x1, y1b-hb), (x0, y0b-hb)), r.choice(('#b08a62', '#a07a58', '#c09a70')))
        s += quad(((x0, y0b-hb*.5), (x1, y1b-hb*.5), (x1, y1b-hb*.5-8), (x0, y0b-hb*.5-8)), '#e8e0d8', ' opacity=".7"')
    s += '</g>'
    # paint aisle behind gondola (left, blurred)
    s += '<g filter="url(#dof)"><rect x="0" y="300" width="80" height="420" fill="#c8a882"/>'
    for yy in (380, 450, 520, 590):
        s += f'<rect x="0" y="{yy}" width="80" height="4" fill="#7a5a42"/>'
        r = random.Random(yy+1); xx = 2
        while xx < 76:
            c = r.choice(('#c94a4a', '#ece6ec', '#3a8a5a', '#e0c070', '#2a2a30'))
            s += f'<rect x="{xx}" y="{yy-26}" width="12" height="26" fill="{c}"/><rect x="{xx}" y="{yy-26}" width="12" height="6" fill="#d8d2d8"/>'
            xx += 14
    s += '</g>'
    # floor + tile grid
    s += '<path d="M0,720 L250,478 L432,478 L540,560 L540,960 L0,960 Z" fill="url(#floor)"/>'
    for i in range(-6, 14):
        x = 340 + i * 90
        s += f'<path d="M{VPX + (x-VPX)*0.17:.0f},478 L{x},960" stroke="#b08e68" stroke-width="1.6" opacity=".7"/>'
    for y in (500, 530, 572, 630, 712, 830):
        s += f'<path d="M0,{y} L540,{y}" stroke="#b08e68" stroke-width="1.6" opacity=".6"/>'
    s += '<rect width="540" height="960" fill="url(#floorPool)" style="mix-blend-mode:screen"/>'
    # ---- right wall steel shelving with boxes ----
    levels = [0, .2, .4, .6, .8, 1.0]
    posts = [0, .25, .5, .75, 1.0]
    # back panel
    s += quad((shelf_pt(0, 0), shelf_pt(1, 0), shelf_pt(1, 1), shelf_pt(0, 1)), '#7a5038')
    r = random.Random(4)
    boxcols = [('#eaa866', '#c8813e', '#9a5a2a'), ('#e09a58', '#bc7436', '#8e5024'), ('#f0b878', '#d08e4a', '#a46630')]
    for li in range(len(levels)-1):
        h0, h1 = levels[li], levels[li+1]
        t = 0.0
        while t < 0.98:
            dt = r.uniform(.07, .12); tb = min(t + dt, 1)
            hb = h0 + (h1-h0) * r.uniform(.62, .9)
            c = r.choice(boxcols)
            p0 = shelf_pt(t+.005, h0+.012); p1 = shelf_pt(tb-.005, h0+.012); p2 = shelf_pt(tb-.005, hb); p3 = shelf_pt(t+.005, hb)
            s += quad((p0, p1, p2, p3), c[1])
            # front face slice (light side towards aisle)
            s += quad((p0, (lerp(p0[0], p1[0], .22), lerp(p0[1], p1[1], .22)), (lerp(p3[0], p2[0], .22), lerp(p3[1], p2[1], .22)), p3), c[0])
            # red brand-less label band + handwritten number
            if r.random() < .7:
                a = .55; b = .75
                q = ((lerp(p3[0], p2[0], .3), lerp(lerp(p3[1], p0[1], a), lerp(p2[1], p1[1], a), .3)),
                     (lerp(p3[0], p2[0], .85), lerp(lerp(p3[1], p0[1], a), lerp(p2[1], p1[1], a), .85)),
                     (lerp(p3[0], p2[0], .85), lerp(lerp(p3[1], p0[1], b), lerp(p2[1], p1[1], b), .85)),
                     (lerp(p3[0], p2[0], .3), lerp(lerp(p3[1], p0[1], b), lerp(p2[1], p1[1], b), .3)))
                s += quad(q, '#a83a3a' if r.random() < .6 else '#ece4da')
            # dust film on top of box
            s += quad((p3, p2, (p2[0], p2[1]+4), (p3[0], p3[1]+4)), '#fff0d8', ' opacity=".3"')
            t = tb + .01
        # shelf plank
        a0 = shelf_pt(0, h0); a1 = shelf_pt(1, h0)
        s += quad((a0, a1, (a1[0], a1[1]+3), (a0[0], a0[1]+8)), '#b8a48e')
        s += quad(((a0[0], a0[1]+8), (a1[0], a1[1]+3), (a1[0], a1[1]+5), (a0[0], a0[1]+14)), '#6a5240')
    # top plank
    a0 = shelf_pt(0, 1); a1 = shelf_pt(1, 1)
    s += quad((a0, a1, (a1[0], a1[1]+3), (a0[0], a0[1]+8)), '#b8a48e')
    for tp in posts:
        b0 = shelf_pt(tp, 0); b1 = shelf_pt(tp, 1); w = lerp(14, 4, persp(tp))
        s += f'<path d="M{b0[0]-w:.1f},{b0[1]:.1f} L{b0[0]:.1f},{b0[1]:.1f} L{b1[0]:.1f},{b1[1]:.1f} L{b1[0]-w:.1f},{b1[1]:.1f} Z" fill="#8a7462"/>'
        s += f'<path d="M{b0[0]-w:.1f},{b0[1]:.1f} L{b0[0]-w*.6:.1f},{b0[1]:.1f} L{b1[0]-w*.6:.1f},{b1[1]:.1f} L{b1[0]-w:.1f},{b1[1]:.1f} Z" fill="#c4ae96"/>'
    # pink + green baskets on a shelf (real detail)
    p = shelf_pt(.38, .4)
    s += f'<g filter="url(#dshS)"><path d="M{p[0]-44:.0f},{p[1]-26:.0f} l48,0 l-6,22 l-36,0 Z" fill="#e26aa0"/><path d="M{p[0]-44:.0f},{p[1]-26:.0f} l48,0 l0,4 l-48,0 Z" fill="#f08cbc"/></g>'
    # ---- gondola end cap (main subject) ----
    gx0, gx1, gy0, gy1 = 76, 312, 300, 770
    # side panel receding to VP
    s += f'<path d="M{gx1},{gy0} L{gx1+28},{gy0+14} L{gx1+28},{gy1-60} L{gx1},{gy1} Z" fill="#2a201e"/>'
    s += f'<g filter="url(#dsh)"><rect x="{gx0}" y="{gy0}" width="{gx1-gx0}" height="{gy1-gy0}" fill="#3a2e2c"/>'
    s += f'<rect x="{gx0}" y="{gy0}" width="10" height="{gy1-gy0}" fill="#56443e"/><rect x="{gx1-10}" y="{gy0}" width="10" height="{gy1-gy0}" fill="#2a201e"/>'
    s += f'<rect x="{gx0-6}" y="{gy1-40}" width="{gx1-gx0+12}" height="40" fill="#30262a"/><rect x="{gx0-6}" y="{gy1-40}" width="{gx1-gx0+12}" height="6" fill="#5a4840"/></g>'
    # pegboard holes
    s += '<g fill="#1e1614">' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.2"/>' for x in range(gx0+16, gx1-10, 14) for y in range(gy0+12, gy1-50, 14)) + '</g>'
    # hanging blister packs: cutting discs, pliers, tape
    r = random.Random(12)
    rows = [(316, 54), (382, 52), (446, 54), (512, 50), (574, 52), (636, 46)]
    for ry, rh in rows:
        x = gx0 + 16
        while x < gx1 - 40:
            w = r.choice((24, 28, 30, 34))
            kind = r.random()
            s += f'<rect x="{x+w/2-1:.0f}" y="{ry-8}" width="2" height="10" fill="#9a98a8"/>'
            g = f'<g filter="url(#dshS)">'
            if kind < .45:  # disc card
                head = r.choice(('#3a5aa8', '#c43a3a', '#2a2a30', '#e2b040'))
                g += f'<rect x="{x}" y="{ry}" width="{w}" height="{rh-12}" rx="2" fill="#e6e2ea"/><rect x="{x}" y="{ry}" width="{w}" height="12" fill="{head}"/>'
                dc = r.choice(('#c45a2a', '#8a3a2a', '#d8d4dc', '#3a3a44', '#d9a040'))
                g += f'<circle cx="{x+w/2:.0f}" cy="{ry+(rh-12)/2+6:.0f}" r="{w*.36:.0f}" fill="{dc}"/><circle cx="{x+w/2:.0f}" cy="{ry+(rh-12)/2+6:.0f}" r="{w*.1:.0f}" fill="#e6e2ea"/><path d="M{x+w/2-w*.3:.0f},{ry+(rh-12)/2+2:.0f} a{w*.3:.0f},{w*.3:.0f} 0 0 1 {w*.3:.0f},-{w*.2:.0f}" stroke="#fff" stroke-width="2" fill="none" opacity=".4"/>'
            elif kind < .75:  # tool in clear pack
                head = r.choice(('#c43a3a', '#e8c040', '#3a7ac0'))
                g += f'<rect x="{x}" y="{ry}" width="{w}" height="{rh-8}" rx="3" fill="{head}"/><rect x="{x+5}" y="{ry+14}" width="{w-10}" height="{rh-28}" rx="3" fill="#f0eef4" opacity=".55"/>'
                g += ''.join(f'<rect x="{x+6+k*6:.0f}" y="{ry+16}" width="4" height="{rh-26}" rx="2" fill="{r.choice(("#e84a3a","#f0d040","#2a2a30","#3a7ac0"))}"/>' for k in range(int((w-10)//6)))
            else:  # gloves / strap
                c = r.choice(('#f08a3a', '#e2e0e8', '#d8c040'))
                g += f'<rect x="{x}" y="{ry}" width="{w}" height="{rh+r.uniform(-4,16):.0f}" rx="4" fill="{c}"/><rect x="{x}" y="{ry}" width="{w*.3:.0f}" height="{rh:.0f}" rx="3" fill="#fff" opacity=".22"/>'
            s += g + '</g>'
            x += w + 4
    # hi-vis vests on far left of gondola
    s += f'<g filter="url(#dshS)"><path d="M{gx0+4},310 l34,0 l6,90 l-46,0 Z" fill="#f07a3a"/><rect x="{gx0+4}" y="340" width="40" height="6" fill="#e8f040"/><rect x="{gx0+4}" y="370" width="42" height="6" fill="#e8f040"/></g>'
    # PVC pipes bundle sticking out the top
    r = random.Random(21)
    pipes = ''
    for i in range(16):
        c = r.choice((('#5c8fc6', '#7eaee0', '#3f6c9c'), ('#cdb85a', '#e2d07a', '#a8963e'), ('#8a8f99', '#a8adb8', '#6a6f7a'), ('#e8e6ec', '#ffffff', '#b8b6c0')))
        x = 150 + i * 12 + r.uniform(-6, 6); ang = r.uniform(-34, -18); L = r.uniform(170, 240); w = r.uniform(9, 14)
        pipes += f'<g transform="translate({x:.0f},322) rotate({ang:.0f})"><rect x="0" y="{-w/2:.1f}" width="{L:.0f}" height="{w:.1f}" fill="{c[0]}"/><rect x="0" y="{-w/2:.1f}" width="{L:.0f}" height="{w*.3:.1f}" fill="{c[1]}"/><rect x="0" y="{w*.25:.1f}" width="{L:.0f}" height="{w*.25:.1f}" fill="{c[2]}"/><ellipse cx="{L:.0f}" cy="0" rx="2.5" ry="{w/2:.1f}" fill="#1e1c24"/></g>'
    s += f'<g filter="url(#dsh)">{pipes}</g>'
    # plastic bag of fittings hanging on pipes
    s += '<path d="M382,236 q30,-8 40,16 l-4,70 q-20,10 -40,0 Z" fill="#e8e6f0" opacity=".55"/>'
    # ---- red rope bundle in plastic (top right) ----
    s += '<g filter="url(#dsh)"><rect x="452" y="0" width="70" height="70" rx="10" fill="#3a5aa8"/><ellipse cx="487" cy="96" rx="44" ry="38" fill="#c43a3a"/><ellipse cx="474" cy="88" rx="22" ry="16" fill="#e2585a"/><path d="M446,96 q41,30 82,0" fill="none" stroke="#8a2a2a" stroke-width="3"/><rect x="440" y="40" width="94" height="96" rx="20" fill="#fff" opacity=".2"/></g>'
    # ---- fluorescent tube (light source) ----
    s += '<path d="M412,120 L500,92 L503,100 L415,128 Z" fill="#f6f6ff"/>'
    s += '<circle cx="452" cy="112" r="200" fill="url(#ftGlow)" style="mix-blend-mode:screen"/>'
    # ---- foreground: paint buckets (left) ----
    def bucket(x, y, w, h, band, lid='#d8d2dc'):
        return (f'<g filter="url(#dsh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#e6e2ea"/><rect x="{x}" y="{y}" width="{w*.25:.0f}" height="{h}" fill="#f4f2f6"/><rect x="{x+w*.78:.0f}" y="{y}" width="{w*.22:.0f}" height="{h}" fill="#b8b2c0"/>'
                f'<rect x="{x}" y="{y+h*.35:.0f}" width="{w}" height="{h*.4:.0f}" fill="{band}"/><rect x="{x+w*.78:.0f}" y="{y+h*.35:.0f}" width="{w*.22:.0f}" height="{h*.4:.0f}" fill="#000" opacity=".22"/>'
                f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{w*.12:.0f}" fill="{lid}"/><ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{w*.12:.0f}" fill="url(#dustFilm)"/></g>')
    s += bucket(-10, 830, 96, 110, '#3a8a5a') + bucket(70, 860, 90, 100, '#c44a4a') + bucket(14, 744, 74, 86, '#3a8a5a') + bucket(84, 790, 66, 72, '#2a2a30')
    # ---- foreground: cement / tile-adhesive sacks (right) ----
    def sack(x, y, w, h, band):
        return (f'<g filter="url(#dsh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#e4e0e8"/><rect x="{x}" y="{y}" width="{w}" height="{h*.35:.0f}" rx="12" fill="#f2f0f4"/><rect x="{x}" y="{y+h*.7:.0f}" width="{w}" height="{h*.3:.0f}" rx="12" fill="#bcb6c4"/>'
                f'<rect x="{x+w*.12:.0f}" y="{y+h*.3:.0f}" width="{w*.6:.0f}" height="{h*.26:.0f}" fill="{band}"/><text x="{x+w*.42:.0f}" y="{y+h*.5:.0f}" text-anchor="middle" {FONT} font-size="{h*.2:.0f}" font-weight="700" fill="#fff">ปูน</text></g>')
    for i, yy in enumerate(range(700, 940, 46)):
        s += sack(300 + (i % 2)*8, yy, 200, 54, '#c43a3a' if i % 2 else '#3a8a5a')
    s += sack(250, 880, 220, 80, '#3a8a5a')
    # basket on sacks
    s += '<g filter="url(#dshS)"><path d="M330,690 l90,0 l-10,22 l-70,0 Z" fill="#5ac08a"/><path d="M330,690 l90,0 l0,5 l-90,0 Z" fill="#7ad8a6"/></g>'
    # afternoon sun through the shop front (behind camera): warm beam + window-bar shadows + dust
    s += '<path d="M0,120 L150,60 L470,960 L0,960 Z" fill="url(#winBeam)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
    s += '<path d="M432,300 L540,110 L540,960 L432,478 Z" fill="#5a2e14" opacity=".14"/>'
    s += '<path d="M0,720 L250,478 L300,478 L210,960 L0,960 Z" fill="#fff0c8" opacity=".2" style="mix-blend-mode:screen"/>'
    s += '<path d="M0,560 L120,520 L330,960 L60,960 Z" fill="#fff0c8" opacity=".18" style="mix-blend-mode:screen"/>'
    s += '<path d="M118,520 L140,512 L360,960 L330,960 Z" fill="#7a4a2a" opacity=".12"/>'
    s += dust(41, (40, 180, 360, 640), 34, '#fff4dc')
    s += '<rect width="540" height="960" fill="#ffa850" opacity=".10" style="mix-blend-mode:multiply"/>'
    s += VIG + TEX
    return s


FRAMES = [
    ('ฉาก 1 · หน้าร้านตอนบ่าย', 'ร้านรุ่งเจริญฮาร์ดแวร์ ห้องแถวสองชั้น แดดบ่ายสีทองส่องเฉียงจากซ้าย ป้ายผ้าขาดรุ่ย ห้องข้าง ๆ ปิดและติดป้ายให้เช่า มีโต๊ะหินกับรถเข็นปูนอยู่หน้าร้าน', frame_ext()),
    ('ฉาก 2 · หลังเคาน์เตอร์', 'มองตรงจากหน้าเคาน์เตอร์เข้าหาผนังหลังร้าน ซ้ายเป็นชั้นสี กลางเป็นแผงแขวนเครื่องมือ ขวาเป็นตู้ลิ้นชักน็อตกับสายยาง ฉากหน้าเป็นตู้กระจกกับของบนเคาน์เตอร์ แดดบ่ายส่องเข้ามาจากประตูร้านทางซ้าย', frame_int2(dust)),
]


def page():
    cards = ''.join(
        f'<figure><div class="frame"><svg viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{t}">{svg}'
        f'<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".75" stroke-dasharray="6 5" stroke-width="1.5"/>'
        f'<text x="270" y="652" text-anchor="middle" {FONT} font-size="15" fill="#fff" fill-opacity=".8">พื้นที่ซับ</text></g></svg></div>'
        f'<figcaption><b>{t}</b><small>{n}</small></figcaption></figure>' for t, n, svg in FRAMES)
    return f'''<title>ฉากร้านรุ่งเจริญ</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&display=swap">
<style>
/* Single dark look by choice: matches the channel's frame-review pages. */
:root{{--stage:#0d0f14;--ink:#d6d8e2;--muted:#8a8ea0;--line:#2a2e3a;--accent:#8f86ff;color-scheme:dark}}
html,body{{margin:0;background:var(--stage);color:var(--ink);font-family:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif}}
.wrap{{max-width:900px;margin:0 auto;padding-block:20px 32px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
header{{display:flex;flex-wrap:wrap;gap:12px;align-items:end;justify-content:space-between;margin-bottom:16px}}
h1{{font-size:18px;font-weight:600;margin:0}} h1 span{{display:block;font-size:13px;font-weight:400;color:var(--muted);margin-top:2px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}}
figure{{margin:0}} .frame{{aspect-ratio:9/16;box-shadow:0 0 0 1px var(--line),0 20px 50px rgba(0,0,0,.5)}}
.frame svg{{display:block;width:100%;height:100%}}
figcaption{{margin-top:10px;font-size:13px;line-height:1.6}} figcaption small{{display:block;color:var(--muted)}}
.guide{{display:none}} .show-guide .guide{{display:inline}}
button{{font:inherit;font-size:13px;color:var(--ink);background:transparent;border:1px solid var(--line);border-radius:6px;padding:6px 12px;cursor:pointer}}
button:hover{{border-color:var(--muted)}} button:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
button[aria-pressed="true"]{{border-color:var(--accent);color:#fff}}
</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{DEFS}</defs></svg>
<div class="wrap" id="wrap"><header><h1>ฉากร้านวัสดุ (อิงร้านจริง)<span>ซีรีส์ร้านแม่เหลือ 30 วัน · ฉากกลางวัน โทนร้อน · ยังไม่ใส่ตัวละคร</span></h1>
<button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''


if __name__ == '__main__':
    open('sets.html', 'w').write(page()); print('ok')
