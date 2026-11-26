"""EP.01 cast sheet: Sun (islander look), the auntie, the rental agent, the dive-instructor neighbour, the gecko.
Faces are built from James's / Tawan's approved heads (characters/james.html, tawan.html): same face,
eye, brow and mouth construction, new hair, recoloured skin, small age/personality marks.
Run: python3 islanders_gen.py -> islanders.html"""
import os, re, runpy

H = os.path.dirname(os.path.abspath(__file__))
J = open(os.path.join(H, 'james.html')).read()
T = open(os.path.join(H, 'tawan.html')).read()
SG = runpy.run_path(os.path.join(H, 'sun_gen.py'))


def grp(src, gid):
    a = src.index(f'<g id="{gid}">')
    b = src.index('\n  </g>', a)
    return src[a + len(f'<g id="{gid}">'):b]


def cut(s, start, end=None):
    a = s.index(start)
    b = s.index(end, a) if end else len(s)
    return s[:a] + s[b:]


# ---------------------------------------------------------------- face kits (no hair)
JK = grp(J, 'jhead')
JK = cut(JK, '<!-- hair: short, chunky spikes -->', '<!-- headphones -->')
JK = cut(JK, '<!-- headphones -->')
JK = cut(JK, '<!-- glasses: round, thin silver wire -->', '<!-- faint blush')
JK = JK.replace('url(#face)', 'url(#jface)').replace('url(#eyeL)', 'url(#jeyeL)').replace('url(#eyeR)', 'url(#jeyeR)')
TK = grp(T, 'thead')
TK = cut(TK, '<!-- crown:')
TK = TK.replace('url(#face)', 'url(#tface)').replace('url(#eyeL)', 'url(#teyeL)').replace('url(#eyeR)', 'url(#teyeR)')

CLIPS = ('<clipPath id="jface"><path d="M -32,-14 C -32,-46 32,-46 32,-14 L 31,6 C 29,22 13,37 0,40 C -13,37 -29,22 -31,6 Z"/></clipPath>'
         '<clipPath id="jeyeL"><path d="M -21,-3 C -17,-6.5 -9,-6.5 -5,-1.5 C -9,0.8 -17,0.8 -21,-3 Z"/></clipPath>'
         '<clipPath id="jeyeR"><path d="M 21,-3 C 17,-6.5 9,-6.5 5,-1.5 C 9,0.8 17,0.8 21,-3 Z"/></clipPath>'
         '<clipPath id="tface"><path d="M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,36 0,39 C -13,36 -28,22 -30,6 Z"/></clipPath>'
         '<clipPath id="teyeL"><path d="M -21,-1 C -18,-7.5 -8,-7.5 -5,-1 C -8,3 -18,3 -21,-1 Z"/></clipPath>'
         '<clipPath id="teyeR"><path d="M 21,-1 C 18,-7.5 8,-7.5 5,-1 C 8,3 18,3 21,-1 Z"/></clipPath>')

J_SKIN = ['#fbe7d8', '#efc7b0', '#d29d86', '#f4d4c0', '#ddb19c', '#fff5ee', '#e6b29c', '#dcae99']
T_SKIN = ['#f8d2ab', '#e8b08a', '#c98462', '#f0c49e', '#fff0dc', '#dc9c76', '#efbf98', '#d39a78', '#d29a78']


def recolor(kit, old, new):
    for o, n in zip(old, new):
        kit = kit.replace(f'"{o}"', f'"{n}"')
    return kit


# skin sets: skin, shade, deep, temple/neck, neck-shade, highlight, nose, lid-line
TAN = ['#e9b993', '#d29e78', '#b4805e', '#dfac85', '#c4906c', '#f5d2b2', '#c8906c', '#c08a6a']
SUNBURNT = ['#f8d8c6', '#ebbca6', '#d09a84', '#f2ccb8', '#dcab96', '#fff0e8', '#e2a690', '#d8a894']
AUNT = ['#e4ae86', '#cc9670', '#ab7652', '#dba37c', '#bd8a66', '#d39a74', '#f2cba8', '#bf8462', '#b9805e']   # Tawan order

# ---------------------------------------------------------------- heads
SMILE_T = '<path d="M -6.5,22 Q 0,25.6 6.5,21.6" fill="none" stroke="#a24a46" stroke-width="2" stroke-linecap="round"/>'
LIP_T = '<path d="M -3.5,25.4 Q 0,27.4 3.5,25.2" fill="none" stroke="#e79a8a" stroke-width="1.6" stroke-linecap="round"/>'
GRIN = ('<path d="M -8,20.6 Q 0,23 8,20.6 Q 6,28.6 0,29 Q -6,28.6 -8,20.6 Z" fill="#7a3a36"/>'
        '<path d="M -6.6,21.4 Q 0,23.4 6.6,21.4 L 6,23.2 Q 0,25.2 -6,23.2 Z" fill="#fbf6f0"/>')

aunt_kit = recolor(TK, T_SKIN, AUNT).replace(SMILE_T, GRIN).replace(LIP_T, '')
aunt_kit = re.sub(r'<path d="M -17,-5.8 L -19,-9.2.*?/>', '', aunt_kit)          # fewer lash flicks: older, no makeup
aunt_kit = re.sub(r'<path d="M 17,-5.8 L 19,-9.2.*?/>', '', aunt_kit)
AUNT_HEAD = ('<g id="h_aunt">'
             '<path d="M -40,6 C -50,-10 -48,-40 -34,-54 C -20,-68 20,-68 34,-54 C 48,-40 50,-10 40,6 C 36,-6 30,-12 24,-14 L -24,-14 C -30,-12 -36,-6 -40,6 Z" fill="#2a2228"/>'
             + aunt_kit +
             # smile lines + crow's feet, kept soft
             '<path d="M -12,15 C -14,19 -13,23 -10,26 M 12,15 C 14,19 13,23 10,26" fill="none" stroke="#b07a58" stroke-width="1.2" stroke-linecap="round"/>'
             '<path d="M -24,-4 l -4,-2 M -24,-1 l -4,1 M 24,-4 l 4,-2 M 24,-1 l 4,1" stroke="#b07a58" stroke-width="1" stroke-linecap="round"/>'
             # short permed curls, dark with grey strands
             + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>' for x, y, r, c in (
                 (-30, -30, 12, '#2a2228'), (-20, -44, 13, '#2a2228'), (-4, -50, 13, '#2a2228'), (12, -48, 13, '#2a2228'), (26, -38, 12, '#2a2228'),
                 (33, -22, 10, '#2a2228'), (-34, -16, 9, '#2a2228'), (-12, -36, 11, '#2a2228'), (6, -36, 11, '#2a2228'), (20, -28, 9, '#2a2228'),
                 (-24, -24, 8, '#2a2228')))
             + '<path d="M -26,-46 q 6,-6 12,-2 M -6,-56 q 6,-5 12,-1 M 14,-50 q 6,-4 10,2 M -36,-28 q 2,-7 8,-9" stroke="#8a8590" stroke-width="1.8" fill="none" stroke-linecap="round" opacity=".8"/>'
             + '<path d="M -26,-26 C -14,-32 14,-32 26,-24 C 14,-26 -14,-26 -26,-20 Z" fill="#2a2228"/>'
             '<circle cx="-31" cy="10" r="2.6" fill="#d9b25e"/><circle cx="31" cy="10" r="2.6" fill="#c49c4c"/>'
             '</g>')

nb_kit = recolor(JK, J_SKIN, SUNBURNT)
nb_kit = nb_kit.replace('fill="#17151d"', 'fill="#8a6440"')                       # light-brown brows
nb_kit = nb_kit.replace('<ellipse cx="-18" cy="12" rx="6" ry="3.2" fill="#e99a86" opacity=".35"/>', '<ellipse cx="-17" cy="10" rx="8" ry="4" fill="#ec8f7c" opacity=".55"/>')
nb_kit = nb_kit.replace('<ellipse cx="18" cy="12" rx="6" ry="3.2" fill="#d98a78" opacity=".35"/>', '<ellipse cx="17" cy="10" rx="8" ry="4" fill="#dc806e" opacity=".55"/>')
NB_HEAD = ('<g id="h_nb">'
           '<path d="M -38,10 C -46,-26 -38,-58 -12,-66 C 10,-72 36,-62 42,-36 C 46,-16 42,0 38,10 L 32,-6 L -32,-6 Z" fill="#a87c50"/>'
           + nb_kit +
           ''.join(f'<circle cx="{x}" cy="{y}" r=".9" fill="#c98466"/>' for x, y in ((-20, 6), (-16, 9), (-12, 6), (-18, 12), (14, 7), (18, 10), (12, 11), (2, 8), (-2, 10)))
           + '<path d="M -26,14 C -24,30 -12,38 0,40 C 12,38 24,30 26,14 C 22,26 12,33 0,34 C -12,33 -22,26 -26,14 Z" fill="#a07850" opacity=".35"/>'
           '<path d="M -8,19 C -4,18 4,18 8,19" stroke="#a07850" stroke-width="2.4" opacity=".4" fill="none"/>'
           # wavy sun-bleached hair: lit chunks on the left
           '<path d="M -38,-6 C -44,-34 -30,-62 -4,-66 C 20,-70 40,-56 42,-30 C 43,-18 40,-8 38,0 L 33,-14 L 28,-6 L 26,-22 L 18,-12 L 16,-28 L 8,-16 L 4,-30 L -4,-18 L -8,-32 L -16,-20 L -20,-32 L -26,-18 L -30,-26 L -34,-10 Z" fill="#a87c50"/>'
           '<path d="M -30,-46 C -20,-60 -4,-64 10,-62 C -4,-56 -16,-48 -24,-36 Z" fill="#d6ab78"/>'
           '<path d="M -36,-24 C -34,-36 -28,-44 -20,-48 C -26,-40 -30,-30 -30,-20 Z" fill="#c69a68"/>'
           '<path d="M 26,-22 L 32,-40 L 33,-14 Z M 16,-28 L 22,-44 L 18,-12 Z" fill="#7d5a38"/>'
           '<path d="M -40,-12 C -48,-8 -50,0 -48,8 C -44,0 -40,-4 -36,-6 Z M 40,-10 C 48,-4 48,4 46,10 C 44,2 40,-2 37,-4 Z" fill="#a87c50"/>'
           '</g>')

