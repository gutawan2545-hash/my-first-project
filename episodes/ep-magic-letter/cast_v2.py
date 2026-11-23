# สร้าง cast.html: ภาพร่างตัวละครใหม่ของตอนจดหมายโรงเรียนเวทมนตร์
# ลายเส้นตาม CLAUDE.md: cut-out ไม่มีเส้นขอบ เงาบล็อก 2-3 ระดับ แสงจากซ้าย พื้น #1b1f2b
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).with_name("cast.html")

def grab(path, start_marker, prefix, feet):
    s = (ROOT / "characters" / path).read_text()
    defs = s[s.index("<defs>") + 6: s.index("</defs>")]
    i = s.index(start_marker) + len(start_marker)
    j = s.index("</g>\n      </svg>", i)
    body = s[i:j]
    def ren(t):
        t = re.sub(r'id="([^"]+)"', lambda m: f'id="{prefix}{m.group(1)}"', t)
        t = re.sub(r'url\(#([^)]+)\)', lambda m: f'url(#{prefix}{m.group(1)})', t)
        t = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{prefix}{m.group(1)}"', t)
        return t
    return ren(defs), f'<g id="{prefix}full"><g transform="translate(0,{-feet})">{ren(body)}</g></g>'

jdefs, jfull = grab("james.html", '<g transform="translate(200,130) scale(1.4)">', "j_", 495)
tdefs, tfull = grab("tawan.html", '<g transform="translate(200,138) scale(1.4)">', "t_", 489)

FACE = "M -32,-14 C -32,-46 32,-46 32,-14 L 31,6 C 29,22 13,37 0,40 C -13,37 -29,22 -31,6 Z"

def face(p, sk, sh, hl, dp, neck_sh=None):
    """หน้าพื้นฐาน + เงาบล็อก (ขมับ ข้างจมูก แก้มขวา ใต้คาง) แสงจากซ้าย"""
    return f'''
    <clipPath id="{p}face"><path d="{FACE}"/></clipPath>
    <rect x="-9" y="20" width="18" height="38" fill="{sk}"/>
    <path d="M -9,26 L 9,26 L 9,46 Q 0,41 -9,49 Z" fill="{neck_sh or sh}"/>
    <path d="{FACE}" fill="{sk}"/>
    <g clip-path="url(#{p}face)">
      <path d="M 16,-34 C 30,-28 34,-14 32,4 C 30,22 14,37 0,40 C 11,32 19,20 20,4 C 21,-10 19,-22 16,-34 Z" fill="{sh}"/>
      <path d="M 34,-26 L 22,-26 L 25,-6 L 34,-4 Z" fill="{dp}"/>
      <path d="M -33,-12 C -33,-30 -28,-38 -22,-41 C -28,-32 -29,-20 -29,-10 L -28,6 C -27,18 -21,28 -15,34 C -23,30 -29,20 -31,6 Z" fill="{hl}"/>
      <path d="M 2,3 L 6.5,15 L 1,17 Z" fill="{sh}"/>
    </g>'''

def blush(c="#e99a86", o=.35):
    return f'<ellipse cx="-18" cy="12" rx="6" ry="3.2" fill="{c}" opacity="{o}"/><ellipse cx="18" cy="12" rx="6" ry="3.2" fill="{c}" opacity="{o}"/>'

def eyes_round(p, iris="#3a2420", lash="#17151d", big=1.0):
    rx, ry = 6.2*big, 5.6*big
    out = ""
    for sx in (-1, 1):
        cx = 13*sx
        out += f'<clipPath id="{p}e{sx}"><ellipse cx="{cx}" cy="-1" rx="{rx}" ry="{ry}"/></clipPath>'
        out += f'<ellipse cx="{cx}" cy="-1" rx="{rx}" ry="{ry}" fill="{"#fbf6f0" if sx<0 else "#efe5da"}"/>'
        out += f'<g clip-path="url(#{p}e{sx})"><circle cx="{cx}" cy="-0.2" r="{4.6*big}" fill="{iris}"/><circle cx="{cx}" cy="-0.2" r="{2.2*big}" fill="#140c0b"/><circle cx="{cx-1.8}" cy="-2.2" r="{1.5*big}" fill="#fff"/><circle cx="{cx+1.6}" cy="1.6" r=".7" fill="#fff"/></g>'
        out += f'<path d="M {cx-rx-1},{-1} C {cx-rx},{-1-ry-2} {cx+rx},{-1-ry-2} {cx+rx+1},{-1} L {cx+rx},{-0.2} C {cx+rx-1},{-1-ry} {cx-rx+1},{-1-ry} {cx-rx},{-0.2} Z" fill="{lash}"/>'
    return out

def eyes_crinkle(col="#2a1d1a"):
    # ตายิ้มปิด แบบคนแก่ใจดี + ตีนกา
    return f'''<path d="M -21,-1 Q -13,-8 -5,-1" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M 21,-1 Q 13,-8 5,-1" fill="none" stroke="{col}" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M -24,-3 L -27,-5 M -24,0 L -27.5,0.5 M 24,-3 L 27,-5 M 24,0 L 27.5,0.5" stroke="{col}" stroke-opacity=".45" stroke-width="1" stroke-linecap="round"/>'''

def eyes_stern(p, iris="#2a1d1a", lid="#2a1d1a"):
    out = ""
    for sx in (-1, 1):
        cx = 13*sx
        shape = f"M {cx-8*sx},-1 C {cx-5*sx},-5 {cx+4*sx},-5.5 {cx+8*sx},-2.5 C {cx+5*sx},1.5 {cx-4*sx},1.8 {cx-8*sx},-1 Z"
        out += f'<clipPath id="{p}s{sx}"><path d="{shape}"/></clipPath><path d="{shape}" fill="#f7f0e8"/>'
        out += f'<g clip-path="url(#{p}s{sx})"><circle cx="{cx}" cy="-1.2" r="3.4" fill="{iris}"/><circle cx="{cx-1.2}" cy="-2.2" r=".9" fill="#fff"/><rect x="{cx-10}" y="-8" width="20" height="5.4" fill="{lid}" opacity=".9"/></g>'
    return out

def eyes_squint(col="#1d1717"):
    return f'''<path d="M -20,-2 C -15,-4.5 -10,-4.5 -6,-2 C -10,-0.6 -15,-0.6 -20,-2 Z" fill="#f2e9df"/><circle cx="-13" cy="-2.1" r="1.9" fill="{col}"/>
    <path d="M 20,-2 C 15,-4.5 10,-4.5 6,-2 C 10,-0.6 15,-0.6 20,-2 Z" fill="#e6dccf"/><circle cx="13" cy="-2.1" r="1.9" fill="{col}"/>
    <path d="M -21,-2.6 C -15,-6 -10,-6 -5,-2.6 M 21,-2.6 C 15,-6 10,-6 5,-2.6" fill="none" stroke="{col}" stroke-width="1.8"/>'''

# ---------- ชุดคลุมโรงเรียน ----------
def robe(c, light, shade, trim, inner, hem=455, w=62):
    return f'''
    <path d="M -47,64 L -36,74 L -44,196 L -76,206 C -78,170 -66,110 -47,64 Z" fill="{light}"/>
    <path d="M 47,64 L 36,74 L 44,196 L 76,206 C 78,170 66,110 47,64 Z" fill="{shade}"/>
    <path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L {w},{hem} L {-w},{hem} L -47,66 C -42,56 -28,51 -12,49 Z" fill="{c}"/>
    <path d="M -47,66 C -42,56 -28,51 -18,50 C -28,120 -34,300 -38,{hem} L {-w},{hem} Z" fill="{light}"/>
    <path d="M 20,50 C 32,53 43,58 47,66 L {w},{hem} L 38,{hem} C 34,300 30,120 20,50 Z" fill="{shade}"/>
    <path d="M -11,52 L 11,52 L 9,{hem} L -9,{hem} Z" fill="{inner}"/>
    <path d="M -13,50 L -8,50 L -6,{hem} L -12,{hem} Z" fill="{trim}"/>
    <path d="M 13,50 L 8,50 L 6,{hem} L 12,{hem} Z" fill="{trim}" opacity=".8"/>
    <path d="M {-w},{hem-6} L {w},{hem-6} L {w},{hem} L {-w},{hem} Z" fill="{trim}" opacity=".85"/>
    <path d="M -76,206 L -44,196 L -45,202 L -75,212 Z" fill="{trim}"/>
    <path d="M 76,206 L 44,196 L 45,202 L 75,212 Z" fill="{trim}" opacity=".8"/>'''

