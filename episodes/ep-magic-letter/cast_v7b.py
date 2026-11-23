# สร้าง cast.html: ภาพร่างตัวละครใหม่ของตอนจดหมายโรงเรียนเวทมนตร์
# ลายเส้นตาม CLAUDE.md: cut-out ไม่มีเส้นขอบ เงาบล็อก 2-3 ระดับ แสงจากซ้าย พื้น #1b1f2b
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = pathlib.Path(__file__).with_name("cast.html")

def grab(path, start_marker, prefix, feet):
    s = (ROOT / "characters" / path).read_text()
    defs = s[s.index("<defs>") + 6: s.index("</defs>")]
    if prefix == "j_":  # ตอนนี้เจมไม่ใส่หูฟัง
        defs = re.sub(r"<!-- headphones -->.*?(?=\n  </g>)", "", defs, flags=re.S)
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
    dia = "".join(f'<path d="M {sx*-10},{y} l 2.6,4 l -2.6,4 l -2.6,-4 Z"/>' for y in range(70, hem-20, 26) for sx in (1,-1))
    return f'''
    <path d="M -38,62 C -40,36 40,36 38,62 Z" fill="{shade}"/>
    <path d="M -30,58 C -30,44 30,44 30,58 Z" fill="{trim}" opacity=".55"/>
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
    <path d="M 76,206 L 44,196 L 45,202 L 75,212 Z" fill="{trim}" opacity=".8"/>
    <path d="M -76,212 L -45,202 L -46,208 C -58,214 -68,216 -76,216 Z" fill="{shade}"/>
    <path d="M 76,212 L 45,202 L 46,208 C 58,214 68,216 76,216 Z" fill="{shade}"/>
    <path d="M -60,120 C -66,150 -70,180 -72,200 L -66,202 C -64,180 -62,150 -58,124 Z" fill="{c}"/>
    <path d="M 60,120 C 66,150 70,180 72,200 L 66,202 C 64,180 62,150 58,124 Z" fill="{c}" opacity=".6"/>
    <g fill="{inner}" opacity=".9">{dia}</g>
    <g fill="{trim}">{"".join(f'<path d="M {x},{hem-14} l 3,3 l -3,3 l -3,-3 Z"/>' for x in range(-w+8, w-4, 14))}</g>'''

def hand(x, y, sk, sh, flip=1):
    return f'<path d="M {x-7},{y} L {x+7},{y} C {x+8},{y+12} {x+5},{y+22} {x},{y+23} C {x-5},{y+22} {x-8},{y+12} {x-7},{y} Z" fill="{sk if flip<0 else sh}"/>'

def shoes(c, cl, y):
    return f'''<path d="M -40,{y} L -8,{y} C -6,{y+8} -8,{y+13} -12,{y+14} L -42,{y+14} C -46,{y+13} -45,{y+4} -40,{y} Z" fill="{cl}"/>
    <path d="M 40,{y} L 8,{y} C 6,{y+8} 8,{y+13} 12,{y+14} L 42,{y+14} C 46,{y+13} 45,{y+4} 40,{y} Z" fill="{c}"/>'''


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

# ---------- ชุดนักเรียน: ผ้าคลุมดำ มีฮูด ซับในสีบ้าน เสื้อสเวตเตอร์คอวี เชิ้ตขาว เนกไท ----------
HOUSES = {
  # lining, lining เงา, เนกไท, แถบ
  "gry":  ("#9a2230", "#6e1622", "#8e1b24", "#d9b24a"),
  "sly":  ("#2f6b4a", "#1f4a33", "#2a5e40", "#c4c8d4"),
  "none": ("#4a4858", "#34323f", "#34323f", "#8a8898"),   # ยังไม่คัดบ้าน
}
RB, RL, RS = "#1d1c24", "#2e2d39", "#111016"   # ผ้าคลุมดำ: กลาง แสง เงา

def student_robe(h, hem=455, w=56, arm_up=False, skirt=False, sk="#f3cfa8", sh="#dcae86"):
    lin, lind, tie, st = HOUSES[h]
    if arm_up:
        rsleeve = f'''<path d="M 40,60 L 52,76 L 76,-60 L 56,-66 Z" fill="{RS}"/>
    <path d="M 56,-66 L 76,-60 L 75,-53 L 55,-59 Z" fill="{lind}"/>
    <path d="M 58,-64 L 72,-60 C 74,-74 72,-90 66,-92 C 60,-92 56,-78 58,-64 Z" fill="{sh}"/>'''
    else:
        rsleeve = f'''<path d="M 47,64 C 64,110 74,170 78,210 L 42,200 L 36,74 Z" fill="{RS}"/>
    <path d="M 60,120 C 66,150 70,180 72,204 L 66,206 C 64,180 62,150 58,124 Z" fill="{RB}"/>
    <path d="M 78,210 L 42,200 L 43,207 C 56,213 68,216 78,216 Z" fill="{lind}"/>'''
    lower = (f'''<path d="M -16,228 L 16,228 L 21,330 L -21,330 Z" fill="#4a4d5a"/>
    <path d="M -8,232 L -10,330 M 0,232 L 0,330 M 8,232 L 10,330" stroke="#3a3c48" stroke-width="2"/>
    <path d="M -20,330 L 20,330 L 24,{hem} L -24,{hem} Z" fill="#2a2932"/>''' if skirt else
             f'<path d="M -16,228 L 16,228 L 24,{hem} L -24,{hem} Z" fill="#3a3d48"/><path d="M -1,300 L 1,300 L 2,{hem} L -2,{hem} Z" fill="#2a2c35"/>')
    return f'''
    <path d="M -36,60 C -38,38 38,38 36,60 Z" fill="{RS}"/>
    <path d="M -47,64 C -64,110 -74,170 -78,210 L -42,200 L -36,74 Z" fill="{RL}"/>
    <path d="M -60,120 C -66,150 -70,180 -72,204 L -66,206 C -64,180 -62,150 -58,124 Z" fill="{RB}"/>
    <path d="M -78,210 L -42,200 L -43,207 C -56,213 -68,216 -78,216 Z" fill="{lin}"/>
    {rsleeve}
    {lower}
    <path d="M -13,52 L 13,52 L 16,232 L -16,232 Z" fill="#5d606c"/>
    <path d="M -13,52 L -4,52 L -6,232 L -16,232 Z" fill="#6d707c"/>
    <path d="M -16,222 L 16,222 L 16,226 L -16,226 Z M -16,228 L 16,228 L 16,231 L -16,231 Z" fill="{st}"/>
    <path d="M -12,49 C -28,51 -42,56 -47,66 L {-w},{hem} L -26,{hem} L -11,52 Z" fill="{RB}"/>
    <path d="M -47,66 C -42,56 -28,51 -18,50 C -28,120 -34,300 -38,{hem} L {-w},{hem} Z" fill="{RL}"/>
    <path d="M -40,200 L -37,200 L -45,{hem} L -50,{hem} Z M -20,260 L -18,260 L -22,{hem} L -26,{hem} Z" fill="{RB}"/>
    <path d="M 12,49 C 28,51 42,56 47,66 L {w},{hem} L 26,{hem} L 11,52 Z" fill="{RB}"/>
    <path d="M 20,50 C 32,53 43,58 47,66 L {w},{hem} L 38,{hem} C 34,300 30,120 20,50 Z" fill="{RS}"/>
    <path d="M 28,180 L 31,180 L 40,{hem} L 34,{hem} Z" fill="{RB}"/>
    <path d="M -12,49 L -8,50 L -22,{hem} L -29,{hem} Z" fill="{lin}"/>
    <path d="M 12,49 L 8,50 L 22,{hem} L 29,{hem} Z" fill="{lind}"/>
    <path d="M {-w},{hem-3} L -26,{hem-3} L -26,{hem} L {-w},{hem} Z M {w},{hem-3} L 26,{hem-3} L 26,{hem} L {w},{hem} Z" fill="#2a2934"/>'''

def student_collar(h):
    """ชิ้นหน้าที่ต้องวาดทับคอ: สเวตเตอร์ช่วงบน คอวี ปกเชิ้ต เนกไท ตะขอผ้าคลุม"""
    lin, lind, tie, st = HOUSES[h]
    return f'''
    <path d="M -14,48 L 14,48 L 15,84 L -15,84 Z" fill="#5d606c"/><path d="M -14,48 L -4,48 L -5,84 L -15,84 Z" fill="#6d707c"/>
    <path d="M -10,48 L 10,48 L 0,92 Z" fill="#f4f1ea"/><path d="M 0,48 L 10,48 L 0,92 Z" fill="#dcd8d0"/>
    <path d="M -12,48 L -10,48 L 0,90 L 10,48 L 12,48 L 0,96 Z" fill="{st}"/>
    <path d="M -3.6,55 L 3.6,55 L 4.4,90 L 0,94 L -4.4,90 Z" fill="{tie}"/>
    <path d="M -4,64 L 4,60 L 4,63.5 L -4,67.5 Z M -4.2,76 L 4.2,72 L 4.3,75.5 L -4.3,79.5 Z" fill="{st}"/>
    <path d="M -4,49 L 4,49 L 3.4,56 L -3.4,56 Z" fill="{tie}"/>
    <path d="M -11,44 L -1,52 L -5,60 L -15,52 Z" fill="#f4f1ea"/><path d="M 11,44 L 1,52 L 5,60 L 15,52 Z" fill="#dcd8d0"/>
    <path d="M -15,48 L -10,49 L -12.5,84 L -17,84 Z" fill="{lin}"/><path d="M 15,48 L 10,49 L 12.5,84 L 17,84 Z" fill="{lind}"/>
    <path d="M -15,66 L 15,66" stroke="#c4c8d4" stroke-width="1.4" stroke-dasharray="2 1.5"/>
    <circle cx="-15" cy="66" r="2.6" fill="#c4c8d4"/><circle cx="15" cy="66" r="2.6" fill="#9aa0aa"/>'''

