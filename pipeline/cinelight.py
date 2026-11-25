"""Odd Hours · Cinematic 2D Lighting (ใช้ซ้ำได้ทุกตอน)

แยกเป็น 5 เลเยอร์ ควบคุมแยกกันได้ในแต่ละฉาก:
  1. background   ฉากหลัง (มาจากตัวสร้างฉากของแต่ละตอน)
  2. shadow       เงาสัมผัสใต้เท้า/วัตถุ + AO ตามซอกมุม (multiply, โทนเทาอมน้ำเงิน)
  3. character    ตัวละคร ห่อด้วยฟิลเตอร์ char_light(): แสงขอบส้มทองเฉพาะด้านที่โดนแสง + เงาไล่นุ่มด้านไกลแสง
                  ฟิลเตอร์อ่านจาก alpha ของตัวละครเอง จึงตามขอบตัวทุกเฟรมระหว่างเคลื่อนไหว
  4. lighting     แสงเรืองเฉพาะจุด (โคม ประตู หน้าต่าง) + ลำแสง (screen) + low-key (multiply)
  5. atmosphere   ฝุ่นที่เห็นเฉพาะในลำแสง + film grain + vignette
แล้วครอบทั้งภาพด้วย grade(): หม่นลงเล็กน้อย เงาเย็นเทาน้ำเงิน ไม่ติดเหลือง ไม่บี้ดำ

หน่วย: ตัวเลขระยะ (ความหนาแสงขอบ ฯลฯ) อยู่ใน user space ของ element ที่ใส่ฟิลเตอร์
"""
import math, random

WARM_RIM = '#ffa456'      # ส้มทองอ่อน (ผสมแบบบวกแสง จึงต้องอิ่มกว่าสีที่ตาเห็น)
WARM_GLOW = '#ffc489'
COOL_AMB = '#5d6b8f'      # เทาอมน้ำเงิน
COOL_DEEP = '#1f2638'
AO_COL = '#161b2a'

_n = [0]
def _id(p):
    _n[0] += 1
    return f'cl{p}{_n[0]}'

def _unit(dx, dy):
    m = math.hypot(dx, dy) or 1
    return dx / m, dy / m

# ---------------- shared defs ----------------
def defs(grain_seed=7):
    return f'''<filter id="clGrade" color-interpolation-filters="sRGB">
<feColorMatrix type="saturate" values=".94"/>
<feComponentTransfer><feFuncR type="table" tableValues="0.03 0.17 0.48 0.8 0.98"/><feFuncG type="table" tableValues="0.04 0.18 0.47 0.78 0.96"/><feFuncB type="table" tableValues="0.08 0.21 0.46 0.75 0.93"/></feComponentTransfer>
</filter>
<filter id="clGrain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="2" seed="{grain_seed}"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="clBlur2" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2"/></filter>
<filter id="clBlur6" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="clBlur14" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="clMoteSharp" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="clMoteSoft" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.4"/></filter>
<radialGradient id="clVig" cx=".5" cy=".47" r=".74"><stop offset=".58" stop-color="{COOL_DEEP}" stop-opacity="0"/><stop offset="1" stop-color="{COOL_DEEP}" stop-opacity=".62"/></radialGradient>'''

