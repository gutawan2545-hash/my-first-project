# ฉากไทยสำหรับสตอรี่บอร์ด (ย่านพระนคร): สไตล์แอนิเมชันวาดมือ แดดอุ่นส่องเป็นลำ เงาอมฟ้า ของเยอะ
# ใช้ร่วมกับ storyboard.py (import แบบ from sb_thai import *)
import math, random
TH = 'font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'

DEFS_THAI = '''
<filter id="mottle" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".014" numOctaves="3" seed="11"/><feColorMatrix values="0 0 0 0 .35  0 0 0 0 .22  0 0 0 0 .16  0 0 0 1.2 -.35"/></filter>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe2a8" stop-opacity=".85"/><stop offset="1" stop-color="#ffcf88" stop-opacity=".25"/></linearGradient>
<linearGradient id="sunfade" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe6b0" stop-opacity=".7"/><stop offset="1" stop-color="#ffd090" stop-opacity="0"/></linearGradient>
<linearGradient id="morningsky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#5aa8e2"/><stop offset=".6" stop-color="#a8d4ee"/><stop offset="1" stop-color="#f6e2c0"/></linearGradient>
<linearGradient id="tealwall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#4f8f8a"/><stop offset="1" stop-color="#6fa8a0"/></linearGradient>
<pattern id="planks" width="540" height="40" patternUnits="userSpaceOnUse"><rect width="540" height="40" fill="#a8683e"/><rect y="0" width="540" height="2" fill="#7a4626"/><rect x="120" y="0" width="2" height="20" fill="#7a4626"/><rect x="330" y="20" width="2" height="20" fill="#7a4626"/><rect y="20" width="540" height="1.4" fill="#8a5230"/><path d="M 40,10 C 80,8 120,12 160,9 M 220,30 C 280,28 320,32 380,29" stroke="#b8784a" stroke-width="1.4" fill="none"/></pattern>
<pattern id="oldtiles" width="34" height="34" patternUnits="userSpaceOnUse"><rect width="34" height="34" fill="#efe2c2"/><rect width="34" height="2" fill="#cdb98e"/><rect width="2" height="34" fill="#cdb98e"/><rect x="6" y="6" width="10" height="6" fill="#f8eed6" opacity=".7"/></pattern>
<pattern id="slats" width="20" height="9" patternUnits="userSpaceOnUse"><rect width="20" height="9" fill="#2f6e5e"/><rect width="20" height="3" fill="#24584a"/><rect y="3" width="20" height="1.4" fill="#4a8e7a"/></pattern>
'''
TEX = '<rect width="540" height="960" filter="url(#mottle)" style="mix-blend-mode:multiply" opacity=".22"/>'

def sunpoly(pts, o=1.0, grad="sun"):
    return f'<path d="M {" L ".join(f"{x},{y}" for x, y in pts)} Z" fill="url(#{grad})" style="mix-blend-mode:screen" opacity="{o}"/>'

def coolshade(pts, o=.28):
    return f'<path d="M {" L ".join(f"{x},{y}" for x, y in pts)} Z" fill="#1d3a52" style="mix-blend-mode:multiply" opacity="{o}"/>'

# ---------- ของในห้องนอน ----------
def wardrobe(x, y):
    return f'''<g transform="translate({x},{y})">
    <path d="M -6,0 L 156,0 L 150,-16 L 0,-16 Z" fill="#6a3a22"/><path d="M 30,-16 C 50,-34 100,-34 120,-16 Z" fill="#7a4428"/>
    <rect x="0" y="0" width="150" height="400" fill="#7a4a2a"/><rect x="0" y="0" width="22" height="400" fill="#8e5a36"/><rect x="128" y="0" width="22" height="400" fill="#5e3620"/>
    <rect x="10" y="12" width="62" height="290" fill="#6a3e22"/><rect x="16" y="18" width="50" height="278" fill="#a8cfd8"/><path d="M 16,18 L 50,18 L 16,140 Z" fill="#d6ecf2" opacity=".8"/><path d="M 30,296 L 66,180 L 66,296 Z" fill="#7aa8b8" opacity=".6"/>
    <rect x="78" y="12" width="62" height="290" fill="#6a3e22"/><rect x="84" y="20" width="50" height="130" fill="#7e4c2c"/><rect x="84" y="162" width="50" height="132" fill="#7e4c2c"/>
    <circle cx="74" cy="160" r="3.4" fill="#e0b860"/><circle cx="80" cy="160" r="3.4" fill="#e0b860"/>
    <rect x="8" y="312" width="134" height="38" fill="#6a3e22"/><rect x="8" y="356" width="134" height="38" fill="#6a3e22"/>
    <path d="M 60,331 C 66,325 84,325 90,331 M 60,375 C 66,369 84,369 90,375" stroke="#e0b860" stroke-width="3" fill="none"/>
    <rect x="10" y="-60" width="70" height="44" fill="#c89a6a"/><rect x="10" y="-60" width="70" height="8" fill="#b08458"/>
    <path d="M 96,-16 C 94,-46 132,-50 136,-20 Z" fill="#c8243a"/><path d="M 96,-16 C 96,-36 110,-46 122,-46 C 110,-38 104,-28 104,-16 Z" fill="#e8434e"/><rect x="96" y="-22" width="40" height="6" fill="#1a1a20"/>
    </g>'''

