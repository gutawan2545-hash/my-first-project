#!/usr/bin/env python3
"""Builds cast.html: character sheet for 'The Second Sister' supporting cast.
Same cut-out style as characters/*.html: flat block shading, light from the left, no outlines."""
import os

FACE = "M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,36 0,39 C -13,36 -28,22 -30,6 Z"
FACE_SQ = "M -32,-14 C -32,-46 32,-46 32,-14 L 32,8 C 31,24 18,37 0,39 C -18,37 -31,24 -32,8 Z"
FACE_KID = "M -30,-10 C -30,-44 30,-44 30,-10 L 29,8 C 27,22 14,32 0,34 C -14,32 -27,22 -29,8 Z"
FACE_ROUND = "M -33,-12 C -33,-45 33,-45 33,-12 L 32,8 C 30,24 16,36 0,38 C -16,36 -30,24 -32,8 Z"

def shading(sk, kid=False):
    """Block shading for light from the left: far cheek, temples, rim light, nose side, under chin."""
    s, sh, dp, tl, hi = sk
    return f'''
      <path d="M 16,-34 C 30,-28 34,-14 32,4 C 30,22 14,37 0,40 C 11,31 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{sh}"/>
      <path d="M 25,-24 L 34,-24 L 34,10 C 32,6 30,0 27,-8 Z" fill="{dp}"/>
      <path d="M -34,-24 L -23,-24 L -26,-8 L -34,-6 Z" fill="{tl}"/>
      <path d="M -33,-12 C -33,-30 -28,-38 -22,-41 C -28,-32 -29,-20 -29,-10 L -28,6 C -27,18 -21,28 -15,34 C -23,30 -29,20 -31,6 Z" fill="{hi}"/>
      <path d="M 2,{6 if kid else 4} L 6,{15 if kid else 15} L 1,{16 if kid else 16.5} Z" fill="{sh}"/>'''

def head(cid, face, sk, eyes, brows, mouth, extra="", back="", front="", neck=True, blush=.45, kid=False):
    s = sk[0]
    out = f'<g id="h-{cid}">'
    out += back
    if neck:
        out += f'<rect x="-8" y="20" width="16" height="38" fill="{sk[1]}"/><path d="M -8,26 L 8,26 L 8,46 Q 0,41 -8,49 Z" fill="{sk[2]}"/>'
    out += f'<clipPath id="fc-{cid}"><path d="{face}"/></clipPath>'
    out += f'<path d="{face}" fill="{s}"/><g clip-path="url(#fc-{cid})">{shading(sk, kid)}</g>'
    by = 14 if kid else 12
    out += f'<ellipse cx="-18" cy="{by}" rx="6.5" ry="3.4" fill="#ec8f88" opacity="{blush}"/><ellipse cx="18" cy="{by}" rx="6.5" ry="3.4" fill="#e0857e" opacity="{blush}"/>'
    out += brows + eyes + mouth + extra + front + '</g>'
    return out

# ---------- eyes ----------
def eyes_double(cid, iris="#3a241c", y=0, r=4.6, lashes=False, tired=False, two=True, big=False):
    k = 1.15 if big else 1
    shape = f"M -21,{-1+y} C -18,{-7.5*k+y} -8,{-7.5*k+y} -5,{-1+y} C -8,{3*k+y} -18,{3*k+y} -21,{-1+y} Z"
    lid = f"M -22,{0+y} C -19,{-8.5*k+y} -8,{-8.5*k+y} -4,{-2+y} L -5,{-1+y} C -9,{-5.6*k+y} -17,{-5.6*k+y} -21,{1+y} Z"
    crease = f"M -20,{-7*k+y} C -16,{-10.5*k+y} -9,{-10.5*k+y} -6,{-7.5*k+y}"
    g = f'<clipPath id="ec-{cid}"><path d="{shape}"/></clipPath>'
    one = f'''<path d="{shape}" fill="#f8efe6"/>
      <g clip-path="url(#ec-{cid})"><circle cx="-13" cy="{0+y}" r="{r*k}" fill="{iris}"/><circle cx="-13" cy="{0+y}" r="{r*k*.47}" fill="#160d0c"/></g>
      <path d="{lid}" fill="#1b1316"/>
      <path d="{crease}" fill="none" stroke="#b98670" stroke-width="1.1"/>'''
    if lashes:
        one += f'<path d="M -20.5,{-1.5+y} L -25,{-5+y} L -21.5,{0.5+y} Z" fill="#1b1316"/>'
    if tired:
        one += f'<path d="M -20,{4.2+y} C -15,{6.6+y} -10,{6.6+y} -6,{4+y}" fill="none" stroke="#b07a66" stroke-width="1" opacity=".8"/>'
    else:
        one += f'<path d="M -19,{2.6*k+y} C -15,{4.2*k+y} -10,{4.2*k+y} -6,{2.2*k+y}" fill="none" stroke="#c08672" stroke-width=".9"/>'
    g += one + f'<g transform="scale(-1,1)">{one}</g>'
    g += f'<circle cx="-14.8" cy="{-1.8+y}" r="{1.5*k}" fill="#fff"/><circle cx="11.2" cy="{-1.8+y}" r="{1.5*k}" fill="#fff"/>'
    if two:
        g += f'<circle cx="-11.4" cy="{1.8+y}" r=".7" fill="#ffe2bf"/><circle cx="14.6" cy="{1.8+y}" r=".7" fill="#ffe2bf"/>'
    return g

def eyes_mono(cid, iris="#21161a", y=0, r=4, narrow=False):
    h = 5.4 if narrow else 6.5
    shape = f"M -21,{-3+y} C -17,{-h+y} -9,{-h+y} -5,{-1.5+y} C -9,{0.8+y} -17,{0.8+y} -21,{-3+y} Z"
    lid = f"M -22.5,{-3+y} C -17,{-h-1.5+y} -9,{-h-1.5+y} -4,{-1.8+y} L -5,{-1+y} C -9,{-h+1.1+y} -17,{-h+1.1+y} -21,{-2+y} Z"
    g = f'<clipPath id="ec-{cid}"><path d="{shape}"/></clipPath>'
    one = f'''<path d="{shape}" fill="#f6eee6"/>
      <g clip-path="url(#ec-{cid})"><circle cx="-13" cy="{-1.6+y}" r="{r}" fill="{iris}"/></g>
      <path d="{lid}" fill="#1a1216"/>
      <path d="M -19,{0.6+y} C -15,{2.4+y} -10,{2.6+y} -6,{1.2+y}" fill="none" stroke="#c49680" stroke-width=".9"/>'''
    g += one + f'<g transform="scale(-1,1)">{one}</g>'
    g += f'<circle cx="-14.4" cy="{-2.9+y}" r="1.1" fill="#fff"/><circle cx="11.6" cy="{-2.9+y}" r="1.1" fill="#fff"/>'
    return g

