#!/usr/bin/env python3
"""บ้านตรงข้าม: ตัวละครที่เหลือ (สามีภรรยาบ้านตรงข้าม, พ่อ แม่ เพื่อนสนิท, บุคคลปริศนา)
ลายเส้นเดียวกับ leads.html / cops.html: cut-out ไม่มีเส้นขอบ เงาบล็อก 2-3 ระดับ แสงกลางจากซ้าย
รัน: python3 others.py -> others.html"""

def face_path(w, chin):
    return (f'M -{w},-14 C -{w},-46 {w},-46 {w},-14 L {w-1},6 C {w-3},22 {w*.45:.1f},{chin-3} 0,{chin} '
            f'C -{w*.45:.1f},{chin-3} -{w-3},22 -{w-1},6 Z')

def head(hid, skin, sh, lt, w=30, chin=40, eyes='soft', brows='soft', mouth='smile', back='', front='', extra='',
         blush='#e48a7e', blush_op=.4, neck_w=8, lip='#a8505a', lash=False, glasses=''):
    fp = face_path(w, chin)
    o = [f'<clipPath id="{hid}F"><path d="{fp}"/></clipPath>',
         f'<clipPath id="{hid}L"><path d="M -21,-1.5 C -17.5,-7 -8.5,-7.4 -4.5,-2 C -8.5,1.6 -17.5,1.8 -21,-1.5 Z"/></clipPath>',
         f'<clipPath id="{hid}R"><path d="M 21,-1.5 C 17.5,-7 8.5,-7.4 4.5,-2 C 8.5,1.6 17.5,1.8 21,-1.5 Z"/></clipPath>',
         f'<g id="{hid}">', back,
         f'<rect x="-{neck_w}" y="20" width="{neck_w*2}" height="38" fill="{sh}"/>',
         f'<path d="M -{neck_w},28 L {neck_w},28 L {neck_w},46 Q 0,41 -{neck_w},49 Z" fill="{sh}" opacity=".7"/>',
         f'<ellipse cx="-{w}" cy="-1" rx="4.6" ry="8" fill="{skin}"/><ellipse cx="{w}" cy="-1" rx="4.6" ry="8" fill="{sh}"/>',
         f'<path d="{fp}" fill="{skin}"/>',
         f'<g clip-path="url(#{hid}F)"><path d="M 16,-34 C {w-1},-28 {w+3},-14 {w},6 C {w-2},22 {w*.5:.0f},{chin-3} 0,{chin} C 11,{chin-9} 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{sh}"/>'
         f'<path d="M -{w+2},-12 C -{w+2},-30 -{w-3},-38 -{w-9},-41 C -{w-3},-32 -{w-2},-20 -{w-2},-10 L -{w-3},8 C -{w-4},20 -{w-10},30 -{w-16},35 C -{w-8},31 -{w-2},21 -{w},6 Z" fill="{lt}"/>'
         f'<path d="M 1.4,1 L 5.4,13 L 1,14.6 Z" fill="{sh}"/></g>',
         f'<ellipse cx="-17" cy="11" rx="6" ry="3.2" fill="{blush}" opacity="{blush_op}"/><ellipse cx="17" cy="11" rx="6" ry="3.2" fill="{blush}" opacity="{blush_op}"/>']
    # brows
    B = {'soft': ('M -21,-12 C -16.5,-16 -9.5,-16.4 -5,-13.4', 2.2),
         'flat': ('M -22,-11.6 L -6,-11', 2.8),
         'arch': ('M -22,-11 C -17,-17 -9,-17.6 -4.6,-13.6', 2.6),
         'thin': ('M -21,-12.6 C -16,-15.6 -10,-15.8 -5.4,-13.6', 1.6)}
    bp, bw = B[brows]
    mirror = bp.replace('-', '§').replace(' ', ' ').replace('§', '')
    def mir(d):
        out = []
        for tok in d.replace(',', ' , ').split():
            if tok in ('M', 'C', 'L', 'Q', ','): out.append(tok)
            else: out.append(tok)
        return d
    # mirror x of brow path manually
    import re
    def mirror_x(d):
        parts = re.split(r'([MCLQ])', d); res = []
        for p in parts:
            if p in ('M', 'C', 'L', 'Q'): res.append(p); continue
            nums = re.findall(r'-?\d+\.?\d*', p)
            pairs = [(float(nums[i]), float(nums[i+1])) for i in range(0, len(nums), 2)]
            res.append(' ' + ' '.join(f'{-x:g},{y:g}' for x, y in pairs) + ' ')
        return ''.join(res)
    o.append(f'<path d="{bp}" fill="none" stroke="#221a1e" stroke-width="{bw}" stroke-linecap="round"/>')
    o.append(f'<path d="{mirror_x(bp)}" fill="none" stroke="#221a1e" stroke-width="{bw}" stroke-linecap="round"/>')
    # eyes
    if eyes == 'closedsmile':
        o.append('<path d="M -20,-1 Q -13,-7 -6,-1 M 20,-1 Q 13,-7 6,-1" fill="none" stroke="#1d1416" stroke-width="2.2" stroke-linecap="round"/>')
    else:
        r = {'soft': 4.4, 'polite': 3.6, 'small': 3.2}[eyes]
        o.append(f'<path d="M -21,-1.5 C -17.5,-7 -8.5,-7.4 -4.5,-2 C -8.5,1.6 -17.5,1.8 -21,-1.5 Z" fill="#fbf4ee"/><path d="M 21,-1.5 C 17.5,-7 8.5,-7.4 4.5,-2 C 8.5,1.6 17.5,1.8 21,-1.5 Z" fill="#efe4da"/>')
        for sx in (-1, 1):
            cx = 12.8 * sx
            o.append(f'<g clip-path="url(#{hid}{"L" if sx<0 else "R"})"><circle cx="{cx}" cy="-1.4" r="{r}" fill="#3a2420"/><circle cx="{cx}" cy="-1.4" r="{r*.45:.1f}" fill="#140b0b"/>'
                     f'<circle cx="{cx-1.4}" cy="-2.8" r="1.1" fill="#fff"/><circle cx="{cx+1.6}" cy="0" r=".55" fill="#fff" opacity=".85"/></g>')
        if eyes == 'polite':   # lids lowered a touch: calm, a little too calm
            o.append(f'<path d="M -22,-7 L -4,-7 L -4,-2.6 C -8.5,-4.6 -17.5,-4.4 -22,-2 Z" fill="{skin}"/><path d="M 22,-7 L 4,-7 L 4,-2.6 C 8.5,-4.6 17.5,-4.4 22,-2 Z" fill="{sh}"/>')
            o.append('<path d="M -22,-2 C -17.5,-4.6 -8.5,-4.8 -3.6,-2.4 M 22,-2 C 17.5,-4.6 8.5,-4.8 3.6,-2.4" fill="none" stroke="#1d1416" stroke-width="2"/>')
        else:
            o.append('<path d="M -22,-1.2 C -18,-8.6 -8,-8.8 -3.6,-2.2 L -4.8,-1.4 C -8.6,-6 -17,-6 -20.6,0 Z" fill="#1d1416"/><path d="M 22,-1.2 C 18,-8.6 8,-8.8 3.6,-2.2 L 4.8,-1.4 C 8.6,-6 17,-6 20.6,0 Z" fill="#1d1416"/>')
        if lash:
            o.append('<path d="M -19.6,-4.6 L -22.4,-7.2 M -16.4,-6.2 L -18,-8.8 M 19.6,-4.6 L 22.4,-7.2 M 16.4,-6.2 L 18,-8.8" stroke="#1d1416" stroke-width="1" stroke-linecap="round"/>')
    # mouth
    M = {'smile': f'<path d="M -6.5,22 Q 0,26 6.5,21.6" fill="none" stroke="{lip}" stroke-width="2" stroke-linecap="round"/>',
         'polite': f'<path d="M -8,22.6 Q 0,27 8,22.6" fill="none" stroke="{lip}" stroke-width="1.9" stroke-linecap="round"/><path d="M -8,22.6 L -9.4,21.4 M 8,22.6 L 9.4,21.4" stroke="{sh}" stroke-width="1.1" stroke-linecap="round"/>',
         'grin': f'<path d="M -9,20 Q 0,31 9,20 Q 0,23 -9,20 Z" fill="#6a2c30"/><path d="M -7.4,20.8 Q 0,23.4 7.4,20.8 L 6.8,22.6 Q 0,25 -6.8,22.6 Z" fill="#fbf6f2"/>',
         'gentle': f'<path d="M -6,21.6 Q 0,24.6 6,21.4" fill="none" stroke="{lip}" stroke-width="2.2" stroke-linecap="round"/><path d="M -3,24.6 Q 0,26 3,24.4" fill="none" stroke="{lt}" stroke-width="1.4" stroke-linecap="round"/>'}
    o.append(M[mouth])
    o.append(extra)
    o.append(glasses)
    o.append(front)
    o.append('</g>')
    return ''.join(o)

