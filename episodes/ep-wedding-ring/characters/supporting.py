# Odd Hours · ตอนงานแต่ง · ตัวละครรอง 9 ตัว (ร่างแรก)
# หน้าตรง ไม่มีเส้นขอบ เงาเป็นบล็อกสี แสงจากซ้าย พื้นหลัง #1b1f2b ตามมาตรฐานช่อง
# รัน: python3 supporting.py -> supporting.html
import math
from wedding_chars import CSS as BASE_CSS

def fx(v): return f'{v:.1f}'

# ================================================================ ชิ้นส่วนใบหน้า
F_FACES = {
    'oval': 'M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,37 0,40 C -13,37 -28,22 -30,6 Z',
    'long': 'M -30,-16 C -30,-46 30,-46 30,-16 L 29,4 C 27,22 12,41 0,45 C -12,41 -27,22 -29,4 Z',
    'round': 'M -32,-12 C -32,-44 32,-44 32,-12 L 31,8 C 29,24 14,37 0,39 C -14,37 -29,24 -31,8 Z',
    'mature': 'M -31,-14 C -31,-44 31,-44 31,-14 L 30,6 C 28,22 14,39 0,42 C -14,39 -28,22 -30,6 Z',
}
M_FACES = {
    'normal': 'M -32,-14 C -32,-46 32,-46 32,-14 L 32,4 C 31,18 18,36 0,43 C -18,36 -31,18 -32,4 Z',
    'round': 'M -33,-12 C -33,-46 33,-46 33,-12 L 32,8 C 30,24 16,38 0,40 C -16,38 -30,24 -32,8 Z',
    'square': 'M -33,-14 C -33,-46 33,-46 33,-14 L 33,10 C 32,24 22,38 0,43 C -22,38 -32,24 -33,10 Z',
}

def shade_face(cid, sk):
    base, s, d, l = sk
    return (f'<g clip-path="url(#{cid})">'
            f'<path d="M 16,-34 C 30,-28 34,-14 32,4 C 30,22 14,38 0,41 C 11,32 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{s}"/>'
            f'<path d="M 25,-24 L 34,-24 L 34,10 C 32,6 30,0 27,-8 Z" fill="{d}"/>'
            f'<path d="M -34,-24 L -23,-24 L -26,-8 L -34,-6 Z" fill="{l}" opacity=".6"/>'
            f'<path d="M -33,-12 C -33,-30 -28,-38 -21,-41 C -27,-32 -28,-20 -28,-10 L -27,6 C -26,18 -20,28 -14,34 C -22,30 -28,20 -30,6 Z" fill="{l}"/>'
            f'<path d="M 2,4 L 5.6,15.4 L 1,16.6 Z" fill="{d}" opacity=".7"/></g>')

def eyes(cid, iris='#4e2e22', h=1.0, lift=0.0, wing=4.6, lashes=2, catch=True, crease=True, smoky=None, heavy=0.0, under=False, lash_col='#1c1214', r=4.7):
    """ตาทั้งสองข้าง สร้างจากพารามิเตอร์: ความสูง หางตาเชิด ปีกอายไลเนอร์ ขนตา ประกาย ชั้นตา อายแชโดว์ เปลือกตาหนัก"""
    o = []
    for sgn, tag in ((-1, 'L'), (1, 'R')):
        def X(x): return x * -sgn  # base coords are for the left eye (negative x)
        ox, oy = -21.6, -1.8 - lift
        ix, iy = -4.8, -1.4
        c1 = (-18.2, -7.8 * h - lift * .4); c2 = (-8.6, -8 * h); c3 = (-8.6, 2.2 * h); c4 = (-17.6, 2.4 * h - lift * .3)
        shape = f'M {fx(X(ox))},{fx(oy)} C {fx(X(c1[0]))},{fx(c1[1])} {fx(X(c2[0]))},{fx(c2[1])} {fx(X(ix))},{fx(iy)} C {fx(X(c3[0]))},{fx(c3[1])} {fx(X(c4[0]))},{fx(c4[1])} {fx(X(ox))},{fx(oy)} Z'
        clip = f'{cid}e{tag}'
        o.append(f'<clipPath id="{clip}"><path d="{shape}"/></clipPath>')
        if smoky:
            o.append(f'<path d="M {fx(X(ox - 1))},{fx(oy - 1)} C {fx(X(c1[0]))},{fx(c1[1] - 5)} {fx(X(c2[0]))},{fx(c2[1] - 5)} {fx(X(ix + .4))},{fx(iy - 2)} C {fx(X(c2[0]))},{fx(c2[1] - 1)} {fx(X(c1[0]))},{fx(c1[1] - 1)} {fx(X(ox - 1))},{fx(oy - 1)} Z" fill="{smoky}" opacity=".75"/>')
        o.append(f'<path d="{shape}" fill="{"#fbf4ec" if sgn < 0 else "#f1e6da"}"/>')
        cx = X(-13); cy = -1.2
        o.append(f'<g clip-path="url(#{clip})"><circle cx="{fx(cx)}" cy="{fx(cy)}" r="{r}" fill="{iris}"/>'
                 f'<path d="M {fx(cx - r)},{fx(cy)} A{r},{r} 0 0,1 {fx(cx + r)},{fx(cy)} Z" fill="#000" opacity=".28"/>'
                 f'<circle cx="{fx(cx)}" cy="{fx(cy)}" r="{fx(r * .46)}" fill="#120808"/>')
        if catch:
            o.append(f'<circle cx="{fx(cx - 1.7 * -sgn * -1 if False else cx + (-1.7 if sgn < 0 else -1.7))}" cy="{fx(cy - 1.8)}" r="1.4" fill="#fff"/><circle cx="{fx(cx + 1.7)}" cy="{fx(cy + 1.9)}" r=".7" fill="#ffe6cc"/>')
        if heavy:
            o.append(f'<path d="M {fx(X(ox - 2))},{fx(oy - 6)} L {fx(X(ix + 2))},{fx(iy - 6)} L {fx(X(ix))},{fx(iy - 6 + heavy * 5)} C {fx(X(c2[0]))},{fx(c2[1] + heavy * 5)} {fx(X(c1[0]))},{fx(c1[1] + heavy * 5)} {fx(X(ox))},{fx(oy - 1 + heavy * 3)} Z" fill="{lash_col}" opacity=".0"/>')
        o.append('</g>')
        # lash line follows the top of the eye, heavier lid pulls it down
        dy = heavy * 2.6
        lash = (f'M {fx(X(ox - 1.2))},{fx(oy + .2)} C {fx(X(c1[0]))},{fx(c1[1] - 1.4 + dy)} {fx(X(c2[0]))},{fx(c2[1] - 1.4 + dy)} {fx(X(ix + .9))},{fx(iy - .2)} '
                f'L {fx(X(ix - .1))},{fx(iy + .7)} C {fx(X(c2[0]))},{fx(c2[1] + 1.6 + dy * 1.4)} {fx(X(c1[0] + .4))},{fx(c1[1] + 1.8 + dy * 1.4)} {fx(X(ox + .2))},{fx(oy + 1.2)} Z')
        o.append(f'<path d="{lash}" fill="{lash_col}"/>')
        if wing:
            o.append(f'<path d="M {fx(X(ox + .2))},{fx(oy + .2)} L {fx(X(ox - wing))},{fx(oy - wing * .7)} L {fx(X(ox + .6))},{fx(oy + 1.8)} Z" fill="{lash_col}"/>')
        for k in range(lashes):
            t = .25 + k * .18
            bx = ox + (ix - ox) * t * .7; by = c1[1] - .6 + dy + k * .2
            o.append(f'<path d="M {fx(X(bx))},{fx(by)} L {fx(X(bx - 1.6))},{fx(by - 2.8)}" stroke="{lash_col}" stroke-width="1" stroke-linecap="round"/>')
        if crease:
            o.append(f'<path d="M {fx(X(ox + 1))},{fx(oy - 4.6)} C {fx(X(c1[0]))},{fx(c1[1] - 3)} {fx(X(c2[0]))},{fx(c2[1] - 2.6)} {fx(X(ix - 1.2))},{fx(iy - 5.6)}" fill="none" stroke="#c28a76" stroke-width=".9" opacity=".8"/>')
        o.append(f'<path d="M {fx(X(-19.4))},{fx(2.4 * h)} C {fx(X(-15))},{fx(4.2 * h)} {fx(X(-10))},{fx(4.2 * h)} {fx(X(-6))},{fx(2.2 * h)}" fill="none" stroke="#b9806e" stroke-width=".8" opacity=".8"/>')
        if under:
            o.append(f'<path d="M {fx(X(-19))},{fx(5.6)} C {fx(X(-15))},{fx(7.6)} {fx(X(-10))},{fx(7.4)} {fx(X(-7))},{fx(5.8)}" fill="none" stroke="#a87868" stroke-width="1.2" opacity=".45"/>')
    return ''.join(o)

