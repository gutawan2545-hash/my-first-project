"""EP.01 เมื่อ Bangkok Native ย้ายไปอยู่เกาะเต่า: storyboard stills (19 shots, 9:16).
Run: python3 storyboard.py -> storyboard.html"""
import os, sys, math, random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'pipeline', 'lighting'))
import cinelight as CL
import sunrig as R

FONT_TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
FONT_EN = 'font-family="Inter, system-ui, sans-serif"'
PUR = '#c9a8ff'


# ================================================================ shared bits
def lg(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{st[0]}" stop-color="{st[1]}"' + (f' stop-opacity="{st[2]}"' if len(st) > 2 else '') + '/>' for st in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def blur(content, sd=2.2):
    return f'<g filter="url(#sb-dof{"2" if sd > 2.5 else ""})">{content}</g>'


def drop(shape, dx=10, dy=12, op=.35):
    """Soft cast shadow offset to the lower right (house rule)."""
    return f'<g transform="translate({dx},{dy})" opacity="{op}" filter="url(#sb-sh)" style="mix-blend-mode:multiply">{shape}</g>'


def palm(x, y, s=1.0, flip=False, dark=False):
    c1, c2, t1, t2 = (('#2f6b5a', '#3f8a6e', '#7a6656', '#5e4c40') if not dark else ('#24503f', '#2f6b55', '#5e4c40', '#493a31'))
    f = -1 if flip else 1
    trunk = (f'<path d="M 0,0 C {6*f},-60 {18*f},-120 {34*f},-170 L {42*f},-168 C {28*f},-118 {16*f},-60 10,0 Z" fill="{t1}"/>'
             f'<path d="M 6,0 C {10*f},-60 {22*f},-118 {38*f},-169 L {42*f},-168 C {28*f},-118 {16*f},-60 10,0 Z" fill="{t2}"/>')
    cx, cy = 38 * f, -170
    leaves = ''
    for ang, ln, col in ((-160, 70, c1), (-120, 62, c2), (-60, 66, c1), (-20, 72, c2), (20, 60, c1), (160, 64, c2), (-90, 50, c2)):
        a = math.radians(ang)
        ex, ey = cx + math.cos(a) * ln * f, cy + math.sin(a) * ln * .55 + 18
        mx, my = cx + math.cos(a) * ln * .5 * f, cy + math.sin(a) * ln * .3 - 10
        leaves += f'<path d="M {cx},{cy} Q {mx:.0f},{my - 14:.0f} {ex:.0f},{ey:.0f} Q {mx:.0f},{my + 4:.0f} {cx},{cy + 4} Z" fill="{col}"/>'
    return f'<g transform="translate({x},{y}) scale({s})">{trunk}{leaves}<circle cx="{cx}" cy="{cy + 6}" r="7" fill="#5e4c40"/></g>'


def boulder(x, y, w, h, c='#a7a3a6', cs='#86828a', ch='#c4c0c2'):
    return (f'<path d="M {x},{y} C {x + w * .05},{y - h * .9} {x + w * .4},{y - h} {x + w * .6},{y - h * .95} C {x + w * .9},{y - h * .85} {x + w},{y - h * .3} {x + w},{y} Z" fill="{c}"/>'
            f'<path d="M {x + w * .55},{y - h * .95} C {x + w * .9},{y - h * .85} {x + w},{y - h * .3} {x + w},{y} L {x + w * .62},{y} C {x + w * .72},{y - h * .4} {x + w * .7},{y - h * .7} {x + w * .55},{y - h * .95} Z" fill="{cs}"/>'
            f'<path d="M {x + w * .1},{y - h * .6} C {x + w * .2},{y - h * .9} {x + w * .4},{y - h * .97} {x + w * .5},{y - h * .95} C {x + w * .3},{y - h * .8} {x + w * .2},{y - h * .6} {x + w * .16},{y - h * .4} Z" fill="{ch}"/>')


def cloud(x, y, s=1.0, op=.9):
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{op}"><ellipse cx="0" cy="0" rx="46" ry="14" fill="#ffffff"/>'
            f'<ellipse cx="-16" cy="-10" rx="22" ry="16" fill="#ffffff"/><ellipse cx="14" cy="-14" rx="26" ry="20" fill="#ffffff"/>'
            f'<ellipse cx="6" cy="4" rx="44" ry="8" fill="#e3ecf6"/></g>')


def tag(text, x=20, y=22):
    w = 22 + len(text) * 8.2
    return (f'<g {FONT_TH}><rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#120e1c" fill-opacity=".82" stroke="#9a86ff" stroke-opacity=".75"/>'
            f'<circle cx="{x + 15}" cy="{y + 15}" r="4.5" fill="#9a86ff"/><text x="{x + 26}" y="{y + 20}" font-size="13" font-weight="500" fill="#f2eefa">{text}</text></g>')


EYE_MARK = ('<g transform="translate(506,36)" opacity=".85"><path d="M -13,0 Q 0,-10 13,0 Q 0,10 -13,0 Z" fill="none" stroke="#b18cff" stroke-width="2"/>'
            '<circle cx="0" cy="0" r="4" fill="#b18cff"/></g>')


def subs(th, en, y=712):
    th = [l for l in th.split('/') if l.strip()]
    en = [l for l in en.split('/') if l.strip()]
    lh_t, lh_e, gap = 26, 17, 6
    h = len(th) * lh_t + (gap + len(en) * lh_e if en else 0)
    top = y - h / 2
    out = f'<g class="subs"><g {FONT_TH} font-weight="700" font-size="20" text-anchor="middle" fill="#ffd84a" stroke="#0b0812" stroke-width="5" stroke-linejoin="round" paint-order="stroke">'
    for i, l in enumerate(th):
        out += f'<text x="270" y="{top + 19 + i * lh_t:.0f}">{l.strip()}</text>'
    out += f'</g><g {FONT_EN} font-weight="500" font-size="13" text-anchor="middle" fill="#ffffff" stroke="#0b0812" stroke-width="4" stroke-linejoin="round" paint-order="stroke">'
    for i, l in enumerate(en):
        out += f'<text x="270" y="{top + len(th) * lh_t + gap + 12 + i * lh_e:.0f}">{l.strip()}</text>'
    return out + '</g></g>'


def card(x, y, w, title, body, px, py):
    """Explainer card (warm white) with a dashed leader to the point it explains."""
    h = 50 if body else 34
    return (f'<g class="info" {FONT_TH}><path d="M{x + w / 2},{y + h} L{px},{py}" stroke="#fff" stroke-width="2" stroke-dasharray="4 4" opacity=".9"/>'
            f'<circle cx="{px}" cy="{py}" r="4.5" fill="#fff"/><circle cx="{px}" cy="{py}" r="9" fill="none" stroke="#fff" stroke-opacity=".55"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#f8f4ec" fill-opacity=".96"/>'
            f'<text x="{x + 12}" y="{y + 22}" font-size="15" font-weight="600" fill="#1a1626">{title}</text>'
            + (f'<text x="{x + 12}" y="{y + 40}" font-size="11.5" fill="#5a5470">{body}</text>' if body else '') + '</g>')


SHARED_DEFS = ('<filter id="sb-dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2.2"/></filter>'
               '<filter id="sb-dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.6"/></filter>'
               '<filter id="sb-sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>'
               '<filter id="sb-glowtxt" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="3"/></filter>')

FRAMES = []
_n = [0]


def sun_char(fid, tx, ty, s, light, **kw):
    """Sun with the cinematic lighting wrapper. light = light position in frame coords."""
    d = CL.aim((tx, ty + 120 * s), light)
    _n[0] += 1
    f, mk = CL.character(f'{fid}-sun{_n[0]}', R.body(**kw), d, 'day',
                         transform=f'translate({tx},{ty}) scale({s})', heads=[('sun', '')], prefix=fid)
    return f, mk


def frame(fid, label, rig='day', bg='', shadow='', chars=(), fg='', light='', atmos='', ui='', defs='', ft=''):
    fdefs = ''.join(c[0] for c in chars)
    cm = ''.join(c[1] for c in chars) + fg
    return CL.compose(rig, bg=bg, shadow=shadow, chars=cm, light=light, atmos=atmos, ui=ui + EYE_MARK,
                      extra_defs=fdefs + defs, label=label, prefix=fid, frame_transform=ft)