# ---------------- heads ----------------
SK = ('#f3cfae', '#deb08c', '#fbe2c8')      # light warm
SK2 = ('#e9bf98', '#d4a27c', '#f6d5b4')     # tan
SK3 = ('#f1c9a6', '#dba684', '#fadcc0')

husband = head('hb', *SK, w=29, chin=42, eyes='polite', brows='flat', mouth='polite', lip='#9a5a50', blush_op=.18,
    front='''<path d="M -31,-8 C -35,-40 -22,-60 0,-61 C 24,-62 36,-44 31,-8 L 29,-22 C 26,-32 18,-36 8,-36 L -20,-34 C -26,-30 -29,-22 -29,-14 Z" fill="#17141a"/>
<path d="M -26,-40 C -14,-56 10,-60 28,-46 C 12,-50 -6,-50 -20,-36 Z" fill="#3c3640"/><path d="M -20,-34 L 8,-36 C -4,-40 -14,-42 -22,-38 Z" fill="#2a2630"/>
<path d="M -14,-50 C -4,-56 12,-56 22,-48" fill="none" stroke="#4e4752" stroke-width="1.4"/>''',
    extra='<path d="M -7,30 C -3,32 3,32 7,30" fill="none" stroke="#deb08c" stroke-width="1.2"/>')

