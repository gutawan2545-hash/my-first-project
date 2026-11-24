# Odd Hours · ตอนงานแต่ง · แผ่นตัวละครเจ้าสาวกับเจ้าบ่าว (ร่างแรก)
# โครงหน้าเจ้าสาวมาจาก characters/tawan.html โครงหน้าเจ้าบ่าวมาจาก characters/james.html
# รัน: python3 wedding_chars.py -> wedding_chars.html
import random, math

def fx(v): return f'{v:.1f}'

# ---------------------------------------------------------------- สี
B_SKIN, B_SKIN_S, B_SKIN_D, B_SKIN_L = '#fbe2cf', '#efc3a8', '#d9a089', '#fff4ea'
B_HAIR, B_HAIR_L = '#2a1c1e', '#4e3a3c'
B_LIP, B_LIP_L = '#cf6f7a', '#eea0a4'
DRESS, DRESS_L, DRESS_S, DRESS_D = '#f5efe7', '#fffdf9', '#ddd3c8', '#c4b8ab'
SILVER, SILVER_L, SILVER_D = '#c3c8cf', '#f4f6f9', '#868d97'

G_SKIN, G_SKIN_S, G_SKIN_D, G_SKIN_L = '#f6dcc8', '#e6bca4', '#c99a84', '#fff0e4'
G_HAIR, G_HAIR_L, G_HAIR_M = '#121118', '#34324a', '#24232f'
G_LIP = '#a8625e'
TUX, TUX_L, TUX_D, TUX_SAT = '#24252e', '#373946', '#15161c', '#2e3040'
SHIRT, SHIRT_S = '#f7f5f1', '#d8d4ce'

def crystals(seed, region_fn, n, y0, y1, dense_top=True):
    """เพชรเม็ดเล็กกระจายบนชุด หนาแน่นที่อกแล้วค่อย ๆ บางลงถึงชายกระโปรง"""
    r = random.Random(seed); o = []
    tries = 0
    while len(o) < n and tries < n * 30:
        tries += 1
        y = r.uniform(y0, y1)
        t = (y - y0) / (y1 - y0)
        if r.random() > (1 - t) ** 1.6 + .03: continue
        x = region_fn(y, r)
        if x is None: continue
        s = r.uniform(.8, 1.7) * (1.15 - t * .4)
        col = r.choice(('#ffffff', '#ffffff', '#e8f0ff', '#f4f6f9', '#dde6f6'))
        o.append(f'<path d="M{fx(x)},{fx(y - s * 1.3)} l{fx(s)},{fx(s * 1.3)} l{fx(-s)},{fx(s * 1.3)} l{fx(-s)},{fx(-s * 1.3)}Z" fill="{col}" opacity="{r.uniform(.7, 1):.2f}"/>')
    return ''.join(o)

def glints(pts):
    o = []
    for x, y, s in pts:
        o.append(f'<g filter="url(#glint)"><path d="M{fx(x)},{fx(y - s * 4)} L{fx(x + s * .7)},{fx(y)} L{fx(x)},{fx(y + s * 4)} L{fx(x - s * .7)},{fx(y)}Z M{fx(x - s * 4)},{fx(y)} L{fx(x)},{fx(y + s * .7)} L{fx(x + s * 4)},{fx(y)} L{fx(x)},{fx(y - s * .7)}Z" fill="#ffffff"/></g>')
    return ''.join(o)