def hand(x, y, sk, sh, flip=1):
    return f'<path d="M {x-7},{y} L {x+7},{y} C {x+8},{y+12} {x+5},{y+22} {x},{y+23} C {x-5},{y+22} {x-8},{y+12} {x-7},{y} Z" fill="{sk if flip<0 else sh}"/>'

def shoes(c, cl, y):
    return f'''<path d="M -40,{y} L -8,{y} C -6,{y+8} -8,{y+13} -12,{y+14} L -42,{y+14} C -46,{y+13} -45,{y+4} -40,{y} Z" fill="{cl}"/>
    <path d="M 40,{y} L 8,{y} C 6,{y+8} 8,{y+13} 12,{y+14} L 42,{y+14} C 46,{y+13} 45,{y+4} 40,{y} Z" fill="{c}"/>'''

ROBE = dict(c="#352f57", light="#4a4378", shade="#231f3d", trim="#b7a0e0")  # ชุดคลุมโรงเรียนยามวิกาล: ม่วงคราม ขอบลาเวนเดอร์

C = {}

# 1 อาจารย์ใหญ่ทองหล่อ
sk, sh, hl, dp = "#f2cfae", "#dcae8c", "#fbe3cb", "#c4977a"
C["head"] = f'''<g id="c_head"><g transform="translate(0,-482)">
  <path d="M -6,470 L -6,-0" />
  <path d="M -72,214 L -66,214 L -60,470 L -66,470 Z" fill="#8a5a36"/><path d="M -69,214 L -66,214 L -61,470 L -64,470 Z" fill="#a8744a"/>
  <circle cx="-68" cy="206" r="9" fill="#c9a24a"/><circle cx="-70" cy="204" r="3.5" fill="#f3dc94"/>
  {robe("#2f5a55","#3f736c","#1f3e3a","#c9a24a","#e9dfd2",hem=468,w=64)}
  <path d="M -44,60 L -30,52 L 40,236 L 26,246 Z" fill="#b5434a"/>
  <g fill="#e9dfd2" opacity=".85"><path d="M -36,74 L -28,70 L -22,86 L -30,90 Z"/><path d="M -16,126 L -8,122 L -2,138 L -10,142 Z"/><path d="M 4,178 L 12,174 L 18,190 L 10,194 Z"/><path d="M 24,226 L 32,222 L 36,234 L 28,238 Z"/></g>
  <path d="M -30,52 L -24,50 L 44,232 L 40,236 Z" fill="#7e2c33"/>
  {hand(-60,206,sk,sh,-1)}{hand(60,206,sk,sh)}
  {shoes("#4a3424","#5e4430",466)}
  <g transform="translate(0,0)">
  {face("hd",sk,sh,hl,dp)}
  <path d="M -33,-20 C -38,10 -36,40 -30,60 L -20,58 C -26,30 -28,0 -26,-20 Z" fill="#e2ddd6"/>
  <path d="M 33,-20 C 38,10 36,40 30,60 L 20,58 C 26,30 28,0 26,-20 Z" fill="#c8c2ba"/>
  <path d="M -30,2 C -26,24 -14,36 0,38 C 14,36 26,24 30,2 C 32,40 22,90 6,150 L 0,140 L -6,150 C -22,90 -32,40 -30,2 Z" fill="#ece8e2"/>
  <path d="M 4,40 C 16,36 26,24 30,2 C 32,40 22,90 6,150 L 0,140 C 6,100 8,70 4,40 Z" fill="#cfc9c2"/>
  <path d="M -24,20 C -20,50 -12,90 -4,130 L -8,128 C -18,90 -26,50 -24,20 Z" fill="#fbf9f6"/>
  <path d="M -14,22 C -8,18 8,18 14,22 C 8,24 3,23 0,26 C -3,23 -8,24 -14,22 Z" fill="#fbf9f6"/>
  <path d="M -9,27 Q 0,31 9,27 Q 0,34 -9,27 Z" fill="#a8665a"/>
  {eyes_crinkle()}
  <path d="M -24,-12 C -18,-18 -10,-18 -4,-12 C -10,-14 -18,-13 -24,-9 Z" fill="#f2efea"/><path d="M 24,-12 C 18,-18 10,-18 4,-12 C 10,-14 18,-13 24,-9 Z" fill="#d6d1ca"/>
  <g fill="#ffffff" fill-opacity=".08" stroke="#7a5230" stroke-width="2.4"><circle cx="-13" cy="-2" r="8.6"/><circle cx="13" cy="-2" r="8.6"/></g>
  <path d="M -4.4,-3 Q 0,-6 4.4,-3" fill="none" stroke="#7a5230" stroke-width="2.2"/>
  {blush("#e08a78",.3)}
  <path d="M -30,-30 C -24,-46 24,-46 30,-30 C 20,-38 -20,-38 -30,-30 Z" fill="{hl}"/>
  <path d="M -6,-44 C -2,-56 6,-58 10,-50 C 6,-52 2,-50 0,-44 Z" fill="#ece8e2"/>
  </g></g></g>'''

# 2 ครูมาลัย (เข้มงวด)
sk, sh, hl, dp = "#f5d6b8", "#e0b493", "#fde6cf", "#c99a7a"
C["strict"] = f'''<g id="c_strict"><g transform="translate(0,-482)">
  {robe("#4a2f6b","#61418a","#33204c","#e0c27a","#f1ebe2",hem=468,w=58)}
  <circle cx="-22" cy="80" r="5" fill="#e0c27a"/><circle cx="-23" cy="79" r="2" fill="#fff3cc"/>
  <path d="M 58,206 L 104,58 L 107,59 L 62,210 Z" fill="#9a6a3c"/>
  {hand(-60,206,sk,sh,-1)}{hand(60,206,sk,sh)}
  {shoes("#2a2030","#3a2e42",466)}
  {face("st",sk,sh,hl,dp)}
  <path d="M -34,-6 C -40,-40 -20,-58 0,-58 C 20,-58 40,-40 34,-6 L 30,-22 C 22,-36 10,-40 0,-40 C -10,-40 -22,-36 -30,-22 Z" fill="#2a2228"/>
  <path d="M -30,-34 C -22,-50 -8,-56 4,-56 C -8,-50 -18,-42 -24,-28 Z" fill="#8a8490"/>
  <path d="M -18,-56 C -20,-80 -6,-92 0,-92 C 6,-92 20,-80 18,-56 Z" fill="#2a2228"/>
  <path d="M -16,-62 C -16,-80 -6,-88 -1,-88 C -6,-80 -8,-70 -8,-58 Z" fill="#433840"/>
  <rect x="-18" y="-60" width="36" height="5" rx="2" fill="#e0c27a"/>
  {eyes_stern("st")}
  <path d="M -23,-11 L -6,-7.5 L -6,-5 L -23,-8.5 Z" fill="#2a2228"/><path d="M 23,-11 L 6,-7.5 L 6,-5 L 23,-8.5 Z" fill="#2a2228"/>
  <g fill="#fff" fill-opacity=".07" stroke="#8e1b24" stroke-width="1.8"><rect x="-22" y="-8" width="18" height="12" rx="2"/><rect x="4" y="-8" width="18" height="12" rx="2"/></g>
  <path d="M -4,-3 L 4,-3 M -22,-4 L -31,-6 M 22,-4 L 31,-6" stroke="#8e1b24" stroke-width="1.6"/>
  {blush("#e08a86",.25)}
  <path d="M -7,25 L 7,25" stroke="#a86068" stroke-width="2" stroke-linecap="round"/>
  </g></g>'''