def brows(col, inner=-11.6, outer=-12.6, t=2.2, arch=1.0, sharp=False):
    o = []
    for sgn in (-1, 1):
        def X(x): return x * -sgn
        ox, ix = -22.6, -5.4
        if sharp:
            o.append(f'<path d="M {fx(X(ox))},{fx(outer)} L {fx(X(ix))},{fx(inner)} L {fx(X(ix + .4))},{fx(inner + t)} L {fx(X(ox + .6))},{fx(outer + t)} Z" fill="{col}"/>')
        else:
            o.append(f'<path d="M {fx(X(ox))},{fx(outer)} C {fx(X(-17))},{fx(outer - 1.6 - arch)} {fx(X(-10.6))},{fx(inner - 1.6 - arch * .6)} {fx(X(ix))},{fx(inner)} L {fx(X(ix - .4))},{fx(inner + t)} C {fx(X(-10.6))},{fx(inner + t - 1.6 - arch * .6)} {fx(X(-16.6))},{fx(outer + t - 1.6 - arch)} {fx(X(ox + .6))},{fx(outer + t)} Z" fill="{col}"/>')
    return ''.join(o)

def mouth(kind, col='#c86a74'):
    dk = '#8e3c4a'
    if kind == 'small':
        return (f'<path d="M -5.6,22.4 C -3.8,20.8 -1.6,20.4 0,21.4 C 1.6,20.4 3.8,20.8 5.6,22.4 Q 0,23.2 -5.6,22.4 Z" fill="{col}" opacity=".85"/>'
                f'<path d="M -5.6,22.4 Q 0,23.2 5.6,22.4 C 4.6,25.6 2.4,26.6 0,26.6 C -2.4,26.6 -4.6,25.6 -5.6,22.4 Z" fill="{col}"/>'
                f'<path d="M -5.6,22.4 Q 0,23.4 5.6,22.4" fill="none" stroke="{dk}" stroke-width=".8"/><ellipse cx="-1.4" cy="24.4" rx="1.6" ry=".7" fill="#fff" opacity=".45"/>')
    if kind == 'dark':
        return (f'<path d="M -7,22.6 C -4.4,20.4 -1.6,20.8 0,22 C 1.6,20.8 4.4,20.4 7,22.6 C 3,23.4 -3,23.4 -7,22.6 Z" fill="#5e1624"/>'
                f'<path d="M -7,22.6 C -3,23.4 3,23.4 7,22.6 C 5.6,27.6 -5.6,27.6 -7,22.6 Z" fill="{col}"/>'
                f'<path d="M -3,25.2 C -1,25.8 1,25.8 3,25.2" fill="none" stroke="#b44a5a" stroke-width="1.1" stroke-linecap="round"/>')
    if kind == 'polite':
        return (f'<path d="M -7,22.4 Q 0,25.6 7,22.4" fill="none" stroke="{dk}" stroke-width="1.6" stroke-linecap="round"/>'
                f'<path d="M -4,24.8 Q 0,26.6 4,24.8" fill="none" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>'
                f'<path d="M -12,20 Q -10,24 -8.6,25.6 M 12,20 Q 10,24 8.6,25.6" fill="none" stroke="#c2927e" stroke-width=".9" opacity=".7"/>')
    if kind == 'grin':
        return (f'<path d="M -8,21.4 Q 0,23 8,21.4 Q 6,29 0,29 Q -6,29 -8,21.4 Z" fill="#7a2c34"/>'
                f'<path d="M -6.6,22.2 Q 0,23.6 6.6,22.2 L 6,24 Q 0,25 -6,24 Z" fill="#ffffff"/>'
                f'<path d="M -3.6,27 Q 0,28.6 3.6,27 Q 0,26 -3.6,27 Z" fill="{col}"/>')
    if kind == 'sad':
        return (f'<path d="M -5.4,24 Q 0,22.4 5.4,24" fill="none" stroke="{dk}" stroke-width="1.5" stroke-linecap="round"/>'
                f'<path d="M -3,26 Q 0,27 3,26" fill="none" stroke="{col}" stroke-width="1.5" stroke-linecap="round"/>')
    if kind == 'blank':  # ยิ้มแข็ง เหมือนกันทุกคน
        return (f'<path d="M -8,22 Q 0,25.4 8,22" fill="none" stroke="{dk}" stroke-width="1.4" stroke-linecap="round"/>'
                f'<path d="M -8,22 l -.8,-1 M 8,22 l .8,-1" stroke="{dk}" stroke-width="1.2" stroke-linecap="round"/>')
    if kind == 'm_smile':
        return (f'<path d="M -7,22.6 Q 0,26.6 7,22.6" fill="none" stroke="#a05a50" stroke-width="1.7" stroke-linecap="round"/>'
                f'<path d="M -3.4,27 Q 0,28.2 3.4,27" fill="none" stroke="#e6b8a2" stroke-width="1.3" stroke-linecap="round"/>')
    if kind == 'm_stern':
        return (f'<path d="M -7,24 L 7,24" stroke="#8a4a44" stroke-width="1.8" stroke-linecap="round"/>'
                f'<path d="M -3.4,27.2 Q 0,28 3.4,27.2" fill="none" stroke="#d9a690" stroke-width="1.2" stroke-linecap="round"/>')
    if kind == 'm_sheepish':
        return (f'<path d="M -6,23.4 Q -1,25.6 5,22.4 L 7,21" fill="none" stroke="#a05a50" stroke-width="1.6" stroke-linecap="round"/>')
    return ''

