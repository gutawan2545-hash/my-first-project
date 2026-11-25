"""Odd Hours · ระบบแสงเงาแบบหนัง 2D (Cinematic 2D Lighting) ใช้ซ้ำได้ทุกตอน

แยกเป็น 4 ชั้น ควบคุมแยกกันต่อฉาก:
  1) Character Layer  : ตัวละครเดิม + ฟิลเตอร์ rim/shade ต่อชิ้นส่วน (หัว ตัว แขน) แสงติดไปกับตัวละครตอนขยับ
  2) Shadow Layer     : เงาสัมผัสใต้เท้า AO ใต้คาง และเงาแวดล้อมโทนเย็น (ทำ low-key ได้ เว้นวงแสงตรงแหล่งกำเนิดแสง)
  3) Lighting Layer   : แสงเรืองเฉพาะจุด (โคม เทียน ประตู หน้าต่าง จอมือถือ) แบบ screen
  4) Atmospheric Layer: ขอบภาพมืด เกรนฟิล์ม ฝุ่นในลำแสง คุมสี (อยู่ใน filmFX ของตัวเรนเดอร์)

ใช้งาน:
    import cinelight as CL
    L = CL.Light(dir=(-.7, -.6), rim='#ffb36b', shade='#2f3a66', ambient='#26304f', ambient_op=.32, lowkey=.0,
                 glows=[(70, 330, 90, '#ffb36b', .35)], pools=[(70, 330, 140)])
    defs = CL.defs({'s3': L, ...})                      # ใส่ครั้งเดียวในหน้า
    CL.char_attr('s3')                                  # -> 'filter="url(#clRim_s3)"' ใส่ที่ <g> หัว/ตัว/แขนของตัวละคร
    CL.scene_layers('s3', L)                            # ใส่ท้ายกลุ่มกล้องของช็อต (ชั้นเงา + ชั้นแสง เคลื่อนไปกับฉาก)
    CL.contact_shadow(x, feet, s)                       # เงาสัมผัสใต้เท้า
    CL.AO_NECK                                          # AO ใต้คาง วางหลังตัวก่อนหัว
dir คือทิศ "ไปหาแหล่งแสง" จากตัวละคร (เช่น แสงมาจากซ้ายบน = (-.7, -.6))
"""
from dataclasses import dataclass, field
import math

@dataclass
class Light:
    dir: tuple = (-.7, -.6)          # ทิศไปหาแหล่งแสงหลัก
    rim: str = '#ffb36b'             # แสงขอบสีส้มทองอ่อน
    rim_op: float = .95
    rim_w: float = 3.2               # ความหนาแสงขอบ (หน่วยของตัวละครก่อนย่อขยาย)
    shade: str = '#5a63a0'           # เงานุ่มฝั่งไกลแสง โทนเทาอมน้ำเงิน
    shade_op: float = .30
    shade_w: float = 11
    ambient: str = '#5a6596'         # เงาแวดล้อมโทนเย็นทับฉากหลัง (multiply) ตัวละครคุมแสงเองด้วยฟิลเตอร์
    ambient_op: float = .22
    char_exp: float = 1.0            # ความสว่างตัวละคร (ฉากกลางคืน .85-.9 ให้กลืนกับฉาก แต่ยังเห็นหน้าชัด)
    lowkey: float = 0.0              # 0-1 ยิ่งมากยิ่งมืดนอกวงแสง (ฉากกลางคืน/ลึกลับ)
    glows: list = field(default_factory=list)   # [(x, y, r, color, opacity)] แสงเรืองเฉพาะจุด
    pools: list = field(default_factory=list)   # [(x, y, r)] วงแสงที่เว้นจากความมืดแบบ low-key

def _n(d):
    l = math.hypot(*d) or 1
    return d[0] / l, d[1] / l

def rim_filter(fid, L):
    dx, dy = _n(L.dir)
    return (f'<filter id="{fid}" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">'
            # ขอบฝั่งรับแสง: จุดที่อยู่ในตัว แต่ถัดไปทางแสงเป็นพื้นว่าง -> หนาบางต่างกันเองตามมุมของขอบเทียบทิศแสง
            f'<feOffset in="SourceAlpha" dx="{-dx * L.rim_w:.2f}" dy="{-dy * L.rim_w:.2f}" result="o1"/>'
            f'<feComposite in="SourceAlpha" in2="o1" operator="out" result="e1"/>'
            f'<feOffset in="SourceAlpha" dx="{-dx * L.rim_w * .45:.2f}" dy="{-dy * L.rim_w * .45:.2f}" result="o2"/>'
            f'<feComposite in="SourceAlpha" in2="o2" operator="out" result="e2"/>'
            f'<feGaussianBlur in="e1" stdDeviation="{L.rim_w * .45:.2f}" result="e1b"/>'
            f'<feComposite in="e1b" in2="SourceAlpha" operator="in" result="e1c"/>'
            f'<feComponentTransfer in="e1c" result="e1d"><feFuncA type="linear" slope=".55"/></feComponentTransfer>'
            f'<feMerge result="edge"><feMergeNode in="e1d"/><feMergeNode in="e2"/></feMerge>'
            f'<feFlood flood-color="{L.rim}" flood-opacity="{L.rim_op}"/><feComposite in2="edge" operator="in" result="rim"/>'
            # เงานุ่มไล่เฉดฝั่งไกลแสง (soft gradient shading)
            f'<feOffset in="SourceAlpha" dx="{dx * L.shade_w:.2f}" dy="{dy * L.shade_w:.2f}" result="o3"/>'
            f'<feComposite in="SourceAlpha" in2="o3" operator="out" result="far"/>'
            f'<feGaussianBlur in="far" stdDeviation="{L.shade_w * .55:.2f}" result="farb"/>'
            f'<feComposite in="farb" in2="SourceAlpha" operator="in" result="farc"/>'
            f'<feFlood flood-color="{L.shade}" flood-opacity="{L.shade_op}"/><feComposite in2="farc" operator="in" result="shade"/>'
            f'<feBlend in="shade" in2="SourceGraphic" mode="multiply" result="s1"/>'
            f'<feComposite in="s1" in2="SourceAlpha" operator="in" result="s2"/>'
            f'<feComponentTransfer in="s2" result="s2e"><feFuncR type="linear" slope="{L.char_exp}"/><feFuncG type="linear" slope="{L.char_exp}"/><feFuncB type="linear" slope="{min(1.0, L.char_exp + .05)}"/></feComponentTransfer>'
            f'<feBlend in="rim" in2="s2e" mode="screen" result="s3"/>'
            f'<feComposite in="s3" in2="SourceAlpha" operator="in"/></filter>')

