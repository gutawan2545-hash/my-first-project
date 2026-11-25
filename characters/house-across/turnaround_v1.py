#!/usr/bin/env python3
"""บ้านตรงข้าม: มุมหมุนรอบตัว (หน้า · ซ้าย · หลัง · ขวา) ท่ายืนตรงเป็นกลาง
หน้าตรงใช้หัวจากแผ่นที่ผ่านแล้ว (leads/cops/others) · มุมข้างหันเต็ม 90 องศา · ลายเส้นเดิม ไม่มีเส้นขอบ เงาบล็อก
รัน: python3 turnaround.py -> turnaround.html"""
import re

def defs_of(fn):
    s = open(fn, encoding='utf-8').read()
    d = s[s.index('<defs>') + 6: s.index('</defs>')]
    return re.sub(r'<linearGradient id="skyBg".*?</linearGradient>', '', d, flags=re.S)
HEAD_DEFS = defs_of('leads.html') + defs_of('cops.html') + defs_of('others.html')

def mirror_x(d):
    """mirror an SVG path's x coordinates (absolute commands only)"""
    parts = re.split(r'([MCLQZ])', d); res = []
    for p in parts:
        if p in ('M', 'C', 'L', 'Q', 'Z'): res.append(p); continue
        nums = re.findall(r'-?\d+\.?\d*', p)
        res.append(' ' + ' '.join(f'{-float(nums[i]):g},{nums[i+1]}' for i in range(0, len(nums), 2)) + ' ')
    return ''.join(res)

# ---------------- character specs ----------------
C = {
 'hero':   dict(name='พระเอก', note='ชุดอยู่บ้าน เฝือกขาซ้าย ไม้ค้ำยันสองข้าง', skin=('#e9bf98', '#d6a47e', '#f6d5b4'), hair='#1a1517', hair_lt='#3c3236',
              top='tee', tc=('#7f9cc8', '#a0b8de', '#6380b0'), bot=('#56607c', '#7280a0', '#454e68'), shoe='#3e4560',
              w=50, sh=48, hem=244, foot=470, ty=140, sc=1.18, head='hero', cast=True, crutch=True, style='crop', face=31),
 'heroine':dict(name='นางเอก', note='เดรสซาตินชมพูกุหลาบ แว่นแคทอาย', skin=('#f6d6bc', '#e6b597', '#fff0e3'), hair='#221519', hair_lt='#4a2d36',
              top='dress', tc=('#d88d9c', '#eeb0bb', '#b86c7e'), bot=None, shoe='#17151b',
              w=40, sh=50, hem=394, foot=490, ty=150, sc=1.2, head='heroine', style='bob', face=30, glasses=True),
 'moo':    dict(name='หมู', note='เพื่อนตำรวจคนอ้วน เครื่องแบบกากี', skin=('#d9a47a', '#c08a62', '#e8b890'), hair='#2a2224', hair_lt='#4a3e42',
              top='uniform', tc=('#8a6c4a', '#a38563', '#6a5136'), bot=('#7a5e40', '#92755a', '#5c452e'), shoe='#15151a',
              w=56, sh=46, hem=238, foot=468, ty=186, sc=1.18, head='moo', belly=True, style='buzz', face=38, stache=True),
 'ton':    dict(name='ต้น', note='เพื่อนตำรวจคนผอม เครื่องแบบกากี แว่นนักบินบนหัว', skin=('#efc8a2', '#dcae88', '#fadbbd'), hair='#1e1a1c', hair_lt='#433a3e',
              top='uniform', tc=('#8a6c4a', '#a38563', '#6a5136'), bot=('#7a5e40', '#92755a', '#5c452e'), shoe='#15151a',
              w=40, sh=56, hem=260, foot=540, ty=112, sc=1.15, head='ton', style='pomp', face=26, shades=True),
 'husband':dict(name='สามีบ้านตรงข้าม', note='เชิ้ตแขนยาวเทาเข้ม สแล็กสีถ่าน', skin=('#f3cfae', '#deb08c', '#fbe2c8'), hair='#17141a', hair_lt='#3c3640',
              top='long', tc=('#4a4a56', '#5c5c6a', '#383842'), bot=('#34343e', '#44444f', '#26262e'), shoe='#2a2024',
              w=44, sh=48, hem=238, foot=468, ty=170, sc=1.22, head='husband', style='slick', face=29),
 'wife':   dict(name='ภรรยาบ้านตรงข้าม', note='เดรสเขียวหม่น ผมมัดครึ่งหัว', skin=('#f1c9a6', '#dba684', '#fadcc0'), hair='#2a1a1c', hair_lt='#4a3236',
              top='dress2', tc=('#7d9a88', '#94b09e', '#647e6e'), bot=None, shoe='#c9b8a8',
              w=44, sh=48, hem=396, foot=470, ty=172, sc=1.22, head='wife', style='halfup', face=29),
}
FRONT_HEAD = {'hero': '<use href="#hhead"/><use href="#hhair"/>', 'heroine': '<use href="#gback"/><use href="#ghead"/>',
              'moo': '<use href="#ahead"/>', 'ton': '<use href="#bhead"/>', 'husband': '<use href="#hb"/>', 'wife': '<use href="#wf"/>'}

