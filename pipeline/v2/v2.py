"""Builds v2.html: the revised episode (13 shots) with animation hooks driven by setT(shot, t)."""
import os, re, json, runpy, base64
HERE = os.path.dirname(os.path.abspath(__file__))
SB = os.path.join(HERE, '..', 'sb')
os.chdir(SB)
A = runpy.run_path('all12.py')
os.chdir(HERE)
G = A['G']; S = A['S']; A8 = A['A']
FONT = G['FONT']; dust = A['dust']; hall = A['hall']; VIG = A['VIG']; TEX = A['TEX']
room_top = A['room_top']; bg = A['bg']; tag = A['tag']; FT = A['FT']; wlen = A['wlen']
TL = json.load(open('timeline.json'))
SH = {s['key']: s for s in TL['shots']}


def rep(s, o, n, count=1):
    assert o in s, o[:100]
    return s.replace(o, n, count)


def group_by_id(src, gid):
    a = src.index(f'<g id="{gid}">'); i = a + 3; depth = 1
    while depth:
        o = src.find('<g', i); c = src.find('</g>', i)
        if o != -1 and o < c and src[o + 2] in ' >':
            depth += 1; i = o + 2
        else:
            depth -= 1; i = c + 4
    return src[a:i]


page = open(os.path.join(SB, 'storyboard3.html')).read()
head = page[:page.index('<div class="wrap"')]

# ---- lids + talking mouths in the shared heads (same parts as the animated v1) ----
lidJ = ('<g class="blinkJ"><path d="M -22,-3 C -18,-8.5 -8,-8.5 -4,-2 C -8,1.5 -18,1.5 -22,-3 Z" fill="#fbe7d8"/>'
        '<path d="M 22,-3 C 18,-8.5 8,-8.5 4,-2 C 8,1.5 18,1.5 22,-3 Z" fill="#f6dccb"/>'
        '<path d="M -21,-1.5 C -17,1.2 -9,1.2 -5,-1.2 M 21,-1.5 C 17,1.2 9,1.2 5,-1.2" stroke="#17151d" stroke-width="1.8" fill="none" stroke-linecap="round"/></g>\n')
head = head.replace('    <!-- glasses: round, thin silver wire -->', lidJ + '    <!-- glasses: round, thin silver wire -->')
mouthJ = '<g class="mouthJ"><ellipse cx="1" cy="24.2" rx="4.6" ry="3.4" fill="#6b3a3a"/><ellipse cx="1" cy="25.6" rx="2.6" ry="1.3" fill="#b0605a"/></g>\n'
mouthJS = '<g class="mouthJ"><ellipse cx="0" cy="25.5" rx="6" ry="6.4" fill="#fbe7d8"/><ellipse cx="0" cy="25.6" rx="4.4" ry="2.4" fill="#6b3a3a"/></g>\n'
hp_parts = head.split('    <!-- hair: short, chunky spikes -->')
out = hp_parts[0]
for k, part in enumerate(hp_parts[1:]):
    out += (mouthJ if k == 0 else mouthJS) + '    <!-- hair: short, chunky spikes -->' + part
head = out
lidT = ('<g class="blinkT"><path d="M -23.5,-1.5 C -19,-10 -7,-10 -3,-2 C -8,3.6 -18,3.6 -23.5,-1.5 Z" fill="#f8d2ab"/>'
        '<path d="M 23.5,-1.5 C 19,-10 7,-10 3,-2 C 8,3.6 18,3.6 23.5,-1.5 Z" fill="#f4caa2"/>'
        '<path d="M -22,0 C -17,3.2 -9,3.2 -4,0.2 M -21.5,0.4 L -26,-1.8 M 22,0 C 17,3.2 9,3.2 4,0.2 M 21.5,0.4 L 26,-1.8" stroke="#1a1118" stroke-width="2" fill="none" stroke-linecap="round"/></g>\n')
mouthT = '<g class="mouthT"><ellipse cx="0" cy="23.4" rx="4.6" ry="3.6" fill="#8a3436"/><path d="M -3.6,21.4 Q 0,20.6 3.6,21.4 L 3.2,22.6 Q 0,22 -3.2,22.6 Z" fill="#fff8f0"/></g>\n'
mouthTS = '<g class="mouthT"><ellipse cx="0" cy="24.2" rx="5.6" ry="6.4" fill="#f8d2ab"/><ellipse cx="0" cy="24.4" rx="4.2" ry="2.2" fill="#7a3434"/></g>\n'
anchor = '    <!-- crown: same outline as the back hair'
parts = head.split(anchor)
out = parts[0]
for k, p in enumerate(parts[1:]):
    out += (mouthT if k == 0 else mouthTS) + lidT + anchor + p
head = out
lidC = ('<g class="blinkC"><path d="M -41,-7 C -36,-21 -14,-21 -9,-6 C -14,4 -36,4 -41,-7 Z" fill="#e79a4a"/>'
        '<path d="M 41,-7 C 36,-21 14,-21 9,-6 C 14,4 36,4 41,-7 Z" fill="#e79a4a"/>'
        '<path d="M -39,-5 C -32,0 -18,0 -11,-4 M 39,-5 C 32,0 18,0 11,-4" stroke="#5a3420" stroke-width="2" fill="none" stroke-linecap="round"/></g>')
for gid in ('eyesSleepy', 'eyesAlert'):
    a = head.index(f'<g id="{gid}">'); b = head.index('\n  </g>', a)
    head = head[:b] + lidC + head[b:]

# ---- James without headphones, and a version glancing toward the door ----
def strip_hp(g):
    a = g.index('    <!-- headphones -->'); b = g.rindex('</g>')
    return g[:a] + g[b:]


jh = group_by_id(head, 'jhead'); jhs = group_by_id(head, 'jheadScared')
hp = jh[jh.index('    <!-- headphones -->'):jh.rindex('</g>')]
jhNH = strip_hp(jh).replace('id="jhead"', 'id="jheadNH"', 1)
jhsNH = strip_hp(jhs).replace('id="jheadScared"', 'id="jheadSNH"', 1)
jhsNHL = (jhsNH.replace('id="jheadSNH"', 'id="jheadSNHL"', 1)
          .replace('<circle cx="-13" cy="-1.6" r="4"', '<circle cx="-17" cy="-1.6" r="4"')
          .replace('<circle cx="13" cy="-1.6" r="4"', '<circle cx="9" cy="-1.6" r="4"')
          .replace('<circle cx="-14.4" cy="-2.9" r="1.1"', '<circle cx="-18.4" cy="-2.9" r="1.1"')
          .replace('<circle cx="11.6" cy="-2.9" r="1.1"', '<circle cx="7.6" cy="-2.9" r="1.1"'))