# 3 ป้าแช่ม ครูปรุงยา
sk, sh, hl, dp = "#e9bf98", "#d09f78", "#f4d2b0", "#b88864"
C["potion"] = f'''<g id="c_potion"><g transform="translate(0,-482)">
  <path d="M -47,64 L -36,74 L -50,190 L -80,200 C -84,160 -70,104 -47,64 Z" fill="#874049"/>
  <path d="M 47,64 L 36,74 L 50,190 L 80,200 C 84,160 70,104 47,64 Z" fill="#4e2028"/>
  <path d="M -14,49 L 14,49 C 40,52 62,70 70,120 C 78,200 76,330 66,468 L -66,468 C -76,330 -78,200 -70,120 C -62,70 -40,52 -14,49 Z" fill="#6b2f35"/>
  <path d="M -70,120 C -62,70 -40,52 -22,50 C -40,110 -48,300 -46,468 L -66,468 C -76,330 -78,200 -70,120 Z" fill="#874049"/>
  <path d="M 24,50 C 46,56 64,74 70,120 C 78,200 76,330 66,468 L 44,468 C 48,300 44,120 24,50 Z" fill="#4e2028"/>
  <path d="M -40,96 L 40,96 C 50,200 52,330 46,440 L -46,440 C -52,330 -50,200 -40,96 Z" fill="#e8dcc8"/>
  <path d="M 20,96 L 40,96 C 50,200 52,330 46,440 L 30,440 C 34,300 30,180 20,96 Z" fill="#cfc0a8"/>
  <path d="M -40,96 L -30,96 C -36,200 -38,330 -34,440 L -46,440 C -52,330 -50,200 -40,96 Z" fill="#f5ecdd"/>
  <g fill="#7bb36a"><circle cx="-14" cy="250" r="5"/><circle cx="8" cy="290" r="3.5"/><circle cx="-20" cy="330" r="2.8"/><circle cx="16" cy="210" r="2.4"/></g>
  <circle cx="-2" cy="270" r="4" fill="#b18cff" opacity=".8"/>
  <path d="M -40,96 L -30,58 M 40,96 L 30,58" stroke="#e8dcc8" stroke-width="5"/>
  <g transform="translate(-74,214) rotate(-8)">
    <path d="M -26,-6 L 26,-6 C 24,14 12,24 0,24 C -12,24 -24,14 -26,-6 Z" fill="#7a4a2c"/>
    <path d="M -26,-6 L -12,-6 C -10,10 -6,20 0,24 C -12,24 -24,14 -26,-6 Z" fill="#94603a"/>
    <rect x="-28" y="-10" width="56" height="6" rx="3" fill="#5e381f"/>
    <rect x="-6" y="24" width="12" height="6" fill="#5e381f"/>
  </g>
  {hand(-60,200,sk,sh,-1)}
  <path d="M 64,170 L 70,168 L 96,232 L 88,236 Z" fill="#94603a"/><circle cx="66" cy="166" r="8" fill="#7a4a2c"/>
  {hand(64,200,sk,sh)}
  {shoes("#c07a4a","#d08e5c",466)}
  {face("pt",sk,sh,hl,dp)}
  <g fill="#3a2a2a"><circle cx="-30" cy="-26" r="11"/><circle cx="-20" cy="-40" r="12"/><circle cx="-4" cy="-46" r="12"/><circle cx="12" cy="-44" r="12"/><circle cx="26" cy="-34" r="11"/><circle cx="33" cy="-18" r="9"/><circle cx="-35" cy="-10" r="8"/></g>
  <g fill="#5a4444"><circle cx="-22" cy="-42" r="5"/><circle cx="-6" cy="-49" r="4.5"/><circle cx="-32" cy="-28" r="4"/></g>
  <g fill="#241a1a"><circle cx="28" cy="-30" r="5"/><circle cx="33" cy="-15" r="4"/></g>
  {eyes_crinkle("#2a1a16")}
  <path d="M -22,-10 Q -14,-15 -6,-11" fill="none" stroke="#3a2a2a" stroke-width="2.4" stroke-linecap="round"/><path d="M 22,-10 Q 14,-15 6,-11" fill="none" stroke="#3a2a2a" stroke-width="2.4" stroke-linecap="round"/>
  {blush("#e0786a",.45)}
  <path d="M -11,22 Q 0,34 11,22 Z" fill="#8e3e3e"/><path d="M -9,22.5 L 9,22.5 L 8,25 L -8,25 Z" fill="#fff8ee"/>
  <circle cx="-34" cy="8" r="2.6" fill="#e0c27a"/><circle cx="34" cy="8" r="2.6" fill="#c9a24a"/>
  </g></g>'''

# 4 ลุงโต ภารโรงร่างยักษ์
sk, sh, hl, dp = "#d9a57c", "#bb875f", "#e8bb93", "#a37552"
C["giant"] = f'''<g id="c_giant"><g transform="scale(1.32) translate(0,-490)">
  <path d="M 72,40 L 78,40 L 80,440 L 74,440 Z" fill="#8a6a3c"/>
  <path d="M 64,430 L 90,430 L 104,488 L 52,488 Z" fill="#c8a868"/><path d="M 78,430 L 90,430 L 104,488 L 82,488 Z" fill="#a8884e"/>
  <path d="M -44,246 L 44,246 L 46,300 L 40,452 L 8,452 L 2,300 L -2,300 L -8,452 L -40,452 L -46,300 Z" fill="#2a2b30"/>
  <path d="M -44,246 L -26,246 L -30,300 L -28,452 L -40,452 L -46,300 Z" fill="#3a3c44"/>
  <path d="M -46,440 L -6,440 L -6,488 L -48,488 Z" fill="#1d2b22"/><path d="M 6,440 L 46,440 L 48,488 L 6,488 Z" fill="#14201a"/>
  <path d="M -60,110 L -44,116 L -44,240 L -62,240 Z" fill="#33456d"/><path d="M 60,110 L 44,116 L 44,240 L 62,240 Z" fill="#1d2a48"/>
  {hand(-53,238,sk,sh,-1)}
  <path d="M 64,234 L 82,234 C 84,250 80,262 72,262 C 64,262 62,250 64,234 Z" fill="{sh}"/>
  <path d="M -14,49 L 14,49 C 34,51 54,58 60,72 L 62,116 L 46,122 L 48,250 L -48,250 L -46,122 L -62,116 L -60,72 C -54,58 -34,51 -14,49 Z" fill="#2a3a5c"/>
  <path d="M -60,72 C -54,58 -34,51 -20,50 C -30,80 -34,140 -32,250 L -48,250 L -46,122 L -62,116 Z" fill="#3b4f7a"/>
  <path d="M 22,50 C 38,53 54,60 60,72 L 62,116 L 46,122 L 48,250 L 30,250 C 32,180 32,100 22,50 Z" fill="#1b2742"/>
  <path d="M -6,52 L 6,52 L 4,250 L -4,250 Z" fill="#1b2742"/>
  <g fill="#e9dfd2"><circle cx="0" cy="96" r="2.2"/><circle cx="0" cy="140" r="2.2"/><circle cx="0" cy="184" r="2.2"/></g>
  <path d="M -50,222 L 50,222 L 50,248 L -50,248 Z" fill="#4f8a5a"/>
  <g fill="#b5434a"><rect x="-44" y="222" width="10" height="26"/><rect x="-18" y="222" width="10" height="26"/><rect x="8" y="222" width="10" height="26"/><rect x="34" y="222" width="10" height="26"/></g>
  <path d="M -50,236 L 50,236 L 50,240 L -50,240 Z" fill="#e9dfd2" opacity=".5"/>
  <path d="M 30,248 L 42,248 L 46,286 L 34,284 Z" fill="#4f8a5a"/>
  <g transform="translate(0,4) scale(1.12)">
  {face("gt",sk,sh,hl,dp)}
  <path d="M -34,-8 C -38,-40 -20,-52 0,-52 C 20,-52 38,-40 34,-8 L 30,-26 L 24,-20 L 20,-32 L 10,-26 L 0,-34 L -10,-26 L -20,-32 L -24,-20 L -30,-26 Z" fill="#1d1a1e"/>
  <path d="M -28,-36 C -20,-46 -8,-50 2,-50 C -8,-44 -16,-38 -22,-30 Z" fill="#3a3640"/>
  {eyes_squint()}
  <path d="M -24,-11 L -5,-10 L -5,-6 L -23,-6.5 Z M 24,-11 L 5,-10 L 5,-6 L 23,-6.5 Z" fill="#1d1a1e"/>
  <path d="M -16,18 C -10,14 -4,15 0,17 C 4,15 10,14 16,18 C 12,22 6,21 0,20 C -6,21 -12,22 -16,18 Z" fill="#1d1a1e"/>
  <path d="M -24,14 C -18,30 -8,36 0,38 C 8,36 18,30 24,14 C 22,26 14,36 0,40 C -14,36 -22,26 -24,14 Z" fill="#a37552" opacity=".45"/>
  <path d="M -7,25 Q 0,30 7,25" fill="none" stroke="#7a4036" stroke-width="2" stroke-linecap="round"/>
  {blush("#c9705e",.3)}
  </g></g></g>'''