# ---------------- front (neutral) ----------------
def legs_front(c):
    b, lt, dk = c['bot']; y0, y1 = c['hem'] - 6, c['foot']; w = min(c['w'] - 8, 44)
    o = (f'<path d="M -{w},{y0} L {w},{y0} L {w+2},{y0+70} L {w-6},{y1} L 8,{y1} L 2,{y0+62} L -2,{y0+62} L -8,{y1} L -{w-6},{y1} L -{w+2},{y0+70} Z" fill="{b}"/>'
         f'<path d="M -{w},{y0} L -{w-14},{y0} L -{w-12},{y0+70} L -{w-14},{y1} L -{w-6},{y1} L -{w+2},{y0+70} Z" fill="{lt}"/>'
         f'<path d="M {w-16},{y0+6} L {w},{y0} L {w+2},{y0+70} L {w-6},{y1} L {w-16},{y1} Z" fill="{dk}"/>')
    if c.get('cast'):  # cast on the viewer's right leg below the knee
        k = y0 + 140
        o += (f'<path d="M 4,{k} L {w-2},{k} L {w-4},{y1+6} C {w-2},{y1+16} {w-6},{y1+22} {w-14},{y1+22} L 14,{y1+22} C 6,{y1+20} 4,{y1+14} 6,{y1+6} Z" fill="#e8e5e0"/>'
              f'<path d="M {w-14},{k} L {w-2},{k} L {w-4},{y1+6} C {w-2},{y1+16} {w-6},{y1+22} {w-14},{y1+22} Z" fill="#c8c4be"/>'
              f'<path d="M 6,{k+40} L {w-3},{k+38} M 6,{k+80} L {w-3},{k+78}" stroke="#cfcbc5" stroke-width="1.2"/>')
    return o

def shoes_front(c, cast=False):
    y = c['foot']; s = c['shoe']
    l = f'<path d="M -40,{y} L -8,{y} C -6,{y+9} -8,{y+15} -12,{y+16} L -42,{y+16} C -46,{y+14} -45,{y+4} -40,{y} Z" fill="{s}"/>'
    r = '' if cast else f'<path d="M 40,{y} L 8,{y} C 6,{y+9} 8,{y+15} 12,{y+16} L 42,{y+16} C 46,{y+14} 45,{y+4} 40,{y} Z" fill="{s}"/>'
    return l + r

def arms_front(c, sleeve_col=None):
    s, sh, lt = c['skin']; w = c['w']; y = c['sh']; hand = c['hem'] - 14 if c['top'] not in ('dress', 'dress2') else 226
    out = (f'<path d="M -{w+6},{y+20} L -{w-8},{y+26} L -{w-6},{hand} L -{w+8},{hand} L -{w+10},{y+100} Z" fill="{s}"/>'
           f'<path d="M {w+6},{y+20} L {w-8},{y+26} L {w-6},{hand} L {w+8},{hand} L {w+10},{y+100} Z" fill="{sh}"/>'
           f'<path d="M -{w+8},{hand-2} L -{w-6},{hand-2} C -{w-5},{hand+12} -{w-7},{hand+22} -{w+1},{hand+24} C -{w+7},{hand+24} -{w+10},{hand+12} -{w+8},{hand-2} Z" fill="{s}"/>'
           f'<path d="M {w+8},{hand-2} L {w-6},{hand-2} C {w-5},{hand+12} {w-7},{hand+22} {w+1},{hand+24} C {w+7},{hand+24} {w+10},{hand+12} {w+8},{hand-2} Z" fill="{sh}"/>')
    if sleeve_col:
        c1, c2, slen = sleeve_col
        out += (f'<path d="M -{w+6},{y+18} L -{w-8},{y+24} L -{w-7},{y+slen} L -{w+10},{y+slen-4} Z" fill="{c1}"/>'
                f'<path d="M {w+6},{y+18} L {w-8},{y+24} L {w-7},{y+slen} L {w+10},{y+slen-4} Z" fill="{c2}"/>')
    return out

def torso_front(c, back=False):
    m, lt, dk = c['tc']; w = c['w']; y = c['sh']; hem = c['hem']
    if c.get('belly'):
        body = (f'M -16,{y} L 16,{y} C 36,{y+2} {w-2},{y+10} {w+2},{y+22} L {w-2},{y+84} C {w+12},{y+114} {w+16},{y+152} {w+4},{y+180} '
                f'C {w-10},{y+204} -{w-10},{y+204} -{w+4},{y+180} C -{w+16},{y+152} -{w+12},{y+114} -{w-2},{y+84} L -{w+2},{y+22} C -{w-2},{y+10} -36,{y+2} -16,{y} Z')
    else:
        body = (f'M -12,{y} L 12,{y} C 28,{y+2} {w-4},{y+7} {w+2},{y+18} L {w-6},{y+52} L {w-4},{hem} L -{w-4},{hem} L -{w-6},{y+52} L -{w+2},{y+18} C -{w-4},{y+7} -28,{y+2} -12,{y} Z')
    o = [f'<path d="{body}" fill="{m}"/>',
         f'<path d="M -{w+2},{y+18} C -{w-4},{y+7} -28,{y+2} -18,{y+1} C -26,{y+30} -28,{y+90} -26,{hem} L -{w-4},{hem} L -{w-6},{y+52} Z" fill="{lt}" opacity=".9"/>',
         f'<path d="M 20,{y+1} C 32,{y+4} {w-2},{y+9} {w+2},{y+18} L {w-6},{y+52} L {w-4},{hem} L 26,{hem} C 28,{y+120} 28,{y+50} 20,{y+1} Z" fill="{dk}" opacity=".9"/>']
    if c['top'] == 'uniform':
        o.append(f'<path d="M -{w+2},{y+18} L {w+2},{y+18} L {w+2},{y+24} L -{w+2},{y+24} Z" fill="none"/>')
        if not back:
            o.append(f'<path d="M -1.6,{y+14} L 1.6,{y+14} L 1.6,{hem} L -1.6,{hem} Z" fill="{lt}" opacity=".5"/>' + ''.join(f'<circle cx="0" cy="{yy}" r="1.6" fill="#c7a46a"/>' for yy in range(y + 50, hem, 38)))
            o.append(f'<path d="M -{w-12},{y+46} L -{w-34},{y+46} L -{w-34},{y+70} L -{w-12},{y+70} Z" fill="{lt}"/><rect x="-{w-12}" y="{y+32}" width="22" height="6" rx="1" fill="#17161c"/>')
            o.append(f'<path d="M {w-34},{y+22} L {w-26},{y+25} L {w-27},{y+34} C {w-28},{y+38} {w-31},{y+40} {w-34},{y+41} C {w-37},{y+40} {w-40},{y+38} {w-41},{y+34} L {w-42},{y+25} Z" fill="#c4c9d4"/>')
        o.append(f'<path d="M -{w},{y+14} L -24,{y+6} L -22,{y+12} L -{w-2},{y+21} Z M {w},{y+14} L 24,{y+6} L 22,{y+12} L {w-2},{y+21} Z" fill="#1f2433"/>')
        bl = hem - 8 if not c.get('belly') else y + 186
        o.append(f'<rect x="-{w-2}" y="{bl}" width="{2*(w-2)}" height="10" fill="#17161c"/>' + ('' if back else f'<rect x="-7" y="{bl-1}" width="14" height="12" rx="1.5" fill="#b9bec9"/>'))
    elif c['top'] == 'long' and not back:
        o.append(f'<path d="M -2,{y+10} L 2,{y+10} L 2,{hem} L -2,{hem} Z" fill="{dk}"/>' + ''.join(f'<circle cx="0" cy="{yy}" r="1.5" fill="#8a8a96"/>' for yy in range(y + 50, hem, 40)))
        o.append(f'<rect x="-{w-2}" y="{hem-8}" width="{2*(w-2)}" height="9" fill="#1f1d24"/>')
    elif c['top'] == 'long':
        o.append(f'<rect x="-{w-2}" y="{hem-8}" width="{2*(w-2)}" height="9" fill="#1f1d24"/><path d="M -{w-4},{y+26} L {w-4},{y+26}" stroke="{dk}" stroke-width="2"/>')
    elif c['top'] == 'tee' and back:
        o.append(f'<path d="M -10,{y} C -6,{y+6} 6,{y+6} 10,{y}" fill="none" stroke="{dk}" stroke-width="3"/>')
    return ''.join(o)