ag_kit = recolor(JK, J_SKIN, TAN)
ag_kit = ag_kit.replace('<path d="M 22,-14.6 C 17,-16 11,-14.6 7,-12.6 L 7,-9.8 C 11,-11.6 17,-12.6 21,-11.4 Z" fill="#17151d"/>',
                        '<path d="M 22,-12.5 L 7,-12 L 7,-9.2 L 21,-9.4 Z" fill="#17151d"/>')   # both brows level: salesman calm
ag_kit = ag_kit.replace('<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>',
                        '<path d="M -7.5,22 Q 0,26.6 7.5,22" fill="none" stroke="#8c4a42" stroke-width="1.9" stroke-linecap="round"/>')
AGENT_HEAD = ('<g id="h_agent">'
              '<path d="M -36,-4 C -40,-40 -24,-58 0,-60 C 24,-58 40,-40 36,-4 L 30,-12 L -30,-12 Z" fill="#1a171d"/>'
              + ag_kit.replace('fill="#b4805e"/>', 'fill="#b4805e"/>', 1) +
              '<path d="M -1,18.6 C -5,17.8 -9,18.6 -11,21 C -7,20.4 -4,20.2 -1,20.6 Z M 1,18.6 C 5,17.8 9,18.6 11,21 C 7,20.4 4,20.2 1,20.6 Z" fill="#1a171d"/>'
              # slick side part with a comb shine
              '<path d="M -36,-10 C -40,-40 -22,-58 2,-58 C 26,-58 40,-42 36,-10 L 32,-22 C 26,-36 10,-42 -10,-40 L -12,-34 C -20,-32 -28,-24 -32,-14 Z" fill="#1a171d"/>'
              '<path d="M -12,-40 C 2,-48 20,-46 30,-34 C 18,-40 6,-42 -10,-38 Z" fill="#4a4652"/>'
              '<path d="M -10,-46 L -14,-38" stroke="#4a4652" stroke-width="1.4"/>'
              # sunglasses pushed up on the head
              '<g transform="translate(0,-46)"><path d="M -24,-4 L -4,-4 L -5,3 C -6,7 -10,8 -14,8 C -20,8 -23,6 -24,2 Z M 24,-4 L 4,-4 L 5,3 C 6,7 10,8 14,8 C 20,8 23,6 24,2 Z" fill="#141218"/>'
              '<path d="M -4,-2 Q 0,-4 4,-2" stroke="#141218" stroke-width="2" fill="none"/><path d="M -19,-3 L -14,-3 L -20,3 Z" fill="#6c7896" opacity=".6"/></g>'
              '</g>')

SUN_HEAD = SG['JDEFS'][SG['JDEFS'].index('<g id="shead">'):].rstrip().replace('id="shead"', 'id="h_sun"', 1)
SUN_TAN = SUN_HEAD.replace('id="h_sun"', 'id="h_suntan"', 1)
for o, n in zip(J_SKIN, TAN):
    SUN_TAN = SUN_TAN.replace(f'"{o}"', f'"{n}"')
SUN_HEADDEFS = SG['JDEFS'][:SG['JDEFS'].index('<g id="shead">')]

# ---------------------------------------------------------------- bodies (James proportions, head at 0,0, light from the left)
def arms(sk, sks, skh, tank=False, sleeve=None):
    top = 'M -40,58 C -50,62 -57,80 -57,104' if tank else 'M -55,114'
    topR = 'M 40,58 C 50,62 57,80 57,104' if tank else 'M 55,114'
    out = (f'<path d="{top} L -57,170 L -54,236 L -42,236 L -40,170 L -40,{60 if tank else 118} Z" fill="{sk}"/>'
           f'<path d="{top} L -57,170 L -54,236 L -51,236 L -52,120 Z" fill="{skh}"/>'
           f'<path d="{topR} L 57,170 L 54,236 L 42,236 L 40,170 L 40,{60 if tank else 118} Z" fill="{sks}"/>'
           f'<path d="M -55,234 L -41,234 C -40,248 -42,262 -48,264 C -54,264 -57,250 -55,234 Z" fill="{sk}"/>'
           f'<path d="M 55,234 L 41,234 C 40,248 42,262 48,264 C 54,264 57,250 55,234 Z" fill="{sks}"/>')
    return out


def tee(c, cl, cd, hem=234, sleeve_len=116):
    return (f'<path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L 57,{sleeve_len} L 40,{sleeve_len + 6} L 42,{hem} L -42,{hem} L -40,{sleeve_len + 6} L -57,{sleeve_len} L -47,66 C -42,56 -28,51 -12,49 Z" fill="{c}"/>'
            f'<path d="M -47,66 C -42,56 -28,51 -18,50 C -26,72 -30,110 -28,{hem} L -42,{hem} L -40,{sleeve_len + 6} L -57,{sleeve_len} Z" fill="{cl}"/>'
            f'<path d="M 20,50 C 32,53 43,58 47,66 L 57,{sleeve_len} L 40,{sleeve_len + 6} L 42,{hem} L 26,{hem} C 28,180 28,100 20,50 Z" fill="{cd}"/>'
            f'<path d="M -12,49 C -8,61 8,61 12,49" fill="none" stroke="{cd}" stroke-width="4"/>')


def tank(c, cl, cd):
    return (f'<path d="M -14,50 C -10,66 10,66 14,50 L 27,52 C 30,72 37,86 41,98 L 42,234 L -42,234 L -41,98 C -37,86 -30,72 -27,52 Z" fill="{c}"/>'
            f'<path d="M -27,52 C -30,72 -37,86 -41,98 L -42,234 L -28,234 C -30,160 -28,90 -20,52 Z" fill="{cl}"/>'
            f'<path d="M 20,52 L 27,52 C 30,72 37,86 41,98 L 42,234 L 28,234 C 30,160 28,90 20,52 Z" fill="{cd}"/>'
            f'<path d="M -14,50 C -10,66 10,66 14,50" fill="none" stroke="{cd}" stroke-width="3"/>')


def shorts(c, cl, cd, sk, sks, print_=None):
    out = (f'<path d="M -44,226 L 44,226 L 49,336 L 6,340 L 2,292 L -2,292 L -6,340 L -49,336 Z" fill="{c}"/>'
           f'<path d="M -44,226 L -28,226 L -32,336 L -49,336 Z" fill="{cl}"/>'
           f'<path d="M 26,230 L 44,226 L 49,336 L 34,338 C 34,300 30,260 26,230 Z" fill="{cd}"/>'
           f'<rect x="-44" y="226" width="88" height="9" fill="{cd}"/><path d="M -4,235 l -6,16 M 4,235 l 6,16" stroke="#f2eee6" stroke-width="1.6"/>')
    if print_:
        out += print_
    out += (f'<path d="M -40,338 L -12,338 L -13,462 L -33,462 Z" fill="{sk}"/><path d="M -40,338 L -34,338 L -33,462 L -36,462 Z" fill="#fff5ee" opacity=".5"/>'
            f'<path d="M 40,338 L 12,338 L 13,462 L 33,462 Z" fill="{sks}"/>'
            f'<path d="M -34,390 C -30,394 -18,394 -14,390" stroke="{sks}" stroke-width="1.2" fill="none"/>')
    return out


def flipflops(strap='#2c3a54', sole='#e9e4dc', sk='#fbe7d8', sks='#efc7b0'):
    return (f'<path d="M -36,460 L -10,460 C -6,468 -8,478 -12,480 L -40,480 C -44,476 -42,466 -36,460 Z" fill="{sk}"/>'
            f'<path d="M 36,460 L 10,460 C 6,468 8,478 12,480 L 40,480 C 44,476 42,466 36,460 Z" fill="{sks}"/>'
            f'<rect x="-46" y="480" width="40" height="7" rx="3" fill="{sole}"/><rect x="6" y="480" width="40" height="7" rx="3" fill="#cfc9be"/>'
            f'<path d="M -38,472 L -24,464 L -10,472 M 38,472 L 24,464 L 10,472" stroke="{strap}" stroke-width="4" fill="none" stroke-linecap="round"/>')


