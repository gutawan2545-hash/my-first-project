# ฉาก 2 แบบใหม่: มองตรงจากหน้าเคาน์เตอร์เข้าหาผนังหลังร้าน (ระดับสายตา)
# แสงแดดบ่ายเข้าจากประตูร้านทางซ้าย (นอกเฟรม) เงาตกไปขวาล่าง
import random

FONT = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'

EXTRA_DEFS = '''
<filter id="dofLite" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="0.9"/></filter>
<linearGradient id="wallDay" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#e6cfa8"/><stop offset="1" stop-color="#f2e0c0"/></linearGradient>
<linearGradient id="tileDay" gradientUnits="userSpaceOnUse" x1="0" y1="640" x2="0" y2="800"><stop offset="0" stop-color="#e9d6b4"/><stop offset="1" stop-color="#f4e6cc"/></linearGradient>
<linearGradient id="sunWall" gradientUnits="userSpaceOnUse" x1="0" y1="80" x2="420" y2="760"><stop offset="0" stop-color="#fff2cc" stop-opacity=".38"/><stop offset=".6" stop-color="#ffd98e" stop-opacity=".14"/><stop offset="1" stop-color="#ffd98e" stop-opacity="0"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e8f4f2" stop-opacity=".55"/><stop offset=".5" stop-color="#cfe6e2" stop-opacity=".22"/><stop offset="1" stop-color="#bcd8d2" stop-opacity=".4"/></linearGradient>
'''


