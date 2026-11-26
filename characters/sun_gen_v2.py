# Generates characters/sun.html. Face construction follows characters/james.html.
SK, SKS, SKD, SKH = "#efc4a0", "#dba882", "#c08a64", "#f8d8ba"
HAIR, HAIRM, HAIRH = "#17141a", "#2a2530", "#3d3646"
MOUTH = "#8c4f45"

def eyes(look=0, lid=-6.0, lidR=None):
    lidR = lid if lidR is None else lidR
    out = []
    for s, l, white, sh in ((-1, lid, "#f8f1ea", SKS), (1, lidR, "#eee3d8", SKD)):
        cid = "eyeL" if s < 0 else "eyeR"
        cx = 13*s + look
        out.append(f'<path d="M {22*s},-4.6 C {17*s},-8.4 {9*s},-8 {5*s},-2 C {9*s},0.8 {17*s},0.6 {22*s},-4.6 Z" fill="{white}"/>')
        out.append(f'<g clip-path="url(#{cid})"><circle cx="{cx}" cy="-2.6" r="4.4" fill="#2b1c17"/>'
                   f'<circle cx="{cx}" cy="-2.6" r="2.2" fill="#120c0a"/>'
                   f'<circle cx="{cx-1.6}" cy="-4" r="1.2" fill="#fff"/><circle cx="{cx+1.6}" cy="-0.8" r="0.6" fill="#fff" opacity=".8"/>'
                   f'<path d="M {24*s},-11 L {2*s},-11 L {2*s},{l-0.4} C {9*s},{l-1.6} {17*s},{l-1.8} {24*s},{l-0.6} Z" fill="{sh}"/></g>')
        out.append(f'<path d="M {4*s},{l+3.6} C {9*s},{l-1.4} {17*s},{l-1.8} {23*s},{l-0.2}" fill="none" stroke="#17141a" stroke-width="2.1" stroke-linecap="round"/>')
        out.append(f'<path d="M {21*s},{l-0.6} L {25.5*s},{l-2.6} L {22.6*s},{l+1.6} Z" fill="#17141a"/>')
        out.append(f'<path d="M {6*s},{l-2.4} C {10*s},{l-5.6} {17*s},{l-6} {21*s},{l-4}" fill="none" stroke="{SKD}" stroke-width="0.9" opacity=".8"/>')
        out.append(f'<path d="M {19*s},0.8 C {15*s},2.4 {10*s},2.6 {6*s},1" fill="none" stroke="{sh}" stroke-width="0.9"/>')
    return "\n".join(out)

BROW_FLAT_L = '<path d="M -24,-15 C -18,-16 -11,-15.4 -5.6,-14.4 L -5.8,-10.4 C -11,-11.2 -17,-11.6 -22.8,-11.2 Z" fill="#17141a"/>'
BROW_FLAT_R = '<path d="M 24,-15 C 18,-16 11,-15.4 5.6,-14.4 L 5.8,-10.4 C 11,-11.2 17,-11.6 22.8,-11.2 Z" fill="#17141a"/>'
BROW_UP_R   = '<path d="M 23.6,-19.4 C 18,-21.4 11,-19.6 5.8,-15.4 L 6.4,-11.4 C 11,-14.8 17,-16.2 22.6,-15.2 Z" fill="#17141a"/>'
BROW_WORRY_L= '<path d="M -23,-11.2 L -6.4,-15 L -6,-10.8 L -22.4,-7.6 Z" fill="#17141a"/>'
BROW_WORRY_R= '<path d="M 23,-11.2 L 6.4,-15 L 6,-10.8 L 22.4,-7.6 Z" fill="#17141a"/>'
BROW_LOW_L  = '<path d="M -23.5,-12.2 L -6,-11.6 L -6.4,-7.6 L -22.6,-8.4 Z" fill="#17141a"/>'

MUST = ('<path d="M -1,20.2 C -4.6,19.6 -8,20.2 -10,22 C -6.8,21.4 -3.8,21.3 -1,21.5 Z" fill="#2a2024" opacity=".8"/>'
        '<path d="M 1,20.2 C 4.6,19.6 8,20.2 10,22 C 6.8,21.4 3.8,21.3 1,21.5 Z" fill="#2a2024" opacity=".8"/>'
        '<path d="M -2.4,33 Q 0,34.4 2.4,33 L 1.6,35 Q 0,35.6 -1.6,35 Z" fill="#2a2024" opacity=".35"/>')