def dress_front(c, back=False):
    m, lt, dk = c['tc']; s, sh, _ = c['skin']; y = c['sh']; hem = c['hem']; foot = c['foot']
    o = []
    # legs + shoes
    o.append(f'<rect x="-24" y="{hem-6}" width="14" height="{foot-hem+8}" fill="{s}"/><rect x="10" y="{hem-6}" width="14" height="{foot-hem+8}" fill="{sh}"/>')
    o.append(f'<path d="M -28,{foot} L -8,{foot} C -6,{foot+7} -8,{foot+12} -12,{foot+13} L -30,{foot+13} C -34,{foot+11} -33,{foot+4} -28,{foot} Z" fill="{c["shoe"]}"/>'
             f'<path d="M 28,{foot} L 8,{foot} C 6,{foot+7} 8,{foot+12} 12,{foot+13} L 30,{foot+13} C 34,{foot+11} 33,{foot+4} 28,{foot} Z" fill="{c["shoe"]}"/>')
    if c['top'] == 'dress':   # slip dress, bare shoulders
        o.append(f'<path d="M -12,{y+2} C -28,{y+4} -38,{y+8} -42,{y+18} L -36,{y+50} L 36,{y+50} L 42,{y+18} C 38,{y+8} 28,{y+4} 12,{y+2} Z" fill="{s}"/>')
        top = y + 36 if not back else y + 46
        o.append(f'<path d="M -30,{top} C -10,{top+12} 10,{top+12} 30,{top} L 33,{y+62} C 32,{y+82} 28,{y+100} 24,{y+112} C 34,{y+132} 40,{y+154} 40,{y+176} L 40,{hem} L -40,{hem} L -40,{y+176} C -40,{y+154} -34,{y+132} -24,{y+112} C -28,{y+100} -32,{y+82} -33,{y+62} Z" fill="{m}"/>')
        o.append(f'<path d="M -30,{top} C -24,{top+6} -20,{top+8} -16,{top+9} C -22,{y+80} -20,{y+100} -12,{y+114} C -22,{y+140} -28,{y+176} -26,{hem} L -40,{hem} L -40,{y+176} C -40,{y+154} -34,{y+132} -24,{y+112} C -28,{y+100} -32,{y+82} -33,{y+62} Z" fill="{lt}"/>')
        o.append(f'<path d="M 18,{top+9} C 24,{top+6} 28,{top+3} 30,{top} L 33,{y+62} C 32,{y+82} 28,{y+100} 24,{y+112} C 34,{y+132} 40,{y+154} 40,{y+176} L 40,{hem} L 30,{hem} C 30,{y+230} 30,{y+180} 22,{y+120} C 26,{y+96} 24,{y+70} 18,{top+9} Z" fill="{dk}"/>')
        if back:
            o.append(f'<path d="M -26,{y+4} L 26,{top+4} M 26,{y+4} L -26,{top+4}" stroke="#b35d72" stroke-width="2" stroke-linecap="round"/>')
        else:
            o.append(f'<path d="M -27,{top+2} L -24,{y+6} M 27,{top+2} L 24,{y+6}" stroke="#b35d72" stroke-width="2" stroke-linecap="round"/>')
    else:                     # dress2: puff sleeves, waistband
        o.append(f'<path d="M -14,{y} L 14,{y} C 30,{y+2} 42,{y+8} 46,{y+18} L 40,{y+62} L 34,{y+102} C 50,{y+172} 62,{y+272} 66,{hem} L -66,{hem} C -62,{y+272} -50,{y+172} -34,{y+102} L -40,{y+62} L -46,{y+18} C -42,{y+8} -30,{y+2} -14,{y} Z" fill="{m}"/>')
        o.append(f'<path d="M -46,{y+18} C -42,{y+8} -30,{y+2} -20,{y+1} C -24,{y+42} -26,{y+82} -22,{y+104} C -36,{y+182} -42,{y+272} -44,{hem} L -66,{hem} C -62,{y+272} -50,{y+172} -34,{y+102} L -40,{y+62} Z" fill="{lt}"/>')
        o.append(f'<path d="M 20,{y+1} C 32,{y+4} 42,{y+9} 46,{y+18} L 40,{y+62} L 34,{y+102} C 50,{y+172} 62,{y+272} 66,{hem} L 44,{hem} C 42,{y+252} 36,{y+172} 24,{y+106} C 28,{y+72} 26,{y+32} 20,{y+1} Z" fill="{dk}"/>')
        o.append(f'<path d="M -36,{y+100} L 36,{y+100} L 35,{y+108} L -35,{y+108} Z" fill="#5a7262"/>')
        o.append(f'<path d="M -46,{y+16} C -58,{y+18} -60,{y+42} -52,{y+52} L -38,{y+48} Z" fill="{lt}"/><path d="M 46,{y+16} C 58,{y+18} 60,{y+42} 52,{y+52} L 38,{y+48} Z" fill="{dk}"/>')
        if not back: o.append(f'<path d="M -10,{y} Q 0,{y+14} 10,{y}" fill="{s}"/>')
    return ''.join(o)