def neck_after(c='#f2eee6'):
    return '<path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>'


SK, SKS, SKH = '#fbe7d8', '#efc7b0', '#fff5ee'
LEAF = ''.join(f'<path d="M {x},{y} q 8,-10 16,0 q -8,6 -16,0 Z" fill="#3f8a8e" transform="rotate({r} {x} {y})"/>'
               for x, y, r in ((-38, 250, -20), (-20, 290, 30), (-36, 314, 10), (14, 254, -30), (28, 296, 20), (10, 318, -10), (-6, 262, 40)))

SUN_ISLAND = (shorts('#24405a', '#2f5272', '#1a2f44', SK, SKS, LEAF) + flipflops('#2fb3b8')
              + arms(SK, SKS, SKH, tank=True)
              + tank('#86b9c8', '#a3cfda', '#6a9fae')
              + '<g transform="translate(-14,120)"><circle r="13" fill="none" stroke="#f2eee6" stroke-width="2.4"/><path d="M -10,3 q 5,-6 10,0 q 5,6 10,0" stroke="#f2eee6" stroke-width="2.2" fill="none"/></g>'
              + '<path d="M -55,226 L -41,226 L -41,231 L -55,231 Z" fill="#8a6a50"/><circle cx="-48" cy="228.5" r="1.6" fill="#f2eee6"/>'
              # half helmet in the right hand
              + '<g transform="translate(62,268)"><path d="M -24,0 C -24,-26 24,-26 24,0 Z" fill="#f2eee6"/><path d="M -24,0 C -24,-26 0,-26 6,-25 C -8,-20 -14,-10 -16,0 Z" fill="#ffffff"/>'
              '<path d="M 8,-24 C 18,-18 24,-10 24,0 L 14,0 C 14,-10 12,-18 8,-24 Z" fill="#d6d1c6"/><rect x="-26" y="-2" width="52" height="5" rx="2" fill="#2fb3b8"/>'
              '<path d="M -14,3 C -10,14 10,14 14,3" stroke="#2c3a54" stroke-width="2.5" fill="none"/></g>'
              + '<g transform="translate(16,74)"><path d="M -12,0 L -2,0 L -2.5,6 C -3,9 -10,9 -11,6 Z M 12,0 L 2,0 L 2.5,6 C 3,9 10,9 11,6 Z" fill="#141218"/><path d="M -2,1 Q 0,-1 2,1" stroke="#141218" stroke-width="1.4" fill="none"/></g>')

AUNT_BODY = ('<path d="M -42,206 L 42,206 L 48,452 L -48,452 Z" fill="#2f6d72"/>'
             '<path d="M -42,206 L -26,206 L -30,452 L -48,452 Z" fill="#3c8186"/><path d="M 26,206 L 42,206 L 48,452 L 32,452 Z" fill="#245458"/>'
             + ''.join(f'<path d="M {-44 + i * 3},{y} L {44 + i * 3},{y}" stroke="#8a5a3c" stroke-width="5" opacity=".75"/>' for i, y in enumerate((240, 300, 360, 420)))
             + ''.join(f'<circle cx="{x}" cy="{y}" r="4" fill="#d9b88a" opacity=".8"/>' for x in (-30, -10, 10, 30) for y in (270, 330, 390))
             + '<path d="M 10,206 L 18,452" stroke="#245458" stroke-width="2"/>'
             '<path d="M -34,450 L -12,450 L -12,462 L -34,462 Z" fill="#e4ae86"/><path d="M 34,450 L 12,450 L 12,462 L 34,462 Z" fill="#cc9670"/>'
             + flipflops('#c4463d', '#e9e4dc', '#e4ae86', '#cc9670')
             + arms('#e4ae86', '#cc9670', '#f2cba8')
             + tee('#c8a2c8', '#dcbcdc', '#a983ad', hem=214, sleeve_len=150)
             + ''.join(f'<g transform="translate({x},{y})"><circle r="5" fill="#e88aa8"/><circle r="2" fill="#f6e2a0"/><path d="M 4,4 q 6,2 8,8" stroke="#5f9060" stroke-width="2" fill="none"/></g>'
                       for x, y in ((-30, 80), (-6, 100), (22, 86), (-24, 140), (6, 150), (30, 128), (-14, 186), (20, 192)))
             # cloth bag with bananas, left hand
             + '<g transform="translate(-62,262)"><path d="M -6,-30 C -6,-48 14,-48 14,-30" stroke="#b49a78" stroke-width="4" fill="none"/>'
             '<path d="M -22,-30 L 30,-30 L 26,30 L -18,30 Z" fill="#e6dcc6"/><path d="M 14,-30 L 30,-30 L 26,30 L 12,30 Z" fill="#cfc3aa"/>'
             '<path d="M -10,-30 C -14,-50 -4,-60 6,-58 C 0,-52 -2,-42 0,-30 Z M 2,-30 C 2,-52 14,-60 22,-54 C 14,-50 10,-42 10,-30 Z" fill="#e8c35e"/>'
             '<path d="M -10,-30 C -12,-44 -8,-52 -2,-56 L 0,-30 Z" fill="#c9a24a"/></g>')

AGENT_BODY = ('<path d="M -41,228 L 41,228 L 44,300 L 37,462 L 9,462 L 2,292 L -2,292 L -9,462 L -37,462 L -44,300 Z" fill="#b9a688"/>'
              '<path d="M -41,228 L -24,228 L -28,300 L -26,462 L -37,462 L -44,300 Z" fill="#cbb999"/>'
              '<path d="M 22,236 L 41,228 L 44,300 L 37,462 L 26,462 C 28,380 26,300 22,236 Z" fill="#9c8a6c"/>'
              '<rect x="-41" y="228" width="82" height="8" fill="#5e4c40"/><rect x="-6" y="228" width="12" height="8" fill="#c9b07a"/>'
              '<path d="M -40,462 L -6,462 C -4,472 -6,478 -10,480 L -42,480 C -46,476 -45,466 -40,462 Z M 40,462 L 6,462 C 4,472 6,478 10,480 L 42,480 C 46,476 45,466 40,462 Z" fill="#5e4434"/>'
              + arms('#e9b993', '#d29e78', '#f5d2b2')
              + tee('#efe6d6', '#faf4ea', '#d6ccba', hem=232)
              + '<path d="M -12,49 L -16,62 L -4,58 Z M 12,49 L 16,62 L 4,58 Z" fill="#faf4ea"/><path d="M 0,56 L 0,84" stroke="#d6ccba" stroke-width="2"/>'
              + ''.join(f'<circle cx="2.5" cy="{y}" r="1.4" fill="#b9ae9a"/>' for y in (64, 74))
              + '<g transform="translate(-24,90)"><rect x="-6" y="-5" width="12" height="10" rx="2" fill="#2f6fb5"/><path d="M -3,0 l 3,-3 l 3,3" stroke="#fff" stroke-width="1.2" fill="none"/></g>'
              # clipboard + keys
              + '<g transform="translate(46,214) rotate(-8)"><rect x="-20" y="-30" width="40" height="54" rx="3" fill="#8a6a50"/><rect x="-16" y="-24" width="32" height="44" fill="#f8f4ec"/>'
              '<rect x="-8" y="-34" width="16" height="8" rx="2" fill="#9aa1b0"/>' + ''.join(f'<path d="M -11,{y} L 11,{y}" stroke="#b9b2a4" stroke-width="1.4"/>' for y in (-14, -6, 2, 10)) + '</g>'
              + '<g transform="translate(-48,272)"><circle r="5" fill="none" stroke="#c9ced8" stroke-width="2"/><path d="M 0,5 L 0,18 M 0,12 l 4,0 M 0,16 l 3,0" stroke="#d9b25e" stroke-width="2.4"/></g>'
              + '<rect x="-55" y="222" width="14" height="6" rx="2" fill="#2c3040"/>')

NB_BODY = (shorts('#d8655a', '#e8836f', '#b44e46', '#f8d8c6', '#ebbca6')
           + '<path d="M -36,460 L -10,460 C -6,468 -8,478 -12,480 L -40,480 C -44,476 -42,466 -36,460 Z" fill="#f8d8c6"/>'
           '<path d="M 36,460 L 10,460 C 6,468 8,478 12,480 L 40,480 C 44,476 42,466 36,460 Z" fill="#ebbca6"/>'
           + arms('#f8d8c6', '#ebbca6', '#fff0e8')
           + tee('#2c3a54', '#3d4f6e', '#1f2a40')
           + '<g transform="translate(0,120)"><path d="M -20,0 q 10,-12 20,0 q 10,12 20,0" stroke="#7fd3d6" stroke-width="3" fill="none"/>'
           '<text x="0" y="24" font-family="Inter, sans-serif" font-size="12" font-weight="700" fill="#7fd3d6" text-anchor="middle">DIVE</text></g>'
           # dive mask in the left hand
           + '<g transform="translate(-60,272)"><rect x="-16" y="-8" width="32" height="15" rx="6" fill="#22303f"/><rect x="-13" y="-5.5" width="26" height="10" rx="4" fill="#9ad7e3"/>'
           '<path d="M -16,0 C -24,-2 -26,12 -18,16 M 16,0 C 24,-2 26,12 18,16" stroke="#22303f" stroke-width="3" fill="none"/></g>')