wife = head('wf', *SK3, w=29, chin=39, eyes='soft', brows='thin', mouth='gentle', lip='#b8606c', lash=True, blush_op=.45,
    back='<path d="M -37,-6 C -40,-46 -20,-62 0,-62 C 20,-62 40,-46 37,-6 L 42,112 L 30,120 L 20,112 L 18,56 L -18,56 L -20,112 L -30,120 L -42,112 Z" fill="#2a1a1c"/><path d="M -37,-6 L -42,112 L -37,116 L -33,0 Z" fill="#4a3236"/>',
    front='''<path d="M -36,-4 C -38,-44 -20,-60 0,-60 C 20,-60 38,-44 36,-4 L 30,-8 C 28,-24 18,-34 6,-38 C -8,-32 -22,-22 -28,-6 Z" fill="#2a1a1c"/>
<path d="M -30,-40 C -22,-52 -10,-56 0,-57 C -10,-52 -20,-46 -26,-34 Z" fill="#4a3236"/>
<path d="M -36,-8 L -28,-8 C -28,20 -27,50 -27,86 L -32,92 L -38,86 C -38,50 -37,20 -36,-8 Z" fill="#2a1a1c"/>
<path d="M 36,-8 L 28,-8 C 28,20 27,50 27,86 L 32,92 L 38,86 C 38,50 37,20 36,-8 Z" fill="#221416"/>
<path d="M -12,-56 C -6,-64 6,-64 12,-56 C 6,-60 -6,-60 -12,-56 Z" fill="#7d9a88"/><path d="M -14,-58 L 14,-58" stroke="#7d9a88" stroke-width="4" stroke-linecap="round"/>''')

dad = head('dd', *SK2, w=30, chin=40, eyes='small', brows='flat', mouth='smile', lip='#8a5048', blush_op=.25,
    front='''<path d="M -32,-6 C -36,-40 -22,-56 0,-57 C 22,-58 36,-42 32,-6 L 29,-18 C 24,-28 14,-32 0,-32 C -14,-32 -24,-28 -29,-18 Z" fill="#9a96a4"/>
<path d="M -24,-42 C -14,-52 6,-54 20,-46 C 6,-48 -8,-46 -18,-38 Z" fill="#c4c0cc"/>''',
    extra='<path d="M -20,-24 C -12,-26 -4,-26 0,-25 M -18,30 C -12,33 -6,34 0,34" fill="none" stroke="#d4a27c" stroke-width="1"/><path d="M -20,4 C -16,6 -11,6 -7,4.6 M 20,4 C 16,6 11,6 7,4.6" fill="none" stroke="#c4946e" stroke-width=".9"/>',
    glasses='<g fill="#fff" fill-opacity=".06" stroke="#6a6270" stroke-width="1.4"><rect x="-23" y="-8" width="18" height="12" rx="3"/><rect x="5" y="-8" width="18" height="12" rx="3"/></g><path d="M -5,-3 L 5,-3 M -23,-4 L -30,-5 M 23,-4 L 30,-5" stroke="#6a6270" stroke-width="1.4"/>')

mom = head('mm', *SK3, w=29, chin=39, eyes='closedsmile', brows='thin', mouth='gentle', lip='#b0606a', blush_op=.5,
    front='''<g fill="#3a2a2c"><circle cx="-26" cy="-26" r="12"/><circle cx="-12" cy="-40" r="13"/><circle cx="6" cy="-44" r="13"/><circle cx="22" cy="-34" r="12"/><circle cx="31" cy="-16" r="9"/><circle cx="-32" cy="-10" r="8"/></g>
<g fill="#5a4448"><circle cx="-14" cy="-44" r="5"/><circle cx="4" cy="-48" r="5"/><circle cx="-28" cy="-30" r="4"/></g>
<circle cx="-30" cy="10" r="2.6" fill="#e8d8c0"/><circle cx="30" cy="10" r="2.6" fill="#d8c8b0"/>''')

friend = head('fr', *SK2, w=30, chin=40, eyes='soft', brows='arch', mouth='grin', blush_op=.3,
    front='''<path d="M -33,-14 C -36,-50 36,-50 33,-14 L 30,-20 C 20,-26 -20,-26 -30,-20 Z" fill="#6f8f8a"/>
<path d="M -34,-16 C -30,-12 30,-12 34,-16 L 34,-10 C 30,-6 -30,-6 -34,-10 Z" fill="#587874"/>
<path d="M -18,-46 L 18,-46" stroke="#86a6a0" stroke-width="3"/><circle cx="0" cy="-50" r="5" fill="#86a6a0"/>
<path d="M -30,-8 C -34,-2 -33,6 -31,10 L -28,-6 Z M 30,-8 C 34,-2 33,6 31,10 L 28,-6 Z" fill="#1c1618"/>''')

DEFS = husband + wife + dad + mom + friend

# ---------------- bodies ----------------
def shoes(y, col='#1e1b24', col2='#15131a'):
    return (f'<path d="M -40,{y} L -8,{y} C -6,{y+9} -8,{y+15} -12,{y+16} L -42,{y+16} C -46,{y+14} -45,{y+4} -40,{y} Z" fill="{col}"/>'
            f'<path d="M 40,{y} L 8,{y} C 6,{y+9} 8,{y+15} 12,{y+16} L 42,{y+16} C 46,{y+14} 45,{y+4} 40,{y} Z" fill="{col2}"/>')