# 5 น้องภูมิ ปี 1 (ชาย 11 ขวบ)
sk, sh, hl, dp = "#f3cfa8", "#dcae86", "#fde3c6", "#c99a72"
def kid_body(extra_hand_r="", tie="#8e1b24", stripe=None, sy=0.8, extra_hand_l=""):
    st = f'<path d="M -5,70 L 5,64 L 5,70 L -5,76 Z M -4,96 L 4,90 L 4,96 L -4,102 Z M -3,120 L 3,114 L 3,120 L -3,126 Z" fill="{stripe}"/>' if stripe else ""
    return f'''<g transform="translate(0,6) scale(0.86,{sy})">
    {robe(**ROBE, inner="#f1ebe2", hem=455, w=56)}
    <path d="M -6,52 L 6,52 L 4,130 L 0,138 L -4,130 Z" fill="{tie}"/>{st}
    {extra_hand_l or hand(-60,206,sk,sh,-1)}{extra_hand_r or hand(60,206,sk,sh)}
    {shoes("#2a2830","#3a3842",453)}
    <path d="M -42,465 L -6,465 L -6,467 L -42,467 Z M 6,465 L 42,465 L 42,467 L 6,467 Z" fill="#b7a0e0"/>
    </g>'''
C["kidboy"] = f'''<g id="c_kidboy"><g transform="translate(0,-385)">
  {kid_body(f'<g transform="translate(60,206)"><rect x="-4" y="6" width="34" height="46" rx="4" fill="#1e2230"/><rect x="0" y="10" width="26" height="36" rx="2" fill="#6f8fd6"/><path d="M 0,10 L 26,10 L 0,40 Z" fill="#8fa9e6"/>{hand(0,0,sk,sh)}</g>')}
  <g transform="scale(1.18)">
  {face("kb",sk,sh,hl,dp)}
  <path d="M -34,-8 C -38,-50 38,-50 34,-8 L 31,-18 L 26,-24 L 16,-22 L 8,-26 L 0,-23 L -8,-26 L -16,-22 L -26,-24 L -31,-18 Z" fill="#221c20"/>
  <path d="M -30,-24 C -26,-40 -12,-46 2,-46 C -10,-40 -20,-34 -24,-24 Z" fill="#4a4048"/>
  {eyes_round("kb", big=1.08)}
  <path d="M -22,-12 Q -14,-15 -6,-12.5 L -6,-10.5 Q -14,-13 -22,-10 Z M 22,-12 Q 14,-15 6,-12.5 L 6,-10.5 Q 14,-13 22,-10 Z" fill="#221c20"/>
  {blush("#ef8f7e",.45)}
  <path d="M -10,21 Q 0,32 10,21 Z" fill="#8a3a3a"/><path d="M -8,21.5 L -1,21.5 L -1,24.5 L -7,24 Z M 2,21.5 L 8,21.5 L 7,24 L 2,24.5 Z" fill="#fff8ee"/>
  </g></g></g>'''

# 6 น้องใบเตย ปี 1 (หญิง 11 ขวบ ยกมือตอบทุกข้อ)
sk, sh, hl, dp = "#f7d6b3", "#e2b48f", "#fde6cf", "#cc9e7c"
C["kidgirl"] = f'''<g id="c_kidgirl"><g transform="translate(0,-385)">
  <g transform="translate(0,6) scale(0.86,0.8)">
    <path d="M -47,64 L -36,74 L -44,196 L -76,206 C -78,170 -66,110 -47,64 Z" fill="{ROBE['light']}"/>
    <path d="M 40,60 L 50,74 L 74,-60 L 56,-66 Z" fill="{ROBE['shade']}"/>
    <path d="M 56,-66 L 74,-60 L 73,-54 L 55,-60 Z" fill="{ROBE['trim']}"/>
    <path d="M 58,-64 L 72,-60 C 74,-74 72,-90 66,-92 C 60,-92 56,-78 58,-64 Z" fill="{sh}"/>
    <path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L 56,455 L -56,455 L -47,66 C -42,56 -28,51 -12,49 Z" fill="{ROBE['c']}"/>
    <path d="M -47,66 C -42,56 -28,51 -18,50 C -28,120 -34,300 -38,455 L -56,455 Z" fill="{ROBE['light']}"/>
    <path d="M 20,50 C 32,53 43,58 47,66 L 56,455 L 38,455 C 34,300 30,120 20,50 Z" fill="{ROBE['shade']}"/>
    <path d="M -11,52 L 11,52 L 9,455 L -9,455 Z" fill="#f1ebe2"/>
    <path d="M -13,50 L -8,50 L -6,455 L -12,455 Z M 13,50 L 8,50 L 6,455 L 12,455 Z M -56,449 L 56,449 L 56,455 L -56,455 Z" fill="{ROBE['trim']}"/>
    <path d="M -6,52 L 6,52 L 4,130 L 0,138 L -4,130 Z" fill="#8e1b24"/>
    <path d="M -76,206 L -44,196 L -45,202 L -75,212 Z" fill="{ROBE['trim']}"/>
    <g transform="translate(-62,186) rotate(-6)"><rect x="-6" y="0" width="40" height="52" rx="3" fill="#7a2f3a"/><rect x="-6" y="0" width="6" height="52" fill="#5a1f2a"/><rect x="4" y="10" width="22" height="6" fill="#e0c27a"/><rect x="32" y="2" width="3" height="48" fill="#efe5d2"/></g>
    {hand(-60,206,sk,sh,-1)}
    {shoes("#e9a8b8","#f4c2ce",453)}
  </g>
  <g transform="scale(1.18)">
  <path d="M -36,-10 C -42,30 -38,52 -30,56 L 30,56 C 38,52 42,30 36,-10 Z" fill="#1c1418"/>
  {face("kg",sk,sh,hl,dp)}
  <path d="M -36,-6 C -42,-50 42,-50 36,-6 L 30,-12 L 28,-22 L 18,-18 L 10,-24 L 0,-18 L -10,-24 L -18,-18 L -28,-22 L -30,-12 Z" fill="#1c1418"/>
  <path d="M -30,-30 C -22,-42 -8,-46 4,-46 C -8,-40 -18,-34 -24,-24 Z" fill="#3a2e36"/>
  <circle cx="-38" cy="-30" r="7" fill="#1c1418"/><circle cx="38" cy="-30" r="7" fill="#120c10"/>
  <circle cx="-33" cy="-34" r="3" fill="#7fb59a"/><circle cx="33" cy="-34" r="3" fill="#6a9e86"/>
  {eyes_round("kg", iris="#4a2a1f", big=1.12)}
  <path d="M -21,-14 Q -14,-17 -7,-14 L -7,-12.6 Q -14,-15 -21,-12.6 Z M 21,-14 Q 14,-17 7,-14 L 7,-12.6 Q 14,-15 21,-12.6 Z" fill="#1c1418"/>
  {blush("#f08a8a",.45)}
  <path d="M -7,22 Q 0,29 7,22 Z" fill="#b0545a"/>
  </g></g></g>'''