def blush(col='#ee8c86', op=.45, rx=6.6):
    return f'<ellipse cx="-18" cy="12.4" rx="{rx}" ry="3.2" fill="{col}" opacity="{op}"/><ellipse cx="18" cy="12.4" rx="{rx}" ry="3.2" fill="{col}" opacity="{op}"/>'

def neck(sk, wide=False):
    w = 9 if wide else 8
    return (f'<rect x="-{w}" y="20" width="{2 * w}" height="38" fill="{sk[1]}"/>'
            f'<path d="M -{w},26 L {w},26 L {w},45 Q 0,40 -{w},48 Z" fill="{sk[2]}"/>')

def ears(sk):
    return (f'<path d="M -31,-8 C -38,-10 -39,6 -32,10 Z" fill="{sk[1]}"/><path d="M 31,-8 C 38,-10 39,6 32,10 Z" fill="{sk[2]}"/>')

# ================================================================ ทรงผม (คืนค่า back, front)
def hair_bob_bangs(c, cl, cd):
    back = f'<path d="M -38,-6 C -40,-44 -22,-63 0,-63 C 22,-63 40,-44 38,-6 L 41,36 L -41,36 Z" fill="{c}"/>'
    front = (f'<path d="M -37,-6 C -39,-44 -21,-62 0,-62 C 21,-62 39,-44 37,-6 L 33,-6 L 33,-15 L -33,-15 L -33,-6 Z" fill="{c}"/>'
             f'<path d="M -30,-40 C -22,-54 -10,-59 0,-59 C -10,-55 -20,-48 -26,-34 Z" fill="{cl}"/>'
             f'<path d="M -33,-15 L 33,-15 L 33,-13 L -33,-13 Z" fill="{cd}"/>'
             f'<path d="M -38,-8 L -29,-8 L -28,36 L -41,36 Z" fill="{c}"/><path d="M 38,-8 L 29,-8 L 28,36 L 41,36 Z" fill="{cd}"/>'
             f'<path d="M -37,0 L -35,0 L -35,34 L -38,34 Z" fill="{cl}"/>')
    return back, front

def hair_long_tucked(c, cl, cd, sk):
    back = (f'<path d="M -38,-6 C -40,-44 -22,-63 0,-63 C 22,-63 40,-44 38,-6 L 44,150 L 32,156 L 20,150 L 8,156 L -4,150 L -16,156 L -28,150 L -44,150 Z" fill="{c}"/>'
            f'<path d="M -38,-6 L -44,150 L -38,152 L -33,0 Z" fill="{cl}"/>')
    front = (f'<path d="M -38,-6 C -40,-44 -22,-63 0,-63 C 22,-63 40,-44 38,-6 L 31,-6 C 29,-24 16,-38 1,-41 L 0,-41 L -1,-41 C -16,-38 -29,-24 -31,-6 Z" fill="{c}"/>'
             f'<path d="M -1,-41 C -14,-46 -26,-40 -32,-28 C -26,-38 -14,-43 -1,-41 Z M -26,-48 C -18,-56 -8,-59 -1,-59 C -8,-55 -16,-52 -21,-44 Z" fill="{cl}"/>'
             f'<path d="M 1,-41 C 14,-46 26,-40 32,-28 C 26,-38 14,-43 1,-41 Z" fill="{cd}"/>'
             # her right side: straight panel over the shoulder
             f'<path d="M -38,-8 L -28,-8 C -26,30 -26,80 -24,140 L -31,148 L -40,140 C -41,80 -40,30 -38,-8 Z" fill="{c}"/>'
             f'<path d="M -36,4 L -33.6,4 C -34,50 -34,100 -33,134 L -35.4,136 C -36,100 -36.4,50 -36,4 Z" fill="{cl}"/>'
             # her left side: tucked behind the ear, falls behind the shoulder
             f'<path d="M 31,-8 C 34,-14 37,-10 38,-6 L 40,30 L 33,24 C 33,10 32,0 31,-8 Z" fill="{cd}"/>'
             f'<path d="M 30,-6 C 36,-8 37,6 31,10 Z" fill="{sk[1]}"/>')
    return back, front

def hair_mom(c, gray):
    back = (f'<circle cx="0" cy="-54" r="17" fill="{c}"/>'
            f'<path d="M -36,-6 C -38,-44 -20,-62 0,-62 C 20,-62 38,-44 36,-6 L 34,10 L -34,10 Z" fill="{c}"/>')
    front = (f'<path d="M -36,-6 C -38,-44 -20,-62 0,-62 C 20,-62 38,-44 36,-6 L 31,-8 C 28,-24 16,-34 -2,-37 C -16,-34 -27,-24 -31,-8 Z" fill="{c}"/>'
             f'<path d="M -2,-37 C 14,-40 28,-30 33,-14 C 26,-26 14,-34 -2,-37 Z M -24,-44 C -16,-52 -6,-56 4,-56" fill="none" stroke="{gray}" stroke-width="2.2"/>'
             f'<path d="M -30,-30 C -26,-40 -18,-46 -8,-49" fill="none" stroke="{gray}" stroke-width="1.6"/>'
             f'<path d="M -31,-8 C -33,2 -32,8 -30,12 L -33,10 C -35,2 -34,-4 -33,-8 Z M 31,-8 C 33,2 32,8 30,12 L 33,10 C 35,2 34,-4 33,-8 Z" fill="{c}"/>')
    return back, front

def hair_low_bun(c, cl, cd):
    back = (f'<ellipse cx="0" cy="34" rx="22" ry="12" fill="{c}"/>'
            f'<path d="M -36,-6 C -38,-44 -20,-62 0,-62 C 20,-62 38,-44 36,-6 L 33,26 L -33,26 Z" fill="{c}"/>')
    front = (f'<path d="M -36,-6 C -38,-44 -20,-62 0,-62 C 20,-62 38,-44 36,-6 L 31,-8 C 29,-26 16,-38 1,-40 L 0,-40 L -1,-40 C -16,-38 -29,-26 -31,-8 Z" fill="{c}"/>'
             f'<path d="M -1,-40 C -12,-48 -24,-46 -30,-36 C -24,-44 -12,-46 -1,-40 Z" fill="{cl}"/>'
             f'<path d="M 1,-40 C 12,-48 24,-46 30,-36 C 24,-44 12,-46 1,-40 Z" fill="{cd}"/>'
             f'<path d="M -31,-8 C -33,6 -32,16 -29,24 L -33,24 C -35,12 -34,0 -33,-8 Z M 31,-8 C 33,6 32,16 29,24 L 33,24 C 35,12 34,0 33,-8 Z" fill="{c}"/>')
    return back, front

def hair_wavy_shoulder(c, cl, cd, clip='#e8c6c8'):
    waves = ''.join(f'<path d="M {s * 34},-4 C {s * 46},14 {s * 38},34 {s * 46},52 C {s * 48},60 {s * 42},66 {s * 36},66 L {s * 22},66 C {s * 28},48 {s * 22},30 {s * 26},6 Z" fill="{c if s < 0 else cd}"/>'
                    f'<path d="M {s * 40},8 C {s * 44},22 {s * 38},36 {s * 44},50" fill="none" stroke="{cl}" stroke-width="2.2"/>' for s in (-1, 1))
    back = f'<path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 40,40 L -40,40 Z" fill="{c}"/>{waves}'
    front = (f'<path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 32,-6 C 30,-24 18,-36 -8,-38 C -18,-34 -28,-24 -32,-6 Z" fill="{c}"/>'
             f'<path d="M -8,-38 C 10,-38 26,-30 32,-12 C 22,-26 8,-32 -8,-38 Z" fill="{cd}"/>'
             f'<path d="M -28,-44 C -20,-55 -8,-59 2,-58 C -8,-54 -18,-48 -24,-40 Z" fill="{cl}"/>'
             f'<path d="M -32,-8 C -36,8 -34,22 -29,32 C -32,20 -32,6 -30,-6 Z M 32,-8 C 36,8 34,22 29,32 C 32,20 32,6 30,-6 Z" fill="{c}"/>'
             f'<path d="M 18,-42 l 10,4 l -2,4 l -10,-4 Z" fill="{clip}"/>')
    return back, front