# ---------------- 3. character layer ----------------
def char_light(light_dir, rim=4.0, rim_col=WARM_RIM, rim_op=1.0, shade=10.0, shade_col='#56638a', shade_op=.48,
               amb_col=COOL_AMB, amb_op=.07, key_col='#ff9a4a', key_op=.45):
    """returns (filter_id, filter_svg). light_dir = vector from the character toward the light.
    rim: thickness of the lit-edge band (thicker where the edge faces the light, thinning to nothing on edges parallel to it)
    shade: width of the soft gradient on the side away from the light."""
    lx, ly = _unit(*light_dir)
    fid = _id('ch')
    f = f'''<filter id="{fid}" x="-15%" y="-10%" width="130%" height="120%" color-interpolation-filters="sRGB">
<feOffset in="SourceAlpha" dx="{-lx*rim:.2f}" dy="{-ly*rim:.2f}" result="rA"/>
<feComposite in="SourceAlpha" in2="rA" operator="out" result="rB"/>
<feGaussianBlur in="rB" stdDeviation="{rim*.3:.2f}" result="rC"/>
<feComposite in="rC" in2="SourceAlpha" operator="in" result="rD"/>
<feFlood flood-color="{rim_col}" flood-opacity="{rim_op}"/><feComposite in2="rD" operator="in" result="RIM"/>
<feOffset in="SourceAlpha" dx="{lx*shade:.2f}" dy="{ly*shade:.2f}" result="sA"/>
<feComposite in="SourceAlpha" in2="sA" operator="out" result="sB"/>
<feGaussianBlur in="sB" stdDeviation="{shade*.7:.2f}" result="sC"/>
<feComposite in="sC" in2="SourceAlpha" operator="in" result="sD"/>
<feFlood flood-color="{shade_col}" flood-opacity="{shade_op}"/><feComposite in2="sD" operator="in" result="SHADE"/>
<feFlood flood-color="{amb_col}" flood-opacity="{amb_op}"/><feComposite in2="SourceAlpha" operator="in" result="AMB"/>
<feOffset in="SourceAlpha" dx="{-lx*shade*1.6:.2f}" dy="{-ly*shade*1.6:.2f}" result="kA"/>
<feComposite in="SourceAlpha" in2="kA" operator="out" result="kB"/>
<feGaussianBlur in="kB" stdDeviation="{shade*1.2:.2f}" result="kC"/>
<feComposite in="kC" in2="SourceAlpha" operator="in" result="kD"/>
<feFlood flood-color="{key_col}" flood-opacity="{key_op}"/><feComposite in2="kD" operator="in" result="KEY"/>
<feBlend in="AMB" in2="SourceGraphic" mode="multiply" result="c1"/>
<feBlend in="SHADE" in2="c1" mode="multiply" result="c2"/>
<feBlend in="KEY" in2="c2" mode="soft-light" result="c3"/>
<feComposite in="RIM" in2="c3" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" result="c4"/>
<feComposite in="c4" in2="SourceAlpha" operator="in"/>
</filter>'''
    return fid, f

def character(svg, fid, transform=''):
    t = f' transform="{transform}"' if transform else ''
    return f'<g class="cl-character"{t}><g filter="url(#{fid})">{svg}</g></g>'