# ---------------------------------------------------------------- หัวเจ้าสาว (โครงจากตะวัน)
BRIDE_HEAD = f'''
  <g id="bback">
    <!-- veil behind -->
    <path d="M -26,-50 C -60,20 -92,180 -104,330 C -60,345 60,345 104,330 C 92,180 60,20 26,-50 Z" fill="#ffffff" opacity=".18"/>
    <path d="M -26,-50 C -60,20 -92,180 -104,330 L -92,333 C -80,190 -52,40 -20,-46 Z" fill="#ffffff" opacity=".22"/>
    <path d="M 26,-50 C 60,20 92,180 104,330 L 96,332 C 84,190 56,40 22,-46 Z" fill="#c9d2e6" opacity=".14"/>
    <!-- bun -->
    <circle cx="0" cy="-60" r="20" fill="{B_HAIR}"/>
    <path d="M -16,-70 C -10,-80 6,-82 14,-72 C 4,-76 -6,-75 -16,-70 Z" fill="{B_HAIR_L}"/>
    <path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 36,30 L -36,30 Z" fill="{B_HAIR}"/>
  </g>
  <g id="bhead">
    <rect x="-8" y="20" width="16" height="38" fill="{B_SKIN_S}"/>
    <path d="M -8,26 L 8,26 L 8,45 Q 0,40 -8,48 Z" fill="{B_SKIN_D}"/>
    <path d="M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,36 0,39 C -13,36 -28,22 -30,6 Z" fill="{B_SKIN}"/>
    <g clip-path="url(#bface)">
      <path d="M 16,-34 C 30,-28 33,-14 31,4 C 29,22 14,36 0,39 C 11,31 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{B_SKIN_S}"/>
      <path d="M 25,-24 L 33,-24 L 33,10 C 31,6 29,0 27,-8 Z" fill="{B_SKIN_D}"/>
      <path d="M -33,-24 L -23,-24 L -26,-8 L -33,-6 Z" fill="#f6d4bc"/>
      <path d="M -32,-12 C -32,-30 -27,-38 -21,-41 C -27,-32 -28,-20 -28,-10 L -27,6 C -26,18 -20,28 -14,34 C -22,30 -28,20 -30,6 Z" fill="{B_SKIN_L}"/>
      <path d="M 2,4 L 6,15 L 1,16.5 Z" fill="#e6ae94"/>
    </g>
    <!-- sweet pink blush -->
    <ellipse cx="-18" cy="12" rx="7" ry="3.8" fill="#f4908e" opacity=".55"/>
    <ellipse cx="18" cy="12" rx="7" ry="3.8" fill="#ea8482" opacity=".55"/>
    <path d="M -22,-13 C -17,-17 -10,-17 -5,-14" fill="none" stroke="#4a2c26" stroke-width="2" stroke-linecap="round"/>
    <path d="M 5,-14 C 10,-17 17,-17 22,-13" fill="none" stroke="#4a2c26" stroke-width="2" stroke-linecap="round"/>
    <path d="M -20,-7 C -16,-10.5 -9,-10.5 -6,-7.5" fill="none" stroke="#dca088" stroke-width="1.1"/>
    <path d="M 20,-7 C 16,-10.5 9,-10.5 6,-7.5" fill="none" stroke="#cf9078" stroke-width="1.1"/>
    <path d="M -21,-1 C -18,-7.5 -8,-7.5 -5,-1 C -8,3 -18,3 -21,-1 Z" fill="#fdf6ee"/>
    <path d="M 21,-1 C 18,-7.5 8,-7.5 5,-1 C 8,3 18,3 21,-1 Z" fill="#f4e9de"/>
    <g clip-path="url(#beyeL)"><circle cx="-13" cy="-0.3" r="5.1" fill="#5a3326"/><circle cx="-13" cy="-0.3" r="2.4" fill="#1e100c"/><circle cx="-14.9" cy="-2.2" r="1.6" fill="#fff"/><circle cx="-11.3" cy="1.5" r=".8" fill="#ffe6cc"/></g>
    <g clip-path="url(#beyeR)"><circle cx="13" cy="-0.3" r="5.1" fill="#5a3326"/><circle cx="13" cy="-0.3" r="2.4" fill="#1e100c"/><circle cx="11.1" cy="-2.2" r="1.6" fill="#fff"/><circle cx="14.7" cy="1.5" r=".8" fill="#ffe6cc"/></g>
    <path d="M -22,0 C -19,-8.5 -8,-8.5 -4,-2 L -5,-1 C -9,-5.6 -17,-5.6 -21,1 Z" fill="#1c1218"/>
    <path d="M -20.5,-1.5 L -26,-5.5 L -24.5,-2.5 L -27,-2 L -21.5,0.5 Z" fill="#1c1218"/>
    <path d="M -17,-5.8 L -19,-9.2 M -13,-6.8 L -14,-10.2 M -9,-6.4 L -9.4,-9.6" stroke="#1c1218" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M 22,0 C 19,-8.5 8,-8.5 4,-2 L 5,-1 C 9,-5.6 17,-5.6 21,1 Z" fill="#1c1218"/>
    <path d="M 20.5,-1.5 L 26,-5.5 L 24.5,-2.5 L 27,-2 L 21.5,0.5 Z" fill="#1c1218"/>
    <path d="M 17,-5.8 L 19,-9.2 M 13,-6.8 L 14,-10.2 M 9,-6.4 L 9.4,-9.6" stroke="#1c1218" stroke-width="1.2" stroke-linecap="round"/>
    <path d="M -19,2.6 C -15,4.2 -10,4.2 -6,2.2" fill="none" stroke="#c58a7a" stroke-width="1"/>
    <path d="M 19,2.6 C 15,4.2 10,4.2 6,2.2" fill="none" stroke="#ba7e6e" stroke-width="1"/>
    <!-- soft sweet smile, rosy lips -->
    <path d="M -6.5,21.6 Q 0,26 6.5,21.6 Q 0,24 -6.5,21.6 Z" fill="{B_LIP}"/>
    <path d="M -6.5,21.6 Q 0,26 6.5,21.6" fill="none" stroke="#b25a66" stroke-width="1.4" stroke-linecap="round"/>
    <path d="M -3.6,25.2 Q 0,27.6 3.6,25.2" fill="none" stroke="{B_LIP_L}" stroke-width="1.8" stroke-linecap="round"/>
    <!-- updo crown with soft side part -->
    <path d="M -38,-4 C -40,-44 -22,-62 0,-62 C 22,-62 40,-44 38,-4 L 31,-6 C 29,-22 18,-33 6,-37 C -8,-32 -24,-22 -31,-6 Z" fill="{B_HAIR}"/>
    <path d="M -31,-38 C -23,-53 -11,-58 -1,-59 C -11,-54 -21,-46 -27,-32 Z" fill="{B_HAIR_L}"/>
    <path d="M 10,-52 C 20,-50 30,-42 33,-30 C 26,-40 18,-46 10,-48 Z" fill="{B_HAIR_L}" opacity=".6"/>
    <!-- face-framing wisps -->
    <path d="M -33,-10 C -36,6 -34,22 -27,34 C -31,20 -31,6 -29,-8 Z" fill="{B_HAIR}"/>
    <path d="M 33,-10 C 36,6 34,22 27,34 C 31,20 31,6 29,-8 Z" fill="{B_HAIR}"/>
    <!-- silver tiara -->
    <path d="M -24,-50 Q 0,-60 24,-50 L 22,-46 Q 0,-55 -22,-46 Z" fill="{SILVER}"/>
    <path d="M -24,-50 Q 0,-60 24,-50" fill="none" stroke="{SILVER_L}" stroke-width=".9"/>
    <path d="M -14,-53 L -12,-60 L -10,-54 Z M -5,-56 L -2.5,-64 L 0,-57 Z M 2.5,-57 L 5,-64 L 7.5,-56 Z M 10,-54 L 12,-60 L 14,-53 Z" fill="{SILVER_L}"/>
    <circle cx="0" cy="-58" r="2.2" fill="#e8f0ff"/>
    <!-- drop earrings -->
    <path d="M -31,10 v6 l-2,4 l2,4 l2,-4 l-2,-4" fill="{SILVER_L}" stroke="{SILVER}" stroke-width=".6"/>
    <path d="M 31,10 v6 l-2,4 l2,4 l2,-4 l-2,-4" fill="{SILVER}" stroke="{SILVER_D}" stroke-width=".6"/>
  </g>'''

