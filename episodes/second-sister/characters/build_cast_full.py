#!/usr/bin/env python3
"""Full-body cast for 'The Second Sister', split into animatable parts.

Every character is one <g id="fb-{cid}"> made of child groups:
  {cid}-legL, {cid}-legR   pivot at the hip   (data-pivot="x,y")
  {cid}-body               torso / robe
  {cid}-armL, {cid}-armR   pivot at the shoulder
  {cid}-head               pivot at the neck
Local coordinates: face centre = (0,0), feet on y≈372 (adults), y≈300 (children).
Heads come from build_cast.py (approved faces) and nuns-test-frame.html (Mariam, Agnes).
Writes cast.html (the sheet) and is imported by scene builders.
"""
import os, sys, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("bc", os.path.join(HERE, "build_cast.py"))
bc = importlib.util.module_from_spec(spec); spec.loader.exec_module(bc)
hs = bc.hs

nuns = open(os.path.join(HERE, "..", "frames", "nuns-test-frame.html")).read()
NUN_DEFS = nuns[nuns.index('<clipPath id="face">'):nuns.index('<filter id="dof"')]
def _nun_head(gid, end_marker):
    g0 = nuns.index(f'<g id="{gid}">')
    g1 = nuns.index(end_marker, g0)
    grp = nuns[g0:g1]
    h0 = grp.index('<!-- head -->')
    head = grp[h0:]
    head = head[:head.rstrip().rfind('</g>')]
    return head
MARIAM_HEAD = _nun_head("mariam", "<!-- ===== SISTER AGNES")
AGNES_HEAD = _nun_head("agnes", '<filter id="dof"')

# Agnes, revised (user): skin pale white with real light and shade (not grey), clearly red lips,
# a calm closed smile instead of the hooked grin. Same face, eyes, veil and habit.
AG_LIPS = ('<path d="M -7.6,21.4 Q -3.4,19.4 0,20.7 Q 3.4,19.4 7.6,21.4 Q 0,23 -7.6,21.4 Z" fill="#b34558"/>'
           '<path d="M -7.6,21.4 Q 0,23 7.6,21.4 Q 4.4,25.4 0,25.7 Q -4.4,25.4 -7.6,21.4 Z" fill="#c95d6e"/>'
           '<path d="M -2.6,23.9 Q 0,24.6 2.6,23.9" stroke="#eea0aa" stroke-width="1" stroke-linecap="round" fill="none" opacity=".7"/>'
           '<path d="M -7.6,21.4 L -8.6,20.6 M 7.6,21.4 L 8.6,20.6" stroke="#94384a" stroke-width=".9" stroke-linecap="round"/>')
AG_PALE = {"#efe2da": "#f7ebe4", "#d3bfb5": "#e4d0c6", "#b39d94": "#cdb6ac", "#e2d1c8": "#f3e5dd", "#fbf4ef": "#fdf6f2",
           "#c8b2a8": "#d8c2b8", "#d9aaa2": "#e0aaa6", "#bfa79f": "#c6b4ba", "#c9b3ab": "#cfbfc4",
           # the older chapel frame (shots 31-32) used warmer skin: same mapping so she matches everywhere
           "#efd5c3": "#f7ebe4", "#d9ad97": "#e4d0c6", "#b98672": "#cdb6ac", "#e5c3ae": "#f3e5dd", "#fdeee2": "#fdf6f2",
           "#cf9f88": "#d8c2b8", "#dfa494": "#e0aaa6", "#caa08a": "#cfbfc4"}
import re as _re
def agnes_pale(head):
    for a, b in AG_PALE.items(): head = head.replace(a, b)
    head = head.replace('opacity=".3"/>', 'opacity=".05"/>').replace('opacity=".08"/>', 'opacity=".04"/>')   # almost no blush
    head = _re.sub(r'<!-- (eerie|calm, closed) smile.*?(?=<use href="#cap"/>)', '<!-- calm closed smile, red lips -->' + AG_LIPS, head, flags=_re.S)
    return head
AGNES_HEAD = agnes_pale(AGNES_HEAD)

# ---------------- part builders ----------------
HIP, KNEE, ANKLE = 182, 280, 358

def part(pid, body, pivot=None):
    pv = f' data-pivot="{pivot[0]},{pivot[1]}"' if pivot else ""
    return f'<g id="{pid}"{pv}>{body}</g>'

def leg(cid, side, pants, shoe, sole="#1e1a1e", skin=None, pants_to=ANKLE, hip=HIP, knee=KNEE, ankle=ANKLE, w=(13, 10, 8)):
    """side -1 = viewer-left (lit), +1 = viewer-right."""
    s = side; xc = s * 16
    m, l, d = pants
    col = m if s < 0 else d
    hi = l if s < 0 else m
    out = ""
    if skin:   # bare shin below the hem
        out += f'<path d="M {xc-w[1]+1},{knee} L {xc+w[1]-1},{knee} L {xc+w[2]},{ankle} L {xc-w[2]},{ankle} Z" fill="{skin[0] if s < 0 else skin[1]}"/>'
    if pants_to > hip:
        pk = min(pants_to, knee)
        out += f'<path d="M {xc-w[0]},{hip} L {xc+w[0]},{hip} L {xc+w[1]},{pk} L {xc-w[1]},{pk} Z" fill="{col}"/>'
        if pants_to > knee:
            out += f'<path d="M {xc-w[1]},{knee-1} L {xc+w[1]},{knee-1} L {xc+w[2]},{pants_to} L {xc-w[2]},{pants_to} Z" fill="{col}"/>'
        edge = xc - w[0] if s < 0 else xc + w[0] - 5
        edge2 = xc - w[2] if s < 0 else xc + w[2] - 4
        out += f'<path d="M {edge},{hip} L {edge+5},{hip} L {edge2+4},{pants_to} L {edge2},{pants_to} Z" fill="{hi}"/>'
    # shoe, front view
    a = ankle
    out += f'<path d="M {xc-w[2]-1},{a-3} L {xc+w[2]+1},{a-3} C {xc+w[2]+5},{a+4} {xc+w[2]+4},{a+11} {xc+w[2]+1},{a+13} L {xc-w[2]-1},{a+13} C {xc-w[2]-4},{a+11} {xc-w[2]-5},{a+4} {xc-w[2]-1},{a-3} Z" fill="{shoe}"/>'
    out += f'<rect x="{xc-w[2]-2}" y="{a+11}" width="{2*w[2]+4}" height="4" rx="2" fill="{sole}"/>'
    return part(f"{cid}-leg{'L' if s < 0 else 'R'}", out, (xc, hip))

