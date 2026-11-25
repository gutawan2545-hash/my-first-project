"""ปกตอนที่ 2 แบบโปสเตอร์ละครเวที (ผู้ใช้สั่ง: จัดวางแบบโปสเตอร์ละครที่รวมตัวละครหลายตัว ชื่อเรื่องตัวใหญ่ด้านล่าง)
ใช้ตัวละครจริงของตอนนี้ + ระบบแสง cinelight · ออกแบบเอง ไม่ลอกองค์ประกอบหรือโลโก้จากภาพตัวอย่าง
รัน: python3 poster.py && node render_poster.js -> ../final/cover_ep2.png"""
import os, sys, re, base64
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'storyboard')); sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'pipeline'))
import storyboard as SB, supporting as SP, wedding_chars as WC, cinelight as CL
os.chdir(HERE)

LIT = CL.Light(dir=(-.6, -.7), rim_w=2.4, shade_w=8, rim_op=.9)
DEFS = (CL.defs({'p': LIT}) + SB.N9.H8.S.DEFS + SB.H8.DEFS_EXTRA + SB.N9.EXTRA_DEFS + WC.DEFS + SB.B2.DEFS + SP.DEFS + SB.P2.DEFS2 + SB.EXTRA_DEFS + SB.CHAR_DEFS)
BG = base64.b64encode(open('bg_lit/hall_nbg.jpg', 'rb').read()).decode()

def ch(key, x, head_y, s, extra=''):
    """วางตัวละครให้หัวอยู่ที่ head_y (กึ่งกลางหน้า) พร้อมแสงขอบ"""
    lf = SB.CH[key][1]; feet = head_y + (lf - 58) * s
    return f'<g filter="url(#clRim_p)" {extra}><g transform="translate({x},{feet - lf * s:.1f}) scale({s})"><use href="#ch_{key}"/></g></g>'

FT = 'font-family="IBM Plex Sans Thai, sans-serif"'
RINGS = ('<g transform="translate(402,572) rotate(-18) scale(.8)"><ellipse cx="-11" cy="0" rx="20" ry="20" fill="none" stroke="#e8edf6" stroke-width="5"/>'
         '<ellipse cx="13" cy="0" rx="20" ry="20" fill="none" stroke="#b8c2d4" stroke-width="5"/><path d="M -11,-20 l 6,-9 l 6,9 Z" fill="#ffffff"/></g>')
svg = f'''<svg id="cover" viewBox="0 0 540 960" xmlns="http://www.w3.org/2000/svg">
<defs>
 <linearGradient id="pBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a2340"/><stop offset=".5" stop-color="#4a3c5c"/><stop offset="1" stop-color="#140f1e"/></linearGradient>
 <linearGradient id="pFade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0814" stop-opacity="0"/><stop offset=".45" stop-color="#0c0814" stop-opacity=".75"/><stop offset="1" stop-color="#07050c" stop-opacity=".97"/></linearGradient>
 <linearGradient id="pTitle" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#e6e2f2"/><stop offset="1" stop-color="#b9b2d6"/></linearGradient>
 <radialGradient id="pMoon"><stop offset="0" stop-color="#e8eeff" stop-opacity=".55"/><stop offset="1" stop-color="#e8eeff" stop-opacity="0"/></radialGradient>
 <radialGradient id="pVig" cx=".5" cy=".42" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".6"/></radialGradient>
 <filter id="pBlur"><feGaussianBlur stdDeviation="5"/></filter>
 <filter id="pGlow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
 <filter id="pGrain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.9" numOctaves="1" seed="9"/><feColorMatrix type="saturate" values="0"/></filter>
</defs>
<rect width="540" height="960" fill="url(#pBg)"/>
<image href="data:image/jpeg;base64,{BG}" width="540" height="960" opacity=".55" filter="url(#pBlur)" preserveAspectRatio="xMidYMid slice"/>
<rect width="540" height="960" fill="#3a2c52" opacity=".35" style="mix-blend-mode:multiply"/>
<circle cx="270" cy="250" r="230" fill="url(#pMoon)"/>
<!-- แถวหลัง: แม่เจ้าบ่าว (ซ้ายบน) · ผู้หญิงชุดดำ (ขวาบน) -->
<g opacity=".95">{ch('mom', 100, 165, 1.1)}</g>
<g>{ch('wb', 442, 235, 1.25)}</g>
<!-- กลุ่มตัวละครรองฝั่งขวา -->
<g>{ch('gm', 520, 430, .78)}{ch('ph', 470, 455, .8)}{ch('staff', 520, 520, .7)}{ch('bm', 455, 540, .7)}{ch('guard', 505, 600, .72)}</g>
<!-- คู่หลัก: เจ้าบ่าวยิ้มร้ายด้านหลัง · เจ้าสาวหน้ากังวลด้านหน้า -->
<g>{ch('groom_sin', 160, 355, 1.95)}</g>
<g>{ch('bride_worry', 298, 410, 2.15)}</g>
<!-- ชื่อเรื่อง -->
<rect y="330" width="540" height="630" fill="url(#pFade)"/>
<g {FT} text-anchor="middle">
 <text x="270" y="506" font-size="25" font-weight="600" fill="#d9d2ee" letter-spacing="2">ถ้าวันนี้เป็น</text>
 <text x="266" y="568" font-size="64" font-weight="700" fill="url(#pTitle)" stroke="#120a1c" stroke-width="3" paint-order="stroke">วันแต่งงาน</text>
 <text x="270" y="610" font-size="35" font-weight="700" fill="#c9a8ff" stroke="#120a1c" stroke-width="3" paint-order="stroke">ของคุณ</text>
</g>
<g transform="translate(270,640)" {FT} text-anchor="middle"><rect x="-108" y="-15" width="216" height="28" rx="6" fill="#8e1b24"/>
 <text x="0" y="4.5" font-size="13" font-weight="600" fill="#fff4f2">กฎข้อเดียว • อย่าให้เขาถอดแหวน</text></g>
<text x="270" y="674" text-anchor="middle" {FT} font-size="11" fill="#a79fc0" letter-spacing="2">ODD HOURS</text>
<!-- มุมขวาบน: โลโก้ดวงตา + ตอน -->
<g transform="translate(490,44)"><ellipse rx="22" ry="16.5" fill="#7a1fff"/><path d="M -16.5,0 C -9,-9.5 9,-9.5 16.5,0 C 9,9.5 -9,9.5 -16.5,0 Z" fill="#05040a"/><circle r="4.6" fill="#d6b0ff"/></g>
<rect width="540" height="960" fill="url(#pVig)"/>
<rect width="540" height="960" filter="url(#pGrain)" opacity=".07" style="mix-blend-mode:screen"/>
</svg>'''
html = ('<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;600;700&display=swap">'
        '<style>html,body{margin:0;background:#000}#cover{display:block;width:540px;height:960px}</style>' + DEFS + svg +
        '<script>document.fonts.ready.then(()=>document.body.dataset.ready="1")</script>')
open('poster.html', 'w').write(html)
print('poster.html')