assert jhsNHL.count('cx="-17"') == 1, 'look variant'
jb = group_by_id(head, 'jbody'); jbS = group_by_id(head, 'jbodyS')
jbNH = jb.replace('id="jbody"', 'id="jbodyNH"', 1).replace('<use href="#jhead"/>', '<use href="#jheadNH"/>')
jbSNH = jbS.replace('id="jbodyS"', 'id="jbodySNH"', 1).replace('<use href="#jheadScared"/>', '<use href="#jheadSNH"/>')
jbSNHL = jbS.replace('id="jbodyS"', 'id="jbodySNHL"', 1).replace('<use href="#jheadScared"/>', '<use href="#jheadSNHL"/>')

# ---- Dean lying down, head that can lift (pose 3 of the cat sheet) ----
C = open(os.path.join(SB, '..', 'oddhours', 'cat.html')).read()
lie = A8['G']['inner_group'](C, '<g transform="translate(-30,40)">')
lie = rep(lie, '<g transform="translate(66,-30) scale(0.95)"><use href="#headBase"/><use href="#eyesSleepy"/></g>',
          '<g class="cathead" transform="translate(66,-30) scale(0.95)"><use href="#headBase"/><g class="eS"><use href="#eyesSleepy"/></g><g class="eA" display="none"><use href="#eyesAlert"/></g></g>')

logo64 = base64.b64encode(open('logo.png', 'rb').read()).decode()
eyemark = ('<g id="eyemark"><ellipse cx="0" cy="0" rx="20" ry="15" fill="#7a1fff"/>'
           '<path d="M -15,0 C -8,-8.5 8,-8.5 15,0 C 8,8.5 -8,8.5 -15,0 Z" fill="#05040a"/><circle cx="0" cy="0" r="4.2" fill="#d6b0ff"/></g>')
def drop(g, starts):
    for st in starts:
        g = re.sub(r'<path d="' + re.escape(st) + r'[^>]*/>', '', g)
    return g


LEFT_J = ['M -55,114', 'M -55,234', 'M -42,238']
LEFT_T = ['M -38,60', 'M -46,92', 'M -51,210']
RIGHT_T = ['M 38,60', 'M 46,92', 'M 51,210']
jbNHnoL = drop(jbNH, LEFT_J).replace('id="jbodyNH"', 'id="jbodyNHnoL"', 1)
tb = group_by_id(head, 'tbody'); tbS = group_by_id(head, 'tbodyS')
tbNoR = drop(tb, RIGHT_T).replace('id="tbody"', 'id="tbodyNoR"', 1)
tbSNoArms = drop(tbS, RIGHT_T + LEFT_T).replace('id="tbodyS"', 'id="tbodySNoArms"', 1)
tbSNoArms = re.sub(r'<ellipse cx="-4[57](\.5)?" cy="20[45]"[^>]*/>', '', tbSNoArms)
th = group_by_id(head, 'thead')
def iris_shift(g, dx, dy):
    for (x, y, r) in [(-13, -0.5, 4.9), (-13, -0.5, 2.3), (13, -0.5, 4.9), (13, -0.5, 2.3), (-14.8, -2.3, 1.5), (-11.4, 1.4, .7), (11.2, -2.3, 1.5), (14.6, 1.4, .7)]:
        rs = ('.7' if r == .7 else str(r))
        g = g.replace(f'<circle cx="{x:g}" cy="{y:g}" r="{rs}"', f'<circle cx="{x+dx:g}" cy="{y+dy:g}" r="{rs}"')
    return g
SMILE = '<path d="M -6.5,22 Q 0,25.6 6.5,21.6" fill="none" stroke="#a24a46" stroke-width="2" stroke-linecap="round"/>'
LIP = '<path d="M -3.5,25.4 Q 0,27.4 3.5,25.2" fill="none" stroke="#e79a8a" stroke-width="1.6" stroke-linecap="round"/>'
assert SMILE in th and LIP in th, 'tawan smile'
FLAT = '<path d="M -5.5,23.2 Q 0,23.8 5.5,23.2" fill="none" stroke="#a24a46" stroke-width="2" stroke-linecap="round"/>'
thDown = iris_shift(th, 0, 2.0).replace('id="thead"', 'id="theadDown"', 1)
thDownS = thDown.replace('id="theadDown"', 'id="theadDownS"', 1).replace(SMILE, FLAT).replace(LIP, '')
thLookS = iris_shift(th, -3.2, 0).replace('id="thead"', 'id="theadLookS"', 1).replace(SMILE, FLAT).replace(LIP, '')
assert thDown.count('cy="1.5" r="4.9"') == 2 and thLookS.count('cx="-16.2"') == 2, 'iris variants'
tbV = ''.join(tbNoR.replace('id="tbodyNoR"', f'id="tb_{v}"', 1).replace('<use href="#thead"/>', f'<use href="#{v}"/>') for v in ('theadDown', 'theadDownS', 'theadLookS'))
assert jbNHnoL.count('M -55,114') == 0 and tbNoR.count('M 38,60') == 0 and tbSNoArms.count('M -38,60') == 0
extra = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + thDown + thDownS + thLookS + tbV + jbNHnoL + tbNoR + tbSNoArms + jhNH + jhsNH + jhsNHL + jbNH + jbSNH + jbSNHL +
         '<filter id="vivid" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="1.3"/><feComponentTransfer><feFuncR type="linear" slope="0.97" intercept="0.0"/><feFuncG type="linear" slope="0.94"/><feFuncB type="linear" slope="0.98" intercept="0.01"/></feComponentTransfer></filter>' + '<filter id="grainF" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="2.2" numOctaves="1" seed="11"/><feColorMatrix type="saturate" values="0"/></filter>' + '<filter id="tintDim" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.86 0 0 0 0.02  0 0.82 0 0 0.02  0 0 0.86 0 0.04  0 0 0 1 0"/></filter>' + f'<g id="hp">{hp}</g><g id="deanLie">{lie}</g>{eyemark}</defs></svg>')