# 7 พี่ฮูก นกฮูกส่งจดหมาย (ง่วง เหนื่อยจากรอบส่งดึก)
C["owl"] = '''<g id="c_owl"><g transform="translate(0,-96)">
  <path d="M -14,92 L -4,92 L -6,98 L -16,98 Z M 4,92 L 14,92 L 16,98 L 6,98 Z" fill="#d9a24a"/>
  <path d="M -34,20 C -40,60 -30,92 0,94 C 30,92 40,60 34,20 C 30,-10 -30,-10 -34,20 Z" fill="#8a6a4a"/>
  <path d="M -20,20 C -24,56 -14,86 0,88 C 14,86 24,56 20,20 Z" fill="#d8c3a0"/>
  <g fill="#b8a07a"><path d="M -10,40 l 4,4 l 4,-4 z"/><path d="M 4,40 l 4,4 l 4,-4 z"/><path d="M -4,56 l 4,4 l 4,-4 z"/><path d="M -12,70 l 4,4 l 4,-4 z"/><path d="M 6,70 l 4,4 l 4,-4 z"/></g>
  <path d="M -34,20 C -46,40 -44,74 -30,88 C -28,64 -26,40 -22,24 Z" fill="#a6825a"/>
  <path d="M 34,20 C 46,40 44,74 30,88 C 28,64 26,40 22,24 Z" fill="#5e4630"/>
  <path d="M 22,30 L 40,62 L 30,70 L 14,36 Z" fill="#6b5a3a"/>
  <rect x="26" y="58" width="22" height="18" rx="3" fill="#6b5a3a"/><rect x="26" y="58" width="22" height="7" rx="2" fill="#544628"/>
  <path d="M 30,68 L 44,68 L 44,74 L 30,74 Z" fill="#efe3c8"/><circle cx="37" cy="66" r="2.2" fill="#8e1b24"/>
  <path d="M -38,-18 C -40,-40 40,-40 38,-18 C 40,10 20,22 0,22 C -20,22 -40,10 -38,-18 Z" fill="#8a6a4a"/>
  <path d="M -38,-18 C -40,-34 -20,-40 -8,-38 C -24,-30 -30,-14 -26,8 C -34,2 -40,-6 -38,-18 Z" fill="#a6825a"/>
  <path d="M 20,-38 C 36,-34 40,-26 38,-18 C 40,4 28,16 14,20 C 26,8 28,-16 20,-38 Z" fill="#5e4630"/>
  <path d="M -36,-28 L -44,-46 L -26,-36 Z" fill="#a6825a"/><path d="M 36,-28 L 44,-46 L 26,-36 Z" fill="#5e4630"/>
  <circle cx="-14" cy="-10" r="13" fill="#e8d8b8"/><circle cx="14" cy="-10" r="13" fill="#d8c3a0"/>
  <circle cx="-14" cy="-9" r="8" fill="#e0a43c"/><circle cx="14" cy="-9" r="8" fill="#e0a43c"/>
  <circle cx="-14" cy="-8" r="4.2" fill="#1a1210"/><circle cx="14" cy="-8" r="4.2" fill="#1a1210"/>
  <circle cx="-16" cy="-10" r="1.5" fill="#fff"/><circle cx="12" cy="-10" r="1.5" fill="#fff"/>
  <path d="M -23,-18 L -5,-18 L -5,-10 C -10,-12 -18,-12 -23,-10 Z" fill="#8a6a4a"/><path d="M 23,-18 L 5,-18 L 5,-10 C 10,-12 18,-12 23,-10 Z" fill="#7a5c3e"/>
  <path d="M -23,-10 C -18,-12 -10,-12 -5,-10" fill="none" stroke="#4a3626" stroke-width="1.6"/><path d="M 23,-10 C 18,-12 10,-12 5,-10" fill="none" stroke="#4a3626" stroke-width="1.6"/>
  <path d="M -4,0 L 4,0 L 0,9 Z" fill="#d9a24a"/>
  <path d="M -26,-30 C -26,-46 26,-46 26,-30 L 30,-26 L -30,-26 Z" fill="#c74a3a"/><path d="M -26,-30 C -26,-40 -10,-44 0,-44 C -12,-40 -18,-34 -18,-28 Z" fill="#e06a52"/>
  <rect x="-4" y="-44" width="8" height="16" fill="#efe3c8" opacity=".9"/>
  <ellipse cx="-24" cy="4" rx="5" ry="2.6" fill="#e99a86" opacity=".4"/><ellipse cx="24" cy="4" rx="5" ry="2.6" fill="#e99a86" opacity=".4"/>
  </g></g>'''

# 8 ลุงยามสมพงษ์
sk, sh, hl, dp = "#e2b48c", "#c99772", "#efc6a2", "#b0805c"
C["guard"] = f'''<g id="c_guard"><g transform="translate(0,-495)">
  <path d="M -41,228 L 41,228 L 44,300 L 37,462 L 9,462 L 2,292 L -2,292 L -9,462 L -37,462 L -44,300 Z" fill="#2a2f45"/>
  <path d="M -41,228 L -24,228 L -28,300 L -26,462 L -37,462 L -44,300 Z" fill="#3a4060"/>
  <path d="M 22,236 L 41,228 L 44,300 L 37,462 L 26,462 C 28,380 26,300 22,236 Z" fill="#1c2032"/>
  {shoes("#121318","#1e2028",470).replace('14}','14}')}
  <path d="M -40,470 L -8,470 L -8,481 L -42,481 Z" fill="#1e2028"/><path d="M 8,470 L 40,470 L 42,481 L 8,481 Z" fill="#121318"/>
  <path d="M -55,114 L -41,118 L -41,180 L -55,180 Z" fill="#e6e9ee"/><path d="M 55,114 L 41,118 L 41,180 L 55,180 Z" fill="#b7bcc6"/>
  <path d="M -55,150 L -41,150 L -40,230 L -54,230 Z" fill="{hl}"/>
  {hand(-48,228,sk,sh,-1)}
  <g transform="translate(26,118) rotate(-10)"><rect x="0" y="0" width="40" height="54" rx="3" fill="#8a6a3c"/><rect x="4" y="8" width="32" height="42" fill="#f4efe4"/><rect x="12" y="-3" width="16" height="7" rx="2" fill="#9aa0aa"/><g fill="#b7bcc6"><rect x="8" y="14" width="22" height="2.4"/><rect x="8" y="21" width="18" height="2.4"/><rect x="8" y="28" width="22" height="2.4"/></g><circle cx="26" cy="40" r="5" fill="none" stroke="#8e1b24" stroke-width="1.6"/></g>
  <path d="M 46,120 L 58,126 L 50,166 L 30,150 Z" fill="#b7bcc6"/>
  {hand(40,150,sk,sh)}
  <path d="M -12,49 L 12,49 C 28,51 42,56 47,66 L 57,116 L 40,122 L 42,234 L -42,234 L -40,122 L -57,116 L -47,66 C -42,56 -28,51 -12,49 Z" fill="#d9dde3"/>
  <path d="M -47,66 C -42,56 -28,51 -18,50 C -26,72 -30,110 -28,234 L -42,234 L -40,122 L -57,116 Z" fill="#eef0f3"/>
  <path d="M 20,50 C 32,53 43,58 47,66 L 57,116 L 40,122 L 42,234 L 26,234 C 28,180 28,100 20,50 Z" fill="#b7bcc6"/>
  <path d="M -42,222 L 42,222 L 42,234 L -42,234 Z" fill="#1c1d24"/><rect x="-7" y="221" width="14" height="14" rx="2" fill="#c9a24a"/>
  <path d="M -32,72 L -12,72 L -12,82 L -32,82 Z" fill="#2a2f45"/><path d="M 12,96 L 30,96 L 30,104 L 12,104 Z" fill="#c9a24a"/>
  <path d="M 16,60 C 10,90 4,110 -2,124" fill="none" stroke="#8e1b24" stroke-width="2"/><rect x="-8" y="122" width="10" height="6" rx="2" fill="#c4c8d4"/>
  <path d="M -12,49 L -2,72 L 0,58 L 2,72 L 12,49 Z" fill="#eef0f3"/>
  {face("gd",sk,sh,hl,dp)}
  <path d="M -32,-10 L -34,-24 L 34,-24 L 32,-10 L 28,-18 L -28,-18 Z" fill="#3a3a40"/><path d="M -32,-12 L -30,-22 L -26,-22 L -28,-12 Z M 32,-12 L 30,-22 L 26,-22 L 28,-12 Z" fill="#8a8a92"/>
  <path d="M -36,-22 C -36,-50 36,-50 36,-22 Z" fill="#2a2f45"/><path d="M -36,-22 C -36,-40 -20,-48 -4,-48 C -18,-42 -26,-34 -26,-22 Z" fill="#3a4060"/>
  <path d="M -38,-24 L 44,-24 C 46,-18 40,-14 30,-14 L -38,-18 Z" fill="#1c2032"/>
  <path d="M -6,-42 L 6,-42 L 8,-32 L 0,-28 L -8,-32 Z" fill="#c9a24a"/>
  {eyes_squint()}
  <path d="M -23,-12 L -6,-9 L -6,-6 L -23,-8.5 Z M 23,-12 L 6,-9 L 6,-6 L 23,-8.5 Z" fill="#26222a"/>
  <path d="M -12,18 C -6,15 6,15 12,18 L 10,21 C 4,19 -4,19 -10,21 Z" fill="#26222a"/>
  <path d="M -6,25.5 L 6,25.5" stroke="#8e4a42" stroke-width="2" stroke-linecap="round"/>
  {blush("#d07a68",.25)}
  </g></g>'''