# ================================================================ backgrounds
def condo_room(fid, door=False):
    d = (lg(f'{fid}w', [(0, '#e9e4ea'), (1, '#d8d0da')]) + lg(f'{fid}sky', [(0, '#b9cde3'), (1, '#e7e2e4')]) +
         lg(f'{fid}fl', [(0, '#b9a79c'), (1, '#9c8a82')]))
    sky = ''
    rnd = random.Random(4)
    for i in range(14):                                  # Bangkok towers, hazy
        x = 40 + i * 24 + rnd.randint(-6, 6); h = rnd.randint(90, 230); w = rnd.randint(18, 30)
        col = rnd.choice(['#a9b4c6', '#9aa6ba', '#b6bfcd'])
        sky += f'<rect x="{x}" y="{430 - h}" width="{w}" height="{h}" fill="{col}"/>'
        for wy in range(430 - h + 8, 420, 12):
            sky += f'<rect x="{x + 4}" y="{wy}" width="{w - 8}" height="3" fill="#c9d2de" opacity=".7"/>'
    # BTS viaduct + jammed cars
    sky += ('<rect x="20" y="372" width="400" height="12" fill="#8c95a6"/><rect x="20" y="384" width="400" height="4" fill="#737c8e"/>'
            '<rect x="70" y="384" width="10" height="46" fill="#7d8698"/><rect x="230" y="384" width="10" height="46" fill="#7d8698"/><rect x="380" y="384" width="10" height="46" fill="#7d8698"/>'
            '<rect x="120" y="356" width="150" height="16" rx="5" fill="#dfe6ee"/><rect x="120" y="364" width="150" height="3" fill="#4f7fbf"/>')
    for i in range(9):
        c = ['#d8655a', '#e8e2da', '#5a6c8e', '#c9cfd8', '#3c4458'][i % 5]
        sky += f'<rect x="{26 + i * 44}" y="418" width="36" height="12" rx="4" fill="{c}"/><circle cx="{30 + i * 44}" cy="425" r="2" fill="#ff8a7a" opacity=".9"/>'
    win = (f'<rect x="20" y="150" width="420" height="300" fill="#e3dde0"/>'
           f'<g clip-path="url(#{fid}wc)"><rect x="28" y="158" width="404" height="284" fill="url(#{fid}sky)"/>{sky}</g>'
           f'<clipPath id="{fid}wc"><rect x="28" y="158" width="404" height="284"/></clipPath>'
           '<rect x="226" y="158" width="8" height="284" fill="#e3dde0"/>')
    room = (f'<rect width="540" height="960" fill="url(#{fid}w)"/>' + blur(win, 2.6) +
            f'<rect y="610" width="540" height="350" fill="url(#{fid}fl)"/><rect y="604" width="540" height="8" fill="#cfc4c4"/>')
    if door:
        room += ('<rect x="400" y="250" width="130" height="360" fill="#8a7468"/><rect x="408" y="258" width="114" height="352" fill="#a28b7d"/>'
                 '<circle cx="414" cy="440" r="5" fill="#d6cfc8"/><path d="M 522,258 L 540,248 L 540,620 L 522,610 Z" fill="#6f5d54"/>')
    else:
        # bed with an open suitcase, clothes
        room += ('<path d="M 300,600 L 540,600 L 540,520 L 320,520 Z" fill="#c9c3d6"/><rect x="300" y="596" width="240" height="22" fill="#a9a2bc"/>'
                 '<rect x="330" y="470" width="210" height="60" rx="10" fill="#e6e1ec"/>')
    return d, room


def sea_sky(fid, horizon=420):
    d = (lg(f'{fid}sk', [(0, '#7fb4e0'), (.7, '#cfe3f1'), (1, '#eef3f6')]) +
         lg(f'{fid}se', [(0, '#3fa7b8'), (.5, '#58c0c4'), (1, '#8fd8cf')]))
    bg = (f'<rect width="540" height="{horizon}" fill="url(#{fid}sk)"/>' + cloud(110, 120, 1.1) + cloud(400, 80, .8) + cloud(300, 200, .6, .8) +
          f'<rect y="{horizon}" width="540" height="{960 - horizon}" fill="url(#{fid}se)"/>')
    return d, bg


# ================================================================ shots
def s01():
    fid = 'f01'
    d, bg = condo_room(fid)
    suitcase = ('<g><rect x="356" y="560" width="150" height="60" rx="8" fill="#3d4f6e"/><rect x="356" y="560" width="150" height="14" rx="6" fill="#516687"/>'
                '<rect x="364" y="566" width="134" height="40" rx="4" fill="#2c3a54"/><path d="M 370,566 L 430,566 L 420,590 L 372,590 Z" fill="#f2eee6"/>'
                '<path d="M 432,566 L 494,566 L 490,584 L 440,588 Z" fill="#2f5a5e"/><path d="M 362,560 L 500,560 L 486,500 L 376,500 Z" fill="#46597a"/></g>')
    ch = [sun_char(fid, 210, 300, .95, (-60, 300), head='dead', tote=False, camera=False)]
    sh = CL.contact_shadow(210, 768, 52) + drop(suitcase, 10, 10, .3) + CL.ao_line(0, 606, 540, 606, 16, .35)
    light = CL.glow(230, 300, 300, '#ffffff', .18, core=False) + CL.shaft([(28, 158), (226, 158), (420, 960), (0, 960)], '#fff4e8', .16, src=(120, 160), end=(200, 900), dust_n=40, seed=2)
    ui = tag('EP.01 · เกาะเต่า') + subs('จะเป็นยังไง ถ้าคุณเป็น Bangkok Native/ที่เบื่อชีวิตในกรุงเทพ/แล้วตัดสินใจเก็บกระเป๋า/ย้ายไปอยู่เกาะเต่า',
                                      'What if you were a Bangkok native, tired of the city,/who packed up and moved to Koh Tao?')
    return frame(fid, 'ช็อต 1', bg=bg, shadow=sh, chars=ch, fg=suitcase, light=light, ui=ui, defs=d)


def s02():
    fid = 'f02'
    d, bg = condo_room(fid, door=True)
    case = ('<g><rect x="392" y="540" width="70" height="104" rx="10" fill="#3d4f6e"/><rect x="392" y="540" width="20" height="104" rx="8" fill="#516687"/>'
            '<rect x="420" y="470" width="6" height="72" fill="#9aa3b4"/><rect x="408" y="466" width="30" height="8" rx="3" fill="#2a2f3c"/>'
            '<circle cx="404" cy="650" r="6" fill="#1b1e28"/><circle cx="450" cy="650" r="6" fill="#1b1e28"/></g>')
    ch = [sun_char(fid, 300, 300, .95, (-60, 300), head='shades', R='R_hang')]
    sh = CL.contact_shadow(300, 768, 52) + CL.contact_shadow(427, 656, 40, 6) + CL.ao_line(0, 606, 400, 606, 16, .35)
    title = (f'<g {FONT_TH} font-weight="700" fill="#fff" stroke="#0b0812" stroke-width="6" paint-order="stroke" stroke-linejoin="round">'
             '<text x="270" y="118" font-size="20" text-anchor="middle" fill="#e6dcff">EP.01</text>'
             '<text x="270" y="162" font-size="34" text-anchor="middle">เมื่อ Bangkok Native</text>'
             f'<text x="270" y="206" font-size="34" text-anchor="middle">ย้ายไปอยู่<tspan fill="{PUR}">เกาะเต่า</tspan></text></g>')
    ui = title + subs('พอกันทีกับรถติด/ไปใช้ชีวิตดีกว่า', 'Enough traffic. Time to actually live.')
    return frame(fid, 'ช็อต 2', bg=bg, shadow=sh, chars=ch, fg=case, light=CL.glow(160, 260, 260, '#ffffff', .16, core=False), ui=ui, defs=d)


TH = [(20.4, 99.9), (20.2, 100.5), (19.5, 101.2), (18.2, 101.1), (17.9, 102.0), (18.2, 103.3), (17.5, 104.5), (16.5, 104.8),
      (15.4, 105.6), (14.3, 105.2), (14.4, 103.5), (13.7, 102.5), (12.6, 102.6), (11.7, 102.9), (12.2, 102.2), (12.6, 101.4),
      (12.7, 100.95), (13.4, 100.95), (13.5, 100.6), (13.45, 100.1), (12.6, 99.95), (11.8, 99.8), (10.9, 99.5), (10.3, 99.2),
      (9.4, 99.3), (9.2, 99.9), (8.4, 100.2), (7.2, 100.6), (6.9, 101.5), (6.2, 102.0), (5.8, 101.6), (6.0, 101.1), (6.6, 100.3),
      (7.0, 99.6), (7.9, 98.4), (8.5, 98.3), (9.4, 98.5), (10.0, 98.6), (11.2, 99.3), (12.2, 99.0), (13.2, 99.1), (14.3, 98.6),
      (15.2, 98.2), (16.3, 98.6), (17.6, 97.8), (18.5, 97.5), (19.6, 97.9), (20.1, 99.0)]