def hair_tight_bun(c, cl):
    back = (f'<circle cx="0" cy="-64" r="15" fill="{c}"/>'
            f'<path d="M -35,-6 C -37,-44 -19,-62 0,-62 C 19,-62 37,-44 35,-6 L 32,6 L -32,6 Z" fill="{c}"/>')
    front = (f'<path d="M -35,-6 C -37,-44 -19,-62 0,-62 C 19,-62 37,-44 35,-6 L 31,-12 C 29,-28 16,-39 0,-40 C -16,-39 -29,-28 -31,-12 Z" fill="{c}"/>'
             f'<path d="M 0,-40 L 0,-61 M -20,-50 C -12,-56 -4,-58 0,-58" fill="none" stroke="{cl}" stroke-width="1.6"/>')
    return back, front

def mhair_curtain(c, cl, cd):
    return (f'<path d="M -35,-6 C -40,-38 -26,-62 0,-63 C 26,-62 40,-38 35,-6 L 32,-12 C 30,-22 22,-30 12,-32 C 8,-26 4,-22 0,-22 C -4,-22 -8,-26 -12,-32 C -22,-30 -30,-22 -32,-12 Z" fill="{c}"/>'
            f'<path d="M -12,-32 C -18,-26 -22,-18 -24,-8 C -18,-16 -10,-22 -2,-24 Z" fill="{c}"/><path d="M 12,-32 C 18,-26 22,-18 24,-8 C 18,-16 10,-22 2,-24 Z" fill="{cd}"/>'
            f'<path d="M -26,-46 C -18,-56 -4,-60 8,-58 C -4,-54 -14,-48 -21,-38 Z" fill="{cl}"/>'
            f'<path d="M -35,-6 L -33,-22 L -30,-8 Z M 35,-6 L 33,-22 L 31,-8 Z" fill="{c}"/>')

def mhair_buzz(c, cl):
    return (f'<path d="M -33,-14 C -34,-44 -18,-56 0,-56 C 18,-56 34,-44 33,-14 L 31,-18 C 30,-34 18,-44 0,-44 C -18,-44 -30,-34 -31,-18 Z" fill="{c}"/>'
            f'<path d="M -33,-14 C -34,-44 -18,-56 0,-56 C 18,-56 34,-44 33,-14" fill="none" stroke="{c}" stroke-width="4"/>'
            f'<path d="M -24,-46 C -14,-53 -2,-55 6,-54" fill="none" stroke="{cl}" stroke-width="2"/>')

def mhair_slick(c, gray):
    return (f'<path d="M -34,-8 C -38,-42 -22,-62 0,-62 C 22,-62 38,-42 34,-8 L 31,-16 C 28,-30 16,-38 0,-39 C -16,-38 -28,-30 -31,-16 Z" fill="{c}"/>'
            f'<path d="M -30,-34 C -20,-50 -4,-54 10,-52 M -24,-28 C -14,-42 2,-46 16,-44 M -18,-22 C -8,-34 6,-38 20,-36" fill="none" stroke="#3a3840" stroke-width="1.2"/>'
            f'<path d="M -34,-8 L -31,-16 L -30,-4 Z M 34,-8 L 31,-16 L 30,-4 Z" fill="{gray}"/>')

# ================================================================ ประกอบหัว
def fhead(cid, sk, face, eye_kw, brow_kw, mouth_kind, lip, hair, blush_op=.4, extra='', brow_col='#2c1c1a', mole=None):
    back, front = hair
    fp = F_FACES[face]
    head = (f'<g transform="scale(.87 1.03)"><clipPath id="{cid}"><path d="{fp}"/></clipPath>{neck(sk)}<path d="{fp}" fill="{sk[0]}"/>{shade_face(cid, sk)}'
            f'{blush(op=blush_op, rx=5.4) if blush_op else ""}{brows(brow_col, **brow_kw)}{eyes(cid, **eye_kw)}'
            f'{mouth(mouth_kind, lip)}{f"<circle cx=\"{mole[0]}\" cy=\"{mole[1]}\" r=\"1\" fill=\"#4a2c24\"/>" if mole else ""}{front}{extra}</g>')
    return f'<g transform="scale(.87 1.03)">{back}</g>', head

def mhead(cid, sk, face, eye_kw, brow_kw, mouth_kind, hair_front, extra='', back=''):
    fp = M_FACES[face]
    head = (f'<g transform="scale(.88 1.03)">{ears(sk)}<clipPath id="{cid}"><path d="{fp}"/></clipPath>{neck(sk, True)}<path d="{fp}" fill="{sk[0]}"/>{shade_face(cid, sk)}'
            f'{brows("#151318", sharp=True, **brow_kw)}{eyes(cid, **eye_kw)}{mouth(mouth_kind)}{hair_front}{extra}</g>')
    return back, head