def shutter(x, y, w, h, flip=1):
    return f'<g transform="translate({x},{y}) skewY({-12*flip})"><rect width="{w}" height="{h}" fill="url(#slats)"/><rect width="{w}" height="{h}" fill="none" stroke="#24584a" stroke-width="4"/></g>'

def old_window(x, y, w, h):
    """หน้าต่างไม้ตึกแถวเก่า เปิดบานเกล็ดออกสองข้าง เห็นตึกฝั่งตรงข้ามกับยอดวัด"""
    cx = x + w / 2
    return f'''<clipPath id="ow{x}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#ow{x})">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#morningsky)"/>
    <ellipse cx="{x+50}" cy="{y+40}" rx="40" ry="12" fill="#ffffff" opacity=".8"/><ellipse cx="{x+w-40}" cy="{y+60}" rx="34" ry="10" fill="#ffffff" opacity=".7"/>
    <path d="M {cx+40},{y+h*.55} L {cx+50},{y+h*.2} L {cx+60},{y+h*.55} Z" fill="#e8b84a"/><path d="M {cx+50},{y+h*.2} L {cx+50},{y+h*.1}" stroke="#e8b84a" stroke-width="2"/>
    <path d="M {cx+30},{y+h*.55} L {cx+70},{y+h*.55} L {cx+64},{y+h*.45} L {cx+36},{y+h*.45} Z" fill="#c8323a"/>
    <rect x="{x-10}" y="{y+h*.5}" width="{w+20}" height="{h}" fill="#e9d6ae"/>
    {"".join(f'<path d="M {x+14+k*56},{y+h} L {x+14+k*56},{y+h*.66} C {x+14+k*56},{y+h*.58} {x+50+k*56},{y+h*.58} {x+50+k*56},{y+h*.66} L {x+50+k*56},{y+h} Z" fill="#2f6e5e"/><path d="M {x+32+k*56},{y+h*.6} L {x+32+k*56},{y+h}" stroke="#24584a" stroke-width="2"/>' for k in range(int(w/56)))}
    <rect x="{x-10}" y="{y+h*.52}" width="{w+20}" height="6" fill="#ffffff" opacity=".8"/>
    <path d="M {x},{y+h*.3} C {x+w*.3},{y+h*.42} {x+w*.7},{y+h*.38} {x+w},{y+h*.28}" stroke="#3a3040" stroke-width="1.6" fill="none"/>
    </g>
    {"".join(f'<rect x="{x+k*w/6:.0f}" y="{y}" width="3" height="{h}" fill="#3a3a40"/>' for k in range(1,6))}
    <path d="M {x-12},{y-12} L {x+w+12},{y-12} L {x+w+12},{y+h+12} L {x-12},{y+h+12} Z M {x},{y} L {x},{y+h} L {x+w},{y+h} L {x+w},{y} Z" fill="#2f6e5e" fill-rule="evenodd"/>
    <rect x="{x-20}" y="{y+h+10}" width="{w+40}" height="12" fill="#24584a"/>
    {shutter(x-44, y+8, 40, h-20, 1)}{shutter(x+w+4, y+8, 40, h-20, -1)}'''

def muaythai_poster(x, y):
    return f'''<g transform="translate({x},{y}) rotate(-2)"><rect width="96" height="132" fill="#f4e6c4"/><rect x="0" y="0" width="96" height="30" fill="#c8243a"/>
    <text x="48" y="22" text-anchor="middle" {TH} font-size="18" font-weight="700" fill="#ffe08a">มวยไทย</text>
    <circle cx="30" cy="66" r="14" fill="#c8243a"/><circle cx="66" cy="66" r="14" fill="#1f5fbf"/><path d="M 22,84 L 38,84 L 34,110 L 26,110 Z" fill="#c8243a"/><path d="M 58,84 L 74,84 L 70,110 L 62,110 Z" fill="#1f5fbf"/>
    <text x="48" y="126" text-anchor="middle" {TH} font-size="10" font-weight="700" fill="#5a2a1a">ศึกวันศุกร์ ราชดำเนิน</text></g>'''