GOLD, RED, GREEN, SILVER = "#d9b24a", "#8e1b24", "#2f6b4a", "#c4c8d4"

# 9 แฮร์รี่ (ล้อเลียน): ผมดำยุ่ง แว่นกลมกรอบดำหนา ตาเขียว แผลสายฟ้าที่หน้าผาก
sk, sh, hl, dp = "#f6dcc4", "#e2b89c", "#fdeadb", "#cc9e84"
C["harry"] = f'''<g id="c_harry"><g transform="translate(0,-385)">
  {kid_body(tie=RED, stripe=GOLD, extra_hand_r=f'<g transform="translate(60,206)"><path d="M 2,4 L 6,4 L 14,-70 L 11,-71 Z" fill="#6a4a2c"/><path d="M 11,-71 L 14,-70 L 13,-62 L 10,-63 Z" fill="#8a6a44"/>{hand(0,0,sk,sh)}</g>')}
  <g transform="scale(1.18)">
  {face("hp",sk,sh,hl,dp)}
  {eyes_round("hp", iris="#3f8a4a", big=1.02)}
  <path d="M -22,-12 Q -14,-15 -6,-12.5 L -6,-10.5 Q -14,-13 -22,-10 Z M 22,-12 Q 14,-15 6,-12.5 L 6,-10.5 Q 14,-13 22,-10 Z" fill="#141217"/>
  <path d="M -36,-6 C -44,-40 -26,-58 -4,-58 L 0,-64 L 6,-57 L 14,-62 L 14,-55 C 30,-52 44,-38 36,-6 L 32,-18 L 28,-12 L 25,-26 L 18,-14 L 13,-28 L 7,-16 L 2,-24 L -4,-15 L -10,-28 L -15,-14 L -20,-26 L -24,-12 L -30,-20 Z" fill="#141217"/>
  <path d="M -42,-30 L -34,-24 L -38,-12 Z M 42,-30 L 34,-24 L 38,-12 Z M -10,-62 L -4,-54 L -14,-54 Z" fill="#141217"/>
  <path d="M -26,-44 C -18,-52 -6,-56 4,-55 C -6,-50 -14,-44 -20,-36 Z" fill="#33303c"/>
  <path d="M 7,-16 L 2,-24 L -1,-17 Z" fill="#141217"/>
  <path d="M 6,-26 L 1,-20 L 4,-20 L -1,-13 L 7,-21 L 4,-21 L 8,-26 Z" fill="#c95a5a"/>
  <g fill="#ffffff" fill-opacity=".07" stroke="#1a1a1e" stroke-width="2.2"><circle cx="-13" cy="-1" r="9.4"/><circle cx="13" cy="-1" r="9.4"/></g>
  <path d="M -3.6,-2.4 Q 0,-4.6 3.6,-2.4 M -22.4,-2 L -31,-3.4 M 22.4,-2 L 31,-3.4" fill="none" stroke="#1a1a1e" stroke-width="2"/>
  <path d="M -21.6,-5 A 9.4,9.4 0 0 1 -14,-10.2" fill="none" stroke="#5a5a66" stroke-width="1.2"/>
  {blush("#ef8f7e",.38)}
  <path d="M -7,23 Q 0,27 7,23" fill="none" stroke="#a05a54" stroke-width="2" stroke-linecap="round"/>
  </g></g></g>'''

# 10 เฮอร์ไมโอนี่ (ล้อเลียน): ผมน้ำตาลฟูฟ่อง ฟันหน้าเด่นนิด ๆ กอดหนังสือกองโต
sk, sh, hl, dp = "#f7d9c0", "#e4b898", "#fde8d6", "#cfa080"
books = f'''<g transform="translate(-62,168)"><rect x="-26" y="0" width="52" height="16" rx="2" fill="#7a2f3a"/><rect x="-24" y="16" width="48" height="18" rx="2" fill="#2f4a6b"/><rect x="-28" y="34" width="56" height="16" rx="2" fill="#5a6b2f"/><rect x="-26" y="50" width="52" height="20" rx="2" fill="#6b4a2f"/><g fill="#e0c27a"><rect x="-10" y="6" width="20" height="3"/><rect x="-8" y="23" width="16" height="3"/><rect x="-12" y="40" width="24" height="3"/><rect x="-10" y="58" width="20" height="3"/></g><rect x="22" y="2" width="3" height="66" fill="#efe5d2" opacity=".7"/>{hand(-16,46,sk,sh,-1)}{hand(18,46,sk,sh)}</g>'''
C["hermione"] = f'''<g id="c_hermione"><g transform="translate(0,-385)">
  <g transform="scale(1.18)"><g fill="#6b4228"><circle cx="-34" cy="-20" r="20"/><circle cx="34" cy="-20" r="20"/><circle cx="-40" cy="8" r="20"/><circle cx="40" cy="8" r="20"/><circle cx="-36" cy="34" r="18"/><circle cx="36" cy="34" r="18"/><circle cx="-24" cy="50" r="14"/><circle cx="24" cy="50" r="14"/></g>
  <g fill="#4e2e1c"><circle cx="40" cy="8" r="12"/><circle cx="36" cy="34" r="11"/><circle cx="24" cy="50" r="8"/></g><g fill="#8a5a3a"><circle cx="-44" cy="0" r="8"/><circle cx="-38" cy="-26" r="7"/></g></g>
  {kid_body(tie=RED, stripe=GOLD, extra_hand_l=books, extra_hand_r=" ")}
  <g transform="scale(1.18)">
  {face("hg",sk,sh,hl,dp)}
  {eyes_round("hg", iris="#6b3e22", big=1.1)}
  <path d="M -21,-13 Q -14,-16 -7,-13 L -7,-11.6 Q -14,-14 -21,-11.6 Z M 21,-13 Q 14,-16 7,-13 L 7,-11.6 Q 14,-14 21,-11.6 Z" fill="#4e2e1c"/>
  <g fill="#6b4228"><circle cx="-20" cy="-36" r="14"/><circle cx="0" cy="-42" r="15"/><circle cx="20" cy="-36" r="14"/><circle cx="-32" cy="-24" r="10"/><circle cx="32" cy="-24" r="10"/></g>
  <g fill="#8a5a3a"><circle cx="-18" cy="-42" r="6"/><circle cx="-2" cy="-49" r="5"/></g>
  <g fill="#4e2e1c"><circle cx="26" cy="-30" r="6"/><circle cx="33" cy="-20" r="5"/></g>
  {blush("#f08a8a",.42)}
  <path d="M -8,22 Q 0,29 8,22 Z" fill="#a8545a"/><rect x="-3.4" y="22" width="6.8" height="3.6" rx="1" fill="#fff8ee"/>
  </g></g></g>'''

