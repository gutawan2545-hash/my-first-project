"""ริกตัวละครรอบ 2: แขนสองท่อน (ต้นแขน + แขนท่อนล่างพร้อมมือ) หมุนที่ไหล่และข้อศอกได้
ตัดแขนเดิมออกจากตัว แล้ววาดแขนใหม่เป็นกลุ่มที่ JS หมุนได้ ตัวแยกเป็นกลุ่มเพื่อหายใจ/ถ่ายน้ำหนัก
id ที่ JS ใช้: {p}Body · {p}LU {p}LF (แขนซ้ายของภาพ) · {p}RU {p}RF · {p}H (หัว) · {p}B (กะพริบ) · {p}M (ปาก) · {p}T (น้ำตา)"""
import re
import supporting as SP
import wedding_chars as WC

def strip(svg, keys):
    for tag in re.findall(r'<[^>]+/>', svg):
        if any(k in tag for k in keys): svg = svg.replace(tag, '', 1)
    return svg

def arm(p, side, sx, sy, L1, L2, w1, w2, up, fore, hand, extra=''):
    """side = 'L' (ซ้ายของภาพ, x ติดลบ) หรือ 'R' · up/fore = (สีกลาง, สีแสง/เงา) · hand = สีมือ"""
    s = -1 if side == 'L' else 1
    ex, ey = sx, sy + L1
    hl = up[1]; fl = fore[1]
    upper = (f'<path d="M {sx - w1 / 2},{sy - 4} Q {sx},{sy - 10} {sx + w1 / 2},{sy - 4} L {ex + w2 / 2},{ey} L {ex - w2 / 2},{ey} Z" fill="{up[0]}"/>'
             f'<path d="M {sx + s * w1 / 2 * -1},{sy - 2} L {ex + s * w2 / 2 * -1},{ey} L {ex + s * (w2 / 2 - 3) * -1},{ey} L {sx + s * (w1 / 2 - 3) * -1},{sy} Z" fill="{hl}" opacity=".8"/>'
             f'<circle cx="{ex}" cy="{ey}" r="{w2 / 2}" fill="{up[0]}"/>')
    wy = ey + L2
    forearm = (f'<path d="M {ex - w2 / 2},{ey} L {ex + w2 / 2},{ey} L {ex + w2 / 2 - 1},{wy} L {ex - w2 / 2 + 1},{wy} Z" fill="{fore[0]}"/>'
               f'<path d="M {ex - s * w2 / 2},{ey} L {ex - s * (w2 / 2 - 3)},{ey} L {ex - s * (w2 / 2 - 3.6)},{wy} L {ex - s * (w2 / 2 - 1)},{wy} Z" fill="{fl}" opacity=".8"/>'
               f'<path d="M {ex - 6},{wy - 2} L {ex + 6},{wy - 2} C {ex + 7},{wy + 12} {ex + 5},{wy + 24} {ex},{wy + 26} C {ex - 5},{wy + 24} {ex - 7},{wy + 12} {ex - 6},{wy - 2} Z" fill="{hand}"/>'
               f'<path d="M {ex + s * 5},{wy + 4} C {ex + s * 9},{wy + 8} {ex + s * 9},{wy + 14} {ex + s * 6},{wy + 17} Z" fill="{hand}"/>' + extra)
    return (f'<g id="{p}{side}U" data-sx="{sx}" data-sy="{sy}"><g>{upper}</g><g id="{p}{side}F" data-ex="{ex}" data-ey="{ey}">{forearm}</g></g>', (sx, sy))