def crutches_front(c):
    w = c['w']; y = c['sh']
    return (f'<rect x="-{w+25}" y="{y+84}" width="4.6" height="{c["foot"]-y-70}" fill="#a3a9b6"/><rect x="{w+20}" y="{y+84}" width="4.6" height="{c["foot"]-y-70}" fill="#7d8391"/>'
            f'<rect x="-{w+29}" y="{y+76}" width="13" height="10" rx="4" fill="#4a4e5c"/><rect x="{w+16}" y="{y+76}" width="13" height="10" rx="4" fill="#3a3d49"/>')

def front_view(k):
    c = CH = C[k]
    o = []
    if c.get('crutch'): o.append(crutches_front(c))
    if c['top'] in ('dress', 'dress2'):
        o.append(arms_front(c) + dress_front(c))
    else:
        o.append(shoes_front(c, c.get('cast')) + legs_front(c))
        sl = (c['tc'][1], c['tc'][2], 66 if c['top'] in ('tee', 'uniform') else 178)
        o.append(arms_front(c, sl) + torso_front(c))
    o.append(FRONT_HEAD[k])
    if c['top'] == 'uniform':
        o.append(f'<path d="M -12,{c["sh"]} L -3,{c["sh"]+14} L -19,{c["sh"]+10} Z" fill="{c["tc"][1]}"/><path d="M 12,{c["sh"]} L 3,{c["sh"]+14} L 19,{c["sh"]+10} Z" fill="{c["tc"][2]}"/>')
    elif c['top'] == 'tee':
        o.append(f'<path d="M -12,{c["sh"]} C -8,{c["sh"]+12} 8,{c["sh"]+12} 12,{c["sh"]}" fill="none" stroke="{c["tc"][2]}" stroke-width="4"/>')
    elif c['top'] == 'long':
        o.append(f'<path d="M -12,{c["sh"]} L -2,{c["sh"]+16} L -18,{c["sh"]+12} Z M 12,{c["sh"]} L 2,{c["sh"]+16} L 18,{c["sh"]+12} Z" fill="{c["tc"][1]}"/>')
    return ''.join(o)

# ---------------- back ----------------
def head_back(c):
    s, sh, lt = c['skin']; hc, hl = c['hair'], c['hair_lt']; w = c['face']; st = c['style']
    o = [f'<rect x="-9" y="18" width="18" height="40" fill="{sh}"/>',
         f'<ellipse cx="-{w}" cy="-1" rx="5" ry="8.6" fill="{s}"/><ellipse cx="{w}" cy="-1" rx="5" ry="8.6" fill="{sh}"/>']
    if st == 'crop':
        o.append(f'<path d="M -{w},-6 C -{w+4},-44 -20,-62 0,-62 C 20,-62 {w+4},-44 {w},-6 L {w-2},12 C 18,20 -18,20 -{w-2},12 Z" fill="{hc}"/>'
                 f'<path d="M -{w-2},6 C -18,14 18,14 {w-2},6 L {w-2},12 C 18,20 -18,20 -{w-2},12 Z" fill="#4a3f44"/><path d="M -20,-46 C -10,-56 10,-58 22,-50 C 8,-52 -6,-50 -16,-42 Z" fill="{hl}"/>')
    elif st == 'buzz':
        o.append(f'<path d="M -{w},-10 C -{w+2},-44 -22,-55 0,-55 C 22,-55 {w+2},-44 {w},-10 C {w-2},8 -{w-2},8 -{w},-10 Z" fill="{hc}"/><path d="M -28,-40 C -16,-50 4,-52 16,-48 C 2,-46 -12,-42 -22,-34 Z" fill="{hl}"/>'
                 f'<path d="M -16,26 Q 0,32 16,26" fill="none" stroke="{sh}" stroke-width="3"/>')
    elif st == 'pomp':
        o.append(f'<path d="M -{w+2},-6 C -{w+6},-44 -18,-64 2,-63 C 24,-64 {w+8},-44 {w+2},-6 L {w+2},30 L 18,26 L 0,30 L -18,26 L -{w+2},30 Z" fill="{hc}"/><path d="M -18,-48 C -6,-60 14,-62 26,-52 C 12,-54 -2,-52 -12,-44 Z" fill="{hl}"/>')
        o.append('<path d="M -22,-48 C -10,-52 10,-52 22,-48" fill="none" stroke="#c8b07a" stroke-width="2"/>')  # sunglasses arms seen from behind
    elif st == 'slick':
        o.append(f'<path d="M -{w+1},-6 C -{w+5},-42 -20,-61 0,-61 C 22,-61 {w+5},-42 {w+1},-6 C {w-2},12 -{w-2},12 -{w+1},-6 Z" fill="{hc}"/>'
                 + ''.join(f'<path d="M {x},-58 C {x*1.2:.0f},-30 {x*1.1:.0f},-10 {x},6" fill="none" stroke="{hl}" stroke-width="1.6"/>' for x in (-14, -4, 6, 16)))
    elif st == 'bob':
        o.append(f'<path d="M -40,-6 C -42,-46 -22,-63 0,-63 C 22,-63 42,-46 40,-6 L 41,30 C 34,38 26,37 22,33 L -22,33 C -26,37 -34,38 -41,30 Z" fill="{hc}"/>'
                 f'<path d="M -30,-42 C -22,-54 -10,-58 0,-58 C -10,-53 -20,-46 -26,-34 Z" fill="{hl}"/><path d="M -2,-58 L 0,30" stroke="#160c10" stroke-width="1.4" opacity=".5"/>'
                 f'<path d="M -38,-2 L -44,-4 M 38,-2 L 44,-4" stroke="#2c1a24" stroke-width="1.3"/>')
    elif st == 'halfup':
        o.append(f'<path d="M -37,-6 C -40,-46 -20,-62 0,-62 C 20,-62 40,-46 37,-6 L 42,118 C 30,126 -30,126 -42,118 Z" fill="{hc}"/><path d="M -37,-6 L -42,118 L -36,120 L -33,0 Z" fill="{hl}"/>'
                 f'<path d="M -30,-30 C -16,-24 16,-24 30,-30 L 4,-14 L -4,-14 Z" fill="#221416"/><ellipse cx="0" cy="-16" rx="7" ry="5" fill="#7d9a88"/>'
                 f'<path d="M -4,-14 C -8,10 -6,40 -10,70 M 4,-14 C 8,10 6,40 10,70" fill="none" stroke="{hl}" stroke-width="1.6"/>')
    return ''.join(o)