def s03():
    fid = 'f03'
    P = lambda lat, lon: (60 + (lon - 97.3) * 34, 70 + (20.5 - lat) * 34)
    pts = ' '.join(f'{x:.1f},{y:.1f}' for x, y in (P(*p) for p in TH))
    bkk, cpn = P(13.75, 100.5), P(10.49, 99.18)
    Q = lambda lat, lon: (318 + (lon - 98.95) * 150, 352 + (10.85 - lat) * 150)     # inset
    coast = ' '.join(f'{x:.0f},{y:.0f}' for x, y in (Q(*p) for p in [(10.85, 99.5), (10.6, 99.3), (10.47, 99.27), (10.3, 99.2), (10.0, 99.15), (9.7, 99.25), (9.55, 99.35)]))
    tao, pier, pg, sm = Q(10.1, 99.84), Q(10.47, 99.27), Q(9.76, 100.03), Q(9.5, 100.0)
    bg = ('<rect width="540" height="960" fill="#1d2a3d"/>'
          + ''.join(f'<path d="M 0,{y} L 540,{y}" stroke="#24344b" stroke-width="1"/>' for y in range(40, 960, 40))
          + ''.join(f'<path d="M {x},0 L {x},960" stroke="#24344b" stroke-width="1"/>' for x in range(30, 540, 40))
          + '<rect x="0" y="0" width="540" height="960" fill="#2e6f8e" opacity=".18"/>')
    mp = (f'<polygon points="{pts}" fill="#e8dfcf" stroke="#f8f2e6" stroke-width="1.6"/>'
          f'<path d="M {bkk[0]:.0f},{bkk[1]:.0f} C {bkk[0] - 30:.0f},{bkk[1] + 40:.0f} {cpn[0] + 10:.0f},{cpn[1] - 60:.0f} {cpn[0]:.0f},{cpn[1]:.0f}" stroke="#d8655a" stroke-width="3" stroke-dasharray="7 6" fill="none"/>'
          f'<circle cx="{bkk[0]:.0f}" cy="{bkk[1]:.0f}" r="7" fill="#d8655a"/><circle cx="{bkk[0]:.0f}" cy="{bkk[1]:.0f}" r="14" fill="none" stroke="#d8655a" opacity=".5"/>'
          f'<circle cx="{cpn[0]:.0f}" cy="{cpn[1]:.0f}" r="6" fill="#2fb3b8"/>'
          f'<text x="{bkk[0] + 14:.0f}" y="{bkk[1] - 8:.0f}" {FONT_TH} font-size="14" font-weight="600" fill="#fff">กรุงเทพ</text>'
          f'<text x="{cpn[0] - 66:.0f}" y="{cpn[1] + 5:.0f}" {FONT_TH} font-size="14" font-weight="600" fill="#fff">ชุมพร</text>'
          f'<text x="{P(11.5, 101.0)[0]:.0f}" y="{P(11.5, 101.0)[1]:.0f}" {FONT_TH} font-size="13" fill="#9ccbe0" font-style="italic">อ่าวไทย</text>'
          f'<rect x="{cpn[0] + 4:.0f}" y="{cpn[1] - 18:.0f}" width="40" height="40" fill="none" stroke="#fff" stroke-width="1.5"/>'
          f'<path d="M {cpn[0] + 44:.0f},{cpn[1] - 18:.0f} L 310,344 M {cpn[0] + 44:.0f},{cpn[1] + 22:.0f} L 310,566" stroke="#fff" stroke-opacity=".6" stroke-width="1.2"/>')
    inset = (f'<rect x="310" y="344" width="212" height="222" rx="14" fill="#7fcfd4" stroke="#fff" stroke-width="2"/>'
             f'<clipPath id="{fid}ic"><rect x="310" y="344" width="212" height="222" rx="14"/></clipPath>'
             f'<g clip-path="url(#{fid}ic)"><polygon points="300,340 {coast} 300,580" fill="#e8dfcf"/>'
             + ''.join(f'<path d="M {330 + i * 30},{400 + (i % 3) * 50} q 8,-5 16,0 q 8,5 16,0" stroke="#fff" stroke-opacity=".5" fill="none" stroke-width="1.5"/>' for i in range(6))
             + f'<path d="M {pier[0]:.0f},{pier[1]:.0f} C {pier[0] + 40:.0f},{pier[1] - 10:.0f} {tao[0] - 30:.0f},{tao[1] - 30:.0f} {tao[0] - 8:.0f},{tao[1] - 4:.0f}" stroke="#d8655a" stroke-width="3" stroke-dasharray="6 5" fill="none"/>'
             f'<ellipse cx="{tao[0]:.0f}" cy="{tao[1]:.0f}" rx="13" ry="16" fill="#6faa6a" stroke="#f8f2e6" stroke-width="2"/>'
             f'<ellipse cx="{pg[0]:.0f}" cy="{pg[1]:.0f}" rx="22" ry="18" fill="#8fbf86" opacity=".8"/><ellipse cx="{sm[0] + 6:.0f}" cy="{sm[1] + 16:.0f}" rx="34" ry="22" fill="#8fbf86" opacity=".7"/>'
             f'<g transform="translate({(pier[0] + tao[0]) / 2 + 6:.0f},{(pier[1] + tao[1]) / 2 - 18:.0f})"><path d="M -14,0 L 14,0 L 9,8 L -10,8 Z" fill="#fff"/><rect x="-6" y="-8" width="12" height="8" fill="#f2eee6"/><rect x="-4" y="-6" width="3" height="3" fill="#3fa7b8"/></g>'
             '</g>'
             f'<text x="{tao[0] + 18:.0f}" y="{tao[1] - 6:.0f}" {FONT_TH} font-size="15" font-weight="700" fill="#16303a">เกาะเต่า</text>'
             f'<text x="{pier[0] - 4:.0f}" y="{pier[1] - 12:.0f}" {FONT_TH} font-size="11" font-weight="600" fill="#16303a">ท่าเรือ</text>'
             f'<text x="{pg[0] - 20:.0f}" y="{pg[1] + 30:.0f}" {FONT_TH} font-size="10" fill="#2a5560">พะงัน</text>')
    noair = (f'<g transform="translate(110,520)" {FONT_TH}><rect x="-70" y="-24" width="168" height="48" rx="24" fill="#f8f4ec"/>'
             '<path d="M -48,4 L -30,-2 L -26,-14 L -22,-14 L -22,-4 L -10,-8 L -10,-4 L -22,2 L -22,10 L -18,13 L -18,15 L -26,12 L -34,14 L -34,12 L -30,9 L -30,3 L -46,8 Z" fill="#1a1626"/>'
             '<circle cx="-29" cy="0" r="17" fill="none" stroke="#d8655a" stroke-width="3"/><path d="M -41,-12 L -17,12" stroke="#d8655a" stroke-width="3"/>'
             '<text x="-4" y="6" font-size="15" font-weight="600" fill="#1a1626">ไม่มีสนามบิน</text></g>')
    ui = tag('เรื่องที่ 1 · ทะเลคือประตูบ้าน') + subs('เกาะเต่าเป็นเกาะเล็ก ๆ กลางอ่าวไทย/ไม่มีสนามบิน การเดินทางเข้าออกเกาะ/จึงต้องอาศัยเรือเป็นหลัก',
                                                   'Koh Tao is a small island in the Gulf of Thailand./No airport, so getting there means a boat.')
    return frame(fid, 'ช็อต 3', bg=bg, fg=mp + inset + noair, ui=ui)


def s04():
    fid = 'f04'
    d, bg = sea_sky(fid, 360)
    bg += ('<path d="M 360,362 C 380,330 420,316 460,322 C 490,326 520,340 540,350 L 540,362 Z" fill="#6f9e78"/>'
           '<path d="M 0,362 C 30,350 60,346 90,352 L 120,362 Z" fill="#86ad86"/>')
    bg = blur(bg, 2.4)
    spray = ''.join(f'<path d="M {i * 60 - 20},{560 + (i % 2) * 30} q 30,-10 60,0" stroke="#fff" stroke-opacity=".7" stroke-width="3" fill="none"/>' for i in range(10))
    boat = ('<path d="M -20,700 L 560,640 L 560,960 L -20,960 Z" fill="#f2eee6"/><path d="M -20,700 L 560,640 L 560,660 L -20,722 Z" fill="#d7d0c4"/>'
            '<rect x="-20" y="610" width="580" height="8" fill="#c8ccd6" transform="rotate(-6 270 610)"/>'
            + ''.join(f'<rect x="{x}" y="{614 - x * .105:.0f}" width="5" height="{96 + x * .0:.0f}" fill="#b8bcc8"/>' for x in range(10, 540, 66))
            + '<rect x="-20" y="560" width="580" height="7" fill="#d9dce4" transform="rotate(-6 270 560)"/>')
    ch = [sun_char(fid, 270, 330, 1.75, (-200, 120), head='wind', L='L_hang', R='R_hang', camera=True)]
    lines = ''.join(f'<path d="M {x},{y} L {x + 90},{y - 8}" stroke="#fff" stroke-opacity=".55" stroke-width="2" stroke-linecap="round"/>' for x, y in ((40, 260), (420, 300), (60, 420), (380, 470), (30, 520)))
    ui = tag('เรื่องที่ 1 · ทะเลคือประตูบ้าน')
    return frame(fid, 'ช็อต 4', bg=bg + spray, chars=ch, fg=boat, light=CL.glow(-40, 80, 380, '#ffffff', .3, core=False), atmos=lines, ui=ui, defs=d)