def chin_ao(cx=0, cy=30, w=18, op=.55):
    """ambient occlusion under the chin: insert between the neck and the face inside a head group"""
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{w}" ry="{w*.55:.1f}" fill="{AO_COL}" opacity="{op}" filter="url(#clBlur2)"/>'

# ---------------- 2. shadow layer ----------------
def contact_shadow(x, y, w, light_dir=(0, -1), op=.55, h=None):
    """soft shadow where a character/object touches the floor, pushed away from the light"""
    lx, ly = _unit(*light_dir)
    h = h or w * .18
    return (f'<ellipse cx="{x - lx*w*.25:.1f}" cy="{y + 2:.1f}" rx="{w*.62:.1f}" ry="{h*1.4:.1f}" fill="{AO_COL}" opacity="{op*.5:.2f}" filter="url(#clBlur6)"/>'
            f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{w*.42:.1f}" ry="{h*.55:.1f}" fill="{AO_COL}" opacity="{op:.2f}" filter="url(#clBlur2)"/>')

def ao_corner(points, op=.45):
    """occlusion band along a crease (wall/floor line, object/wall contact): pass a thin polygon"""
    return f'<polygon points="{points}" fill="{AO_COL}" opacity="{op}" filter="url(#clBlur6)" style="mix-blend-mode:multiply"/>'

def shadow_layer(*items):
    return f'<g class="cl-shadow" style="mix-blend-mode:multiply">{"".join(items)}</g>'

# ---------------- 4. lighting layer ----------------
def glow(x, y, r, col=WARM_GLOW, op=.85):
    gid = _id('gl')
    return (f'<defs><radialGradient id="{gid}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/><stop offset=".3" stop-color="{col}" stop-opacity="{op*.45:.2f}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient></defs><circle cx="{x}" cy="{y}" r="{r}" fill="url(#{gid})" style="mix-blend-mode:screen"/>')

def cone(points, col=WARM_GLOW, op=.38, axis=((0, 0), (0, 1))):
    gid = _id('cn')
    (x1, y1), (x2, y2) = axis
    return (f'<defs><linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"><stop offset="0" stop-color="{col}" stop-opacity="{op}"/>'
            f'<stop offset="1" stop-color="{col}" stop-opacity="0"/></linearGradient></defs><polygon points="{points}" fill="url(#{gid})" filter="url(#clBlur14)" style="mix-blend-mode:screen"/>')

def low_key(cx, cy, r, col=COOL_DEEP, op=.7):
    """darken everything outside the motivated light pool (multiply)"""
    gid = _id('lk')
    return (f'<defs><radialGradient id="{gid}" gradientUnits="userSpaceOnUse" cx="{cx}" cy="{cy}" r="{r}"><stop offset=".12" stop-color="#ffffff"/><stop offset="1" stop-color="{col}"/></radialGradient></defs>'
            f'<rect width="540" height="960" fill="url(#{gid})" opacity="{op}" style="mix-blend-mode:multiply"/>')

def ambient(col=COOL_AMB, op=.3):
    """cool blue-grey fill over the whole frame so shadows read cool against warm lights"""
    return f'<rect width="540" height="960" fill="{col}" opacity="{op}" style="mix-blend-mode:multiply"/>'

def lighting_layer(*items):
    return f'<g class="cl-lighting">{"".join(items)}</g>'

# ---------------- 5. atmosphere layer ----------------
def dust_in(points, seed=1, n=40, col='#ffe6c8'):
    """dust motes that only show inside a light shaft (clipped to it)"""
    cid = _id('dc')
    xs = [float(p.split(',')[0]) for p in points.split()]; ys = [float(p.split(',')[1]) for p in points.split()]
    r = random.Random(seed)
    far = ''.join(f'<circle cx="{r.uniform(min(xs),max(xs)):.0f}" cy="{r.uniform(min(ys),max(ys)):.0f}" r="{r.uniform(1.2,2.4):.1f}" opacity="{r.uniform(.25,.5):.2f}"/>' for _ in range(n))
    near = ''.join(f'<circle cx="{r.uniform(min(xs),max(xs)):.0f}" cy="{r.uniform(min(ys),max(ys)):.0f}" r="{r.uniform(.5,1.1):.1f}" opacity="{r.uniform(.6,1):.2f}"/>' for _ in range(n // 2))
    return (f'<clipPath id="{cid}"><polygon points="{points}"/></clipPath><g clip-path="url(#{cid})" fill="{col}">'
            f'<g filter="url(#clMoteSoft)">{far}</g><g filter="url(#clMoteSharp)">{near}</g></g>')

def atmosphere_layer(*items, grain=.07, vignette=True):
    v = '<rect width="540" height="960" fill="url(#clVig)"/>' if vignette else ''
    return (f'<g class="cl-atmosphere">{"".join(items)}{v}'
            f'<rect width="540" height="960" filter="url(#clGrain)" opacity="{grain}" style="mix-blend-mode:overlay"/></g>')

# ---------------- compose ----------------
def env_layer(*items):
    """multiply passes (ambient, low_key) that grade the SET only; characters sit above it and get their own light"""
    return f'<g class="cl-env">{"".join(items)}</g>'

def compose(background, shadow='', env='', character='', lighting='', atmosphere='', grade=True):
    """order: background -> shadow -> env (set darkening) -> character -> lighting (screen glows over all) -> atmosphere"""
    g = ' filter="url(#clGrade)"' if grade else ''
    return (f'<g class="cl-frame"{g}><g class="cl-background">{background}</g>{shadow}{env}{character}{lighting}</g>{atmosphere}')