def arm(cid, side, sleeve, skin, short=False, sh=(42, 66), el=(48, 146), wr=(50, 214), wide=False, hand_extra="", thick=1.0):
    s = side
    sx, sy = s * sh[0], sh[1]; ex, ey = s * el[0], el[1]; wx, wy = s * wr[0], wr[1]
    m, l, d = sleeve
    col = l if s < 0 else d
    sk = skin[0] if s < 0 else skin[1]
    out = ""
    # skin under everything (forearm), sleeve on top
    t = thick
    out += f'<path d="M {sx-8*t},{sy} L {sx+8*t},{sy} L {ex+7*t},{ey} L {wx+6*t},{wy} L {wx-6*t},{wy} L {ex-7*t},{ey} Z" fill="{sk}"/>'
    if short:
        out += f'<path d="M {sx-11*t},{sy-4} C {sx-14*t},{sy+20} {s*46-12*t},{96} {s*46-11*t},{114} L {s*46+11*t},{114} C {s*46+12*t},{96} {sx+14*t},{sy+20} {sx+11*t},{sy-4} Z" fill="{col}"/>'
        out += f'<path d="M {s*46-10*t},{108} Q {s*46},{104} {s*46+10*t},{108}" stroke="{d}" stroke-width="1.4" fill="none"/><path d="M {sx-4*s},{sy+8} q {2*s},{14} {-1*s},{26}" stroke="{d}" stroke-width="1.2" fill="none" opacity=".7"/>'
    else:
        cuff = 12 if wide else 8
        out += f'<path d="M {sx-10},{sy-2} L {sx+10},{sy-2} L {ex+8},{ey} L {wx+cuff},{wy} L {wx-cuff},{wy} L {ex-8},{ey} Z" fill="{col}"/>'
        out += f'<path d="M {wx-cuff},{wy-6} L {wx+cuff},{wy-6} L {wx+cuff},{wy} L {wx-cuff},{wy} Z" fill="{m}"/>'
    out += f'<ellipse cx="{wx}" cy="{wy+10}" rx="7" ry="10" fill="{sk}"/>'
    out += f'<path d="M {wx-7},{wy+8} C {wx-7},{wy+14} {wx-5},{wy+19} {wx-2},{wy+20}" fill="none" stroke="{skin[1]}" stroke-width="1.2" opacity=".6"/>'
    out += hand_extra
    return part(f"{cid}-arm{'L' if s < 0 else 'R'}", out, (sx, sy))

def torso_basic(cols, top=52, waist=150, hip=HIP + 6, sw=40, ww=34, hw=38):
    m, l, d = cols
    return (f'<path d="M -14,{top} C -26,{top+2} -{sw-4},{top+6} -{sw},{top+16} L -{ww},{waist} L -{hw},{hip} L {hw},{hip} L {ww},{waist} L {sw},{top+16} C {sw-4},{top+6} 26,{top+2} 14,{top} Z" fill="{m}"/>'
            f'<path d="M -{sw},{top+16} C -{sw-4},{top+6} -26,{top+2} -16,{top+1} C -22,{top+50} -24,{hip-40} -22,{hip} L -{hw},{hip} L -{ww},{waist} Z" fill="{l}"/>'
            f'<path d="M 18,{top+2} C 28,{top+4} {sw-4},{top+8} {sw},{top+16} L {ww},{waist} L {hw},{hip} L 24,{hip} C 26,{hip-40} 24,{top+50} 18,{top+2} Z" fill="{d}"/>')

def robe(cols, top=52, hem=358, flare=50):
    m, l, d = cols
    return (f'<path d="M -14,{top} C -26,{top+2} -36,{top+6} -40,{top+16} L -36,150 L -{flare},{hem} L {flare},{hem} L 36,150 L 40,{top+16} C 36,{top+6} 26,{top+2} 14,{top} Z" fill="{m}"/>'
            f'<path d="M -40,{top+16} C -36,{top+6} -26,{top+2} -16,{top+1} C -22,120 -24,240 -24,{hem} L -{flare},{hem} L -36,150 Z" fill="{l}"/>'
            f'<path d="M 18,{top+2} C 28,{top+4} 36,{top+8} 40,{top+16} L 36,150 L {flare},{hem} L 26,{hem} C 26,240 26,120 18,{top+2} Z" fill="{d}"/>'
            f'<path d="M -6,200 L -8,{hem} M 8,210 L 10,{hem}" stroke="{d}" stroke-width="1.4" opacity=".6"/>')

def figure(cid, parts_back, legs, body, arms, head, front=""):
    return f'<g id="fb-{cid}">{parts_back}{legs}{part(cid + "-body", body)}{arms}{part(cid + "-head", head, (0, 52))}{front}</g>'

HABIT = ("#e6e0d5", "#f6f1e8", "#bfb6a9")
SHOE_BLACK = "#1d1a20"

def nun(cid, head, skin, veil="#1a1520", vhi="#2c2532", vlo="#120e16", hand_extra_R="", robe_cols=HABIT):
    back = hs(bc.habit_back(veil))
    legs = leg(cid, -1, robe_cols, SHOE_BLACK, pants_to=0) + leg(cid, 1, robe_cols, SHOE_BLACK, pants_to=0)
    body = robe(robe_cols)
    arms = (arm(cid, -1, robe_cols, skin, wide=True) + arm(cid, 1, robe_cols, skin, wide=True, hand_extra=hand_extra_R))
    top = hs(bc.habit_over(vhi, vlo) + head)
    return figure(cid, back, legs, body, arms, top)

