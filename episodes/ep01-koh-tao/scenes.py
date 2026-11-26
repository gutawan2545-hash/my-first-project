"""EP.01 scene art, second pass: layered depth, block-shaded props, real light patterns.
Each function returns (defs, bg, fg, shadow, light) in 540x960 frame units."""
import math, random

FONT_EN = 'font-family="Inter, system-ui, sans-serif"'


def G(id_, stops, x1=0, y1=0, x2=0, y2=1):
    s = ''.join(f'<stop offset="{st[0]}" stop-color="{st[1]}"' + (f' stop-opacity="{st[2]}"' if len(st) > 2 else '') + '/>' for st in stops)
    return f'<linearGradient id="{id_}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">{s}</linearGradient>'


def RG(id_, stops, cx=.5, cy=.5, r=.5):
    s = ''.join(f'<stop offset="{st[0]}" stop-color="{st[1]}"' + (f' stop-opacity="{st[2]}"' if len(st) > 2 else '') + '/>' for st in stops)
    return f'<radialGradient id="{id_}" cx="{cx}" cy="{cy}" r="{r}">{s}</radialGradient>'


def blur(c, sd=1):
    return f'<g filter="url(#sb-dof{"2" if sd > 1 else ""})">{c}</g>'


def castsh(shape, dx=12, dy=14, op=.3):
    return f'<g transform="translate({dx},{dy})" opacity="{op}" filter="url(#sb-sh)" style="mix-blend-mode:multiply">{shape}</g>'


def cumulus(x, y, s=1.0, op=1.0):
    """Puffy cloud: lit top, cool lavender underside (block steps, no outline)."""
    return (f'<g transform="translate({x},{y}) scale({s})" opacity="{op}">'
            '<ellipse cx="0" cy="8" rx="70" ry="16" fill="#d9e2f0"/>'
            '<circle cx="-36" cy="-4" r="24" fill="#f7f9fc"/><circle cx="-8" cy="-18" r="32" fill="#ffffff"/>'
            '<circle cx="28" cy="-8" r="26" fill="#f7f9fc"/><circle cx="52" cy="2" r="16" fill="#eef2f8"/>'
            '<path d="M -64,8 C -40,20 40,22 68,8 C 50,16 -40,16 -64,8 Z" fill="#c9d3e6"/>'
            '<circle cx="-14" cy="-26" r="14" fill="#ffffff"/></g>')


def palm(x, y, s=1.0, flip=False, tone=0):
    lv = [('#2f6b5a', '#3f8a6e', '#4fa07c'), ('#285e50', '#357a62', '#438f70')][tone]
    f = -1 if flip else 1
    out = (f'<path d="M 0,0 C {6 * f},-60 {18 * f},-120 {34 * f},-170 L {42 * f},-168 C {28 * f},-118 {16 * f},-60 11,0 Z" fill="#8a7462"/>'
           f'<path d="M 6,0 C {10 * f},-60 {22 * f},-118 {38 * f},-169 L {42 * f},-168 C {28 * f},-118 {16 * f},-60 11,0 Z" fill="#6c5a4c"/>'
           + ''.join(f'<path d="M {2 + i * 1.6 * f:.1f},{-i * 17} l {9 * f},-3" stroke="#5e4c40" stroke-width="1.6"/>' for i in range(1, 10)))
    cx, cy = 38 * f, -170
    for k, (ang, ln) in enumerate(((-170, 78), (-135, 70), (-100, 52), (-60, 70), (-25, 80), (15, 66), (165, 70), (195, 60))):
        a = math.radians(ang)
        ex, ey = cx + math.cos(a) * ln * f, cy + math.sin(a) * ln * .5 + 24
        mx, my = cx + math.cos(a) * ln * .5 * f, cy + math.sin(a) * ln * .32 - 12
        col = lv[k % 3]
        out += f'<path d="M {cx},{cy} Q {mx:.0f},{my - 16:.0f} {ex:.0f},{ey:.0f} Q {mx:.0f},{my + 6:.0f} {cx},{cy + 4} Z" fill="{col}"/>'
        out += f'<path d="M {cx},{cy} Q {mx:.0f},{my - 10:.0f} {ex:.0f},{ey:.0f}" stroke="#1f4a3d" stroke-width="1.2" fill="none" opacity=".5"/>'
    out += f'<circle cx="{cx - 4 * f}" cy="{cy + 8}" r="6" fill="#6c5a4c"/><circle cx="{cx + 5 * f}" cy="{cy + 10}" r="5.5" fill="#5e4c40"/>'
    return f'<g transform="translate({x},{y}) scale({s})">{out}</g>'