def eyes_old(cid, iris="#2a1d1a", y=0, wide=False):
    h = 7 if wide else 5.2
    shape = f"M -20,{-1+y} C -17,{-h+y} -9,{-h+y} -6,{-1+y} C -9,{2+y} -17,{2+y} -20,{-1+y} Z"
    g = f'<clipPath id="ec-{cid}"><path d="{shape}"/></clipPath>'
    one = f'''<path d="{shape}" fill="{'#fbf6ee' if wide else '#f1e6dc'}"/>
      <g clip-path="url(#ec-{cid})"><circle cx="-13" cy="{-0.6+y}" r="{3.6 if wide else 3.4}" fill="{iris}"/></g>
      <path d="M -21,{-0.5+y} C -18,{-h-1.2+y} -9,{-h-1.2+y} -5,{-1.5+y} L -6,{-0.8+y} C -9,{-h+1.4+y} -17,{-h+1.4+y} -20,{0.2+y} Z" fill="#2a1d20"/>
      <path d="M -21,{-h-2.4+y} C -16,{-h-5+y} -9,{-h-5+y} -6,{-h-2.4+y}" fill="none" stroke="#b58b78" stroke-width="1"/>
      <path d="M -19,{3.6+y} C -15,{6+y} -10,{6+y} -7,{3.6+y} M -24,{-1+y} L -28,{-3+y} M -24,{1.5+y} L -28,{2+y}" fill="none" stroke="#b58b78" stroke-width=".9"/>'''
    g += one + f'<g transform="scale(-1,1)">{one}</g>'
    g += f'<circle cx="-14.2" cy="{-1.8+y}" r="{1.2 if wide else .9}" fill="#fff"/><circle cx="11.8" cy="{-1.8+y}" r="{1.2 if wide else .9}" fill="#fff"/>'
    return g

def brow(d, col, w=2.2):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/><path d="{d}" transform="scale(-1,1)" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'

def mouth(d, col, w=1.9, lower=None, lcol=None):
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
    if lower:
        s += f'<path d="{lower}" fill="none" stroke="{lcol}" stroke-width="1.4" stroke-linecap="round"/>'
    return s

# ---------- habit (from nuns-test-frame) ----------
def habit_back(veil="#1a1520"):
    return f'<path d="M -44,-30 C -46,-66 -22,-78 0,-78 C 22,-78 46,-66 44,-30 L 54,60 L 64,140 L -64,140 L -54,60 Z" fill="{veil}"/>'
def habit_front(veil="#1a1520", veil_hi="#3a3142", veil_lo="#120e16"):
    return f'''
    <path d="M -38,-24 C -38,-50 -20,-62 0,-62 C 20,-62 38,-50 38,-24 L 37,8 C 35,32 20,50 0,54 C -20,50 -35,32 -37,8 Z" fill="#ece6dc"/>'''
def wimple():
    return '''<path d="M -38,-24 C -38,-50 -20,-62 0,-62 C 20,-62 38,-50 38,-24 L 37,8 C 35,32 20,50 0,54 C -20,50 -35,32 -37,8 Z" fill="#ece6dc"/>
    <path d="M 31,-22 L 38,-22 L 37,8 C 35,32 20,50 0,54 C 20,46 30,30 31,0 Z" fill="#cdc4b7"/>
    <path d="M -24,40 C -12,48 12,48 24,40 C 18,48 10,52 0,54 C -10,52 -18,48 -24,40 Z" fill="#b9afa2"/>'''
def cap(veil="#1a1520", hi="#3a3142"):
    return f'''<path d="M -34,-14 C -34,-44 34,-44 34,-14 C 22,-22 -22,-22 -34,-14 Z" fill="#f3eee6"/>
    <path d="M 24,-34 C 31,-30 34,-22 34,-14 C 31,-16 28,-18 25,-19 Z" fill="#d3cabd"/>
    <path d="M -34,-14 C -22,-22 22,-22 34,-14" fill="none" stroke="#bdb3a5" stroke-width="1.2"/>
    <path d="M -44,-24 C -46,-66 -22,-78 0,-78 C 22,-78 46,-66 44,-24 L 37,-20 C 35,-40 20,-48 0,-48 C -20,-48 -35,-40 -37,-20 Z" fill="{veil}"/>
    <path d="M -38,-50 C -30,-66 -16,-73 -2,-74 C -16,-68 -28,-58 -33,-42 Z" fill="{hi}"/>'''
def habit_body(robe=("#e6e0d5","#f6f1e8","#bfb6a9"), **_):
    m, l, d = robe
    return f'''
    <path d="M -16,54 C -30,56 -44,62 -50,74 L -58,260 L 58,260 L 50,74 C 44,62 30,56 16,54 Z" fill="{m}"/>
    <path d="M -50,74 C -44,62 -30,56 -18,55 C -26,90 -28,150 -28,260 L -58,260 Z" fill="{l}"/>
    <path d="M 22,56 C 36,59 46,65 50,74 L 58,260 L 30,260 C 30,150 30,96 22,56 Z" fill="{d}"/>'''
def habit_over(vhi="#2c2532", vlo="#120e16"):
    return f'''
    <path d="M -44,-26 L -54,62 L -64,138 L -50,134 L -42,64 L -37,-20 Z" fill="{vhi}"/>
    <path d="M 44,-26 L 54,62 L 64,138 L 50,134 L 42,64 L 37,-20 Z" fill="{vlo}"/>
    <path d="M -28,42 C -18,54 18,54 28,42 L 40,66 C 26,76 -26,76 -40,66 Z" fill="#f3eee6"/>
    <path d="M 14,52 C 22,50 26,46 28,42 L 40,66 C 34,70 28,72 22,73 Z" fill="#cdc4b7"/>'''
def nun_head(cid, sk, eyes, brows, mouth_, extra="", veil="#1a1520", hi="#3a3142", blush=.45):
    # wimple goes behind the face; cap on top
    h = head(cid, FACE, sk, eyes, brows, mouth_, extra=extra, back=wimple(), front=cap(veil, hi), neck=False, blush=blush)
    return h

# ---------- palettes ----------
SK_MEK   = ("#eec4a2", "#d9a27e", "#b98262", "#e2b393", "#fbdcc0")
SK_DAENG = ("#e3b088", "#c98f69", "#a8714f", "#d6a07a", "#f2c8a2")
SK_CAT   = ("#f1d3bd", "#dcb19a", "#bf917a", "#e6c3ac", "#fbe6d6")
SK_LUC   = ("#efd6c6", "#d9b5a2", "#bd9583", "#e4c6b5", "#fbeadf")
SK_ROSA  = ("#f5d3b4", "#e2b08f", "#c78f6e", "#ebc2a2", "#ffe7d0")
SK_JOS   = ("#ebc6a6", "#d4a585", "#b78666", "#e0b797", "#f9dcc3")
SK_THANA = ("#d9a37c", "#bf875f", "#9c6845", "#cd9670", "#ecbc94")
SK_KIDM  = ("#efc6a3", "#dba680", "#bd8763", "#e4b693", "#fcdcc0")
SK_PLA   = ("#f2cdab", "#dfaa86", "#c38d69", "#e8bd9a", "#ffe2c6")
SK_TWIN  = ("#f6dcc4", "#e4b89c", "#c99478", "#ecc9ae", "#fff0e2")

