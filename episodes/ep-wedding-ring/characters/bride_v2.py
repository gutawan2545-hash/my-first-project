# Odd Hours · ตอนงานแต่ง · เจ้าสาว รอบ 2
# ทรงหน้าแบบเดิม + ไฝใต้ตา + ผมยาวตรงสีน้ำตาลเข้ม + ขนตาพอประมาณ + ทรงปากสวยขึ้น
# ต่างจากตะวัน: ผมน้ำตาลเข้มเงา คิ้วตรงนุ่ม ตาเรียวยาวขึ้น มีไฝ
# รัน: python3 bride_v2.py -> bride_v2.html
from wedding_chars import (B_SKIN, B_SKIN_S, B_SKIN_D, B_SKIN_L, SILVER, SILVER_L, SILVER_D, DRESS, DRESS_L, bride_body, crystals, CSS)

H, H_L, H_D, H_SHINE = '#3a2620', '#5e4034', '#24160f', '#7a5848'
LASH = '#1e1210'
FACE = 'M -31,-14 C -31,-45 31,-45 31,-14 L 30,6 C 28,22 13,37 0,40 C -13,37 -28,22 -30,6 Z'
EYE_L = 'M -21.5,-1.6 C -18,-7.6 -8.6,-7.8 -4.8,-1.4 C -8.6,2.4 -17.6,2.6 -21.5,-1.6 Z'
EYE_R = 'M 21.5,-1.6 C 18,-7.6 8.6,-7.8 4.8,-1.4 C 8.6,2.4 17.6,2.6 21.5,-1.6 Z'

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
  <!-- double lid crease -->
  <path d="M -20.6,-6.6 C -16,-10 -9.6,-10.2 -6,-7.2" fill="none" stroke="#d8a088" stroke-width="1"/>
  <path d="M 20.6,-6.6 C 16,-10 9.6,-10.2 6,-7.2" fill="none" stroke="#cc9480" stroke-width="1"/>
  <!-- eyes: a little longer than Tawan's, soft -->
  <path d="{EYE_L}" fill="#fdf6ee"/><path d="{EYE_R}" fill="#f4e9de"/>
  <g clip-path="url(#b2eyeL)"><circle cx="-13" cy="-.8" r="4.9" fill="#4e2e22"/><circle cx="-13" cy="-.8" r="2.3" fill="#180c0a"/><circle cx="-14.8" cy="-2.6" r="1.5" fill="#fff"/><circle cx="-11.4" cy="1" r=".7" fill="#ffe6cc"/></g>
  <g clip-path="url(#b2eyeR)"><circle cx="13" cy="-.8" r="4.9" fill="#4e2e22"/><circle cx="13" cy="-.8" r="2.3" fill="#180c0a"/><circle cx="11.2" cy="-2.6" r="1.5" fill="#fff"/><circle cx="14.6" cy="1" r=".7" fill="#ffe6cc"/></g>
  <!-- upper lash line with a small wing, just a few lashes -->
  <path d="M -22.6,-1.4 C -18.6,-9 -8.6,-9.2 -4,-1.6 L -5,-.8 C -9,-6.4 -17.6,-6.2 -21.2,-.4 Z" fill="{LASH}"/>
  <path d="M -21.4,-1.2 L -26.4,-4.6 L -21.8,.2 Z" fill="{LASH}"/>
  <path d="M -16.6,-6 L -18,-8.8 M -12.6,-6.8 L -13.2,-9.6" stroke="{LASH}" stroke-width="1" stroke-linecap="round"/>
  <path d="M 22.6,-1.4 C 18.6,-9 8.6,-9.2 4,-1.6 L 5,-.8 C 9,-6.4 17.6,-6.2 21.2,-.4 Z" fill="{LASH}"/>
  <path d="M 21.4,-1.2 L 26.4,-4.6 L 21.8,.2 Z" fill="{LASH}"/>
  <path d="M 16.6,-6 L 18,-8.8 M 12.6,-6.8 L 13.2,-9.6" stroke="{LASH}" stroke-width="1" stroke-linecap="round"/>
  <path d="M -19.4,2.4 C -15,4.2 -10,4.2 -6,2.2" fill="none" stroke="#c48a7a" stroke-width=".9"/>
  <path d="M 19.4,2.4 C 15,4.2 10,4.2 6,2.2" fill="none" stroke="#b87e6e" stroke-width=".9"/>
  <!-- beauty mark under her left eye -->
  <circle cx="15.8" cy="6.4" r="1" fill="#4a2c24"/>
  <!-- lips: defined cupid's bow, fuller lower lip, soft rose -->
  <path d="M -7.4,21.8 C -5,20.2 -2.6,19.6 -1.2,20.8 Q 0,21.6 1.2,20.8 C 2.6,19.6 5,20.2 7.4,21.8 C 4,22.8 -4,22.8 -7.4,21.8 Z" fill="#b65866"/>
  <path d="M -7.4,21.8 C -4,22.8 4,22.8 7.4,21.8 C 6,26.6 3,27.8 0,27.8 C -3,27.8 -6,26.6 -7.4,21.8 Z" fill="#cc6e78"/>
  <path d="M -7.4,21.8 C -4,22.8 4,22.8 7.4,21.8" fill="none" stroke="#8e3c4a" stroke-width=".9"/>
  <path d="M -3.2,24.6 C -1.6,25.4 0,25.4 1.2,25" fill="none" stroke="#efa6aa" stroke-width="1.5" stroke-linecap="round"/>
  <path d="M 6,27 C 3,28.6 -3,28.6 -6,27" fill="none" stroke="{B_SKIN_S}" stroke-width="1" opacity=".7"/>
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
</g>'''

DEFS = f'''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<clipPath id="b2face"><path d="{FACE}"/></clipPath><clipPath id="b2eyeL"><path d="{EYE_L}"/></clipPath><clipPath id="b2eyeR"><path d="{EYE_R}"/></clipPath>
<filter id="glint" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation=".5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{HEAD}</defs></svg>'''