def boulder(x, y, w, h, tone=0):
    c, cs, ch = [('#a9a5a9', '#86828a', '#c9c5c8'), ('#9a969c', '#7a7680', '#bcb8bc')][tone]
    return (f'<path d="M {x},{y} C {x + w * .05},{y - h * .9} {x + w * .4},{y - h} {x + w * .6},{y - h * .95} C {x + w * .9},{y - h * .85} {x + w},{y - h * .3} {x + w},{y} Z" fill="{c}"/>'
            f'<path d="M {x + w * .55},{y - h * .95} C {x + w * .9},{y - h * .85} {x + w},{y - h * .3} {x + w},{y} L {x + w * .62},{y} C {x + w * .72},{y - h * .4} {x + w * .7},{y - h * .7} {x + w * .55},{y - h * .95} Z" fill="{cs}"/>'
            f'<path d="M {x + w * .1},{y - h * .6} C {x + w * .2},{y - h * .9} {x + w * .4},{y - h * .97} {x + w * .5},{y - h * .95} C {x + w * .3},{y - h * .8} {x + w * .2},{y - h * .6} {x + w * .16},{y - h * .4} Z" fill="{ch}"/>'
            f'<path d="M {x + w * .3},{y - h * .5} l {w * .12},{h * .25}" stroke="{cs}" stroke-width="1.5" opacity=".7"/>')


def sea(fid, y0, y1, far='#1f78a6', mid='#2fa2c0', near='#5ccbc9', seed=3):
    rnd = random.Random(seed)
    out = f'<rect y="{y0}" width="540" height="{y1 - y0}" fill="url(#{fid}sea)"/>'
    for i in range(26):                                   # wave strokes, smaller toward the horizon
        t = (i / 26) ** 1.7
        y = y0 + 6 + t * (y1 - y0 - 10)
        w = 10 + t * 70
        x = rnd.uniform(-20, 540)
        out += f'<path d="M {x:.0f},{y:.0f} q {w / 2:.0f},{-2 - t * 5:.1f} {w:.0f},0" stroke="#ffffff" stroke-opacity="{.35 + t * .3:.2f}" stroke-width="{1 + t * 2:.1f}" fill="none" stroke-linecap="round"/>'
    for i in range(5):                                    # soft light bands (no sparkles)
        y = y0 + 8 + i * (y1 - y0) / 6
        out += f'<rect x="0" y="{y:.0f}" width="540" height="{3 + i:.0f}" fill="#ffffff" opacity=".10"/>'
    return G(f'{fid}sea', [(0, far), (.45, mid), (1, near)]), out