def old_photo(x, y):
    return f'''<g transform="translate({x},{y})"><rect width="54" height="66" fill="#5a3420"/><rect x="5" y="5" width="44" height="56" fill="#d8cdb4"/>
    <circle cx="27" cy="26" r="9" fill="#8a7a64"/><path d="M 14,58 C 14,40 40,40 40,58 Z" fill="#6a5a48"/></g>'''

def axe_pillow(x, y, s=1.0):
    """หมอนขวาน"""
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M 0,0 L 60,0 L 30,-46 Z" fill="#c8243a"/><path d="M 0,0 L 30,-46 L 24,-46 L -6,0 Z" fill="#e8434e"/>
    <path d="M 12,-8 L 48,-8 L 30,-34 Z" fill="none" stroke="#f0c860" stroke-width="2"/><path d="M 22,-12 L 38,-12 L 30,-24 Z" fill="#f0c860"/>
    <rect x="-8" y="0" width="76" height="12" rx="3" fill="#a81a2a"/><g fill="#f0c860">{"".join(f'<rect x="{-4+k*10}" y="3" width="5" height="5"/>' for k in range(7))}</g></g>'''

def thai_blanket(x, y, w=230):
    flowers = "".join(f'<g transform="translate({x+18+k*30},{y+6+(k%2)*10})"><circle r="6" fill="#f4f0e4"/><circle r="2.6" fill="#f0c860"/></g>' for k in range(int(w/30)))
    return f'''<path d="M {x},{y} C {x+50},{y-24} {x+w-50},{y-28} {x+w},{y-6} L {x+w+10},{y+36} L {x-8},{y+36} Z" fill="#d8566e"/>
    <path d="M {x},{y} C {x+50},{y-24} {x+w*.5},{y-26} {x+w*.6},{y-22} C {x+w*.4},{y-8} {x+20},{y+8} {x-8},{y+36} Z" fill="#e8748a"/>{flowers}'''

def mattress2(x, y, w=320):
    return f'''<g transform="translate({x},{y})"><rect x="-10" y="20" width="{w+20}" height="16" fill="#c8a868"/>{"".join(f'<rect x="{-10+k*16}" y="20" width="8" height="16" fill="#b08e50"/>' for k in range(int((w+20)/16)))}
    <rect x="0" y="0" width="{w}" height="30" rx="8" fill="#f2ece0"/><rect x="0" y="20" width="{w}" height="12" rx="5" fill="#d8ccb8"/></g>'''

def old_fan(x, y, s=1.0):
    spokes = "".join(f'<path d="M 0,-150 L {34*math.cos(a/10*6.283):.1f},{-150+34*math.sin(a/10*6.283):.1f}" stroke="#b8d8cc" stroke-width="1.2"/>' for a in range(10))
    return f'''<g transform="translate({x},{y}) scale({s})"><ellipse rx="30" ry="7" fill="#5a8a7a"/><rect x="-4" y="-120" width="8" height="120" fill="#6ea898"/><rect x="-4" y="-120" width="3" height="120" fill="#9ccab8"/>
    <rect x="-12" y="-56" width="24" height="14" rx="4" fill="#5a8a7a"/><circle cx="-5" cy="-49" r="2" fill="#f0c860"/><circle cx="3" cy="-49" r="2" fill="#e8e0d0"/>
    <circle cx="0" cy="-150" r="34" fill="#9ccab8" opacity=".35"/>{spokes}<circle cx="0" cy="-150" r="34" fill="none" stroke="#b8d8cc" stroke-width="3"/>
    <path d="M 0,-150 C 10,-170 24,-166 20,-154 Z M 0,-150 C -16,-140 -22,-126 -10,-126 Z M 0,-150 C 8,-132 20,-130 22,-140 Z" fill="#5a8a7a"/><circle cx="0" cy="-150" r="6" fill="#3a6a5a"/></g>'''

def hanging_bulb(x, y):
    return f'<path d="M {x},0 L {x},{y-14}" stroke="#2a2020" stroke-width="1.4"/><rect x="{x-5}" y="{y-16}" width="10" height="8" fill="#3a3030"/><circle cx="{x}" cy="{y}" r="9" fill="#fff0c8"/><circle cx="{x}" cy="{y}" r="26" fill="#ffe2a8" opacity=".25"/>'

def radio_shelf(x, y):
    return f'''<rect x="{x}" y="{y}" width="120" height="8" fill="#6a3a22"/><rect x="{x}" y="{y+8}" width="120" height="3" fill="#4a2814"/>
    <rect x="{x+8}" y="{y-34}" width="56" height="34" rx="4" fill="#c8a060"/><circle cx="{x+24}" cy="{y-17}" r="10" fill="#5a3a22"/><rect x="{x+40}" y="{y-28}" width="18" height="6" fill="#efe2c2"/><circle cx="{x+50}" cy="{y-10}" r="3" fill="#5a3a22"/><path d="M {x+58},{y-34} L {x+74},{y-60}" stroke="#a8a8b0" stroke-width="1.6"/>
    <rect x="{x+76}" y="{y-26}" width="16" height="26" rx="2" fill="#d8323e"/><rect x="{x+96}" y="{y-20}" width="18" height="20" rx="3" fill="#f4f0e4"/><rect x="{x+98}" y="{y-14}" width="14" height="4" fill="#2f8a5a"/>'''

def thai_calendar(x, y):
    return f'''<g transform="translate({x},{y})"><rect width="60" height="84" fill="#f4f0e4"/><rect width="60" height="34" fill="#2f6e5e"/><path d="M 6,30 L 20,12 L 30,22 L 40,8 L 54,30 Z" fill="#e8b84a"/>
    <text x="30" y="58" text-anchor="middle" font-family="Inter" font-size="20" font-weight="800" fill="#c8243a">๒๓</text><text x="30" y="76" text-anchor="middle" {TH} font-size="9" fill="#5a3a22">พฤศจิกายน</text></g>'''

def slippers(x, y):
    return f'<ellipse cx="{x}" cy="{y}" rx="16" ry="7" fill="#1f5fbf"/><ellipse cx="{x+30}" cy="{y+4}" rx="16" ry="7" fill="#1f5fbf"/><path d="M {x-6},{y-2} L {x+2},{y-7} L {x+8},{y-2}" stroke="#f4f0e4" stroke-width="2.4" fill="none"/><path d="M {x+24},{y+2} L {x+32},{y-3} L {x+38},{y+2}" stroke="#f4f0e4" stroke-width="2.4" fill="none"/>'

def bedroom2(blur="bgblur"):
    """ห้องนอนชั้นสองตึกแถวเก่าย่านพระนคร: ผนังเขียวหัวเป็ด ไม้บุผนังครึ่งล่าง พื้นไม้กระดาน หน้าต่างบานเกล็ดเปิดออก แดดเช้าส่องเป็นลำ"""
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#tealwall)"/>
    <rect y="0" width="540" height="26" fill="#5a3a28"/><rect y="26" width="540" height="6" fill="#7a5038"/>
    <rect y="468" width="540" height="140" fill="#8a5634"/>{"".join(f'<rect x="{k*68}" y="480" width="56" height="116" fill="#7a4a2c"/><rect x="{k*68}" y="480" width="56" height="5" fill="#a8704a"/>' for k in range(8))}
    <rect y="464" width="540" height="8" fill="#a8704a"/>
    {old_window(270, 110, 200, 250)}
    {wardrobe(16, 210)}
    {old_photo(190, 110)}{muaythai_poster(184, 200)}{thai_calendar(196, 350)}
    {radio_shelf(408, 430)}
    {hanging_bulb(150, 120)}
    <rect y="604" width="540" height="356" fill="url(#planks)"/><rect y="604" width="540" height="8" fill="#5a3420"/>
    {coolshade([(0,32),(160,32),(150,960),(0,960)], .22)}
    {sunpoly([(270,372),(470,372),(400,960),(40,960)], .55)}
    {sunpoly([(270,360),(470,360),(470,300),(300,240)], .25)}
    </g>{TEX}'''