# ---------------------------------------------------------------- หัวเจ้าบ่าว (โครงจากเจม)
GROOM_HEAD = f'''
  <g id="ghead">
    <!-- ears -->
    <path d="M -31,-8 C -38,-10 -39,6 -32,10 Z" fill="{G_SKIN_S}"/>
    <path d="M 31,-8 C 38,-10 39,6 32,10 Z" fill="{G_SKIN_D}"/>
    <rect x="-9" y="20" width="18" height="38" fill="{G_SKIN_S}"/>
    <path d="M -9,26 L 9,26 L 9,46 Q 0,41 -9,49 Z" fill="{G_SKIN_D}"/>
    <!-- face: a touch sharper at the jaw than James -->
    <path d="M -32,-14 C -32,-46 32,-46 32,-14 L 31,4 C 29,20 14,36 0,40 C -14,36 -29,20 -31,4 Z" fill="{G_SKIN}"/>
    <g clip-path="url(#gface)">
      <path d="M 16,-34 C 30,-28 34,-14 32,4 C 30,22 14,37 0,40 C 11,32 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{G_SKIN_S}"/>
      <path d="M 26,-24 L 34,-24 L 34,10 C 32,6 30,0 28,-8 Z" fill="{G_SKIN_D}"/>
      <path d="M -34,-24 L -24,-24 L -27,-8 L -34,-6 Z" fill="#f2d0bc"/>
      <path d="M -33,-12 C -33,-30 -28,-38 -22,-41 C -28,-32 -29,-20 -29,-10 L -28,6 C -27,18 -21,28 -15,34 C -23,30 -29,20 -31,6 Z" fill="{G_SKIN_L}"/>
      <path d="M 2,3 L 6.5,15 L 1,17 Z" fill="#dca690"/>
      <!-- cheekbone shadow, makes the face colder -->
      <path d="M 16,9 L 28,6 L 27,13 Z" fill="{G_SKIN_D}" opacity=".22"/>
      
    </g>
    <!-- brows: straight, sharp, inner ends pulled low -->
    <path d="M -23,-14.5 L -7,-11.6 L -7.4,-8.8 L -22,-11.2 Z" fill="#141218"/>
    <path d="M 23,-14.5 L 7,-11.6 L 7.4,-8.8 L 22,-11.2 Z" fill="#141218"/>
    <!-- narrow monolid eyes, half-lidded, upturned outer corners -->
    <path d="M -21,-3.2 C -17,-6 -9,-6 -5,-1.6 C -9,0.6 -17,0.4 -21,-3.2 Z" fill="#f6f0ea"/>
    <path d="M 21,-3.2 C 17,-6 9,-6 5,-1.6 C 9,0.6 17,0.4 21,-3.2 Z" fill="#ebe1d8"/>
    <g clip-path="url(#geyeL)"><circle cx="-12" cy="-1.6" r="3.6" fill="#22161a"/><circle cx="-13" cy="-2.6" r=".8" fill="#fff"/></g>
    <g clip-path="url(#geyeR)"><circle cx="12" cy="-1.6" r="3.6" fill="#22161a"/><circle cx="11" cy="-2.6" r=".8" fill="#fff"/></g>
    <!-- heavy upper lids sit low over the iris -->
    <path d="M -23,-3.6 C -17,-7.6 -9,-7.6 -4,-1.6 L -5,-0.6 C -9,-4 -16,-4.2 -21,-2.2 Z" fill="#141218"/>
    <path d="M 23,-3.6 C 17,-7.6 9,-7.6 4,-1.6 L 5,-0.6 C 9,-4 16,-4.2 21,-2.2 Z" fill="#141218"/>
    <path d="M -21.4,-3 L -25,-5.4 L -21.8,-2 Z M 21.4,-3 L 25,-5.4 L 21.8,-2 Z" fill="#141218"/>
    <path d="M -19,1 C -15,2.6 -10,2.6 -6,1.4" fill="none" stroke="#c99a84" stroke-width="0.9"/>
    <path d="M 19,1 C 15,2.6 10,2.6 6,1.4" fill="none" stroke="#bc8c76" stroke-width="0.9"/>
    <!-- thin closed-mouth smirk, one corner up -->
    <path d="M -6.5,23.6 Q 0,24.6 6,22.2 L 8.2,20.6" fill="none" stroke="{G_LIP}" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M -3.2,26.6 Q 0,27.6 3.2,26.6" fill="none" stroke="{G_SKIN_S}" stroke-width="1.3" stroke-linecap="round"/>
    <!-- neat comma hair, swept to one side, one lock falling on the forehead -->
    <path d="M -35,-6 C -40,-36 -28,-60 0,-63 C 28,-63 40,-44 36,-6 L 32,-20 C 27,-31 17,-36 5,-35 C 13,-31 16,-25 14,-18 C 9,-25 -1,-29 -13,-29 C -21,-28 -28,-22 -32,-14 Z" fill="{G_HAIR}"/>
    <path d="M -27,-46 C -18,-56 -4,-60 8,-58 C -4,-54 -14,-48 -21,-38 Z" fill="{G_HAIR_L}"/>
    <path d="M 5,-35 C 13,-31 16,-25 14,-18 L 11,-22 C 11,-27 8,-31 5,-35 Z" fill="{G_HAIR_M}"/>
    <path d="M 14,-18 C 13,-15 11,-14 9,-14.4 C 11,-15.6 11.6,-17 11,-20 Z" fill="{G_HAIR}"/>
    <path d="M -35,-6 L -33,-24 L -30,-8 Z M 36,-6 L 34,-22 L 32,-8 Z" fill="{G_HAIR}"/>
  </g>'''