GECKO = ('<g>'
         # tail: short, chubby, curled
         '<path d="M 4,40 C 14,62 34,70 42,58 C 48,48 40,40 32,44 C 38,48 36,54 30,54 C 20,54 14,44 12,34 Z" fill="#8aa2c2"/>'
         # stubby legs with round toe pads
         + ''.join(f'<path d="M {x0},{y0} L {x1},{y1}" stroke="#8aa2c2" stroke-width="11" stroke-linecap="round"/>'
                   f'<circle cx="{x1 + dx}" cy="{y1 - 5}" r="4.2" fill="#9cb3d0"/><circle cx="{x1 + dx * 1.6:.1f}" cy="{y1}" r="4.2" fill="#9cb3d0"/><circle cx="{x1 + dx}" cy="{y1 + 5}" r="4.2" fill="#9cb3d0"/>'
                   for x0, y0, x1, y1, dx in ((-14, -4, -30, -16, -5), (14, -4, 30, -16, 5), (-12, 26, -28, 38, -5), (12, 26, 28, 38, 5)))
         # round body, soft belly-light band on the lit side
         + '<ellipse cx="0" cy="12" rx="20" ry="30" fill="#8aa2c2"/><path d="M -20,12 C -20,-6 -12,-16 -4,-18 C -12,-6 -14,10 -12,30 C -16,26 -20,20 -20,12 Z" fill="#a7bcd8"/>'
         # big round head
         '<ellipse cx="0" cy="-34" rx="27" ry="23" fill="#8aa2c2"/><path d="M -27,-34 C -27,-48 -16,-56 -4,-57 C -16,-50 -21,-40 -20,-26 C -24,-28 -27,-31 -27,-34 Z" fill="#a7bcd8"/>'
         # a few round orange spots, no bumps
         + ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#f0956e"/>' for x, y, r in ((-7, 0, 3.6), (8, 10, 3.2), (-5, 24, 3), (10, -48, 2.6), (-14, -46, 2.2), (30, 56, 2.4)))
         # big sparkly eyes, blush, tiny smile
         + '<circle cx="-11" cy="-36" r="8.5" fill="#2a2433"/><circle cx="11" cy="-36" r="8.5" fill="#2a2433"/>'
         '<circle cx="-13.6" cy="-39" r="3.2" fill="#fff"/><circle cx="8.4" cy="-39" r="3.2" fill="#fff"/><circle cx="-8.6" cy="-33" r="1.4" fill="#fff"/><circle cx="13.4" cy="-33" r="1.4" fill="#fff"/>'
         '<ellipse cx="-19" cy="-24" rx="5" ry="2.8" fill="#f09a9a" opacity=".7"/><ellipse cx="19" cy="-24" rx="5" ry="2.8" fill="#f09a9a" opacity=".7"/>'
         '<path d="M -5,-23 Q 0,-19 5,-23" stroke="#4a5a74" stroke-width="1.8" fill="none" stroke-linecap="round"/>'
         '</g>')

# ---------------------------------------------------------------- more islanders (added after the first review)
UNCLE_SKIN = ['#d9a07a', '#c08860', '#9e6a48', '#cf9672', '#b27c58', '#e8bc98', '#b07a56', '#a87452']
un_kit = recolor(JK, J_SKIN, UNCLE_SKIN).replace('fill="#17151d"', 'fill="#8a8590"')          # grey brows
un_kit = un_kit.replace('<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>', GRIN)
UNCLE_HEAD = ('<g id="h_uncle">' + un_kit +
              '<path d="M -18,-26 q 18,-4 36,0 M -14,-21 q 14,-3 28,0" stroke="#a87452" stroke-width="1.1" fill="none" opacity=".8"/>'
              '<path d="M -12,15 C -14,19 -13,23 -10,26 M 12,15 C 14,19 13,23 10,26" fill="none" stroke="#a06a48" stroke-width="1.2"/>'
              '<path d="M -1,18.4 C -6,17.4 -11,18.6 -13,21.6 C -8,20.6 -4,20.2 -1,20.4 Z M 1,18.4 C 6,17.4 11,18.6 13,21.6 C 8,20.6 4,20.2 1,20.4 Z" fill="#cfcbd2"/>'
              '<path d="M -32,-8 C -34,-40 -18,-50 0,-50 C 18,-50 34,-40 32,-8 C 30,-24 22,-36 0,-38 C -22,-36 -30,-24 -32,-8 Z" fill="#9a96a0"/>'
              '<path d="M -26,-34 C -16,-44 4,-46 16,-42 C 4,-40 -12,-38 -22,-30 Z" fill="#c4c0c8"/>'
              '</g>')

el_kit = recolor(JK, J_SKIN, TAN).replace('<path d="M 22,-14.6 C 17,-16 11,-14.6 7,-12.6 L 7,-9.8 C 11,-11.6 17,-12.6 21,-11.4 Z" fill="#17151d"/>',
                                           '<path d="M 22,-12.5 L 7,-12 L 7,-9.2 L 21,-9.4 Z" fill="#17151d"/>')
el_kit = el_kit.replace('<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>',
                        '<path d="M -7,22.4 Q 0,26 7,22.4" fill="none" stroke="#8c4a42" stroke-width="1.9" stroke-linecap="round"/>')
ELEC_HEAD = ('<g id="h_elec">'
             '<path d="M -34,-6 C -36,-30 -24,-40 0,-40 C 24,-40 36,-30 34,-6 L 30,-14 L -30,-14 Z" fill="#1a171d"/>' + el_kit +
             # cap + headlamp
             '<path d="M -34,-24 C -34,-52 34,-52 34,-24 Z" fill="#2c3a54"/><path d="M -34,-24 C -34,-48 -10,-52 0,-52 C -18,-46 -26,-36 -28,-24 Z" fill="#3d4f6e"/>'
             '<path d="M -36,-24 L 44,-24 C 46,-20 40,-18 30,-18 L -36,-20 Z" fill="#22304a"/>'
             '<path d="M -36,-30 L 36,-30" stroke="#1b1d24" stroke-width="4"/><rect x="-8" y="-38" width="16" height="11" rx="3" fill="#1b1d24"/><circle cx="0" cy="-32.5" r="4" fill="#fff6dc"/>'
             '</g>')
LAMP_GLOW = '<circle cx="0" cy="-32.5" r="22" fill="#fff4d6" opacity=".22"/><circle cx="0" cy="-32.5" r="10" fill="#fff4d6" opacity=".35"/>'

VENDOR_SKIN = ['#eebd94', '#d6a27a', '#b88158', '#e5b38a', '#c99670', '#dba27a', '#f7d8b6', '#c78c66', '#c08562']
ve_kit = recolor(TK, T_SKIN, VENDOR_SKIN)
VENDOR_HEAD = ('<g id="h_vendor">'
               '<path d="M -36,0 C -40,-40 -22,-58 0,-58 C 22,-58 40,-40 36,0 L 28,-10 L -28,-10 Z" fill="#1d171c"/>' + ve_kit +
               '<path d="M -34,-6 C -36,-42 -18,-56 2,-56 C 22,-56 36,-42 34,-6 C 30,-26 18,-38 2,-40 C -16,-38 -30,-26 -34,-6 Z" fill="#1d171c"/>'
               '<circle cx="0" cy="-62" r="14" fill="#1d171c"/><path d="M -10,-66 q 10,-8 20,0" stroke="#3a3038" stroke-width="2" fill="none"/>'
               '<path d="M -14,-56 L 14,-56" stroke="#e8835f" stroke-width="4" stroke-linecap="round"/>'
               '</g>')

dv_kit = recolor(JK, J_SKIN, ['#f3cdb3', '#e2b294', '#c7967a', '#ecc2a6', '#d3a486', '#fbe2cf', '#d9a286', '#cfa088'])
dv_kit = dv_kit.replace('<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>', GRIN)
DIVER_HEAD = ('<g id="h_diver">'
              '<path d="M -34,-4 C -38,-38 -22,-56 0,-56 C 22,-56 38,-38 34,-4 L 28,-14 L -28,-14 Z" fill="#3a2a22"/>' + dv_kit +
              '<path d="M -34,-10 C -38,-40 -20,-56 2,-56 C 24,-56 38,-40 34,-10 C 30,-30 16,-38 -2,-38 C -18,-38 -30,-28 -34,-10 Z" fill="#3a2a22"/>'
              '<path d="M -24,-42 C -14,-50 4,-52 14,-48 C 2,-46 -12,-42 -20,-34 Z" fill="#5e4636"/>'
              '<g><path d="M -36,-30 C -30,-36 30,-36 36,-30" stroke="#22303f" stroke-width="3.4" fill="none"/><rect x="-23" y="-46" width="46" height="17" rx="7" fill="#22303f"/>'
              '<rect x="-19.5" y="-43.6" width="39" height="12" rx="5" fill="#9ad7e3" opacity=".9"/><path d="M -16,-42 L -9,-42 L -15,-33 Z" fill="#fff" opacity=".55"/></g>'
              '</g>')