def kid(cid, h, head_svg, sk, sh, sy=0.95, hand_l=None, hand_r=None, arm_up=False, skirt=False, back="", hs=1.02, bx=0.92):
    """นักเรียนปี 1 อายุ 18: สัดส่วนผู้ใหญ่ ความสูงตาม sy"""
    ty = -round(467*sy + 2)
    shoes_svg = shoes("#1a191f", "#2a2830", 453)
    return f'''<g id="{cid}"><g transform="translate(0,{ty})">
  {back}
  <g transform="scale({bx},{sy})">
    {student_robe(h, arm_up=arm_up, skirt=skirt, sk=sk, sh=sh)}
    {hand_l if hand_l is not None else hand(-60,206,sk,sh,-1)}{"" if arm_up else (hand_r if hand_r is not None else hand(60,206,sk,sh))}
    {shoes_svg}
  </g>
  <g transform="scale({hs})">{head_svg}</g>
  <g transform="scale({bx},{sy})">{student_collar(h)}</g>
  </g></g>'''

BROW = '<path d="M -22,-12 Q -14,-15 -6,-12.5 L -6,-10.5 Q -14,-13 -22,-10 Z M 22,-12 Q 14,-15 6,-12.5 L 6,-10.5 Q 14,-13 22,-10 Z" fill="{c}"/>'

# 5 น้องภูมิ ปี 1 (ยังไม่คัดบ้าน)
sk, sh, hl, dp = "#f3cfa8", "#dcae86", "#fde3c6", "#c99a72"
C["kidboy"] = kid("c_kidboy", "none", f'''
  {face("kb",sk,sh,hl,dp)}
  <path d="M -34,-8 C -38,-50 38,-50 34,-8 L 31,-18 L 26,-24 L 16,-22 L 8,-26 L 0,-23 L -8,-26 L -16,-22 L -26,-24 L -31,-18 Z" fill="#221c20"/>
  <path d="M -30,-24 C -26,-40 -12,-46 2,-46 C -10,-40 -20,-34 -24,-24 Z" fill="#4a4048"/>
  {eyes_round("kb", big=0.95)}{BROW.format(c="#221c20")}
  {blush("#ef8f7e",.45)}
  <path d="M -10,21 Q 0,32 10,21 Z" fill="#8a3a3a"/><path d="M -8,21.5 L 8,21.5 L 7,24.5 L -7,24.5 Z" fill="#fff8ee"/>''',
  sk, sh, hand_r=f'<g transform="translate(60,206)"><rect x="-4" y="6" width="34" height="46" rx="4" fill="#1e2230"/><rect x="0" y="10" width="26" height="36" rx="2" fill="#6f8fd6"/><path d="M 0,10 L 26,10 L 0,40 Z" fill="#8fa9e6"/>{hand(0,0,sk,sh)}</g>')

# 6 น้องใบเตย ปี 1 (ยังไม่คัดบ้าน ยกมือ)
sk, sh, hl, dp = "#f7d6b3", "#e2b48f", "#fde6cf", "#cc9e7c"
C["kidgirl"] = kid("c_kidgirl", "none", f'''
  {face("kg",sk,sh,hl,dp)}
  <path d="M -36,-6 C -42,-50 42,-50 36,-6 L 30,-12 L 28,-22 L 18,-18 L 10,-24 L 0,-18 L -10,-24 L -18,-18 L -28,-22 L -30,-12 Z" fill="#1c1418"/>
  <path d="M -30,-30 C -22,-42 -8,-46 4,-46 C -8,-40 -18,-34 -24,-24 Z" fill="#3a2e36"/>
  <circle cx="-38" cy="-30" r="7" fill="#1c1418"/><circle cx="38" cy="-30" r="7" fill="#120c10"/>
  <circle cx="-33" cy="-34" r="3" fill="#7fb59a"/><circle cx="33" cy="-34" r="3" fill="#6a9e86"/>
  {eyes_round("kg", iris="#4a2a1f", big=0.98)}
  <path d="M -21,-14 Q -14,-17 -7,-14 L -7,-12.6 Q -14,-15 -21,-12.6 Z M 21,-14 Q 14,-17 7,-14 L 7,-12.6 Q 14,-15 21,-12.6 Z" fill="#1c1418"/>
  {blush("#f08a8a",.45)}<path d="M -7,22 Q 0,29 7,22 Z" fill="#b0545a"/>''',
  sk, sh, sy=0.9, arm_up=True, skirt=True,
  back='<g transform="scale(1.02)"><path d="M -36,-10 C -42,30 -38,52 -30,56 L 30,56 C 38,52 42,30 36,-10 Z" fill="#1c1418"/></g>',
  hand_l=f'<g transform="translate(-62,186) rotate(-6)"><rect x="-6" y="0" width="40" height="52" rx="3" fill="#7a2f3a"/><rect x="-6" y="0" width="6" height="52" fill="#5a1f2a"/><rect x="4" y="10" width="22" height="6" fill="#e0c27a"/><rect x="32" y="2" width="3" height="48" fill="#efe5d2"/>{hand(2,20,sk,sh,-1)}</g>')

# 9 แฮร์รี่ (ล้อเลียน)
sk, sh, hl, dp = "#f6dcc4", "#e2b89c", "#fdeadb", "#cc9e84"
C["harry"] = kid("c_harry", "gry", f'''
  {face("hp",sk,sh,hl,dp)}
  {eyes_round("hp", iris="#3f8a4a", big=0.94)}{BROW.format(c="#141217")}
  <path d="M -36,-6 C -44,-40 -26,-58 -4,-58 L 0,-64 L 6,-57 L 14,-62 L 14,-55 C 30,-52 44,-38 36,-6 L 32,-18 L 28,-12 L 25,-26 L 18,-14 L 13,-28 L 7,-16 L 2,-24 L -4,-15 L -10,-28 L -15,-14 L -20,-26 L -24,-12 L -30,-20 Z" fill="#141217"/>
  <path d="M -42,-30 L -34,-24 L -38,-12 Z M 42,-30 L 34,-24 L 38,-12 Z M -10,-62 L -4,-54 L -14,-54 Z" fill="#141217"/>
  <path d="M -26,-44 C -18,-52 -6,-56 4,-55 C -6,-50 -14,-44 -20,-36 Z" fill="#33303c"/>
  <path d="M 6,-26 L 1,-20 L 4,-20 L -1,-13 L 7,-21 L 4,-21 L 8,-26 Z" fill="#c95a5a"/>
  <g fill="#ffffff" fill-opacity=".07" stroke="#1a1a1e" stroke-width="2.2"><circle cx="-13" cy="-1" r="9.4"/><circle cx="13" cy="-1" r="9.4"/></g>
  <path d="M -3.6,-2.4 Q 0,-4.6 3.6,-2.4 M -22.4,-2 L -31,-3.4 M 22.4,-2 L 31,-3.4" fill="none" stroke="#1a1a1e" stroke-width="2"/>
  <path d="M -21.6,-5 A 9.4,9.4 0 0 1 -14,-10.2" fill="none" stroke="#5a5a66" stroke-width="1.2"/>
  {blush("#ef8f7e",.38)}<path d="M -7,23 Q 0,27 7,23" fill="none" stroke="#a05a54" stroke-width="2" stroke-linecap="round"/>''',
  sk, sh, sy=0.94, hand_r=f'<g transform="translate(60,206)"><path d="M 2,4 L 6,4 L 14,-70 L 11,-71 Z" fill="#6a4a2c"/><path d="M 11,-71 L 14,-70 L 13,-62 L 10,-63 Z" fill="#8a6a44"/>{hand(0,0,sk,sh)}</g>')

# 10 เฮอร์ไมโอนี่ (ล้อเลียน)
sk, sh, hl, dp = "#f7d9c0", "#e4b898", "#fde8d6", "#cfa080"
books = f'''<g transform="translate(-62,168)"><rect x="-26" y="0" width="52" height="16" rx="2" fill="#7a2f3a"/><rect x="-24" y="16" width="48" height="18" rx="2" fill="#2f4a6b"/><rect x="-28" y="34" width="56" height="16" rx="2" fill="#5a6b2f"/><rect x="-26" y="50" width="52" height="20" rx="2" fill="#6b4a2f"/><g fill="#e0c27a"><rect x="-10" y="6" width="20" height="3"/><rect x="-8" y="23" width="16" height="3"/><rect x="-12" y="40" width="24" height="3"/><rect x="-10" y="58" width="20" height="3"/></g>{hand(-16,46,sk,sh,-1)}{hand(18,46,sk,sh)}</g>'''
C["hermione"] = kid("c_hermione", "gry", f'''
  {face("hg",sk,sh,hl,dp)}
  {eyes_round("hg", iris="#6b3e22", big=0.98)}
  <path d="M -21,-13 Q -14,-16 -7,-13 L -7,-11.6 Q -14,-14 -21,-11.6 Z M 21,-13 Q 14,-16 7,-13 L 7,-11.6 Q 14,-14 21,-11.6 Z" fill="#4e2e1c"/>
  <g fill="#6b4228"><circle cx="-20" cy="-36" r="14"/><circle cx="0" cy="-42" r="15"/><circle cx="20" cy="-36" r="14"/><circle cx="-32" cy="-24" r="10"/><circle cx="32" cy="-24" r="10"/></g>
  <g fill="#8a5a3a"><circle cx="-18" cy="-42" r="6"/><circle cx="-2" cy="-49" r="5"/></g><g fill="#4e2e1c"><circle cx="26" cy="-30" r="6"/><circle cx="33" cy="-20" r="5"/></g>
  {blush("#f08a8a",.42)}<path d="M -8,22 Q 0,29 8,22 Z" fill="#a8545a"/><rect x="-3.4" y="22" width="6.8" height="3.6" rx="1" fill="#fff8ee"/>''',
  sk, sh, sy=0.9, skirt=True, hand_l=books, hand_r="",
  back='''<g transform="scale(1.02)"><g fill="#6b4228"><circle cx="-34" cy="-20" r="20"/><circle cx="34" cy="-20" r="20"/><circle cx="-40" cy="8" r="20"/><circle cx="40" cy="8" r="20"/><circle cx="-36" cy="34" r="18"/><circle cx="36" cy="34" r="18"/><circle cx="-24" cy="50" r="14"/><circle cx="24" cy="50" r="14"/></g><g fill="#4e2e1c"><circle cx="40" cy="8" r="12"/><circle cx="36" cy="34" r="11"/><circle cx="24" cy="50" r="8"/></g><g fill="#8a5a3a"><circle cx="-44" cy="0" r="8"/><circle cx="-38" cy="-26" r="7"/></g></g>''')