# ---------- ร้านทอง ----------
def poster_collage(x, y, w, h, seed=3):
    r = random.Random(seed); out = ""
    cols = ["#f4e6c4", "#e8c86a", "#7fae8a", "#e88a6a", "#f0dcb0", "#c8d8b8"]
    labels = ["ทอง", "ราคาวันนี้", "รับซื้อ", "ผ่อนได้", "แท้ ๙๖.๕", "ขายฝาก"]
    for k in range(12):
        px, py, pw, ph = x + r.uniform(0, w - 70), y + r.uniform(0, h - 60), r.uniform(46, 80), r.uniform(40, 70)
        c = r.choice(cols)
        out += f'<g transform="translate({px:.0f},{py:.0f}) rotate({r.uniform(-6,6):.1f})"><rect width="{pw:.0f}" height="{ph:.0f}" fill="{c}"/><rect x="4" y="4" width="{pw-8:.0f}" height="8" fill="#c8243a" opacity=".7"/>'
        out += f'<text x="{pw/2:.0f}" y="{ph*.6:.0f}" text-anchor="middle" {TH} font-size="11" font-weight="700" fill="#5a2a1a">{r.choice(labels)}</text>'
        out += "".join(f'<rect x="6" y="{ph*.7+j*5:.0f}" width="{pw-12-j*8:.0f}" height="2" fill="#8a6a4a" opacity=".6"/>' for j in range(2)) + '</g>'
    return out