# ================================================================ ตัวผู้หญิง (พิกัดเดียวกับตะวัน เท้าราว y 462)
def fbody(sk, top, skirt, hem=456, flare=60, neckline='high', sleeves='none', sleeve_col=None, shoes='#1c1a20', extra='', legs=True):
    base, s, d, l = sk
    tb, tl, ts = top
    kb, kl, ks = skirt
    o = []
    if hem < 440 and legs:
        o.append(f'<path d="M -22,{hem - 4} L -10,{hem - 4} L -11,446 L -21,446 Z" fill="{base}"/><path d="M 10,{hem - 4} L 22,{hem - 4} L 21,446 L 11,446 Z" fill="{s}"/>')
    o.append(f'<path d="M -24,444 L -8,444 L -6,456 L -26,456 Z M 8,444 L 24,444 L 26,456 L 6,456 Z" fill="{shoes}"/>')
    # skirt
    o.append(f'<path d="M -33,146 L 33,146 C {flare * .6},{(146 + hem) / 2} {flare * .9},{hem - 30} {flare},{hem} L {-flare},{hem} C {-flare * .9},{hem - 30} {-flare * .6},{(146 + hem) / 2} -33,146 Z" fill="{kb}"/>')
    o.append(f'<path d="M -33,146 L -14,146 C {-flare * .3},{(146 + hem) / 2} {-flare * .5},{hem - 30} {-flare * .55},{hem} L {-flare},{hem} C {-flare * .9},{hem - 30} {-flare * .6},{(146 + hem) / 2} -33,146 Z" fill="{kl}"/>')
    o.append(f'<path d="M 16,146 L 33,146 C {flare * .6},{(146 + hem) / 2} {flare * .9},{hem - 30} {flare},{hem} L {flare * .55},{hem} C {flare * .45},{hem - 30} {flare * .3},{(146 + hem) / 2} 16,146 Z" fill="{ks}"/>')
    # shoulders skin + arms
    o.append(f'<path d="M -10,50 L 10,50 C 22,51 34,55 39,64 L 37,100 L -37,100 L -39,64 C -34,55 -22,51 -10,50 Z" fill="{base}"/>')
    o.append(f'<path d="M 18,52 C 30,55 37,58 39,64 L 37,100 L 24,100 C 25,80 23,64 18,52 Z" fill="{s}"/>')
    o.append(f'<path d="M -38,60 C -46,64 -49,80 -49,100 L -51,212 L -40,212 L -38,110 Z" fill="{base}"/><path d="M -46,92 C -47,100 -48,110 -48,120 L -49,212 L -46,212 L -45,120 Z" fill="{l}"/>')
    o.append(f'<path d="M 38,60 C 46,64 49,80 49,100 L 51,212 L 40,212 L 38,110 Z" fill="{s}"/><path d="M 46,92 C 48,100 49,110 49,120 L 51,212 L 47,212 Z" fill="{d}"/>')
    o.append(f'<path d="M -51,210 L -40,210 C -39,224 -41,236 -46,238 C -51,238 -53,226 -51,210 Z" fill="{base}"/><path d="M 51,210 L 40,210 C 39,224 41,236 46,238 C 51,238 53,226 51,210 Z" fill="{s}"/>')
    # sleeves
    sc = sleeve_col or top
    if sleeves in ('short', 'three', 'long', 'sheer'):
        end = {'short': 96, 'three': 170, 'long': 212, 'sheer': 212}[sleeves]
        op = ' opacity=".55"' if sleeves == 'sheer' else ''
        o.append(f'<path d="M -40,60 C -48,64 -51,80 -51,100 L -52,{end} L -39,{end} L -37,96 Z" fill="{sc[0]}"{op}/><path d="M -49,92 L -52,{end} L -48,{end} L -46,96 Z" fill="{sc[1]}"{op}/>')
        o.append(f'<path d="M 40,60 C 48,64 51,80 51,100 L 52,{end} L 39,{end} L 37,96 Z" fill="{sc[2]}"{op}/>')
    # bodice
    if neckline == 'high':
        bod = 'M -14,50 C -10,56 10,56 14,50 C 26,52 36,56 40,64 L 37,150 L -37,150 L -40,64 C -36,56 -26,52 -14,50 Z'
    elif neckline == 'v':
        bod = 'M -14,50 L 0,86 L 14,50 C 26,52 36,56 40,64 L 37,150 L -37,150 L -40,64 C -36,56 -26,52 -14,50 Z'
    elif neckline == 'square':
        bod = 'M -30,72 L 30,72 L 34,66 C 36,62 38,62 39,64 L 37,150 L -37,150 L -39,64 C -38,62 -36,62 -34,66 Z'
    else:  # sweetheart
        bod = 'M -36,84 C -32,72 -16,70 -6,79 Q 0,84 6,79 C 16,70 32,72 36,84 L 31,150 L -31,150 Z'
    o.append(f'<path d="{bod}" fill="{tb}"/>')
    o.append(f'<clipPath id="bod{abs(hash((tb, neckline, kb))) % 9999}"><path d="{bod}"/></clipPath>')
    cid = f'bod{abs(hash((tb, neckline, kb))) % 9999}'
    o.append(f'<g clip-path="url(#{cid})"><rect x="-42" y="40" width="18" height="120" fill="{tl}"/><rect x="22" y="40" width="20" height="120" fill="{ts}"/></g>')
    o.append(extra)
    return ''.join(o)

# ================================================================ ตัวผู้ชาย (พิกัดเดียวกับเจม เท้าราว y 488)
def mbody(sk, pants, top, shirt='#f7f5f1', tie=None, lapels=True, rolled=False, shoes='#16161c', vest=None, extra=''):
    base, s, d, l = sk
    pb, pl, pd = pants; jb, jl, jd = top
    o = [f'<path d="M -40,226 L 40,226 L 43,300 L 37,470 L 9,470 L 2,292 L -2,292 L -9,470 L -37,470 L -43,300 Z" fill="{pb}"/>',
         f'<path d="M -40,226 L -24,226 L -27,300 L -25,470 L -37,470 L -43,300 Z" fill="{pl}"/>',
         f'<path d="M 22,232 L 40,226 L 43,300 L 37,470 L 26,470 C 28,380 26,300 22,232 Z" fill="{pd}"/>',
         f'<path d="M -40,468 L -8,468 C -4,476 -6,486 -10,488 L -44,488 C -48,484 -46,472 -40,468 Z" fill="{shoes}"/>',
         f'<path d="M 40,468 L 8,468 C 4,476 6,486 10,488 L 44,488 C 48,484 46,472 40,468 Z" fill="{shoes}"/>']
    end = 160 if rolled else 226
    o.append(f'<path d="M -50,68 C -58,76 -60,100 -60,120 L -58,{end} L -44,{end} L -44,118 Z" fill="{jl}"/>')
    o.append(f'<path d="M 50,68 C 58,76 60,100 60,120 L 58,{end} L 44,{end} L 44,118 Z" fill="{jd}"/>')
    if rolled:
        o.append(f'<rect x="-60" y="{end - 8}" width="17" height="10" rx="3" fill="{jb}"/><rect x="43" y="{end - 8}" width="17" height="10" rx="3" fill="{jd}"/>')
        o.append(f'<path d="M -58,{end + 2} L -45,{end + 2} L -44,228 L -58,228 Z" fill="{base}"/><path d="M 58,{end + 2} L 45,{end + 2} L 44,228 L 58,228 Z" fill="{s}"/>')
    else:
        o.append(f'<rect x="-59" y="222" width="15" height="7" fill="{shirt}"/><rect x="44" y="222" width="15" height="7" fill="#d8d4ce"/>')
    o.append(f'<path d="M -59,229 L -44,229 C -43,244 -45,258 -51,260 C -57,260 -60,246 -59,229 Z" fill="{base}"/>')
    o.append(f'<path d="M 59,229 L 44,229 C 43,244 45,258 51,260 C 57,260 60,246 59,229 Z" fill="{s}"/>')
    o.append(f'<path d="M -12,49 L 12,49 C 30,51 46,56 50,68 L 50,236 L -50,236 L -50,68 C -46,56 -30,51 -12,49 Z" fill="{jb}"/>')
    o.append(f'<path d="M -50,68 C -46,56 -30,51 -18,50 C -26,80 -30,130 -30,236 L -50,236 Z" fill="{jl}"/>')
    o.append(f'<path d="M 22,50 C 34,53 46,58 50,68 L 50,236 L 32,236 C 32,160 30,90 22,50 Z" fill="{jd}"/>')
    if lapels:
        o.append(f'<path d="M -12,49 L 12,49 L 0,148 Z" fill="{shirt}"/><path d="M 4,52 L 12,49 L 0,148 Z" fill="#d8d4ce"/>')
        if tie:
            o.append(f'<path d="M -4,58 L 4,58 L 6,66 L 3,138 L 0,144 L -3,138 L -6,66 Z" fill="{tie[0]}"/><path d="M 0,58 L 4,58 L 6,66 L 3,138 L 0,144 Z" fill="{tie[1]}"/><path d="M -4,56 L 4,56 L 5,62 L -5,62 Z" fill="{tie[0]}"/>')
        o.append(f'<path d="M -12,49 L 0,148 L -6,150 L -26,96 L -18,90 L -24,62 Z" fill="{jl}"/><path d="M 12,49 L 0,148 L 6,150 L 26,96 L 18,90 L 24,62 Z" fill="{jd}"/>')
        o.append(f'<circle cx="0" cy="166" r="2.4" fill="#0e0e12"/><circle cx="0" cy="188" r="2.4" fill="#0e0e12"/>')
    else:
        o.append(f'<path d="M -12,49 L 0,64 L 12,49 L 8,48 L 0,58 L -8,48 Z" fill="{jd}"/><path d="M -6,49 L 0,58 L 6,49 Z" fill="{base}"/>')
        o.append(f'<path d="M 0,64 L 0,236" stroke="{jd}" stroke-width="1"/>' + ''.join(f'<circle cx="0" cy="{y}" r="1.6" fill="{jd}"/>' for y in (80, 110, 140, 170, 200)))
    if vest:
        vb, vl, vd = vest
        o.append(f'<path d="M -40,60 L -12,52 L -2,236 L -46,236 L -46,70 Z" fill="{vb}"/><path d="M -40,60 L -30,57 L -36,236 L -46,236 L -46,70 Z" fill="{vl}"/>')
        o.append(f'<path d="M 40,60 L 12,52 L 2,236 L 46,236 L 46,70 Z" fill="{vd}"/>')
        for (x, y) in ((-34, 130), (-34, 180), (18, 130), (18, 180)):
            o.append(f'<rect x="{x}" y="{y}" width="16" height="18" fill="{vd if x > 0 else vb}" stroke="{vd}" stroke-width="1.2"/><path d="M {x},{y + 5} h16" stroke="{vd}" stroke-width="1.2"/>')
    o.append(extra)
    return ''.join(o)