HAIR = "#1a1619"; HAIR_HI = "#3a3238"

def hs(svg, k=0.82):
    """Shrink a head (and anything attached to it) around the collar line so the neck still meets the body."""
    return f'<g transform="translate(0,{50*(1-k):.1f}) scale({k})">{svg}</g>'


cards = []

# ===== 1. MEK =====
mek_back = f'<path d="M -37,-8 C -41,-42 -24,-62 0,-63 C 24,-62 41,-42 37,-8 L 35,18 L 28,12 L -28,12 L -35,18 Z" fill="{HAIR}"/>'
mek_front = f'''<path d="M -37,-6 C -42,-38 -28,-60 -4,-62 C 22,-64 42,-46 37,-6 L 33,-16 L 31,-2 C 27,-16 23,-24 15,-29 C 11,-19 2,-13 -9,-11 L -7,-20 C -15,-15 -23,-10 -30,-2 L -32,-14 Z" fill="{HAIR}"/>
  <path d="M -30,-42 C -22,-55 -9,-60 3,-60 C -8,-55 -18,-48 -24,-36 Z" fill="{HAIR_HI}"/>
  <path d="M 15,-29 L 22,-40 L 20,-24 Z M -9,-11 L -2,-30 L -3,-14 Z" fill="#2b2428"/>'''
mek_extra = '<path d="M -15,23 C -9,35 9,35 15,23 C 12,32 6,37 0,38 C -6,37 -12,32 -15,23 Z" fill="#b98262" opacity=".28"/><path d="M -6,18 Q 0,17 6,18" fill="none" stroke="#b98262" stroke-width="1" opacity=".5"/>'
mek_head = head("mek", FACE, SK_MEK,
    eyes_double("mek", iris="#2e1f18", r=4.4, tired=False, two=True),
    brow("M -23,-12.4 C -18,-13.6 -11,-13.8 -7,-12.8", "#1e1719", 2.4),
    mouth("M -6,23.4 Q 0,24.6 6,23", "#a8705e", 1.9, "M -3,26.4 Q 0,27.4 3,26.4", "#d9a08a"),
    extra=mek_extra, back=mek_back, front=mek_front)
mek_body = '''
  <path d="M -16,52 C -32,54 -46,60 -52,74 L -58,260 L 58,260 L 52,74 C 46,60 32,54 16,52 Z" fill="#5d6f8a"/>
  <path d="M -52,74 C -46,60 -32,54 -18,53 C -24,90 -28,170 -30,260 L -58,260 Z" fill="#7889a6"/>
  <path d="M 24,55 C 38,58 48,64 52,74 L 58,260 L 34,260 C 34,170 32,100 24,55 Z" fill="#45546c"/>
  <path d="M -15,52 C -10,60 10,60 15,52 L 18,260 L -18,260 Z" fill="#e8e4dc"/>
  <path d="M 6,58 L 18,260 L 10,260 L 4,60 Z" fill="#c9c3b8"/>
  <path d="M -15,52 C -10,60 10,60 15,52" fill="none" stroke="#cfc9be" stroke-width="3"/>
  <path d="M -18,54 L -12,130 L -20,260 M 18,54 L 12,130 L 20,260" fill="none" stroke="#3b4860" stroke-width="2.2"/>
  <path d="M -40,90 L -28,90 L -28,104 L -40,104 Z" fill="#4c5c76"/>
  <path d="M -34,58 L 40,170" stroke="#2a2420" stroke-width="4.5"/>
  <rect x="22" y="160" width="34" height="22" rx="3" fill="#2b2b30"/><rect x="22" y="160" width="34" height="5" fill="#45454c"/>
  <circle cx="39" cy="173" r="8" fill="#16161a"/><circle cx="39" cy="173" r="4.5" fill="#3a4a66"/><circle cx="37" cy="171" r="1.4" fill="#cfd8ec"/>
  <rect x="25" y="156" width="8" height="4" fill="#45454c"/>'''
cards.append(("mek", "เมฆ", "31 ปี · ผู้เล่าเรื่อง · ช่างภาพ อดีตเด็กกำพร้าที่นี่",
  "ผิวสองสีอมพีช · ผมดำยุ่งยาวระคิ้ว ปอยใหญ่ปัดข้าง ยาวคลุมต้นคอ · ตาสองชั้นหนังตาหนัก ดูเหนื่อย มีถุงใต้ตาจาง ๆ · คิ้วหนาตรง · หนวดเคราเขียวจาง ๆ ที่คาง · แจ็กเก็ตยีนส์ซีดทับเสื้อยืดขาว กล้องฟิล์มสะพายข้าง · ไม่ใส่แว่น ไม่ใส่หูฟัง (ให้ต่างจากเจมส์ชัด)",
  mek_body + hs(mek_head), [("#eec4a2","ผิว"),("#d9a27e","ผิวเงา"),("#1a1619","ผม"),("#5d6f8a","แจ็กเก็ต"),("#e8e4dc","เสื้อยืด"),("#a8705e","ปาก")]))

# ===== 2. PA DAENG =====
dg_back = '<path d="M -40,-10 C -46,-46 -26,-64 0,-64 C 26,-64 46,-46 40,-10 L 38,8 L -38,8 Z" fill="#a9a4a6"/>'
dg_front = '''<path d="M -40,-8 C -48,-30 -40,-56 -18,-62 C -6,-68 10,-68 22,-62 C 42,-54 48,-30 40,-8 C 38,-18 34,-24 30,-26 C 30,-34 22,-38 16,-34 C 12,-42 2,-42 -2,-36 C -8,-42 -18,-40 -20,-32 C -28,-34 -34,-26 -32,-18 C -36,-16 -38,-12 -40,-8 Z" fill="#b9b4b6"/>
  <g fill="#d6d1d2"><circle cx="-24" cy="-48" r="6"/><circle cx="-10" cy="-56" r="6.5"/><circle cx="6" cy="-56" r="6"/><circle cx="-34" cy="-32" r="5"/></g>
  <g fill="#8f8a8d"><circle cx="22" cy="-48" r="6"/><circle cx="34" cy="-30" r="5"/><circle cx="16" cy="-58" r="4"/></g>'''
dg_extra = '<path d="M -14,14 C -12,20 -9,22 -7,23 M 14,14 C 12,20 9,22 7,23" fill="none" stroke="#a8714f" stroke-width="1" opacity=".7"/><path d="M -18,-24 L -8,-25 M 8,-25 L 18,-24" stroke="#c98f69" stroke-width="1" opacity=".6"/>'
dg_head = head("daeng", FACE_ROUND, SK_DAENG,
    eyes_old("daeng", iris="#2a1b16"),
    brow("M -22,-11 C -17,-14 -11,-14 -6,-12.5", "#6e6466", 2),
    mouth("M -8,22 Q 0,28 8,22", "#8e4e48", 2, "M -4,26 Q 0,27.6 4,26", "#c98f7a"),
    extra=dg_extra, back=dg_back, front=dg_front, blush=.5)
