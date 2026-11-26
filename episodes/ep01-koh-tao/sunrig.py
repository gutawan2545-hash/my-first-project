"""Sun (EP.01) as reusable parts: head variants + body with swappable arms/outfit.
Shapes come from characters/sun_gen.py (James's head, slim face, no glasses, Sun's outfit)."""
import os, re, runpy

HERE = os.path.dirname(os.path.abspath(__file__))
SG = runpy.run_path(os.path.join(HERE, '..', '..', 'characters', 'sun_gen.py'))
JDEFS = SG['JDEFS']
SK, SKS, SKD, SKH = SG['SK'], SG['SKS'], SG['SKD'], SG['SKH']

CLIPS = JDEFS[:JDEFS.index('<g id="shead">')]
HEAD = JDEFS[JDEFS.index('<g id="shead">'):].rstrip()
assert HEAD.endswith('</g>')

BL = '<path d="M -22,-12.5 L -7,-12 L -7,-9.2 L -21,-9.4 Z" fill="#17151d"/>'
BR = '<path d="M 22,-14.6 C 17,-16 11,-14.6 7,-12.6 L 7,-9.8 C 11,-11.6 17,-12.6 21,-11.4 Z" fill="#17151d"/>'
MO = ('<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/>'
      '<path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>')
for x in (BL, BR, MO):
    assert x in HEAD, x[:40]

BR_FLAT = '<path d="M 22,-12.5 L 7,-12 L 7,-9.2 L 21,-9.4 Z" fill="#17151d"/>'
BL_WORRY = '<path d="M -22,-9.6 L -7,-13.6 L -7,-10.8 L -21,-6.8 Z" fill="#17151d"/>'
BR_WORRY = '<path d="M 22,-9.6 L 7,-13.6 L 7,-10.8 L 21,-6.8 Z" fill="#17151d"/>'
BL_LOW = '<path d="M -22,-10.6 L -7,-9.4 L -7,-6.6 L -21,-7.6 Z" fill="#17151d"/>'
BR_LOW = '<path d="M 22,-10.6 L 7,-9.4 L 7,-6.6 L 21,-7.6 Z" fill="#17151d"/>'

M_FLAT = '<path d="M -6,23.8 L 6,23.8" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/>'
M_DOWN = '<path d="M -6,24.8 Q 0,23 6,24.8" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/>'
M_OPEN = ('<ellipse cx="0" cy="25" rx="5" ry="4.4" fill="#6a2f2c"/>'
          '<path d="M -3,27.8 Q 0,29.2 3,27.8" stroke="#d98a80" stroke-width="1.6" fill="none"/>')
M_TALK = '<path d="M -5.5,22.8 Q 0,22.2 5.5,22.8 Q 4,27.2 0,27.4 Q -4,27.2 -5.5,22.8 Z" fill="#7a3a36"/>'
M_GRIN = ('<path d="M -7,22 Q 0,24 7.5,21 Q 5,27.6 0,27.8 Q -5,27.4 -7,22 Z" fill="#7a3a36"/>'
          '<path d="M -5.4,22.6 Q 0,24 6,22 L 5.4,23.6 Q 0,25.2 -5,24 Z" fill="#fbf6f0"/>')


def lids(y):
    return (f'<g clip-path="url(#eyeL)"><rect x="-23" y="-9" width="20" height="{y + 9:.1f}" fill="#efc7b0"/></g>'
            f'<g clip-path="url(#eyeR)"><rect x="3" y="-9" width="20" height="{y + 9:.1f}" fill="#e6bba5"/></g>'
            f'<path d="M -22,{y + .6:.1f} C -16,{y - .8:.1f} -10,{y - .8:.1f} -4.5,{y + .8:.1f}" stroke="#17151d" stroke-width="1.9" fill="none" stroke-linecap="round"/>'
            f'<path d="M 22,{y + .6:.1f} C 16,{y - .8:.1f} 10,{y - .8:.1f} 4.5,{y + .8:.1f}" stroke="#17151d" stroke-width="1.9" fill="none" stroke-linecap="round"/>')


SWEAT = ('<path d="M 31,-26 C 34.5,-19 35.5,-15 32,-13 C 28.5,-15 28.5,-19 31,-26 Z" fill="#d6ecff" opacity=".95"/>'
         '<path d="M -33,-14 C -30.5,-9 -30,-6 -32.5,-4.6 C -35,-6 -35,-9 -33,-14 Z" fill="#d6ecff" opacity=".85"/>')