def build():
    full = f'''<svg viewBox="0 0 400 900" role="img" aria-label="เจ้าสาวเต็มตัว ผมยาวตรงสีน้ำตาลเข้ม ชุดเกาะอกประดับเพชร">
<rect width="400" height="900" fill="#1b1f2b"/><rect y="760" width="400" height="140" fill="#161a24"/><ellipse cx="200" cy="790" rx="170" ry="16" fill="#10131b"/>
<g transform="translate(200,138) scale(1.4)"><use href="#b2back"/>{bride_body()}<use href="#b2head"/></g></svg>'''
    face = f'''<svg viewBox="-75 -84 150 156" role="img" aria-label="ใบหน้าเจ้าสาวระยะใกล้">
<rect x="-75" y="-84" width="150" height="156" fill="#1b1f2b"/><use href="#b2back"/>
<path d="M -50,72 C -48,58 -30,51 -14,50 L 14,50 C 30,51 48,58 50,72 Z" fill="{B_SKIN}"/><path d="M 20,51 C 36,54 48,60 50,72 L 30,72 C 30,64 28,56 20,51 Z" fill="{B_SKIN_S}"/>
<path d="M -12,53 Q 0,70 12,53" fill="none" stroke="{SILVER}" stroke-width=".9"/><path d="M 0,61.5 l 2,3 l -2,4 l -2,-4 Z" fill="{SILVER_L}"/>
<use href="#b2head"/></svg>'''
    chips = ''.join(f'<span><i style="background:{c}"></i>{n}</span>' for c, n in ((B_SKIN, 'ผิว'), (B_SKIN_S, 'ผิวเงา'), (H, 'ผมน้ำตาลเข้ม'), (H_SHINE, 'ผมเงา'), ('#cc6e78', 'ปาก'), (SILVER, 'เงิน')))
    page = CSS.replace('<title>เจ้าสาวกับเจ้าบ่าว</title>', '<title>เจ้าสาว รอบ 2</title>') + DEFS + f'''<div class="wrap"><section><h1>เจ้าสาว รอบ 2<span>ทรงหน้าแบบเดิม · ผมยาวตรงสีน้ำตาลเข้ม · มีไฝใต้ตา</span></h1>
<div class="panels"><figure>{full}<figcaption>เต็มตัว · ผมยาวตรงถึงเอว ปล่อยด้านหน้าลงบนไหล่สองข้าง ผ้าคลุมกับมงกุฎเงินเส้นบาง ชุดเกาะอกประดับเพชรแบบเดิม</figcaption></figure>
<figure>{face}<figcaption>ใบหน้าระยะใกล้ · ทรงหน้าแบบเดิม ตาสองชั้นเรียวยาวขึ้นนิด ขนตาพอประมาณมีหางตาเล็ก ๆ คิ้วตรงนุ่ม ไฝเล็กใต้ตาข้างซ้ายของเธอ ปากมีกระจับชัด ปากล่างอิ่ม สีกุหลาบอ่อน ผมสีน้ำตาลเข้มเกือบดำมีเงาประกาย ผมกรอบหน้าเริ่มที่โหนกแก้ม</figcaption>
<div class="chips">{chips}</div></figure></div></section></div>'''
    open('bride_v2.html', 'w').write(page); print('ok', len(page))

if __name__ == '__main__':
    build()