# 11 รอน (ล้อเลียน): ผมแดง กระ ตัวสูงเก้งก้าง จมูกยาว กินแซนด์วิชอยู่
sk, sh, hl, dp = "#fbe2d0", "#eabca4", "#fff0e6", "#d4a088"
sandwich = f'''<g transform="translate(60,200)"><path d="M -6,-8 L 26,-8 L 10,-30 Z" fill="#e6c48a"/><path d="M -4,-10 L 24,-10 L 22,-13 L -2,-13 Z" fill="#7bb36a"/><path d="M -6,-14 L 26,-14 L 10,-34 Z" fill="#f0d6a0"/><circle cx="20" cy="-14" r="5" fill="#1b1f2b"/>{hand(0,0,sk,sh)}</g>'''
C["ron"] = f'''<g id="c_ron"><g transform="translate(0,-425)">
  {kid_body(tie=RED, stripe=GOLD, sy=0.88, extra_hand_r=sandwich)}
  <g transform="scale(1.16)">
  {face("rn",sk,sh,hl,dp)}
  <path d="M 1,0 L 5,18 L 0,19 Z" fill="{sh}"/>
  {eyes_round("rn", iris="#3a6aa0", big=1.0)}
  <path d="M -22,-11 Q -14,-14 -6,-11.5 L -6,-9.5 Q -14,-12 -22,-9 Z M 22,-11 Q 14,-14 6,-11.5 L 6,-9.5 Q 14,-12 22,-9 Z" fill="#a8401c"/>
  <path d="M -35,-4 C -42,-42 -24,-56 0,-56 C 24,-56 42,-42 35,-4 L 31,-20 L 24,-14 L 20,-26 L 10,-18 L 4,-28 L -4,-18 L -12,-28 L -18,-16 L -24,-24 L -30,-14 Z" fill="#c8562a"/>
  <path d="M -26,-42 C -18,-52 -6,-55 4,-54 C -6,-48 -14,-42 -20,-34 Z" fill="#e2783e"/>
  <path d="M 20,-26 L 24,-14 L 31,-20 L 35,-4 C 38,-24 32,-40 22,-46 Z" fill="#a8401c"/>
  <g fill="#c87a54" opacity=".7"><circle cx="-18" cy="6" r="1.2"/><circle cx="-14" cy="9" r="1.1"/><circle cx="-21" cy="10" r="1"/><circle cx="-10" cy="7" r="1"/><circle cx="18" cy="6" r="1.2"/><circle cx="14" cy="9" r="1.1"/><circle cx="21" cy="10" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="-2" cy="4" r=".9"/><circle cx="3" cy="5" r=".9"/></g>
  {blush("#ef8f7e",.32)}
  <path d="M -8,24 Q 0,30 8,24 Q 0,27 -8,24 Z" fill="#a8545a"/><ellipse cx="9" cy="23" rx="2" ry="1.4" fill="#e6c48a"/>
  </g></g></g>'''

# 12 เดรโก (ล้อเลียน): ผมบลอนด์ทองซีดหวีเสยเรียบ หน้าแหลม ยิ้มเยาะ ตาเทา
sk, sh, hl, dp = "#fbeee4", "#e8d2c2", "#fffaf5", "#d2b6a4"
C["draco"] = f'''<g id="c_draco"><g transform="translate(0,-392)">
  {kid_body(tie=GREEN, stripe=SILVER, sy=0.81)}
  <g transform="scale(1.18)">
  {face("dm",sk,sh,hl,dp)}
  <path d="M -24,16 C -16,30 -8,36 0,40 C -12,38 -22,30 -26,18 Z" fill="{sh}" opacity=".6"/>
  {eyes_stern("dm", iris="#6a7480", lid="#d8c9a0")}
  <path d="M -23,-12 L -6,-10 L -6,-7.5 L -22,-9 Z" fill="#c9b886"/><path d="M 23,-15 C 17,-15 11,-13 6,-10.5 L 6,-8 C 11,-10 17,-11.6 22,-11.6 Z" fill="#c9b886"/>
  <path d="M -34,-8 C -38,-44 -18,-54 2,-54 C 24,-54 40,-42 34,-8 C 32,-22 26,-30 14,-34 C 4,-37 -8,-36 -18,-30 C -26,-26 -30,-18 -34,-8 Z" fill="#e8dfc6"/>
  <path d="M -30,-26 C -26,-42 -10,-50 6,-50 C 0,-46 -14,-40 -22,-30 Z" fill="#fbf6e6"/>
  <path d="M 14,-34 C 26,-30 32,-22 34,-8 C 38,-30 30,-46 18,-50 Z" fill="#c9b886"/>
  <path d="M -12,-50 C -4,-44 8,-42 20,-46 M -16,-44 C -6,-38 8,-37 22,-40" fill="none" stroke="#c9b886" stroke-width="1.4"/>
  {blush("#e8a0a0",.22)}
  <path d="M -6,25 Q 2,26 8,21" fill="none" stroke="#b07a7a" stroke-width="1.8" stroke-linecap="round"/>
  </g></g></g>'''

INFO = [
  ("head", "อาจารย์ใหญ่ทองหล่อ", "ครูใหญ่ อายุราว 90 · ใจดี ยิ้มตาหยี เคราขาวยาวถึงอก แว่นกรอบกระ · ผ้าขาวม้าพาดไหล่แทนผ้าพันคอ ไม้เท้าตะเกียงทอง", 1.0),
  ("strict", "ครูมาลัย", "ครูประจำชั้นปี 1 · เข้มงวดสุดในโรงเรียน ผมเกล้ามวยสูงมีปอยหงอก แว่นเหลี่ยมกรอบแดง · ถือไม้เรียวแทนไม้กายสิทธิ์", 1.0),
  ("potion", "ป้าแช่ม", "ครูวิชาปรุงยา · ผมดัดหยิก ยิ้มกว้าง ผ้ากันเปื้อนเปื้อนยาเขียว · ปรุงยาด้วยครกกับสากแบบตำส้มตำ", 1.0),
  ("giant", "ลุงโต", "ภารโรงร่างยักษ์ สูงกว่าเจมราวหนึ่งในสาม · เสื้อม่อฮ่อม ผ้าขาวม้าคาดเอว รองเท้าบูทยาง ไม้กวาดทางมะพร้าว · หน้าดุแต่ใจดี", 1.0),
  ("harry", "แฮร์รี่ (ฉบับล้อเลียน)", "เด็กชายผู้มีชื่อเสียง อายุ 11 · ผมดำยุ่ง แว่นกลมกรอบดำหนา ตาเขียว แผลสายฟ้าที่หน้าผาก · งงว่าทำไมมีผู้ใหญ่ใส่แว่นกลมเหมือนตัวเองมานั่งเรียนด้วย", 1.0),
  ("hermione", "เฮอร์ไมโอนี่ (ฉบับล้อเลียน)", "หัวหน้าห้องตัวจริง อายุ 11 · ผมน้ำตาลฟูฟ่อง ฟันหน้าเด่นนิด ๆ กอดหนังสือสี่เล่ม · ชอบแก้คำร่ายคาถาของเจมที่ออกเสียงแบบไทย", 1.0),
  ("ron", "รอน (ฉบับล้อเลียน)", "เพื่อนซี้ อายุ 11 · ผมแดง กระเต็มหน้า ตัวสูงเก้งก้าง แทะแซนด์วิชตลอด · ตื่นเต้นกับหม้อหุงข้าวของเจมมากกว่าเวทมนตร์", 1.0),
  ("draco", "เดรโก (ฉบับล้อเลียน)", "คู่ปรับ อายุ 11 · ผมบลอนด์ทองซีดหวีเสย หน้าแหลม ยิ้มเยาะ เนกไทเขียวเงิน · เรียกเจมว่า \"ลุง\"", 1.0),
  ("kidboy", "น้องภูมิ", "เพื่อนร่วมชั้นปี 1 อายุ 11 · ผมเกรียน ฟันหลอ ติดแท็บเล็ต ชอบถามเจมว่า \"พี่ซ้ำชั้นมากี่ปีครับ\"", 1.0),
  ("kidgirl", "น้องใบเตย", "เพื่อนร่วมชั้นปี 1 อายุ 11 · ผมหน้าม้า มัดจุกสองข้าง ยกมือตอบทุกข้อ หอบหนังสือเล่มหนาไปทุกที่", 1.0),
  ("owl", "พี่ฮูก", "นกฮูกส่งจดหมาย · ตาปรือเพราะวิ่งรอบดึก ใส่หมวกกันน็อกสีแดง สะพายกระเป๋าจดหมาย · ตัวเล็กเท่าแมวนั่ง", 1.0),
  ("guard", "ลุงยามสมพงษ์", "รปภ. ล็อบบี้คอนโด · ตาหรี่ หนวดเล็ก ถือคลิปบอร์ดแลกบัตร นกหวีดห้อยคอ · ไม่ยอมให้นกฮูกขึ้นลิฟต์", 1.0),
]