# ---------------- characters ----------------
F = {}

# Mek
MEK_SKIN = ("#eec4a2", "#d9a27e")
mek_torso = (torso_basic(("#e8e4dc", "#f4f1ea", "#c9c3b8"), ww=32, hw=36)
  + '<path d="M -40,68 C -36,58 -26,54 -16,53 L -12,130 L -16,200 L -40,200 L -38,150 Z" fill="#7889a6"/>'
  + '<path d="M 40,68 C 36,58 26,54 16,53 L 12,130 L 16,200 L 40,200 L 38,150 Z" fill="#45546c"/>'
  + '<path d="M -40,68 L -38,150 L -40,200 L -30,200 L -30,80 Z" fill="#8a9ab6"/>'
  + '<path d="M -16,53 L -12,130 L -16,200 M 16,53 L 12,130 L 16,200" fill="none" stroke="#3b4860" stroke-width="2.2"/>'
  + '<rect x="-34" y="100" width="12" height="12" fill="#4c5c76"/>'
  + '<path d="M -36,186 L 36,186 L 36,192 L -36,192 Z" fill="#2a2a30" opacity=".0"/>'
  + '<path d="M -30,62 L 30,176" stroke="#2a2420" stroke-width="4"/>'
  + '<rect x="18" y="168" width="28" height="18" rx="3" fill="#2b2b30"/><circle cx="32" cy="178" r="6.5" fill="#16161a"/><circle cx="32" cy="178" r="3.6" fill="#3a4a66"/><circle cx="30.6" cy="176.6" r="1.1" fill="#cfd8ec"/>')
F["mek"] = figure("mek", "",
  leg("mek", -1, ("#2e3448", "#3e4660", "#232838"), "#e8e4dc", "#8a8690") + leg("mek", 1, ("#2e3448", "#3e4660", "#232838"), "#d4d0c8", "#7a7680"),
  mek_torso,
  arm("mek", -1, ("#5d6f8a", "#7889a6", "#45546c"), MEK_SKIN) + arm("mek", 1, ("#5d6f8a", "#7889a6", "#45546c"), MEK_SKIN),
  hs(bc.mek_head))

# Pa Daeng: fuller, rounder body with weight in the blouse, apron and sarong
DG_SKIN = ("#e3b088", "#c98f69")
dg_torso = (
  # blouse: round shoulders, bust and belly
  '<path d="M -16,52 C -34,54 -46,60 -48,78 C -50,100 -48,122 -45,140 C -49,160 -50,178 -46,192 L 46,192 C 50,178 49,160 45,140 C 48,122 50,100 48,78 C 46,60 34,54 16,52 Z" fill="#8a3a3e"/>'
  '<path d="M -48,78 C -46,60 -34,54 -18,53 C -26,90 -30,140 -28,192 L -46,192 C -50,178 -49,160 -45,140 C -48,122 -50,100 -48,78 Z" fill="#a54a4e"/>'
  '<path d="M 20,54 C 34,56 46,62 48,78 C 50,100 48,122 45,140 C 49,160 50,178 46,192 L 30,192 C 32,140 30,92 20,54 Z" fill="#6c2b30"/>'
  '<path d="M -36,108 C -26,120 -10,120 -2,112 M 2,112 C 10,120 26,120 36,108" stroke="#6c2b30" stroke-width="1.6" fill="none" opacity=".7"/>'
  '<g fill="#e9c6b0" opacity=".5"><circle cx="-36" cy="96" r="2"/><circle cx="-24" cy="128" r="2"/><circle cx="-40" cy="160" r="2"/><circle cx="36" cy="92" r="2"/><circle cx="40" cy="140" r="2"/><circle cx="28" cy="170" r="2"/></g>'
  # sarong with batik bands and folds, slightly flared
  '<path d="M -44,188 L 44,188 L 40,354 L -40,354 Z" fill="#4a3a4a"/><path d="M -44,188 L -22,188 L -22,354 L -40,354 Z" fill="#5c4a5c"/><path d="M 24,188 L 44,188 L 40,354 L 24,354 Z" fill="#3a2c3a"/>'
  '<g stroke="#8a7a5a" stroke-width="1.6" opacity=".55" fill="none"><path d="M -42,214 L 42,214 M -41,318 L 41,318"/><path d="M -40,222 l 6,6 l 6,-6 l 6,6 l 6,-6 l 6,6 l 6,-6 l 6,6 l 6,-6 l 6,6 l 6,-6 l 6,6 l 6,-6 l 6,6"/></g>'
  '<path d="M -6,190 L -10,354 M 12,196 L 16,354" stroke="#2c2030" stroke-width="1.6" opacity=".6"/><path d="M 30,190 C 34,206 30,222 34,236" stroke="#2c2030" stroke-width="2" fill="none"/>'
  # apron: bib with neck strap, wide skirt with folds, pocket, side bow
  '<path d="M -26,84 L 26,84 L 30,146 L -30,146 Z" fill="#8fa3b0"/><path d="M -26,84 L -12,84 L -14,146 L -30,146 Z" fill="#a9bbc6"/>'
  '<path d="M -26,84 C -24,68 -18,60 -12,56 M 26,84 C 24,68 18,60 12,56" fill="none" stroke="#8fa3b0" stroke-width="4"/>'
  '<path d="M -38,146 L 38,146 C 42,200 44,250 44,296 L -44,296 C -44,250 -42,200 -38,146 Z" fill="#8fa3b0"/><path d="M -38,146 L -16,146 C -18,200 -20,250 -20,296 L -44,296 C -44,250 -42,200 -38,146 Z" fill="#a9bbc6"/>'
  '<path d="M 18,146 L 38,146 C 42,200 44,250 44,296 L 22,296 C 22,250 20,200 18,146 Z" fill="#748894"/>'
  '<g stroke="#6a7c88" stroke-width="1.5" opacity=".7" fill="none"><path d="M -8,160 C -10,210 -8,260 -12,296"/><path d="M 8,160 C 10,210 8,260 10,296"/><path d="M -28,170 C -30,220 -30,260 -34,296"/></g>'
  '<rect x="-38" y="142" width="76" height="8" fill="#748894"/><path d="M 38,146 c 10,-6 14,4 6,8 c 8,4 2,14 -6,6 Z" fill="#748894"/><path d="M 42,152 l 6,22 M 40,152 l -2,24" stroke="#748894" stroke-width="4"/>'
  '<rect x="-20" y="190" width="40" height="28" rx="3" fill="#748894"/><path d="M -20,196 L 20,196" stroke="#6a7c88" stroke-width="1.4"/>'
  '<g transform="translate(-40,200)"><circle r="8" fill="none" stroke="#b49a5a" stroke-width="2.4"/><path d="M -3,6 l -3,15 l 4,0 l 1,-5 l 3,0 Z M 4,7 l 2,13 l 4,-1 l -1,-5 Z" fill="#c9ad66"/></g>')