def defs(lights):
    o = ['<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>',
         '<filter id="clSoft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>',
         '<filter id="clAO" x="-50%" y="-80%" width="200%" height="260%"><feGaussianBlur stdDeviation="3.2"/></filter>',
         '<radialGradient id="clGlow"><stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset=".35" stop-color="#fff" stop-opacity=".45"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>',
         '<radialGradient id="clPool"><stop offset="0" stop-color="#000"/><stop offset=".55" stop-color="#000" stop-opacity=".75"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>',
         '<radialGradient id="clContact"><stop offset="0" stop-color="#0c0a16" stop-opacity=".75"/><stop offset=".6" stop-color="#0c0a16" stop-opacity=".3"/><stop offset="1" stop-color="#0c0a16" stop-opacity="0"/></radialGradient>']
    cols = sorted({c for L in lights.values() for _, _, _, c, _ in L.glows})
    for c in cols:   # แสงเรือง: แกนสว่างเล็ก ๆ แล้วฟุ้งจางออก
        o.append(f'<radialGradient id="clG{c[1:]}"><stop offset="0" stop-color="#fff8ee" stop-opacity=".95"/><stop offset=".08" stop-color="{c}" stop-opacity=".9"/>'
                 f'<stop offset=".3" stop-color="{c}" stop-opacity=".35"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient>')
    for k, L in lights.items():
        o.append(rim_filter(f'clRim_{k}', L))
        if L.pools:
            o.append(f'<mask id="clMask_{k}" maskUnits="userSpaceOnUse" x="-200" y="-200" width="940" height="1360">'
                     '<rect x="-200" y="-200" width="940" height="1360" fill="#fff"/>' +
                     ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#clPool)"/>' for x, y, r in L.pools) + '</mask>')
    o.append('</defs></svg>')
    return ''.join(o)

def char_attr(k):
    return f'filter="url(#clRim_{k})"'

def shadow_layer(k, L):
    """ชั้นเงาแวดล้อม + low-key วางทับฉากหลัง แต่อยู่ใต้ตัวละคร"""
    m = f' mask="url(#clMask_{k})"' if L.pools else ''
    return (f'<g class="clShadow"><rect x="-200" y="-200" width="940" height="1360" fill="{L.ambient}" opacity="{L.ambient_op}" style="mix-blend-mode:multiply"/>'
            + (f'<rect x="-200" y="-200" width="940" height="1360" fill="#0a0914" opacity="{L.lowkey * .6:.3f}" style="mix-blend-mode:multiply"{m}/>' if L.lowkey else '') + '</g>')

def light_layer(k, L):
    """ชั้นแสงเรืองเฉพาะจุด วางบนสุดของฉาก (screen)"""
    return ('<g class="clLight" style="mix-blend-mode:screen">' +
            ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#clG{c[1:]})" opacity="{op}"/>' for x, y, r, c, op in L.glows) + '</g>')

def scene_layers(k, L):
    return shadow_layer(k, L) + light_layer(k, L)

def contact_shadow(x, feet, s, w=62):
    return f'<ellipse cx="{x + 6 * s:.1f}" cy="{feet + 2 * s:.1f}" rx="{w * s:.1f}" ry="{9 * s:.1f}" fill="url(#clContact)"/>'

AO_NECK = '<ellipse cx="0" cy="45" rx="15" ry="7" fill="#1e1a33" opacity=".38" filter="url(#clAO)"/>'

STANDARD = """Cinematic 2D Lighting (มาตรฐานช่อง): แสงขอบส้มทองอ่อนเฉพาะฝั่งรับแสง หนาบางตามทิศแสง · เงานุ่มไล่เฉดฝั่งไกลแสงโทนเทาอมน้ำเงิน ·
เงาแวดล้อมเย็นตัดกับแสงอุ่น · low-key สำหรับฉากกลางคืน/ลึกลับ (เว้นวงแสงตรงแหล่งกำเนิดแสง) · แสงเรืองเฉพาะจุดที่โคม ประตู หน้าต่าง ·
เงาสัมผัสใต้เท้า AO ใต้คาง · ขอบภาพมืดนุ่ม เกรนฟิล์มบาง ฝุ่นในลำแสง · คุมสีหม่นเล็กน้อย ห้ามติดเหลืองทั้งภาพ ห้ามมืดจนไม่เห็นหน้า"""