def blink(p, skin, ex=13, ey=-1.6, rx=10, ry=7, scale=None):
    g = (f'<g id="{p}B" display="none">' + ''.join(
        f'<ellipse cx="{s * ex}" cy="{ey}" rx="{rx}" ry="{ry}" fill="{skin}"/><path d="M {s * (ex + 9)},{ey + .5} Q {s * ex},{ey + 4} {s * (ex - 9)},{ey + .5}" fill="none" stroke="#1c1214" stroke-width="1.6" stroke-linecap="round"/>'
        for s in (-1, 1)) + '</g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
def mouth(p, skin, lip, scale=None):
    g = (f'<g id="{p}M" display="none"><ellipse cx="0" cy="24.2" rx="8.8" ry="5" fill="{skin}"/>'
         f'<ellipse id="{p}Mo" cx="0" cy="24.4" rx="4.6" ry="2" fill="#4a1420" stroke="{lip}" stroke-width="1.8"/>'
         f'<rect id="{p}Mt" x="-3" y="22.6" width="6" height="1.4" rx=".6" fill="#ffffff"/></g>')
    return f'<g transform="{scale}">{g}</g>' if scale else g
def tears(p):
    return (f'<g id="{p}T" display="none"><path d="M -14,4 C -15,12 -13,20 -15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/>'
            f'<path d="M 14,4 C 15,12 13,20 15,30" stroke="#cfe0ff" stroke-width="2" fill="none" opacity=".85"/><circle cx="-15" cy="31" r="1.8" fill="#e6f0ff"/></g>')

F_ARM_KEYS = ('M -38,60 C', 'M 38,60 C', 'M -46,92', 'M 46,92', 'M -51,210', 'M 51,210', 'M -51,150', 'x="41.5"', 'cx="45"')
M_ARM_KEYS = ('M -50,68 C -58', 'M 50,68 C 58', '-58,96', 'x="-59"', 'x="44"', 'M -59,229', 'M 59,229', 'cx="-51.5"', 'cx="51.5"', 'x="45.5"', 'x="44.5"')
RING = '<rect x="{x}" y="{y}" width="7" height="2.6" rx="1.2" fill="#f4f6f9"/><circle cx="{cx}" cy="{cy}" r="1.6" fill="#e8f0ff"/>'

def wrap(p, back, body, arms, head, lf):
    return (f'<g id="{p}">{back}<g id="{p}Body">{body}</g>{arms}<g id="{p}H">{head}</g></g>', lf)

def bride_rig(p, heads=('b2head', 'b2head_worry', 'b2head_scared')):
    body = strip(WC.bride_body(), F_ARM_KEYS)
    L, _ = arm(p, 'L', -43, 66, 74, 72, 12, 10, ('#fbe2cf', '#fff4ea'), ('#fbe2cf', '#fff4ea'), '#fbe2cf')
    R, _ = arm(p, 'R', 43, 66, 74, 72, 12, 10, ('#efc3a8', '#d9a089'), ('#efc3a8', '#d9a089'), '#efc3a8',
               RING.format(x=39.5, y=226, cx=43, cy=225.4))
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    return wrap(p, '<use href="#b2back"/>', body, L + R, hs + blink(p, '#fbe2cf') + tears(p), 462)

def woman_rig(p):
    n, nt, kind, back, head, body = SP.c_woman_black()
    body = strip(body, F_ARM_KEYS)
    glove = ('#141218', '#2c2a34')
    L, _ = arm(p, 'L', -43, 66, 74, 72, 12, 10, ('#f1d8cc', '#fbeae2'), glove, '#141218')
    R, _ = arm(p, 'R', 43, 66, 74, 72, 12, 10, ('#dcb7aa', '#c49688'), glove, '#141218', RING.format(x=39.5, y=226, cx=43, cy=225.4))
    sc = 'scale(.87 1.03)'
    return wrap(p, back, body, L + R, head + blink(p, '#f1d8cc', scale=sc) + mouth(p, '#f1d8cc', '#8e2236', scale=sc), 460)

def male_arms(p, sleeve_l, sleeve_d, shirt, skin_l, skin_d, ring=False):
    L, _ = arm(p, 'L', -52, 72, 80, 78, 15, 13, (sleeve_l, '#454856'), (sleeve_l, '#454856'), skin_l,
               f'<rect x="-59" y="226" width="14" height="6" fill="{shirt}" transform="translate(7,-0)"/>')
    R, _ = arm(p, 'R', 52, 72, 80, 78, 15, 13, (sleeve_d, '#0e0f14'), (sleeve_d, '#0e0f14'), skin_d,
               f'<rect x="45" y="226" width="14" height="6" fill="#d8d4ce" transform="translate(0,0)"/>' + (RING.format(x=48.5, y=244, cx=52, cy=243.4) if ring else ''))
    return L + R

def groom_rig(p, heads=('ghead', 'ghead_angry', 'ghead_sin')):
    body = strip(WC.groom_body(), M_ARM_KEYS)
    hs = ''.join(f'<use id="{p}H{k}" href="#{h}" display="{"inline" if k == 0 else "none"}"/>' for k, h in enumerate(heads))
    head = hs + blink(p, '#f6dcc8', 12, -1.6, 9.6, 5.4) + mouth(p, '#f6dcc8', WC.G_LIP) + '<path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="#d8d4ce" stroke-width="2"/>'
    return wrap(p, '', body, male_arms(p, WC.TUX_L, WC.TUX_D, WC.SHIRT, WC.G_SKIN, WC.G_SKIN_S, True), head, 488)

def guard_rig(p):
    n, nt, kind, back, head, body = SP.c_guard()
    body = strip(body, M_ARM_KEYS)
    return wrap(p, back, body, male_arms(p, '#24242c', '#0c0c10', '#f7f5f1', '#ecc4a2', '#d8a682'),
                head + blink(p, '#ecc4a2', 12, -1.6, 9.6, 5.4, scale='scale(.88 1.03)'), 488)
