"""Odd Hours motion-graphics components (Python side). Each function returns SVG carrying the data attributes
that pipeline/motion/oddmotion.js animates. Reusable for every episode.

Order inside one callout (channel standard): focus dot -> leader line draws -> card opens from the line end
-> text lines arrive -> hold to read -> leave in reverse, staggered.
"""
import re

TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
EN = 'font-family="Inter, system-ui, sans-serif"'


def _io(kind, at, dur, out='fade', out_at=None, out_dur=.45, extra=''):
    o = f' data-out="{out}" data-out-at="{out_at:.2f}" data-out-dur="{out_dur:.2f}"' if out_at is not None else ''
    return f'data-in="{kind}" data-at="{at:.2f}" data-dur="{dur:.2f}"{o} {extra}'


def tag(text, at, out_at, x=20, y=22):
    w = 26 + len(text) * 8.4
    return (f'<g {_io("fade-left", at, .6, "fade", out_at)} {TH}><rect x="{x}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#120e1c" fill-opacity=".82" stroke="#9a86ff" stroke-opacity=".8"/>'
            f'<circle cx="{x + 15}" cy="{y + 15}" r="4.5" fill="#9a86ff"/><text x="{x + 26}" y="{y + 20}" font-size="13" font-weight="600" fill="#f2eefa">{text}</text></g>')


def step(n, title, sub, at, out_at, y=66):
    return (f'<g {TH}>'
            f'<g {_io("mask-right", at, .7, "mask-left", out_at + .25, .5)}><rect x="26" y="{y + 5}" width="488" height="74" rx="14" fill="#120e1c" opacity=".35"/>'
            f'<rect x="22" y="{y}" width="488" height="74" rx="14" fill="#f8f3ea"/><rect x="22" y="{y}" width="8" height="74" rx="4" fill="#9a86ff"/></g>'
            f'<g {_io("pop", at + .25, .55, "shrink", out_at + .1, .35)}><rect x="44" y="{y + 13}" width="48" height="48" rx="12" fill="#7a5ab8"/>'
            f'<text x="68" y="{y + 47}" font-size="26" font-weight="800" fill="#fff" text-anchor="middle">{n}</text></g>'
            f'<text {_io("fade-left", at + .4, .6, "fade", out_at, .3)} x="108" y="{y + 38}" font-size="23" font-weight="800" fill="#1d1626">{title}</text>'
            f'<text {_io("fade", at + .65, .6, "fade", out_at, .3)} x="108" y="{y + 60}" {EN} font-size="11" font-weight="700" fill="#8a7fa0" letter-spacing=".8">{sub}</text></g>')


def callout(x, y, w, lines, px, py, at, out_at, color='#c4463d', h=None):
    """Card at (x,y,w) explains the point (px,py). lines: list of strings, revealed one by one."""
    h = h or 18 + 22 * len(lines)
    ex, ey = x + w / 2, (y + h if py > y + h else y)
    mx, my = (ex + px) / 2, (ey + py) / 2 + (18 if py > ey else -18)
    txt = ''.join(f'<text class="om-l" x="{x + w / 2:.0f}" y="{y + 28 + i * 22}" font-size="16" font-weight="800" fill="#fff" text-anchor="middle">{l}</text>' for i, l in enumerate(lines))
    return (f'<g {TH}>'
            f'<g {_io("pop", at, .45, "shrink", out_at + .6, .3)}><circle cx="{px}" cy="{py}" r="11" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="2"/><circle cx="{px}" cy="{py}" r="5" fill="#fff"/></g>'
            f'<path {_io("draw", at + .25, .6, "draw-back", out_at + .35, .4)} d="M {px},{py} Q {mx:.0f},{my:.0f} {ex:.0f},{ey:.0f}" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" data-dash="6 5"/>'
            f'<g {_io("grow", at + .8, .5, "mask-right", out_at + .15, .4)}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{color}"/></g>'
            f'<g {_io("lines", at + 1.0, .45, "fade", out_at, .3)} data-stagger=".18">{txt}</g></g>')


def arrow(d, at, out_at, color='#ffffff', width=4):
    """Arrow drawn along path d; head appears at the very end of the stroke."""
    end = re.findall(r'[-\d.]+', d)[-2:]
    ex, ey = float(end[0]), float(end[1])
    return (f'<g {_io("arrow", at, .8, "draw-back", out_at, .4)}><path class="om-line" d="{d}" stroke="{color}" stroke-width="{width}" fill="none" stroke-linecap="round"/>'
            f'<g class="om-head" opacity="0"><circle cx="{ex}" cy="{ey}" r="{width * 1.8}" fill="{color}"/></g></g>')


def subs(th, en, at, out_at, y=712, line_gap=.55):
    """Channel subtitles (yellow Thai, small white English), each Thai line arrives on its own beat."""
    th = [l for l in th.split('/') if l.strip()]
    en = [l for l in en.split('/') if l.strip()]
    h = len(th) * 26 + 6 + len(en) * 17
    top = y - h / 2
    tl = ''.join(f'<text class="om-l" x="270" y="{top + 19 + i * 26:.0f}">{l.strip()}</text>' for i, l in enumerate(th))
    el = ''.join(f'<text x="270" y="{top + len(th) * 26 + 18 + i * 17:.0f}">{l.strip()}</text>' for i, l in enumerate(en))
    return (f'<g {_io("lines", at, .4, "fade", out_at, .35)} data-stagger="{line_gap}" {TH} font-weight="700" font-size="20" text-anchor="middle" fill="#ffd84a" stroke="#0b0812" stroke-width="5" stroke-linejoin="round" paint-order="stroke">{tl}</g>'
            f'<g {_io("fade", at + .25, .5, "fade", out_at, .35)} {EN} font-weight="500" font-size="13" text-anchor="middle" fill="#ffffff" stroke="#0b0812" stroke-width="4" stroke-linejoin="round" paint-order="stroke">{el}</g>')