def back_view(k):
    c = dict(C[k])
    o = []
    if c.get('crutch'): o.append(crutches_front(c))
    if c['top'] in ('dress', 'dress2'):
        o.append(arms_front(c) + dress_front(c, back=True))
        o.append(head_back(c))
    else:
        cc = dict(c)
        if cc.get('cast'):   # seen from behind the cast is on the viewer's left
            o.append(f'<g transform="scale(-1,1)">{legs_front(cc)}</g>' + f'<g transform="scale(-1,1)">{shoes_front(cc, True)}</g>')
            # back pockets
        else:
            o.append(shoes_front(cc) + legs_front(cc))
        b = cc['bot']
        o.append(f'<path d="M -30,{c["hem"]+10} L -10,{c["hem"]+10} L -12,{c["hem"]+34} L -30,{c["hem"]+32} Z M 30,{c["hem"]+10} L 10,{c["hem"]+10} L 12,{c["hem"]+34} L 30,{c["hem"]+32} Z" fill="{b[2]}" opacity=".7"/>')
        sl = (c['tc'][1], c['tc'][2], 66 if c['top'] in ('tee', 'uniform') else 178)
        o.append(arms_front(c, sl) + torso_front(c, back=True))
        o.append(f'<path d="M 0,{c["sh"]+20} L 0,{c["hem"]-10}" stroke="{c["tc"][2]}" stroke-width="1.4" opacity=".5"/>')
        o.append(head_back(c))
    return ''.join(o)