def s05():
    fid = 'f05'
    bg = ('<rect width="540" height="960" fill="#e9eef2"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#c7d2dc"/>' for x in range(20, 540, 26) for y in range(20, 560, 26)))
    steps = [('โกดัง', 90, '#5a6c8e'), ('รถบรรทุก', 210, '#d8655a'), ('ท่าเรือชุมพร', 330, '#2fb3b8'), ('ข้ามทะเล', 450, '#3d4f6e')]
    icons = (
        '<g transform="translate(90,230)"><path d="M -40,0 L 0,-26 L 40,0 L 40,40 L -40,40 Z" fill="#5a6c8e"/><rect x="-14" y="12" width="28" height="28" fill="#2c3a54"/><path d="M -40,0 L 0,-26 L 40,0" stroke="#3d4f6e" stroke-width="5" fill="none"/></g>'
        '<g transform="translate(210,236)"><rect x="-44" y="-18" width="58" height="40" rx="4" fill="#f2eee6"/><path d="M 14,-6 L 34,-6 L 46,8 L 46,22 L 14,22 Z" fill="#d8655a"/><rect x="22" y="-2" width="12" height="9" fill="#bfe3ee"/><circle cx="-28" cy="26" r="8" fill="#2c3040"/><circle cx="30" cy="26" r="8" fill="#2c3040"/></g>'
        '<g transform="translate(330,236)"><rect x="-44" y="10" width="88" height="12" fill="#8a7468"/>' + ''.join(f'<rect x="{-40 + i * 20}" y="22" width="5" height="18" fill="#6f5d54"/>' for i in range(5)) + '<path d="M -20,10 L -20,-30 L 10,-14 L -20,-6" fill="#2fb3b8"/></g>'
        '<g transform="translate(450,236)"><path d="M -40,8 L 40,8 L 30,24 L -32,24 Z" fill="#f2eee6"/><rect x="-16" y="-8" width="30" height="16" fill="#e8e2da"/>'
        '<path d="M -50,34 q 12,-10 25,0 q 12,10 25,0 q 12,-10 25,0 q 12,10 25,0" stroke="#2fb3b8" stroke-width="4" fill="none"/></g>')
    labels = ''.join(f'<text x="{x}" y="300" {FONT_TH} font-size="14" font-weight="600" fill="#1a1626" text-anchor="middle">{t}</text>' for t, x, c in steps)
    path = '<path d="M 90,330 L 450,330" stroke="#1a1626" stroke-width="2.5" stroke-dasharray="6 6"/>' + ''.join(f'<circle cx="{x}" cy="330" r="7" fill="{c}"/>' for t, x, c in steps)
    box = ('<g transform="translate(330,328)"><rect x="-16" y="-34" width="32" height="26" rx="2" fill="#c49a6c"/><rect x="-16" y="-34" width="32" height="7" fill="#a97f55"/><rect x="-3" y="-34" width="6" height="26" fill="#e6d2b0"/></g>')
    storm = ('<g transform="translate(270,452)"><rect x="-200" y="-70" width="400" height="150" rx="18" fill="#1d2a3d"/>'
             '<path d="M -200,30 q 25,-30 50,0 q 25,30 50,0 q 25,-30 50,0 q 25,30 50,0 q 25,-30 50,0 q 25,30 50,0 q 25,-30 50,0 q 25,30 50,0 L 200,80 L -200,80 Z" fill="#2f7f96"/>'
             '<path d="M -200,50 q 25,-22 50,0 q 25,22 50,0 q 25,-22 50,0 q 25,22 50,0 q 25,-22 50,0 q 25,22 50,0 q 25,-22 50,0 q 25,22 50,0 L 200,80 L -200,80 Z" fill="#3fa7b8"/>'
             '<g transform="translate(-10,6) rotate(-14)"><path d="M -34,4 L 34,4 L 26,18 L -28,18 Z" fill="#f2eee6"/><rect x="-14" y="-10" width="26" height="14" fill="#e8e2da"/></g>'
             '<path d="M -170,-40 q 30,-12 60,0 M -160,-20 q 40,-14 80,0 M 90,-46 q 30,-12 60,0 M 100,-26 q 40,-14 80,0" stroke="#cfe6ff" stroke-width="3" fill="none" stroke-linecap="round"/>'
             f'<text x="0" y="-38" {FONT_TH} font-size="17" font-weight="700" fill="#fff" text-anchor="middle">คลื่นลมแรง = ของมาช้า</text></g>')
    ui = tag('เรื่องที่ 2 · สนิทกับพยากรณ์อากาศ') + subs('สินค้าหลายอย่างต้องขนส่งมาทางเรือ/ถ้าคลื่นลมแรง/พัสดุของคุณก็อาจมาช้ากว่าปกติ',
                                                        'Most goods arrive by boat./When the sea gets rough, your parcel runs late.')
    return frame(fid, 'ช็อต 5', bg=bg, fg=icons + labels + path + box + storm, ui=ui)


def porch(fid):
    d, bg = sea_sky(fid, 330)
    bg += boulder(380, 370, 160, 70) + boulder(-20, 360, 120, 40)
    bg = blur(bg + palm(470, 520, .9, True) + palm(40, 500, .8), 2.6)
    deck = ('<rect y="560" width="540" height="400" fill="#b58f72"/>' + ''.join(f'<rect y="{560 + i * 34}" width="540" height="3" fill="#9c785e"/>' for i in range(12)) +
            '<rect x="0" y="420" width="540" height="10" fill="#8e6b52"/><rect x="0" y="470" width="540" height="8" fill="#8e6b52"/>' +
            ''.join(f'<rect x="{x}" y="420" width="10" height="142" fill="#8e6b52"/>' for x in (10, 180, 350, 520)) +
            '<g transform="translate(470,560)"><path d="M -24,0 L 24,0 L 18,-40 L -18,-40 Z" fill="#c9a07e"/><path d="M 0,-40 C -30,-80 -40,-110 -20,-130 C -10,-100 0,-80 0,-40 M 0,-40 C 20,-90 40,-100 50,-120 C 40,-90 20,-70 0,-40" fill="#3f8a6e"/></g>')
    return d, bg + deck


def s06():
    fid = 'f06'
    d, bg = porch(fid)
    ch = [sun_char(fid, 250, 300, 1.25, (-220, 150), head='talk', front='L_phone', camera=False)]
    ui = tag('เรื่องที่ 2 · สนิทกับพยากรณ์อากาศ') + subs('พี่ครับ ของผมถึงไหนแล้ว?', 'Hi, where is my parcel now?')
    return frame(fid, 'ช็อต 6', bg=bg, shadow=CL.contact_shadow(250, 916, 66), chars=ch, light=CL.glow(-40, 120, 360, '#ffffff', .28, core=False), ui=ui, defs=d)


def s07():
    fid = 'f07'
    d, bg = porch(fid)
    bg = blur(bg, 3.6)
    phone = ('<g transform="translate(270,420) rotate(-4)"><rect x="-120" y="-250" width="240" height="470" rx="34" fill="#15151c"/>'
             '<rect x="-108" y="-236" width="216" height="442" rx="26" fill="#f4f1ec"/>'
             f'<g {FONT_TH} text-anchor="middle"><text x="0" y="-178" font-size="13" fill="#6a6478">กำลังสนทนา · 00:12</text>'
             '<circle cx="0" cy="-118" r="38" fill="#2fb3b8"/><path d="M -18,-122 L 0,-136 L 18,-122 L 18,-100 L -18,-100 Z" fill="#fff"/><rect x="-6" y="-114" width="12" height="14" fill="#2fb3b8"/>'
             '<text x="0" y="-56" font-size="19" font-weight="700" fill="#1a1626">ขนส่ง · สาขาเกาะเต่า</text>'
             '<g transform="translate(0,-10)">' + ''.join(f'<rect x="{-70 + i * 10}" y="{-h / 2}" width="5" height="{h}" rx="2.5" fill="#2fb3b8"/>' for i, h in enumerate([8, 18, 30, 14, 36, 22, 10, 26, 40, 18, 12, 28, 16, 8, 20])) + '</g>'
             '<rect x="-90" y="34" width="180" height="104" rx="14" fill="#e3edf0"/>'
             '<text x="0" y="60" font-size="12" fill="#4a5a66">สถานะพัสดุ</text>'
             '<circle cx="-56" cy="96" r="7" fill="#2fb3b8"/><path d="M -49,96 L 49,96" stroke="#9fb4bf" stroke-width="3" stroke-dasharray="5 5"/><circle cx="56" cy="96" r="7" fill="#c9d4da"/>'
             '<text x="-56" y="124" font-size="12" font-weight="600" fill="#1a1626">ชุมพร</text><text x="56" y="124" font-size="12" fill="#8a96a0">เกาะเต่า</text></g>'
             '<circle cx="0" cy="176" r="24" fill="#d8655a"/><path d="M -12,176 L 12,176" stroke="#fff" stroke-width="5" stroke-linecap="round"/></g>')
    hand = f'<path d="M 120,700 C 150,640 170,600 190,600 L 210,640 L 180,760 L 110,760 Z" fill="{R.SK}"/>'
    ui = tag('เรื่องที่ 2 · สนิทกับพยากรณ์อากาศ') + subs('ยังอยู่ชุมพรครับ', 'It’s still in Chumphon.') + card(330, 120, 180, 'เสียงพนักงาน', 'พูดผ่านโทรศัพท์ กล้องอยู่ที่จอ', 300, 330)
    return frame(fid, 'ช็อต 7', bg=bg, fg=drop(phone, 14, 16, .4) + phone + hand, ui=ui, defs=d)


def s08():
    fid = 'f08'
    d, bg = porch(fid)
    ch = [sun_char(fid, 270, 330, 2.2, (-240, 160), head='dead', front='L_phone', camera=False, tote=False)]
    ui = tag('เรื่องที่ 2 · สนิทกับพยากรณ์อากาศ') + subs('อ๋อ… ยังไม่ได้ลงเรือเลย', 'Oh… it hasn’t even boarded the boat.')
    return frame(fid, 'ช็อต 8', bg=blur(bg, 3.6), chars=ch, light=CL.glow(-40, 160, 360, '#ffffff', .25, core=False), ui=ui, defs=d)


def iso_tile(cx, cy, w, col_top, col_l, col_r, h=26):
    a, b = w, w / 2
    return (f'<path d="M {cx},{cy - b} L {cx + a},{cy} L {cx},{cy + b} L {cx - a},{cy} Z" fill="{col_top}"/>'
            f'<path d="M {cx - a},{cy} L {cx},{cy + b} L {cx},{cy + b + h} L {cx - a},{cy + h} Z" fill="{col_l}"/>'
            f'<path d="M {cx + a},{cy} L {cx},{cy + b} L {cx},{cy + b + h} L {cx + a},{cy + h} Z" fill="{col_r}"/>')