# 11 รอน (ล้อเลียน)
sk, sh, hl, dp = "#fbe2d0", "#eabca4", "#fff0e6", "#d4a088"
C["ron"] = kid("c_ron", "gry", f'''
  {face("rn",sk,sh,hl,dp)}<path d="M 1,0 L 5,18 L 0,19 Z" fill="{sh}"/>
  {eyes_round("rn", iris="#3a6aa0", big=0.92)}{BROW.format(c="#a8401c")}
  <path d="M -35,-4 C -42,-42 -24,-56 0,-56 C 24,-56 42,-42 35,-4 L 31,-20 L 24,-14 L 20,-26 L 10,-18 L 4,-28 L -4,-18 L -12,-28 L -18,-16 L -24,-24 L -30,-14 Z" fill="#c8562a"/>
  <path d="M -26,-42 C -18,-52 -6,-55 4,-54 C -6,-48 -14,-42 -20,-34 Z" fill="#e2783e"/><path d="M 20,-26 L 24,-14 L 31,-20 L 35,-4 C 38,-24 32,-40 22,-46 Z" fill="#a8401c"/>
  <g fill="#c87a54" opacity=".7"><circle cx="-18" cy="6" r="1.2"/><circle cx="-14" cy="9" r="1.1"/><circle cx="-21" cy="10" r="1"/><circle cx="-10" cy="7" r="1"/><circle cx="18" cy="6" r="1.2"/><circle cx="14" cy="9" r="1.1"/><circle cx="21" cy="10" r="1"/><circle cx="10" cy="7" r="1"/><circle cx="-2" cy="4" r=".9"/><circle cx="3" cy="5" r=".9"/></g>
  {blush("#ef8f7e",.32)}<path d="M -8,24 Q 0,30 8,24 Q 0,27 -8,24 Z" fill="#a8545a"/><ellipse cx="9" cy="23" rx="2" ry="1.4" fill="#e6c48a"/>''',
  sk, sh, sy=1.0,
  hand_r=f'<g transform="translate(60,200)"><path d="M -6,-8 L 26,-8 L 10,-30 Z" fill="#e6c48a"/><path d="M -4,-10 L 24,-10 L 22,-13 L -2,-13 Z" fill="#7bb36a"/><path d="M -6,-14 L 26,-14 L 10,-34 Z" fill="#f0d6a0"/><circle cx="20" cy="-14" r="5" fill="#1b1f2b"/>{hand(0,0,sk,sh)}</g>')

# 12 เดรโก (ล้อเลียน) หน้าเดิมที่ผ่านแล้ว
sk, sh, hl, dp = "#fbeee4", "#e8d2c2", "#fffaf5", "#d2b6a4"
C["draco"] = kid("c_draco", "sly", f'''
  {face("dm",sk,sh,hl,dp)}
  <path d="M -24,16 C -16,30 -8,36 0,40 C -12,38 -22,30 -26,18 Z" fill="{sh}" opacity=".6"/>
  {eyes_stern("dm", iris="#6a7480", lid="#d8c9a0")}
  <path d="M -23,-12 L -6,-10 L -6,-7.5 L -22,-9 Z" fill="#c9b886"/><path d="M 23,-15 C 17,-15 11,-13 6,-10.5 L 6,-8 C 11,-10 17,-11.6 22,-11.6 Z" fill="#c9b886"/>
  <path d="M -34,-8 C -38,-44 -18,-54 2,-54 C 24,-54 40,-42 34,-8 C 32,-22 26,-30 14,-34 C 4,-37 -8,-36 -18,-30 C -26,-26 -30,-18 -34,-8 Z" fill="#e8dfc6"/>
  <path d="M -30,-26 C -26,-42 -10,-50 6,-50 C 0,-46 -14,-40 -22,-30 Z" fill="#fbf6e6"/><path d="M 14,-34 C 26,-30 32,-22 34,-8 C 38,-30 30,-46 18,-50 Z" fill="#c9b886"/>
  <path d="M -12,-50 C -4,-44 8,-42 20,-46 M -16,-44 C -6,-38 8,-37 22,-40" fill="none" stroke="#c9b886" stroke-width="1.4"/>
  {blush("#e8a0a0",.22)}<path d="M -6,25 Q 2,26 8,21" fill="none" stroke="#b07a7a" stroke-width="1.8" stroke-linecap="round"/>''',
  sk, sh, sy=0.96)

# 13 เจมในชุดนักเรียน (ยังไม่คัดบ้าน) ใช้หัวจากแผ่นตัวละครที่ผ่านแล้ว
sk, sh = "#fbe7d8", "#efc7b0"
C["james_robe"] = f'''<g id="c_james_robe"><g transform="translate(0,-482)">
  {student_robe("none", hem=468, w=60, sk=sk, sh=sh)}
  {hand(-60,206,sk,sh,-1)}
  <g transform="translate(60,206)"><path d="M -6,6 L 30,6 L 26,-24 L -2,-24 Z" fill="#e8dcc8"/><path d="M -2,-24 L 26,-24 L 12,-10 Z" fill="#d8ccb6"/><circle cx="12" cy="-12" r="4" fill="#8e1b24"/>{hand(0,0,sk,sh)}</g>
  {shoes("#1a191f","#2a2830",466)}
  <use href="#j_jhead"/>
  {student_collar("none")}
  </g></g>'''