LOWLIP = f'<path d="M -4,27.6 Q 0,29 4,27.6" fill="none" stroke="{SKS}" stroke-width="1.4" stroke-linecap="round"/>'
M_FLAT  = f'<path d="M -6.5,24.2 L 6.5,24.2" stroke="{MOUTH}" stroke-width="1.8" stroke-linecap="round"/>'
M_SMIRK = (f'<path d="M -6.5,24.6 C -2,25.6 3,25.2 7,22.6" fill="none" stroke="{MOUTH}" stroke-width="1.8" stroke-linecap="round"/>'
           f'<path d="M 7.6,21.2 C 8.6,22 8.8,23.4 8.2,24.4" fill="none" stroke="{SKS}" stroke-width="1" stroke-linecap="round"/>')
M_SIDE  = f'<path d="M -6,23.8 Q 0,23.8 6.5,25.2" fill="none" stroke="{MOUTH}" stroke-width="1.8" stroke-linecap="round"/>'
M_DRY   = (f'<path d="M -9.5,23 Q 0,26 9.5,23" fill="none" stroke="{MOUTH}" stroke-width="1.8" stroke-linecap="round"/>'
           f'<path d="M -10.5,22 L -11.6,24.6 M 10.5,22 L 11.6,24.6" stroke="{SKD}" stroke-width="1.1" stroke-linecap="round"/>')

SHADES = ('<g><path d="M -25,-9 L -3,-9 L -3.6,-1 C -4,4 -8,6 -13,6 C -19,6 -24,3 -24.6,-2 Z" fill="#141218"/>'
          '<path d="M 25,-9 L 3,-9 L 3.6,-1 C 4,4 8,6 13,6 C 19,6 24,3 24.6,-2 Z" fill="#141218"/>'
          '<path d="M -3,-7 Q 0,-9 3,-7" fill="none" stroke="#141218" stroke-width="2"/>'
          '<path d="M -25,-8 L -33,-6.5 M 25,-8 L 33,-6.5" stroke="#141218" stroke-width="2"/>'
          '<path d="M -21,-7 L -15,-7 L -22,1 Z" fill="#5a6278" opacity=".55"/>'
          '<path d="M 7,-7 L 11,-7 L 5,0 Z" fill="#5a6278" opacity=".35"/></g>')

def head(hid, brows, eye_svg, mouth, extra=""):
    return f'''<g id="{hid}">
    <use href="#sbase"/>
    {brows}
    {eye_svg}
    <ellipse cx="-18" cy="12" rx="6" ry="3.2" fill="#d9846c" opacity=".3"/>
    <ellipse cx="18" cy="12" rx="6" ry="3.2" fill="#c97660" opacity=".3"/>
    {MUST}
    {mouth}
    {LOWLIP}
    {extra}
    <use href="#sfronthair"/>
    <path d="M 30.6,6 C 33,5.4 35.4,6.6 35,9 C 34.6,11 32,11.2 30.8,10 Z" fill="{SKS}"/>
    <circle cx="33" cy="12.4" r="2.3" fill="none" stroke="#d7dbe4" stroke-width="1.1"/>
  </g>'''