def bride_body():
    o = []
    # skirt (ball gown) + train
    o.append(f'<ellipse cx="0" cy="458" rx="128" ry="16" fill="{DRESS_S}"/>')
    sk = 'M -30,150 C -52,200 -96,330 -114,456 Q 0,470 114,456 C 96,330 52,200 30,150 Z'
    o.append(f'<path d="{sk}" fill="{DRESS}"/>')
    o.append(f'<path d="M -30,150 C -52,200 -96,330 -114,456 Q -90,460 -66,462 C -64,340 -40,210 -14,150 Z" fill="{DRESS_L}"/>')
    o.append(f'<path d="M 18,150 C 40,210 64,330 74,462 Q 96,460 114,456 C 96,330 52,200 30,150 Z" fill="{DRESS_S}"/>')
    o.append(f'<path d="M 36,190 C 62,280 84,380 96,458 L 112,456 C 96,340 66,240 40,180 Z" fill="{DRESS_D}" opacity=".7"/>')
    for x0, x1, col in ((-8, 6, DRESS_S), (-40, -30, '#ebe3d8'), (40, 52, DRESS_D)):
        o.append(f'<path d="M {x0 * .3},160 C {x0 * .8},260 {x0 * 1.3},380 {x0 * 1.6},462 L {x1 * 1.6},462 C {x1 * 1.3},380 {x1 * .8},260 {x1 * .3},160 Z" fill="{col}" opacity=".55"/>')
    # lace hem
    hem = ''.join(f'<path d="M {x},{460 - abs(x) * .03} q 5,7 10,0" fill="none" stroke="#ffffff" stroke-width="1.6"/>' for x in range(-112, 112, 10))
    o.append(hem)
    # skin: shoulders and upper chest
    o.append(f'<path d="M -10,50 L 10,50 C 22,51 34,55 39,64 L 37,96 L -37,96 L -39,64 C -34,55 -22,51 -10,50 Z" fill="{B_SKIN}"/>')
    o.append(f'<path d="M 18,52 C 30,55 37,58 39,64 L 37,96 L 24,96 C 25,80 23,64 18,52 Z" fill="{B_SKIN_S}"/>')
    o.append(f'<path d="M -6,66 L 6,66 L 4,80 L -4,80 Z" fill="{B_SKIN_S}" opacity=".5"/>')
    # arms
    o.append(f'<path d="M -38,60 C -46,64 -49,80 -49,100 L -51,212 L -40,212 L -38,110 Z" fill="{B_SKIN}"/>')
    o.append(f'<path d="M -46,92 C -47,100 -48,110 -48,120 L -49,212 L -46,212 L -45,120 Z" fill="{B_SKIN_L}"/>')
    o.append(f'<path d="M 38,60 C 46,64 49,80 49,100 L 51,212 L 40,212 L 38,110 Z" fill="{B_SKIN_S}"/>')
    o.append(f'<path d="M 46,92 C 48,100 49,110 49,120 L 51,212 L 47,212 Z" fill="{B_SKIN_D}"/>')
    o.append(f'<path d="M -51,210 L -40,210 C -39,224 -41,236 -46,238 C -51,238 -53,226 -51,210 Z" fill="{B_SKIN}"/>')
    o.append(f'<path d="M 51,210 L 40,210 C 39,224 41,236 46,238 C 51,238 53,226 51,210 Z" fill="{B_SKIN_S}"/>')
    # silver ring on her left hand (viewer's right)
    o.append(f'<rect x="41.5" y="224" width="7" height="2.6" rx="1.2" fill="{SILVER_L}"/><circle cx="45" cy="223.4" r="1.6" fill="#e8f0ff"/>')
    # strapless sweetheart bodice
    bod = 'M -36,84 C -32,72 -16,70 -6,79 Q 0,84 6,79 C 16,70 32,72 36,84 L 31,152 L -31,152 Z'
    o.append(f'<path d="{bod}" fill="{DRESS}"/>')
    o.append(f'<path d="M -36,84 C -32,72 -16,70 -6,79 L -10,152 L -31,152 Z" fill="{DRESS_L}"/>')
    o.append(f'<path d="M 14,74 C 24,72 33,76 36,84 L 31,152 L 20,152 C 22,120 20,92 14,74 Z" fill="{DRESS_S}"/>')
    o.append(f'<path d="M -2,84 L 0,152 M -20,80 C -18,110 -16,130 -16,152 M 20,80 C 18,110 16,130 16,152" fill="none" stroke="{DRESS_S}" stroke-width="1" opacity=".7"/>')
    o.append(f'<path d="M -36,84 C -32,72 -16,70 -6,79 Q 0,84 6,79 C 16,70 32,72 36,84" fill="none" stroke="#ffffff" stroke-width="1.8"/>')
    # crystal waist band
    o.append(f'<path d="M -31,147 L 31,147 L 31,155 L -31,155 Z" fill="{SILVER}"/><path d="M -31,147 L 31,147 L 31,149.5 L -31,149.5 Z" fill="{SILVER_L}"/>')
    o.append(''.join(f'<circle cx="{x}" cy="151.2" r="1.7" fill="#ffffff"/>' for x in range(-28, 30, 5)))
    # crystals: dense on bodice, fading down the skirt
    def bodice_x(y, r):
        if y < 80: return None
        hw = 33 - (y - 84) * .04
        return r.uniform(-hw, hw)
    def skirt_x(y, r):
        t = (y - 156) / 300
        hw = 30 + t * 82
        return r.uniform(-hw, hw)
    o.append(crystals(3, bodice_x, 230, 78, 152))
    o.append(crystals(4, skirt_x, 300, 156, 456))
    o.append(glints([(-18, 96, 1.1), (12, 108, .9), (-4, 128, 1.2), (24, 118, .8), (-26, 176, .9), (16, 206, .8), (-40, 250, .7)]))
    # necklace
    o.append(f'<path d="M -12,53 Q 0,70 12,53" fill="none" stroke="{SILVER}" stroke-width=".9"/><path d="M 0,61.5 l 2,3 l -2,4 l -2,-4 Z" fill="{SILVER_L}"/>')
    return ''.join(o)