def rr(x, y, w, h, c, rx=0, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{c}"{extra}/>'


# ---------------- products ----------------
def paint_bucket(x, y, w, h, label, accent, handle=True):
    s = rr(x, y, w, h, '#e9e1d2') + rr(x, y, w*.22, h, '#f8f2e6') + rr(x+w*.8, y, w*.2, h, '#c8b9a2')
    s += rr(x, y+h*.22, w, h*.56, label) + rr(x+w*.8, y+h*.22, w*.2, h*.56, '#000', extra=' opacity=".2"') + rr(x, y+h*.22, w*.22, h*.56, '#fff', extra=' opacity=".18"')
    s += f'<circle cx="{x+w*.5:.1f}" cy="{y+h*.5:.1f}" r="{min(w,h)*.16:.1f}" fill="{accent}"/>'
    s += rr(x+w*.14, y+h*.66, w*.5, 2, '#fff', extra=' opacity=".75"')
    s += rr(x-1, y-3, w+2, 6, '#cfc3ae', 2) + rr(x-1, y-3, w*.3, 6, '#ece4d4', 2)
    if handle:
        s += f'<path d="M{x+w*.12:.1f},{y+2:.1f} q{w*.38:.1f},-{h*.3:.1f} {w*.76:.1f},0" fill="none" stroke="#8a7e6c" stroke-width="1.6"/>'
    return s


def tin(x, y, w, h, label):
    s = rr(x, y, w, h, '#b9b2a6') + rr(x, y, w*.25, h, '#ddd7cc') + rr(x+w*.78, y, w*.22, h, '#8e877c')
    s += rr(x, y+h*.2, w, h*.62, label) + rr(x+w*.78, y+h*.2, w*.22, h*.62, '#000', extra=' opacity=".2"')
    s += rr(x+w*.18, y+h*.45, w*.5, 1.6, '#fff', extra=' opacity=".7"') + rr(x-.5, y-2, w+1, 3, '#a39c90', 1)
    return s


def spray(x, y, c):
    return (rr(x, y+8, 11, 34, '#d8d4cc', 2) + rr(x, y+8, 3, 34, '#f2efe8') + rr(x+8, y+8, 3, 34, '#a8a298')
            + rr(x, y+16, 11, 16, c) + rr(x+1.5, y, 8, 9, c, 2) + rr(x+1.5, y, 2.5, 9, '#fff', extra=' opacity=".3"'))


def hook(x, y):
    return f'<path d="M{x},{y} l0,7" stroke="#7d746c" stroke-width="1.6"/>'


def card(x, y, w, h, head):
    return rr(x, y, w, h, '#f4efe6', 1.5) + rr(x, y, w, h*.24, head, 1.5) + rr(x+w/2-3, y+2, 6, 2.5, '#3a302c', 1)


def hammer(x, y):
    return (rr(x-3, y, 6, 52, '#c88e56', 2) + rr(x-3, y, 2, 52, '#e0aa72', 1) + rr(x-3, y+34, 6, 18, '#2a2a30', 2)
            + f'<path d="M{x-14},{y-2} l26,0 l4,4 l-4,6 l-26,0 Z" fill="#8e949e"/><path d="M{x-14},{y-2} l26,0 l0,3 l-26,0 Z" fill="#c4c9d0"/>')


def pliers(x, y, c):
    return (f'<path d="M{x-2},{y} l-7,40 l5,1 l6,-34 Z" fill="{c}"/><path d="M{x+2},{y} l7,40 l-5,1 l-6,-34 Z" fill="{c}"/>'
            f'<path d="M{x-3},{y-16} l3,16 l3,-16 l-1,-4 l-4,0 Z" fill="#9aa0a8"/><circle cx="{x}" cy="{y}" r="2.6" fill="#6a7078"/>')


def screwdriver(x, y, c):
    return rr(x-3.5, y, 7, 20, c, 3) + rr(x-3.5, y, 2.4, 20, '#fff', 2, ' opacity=".3"') + rr(x-1, y+20, 2, 22, '#a8aeb6')


def tape_measure_card(x, y):
    return card(x, y, 30, 40, '#e8b828') + rr(x+4, y+12, 22, 22, '#e8b828', 5) + rr(x+4, y+12, 22, 7, '#2a2a30', 3) + f'<circle cx="{x+15}" cy="{y+25}" r="5" fill="#c9a018"/>' + rr(x+24, y+28, 5, 4, '#c4c9d0')


def lock_card(x, y):
    return (card(x, y, 28, 40, '#c43a34') + f'<path d="M{x+8},{y+22} v-5 a6,6 0 0 1 12,0 v5" fill="none" stroke="#b8bec6" stroke-width="2.4"/>'
            + rr(x+6, y+21, 16, 13, '#d0a43c', 2) + rr(x+6, y+21, 5, 13, '#ecc464', 2) + f'<circle cx="{x+14}" cy="{y+27}" r="1.5" fill="#6a4a1a"/>')


def disc_card(x, y, c):
    return card(x, y, 32, 38, '#2a5aa8') + f'<circle cx="{x+16}" cy="{y+23}" r="11" fill="{c}"/><circle cx="{x+16}" cy="{y+23}" r="3" fill="#f4efe6"/><path d="M{x+8},{y+18} a10,10 0 0 1 8,-6" stroke="#fff" stroke-width="1.5" fill="none" opacity=".45"/>'


def brush_card(x, y):
    return (card(x, y, 24, 46, '#3a7a4a') + rr(x+8, y+12, 8, 14, '#c88e56', 2) + rr(x+6, y+25, 12, 4, '#b8bec6') + rr(x+6, y+29, 12, 13, '#3a2c22', 1) + rr(x+6, y+29, 4, 13, '#5a4a3a', 1))


def gloves(x, y):
    return (f'<path d="M{x},{y} h16 v22 l4,12 l-6,0 l-1,-4 l-2,5 h-4 l-1,-6 l-2,6 h-4 Z" fill="#e8e2d4"/><path d="M{x},{y} h5 v34 h-5 Z" fill="#fff" opacity=".4"/>'
            f'<path d="M{x+2},{y+12} h14 v10 h-14 Z" fill="#e2733a"/>')


def hose(x, y, r, c, cd):
    return ''.join(f'<ellipse cx="{x}" cy="{y+i*2.2:.1f}" rx="{r}" ry="{r*.92:.1f}" fill="none" stroke="{c if i%2 else cd}" stroke-width="5"/>' for i in range(5)) + rr(x-3, y-r-8, 6, 10, '#7d746c')


def box(x, y, w, h, seed, mark=True):
    r = random.Random(seed)
    c = r.choice((('#e0a868', '#c4874a', '#9e6634'), ('#d89c5c', '#b87c40', '#8e5a2c'), ('#e8b47a', '#cc935a', '#a46c38')))
    s = rr(x, y, w, h, c[1]) + rr(x, y, w*.25, h, c[0]) + rr(x+w*.85, y, w*.15, h, c[2])
    s += rr(x, y+h*.1, w, 3, '#e8d6b4', extra=' opacity=".55"')  # packing tape
    if mark:
        s += rr(x+w*.2, y+h*.5, w*.6, h*.2, '#f4ead6', 1, ' opacity=".85"')
        s += f'<text x="{x+w*.5:.0f}" y="{y+h*.5+h*.15:.0f}" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="8" fill="#2a2030" opacity=".8">{r.choice(["ข้องอ 1/2", "สามทาง", "ต่อตรง", "ตะปู 2 นิ้ว", "กาวยาง", "เทปพันสาย"])}</text>'
    return s


# ---------------- the frame ----------------
def frame_int2(dust):
    s = '<rect width="540" height="960" fill="url(#wallDay)"/>'
    # ceiling + tube light
    s += rr(0, 0, 540, 70, '#a87e5c') + rr(0, 64, 540, 8, '#8a6448') + rr(0, 70, 540, 6, '#f2e2c4')
    s += rr(300, 30, 120, 7, '#fffaf0', 3) + rr(296, 26, 128, 4, '#c9b49a', 2)

    back = ''
    # ===== top stock shelf (y 100-200) =====
    back += rr(0, 196, 540, 8, '#8a6a52') + rr(0, 204, 540, 4, '#5e4636')
    xs = [8, 70, 124, 190, 262, 330, 392, 456]
    for i, x in enumerate(xs):
        w = 54 + (i * 13) % 14; h = 58 + (i * 17) % 26
        back += f'<g filter="url(#dshS)">{box(x, 196-h, w, h, i)}</g>'
    # wall clock + calendar
    back += f'<g filter="url(#dshS)"><circle cx="476" cy="244" r="20" fill="#7a4e32"/><circle cx="476" cy="244" r="16" fill="#fbf4e6"/><path d="M476,244 l0,-10 M476,244 l7,4" stroke="#2a2030" stroke-width="2" stroke-linecap="round"/></g>'
    back += f'<g filter="url(#dshS)">{rr(20, 222, 66, 86, "#fbf4e6")}{rr(20, 222, 66, 22, "#c8423a")}<text x="53" y="238" text-anchor="middle" {FONT} font-size="11" font-weight="700" fill="#fff">ปฏิทิน</text>'
    back += ''.join(rr(26 + (k % 7) * 8.2, 250 + (k // 7) * 10, 5.5, 6, '#c8423a' if k in (6, 13, 20) else '#8a7e74') for k in range(35)) + '</g>'

    # ===== left: paint shelving (x 0-150) =====
    back += rr(0, 320, 150, 330, '#a9805c') + rr(0, 320, 150, 330, '#6a4430', extra=' opacity=".35"')
    for yy in (420, 520, 620):
        back += rr(0, yy, 150, 7, '#c49a72') + rr(0, yy+7, 150, 4, '#6a4a34')
    back += rr(144, 320, 8, 330, '#8a6448')
    labs = [('#2f6aa8', '#e6c34a'), ('#c8423a', '#fbf4e6'), ('#3a8a5a', '#fbf4e6'), ('#e6a23a', '#2a2030'), ('#7a3a8a', '#fbf4e6')]
    # row 1: tins
    for i in range(7):
        back += f'<g filter="url(#dshS)">{tin(6+i*20, 386, 17, 34, labs[i%5][0])}</g>'
    # row 2: medium buckets
    for i in range(4):
        back += f'<g filter="url(#dshS)">{paint_bucket(6+i*36, 474, 31, 46, labs[(i+1)%5][0], labs[(i+1)%5][1], False)}</g>'
    # row 3: big buckets
    for i in range(3):
        back += f'<g filter="url(#dshS)">{paint_bucket(6+i*47, 556, 42, 64, labs[(i+2)%5][0], labs[(i+2)%5][1])}</g>'

    # ===== center: pegboard with tools (x 162-388) =====
    back += f'<g filter="url(#dshS)">{rr(162, 230, 226, 330, "#d8b98e")}{rr(162, 230, 226, 6, "#ecd4ae")}{rr(382, 230, 6, 330, "#b0906a")}</g>'
    back += '<g fill="#8a6a4a">' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.4"/>' for x in range(172, 382, 12) for y in range(242, 552, 12)) + '</g>'
    tools = ''
    # row A (y 250): hammers + pliers + screwdrivers
    for i, x in enumerate((182, 206)):
        tools += hook(x, 244) + hammer(x, 254)
    for i, (x, c) in enumerate(((236, '#c8423a'), (256, '#2f6aa8'), (276, '#e6a23a'))):
        tools += hook(x, 244) + pliers(x, 268, c)
    tools += rr(296, 250, 80, 6, '#7d746c')
    for i, c in enumerate(('#c8423a', '#e6c34a', '#2f6aa8', '#c8423a', '#3a8a5a', '#2a2a30')):
        tools += screwdriver(304 + i * 12, 256, c)
    # row B (y 324): blister cards
    x = 172
    for f in (lambda x: tape_measure_card(x, 324), lambda x: lock_card(x, 324), lambda x: lock_card(x, 324),
              lambda x: tape_measure_card(x, 324), lambda x: disc_card(x, 324, '#c4632a'), lambda x: disc_card(x, 324, '#5a5a62')):
        tools += hook(x + 15, 318) + f(x)
        x += 35
    # row C (y 392): brushes, gloves, discs
    x = 174
    for k in range(3):
        tools += hook(x + 12, 386) + brush_card(x, 392); x += 29
    for k in range(2):
        tools += hook(x + 10, 386) + gloves(x, 394); x += 26
    for c in ('#c4632a', '#3a3a42'):
        tools += hook(x + 16, 386) + disc_card(x, 392, c); x += 36
    # row D (y 462): tape rolls on a rod + cable ties
    tools += rr(176, 462, 200, 5, '#7d746c')
    for i, (c, d) in enumerate((('#f2eee6', '#cfc8bc'), ('#3a3a42', '#1e1e24'), ('#e8c24a', '#b8941e'), ('#2f6aa8', '#1e4a80'), ('#c8423a', '#8e2a24'), ('#f2eee6', '#cfc8bc'), ('#3a8a5a', '#24603c'))):
        cx = 192 + i * 27
        tools += f'<circle cx="{cx}" cy="486" r="12" fill="{c}"/><circle cx="{cx}" cy="486" r="12" fill="none" stroke="{d}" stroke-width="2"/><circle cx="{cx}" cy="486" r="5" fill="#d8b98e"/>'
    tools += hook(250, 512) + card(236, 518, 30, 36, '#2a2a30') + ''.join(rr(240 + k * 5, 530, 2, 20, '#f2eee6') for k in range(5))
    tools += hook(300, 512) + card(286, 518, 30, 36, '#c8423a') + rr(292, 530, 18, 18, '#b8bec6', 9) + rr(297, 535, 8, 8, '#d8b98e', 4)
    tools += hook(350, 512) + card(336, 518, 30, 36, '#e6a23a') + rr(342, 532, 18, 6, '#8e949e') + rr(342, 542, 18, 6, '#8e949e')
    back += f'<g filter="url(#dshS)">{tools}</g>'

    # ===== right: parts drawer cabinet + hoses (x 400-540) =====
    back += f'<g filter="url(#dshS)">{rr(400, 300, 140, 200, "#8fb2ac")}{rr(400, 300, 140, 6, "#b2d0ca")}{rr(400, 300, 6, 200, "#a8c8c2")}'
    for rI in range(7):
        for cI in range(5):
            dx = 410 + cI * 26; dy = 312 + rI * 26
            back += rr(dx, dy, 22, 21, '#e9e2d2', 1.5) + rr(dx, dy, 22, 3, '#fbf6ea') + rr(dx+4, dy+5, 14, 5, '#fbf6ea') + rr(dx+7, dy+14, 8, 3, '#6a6460', 1.5)
    back += '</g>'
    back += f'<g filter="url(#dshS)">{hose(436, 548, 26, "#3a8a5a", "#2a6a44")}{hose(500, 552, 24, "#2f6aa8", "#1e4a80")}</g>'
    back += rr(400, 516, 140, 4, '#7d746c')

    # skirting + floor
    back += rr(0, 650, 540, 10, '#c4a27e')
    back += '<rect x="0" y="660" width="540" height="140" fill="url(#tileDay)"/>'
    back += ''.join(f'<path d="M{270+(x-270)*.55:.0f},660 L{x},800" stroke="#cdb593" stroke-width="1.4"/>' for x in range(-330, 900, 110))
    back += '<path d="M0,700 L540,700 M0,752 L540,752" stroke="#cdb593" stroke-width="1.4"/>'
    fl = ''
    # stacked plastic buckets (left)
    for k in range(4):
        fl += f'<path d="M{20},{646-k*9} l50,0 l-5,-26 l-40,0 Z" fill="{("#e86a8a","#5aa6d6","#e86a8a","#5aa6d6")[k]}"/>'
    fl += rr(18, 560, 54, 6, '#f08aa6', 2)
    # cement sacks (small stack)
    for k in range(3):
        fl += rr(88 + (k%2)*4, 620 - k*22, 80, 24, '#efe8dc', 8) + rr(88 + (k%2)*4, 620-k*22, 80, 8, '#fbf6ee', 6) + rr(100 + (k%2)*4, 628-k*22, 40, 8, ('#c8423a','#3a8a5a','#c8423a')[k])
    # broom + mop leaning on the wall (right)
    fl += '<path d="M470,650 L500,470" stroke="#c88e56" stroke-width="4"/><path d="M462,654 l-6,-6 l40,-12 l14,10 Z" fill="#9c7a52"/>'
    fl += '<path d="M520,650 L528,500" stroke="#5aa6d6" stroke-width="4"/><path d="M506,652 l30,0 l-4,-22 l-22,0 Z" fill="#e8e2d4"/>'
    # step stool (centre)
    fl += rr(300, 612, 56, 8, '#3a7ac0', 2) + rr(304, 620, 6, 32, '#2a5a9a') + rr(346, 620, 6, 32, '#2a5a9a') + rr(300, 612, 56, 3, '#6aa0dc', 2)
    back += f'<g filter="url(#dsh)">{fl}</g>'
    s += f'<g filter="url(#dofLite)">{back}</g>'

    # ===== sunlight from the shop door (left, out of frame) =====
    s += '<path d="M0,80 L150,80 L470,800 L0,800 Z" fill="url(#sunWall)" style="mix-blend-mode:screen"/>'
    s += '<path d="M60,80 L84,80 L404,800 L380,800 Z" fill="#7a4a2a" opacity=".10"/><path d="M0,330 L0,300 L250,800 L220,800 Z" fill="#7a4a2a" opacity=".08"/>'
    s += '<path d="M150,80 L540,80 L540,800 L470,800 Z" fill="#6a3a1e" opacity=".16"/>'

    # ===== foreground: glass display counter (y 770-960) =====
    fg = rr(0, 770, 540, 16, '#f4e8d2') + rr(0, 770, 540, 4, '#fffaf0') + rr(0, 786, 540, 6, '#b8946c')
    fg += rr(0, 792, 540, 168, '#8a5e40') + rr(0, 792, 540, 6, '#6a4630')
    # glass case with small items inside
    fg += rr(16, 804, 508, 128, '#5e3e2c')
    inside = ''
    r = random.Random(77)
    for row, yy in enumerate((812, 872)):
        inside += rr(16, yy + 52, 508, 4, '#d8c4a4')
        x = 26
        while x < 500:
            k = r.random()
            if k < .35:
                c = r.choice(('#f2eee6', '#e8c24a', '#c8423a'))
                inside += rr(x, yy + 22, 30, 30, c, 2) + rr(x, yy + 22, 30, 8, '#2a2a30', 2) + rr(x + 5, yy + 34, 20, 3, '#8a7e74')
                x += 36
            elif k < .6:
                inside += lock_card(x, yy + 12); x += 34
            elif k < .8:
                inside += ''.join(f'<rect x="{x+j*7}" y="{yy+30}" width="5" height="22" rx="1" fill="#{r.choice(["e8d8b8","c8423a","2f6aa8"])}"/>' for j in range(4)); x += 34
            else:
                inside += f'<circle cx="{x+14}" cy="{yy+38}" r="13" fill="#2a2a30"/><circle cx="{x+14}" cy="{yy+38}" r="5" fill="#8e949e"/>'; x += 34
    fg += f'<g filter="url(#dofLite)">{inside}</g>'
    fg += '<rect x="16" y="804" width="508" height="128" fill="url(#glass)"/>'
    fg += '<path d="M60,804 L120,804 L40,932 L16,932 L16,880 Z" fill="#ffffff" opacity=".22"/><path d="M300,804 L330,804 L250,932 L220,932 Z" fill="#ffffff" opacity=".14"/>'
    fg += rr(268, 804, 4, 128, '#8a5e40')
    fg += rr(0, 940, 540, 20, '#6a4630')
    # counter-top items
    top = ''
    # receipt book + pen
    top += rr(70, 748, 64, 26, '#fbf4e6', 2) + rr(70, 748, 64, 6, '#2f6aa8', 2) + ''.join(rr(76, 758 + k * 4.5, 50, 1.4, '#a89c90') for k in range(3))
    top += f'<path d="M100,766 l40,-8" stroke="#2a2a30" stroke-width="3" stroke-linecap="round"/>'
    # calculator
    top += rr(156, 742, 40, 32, '#3a3a42', 3) + rr(160, 746, 32, 9, '#b8c8a8', 1) + ''.join(rr(161 + (k % 4) * 8, 758 + (k // 4) * 5.5, 6, 4, '#e8e2d4' if k % 4 < 3 else '#e2733a', 1) for k in range(12))
    # pen cup
    top += rr(214, 736, 22, 38, '#2f6aa8', 3) + rr(214, 736, 7, 38, '#5a8cc8', 3) + f'<path d="M219,736 l-4,-22 M226,736 l2,-26 M232,736 l6,-18" stroke="#2a2a30" stroke-width="2.5" stroke-linecap="round"/><circle cx="215" cy="714" r="2" fill="#c8423a"/>'
    # small desk fan (Thai shop staple)
    top += '<g>' + rr(436, 760, 52, 12, '#e8e2d4', 4) + rr(456, 724, 10, 38, '#d8d0c0') + '<circle cx="461" cy="712" r="30" fill="#bcd8e2" opacity=".85"/><circle cx="461" cy="712" r="30" fill="none" stroke="#e8e2d4" stroke-width="3"/>'
    top += ''.join(f'<path d="M461,712 L{461+26*__import__("math").cos(a):.1f},{712+26*__import__("math").sin(a):.1f}" stroke="#e8e2d4" stroke-width="1.2"/>' for a in [k * 0.524 for k in range(12)])
    top += '<path d="M461,712 l-14,-18 a22,22 0 0 1 16,-4 Z" fill="#8fb2ac" opacity=".8"/><path d="M461,712 l22,6 a22,22 0 0 1 -6,15 Z" fill="#8fb2ac" opacity=".8"/><path d="M461,712 l-8,20 a22,22 0 0 1 -14,-10 Z" fill="#8fb2ac" opacity=".8"/><circle cx="461" cy="712" r="6" fill="#e8e2d4"/></g>'
    # basket of electrical tape
    top += f'<path d="M300,744 l84,0 l-6,30 l-72,0 Z" fill="#5ac08a"/><path d="M300,744 l84,0 l0,5 l-84,0 Z" fill="#82dcaa"/>' + ''.join(f'<circle cx="{316+k*16}" cy="742" r="8" fill="{c}"/><circle cx="{316+k*16}" cy="742" r="3" fill="#f2e6cc"/>' for k, c in enumerate(('#2a2a30', '#c8423a', '#2f6aa8', '#e8c24a', '#3a8a5a')))
    fg += f'<g filter="url(#dsh)">{top}</g>'
    # sun spill on the counter top from the left
    fg += '<path d="M0,770 L260,770 L230,786 L0,786 Z" fill="#fff2cc" opacity=".4"/>'
    s += fg

    # dust in the sunbeam
    s += dust(52, (20, 120, 340, 600), 34, '#fff4dc')
    s += '<rect width="540" height="960" fill="#ffa850" opacity=".08" style="mix-blend-mode:multiply"/>'
    return s