def s09():
    fid = 'f09'
    bg = '<rect width="540" height="960" fill="#e9eef2"/>'
    # Bangkok: flat tile, grid road, BTS pillars
    bkk = iso_tile(140, 300, 110, '#cfd5de', '#a9b2c0', '#939caa')
    bkk += '<path d="M 70,265 L 210,335 M 140,245 L 60,285 M 220,285 L 130,330" stroke="#7d8698" stroke-width="7" stroke-linecap="round"/>'
    bkk += ''.join(f'<rect x="{80 + i * 30}" y="{250 + i * 15 - 30}" width="5" height="30" fill="#6f788a"/>' for i in range(5))
    bkk += '<path d="M 80,220 L 210,285" stroke="#4f7fbf" stroke-width="6"/>'
    bkk += ''.join(f'<rect x="{x}" y="{y - h}" width="16" height="{h}" fill="#b6bfcd"/><rect x="{x + 16}" y="{y - h + 8}" width="8" height="{h - 8}" fill="#9aa6ba"/>' for x, y, h in ((160, 300, 60), (190, 310, 80), (110, 320, 50)))
    # Koh Tao: stacked tiles = hill, winding road climbing
    tao = ''
    for i, (dy, w, c) in enumerate([(0, 110, '#7fb07a'), (-34, 80, '#6fa46c'), (-66, 54, '#5f985e'), (-94, 30, '#558c55')]):
        tao += iso_tile(400, 330 + dy, w, c, '#4f7f52', '#3f6d44', 30)
    tao += '<path d="M 310,340 C 350,350 420,330 450,312 C 470,300 420,290 380,296 C 350,300 360,276 400,270 C 430,265 425,248 400,244" stroke="#efe6d8" stroke-width="7" fill="none" stroke-linecap="round"/>'
    tao += '<path d="M 310,340 C 350,350 420,330 450,312 C 470,300 420,290 380,296 C 350,300 360,276 400,270 C 430,265 425,248 400,244" stroke="#d8655a" stroke-width="2" stroke-dasharray="4 4" fill="none"/>'
    tao += boulder(440, 360, 40, 24) + palm(330, 330, .25) + palm(460, 300, .22, True)
    labels = (f'<g {FONT_TH} font-weight="700" text-anchor="middle"><text x="140" y="420" font-size="18" fill="#1a1626">กรุงเทพ</text><text x="140" y="442" font-size="13" font-weight="500" fill="#5a5470">ราบ เดินตรงยาว</text>'
              '<text x="400" y="420" font-size="18" fill="#1a1626">เกาะเต่า</text><text x="400" y="442" font-size="13" font-weight="500" fill="#5a5470">เนินชัน ถนนคดเคี้ยว</text></g>')
    prof = ('<g transform="translate(60,470)"><rect x="0" y="0" width="420" height="92" rx="12" fill="#fff"/>'
            '<path d="M 20,70 L 190,70" stroke="#7d8698" stroke-width="4"/><path d="M 230,70 C 270,70 290,24 330,22 C 360,22 370,40 400,30" stroke="#5f985e" stroke-width="4" fill="none"/>'
            f'<text x="105" y="40" {FONT_TH} font-size="12" fill="#5a5470" text-anchor="middle">500 ม. = เดินสบาย</text>'
            f'<text x="315" y="62" {FONT_TH} font-size="12" fill="#5a5470" text-anchor="middle">500 ม. = ปีนเนิน</text></g>')
    stat = (f'<g transform="translate(270,140)" {FONT_TH} text-anchor="middle"><rect x="-130" y="-46" width="260" height="76" rx="14" fill="#1d2a3d"/>'
            '<text x="0" y="-8" font-size="30" font-weight="700" fill="#fff">~21 ตร.กม.</text><text x="0" y="16" font-size="13" fill="#9ccbe0">พื้นที่ทั้งเกาะ · ส่วนใหญ่เป็นเขา</text></g>')
    ui = tag('เรื่องที่ 3 · จาก BTS เป็นมอเตอร์ไซค์') + subs('แม้เกาะเต่าจะมีพื้นที่ประมาณ 21 ตารางกิโลเมตร/แต่ภูมิประเทศส่วนใหญ่/เป็นภูเขาและเนินเขา',
                                                          'Koh Tao is only about 21 km²,/but most of it is hills and mountains.')
    return frame(fid, 'ช็อต 9', bg=bg, fg=bkk + tao + labels + prof + stat, ui=ui)


def hill_road(fid, steep=False):
    d = lg(f'{fid}sk', [(0, '#86bde6'), (1, '#e6f0f5')]) + lg(f'{fid}rd', [(0, '#cfc7bc'), (1, '#b7aea2')])
    bg = (f'<rect width="540" height="960" fill="url(#{fid}sk)"/>' + cloud(120, 110, 1) + cloud(420, 160, .7) +
          '<path d="M -20,520 C 80,380 200,300 300,260 C 380,230 460,220 560,230 L 560,960 L -20,960 Z" fill="#6fa46c"/>'
          '<path d="M -20,600 C 100,470 220,380 330,330 C 420,290 480,280 560,282 L 560,960 L -20,960 Z" fill="#5f985e"/>')
    bg += palm(60, 560, .8) + palm(470, 440, .7, True) + boulder(400, 520, 120, 70)
    sign = (f'<g transform="translate(70,520)"><rect x="-4" y="0" width="8" height="120" fill="#6f5d54"/><rect x="-60" y="-50" width="140" height="54" rx="6" fill="#f2eee6"/>'
            f'<text x="10" y="-28" {FONT_TH} font-size="14" font-weight="700" fill="#d8655a" text-anchor="middle">เช่ามอเตอร์ไซค์</text>'
            f'<text x="10" y="-10" {FONT_TH} font-size="12" fill="#3d4f6e" text-anchor="middle">ราคาต่อวัน</text></g>') if not steep else ''
    bg = blur(bg + sign, 2.2)
    road = f'<path d="M 120,960 L 420,960 L 300,300 L 262,300 Z" fill="url(#{fid}rd)"/>' + ''.join(f'<path d="M {270 + (960 - y) * -.01:.0f},{y} L {272:.0f},{y - 30}" stroke="#efe9df" stroke-width="{2 + (y - 300) / 160:.1f}"/>' for y in range(360, 960, 70))
    return d, bg + road


def s10():
    fid = 'f10'
    d, bg = hill_road(fid)
    ch = [sun_char(fid, 250, 330, 1.05, (-200, 100), head='smirktalk', R='R_pointup')]
    ui = tag('เรื่องที่ 3 · จาก BTS เป็นมอเตอร์ไซค์') + subs('500 เมตรเอง/ไม่ต้องเช่ารถหรอก', 'It’s just 500 meters. No need to rent a bike.') + card(330, 90, 170, 'จุดหมาย 500 ม.', 'อยู่บนยอดเนินนั้น', 290, 300)
    return frame(fid, 'ช็อต 10', bg=bg, shadow=CL.contact_shadow(250, 846, 56), chars=ch, light=CL.glow(-30, 90, 380, '#ffffff', .3, core=False), ui=ui, defs=d)


def s11():
    fid = 'f11'
    d, bg = hill_road(fid, steep=True)
    ch = [sun_char(fid, 270, 300, 1.15, (-200, 100), head='pant', R='R_hang')]
    sweat = '<path d="M 286,486 C 300,520 296,560 280,580 C 266,556 270,520 286,486 Z" fill="#26494d" opacity=".45"/>'
    heat = ''.join(f'<path d="M {x},{y} q 6,-10 0,-20 q -6,-10 0,-20" stroke="#fff" stroke-opacity=".5" stroke-width="2" fill="none"/>' for x, y in ((180, 220), (360, 230), (390, 200)))
    ui = tag('เรื่องที่ 3 · จาก BTS เป็นมอเตอร์ไซค์') + subs('แม่ง… เมตรของใครวะ', 'Seriously… whose meters are these?')
    return frame(fid, 'ช็อต 11', bg=bg, shadow=CL.contact_shadow(270, 870, 60), chars=ch, fg=sweat, atmos=heat,
                 light=CL.glow(-30, 90, 380, '#ffffff', .32, core=False), ui=ui, defs=d, ft='rotate(-7 270 480) translate(-30,0) scale(1.12)')


def s12():
    fid = 'f12'
    bg = '<rect width="540" height="960" fill="#1d2a3d"/>' + ''.join(f'<circle cx="{x}" cy="{y}" r="1.2" fill="#2e4058"/>' for x in range(15, 540, 22) for y in range(15, 580, 22))
    tao = (270, 330)
    srcs = [('ยุโรป', 70, 120), ('อเมริกา', 40, 300), ('จีน · เกาหลี · ญี่ปุ่น', 420, 110), ('ออสเตรเลีย', 450, 520), ('อินเดีย', 60, 500), ('ทั่วไทย', 470, 300)]
    arcs = ''
    for t, x, y in srcs:
        mx, my = (x + tao[0]) / 2, min(y, tao[1]) - 80
        arcs += (f'<path d="M {x},{y} Q {mx},{my} {tao[0]},{tao[1]}" stroke="#2fb3b8" stroke-width="2.4" fill="none" stroke-dasharray="5 6"/>'
                 f'<circle cx="{x}" cy="{y}" r="5" fill="#9ccbe0"/>'
                 f'<text x="{x}" y="{y + 22}" {FONT_TH} font-size="13" font-weight="600" fill="#e6eef5" text-anchor="middle">{t}</text>')
    hub = (f'<circle cx="{tao[0]}" cy="{tao[1]}" r="44" fill="#2fb3b8" opacity=".22"/><circle cx="{tao[0]}" cy="{tao[1]}" r="26" fill="#2fb3b8"/>'
           f'<g transform="translate({tao[0]},{tao[1]})"><rect x="-13" y="-8" width="26" height="12" rx="5" fill="#1d2a3d"/><rect x="-10" y="-6" width="20" height="8" rx="3" fill="#9ad7e3"/><path d="M -13,-2 L -18,4 M 13,-2 L 18,4" stroke="#1d2a3d" stroke-width="2.5"/></g>'
           f'<text x="{tao[0]}" y="{tao[1] + 50}" {FONT_TH} font-size="18" font-weight="700" fill="#fff" text-anchor="middle">เกาะเต่า</text>')
    fact = (f'<g transform="translate(270,440)" {FONT_TH} text-anchor="middle"><rect x="-170" y="-14" width="340" height="56" rx="14" fill="#f8f4ec"/>'
            '<text x="0" y="8" font-size="14" font-weight="700" fill="#1a1626">แหล่งเรียนดำน้ำยอดนิยมของโลก</text>'
            '<text x="0" y="28" font-size="12" fill="#5a5470">คนดำน้ำจากทั่วโลกมาเรียนและทำงานที่นี่</text></g>')
    ui = tag('เรื่องที่ 4 · เพื่อนบ้านจากทั่วโลก') + subs('เกาะเต่ามีชื่อเสียงด้านการดำน้ำ/คุณจึงอาจได้ใช้ภาษาอังกฤษ/บ่อยขึ้นในชีวิตประจำวัน',
                                                        'Koh Tao is famous for diving,/so you’ll likely use English a lot more.')
    return frame(fid, 'ช็อต 12', bg=bg, fg=arcs + hub + fact, ui=ui)