dg_body = '''
  <path d="M -16,52 C -34,54 -50,62 -56,78 L -62,260 L 62,260 L 56,78 C 50,62 34,54 16,52 Z" fill="#8a3a3e"/>
  <path d="M -56,78 C -50,62 -34,54 -20,53 C -28,96 -32,180 -34,260 L -62,260 Z" fill="#a54a4e"/>
  <path d="M 26,55 C 42,59 52,66 56,78 L 62,260 L 38,260 C 38,180 34,100 26,55 Z" fill="#6c2b30"/>
  <g fill="#e9c6b0" opacity=".55"><circle cx="-40" cy="100" r="2.2"/><circle cx="-30" cy="130" r="2.2"/><circle cx="-44" cy="160" r="2.2"/><circle cx="40" cy="96" r="2.2"/><circle cx="46" cy="140" r="2.2"/></g>
  <path d="M -14,52 C -8,62 8,62 14,52" fill="none" stroke="#6c2b30" stroke-width="3"/>
  <path d="M -36,88 L 36,88 L 42,260 L -42,260 Z" fill="#8fa3b0"/>
  <path d="M -36,88 L -16,88 L -20,260 L -42,260 Z" fill="#a9bbc6"/>
  <path d="M 18,88 L 36,88 L 42,260 L 24,260 Z" fill="#748894"/>
  <path d="M -36,88 C -34,72 -26,62 -14,56 M 36,88 C 34,72 26,62 14,56" fill="none" stroke="#8fa3b0" stroke-width="4"/>
  <rect x="-20" y="150" width="40" height="26" fill="#748894"/><rect x="-20" y="150" width="40" height="4" fill="#667a86"/>
  <path d="M 44,200 m -9,0 a 9,9 0 1 0 18,0 a 9,9 0 1 0 -18,0" fill="none" stroke="#b49a5a" stroke-width="2.4"/>
  <path d="M 40,206 l -3,16 l 4,0 l 1,-5 l 3,0 l 0,-3 l -3,0 Z M 48,207 l 2,14 l 4,-1 l -1,-5 Z" fill="#c9ad66"/>'''
cards.append(("daeng", "ป้าแดง", "67 ปี · แม่ครัวใหญ่ ผู้ตายใน EP1",
  "ผิวคล้ำอุ่นกว่าทุกคน · หน้ากลมเต็ม แก้มอิ่ม · ผมหงอกสั้นดัดลอนเป็นก้อน · ตาเล็กมีตีนกา ร่องแก้มลึก · ยิ้มกว้างใจดี · เสื้อลายดอกเล็กสีแดงเลือดหมู ผ้ากันเปื้อนสีฟ้าเทา · พวงกุญแจใหญ่ทองเหลืองที่เอว (สำคัญในเรื่อง)",
  dg_body + hs(dg_head), [("#e3b088","ผิว"),("#c98f69","ผิวเงา"),("#b9b4b6","ผม"),("#8a3a3e","เสื้อ"),("#8fa3b0","ผ้ากันเปื้อน"),("#b49a5a","กุญแจ")]))

# ===== 3. MOTHER CATARINA =====
cat_extra = '''<g fill="none" stroke="#141216" stroke-width="2.6"><rect x="-23" y="-8" width="18" height="12" rx="2"/><rect x="5" y="-8" width="18" height="12" rx="2"/></g>
  <path d="M -5,-3 L 5,-3 M -23,-4 L -31,-5 M 23,-4 L 31,-5" stroke="#141216" stroke-width="2.2"/>
  <path d="M -21,-6 L -17,-6" stroke="#8a8a98" stroke-width="1.2"/>
  <path d="M -10,17 C -12,22 -12,26 -9,29 M 10,17 C 12,22 12,26 9,29" fill="none" stroke="#bf917a" stroke-width="1" opacity=".7"/>'''
cat_head = nun_head("cat", SK_CAT,
    eyes_mono("cat", iris="#1e1416", narrow=True),
    brow("M -23,-12.5 L -6,-11", "#2a2024", 2.4),
    mouth("M -7,24 L 7,24", "#93605e", 1.9, "M -3,26.6 L 3,26.6", "#c99a8e"),
    extra=cat_extra)
cat_body = hs(habit_back()) + habit_body() + '''
  <path d="M -1.6,74 L 1.6,74 L 1.6,108 L -1.6,108 Z M -9,82 L 9,82 L 9,85.5 L -9,85.5 Z" fill="#9a8a5a"/>
  <rect x="-40" y="150" width="34" height="44" rx="2" fill="#3b3f4a" transform="rotate(-6 -23 172)"/><rect x="-40" y="150" width="8" height="44" fill="#535866" transform="rotate(-6 -23 172)"/>'''
cards.append(("cat", "มาเธอร์คาทารีนา", "55 ปี · อธิการิณีคนปัจจุบัน",
  "หน้ายาวเรียว ผิวขาวเหลือง · แว่นกรอบดำเหลี่ยมหนา · ตาชั้นเดียวแคบ คิ้วตรงต่ำ · ปากตรงเป็นเส้น ไม่ยิ้ม · ร่องข้างจมูกชัด · ชุดซิสเตอร์เต็มยศ กางเขนทองเหลืองที่อก ถือแฟ้มเอกสารสีเข้มเสมอ",
  cat_body + hs(habit_over() + cat_head), [("#f1d3bd","ผิว"),("#dcb19a","ผิวเงา"),("#141216","แว่น"),("#93605e","ปาก"),("#9a8a5a","กางเขน")]))

# ===== 4. MOTHER LUCIA =====
luc_extra = '''<path d="M -26,4 C -24,14 -20,22 -14,27 M 26,4 C 24,14 20,22 14,27" fill="none" stroke="#bd9583" stroke-width="1.2" opacity=".8"/>
  <path d="M -12,18 C -14,24 -13,29 -10,32 M 12,18 C 14,24 13,29 10,32 M -6,31 Q 0,34 6,31" fill="none" stroke="#bd9583" stroke-width="1" opacity=".7"/>
  <path d="M -16,-10 C -12,-12 -8,-12 -5,-11" fill="none" stroke="#d9b5a2" stroke-width=".9"/>'''
luc_head = nun_head("luc", SK_LUC,
    eyes_old("luc", iris="#47566a", wide=True),
    brow("M -22,-13 C -17,-15.5 -11,-15.5 -6,-13.5", "#a8a0a4", 1.8),
    mouth("M -6,23 Q 0,25.4 6,23", "#a27a78", 1.6),
    extra=luc_extra, blush=.25)