# ---------------- side (facing viewer's left, full 90°) ----------------
def head_side(c):
    s, sh, lt = c['skin']; hc, hl = c['hair'], c['hair_lt']; st = c['style']
    fat = c.get('belly'); long_ = st == 'pomp'
    chin = 44 if long_ else (40 if not fat else 40)
    face = (f'M 6,-46 C -18,-46 -30,-32 -30,-12 L -30,-4 L -36,6 L -31,9 L -31,13 C -33,15 -32,18 -29,19 C -31,21 -30,24 -27,25 '
            f'C -27,31 -23,{chin-4} -12,{chin} L -2,{chin+2} C 8,{chin+1} 14,{chin-8} 16,{chin-16} L 24,8 C 32,-6 30,-34 6,-46 Z')
    if fat:
        face = ('M 6,-46 C -22,-46 -36,-32 -36,-12 L -36,-2 L -42,8 L -36,11 L -36,15 C -38,17 -37,20 -34,21 C -36,24 -34,28 -30,30 '
                'C -28,38 -18,44 -4,44 L 6,44 C 16,42 22,32 24,22 L 28,6 C 34,-8 32,-34 6,-46 Z')
    o = [f'<path d="M -6,22 L 12,20 L 16,60 L -4,60 Z" fill="{sh}"/>', f'<path d="{face}" fill="{s}"/>',
         f'<path d="M 24,8 C 32,-6 30,-34 6,-46 C 18,-36 22,-20 20,0 C 18,14 14,24 6,32 C 12,30 16,24 18,18 Z" fill="{sh}" opacity=".6"/>',
         f'<ellipse cx="9" cy="0" rx="5.4" ry="8.4" fill="{s}"/><path d="M 9,-5 C 6,-2 6,3 9,6" fill="none" stroke="{sh}" stroke-width="1.4"/>']
    ex = -22 if not fat else -26
    if st == 'buzz':   # happy squint
        o.append(f'<path d="M {ex-5},-2 Q {ex-1},-7 {ex+4},-2" fill="none" stroke="#1d1416" stroke-width="2.4" stroke-linecap="round"/>')
    else:
        o.append(f'<path d="M {ex-5},-2 C {ex-3},-5 {ex+2},-5 {ex+5},-1.4 C {ex+2},0.6 {ex-2},0.8 {ex-5},-2 Z" fill="#fbf4ee"/>'
                 f'<circle cx="{ex-1.4}" cy="-2" r="2.4" fill="#2a1a16"/><circle cx="{ex-2}" cy="-2.8" r=".7" fill="#fff"/>'
                 f'<path d="M {ex-6},-2.4 C {ex-3},-6 {ex+2},-6 {ex+6},-1.8" fill="none" stroke="#1d1416" stroke-width="1.8"/>')
        if st in ('bob', 'halfup'):
            o.append(f'<path d="M {ex-6},-2.6 L {ex-9},-5.4" stroke="#1d1416" stroke-width="1.4" stroke-linecap="round"/>')
        if st == 'pomp':
            o.append(f'<path d="M {ex-6},-4.6 C {ex-2},-5.4 {ex+3},-5 {ex+6},-3" fill="{s}"/>')
    o.append(f'<path d="M {ex-8},-12 C {ex-4},-15 {ex+3},-15 {ex+8},-12.6" fill="none" stroke="#221a1e" stroke-width="2.2" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="{ex+6}" cy="11" rx="5" ry="3" fill="#e48a7e" opacity=".35"/>')
    lip = '#9a5a50' if st in ('crop', 'slick', 'buzz', 'pomp') else '#b8606c'
    if st == 'buzz':
        o.append('<path d="M -40,16 Q -34,22 -28,18 L -36,17 Z" fill="#5a2a2c"/><path d="M -38,12 Q -33,11 -29,13" fill="none" stroke="#2a2224" stroke-width="2.4"/>')
    else:
        o.append(f'<path d="M -30,{16 if not long_ else 18} L -26,{17 if not long_ else 19}" stroke="{lip}" stroke-width="1.8" stroke-linecap="round"/>')
    if st == 'pomp':
        o.append('<path d="M -26,19 L -36,15" stroke="#e8d2a0" stroke-width="1.4" stroke-linecap="round"/><path d="M -16,{0} L -10,{0}" stroke="none"/>'.replace('{0}', '46'))
        o.append('<path d="M -14,44 L -10,49 L -6,45 Z" fill="#241c1e"/>')
    if st == 'crop':
        o.append('<path d="M -24,26 C -20,34 -12,40 -2,42 C 8,41 14,33 16,24 L 10,26 C 6,32 0,35 -6,35 C -14,34 -20,30 -24,26 Z" fill="#5b4a48" opacity=".22"/>')
    if c.get('glasses'):
        o.append(f'<path d="M {ex-6},-6 L {ex+6},-6.6 L {ex+5},3 C {ex+2},5 {ex-4},5 {ex-6},2 Z" fill="#ffffff" fill-opacity=".08" stroke="#2c1a24" stroke-width="1.3"/>'
                 f'<path d="M {ex+6},-5.6 L 6,-4" stroke="#2c1a24" stroke-width="1.3"/><path d="M {ex+6},-6.6 L {ex+8},-9 L {ex+4},-8.6 Z" fill="#2c1a24"/>')
    # hair
    if st == 'crop':
        o.append(f'<path d="M -30,-14 C -32,-42 -14,-62 8,-61 C 28,-60 36,-40 30,-6 L 26,10 L 18,12 L 18,-8 C 10,-18 -2,-22 -14,-22 L -28,-18 Z" fill="{hc}"/>'
                 f'<path d="M 14,-14 L 20,-14 L 18,-2 L 15,-2 Z" fill="#3a3034"/><path d="M -16,-50 C -4,-58 14,-58 24,-48 C 10,-52 -2,-50 -12,-44 Z" fill="{hl}"/>')
    elif st == 'buzz':
        o.append(f'<path d="M -34,-18 C -34,-46 -14,-56 8,-56 C 26,-56 34,-42 32,-14 L 26,-20 C 12,-28 -16,-30 -30,-24 Z" fill="{hc}"/>')
    elif st == 'pomp':
        o.append(f'<path d="M -30,-16 C -40,-46 -20,-68 4,-66 C 26,-64 36,-44 30,-8 L 30,30 L 20,26 L 18,-8 C 8,-24 -8,-28 -22,-26 Z" fill="{hc}"/><path d="M -30,-40 C -20,-60 4,-66 22,-56 C 6,-58 -10,-54 -24,-36 Z" fill="{hl}"/>'
                 '<ellipse cx="-12" cy="-52" rx="11" ry="6" fill="#2e3e50" stroke="#c8b07a" stroke-width="1.2"/><path d="M -1,-52 L 10,-46" stroke="#c8b07a" stroke-width="1.2"/>')
    elif st == 'slick':
        o.append(f'<path d="M -30,-12 C -34,-42 -16,-62 6,-61 C 28,-60 36,-40 31,-6 C 29,8 24,16 18,18 L 18,-6 C 10,-20 -6,-26 -20,-26 L -28,-22 Z" fill="{hc}"/>'
                 + ''.join(f'<path d="M -24,{y} C -6,{y-6} 14,{y-2} 28,{y+12}" fill="none" stroke="{hl}" stroke-width="1.4"/>' for y in (-50, -40, -30)))
    elif st == 'bob':
        o.append(f'<path d="M -34,-16 C -36,-46 -14,-64 8,-63 C 32,-62 44,-42 42,-6 L 44,32 C 38,40 28,40 22,36 L 16,10 C 14,-2 6,-10 -4,-14 L -34,-14 Z" fill="{hc}"/>'
                 f'<path d="M -34,-18 L -32,-12 L -18,-13 L -16,-18 Z" fill="{hc}"/><path d="M -20,-48 C -6,-60 16,-60 32,-48 C 14,-52 -2,-50 -14,-42 Z" fill="{hl}"/>'
                 f'<circle cx="8" cy="12" r="3.2" fill="none" stroke="#d8b46a" stroke-width="1.3"/>')
    elif st == 'halfup':
        o.append(f'<path d="M -30,-14 C -34,-44 -14,-63 8,-62 C 30,-61 40,-42 36,-6 L 44,118 C 36,124 28,124 22,118 L 18,8 C 14,-6 4,-14 -8,-18 L -28,-18 Z" fill="{hc}"/>'
                 f'<ellipse cx="24" cy="-22" rx="5" ry="7" fill="#7d9a88"/><path d="M -16,-50 C -2,-58 16,-58 28,-48 C 12,-52 -2,-50 -12,-44 Z" fill="{hl}"/>')
    return ''.join(o)