F["daeng"] = figure("daeng", "",
  leg("daeng", -1, ("#4a3a4a",) * 3, "#6a4a3a", "#3a2a22", skin=DG_SKIN, pants_to=0) + leg("daeng", 1, ("#4a3a4a",) * 3, "#5a3e30", "#3a2a22", skin=DG_SKIN, pants_to=0),
  dg_torso,
  arm("daeng", -1, ("#8a3a3e", "#a54a4e", "#6c2b30"), DG_SKIN, short=True, sh=(46, 68), el=(52, 146), wr=(54, 212), thick=1.25) + arm("daeng", 1, ("#8a3a3e", "#a54a4e", "#6c2b30"), DG_SKIN, short=True, sh=(46, 68), el=(52, 146), wr=(54, 212), thick=1.25),
  hs(bc.dg_head))

# Mother Catarina (with folder in her right hand = viewer-left)
CAT_SKIN = ("#f1d3bd", "#dcb19a")
F["cat"] = nun("cat", bc.cat_head, CAT_SKIN)
F["cat"] = F["cat"].replace(f'<g id="cat-armL"', '<g id="cat-armL"', 1)
CAT_CROSS = '<path d="M -1.6,74 L 1.6,74 L 1.6,108 L -1.6,108 Z M -9,82 L 9,82 L 9,85.5 L -9,85.5 Z" fill="#9a8a5a"/>'
F["cat"] = F["cat"].replace('<g id="cat-armL"', f'<g id="cat-cross">{CAT_CROSS}</g><g id="cat-armL"', 1)

# Sister Rosa (white veil)
ROSA_SKIN = ("#f5d3b4", "#e2b08f")
F["rosa"] = nun("rosa", bc.rosa_head, ROSA_SKIN, veil="#e9e4da", vhi="#f7f3ec", vlo="#c7bfb2")

# Sister Mariam (scar on her left hand = viewer-right)
MAR_SKIN = ("#f6dcc4", "#e4b89c")
SCAR = '<path d="M 46,222 C 50,220 54,222 54,227 C 52,231 48,230 46,227 Z M 49,231 C 51,231 53,233 52,235 C 50,236 48,234 49,231 Z" fill="#d98f86" opacity=".8"/>'
F["mariam"] = nun("mariam", MARIAM_HEAD, MAR_SKIN, hand_extra_R=SCAR)

# Sister Agnes: pale; same habit
AG_SKIN = ("#f7ebe4", "#e4d0c6")
F["agnes"] = nun("agnes", AGNES_HEAD, AG_SKIN)

# ---- identity at first glance (user): each sister gets one thing you can read from across the room; same habit underneath
def _into_body(fig, cid, svg):
    i = fig.index(f'<g id="{cid}-body">'); j = fig.index('</g>', i)
    return fig[:j] + svg + fig[j:]
# a plain sister for crowds (no accessories), so the background never looks like a named character
def _plain_face(h):
    """Ordinary sister for crowds: plain, not pretty: no blush, small dot eyes without lash wings or sparkle, straight heavier brows, flat mouth."""
    h = h.replace("#f6dcc4", "#e9caae").replace("#fff0e2", "#f4dcc6").replace("#e4b89c", "#d6aa8c")
    h = h.replace('opacity=".45"/>', 'opacity="0"/>')
    h = re.sub(r'<circle cx="-?1[14]\.\d" cy="-?1\.8" r="[\d.]+" fill="#(fff|ffe2bf)"/>', "", h)
    h = h.replace('r="4.9" fill="#4a2c22"', 'r="3.4" fill="#3a2a22"')
    h = re.sub(r'<path d="M -?20\.5,-1\.5 L -?24\.5,-4 L -?21\.5,0\.5 Z" fill="#1d1418"/>', "", h)
    h = h.replace('<path d="M -22,-11.5 C -17,-13 -11,-15 -6,-17" fill="none" stroke="#3a2a26" stroke-width="2.1"', '<path d="M -22,-12 L -6,-13" fill="none" stroke="#3a2a26" stroke-width="2.8"')
    h = h.replace('<path d="M 6,-17 C 11,-15 17,-13 22,-11.5" fill="none" stroke="#3a2a26" stroke-width="2.1"', '<path d="M 6,-13 L 22,-12" fill="none" stroke="#3a2a26" stroke-width="2.8"')
    h = h.replace('<path d="M -5.5,23.2 Q 0,21.8 5.5,23.2" fill="none" stroke="#b5767a"', '<path d="M -6,23.6 L 6,23.6" fill="none" stroke="#9a6a62"')
    return h