SHADES = ('<g><path d="M -24,-8 L -3,-8 L -3.6,-0.5 C -4,4 -8,5.5 -13,5.5 C -19,5.5 -23.6,3 -24,-1 Z" fill="#141218"/>'
          '<path d="M 24,-8 L 3,-8 L 3.6,-0.5 C 4,4 8,5.5 13,5.5 C 19,5.5 23.6,3 24,-1 Z" fill="#141218"/>'
          '<path d="M -3,-6.4 Q 0,-8.4 3,-6.4" fill="none" stroke="#141218" stroke-width="2"/>'
          '<path d="M -24,-7 L -32,-5.4 M 24,-7 L 32,-5.4" stroke="#141218" stroke-width="2"/>'
          '<path d="M -20,-6.4 L -14.5,-6.4 L -21,1 Z" fill="#6c7896" opacity=".6"/>'
          '<path d="M 7,-6.4 L 10.5,-6.4 L 5,0 Z" fill="#6c7896" opacity=".4"/></g>')
MASK = ('<g><path d="M -36,-30 C -30,-36 30,-36 36,-30" stroke="#22303f" stroke-width="3.4" fill="none"/>'
        '<rect x="-23" y="-44" width="46" height="17" rx="7" fill="#22303f"/>'
        '<rect x="-19.5" y="-41.6" width="39" height="12" rx="5" fill="#9ad7e3" opacity=".9"/>'
        '<path d="M -16,-40 L -9,-40 L -15,-31 Z" fill="#fff" opacity=".55"/></g>')
WIND = ('<path d="M 18,-52 C 32,-58 46,-58 58,-54 C 46,-50 34,-46 26,-40 Z" fill="#16151c"/>'
        '<path d="M 26,-34 C 40,-38 54,-36 64,-30 C 50,-28 40,-26 32,-20 Z" fill="#16151c"/>'
        '<path d="M 6,-62 C 22,-72 38,-74 50,-70 C 36,-66 24,-60 16,-54 Z" fill="#16151c"/>'
        '<path d="M 10,-60 C 22,-66 32,-68 42,-67 C 30,-63 22,-60 16,-56 Z" fill="#3b3a52"/>')


def variant(vid, brows=None, mouth=None, extra='', lid=None):
    g = HEAD.replace('id="shead"', f'id="{vid}"', 1)
    if brows:
        g = g.replace(BL, brows[0]).replace(BR, brows[1])
    if mouth is not None:
        g = g.replace(MO, mouth)
    add = (lids(lid) if lid is not None else '') + extra
    if add:
        g = g[:-len('</g>')] + add + '</g>'
    return g


HEADS = {
    'smirk': 'shead',
    'dead': 'sh_dead', 'talk': 'sh_talk', 'pant': 'sh_pant', 'annoy': 'sh_annoy',
    'shades': 'sh_shades', 'wind': 'sh_wind', 'mask': 'sh_mask', 'grin': 'sh_grin', 'smirktalk': 'sh_smtalk',
}
HEAD_DEFS = CLIPS + HEAD + ''.join([
    variant('sh_dead', (BL, BR_FLAT), M_FLAT, lid=-3.6),
    variant('sh_talk', None, M_TALK),
    variant('sh_smtalk', None, M_TALK),
    variant('sh_pant', (BL_WORRY, BR_WORRY), M_OPEN, SWEAT, lid=-3.0),
    variant('sh_annoy', (BL_LOW, BR_LOW), M_DOWN, lid=-2.6),
    variant('sh_shades', None, MO, SHADES),
    variant('sh_wind', None, M_FLAT, f'<g transform="rotate(9 0 -2)">{SHADES}</g>' + WIND),
    variant('sh_mask', None, M_GRIN, MASK),
    variant('sh_grin', None, M_GRIN, lid=-4.0),
])

# ---------------------------------------------------------------- body parts
BODY = SG['BODY']
PARTS = {}
for chunk in re.split(r'(?=<!--)', BODY):
    m = re.match(r'<!--\s*(.*?)\s*-->', chunk.strip())
    if not m:
        continue
    k = m.group(1)
    key = ('trousers' if 'trousers' in k else 'ankles' if 'ankles' in k else 'shoes' if 'sneakers' in k
           else 'larm' if 'left forearm' in k else 'tee' if 'tee under' in k else 'shirt' if 'overshirt' in k
           else 'collar' if 'collar' in k else 'pocket' if 'pocket with' in k else 'tote' if 'tote' in k
           else 'rarm' if 'right forearm' in k else 'camera' if 'camera' in k else k)
    PARTS[key] = chunk

NECK_AFTER = ('<path d="M -9.5,56 L 9.5,56 L 9.5,58 L -9.5,58 Z" fill="#f2eee6"/>'
              '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'
              '<path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/>')
STRAP = '<path d="M -9,58 L -11,66 M 9,58 L 9.6,66" stroke="#2a2024" stroke-width="1.8"/>'