def side_view(k, near_detail=False):
    """facing the viewer's left. near_detail=True draws the leg/cast & chest badge for the opposite side (used for the right view, then mirrored)"""
    c = C[k]; m, lt, dk = c['tc']; s, sh, _ = c['skin']; y = c['sh']; hem = c['hem']; foot = c['foot']
    o = []
    if c.get('crutch'):
        o.append(f'<rect x="10" y="{y+84}" width="4.6" height="{foot-y-70}" fill="#7d8391"/><rect x="6" y="{y+76}" width="13" height="10" rx="4" fill="#3a3d49"/>')
    # legs (back then front)
    if c['top'] in ('dress', 'dress2'):
        o.append(f'<rect x="-2" y="{hem-6}" width="12" height="{foot-hem+8}" fill="{sh}"/><rect x="-12" y="{hem-6}" width="13" height="{foot-hem+8}" fill="{s}"/>')
        o.append(f'<path d="M -26,{foot+2} L 2,{foot} L 4,{foot+13} L -30,{foot+13} C -32,{foot+9} -30,{foot+4} -26,{foot+2} Z" fill="{c["shoe"]}"/>')
    else:
        b, bl, bd = c['bot']; lw = 34 if not c.get('belly') else 40
        o.append(f'<path d="M -10,{hem-6} L {lw-12},{hem-6} L {lw-14},{foot} L 0,{foot} Z" fill="{bd}"/>')
        o.append(f'<path d="M -{lw-14},{hem-6} L 10,{hem-6} L 6,{foot} L -14,{foot} Z" fill="{b}"/><path d="M -{lw-14},{hem-6} L -10,{hem-6} L -14,{foot} L -16,{foot} Z" fill="{bl}"/>')
        cast_back = c.get('cast') and not near_detail; cast_near = c.get('cast') and near_detail
        if cast_back:
            o.append(f'<path d="M -2,{hem+134} L {lw-12},{hem+134} L {lw-14},{foot+10} C {lw-14},{foot+18} {lw-18},{foot+22} {lw-24},{foot+22} L -8,{foot+22} C -10,{foot+16} -6,{foot+10} -2,{foot+8} Z" fill="#c8c4be"/>')
        o.append(f'<path d="M -22,{foot} L 6,{foot} L 8,{foot+16} L -28,{foot+16} C -30,{foot+10} -28,{foot+4} -22,{foot} Z" fill="{c["shoe"]}"/>' if not cast_near else
                 f'<path d="M -16,{hem+134} L 8,{hem+134} L 6,{foot+10} C 6,{foot+18} 2,{foot+22} -4,{foot+22} L -30,{foot+22} C -34,{foot+16} -28,{foot+10} -18,{foot+8} Z" fill="#e8e5e0"/><path d="M -14,{hem+174} L 7,{hem+174}" stroke="#cfcbc5" stroke-width="1.2"/>')
        if cast_near:
            o.append(f'<path d="M 4,{foot} L 26,{foot} L 28,{foot+16} L -2,{foot+16} Z" fill="{c["shoe"]}" opacity=".85"/>')
    # torso
    if c['top'] in ('dress', 'dress2'):
        if c['top'] == 'dress':
            o.append(f'<path d="M -10,{y} C -18,{y+8} -20,{y+20} -18,{y+40} L 14,{y+40} C 16,{y+20} 14,{y+8} 8,{y} Z" fill="{s}"/>')
            o.append(f'<path d="M -20,{y+34} C -26,{y+50} -22,{y+70} -16,{y+96} C -22,{y+130} -24,{y+180} -28,{hem} L 26,{hem} C 24,{y+200} 22,{y+130} 18,{y+100} C 20,{y+70} 18,{y+44} 14,{y+34} Z" fill="{m}"/>'
                     f'<path d="M -20,{y+34} C -26,{y+50} -22,{y+70} -16,{y+96} C -22,{y+130} -24,{y+180} -28,{hem} L -14,{hem} C -12,{y+180} -8,{y+120} -6,{y+96} C -10,{y+70} -10,{y+50} -8,{y+36} Z" fill="{lt}"/>'
                     f'<path d="M -4,{y+36} L -6,{y+4}" stroke="#b35d72" stroke-width="2"/>')
        else:
            o.append(f'<path d="M -12,{y} C -24,{y+10} -26,{y+40} -24,{y+100} C -40,{y+190} -48,{y+280} -52,{hem} L 40,{hem} C 38,{y+280} 32,{y+190} 22,{y+100} C 24,{y+40} 18,{y+8} 10,{y} Z" fill="{m}"/>'
                     f'<path d="M -12,{y} C -24,{y+10} -26,{y+40} -24,{y+100} C -40,{y+190} -48,{y+280} -52,{hem} L -30,{hem} C -24,{y+260} -14,{y+180} -10,{y+100} C -12,{y+50} -8,{y+10} -2,{y} Z" fill="{lt}"/>'
                     f'<path d="M -24,{y+100} L 22,{y+100} L 22,{y+108} L -24,{y+108} Z" fill="#5a7262"/>')
    else:
        if c.get('belly'):
            o.append(f'<path d="M -14,{y} C -30,{y+12} -36,{y+40} -40,{y+80} C -58,{y+110} -60,{y+160} -46,{y+190} L 26,{y+194} C 30,{y+150} 30,{y+80} 28,{y+40} C 26,{y+16} 20,{y+4} 10,{y} Z" fill="{m}"/>'
                     f'<path d="M -14,{y} C -30,{y+12} -36,{y+40} -40,{y+80} C -58,{y+110} -60,{y+160} -46,{y+190} L -30,{y+192} C -40,{y+150} -36,{y+100} -26,{y+70} C -24,{y+40} -20,{y+14} -6,{y} Z" fill="{lt}"/>')
            bl_y = y + 186
        else:
            o.append(f'<path d="M -12,{y} C -28,{y+10} -31,{y+40} -29,{y+80} L -26,{hem} L 25,{hem} L 28,{y+80} C 30,{y+40} 22,{y+8} 10,{y} Z" fill="{m}"/>'
                     f'<path d="M -12,{y} C -28,{y+10} -31,{y+40} -29,{y+80} L -26,{hem} L -12,{hem} C -14,{y+120} -14,{y+40} -4,{y} Z" fill="{lt}"/>')
            bl_y = hem - 8
        if c['top'] == 'uniform':
            o.append(f'<rect x="{-46 if c.get("belly") else -27}" y="{bl_y}" width="{72 if c.get("belly") else 53}" height="10" fill="#17161c"/>')
            o.append(f'<path d="M -6,{y+4} L 12,{y+2} L 12,{y+8} L -6,{y+10} Z" fill="#1f2433"/>')
            if not near_detail:
                o.append(f'<path d="{"M -34" if c.get("belly") else "M -22"},{y+46} l 10,0 l 0,20 l -10,0 Z" fill="{lt}"/>')
            else:
                o.append(f'<path d="M {-30 if c.get("belly") else -20},{y+24} l 7,2 l -1,8 c -1,4 -3,5 -5,6 c -2,-1 -4,-2 -5,-6 l 0,-8 Z" fill="#c4c9d4"/>')
        elif c['top'] == 'long':
            o.append(f'<rect x="-27" y="{hem-8}" width="53" height="9" fill="#1f1d24"/>')
        o.append(f'<path d="M -10,{y} L -6,{y+12} L 8,{y+12} L 10,{y} Z" fill="{dk}" opacity=".6"/>' if c['top'] != 'tee' else f'<path d="M -10,{y} C -8,{y+6} 4,{y+6} 8,{y}" fill="none" stroke="{dk}" stroke-width="3"/>')
    # near arm hanging at the side
    hand = hem - 14 if c['top'] not in ('dress', 'dress2') else 226
    slen = {'tee': 66, 'uniform': 66, 'long': 178}.get(c['top'], 0)
    o.append(f'<path d="M -8,{y+16} L 10,{y+14} L 8,{hand} L -6,{hand} Z" fill="{s}"/><path d="M 4,{y+16} L 10,{y+14} L 8,{hand} L 4,{hand} Z" fill="{sh}"/>')
    o.append(f'<path d="M -7,{hand-2} L 8,{hand-2} C 9,{hand+12} 6,{hand+22} 0,{hand+24} C -6,{hand+22} -9,{hand+12} -7,{hand-2} Z" fill="{s}"/>')
    if slen:
        o.append(f'<path d="M -10,{y+12} L 12,{y+10} L 10,{y+slen} L -8,{y+slen+2} Z" fill="{lt}"/><path d="M 4,{y+12} L 12,{y+10} L 10,{y+slen} L 4,{y+slen} Z" fill="{dk}"/>')
    if c['top'] == 'dress2':
        o.append(f'<path d="M -14,{y+10} C -18,{y+30} -10,{y+50} 4,{y+52} C 16,{y+50} 18,{y+30} 12,{y+10} Z" fill="{lt}"/>')
    if c.get('crutch'):
        o.append(f'<rect x="-14" y="{y+84}" width="4.6" height="{foot-y-70}" fill="#a3a9b6"/><rect x="-18" y="{y+76}" width="13" height="10" rx="4" fill="#4a4e5c"/><rect x="-14" y="{hand+4}" width="18" height="6" rx="2" fill="#2c2f3a"/>')
    o.append(head_side(c))
    return ''.join(o)