# ---------------- shots ----------------
SV = {}
arm_hp = ('<path d="M -57,64 C -66,60 -76,52 -80,40 L -66,34 L -50,58 Z" fill="#2b3768"/>'
          '<path d="M -80,42 L -66,34 L -40,-2 L -50,-8 Z" fill="#fbe7d8"/><ellipse cx="-44" cy="-4" rx="9" ry="10" fill="#fbe7d8"/>')
SV['hook'] = S['s1'].replace(VIG + TEX, '')
s2 = S['s2'].replace(VIG + TEX, '')
s2 = rep(s2, '<g filter="url(#tintWarm)"><use href="#jbody" transform="translate(262,320) scale(1.7)"/></g>',
         '<g filter="url(#tintWarm)"><g transform="translate(262,320) scale(1.7)"><use href="#jbodyNHnoL"/>'
         f'<g class="hpgrp"><use href="#hp"/>{arm_hp}</g></g></g>')
s2 = rep(s2, '<circle cx="430" cy="820" r="90" fill="#9fb0ff" opacity=".18"', '<circle class="phoneglow" cx="430" cy="820" r="90" fill="#9fb0ff" opacity=".18"')
# --- monitor seen from behind: casing, back panel, vents, stand, cable, light spilling round the edges ---
MON = ('<defs><linearGradient id="monCase" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3646"/><stop offset="1" stop-color="#1b1922"/></linearGradient>'
       '<radialGradient id="faceLight2" gradientUnits="userSpaceOnUse" cx="250" cy="420" r="220"><stop offset="0" stop-color="#f2b8d6" stop-opacity=".30"/>'
       '<stop offset=".55" stop-color="#b79cff" stop-opacity=".12"/><stop offset="1" stop-color="#b79cff" stop-opacity="0"/></radialGradient>'
       '<linearGradient id="monBeam2" gradientUnits="userSpaceOnUse" x1="200" y1="480" x2="250" y2="260"><stop offset="0" stop-color="#f6c6a0" stop-opacity=".22"/><stop offset="1" stop-color="#c7a8ff" stop-opacity="0"/></linearGradient>'
       '<filter id="tintLilac" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1.0 0 0 0 0.03  0 0.88 0 0 0.0  0 0 0.98 0 0.05  0 0 0 1 0"/></filter></defs>'
       '<path d="M10,478 L340,470 L346,486 L16,494 Z" fill="#f4c49c" opacity=".55" filter="url(#bokeh)"/>'                 # warm light leaking over the top edge
       '<path d="M8,486 L8,486" />'
       '<rect x="14" y="484" width="330" height="200" rx="14" fill="url(#monCase)"/>'
       '<rect x="14" y="484" width="330" height="200" rx="14" fill="none" stroke="#c9a6e8" stroke-opacity=".55" stroke-width="2.5"/>'
       '<rect x="104" y="530" width="150" height="112" rx="16" fill="#2a2734"/><rect x="104" y="530" width="150" height="112" rx="16" fill="none" stroke="#3e3a4c" stroke-width="2"/>'
       + ''.join(f'<rect x="{122+k*12}" y="548" width="5" height="22" rx="2" fill="#1d1b25"/>' for k in range(10)) +
       '<circle cx="179" cy="604" r="9" fill="#3a3648"/><circle cx="179" cy="604" r="4" fill="#8d7ac0" opacity=".8"/>'
       '<rect x="166" y="642" width="26" height="50" fill="#24222c"/><rect x="166" y="642" width="6" height="50" fill="#33303d"/>'
       '<path d="M186,660 C200,680 220,684 236,692" stroke="#15141b" stroke-width="5" fill="none"/>'
       '<ellipse cx="179" cy="694" rx="60" ry="7" fill="#15131b"/>')
s2 = s2.replace('<path d="M-10,500 L340,466 L368,700 L-10,700 Z" fill="url(#monBack)"/>', MON)
s2 = s2.replace('<path d="M120,600 l16,-14 l16,14 l-16,14 Z" fill="#d9c6d6" opacity=".7"/>', '')
s2 = s2.replace('<path d="M340,466 L368,700 L360,700 L334,468 Z" fill="#f6d2c4"/>', '')
s2 = s2.replace('url(#faceLight)', 'url(#faceLight2)').replace('url(#monBeam)', 'url(#monBeam2)')
s2 = s2.replace('<g filter="url(#tintWarm)"><g transform="translate(262,320) scale(1.7)">', '<g filter="url(#tintLilac)"><g transform="translate(262,320) scale(1.7)">')
s2 = s2.replace('<rect x="0" y="696" width="340" height="10" fill="#f0c0b0" opacity=".5" filter="url(#bokeh)"/>', '<rect x="14" y="690" width="330" height="8" fill="#e8b8e0" opacity=".35" filter="url(#bokeh)"/>')
SV['headphones'] = s2

# phone history list in Tawan's hands
s5 = A['s5'].replace(VIG + TEX, '')
a = s5.index('<g font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"><text x="270" y="180"')
b = s5.index('</g>', a) + 4
rows = ''
AM = {1: '10', 2: '48', 3: '41', 4: '65', 5: '19', 6: '72', 7: '33', 8: '07', 9: '64', 10: '96'}
for i, night in enumerate(range(10, 0, -1)):
    y = 170 + i * 48
    st = AM[night]
    rows += (f'<g><rect x="182" y="{y}" width="176" height="42" rx="9" fill="#eef0f8" fill-opacity=".1"/>'
             f'<text x="194" y="{y+17}" font-size="10" fill="#9aa3c8">คืนที่ {night} · 04:00</text>'
             f'<text x="194" y="{y+34}" font-size="14" font-weight="500" fill="#e8ecff">เงินเข้า +333.{st[0]}<tspan fill="#ffd84a" font-weight="600">{st[1]}</tspan> บาท</text></g>')
hl = ('<g class="hl" opacity="0"><rect x="180" y="{y}" width="180" height="94" rx="11" fill="none" stroke="#c9a8ff" stroke-width="2.4"/>'
      '<circle cx="{cx}" cy="{c1}" r="11" fill="none" stroke="#ffd84a" stroke-width="2"/><circle cx="{cx}" cy="{c2}" r="11" fill="none" stroke="#ffd84a" stroke-width="2"/></g>')