# ================================================================ condo, Bangkok
def condo(fid):
    d = (G(f'{fid}sky', [(0, '#8fbde6'), (1, '#e4edf4')]) + G(f'{fid}wall', [(0, '#ece6ea'), (1, '#e0d8de')], 0, 0, 1, 0) +
         G(f'{fid}fl', [(0, '#cdae92'), (1, '#b38f72')]) + G(f'{fid}glass', [(0, '#ffffff', .0), (.5, '#ffffff', .22), (1, '#ffffff', 0)], 0, 0, 1, 1))
    rnd = random.Random(11)
    view = f'<rect x="20" y="110" width="320" height="460" fill="url(#{fid}sky)"/>' + cumulus(110, 180, .7) + cumulus(280, 150, .5, .9)
    for i in range(12):                                   # far towers
        x = 10 + i * 30 + rnd.randint(-6, 6); h = rnd.randint(120, 230)
        view += f'<rect x="{x}" y="{420 - h}" width="{rnd.randint(18, 28)}" height="{h}" fill="#b8c7da"/>'
    for i in range(7):                                    # mid towers, lit face + shade face + window grid
        x = 10 + i * 50 + rnd.randint(-8, 8); h = rnd.randint(150, 260); w = rnd.randint(30, 42)
        view += (f'<rect x="{x}" y="{430 - h}" width="{w}" height="{h}" fill="#9fb2cb"/><rect x="{x + w * .62:.0f}" y="{430 - h}" width="{w * .38:.0f}" height="{h}" fill="#8599b5"/>'
                 + ''.join(f'<rect x="{x + 4}" y="{wy}" width="{w * .55:.0f}" height="3" fill="#d6e1ee" opacity=".8"/>' for wy in range(430 - h + 10, 424, 11)))
    view += ('<rect x="290" y="150" width="60" height="420" fill="#7d8fab"/><rect x="290" y="150" width="22" height="420" fill="#93a6c2"/>'
             + ''.join(f'<rect x="296" y="{y}" width="48" height="4" fill="#c7d4e4" opacity=".7"/>' for y in range(160, 560, 14)))
    # rain trees + road + traffic
    view += ''.join(f'<ellipse cx="{x}" cy="452" rx="{r}" ry="{r * .7:.0f}" fill="{c}"/>' for x, r, c in ((40, 26, '#6f9e6a'), (110, 30, '#5f9060'), (200, 24, '#6f9e6a'), (270, 28, '#5f9060')))
    view += '<rect x="20" y="470" width="320" height="100" fill="#8c909c"/><rect x="20" y="512" width="320" height="3" fill="#e9e6df" opacity=".8"/>'
    cars = ['#e88aa8', '#eef0f4', '#c9cfd8', '#d8655a', '#e88aa8', '#3c4458', '#eef0f4', '#2f6fb5']
    for row, y in ((0, 478), (1, 520)):
        for i in range(7):
            x = 14 + i * 48 + row * 20
            c = cars[(i + row * 3) % len(cars)]
            view += (f'<rect x="{x}" y="{y}" width="38" height="20" rx="6" fill="{c}"/><rect x="{x + 7}" y="{y - 8}" width="22" height="11" rx="4" fill="{c}"/>'
                     f'<rect x="{x + 9}" y="{y - 6}" width="18" height="7" rx="2" fill="#5a6c8e" opacity=".8"/><circle cx="{x + 3}" cy="{y + 12}" r="2.2" fill="#ff7a6a"/>')
    # BTS viaduct + train
    view += ('<rect x="20" y="404" width="320" height="16" fill="#cdd2db"/><rect x="20" y="420" width="320" height="7" fill="#9aa1b0"/>'
             + ''.join(f'<rect x="{x}" y="427" width="12" height="50" fill="#a9afbd"/><rect x="{x + 8}" y="427" width="4" height="50" fill="#8a91a0"/>' for x in (60, 190, 310))
             + '<rect x="70" y="380" width="200" height="24" rx="8" fill="#eef1f5"/><rect x="70" y="394" width="200" height="4" fill="#2f6fb5"/>'
             + ''.join(f'<rect x="{80 + i * 22}" y="384" width="15" height="8" rx="2" fill="#3a4b6a"/>' for i in range(8)))
    win = (f'<clipPath id="{fid}wc"><rect x="20" y="110" width="320" height="460"/></clipPath>'
           f'<g clip-path="url(#{fid}wc)">{blur(view, 1)}<rect x="20" y="110" width="320" height="460" fill="url(#{fid}glass)"/>'
           '<path d="M 60,110 L 140,110 L 40,570 L 20,570 L 20,300 Z" fill="#fff" opacity=".10"/><path d="M 200,110 L 230,110 L 140,570 L 120,570 Z" fill="#fff" opacity=".08"/></g>'
           '<g fill="#2b2d36"><rect x="14" y="104" width="332" height="8"/><rect x="14" y="566" width="332" height="10"/><rect x="14" y="104" width="8" height="472"/><rect x="338" y="104" width="8" height="472"/>'
           '<rect x="176" y="104" width="6" height="472"/><rect x="14" y="216" width="332" height="5"/></g>'
           '<rect x="14" y="576" width="340" height="10" fill="#d6ccd2"/>')
    curtain = ('<path d="M 330,90 L 400,90 L 404,600 L 326,600 Z" fill="#f8f6f4" opacity=".86"/>'
               + ''.join(f'<path d="M {336 + i * 13},96 C {338 + i * 13},300 {334 + i * 13},450 {338 + i * 13},598" stroke="#ddd6da" stroke-width="5" fill="none" opacity=".8"/>' for i in range(5))
               + '<rect x="0" y="84" width="420" height="8" rx="3" fill="#9aa1b0"/>')
    wall = (f'<rect width="540" height="610" fill="url(#{fid}wall)"/><path d="M 470,0 L 540,0 L 540,610 L 470,610 Z" fill="#d6ccd6"/>'
            '<rect y="596" width="540" height="14" fill="#f2eef0"/><rect y="606" width="540" height="4" fill="#cfc4c8"/>')
    poster = ('<g><rect x="396" y="150" width="104" height="146" fill="#1f3b40"/><circle cx="448" cy="208" r="30" fill="#e8735f"/>'
              '<rect x="396" y="232" width="104" height="64" fill="#2f5a5e"/><path d="M 396,250 q 26,-10 52,0 q 26,10 52,0 L 500,296 L 396,296 Z" fill="#3f7a7e"/>'
              f'<text x="448" y="282" {FONT_EN} font-size="12" font-weight="700" fill="#f2eee6" text-anchor="middle">ODD NIGHTS</text>'
              '<rect x="392" y="146" width="112" height="154" fill="none" stroke="#1b1d24" stroke-width="4"/></g>')
    plant = ('<g transform="translate(70,700)"><path d="M -30,0 L 30,0 L 24,-56 L -24,-56 Z" fill="#c98b6c"/><path d="M 6,0 L 30,0 L 24,-56 L 10,-56 Z" fill="#a8725a"/>'
             '<rect x="-27" y="-62" width="54" height="8" rx="3" fill="#b77d62"/>'
             + ''.join(f'<path d="M 0,-60 Q {dx * .5:.0f},{-100 + dy * .3:.0f} {dx},{dy - 120} Q {dx * .9:.0f},{dy - 80} 0,-60 Z" fill="{c}"/>' for dx, dy, c in ((-60, -40, '#2f6b5a'), (50, -60, '#3f8a6e'), (-20, -110, '#3f8a6e'), (30, -10, '#2f6b5a'), (-56, 30, '#3f8a6e')))
             + '</g>')
    bed = ('<path d="M 300,560 L 560,560 L 560,700 L 300,700 Z" fill="#a07e64"/><path d="M 300,560 L 560,560 L 560,574 L 300,574 Z" fill="#b8957a"/>'
           '<rect x="306" y="520" width="254" height="56" rx="10" fill="#f4f1f2"/>'
           '<path d="M 296,560 C 360,540 470,548 560,540 L 560,640 C 470,650 380,646 300,648 Z" fill="#cfcadf"/>'
           '<path d="M 296,560 C 360,540 470,548 560,540 L 560,560 C 470,566 380,566 300,580 Z" fill="#dedaea"/>'
           '<path d="M 330,600 C 380,590 430,610 480,598" stroke="#b8b2cc" stroke-width="3" fill="none"/>'
           '<rect x="456" y="470" width="96" height="58" rx="18" fill="#f8f6f6"/><rect x="456" y="510" width="96" height="18" rx="9" fill="#e6e1e6"/>')
    suitcase = ('<g><path d="M 340,560 L 470,560 L 462,600 L 348,600 Z" fill="#2c3a54"/><path d="M 340,560 L 470,560 L 470,568 L 340,568 Z" fill="#3d4f6e"/>'
                '<path d="M 350,560 L 410,560 L 404,586 L 352,586 Z" fill="#f2eee6"/><path d="M 352,572 L 404,572" stroke="#d8d2c6" stroke-width="2"/>'
                '<path d="M 412,560 L 464,560 L 458,584 L 418,586 Z" fill="#2f5a5e"/><path d="M 418,566 l 4,4 m 8,-4 l 4,4 m 8,-4 l 4,4" stroke="#e9e1d0" stroke-width="1.5"/>'
                '<path d="M 346,560 L 466,560 L 452,488 L 360,488 Z" fill="#46597a"/><path d="M 346,560 L 380,560 L 376,488 L 360,488 Z" fill="#56698a"/>'
                '<rect x="420" y="548" width="26" height="10" rx="4" fill="#141218"/><rect x="434" y="548" width="12" height="10" rx="4" fill="#141218"/></g>')
    floor = (f'<rect y="610" width="540" height="350" fill="url(#{fid}fl)"/>'
             + ''.join(f'<path d="M {270 + (x - 270) * .32:.0f},610 L {x},960" stroke="#a88568" stroke-width="1.6"/>' for x in range(-400, 940, 70))
             + ''.join(f'<path d="M 0,{y} L 540,{y}" stroke="#ae8b6e" stroke-width="1" opacity=".6"/>' for y in (650, 700, 770, 860))
             + '<ellipse cx="250" cy="790" rx="190" ry="54" fill="#efe9e2"/><ellipse cx="250" cy="790" rx="160" ry="42" fill="none" stroke="#2f5a5e" stroke-width="3" opacity=".6"/>')
    # sun through the window: pane-shaped patches thrown down-right onto floor + rug, and onto the bed
    sunpatch = ('<g opacity=".55" filter="url(#sb-dof)" style="mix-blend-mode:screen">'
                '<path d="M 150,640 L 290,640 L 360,760 L 200,760 Z" fill="#fff6ea"/><path d="M 300,640 L 430,640 L 520,760 L 372,760 Z" fill="#fff6ea"/>'
                '<path d="M 206,772 L 364,772 L 430,880 L 250,880 Z" fill="#fff3e6"/><path d="M 378,772 L 526,772 L 600,880 L 444,880 Z" fill="#fff3e6"/></g>')
    bg = wall + win + curtain + castsh(poster) + poster + bed + castsh(suitcase, 8, 8, .35) + suitcase + floor + sunpatch
    fg = plant
    shadow = castsh('<path d="M 30,700 L 110,700 L 160,740 L 60,740 Z" fill="#000"/>', 0, 0, .25)
    return d, bg, fg, shadow