BASE = f'''<g id="sbase">
    <!-- back hair, behind ears and face -->
    <path d="M -41,18 C -48,-24 -43,-54 -20,-64 C -6,-70 10,-70 22,-64 C 45,-54 48,-24 41,18 L 37,10 L 34,24 L 29,4 L -29,4 L -34,24 L -37,10 Z" fill="{HAIR}"/>
    <path d="M -20,22 L -28,31 L -14,27 Z M 20,22 L 29,30 L 14,27 Z" fill="{HAIR}"/>
    <!-- neck + under-chin shadow -->
    <rect x="-9.5" y="20" width="19" height="38" fill="#d9a67e"/>
    <path d="M -9.5,26 L 9.5,26 L 9.5,46 Q 0,41 -9.5,49 Z" fill="#c08b64"/>
    <!-- ears -->
    <ellipse cx="-32" cy="1" rx="5.5" ry="8.5" fill="{SKH}"/>
    <ellipse cx="32" cy="1" rx="5.5" ry="8.5" fill="{SKS}"/>
    <path d="M 31,-3 C 34,-1 34,4 31,6" fill="none" stroke="{SKD}" stroke-width="1.2"/>
    <!-- face: a touch squarer jaw than James -->
    <path d="M -31,-14 C -31,-47 31,-47 31,-14 L 30,5 C 28,21 16,34 0,41 C -16,34 -28,21 -30,5 Z" fill="{SK}"/>
    <g clip-path="url(#face)">
      <path d="M 16,-34 C 30,-28 34,-14 32,4 C 30,22 14,37 0,40 C 11,32 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{SKS}"/>
      <path d="M 26,-24 L 34,-24 L 34,10 C 32,6 30,0 28,-8 Z" fill="{SKD}"/>
      <path d="M -34,-24 L -24,-24 L -27,-8 L -34,-6 Z" fill="#dcaa80"/>
      <path d="M 34,-26 L 22,-26 L 25,-6 L 34,-4 Z" fill="{SKD}"/>
      <path d="M -33,-12 C -33,-30 -28,-38 -22,-41 C -28,-32 -29,-20 -29,-10 L -28,6 C -27,18 -21,28 -15,34 C -23,30 -29,20 -31,6 Z" fill="{SKH}"/>
      <path d="M 1.4,-6 L 3.6,-6 L 7.4,13.6 L 2,16.6 Z" fill="{SKS}"/><path d="M -1.6,-5 L 0.2,-5 L -0.6,11 Z" fill="{SKH}"/><path d="M -4.6,15.4 C -3,13.6 -1,15.6 0,16.6 C 2,15.6 4,13.6 6,15.4" fill="none" stroke="{SKD}" stroke-width="1.2" stroke-linecap="round"/>
    </g>
  </g>
  <g id="sfronthair">
    <!-- crown with a centre part -->
    <path d="M -33,-36 C -30,-68 30,-68 33,-36 C 22,-48 10,-52 0,-47 C -10,-52 -22,-48 -33,-36 Z" fill="{HAIR}"/>
    <path d="M -28,-54 C -30,-66 -20,-72 -12,-70 C -8,-76 4,-77 8,-71 C 16,-74 26,-68 26,-56 Z" fill="{HAIR}"/>
    <path d="M -4,-70 C 0,-76 8,-78 12,-75 C 7,-74 3,-72 0,-68 Z" fill="{HAIR}"/>
    <path d="M -22,-60 C -16,-68 -6,-70 2,-68 C -6,-64 -14,-60 -18,-54 Z" fill="{HAIRH}"/>
    <!-- curtain bangs, chunky shaggy ends -->
    <path d="M 0,-50 C -14,-53 -30,-47 -36,-31 C -39,-20 -38,-6 -35,7 L -31,-5 L -28,3 L -26,-14 L -21,-11 L -20,-24 L -13,-21 C -10,-32 -5,-40 0,-45 Z" fill="{HAIR}"/>
    <path d="M 0,-50 C 14,-53 30,-47 36,-31 C 39,-20 38,-6 36,9 L 32,-3 L 29,5 L 27,-13 L 22,-9 L 20,-23 L 14,-19 C 10,-31 5,-40 0,-45 Z" fill="{HAIR}"/>
    <!-- light from the left: a lit band on the left curtain, shade on the right -->
    <path d="M -4,-49 C -16,-50 -27,-44 -32,-32 C -26,-38 -16,-43 -6,-44 Z" fill="{HAIRH}"/>
    <path d="M -33,-26 C -35,-16 -34,-6 -33,2 L -31,-5 C -32,-12 -32,-20 -30,-27 Z" fill="{HAIRM}"/>
    <path d="M 20,-23 L 24,-38 L 22,-9 Z M 29,5 L 33,-20 L 32,-3 Z" fill="#0e0c11"/>
    <!-- messy flyaways on top -->
    <path d="M -8,-36 C -12,-30 -14,-24 -13,-17 L -9,-25 C -8,-30 -6,-34 -3,-38 Z" fill="{HAIR}"/>
    <path d="M -16,-46 C -22,-42 -27,-36 -29,-28 C -24,-34 -19,-39 -13,-42 Z" fill="{HAIRH}"/>
    <path d="M 26,-50 C 32,-54 37,-54 40,-51 C 35,-50 32,-47 30,-44 Z" fill="{HAIR}"/>
    <path d="M -2,-45 L -6,-36 L 1,-44 Z" fill="{HAIR}"/>
  </g>'''