# ================================================================ ตัวละคร
SK_PALE = ('#f1d8cc', '#dcb7aa', '#c49688', '#fbeae2')
SK_FAIR = ('#fbe2cf', '#efc3a8', '#d9a089', '#fff4ea')
SK_WARM = ('#f4cfae', '#e3ae8a', '#c98a68', '#fde6d0')
SK_TAN = ('#e8b98e', '#d49c70', '#b47c54', '#f6d4b4')
SK_MALE = ('#f6dcc8', '#e6bca4', '#c99a84', '#fff0e4')
SK_MALE_T = ('#ecc4a2', '#d8a682', '#ba8664', '#f8dcc4')
SILVER, SILVER_L = '#c3c8cf', '#f4f6f9'

def c_woman_black():
    hb, hf = hair_long_tucked('#0e0b10', '#34303e', '#060508', SK_PALE)
    hat = ('<ellipse cx="-18" cy="-52" rx="15" ry="5.4" fill="#0c0b10" transform="rotate(-16 -18 -52)"/>'
           '<path d="M -30,-56 C -40,-70 -30,-78 -18,-72" fill="none" stroke="#2a2832" stroke-width="2"/>'
           '<path d="M -32,-56 L 6,-56 L 4,-30 C -8,-26 -22,-28 -32,-34 Z" fill="url(#net)" opacity=".7"/>')
    ear = (f'<circle cx="31.4" cy="10" r="1.4" fill="{SILVER_L}"/><path d="M 31.4,11.4 V16" stroke="#c3c8cf" stroke-width=".8"/>'
           '<path d="M 31.4,16 l 2.4,3.6 l -2.4,6.4 l -2.4,-6.4 Z" fill="#dde6f6"/><path d="M 31.4,16 l 2.4,3.6 l -2.4,6.4 Z" fill="#aebbd4"/>')
    back, head = fhead('wbf', SK_PALE, 'long', dict(iris='#2a1814', lift=1.1, wing=5.4, lashes=2, smoky='#8a6474', r=4.6),
                       dict(inner=-11.4, outer=-13, arch=1.0, t=2), 'small', '#8e2236', (hb, hf), blush_op=.15, extra=hat + ear, brow_col='#141016', mole=None)
    gloves = ('<path d="M -51,150 L -40,150 L -40,212 L -51,212 Z M 51,150 L 40,150 L 40,212 L 51,212 Z" fill="#141218"/>'
              '<path d="M -51,210 L -40,210 C -39,224 -41,236 -46,238 C -51,238 -53,226 -51,210 Z M 51,210 L 40,210 C 39,224 41,236 46,238 C 51,238 53,226 51,210 Z" fill="#141218"/>'
              '<path d="M -51,150 L -40,150 L -40,154 L -51,154 Z M 51,150 L 40,150 L 40,154 L 51,154 Z" fill="#2c2a34"/>'
              f'<rect x="41.5" y="224" width="7" height="2.6" rx="1.2" fill="{SILVER_L}"/><circle cx="45" cy="223.4" r="1.6" fill="#e8f0ff"/>')
    body = fbody(SK_PALE, ('#16141a', '#2a2832', '#0c0b10'), ('#16141a', '#2a2832', '#0c0b10'), hem=458, flare=48, neckline='square', extra=gloves)
    return 'ผู้หญิงชุดดำ', 'เจ้าสาวของปีที่แล้ว สวยแบบลึกลับ หน้าเรียว ผิวซีดเย็น ผมยาวตรงสีดำแสกกลาง ทัดหูข้างหนึ่ง ตาเฉี่ยวหางตาเชิด อายแชโดว์บาง ๆ ปากทรงสวยสีแดงเข้ม ต่างหูเพชรหยดน้ำ หมวกเล็กมีตาข่ายบางคลุมแค่หน้าผาก เดรสดำคอเหลี่ยมยาวถึงพื้น ถุงมือดำ และแหวนเงินแบบเดียวกับเจ้าสาวทับถุงมือ', 'f', back, head, body

def c_mother():
    hb, hf = hair_mom('#2a2226', '#a39ca6')
    pearls = ''.join(f'<circle cx="{fx(-11 + i * 2.2)}" cy="{fx(53 + 7 * math.sin(math.pi * i / 10))}" r="1.3" fill="#f6f2ea"/>' for i in range(11))
    ear = '<circle cx="-30" cy="11" r="2.2" fill="#f6f2ea"/><circle cx="30" cy="11" r="2.2" fill="#e2dcd2"/>'
    back, head = fhead('mmf', SK_WARM, 'mature', dict(iris='#3e2418', h=.88, wing=1.6, lashes=1, heavy=.4, under=True, r=4.3),
                       dict(inner=-11.4, outer=-12.4, arch=1.4, t=1.8), 'polite', '#b8606a', (hb, hf), blush_op=.25, extra=ear)
    lace = ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#b98ea6"/>' for x in range(-32, 34, 8) for y in range(70, 146, 10))
    clutch = '<rect x="-60" y="226" width="22" height="14" rx="3" fill="#4a2e44"/><rect x="-60" y="226" width="22" height="4" rx="2" fill="#c3c8cf"/>'
    body = fbody(SK_WARM, ('#9a6e8a', '#b48aa4', '#7a5270'), ('#5a2e4a', '#74405e', '#40203a'), hem=458, flare=40, neckline='high', sleeves='three',
                 sleeve_col=('#a07892', '#b894aa', '#80587a'), extra=lace + pearls + clutch)
    return 'แม่เจ้าบ่าว', 'อายุราว 55 ผมเกล้ามวยมีผมขาวแซม ตาเปลือกตาหนักนิด ๆ ยิ้มสุภาพแต่ตาไม่ยิ้มตาม ใส่เสื้อลูกไม้สีม่วงหม่นแขนสามส่วน ผ้าถุงยาวสีพลัม สร้อยไข่มุก ต่างหูมุก กระเป๋าคลัตช์', 'f', back, head, body