def groom_body():
    o = []
    # trousers
    o.append(f'<path d="M -40,226 L 40,226 L 43,300 L 37,470 L 9,470 L 2,292 L -2,292 L -9,470 L -37,470 L -43,300 Z" fill="{TUX}"/>')
    o.append(f'<path d="M -40,226 L -24,226 L -27,300 L -25,470 L -37,470 L -43,300 Z" fill="{TUX_L}"/>')
    o.append(f'<path d="M 22,232 L 40,226 L 43,300 L 37,470 L 26,470 C 28,380 26,300 22,232 Z" fill="{TUX_D}"/>')
    o.append(f'<path d="M -23,240 L -23,470 M 23,240 L 23,470" stroke="{TUX_SAT}" stroke-width="2"/>')
    # oxford shoes
    o.append(f'<path d="M -40,468 L -8,468 C -4,476 -6,486 -10,488 L -44,488 C -48,484 -46,472 -40,468 Z" fill="#16161c"/>')
    o.append(f'<path d="M -36,470 L -18,470 C -16,474 -20,476 -26,476 L -36,476 Z" fill="#3e3e4c"/>')
    o.append(f'<path d="M 40,468 L 8,468 C 4,476 6,486 10,488 L 44,488 C 48,484 46,472 40,468 Z" fill="#0f0f14"/>')
    o.append(f'<path d="M 18,470 L 30,470 C 30,474 28,476 22,476 Z" fill="#2c2c38"/>')
    # sleeves + hands
    o.append(f'<path d="M -50,68 C -58,76 -60,100 -60,120 L -58,226 L -44,226 L -44,118 Z" fill="{TUX_L}"/>')
    o.append(f'<path d="M -58,96 C -59,110 -59,130 -58,226 L -54,226 L -54,120 Z" fill="#454856"/>')
    o.append(f'<path d="M 50,68 C 58,76 60,100 60,120 L 58,226 L 44,226 L 44,118 Z" fill="{TUX_D}"/>')
    o.append(f'<rect x="-59" y="222" width="15" height="7" fill="{SHIRT}"/><rect x="44" y="222" width="15" height="7" fill="{SHIRT_S}"/>')
    o.append(f'<circle cx="-51.5" cy="225.5" r="1.4" fill="{SILVER}"/><circle cx="51.5" cy="225.5" r="1.4" fill="{SILVER_D}"/>')
    o.append(f'<path d="M -59,229 L -44,229 C -43,244 -45,258 -51,260 C -57,260 -60,246 -59,229 Z" fill="{G_SKIN}"/>')
    o.append(f'<path d="M 59,229 L 44,229 C 43,244 45,258 51,260 C 57,260 60,246 59,229 Z" fill="{G_SKIN_S}"/>')
    # silver ring on his left hand (viewer's right)
    o.append(f'<rect x="45.5" y="246" width="7" height="2.6" rx="1.2" fill="{SILVER_L}"/>')
    # jacket body
    jk = 'M -12,49 L 12,49 C 30,51 46,56 50,68 L 50,236 L -50,236 L -50,68 C -46,56 -30,51 -12,49 Z'
    o.append(f'<path d="{jk}" fill="{TUX}"/>')
    o.append(f'<path d="M -50,68 C -46,56 -30,51 -18,50 C -26,80 -30,130 -30,236 L -50,236 Z" fill="{TUX_L}"/>')
    o.append(f'<path d="M 22,50 C 34,53 46,58 50,68 L 50,236 L 32,236 C 32,160 30,90 22,50 Z" fill="{TUX_D}"/>')
    # shirt + tie in the V
    o.append(f'<path d="M -12,49 L 12,49 L 0,148 Z" fill="{SHIRT}"/>')
    o.append(f'<path d="M 4,52 L 12,49 L 0,148 Z" fill="{SHIRT_S}"/>')
    o.append(f'<path d="M -4,58 L 4,58 L 6,66 L 3,138 L 0,144 L -3,138 L -6,66 Z" fill="{SILVER}"/>')
    o.append(f'<path d="M 0,58 L 4,58 L 6,66 L 3,138 L 0,144 Z" fill="{SILVER_D}"/>')
    o.append(f'<path d="M -4,56 L 4,56 L 5,62 L -5,62 Z" fill="{SILVER_L}"/>')
    # satin lapels with silver piping
    o.append(f'<path d="M -12,49 L 0,148 L -6,150 L -26,96 L -18,90 L -24,62 Z" fill="{TUX_SAT}"/>')
    o.append(f'<path d="M 12,49 L 0,148 L 6,150 L 26,96 L 18,90 L 24,62 Z" fill="#1d1e26"/>')
    o.append(f'<path d="M -12,49 L -24,62 L -18,90 L -26,96 L -6,150 M 12,49 L 24,62 L 18,90 L 26,96 L 6,150" fill="none" stroke="{SILVER}" stroke-width="1"/>')
    # buttons + pocket square
    o.append(f'<circle cx="0" cy="166" r="2.4" fill="#0e0e12"/><circle cx="0" cy="188" r="2.4" fill="#0e0e12"/>')
    o.append(f'<path d="M -40,106 L -26,106 L -26,109 L -40,109 Z" fill="#0e0e12"/><path d="M -38,106 L -35,100 L -32,104 L -29,99 L -27,106 Z" fill="{SILVER_L}"/>')
    # dark red rose boutonniere on his left lapel (viewer's right)
    o.append(f'<path d="M 22,102 l 6,10" stroke="#3e5638" stroke-width="1.6"/><path d="M 24,104 q 5,-1 6,4 q -4,1 -6,-4 Z" fill="#4e6a46"/>')
    o.append(f'<circle cx="21" cy="99" r="5.2" fill="#6e1a26"/><path d="M 16,99 A5.2,5.2 0 0 1 21,93.8 A4.4,4.4 0 0 0 16,99 Z" fill="#9a2e3a"/><path d="M 18,100 A3,3 0 1 1 23.6,100.6" fill="none" stroke="#3e0c14" stroke-width="1"/>')
    return ''.join(o)

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <clipPath id="bface"><path d="M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,36 0,39 C -13,36 -28,22 -30,6 Z"/></clipPath>
  <clipPath id="beyeL"><path d="M -21,-1 C -18,-7.5 -8,-7.5 -5,-1 C -8,3 -18,3 -21,-1 Z"/></clipPath>
  <clipPath id="beyeR"><path d="M 21,-1 C 18,-7.5 8,-7.5 5,-1 C 8,3 18,3 21,-1 Z"/></clipPath>
  <clipPath id="gface"><path d="M -32,-14 C -32,-46 32,-46 32,-14 L 31,4 C 29,20 14,36 0,40 C -14,36 -29,20 -31,4 Z"/></clipPath>
  <clipPath id="geyeL"><path d="M -21,-3.2 C -17,-6 -9,-6 -5,-1.6 C -9,0.6 -17,0.4 -21,-3.2 Z"/></clipPath>
  <clipPath id="geyeR"><path d="M 21,-3.2 C 17,-6 9,-6 5,-1.6 C 9,0.6 17,0.4 21,-3.2 Z"/></clipPath>
  <filter id="glint" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation=".5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  {BRIDE_HEAD}
  {GROOM_HEAD}