luc_body = '''<path d="M -78,40 L -70,40 L -66,260 L -76,260 Z M 70,40 L 78,40 L 76,260 L 66,260 Z" fill="#3a3238"/><rect x="-78" y="36" width="156" height="10" rx="4" fill="#4a4248"/>''' + hs(habit_back()) + habit_body() + '''
  <path d="M -54,70 C -40,60 -24,58 -10,60 L -18,260 L -60,260 Z" fill="#8c8a94"/>
  <path d="M -54,70 C -46,64 -36,61 -26,60 L -34,260 L -60,260 Z" fill="#a6a4ae"/>
  <path d="M 54,70 C 40,60 24,58 10,60 L 18,260 L 60,260 Z" fill="#6c6a74"/>
  <path d="M -10,140 C -12,170 -4,190 0,196 C 4,190 12,170 10,140" fill="none" stroke="#4a3328" stroke-width="2.6" stroke-dasharray="2.6 1.6" stroke-linecap="round"/>
  <rect x="-1.4" y="196" width="2.8" height="16" fill="#3a2a22"/><rect x="-5" y="200" width="10" height="2.8" fill="#3a2a22"/>
  <path d="M -16,128 C -12,122 -2,122 2,128 L 3,142 C -2,148 -12,148 -16,142 Z" fill="#efd6c6"/>
  <path d="M 16,128 C 12,122 2,122 0,128 L 0,142 C 2,148 12,148 16,142 Z" fill="#d9b5a2"/>'''
cards.append(("luc", "มาเธอร์ลูเซีย", "76 ปี · อธิการิณีในคืนไฟไหม้ ผู้เขียนกฎ 7 ข้อ · สมองเสื่อม",
  "ผิวซีดบาง ริ้วรอยลึกรอบปากและแก้ม · คิ้วจางสีเทา · **ตาโตใสสีเทาอมฟ้าผิดปกติ** เวลาจำเรื่องเก่าได้ (จุดที่ทำให้หลอน) · ยิ้มบางเหมือนคุยกับเด็ก · คลุมเสื้อไหมพรมสีเทาทับชุดซิสเตอร์ นั่งรถเข็นสีเข้ม กำลูกประคำไม้",
  luc_body + hs(habit_over() + luc_head), [("#efd6c6","ผิว"),("#d9b5a2","ผิวเงา"),("#47566a","ตา"),("#8c8a94","เสื้อไหมพรม"),("#3a3238","รถเข็น")]))

# ===== 5. SISTER ROSA (novice: white veil) =====
rosa_extra = '<g fill="#c78f6e" opacity=".45"><circle cx="-20" cy="7" r=".9"/><circle cx="-16" cy="9" r=".8"/><circle cx="-22" cy="10" r=".7"/><circle cx="20" cy="7" r=".9"/><circle cx="16" cy="9" r=".8"/><circle cx="22" cy="10" r=".7"/></g>'
rosa_head = head("rosa", FACE_ROUND, SK_ROSA,
    eyes_double("rosa", iris="#3e2418", r=5, lashes=True, big=True),
    brow("M -22,-13 C -17,-15 -11,-17 -6,-18.5", "#3a2622", 2.1),
    '<ellipse cx="0" cy="24" rx="4" ry="3.2" fill="#8e4a4c"/><ellipse cx="0" cy="25.4" rx="2.4" ry="1.4" fill="#d27e7e"/>',
    extra=rosa_extra, back=wimple(), front=cap("#f4f0e8", "#ffffff"), neck=False, blush=.55)
rosa_body = hs(habit_back("#e9e4da")) + habit_body() + '''
  <path d="M -16,118 C -12,112 -2,112 2,118 L 3,134 C -2,140 -12,140 -16,134 Z" fill="#f5d3b4"/>
  <path d="M 16,118 C 12,112 2,112 0,118 L 0,134 C 2,140 12,140 16,134 Z" fill="#e2b08f"/>
  <path d="M -50,76 C -60,96 -60,118 -52,134 L -14,138 L -10,120 L -36,112 C -38,100 -40,88 -44,80 Z" fill="#f6f1e8"/>
  <path d="M 50,76 C 60,96 60,118 52,134 L 14,138 L 10,120 L 36,112 C 38,100 40,88 44,80 Z" fill="#bfb6a9"/>
  <path d="M -6,132 C -10,150 -4,164 0,170 C 4,164 10,150 6,132" fill="none" stroke="#6a4a3a" stroke-width="2.2" stroke-dasharray="2.2 1.6" stroke-linecap="round"/>'''
cards.append(("rosa", "ซิสเตอร์โรซา", "22 ปี · ซิสเตอร์ฝึกหัด ขี้กลัว ช่างพูด",
  "หน้ากลม แก้มป่อง ฝ้ากระจาง ๆ ที่แก้ม · ตาสองชั้นโตกลม ขนตางอน คิ้วยกสูงตลอด (ตกใจง่าย) · ปากเปิดเล็ก ๆ เหมือนกำลังจะพูด · **ผ้าคลุมศีรษะสีขาว** เพราะยังเป็นซิสเตอร์ฝึกหัด ทำให้แยกจากซิสเตอร์คนอื่นได้ทันที · กำลูกประคำ",
  hs(habit_back("#e9e4da")) + habit_body() + hs(habit_over("#f7f3ec", "#c7bfb2")) + rosa_body.split(habit_body(),1)[1] + hs(rosa_head), [("#f5d3b4","ผิว"),("#e2b08f","ผิวเงา"),("#e9e4da","ผ้าคลุมขาว"),("#8e4a4c","ปาก")]))

# ===== 6. FATHER JOSEPH =====
jos_back = '<path d="M -34,-8 C -38,-42 -22,-58 0,-59 C 22,-58 38,-42 34,-8 L 32,4 L -32,4 Z" fill="#232025"/>'
jos_front = '''<path d="M -34,-8 C -38,-40 -22,-58 0,-59 C 22,-58 38,-40 34,-8 L 31,-18 C 28,-30 18,-38 2,-38 C -14,-38 -26,-32 -31,-18 Z" fill="#232025"/>
  <path d="M -34,-8 L -31,-18 L -29,-6 Z M 34,-8 L 31,-18 L 29,-6 Z" fill="#8f8a90"/>
  <path d="M -26,-44 C -18,-53 -6,-56 4,-56 C -6,-52 -16,-46 -21,-38 Z" fill="#45404a"/>'''
jos_extra = '<path d="M -10,16 C -12,21 -11,25 -8,28 M 10,16 C 12,21 11,25 8,28" fill="none" stroke="#b78666" stroke-width="1" opacity=".6"/>'
jos_head = head("jos", FACE, SK_JOS,
    eyes_double("jos", iris="#2a1c16", r=4.2, tired=True, two=False),
    brow("M -22,-13.5 C -17,-14 -11,-15 -6,-16.5", "#2a2226", 2.1),
    mouth("M -6,24 Q 0,22.6 6,24", "#9a6458", 1.8),
    extra=jos_extra, back=jos_back, front=jos_front)