def trousers(y0, y1, c, lt, dk, w=40):
    return (f'<path d="M -{w},{y0} L {w},{y0} L {w+2},{y0+70} L {w-6},{y1} L 8,{y1} L 2,{y0+62} L -2,{y0+62} L -8,{y1} L -{w-6},{y1} L -{w+2},{y0+70} Z" fill="{c}"/>'
            f'<path d="M -{w},{y0} L -{w-14},{y0} L -{w-12},{y0+70} L -{w-14},{y1} L -{w-6},{y1} L -{w+2},{y0+70} Z" fill="{lt}"/>'
            f'<path d="M {w-16},{y0+6} L {w},{y0} L {w+2},{y0+70} L {w-6},{y1} L {w-16},{y1} C {w-14},{(y0+y1)/2} {w-14},{y0+70} {w-16},{y0+6} Z" fill="{dk}"/>')

def shirt(c, lt, dk, hem=236, w=46, sleeves='long', skin=('#f3cfae', '#deb08c')):
    o = []
    if sleeves == 'upper':   # long sleeves that bend at the elbow: caller draws the forearms
        o.append(f'<path d="M -{w+8},70 L -{w-6},76 L -{w-6},156 L -{w+10},152 Z" fill="{lt}"/><path d="M {w+8},70 L {w-6},76 L {w-6},156 L {w+10},152 Z" fill="{dk}"/>')
    elif sleeves == 'long':
        o.append(f'<path d="M -{w+8},70 L -{w-6},76 L -{w-4},228 L -{w+10},228 L -{w+12},150 Z" fill="{lt}"/><path d="M {w+8},70 L {w-6},76 L {w-4},228 L {w+10},228 L {w+12},150 Z" fill="{dk}"/>')
        o.append(f'<path d="M -{w+10},226 L -{w-4},226 C -{w-3},240 -{w-5},252 -{w+3},254 C -{w+9},254 -{w+12},242 -{w+10},226 Z" fill="{skin[0]}"/><path d="M {w+10},226 L {w-4},226 C {w-3},240 {w-5},252 {w+3},254 C {w+9},254 {w+12},242 {w+10},226 Z" fill="{skin[1]}"/>')
    else:
        o.append(f'<path d="M -{w+8},112 L -{w-6},116 L -{w-4},228 L -{w+10},228 L -{w+12},150 Z" fill="{skin[0]}"/><path d="M {w+8},112 L {w-6},116 L {w-4},228 L {w+10},228 L {w+12},150 Z" fill="{skin[1]}"/>')
        o.append(f'<path d="M -{w+10},226 L -{w-4},226 C -{w-3},240 -{w-5},252 -{w+3},254 C -{w+9},254 -{w+12},242 -{w+10},226 Z" fill="{skin[0]}"/><path d="M {w+10},226 L {w-4},226 C {w-3},240 {w-5},252 {w+3},254 C {w+9},254 {w+12},242 {w+10},226 Z" fill="{skin[1]}"/>')
    o.append(f'<path d="M -12,48 L 12,48 C 28,50 {w-4},55 {w+2},66 L {w+10},{116 if sleeves!="long" else 80} L {w-6},{122 if sleeves!="long" else 86} L {w-4},{hem} L -{w-4},{hem} L -{w-6},{122 if sleeves!="long" else 86} L -{w+10},{116 if sleeves!="long" else 80} L -{w+2},66 C -{w-4},55 -28,50 -12,48 Z" fill="{c}"/>')
    o.append(f'<path d="M -{w+2},66 C -{w-4},55 -28,50 -18,49 C -26,74 -28,120 -26,{hem} L -{w-4},{hem} L -{w-6},100 Z" fill="{lt}"/>')
    o.append(f'<path d="M 20,49 C 32,52 {w-2},57 {w+2},66 L {w-6},100 L {w-4},{hem} L 26,{hem} C 28,180 28,100 20,49 Z" fill="{dk}"/>')
    return ''.join(o)

def figure(body, ty, sc):
    return f'<g transform="translate(200,{ty}) scale({sc})">{body}</g>'

def panel(content, label, h=900):
    return (f'<svg viewBox="0 0 400 {h}" role="img" aria-label="{label}"><rect width="400" height="{h}" fill="url(#skyBg)"/>'
            f'<rect y="{h-130}" width="400" height="130" fill="#ede5ea"/><ellipse cx="200" cy="{h-144}" rx="80" ry="9" fill="#cfc2d2"/>{content}</svg>')

def closeup(use, collar):
    return (f'<svg viewBox="-75 -80 150 150" role="img" aria-label="ใบหน้าระยะใกล้"><rect x="-75" y="-80" width="150" height="150" fill="url(#skyBg)"/>{collar}<use href="#{use}"/></svg>')

# husband: dark grey long-sleeve shirt, charcoal slacks, loafers, hands clasped in front
hb_body = (shoes(466, '#2a2024', '#1f171a') + trousers(232, 468, '#34343e', '#44444f', '#26262e') +
           shirt('#4a4a56', '#5c5c6a', '#383842', hem=238, w=44, sleeves='upper') +
           '<rect x="-46" y="230" width="92" height="9" fill="#1f1d24"/><rect x="-6" y="229" width="12" height="11" rx="1.5" fill="#b9bec9"/>' +
           '<path d="M -2,58 L 2,58 L 2,232 L -2,232 Z" fill="#3c3c46"/><g fill="#8a8a96"><circle cx="0" cy="100" r="1.5"/><circle cx="0" cy="140" r="1.5"/><circle cx="0" cy="180" r="1.5"/></g>' +
           # forearms crossing to clasp in front of the belt
           '<path d="M -54,150 L -38,154 L -6,218 L -18,226 Z" fill="#5c5c6a"/><path d="M 54,150 L 38,154 L 6,218 L 18,226 Z" fill="#383842"/>' +
           '<ellipse cx="-4" cy="222" rx="11" ry="8" fill="#f3cfae"/><ellipse cx="6" cy="224" rx="10" ry="7.6" fill="#deb08c"/>' +
           '<use href="#hb"/><path d="M -12,48 L -2,64 L -18,60 Z" fill="#5c5c6a"/><path d="M 12,48 L 2,64 L 18,60 Z" fill="#383842"/>')