HEADS = "\n  ".join([
    head("s_dead", BROW_FLAT_L+BROW_FLAT_R, eyes(0, -4.8), M_FLAT),
    head("s_side", BROW_LOW_L+BROW_FLAT_R, eyes(4.4, -4.4), M_SIDE),
    head("s_smirk", BROW_FLAT_L+BROW_UP_R, eyes(0, -6.0, -7.4), M_SMIRK),
    head("s_dry", BROW_WORRY_L+BROW_WORRY_R, eyes(0, -4.6), M_DRY),
    head("s_cool", BROW_FLAT_L+BROW_UP_R, "", M_SMIRK, SHADES),
])

BODY = f'''
          <!-- wide-leg charcoal trousers, cropped above the ankle -->
          <path d="M -44,226 L 44,226 L 50,300 L 51,454 L 8,454 L 3,298 L -3,298 L -8,454 L -51,454 L -50,300 Z" fill="#2b2d36"/>
          <path d="M -44,226 L -28,226 L -32,300 L -34,454 L -51,454 L -50,300 Z" fill="#3b3e4b"/>
          <path d="M 24,232 L 44,226 L 50,300 L 51,454 L 36,454 C 36,370 32,300 24,232 Z" fill="#1e2027"/>
          <path d="M -3,298 L 3,298 L 7,350 L -7,350 Z" fill="#1e2027"/>
          <path d="M -12,300 L -10,454 M 14,300 L 18,454" stroke="#24262e" stroke-width="1.4"/>
          <!-- ankles -->
          <rect x="-36" y="452" width="15" height="12" fill="#d9a67e"/>
          <rect x="21" y="452" width="15" height="12" fill="#c08b64"/>
          <!-- off-white canvas sneakers, gum sole -->
          <path d="M -46,462 L -16,462 C -11,468 -8,476 -8,483 L -50,483 C -52,476 -50,466 -46,462 Z" fill="#ece6da"/>
          <path d="M -46,462 L -36,462 L -40,483 L -50,483 C -52,476 -50,466 -46,462 Z" fill="#f8f4ec"/>
          <path d="M -36,465 L -22,465 M -35,470 L -20,470" stroke="#9aa0b0" stroke-width="1.4"/>
          <rect x="-51" y="483" width="44" height="8" rx="2" fill="#a77d5a"/>
          <path d="M 46,462 L 16,462 C 11,468 8,476 8,483 L 50,483 C 52,476 50,466 46,462 Z" fill="#d6cfc2"/>
          <path d="M 46,462 L 38,462 L 44,483 L 50,483 C 52,476 50,466 46,462 Z" fill="#c2bbae"/>
          <path d="M 22,465 L 36,465 M 20,470 L 35,470" stroke="#858b9a" stroke-width="1.4"/>
          <rect x="7" y="483" width="44" height="8" rx="2" fill="#8d6748"/>
          <!-- left forearm + hand, hanging loose -->
          <path d="M -63,136 L -47,142 L -45,230 L -58,232 Z" fill="{SK}"/>
          <path d="M -63,136 L -58,138 L -54,232 L -58,232 Z" fill="{SKH}"/>
          <path d="M -58,230 L -45,229 C -43,244 -45,258 -51,260 C -57,260 -60,246 -58,230 Z" fill="{SK}"/>
          <path d="M -46,234 C -42,238 -42,244 -45,247 L -47,242 Z" fill="{SKS}"/>
          <!-- off-white tee under the open overshirt -->
          <path d="M -16,50 L 16,50 L 18,236 L -18,236 Z" fill="#f2eee6"/>
          <path d="M 6,52 L 16,50 L 18,236 L 9,236 Z" fill="#d9d3c8"/>
          <path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/>
          <!-- oversized sage overshirt, dropped shoulders, boxy -->
          <path d="M -12,50 C -30,52 -44,56 -52,64 L -66,140 L -46,146 L -49,238 L -14,238 L -11,96 Z" fill="#2f5a5e"/>
          <path d="M -52,64 C -46,58 -36,54 -28,52 C -34,80 -36,140 -36,238 L -49,238 L -46,146 L -66,140 Z" fill="#3e7074"/>
          <path d="M 12,50 C 30,52 44,56 52,64 L 66,140 L 46,146 L 49,238 L 14,238 L 11,96 Z" fill="#26494d"/>
          <path d="M 28,52 C 40,55 48,59 52,64 L 66,140 L 46,146 L 49,238 L 34,238 C 36,170 34,100 28,52 Z" fill="#1d3b3f"/>
          <path d="M -64,132 L -46,138 L -46,146 L -66,140 Z" fill="#e9e1d0"/>
          <path d="M 64,132 L 46,138 L 46,146 L 66,140 Z" fill="#d2c9b6"/>
          <path d="M -12,50 C -30,52 -44,56 -52,64 L -64,132 L -46,138 L -49,238 L -14,238 L -11,96 Z M 12,50 C 30,52 44,56 52,64 L 64,132 L 46,138 L 49,238 L 14,238 L 11,96 Z" fill="url(#print)"/>
          <!-- camp collar -->
          <path d="M -12,50 L -24,54 L -15,82 L -9,64 Z" fill="#4b8286"/>
          <path d="M 12,50 L 24,54 L 15,82 L 9,64 Z" fill="#1f3f43"/>
          <!-- chest pocket with sunglasses hooked in it -->
          <rect x="18" y="88" width="20" height="22" rx="1" fill="#24474b"/>
          <path d="M 18,88 L 38,88 L 38,91 L 18,91 Z" fill="#d2c9b6"/>
          <path d="M 19,92 L 27,92 L 26.5,100 C 26,104 20,104 19.5,100 Z M 29,92 L 37,92 L 36.5,100 C 36,104 30,104 29.5,100 Z" fill="#141218"/>
          <path d="M 27,93 Q 28,91.5 29,93" fill="none" stroke="#141218" stroke-width="1.4"/>
          <path d="M 20.5,93.5 L 23,93.5 L 20.5,97 Z" fill="#5a6278" opacity=".6"/>
          <!-- canvas tote on his left shoulder -->
          <path d="M 30,52 L 58,200 M 38,54 L 82,200" stroke="#bfb397" stroke-width="3.2"/>
          <path d="M 50,198 L 88,198 L 92,266 L 48,266 Z" fill="#d8cdb4"/>
          <path d="M 78,198 L 88,198 L 92,266 L 82,266 Z" fill="#bdb196"/>
          <path d="M 50,198 L 88,198 L 88,203 L 50,203 Z" fill="#c4b89c"/>
          <circle cx="66" cy="232" r="7" fill="none" stroke="#2f5a5e" stroke-width="2"/>
          <path d="M 61,236 L 66,229 L 71,236" fill="none" stroke="#2f5a5e" stroke-width="1.6"/>
          <!-- right forearm going into the trouser pocket -->
          <path d="M 47,142 L 64,138 L 47,252 L 34,248 Z" fill="{SKS}"/>
          <path d="M 60,140 L 64,138 L 47,252 L 44,251 Z" fill="{SKD}"/>
          <path d="M 31,246 L 48,243 L 48,256 C 42,254 36,253 31,252 Z" fill="#2b2d36"/>
          <path d="M 32,247 L 48,244" stroke="#1f222b" stroke-width="1.6"/>
          <!-- film camera on a neck strap -->
          <path d="M -9,58 L -22,112 M 9,58 L 4,112" stroke="#2a2024" stroke-width="1.8"/>
          <rect x="-28" y="108" width="38" height="24" rx="3" fill="#202028"/>
          <rect x="-28" y="108" width="38" height="8" rx="2" fill="#b9bcc6"/>
          <rect x="-28" y="108" width="12" height="8" rx="2" fill="#d6d9e1"/>
          <rect x="2" y="104" width="6" height="4" fill="#9a9dab"/>
          <circle cx="-9" cy="122" r="8" fill="#383a46"/>
          <circle cx="-9" cy="122" r="5" fill="#15151c"/>
          <circle cx="-11" cy="120" r="1.6" fill="#8d95b4"/>'''

