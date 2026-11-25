# Odd Hours · ตอนงานแต่ง · เจ้าสาว รอบ 2
# ทรงหน้าแบบเดิม + ไฝใต้ตา + ผมยาวตรงสีน้ำตาลเข้ม + ขนตาพอประมาณ + ทรงปากสวยขึ้น
# ต่างจากตะวัน: ผมน้ำตาลเข้มเงา คิ้วตรงนุ่ม ตาเรียวยาวขึ้น มีไฝ
# รัน: python3 bride_v2.py -> bride_v2.html
from wedding_chars import (B_SKIN, B_SKIN_S, B_SKIN_D, B_SKIN_L, SILVER, SILVER_L, SILVER_D, DRESS, DRESS_L, bride_body, crystals, CSS)

H, H_L, H_D, H_SHINE = '#141017', '#2e2834', '#0b090d', '#4a4458'
LASH = '#1e1210'
FACE = 'M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,37 0,40 C -13,37 -28,22 -30,6 Z'
EYE_L = 'M -21.6,-1.8 C -18.2,-7.8 -8.6,-8 -4.8,-1.4 C -8.6,2.2 -17.6,2.4 -21.6,-1.8 Z'
EYE_R = 'M 21.6,-1.8 C 18.2,-7.8 8.6,-8 4.8,-1.4 C 8.6,2.2 17.6,2.4 21.6,-1.8 Z'