# ================================================================ ferry deck
def ferry(fid):
    sd, sw = sea(fid, 372, 960)
    d = G(f'{fid}sky', [(0, '#4f9ad6'), (.65, '#b9dcf0'), (1, '#e8f3f6')]) + sd + G(f'{fid}deck', [(0, '#ecebe7'), (1, '#d8d6d0')])
    sky = f'<rect width="540" height="380" fill="url(#{fid}sky)"/>' + cumulus(120, 150, 1.1) + cumulus(420, 110, .8) + cumulus(330, 250, .55, .9)
    far = '<path d="M -10,374 C 40,356 90,350 140,358 C 170,362 190,368 210,374 Z" fill="#9fc0cc"/>'
    tao = ('<path d="M 300,376 C 330,330 370,300 410,296 C 450,292 480,310 510,326 C 530,336 545,350 560,376 Z" fill="#5e9a6a"/>'
           '<path d="M 300,376 C 330,330 370,300 410,296 C 420,296 430,298 438,300 C 400,312 360,340 340,376 Z" fill="#78b07a"/>'
           '<path d="M 440,330 C 470,320 500,330 530,346 L 560,376 L 470,376 Z" fill="#4f8a5e"/>'
           + ''.join(f'<rect x="{x}" y="{y}" width="7" height="5" fill="#f4f1ec"/><path d="M {x - 1},{y} l 4.5,-3 l 4.5,3 Z" fill="#c87a5e"/>' for x, y in ((360, 352), (380, 344), (470, 346), (490, 352)))
           + boulder(318, 378, 26, 12) + boulder(500, 378, 30, 14) + '<rect x="330" y="372" width="160" height="4" fill="#efe6d8"/>')
    wake = ('<path d="M -20,960 C 60,800 140,620 230,470 C 260,420 300,390 330,376 C 290,400 250,440 220,500 C 160,620 120,780 90,960 Z" fill="#ffffff" opacity=".55"/>'
            '<path d="M 20,960 C 80,820 150,660 230,500" stroke="#ffffff" stroke-width="6" stroke-opacity=".7" fill="none" stroke-dasharray="20 14"/>')
    bg = blur(sky + far + tao, 1) + sw + wake
    deck = (f'<path d="M -20,760 L 560,700 L 560,960 L -20,960 Z" fill="url(#{fid}deck)"/>'
            + ''.join(f'<path d="M {x},{760 - (x + 20) * .103:.0f} L {x - 60},960" stroke="#c9c6bf" stroke-width="1.4"/>' for x in range(20, 600, 46)))
    rail = ''
    for x in range(-10, 560, 54):
        top = 616 - (x + 20) * .1
        rail += f'<rect x="{x}" y="{top:.0f}" width="6" height="{150:.0f}" fill="#b9c0cc"/><rect x="{x}" y="{top:.0f}" width="2" height="150" fill="#e6eaf0"/>'
    rail += ('<path d="M -20,618 L 560,560" stroke="#c9d0da" stroke-width="9" stroke-linecap="round"/><path d="M -20,615 L 560,557" stroke="#eef2f6" stroke-width="3" stroke-linecap="round"/>'
             '<path d="M -20,680 L 560,622" stroke="#b9c0cc" stroke-width="5"/>'
             '<g transform="translate(470,600)"><circle r="34" fill="#e2574c"/><circle r="17" fill="#3fa2bf"/>'
             '<path d="M -34,0 A 34,34 0 0 1 -24,-24 L -12,-12 A 17,17 0 0 0 -17,0 Z M 34,0 A 34,34 0 0 1 24,24 L 12,12 A 17,17 0 0 0 17,0 Z" fill="#f4f1ec"/>'
             '<path d="M -24,24 A 34,34 0 0 1 -34,0 L -17,0 A 17,17 0 0 0 -12,12 Z" fill="#c4463d"/></g>')
    bag = ('<g transform="translate(70,760)"><rect x="-34" y="-70" width="68" height="84" rx="16" fill="#3d4f6e"/><rect x="-34" y="-70" width="22" height="84" rx="11" fill="#4f6386"/>'
           '<rect x="-22" y="-30" width="44" height="30" rx="8" fill="#2c3a54"/><path d="M -20,-70 C -20,-92 20,-92 20,-70" stroke="#2c3a54" stroke-width="6" fill="none"/></g>')
    fg = rail + deck + castsh(bag, 10, 8, .35) + bag
    spray = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" opacity=".7"/>' for x, y, r in ((40, 520, 2.4), (70, 500, 1.6), (520, 470, 2.2), (500, 500, 1.4), (30, 470, 1.2)))
    return d, bg, fg, spray