F["nunx"] = nun("nunx", _plain_face(MARIAM_HEAD), ("#e9caae", "#d6aa8c"))
# Mariam: a long pale-blue scapular down the front and a blue rosary in her hand
F["mariam"] = _into_body(F["mariam"], "mariam",
    '<path d="M -13,62 L 13,62 L 16,352 L -16,352 Z" fill="#a9c6e8"/><path d="M 4,62 L 13,62 L 16,352 L 6,352 Z" fill="#87a8d0"/><path d="M -16,346 L 16,346" stroke="#6a8ab8" stroke-width="2"/>')
F["mariam"] = F["mariam"].replace(SCAR, SCAR + ''.join(f'<circle cx="{48 + 4 * __import__("math").sin(k * .6):.1f}" cy="{228 + k * 4.2:.1f}" r="1.9" fill="#4a7ac8"/>' for k in range(9))
    + '<path d="M 49,266 L 49,278 M 45,270 L 53,270" stroke="#c8b07a" stroke-width="2"/>', 1)
F["mariam"] = F["mariam"].replace("<!-- small, unsure mouth -->", '<circle cx="17.5" cy="7.5" r="1.25" fill="#5a3830"/><!-- small, unsure mouth -->', 1)   # mole under the right eye
# Agnes: grey-blue infirmary apron with a red cross on the bib (the nurse)
F["agnes"] = _into_body(F["agnes"], "agnes",
    '<path d="M -22,96 L 22,96 L 24,150 L 40,300 L -40,300 L -24,150 Z" fill="#b4c2d4"/><path d="M 8,96 L 22,96 L 24,150 L 40,300 L 14,300 Z" fill="#94a4ba"/>'
    '<path d="M -22,96 L -32,64 M 22,96 L 32,64" stroke="#94a4ba" stroke-width="4"/><path d="M -24,150 L 24,150" stroke="#8494aa" stroke-width="3"/>'
    '<rect x="-7" y="106" width="14" height="14" rx="2" fill="#f4f0f2"/><path d="M 0,108 L 0,118 M -5,113 L 5,113" stroke="#c8323c" stroke-width="3.2"/>')
_lash = "".join(f'<path d="{d}" fill="none" stroke="#1b1316" stroke-width=".9" stroke-linecap="round"/>' for d in (
    "M -20.4,-2.6 C -21.4,-3.2 -22.1,-4 -22.5,-5", "M -18.4,-5.2 C -19.1,-6.1 -19.5,-7 -19.6,-8",
    "M 20.4,-2.6 C 21.4,-3.2 22.1,-4 22.5,-5", "M 18.4,-5.2 C 19.1,-6.1 19.5,-7 19.6,-8"))
_r = F["rosa"]
_r = _r.replace('<ellipse cx="-18" cy="12" rx="6.5" ry="3.4" fill="#ec8f88" opacity="0.55"/><ellipse cx="18" cy="12" rx="6.5" ry="3.4" fill="#e0857e" opacity="0.55"/>',
    '<ellipse cx="-18" cy="12" rx="7" ry="3.6" fill="#f29aa4" opacity=".55"/><ellipse cx="18" cy="12" rx="7" ry="3.6" fill="#e98e98" opacity=".55"/>', 1)
_r = _r.replace('<circle cx="-14.8" cy="-1.8" r="1.7249999999999999" fill="#fff"/><circle cx="11.2" cy="-1.8" r="1.7249999999999999" fill="#fff"/>',
    _lash + '<circle cx="-14.8" cy="-1.8" r="1.9" fill="#fff"/><circle cx="11.2" cy="-1.8" r="1.9" fill="#fff"/>', 1)
_r = _r.replace('<ellipse cx="0" cy="24" rx="4" ry="3.2" fill="#8e4a4c"/><ellipse cx="0" cy="25.4" rx="2.4" ry="1.4" fill="#d27e7e"/>',
    '<ellipse cx="0" cy="24" rx="4" ry="3.1" fill="#b2606a"/><ellipse cx="0" cy="25.4" rx="2.4" ry="1.3" fill="#e2949a"/>', 1)
assert _r != F["rosa"]; F["rosa"] = _r
# Mother Catharina: deep purple cincture with a hanging end, the superior's large cross already on her chest
F["cat"] = _into_body(F["cat"], "cat",
    '<path d="M -37,144 L 37,144 L 38,156 L -38,156 Z" fill="#5a2a6e"/><path d="M -30,156 L -22,156 L -24,236 L -32,236 Z" fill="#5a2a6e"/><path d="M -32,236 L -24,236 L -22,244 L -34,244 Z" fill="#7a4a8e"/>')

# Father Joseph
JOS_SKIN = ("#ebc6a6", "#d4a585")
jos_body = (robe(("#ece8e0", "#faf7f1", "#c4bdb2"), flare=44)
  + '<rect x="-13" y="52" width="26" height="9" rx="2" fill="#16141a"/><rect x="-4" y="54" width="8" height="5" fill="#f4f1ea"/>'
  + ''.join(f'<circle cx="0" cy="{y}" r="1.8" fill="#bcb4a8"/>' for y in range(80, 350, 18))
  + '<path d="M -36,150 L 36,150 L 37,160 L -37,160 Z" fill="#1d1a20"/><path d="M 20,160 L 28,160 L 30,250 L 22,250 Z" fill="#1d1a20"/>')
F["jos"] = figure("jos", "",
  leg("jos", -1, ("#ece8e0",) * 3, SHOE_BLACK, pants_to=0) + leg("jos", 1, ("#ece8e0",) * 3, SHOE_BLACK, pants_to=0),
  jos_body,
  arm("jos", -1, ("#ece8e0", "#faf7f1", "#c4bdb2"), JOS_SKIN) + arm("jos", 1, ("#ece8e0", "#faf7f1", "#c4bdb2"), JOS_SKIN),
  hs(bc.jos_head))