# 4 ลุงโต ภารโรงร่างยักษ์ (ฉบับล้อเลียนแฮกริด): ผมกับเคราดกฟู โค้ทหนังยาวกระเป๋าเยอะ ถือร่มกระดาษบ่อสร้างสีชมพู
sk, sh, hl, dp = "#e0ae88", "#c48f68", "#ecc29e", "#a87756"
HAIR, HAIRL, HAIRD = "#2a1f1c", "#46362f", "#1a1312"
C["giant"] = f'''<g id="c_giant"><g transform="scale(1.32) translate(0,-490)">
  <path d="M 74,40 L 79,40 L 80,300 L 75,300 Z" fill="#9a7444"/>
  <path d="M 76,28 L 77,28 L 80,60 L 73,60 Z" fill="#6a4a2c"/>
  <path d="M 66,60 L 88,60 L 84,250 L 70,250 Z" fill="#e88aa8"/><path d="M 77,60 L 88,60 L 84,250 L 78,250 Z" fill="#c76a8a"/>
  <path d="M 68,100 L 86,100 M 69,150 L 86,150 M 70,200 L 85,200" stroke="#f6b6c8" stroke-width="2"/>
  <path d="M -42,300 L 42,300 L 44,440 L 6,440 L 2,330 L -2,330 L -6,440 L -44,440 Z" fill="#3a3530"/>
  <path d="M -48,410 L -4,410 L -4,488 L -52,488 C -54,470 -52,440 -48,410 Z" fill="#5a3e28"/><path d="M -48,410 L -36,410 L -38,488 L -52,488 C -54,470 -52,440 -48,410 Z" fill="#6e4e34"/>
  <path d="M 4,410 L 48,410 C 52,440 54,470 52,488 L 4,488 Z" fill="#432d1c"/>
  <path d="M -54,476 L -4,476 L -4,488 L -54,488 Z M 4,476 L 54,476 L 54,488 L 4,488 Z" fill="#2a1c12"/>
  <path d="M -16,52 L 16,52 L 20,300 L -20,300 Z" fill="#7a5a3e"/>
  <path d="M -16,52 L -4,52 L -6,300 L -20,300 Z" fill="#8c6a4a"/>
  <g fill="#e9dfd2"><circle cx="0" cy="110" r="2.4"/><circle cx="0" cy="160" r="2.4"/></g>
  <path d="M -22,224 L 22,224 L 22,246 L -22,246 Z" fill="#4f8a5a"/><g fill="#b5434a"><rect x="-18" y="224" width="8" height="22"/><rect x="2" y="224" width="8" height="22"/></g>
  <path d="M -62,74 C -76,120 -80,190 -78,250 L -56,252 L -46,110 Z" fill="#82603f"/>
  <path d="M 62,74 C 76,120 80,190 78,250 L 56,252 L 46,110 Z" fill="#4a3222"/>
  <path d="M -78,248 L -56,250 L -56,258 L -78,256 Z" fill="#5a3e28"/><path d="M 78,248 L 56,250 L 56,258 L 78,256 Z" fill="#33241a"/>
  <path d="M -76,256 L -58,256 C -56,274 -60,286 -67,287 C -74,287 -78,274 -76,256 Z" fill="{sk}"/>
  <path d="M 58,256 L 76,256 C 78,274 74,286 67,287 C 60,287 56,274 58,256 Z" fill="{sh}"/>
  <path d="M -16,48 C -40,50 -58,58 -64,76 L -70,420 L -18,420 L -14,60 Z" fill="#6b4a32"/>
  <path d="M -64,76 C -58,60 -44,52 -28,50 C -40,120 -46,300 -48,420 L -70,420 Z" fill="#82603f"/>
  <path d="M 16,48 C 40,50 58,58 64,76 L 70,420 L 18,420 L 14,60 Z" fill="#5a3e28"/>
  <path d="M 30,50 C 46,54 60,62 64,76 L 70,420 L 46,420 C 46,300 42,120 30,50 Z" fill="#4a3222"/>
  <path d="M -16,48 L -6,52 L -26,130 L -34,96 Z" fill="#82603f"/><path d="M -16,48 L -10,50 L -26,128 L -30,110 Z" fill="#9a7650"/>
  <path d="M 16,48 L 6,52 L 26,130 L 34,96 Z" fill="#4a3222"/>
  <g fill="#4e3624"><rect x="-58" y="180" width="26" height="30" rx="3"/><rect x="-56" y="300" width="28" height="34" rx="3"/><rect x="30" y="160" width="24" height="28" rx="3"/><rect x="30" y="290" width="28" height="34" rx="3"/><rect x="-50" y="120" width="16" height="20" rx="2"/></g>
  <g fill="#5e4230"><rect x="-58" y="180" width="26" height="7" rx="2"/><rect x="-56" y="300" width="28" height="8" rx="2"/></g>
  <g fill="#3a281a"><rect x="30" y="160" width="24" height="7" rx="2"/><rect x="30" y="290" width="28" height="8" rx="2"/></g>
  <path d="M -48,180 L -46,170 L -42,180 Z" fill="#efe3c8"/><circle cx="44" cy="156" r="5" fill="#d8c3a0"/>
  <path d="M -70,414 L -18,414 L -18,420 L -70,420 Z M 18,414 L 70,414 L 70,420 L 18,420 Z" fill="#3a281a"/>
  <g transform="translate(0,2) scale(1.12)">
  <path d="M -44,-30 C -52,-10 -50,30 -42,56 C -40,40 -38,20 -36,0 Z M 44,-30 C 52,-10 50,30 42,56 C 40,40 38,20 36,0 Z" fill="{HAIR}"/>
  {face("gt",sk,sh,hl,dp)}
  <path d="M -34,-14 C -38,10 -34,30 -24,44 C -18,58 -10,66 0,70 C 10,66 18,58 24,44 C 34,30 38,10 34,-14 L 30,6 C 26,18 18,22 10,20 C 6,24 -6,24 -10,20 C -18,22 -26,18 -30,6 Z" fill="{HAIR}"/>
  <path d="M -24,44 L -20,62 L -14,56 L -8,72 L -2,62 L 4,74 L 10,60 L 16,66 L 20,52 C 14,60 8,66 0,70 C -10,66 -18,58 -24,44 Z" fill="{HAIR}"/>
  <path d="M -34,-14 C -36,6 -32,26 -24,40 C -28,24 -30,8 -28,-6 Z" fill="{HAIRL}"/>
  <path d="M 26,10 C 30,24 28,36 22,46 C 30,36 34,22 34,-6 Z" fill="{HAIRD}"/>
  <path d="M -12,20 C -6,17 6,17 12,20 C 8,24 4,23 0,25 C -4,23 -8,24 -12,20 Z" fill="{HAIRL}"/>
  <path d="M -6,27 Q 0,31 6,27 Q 0,33 -6,27 Z" fill="#9a5a4a"/>
  <ellipse cx="1" cy="10" rx="7" ry="6" fill="{sh}"/><ellipse cx="-1" cy="8.5" rx="4.5" ry="3.8" fill="{sk}"/>
  <g fill="#120c0a"><ellipse cx="-13" cy="-2" rx="3.6" ry="4"/><ellipse cx="13" cy="-2" rx="3.6" ry="4"/></g>
  <circle cx="-14.2" cy="-3.4" r="1.2" fill="#fff"/><circle cx="11.8" cy="-3.4" r="1.2" fill="#fff"/>
  <path d="M -24,-10 C -18,-15 -9,-15 -5,-11 L -6,-8 C -11,-11 -18,-11 -24,-7 Z M 24,-10 C 18,-15 9,-15 5,-11 L 6,-8 C 11,-11 18,-11 24,-7 Z" fill="{HAIR}"/>
  {blush("#d27a62",.38)}
  <path d="M -40,-6 C -50,-44 -26,-66 0,-66 C 28,-66 50,-44 40,-6 L 36,-22 L 32,-14 L 28,-30 L 20,-22 L 14,-34 L 6,-26 L 0,-36 L -6,-26 L -14,-34 L -20,-22 L -28,-30 L -32,-14 L -36,-22 Z" fill="{HAIR}"/>
  <path d="M -32,-40 C -22,-56 -8,-62 6,-62 C -6,-56 -16,-48 -24,-36 Z" fill="{HAIRL}"/>
  <path d="M 24,-56 L 40,-60 L 32,-46 Z M -26,-58 L -40,-56 L -32,-46 Z M 4,-64 L 10,-74 L 14,-62 Z" fill="{HAIR}"/>
  </g></g></g>'''

# 14 ต้น เพื่อนคนอีสาน (27 ปี จากขอนแก่น ได้จดหมายช้าเหมือนเจม) ยิ้มกว้าง ผ้าขาวม้าพันคอ ถือกระติบข้าวเหนียว
sk, sh, hl, dp = "#c98f62", "#ad7448", "#d9a274", "#95603a"
C["ton"] = f'''<g id="c_ton"><g transform="translate(0,-478)">
  {student_robe("none", hem=466, w=62, sk=sk, sh=sh)}
  {hand(-60,206,sk,sh,-1)}
  <g transform="translate(52,214) scale(1.5)">
    <path d="M 2,6 C 0,-18 24,-18 22,6" fill="none" stroke="#6a4a2a" stroke-width="2.4"/>
    <path d="M -5,6 L 29,6 L 29,20 L -5,20 Z" fill="#c9a26a"/><path d="M -5,6 L 5,6 L 5,20 L -5,20 Z" fill="#dcb87e"/><path d="M 21,6 L 29,6 L 29,20 L 21,20 Z" fill="#a8844e"/>
    <path d="M -5,18 L 29,18 L 29,21 L -5,21 Z" fill="#8a6a3a"/>
    <path d="M -2,21 L 26,21 L 26,54 L -2,54 Z" fill="url(#pweave)"/>
    <path d="M -2,21 L 6,21 L 6,54 L -2,54 Z" fill="#fff" opacity=".14"/><path d="M 19,21 L 26,21 L 26,54 L 19,54 Z" fill="#000" opacity=".2"/>
    <path d="M -4,52 L 28,52 L 28,57 L -4,57 Z" fill="#8a6a3a"/>
    <path d="M -2,57 L 3,57 L 2,66 L -1,66 Z M 21,57 L 26,57 L 25,66 L 22,66 Z M 9,57 L 15,57 L 14,63 L 10,63 Z" fill="#7a5a32"/>
    {hand(12,-10,sk,sh)}
  </g>
  {shoes("#1a191f","#2a2830",464)}
  {face("tn",sk,sh,hl,dp)}
  <path d="M -33,-10 C -34,-30 -26,-36 -20,-38 L -20,-14 Z M 33,-10 C 34,-30 26,-36 20,-38 L 20,-14 Z" fill="#3a3036"/>
  <path d="M -24,-18 C -28,-50 28,-50 24,-18 L 20,-26 L 14,-22 L 10,-32 L 4,-24 L -2,-34 L -8,-24 L -14,-32 L -18,-22 Z" fill="#141114"/>
  <path d="M -18,-36 C -10,-46 2,-48 10,-46 C 2,-42 -6,-38 -12,-30 Z" fill="#3a3036"/>
  {eyes_round("tn", iris="#2a1a12", big=0.86)}
  <path d="M -23,-12 L -6,-11 L -6,-7.6 L -23,-8.4 Z M 23,-12 L 6,-11 L 6,-7.6 L 23,-8.4 Z" fill="#141114"/>
  {blush("#c0604a",.35)}
  <path d="M -12,20 Q 0,34 12,20 Z" fill="#7a2e2a"/><path d="M -10,20.5 L 10,20.5 L 9,24 L -9,24 Z" fill="#fff8ee"/>
  {student_collar("none")}
  <path d="M -26,46 C -18,60 18,60 26,46 L 31,58 C 18,73 -18,73 -31,58 Z" fill="url(#pkm)"/>
  <path d="M 0,64 C 12,64 22,58 26,46 L 31,58 C 22,67 12,72 0,72 Z" fill="#000" opacity=".2"/>
  <path d="M 13,62 L 29,56 L 33,142 L 17,146 Z" fill="url(#pkm)"/><path d="M 24,58 L 29,56 L 33,142 L 27,144 Z" fill="#000" opacity=".22"/>
  <path d="M 17,146 L 33,142 L 34,150 L 18,154 Z" fill="#e9dfd2"/><path d="M 20,147 L 20.5,154 M 24,146 L 24.5,153 M 28,145 L 28.5,152 M 32,144 L 32.5,151" stroke="#b8423e" stroke-width="1"/>
  <path d="M -29,56 L -13,62 L -17,174 L -34,170 Z" fill="url(#pkm)"/><path d="M -29,56 L -24,58 L -29,171 L -34,170 Z" fill="#fff" opacity=".12"/>
  <path d="M -34,170 L -17,174 L -17.5,183 L -34.5,179 Z" fill="#e9dfd2"/><path d="M -31,171 L -31.5,179 M -27,172 L -27.5,180 M -23,173 L -23.5,181 M -19,174 L -19.5,182" stroke="#b8423e" stroke-width="1"/>
  </g></g>'''