def ceiling_fan(x, y):
    return f'''<path d="M {x},0 L {x},{y}" stroke="#3a2a20" stroke-width="3"/><ellipse cx="{x}" cy="{y}" rx="14" ry="8" fill="#5a3a28"/>
    <path d="M {x-12},{y} L {x-110},{y+10} L {x-110},{y-2} Z M {x+12},{y} L {x+110},{y-6} L {x+108},{y+8} Z" fill="#7a4a2a"/>'''

def pendulum_clock(x, y):
    return f'''<g transform="translate({x},{y})"><path d="M -30,-10 L 30,-10 L 22,-30 L -22,-30 Z" fill="#5a2e1a"/><rect x="-30" y="-10" width="60" height="130" fill="#6a3a22"/><rect x="-24" y="-4" width="48" height="48" rx="24" fill="#f4ecd8"/>
    <path d="M 0,20 L 0,2 M 0,20 L 12,26" stroke="#2a1a14" stroke-width="2.4"/><rect x="-16" y="52" width="32" height="60" fill="#3a1e12"/><path d="M 0,52 L 4,96" stroke="#e0b860" stroke-width="2"/><circle cx="4" cy="100" r="8" fill="#e0b860"/></g>'''

def folding_doors(x, y, w, h):
    """บานเฟี้ยมไม้ พับเปิด เห็นถนนข้างนอก"""
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#morningsky)"/><rect x="{x}" y="{y+h*.45:.0f}" width="{w}" height="{h*.55:.0f}" fill="#efe0c0"/>
    <rect x="{x+10}" y="{y+h*.55:.0f}" width="40" height="{h*.45:.0f}" fill="#8a5634"/><rect x="{x+w-56}" y="{y+h*.5:.0f}" width="46" height="{h*.5:.0f}" fill="#2f6e5e"/>
    <rect x="{x}" y="{y+h-26}" width="{w}" height="26" fill="#8a8078"/>
    {"".join(f'<rect x="{x-60+k*14}" y="{y}" width="12" height="{h}" fill="{["#8a5634","#7a4a2c"][k%2]}"/>' for k in range(4))}
    {"".join(f'<rect x="{x+w+4+k*14}" y="{y}" width="12" height="{h}" fill="{["#7a4a2c","#6a3e22"][k%2]}"/>' for k in range(4))}
    <rect x="{x-64}" y="{y-14}" width="{w+128}" height="14" fill="#5a3420"/>'''

def gold_shop2(blur="bgblur"):
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="#9a1e28"/><rect width="540" height="380" fill="#a8242e"/>
    <rect y="380" width="540" height="230" fill="url(#oldtiles)"/>
    {poster_collage(10, 90, 230, 170, 5)}
    {gold_chains(270, 96, 250, 150, 10)}
    <rect x="150" y="20" width="240" height="56" fill="#7a1018"/><rect x="156" y="26" width="228" height="44" fill="none" stroke="#f0cc60" stroke-width="2"/>
    <text x="270" y="58" text-anchor="middle" {TH} font-size="26" font-weight="700" fill="#f4d878">ห้างทอง ซิ่งเฮง</text>
    {ceiling_fan(270, 90)}
    {price_board(24, 280)}{pendulum_clock(470, 290)}{shrine(380, 370)}
    {folding_doors(190, 300, 150, 300)}
    <rect x="20" y="396" width="150" height="10" fill="#5a2a1e"/>{lucky_cat(60, 396, .8)}{plant(130, 396, .7, "#2f6e5e")}
    <rect y="604" width="540" height="356" fill="url(#terrazzo)"/><rect y="604" width="540" height="6" fill="#6a4a3a"/>
    {sunpoly([(190,300),(340,300),(420,960),(100,960)], .6)}
    {coolshade([(0,0),(140,0),(110,960),(0,960)], .2)}
    </g>{TEX}'''