# Captain Thana
TH_SKIN = ("#d9a37c", "#bf875f")
th_torso = (torso_basic(("#8a6c4c", "#a3845f", "#6c5238"), sw=42, ww=36, hw=38)
  + '<path d="M -16,52 L 0,72 L 16,52 L 22,58 L 0,84 L -22,58 Z" fill="#7a5e42"/><path d="M 0,72 L 0,180" stroke="#6c5238" stroke-width="1.6"/>'
  + ''.join(f'<circle cx="0" cy="{y}" r="2" fill="#c8b07a"/>' for y in (100, 125, 150))
  + '<rect x="-34" y="92" width="22" height="18" rx="2" fill="#7a5e42"/><rect x="12" y="92" width="22" height="18" rx="2" fill="#5e4630"/>'
  + '<rect x="-32" y="82" width="18" height="5" fill="#2a3a6a"/><rect x="-32" y="82" width="6" height="5" fill="#b33a3a"/><rect x="-20" y="82" width="6" height="5" fill="#e8e0d0"/>'
  + '<path d="M 18,82 L 28,82 L 26,89 L 23,92 L 20,89 Z" fill="#c8b07a"/>'
  + '<rect x="-38" y="172" width="76" height="10" fill="#1e1a1a"/><rect x="-6" y="172" width="12" height="10" fill="#c8b07a"/>'
  + '<path d="M -44,60 L -30,56 L -30,64 L -44,68 Z M 44,60 L 30,56 L 30,64 L 44,68 Z" fill="#5e4630"/>')
F["thana"] = figure("thana", "",
  leg("thana", -1, ("#7a5e42", "#8e7050", "#5e4630"), "#141214", "#0a0a0c") + leg("thana", 1, ("#7a5e42", "#8e7050", "#5e4630"), "#141214", "#0a0a0c"),
  th_torso,
  arm("thana", -1, ("#8a6c4c", "#a3845f", "#6c5238"), TH_SKIN) + arm("thana", 1, ("#8a6c4c", "#a3845f", "#6c5238"), TH_SKIN),
  hs(bc.th_head))

# Mother Lucia: seated in a wheelchair (front view)
LUC_SKIN = ("#efd6c6", "#d9b5a2")
# seated for real (revised): head and torso sit ~60 lower than a standing figure, thighs come toward us (lap + knees),
# shins drop to the footrest, big wheels in three-quarter view, armrests and push handles; same face, habit and hands.
SEAT = 60
chair_back = ('<path d="M -58,96 L -50,96 L -48,262 L -56,262 Z M 50,96 L 58,96 L 56,262 L 48,262 Z" fill="#3a3238"/>'
  '<path d="M -66,92 L -50,92 L -50,100 L -66,100 Z M 50,92 L 66,92 L 66,100 L 50,100 Z" fill="#1e1a1e"/>'   # push-handle grips
  '<rect x="-52" y="112" width="104" height="104" rx="4" fill="#2a2428"/><rect x="-52" y="112" width="104" height="8" fill="#3a3238"/>')
chair_front = ('<g><ellipse cx="-70" cy="262" rx="18" ry="66" fill="#1e1a1e"/><ellipse cx="-70" cy="262" rx="12" ry="56" fill="none" stroke="#6a646c" stroke-width="2.4"/>'
  + "".join(f'<path d="M -70,262 L {-70 + 11 * c:.1f},{262 + 54 * sn:.1f}" stroke="#8a848c" stroke-width=".9"/>' for c, sn in ((1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)))
  + '<circle cx="-70" cy="262" r="4" fill="#9a949c"/>'
  '<ellipse cx="70" cy="262" rx="18" ry="66" fill="#141216"/><ellipse cx="70" cy="262" rx="12" ry="56" fill="none" stroke="#4a444c" stroke-width="2.4"/>'
  + "".join(f'<path d="M 70,262 L {70 + 11 * c:.1f},{262 + 54 * sn:.1f}" stroke="#5a545c" stroke-width=".9"/>' for c, sn in ((1, 0), (.7, .7), (0, 1), (-.7, .7), (-1, 0), (-.7, -.7), (0, -1), (.7, -.7)))
  + '<circle cx="70" cy="262" r="4" fill="#6a646c"/></g>'
  '<path d="M -66,196 L -44,196 L -44,204 L -66,204 Z" fill="#2a2428"/><path d="M 44,196 L 66,196 L 66,204 L 44,204 Z" fill="#1e1a1e"/>'   # armrest pads
  '<path d="M -60,204 L -56,204 L -54,248 L -58,248 Z M 56,204 L 60,204 L 58,248 L 54,248 Z" fill="#3a3238"/>'
  '<path d="M -44,322 L -30,322 L -30,330 L -44,334 Z M 30,322 L 44,322 L 44,334 L 30,330 Z" fill="#4a4248"/><rect x="-44" y="330" width="88" height="6" fill="#4a4248"/>'   # footrests
  '<circle cx="-40" cy="346" r="7" fill="#1e1a1e"/><circle cx="40" cy="346" r="7" fill="#141216"/>')
def _down(svg): return f'<g transform="translate(0,{SEAT})">{svg}</g>'
luc_body = (_down(robe(HABIT, hem=150, flare=42)
    + '<path d="M -54,70 C -40,60 -24,58 -10,60 L -16,150 L -50,150 Z" fill="#a6a4ae"/><path d="M 54,70 C 40,60 24,58 10,60 L 16,150 L 50,150 Z" fill="#6c6a74"/>')
  + '<path d="M -46,204 L 46,204 L 48,246 L -48,246 Z" fill="#e6e0d5"/><path d="M -46,204 L 46,204 L 46,214 L -46,214 Z" fill="#f6f1e8"/>'   # lap: tops of the thighs catch the light
  + '<ellipse cx="-22" cy="242" rx="20" ry="9" fill="#efe9df"/><ellipse cx="22" cy="242" rx="20" ry="9" fill="#d8d0c4"/><path d="M -48,246 L 48,246 L 46,254 L -46,254 Z" fill="#bfb6a9"/>'   # knees + shadow under them
  + '<path d="M -40,254 L -6,254 L -8,324 L -36,324 Z" fill="#f2ede4"/><path d="M 6,254 L 40,254 L 36,324 L 8,324 Z" fill="#bfb6a9"/><path d="M -6,254 L 6,254 L 4,324 L -4,324 Z" fill="#a89e92"/>'
  + '<path d="M -10,200 C -12,220 -4,232 0,236 C 4,232 12,220 10,200" fill="none" stroke="#4a3328" stroke-width="2.6" stroke-dasharray="2.6 1.6" stroke-linecap="round"/>'
  + '<rect x="-1.4" y="236" width="2.8" height="14" fill="#3a2a22"/><rect x="-5" y="240" width="10" height="2.8" fill="#3a2a22"/>')