PAKAOMA = ('<g><path d="M 14,50 C 26,52 40,58 46,70 L 42,92 C 34,78 24,70 10,66 Z" fill="#c4463d"/>'
           + ''.join(f'<path d="M {14 + i * 7},{52 + i * 3} L {10 + i * 8},{68 + i * 5}" stroke="#2f6d72" stroke-width="2.4"/>' for i in range(5))
           + '<path d="M 20,60 L 44,76" stroke="#f2eee6" stroke-width="1.6"/><path d="M 42,92 L 40,130 L 30,128 L 34,90 Z" fill="#c4463d"/>'
           '<path d="M 32,98 L 41,100 M 31,110 L 40,112 M 31,122 L 40,124" stroke="#2f6d72" stroke-width="2"/></g>')
UNCLE_BODY = ('<path d="M -44,226 L 44,226 L 46,350 L 6,352 L 2,292 L -2,292 L -6,352 L -46,350 Z" fill="#2c3a54"/>'
              '<path d="M -44,226 L -28,226 L -30,350 L -46,350 Z" fill="#3d4f6e"/>'
              '<path d="M -38,350 L -12,350 L -13,462 L -33,462 Z" fill="#d9a07a"/><path d="M 38,350 L 12,350 L 13,462 L 33,462 Z" fill="#c08860"/>'
              + flipflops('#3c4458', '#5e6270', '#d9a07a', '#c08860')
              + arms('#d9a07a', '#c08860', '#e8bc98', tank=True)
              + tank('#f2eee6', '#ffffff', '#d6d0c4') + PAKAOMA
              + '<g transform="translate(52,268)"><circle r="5" fill="none" stroke="#c9ced8" stroke-width="2"/><rect x="-4" y="5" width="8" height="12" rx="2" fill="#2c3040"/></g>')
ELEC_BODY = ('<path d="M -41,228 L 41,228 L 44,300 L 38,420 L 9,420 L 2,292 L -2,292 L -9,420 L -38,420 L -44,300 Z" fill="#5e6650"/>'
             '<path d="M -41,228 L -24,228 L -28,300 L -26,420 L -38,420 L -44,300 Z" fill="#717a62"/>'
             '<rect x="-46" y="300" width="14" height="30" rx="3" fill="#4f5644"/><rect x="32" y="300" width="14" height="30" rx="3" fill="#4f5644"/>'
             '<path d="M -40,416 L -8,416 L -6,480 L -44,480 Z" fill="#1d1f26"/><path d="M 40,416 L 8,416 L 6,480 L 44,480 Z" fill="#14161c"/>'
             '<rect x="-46" y="476" width="42" height="9" rx="3" fill="#2c2f38"/><rect x="4" y="476" width="42" height="9" rx="3" fill="#24262e"/>'
             + arms('#e9b993', '#d29e78', '#f5d2b2')
             + tee('#2c3a54', '#3d4f6e', '#1f2a40', hem=232)
             + '<path d="M -44,150 L 44,150 L 44,160 L -44,160 Z" fill="#e8835f"/><path d="M -44,154 L 44,154" stroke="#f6d0b8" stroke-width="2"/>'
             '<rect x="-44" y="222" width="88" height="12" fill="#6f5442"/><rect x="18" y="226" width="16" height="26" rx="3" fill="#5e4636"/>'
             '<path d="M -26,226 L -26,252 M -20,226 L -18,250" stroke="#9aa1b0" stroke-width="4" stroke-linecap="round"/><rect x="-30" y="238" width="10" height="16" rx="2" fill="#c4463d"/>'
             '<g transform="translate(-60,266)"><rect x="-6" y="-24" width="12" height="30" rx="4" fill="#1b1d24"/><rect x="-8" y="-30" width="16" height="8" rx="2" fill="#2c3040"/><circle cx="0" cy="-26" r="4" fill="#fff6dc"/></g>')
VENDOR_BODY = ('<path d="M -42,206 L 42,206 L 48,452 L -48,452 Z" fill="#5e4a6a"/><path d="M -42,206 L -26,206 L -30,452 L -48,452 Z" fill="#6f5a7c"/>'
               + ''.join(f'<path d="M -46,{y} L 46,{y}" stroke="#c9a87a" stroke-width="3" opacity=".7"/>' for y in (260, 330, 400))
               + '<path d="M -34,450 L -12,450 L -12,462 L -34,462 Z" fill="#eebd94"/><path d="M 34,450 L 12,450 L 12,462 L 34,462 Z" fill="#d6a27a"/>'
               + flipflops('#2f6d72', '#e9e4dc', '#eebd94', '#d6a27a')
               + arms('#eebd94', '#d6a27a', '#f7d8b6')
               + tee('#e9a090', '#f2b6a6', '#c98272', hem=214, sleeve_len=126)
               + '<path d="M -30,96 L 30,96 L 34,236 L -34,236 Z" fill="#2f8f94"/><path d="M -30,96 L -16,96 L -20,236 L -34,236 Z" fill="#3fa2a6"/>'
               '<path d="M -26,96 L -30,58 M 26,96 L 30,58" stroke="#2f8f94" stroke-width="4"/><rect x="-16" y="150" width="32" height="24" rx="4" fill="#257a7e"/>')
DIVER_BODY = ('<path d="M -44,226 L 44,226 L 46,300 L 40,456 L 8,456 L 3,298 L -3,298 L -8,456 L -40,456 L -46,300 Z" fill="#1f2b46"/>'
              '<path d="M -44,226 L -30,226 L -32,300 L -30,456 L -40,456 L -46,300 Z" fill="#2c3b5e"/>'
              '<path d="M -40,300 L -36,456 M 38,300 L 36,456" stroke="#2fb3b8" stroke-width="3"/>'
              '<path d="M -40,454 L -10,454 L -8,470 L -44,470 Z" fill="#f3cdb3"/><path d="M 40,454 L 10,454 L 8,470 L 44,470 Z" fill="#e2b294"/>'
              '<path d="M -55,114 L -41,118 L -40,170 L -42,236 L -54,236 L -57,170 Z" fill="#1f2b46"/><path d="M 55,114 L 41,118 L 40,170 L 42,236 L 54,236 L 57,170 Z" fill="#162036"/>'
              '<path d="M -55,234 L -41,234 C -40,248 -42,262 -48,264 C -54,264 -57,250 -55,234 Z" fill="#f3cdb3"/><path d="M 55,234 L 41,234 C 40,248 42,262 48,264 C 54,264 57,250 55,234 Z" fill="#e2b294"/>'
              + tee('#1f2b46', '#2c3b5e', '#162036', hem=234, sleeve_len=230)
              + '<path d="M -48,72 L -40,180 M 48,72 L 40,180" stroke="#2fb3b8" stroke-width="3.2"/>'
              '<g transform="translate(70,300) rotate(10)"><path d="M -10,-50 L 10,-50 L 18,40 L -18,40 Z" fill="#2fb3b8"/><path d="M -10,-50 L 0,-50 L -4,40 L -18,40 Z" fill="#4fc6ca"/></g>')

DOG = ('<g>'
       '<path d="M 70,-30 C 92,-46 100,-70 86,-76 C 82,-62 74,-48 62,-40 Z" fill="#b98057"/>'                          # curled tail
       '<path d="M -40,10 L -32,10 L -30,62 L -40,62 Z M -14,10 L -4,10 L -4,62 L -14,62 Z" fill="#93623f"/>'           # far legs
       '<ellipse cx="14" cy="-14" rx="62" ry="32" fill="#b98057"/>'
       '<path d="M -48,-14 C -48,-34 -20,-46 14,-46 C 40,-46 64,-38 72,-24 C 50,-34 20,-38 -6,-36 C -26,-34 -40,-26 -48,-14 Z" fill="#d4a274"/>'
       '<path d="M 30,8 C 50,8 68,0 74,-14 C 70,4 52,16 28,16 Z" fill="#93623f"/>'
       '<path d="M -52,-6 C -50,10 -36,18 -24,14 C -30,6 -36,-2 -38,-14 Z" fill="#f2e6d6"/>'                             # white chest
       '<path d="M -26,14 L -16,14 L -16,66 L -27,66 Z M 46,8 L 56,4 L 58,64 L 47,64 Z M 20,14 L 30,12 L 31,64 L 21,64 Z" fill="#b98057"/>'
       '<path d="M -27,62 L -14,62 C -12,68 -14,72 -18,72 L -30,72 C -32,68 -31,64 -27,62 Z M 47,60 L 60,60 C 62,66 60,70 56,70 L 44,70 C 42,66 43,62 47,60 Z M 21,60 L 33,60 C 35,66 33,70 29,70 L 18,70 C 16,66 17,62 21,60 Z" fill="#f2e6d6"/>'
       # head, side view (full 90 degrees)
       '<path d="M -44,-40 C -50,-70 -30,-86 -10,-80 C 4,-76 10,-60 4,-44 C 0,-34 -14,-28 -28,-30 Z" fill="#b98057"/>'
       '<path d="M -44,-40 C -50,-70 -30,-86 -10,-80 C -26,-76 -36,-62 -34,-44 Z" fill="#d4a274"/>'
       '<path d="M -44,-52 L -76,-50 C -82,-48 -82,-38 -76,-36 L -46,-32 Z" fill="#d4a274"/>'                           # snout
       '<path d="M -76,-36 L -46,-32 L -46,-28 L -72,-30 Z" fill="#f2e6d6"/>'
       '<ellipse cx="-79" cy="-46" rx="5" ry="4" fill="#2a2024"/>'
       '<path d="M -10,-80 L -2,-104 L 8,-78 Z" fill="#93623f"/><path d="M -8,-82 L -2,-98 L 4,-80 Z" fill="#c98f6a"/>'      # ear
       '<circle cx="-40" cy="-58" r="4.6" fill="#2a2024"/><circle cx="-41.6" cy="-59.6" r="1.6" fill="#fff"/>'
       '<path d="M -70,-32 Q -62,-26 -54,-30" stroke="#6a4430" stroke-width="1.6" fill="none"/>'
       '<ellipse cx="-50" cy="-44" rx="5" ry="2.6" fill="#e88a7a" opacity=".5"/>'
       '<path d="M -36,-30 L -12,-28 L -14,-22 L -36,-24 Z" fill="#2fb3b8"/>'                                           # collar from a neighbour
       '</g>')