screen = (f'<defs><clipPath id="scrClip"><rect x="176" y="150" width="188" height="368" rx="8"/></clipPath></defs>'
          f'<g {FONT}><text x="270" y="140" text-anchor="middle" font-size="12" fill="#c9d0f0">รายการย้อนหลัง</text>'
          f'<g clip-path="url(#scrClip)"><g class="scrollList">{rows}' +
          hl.format(y=170 + 8 * 48 - 3, cx=303, c1=170 + 8 * 48 + 29, c2=170 + 9 * 48 + 29) + '</g></g></g>')
s5 = s5[:a] + screen + s5[b:]
s5 = rep(s5, '<g class="press">', '<g class="press">') if '<g class="press">' in s5 else s5
s5 = rep(s5, A['thumb'], f'<g class="swipe">{A["thumb"]}</g>')
SV['scroll'] = s5
dp = A['s5'].replace(VIG + TEX, '')
a = dp.index('<g font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"><text x="270" y="180"'); b = dp.index('</g>', a) + 4
KEYS = [('1', 210, 250), ('2', 270, 250), ('3', 330, 250), ('4', 210, 306), ('5', 270, 306), ('6', 330, 306),
        ('7', 210, 362), ('8', 270, 362), ('9', 330, 362), ('*', 210, 418), ('0', 270, 418), ('#', 330, 418)]
pad = ''.join(f'<g class="key" data-d="{d}"><circle cx="{x}" cy="{y}" r="23" fill="#2c3264"/><circle class="flash" cx="{x}" cy="{y}" r="23" fill="#c9a8ff" opacity="0"/>'
              f'<text x="{x}" y="{y+8}" text-anchor="middle" font-size="22" font-weight="500" fill="#eef0ff">{d}</text></g>' for d, x, y in KEYS)
dial_screen = (f'<g {FONT}><text x="270" y="150" text-anchor="middle" font-size="11" fill="#9aa3c8">โทรศัพท์</text>'
               '<text class="num" x="270" y="200" text-anchor="middle" font-size="27" font-weight="500" fill="#ffffff" letter-spacing="1"></text>'
               '<rect class="caret" x="356" y="180" width="2" height="26" fill="#c9a8ff"/>' + pad +
               '<circle class="callbtn" cx="270" cy="482" r="23" fill="#3cb46e"/><path d="M262,478 q2,-6 6,-4 l2,3 q-3,3 -1,6 q3,4 7,5 q2,-2 5,0 l2,3 q-2,5 -6,4 q-12,-3 -15,-17 Z" fill="#ffffff"/></g>')
dp = dp[:a] + dial_screen + dp[b:]
dp = rep(dp, A['thumb'], f'<g class="tap">{A["thumb"]}</g>')
SV['dialpad'] = dp + dust(311, (330, 10, 540, 260), 12)

# two-shot in the bedroom: James reads, Tawan writes
pad_t = ('<g class="writeArm"><rect x="-26" y="112" width="52" height="40" rx="3" fill="#f4ead8"/><path d="M -18,124 L 14,124 M -18,134 L 6,134" stroke="#9b8670" stroke-width="2"/>'
         '<path d="M 50,94 L 39,100 L 17,144 L 29,150 Z" fill="#e8b08a"/><path d="M 18,150 L 30,120" stroke="#2a2a33" stroke-width="3" stroke-linecap="round"/><ellipse cx="22" cy="146" rx="7" ry="6" fill="#f8d2ab"/></g>')
armJphone = G['arm'] + '<rect x="-36" y="54" width="18" height="34" rx="3" fill="#0c0d14"/><rect x="-34" y="57" width="14" height="27" rx="2" fill="#5a6ab0"/>'
lampglow = '<circle cx="480" cy="230" r="170" fill="#f2c8e4" opacity=".08" filter="url(#haze)" style="mix-blend-mode:screen"/>'
fore = ('<g filter="url(#dof)"><path d="M-20,760 C120,720 300,780 560,730 L560,960 L-20,960 Z" fill="#21152a"/>'
        '<path d="M-20,760 C120,720 300,780 560,730 L560,770 C300,800 120,760 -20,800 Z" fill="#3a2634"/></g>')
SV['read'] = (room_top + bg + '<g filter="url(#vivid)"><g transform="translate(160,330) scale(1.5)"><use href="#jbodyNHnoL"/>' + armJphone + '</g>'
              '<g transform="translate(400,345) scale(1.5)"><use href="#tbodyNoR"/>' + pad_t + '</g></g>' + fore + lampglow + dust(201, (330, 120, 530, 420), 14))

# paper close-up: the ten digits get written
digits = '0815923746'
dg = ''
for k, d in enumerate(digits):
    x = 150 + k * 26 + (12 if k >= 3 else 0) + (12 if k >= 6 else 0)
    dg += f'<text class="dg" x="{x}" y="470" font-family="Caveat, Comic Sans MS, cursive" font-size="44" font-weight="700" fill="#2b2a4a" opacity="0">{d}</text>'
hand_w = ('<g class="penhand"><path d="M 0,0 L 60,-70" stroke="#2a2a33" stroke-width="7" stroke-linecap="round"/><path d="M 0,0 L 8,-10" stroke="#c9c2b4" stroke-width="7" stroke-linecap="round"/>'
          '<path d="M 40,-40 C 70,-60 130,-40 150,10 C 170,60 150,140 120,200 L 40,200 C 50,120 30,60 20,30 Z" fill="#e2b29c"/>'
          '<path d="M 40,-40 C 70,-60 130,-40 150,10 C 120,-20 80,-30 50,-20 Z" fill="#f0c4ae"/></g>')
SV['write'] = (f'<rect width="540" height="960" fill="url(#duvet)"/><g filter="url(#dof2)"><rect x="300" y="-20" width="260" height="200" rx="40" fill="#d6cce2"/></g>'
               '<circle cx="500" cy="60" r="220" fill="#ffe6da" opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/>'
               '<g transform="translate(270,470) rotate(-4)"><g transform="translate(14,18)" filter="url(#sh)" opacity=".45"><rect x="-180" y="-150" width="360" height="300" fill="#2a0e1c"/></g>'
               '<rect x="-180" y="-150" width="360" height="300" rx="6" fill="#f4ead8"/><rect x="-180" y="-150" width="360" height="30" rx="6" fill="#e5735f"/>'
               f'<text x="-164" y="-129" {FONT} font-size="14" fill="#fff">เลขหลักสุดท้าย · คืนที่ 1–10</text>'
               '<path d="M -164,64 L 164,64 M -164,100 L 164,100" stroke="#d9c9b4" stroke-width="2"/></g>'
               f'<g transform="translate(0,0)">{dg}</g>{hand_w}' + dust(211, (330, 10, 540, 300), 16))