# ---------------- page ----------------
def panel(inner, k, label):
    c = C[k]
    return (f'<figure><svg viewBox="0 0 400 900" role="img" aria-label="{c["name"]} {label}"><rect width="400" height="900" fill="url(#skyBg)"/>'
            f'<rect y="770" width="400" height="130" fill="#ede5ea"/><ellipse cx="200" cy="{c["ty"] + (c["foot"]+16)*c["sc"]:.0f}" rx="76" ry="9" fill="#cfc2d2"/>'
            f'<g transform="translate(200,{c["ty"]}) scale({c["sc"]})">{inner}</g></svg><figcaption>{label}</figcaption></figure>')

rows = []
for k in ('hero', 'heroine', 'moo', 'ton', 'husband', 'wife'):
    c = C[k]
    views = [panel(front_view(k), k, 'หน้า'),
             panel(side_view(k), k, 'ซ้าย (หันไปทางซ้ายของจอ)'),
             panel(back_view(k), k, 'หลัง'),
             panel(f'<g transform="scale(-1,1)">{side_view(k, near_detail=True)}</g>', k, 'ขวา (หันไปทางขวาของจอ)')]
    rows.append(f'<section><h2>{c["name"]}<span>{c["note"]}</span></h2><div class="four">{"".join(views)}</div></section>')

page = f'''<title>บ้านตรงข้าม มุมหมุนรอบตัว</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: one row of four views per character (front, left, back, right); 2 per row on phones. Same look as the character sheets. */
:root {{ --stage:#f5f0f3; --ink:#3b3346; --muted:#847a90; --line:#e2d9e3; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:light; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1100px; margin:0 auto; display:grid; gap:30px; }}
h1 {{ font-size:20px; font-weight:500; margin:0; }} header p {{ margin:6px 0 0; color:var(--muted); font-size:13px; line-height:1.6; }}
h2 {{ font-size:18px; font-weight:500; margin:0 0 10px; }} h2 span {{ color:var(--muted); font-weight:400; margin-left:8px; font-size:14px; }}
.four {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; }}
@media (max-width:640px) {{ .four {{ grid-template-columns:repeat(2,1fr); }} }}
figure {{ margin:0; display:grid; gap:6px; min-width:0; }}
figure svg {{ display:block; width:100%; height:auto; border-radius:6px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ font-size:12px; color:var(--muted); text-align:center; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<linearGradient id="skyBg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ab9cd8"/><stop offset=".6" stop-color="#cdb6dd"/><stop offset="1" stop-color="#e6cfe2"/></linearGradient>
{HEAD_DEFS}</defs></svg>
<div class="wrap"><header><h1>บ้านตรงข้าม · มุมหมุนรอบตัว</h1>
<p>หน้า · ซ้าย · หลัง · ขวา ในท่ายืนตรงเป็นกลาง ใช้เป็นแบบอ้างอิงตอนจัดท่าในฉาก · มุมข้างหันเต็ม 90 องศาตามมาตรฐานช่อง · หน้าตรงใช้หัวจากแผ่นที่ผ่านแล้ว รายละเอียดที่อยู่ข้างเดียว เช่น เฝือกและตราโล่ วางตามด้านที่ถูกต้องในแต่ละมุม</p></header>
{"".join(rows)}</div>'''
open('turnaround.html', 'w', encoding='utf-8').write(page)
print('ok')