# ---------------------------------------------------------------- dog v2: sitting, front view, built like Dean's sheet (round head, full cheeks, block shading)
DC, DL, DS, DCR, DCS = '#c8915e', '#deb183', '#a5703f', '#f6eadb', '#e2cfb6'
DOG = (f'<g>'
       # tail wagging up on the viewer's right
       f'<path d="M 52,150 C 80,140 92,110 86,92 C 96,104 98,130 84,150 C 76,160 62,164 52,162 Z" fill="{DC}"/>'
       f'<path d="M 86,92 C 92,100 94,112 92,122 C 90,110 88,100 86,92 Z" fill="{DL}"/>'
       # haunches + body
       f'<ellipse cx="-44" cy="140" rx="26" ry="30" fill="{DC}"/><ellipse cx="44" cy="140" rx="26" ry="30" fill="{DS}"/>'
       f'<path d="M -56,146 C -62,90 -40,36 0,34 C 40,36 62,90 56,146 C 54,164 34,172 0,172 C -34,172 -54,164 -56,146 Z" fill="{DC}"/>'
       f'<path d="M 22,40 C 48,52 62,96 56,146 C 54,162 40,170 20,172 C 36,150 42,104 22,40 Z" fill="{DS}"/>'
       f'<path d="M -46,80 C -40,56 -26,42 -12,38 C -30,54 -38,80 -40,116 Z" fill="{DL}"/>'
       # cream chest
       f'<path d="M -24,44 C -14,36 14,36 24,44 C 28,84 16,114 0,120 C -16,114 -28,84 -24,44 Z" fill="{DCR}"/>'
       f'<path d="M 8,38 C 18,38 24,42 24,44 C 28,84 16,114 0,120 C 12,100 16,70 8,38 Z" fill="{DCS}"/>'
       # front legs, a bit longer than the cat's, round paws
       f'<path d="M -24,166 L -24,108 C -24,98 -6,98 -6,108 L -6,166 Z" fill="{DL}"/>'
       f'<path d="M 6,166 L 6,108 C 6,98 24,98 24,108 L 24,166 Z" fill="{DC}"/>'
       f'<ellipse cx="-15" cy="168" rx="13" ry="7" fill="{DCR}"/><ellipse cx="15" cy="168" rx="13" ry="7" fill="{DCS}"/>'
       f'<path d="M -19,164 L -19,170 M -11,164 L -11,170 M 11,164 L 11,170 M 19,164 L 19,170" stroke="{DCS}" stroke-width="1.2"/>'
       # collar with a tag
       f'<path d="M -28,40 C -14,50 14,50 28,40 L 28,47 C 14,57 -14,57 -28,47 Z" fill="#2fb3b8"/><circle cx="0" cy="56" r="5" fill="#e2b04a"/>'
       # head: ears up with soft folded tips
       f'<path d="M -46,-30 L -54,-76 C -42,-74 -28,-60 -22,-46 Z" fill="{DC}"/><path d="M -44,-36 L -50,-68 C -42,-64 -34,-54 -30,-44 Z" fill="#e8b4a0"/>'
       f'<path d="M -54,-76 C -50,-70 -46,-66 -40,-64 L -48,-60 Z" fill="{DS}"/>'
       f'<path d="M 46,-30 L 54,-76 C 42,-74 28,-60 22,-46 Z" fill="{DS}"/><path d="M 44,-36 L 50,-68 C 42,-64 34,-54 30,-44 Z" fill="#d49c8a"/>'
       f'<path d="M -54,4 C -56,-34 -30,-52 0,-52 C 30,-52 56,-34 54,4 C 52,32 30,46 0,46 C -30,46 -52,32 -54,4 Z" fill="{DC}"/>'
       f'<path d="M 30,-46 C 50,-34 58,-10 54,8 C 50,32 28,46 0,46 C 24,38 40,22 42,2 C 44,-18 40,-34 30,-46 Z" fill="{DS}"/>'
       f'<path d="M -50,-20 C -42,-40 -22,-50 -6,-50 C -24,-44 -36,-34 -44,-14 Z" fill="{DL}"/>'
       # cream muzzle (longer than the cat's), black round nose, happy open mouth
       f'<path d="M -22,12 C -24,-4 -8,-8 0,-2 C 8,-8 24,-4 22,12 C 20,30 10,38 0,38 C -10,38 -20,30 -22,12 Z" fill="{DCR}"/>'
       f'<path d="M 4,-2 C 12,-8 24,-4 22,12 C 20,30 10,38 2,38 C 12,30 16,16 4,-2 Z" fill="{DCS}"/>'
       f'<ellipse cx="0" cy="4" rx="7.5" ry="5.6" fill="#2a2024"/><ellipse cx="-2.4" cy="2.4" rx="2.4" ry="1.4" fill="#6a5a60"/>'
       f'<path d="M 0,9.6 L 0,14 M -9,15 Q -4.5,21 0,15 Q 4.5,21 9,15" fill="none" stroke="#6a4430" stroke-width="1.5" stroke-linecap="round"/>'
       f'<path d="M -5,18 Q 0,30 5,18 Z" fill="#e8838a"/><path d="M 0,19 L 0,25" stroke="#c96a70" stroke-width="1"/>'
       f'<ellipse cx="-32" cy="12" rx="7" ry="4" fill="#f09a8c" opacity=".5"/><ellipse cx="32" cy="12" rx="7" ry="4" fill="#e08c7c" opacity=".45"/>'
       # big friendly eyes, a brow tuft each (a Thai street dog's expressive "eyebrows")
       f'<ellipse cx="-20" cy="-14" rx="7.4" ry="8.2" fill="#3a2614"/><ellipse cx="20" cy="-14" rx="7.4" ry="8.2" fill="#3a2614"/>'
       f'<circle cx="-22.6" cy="-17.4" r="2.8" fill="#fff8ee"/><circle cx="17.4" cy="-17.4" r="2.8" fill="#fff8ee"/><circle cx="-17.6" cy="-11" r="1.2" fill="#fff8ee"/><circle cx="22.4" cy="-11" r="1.2" fill="#fff8ee"/>'
       f'<ellipse cx="-20" cy="-28" rx="5" ry="2.6" fill="{DL}"/><ellipse cx="20" cy="-28" rx="5" ry="2.6" fill="#c9966a"/>'
       f'</g>')

# ---------------------------------------------------------------- Lae: island-born dive instructor (built on Tawan's head)
LAE_SKIN = ['#f0c29a', '#dca27c', '#bb7e5a', '#e8b690', '#fbe2c6', '#cf9270', '#e6b48c', '#c88c68', '#c88c6a']
lae_kit = recolor(TK, T_SKIN, LAE_SKIN)
HAIR_L, HAIR_LH = '#2a1c18', '#6e4a34'
LAE_BACK = ('<g id="h_lae_back">'
            f'<path d="M -38,-4 C -42,-46 -22,-64 0,-64 C 22,-64 42,-46 38,-4 C 44,20 40,40 46,60 C 52,80 44,100 50,122 L 40,132 C 36,116 30,124 22,118 L 18,58 L -18,58 L -22,118 C -30,124 -36,116 -40,132 L -50,122 C -44,100 -52,80 -46,60 C -40,40 -44,20 -38,-4 Z" fill="{HAIR_L}"/>'
            f'<path d="M -42,30 C -46,50 -40,70 -46,92 C -42,104 -46,114 -44,124 L -48,122 C -50,104 -42,84 -48,64 C -46,52 -46,40 -42,30 Z" fill="{HAIR_LH}"/>'
            '</g>')