# ---------- ถนนย่านพระนคร ----------
def shophouse(x, ground, w, col, sign=None, sign_col="#c8243a", seed=1):
    r = random.Random(seed)
    top = ground - 430
    arches = "".join(f'''<path d="M {x+16+k*(w-20)/3:.0f},{top+180} L {x+16+k*(w-20)/3:.0f},{top+110} C {x+16+k*(w-20)/3:.0f},{top+84} {x+(w-20)/3*(k+1)-4:.0f},{top+84} {x+(w-20)/3*(k+1)-4:.0f},{top+110} L {x+(w-20)/3*(k+1)-4:.0f},{top+180} Z" fill="#2f6e5e"/>
      <path d="M {x+16+k*(w-20)/3+((w-20)/3-20)/2:.0f},{top+92} L {x+16+k*(w-20)/3+((w-20)/3-20)/2:.0f},{top+180}" stroke="#24584a" stroke-width="2"/>''' for k in range(3))
    doors = "".join(f'<rect x="{x+8+k*(w-16)/6:.0f}" y="{ground-150}" width="{(w-16)/6-3:.0f}" height="150" fill="{["#8a5634","#7a4a2c"][k%2]}"/>' for k in range(6))
    plants = "".join(f'<g transform="translate({x+20+k*40},{ground})"><path d="M -10,0 L 10,0 L 8,-16 L -8,-16 Z" fill="#c87a4a"/><circle cy="-26" r="14" fill="#5a9a68"/><circle cx="-8" cy="-20" r="9" fill="#4a8a58"/></g>' for k in range(r.randint(1, 2)))
    sg = f'<rect x="{x+12}" y="{ground-196}" width="{w-24}" height="34" rx="3" fill="{sign_col}"/><text x="{x+w/2}" y="{ground-172}" text-anchor="middle" {TH} font-size="17" font-weight="700" fill="#fff4d0">{sign}</text>' if sign else ""
    return f'''<rect x="{x}" y="{top}" width="{w}" height="{ground-top}" fill="{col}"/>
    <rect x="{x}" y="{top}" width="{w}" height="18" fill="#f4ecd8"/><rect x="{x}" y="{top+18}" width="{w}" height="6" fill="#c8b48a"/>
    <path d="M {x+w/2-30},{top} C {x+w/2-20},{top-24} {x+w/2+20},{top-24} {x+w/2+30},{top} Z" fill="#f4ecd8"/>
    {arches}<rect x="{x+6}" y="{top+180}" width="{w-12}" height="8" fill="#f4ecd8"/>
    <rect x="{x}" y="{top+200}" width="{w}" height="10" fill="#c8b48a"/>
    <path d="M {x+4},{ground-160} L {x+w-4},{ground-160} L {x+w+8},{ground-136} L {x-8},{ground-136} Z" fill="#e8e0cc" opacity=".9"/>
    {doors}{sg}{plants}'''

def power_lines(y0):
    return f'''<path d="M -10,{y0} C 160,{y0+40} 380,{y0+30} 560,{y0-6} M -10,{y0+16} C 180,{y0+50} 360,{y0+44} 560,{y0+10} M -10,{y0+30} C 200,{y0+62} 340,{y0+60} 560,{y0+26} M 40,{y0+20} C 120,{y0+80} 260,{y0+70} 300,{y0+40}" fill="none" stroke="#2a2428" stroke-width="1.8"/>'''