# 15 ไอ้เหลือง ไก่ชนพันธุ์เหลืองหางขาว (ไปรษณีย์ประจำสาขาไทย) หันข้างเต็ม 90 องศา หันซ้าย
C["rooster"] = """<g id="c_rooster"><g transform="translate(0,0)">
  <path d="M 26,-86 C 50,-130 84,-150 104,-136 C 88,-128 70,-108 60,-84 Z" fill="#efe9df"/>
  <path d="M 30,-80 C 60,-118 96,-124 112,-104 C 92,-104 72,-90 58,-70 Z" fill="#d9d1c2"/>
  <path d="M 30,-74 C 62,-96 92,-90 104,-70 C 84,-76 66,-70 52,-58 Z" fill="#efe9df"/>
  <path d="M 28,-90 C 46,-140 70,-160 88,-156 C 74,-148 58,-126 48,-96 Z" fill="#fbf8f2"/>
  <path d="M -6,-36 L -2,-36 L -4,-6 L -8,-6 Z M 10,-36 L 14,-36 L 12,-6 L 8,-6 Z" fill="#d9b24a"/>
  <path d="M -8,-6 L -4,-6 L -2,0 L -16,0 L -14,-3 Z M 8,-6 L 12,-6 L 14,0 L 0,0 L 2,-3 Z" fill="#c99a3a"/>
  <path d="M -16,-58 C -16,-40 -8,-32 2,-32 L 22,-34 C 20,-46 14,-56 4,-60 Z" fill="#2a1e1a"/>
  <path d="M -30,-96 C -36,-70 -26,-46 -6,-42 C 14,-38 34,-50 38,-74 C 40,-90 26,-100 6,-100 C -10,-100 -24,-100 -30,-96 Z" fill="#1d1614"/>
  <path d="M -30,-96 C -36,-74 -28,-54 -14,-48 C -22,-62 -24,-80 -20,-96 Z" fill="#3a2a24"/>
  <path d="M -4,-90 C 12,-94 30,-88 34,-74 C 30,-62 18,-56 4,-58 C -4,-70 -6,-80 -4,-90 Z" fill="#a8541c"/>
  <path d="M 2,-86 C 14,-90 26,-84 30,-74 C 22,-78 12,-78 4,-74 Z" fill="#e0952e"/>
  <path d="M 6,-70 L 34,-72 L 30,-62 L 8,-62 Z" fill="#3a2a24"/>
  <path d="M 20,-100 C 32,-102 40,-94 42,-84 C 34,-90 26,-92 18,-92 Z" fill="#e8a33a"/>
  <path d="M -30,-96 C -34,-120 -30,-138 -22,-146 L -6,-146 C -2,-132 4,-114 14,-100 C 0,-96 -18,-94 -30,-96 Z" fill="#e8a33a"/>
  <path d="M -30,-96 C -34,-118 -30,-134 -24,-142 C -24,-126 -22,-110 -18,-98 Z" fill="#f4c46a"/>
  <path d="M -10,-140 C -6,-124 0,-110 14,-100 L 8,-98 C -2,-108 -8,-122 -12,-136 Z" fill="#c27a24"/>
  <path d="M -14,-120 L -10,-100 M -6,-126 L -2,-104 M 2,-118 L 6,-102" stroke="#c27a24" stroke-width="1.6"/>
  <path d="M -26,-140 C -28,-156 -18,-164 -8,-160 C -2,-156 -2,-146 -6,-140 Z" fill="#c8382a"/>
  <path d="M -24,-158 C -22,-166 -14,-168 -10,-162 C -8,-168 0,-166 0,-158 C -8,-160 -18,-160 -24,-158 Z" fill="#d43a2c"/>
  <path d="M -26,-150 L -40,-147 L -27,-143 Z" fill="#e0b040"/><path d="M -26,-147 L -40,-147 L -27,-143 Z" fill="#c4922a"/>
  <path d="M -26,-142 C -28,-134 -24,-130 -20,-132 C -18,-136 -20,-140 -22,-142 Z" fill="#c8382a"/>
  <circle cx="-17" cy="-151" r="3.4" fill="#e8a83a"/><circle cx="-17.6" cy="-151" r="1.8" fill="#1a1210"/><circle cx="-18.2" cy="-152" r=".7" fill="#fff"/>
  <path d="M -22,-156 L -12,-154 L -12,-152.6 L -22,-154 Z" fill="#7a1e16"/>
  <ellipse cx="-14" cy="-145" rx="3.6" ry="1.8" fill="#ff9a8a" opacity=".55"/>
  <path d="M -22,-118 C -10,-106 4,-96 18,-84" fill="none" stroke="#6b4a2c" stroke-width="2.6"/>
  <g transform="translate(14,-92) rotate(10)"><rect x="0" y="0" width="22" height="16" rx="3" fill="#6b4a2c"/><rect x="0" y="0" width="22" height="6" rx="2" fill="#83603a"/><path d="M 4,-6 L 20,-6 L 20,4 L 4,4 Z" fill="#efe3c8"/><circle cx="12" cy="0" r="2.6" fill="#8e1b24"/></g>
  </g></g>"""

# 16 ซิ่ง ตัวเอก เด็กแว้นเยาวราช อายุ 18 · ผมปัดหน้าม้าทองปิดตาข้างหนึ่ง ข้างไถสั้น ฟันทองหนึ่งซี่ เสื้อยืดดำโอเวอร์ไซซ์ลายไฟที่ชายเสื้อ โลโก้ ZING ที่อก ยีนส์ขาเดฟขาดเข่า โซ่กระเป๋าตังค์ รองเท้าแตะหูคีบ
sk, sh, hl, dp = "#e8b88e", "#cc9a70", "#f4cca6", "#b07e58"
SING_HEAD = f'''
  {face("sg",sk,sh,hl,dp)}
  <path d="M -33,-6 C -35,-22 -32,-32 -26,-36 L -24,-8 Z" fill="#3a3238"/><path d="M 33,-6 C 35,-22 32,-32 26,-36 L 24,-8 Z" fill="#2a2428"/>
  <g fill="#5a5058" opacity=".6"><circle cx="-30" cy="-18" r=".8"/><circle cx="-28" cy="-26" r=".8"/><circle cx="29" cy="-20" r=".8"/></g>
  {eyes_stern("sg", iris="#2a1a12", lid="#a87650")}
  <path d="M 23,-17 C 18,-21 11,-19 6,-14.5 L 6,-11.5 C 11,-15.5 18,-17 22,-14 Z" fill="#2a2024"/>
  <path d="M -26,-34 C -20,-52 6,-58 24,-48 C 34,-42 38,-30 34,-14 C 30,-24 22,-30 14,-30 C 6,-24 -6,-14 -18,-6 C -24,-2 -30,2 -34,6 C -38,-12 -34,-26 -26,-34 Z" fill="#e6b04a"/>
  <path d="M 14,-30 C 6,-24 -6,-14 -18,-6 C -24,-2 -30,2 -34,6 C -30,-6 -20,-16 -8,-22 C 0,-26 8,-30 14,-30 Z" fill="#c48a2e"/>
  <path d="M -20,-44 C -10,-54 6,-56 18,-50 C 6,-48 -6,-44 -14,-36 Z" fill="#f4cc72"/>
  <path d="M 14,-30 C 22,-30 30,-24 34,-14 C 36,-28 32,-40 24,-46 Z" fill="#a8742a"/>
  <path d="M -26,-34 C -22,-42 -16,-46 -10,-48 C -14,-42 -18,-38 -20,-34 Z" fill="#2a2024"/>
  <circle cx="-33" cy="6" r="1.8" fill="#dfe3ea"/>
  {blush("#d27a62",.3)}
  <path d="M -7,23.6 Q 1,26 9,20.6" fill="none" stroke="#8e4a3e" stroke-width="2" stroke-linecap="round"/>
  <rect x="2.4" y="22.4" width="3.4" height="3" rx=".6" fill="#e8c24a"/>'''