def c_staff():
    hb, hf = hair_low_bun('#1c1418', '#3a2e34', '#100a0c')
    back, head = fhead('stf', SK_TAN, 'oval', dict(iris='#3e2418', wing=1.6, lashes=1, r=4.6),
                       dict(inner=-14.4, outer=-11.6, arch=.4, t=2), 'sad', '#b26a6a', (hb, hf), blush_op=.3)
    tag = '<rect x="-30" y="92" width="18" height="6" rx="1" fill="#c3c8cf"/><rect x="-28" y="94" width="10" height="1.4" fill="#5a5a66"/>'
    vest = ('<path d="M -14,50 L 0,86 L 14,50 C 26,52 36,56 40,64 L 37,150 L -37,150 L -40,64 C -36,56 -26,52 -14,50 Z" fill="#232a44"/>'
            '<path d="M -40,64 C -36,56 -26,52 -16,51 L -12,58 L -24,150 L -37,150 Z" fill="#323a5a"/><path d="M -6,58 L 0,86 L 6,58 L 0,64 Z" fill="#f7f5f1"/>')
    body = fbody(SK_TAN, ('#f7f5f1', '#ffffff', '#d8d4ce'), ('#232a44', '#323a5a', '#161c30'), hem=320, flare=40, neckline='high', sleeves='long',
                 sleeve_col=('#f7f5f1', '#ffffff', '#d8d4ce'), extra=vest + tag)
    return 'พนักงานโรงแรม', 'อายุราว 26 ผมเกล้ามวยต่ำเรียบร้อย คิ้วหัวยกขึ้นแบบสงสาร ปากคว่ำนิด ๆ เสื้อเชิ้ตขาว เสื้อกั๊กกับกระโปรงสีกรมท่า ป้ายชื่อเงิน', 'f', back, head, body

def c_new_bride():
    hb, hf = hair_wavy_shoulder('#3a2620', '#6a4a3c', '#24160f', clip='#f6f2ec')
    veil = '<path d="M -26,-50 C -60,20 -92,180 -104,330 C -60,345 60,345 104,330 C 92,180 60,20 26,-50 Z" fill="#ffffff" opacity=".16"/>'
    crown = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in ((-24, -47, 3.4, '#fbf6ee'), (-12, -53, 3, '#f8dcd6'), (0, -55, 3.4, '#ffffff'), (12, -53, 3, '#f8dcd6'), (24, -47, 3.4, '#fbf6ee')))
    back, head = fhead('nbf', SK_FAIR, 'oval', dict(iris='#5a3a2c', h=1.08, wing=2.4, lashes=2, r=5.2),
                       dict(inner=-11.2, outer=-12, arch=1.2, t=1.8), 'small', '#e0707e', (hb, hf), blush_op=.55, extra=crown)
    lace = ''.join(f'<circle cx="{x + (y % 20) / 4}" cy="{y}" r="1.2" fill="#e6dcd0"/>' for x in range(-60, 62, 9) for y in range(160, 452, 14) if abs(x) < 30 + (y - 146) * .2)
    sleeves_sheer = '<path d="M -10,50 L 10,50 C 22,51 34,55 39,64 L 37,84 L -37,84 L -39,64 C -34,55 -22,51 -10,50 Z" fill="#ffffff" opacity=".35"/>'
    body = fbody(SK_FAIR, ('#f8f3ec', '#ffffff', '#ddd3c8'), ('#f5efe7', '#fffdf9', '#ddd3c8'), hem=456, flare=96, neckline='square', sleeves='sheer',
                 sleeve_col=('#ffffff', '#ffffff', '#e8e2da'), extra=sleeves_sheer + lace)
    return 'เจ้าสาวคนใหม่', 'เจ้าสาวในฉากหนึ่งปีต่อมา หน้ากลมหวาน ตาโต ผมน้ำตาลลอนประบ่า มงกุฎดอกไม้ ชุดลูกไม้คอเหลี่ยม แขนยาวซีทรู กระโปรงบานกว้างกว่าชุดเจ้าสาวคนแรก ทำให้แยกออกได้ทันทีในฉากจบ', 'f', back + veil, head, body

def c_bridesmaid():
    hb, hf = hair_wavy_shoulder('#2a1c18', '#5a3e34', '#1a100c')
    back, head = fhead('bmf', SK_WARM, 'oval', dict(iris='#4a2a1e', wing=2.6, lashes=2, r=4.8),
                       dict(inner=-12.6, outer=-13, arch=1.6, t=2), 'grin', '#d06a76', (hb, hf), blush_op=.5)
    phone = ('<rect x="38" y="200" width="14" height="24" rx="2.4" fill="#1e1e26"/><rect x="39.6" y="202" width="10.8" height="18" rx="1.4" fill="#5a78c0"/>'
             '<circle cx="45" cy="221.6" r=".9" fill="#3a3a46"/>')
    body = fbody(SK_WARM, ('#d49aa0', '#e8b4b8', '#b07a82'), ('#d49aa0', '#e8b4b8', '#b07a82'), hem=330, flare=46, neckline='v', shoes='#c8a090', extra=phone)
    return 'เพื่อนเจ้าสาว', 'แขกฝั่งเจ้าสาว ร่าเริง ยิ้มกว้าง ผมลอนประบ่าติดกิ๊บ ชุดเดรสสีชมพูกุหลาบหม่นคอวี ถือมือถือถ่ายรูปตลอด ตัดกับแขกฝั่งเจ้าบ่าวที่ไม่ถ่ายรูปเลย', 'f', back, head, body

def c_guest_w():
    hb, hf = hair_tight_bun('#18141a', '#34303a')
    back, head = fhead('gwf', SK_PALE, 'oval', dict(iris='#22181a', wing=0, lashes=0, catch=False, r=3.6),
                       dict(inner=-12, outer=-12, arch=.6, t=1.8), 'blank', '#a8626a', (hb, hf), blush_op=0, brow_col='#22181c')
    hands = '<path d="M -20,206 C -10,200 10,200 20,206 L 18,220 C 8,224 -8,224 -18,220 Z" fill="#f1d8cc"/>'
    body = fbody(SK_PALE, ('#6e7a72', '#86928a', '#56605a'), ('#6e7a72', '#86928a', '#56605a'), hem=456, flare=36, neckline='high', sleeves='long',
                 sleeve_col=('#6e7a72', '#86928a', '#56605a'), extra='')
    return 'แขกหญิงฝั่งเจ้าบ่าว', 'ผมเกล้ามวยตึงแสกกลาง แต่งตัวเรียบร้อยแบบโบราณ ชุดยาวสีเขียวเทาแขนยาว ตาดำเล็กไม่มีประกาย ยิ้มแข็งเส้นเดียวกับแขกฝั่งเจ้าบ่าวทุกคน ไม่ถือมือถือ', 'f', back, head, body