luc_arms = (part("luc-armL", '<path d="M -46,128 L -30,128 L -24,180 L -8,206 L -18,216 L -38,184 Z" fill="#a6a4ae"/><ellipse cx="-10" cy="210" rx="9" ry="7" fill="#efd6c6"/>', (-42, 126))
  + part("luc-armR", '<path d="M 46,128 L 30,128 L 24,180 L 8,206 L 18,216 L 38,184 Z" fill="#6c6a74"/><ellipse cx="10" cy="210" rx="9" ry="7" fill="#d9b5a2"/>', (42, 126)))
luc_legs = (part("luc-legL", f'<path d="M -34,324 L -10,324 L -10,334 L -34,334 Z" fill="{SHOE_BLACK}"/>', (-20, 254))
  + part("luc-legR", f'<path d="M 10,324 L 34,324 L 34,334 L 10,334 Z" fill="{SHOE_BLACK}"/>', (20, 254)))
F["luc"] = figure("luc", chair_back + _down(hs(bc.habit_back())), luc_legs, luc_body, luc_arms, _down(hs(bc.habit_over() + bc.luc_head)), chair_front).replace('id="luc-head" data-pivot="0,52"', f'id="luc-head" data-pivot="0,{52 + SEAT}"')

# ---------------- children (2549 flashback) ----------------
KH, KK, KA = 140, 214, 286  # hip, knee, ankle for kids
def kid(cid, head, skin, gown, tag, hand_extra_L="", hand_extra_R=""):
    m, l, d = gown
    legs = (leg(cid, -1, gown, skin[0], "#c9a088", skin=skin, pants_to=0, hip=KH, knee=KK, ankle=KA, w=(11, 8, 7))
            + leg(cid, 1, gown, skin[1], "#b98a72", skin=skin, pants_to=0, hip=KH, knee=KK, ankle=KA, w=(11, 8, 7)))
    body = (f'<path d="M -12,46 C -22,48 -30,52 -34,62 L -42,250 L 42,250 L 34,62 C 30,52 22,48 12,46 Z" fill="{m}"/>'
            f'<path d="M -34,62 C -30,52 -22,48 -14,47 C -18,90 -20,170 -20,250 L -42,250 Z" fill="{l}"/>'
            f'<path d="M 18,48 C 26,51 32,56 34,62 L 42,250 L 22,250 C 22,170 22,96 18,48 Z" fill="{d}"/>'
            f'<path d="M -12,46 C -8,54 8,54 12,46" fill="none" stroke="{d}" stroke-width="3"/>'
            f'<rect x="-18" y="72" width="28" height="11" rx="1.5" fill="#fbf8f2"/><text x="-4" y="80.5" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7" font-weight="700" fill="#b33a3a">{tag}</text>')
    arms = (arm(cid, -1, gown, skin, sh=(32, 58), el=(38, 112), wr=(40, 164), hand_extra=hand_extra_L)
            + arm(cid, 1, gown, skin, sh=(32, 58), el=(38, 112), wr=(40, 164), hand_extra=hand_extra_R))
    return figure(cid, "", legs, body, arms, head)

KID_GOWN = ("#ece6da", "#f8f4ec", "#c9c1b3")
F["mkid"] = kid("mkid", bc.mkid, ("#efc6a3", "#dba680"), KID_GOWN, "เมฆ")
F["jan"] = kid("jan", bc.pla, ("#f2cdab", "#dfaa86"), ("#f3e4e0", "#fdf3f0", "#d8c4bf"), "จันทร์")
DOLL = '<g transform="translate(46,170)"><path d="M -6,0 L 6,0 L 8,16 L -8,16 Z" fill="#e7b7c0"/><circle cx="0" cy="-5" r="6" fill="#f1cfd4"/><path d="M -6,-7 C -6,-13 6,-13 6,-7 Z" fill="#6a4a3a"/></g>'
KID_MOLE = '<circle cx="17.5" cy="10.5" r="1.35" fill="#5a3830"/>'   # the twins share Mariam's mole under the right eye (user)
F["twinM"] = kid("twinM", bc.twinM + KID_MOLE, ("#f6dcc4", "#e4b89c"), KID_GOWN, "มาเรียม", hand_extra_R=DOLL)
CANDLE = '<g transform="translate(-40,150)"><rect x="-2.5" y="-24" width="5" height="22" fill="#f1ebdd"/><path d="M 0,-34 C -3,-30 -3,-27 0,-25 C 3,-27 3,-30 0,-34 Z" fill="#fff4dc"/></g>'
F["twinA"] = kid("twinA", bc.twinA + bc.MARTHA_LID + KID_MOLE, ("#f6dcc4", "#e4b89c"), KID_GOWN, "มาร์ธา", hand_extra_L=CANDLE)

DEFS = NUN_DEFS + "".join(F.values())