# the long sleeves end at the elbow bend here, so blank out the default straight forearms/hands
hb_body = hb_body.replace(shirt('#4a4a56', '#5c5c6a', '#383842', hem=238, w=44),
                          shirt('#4a4a56', '#5c5c6a', '#383842', hem=238, w=44).split('<path d="M -12,48')[0].split('<path d="M -54,226')[0] if False else shirt('#4a4a56', '#5c5c6a', '#383842', hem=238, w=44))

# wife: muted green midi dress, watering can, flats
wf_body = ('<use href="#wfback"/>' if False else '') + (
    '<path d="M -34,470 L -10,470 C -8,478 -10,483 -14,484 L -36,484 C -40,482 -39,474 -34,470 Z" fill="#c9b8a8"/><path d="M 34,470 L 10,470 C 8,478 10,483 14,484 L 36,484 C 40,482 39,474 34,470 Z" fill="#b8a898"/>'
    '<rect x="-26" y="390" width="14" height="82" fill="#f1c9a6"/><rect x="12" y="390" width="14" height="82" fill="#dba684"/>'
    # arms
    '<path d="M -50,66 L -38,72 L -44,226 L -56,226 Z" fill="#f1c9a6"/><path d="M -56,224 L -44,224 C -43,238 -45,248 -50,250 C -55,250 -58,238 -56,224 Z" fill="#f1c9a6"/>'
    '<path d="M 50,66 L 38,72 L 46,150 L 58,146 Z" fill="#dba684"/><path d="M 58,146 L 46,150 L 70,212 L 80,204 Z" fill="#dba684"/>'
    # dress
    '<path d="M -14,48 L 14,48 C 30,50 42,56 46,66 L 40,110 L 34,150 C 50,220 62,320 66,396 L -66,396 C -62,320 -50,220 -34,150 L -40,110 L -46,66 C -42,56 -30,50 -14,48 Z" fill="#7d9a88"/>'
    '<path d="M -46,66 C -42,56 -30,50 -20,49 C -24,90 -26,130 -22,152 C -36,230 -42,320 -44,396 L -66,396 C -62,320 -50,220 -34,150 L -40,110 Z" fill="#94b09e"/>'
    '<path d="M 20,49 C 32,52 42,57 46,66 L 40,110 L 34,150 C 50,220 62,320 66,396 L 44,396 C 42,300 36,220 24,154 C 28,120 26,80 20,49 Z" fill="#647e6e"/>'
    '<path d="M -36,148 L 36,148 L 35,156 L -35,156 Z" fill="#5a7262"/>'
    '<path d="M -10,48 Q 0,62 10,48" fill="#f1c9a6"/>'
    # sleeves (short puff)
    '<path d="M -46,64 C -58,66 -60,90 -52,100 L -38,96 Z" fill="#94b09e"/><path d="M 46,64 C 58,66 60,90 52,100 L 38,96 Z" fill="#647e6e"/>'
    # watering can in the right hand
    '<g transform="translate(86,214)"><path d="M -18,0 L 18,0 L 14,40 L -14,40 Z" fill="#c9c3d6"/><path d="M -18,0 L -8,0 L -6,40 L -14,40 Z" fill="#ddd8e8"/>'
    '<path d="M 16,10 L 42,-14 L 46,-10 L 18,18 Z" fill="#b8b2c8"/><ellipse cx="45" cy="-13" rx="4" ry="6" fill="#a8a2b8" transform="rotate(-45 45 -13)"/>'
    '<path d="M -10,0 C -10,-20 10,-20 10,0" fill="none" stroke="#b8b2c8" stroke-width="4"/></g>'
    '<ellipse cx="78" cy="208" rx="9" ry="7.6" fill="#dba684"/>'
    '<use href="#wf"/>')

# dad: navy polo, beige slacks
dd_body = (shoes(466, '#5a4a40', '#4a3c34') + trousers(232, 468, '#c9b89e', '#d8c8b0', '#b0a084', w=42) +
           shirt('#3e4e78', '#506090', '#2e3a60', hem=240, w=46, sleeves='short', skin=('#e9bf98', '#d4a27c')) +
           '<path d="M -10,48 L 10,48 L 6,78 L -6,78 Z" fill="#2e3a60"/><circle cx="0" cy="62" r="1.5" fill="#d6d4d5"/><circle cx="0" cy="72" r="1.5" fill="#d6d4d5"/>' +
           '<rect x="-44" y="230" width="88" height="9" fill="#4a3a30"/>' +
           '<use href="#dd"/><path d="M -14,46 L -2,58 L -22,58 Z" fill="#506090"/><path d="M 14,46 L 2,58 L 22,58 Z" fill="#2e3a60"/>')