jos_head = f'<g transform="scale(1,1.06)">{jos_head}</g>'
jos_body = '''
  <path d="M -14,54 C -30,56 -42,62 -48,74 L -54,260 L 54,260 L 48,74 C 42,62 30,56 14,54 Z" fill="#ece8e0"/>
  <path d="M -48,74 C -42,62 -30,56 -16,55 C -22,100 -26,180 -26,260 L -54,260 Z" fill="#faf7f1"/>
  <path d="M 22,56 C 34,59 44,65 48,74 L 54,260 L 30,260 C 30,180 30,100 22,56 Z" fill="#c4bdb2"/>
  <rect x="-13" y="52" width="26" height="9" rx="2" fill="#16141a"/><rect x="-4" y="54" width="8" height="5" fill="#f4f1ea"/>
  <g fill="#bcb4a8"><circle cx="0" cy="80" r="1.8"/><circle cx="0" cy="98" r="1.8"/><circle cx="0" cy="116" r="1.8"/><circle cx="0" cy="134" r="1.8"/><circle cx="0" cy="152" r="1.8"/><circle cx="0" cy="170" r="1.8"/></g>
  <path d="M 0,62 L 0,260" stroke="#d6d0c6" stroke-width="1.2"/>
  <path d="M -34,150 L 34,150 L 36,160 L -36,160 Z" fill="#1d1a20"/>'''
cards.append(("jos", "คุณพ่อยอแซฟ", "45 ปี · บาทหลวงประจำโบสถ์ รู้ความลับจากคำสารภาพ",
  "สูง หน้ายาว ผิวสองสี · ผมดำสั้นเรียบ แซมเทาที่ขมับ · ตาสองชั้นเศร้า หนังตาหนัก คิ้วตกที่หาง · ปากโค้งลงนิด ๆ · ชุดบาทหลวงสีขาว คอปกโรมันดำ คาดเอวดำ · มือสั่นเวลาโกหก (ใช้ในฉาก)",
  jos_body + hs(jos_head), [("#ebc6a6","ผิว"),("#d4a585","ผิวเงา"),("#232025","ผม"),("#ece8e0","ชุดบาทหลวง"),("#16141a","คอปก")]))

# ===== 7. POLICE CAPTAIN THANA =====
th_back = '<path d="M -35,-10 C -38,-44 -22,-58 0,-58 C 22,-58 38,-44 35,-10 Z" fill="#1c1a1d"/>'
th_front = '''<path d="M -35,-8 C -38,-42 -22,-57 0,-57 C 22,-57 38,-42 35,-8 L 32,-14 C 30,-28 18,-36 0,-36 C -18,-36 -30,-28 -32,-14 Z" fill="#1c1a1d"/>
  <path d="M -32,-14 C -30,-28 -18,-36 0,-36 C 18,-36 30,-28 32,-14 L 32,-22 C 26,-44 -26,-44 -32,-22 Z" fill="#3a3538" opacity=".7"/>'''
th_extra = '''<path d="M -17,20 C -10,34 10,34 17,20 C 14,32 8,38 0,39 C -8,38 -14,32 -17,20 Z" fill="#7a5038" opacity=".38"/>
  <path d="M -9,17 Q 0,15 9,17" fill="none" stroke="#7a5038" stroke-width="2.4" opacity=".55"/>
  <path d="M -21,5 C -16,7.6 -10,7.6 -6,5" fill="none" stroke="#9c6845" stroke-width="1.2"/>'''
th_head = head("thana", FACE_SQ, SK_THANA,
    eyes_mono("thana", iris="#1e1414"),
    brow("M -24,-12 L -6,-13", "#141114", 3.4),
    mouth("M -7,25 Q 0,24 7,25.6", "#7c4a3e", 2),
    extra=th_extra, back=th_back, front=th_front, blush=.2)
th_body = '''
  <path d="M -16,52 C -34,54 -48,60 -54,74 L -60,260 L 60,260 L 54,74 C 48,60 34,54 16,52 Z" fill="#8a6c4c"/>
  <path d="M -54,74 C -48,60 -34,54 -20,53 C -26,100 -30,180 -32,260 L -60,260 Z" fill="#a3845f"/>
  <path d="M 26,55 C 40,58 50,64 54,74 L 60,260 L 36,260 C 36,180 34,100 26,55 Z" fill="#6c5238"/>
  <path d="M -16,52 L 0,72 L 16,52 L 22,58 L 0,84 L -22,58 Z" fill="#7a5e42"/>
  <path d="M 0,72 L 0,260" stroke="#6c5238" stroke-width="1.6"/>
  <g fill="#c8b07a"><circle cx="0" cy="100" r="2"/><circle cx="0" cy="130" r="2"/><circle cx="0" cy="160" r="2"/><circle cx="0" cy="190" r="2"/></g>
  <rect x="-40" y="96" width="24" height="20" rx="2" fill="#7a5e42"/><rect x="16" y="96" width="24" height="20" rx="2" fill="#5e4630"/>
  <path d="M -40,96 L -16,96 L -16,102 L -40,102 Z M 16,96 L 40,96 L 40,102 L 16,102 Z" fill="#6c5238"/>
  <rect x="-38" y="84" width="20" height="5" fill="#2a3a6a"/><rect x="-38" y="84" width="7" height="5" fill="#b33a3a"/><rect x="-24" y="84" width="6" height="5" fill="#e8e0d0"/>
  <path d="M 22,84 L 34,84 L 32,92 L 28,95 L 24,92 Z" fill="#c8b07a"/>
  <path d="M -56,62 L -36,58 L -36,66 L -56,70 Z M 56,62 L 36,58 L 36,66 L 56,70 Z" fill="#5e4630"/>
  <path d="M -54,64 L -40,61 M 54,64 L 40,61" stroke="#c8b07a" stroke-width="1.6"/>'''
cards.append(("thana", "ร.ต.อ.ธนา", "40 ปี · ตำรวจ สน.บางกอกน้อย",
  "ผิวคล้ำ หน้าเหลี่ยมกรามกว้าง · ผมสั้นเกรียนรองทรง · ตาชั้นเดียวง่วง มีถุงใต้ตาชัด · คิ้วหนาเข้ม · หนวดเคราเขียวครึ้ม · ชุดตำรวจสีกากี กระดุมทอง ป้ายสีเล็ก ๆ ที่อก (ลดรายละเอียดเครื่องหมายจริง) · พูดน้อย หน้าเหนื่อยแต่ยุติธรรม",
  th_body + hs(th_head), [("#d9a37c","ผิว"),("#bf875f","ผิวเงา"),("#1c1a1d","ผม"),("#8a6c4c","ชุดกากี"),("#c8b07a","กระดุม")]))

# ===== 8. KIDS (2549 flashback lineup) =====
def nightgown(col=("#ece6da","#f8f4ec","#c9c1b3"), tag=None, w=46, h=200):
    m, l, d = col
    s = f'''<path d="M -12,46 C -24,48 -36,54 -40,64 L -{w},{h} L {w},{h} L 40,64 C 36,54 24,48 12,46 Z" fill="{m}"/>
    <path d="M -40,64 C -36,54 -24,48 -14,47 C -20,90 -22,150 -22,{h} L -{w},{h} Z" fill="{l}"/>
    <path d="M 18,48 C 28,51 36,56 40,64 L {w},{h} L 24,{h} C 24,150 24,96 18,48 Z" fill="{d}"/>
    <path d="M -12,46 C -8,54 8,54 12,46" fill="none" stroke="{d}" stroke-width="3"/>'''
    if tag:
        s += f'<rect x="-34" y="76" width="26" height="11" rx="1.5" fill="#fbf8f2"/><text x="-21" y="84.5" text-anchor="middle" font-family="IBM Plex Sans Thai, sans-serif" font-size="7" font-weight="700" fill="#b33a3a">{tag}</text>'
    return s