# ---------------- sheet ----------------
ADULTS = [
 ("mek", "เมฆ", "31 · ผู้เล่าเรื่อง", "แจ็กเก็ตยีนส์ซีด เสื้อยืดขาว กางเกงยีนส์เข้ม รองเท้าผ้าใบขาว กล้องฟิล์มสะพายข้าง"),
 ("mariam", "ซิสเตอร์มาเรียม", "29 · แฝดที่รอด", "ชุดซิสเตอร์ยาวถึงข้อเท้า รองเท้าหนังดำ แผลไฟไหม้ที่หลังมือซ้าย"),
 ("agnes", "ซิสเตอร์อักเนส", "29 · ห้องพยาบาล (มาร์ธา)", "ผิวซีดจนเกือบเทา ยิ้มหลอน มือก็ซีด เป็นคนจริง ไม่ใช่วิญญาณ"),
 ("daeng", "ป้าแดง", "67 · แม่ครัว", "เสื้อลายดอกแขนสั้น ผ้าถุงสีม่วงเข้ม ผ้ากันเปื้อนยาวถึงเข่า รองเท้าแตะ พวงกุญแจที่เอว"),
 ("cat", "มาเธอร์คาทารีนา", "55 · อธิการิณี", "ชุดซิสเตอร์เต็มยศ กางเขนทองเหลือง"),
 ("rosa", "ซิสเตอร์โรซา", "22 · ซิสเตอร์ฝึกหัด", "ผ้าคลุมศีรษะสีขาว"),
 ("jos", "คุณพ่อยอแซฟ", "45 · บาทหลวง", "ชุดบาทหลวงขาวยาวถึงข้อเท้า คาดเอวดำ รองเท้าดำ"),
 ("thana", "ร.ต.อ.ธนา", "40 · ตำรวจ", "เสื้อกากีเหน็บในกางเกง เข็มขัดดำ กางเกงกากีเข้ม รองเท้าบูตดำ"),
 ("luc", "มาเธอร์ลูเซีย", "76 · นั่งรถเข็น", "นั่งรถเข็นตลอด มือวางบนตัก กำลูกประคำ เท้าวางบนที่พักเท้า"),
]
KIDS = [("mkid", "เมฆตอนเด็ก", "11"), ("jan", "จันทร์เจ้า", "8 · กิ๊บรูปพระจันทร์"), ("twinM", "มาเรียมตอนเด็ก", "9 · กอดตุ๊กตา"), ("twinA", "มาร์ธาตอนเด็ก", "9 · ถือเทียนมือซ้าย")]

def adult_card(cid, name, sub, desc):
    return (f'<figure><svg viewBox="-80 -70 160 450" role="img" aria-label="{name}"><rect x="-80" y="-70" width="160" height="450" fill="#1b1f2b"/>'
            f'<ellipse cx="0" cy="374" rx="52" ry="7" fill="#10131b"/><use href="#fb-{cid}"/></svg>'
            f'<figcaption><b>{name}</b> <span class="sub">{sub}</span><br>{desc}</figcaption></figure>')

kid_svg = '<svg viewBox="0 0 560 470" role="img" aria-label="เด็กในหอปี 2549"><rect width="560" height="470" fill="#1b1f2b"/><rect y="432" width="560" height="38" fill="#161a24"/>'
for i, (cid, k) in enumerate([("mkid", 1.18), ("jan", 1.0), ("twinM", 1.1), ("twinA", 1.1)]):
    x = 75 + i * 137
    y = 430 - 302 * k
    kid_svg += f'<ellipse cx="{x}" cy="432" rx="40" ry="6" fill="#10131b"/><g transform="translate({x},{y:.0f}) scale({k})"><use href="#fb-{cid}"/></g>'
kid_svg += '</svg>'

html = f'''<title>แม่ชีคนที่สอง ตัวละครเต็มตัว</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: responsive grid of full-body cards (5 / 3 / 2 columns) plus one wide card for the children. Single dark look by choice, matching the other character sheets. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a;
  --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); margin:0; }}
body {{ font-family:var(--font); padding:24px max(16px, env(safe-area-inset-right,0px)) 40px max(16px, env(safe-area-inset-left,0px)); }}
.wrap {{ max-width:1100px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
p.note {{ margin:0; font-size:13px; color:var(--muted); line-height:1.6; }}
.grid {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:16px; }}
@media (max-width:900px) {{ .grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure.wide {{ grid-column:1 / -1; }}
figure svg {{ display:block; width:100%; height:auto; border-radius:6px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:12.5px; color:var(--muted); line-height:1.6; }} figcaption b {{ color:var(--ink); font-weight:500; }}
.sub {{ font-size:12px; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{DEFS}</defs></svg>
<div class="wrap">
  <h1>แม่ชีคนที่สอง · ตัวละครเต็มตัว<span>หน้าตรง แสงจากซ้าย · แยกชิ้นขา แขน ตัว หัว ไว้ทำแอนิเมชัน</span></h1>
  <p class="note">ทุกตัวแยกเป็นชิ้น: ขาซ้าย ขาขวา (หมุนที่สะโพก) · ตัว · แขนซ้าย แขนขวา (หมุนที่หัวไหล่) · หัว (หมุนที่คอ) ชิ้นละกลุ่ม พร้อมจุดหมุนในไฟล์ เพื่อให้เดิน โบกมือ หันหน้าได้ตอนทำคลิป</p>
  <div class="grid">
{"".join(adult_card(*a) for a in ADULTS)}
    <figure class="wide">{kid_svg}<figcaption><b>เด็กในหอ ปี 2549</b> · เมฆตอนเด็ก (11) · จันทร์เจ้า (8) ผมแกละ <b>กิ๊บรูปพระจันทร์</b> ชุดนอนชมพูอ่อน · มาเรียมตอนเด็ก (9) กอดตุ๊กตา · มาร์ธาตอนเด็ก (9) ถือเทียนมือซ้าย · เด็กทุกคนเท้าเปล่า ชุดนอนยาวครึ่งแข้ง มีป้ายชื่อผ้าปักตัวแดง</figcaption></figure>
  </div>
</div>'''

if __name__ == "__main__":
    open(os.path.join(HERE, "cast.html"), "w").write(html)
    print("wrote cast.html", len(html) // 1024, "KB")