def counter(x, y, to, fmt, at, out_at, size=30, color='#1a1626', frm=0, anchor='middle'):
    return (f'<text {_io("count", at, 1.2, "fade", out_at)} data-count-to="{to}" data-count-from="{frm}" data-count-fmt="{fmt}" x="{x}" y="{y}" {TH} font-size="{size}" font-weight="800" fill="{color}" text-anchor="{anchor}">{fmt.replace("{n}", str(frm))}</text>')


def pop(content, at, out_at, dur=.55):
    return f'<g {_io("pop", at, dur, "shrink", out_at, .35)}>{content}</g>'


def reveal(content, at, out_at, kind='fade-up', dur=.6, out='fade'):
    return f'<g {_io(kind, at, dur, out, out_at)}>{content}</g>'


# ---------------------------------------------------------------- animated faces
def group(src, gid):
    """Extract <g id="gid">...</g> from a defs string (nested groups ok)."""
    a = src.index(f'<g id="{gid}"')
    depth, i = 0, a
    while True:
        o, c = src.find('<g', i + 1), src.find('</g>', i + 1)
        if o != -1 and o < c:
            depth += 1; i = o
        else:
            if depth == 0:
                return src[a:c + 4]
            depth -= 1; i = c


JAMES_EYES = ('M -21,-3 C -17,-6.5 -9,-6.5 -5,-1.5 C -9,0.8 -17,0.8 -21,-3 Z', 'M 21,-3 C 17,-6.5 9,-6.5 5,-1.5 C 9,0.8 17,0.8 21,-3 Z',
              'M -21.5,-2.2 C -16,0.4 -10,0.4 -4.5,-1.2', 'M 21.5,-2.2 C 16,0.4 10,0.4 4.5,-1.2')
TAWAN_EYES = ('M -21,-1 C -18,-7.5 -8,-7.5 -5,-1 C -8,3 -18,3 -21,-1 Z', 'M 21,-1 C 18,-7.5 8,-7.5 5,-1 C 8,3 18,3 21,-1 Z',
              'M -22,0.5 C -16,3.4 -10,3.4 -4,0.4', 'M 22,0.5 C 16,3.4 10,3.4 4,0.4')
MOUTH_JAMES = ('<path d="M -5.5,22.8 Q 0,22.2 5.5,22.8 Q 4,26.4 0,26.6 Q -4,26.4 -5.5,22.8 Z" fill="#7a3a36"/>',
               '<path d="M -6.5,22.2 Q 0,21.6 6.5,22.2 Q 5,29.4 0,29.6 Q -5,29.4 -6.5,22.2 Z" fill="#6a2f2c"/><path d="M -3,27.4 Q 0,28.8 3,27.4" stroke="#d98a80" stroke-width="1.4" fill="none"/>')
MOUTH_TAWAN = ('<path d="M -5,22.4 Q 0,21.8 5,22.4 Q 4,25.8 0,26 Q -4,25.8 -5,22.4 Z" fill="#8a3a3e"/>',
               '<path d="M -6,22 Q 0,21.4 6,22 Q 5,28.4 0,28.6 Q -5,28.4 -6,22 Z" fill="#7a2f34"/><path d="M -3,26.6 Q 0,27.8 3,26.6" stroke="#e79a8a" stroke-width="1.3" fill="none"/>')


def anim_head(defs_src, src_id, new_id, skin, kind='james', clips=('eyeL', 'eyeR')):
    """Copy a head group under a new id with animatable parts:
    #id-iL/#id-iR iris wrappers (glance), #id-bl closed lids (blink), #id-m1/#id-m2 open mouths (talk)."""
    g = group(defs_src, src_id).replace(f'id="{src_id}"', f'id="{new_id}"', 1)
    for side, cid in zip('LR', clips):
        g = re.sub(rf'(<g clip-path="url\(#{cid}\)">)(.*?)(</g>)', rf'\1<g id="{new_id}-i{side}">\2</g>\3', g, count=1, flags=re.S)
    eyes = JAMES_EYES if kind == 'james' else TAWAN_EYES
    mouths = MOUTH_JAMES if kind == 'james' else MOUTH_TAWAN
    lids = (f'<g id="{new_id}-bl" display="none"><path d="{eyes[0]}" fill="{skin}"/><path d="{eyes[1]}" fill="{skin}"/>'
            f'<path d="{eyes[2]}" stroke="#17151d" stroke-width="1.9" fill="none" stroke-linecap="round"/><path d="{eyes[3]}" stroke="#17151d" stroke-width="1.9" fill="none" stroke-linecap="round"/></g>')
    m = f'<g id="{new_id}-m1" display="none">{mouths[0]}</g><g id="{new_id}-m2" display="none">{mouths[1]}</g>'
    return g[:-len('</g>')] + m + lids + '</g>'