def chest(fill_l="#2f5a5e"):
    return f'''<path d="M -16,50 L 16,50 L 20,72 L -20,72 Z" fill="#f2eee6"/>
        <path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/>
        <path d="M -54,72 C -52,58 -32,52 -12,50 L -11,72 Z" fill="#3e7074"/>
        <path d="M 54,72 C 52,58 32,52 12,50 L 11,72 Z" fill="#1d3b3f"/>
        <path d="M -12,50 L -24,54 L -18,72 L -9,64 Z" fill="#4b8286"/>
        <path d="M 12,50 L 24,54 L 18,72 L 9,64 Z" fill="#1f3f43"/>
        <path d="M 30,52 L 34,72" stroke="#bfb397" stroke-width="3.2"/>
        <path d="M -9,58 L -13,72 M 9,58 L 8,72" stroke="#2a2024" stroke-width="1.8"/>'''

EXPR = [("s_dead","หน้าตาย","มุกเงียบ ไม่แสดงอารมณ์"),
        ("s_side","เหลือบมอง","มุกรีแอ็กชัน ตามองไปข้าง"),
        ("s_smirk","ยักคิ้ว ยิ้มมุมปาก","หน้าหลัก มั่นใจ มีออร่า"),
        ("s_dry","ยิ้มแห้ง","หลังพลาด รักษาฟอร์ม"),
        ("s_cool","ใส่แว่นกันแดด","ท่าเท่ประจำตัว")]