# ================================================================ beach cafe
def beach_cafe(fid):
    sd, sw = sea(fid, 380, 540, '#2a8fbd', '#3fb4c6', '#8fe0d6', 7)
    d = (G(f'{fid}sky', [(0, '#5aa2da'), (.7, '#c6e3f2'), (1, '#eef5f6')]) + sd + G(f'{fid}sand', [(0, '#f4eee4'), (1, '#e6dccd')]) +
         G(f'{fid}deck', [(0, '#c4a083'), (1, '#a9876b')]) + G(f'{fid}top', [(0, '#b48e70'), (1, '#9c785e')]))
    sky = f'<rect width="540" height="390" fill="url(#{fid}sky)"/>' + cumulus(140, 170, .9) + cumulus(430, 220, .6, .9)
    hill = ('<path d="M 300,384 C 340,330 400,300 450,304 C 490,308 520,330 560,350 L 560,384 Z" fill="#6aa477"/>'
            '<path d="M 300,384 C 340,330 400,300 450,304 C 420,320 380,350 360,384 Z" fill="#85b98a"/>')
    longtail = ('<g transform="translate(120,470)"><path d="M -70,0 C -40,14 40,14 80,-4 L 92,-26 C 70,-10 30,-6 -60,-8 Z" fill="#7e5338"/>'
                '<path d="M -70,0 C -40,14 40,14 80,-4 L 78,2 C 40,18 -40,18 -70,4 Z" fill="#5e3c28"/>'
                '<path d="M -60,-8 L 70,-12" stroke="#2f6fb5" stroke-width="4"/>'
                '<path d="M 88,-24 l 8,-10 m -10,8 l 2,-14 m -6,12 l -4,-12" stroke="#e88aa8" stroke-width="3"/><path d="M 86,-22 l 10,-4" stroke="#3fb4c6" stroke-width="3"/>'
                '<path d="M -64,-8 L -96,10" stroke="#3c4458" stroke-width="3"/><rect x="-20" y="-30" width="50" height="6" fill="#f2eee6"/><rect x="-16" y="-24" width="3" height="16" fill="#8a7462"/><rect x="24" y="-24" width="3" height="16" fill="#8a7462"/></g>')
    beach = (f'<path d="M 0,540 C 140,528 300,548 540,532 L 540,640 L 0,640 Z" fill="url(#{fid}sand)"/>'
             '<path d="M 0,540 C 140,528 300,548 540,532" stroke="#ffffff" stroke-width="5" fill="none" opacity=".85"/>'
             '<path d="M 0,548 C 150,536 300,556 540,540" stroke="#ffffff" stroke-width="2" fill="none" opacity=".5"/>')
    rocks = boulder(400, 560, 120, 70) + boulder(470, 548, 90, 46, 1) + boulder(-20, 556, 90, 40, 1)
    palms = palm(40, 600, .95) + palm(520, 590, .85, True, 1) + palm(470, 600, .7, True)
    bg = blur(sky + hill, 1) + blur(sw + longtail + beach + rocks + palms, 1)
    floor = (f'<rect y="620" width="540" height="340" fill="url(#{fid}deck)"/>'
             + ''.join(f'<path d="M 0,{620 + i * i * 3.4:.0f} L 540,{620 + i * i * 3.4:.0f}" stroke="#9a7a60" stroke-width="{1 + i * .2:.1f}"/>' for i in range(1, 11)))
    dapple = ''.join(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{rx * .35:.0f}" fill="#fff4e6" opacity=".35" filter="url(#sb-dof)" style="mix-blend-mode:screen"/>'
                     for x, y, rx in ((60, 700, 30), (150, 760, 40), (420, 740, 36), (500, 820, 30), (90, 880, 44), (330, 900, 38)))
    post = ('<rect x="-6" y="0" width="34" height="960" fill="#8a6a50"/><rect x="18" y="0" width="10" height="960" fill="#6f5442"/>'
            + ''.join(f'<rect x="-6" y="{y}" width="34" height="4" fill="#6f5442"/>' for y in range(60, 960, 120)))
    thatch = ''
    rnd = random.Random(5)
    for row, (y, c) in enumerate(((0, '#8f6a4a'), (30, '#a37c58'), (58, '#b58d68'))):
        for i in range(30):
            x = i * 19 + rnd.uniform(-4, 4)
            L = 38 + rnd.uniform(-6, 12)
            thatch += f'<path d="M {x:.0f},{y} L {x + 18:.0f},{y} L {x + 12:.0f},{y + L:.0f} L {x + 4:.0f},{y + L - 4:.0f} Z" fill="{c}"/>'
    thatch = f'<rect width="540" height="40" fill="#7d5c40"/>{thatch}<rect y="0" width="540" height="10" fill="#6a4c34"/>'
    hang = ('<g transform="translate(470,0)"><path d="M 0,90 L 0,150" stroke="#5e4c40" stroke-width="2"/><path d="M -18,150 L 18,150 L 13,176 L -13,176 Z" fill="#c98b6c"/>'
            '<path d="M -14,152 C -30,180 -26,210 -20,230 M 0,152 C -4,190 4,220 0,250 M 12,152 C 26,180 24,210 20,236" stroke="#3f8a6e" stroke-width="5" fill="none" stroke-linecap="round"/></g>')
    top = (f'<path d="M 30,600 L 510,600 L 540,656 L 0,656 Z" fill="url(#{fid}top)"/><path d="M 0,656 L 540,656 L 540,674 L 0,674 Z" fill="#7d5f4a"/>'
           '<path d="M 30,600 L 510,600 L 512,604 L 28,604 Z" fill="#cba98a"/>'
           '<rect x="70" y="674" width="18" height="290" fill="#6f5442"/><rect x="452" y="674" width="18" height="290" fill="#5e4636"/>')
    props = ('<g transform="translate(430,614)"><path d="M -14,0 L 14,0 L 11,-24 L -11,-24 Z" fill="#f4f1ec"/><path d="M -11,-24 L 11,-24 L 10,-18 L -10,-18 Z" fill="#c8ab94"/>'
             '<path d="M 0,-24 C -8,-40 -4,-52 0,-60 C 4,-52 8,-40 0,-24 Z" fill="#4fa07c"/><path d="M 0,-26 C 8,-36 14,-40 18,-40 C 14,-32 8,-28 0,-26 Z" fill="#3f8a6e"/></g>'
             '<g transform="translate(110,626) rotate(-8)"><rect x="-20" y="-9" width="40" height="18" rx="4" fill="#1b1d24"/><rect x="-17" y="-6" width="34" height="12" rx="2" fill="#3a4b6a"/></g>')
    fg = top + props + thatch + hang + post
    shadow = (castsh('<path d="M 0,656 L 540,656 L 560,720 L 20,720 Z" fill="#000"/>', 6, 10, .3) + dapple)
    return d, bg + floor, fg, shadow