</defs></svg>'''

CSS = '''<title>เจ้าสาวกับเจ้าบ่าว</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one row per character (full body + face close-up), stacking on phones. Single dark look by choice, same as the channel's character sheets. */
:root{--stage:#0d0f14;--ink:#d4d6e0;--muted:#80849a;--line:#2a2e3a;--font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif;color-scheme:dark}
html,body{background:var(--stage);color:var(--ink)}
body{font-family:var(--font);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:24px 32px}
.wrap{max-width:980px;margin:0 auto;display:grid;gap:28px}
h1{font-size:18px;font-weight:500;margin:0}
h1 span{color:var(--muted);font-weight:400;margin-left:8px;font-size:14px}
section{display:grid;gap:12px}
.panels{display:grid;grid-template-columns:4fr 5fr;gap:16px;align-items:start}
@media (max-width:640px){.panels{grid-template-columns:1fr}}
figure{margin:0;min-width:0;display:grid;gap:8px}
figure svg{display:block;width:100%;height:auto;border-radius:6px;box-shadow:0 0 0 1px var(--line)}
figcaption{font-size:13px;color:var(--muted);line-height:1.6}
.chips{display:flex;flex-wrap:wrap;gap:10px 16px;font-size:12px;color:var(--muted)}
.chips span{display:inline-flex;align-items:center;gap:6px}
.chips i{width:14px;height:14px;border-radius:3px;display:inline-block;box-shadow:0 0 0 1px var(--line)}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">'''

def chips(items): return '<div class="chips">' + ''.join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in items) + '</div>'