HAND = lambda x, y, c=SK: f'<ellipse cx="{x}" cy="{y}" rx="7" ry="9" fill="{c}"/>'
ARMS = {
    'L_hang': PARTS['larm'],
    'R_hang': (f'<path d="M 63,136 L 47,142 L 45,230 L 58,232 Z" fill="{SKS}"/>'
               f'<path d="M 63,136 L 58,138 L 54,232 L 58,232 Z" fill="{SKD}"/>'
               f'<path d="M 58,230 L 45,229 C 43,244 45,258 51,260 C 57,260 60,246 58,230 Z" fill="{SKS}"/>'),
    'R_pocket': PARTS['rarm'],
    'L_point': (f'<path d="M -64,128 L -50,142 L -112,118 L -118,104 Z" fill="{SK}"/>'
                f'<path d="M -64,128 L -60,132 L -116,108 L -118,104 Z" fill="{SKH}"/>'
                f'<ellipse cx="-122" cy="108" rx="9" ry="7" fill="{SK}"/>'
                f'<path d="M -126,102 L -146,94 L -147,99 L -127,107 Z" fill="{SK}"/>'),
    'R_point': (f'<path d="M 64,128 L 50,142 L 112,118 L 118,104 Z" fill="{SKS}"/>'
                f'<ellipse cx="122" cy="108" rx="9" ry="7" fill="{SKS}"/>'
                f'<path d="M 126,102 L 146,94 L 147,99 L 127,107 Z" fill="{SKS}"/>'),
    'R_pointup': (f'<path d="M 62,132 L 48,142 L 92,58 L 104,64 Z" fill="{SKS}"/>'
                  f'<ellipse cx="99" cy="56" rx="8" ry="9" fill="{SKS}"/>'
                  f'<path d="M 96,50 L 104,26 L 109,28 L 102,52 Z" fill="{SKS}"/>'),
    'table': (f'<path d="M -63,136 L -47,142 L -18,222 L -34,230 Z" fill="{SK}"/>'
              f'<path d="M 63,136 L 47,142 L 18,222 L 34,230 Z" fill="{SKS}"/>'
              + HAND(-26, 228) + HAND(26, 228, SKS)),
}
# arms drawn after the head (hand at the ear / face)
FRONT = {
    'L_phone': (f'<path d="M -64,134 L -48,142 L -30,18 L -44,12 Z" fill="{SK}"/>'
                f'<path d="M -64,134 L -60,136 L -42,14 L -44,12 Z" fill="{SKH}"/>'
                '<rect x="-46" y="-14" width="11" height="26" rx="3" fill="#15151c" transform="rotate(-12 -40 0)"/>'
                + HAND(-38, 10)),
    'R_coffee': (f'<path d="M 63,136 L 47,142 L 30,120 L 42,108 Z" fill="{SKS}"/>'
                 '<path d="M 22,92 L 44,92 L 41,120 L 25,120 Z" fill="#f4efe6"/><rect x="21" y="88" width="24" height="5" rx="2" fill="#4a3a34"/>'
                 '<path d="M 24,102 L 42,102 L 41.4,110 L 24.6,110 Z" fill="#b98c6a"/>' + HAND(34, 116, SKS)),
}