C["sing"] = f'''<g id="c_sing"><g transform="translate(0,-480)">
  <path d="M -34,232 L 34,232 L 34,300 L 27,464 L 8,464 L 3,292 L -3,292 L -8,464 L -27,464 L -34,300 Z" fill="#262832"/>
  <path d="M -34,232 L -20,232 L -23,300 L -20,464 L -27,464 L -34,300 Z" fill="#363a48"/>
  <path d="M 18,236 L 34,232 L 34,300 L 27,464 L 20,464 C 22,380 21,300 18,236 Z" fill="#1a1c24"/>
  <path d="M -28,338 L -14,336 M -27,344 L -15,343 M 14,340 L 26,338 M 15,346 L 25,345" stroke="#8a90a4" stroke-width="2.2" stroke-linecap="round"/>
  <path d="M 20,250 C 30,270 40,272 40,290" fill="none" stroke="#c4c8d4" stroke-width="1.6" stroke-dasharray="2 1.4"/>
  <rect x="-26" y="462" width="14" height="10" fill="{sk}"/><rect x="12" y="462" width="14" height="10" fill="{sh}"/>
  <path d="M -34,472 L -6,472 L -6,478 L -34,478 Z" fill="#2a5aa8"/><path d="M 6,472 L 34,472 L 34,478 L 6,478 Z" fill="#1e468a"/>
  <path d="M -19,462 L -24,472 M -19,462 L -14,472 M 19,462 L 14,472 M 19,462 L 24,472" stroke="#2a5aa8" stroke-width="2.4"/>
  <path d="M -54,134 L -42,138 L -40,236 L -52,236 Z" fill="{sk}"/><path d="M -54,134 L -50,135 L -50,236 L -52,236 Z" fill="{hl}"/>
  <path d="M 54,134 L 42,138 L 40,236 L 52,236 Z" fill="{sh}"/>
  {hand(-46,234,sk,sh,-1)}
  <g transform="translate(46,206)">
    <path d="M -22,30 C -24,4 -12,-10 6,-10 C 24,-10 34,4 32,30 Z" fill="#8e1b24"/><path d="M -22,30 C -24,8 -14,-6 0,-9 C -10,0 -14,14 -14,30 Z" fill="#b02a34"/>
    <path d="M -22,24 L 32,24 L 32,32 L -22,32 Z" fill="#1a1a20"/>
    <rect x="-6" y="0" width="16" height="7" rx="2" fill="#f0c050" transform="rotate(-12 2 3)"/><circle cx="20" cy="10" r="4" fill="#e8e8f0"/>
    {hand(0,24,sk,sh)}
  </g>
  <path d="M -12,49 L 12,49 C 30,51 46,56 52,68 L 64,136 L 44,142 L 46,252 L -46,252 L -44,142 L -64,136 L -52,68 C -46,56 -30,51 -12,49 Z" fill="#1c1b22"/>
  <path d="M -52,68 C -46,56 -30,51 -18,50 C -28,80 -32,140 -30,252 L -46,252 L -44,142 L -64,136 Z" fill="#2c2b35"/>
  <path d="M 22,50 C 36,54 48,60 52,68 L 64,136 L 44,142 L 46,252 L 30,252 C 32,180 30,100 22,50 Z" fill="#111016"/>
<g transform="translate(0,151) scale(1,.4)"><path d="M -46,252 L -46,214 C -40,200 -36,222 -30,206 C -26,190 -20,214 -14,196 C -10,184 -4,206 2,192 C 8,178 12,204 18,190 C 24,176 28,200 34,190 C 40,180 42,204 46,198 L 46,252 Z" fill="#c8432e"/>
  <path d="M -46,252 L -46,230 C -40,220 -36,234 -30,224 C -24,212 -18,230 -12,218 C -6,208 0,228 6,216 C 12,206 18,226 24,214 C 30,204 36,226 46,216 L 46,252 Z" fill="#e8843a"/>
  <path d="M -40,252 C -34,240 -28,248 -22,238 C -16,230 -10,246 -2,236 C 6,228 12,246 20,236 C 28,228 34,246 42,240 L 42,252 Z" fill="#f0c050"/></g>
  <text x="-34" y="100" font-family="Inter, sans-serif" font-size="13" font-weight="800" fill="#e8843a" transform="skewX(-12)">ZING</text><path d="M -34,104 L 4,104" stroke="#c8432e" stroke-width="2"/>
  <path d="M -12,49 C -8,61 8,61 12,49" fill="none" stroke="#2c2b35" stroke-width="4"/>
  <g transform="translate(0,2)">{SING_HEAD}</g>
  <path d="M -12,52 C -8,72 8,72 12,52" fill="none" stroke="#c4c8d4" stroke-width="1.6" stroke-dasharray="2 1.4"/>
  </g></g>'''
C["sing_robe"] = f'''<g id="c_sing_robe"><g transform="translate(0,-482)">
  {student_robe("none", hem=468, w=60, sk=sk, sh=sh)}
  {hand(-60,206,sk,sh,-1)}
  <g transform="translate(60,206)"><path d="M 2,4 L 6,4 L 4,-62 L 1,-62 Z" fill="#d8c09a"/><circle cx="3" cy="-56" r="7" fill="#9a5a3a"/><circle cx="1" cy="-58" r="2.4" fill="#b8784e"/>{hand(0,0,sk,sh)}</g>
  {shoes("#1a191f","#2a2830",466)}
  {SING_HEAD}
  {student_collar("none")}
  </g></g>'''

# 17 อาม้า แม่ของซิ่ง เจ้าของร้านทองชั้นล่าง · ชุดนอนลายดอก โรลม้วนผม สร้อยทองเส้นโต แว่นห้อยคอ กัดเหรียญเช็กทอง
sk, sh, hl, dp = "#f6dcc4", "#e2b89c", "#fdeadb", "#cc9e84"
C["ama"] = f'''<g id="c_ama"><g transform="translate(0,-462)">
  <path d="M -40,240 L 40,240 L 42,450 L 6,450 L 2,300 L -2,300 L -6,450 L -42,450 Z" fill="#e8a0b0"/>
  <path d="M -40,240 L -26,240 L -28,450 L -42,450 Z" fill="#f4bccb"/><path d="M 24,240 L 40,240 L 42,450 L 28,450 Z" fill="#c9808f"/>
  <path d="M -42,450 L -6,450 L -4,462 L -44,462 Z" fill="#7a5aa8"/><path d="M 6,450 L 42,450 L 44,462 L 4,462 Z" fill="#5e4488"/>
  <path d="M -58,110 L -44,116 L -46,220 L -60,220 Z" fill="#f4bccb"/><path d="M 58,110 L 44,116 L 46,170 L 58,166 Z" fill="#c9808f"/>
  <g fill="#e0b84a"><rect x="-61" y="214" width="16" height="4" rx="2"/><rect x="-61" y="220" width="16" height="4" rx="2"/></g>
  {hand(-53,224,sk,sh,-1)}
  <path d="M -14,49 L 14,49 C 36,51 54,58 60,74 C 66,120 62,200 56,256 L -56,256 C -62,200 -66,120 -60,74 C -54,58 -36,51 -14,49 Z" fill="#e8a0b0"/>
  <path d="M -60,74 C -54,58 -36,51 -20,50 C -32,100 -38,180 -36,256 L -56,256 C -62,200 -66,120 -60,74 Z" fill="#f4bccb"/>
  <path d="M 24,50 C 44,56 56,62 60,74 C 66,120 62,200 56,256 L 36,256 C 40,180 38,100 24,50 Z" fill="#c9808f"/>
  <g fill="#fff4f6"><circle cx="-30" cy="100" r="4"/><circle cx="10" cy="130" r="4"/><circle cx="-14" cy="180" r="4"/><circle cx="30" cy="200" r="4"/><circle cx="-36" cy="230" r="4"/><circle cx="-20" cy="320" r="4"/><circle cx="20" cy="380" r="4"/><circle cx="24" cy="290" r="4"/></g>
  <g fill="#d4506a"><circle cx="-30" cy="100" r="1.6"/><circle cx="10" cy="130" r="1.6"/><circle cx="-14" cy="180" r="1.6"/><circle cx="30" cy="200" r="1.6"/><circle cx="-36" cy="230" r="1.6"/><circle cx="-20" cy="320" r="1.6"/><circle cx="20" cy="380" r="1.6"/><circle cx="24" cy="290" r="1.6"/></g>
  <path d="M 46,166 L 58,162 L 40,104 L 30,110 Z" fill="#c9808f"/>
  {hand(34,100,sk,sh)}<g transform="translate(34,96)"><circle r="9" fill="#e8c24a"/><circle r="6" fill="#f4d878"/><circle cx="-2" cy="-2" r="2" fill="#fff4c0"/></g>
  {face("am",sk,sh,hl,dp)}
  <g fill="#2a2226"><circle cx="-30" cy="-22" r="10"/><circle cx="-20" cy="-36" r="11"/><circle cx="-4" cy="-42" r="11"/><circle cx="12" cy="-40" r="11"/><circle cx="26" cy="-30" r="10"/><circle cx="32" cy="-14" r="8"/><circle cx="-34" cy="-6" r="7"/></g>
  <g fill="#8a8490"><circle cx="-18" cy="-40" r="4"/><circle cx="8" cy="-46" r="3.5"/></g>
  <g><rect x="-30" y="-58" width="14" height="10" rx="5" fill="#f08aa8" transform="rotate(-20 -23 -53)"/><rect x="-6" y="-60" width="14" height="10" rx="5" fill="#8ac8e8"/><rect x="16" y="-56" width="14" height="10" rx="5" fill="#f0c860" transform="rotate(18 23 -51)"/></g>
  {eyes_squint()}
  <path d="M -23,-11 L -6,-9 L -6,-6.4 L -23,-8.2 Z M 23,-11 L 6,-9 L 6,-6.4 L 23,-8.2 Z" fill="#2a2226"/>
  <g fill="#fff" fill-opacity=".08" stroke="#c9a24a" stroke-width="1.4"><ellipse cx="-12" cy="3" rx="8" ry="5.4"/><ellipse cx="12" cy="3" rx="8" ry="5.4"/></g>
  <path d="M -4,3 L 4,3 M -20,4 C -26,20 -22,40 -14,52 M 20,4 C 26,20 22,40 14,52" fill="none" stroke="#c9a24a" stroke-width="1.1"/>
  {blush("#e08a86",.3)}
  <path d="M -5,25 Q 0,23 5,25 Q 0,27 -5,25 Z" fill="#b0545a"/>
  <path d="M -16,50 C -10,72 10,72 16,50" fill="none" stroke="#e0b84a" stroke-width="3.6"/>
  <path d="M -16,50 C -10,72 10,72 16,50" fill="none" stroke="#f4d878" stroke-width="1.2" stroke-dasharray="2 2.4"/>
  <circle cx="0" cy="72" r="6" fill="#e0b84a"/><circle cx="-1.4" cy="70.6" r="2" fill="#f4d878"/>
  </g></g>'''