def beach_street(fid):
    d = lg(f'{fid}sk', [(0, '#86bde6'), (1, '#eaf2f5')]) + lg(f'{fid}rd', [(0, '#d9d2c8'), (1, '#c6bdb1')])
    bg = f'<rect width="540" height="960" fill="url(#{fid}sk)"/>' + cloud(400, 100, .9)
    shops = ''
    for x, w, c, t in ((-10, 170, '#f2eee6', 'DIVE CENTER'), (170, 150, '#bfe3ee', 'CAFÉ'), (330, 220, '#f6d8cf', 'DIVE SHOP')):
        shops += (f'<rect x="{x}" y="250" width="{w}" height="330" fill="{c}"/><path d="M {x - 8},250 L {x + w / 2},200 L {x + w + 8},250 Z" fill="#8e6b52"/>'
                  f'<rect x="{x + 12}" y="270" width="{w - 24}" height="34" rx="4" fill="#1d2a3d"/><text x="{x + w / 2}" y="293" {FONT_EN} font-size="14" font-weight="700" fill="#fff" text-anchor="middle">{t}</text>'
                  f'<rect x="{x + 20}" y="330" width="{w - 40}" height="150" fill="#3d4f6e" opacity=".55"/>'
                  f'<path d="M {x},520 L {x + w},520 L {x + w - 10},560 L {x + 10},560 Z" fill="#2fb3b8" opacity=".8"/>')
    shops += palm(160, 600, .9) + palm(520, 620, .8, True)
    bg = blur(bg + shops, 2.6)
    road = f'<rect y="580" width="540" height="380" fill="url(#{fid}rd)"/><path d="M 0,580 L 540,580" stroke="#a89f93" stroke-width="4"/>'
    return d, bg + road


def s13():
    fid = 'f13'
    d, bg = beach_street(fid)
    ch = [sun_char(fid, 340, 330, 1.0, (-200, 120), head='smirktalk', L='L_point')]
    tourist = f'<g transform="translate(110,420) scale(1.25)">{R.TOURIST}</g>'
    tf = CL.char_filter(f'{fid}-tour-f', CL.aim((110, 600), (-200, 120)), 'day')
    tour = (tf, f'<g filter="url(#{fid}-tour-f)">{tourist}</g>')
    sh = CL.contact_shadow(340, 822, 52) + CL.contact_shadow(110, 1006, 66)
    ui = (tag('เรื่องที่ 4 · เพื่อนบ้านจากทั่วโลก') +
          subs('(นักท่องเที่ยว) ชายหาดไปทางไหนครับ?/(ซัน) You go ตรงไป แล้วก็… เลี้ยวซ้าย', 'Tourist: Where is the beach?/Sun: You go straight, and then… turn left.'))
    return frame(fid, 'ช็อต 13', bg=bg, shadow=sh, chars=[tour] + ch, light=CL.glow(-30, 100, 380, '#ffffff', .28, core=False), ui=ui, defs=d)