def body(head='smirk', L='L_hang', R='R_pocket', tote=True, camera=True, pocket_shades=True, outfit='std',
         legs=True, front=''):
    p = PARTS
    out = ''
    if legs:
        if outfit == 'wetsuit':
            out += ('<path d="M -44,226 L 44,226 L 46,300 L 40,456 L 8,456 L 3,298 L -3,298 L -8,456 L -40,456 L -46,300 Z" fill="#1f2b46"/>'
                    '<path d="M -44,226 L -30,226 L -32,300 L -30,456 L -40,456 L -46,300 Z" fill="#2c3b5e"/>'
                    '<path d="M -40,300 L -36,456 M 38,300 L 36,456" stroke="#2fb3b8" stroke-width="3"/>'
                    f'<path d="M -40,454 L -10,454 L -8,470 L -44,470 Z" fill="{SK}"/><path d="M 40,454 L 10,454 L 8,470 L 44,470 Z" fill="{SKS}"/>'
                    '<path d="M -48,468 L -6,468 L -2,490 L -54,490 Z" fill="#2fb3b8"/><path d="M 48,468 L 6,468 L 2,490 L 54,490 Z" fill="#228f94"/>')
        else:
            out += p['trousers'] + p['ankles'] + p['shoes']
    if outfit == 'wetsuit':
        out += ARMS[L].replace(SK, '#1f2b46').replace(SKH, '#2c3b5e') if L == 'L_hang' else ARMS[L]
        out += ('<path d="M -12,50 C -30,52 -44,56 -52,64 L -64,140 L -46,146 L -46,238 L 46,238 L 46,146 L 64,140 L 52,64 C 44,56 30,52 12,50 Z" fill="#1f2b46"/>'
                '<path d="M -52,64 C -46,58 -36,54 -28,52 C -34,90 -34,150 -32,238 L -46,238 L -46,146 L -64,140 Z" fill="#2c3b5e"/>'
                '<path d="M 28,52 C 40,55 48,59 52,64 L 64,140 L 46,146 L 46,238 L 32,238 C 34,160 34,100 28,52 Z" fill="#162036"/>'
                '<path d="M -50,72 L -40,180 M 50,72 L 40,180" stroke="#2fb3b8" stroke-width="3.2"/>'
                '<path d="M -1,52 L 1,52 L 1,150 L -1,150 Z" fill="#0f1626"/>')
        out += ARMS[R] if R != 'R_pocket' else ARMS['R_hang']
    else:
        out += ARMS[L] + p['tee'] + p['shirt'] + p['collar']
        out += p['pocket'] if pocket_shades else re.sub(r'<path d="M 19,92.*?$', '', p['pocket'], flags=re.S)
        if tote:
            out += p['tote']
        out += ARMS[R]
        if camera:
            out += p['camera']
    out += f'<use href="#{HEADS[head]}"/>'
    if outfit != 'wetsuit':
        out += NECK_AFTER + (STRAP if camera else '')
    out += ''.join(FRONT[f] for f in front.split() if f)
    return out


# ---------------------------------------------------------------- tourist (back view: no new face drawn)
TOURIST = ('<g>'
           '<path d="M -40,226 L 40,226 L 44,300 L 8,300 L 3,282 L -3,282 L -8,300 L -44,300 Z" fill="#b9a688"/>'
           '<path d="M -40,226 L -26,226 L -30,300 L -44,300 Z" fill="#cbb999"/>'
           '<path d="M -38,300 L -12,300 L -14,452 L -34,452 Z M 38,300 L 12,300 L 14,452 L 34,452 Z" fill="#f0c4a8"/>'
           '<path d="M 38,300 L 26,300 L 28,452 L 34,452 Z" fill="#dba68a"/>'
           '<path d="M -40,450 L -10,450 L -8,470 L -44,470 Z M 40,450 L 10,450 L 8,470 L 44,470 Z" fill="#5a6f8c"/>'
           '<path d="M -56,108 L -44,112 L -42,230 L -54,232 Z" fill="#f0c4a8"/><path d="M 56,108 L 44,112 L 42,230 L 54,232 Z" fill="#dba68a"/>'
           '<path d="M -44,56 C -30,50 30,50 44,56 L 46,116 L 42,228 L -42,228 L -46,116 Z" fill="#e0786a"/>'
           '<path d="M -44,56 C -36,52 -28,51 -22,51 C -28,90 -30,160 -28,228 L -42,228 L -46,116 Z" fill="#ec9183"/>'
           '<path d="M 24,52 C 34,53 40,54 44,56 L 46,116 L 42,228 L 28,228 C 30,160 30,100 24,52 Z" fill="#c4614f"/>'
           '<rect x="-30" y="70" width="60" height="96" rx="14" fill="#2c3a5a"/><rect x="-30" y="70" width="18" height="96" rx="9" fill="#3a4b70"/>'
           '<path d="M -24,74 L -30,56 M 24,74 L 30,56" stroke="#1f2a44" stroke-width="5"/>'
           '<rect x="-9" y="20" width="18" height="34" fill="#f0c4a8"/><rect x="2" y="20" width="7" height="34" fill="#dba68a"/>'
           '<path d="M -31,-10 C -32,-44 32,-44 31,-10 C 31,10 22,26 0,28 C -22,26 -31,10 -31,-10 Z" fill="#cdb48e"/>'
           '<path d="M -31,-10 C -32,-40 -10,-46 -2,-44 C -18,-36 -24,-20 -22,6 C -28,0 -31,-4 -31,-10 Z" fill="#dcc6a2"/>'
           '<path d="M 14,-40 C 26,-34 32,-22 31,-10 C 31,6 24,22 12,27 C 20,12 22,-14 14,-40 Z" fill="#b39a74"/>'
           '<circle cx="2" cy="-46" r="13" fill="#cdb48e"/><circle cx="-2" cy="-50" r="6" fill="#dcc6a2"/>'
           '<path d="M -26,-30 C -16,-36 16,-36 26,-30" stroke="#e0786a" stroke-width="3" fill="none"/>'
           '</g>')