# 18 ป้าแต๋ว แม่ค้าไม้กายสิทธิ์ ตลาดนัดเวทมนตร์ · ตะโกนเสียงดัง กระเป๋าคาดเอว ถือไม้กายสิทธิ์กำโต
sk, sh, hl, dp = "#d9a57c", "#bb875f", "#e8bb93", "#a37552"
wands = "".join(f'<path d="M 0,0 L {x},{-70-abs(x)/3:.0f}" stroke="{c}" stroke-width="3.4" stroke-linecap="round"/>' for x, c in [(-22,"#6a4a2c"),(-10,"#8a6a44"),(0,"#5a3a22"),(10,"#9a7650"),(22,"#7a5632"),(-4,"#d8c09a")])
C["vendor"] = f'''<g id="c_vendor"><g transform="translate(0,-468)">
  <path d="M -40,236 L 40,236 L 40,452 L 6,452 L 2,300 L -2,300 L -6,452 L -40,452 Z" fill="#3a3d48"/>
  <path d="M -40,236 L -26,236 L -28,452 L -40,452 Z" fill="#4c5062"/>
  <path d="M -42,452 L -6,452 L -6,466 L -44,466 Z" fill="#c43a3a"/><path d="M 6,452 L 42,452 L 44,466 L 6,466 Z" fill="#9a2a2a"/>
  <path d="M -58,112 L -44,118 L -40,140 L -60,138 Z" fill="#6aa8a0"/>
  <path d="M -60,138 L -42,140 L -60,60 L -74,66 Z" fill="{sk}"/>
  {hand(-67,40,sk,sh,-1)}
  <path d="M 58,112 L 44,118 L 46,226 L 60,226 Z" fill="{sh}"/>
  <g transform="translate(53,224)">{wands}{hand(0,0,sk,sh)}</g>
  <path d="M -14,49 L 14,49 C 34,51 52,58 58,72 L 60,116 L 44,122 L 46,248 L -46,248 L -44,122 L -60,116 L -58,72 C -52,58 -34,51 -14,49 Z" fill="#6aa8a0"/>
  <path d="M -58,72 C -52,58 -34,51 -20,50 C -30,80 -34,140 -32,248 L -46,248 L -44,122 L -60,116 Z" fill="#82bcb4"/>
  <path d="M 22,50 C 38,53 52,60 58,72 L 60,116 L 44,122 L 46,248 L 30,248 C 32,180 32,100 22,50 Z" fill="#4e8a82"/>
  <g fill="#f2ead8" opacity=".8"><circle cx="-24" cy="90" r="5"/><circle cx="18" cy="110" r="5"/><circle cx="-8" cy="150" r="5"/><circle cx="26" cy="180" r="5"/></g>
  <path d="M -36,120 L 36,120 L 40,330 L -40,330 Z" fill="#2a3a5c"/><path d="M 20,120 L 36,120 L 40,330 L 26,330 Z" fill="#1d2a48"/>
  <path d="M -36,120 L -26,60 M 36,120 L 26,60" stroke="#2a3a5c" stroke-width="4"/>
  <path d="M -42,220 L 42,220 L 42,250 L -42,250 Z" fill="#1a1a20"/><path d="M -30,226 L 30,226" stroke="#c4c8d4" stroke-width="1.6" stroke-dasharray="3 2"/>
  <rect x="-12" y="238" width="24" height="10" rx="2" fill="#e88aa8"/><text x="0" y="246" font-size="7" text-anchor="middle" fill="#1a1a20" font-family="IBM Plex Sans Thai, sans-serif" font-weight="700">100</text>
  {face("vd",sk,sh,hl,dp)}
  <path d="M -34,-8 C -38,-42 -18,-54 2,-54 C 24,-54 38,-40 34,-8 C 28,-26 16,-34 0,-34 C -16,-34 -28,-26 -34,-8 Z" fill="#1d1a1e"/>
  <circle cx="0" cy="-60" r="13" fill="#1d1a1e"/><circle cx="-4" cy="-64" r="5" fill="#3a3640"/>
  <path d="M -36,-24 C -20,-34 20,-34 36,-24 L 36,-18 C 20,-28 -20,-28 -36,-18 Z" fill="#e88aa8"/>
  {eyes_crinkle("#2a1a16")}
  <path d="M -23,-12 Q -15,-16 -6,-12 M 23,-12 Q 15,-16 6,-12" fill="none" stroke="#1d1a1e" stroke-width="2.4" stroke-linecap="round"/>
  {blush("#d0705e",.4)}
  <path d="M -10,18 Q 0,16 10,18 Q 8,34 0,34 Q -8,34 -10,18 Z" fill="#7a2e2a"/><path d="M -8,18.4 L 8,18.4 L 7,21 L -7,21 Z" fill="#fff8ee"/><ellipse cx="0" cy="29" rx="5" ry="3" fill="#c45a5a"/>
  <circle cx="-34" cy="8" r="3.4" fill="none" stroke="#e0b84a" stroke-width="1.6"/><circle cx="34" cy="8" r="3.4" fill="none" stroke="#c9a24a" stroke-width="1.6"/>
  </g></g>'''

# 19 หมวกคัดสรร (ฉบับล้อเลียน) หมวกผ้าเก่าปะผ้าขาวม้า พับเป็นหน้า พูดได้
C["hat"] = '''<g id="c_hat"><g>
  <path d="M -62,0 C -64,-14 -40,-20 0,-20 C 40,-20 64,-14 62,0 C 40,8 -40,8 -62,0 Z" fill="#5a3e28"/>
  <path d="M -62,0 C -64,-14 -40,-20 -10,-20 C -36,-14 -50,-8 -50,4 C -56,3 -60,2 -62,0 Z" fill="#7a5638"/>
  <path d="M -34,-16 C -30,-50 -20,-80 -4,-104 C 6,-118 20,-126 34,-122 C 26,-116 18,-108 14,-96 C 22,-70 30,-40 34,-16 C 10,-10 -10,-10 -34,-16 Z" fill="#6a4a32"/>
  <path d="M -34,-16 C -30,-50 -20,-80 -4,-104 C -10,-80 -16,-50 -18,-14 C -24,-14 -30,-15 -34,-16 Z" fill="#84603f"/>
  <path d="M 14,-96 C 22,-70 30,-40 34,-16 C 26,-14 20,-13 14,-13 C 16,-40 16,-70 14,-96 Z" fill="#4a3222"/>
  <path d="M 34,-122 C 40,-120 44,-112 42,-104 C 38,-110 32,-114 26,-116 Z" fill="#6a4a32"/>
  <path d="M 6,-86 L 22,-82 L 20,-64 L 4,-68 Z" fill="url(#pkm)"/>
  <path d="M 6,-86 L 22,-82 M 20,-64 L 4,-68" stroke="#e9dfd2" stroke-width="1" stroke-dasharray="2 2"/>
  <path d="M -22,-60 C -16,-66 -8,-66 -4,-60 C -10,-62 -16,-62 -22,-58 Z" fill="#2a1a10"/>
  <path d="M 4,-58 C 10,-64 18,-64 22,-58 C 16,-60 10,-60 4,-56 Z" fill="#2a1a10"/>
  <path d="M -20,-62 C -18,-70 -10,-72 -4,-66" fill="none" stroke="#3a2618" stroke-width="2"/>
  <path d="M -18,-38 C -10,-34 6,-34 16,-40 C 10,-28 -8,-26 -18,-38 Z" fill="#1a0f08"/>
  <path d="M -26,-48 C -14,-44 10,-44 22,-50 M -28,-28 C -12,-22 12,-22 26,-28" fill="none" stroke="#4a3222" stroke-width="1.6"/>
  <path d="M -50,-6 C -30,-2 30,-2 50,-6" fill="none" stroke="#3a281a" stroke-width="2"/>
  </g></g>'''

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