LAE_HEAD = ('<g id="h_lae">' + lae_kit +
            # centre-parted crown + wavy curtains framing the face down to the shoulders
            f'<path d="M -38,-4 C -40,-46 -22,-64 0,-64 C 22,-64 40,-46 38,-4 L 31,-6 C 29,-24 18,-36 0,-40 C -18,-36 -29,-24 -31,-6 Z" fill="{HAIR_L}"/>'
            f'<path d="M -30,-42 C -22,-56 -10,-60 -2,-61 C -12,-54 -22,-46 -27,-34 Z" fill="{HAIR_LH}"/>'
            f'<path d="M -38,-10 L -30,-10 C -32,10 -26,26 -32,44 C -36,58 -28,72 -32,90 L -40,96 C -36,80 -44,66 -40,52 C -36,36 -42,18 -38,-10 Z" fill="{HAIR_L}"/>'
            f'<path d="M -36,0 C -38,20 -33,32 -37,48 C -40,60 -34,70 -37,84 L -38,84 C -38,70 -42,60 -39,48 C -36,32 -40,20 -36,0 Z" fill="{HAIR_LH}"/>'
            f'<path d="M 38,-10 L 30,-10 C 32,10 26,26 32,44 C 36,58 28,72 32,90 L 40,96 C 36,80 44,66 40,52 C 36,36 42,18 38,-10 Z" fill="{HAIR_L}"/>'
            # frangipani behind the left ear
            '<g transform="translate(-34,-14)">' + ''.join(f'<ellipse cx="0" cy="-6" rx="4.2" ry="7" fill="#fbf7f0" transform="rotate({a})"/>' for a in (0, 72, 144, 216, 288))
            + '<circle r="3" fill="#f2c26a"/></g>'
            '<path d="M -26,46 C -14,58 14,58 26,46" stroke="#e9e1d0" stroke-width="1.4" fill="none"/>'
            + ''.join(f'<ellipse cx="{x}" cy="{y}" rx="2.6" ry="1.8" fill="#f3ece0"/>' for x, y in ((-18, 52), (-9, 55.6), (0, 57), (9, 55.6), (18, 52)))
            + '</g>')
LAE_BODY = ('<use href="#h_lae_back"/>'
            # legs + sandals
            '<path d="M -40,236 L -12,236 L -13,446 L -33,446 Z" fill="#f0c29a"/><path d="M 40,236 L 12,236 L 13,446 L 33,446 Z" fill="#dca27c"/>'
            '<path d="M -40,236 L -34,236 L -32,446 L -35,446 Z" fill="#fbe2c6" opacity=".6"/>'
            '<path d="M -34,446 L -12,446 C -10,454 -12,460 -16,462 L -38,462 C -41,458 -40,450 -34,446 Z" fill="#f0c29a"/>'
            '<path d="M 34,446 L 12,446 C 10,454 12,460 16,462 L 38,462 C 41,458 40,450 34,446 Z" fill="#dca27c"/>'
            '<rect x="-42" y="460" width="34" height="6" rx="3" fill="#8a6a50"/><rect x="8" y="460" width="34" height="6" rx="3" fill="#6f5442"/>'
            '<path d="M -36,454 L -24,448 L -12,454 M 36,454 L 24,448 L 12,454" stroke="#8a6a50" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
            '<path d="M -34,436 C -26,440 -18,440 -12,436" stroke="#f3ece0" stroke-width="2" fill="none" stroke-dasharray="2 2"/>'
            # high-waist denim shorts
            '<path d="M -40,150 L 40,150 L 44,240 L 6,244 L 2,206 L -2,206 L -6,244 L -44,240 Z" fill="#7f9cc2"/>'
            '<path d="M -40,150 L -26,150 L -30,240 L -44,240 Z" fill="#9db6d6"/><path d="M 24,152 L 40,150 L 44,240 L 32,242 C 32,210 28,180 24,152 Z" fill="#647fa6"/>'
            '<path d="M -44,236 L -6,240 M 6,240 L 44,236" stroke="#e8eef6" stroke-width="2.4"/>'
            # bare arms
            '<path d="M -38,60 C -46,64 -49,80 -49,100 L -51,212 L -40,212 L -38,110 Z" fill="#f0c29a"/><path d="M -46,92 C -47,100 -48,110 -48,120 L -49,212 L -46,212 L -45,120 Z" fill="#fbe2c6"/>'
            '<path d="M 38,60 C 46,64 49,80 49,100 L 51,212 L 40,212 L 38,110 Z" fill="#dca27c"/>'
            '<path d="M -51,210 L -40,210 C -39,224 -41,236 -46,238 C -51,238 -53,226 -51,210 Z" fill="#f0c29a"/>'
            '<path d="M 51,210 L 40,210 C 39,224 41,236 46,238 C 51,238 53,226 51,210 Z" fill="#dca27c"/>'
            # teal crop top
            '<path d="M -26,62 C -14,58 14,58 26,62 L 30,140 L -30,140 Z" fill="#2f9a9e"/><path d="M -26,62 C -20,60 -16,60 -12,60 L -16,140 L -30,140 Z" fill="#45b0b2"/>'
            '<path d="M -30,140 L 30,140 L 30,152 L -30,152 Z" fill="#f0c29a"/>'
            # open white linen shirt, sleeves rolled to the elbow, knotted at the waist
            '<path d="M -12,50 C -24,52 -36,56 -40,64 L -50,108 L -38,112 L -36,140 L -24,150 L -20,64 Z" fill="#f6f2ea"/>'
            '<path d="M 12,50 C 24,52 36,56 40,64 L 50,108 L 38,112 L 36,140 L 24,150 L 20,64 Z" fill="#dcd5c8"/>'
            '<path d="M -50,100 L -38,104 L -38,112 L -50,108 Z M 50,100 L 38,104 L 38,112 L 50,108 Z" fill="#e6e0d4"/>'
            '<path d="M -22,140 C -10,146 10,146 22,140 L 18,156 L 6,150 L 0,160 L -6,150 L -18,156 Z" fill="#ece6da"/><circle cx="0" cy="146" r="5" fill="#dcd5c8"/>'
            # iced coffee in the right hand
            '<g transform="translate(56,206)"><path d="M -10,0 L 10,0 L 8,30 L -8,30 Z" fill="#f4efe6" opacity=".9"/><path d="M -9,10 L 9,10 L 8,30 L -8,30 Z" fill="#a9785a"/>'
            '<rect x="-11" y="-3" width="22" height="4" rx="2" fill="#e8e2da"/><path d="M 3,-3 L 6,-16" stroke="#2fb3b8" stroke-width="2"/></g>')

EXTRA_TOURIST = runpy.run_path(os.path.join(H, '..', 'episodes', 'ep01-koh-tao', 'sunrig.py'))['TOURIST']


# ---------------------------------------------------------------- page
def fig(svg_inner, cap, title, chips, view='0 0 400 900', h=None):
    return (f'<figure><svg viewBox="{view}" role="img" aria-label="{title}">{svg_inner}</svg>'
            f'<figcaption><b>{title}</b><br>{cap}</figcaption>'
            f'<div class="chips">' + ''.join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in chips) + '</div></figure>')


def stage(inner, tx=200, ty=132, s=1.4, floor=True):
    return ('<rect width="400" height="900" fill="#1b1f2b"/>' + ('<rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="816" rx="78" ry="10" fill="#10131b"/>' if floor else '')
            + f'<g transform="translate({tx},{ty}) scale({s})">{inner}</g>')


