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
    fig(stage(SUN_CITY + '<use href="#h_sun"/>' + '<path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/><path d="M -9,58 L -11,66 M 9,58 L 9.6,66" stroke="#2a2024" stroke-width="1.8"/>'),
        'ใช้ตอนย้อนอดีต · ชุดอินดี้เดิมตาม characters/sun.html', 'ซัน · ลุคกรุงเทพ (อดีต)', [('#2f5a5e', 'เชิ้ต'), ('#2b2d36', 'กางเกง')]),
    fig(stage(SUN_ISLAND + '<use href="#h_sun"/>' + neck_after()),
        'ใช้ตอนปัจจุบัน · เสื้อกล้ามสีฟ้าซีดแดด กางเกงขาสั้นลายใบไม้ รองเท้าแตะ ถือหมวกกันน็อกครึ่งใบ แว่นกันแดดเกี่ยวคอเสื้อ สร้อยเงินเส้นเดิม กำไลเชือก',
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
close = (fig('<rect x="-75" y="-78" width="150" height="150" fill="#1b1f2b"/><path d="M -50,72 C -48,58 -30,50 -12,49 L 12,49 C 30,50 48,58 50,72 Z" fill="#86b9c8"/><use href="#h_sun"/>',
             'สีผิวเดิมของเจม (ตามกฎตอนนี้)', 'ผิวเดิม', [], view='-75 -78 150 150')
         + fig('<rect x="-75" y="-78" width="150" height="150" fill="#1b1f2b"/><path d="M -50,72 C -48,58 -30,50 -12,49 L 12,49 C 30,50 48,58 50,72 Z" fill="#86b9c8"/><use href="#h_suntan"/>',
               'ผิวแทนแดดหลังอยู่เกาะสองปี (ต้องให้เจ้าของช่องอนุมัติก่อน เพราะขัดกฎสีผิว)', 'ทางเลือก · ผิวแทนแดด', [], view='-75 -78 150 150'))

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
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>{CLIPS}{SUN_HEADDEFS}{SUN_HEAD}{SUN_TAN}{AUNT_HEAD}{NB_HEAD}{AGENT_HEAD}</defs></svg>
<div class="wrap">
  <h1>ตัวละคร EP.01 เกาะเต่า<span>ร่างแรก · หน้าตรง · แสงกลางจากซ้าย · หน้าต่อยอดจากหัวเจมและตะวัน</span></h1>
  <div class="grid">{''.join(cards)}</div>
  <h2>สีผิวซันตอนเป็นชาวเกาะ</h2>
  <div class="pair">{close}</div>
</div>
'''
open(os.path.join(H, 'islanders.html'), 'w').write(page)
print(len(page))