def s14():
    fid = 'f14'
    d = lg(f'{fid}m', [(0, '#efe9f2'), (1, '#d9d3e0')]) + lg(f'{fid}u', [(0, '#5fc3c9'), (1, '#1f6f8e')])
    mall = (f'<rect x="0" y="0" width="270" height="960" fill="url(#{fid}m)"/>'
            + ''.join(f'<rect x="{x}" y="150" width="70" height="300" fill="#c9d6e6" opacity=".8"/><rect x="{x}" y="150" width="70" height="20" fill="#3d4f6e"/>' for x in (10, 100, 190))
            + '<rect x="0" y="480" width="270" height="16" fill="#b9b2c4"/><rect x="0" y="560" width="270" height="400" fill="#cfc8d8"/>'
            + ''.join(f'<rect x="{x}" y="570" width="2" height="390" fill="#bdb6c9"/>' for x in range(30, 270, 50)))
    under = (f'<rect x="270" y="0" width="270" height="960" fill="url(#{fid}u)"/>'
             + ''.join(f'<path d="M {300 + i * 50},0 L {280 + i * 50},500" stroke="#fff" stroke-opacity=".12" stroke-width="14"/>' for i in range(5))
             + '<path d="M 270,720 C 320,680 360,700 400,670 C 440,640 480,690 540,660 L 540,960 L 270,960 Z" fill="#e0c9b8"/>'
             + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f2eee6" opacity=".55"/>' for x, y, r in ((460, 300, 3), (470, 270, 2), (455, 240, 2.5), (380, 200, 2))))
    bg = blur(mall, 2.2) + blur(under, 2.2) + '<rect x="268" y="0" width="4" height="960" fill="#fff"/>'
    ch = [sun_char(fid, 135, 290, .78, (-200, 100), head='shades', camera=False),
          sun_char(fid, 405, 290, .78, (300, -200), head='mask', outfit='wetsuit', camera=False, tote=False)]
    lab = (f'<g {FONT_TH} font-weight="700" text-anchor="middle" font-size="16" fill="#fff" stroke="#0b0812" stroke-width="4" paint-order="stroke">'
           '<text x="135" y="120">วันหยุดแบบเดิม</text><text x="405" y="120">วันหยุดแบบใหม่</text></g>')
    ui = tag('เรื่องที่ 5 · วันหยุดเปลี่ยนไป') + lab + subs('จากที่เคยเดินสยามในวันหยุด/คุณอาจเปลี่ยนมาเรียนดำน้ำ', 'Instead of weekends at Siam,/you might learn to dive.')
    return frame(fid, 'ช็อต 14', bg=bg, shadow=CL.contact_shadow(135, 676, 40), chars=ch, ui=ui, defs=d)


def s15():
    fid = 'f15'
    d = lg(f'{fid}w', [(0, '#7fd3d6'), (.35, '#3fa7b8'), (1, '#123f5c')]) + lg(f'{fid}s', [(0, '#d6eef6'), (1, '#9fd2ea')])
    bg = (f'<rect width="540" height="150" fill="url(#{fid}s)"/><rect y="150" width="540" height="810" fill="url(#{fid}w)"/>'
          '<path d="M 0,150 q 30,-8 60,0 q 30,8 60,0 q 30,-8 60,0 q 30,8 60,0 q 30,-8 60,0 q 30,8 60,0 q 30,-8 60,0 q 30,8 60,0 q 30,-8 60,0" stroke="#fff" stroke-width="3" fill="none"/>'
          + ''.join(f'<path d="M {60 + i * 90},150 L {30 + i * 90},600" stroke="#fff" stroke-opacity=".08" stroke-width="22"/>' for i in range(6)))
    boat = '<g transform="translate(120,146)"><path d="M -50,0 L 50,0 L 38,16 L -40,16 Z" fill="#f2eee6"/><rect x="-20" y="-16" width="40" height="16" fill="#e8e2da"/><path d="M 38,0 L 38,-30" stroke="#d8655a" stroke-width="3"/></g>'
    reef = ('<path d="M 0,760 C 60,720 120,740 170,700 C 230,660 300,720 360,690 C 420,660 480,700 540,680 L 540,960 L 0,960 Z" fill="#d9c2ae"/>'
            '<g transform="translate(110,720)"><path d="M 0,0 C -10,-40 -30,-50 -26,-80 M 0,0 C 6,-36 20,-50 16,-84 M 0,0 C 14,-20 34,-30 40,-56" stroke="#e8735f" stroke-width="9" fill="none" stroke-linecap="round"/></g>'
            '<g transform="translate(300,700)"><ellipse cx="0" cy="0" rx="40" ry="24" fill="#c97fb0"/><ellipse cx="-6" cy="-6" rx="30" ry="14" fill="#dd9cc6"/></g>'
            '<g transform="translate(450,690)"><path d="M 0,0 C -20,-30 -10,-60 0,-90 C 10,-60 20,-30 0,0 Z" fill="#6fbf8a"/><path d="M 20,4 C 10,-24 22,-50 32,-70 C 36,-44 34,-20 20,4 Z" fill="#5aa878"/></g>')
    fish = ''
    rnd = random.Random(8)
    for i in range(22):
        x, y = 300 + rnd.uniform(-90, 120), 420 + rnd.uniform(-60, 60)
        fish += f'<g transform="translate({x:.0f},{y:.0f})"><ellipse cx="0" cy="0" rx="8" ry="4" fill="#f6c86a"/><path d="M -7,0 L -13,-4 L -13,4 Z" fill="#f6c86a"/><circle cx="4" cy="-1" r="1" fill="#1a1626"/></g>'
    fish = fish.replace('#f6c86a', '#f2a65a')       # warm coral-orange fish, not yellow
    diver = ('<g transform="translate(170,420) rotate(-12)"><rect x="-40" y="-10" width="80" height="22" rx="10" fill="#1f2b46"/><rect x="-30" y="-18" width="34" height="12" rx="5" fill="#9aa3b4"/>'
             f'<circle cx="52" cy="0" r="13" fill="{R.SK}"/><rect x="44" y="-6" width="18" height="9" rx="3" fill="#9ad7e3" stroke="#22303f" stroke-width="2"/>'
             '<path d="M -40,0 L -70,-10 L -74,6 Z M -40,8 L -68,18 L -66,30 Z" fill="#2fb3b8"/>'
             + ''.join(f'<circle cx="{62 + i * 4}" cy="{-20 - i * 18}" r="{3 - i * .4:.1f}" fill="#fff" opacity=".7"/>' for i in range(5)) + '</g>')
    depth = ''.join(f'<g {FONT_EN}><path d="M 500,{y} L 530,{y}" stroke="#fff" stroke-opacity=".7" stroke-width="2"/><text x="494" y="{y + 4}" font-size="12" fill="#fff" text-anchor="end">{t}</text></g>'
                    for y, t in ((150, '0 m'), (330, '5 m'), (520, '12 m'), (690, '18 m')))
    ui = (tag('เรื่องที่ 5 · วันหยุดเปลี่ยนไป') + card(280, 210, 200, 'ใบดำน้ำขั้นแรก', 'ดำได้ลึกไม่เกิน 18 เมตร', 505, 690) +
          subs('และค้นพบโลกอีกใบ/ที่อยู่ใต้ผิวน้ำ', 'and find a whole world under the surface.'))
    return frame(fid, 'ช็อต 15', bg=bg, fg=boat + reef + fish + diver + depth, ui=ui, defs=d)


def cafe(fid):
    d, bg = sea_sky(fid, 380)
    bg += boulder(30, 420, 140, 60) + boulder(420, 410, 140, 50)
    bg = blur(bg + palm(490, 560, .9, True), 2.6)
    floor = '<rect y="560" width="540" height="400" fill="#c9a888"/>' + ''.join(f'<rect y="{560 + i * 30}" width="540" height="2" fill="#b08f70"/>' for i in range(14))
    return d, bg + floor


TABLE = ('<path d="M 30,600 L 510,600 L 540,660 L 0,660 Z" fill="#9c785e"/><rect x="0" y="660" width="540" height="20" fill="#7d5f4a"/>'
         '<rect x="60" y="680" width="16" height="280" fill="#6f5442"/><rect x="464" y="680" width="16" height="280" fill="#6f5442"/>')


def laptop(x, y):
    return (f'<g transform="translate({x},{y})"><path d="M -90,0 L 90,0 L 104,22 L -104,22 Z" fill="#c8ccd6"/>'
            f'<path d="M -84,0 L 84,0 L 74,-120 L -74,-120 Z" fill="#9aa1b0"/><path d="M -76,-6 L 76,-6 L 68,-112 L -68,-112 Z" fill="#2c3448"/>'
            f'<circle cx="0" cy="-62" r="8" fill="#e8edf5"/></g>')


def notif(x, y, title, body, col='#d8655a', s=1.0, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {FONT_TH}><rect x="0" y="0" width="200" height="52" rx="12" fill="#f8f4ec" opacity=".97"/>'
            f'<rect x="10" y="10" width="32" height="32" rx="8" fill="{col}"/><text x="52" y="24" font-size="13" font-weight="700" fill="#1a1626">{title}</text>'
            f'<text x="52" y="41" font-size="11" fill="#5a5470">{body}</text><circle cx="196" cy="4" r="9" fill="#e5484d"/>'
            f'<text x="196" y="8" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">!</text></g>')


def s16():
    fid = 'f16'
    d, bg = cafe(fid)
    ch = [sun_char(fid, 270, 360, 1.15, (-220, 120), head='smirk', L='table', R='R_hang', front='R_coffee', camera=False, tote=False)]
    fg = TABLE + drop(laptop(250, 630), 8, 8, .3) + laptop(250, 630)
    pops = notif(30, 120, 'อีเมลงาน', 'แก้ไฟล์ด่วนก่อนเที่ยง', '#5a6c8e', .95, -3) + notif(300, 190, 'แชทลูกค้า', '“ว่างคุยไหมครับ”', '#2fb3b8', .9, 4)
    light = CL.glow(-30, 120, 380, '#ffffff', .3, core=False) + CL.shaft([(0, 60), (160, 0), (420, 640), (200, 700)], '#fff8ee', .14, src=(60, 40), end=(330, 640), dust_n=30, seed=4)
    ui = tag('เรื่องที่ 6 · ชีวิตการทำงานเปลี่ยนไป') + pops + subs('คุณอาจทำงานเกี่ยวกับการท่องเที่ยว/หรือถ้าทำงานออนไลน์ได้/ก็อาจย้ายโต๊ะทำงานมาไว้ริมทะเล',
                                                                  'You might work in tourism,/or if you work online, move your desk to the beach.')
    return frame(fid, 'ช็อต 16', bg=bg, chars=ch, fg=fg, light=light, ui=ui, defs=d)


def s17():
    fid = 'f17'
    d, bg = cafe(fid)
    ch = [sun_char(fid, 270, 360, 2.4, (-240, 160), head='annoy', L='table', R='R_hang', camera=False, tote=False)]
    pops = (notif(20, 90, 'อีเมลงาน', 'แก้ไฟล์ด่วนก่อนเที่ยง', '#5a6c8e', .9, -6) + notif(330, 120, 'แชทลูกค้า', '“ว่างคุยไหมครับ”', '#2fb3b8', .85, 5) +
            notif(10, 250, 'ประชุมด่วน', 'อีก 5 นาที', '#d8655a', .85, 3) + notif(340, 300, 'งานใหม่', 'กำหนดส่งพรุ่งนี้', '#7a5ab8', .9, -4) +
            notif(170, 40, 'แจ้งเตือน (12)', 'ยังไม่ได้อ่าน', '#e5484d', .9, 2))
    ui = tag('เรื่องที่ 6 · ชีวิตการทำงานเปลี่ยนไป') + pops + subs('ย้ายมาไกลขนาดนี้/ยังตามกูมาอีก', 'I moved this far…/and it still found me.')
    return frame(fid, 'ช็อต 17', bg=blur(bg, 3.6), chars=ch, light=CL.glow(-30, 160, 360, '#ffffff', .24, core=False), ui=ui, defs=d)


def s18():
    fid = 'f18'
    d = (lg(f'{fid}sk', [(0, '#8fb3dc'), (.6, '#e9d6dc'), (1, '#f6e4da')]) + lg(f'{fid}se', [(0, '#7fbcc8'), (1, '#4f9fb2')]) +
         lg(f'{fid}sa', [(0, '#efe4d6'), (1, '#e2d2c0')]))
    bg = (f'<rect width="540" height="430" fill="url(#{fid}sk)"/>' + cloud(380, 130, 1, .8) + cloud(120, 200, .7, .7) +
          '<circle cx="430" cy="380" r="46" fill="#fff4ea" opacity=".9"/>' +
          f'<rect y="430" width="540" height="160" fill="url(#{fid}se)"/><path d="M 0,590 C 120,570 260,600 540,575 L 540,960 L 0,960 Z" fill="url(#{fid}sa)"/>')
    bg = blur(bg + boulder(10, 470, 130, 60), 2.0)
    palms = palm(40, 640, 1.05) + palm(510, 640, 1.05, True)
    hammock = ('<path d="M 70,560 C 170,700 370,700 470,560" stroke="#efe6d8" stroke-width="4" fill="none"/>'
               '<path d="M 90,580 C 190,720 350,720 450,580 C 400,660 140,660 90,580 Z" fill="#2fb3b8"/>'
               '<path d="M 90,580 C 190,720 350,720 450,580 C 420,640 380,660 330,664 C 260,670 160,650 90,580 Z" fill="#3fc0c4"/>'
               + ''.join(f'<path d="M {110 + i * 40},{600 + abs(i - 4) * -4 + 30} L {120 + i * 40},{690 - abs(i - 4) * 8}" stroke="#f2eee6" stroke-width="1.6" opacity=".6"/>' for i in range(9)))
    sun = R.body(head='grin', L='L_hang', R='R_hang', camera=False, tote=False)
    f = CL.char_filter(f'{fid}-sun-f', CL.aim((270, 600), (430, 380)), 'day')
    ch = (f, f'<g filter="url(#{fid}-sun-f)"><g transform="translate(170,462) rotate(-78) scale(.56)">{sun}</g></g>')
    hammock = f'<g transform="translate(0,-150)">{hammock}</g>'
    front = '<path d="M 140,640 C 220,720 340,716 420,640 C 360,700 200,700 140,640 Z" fill="#2fb3b8" opacity=".95" transform="translate(0,-150)"/>'
    light = CL.glow(430, 380, 300, '#ffd9b8', .32) + CL.shaft([(430, 380), (470, 380), (330, 960), (120, 960)], '#ffe2c8', .12, src=(440, 380), end=(250, 900), dust_n=26, seed=6)
    ui = tag('ปิดเรื่อง') + subs('ชีวิตบนเกาะอาจไม่ได้สบายขึ้นทุกอย่าง/แต่ชีวิตประจำวันของคุณจะไม่เหมือนเดิม',
                                'Island life isn’t easier in every way,/but your everyday life won’t be the same.')
    return frame(fid, 'ช็อต 18', bg=bg, shadow=CL.contact_shadow(270, 690, 120, 12, .6), chars=[ch], fg=hammock + front + palms, light=light, ui=ui, defs=d)


def s19():
    fid = 'f19'
    base = s18().split('<g id="L-ui">')[0]
    q = (f'<g {FONT_TH}><rect x="40" y="120" width="460" height="230" rx="18" fill="#120e1c" fill-opacity=".9" stroke="#9a86ff" stroke-opacity=".7"/>'
         '<text x="270" y="166" font-size="20" font-weight="700" fill="#fff" text-anchor="middle">แล้วคุณล่ะ จะเลือกทางไหน?</text>'
         '<rect x="64" y="190" width="412" height="56" rx="12" fill="#f6f2fb"/><rect x="64" y="190" width="412" height="56" rx="12" fill="none" stroke="#ffd84a" stroke-width="3"/>'
         '<text x="86" y="225" font-size="16" font-weight="700" fill="#7a5ab8">A</text><text x="110" y="225" font-size="16" font-weight="600" fill="#1a1626">ย้ายเลย ทะเลรออยู่</text>'
         '<rect x="64" y="262" width="412" height="56" rx="12" fill="#f6f2fb" fill-opacity=".75"/>'
         '<text x="86" y="297" font-size="16" font-weight="700" fill="#7a5ab8">B</text><text x="110" y="297" font-size="16" font-weight="600" fill="#1a1626">ขออยู่กรุงเทพกับรถติดต่อ</text></g>')
    ui = q + subs('แล้วคุณล่ะ/อยากลองทิ้งความเป็น Bangkok Native ดูไหม?', 'What about you?/Would you leave Bangkok behind? Comment A or B.')
    return base.replace('aria-label="ช็อต 18"', 'aria-label="ช็อต 19"') + f'<g id="L-ui">{ui}{EYE_MARK}</g></svg>'


SHOTS = [
    (s01, '00:00–00:05', 'เปิดเรื่อง · เก็บกระเป๋า', 'ผู้บรรยาย', 'ห้องคอนโดกลางวัน หน้าต่างเห็นตึก BTS และรถติด ซันหน้าตายยืนข้างกระเป๋าเดินทางที่เปิดอยู่ ดนตรีชะชะช่าเริ่ม'),
    (s02, '00:05–00:09', 'ชื่อเรื่อง · ออกจากห้อง', 'ซัน', 'ซันใส่แว่นกันแดด ลากกระเป๋าเดินออกประตูอย่างมั่นใจ ชื่อตอนขึ้นพร้อมจังหวะ ชะ ชะ ช่า'),
    (s03, '00:09–00:16', 'แผนที่ · ไม่มีสนามบิน', 'ผู้บรรยาย', 'Animated map: ซูมจากกรุงเทพ ลากเส้นลงชุมพร แล้วซูมเข้ากรอบขยาย เรือแล่นจากท่าเรือไปเกาะเต่า ป้าย “ไม่มีสนามบิน”'),
    (s04, '00:16–00:20', 'บนเรือ · ยังพยายามเท่', '—', 'ซันนั่งริมราวเรือ ผมปลิว แว่นกันแดดเอียง หน้ายังนิ่งพยายามเท่ ละอองน้ำกับเส้นลม (มุกภาพ ไม่มีบทพูด)'),
    (s05, '00:20–00:26', 'กราฟิก · เส้นทางพัสดุ', 'ผู้บรรยาย', 'Process animation: กล่องพัสดุวิ่งจากโกดัง → รถบรรทุก → ท่าเรือชุมพร → เรือโคลงกลางคลื่นลม'),
    (s06, '00:26–00:28', 'โทรตามของ', 'ซัน', 'ระเบียงบ้านไม้บนเกาะ ซันยกมือถือแนบหู ถามแบบสบาย ๆ'),
    (s07, '00:28–00:30', 'ปลายสาย', 'พนักงาน (เสียง)', 'กล้องตัดไปที่จอโทรศัพท์ขณะพนักงานพูด คลื่นเสียงขยับตามเสียง สถานะพัสดุค้างที่ชุมพร'),
    (s08, '00:30–00:32', 'มุกเงียบ', 'ซัน', 'ใกล้หน้าซัน หน้าตาย เว้นจังหวะเงียบครึ่งวินาทีก่อนพูด แล้วตัดเข้าหัวข้อถัดไปด้วยจังหวะชะชะช่า'),
    (s09, '00:32–00:38', 'Isometric · ราบ vs เนิน', 'ผู้บรรยาย', 'เทียบกรุงเทพที่ราบกับเกาะเต่าที่เป็นเนิน เส้นทาง 500 ม. ของแต่ละที่ และป้าย ~21 ตร.กม.'),
    (s10, '00:38–00:41', 'มั่นใจ', 'ซัน', 'ตีนเนิน ป้ายเช่ามอเตอร์ไซค์ด้านหลัง ซันชี้ขึ้นยอดเนินแบบมั่นใจ'),
    (s11, '00:41–00:45', 'กลางเนิน', 'ซัน', 'ตัดภาพชนทันที กล้องเอียงให้เห็นความชัน ซันหอบ เหงื่อแตก เสื้อเปียก แล้วชะชะช่าเล่นตบมุก'),
    (s12, '00:45–00:51', 'กราฟิก · คนจากทั่วโลก', 'ผู้บรรยาย', 'เส้นทางนักท่องเที่ยวจากทั่วโลกพุ่งเข้าเกาะเต่า ไอคอนหน้ากากดำน้ำ การ์ดข้อมูลแหล่งเรียนดำน้ำ'),
    (s13, '00:51–00:57', 'ถามทาง', 'นักท่องเที่ยว → ซัน', 'ถนนริมหาดหน้าร้านดำน้ำ นักท่องเที่ยวเดินเข้าเฟรมจากซ้าย (เห็นด้านหลัง) ซันชี้ทางอย่างมั่นใจ ภาษาอังกฤษปนไทย บทสั้นต่อกันจึงใช้ภาพสองคน'),
    (s14, '00:57–01:02', 'เทียบวันหยุด', 'ผู้บรรยาย', 'Animated comparison: ซันท่าเดิมเป๊ะ ซ้ายเดินห้าง ขวาในชุดดำน้ำ เส้นแบ่งกลางเลื่อนจากซ้ายไปขวา'),
    (s15, '01:02–01:08', 'ภาพตัดขวางใต้ทะเล', 'ผู้บรรยาย', 'Cross-section: กล้องเลื่อนลงจากผิวน้ำ นักดำน้ำ ฝูงปลา แนวปะการัง ขีดบอกความลึก'),
    (s16, '01:08–01:15', 'โต๊ะทำงานริมทะเล', 'ผู้บรรยาย', 'คาเฟ่ริมทะเล ซันจิบกาแฟหน้าโน้ตบุ๊ก ยิ้มสบาย แล้วแจ้งเตือนเริ่มเด้ง'),
    (s17, '01:15–01:21', 'งานตามมา', 'ซัน', 'แจ้งเตือนเด้งรัว ดนตรีหยุด ซูมเข้าหน้าซันที่หน้าบึ้ง พูดเสียงเรียบ แล้วดนตรีกลับเข้าชะชะช่า'),
    (s18, '01:21–01:26', 'เปลริมทะเล', 'ผู้บรรยาย', 'ช่วงบ่ายแก่ ซันนอนเปลระหว่างต้นมะพร้าว ยิ้มสบาย แสงอุ่นจากดวงอาทิตย์ด้านขวา'),
    (s19, '01:26–01:30', 'การ์ดคำถาม A/B', 'ผู้บรรยาย', 'การ์ดตัวเลือก A/B ไฮไลต์สลับไปมาพร้อมเสียงคลิก เว้นเวลาให้คนดูเลือก ดนตรีชะชะช่าปิดท้าย ตามด้วย outro'),
]


def build():
    figs = ''
    for i, (fn, t, title, who, note) in enumerate(SHOTS, 1):
        svg = fn()
        figs += (f'<figure>{svg}<figcaption><span class="n">ช็อต {i} · {t}</span><b>{title}</b>'
                 f'<span class="who">เสียง: {who}</span><span class="note">{note}</span></figcaption></figure>')
    page = f'''<title>Odd Hours EP.01 เกาะเต่า</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: storyboard grid of 9:16 stills, 4 across on desktop, 2 on tablet, 1 on phone. Single dark look by choice, like the other Odd Hours boards. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#9a86ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:18px; }}
header {{ display:flex; flex-wrap:wrap; gap:12px; align-items:baseline; justify-content:space-between; }}
h1 {{ font-size:18px; font-weight:500; margin:0; text-wrap:balance; }}
h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.tools {{ display:flex; gap:8px; flex-wrap:wrap; }}
.tools button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:8px; padding:6px 12px; cursor:pointer; }}
.tools button[aria-pressed="true"] {{ border-color:var(--accent); }}
.grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:18px; }}
@media (max-width:980px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; aspect-ratio:9/16; border-radius:6px; box-shadow:0 0 0 1px var(--line); overflow:hidden; }}
figcaption {{ display:grid; gap:3px; font-size:13px; line-height:1.55; }}
.n {{ font-size:11px; letter-spacing:.04em; color:var(--accent); }}
.who {{ color:#ffd84a; font-size:12px; }}
.note {{ color:var(--muted); font-size:12px; }}
.nosubs .subs, .noinfo .info {{ display:none; }}
.guide {{ display:none; }} .showguide .guide {{ display:inline; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600;700&family=Inter:wght@500;700&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{R.HEAD_DEFS}{SHARED_DEFS}</defs></svg>
<div class="wrap" id="board">
  <header><h1>เมื่อ Bangkok Native ย้ายไปอยู่เกาะเต่า<span>Odd Hours · EP.01 · สตอรี่บอร์ด 19 ช็อต · ราว 90 วินาที · ยังไม่พากย์</span></h1>
  <div class="tools"><button data-c="nosubs" aria-pressed="true">ซับ</button><button data-c="noinfo" aria-pressed="true">กราฟิก</button><button data-c="showguide" aria-pressed="false">แสดงพื้นที่ซับ</button></div></header>
  <div class="grid">{figs}</div>
</div>
<script>
document.querySelectorAll('svg[role=img]').forEach(s => s.insertAdjacentHTML('beforeend', '<rect class="guide" x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/>'));
document.querySelectorAll('.tools button').forEach(b => b.addEventListener('click', () => {{
  const c = b.dataset.c, on = b.getAttribute('aria-pressed') !== 'true';
  b.setAttribute('aria-pressed', on);
  document.getElementById('board').classList.toggle(c, c === 'showguide' ? on : !on);
}}));
</script>
'''
    out = os.path.join(HERE, 'storyboard.html')
    open(out, 'w').write(page)
    print(out, len(page))


if __name__ == '__main__':
    build()