def c_photographer():
    hf = mhair_curtain('#3a2a24', '#5e4438', '#24170f')
    stub = ''.join(f'<circle cx="{x}" cy="{y}" r=".5" fill="#a98a7a"/>' for x in range(-12, 13, 3) for y in (31, 34) if abs(x) < 12)
    back, head = mhead('phm', SK_MALE_T, 'normal', dict(iris='#3a2418', wing=0, lashes=0, crease=True, r=4.4),
                       dict(inner=-11.6, outer=-13, t=2.4), 'm_sheepish', hf, extra=stub)
    cam = ('<path d="M -14,52 L -20,120 M 14,52 L 20,120" stroke="#1a1a20" stroke-width="2.4"/>'
           '<rect x="-24" y="116" width="48" height="32" rx="4" fill="#24242c"/><rect x="-24" y="116" width="48" height="8" rx="3" fill="#3a3a46"/>'
           '<circle cx="0" cy="134" r="12" fill="#14141a"/><circle cx="0" cy="134" r="8" fill="#2c3448"/><circle cx="-3" cy="131" r="2.4" fill="#8aa0c8"/>'
           '<rect x="12" y="110" width="8" height="6" fill="#3a3a46"/>')
    body = mbody(SK_MALE_T, ('#2e3a52', '#3e4c66', '#202a3c'), ('#1c1c22', '#2c2c36', '#121216'), lapels=False, rolled=True, shoes='#e8e4dc',
                 vest=('#8a7e62', '#a29676', '#6a604a'), extra=cam)
    return 'ช่างภาพ', 'อายุราว 30 ผมน้ำตาลเข้มแสกกลาง หนวดเคราจาง ๆ ยิ้มเจื่อนเหมือนเพิ่งพูดอะไรผิด เสื้อเชิ้ตดำพับแขน เสื้อกั๊กกระเป๋าเยอะสีกากี ยีนส์ สนีกเกอร์ขาว กล้องห้อยคอ', 'm', back, head, body

def c_guard():
    hf = mhair_buzz('#18161c', '#3a3842')
    ear = '<path d="M 33,4 C 38,10 34,16 38,22 C 42,28 36,34 40,42 C 42,48 38,52 36,56" fill="none" stroke="#24242c" stroke-width="1.4"/><circle cx="33" cy="2" r="2.4" fill="#24242c"/>'
    back, head = mhead('gdm', SK_MALE_T, 'square', dict(iris='#1e1414', wing=0, lashes=0, crease=False, heavy=.5, r=3.8),
                       dict(inner=-10.4, outer=-13.4, t=3), 'm_stern', hf, extra=ear)
    body = mbody(SK_MALE_T, ('#141418', '#24242c', '#0c0c10'), ('#141418', '#24242c', '#0c0c10'), tie=('#141418', '#0a0a0e'))
    return 'รปภ.', 'อายุราว 40 หน้าเหลี่ยม ผมเกรียน คิ้วหนากดต่ำ หน้านิ่งไม่ยิ้ม สูทดำ เน็คไทดำ หูฟังมีสายขดที่หูขวา', 'm', back, head, body

def c_guest_m():
    hf = mhair_slick('#1c1a20', '#8e8a94')
    back, head = mhead('gmm', SK_PALE, 'normal', dict(iris='#22181a', wing=0, lashes=0, crease=False, catch=False, r=3.4),
                       dict(inner=-12, outer=-12.6, t=2.2), 'blank', hf)
    body = mbody(SK_PALE, ('#4a4c54', '#5c5e68', '#36383e'), ('#4a4c54', '#5c5e68', '#36383e'), tie=('#5e3a44', '#422830'))
    return 'แขกชายฝั่งเจ้าบ่าว', 'ผมหวีเสยเรียบแปล้ จอนสีเทา สูทเทาเน็คไทแดงหม่น ตาดำเล็กไม่มีประกาย ยิ้มแข็งเส้นเดียวกับแขกหญิงฝั่งเจ้าบ่าว ยืนนิ่ง ไม่ถือมือถือ', 'm', back, head, body

CHARS = [c_woman_black, c_mother, c_photographer, c_staff, c_guard, c_new_bride, c_bridesmaid, c_guest_w, c_guest_m]

DEFS = '''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<pattern id="net" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><path d="M0,0 H4 M0,0 V4" stroke="#0a0a0e" stroke-width=".55" opacity=".85"/></pattern>
</defs></svg>'''

CSS = BASE_CSS.replace('<title>เจ้าสาวกับเจ้าบ่าว</title>', '<title>ตัวละครรองงานแต่ง</title>').replace(
    '.panels{display:grid;grid-template-columns:4fr 5fr;gap:16px;align-items:start}',
    '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:22px}.card{display:grid;gap:8px;min-width:0}.pair{display:grid;grid-template-columns:4fr 5fr;gap:8px;align-items:start}.card h2{font-size:15px;font-weight:500;margin:0;color:#e6e8f0}.card h2 span{font-size:12px;color:var(--muted);font-weight:400;margin-left:6px}')

def build():
    cards = ''
    for i, fn in enumerate(CHARS):
        name, note, kind, back, head, body = fn()
        if kind == 'f':
            full = f'<svg viewBox="0 0 400 900" role="img" aria-label="{name} เต็มตัว"><rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="790" rx="90" ry="10" fill="#10131b"/><g transform="translate(200,138) scale(1.4)">{back}{body}{head}</g></svg>'
        else:
            full = f'<svg viewBox="0 0 400 900" role="img" aria-label="{name} เต็มตัว"><rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="815" rx="80" ry="10" fill="#10131b"/><g transform="translate(200,130) scale(1.4)">{back}{body}{head}</g></svg>'
        face = f'<svg viewBox="-75 -84 150 156" role="img" aria-label="หน้า{name}"><rect x="-75" y="-84" width="150" height="156" fill="#1b1f2b"/><g id="face{i}">{back}{body}{head}</g></svg>'
        cards += f'<div class="card"><h2>{i + 1}. {name}</h2><div class="pair"><figure>{full}</figure><figure>{face}</figure></div><figcaption>{note}</figcaption></div>'
    page = CSS + DEFS + f'''<div class="wrap"><h1>ตัวละครรอง · ตอนงานแต่ง<span>รอบ 2 · หน้าเรียวลง · หน้าตรง · แสงกลางจากซ้าย</span></h1><div class="grid">{cards}</div></div>'''
    # clipPath ids repeat between the full-body and face panels of a card; make the face copies unique
    import re
    out, n = [], [0]
    for chunk in page.split('<g id="face'):
        out.append(chunk)
    page2 = out[0]
    for k, chunk in enumerate(out[1:]):
        end = chunk.index('</svg>')
        body_part = re.sub(r'id="([^"]+)"', lambda m: f'id="{m.group(1)}_f"', chunk[:end])
        body_part = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{m.group(1)}_f)' if m.group(1) != 'net' else 'url(#net)', body_part)
        page2 += '<g id="face' + body_part + chunk[end:]
    open('supporting.html', 'w').write(page2); print('ok', len(page2))

if __name__ == '__main__':
    build()