bob_back = f'<path d="M -38,-6 C -42,-44 -22,-62 0,-62 C 22,-62 42,-44 38,-6 L 40,24 L 26,26 L -26,26 L -40,24 Z" fill="{HAIR}"/>'
bob_front = f'''<path d="M -38,-6 C -42,-44 -22,-62 0,-62 C 22,-62 42,-44 38,-6 L 34,-4 L 33,-20 L -33,-20 L -34,-4 Z" fill="{HAIR}"/>
  <path d="M -38,-6 L -34,-4 L -36,22 L -40,24 Z M 38,-6 L 34,-4 L 36,22 L 40,24 Z" fill="{HAIR}"/>
  <path d="M -30,-42 C -22,-55 -9,-60 3,-60 C -8,-55 -18,-48 -24,-36 Z" fill="{HAIR_HI}"/>'''
twinM = head("twinM", FACE_KID, SK_TWIN, eyes_double("twinM", iris="#4a2c22", y=3, r=5, big=True),
    brow("M -21,-9 C -16,-11.5 -10,-11.5 -6,-10", "#3a2a26", 2),
    mouth("M -6,22 Q 0,26.6 6,22", "#b5767a", 2), back=bob_back, front=bob_front, kid=True, blush=.55)
twinA = head("twinA", FACE_KID, SK_TWIN, eyes_double("twinA", iris="#1e1416", y=3.4, r=5, big=True, two=False),
    brow("M -21,-9.5 L -6,-10", "#3a2a26", 2),
    mouth("M -5,23 L 5,23", "#a8706e", 1.8), back=bob_back, front=bob_front, kid=True, blush=.3)
# Martha: heavy lid over the top of the eye, flat stare
MARTHA_LID = '<path d="M -22,-1 C -18,-6 -8,-6 -4,-1 L -5,0 C -9,-3.2 -17,-3.2 -21,0.4 Z M 22,-1 C 18,-6 8,-6 4,-1 L 5,0 C 9,-3.2 17,-3.2 21,0.4 Z" fill="#1b1316" transform="translate(0,3.6)"/>'
twinA = twinA.replace('</g>', '', 0)
pla_back = f'<path d="M -36,-6 C -40,-42 -22,-60 0,-60 C 22,-60 40,-42 36,-6 Z" fill="{HAIR}"/><path d="M -36,-8 C -48,-4 -54,10 -50,24 C -46,14 -42,6 -36,2 Z M 36,-8 C 48,-4 54,10 50,24 C 46,14 42,6 36,2 Z" fill="{HAIR}"/>'
pla_front = f'''<path d="M -36,-6 C -40,-42 -22,-60 0,-60 C 22,-60 40,-42 36,-6 L 30,-14 L 24,-20 L 14,-16 L 4,-22 L -6,-16 L -16,-22 L -26,-16 L -32,-12 Z" fill="{HAIR}"/>
  <path d="M -28,-40 C -20,-52 -8,-57 2,-57 C -8,-52 -16,-46 -22,-36 Z" fill="{HAIR_HI}"/>
  <circle cx="-36" cy="-8" r="3.4" fill="#e0795f"/><circle cx="36" cy="-8" r="3.4" fill="#e0795f"/>
  <g transform="translate(22,-30) rotate(-14)"><path d="M -4,-9 A 9.5,9.5 0 1 0 7,6 A 7.5,7.5 0 1 1 -4,-9 Z" fill="#f2d36a"/><path d="M -4,-9 A 9.5,9.5 0 0 0 -8,2 A 7.5,7.5 0 0 1 -4,-9 Z" fill="#fff0b8"/><circle cx="6" cy="-6" r="1.3" fill="#fff6d0"/></g></g>'''
pla = head("pla", FACE_KID, SK_PLA, eyes_double("pla", iris="#3e2418", y=3, r=5.2, big=True),
    brow("M -21,-9 C -16,-12 -10,-12 -6,-10.5", "#2e1f1c", 2),
    '<path d="M -5,21.6 Q 0,26.4 5,21.6 Q 0,23.2 -5,21.6 Z" fill="#c4645f"/><path d="M -5,21.6 Q 0,23.2 5,21.6" fill="none" stroke="#9a4a48" stroke-width="1.2" stroke-linecap="round"/>',
    back=pla_back, front=pla_front, kid=True, blush=.6)
mk_back = f'<path d="M -35,-8 C -38,-42 -22,-58 0,-58 C 22,-58 38,-42 35,-8 Z" fill="{HAIR}"/>'
mk_front = f'''<path d="M -35,-6 C -40,-40 -24,-58 0,-58 C 24,-58 40,-40 35,-6 L 31,-12 L 27,-20 L 20,-14 L 14,-22 L 6,-15 L -2,-23 L -10,-15 L -18,-22 L -24,-14 L -30,-18 L -32,-8 Z" fill="{HAIR}"/>
  <path d="M 6,-58 L 10,-66 L 14,-57 Z M -8,-58 L -10,-65 L -2,-58 Z" fill="{HAIR}"/>
  <path d="M -26,-42 C -18,-52 -6,-56 4,-56 C -6,-51 -14,-45 -20,-37 Z" fill="{HAIR_HI}"/>'''
mkid = head("mkid", FACE_KID, SK_KIDM, eyes_double("mkid", iris="#2e1f18", y=3, r=4.8, big=True, two=True),
    brow("M -21,-9 C -16,-10.5 -10,-10.5 -6,-9", "#1e1719", 2.3),
    mouth("M -4.5,23.6 Q 0,25.6 4.5,23.6", "#a8705e", 1.8),
    extra='<rect x="18" y="-26" width="9" height="5" rx="1" fill="#e8d6b8" transform="rotate(20 22 -24)"/>',
    back=mk_back, front=mk_front, kid=True, blush=.4)