def temple_far(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})" opacity=".9"><path d="M -40,0 L 40,0 L 30,-30 L -30,-30 Z" fill="#e0b26a"/><path d="M -30,-30 L 30,-30 L 16,-80 L -16,-80 Z" fill="#e8c06a"/>
    <path d="M -16,-80 L 16,-80 L 0,-150 Z" fill="#f0cc70"/><path d="M -50,0 L -40,-14 L 40,-14 L 50,0 Z" fill="#c8323a"/></g>'''

def phranakhon_street(blur="bgblur", ground=640):
    cols = ["#e6c690", "#9ccab8", "#e3957a", "#efe0c0", "#c9b8d8"]
    signs = [("กาแฟโบราณ", "#2f6e5e"), ("ห้างทอง", "#c8243a"), ("ข้าวมันไก่", "#e8743a"), ("ตัดผม", "#1f5fbf"), (None, "")]
    houses = "".join(shophouse(-40 + k*130, ground, 130, cols[k % 5], signs[k % 5][0], signs[k % 5][1], k) for k in range(5))
    return f'''<g filter="url(#{blur})">
    <rect width="540" height="960" fill="url(#morningsky)"/>
    <ellipse cx="120" cy="80" rx="70" ry="18" fill="#ffffff" opacity=".85"/><ellipse cx="400" cy="120" rx="60" ry="14" fill="#ffffff" opacity=".7"/>
    {temple_far(440, 230, 1.0)}<path d="M 300,230 C 330,190 380,186 400,230 Z" fill="#b8a888" opacity=".7"/>
    {houses}
    {power_lines(150)}
    <rect x="474" y="80" width="12" height="{ground-80}" fill="#9a948a"/><rect x="460" y="110" width="40" height="5" fill="#7a746a"/>
    <rect y="{ground}" width="540" height="{960-ground}" fill="#8a8078"/><rect y="{ground}" width="540" height="34" fill="#c8bca8"/><rect y="{ground+34}" width="540" height="5" fill="#9a8e7a"/>
    <path d="M 0,{ground+150} L 540,{ground+150}" stroke="#f4ecd8" stroke-width="5" stroke-dasharray="44 28"/>
    {coolshade([(0,ground-430),(90,ground-430),(260,ground+320),(0,ground+320)], .26)}
    {sunpoly([(300,0),(540,0),(540,960),(420,960)], .35, "sunfade")}
    </g>{TEX}'''

def soi2(blur="bgblur", ground=660):
    return f'''{phranakhon_street(blur, ground)}
    <g filter="url(#{blur})"><rect x="300" y="{ground-118}" width="150" height="36" rx="4" fill="#1f5fbf"/><text x="375" y="{ground-93}" text-anchor="middle" {TH} font-size="16" font-weight="700" fill="#fff">ซอย ๓ พระนคร</text>
    {tree(500, ground, .9)}{win_riders(320, ground+14)}</g>'''

# ---------- ตุ๊กตุ๊กไทย (อิงภาพจริง) ----------
def tuktuk_thai(x, y, s=1.0, rot=0):
    """หันข้างเต็ม หน้ารถไปทางซ้าย · หน้ากากรถสีขาวแถบน้ำเงิน ไฟหน้ากลมโครเมียม โช้คหน้าคู่ ล้อหน้าขอบแดง บังโคลนน้ำเงิน
    กระจกหน้า ไฟตัดหมอกเหลืองสี่ดวงใต้หลังคา หลังคาผ้าน้ำเงินระบายเงิน ป้าย TAXI · เบาะแดง ราวโครเมียม ตัวรถน้ำเงิน ล้อหลังเล็ก"""
    fringe = "".join(f'<path d="M {-118+k*12},-186 q 6,8 12,0" fill="#e4e8ee" stroke="#b8bec8" stroke-width=".8"/>' for k in range(20))
    pleats = "".join(f'<path d="M {4+k*12},-118 L {4+k*12},-76" stroke="#a81a2a" stroke-width="1.4"/>' for k in range(8))
    return f'''<g transform="translate({x},{y}) rotate({rot}) scale({s})">
    <path d="M 100,-6 L 128,-6 L 128,2 L 100,2 Z" fill="#9aa0aa"/>
    <circle cx="84" cy="0" r="19" fill="#16161c"/><circle cx="84" cy="0" r="9" fill="#d8dde6"/><circle cx="84" cy="0" r="3" fill="#16161c"/>
    <path d="M 60,-14 C 60,-36 108,-36 108,-14" fill="none" stroke="#d8dde6" stroke-width="5"/>
    <path d="M -100,-62 L 112,-62 L 112,-14 L -100,-14 Z" fill="#1f5fbf"/><path d="M 30,-62 L 112,-62 L 112,-14 L 40,-14 Z" fill="#174a98"/>
    <path d="M -100,-62 L 112,-62 L 112,-56 L -100,-56 Z" fill="#d8dde6"/><path d="M -100,-20 L 112,-20" stroke="#d8dde6" stroke-width="2"/>
    <path d="M -96,-14 L -10,-14 L -10,-6 L -96,-6 Z" fill="#5a5e6a"/>{"".join(f'<path d="M {-94+k*8},-14 L {-90+k*8},-6" stroke="#8a8e9a" stroke-width="1"/>' for k in range(11))}
    <path d="M -2,-120 C -2,-126 4,-128 10,-128 L 100,-128 L 100,-70 L -2,-70 Z" fill="#c8243a"/>{pleats}<path d="M -2,-120 L 100,-120 L 100,-114 L -2,-114 Z" fill="#e8434e"/>
    <path d="M -6,-74 L 106,-74 L 106,-62 L -6,-62 Z" fill="#c8243a"/><path d="M -6,-74 L 106,-74 L 106,-70 L -6,-70 Z" fill="#e8434e"/>
    <path d="M -80,-96 L -54,-96 L -54,-62 L -80,-62 Z" fill="#c8243a"/><path d="M -84,-66 L -50,-66 L -50,-60 L -84,-60 Z" fill="#a81a2a"/>
    <path d="M 0,-100 L 100,-100" stroke="#d8dde6" stroke-width="3"/><path d="M 100,-100 L 112,-62" stroke="#d8dde6" stroke-width="3"/>
    <path d="M -10,-186 L -10,-62 M 108,-184 L 108,-62 M -56,-186 L -56,-96" stroke="#d8dde6" stroke-width="4"/>
    <path d="M -126,-14 L -114,-14 L -118,-60 L -128,-60 Z" fill="#d8dde6"/><path d="M -138,-14 L -128,-14 L -130,-60 L -140,-60 Z" fill="#b8bec8"/>
    <circle cx="-128" cy="0" r="21" fill="#16161c"/><circle cx="-128" cy="0" r="11" fill="#d8325a"/><circle cx="-128" cy="0" r="4" fill="#d8dde6"/>
    <path d="M -156,-22 C -156,-40 -104,-40 -100,-24 L -108,-22 C -112,-32 -148,-32 -148,-20 Z" fill="#1f5fbf"/><path d="M -156,-22 C -156,-30 -150,-36 -140,-38" stroke="#d8dde6" stroke-width="2" fill="none"/>
    <path d="M -136,-60 C -146,-80 -146,-110 -138,-130 L -96,-130 L -96,-60 Z" fill="#f4f4f6"/><path d="M -136,-60 C -146,-80 -146,-110 -138,-130 L -126,-130 C -132,-110 -132,-80 -124,-60 Z" fill="#ffffff"/>
    <path d="M -140,-100 L -96,-100 L -96,-90 L -142,-88 Z" fill="#1f5fbf"/><path d="M -142,-78 L -96,-78" stroke="#d8325a" stroke-width="2"/>
    <circle cx="-142" cy="-114" r="11" fill="#d8dde6"/><circle cx="-143" cy="-114" r="7.4" fill="#fff6d0"/><circle cx="-145" cy="-116" r="2.4" fill="#ffffff"/>
    <circle cx="-138" cy="-72" r="5" fill="#d8dde6"/><circle cx="-139" cy="-72" r="3" fill="#ffd27a"/>
    <path d="M -138,-130 L -132,-180 L -100,-180 L -96,-130 Z" fill="#1a1a22"/><path d="M -134,-134 L -129,-176 L -104,-176 L -100,-134 Z" fill="#a8d4f0" opacity=".8"/><path d="M -129,-176 L -116,-176 L -132,-140 Z" fill="#e6f4fa" opacity=".8"/>
    <path d="M -136,-150 L -156,-160 L -158,-146 Z" fill="#1a1a22"/><rect x="-166" y="-170" width="12" height="18" rx="3" fill="#d8dde6"/>
    {"".join(f'<circle cx="{-134+k*9}" cy="-182" r="4" fill="#f0c040"/>' for k in range(4))}
    <path d="M -140,-186 C -60,-206 60,-204 118,-188 L 120,-180 C 60,-194 -60,-196 -142,-178 Z" fill="#2f5ea8"/><path d="M -140,-186 C -60,-206 0,-205 40,-202 C -20,-198 -80,-192 -140,-180 Z" fill="#4a7ac4"/>
    {fringe}
    <rect x="-132" y="-214" width="58" height="20" rx="4" fill="#f4f4f6"/><rect x="-132" y="-214" width="58" height="5" rx="2" fill="#d8dde6"/><text x="-103" y="-199" text-anchor="middle" font-family="Inter" font-size="13" font-weight="800" fill="#1f3a7a">TAXI</text>
    <rect x="-14" y="-40" width="40" height="18" rx="2" fill="#f0c040"/><text x="6" y="-27" text-anchor="middle" {TH} font-size="10" font-weight="700" fill="#1a1a20">สก 5454</text>
    </g>'''

def tuk_driver(x, y, s=1.0):
    return f'''<g transform="translate({x},{y}) scale({s})"><path d="M -16,0 L 16,0 L 14,-40 C 8,-48 -8,-48 -14,-40 Z" fill="#2a5a8a"/><path d="M -12,-40 L 12,-40 L 10,-10 L -10,-10 Z" fill="#e8743a"/>
    <rect x="-5" y="-54" width="10" height="10" fill="#c48a5e"/><circle cx="0" cy="-64" r="14" fill="#c48a5e"/><path d="M -15,-66 C -14,-82 14,-82 15,-66 Z" fill="#c8243a"/><path d="M -4,-70 L -22,-68 L -15,-64 Z" fill="#c8243a"/>
    <circle cx="-5" cy="-62" r="3.6" fill="#fff"/><circle cx="5" cy="-62" r="3.6" fill="#fff"/><circle cx="-6" cy="-62" r="1.6" fill="#1a1a20"/><circle cx="4" cy="-62" r="1.6" fill="#1a1a20"/><ellipse cx="0" cy="-53" rx="3.4" ry="3" fill="#7a2e2a"/>
    <path d="M -20,-30 L -34,-34" stroke="#c48a5e" stroke-width="5" stroke-linecap="round"/></g>'''