SV['realize'] = (room_top + bg + '<g filter="url(#vivid)"><g transform="translate(270,300) scale(2.0)"><use href="#tbodySNoArms"/><path d="M -50,96 L -38,100 L -47,134 L -61,131 Z" fill="#f8d2ab"/><path d="M 50,96 L 38,100 L 47,130 L 61,127 Z" fill="#e8b08a"/></g></g>'
                 '<g transform="translate(270,560) rotate(-6)"><rect x="-120" y="-40" width="240" height="120" rx="5" fill="#f4ead8"/>'
                 '<text x="-100" y="10" font-family="Caveat, cursive" font-size="34" font-weight="700" fill="#2b2a4a">081 592 37..</text></g>'
                 '<g filter="url(#vivid)"><ellipse cx="160" cy="570" rx="22" ry="26" fill="#f8d2ab"/><ellipse cx="380" cy="560" rx="22" ry="26" fill="#e8b08a"/></g>'
                 + lampglow + dust(221, (330, 120, 530, 420), 14))

armT = A['armT']
duo = lambda jb_id: (room_top + bg + f'<g filter="url(#vivid)"><g transform="translate(160,350) scale(1.9)"><use href="#{jb_id}"/></g>'
                     f'<g transform="translate(400,365) scale(1.9)"><use href="#tbodyNoR"/><g class="hangarm">{armT}</g></g></g>' + fore + lampglow + dust(231, (330, 120, 530, 420), 12))
SV['dial'] = duo('jbodySNH')
armTphone = ('<path d="M 50,64 C 58,72 62,92 62,110 L 46,114 L 40,74 Z" fill="#f3e6cf"/>'
             '<path d="M 60,106 L 47,113 L 20,100 L 28,86 Z" fill="#e8b08a"/><ellipse cx="22" cy="93" rx="9" ry="8" fill="#e8b08a"/>'
             '<g transform="rotate(-12 14 88)"><rect x="4" y="70" width="18" height="32" rx="3" fill="#0c0d14"/><circle cx="9" cy="75" r="1.6" fill="#3a3a48"/></g>')
SV['tawanlook'] = (room_top + bg + '<g filter="url(#vivid)"><g transform="translate(270,300) scale(2.1)">'
                   '<g class="fA"><use href="#tb_theadDown"/></g><g class="fB" display="none"><use href="#tb_theadDownS"/></g><g class="fC" display="none"><use href="#tb_theadLookS"/></g>'
                   + armTphone + '</g></g>' + lampglow + dust(301, (330, 120, 530, 420), 12))
SV['glance'] = duo('jbodySNH').replace('<use href="#jbodySNH"/>', '<g class="lookA"><use href="#jbodySNH"/></g><g class="lookB" display="none"><use href="#jbodySNHL"/></g>')

SV['dean'] = (hall(560, (30, 170, 196, 560)) + '<rect x="30" y="552" width="166" height="8" fill="#08060c"/>'
              '<path d="M540,300 L420,300 L120,960 L540,960 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
              '<use href="#deanLie" transform="translate(330,500) scale(0.7)"/>' + dust(241, (300, 300, 540, 620), 14))

SV['whisper'] = (room_top + bg + '<rect width="540" height="960" fill="#0a0612" opacity=".35"/>'
                 '<g filter="url(#vivid)"><use href="#jbodySNH" transform="translate(250,330) scale(2.3)"/></g>' + dust(251, (40, 160, 300, 480), 12))

DOOR_F = (155, 150, 385, 691)          # front-on: 230 x 541 = 85:200, both jambs + a strip of floor
x0, y0, x1, y1 = DOOR_F
SV['door'] = (hall(y1, DOOR_F) + f'<rect class="underlight" x="{x0}" y="{y1-8}" width="{x1-x0}" height="8" fill="#e2ecff"/>'
              '<rect width="540" height="960" fill="url(#coolPool)" style="mix-blend-mode:screen"/>'
              + '<g class="pulse" fill="none" stroke="#e2ecff" stroke-width="3" stroke-linecap="round" opacity=".8"><path d="M{x1},{y} q14,20 0,40"/><path d="M{x2},{y2} q22,32 0,64"/><path d="M{x3},{y} q-14,20 0,40"/><path d="M{x4},{y2} q-22,32 0,64"/></g>'.format(x1=300, x2=314, x3=240, x4=226, y=400, y2=388) + dust(281, (150, 600, 400, 760), 14, '#eef4ff'))
# ---- hallway in perspective, the same storage door at the far end (85:200) ----
DX0, DY0, DX1, DY1 = 232, 300, 308, 479          # 76 x 179 = 85:200
hallp = ('<rect width="540" height="960" fill="#120e18"/>'
         '<path d="M0,0 L190,250 L350,250 L540,0 Z" fill="#17121e"/>'                      # ceiling
         '<path d="M0,0 L190,250 L190,500 L0,960 Z" fill="#221a2a"/>'                      # left wall
         '<path d="M540,0 L350,250 L350,500 L540,960 Z" fill="#1d1724"/>'                  # right wall
         '<rect x="190" y="250" width="160" height="250" fill="url(#hallWall)"/>'          # end wall
         '<path d="M0,960 L190,500 L350,500 L540,960 Z" fill="#231a26"/>'                  # floor
         + ''.join(f'<line x1="{190+k*20}" y1="500" x2="{-140+k*82}" y2="960" stroke="#0e0a14" stroke-opacity=".5" stroke-width="1.5"/>' for k in range(9))
         + '<path d="M0,940 L190,496 L190,500 L0,960 Z" fill="#120e18"/><path d="M540,940 L350,496 L350,500 L540,960 Z" fill="#120e18"/>'
         f'<rect x="{DX0-6}" y="{DY0-6}" width="{DX1-DX0+12}" height="{DY1-DY0+6}" fill="#2e2228"/><rect x="{DX0}" y="{DY0}" width="{DX1-DX0}" height="{DY1-DY0}" fill="#3a2c32"/>'
         f'<rect x="{DX0+8}" y="{DY0+10}" width="{DX1-DX0-16}" height="64" fill="none" stroke="#2a1e24" stroke-width="2"/><rect x="{DX0+8}" y="{DY0+94}" width="{DX1-DX0-16}" height="72" fill="none" stroke="#2a1e24" stroke-width="2"/>'
         f'<circle cx="{DX1-9}" cy="{(DY0+DY1)/2+9}" r="3" fill="#9a96a0"/>'
         f'<rect class="underlight" x="{DX0}" y="{DY1-3}" width="{DX1-DX0}" height="3" fill="#e2ecff"/>'
         f'<path d="M{DX0-30},{DY1} L{DX1+30},{DY1} L{DX1+90},{DY1+90} L{DX0-90},{DY1+90} Z" fill="#cfe0ff" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/>'
         '<g class="pulse" fill="none" stroke="#e2ecff" stroke-width="2" stroke-linecap="round" opacity=".8"><path d="M286,368 q8,12 0,24"/><path d="M294,360 q14,20 0,40"/><path d="M254,368 q-8,12 0,24"/><path d="M246,360 q-14,20 0,40"/></g>')