def build():
    bride_full = f'''<svg viewBox="0 0 400 900" role="img" aria-label="เจ้าสาวเต็มตัว หน้าตรง ชุดเกาะอกประดับเพชร">
<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="790" rx="170" ry="16" fill="#10131b"/>
<g transform="translate(200,138) scale(1.4)"><use href="#bback"/>{bride_body()}<use href="#bhead"/></g></svg>'''
    bride_face = f'''<svg viewBox="-75 -84 150 156" role="img" aria-label="ใบหน้าเจ้าสาวระยะใกล้">
<rect x="-75" y="-84" width="150" height="156" fill="#1b1f2b"/><use href="#bback"/>
<path d="M -50,72 C -48,58 -30,51 -14,50 L 14,50 C 30,51 48,58 50,72 Z" fill="{B_SKIN}"/><path d="M 20,51 C 36,54 48,60 50,72 L 30,72 C 30,64 28,56 20,51 Z" fill="{B_SKIN_S}"/>
<path d="M -12,53 Q 0,70 12,53" fill="none" stroke="{SILVER}" stroke-width=".9"/><path d="M 0,61.5 l 2,3 l -2,4 l -2,-4 Z" fill="{SILVER_L}"/>
<use href="#bhead"/></svg>'''
    groom_full = f'''<svg viewBox="0 0 400 900" role="img" aria-label="เจ้าบ่าวเต็มตัว หน้าตรง ทักซิโด้สีดำ">
<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="815" rx="80" ry="10" fill="#10131b"/>
<g transform="translate(200,130) scale(1.4)">{groom_body()}<use href="#ghead"/>
<path d="M -12,49 C -8,59 8,59 12,49" fill="none" stroke="{SHIRT_S}" stroke-width="2"/></g></svg>'''
    groom_face = f'''<svg viewBox="-75 -84 150 156" role="img" aria-label="ใบหน้าเจ้าบ่าวระยะใกล้">
<rect x="-75" y="-84" width="150" height="156" fill="#1b1f2b"/>
<path d="M -56,72 C -54,58 -34,51 -12,49 L 12,49 C 34,51 54,58 56,72 Z" fill="{TUX}"/><path d="M -12,49 L 12,49 L 0,72 Z" fill="{SHIRT}"/>
<path d="M -4,58 L 4,58 L 5,72 L -5,72 Z" fill="{SILVER}"/><path d="M -4,56 L 4,56 L 5,62 L -5,62 Z" fill="{SILVER_L}"/>
<path d="M -12,49 L -2,72 L -14,72 L -24,62 Z" fill="{TUX_SAT}"/><path d="M 12,49 L 2,72 L 14,72 L 24,62 Z" fill="#1d1e26"/>
<use href="#ghead"/></svg>'''
    page = CSS + DEFS + f'''<div class="wrap">
<section><h1>เจ้าสาว<span>ร่างแรก · หน้าตรง · แสงกลางจากซ้าย</span></h1>
<div class="panels"><figure>{bride_full}<figcaption>เต็มตัว · ชุดเกาะอกทรงหัวใจ ประดับเพชรหนาแน่นที่อกแล้วค่อย ๆ บางลงถึงชายกระโปรงยาวทรงบอลกาวน์ เข็มขัดเพชรเส้นเล็ก ผ้าคลุมโปร่งด้านหลัง แหวนเงินที่มือซ้าย</figcaption></figure>
<figure>{bride_face}<figcaption>ใบหน้าระยะใกล้ · หน้าหวาน ตาสองชั้นกลมโต ขนตางอน ประกายในตาสองจุด แก้มชมพู ปากชมพูกุหลาบ ผิวขาวอมพีชแต่ไม่ขาวจัด ผมเกล้ามวยมีปอยข้างหน้า มงกุฎเงินกับต่างหูระย้า</figcaption>
{chips([(B_SKIN, 'ผิว'), (B_SKIN_S, 'ผิวเงา'), (B_HAIR, 'ผม'), (DRESS, 'ชุด'), (SILVER, 'เงิน'), (B_LIP, 'ปาก')])}</figure></div></section>
<section><h1>เจ้าบ่าว<span>ร่างแรก · หน้าตรง · แสงกลางจากซ้าย</span></h1>
<div class="panels"><figure>{groom_full}<figcaption>เต็มตัว · สูงกว่าเจ้าสาวราวหนึ่งในสี่หัว ไหล่กว้าง ทักซิโด้ดำปกซาตินขอบเงิน เน็คไทเงิน กุหลาบแดงเลือดหมูที่ปกเสื้อ ผ้าเช็ดหน้าเงิน แหวนเงินที่มือซ้าย</figcaption></figure>
<figure>{groom_face}<figcaption>ใบหน้าระยะใกล้ · หล่อแนวตี๋ ผิวขาวอมพีชนิด ๆ ตาชั้นเดียวเรียวยาว หางตาเชิด เปลือกตาบนหนักปิดตาดำครึ่งหนึ่ง ตาดำเล็ก คิ้วตรงคม หัวคิ้วกดต่ำ ยิ้มมุมปากข้างเดียวแบบปิดปาก ผมดำปัดข้างมีปอยตกหน้าผาก ดูสุภาพแต่ร้ายเงียบ ๆ</figcaption>
{chips([(G_SKIN, 'ผิว'), (G_SKIN_S, 'ผิวเงา'), (G_HAIR, 'ผม'), (TUX, 'ทักซิโด้'), (SILVER, 'เงิน'), ('#6e1a26', 'กุหลาบ')])}</figure></div></section>
</div>'''
    open('wedding_chars.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