# mom: soft lilac blouse, long dusty skirt
mm_body = ('<path d="M -30,470 L -8,470 C -6,478 -8,483 -12,484 L -32,484 C -36,482 -35,474 -30,470 Z" fill="#6a5a6a"/><path d="M 30,470 L 8,470 C 6,478 8,483 12,484 L 32,484 C 36,482 35,474 30,470 Z" fill="#5a4a5a"/>'
           '<path d="M -40,226 L 40,226 C 48,300 54,380 56,456 L -56,456 C -54,380 -48,300 -40,226 Z" fill="#8a6c8e"/><path d="M -40,226 L -24,226 C -30,300 -34,380 -34,456 L -56,456 C -54,380 -48,300 -40,226 Z" fill="#9e80a2"/>'
           '<rect x="-24" y="454" width="12" height="18" fill="#f1c9a6"/><rect x="12" y="454" width="12" height="18" fill="#dba684"/>' +
           shirt('#c8b0d8', '#d8c4e4', '#a890bc', hem=236, w=44, sleeves='long', skin=('#f1c9a6', '#dba684')) +
           '<path d="M -8,50 Q 0,70 8,50" fill="#f1c9a6"/><g fill="#efe6f2"><circle cx="-6" cy="60" r="2.4"/><circle cx="0" cy="64" r="2.4"/><circle cx="6" cy="60" r="2.4"/></g>' +
           '<use href="#mm"/>')

# best friend: oversized teal-grey hoodie, jeans, sneakers, holding a gift box
fr_body = ('<path d="M -40,466 L -6,466 C -2,475 -4,481 -10,482 L -42,482 C -46,480 -45,470 -40,466 Z" fill="#f2eef4"/><path d="M 40,466 L 6,466 C 2,475 4,481 10,482 L 42,482 C 46,480 45,470 40,466 Z" fill="#e2dcea"/>' +
           trousers(232, 468, '#4a5878', '#5a6a8e', '#3a4664', w=40) +
           shirt('#8a6e9e', '#9e84b2', '#705688', hem=246, w=50, sleeves='long', skin=('#e9bf98', '#d4a27c')) +
           '<path d="M -26,150 L 26,150 L 30,196 L -30,196 Z" fill="#705688"/>' +   # front pocket
           '<path d="M -14,48 C -30,52 -36,40 -30,30 M 14,48 C 30,52 36,40 30,30" fill="none" stroke="#705688" stroke-width="8" stroke-linecap="round"/>' +  # hood rim
           '<path d="M -4,60 L -6,96 M 4,60 L 6,96" stroke="#e6e0ee" stroke-width="2" stroke-linecap="round"/>' +
           '<g transform="translate(0,206)"><rect x="-28" y="-26" width="56" height="44" rx="3" fill="#e8a6b8"/><rect x="-5" y="-26" width="10" height="44" fill="#fbe6a0"/><rect x="-28" y="-6" width="56" height="8" fill="#fbe6a0"/>'
           '<path d="M 0,-26 C -16,-42 -24,-28 0,-26 C 24,-28 16,-42 0,-26 Z" fill="#fbe6a0"/></g>' +
           '<ellipse cx="-34" cy="204" rx="10" ry="8" fill="#e9bf98"/><ellipse cx="34" cy="204" rx="10" ry="8" fill="#d4a27c"/>' +
           '<use href="#fr"/>')

# mystery watcher: hooded silhouette with binoculars, no face, cold rim light only
mystery = '''<svg viewBox="0 0 400 900" role="img" aria-label="บุคคลปริศนา หันหลัง สวมฮู้ด ยกกล้องส่องทางไกลมองออกหน้าต่าง">
<rect width="400" height="900" fill="#1e1940"/>
<rect x="50" y="70" width="300" height="430" fill="#2c2660"/><rect x="50" y="70" width="300" height="430" fill="none" stroke="#3e3474" stroke-width="12"/><rect x="196" y="70" width="8" height="430" fill="#3e3474"/>
<circle cx="285" cy="150" r="34" fill="#d8d4ff" opacity=".9"/><circle cx="285" cy="150" r="96" fill="#9a94e8" opacity=".12"/>
<g fill="#4a4286" opacity=".7"><rect x="70" y="380" width="40" height="120"/><rect x="118" y="340" width="34" height="160"/><rect x="240" y="360" width="44" height="140"/><rect x="292" y="400" width="40" height="100"/></g>
<g fill="#ffcf9e" opacity=".8"><rect x="126" y="360" width="6" height="8"/><rect x="138" y="390" width="6" height="8"/><rect x="250" y="380" width="6" height="8"/></g>
<rect x="30" y="500" width="340" height="18" fill="#3e3474"/>
<g transform="translate(200,210) scale(1.25)">
  <!-- hoodie from behind, arms raised holding binoculars to the face -->
  <path d="M -64,100 C -70,70 -66,40 -48,30 L 48,30 C 66,40 70,70 64,100 L 70,330 L -70,330 Z" fill="#14112a"/>
  <path d="M -64,100 C -70,70 -66,40 -48,30 L -30,30 C -44,60 -50,140 -52,330 L -70,330 Z" fill="#1d1938"/>
  <path d="M 48,30 C 66,40 70,70 64,100 L 70,330" fill="none" stroke="#8e88d8" stroke-width="2" opacity=".65"/>
  <!-- upper arms angled up and forward -->
  <path d="M -48,40 C -70,40 -86,30 -88,6 C -88,-14 -76,-24 -62,-24 L -40,-6 Z" fill="#14112a"/>
  <path d="M 48,40 C 70,40 86,30 88,6 C 88,-14 76,-24 62,-24 L 40,-6 Z" fill="#14112a"/>
  <path d="M 62,-24 C 76,-24 88,-14 88,6 C 86,30 70,40 48,40" fill="none" stroke="#8e88d8" stroke-width="2" opacity=".6"/>
  <!-- binocular barrels peeking past the hood -->
  <rect x="-50" y="-34" width="18" height="20" rx="5" fill="#0a0818"/><rect x="32" y="-34" width="18" height="20" rx="5" fill="#0a0818"/>
  <circle cx="-41" cy="-34" r="6" fill="#1a163a"/><circle cx="41" cy="-34" r="6" fill="#1a163a"/>
  <!-- hood -->
  <path d="M -44,32 C -54,0 -48,-46 -22,-62 C -8,-70 8,-70 22,-62 C 48,-46 54,0 44,32 C 28,42 -28,42 -44,32 Z" fill="#100e22"/>
  <path d="M -44,32 C -54,0 -48,-46 -22,-62 C -8,-70 0,-70 6,-68 C -20,-56 -34,-20 -30,30 Z" fill="#1d1938"/>
  <path d="M 22,-62 C 48,-46 54,0 44,32" fill="none" stroke="#a8a2f0" stroke-width="2.4" opacity=".75"/>
  <path d="M 0,-66 C -4,-30 -4,0 0,34" fill="none" stroke="#2a2552" stroke-width="2"/>
  <!-- legs -->
  <rect x="-40" y="330" width="34" height="140" fill="#0e0c1e"/><rect x="6" y="330" width="34" height="140" fill="#0e0c1e"/>
  <path d="M 40,330 L 40,470" stroke="#8e88d8" stroke-width="1.6" opacity=".5"/>
</g>
<rect y="770" width="400" height="130" fill="#14112a"/></svg>'''