# ---- James from behind (head units), head can face Tawan (A) or the door (B) ----
SKB = '#f2d6c6'
jback_body = ('<rect x="-9" y="22" width="18" height="36" fill="' + SKB + '"/>'
              '<path d="M -55,114 L -41,118 L -40,170 L -42,236 L -54,236 L -57,170 Z" fill="' + SKB + '"/><path d="M 55,114 L 41,118 L 40,170 L 42,236 L 54,236 L 57,170 Z" fill="#e2bba6"/>'
              '<path d="M -55,234 L -41,234 C -40,248 -42,262 -48,264 C -54,264 -57,250 -55,234 Z" fill="' + SKB + '"/><path d="M 55,234 L 41,234 C 40,248 42,262 48,264 C 54,264 57,250 55,234 Z" fill="#e2bba6"/>'
              '<path d="M -41,228 L 41,228 L 44,300 L 37,462 L 9,462 L 2,292 L -2,292 L -9,462 L -37,462 L -44,300 Z" fill="#33406e"/>'
              '<path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L 57,116 L 40,122 L 42,234 L -42,234 L -40,122 L -57,116 L -47,66 C -42,56 -28,51 -12,49 Z" fill="#2b3768"/>'
              '<path d="M 20,50 C 32,53 43,58 47,66 L 57,116 L 40,122 L 42,234 L 26,234 C 28,180 28,100 20,50 Z" fill="#1c2448"/>'
              '<path d="M -14,50 C -6,56 6,56 14,50" fill="none" stroke="#a9b8e8" stroke-width="2.5"/><path d="M 0,58 L 0,232" stroke="#1c2448" stroke-width="1.5"/>'
              '<path d="M -57,116 L -40,122 M 57,116 L 40,122 M -42,232 L 42,232" stroke="#a9b8e8" stroke-width="2"/>')
hairB = ('M -34,-6 C -40,-50 -14,-64 2,-64 C 26,-64 40,-50 34,-6 C 34,14 26,30 12,34 L -12,34 C -26,30 -34,14 -34,-6 Z '
         'M -26,-46 L -30,-66 L -14,-56 L -8,-72 L 2,-58 L 12,-70 L 16,-56 L 30,-64 L 26,-44 Z')
headA = ('<g class="hA"><ellipse cx="-33" cy="4" rx="7" ry="11" fill="' + SKB + '"/>'
         '<path d="M 22,-6 C 34,-6 40,8 36,22 C 32,32 22,36 14,34 Z" fill="' + SKB + '"/>'
         '<g transform="translate(-6 0)"><path d="' + hairB + '" fill="#14111c"/><path d="M -24,-44 C -14,-56 0,-60 12,-58 C 0,-52 -12,-46 -18,-34 Z" fill="#33324a"/></g></g>')
headB = ('<g class="hB" display="none"><ellipse cx="-33" cy="4" rx="7" ry="11" fill="' + SKB + '"/><ellipse cx="33" cy="4" rx="7" ry="11" fill="#e2bba6"/>'
         '<path d="' + hairB + '" fill="#14111c"/><path d="M -24,-44 C -14,-56 0,-60 12,-58 C 0,-52 -12,-46 -18,-34 Z" fill="#33324a"/><path d="M -6,-10 C -2,6 2,18 0,30" stroke="#24222f" stroke-width="2" fill="none"/></g>')
JBACK = f'<g class="jback">{jback_body}{headA}{headB}</g>'
# ---- Tawan from behind, phone at her ear (head units) ----
TBACK = ('<g><path d="M -40,64 C -46,68 -50,86 -50,104 L -51,212 L -40,212 L -38,110 Z" fill="#f8d2ab"/>'
         '<path d="M -42,158 L 42,158 L 46,200 L 50,442 L 8,442 L 3,252 L -3,252 L -8,442 L -50,442 Z" fill="#e6d6bc"/>'
         '<path d="M -14,50 L 14,50 C 26,52 36,56 40,64 L 50,98 L 38,102 L 41,204 L -41,204 L -38,102 L -50,98 L -40,64 C -36,56 -26,52 -14,50 Z" fill="#efe2c8"/>'
         '<path d="M 18,51 C 28,53 37,57 40,64 L 50,98 L 38,102 L 41,204 L 26,204 C 27,140 24,80 18,51 Z" fill="#cdb593"/>'
         '<path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 45,130 L 37,138 L 29,131 L 20,136 L 0,140 L -20,136 L -29,131 L -37,138 L -45,130 Z" fill="#17121a"/>'
         '<path d="M -38,-4 L -45,130 L -40,135 L -34,0 Z" fill="#372a32"/>'
         '<path d="M 50,64 C 58,72 62,92 62,110 L 48,112 L 40,74 Z" fill="#efe2c8"/><path d="M 60,106 L 48,112 L 40,30 L 52,24 Z" fill="#e8b08a"/>'
         '<ellipse cx="46" cy="18" rx="9" ry="10" fill="#e8b08a"/><rect x="38" y="-10" width="12" height="32" rx="3" fill="#0c0d14"/></g>')
SV['ots'] = (hallp + dust(291, (190, 380, 360, 560), 12, '#eef4ff')
             + '<circle cx="455" cy="485" r="80" fill="#9fb4ff" opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/>'
             '<g filter="url(#tintDim)"><g transform="translate(400,500) scale(1.55)">' + TBACK + '</g>'
             '<g class="jstep" transform="translate(185,470) scale(2.0)">' + JBACK + '</g></g>')