INFO = [
  ("head", "อาจารย์ใหญ่ทองหล่อ", "ครูใหญ่ อายุราว 90 · ใจดี ยิ้มตาหยี เคราขาวยาวถึงอก แว่นกรอบกระ · ผ้าขาวม้าพาดไหล่แทนผ้าพันคอ ไม้เท้าตะเกียงทอง", 1.0),
  ("strict", "ครูมาลัย", "ครูประจำชั้นปี 1 · เข้มงวดสุดในโรงเรียน ผมเกล้ามวยสูงมีปอยหงอก แว่นเหลี่ยมกรอบแดง · ถือไม้เรียวแทนไม้กายสิทธิ์", 1.0),
  ("potion", "ป้าแช่ม", "ครูวิชาปรุงยา · ผมดัดหยิก ยิ้มกว้าง ผ้ากันเปื้อนเปื้อนยาเขียว · ปรุงยาด้วยครกกับสากแบบตำส้มตำ", 1.0),
  ("giant", "ลุงโต (ฉบับล้อเลียนแฮกริด)", "ภารโรงร่างยักษ์ สูงกว่าเจมราวหนึ่งในสาม · ผมกับเคราดกฟู โค้ทหนังยาวกระเป๋าเต็มตัว ผ้าขาวม้าคาดเอว ถือร่มกระดาษบ่อสร้างสีชมพู · เป็นคนพาเจมไปซื้อของ ตัวใหญ่จนลิฟต์คอนโดร้องเตือน", 1.0),
  ("sing", "ซิ่ง (ตัวเอก)", "เด็กแว้นเยาวราช อายุ 18 จบ ม.6 เกรด 1.50 · ผมปัดหน้าม้าทองปิดตาข้างหนึ่ง ข้างไถสั้น ฟันทองหนึ่งซี่ ต่างหูเม็ดเดียว · เสื้อยืดดำโอเวอร์ไซซ์ลายไฟที่ชายเสื้อ โลโก้ ZING ที่อก ยีนส์ขาเดฟขาดเข่า โซ่กระเป๋าตังค์ รองเท้าแตะหูคีบ หิ้วหมวกกันน็อกติดสติกเกอร์", 1.0),
  ("sing_robe", "ซิ่ง (ชุดนักเรียน)", "ผ้าคลุมดำ ซับในเทาเพราะยังไม่คัดบ้าน · ถือไม้กายสิทธิ์ที่จริง ๆ คือไม้เสียบลูกชิ้นเหลือลูกเดียว", 1.0),
  ("ama", "อาม้า", "แม่ของซิ่ง เจ้าของร้านทองชั้นล่างของตึกแถว · ชุดนอนลายดอก โรลม้วนผมสามสี แว่นห้อยสร้อย สร้อยทองเส้นโต · เห็นเหรียญทองต้องกัดเช็กก่อน", 1.0),
  ("vendor", "ป้าแต๋ว", "แม่ค้าไม้กายสิทธิ์ในตลาดนัดเวทมนตร์ · ผ้าคาดผมชมพู กระเป๋าคาดเอว ตะโกน \"สามอันร้อยจ้า!\" ถือไม้กายสิทธิ์กำโต", 1.0),
  ("hat", "หมวกคัดสรร (ฉบับล้อเลียน)", "หมวกผ้าเก่าปะด้วยผ้าขาวม้า รอยพับเป็นตากับปาก พูดได้ · ลังเลกับซิ่งจนโยนให้คนดูโหวต", 1.0),
  ("ton", "ต้น เพื่อนคนอีสาน", "18 ปี จากขอนแก่น เพิ่งจบ ม.6 เหมือนเจม · ยิ้มกว้าง ผ้าขาวม้าลายตาหมากรุกพาดคอทับผ้าคลุม ถือกระติบข้าวเหนียวสานไม้ไผ่มีขา แอบพกปลาแดกมาในกระเป๋า · พูดอีสาน เป็นเพื่อนซี้ของเจม", 1.0),
  ("harry", "แฮร์รี่ (ฉบับล้อเลียน)", "ผู้ชายผู้มีชื่อเสียง อายุ 18 · ผมดำยุ่ง แว่นกลมกรอบดำหนา ตาเขียว แผลสายฟ้าที่หน้าผาก · งงที่เจมใส่แว่นกลมเหมือนกัน", 1.0),
  ("hermione", "เฮอร์ไมโอนี่ (ฉบับล้อเลียน)", "หัวหน้าห้องตัวจริง อายุ 18 · ผมน้ำตาลฟูฟ่อง ฟันหน้าเด่นนิด ๆ กอดหนังสือสี่เล่ม · ชอบแก้คำร่ายคาถาของเจมที่ออกเสียงแบบไทย", 1.0),
  ("ron", "รอน (ฉบับล้อเลียน)", "เพื่อนซี้ อายุ 18 · ผมแดง กระเต็มหน้า ตัวสูงเก้งก้าง แทะแซนด์วิชตลอด · ตื่นเต้นกับหม้อหุงข้าวของเจมมากกว่าเวทมนตร์", 1.0),
  ("draco", "เดรโก (ฉบับล้อเลียน)", "คู่ปรับ อายุ 18 · ผมบลอนด์ทองซีดหวีเสย หน้าแหลม ยิ้มเยาะ เนกไทเขียวเงิน · ชอบเหยียดเจมกับต้นว่า \"พวกบ้านนอก\"", 1.0),
  ("kidboy", "ภูมิ", "เพื่อนร่วมชั้นปี 1 อายุ 18 · ผมรองทรง ติดแท็บเล็ต ไลฟ์สดทุกอย่างที่เห็นในโลกเวทมนตร์", 1.0),
  ("kidgirl", "ใบเตย", "เพื่อนร่วมชั้นปี 1 อายุ 18 · ผมหน้าม้า มัดจุกสองข้าง ยกมือตอบทุกข้อ หอบหนังสือเล่มหนาไปทุกที่", 1.0),
  ("rooster", "ไอ้เหลือง ไก่ชนไปรษณีย์", "ไก่ชนพันธุ์เหลืองหางขาว · นกฮูกที่อังกฤษงานล้น สาขาไทยเลยใช้ไก่ชนส่งจดหมายแทน · ขันปลุกตีห้าใส่หน้าก่อนส่งของ สะพายกระเป๋าจดหมายใบจิ๋ว หน้ากวนนิด ๆ", 1.0),
]

S = 1.0  # สเกลกลาง: ทุกตัวยืนบนพื้นเดียวกัน ความสูงเทียบกันได้
def card(key, name, desc):
    sc = {"owl":2.2,"rooster":2.2,"hat":2.6}.get(key,1.15)
    return f'''<figure class="card">
  <svg viewBox="0 0 400 1000" role="img" aria-label="{name} เต็มตัว หน้าตรง">
    <rect width="400" height="1000" fill="#1b1f2b"/><rect y="930" width="400" height="70" fill="#161a24"/>
    <ellipse cx="200" cy="948" rx="{90 if key=='giant' else (60 if key in ('owl','rooster','hat') else 74)}" ry="10" fill="#10131b"/>
    <use href="#c_{key}" transform="translate({150 if key=="rooster" else 200},{920 if key=="hat" else 948}) scale({sc})"/>
  </svg>
  <figcaption><b>{name}</b><span>{desc}</span></figcaption>
</figure>'''

lineup_order = [("c_sing", "ซิ่ง", 1), ("c_ama", "อาม้า", 1), ("c_vendor", "ป้าแต๋ว", 1), ("c_ton", "ต้น", 1), ("c_head","ทองหล่อ",1), ("c_strict","มาลัย",1), ("c_potion","ป้าแช่ม",1), ("c_giant","ลุงโต",1), ("c_harry","แฮร์รี่",1), ("c_hermione","เฮอร์ไมโอนี่",1), ("c_ron","รอน",1), ("c_draco","เดรโก",1), ("c_kidboy","ภูมิ",1), ("c_kidgirl","ใบเตย",1), ("c_rooster","ไอ้เหลือง",1)]
gaps = {"c_giant": 260, "c_potion": 190, "c_hermione": 175}
x = 90; uses = ""; labels = ""
for ref, nm, _ in lineup_order:
    w = gaps.get(ref, 160 if ref not in ("c_owl","c_rooster") else 170)
    cx = x + w/2
    uses += f'<ellipse cx="{cx}" cy="950" rx="{w*0.36}" ry="9" fill="#10131b"/><use href="#{ref}" transform="translate({cx},950)"/>'
    labels += f'<text x="{cx}" y="985" text-anchor="middle">{nm}</text>'
    x += w
LW = x + 70

html = f'''<title>แคสต์ฮอกวอตส์สาขาไทย</title>
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
<pattern id="pkm" width="14" height="14" patternUnits="userSpaceOnUse"><rect width="14" height="14" fill="#b8423e"/><rect x="0" width="4" height="14" fill="#2f5e8a" opacity=".85"/><rect y="0" width="14" height="4" fill="#2f5e8a" opacity=".6"/><rect x="8" width="1.6" height="14" fill="#f2ead8"/><rect y="8" width="14" height="1.6" fill="#f2ead8" opacity=".85"/><rect x="11" width="1" height="14" fill="#e8c24a"/><rect y="11" width="14" height="1" fill="#e8c24a" opacity=".8"/></pattern>
<pattern id="pweave" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#d8b878"/><rect width="3" height="3" fill="#b8945a"/><rect x="3" y="3" width="3" height="3" fill="#b8945a"/><rect x="0" y="2.4" width="3" height=".6" fill="#efd6a0"/><rect x="3" y="5.4" width="3" height=".6" fill="#efd6a0"/></pattern>
</defs></svg>

<div class="wrap">
  <h1>ตัวละครฮอกวอตส์ สาขาประเทศไทย · ภาพร่าง v7<span>ตอน "ถ้าพรุ่งนี้ตื่นมาเจอจดหมายตอบรับจากฮอกวอตส์ สาขาประเทศไทย" · หน้าตรง · แสงกลางจากซ้าย · ตัวเอกใหม่: ซิ่ง เด็กแว้นเยาวราช</span></h1>
  <h2>เทียบความสูงทั้งแคสต์</h2>
  <div class="lineup"><svg viewBox="0 120 {LW} 890" role="img" aria-label="ตัวละครทุกตัวยืนเรียงเทียบความสูง">
    <rect x="0" y="120" width="{LW}" height="890" fill="#1b1f2b"/><rect x="0" y="950" width="{LW}" height="60" fill="#161a24"/>
    {uses}{labels}
  </svg></div>
  <h2>ตัวละครใหม่</h2>
  <div class="grid">
    {''.join(card(k,n,d) for k,n,d,_ in INFO)}
  </div>
  <p class="note"><b>ชุดนักเรียน</b> ผ้าคลุมดำมีฮูด ซับในกับเนกไทเป็นสีบ้าน (แดงทองกับเขียวเงิน) ข้างในเป็นสเวตเตอร์เทาคอวี เชิ้ตขาว เด็กที่ยังไม่คัดบ้านใช้ซับในเทา · แฮร์รี่ เฮอร์ไมโอนี่ รอน และเดรโก วาดเป็นฉบับล้อเลียนด้วยลายเส้นของช่อง อ้างอิงลักษณะจากหนังสือ ไม่ใช้หน้านักแสดง ไม่ใช้ตราบ้านหรือตราโรงเรียน ใช้แค่สีเนกไทบอกฝั่ง · ตัวละครอื่นเป็นตัวละครของเราเอง</p>
</div>
'''
OUT.write_text(html)
print("wrote", OUT, len(html))