kids_svg = f'''
  <g transform="translate(72,118) scale(1.22)">{nightgown(tag="เมฆ", w=44)}
    <path d="M -40,64 L -48,120 L -40,124 L -32,82 Z" fill="#f8f4ec"/><path d="M 40,64 L 48,120 L 40,124 L 32,82 Z" fill="#c9c1b3"/>
    <ellipse cx="-44" cy="126" rx="5" ry="6" fill="#efc6a3"/><ellipse cx="44" cy="126" rx="5" ry="6" fill="#dba680"/>
    {mkid}</g>
  <g transform="translate(196,162) scale(1.0)">{nightgown(col=("#f3e4e0","#fdf3f0","#d8c4bf"), tag="จันทร์", w=44)}
    <path d="M -40,64 L -48,118 L -40,122 L -32,82 Z" fill="#fdf3f0"/><path d="M 40,64 L 48,118 L 40,122 L 32,82 Z" fill="#d8c4bf"/>
    <ellipse cx="-44" cy="124" rx="5" ry="6" fill="#f2cdab"/><ellipse cx="44" cy="124" rx="5" ry="6" fill="#dfaa86"/>
    {pla}</g>
  <g transform="translate(320,138) scale(1.1)">{nightgown(tag="มาเรียม", w=44)}
    <path d="M -40,64 L -48,118 L -40,122 L -32,82 Z" fill="#f8f4ec"/><path d="M 40,64 L 48,118 L 40,122 L 32,82 Z" fill="#c9c1b3"/>
    <ellipse cx="-44" cy="124" rx="5" ry="6" fill="#f6dcc4"/>
    <path d="M 40,118 L 50,112 L 56,120 L 46,128 Z" fill="#e7b7c0"/><circle cx="52" cy="110" r="5" fill="#f1cfd4"/><ellipse cx="44" cy="124" rx="5" ry="6" fill="#e4b89c"/>
    {twinM}</g>
  <g transform="translate(446,138) scale(1.1)">{nightgown(tag="มาร์ธา", w=44)}
    <path d="M -40,64 L -44,104 L -36,108 L -32,82 Z" fill="#f8f4ec"/><path d="M 40,64 L 48,118 L 40,122 L 32,82 Z" fill="#c9c1b3"/>
    <ellipse cx="44" cy="124" rx="5" ry="6" fill="#e4b89c"/>
    <rect x="-46" y="74" width="5" height="24" fill="#f1ebdd"/><path d="M -43.5,66 C -46,70 -46,73 -43.5,75 C -41,73 -41,70 -43.5,66 Z" fill="#fff4dc"/>
    <ellipse cx="-42" cy="104" rx="6" ry="6" fill="#f6dcc4"/>
    {twinA + MARTHA_LID}
    <!-- C -18,-6 -8,-6 -4,-1 L -5,0 C -9,-3.2 -17,-3.2 -21,0.4 Z M 22,-1 C 18,-6 8,-6 4,-1 L 5,0 C 9,-3.2 17,-3.2 21,0.4 Z" fill="#1b1316" transform="translate(0,3.6)"/> -->
  </g>'''

# ---------- page ----------
def card(cid, name, sub, desc, art, chips, vb="-84 -76 168 228"):
    ch = "".join(f'<span><i style="background:{c}"></i>{t}</span>' for c, t in chips)
    return f'''<figure>
  <svg viewBox="{vb}" role="img" aria-label="{name}"><rect x="-110" y="-110" width="220" height="380" fill="#1b1f2b"/>{art}</svg>
  <figcaption><b>{name}</b> <span class="sub">{sub}</span><br>{desc}</figcaption>
  <div class="chips">{ch}</div>
</figure>'''

body = "\n".join(card(*c) for c in cards)
kids = f'''<figure class="wide">
  <svg viewBox="0 0 520 330" role="img" aria-label="เด็กในหอปี 2549"><rect width="520" height="330" fill="#1b1f2b"/>
  <rect y="300" width="520" height="30" fill="#161a24"/>{kids_svg}</svg>
  <figcaption><b>เด็กในหอ ปี 2549</b> <span class="sub">ใช้ในฉากย้อนอดีต · โทนซีดและเกรนหนาตอนอยู่ในฉาก</span><br>
  <b>เมฆตอนเด็ก (11)</b> ผอม ผมสั้นชี้ ๆ ทำหน้าบึ้ง คิ้วขมวด พลาสเตอร์ที่หน้าผาก ·
  <b>จันทร์เจ้า (8)</b> ตัวเล็กสุด ผมแกละสองข้าง ยางรัดผมสีส้ม <b>กิ๊บรูปพระจันทร์สีเหลืองนวล</b> (ของสำคัญที่สุดในเรื่อง) ยิ้มหวาน ชุดนอนสีชมพูอ่อน ·
  <b>มาเรียมตอนเด็ก (9)</b> ผมบ็อบหน้าม้าตรง ตาสองประกาย ยิ้มหวาน กอดตุ๊กตา ถนัดขวา ·
  <b>มาร์ธาตอนเด็ก (9)</b> หน้าเหมือนมาเรียมทุกอย่าง แต่หนังตาบนปิดครึ่งตา ประกายจุดเดียว ปากตรง ไม่ยิ้ม <b>ถือเทียนมือซ้าย</b> ·
  เด็กทุกคนใส่ชุดนอนของหอ มีป้ายชื่อผ้าปักตัวแดงที่อก (ป้ายแบบเดียวกับที่อยู่ในมือป้าแดง)<br>
  <b>ข้อห้ามในฉาก:</b> ห้ามเห็นหน้าแฝดชัดใน EP1 ให้เห็นแค่ด้านหลัง เงา หรือมุมไกล</figcaption>
</figure>'''

html = f'''<title>แม่ชีคนที่สอง ตัวละคร</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: responsive grid of character cards (3 / 2 / 1 columns), one wide card for the children. Single dark look by choice, matching the other character sheets. */
:root {{
  --stage: #0d0f14; --ink: #d4d6e0; --muted: #80849a; --line: #2a2e3a;
  --font: "IBM Plex Sans Thai", "Noto Sans Thai", system-ui, sans-serif;
  color-scheme: dark;
}}
html, body {{ background: var(--stage); color: var(--ink); margin: 0; }}
body {{ font-family: var(--font); padding: 24px max(16px, env(safe-area-inset-right, 0px)) 40px max(16px, env(safe-area-inset-left, 0px)); }}
.wrap {{ max-width: 1100px; margin: 0 auto; display: grid; gap: 18px; }}
h1 {{ font-size: 18px; font-weight: 500; margin: 0; }}
h1 span {{ color: var(--muted); font-weight: 400; margin-left: 8px; font-size: 14px; }}
.grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; }}
@media (max-width: 900px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
@media (max-width: 560px) {{ .grid {{ grid-template-columns: 1fr; }} }}
figure {{ margin: 0; min-width: 0; display: grid; gap: 8px; align-content: start; }}
figure.wide {{ grid-column: 1 / -1; }}
figure svg {{ display: block; width: 100%; height: auto; border-radius: 6px; box-shadow: 0 0 0 1px var(--line); }}
figcaption {{ font-size: 13px; color: var(--muted); line-height: 1.65; }}
figcaption b {{ color: var(--ink); font-weight: 500; }}
.sub {{ font-size: 12px; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 8px 14px; font-size: 12px; color: var(--muted); }}
.chips span {{ display: inline-flex; align-items: center; gap: 6px; }}
.chips i {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; box-shadow: 0 0 0 1px var(--line); }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;700&display=swap">
<div class="wrap">
  <h1>แม่ชีคนที่สอง · ตัวละครชุดใหม่<span>ครึ่งตัว หน้าตรง แสงกลางจากซ้าย · ซิสเตอร์มาเรียม อักเนส และเจมส์ใช้แบบเดิม</span></h1>
  <div class="grid">
{body}
{kids}
  </div>
</div>'''
if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cast_halfbody.html")
    open(out, "w").write(html)
    print("wrote", out)