SUN_CITY = SG['BODY']
cards = [

    fig('<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="790" rx="110" ry="11" fill="#10131b"/>'
        + '<g transform="translate(200,440) scale(2.0)">' + DOG + '</g>',
        'หมาเกาะประจำซอย · นั่งหน้าตรง วาดแบบเดียวกับดีน (แมวส้มของเจม) หัวกลม แก้มเต็ม ตาโตมีประกาย จมูกกลม ยิ้มแลบลิ้นนิด ๆ ขนสั้นสีน้ำตาลอ่อน อกครีม หูตั้งปลายพับ หางกระดิก ปลอกคอสีฟ้ามีป้ายชื่อ', 'หมาเกาะ',
        [('#c8915e', 'ขน'), ('#f6eadb', 'อก'), ('#2fb3b8', 'ปลอกคอ')]),
    fig(stage(LAE_BODY + '<use href="#h_lae"/>', ty=138),
        'เล · สาวเกาะโดยกำเนิด ครูสอนดำน้ำ · ต่อยอดจากหัวตะวัน ผิวแทนสวย ผมยาวลอนดำอมน้ำตาลซีดแดด แสกกลาง ทัดดอกลีลาวดี สร้อยเปลือกหอย · เสื้อครอปสีเขียวทะเลกับเชิ้ตลินินขาวผูกเอว กางเกงยีนส์ขาสั้นเอวสูง รองเท้าแตะหนัง ถือกาแฟเย็น', 'เล (ตัวละครหญิง)',
        [('#f0c29a', 'ผิว'), ('#2a1c18', 'ผม'), ('#2f9a9e', 'เสื้อครอป'), ('#7f9cc2', 'ยีนส์')]),
    fig(stage(UNCLE_BODY + '<use href="#h_uncle"/>'),
        'ลุงรถกระบะที่ท่าเรือ · ต่อยอดจากหัวเจม ผิวคล้ำแดด ผมเกรียนสีดอกเลา หนวดขาว ยิ้มกว้าง เสื้อกล้ามขาว ผ้าขาวม้าพาดไหล่ กางเกงขาสั้น รองเท้าแตะ ถือกุญแจรถ', 'ลุงรถกระบะ',
        [('#d9a07a', 'ผิว'), ('#f2eee6', 'เสื้อกล้าม'), ('#c4463d', 'ผ้าขาวม้า')]),
    fig(stage(ELEC_BODY + '<use href="#h_elec"/>' + LAMP_GLOW),
        'พี่ช่างไฟ · ต่อยอดจากหัวเจม ผิวแทน หน้านิ่ง ๆ ชิล ๆ หมวกแก๊ปติดไฟฉายคาดหัว เสื้อช่างสีกรมแถบสะท้อนแสง กางเกงคาร์โก รองเท้าบูต เข็มขัดเครื่องมือ', 'พี่ช่างไฟ',
        [('#2c3a54', 'เสื้อ'), ('#e8835f', 'แถบสะท้อนแสง'), ('#5e6650', 'กางเกง')]),
    fig(stage(SUN_CITY + '<use href="#h_sun"/>' + '<path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/><path d="M -9,58 L -11,66 M 9,58 L 9.6,66" stroke="#2a2024" stroke-width="1.8"/>'),
        'ใช้ตอนย้อนอดีต · ชุดอินดี้เดิมตาม characters/sun.html', 'ซัน · ลุคกรุงเทพ (อดีต)', [('#2f5a5e', 'เชิ้ต'), ('#2b2d36', 'กางเกง')]),
    fig(stage(recolor(SUN_ISLAND, J_SKIN, TAN) + '<use href="#h_suntan"/>' + neck_after()),
        'ใช้ตอนปัจจุบัน · ผิวแทนแดด · เสื้อกล้ามสีฟ้าซีดแดด กางเกงขาสั้นลายใบไม้ รองเท้าแตะ ถือหมวกกันน็อกครึ่งใบ แว่นกันแดดเกี่ยวคอเสื้อ สร้อยเงินเส้นเดิม กำไลเชือก',
        'ซัน · ลุคชาวเกาะ (ปัจจุบัน)', [('#86b9c8', 'เสื้อกล้าม'), ('#24405a', 'กางเกงขาสั้น'), ('#2fb3b8', 'สายรองเท้า/หมวก')]),
    fig(stage(AUNT_BODY + '<use href="#h_aunt"/>', ty=150, s=1.32),
        'ป้าร้านข้างทาง · ต่อยอดจากหัวตะวัน ผิวแทน ผมดัดสั้นมีผมหงอกแซม ยิ้มกว้าง เสื้อลายดอก ผ้าถุงลายบาติก ถือถุงผ้าใส่กล้วย', 'ป้าร้านข้างทาง',
        [('#e4ae86', 'ผิว'), ('#c8a2c8', 'เสื้อลายดอก'), ('#2f6d72', 'ผ้าถุง')]),
    fig(stage(AGENT_BODY + '<use href="#h_agent"/>'),
        'นายหน้าบ้านเช่า · ต่อยอดจากหัวเจม ผิวแทน ผมหวีเรียบแสกข้าง หนวดบาง แว่นดำบนหัว เสื้อโปโล กางเกงสีกากี ถือคลิปบอร์ดกับพวงกุญแจ', 'นายหน้าบ้านเช่า',
        [('#e9b993', 'ผิว'), ('#efe6d6', 'โปโล'), ('#b9a688', 'กางเกง')]),
    fig(stage(NB_BODY + '<use href="#h_nb"/>' + neck_after()),
        'เพื่อนบ้านต่างชาติ ครูสอนดำน้ำ · ต่อยอดจากหัวเจม ผิวขาวโดนแดดแดง กระที่จมูก ผมน้ำตาลอ่อนซีดแดด หนวดเคราจาง เสื้อยืดร้านดำน้ำ ถือหน้ากาก เดินเท้าเปล่า', 'เพื่อนบ้านต่างชาติ',
        [('#f8d8c6', 'ผิว'), ('#a87c50', 'ผม'), ('#2c3a54', 'เสื้อ'), ('#d8655a', 'กางเกง')]),
    fig('<rect width="400" height="900" fill="#1b1f2b"/>' + ''.join(f'<rect x="{x}" y="{y}" width="78" height="78" fill="#e9e4dc" stroke="#d2ccc2" stroke-width="2"/>' for x in range(4, 400, 80) for y in range(250, 650, 80))
        + '<g transform="translate(200,440) rotate(-10) scale(2.6)">' + GECKO + '</g>',
        'ตุ๊กแกประจำบ้านแบบน่ารัก · หัวกลมโต ตาโตมีประกาย แก้มแดง ยิ้มนิด ๆ ตัวป้อม นิ้วกลม ไม่มีผิวตะปุ่มตะป่ำ ในฉากจะตัวเล็กอยู่มุมภาพ ไม่ซูมใกล้ · โผล่ 2 ครั้ง (คืนแรก และตอนไฟดับ)', 'ตุ๊กแก', [('#7d93b0', 'ตัว'), ('#e8835f', 'จุด'), ('#e2b04a', 'ตา')]),
]
cards = cards[4:6] + [cards[1]] + cards[6:] + [cards[0]] + cards[2:4]          # Sun first, new islanders after the first-round cast
extras = ('<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/>'
          + '<g transform="translate(70,330) scale(.8)">' + VENDOR_BODY + '<use href="#h_vendor"/></g>'
          + '<g transform="translate(200,330) scale(.8)">' + DIVER_BODY + '<use href="#h_diver"/></g>'
          + '<g transform="translate(330,330) scale(.8)">' + EXTRA_TOURIST + '</g>')
cards.append(fig(extras, 'ตัวประกอบไม่มีบท · แม่ค้าในตลาด (หัวตะวัน) · นักดำน้ำ (หัวเจม) · นักท่องเที่ยวหันหลัง ในฉากจะตัวเล็กและเบลอเป็นฉากหลัง', 'ตัวประกอบ', []))

close = (fig('<rect x="-75" y="-78" width="150" height="150" fill="#1b1f2b"/><path d="M -50,72 C -48,58 -30,50 -12,49 L 12,49 C 30,50 48,58 50,72 Z" fill="#86b9c8"/><use href="#h_sun"/>',
             'ใช้ตอนย้อนอดีตที่ยังอยู่กรุงเทพ', 'ย้อนอดีต · ผิวเดิม', [], view='-75 -78 150 150')
         + fig('<rect x="-75" y="-78" width="150" height="150" fill="#1b1f2b"/><path d="M -50,72 C -48,58 -30,50 -12,49 L 12,49 C 30,50 48,58 50,72 Z" fill="#86b9c8"/><use href="#h_suntan"/>',
               'ใช้ตอนเป็นชาวเกาะ (เจ้าของช่องเลือกแล้ว)', 'ตอนนี้ · ผิวแทนแดด', [], view='-75 -78 150 150'))

page = f'''<title>Odd Hours ตัวละคร EP.01</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: cast cards, 3 across on desktop, 2 on tablet, 1 on phone; skin option pair below. Single dark look by choice, like the other sheets. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1080px; margin:0 auto; display:grid; gap:18px; }}
h1 {{ font-size:18px; font-weight:500; margin:0; }} h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
h2 {{ font-size:15px; font-weight:500; margin:10px 0 0; }}
.grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:16px; }}
.pair {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:16px; max-width:640px; }}
@media (max-width:900px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid, .pair {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; border-radius:6px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:13px; color:var(--muted); line-height:1.55; }} figcaption b {{ color:var(--ink); font-weight:500; }}
.chips {{ display:flex; flex-wrap:wrap; gap:8px 14px; font-size:12px; color:var(--muted); }}
.chips span {{ display:inline-flex; align-items:center; gap:6px; }}
.chips i {{ width:14px; height:14px; border-radius:3px; display:inline-block; box-shadow:0 0 0 1px var(--line); }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{CLIPS}{SUN_HEADDEFS}{SUN_HEAD}{SUN_TAN}{AUNT_HEAD}{NB_HEAD}{AGENT_HEAD}{UNCLE_HEAD}{ELEC_HEAD}{VENDOR_HEAD}{DIVER_HEAD}{LAE_BACK}{LAE_HEAD}</defs></svg>
<div class="wrap">
  <h1>ตัวละคร EP.01 เกาะเต่า<span>ร่างแรก · หน้าตรง · แสงกลางจากซ้าย · หน้าต่อยอดจากหัวเจมและตะวัน</span></h1>
  <div class="grid">{''.join(cards)}</div>
  <h2>สีผิวซันตอนเป็นชาวเกาะ</h2>
  <div class="pair">{close}</div>
</div>
'''
open(os.path.join(H, 'islanders.html'), 'w').write(page)
print(len(page))