HEAD = f'''
<g id="b2back">
  <path d="M -26,-50 C -60,20 -92,180 -104,330 C -60,345 60,345 104,330 C 92,180 60,20 26,-50 Z" fill="#ffffff" opacity=".16"/>
  <path d="M -26,-50 C -60,20 -92,180 -104,330 L -92,333 C -80,190 -52,40 -20,-46 Z" fill="#ffffff" opacity=".2"/>
  <!-- long straight hair behind the shoulders, down to the waist -->
  <path d="M -38,-6 C -40,-44 -22,-63 0,-63 C 22,-63 40,-44 38,-6 L 46,150 L 34,158 L 22,152 L 12,158 L 0,152 L -12,158 L -22,152 L -34,158 L -46,150 Z" fill="{H}"/>
  <path d="M -38,-6 L -46,150 L -40,154 L -33,0 Z" fill="{H_L}"/>
  <path d="M 38,-6 L 46,150 L 40,154 L 34,0 Z" fill="{H_D}"/>
</g>
<g id="b2head">
  <rect x="-8" y="20" width="16" height="38" fill="{B_SKIN_S}"/>
  <path d="M -8,26 L 8,26 L 8,45 Q 0,40 -8,48 Z" fill="{B_SKIN_D}"/>
  <path d="{FACE}" fill="{B_SKIN}"/>
  <g clip-path="url(#b2face)">
    <path d="M 16,-34 C 30,-28 33,-14 31,4 C 29,22 14,37 0,40 C 11,31 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{B_SKIN_S}"/>
    <path d="M 25,-24 L 33,-24 L 33,10 C 31,6 29,0 27,-8 Z" fill="{B_SKIN_D}"/>
    <path d="M -33,-24 L -23,-24 L -26,-8 L -33,-6 Z" fill="#f6d4bc"/>
    <path d="M -32,-12 C -32,-30 -27,-38 -21,-41 C -27,-32 -28,-20 -28,-10 L -27,6 C -26,18 -20,28 -14,34 C -22,30 -28,20 -30,6 Z" fill="{B_SKIN_L}"/>
    <path d="M 2,4 L 5.6,15.4 L 1,16.6 Z" fill="#e6ae94"/>
  </g>
  <ellipse cx="-18" cy="12.4" rx="6.6" ry="3.2" fill="#f2908e" opacity=".45"/>
  <ellipse cx="18" cy="12.4" rx="6.6" ry="3.2" fill="#e8847f" opacity=".45"/>
  <!-- soft straight brows -->
  <path d="M -22.6,-12.6 C -17,-14.6 -10.6,-14.6 -5.4,-12.8 L -5.8,-10.8 C -10.6,-12.4 -16.6,-12.4 -22,-10.6 Z" fill="{H}"/>
  <path d="M 22.6,-12.6 C 17,-14.6 10.6,-14.6 5.4,-12.8 L 5.8,-10.8 C 10.6,-12.4 16.6,-12.4 22,-10.6 Z" fill="{H}"/>
  <path d="M -21.4,-3 C -18,-9.6 -8.6,-9.8 -4.6,-2.4 C -8.6,-8 -17.6,-8 -21.4,-3 Z" fill="#e2a294" opacity=".55"/>
  <path d="M 21.4,-3 C 18,-9.6 8.6,-9.8 4.6,-2.4 C 8.6,-8 17.6,-8 21.4,-3 Z" fill="#d89688" opacity=".55"/>
  <!-- double lid crease -->
  <path d="M -20.6,-6.6 C -16,-10 -9.6,-10.2 -6,-7.2" fill="none" stroke="#d8a088" stroke-width="1"/>
  <path d="M 20.6,-6.6 C 16,-10 9.6,-10.2 6,-7.2" fill="none" stroke="#cc9480" stroke-width="1"/>
  <!-- eyes: a little longer than Tawan's, soft -->
  <path d="{EYE_L}" fill="#fdf6ee"/><path d="{EYE_R}" fill="#f4e9de"/>
  <g clip-path="url(#b2eyeL)"><circle cx="-13" cy="-1.2" r="4.7" fill="#5a3426"/><path d="M -17.7,-1.2 A4.7,4.7 0 0,1 -8.3,-1.2 Z" fill="#2e1812"/><circle cx="-13" cy="-1.2" r="2.1" fill="#120808"/><circle cx="-14.7" cy="-3" r="1.5" fill="#fff"/><circle cx="-11.2" cy=".9" r=".8" fill="#ffe6cc"/><circle cx="-11.6" cy="-3.6" r=".45" fill="#fff"/></g>
  <g clip-path="url(#b2eyeR)"><circle cx="13" cy="-1.2" r="4.7" fill="#5a3426"/><path d="M 8.3,-1.2 A4.7,4.7 0 0,1 17.7,-1.2 Z" fill="#2e1812"/><circle cx="13" cy="-1.2" r="2.1" fill="#120808"/><circle cx="11.3" cy="-3" r="1.5" fill="#fff"/><circle cx="14.8" cy=".9" r=".8" fill="#ffe6cc"/><circle cx="14.4" cy="-3.6" r=".45" fill="#fff"/></g>
  <!-- upper lash line with a small wing, just a few lashes -->
  <path d="M -22.8,-1.6 C -18.8,-9.2 -8.5,-9.4 -3.9,-1.6 L -4.9,-.7 C -9,-6.4 -17.7,-6.2 -21.4,-.5 Z" fill="{LASH}"/>
  <path d="M -21.8,-1.4 L -28,-5.8 L -26.2,-2.6 L -22.2,.2 Z" fill="{LASH}"/>
  <path d="M -19.2,-4.8 L -21.2,-7.4 M -15.4,-6.6 L -16.4,-9.4 M -11.4,-7 L -11.8,-9.8" stroke="{LASH}" stroke-width="1.1" stroke-linecap="round"/>
  <path d="M 22.8,-1.6 C 18.8,-9.2 8.5,-9.4 3.9,-1.6 L 4.9,-.7 C 9,-6.4 17.7,-6.2 21.4,-.5 Z" fill="{LASH}"/>
  <path d="M 21.8,-1.4 L 28,-5.8 L 26.2,-2.6 L 22.2,.2 Z" fill="{LASH}"/>
  <path d="M 19.2,-4.8 L 21.2,-7.4 M 15.4,-6.6 L 16.4,-9.4 M 11.4,-7 L 11.8,-9.8" stroke="{LASH}" stroke-width="1.1" stroke-linecap="round"/>
  <path d="M -19.4,2.4 C -15,4.2 -10,4.2 -6,2.2" fill="none" stroke="#c48a7a" stroke-width=".9"/>
  <path d="M 19.4,2.4 C 15,4.2 10,4.2 6,2.2" fill="none" stroke="#b87e6e" stroke-width=".9"/>
  <!-- beauty mark under her left eye -->
  <circle cx="15.8" cy="6.4" r="1" fill="#4a2c24"/>
  <!-- lips: small and soft, lifted corners, glossy lower lip -->
  <path d="M -5.8,22.4 C -3.8,20.8 -1.6,20.4 0,21.4 C 1.6,20.4 3.8,20.8 5.8,22.4 Q 0,23.2 -5.8,22.4 Z" fill="#c25c6a"/>
  <path d="M -5.8,22.4 Q 0,23.2 5.8,22.4 C 4.8,25.8 2.4,26.8 0,26.8 C -2.4,26.8 -4.8,25.8 -5.8,22.4 Z" fill="#d97884"/>
  <path d="M -5.8,22.4 Q 0,23.4 5.8,22.4" fill="none" stroke="#9a4052" stroke-width=".8"/>
  <path d="M -5.8,22.4 l -1,-.8 M 5.8,22.4 l 1,-.8" stroke="#b25a66" stroke-width=".8" stroke-linecap="round"/>
  <ellipse cx="-1.4" cy="24.6" rx="1.8" ry=".75" fill="#ffffff" opacity=".55"/>
  <!-- crown: soft side part, glossy dark-brown hair -->
  <path d="M -38,-6 C -40,-44 -22,-63 0,-63 C 22,-63 40,-44 38,-6 L 31,-6 C 29,-22 20,-34 8,-38 C -6,-34 -22,-24 -30,-6 Z" fill="{H}"/>
  <path d="M -32,-36 C -24,-52 -12,-58 -2,-59 C -12,-54 -22,-46 -28,-30 Z" fill="{H_SHINE}"/>
  <path d="M 8,-38 C 20,-34 29,-22 31,-6 L 27,-8 C 25,-20 18,-30 8,-38 Z" fill="{H_D}"/>
  <!-- face-framing layers from cheekbone down -->
  <path d="M -30,-6 C -31,10 -29,24 -24,34 C -28,34 -32,30 -34,24 C -34,12 -33,0 -31,-6 Z" fill="{H}"/>
  <path d="M 30,-6 C 31,10 29,24 24,34 C 28,34 32,30 34,24 C 34,12 33,0 31,-6 Z" fill="{H_D}"/>
  <!-- straight front panels over the shoulders, longer than Tawan's -->
  <path d="M -38,-8 L -28,-8 C -26,30 -26,80 -24,140 L -31,148 L -40,140 C -41,80 -40,30 -38,-8 Z" fill="{H}"/>
  <path d="M -36,4 L -33.6,4 C -34,50 -34,100 -33,134 L -35.4,136 C -36,100 -36.4,50 -36,4 Z" fill="{H_SHINE}"/>
  <path d="M 38,-8 L 28,-8 C 26,30 26,80 24,140 L 31,148 L 40,140 C 41,80 40,30 38,-8 Z" fill="{H_D}"/>
  <path d="M 34,4 L 36,4 C 36,50 36.4,100 36,134 L 34,136 C 33.6,100 34,50 34,4 Z" fill="{H}"/>
  <!-- thin silver tiara + drop earrings -->
  <path d="M -24,-50 Q 0,-60 24,-50 L 22,-46.4 Q 0,-55.4 -22,-46.4 Z" fill="{SILVER}"/>
  <path d="M -24,-50 Q 0,-60 24,-50" fill="none" stroke="{SILVER_L}" stroke-width=".9"/>
  <path d="M -12,-53.4 L -10,-59 L -8,-54 Z M -2.4,-55.6 L 0,-63 L 2.4,-55.6 Z M 8,-54 L 10,-59 L 12,-53.4 Z" fill="{SILVER_L}"/>
  <circle cx="0" cy="-58" r="2" fill="#e8f0ff"/>
  <g>
    <circle cx="-29.4" cy="9" r="1.6" fill="{SILVER_L}"/><path d="M -29.4,10.6 V15" stroke="{SILVER}" stroke-width=".8"/>
    <path d="M -29.4,15 l 2.6,4 l -2.6,7 l -2.6,-7 Z" fill="#f4f8ff"/><path d="M -29.4,15 l 2.6,4 l -2.6,7 Z" fill="#c8d4ea"/>
    <circle cx="-30.4" cy="18.6" r=".7" fill="#fff"/>
    <circle cx="29.4" cy="9" r="1.6" fill="{SILVER}"/><path d="M 29.4,10.6 V15" stroke="{SILVER_D}" stroke-width=".8"/>
    <path d="M 29.4,15 l 2.6,4 l -2.6,7 l -2.6,-7 Z" fill="#dde6f6"/><path d="M 29.4,15 l 2.6,4 l -2.6,7 Z" fill="#aebbd4"/>
  </g>
</g>'''

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<clipPath id="b2face"><path d="{FACE}"/></clipPath><clipPath id="b2eyeL"><path d="{EYE_L}"/></clipPath><clipPath id="b2eyeR"><path d="{EYE_R}"/></clipPath>
<filter id="glint" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation=".5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{HEAD}</defs></svg>'''