SV['behind'] = (hall(620, (330, 140, 490, 620)).replace('fill="#3a2c32"/>', 'fill="#c99a7a"/>', 1) +
                '<path d="M330,620 L490,620 L540,960 L250,960 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
                '<g filter="url(#tintNight)"><g transform="translate(395,330) scale(1.15)"><use href="#tbodyNoR"/>' + armT + '</g></g>'
                '<circle cx="438" cy="330" r="60" fill="#9fb4ff" opacity=".25" filter="url(#haze)" style="mix-blend-mode:screen"/>'
                '<g filter="url(#tintNight)"><use href="#jbodySNH" transform="translate(200,320) scale(1.45)"/></g>' + dust(261, (300, 160, 520, 600), 12))

# end card: hand stops before the knob, question above, logo under it
lw = 280; lh = lw * 260 / 1595; lx = 130; ly = 318
ecx = lx + 145 * lw / 1595; ecy = ly + 151 * lw / 1595
lw = 300; lh = lw * 260 / 1595; lx = 120; ly = 530
ecx = lx + 145 * lw / 1595; ecy = ly + 151 * lw / 1595
KX, KY = 330, 680
SV['endcard'] = ('<rect width="540" height="960" fill="#3a2c32"/>'
                 '<rect x="40" y="40" width="460" height="330" fill="none" stroke="#2a1e24" stroke-width="5"/><rect x="40" y="420" width="460" height="520" fill="none" stroke="#2a1e24" stroke-width="5"/>'
                 '<rect width="540" height="960" fill="#0a0612" opacity=".35"/>'
                 f'<circle cx="{KX}" cy="{KY}" r="150" fill="#cfe0ff" opacity=".10" filter="url(#haze)" style="mix-blend-mode:screen"/>'
                 f'<ellipse cx="{KX}" cy="{KY}" rx="20" ry="46" fill="#2a2024"/><circle cx="{KX}" cy="{KY}" r="22" fill="#9a96a0"/><circle cx="{KX-5}" cy="{KY-5}" r="8" fill="#d9d6e0"/>'
                 '<g class="reach" filter="url(#tintDim)"><g transform="translate(250 690)">'
                 '<path d="M -230,330 L -150,330 L 10,22 L -22,-6 Z" fill="#efc7b0"/>'
                 '<path d="M -230,330 L -196,330 L -14,4 L -22,-6 Z" fill="#fbe7d8"/>'
                 '<ellipse cx="0" cy="0" rx="25" ry="31" transform="rotate(-32)" fill="#f6dccb"/>'
                 '<path d="M 14,-22 q 18,-10 28,2" stroke="#f6dccb" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 20,-10 q 20,-6 30,6" stroke="#f6dccb" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 22,3 q 18,-2 26,9" stroke="#efc7b0" stroke-width="10.5" stroke-linecap="round" fill="none"/>'
                 '<path d="M 18,16 q 14,0 20,9" stroke="#e6b9a2" stroke-width="9.5" stroke-linecap="round" fill="none"/>'
                 '<path d="M -6,20 q 20,8 32,-2" stroke="#efc7b0" stroke-width="11" stroke-linecap="round" fill="none"/>'
                 '<path d="M 6,-16 q 4,14 0,30" stroke="#d29d86" stroke-width="1.6" fill="none" opacity=".7"/></g></g>'
                 + dust(271, (60, 520, 300, 760), 12, '#eef4ff') +
                 f'<g class="q" opacity="0" {FT} text-anchor="middle">'
                 '<text x="270" y="392" font-size="32" font-weight="500" fill="#f2eefa" stroke="#0b0812" stroke-width="6" paint-order="stroke">ถ้าเป็นคุณ…</text>'
                 '<text x="270" y="462" font-size="50" font-weight="700" fill="#ffffff" stroke="#0b0812" stroke-width="8" paint-order="stroke">จะ<tspan fill="#c9a8ff">เปิดประตู</tspan>ไหม?</text></g>'
                 f'<g class="logo" opacity="0"><image href="data:image/png;base64,{logo64}" x="{lx}" y="{ly}" width="{lw}" height="{lh:.1f}"/>'
                 f'<g class="logolid" display="none"><ellipse cx="{ecx:.1f}" cy="{ecy:.1f}" rx="21" ry="10" fill="#7a1fff"/>'
                 f'<path d="M {ecx-18:.1f},{ecy+1:.1f} C {ecx-8:.1f},{ecy+5:.1f} {ecx+8:.1f},{ecy+5:.1f} {ecx+18:.1f},{ecy+1:.1f}" stroke="#05040a" stroke-width="2" fill="none"/></g></g>')


# ---- old-draft ending: ringtone of the lost phone, then the A/B choice ----
sD = A['sD'].replace(VIG + TEX, '')
sD = rep(sD, '<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(230,300) scale(2.3)"/></g>',
         '<g filter="url(#tintDim)"><use href="#jbodySNH" transform="translate(230,300) scale(2.3)"/></g>')
sD = sD.replace('fill="#e2ecff" opacity="', 'class="note" fill="#e2ecff" opacity="')
SV['oldtone'] = sD
s8 = A8['s8'].replace(VIG + TEX, '')
s8 = rep(s8, '<g filter="url(#tintNight)"><path d="M0,520', '<g filter="url(#tintDim)" class="reach"><path d="M0,520')
SV['choice'] = s8
INFO_OLD = {'oldtone': A['NEW']['D'][5], 'choice': '<g class="choicecard">' + A8['INFO'][7] + '</g>'}