def section(name, sub, full, close, cap_full, cap_close, chips, notes):
    ch = ''.join(f'<span><i style="background:{c}"></i>{t}</span>' for c, t in chips)
    nt = ''.join(f'<li>{n}</li>' for n in notes)
    right = (f'<figure>{close}<figcaption>{cap_close}</figcaption><div class="chips">{ch}</div><ul class="notes">{nt}</ul></figure>' if close
             else f'<figure><div class="chips">{ch}</div><ul class="notes">{nt}</ul></figure>')
    return (f'<section><h2>{name}<span>{sub}</span></h2><div class="panels"><figure>{full}<figcaption>{cap_full}</figcaption></figure>{right}</div></section>')

S = []
S.append(section('สามีบ้านตรงข้าม', 'นักแสดงคณะเดียวกับแฟนพระเอก ราว 32 ปี · สุภาพเกินไปจนน่าสงสัย',
    panel(figure(hb_body, 170, 1.22), 'สามีบ้านตรงข้าม เต็มตัว ประสานมือด้านหน้า'),
    closeup('hb', '<path d="M -54,70 C -52,58 -32,50 -12,48 L 12,48 C 32,50 52,58 54,70 Z" fill="#4a4a56"/><path d="M -12,48 L -2,64 L -18,60 Z M 12,48 L 2,64 L 18,60 Z" fill="#5c5c6a"/>'),
    'เต็มตัว · สูงโปร่งพอ ๆ กับพระเอก · เชิ้ตแขนยาวสีเทาเข้ม กางเกงสแล็กสีถ่าน รองเท้าหนัง · ยืนตัวตรง ประสานมือด้านหน้าแบบสุภาพ',
    'ใบหน้าระยะใกล้ · ผมเสยเรียบแปล้ หน้าเกลี้ยง คิ้วตรง · ตาหรี่ลงเล็กน้อย ยิ้มสุภาพเท่ากันสองข้าง ดูนิ่งเกินไปจนคนดูไม่ไว้ใจ',
    [('#f3cfae', 'ผิว'), ('#17141a', 'ผม'), ('#4a4a56', 'เชิ้ต'), ('#34343e', 'กางเกง')],
    ['ช็อตเงยหน้าขึ้นมายิ้มให้พระเอกในฉาก 4 ใช้หน้านี้ ซูมช้า ๆ ให้รอยยิ้มค่อย ๆ ขึ้น', 'พอเฉลยในฉาก 7 เปลี่ยนเป็นยิ้มกว้างหัวเราะ คนดูจะรู้ทันทีว่าเป็นคนธรรมดา']))
S.append(section('ภรรยาบ้านตรงข้าม', 'นักแสดงคณะเดียวกัน ราว 28 ปี · อ่อนโยน ดูแลต้นไม้ทุกเช้า',
    panel(figure(wf_body, 172, 1.22), 'ภรรยาบ้านตรงข้าม เต็มตัว ถือบัวรดน้ำ'),
    closeup('wf', '<path d="M -54,70 C -52,58 -32,50 -14,48 L 14,48 C 32,50 52,58 54,70 Z" fill="#7d9a88"/><path d="M -10,48 Q 0,62 10,48" fill="#f1c9a6"/>'),
    'เต็มตัว · เดรสยาวครึ่งน่องสีเขียวหม่น แขนตุ๊กตา คาดเอว รองเท้าแฟลตสีครีม · ถือบัวรดน้ำสีเงิน',
    'ใบหน้าระยะใกล้ · ผมยาวตรงมัดครึ่งหัวด้วยยางสีเขียวเซจ ตาหวาน ขนตาสั้นงอน คิ้วบาง ยิ้มอ่อน',
    [('#f1c9a6', 'ผิว'), ('#2a1a1c', 'ผม'), ('#7d9a88', 'เดรส'), ('#c9c3d6', 'บัวรดน้ำ')],
    ['ในฉาก 3 เห็นแค่ระยะไกลตอนรดน้ำต้นไม้ และเป็นเงาในฉากทะเลาะกับฉาก 5', 'ฉาก 7 ยืนข้างสามี ยิ้มแหย ๆ ขอโทษพระเอก']))