expr_figs = "\n".join(f'''    <figure>
      <svg viewBox="-50 -74 100 132" role="img" aria-label="ซัน {t}">
        <rect x="-50" y="-74" width="100" height="132" fill="#1b1f2b"/>
        {chest()}
        <use href="#{i}"/>
      </svg>
      <figcaption><b>{t}</b><br>{d}</figcaption>
    </figure>''' for i,t,d in EXPR)

html = f'''<title>Odd Hours ซัน</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: full body + close-up side by side, expression strip below; stacks on phones. Single dark look by choice, matching the other sheets. */
:root {{
  --stage: #0d0f14;
  --ink: #d4d6e0;
  --muted: #80849a;
  --line: #2a2e3a;
  --font: "IBM Plex Sans Thai", "Noto Sans Thai", system-ui, sans-serif;
  color-scheme: dark;
}}
html, body {{ background: var(--stage); color: var(--ink); }}
body {{
  font-family: var(--font);
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 24px 32px;
}}
.wrap {{ max-width: 980px; margin: 0 auto; display: grid; gap: 16px; }}
h1 {{ font-size: 18px; font-weight: 500; margin: 0; }}
h1 span {{ color: var(--muted); font-weight: 400; margin-left: 8px; font-size: 14px; }}
h2 {{ font-size: 15px; font-weight: 500; margin: 8px 0 0; }}
.panels {{ display: grid; grid-template-columns: 4fr 5fr; gap: 16px; align-items: start; }}
.expr {{ display: grid; grid-template-columns: repeat(5, minmax(0,1fr)); gap: 12px; }}
@media (max-width: 640px) {{ .panels {{ grid-template-columns: 1fr; }} .expr {{ grid-template-columns: repeat(2, minmax(0,1fr)); }} }}
figure {{ margin: 0; min-width: 0; display: grid; gap: 8px; align-content: start; }}
figure svg {{ display: block; width: 100%; height: auto; border-radius: 6px; box-shadow: 0 0 0 1px var(--line); }}
figcaption {{ font-size: 13px; color: var(--muted); }}
figcaption b {{ color: var(--ink); font-weight: 500; }}
.chips {{ display: flex; flex-wrap: wrap; gap: 10px 16px; font-size: 12px; color: var(--muted); }}
.chips span {{ display: inline-flex; align-items: center; gap: 6px; }}
.chips i {{ width: 14px; height: 14px; border-radius: 3px; display: inline-block; box-shadow: 0 0 0 1px var(--line); }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">

<!-- shared definitions: Sun's head parts, drawn once; each expression swaps brows, eyes and mouth -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<defs>
  <pattern id="print" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M 3,4 l 2.4,-2 l 2.4,2 l -2.4,2 Z" fill="#e9e1d0" opacity=".55"/><path d="M 11,12 q 2,-2.4 4,0" fill="none" stroke="#e9e1d0" stroke-width="1" opacity=".45"/></pattern>
  <clipPath id="face"><path d="M -31,-14 C -31,-47 31,-47 31,-14 L 30,5 C 28,21 16,34 0,41 C -16,34 -28,21 -30,5 Z"/></clipPath>
  <clipPath id="eyeL"><path d="M -21,-3 C -17,-7.5 -9,-7.5 -5,-2 C -9,1 -17,1 -21,-3 Z"/></clipPath>
  <clipPath id="eyeR"><path d="M 21,-3 C 17,-7.5 9,-7.5 5,-2 C 9,1 17,1 21,-3 Z"/></clipPath>
  {BASE}
  {HEADS}
</defs>
</svg>

<div class="wrap">
  <h1>ซัน<span>27 ปี · Bangkok Native สายอินดี้ · มั่นใจ กวนแบบหน้าตาย · หน้าตรง · แสงกลางจากซ้าย</span></h1>

  <div class="panels">
    <figure>
      <svg viewBox="0 0 400 900" role="img" aria-label="ซันเต็มตัว หน้าตรง มือหนึ่งล้วงกระเป๋า">
        <rect width="400" height="900" fill="#1b1f2b"/>
        <rect y="760" width="400" height="140" fill="#161a24"/>
        <ellipse cx="200" cy="818" rx="84" ry="10" fill="#10131b"/>
        <g transform="translate(200,132) scale(1.4)">
          {BODY}
          <use href="#s_smirk"/>
          <path d="M -9.5,56 L 9.5,56 L 9.5,58 L -9.5,58 Z" fill="#f2eee6"/>
          <path d="M -9,47 C -5,55 5,55 9,47" fill="none" stroke="#cfd3dc" stroke-width="0.9"/>
          <path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/>
          <path d="M -9,58 L -11,66 M 9,58 L 9.6,66" stroke="#2a2024" stroke-width="1.8"/>
        </g>
      </svg>
      <figcaption>เต็มตัว · สูงราว 5.5 หัว · เชิ้ตฮาวายโอเวอร์ไซซ์สีเขียวหัวเป็ดลายเล็ก เปิดหน้า พับแขน ทับเสื้อยืดขาว · กางเกงขากว้างสีดำถ่าน · สร้อยเงินเส้นบาง ต่างหูห่วงเงิน · ผ้าใบขาวพื้นยาง · กระเป๋าผ้า · กล้องฟิล์มคล้องคอ · แว่นกันแดดเกี่ยวกระเป๋าเสื้อ</figcaption>
    </figure>

    <figure>
      <svg viewBox="-75 -78 150 150" role="img" aria-label="ใบหน้าซันระยะใกล้">
        <rect x="-75" y="-78" width="150" height="150" fill="#1b1f2b"/>
        <path d="M -16,50 L 16,50 L 20,72 L -20,72 Z" fill="#f2eee6"/>
        <path d="M -56,72 C -54,58 -32,52 -12,50 L -11,72 Z" fill="#3e7074"/>
        <path d="M 56,72 C 54,58 32,52 12,50 L 11,72 Z" fill="#1d3b3f"/>
        <path d="M -12,50 L -24,54 L -18,72 L -9,64 Z" fill="#4b8286"/>
        <path d="M 12,50 L 24,54 L 18,72 L 9,64 Z" fill="#1f3f43"/>
        <path d="M 30,52 L 34,72 M 38,54 L 43,72" stroke="#bfb397" stroke-width="3.2"/>
        <use href="#s_smirk"/>
        <path d="M -10,50 C -6,58 6,58 10,50" fill="none" stroke="#c9c1b2" stroke-width="2.4"/>
        <path d="M -9,58 L -13,72 M 9,58 L 8,72" stroke="#2a2024" stroke-width="1.8"/>
      </svg>
      <figcaption>ใบหน้าระยะใกล้ · ผมทรงเซอร์แสกกลาง ยอดฟู ปลายผมท้ายทอยดีดออก · คิ้วหนาหางเชิด · ตาคมหางตาเชิด ชั้นตาบาง · หนวดบาง · กรามเรียว · เงาบล็อกที่ขมับ ข้างจมูก แก้มฝั่งไกลแสง ใต้คาง</figcaption>
      <div class="chips">
        <span><i style="background:{SK}"></i>ผิว</span>
        <span><i style="background:{SKS}"></i>ผิวเงา</span>
        <span><i style="background:{HAIR}"></i>ผม</span>
        <span><i style="background:#2f5a5e"></i>เชิ้ตหัวเป็ด</span>
        <span><i style="background:#f2eee6"></i>เสื้อยืด</span>
        <span><i style="background:#2b2d36"></i>กางเกง</span>
        <span><i style="background:#d8cdb4"></i>กระเป๋าผ้า</span>
      </div>
    </figure>
  </div>

  <h2>สีหน้าหลักสำหรับมุก</h2>
  <div class="expr">
{expr_figs}
  </div>
</div>
'''
import os; open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"sun_v2.html"),"w").write(html)
print(len(html))