# ---------------- subtitles (time windows) ----------------
SUB = {
    'J1': (['ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน', 'คุณจะยังคิดว่าเขาโอนผิดไหมครับ?'], ['If someone sent money to your account', 'at 4 a.m. every night,', 'would you still think it was a mistake?']),
    'J2': (['สามร้อยสามสิบสามบาททุกคืน', 'ผมแจ้งธนาคารไปแล้ว แต่เงินก็ยังเข้า'], ['333 baht every night.', 'I told the bank, but it keeps coming.']),
    'J2b': (['แฟนผมเลื่อนดูยอดย้อนหลัง', 'แล้วก็หยุดนิ่ง'], ['My girlfriend scrolled back through it,', 'then froze.']),
    'T1': (['เจม ลองดูยอดเงินแต่ละคืนสิ…', 'เอาแค่ตัวเลขหลักสุดท้าย อ่านให้ฟังหน่อย', 'เริ่มจากคืนแรกนะ'], ['James, look at each night\'s amount…', 'Just read me the last digit of each,', 'starting from the first night.']),
    'J3a': (['ศูนย์… แปด…'], ['Zero… eight…']),
    'T2a': (['เดี๋ยวนะ…', 'นี่มันเบอร์มือถือ'], ['Wait…', 'this is a phone number.']),
    'J4': (['ลองโทรไปอีกรอบไหม'], ['Should we call it again?']),
    'J6': (['และเสียงเรียกเข้านั้น', 'เป็นเพลงเดียวกับมือถือเครื่องเก่าของผม', 'ที่หายไปตั้งแต่ปีก่อน'], ['And that ringtone was the same song', 'as my old phone, the one I lost last year.']),
    'J5': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน', 'หรือพาแฟนกับแมวออกจากบ้านก่อน', 'คอมเมนต์บอกผมหน่อยครับ'], ['If you were me, would you open the door,', 'or get my girlfriend and the cat out first?', 'Tell me in the comments.']),
}


def subgroup(cls, th, en):
    n = len(th); m = len(en); big = max(wlen(l) for l in th)
    fs = 21 if n <= 3 and big <= 27 else 20
    lh = fs + 8; efs = 13; elh = 17; gap = 7
    total = n * lh + gap + m * elh; top = 712 - total / 2
    t_ = ''.join(f'<text x="270" y="{top + fs + i*lh:.0f}">{l}</text>' for i, l in enumerate(th))
    ey = top + n * lh + gap
    e_ = ''.join(f'<text x="270" y="{ey + efs + i*elh:.0f}">{l}</text>' for i, l in enumerate(en))
    return (f'<g class="sub {cls}" opacity="0" {FT} text-anchor="middle" stroke="#0b0812" stroke-linejoin="round" paint-order="stroke">'
            f'<g font-weight="600" font-size="{fs}" fill="#ffd84a" stroke-width="7">{t_}</g>'
            f'<g font-family="Inter, IBM Plex Sans Thai, sans-serif" font-weight="500" font-size="{efs}" fill="#ffffff" stroke-width="4.5">{e_}</g></g>')


ev = TL['events']
order = [s['key'] for s in TL['shots']]
subs_by_shot = {k: [] for k in order}
for idx, (at, line) in enumerate(ev):
    if line not in SUB:
        continue
    s = max((x for x in TL['shots'] if x['start'] <= at + 1e-6), key=lambda x: x['start'])
    rel = at - s['start']
    nxt = [a for a, l in ev[idx + 1:] if l in SUB]
    end_abs = min(nxt[0] if nxt else 1e9, s['start'] + s['dur'])
    subs_by_shot[s['key']].append((round(rel - 0.05, 2), round(end_abs - s['start'], 2), line))

INFO = {'hook': tag(20, 20, '04:00'), 'write': '', **INFO_OLD}
GRAIN = ('<rect width="540" height="960" filter="url(#stipple)" opacity=".10" style="mix-blend-mode:overlay"/>'
         '<rect width="540" height="960" filter="url(#grainF)" opacity=".085" style="mix-blend-mode:screen"/>')
cards = ''
cfg = []
for i, k in enumerate(order):
    s = SH[k]
    subs = ''.join(subgroup(f's{j}', *SUB[line]) for j, (_, _, line) in enumerate(subs_by_shot[k]))
    wm = '<g class="wm" transform="translate(500,48)" opacity=".85"><use href="#eyemark"/></g>'
    cards += (f'<figure data-i="{i}"><svg viewBox="0 0 540 960" role="img" aria-label="{k}"><defs><filter id="zb{i}" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="0"/></filter></defs>'
              f'<g class="cam" filter="url(#zb{i})">{SV[k]}{dust(700 + i, (20, 80, 520, 900), 9)}{VIG}{GRAIN}</g><g class="info">{INFO.get(k, "")}</g>{subs}{wm}</svg></figure>\n')
    cfg.append(dict(key=k, dur=s['dur'], frames=s['frames'], mJ=s['mJ'], mT=s['mT'], zb=bool(s.get('zb')),
                    zbNext=bool(SH[order[i + 1]].get('zb')) if i + 1 < len(order) else False,
                    shake=s.get('shake'), subs=[[a, b] for a, b, _ in subs_by_shot[k]],
                    **{x: s[x] for x in ('stop', 'pens', 'ring_from', 'hangup', 'hand_stop', 'card_in', 'taps', 'call') if x in s}))

JS = open('v2.js').read().replace('__CFG__', json.dumps(cfg))
css = '<style>body{padding:0!important}header{display:none!important}.wrap{max-width:none!important}.grid{display:block!important}figure{margin:0}figure svg{width:540px!important;height:960px!important;border-radius:0!important;box-shadow:none!important}</style>'
fonts = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Caveat:wght@700&family=Inter:wght@500&display=swap">'
html = head + extra + css + fonts + f'<div class="wrap"><div class="grid">{cards}</div></div>' + JS
SM = '<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>'
LIP = '<path d="M -3.5,27.4 Q 0,28.8 3.5,27.4" fill="none" stroke="#efc7b0" stroke-width="1.4" stroke-linecap="round"/>'
assert SM in html and LIP in html, 'james mouth'
html = html.replace(SM, '<path d="M -6.5,24.6 Q 0,25.6 6.5,24.2" fill="none" stroke="#a87466" stroke-width="1.7" stroke-linecap="round"/>')
html = html.replace(LIP, '<path d="M -2.6,28.8 Q 0,29.6 2.6,28.8" fill="none" stroke="#e6bea8" stroke-width="1.3" stroke-linecap="round"/>')
for o, n in [('#a05a50', '#a87466'), ('#6b3a3a', '#9a6a60'), ('#b0605a', '#c99a8c'),        # James: no red
             ('#a24a46', '#c47f86'), ('#e79a8a', '#ebb3b3'), ('#8a3436', '#a8646e'),         # Tawan: dusty pink
             ('#7a3434', '#9c5f68'), ('#d27a74', '#e0a5aa')]:
    html = html.replace(o, n)
open('v2.html', 'w').write(html)
json.dump([c['frames'] for c in cfg], open('frames.json', 'w'))
print('v2 built', len(cfg), 'shots', sum(c['frames'] for c in cfg), 'frames')