S = 1.0  # สเกลกลาง: ทุกตัวยืนบนพื้นเดียวกัน ความสูงเทียบกันได้
def card(key, name, desc):
    sc = 1.15 if key != "owl" else 1.6
    return f'''<figure class="card">
  <svg viewBox="0 0 400 1000" role="img" aria-label="{name} เต็มตัว หน้าตรง">
    <rect width="400" height="1000" fill="#1b1f2b"/><rect y="930" width="400" height="70" fill="#161a24"/>
    <ellipse cx="200" cy="948" rx="{90 if key=='giant' else (44 if key=='owl' else 74)}" ry="10" fill="#10131b"/>
    <use href="#c_{key}" transform="translate(200,948) scale({sc})"/>
  </svg>
  <figcaption><b>{name}</b><span>{desc}</span></figcaption>
</figure>'''

lineup_order = [("j_full", "เจม", 1), ("t_full", "ตะวัน", 1), ("c_head","ทองหล่อ",1), ("c_strict","มาลัย",1), ("c_potion","ป้าแช่ม",1), ("c_giant","ลุงโต",1), ("c_harry","แฮร์รี่",1), ("c_hermione","เฮอร์ไมโอนี่",1), ("c_ron","รอน",1), ("c_draco","เดรโก",1), ("c_kidboy","ภูมิ",1), ("c_kidgirl","ใบเตย",1), ("c_guard","ลุงยาม",1), ("c_owl","พี่ฮูก",1)]
gaps = {"c_giant": 260, "c_potion": 190, "c_hermione": 175}
x = 90; uses = ""; labels = ""
for ref, nm, _ in lineup_order:
    w = gaps.get(ref, 160 if ref != "c_owl" else 120)
    cx = x + w/2
    uses += f'<ellipse cx="{cx}" cy="950" rx="{w*0.36}" ry="9" fill="#10131b"/><use href="#{ref}" transform="translate({cx},950)"/>'
    labels += f'<text x="{cx}" y="985" text-anchor="middle">{nm}</text>'
    x += w
LW = x + 70

html = f'''<title>แคสต์โรงเรียนเวทมนตร์</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500;600&display=swap">
<style>
/* Layout: lineup เทียบความสูงทั้งแคสต์ ตามด้วยการ์ดตัวละครทีละตัว · โทนมืดตามแผ่นตัวละครของช่อง */
:root {{
  --stage: #0d0f14; --panel: #1b1f2b; --ink: #d4d6e0; --muted: #80849a; --line: #2a2e3a; --accent: #c9a8ff;
  --font: "IBM Plex Sans Thai", "Noto Sans Thai", system-ui, sans-serif;
  color-scheme: dark;
}}
html, body {{ background: var(--stage); color: var(--ink); }}
body {{ font-family: var(--font); padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); padding-block: 24px 40px; }}
.wrap {{ max-width: 1100px; margin: 0 auto; display: grid; gap: 20px; }}
h1 {{ font-size: 20px; font-weight: 600; margin: 0; text-wrap: balance; }}
h1 span {{ display: block; color: var(--muted); font-weight: 400; font-size: 14px; margin-top: 4px; }}
h2 {{ font-size: 15px; font-weight: 500; margin: 8px 0 0; color: var(--accent); letter-spacing: .02em; }}
.lineup {{ overflow-x: auto; border-radius: 6px; box-shadow: 0 0 0 1px var(--line); }}
.lineup svg {{ display: block; width: 100%; min-width: 760px; height: auto; }}
.lineup text {{ fill: var(--muted); font: 500 22px var(--font); }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; }}
.card {{ margin: 0; display: grid; gap: 8px; align-content: start; min-width: 0; }}
.card svg {{ display: block; width: 100%; height: auto; border-radius: 6px; box-shadow: 0 0 0 1px var(--line); }}
figcaption {{ display: grid; gap: 2px; font-size: 13px; line-height: 1.55; }}
figcaption b {{ font-weight: 600; font-size: 15px; }}
figcaption span {{ color: var(--muted); }}
.note {{ font-size: 13px; color: var(--muted); line-height: 1.6; max-width: 70ch; }}
.note b {{ color: var(--ink); font-weight: 500; }}
</style>

<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
{jdefs}
{tdefs}
{jfull}
{tfull}
{''.join(C.values())}
</defs></svg>

<div class="wrap">
  <h1>ตัวละครโรงเรียนยามวิกาล · ภาพร่าง v2<span>ตอน "ถ้าพรุ่งนี้ตื่นมาเจอจดหมายตอบรับจากฮอกวอตส์" · หน้าตรง · แสงกลางจากซ้าย · ลายเส้นเดียวกับเจมและตะวัน</span></h1>
  <h2>เทียบความสูงทั้งแคสต์</h2>
  <div class="lineup"><svg viewBox="0 120 {LW} 890" role="img" aria-label="ตัวละครทุกตัวยืนเรียงเทียบความสูง">
    <rect x="0" y="120" width="{LW}" height="890" fill="#1b1f2b"/><rect x="0" y="950" width="{LW}" height="60" fill="#161a24"/>
    {uses}{labels}
  </svg></div>
  <h2>ตัวละครใหม่</h2>
  <div class="grid">
    {''.join(card(k,n,d) for k,n,d,_ in INFO)}
  </div>
  <p class="note"><b>ชุดคลุมนักเรียน</b> สีม่วงครามขอบลาเวนเดอร์ เข้ากับโทนของช่อง เจมจะได้ชุดนี้ด้วยตอนเข้าเรียน · แฮร์รี่ เฮอร์ไมโอนี่ รอน และเดรโก วาดเป็นฉบับล้อเลียนด้วยลายเส้นของช่อง อ้างอิงลักษณะจากหนังสือ ไม่ใช้หน้านักแสดง ไม่ใช้ตราบ้านหรือตราโรงเรียน ใช้แค่สีเนกไทบอกฝั่ง · ตัวละครอื่นเป็นตัวละครของเราเอง</p>
</div>
'''
OUT.write_text(html)
print("wrote", OUT, len(html))