S.append(f'''<section><h2>ตัวประกอบฉากเซอร์ไพรส์<span>พ่อ แม่ และเพื่อนสนิทของพระเอก · อยู่ระยะกลางในฉาก 7–8</span></h2>
<div class="trio"><figure>{panel(figure(dd_body, 176, 1.15), 'พ่อของพระเอก')}<figcaption><b>พ่อ</b> ราว 58 ปี ผมสีเทา แว่นกรอบเหลี่ยม เสื้อโปโลกรม สแล็กสีเบจ ยิ้มใจดี</figcaption></figure>
<figure>{panel(figure(mm_body, 182, 1.1), 'แม่ของพระเอก')}<figcaption><b>แม่</b> ราว 55 ปี ผมดัดสั้น ต่างหูมุก เสื้อแขนยาวสีม่วงอ่อน กระโปรงยาว ยิ้มตาหยี</figcaption></figure>
<figure>{panel(figure(fr_body, 170, 1.2), 'เพื่อนสนิทของพระเอก')}<figcaption><b>เพื่อนสนิท</b> ราว 30 ปี หมวกไหมพรม ฮู้ดดี้ตัวโคร่ง ยีนส์ สนีกเกอร์ ถือกล่องของขวัญ ยิ้มกว้าง</figcaption></figure></div></section>''')
S.append(section('บุคคลปริศนา', 'ฉาก 8 เท่านั้น · หันหลังใส่ฮู้ดเท่านั้น ห้ามเห็นหน้า ห้ามบอกเพศ', mystery, '',
    'หันหลังให้กล้องเสมอ สวมฮู้ดคลุมหัว ยกกล้องส่องทางไกลมองออกหน้าต่างไปที่งานเลี้ยง แสงจันทร์ติดขอบฮู้ด ไหล่ และแขนเป็นเส้นบาง ๆ ไม่เห็นหน้า มือ หรือผม',
    '', [('#14112a', 'ฮู้ด'), ('#8e88d8', 'แสงขอบจันทร์')],
    ['ใช้มุมหันหลังมุมเดียว ห้ามหันหน้า หันข้าง หรือเห็นมือชัด เพื่อไม่ให้เดาได้ว่าเป็นใคร', 'เปิดตัวด้วยการแพนกล้องจากงานเลี้ยงมาที่ห้องนี้ เห็นแผ่นหลังสวมฮู้ดกับกล้องส่องทางไกล แล้วหยุดนิ่งก่อนตัดดำ']))

page = f'''<title>บ้านตรงข้าม ตัวละครอื่น ๆ</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: husband & wife rows (full body + close-up), a 3-up row for the party extras, then the mystery silhouette. Same look as the lead sheet. */
:root {{ --stage:#f5f0f3; --panel:#fff; --ink:#3b3346; --muted:#847a90; --line:#e2d9e3; --accent:#8a6cc8; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:light; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:980px; margin:0 auto; display:grid; gap:36px; }}
header p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.6; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }}
h2 {{ font-size:18px; font-weight:500; margin:0; }} h2 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
section {{ display:grid; gap:14px; }}
.panels {{ display:grid; grid-template-columns:4fr 5fr; gap:16px; align-items:start; }}
.trio {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
@media (max-width:640px) {{ .panels, .trio {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; border-radius:6px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:13px; color:var(--muted); line-height:1.6; }} figcaption b {{ color:var(--ink); font-weight:500; }}
.chips {{ display:flex; flex-wrap:wrap; gap:10px 16px; font-size:12px; color:var(--muted); }}
.chips span {{ display:inline-flex; align-items:center; gap:6px; }}
.chips i {{ width:14px; height:14px; border-radius:3px; display:inline-block; box-shadow:0 0 0 1px var(--line); }}
ul.notes {{ margin:0; padding-left:18px; font-size:13px; line-height:1.7; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="skyBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ab9cd8"/><stop offset=".6" stop-color="#cdb6dd"/><stop offset="1" stop-color="#e6cfe2"/></linearGradient>
{DEFS}</defs></svg>
<div class="wrap"><header><h1>บ้านตรงข้าม · ตัวละครอื่น ๆ</h1>
<p>ลายเส้นเดียวกับพระเอก นางเอก และแก๊งเพื่อนตำรวจ · สามีภรรยาบ้านตรงข้ามคือนักแสดงคณะเดียวกับแฟนพระเอก ต้องดูน่าสงสัยตอนต้นเรื่อง แต่กลายเป็นคนธรรมดาตอนเฉลย</p></header>
{"".join(S)}</div>'''
open('others.html', 'w', encoding='utf-8').write(page)
print('ok')