def build():
    full = f'''<svg viewBox="0 0 400 900" role="img" aria-label="เจ้าสาวเต็มตัว ผมยาวตรงสีดำ ชุดเกาะอกประดับเพชร">
<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="790" rx="170" ry="16" fill="#10131b"/>
<g transform="translate(200,138) scale(1.4)"><use href="#b2back"/>{bride_body()}<use href="#b2head"/></g></svg>'''
    face = f'''<svg viewBox="-75 -84 150 156" role="img" aria-label="ใบหน้าเจ้าสาวระยะใกล้">
<rect x="-75" y="-84" width="150" height="156" fill="#1b1f2b"/><use href="#b2back"/>
<path d="M -50,72 C -48,58 -30,51 -14,50 L 14,50 C 30,51 48,58 50,72 Z" fill="{B_SKIN}"/><path d="M 20,51 C 36,54 48,60 50,72 L 30,72 C 30,64 28,56 20,51 Z" fill="{B_SKIN_S}"/>
<path d="M -12,53 Q 0,70 12,53" fill="none" stroke="{SILVER}" stroke-width=".9"/><path d="M 0,61.5 l 2,3 l -2,4 l -2,-4 Z" fill="{SILVER_L}"/>
<use href="#b2head"/></svg>'''
    chips = ''.join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in ((B_SKIN, 'ผิว'), (B_SKIN_S, 'ผิวเงา'), (H, 'ผมดำ'), (H_SHINE, 'ผมเงา'), ('#d97884', 'ปาก'), (SILVER, 'เงิน')))
    page = CSS.replace('<title>เจ้าสาวกับเจ้าบ่าว</title>', '<title>เจ้าสาว รอบ 2</title>') + DEFS + f'''<div class="wrap"><section><h1>เจ้าสาว รอบ 2<span>ทรงหน้าแบบเดิม · ผมยาวตรงสีดำ · มีไฝใต้ตา · ต่างหูเพชร</span></h1>
<div class="panels"><figure>{full}<figcaption>เต็มตัว · ผมยาวตรงถึงเอว ปล่อยด้านหน้าลงบนไหล่สองข้าง ผ้าคลุมกับมงกุฎเงินเส้นบาง ชุดเกาะอกประดับเพชรแบบเดิม</figcaption></figure>
<figure>{face}<figcaption>ใบหน้าระยะใกล้ · ทรงหน้าแบบเดิม ตาขนาดพอดี คม ตาดำไล่สองโทนมีประกายสามจุด อายแชโดว์ชมพูน้ำตาลบาง ๆ อายไลเนอร์หางยาวขึ้น ขนตาสามเส้นต่อข้าง คิ้วตรงนุ่ม ไฝใต้ตา ปากเล็กอิ่ม มุมปากยกนิด ๆ ปากล่างฉ่ำ ต่างหูเพชรหยดน้ำ ผมดำมีเงาประกาย</figcaption>
<div class="chips">{chips}</div></figure></div></section></div>'''
    open('bride_v2.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
