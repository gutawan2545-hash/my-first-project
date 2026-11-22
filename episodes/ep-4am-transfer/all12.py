import runpy
A = runpy.run_path('all8.py')          # rebuilds storyboard2 and exposes every piece
G = A['G']; S = A['S']
FONT = G['FONT']; phone = G['phone']; dust = A['dust']; hall = A['hall']
tag = A['tag']; callout = A['callout']; digits = A['digits']; wlen = A['wlen']
VIG = A['VIG']; TEX = A['TEX']; bg = A['bg']; room_top = A['room_top']
INFO = A['INFO']; SUBS = A['SUBS']; old = A['old']; FT = A['FT']


def rep(s, o, n):
    assert o in s, o[:80]
    return s.replace(o, n, 1)


BRIGHT = '<filter id="bright" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1.10 0 0 0 0.05  0 1.06 0 0 0.04  0 0 1.04 0 0.04  0 0 0 1 0"/></filter>'

# ---------- shot 4: brighten the person, no spotlight ----------
s4 = A['s4']
s4 = rep(s4, '<circle cx="290" cy="270" r="130" fill="#ffe9dc" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/><circle cx="290" cy="250" r="80" fill="#fff2ea" opacity=".18" filter="url(#haze)" style="mix-blend-mode:screen"/>', '')
s4 = rep(s4, '<g filter="url(#tintWarm)"><use href="#tbody" transform="translate(270,250) scale(1.9)"/></g>', '<g filter="url(#bright)"><use href="#tbody" transform="translate(270,250) scale(1.9)"/></g>')
s4 = rep(s4, '<g filter="url(#tintWarm)"><ellipse cx="172" cy="520"', '<g filter="url(#bright)"><ellipse cx="172" cy="520"')

# ---------- shot 5: believable hand ----------
s5 = A['s5f']
SK, SKM, SKD, NAIL = '#d8a493', '#c08a7c', '#a8746a', '#f0cfc4'
fingers = ''.join(
    f'<g transform="translate(176,{y}) rotate({r})"><rect x="-34" y="-15" width="46" height="30" rx="15" fill="{SKM}"/>'
    f'<rect x="-34" y="-15" width="20" height="30" rx="10" fill="{SK}"/><path d="M -12,-13 L -12,13" stroke="{SKD}" stroke-width="1.4" opacity=".6"/></g>'
    for y, r in [(292, -6), (336, -2), (380, 2), (422, 6)])
palm = (f'<g><path d="M290,960 L440,960 L410,640 L300,628 Z" fill="{SKM}"/><path d="M400,960 L440,960 L410,640 L392,640 Z" fill="{SKD}"/>'
        f'<path d="M232,500 C222,580 252,650 330,660 C396,664 420,610 414,520 Z" fill="{SKM}"/>'
        f'<path d="M232,500 C226,560 244,610 290,640 C262,600 252,556 254,500 Z" fill="{SK}"/></g>')
thumb = (f'<g><path d="M410,600 C400,556 344,506 300,482 C286,474 270,482 276,496 C292,520 344,566 362,618 Z" fill="{SK}"/>'
         f'<path d="M410,600 C402,572 380,548 352,528 C368,556 380,588 386,614 Z" fill="{SKM}"/>'
         f'<path d="M332,508 C326,520 324,530 330,540" stroke="{SKD}" stroke-width="1.6" fill="none" opacity=".6"/>'
         f'<ellipse cx="288" cy="487" rx="9" ry="6.5" transform="rotate(32 288 487)" fill="{NAIL}"/>'
         f'<ellipse cx="286" cy="485" rx="4" ry="2.4" transform="rotate(32 286 485)" fill="#ffffff" opacity=".45"/></g>')
s5 = rep(s5, '<g><path d="M300,960 L420,960 L360,600 L300,590 Z" fill="#c99486"/><path d="M380,960 L420,960 L360,600 L350,600 Z" fill="#a87a74"/><ellipse cx="330" cy="540" rx="60" ry="62" fill="#c99486"/></g>', palm + fingers)
s5 = rep(s5, '<g><path d="M200,620 C214,570 240,510 258,478 C264,470 274,474 272,484 C262,516 248,572 236,620 Z" fill="#e2b2a0"/><ellipse cx="372" cy="300" rx="11" ry="18" fill="#c99486"/><ellipse cx="374" cy="348" rx="11" ry="17" fill="#c99486"/><ellipse cx="372" cy="394" rx="10" ry="15" fill="#b88478"/></g>', thumb)

# ---------- shot 6: smaller cat ----------
s6 = rep(A['s6'], '<use href="#catSideAlert" transform="translate(150,452) scale(1.05)"/>', '<use href="#catSideAlert" transform="translate(190,488) scale(0.68)"/>')
s6 = rep(s6, "<g fill=\"#fff6ec\"><g filter=\"url(#moteBlur)\">", "<g fill=\"#fff6ec\"><g filter=\"url(#moteBlur)\">")

# ---------- new shot A: nights 3-9 stacked on the lock screen ----------
s1 = S['s1']
a = s1.index('<g font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"><text x="0" y="-92"')
b = s1.index('</g>', a) + 4
rows = ''
for i, st in enumerate(['12', '58', '33', '70', '06', '91', '25']):
    y = -118 + i * 36
    rows += (f'<rect x="-64" y="{y}" width="128" height="30" rx="8" fill="#eef0f8" fill-opacity="{0.94 - i*0.06:.2f}"/>'
             f'<text x="-56" y="{y+13}" font-size="7.5" fill="#4a5070">ธนาคาร · 04:00 · คืน {i+3}</text>'
             f'<text x="-56" y="{y+25}" font-size="10" font-weight="500" fill="#14172b">เงินเข้า +333.{st} บาท</text>')
sA = s1[:a] + f'<g {FONT}>' + rows + '</g>' + s1[b:]
sA = sA.replace('<text x="-40" y="-22" font-size="18" fill="#7a4a20">333.07</text><text x="-40" y="4" font-size="18" fill="#7a4a20">333.41 ?</text>',
                '<text x="-40" y="-22" font-size="18" fill="#7a4a20">ตีสี่ตรง</text><text x="-40" y="4" font-size="18" fill="#7a4a20">ทุกคืน!</text>')

# ---------- new shot B: the cat waits at the storage door every night ----------
sB = hall(560, (330, 170, 490, 560))
sB += '<rect x="0" y="140" width="150" height="420" fill="#2e2228"/><rect x="0" y="152" width="136" height="408" fill="#6a5560"/><rect x="0" y="152" width="136" height="408" fill="#fff0e4" opacity=".45"/>'
sB += '<path d="M136,300 L200,300 L460,960 L0,960 L0,560 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
sB += '<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(76,236) scale(0.65)"/></g>'
sB += '<rect x="136" y="140" width="14" height="420" fill="#2e2228"/><rect x="0" y="140" width="150" height="12" fill="#2e2228"/>'
sB += '<use href="#catSide" transform="translate(270,508) scale(0.5)"/><rect x="330" y="552" width="160" height="8" fill="#08060c"/>'
sB += dust(81, (40, 300, 260, 620), 16) + VIG + TEX

# ---------- new shot C: James tries to stop her ----------
armT = '<path d="M 50,64 C 58,72 62,92 62,110 L 46,114 L 40,74 Z" fill="#f3e6cf"/><path d="M 60,106 L 46,112 L 26,10 L 40,4 Z" fill="#e8b08a"/><ellipse cx="32" cy="2" rx="9" ry="10" fill="#e8b08a"/><rect x="18" y="-26" width="12" height="34" rx="3" fill="#0c0d14"/>'
armJ = '<path d="M 50,64 C 60,70 70,84 78,96 L 66,108 L 44,80 Z" fill="#2b3768"/><path d="M 76,94 L 64,108 L 120,128 L 126,112 Z" fill="#fbe7d8"/><ellipse cx="128" cy="120" rx="11" ry="9" fill="#fbe7d8"/>'
sC = room_top + bg + '<g filter="url(#bright)"><g transform="translate(150,330) scale(1.5)"><use href="#jbodyS"/>' + armJ + '</g>'
sC += '<g transform="translate(395,345) scale(1.5)"><use href="#tbody"/>' + armT + '</g></g>'
sC += '<g filter="url(#dof)"><path d="M-20,740 C120,700 300,760 560,710 L560,960 L-20,960 Z" fill="#21152a"/><path d="M-20,740 C120,700 300,760 560,710 L560,750 C300,780 120,740 -20,780 Z" fill="#3a2634"/></g>'
sC += dust(91, (300, 180, 520, 460), 14) + VIG + TEX

# ---------- new shot D: the ringtone of the phone he lost ----------
notes = ''.join(f'<g transform="translate({x},{y}) rotate({r})" fill="#e2ecff" opacity="{o}"><ellipse cx="0" cy="18" rx="8" ry="6"/><rect x="6" y="-14" width="3" height="32"/><path d="M9,-14 q14,4 12,16" stroke="#e2ecff" stroke-width="3" fill="none"/></g>'
                for x, y, r, o in [(440, 300, 10, .9), (480, 400, -8, .7), (400, 470, 14, .6), (500, 220, -12, .5)])
sD = '<rect width="540" height="960" fill="url(#hallWall)"/><rect x="420" y="0" width="140" height="960" fill="#3a2c32"/><rect x="414" y="0" width="8" height="960" fill="#e2ecff" opacity=".5" filter="url(#bokeh)"/>'
sD += '<circle cx="470" cy="380" r="200" fill="#9fb4ff" opacity=".16" filter="url(#haze)" style="mix-blend-mode:screen"/>'
sD += '<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(230,300) scale(2.3)"/></g>' + notes
sD += dust(101, (360, 160, 540, 560), 14, '#eef4ff') + VIG + TEX

# ---------- order, subtitles, graphics ----------
NEW = {
    'A': ('คืนที่สามถึงเก้า · ตีสี่ตรงทุกคืน', 'หลังจากนั้นเงินก็เข้าทุกคืน ตอนตีสี่ตรง ไม่เคยช้าแม้แต่นาทีเดียว',
          ['หลังจากนั้นเงินก็เข้าทุกคืน', 'ตอนตีสี่ตรง', 'ไม่เคยช้าแม้แต่นาทีเดียว'],
          'มุมบนลงโต๊ะเหมือนช็อต 1 หน้าจอมือถือมีแจ้งเตือนซ้อนกันเจ็ดคืน ทุกอันเวลา 04:00 โน้ตเขียนว่า "ตีสี่ตรง ทุกคืน!"', sA,
          tag(20, 20, 'คืนที่ 3–9') + callout(330, 420, '04:00 ทุกครั้ง', 318, 330, 'ยอดต่างกันแค่สตางค์', 180)),
    'B': ('แมวเริ่มรอหน้าห้องเก็บของ', 'ช่วงเดียวกันนั้น แมวส้มของผมเริ่มตื่นมานั่งเฝ้าหน้าห้องเก็บของทุกคืนตอนตีสี่',
          ['ช่วงเดียวกันนั้น แมวส้มของผม', 'เริ่มตื่นมานั่งเฝ้าหน้าห้องเก็บของ', 'ทุกคืนตอนตีสี่'],
          'ทางเดินมืด แมวตัวเล็กยืนนิ่งหันไปทางห้องเก็บของ เจมส์ยืนเต็มตัวอยู่ที่ประตูห้องนอน แอบมองแมวด้วยสีหน้ากังวล แสงจากห้องส่องออกมาด้านหลัง', sB,
          tag(20, 20, 'ทุกคืน · 04:00') + callout(320, 92, 'ห้องเก็บของ', 410, 170, None, 150)),
    'C': ('พยายามห้าม', 'ผมพยายามห้ามเธอ แต่เธอกดโทรออกไปแล้ว',
          ['ผมพยายามห้ามเธอ', 'แต่เธอกดโทรออกไปแล้ว'],
          'ในห้องนอน ความสว่างเท่าช็อต 6 เจมส์หน้าตกใจเอื้อมมือไปห้าม ตะวันยกมือถือแนบหูแล้ว ผ้าห่มเบลออยู่ฉากหน้า', sC,
          tag(20, 20, 'กำลังโทรออก…')),
    'D': ('เสียงเรียกเข้าที่คุ้นเคย', 'และเสียงเรียกเข้านั้น เป็นเพลงเดียวกับมือถือเครื่องเก่าของผม ที่หายไปตั้งแต่ปีก่อน',
          ['และเสียงเรียกเข้านั้น', 'เป็นเพลงเดียวกับมือถือเครื่องเก่าของผม', 'ที่หายไปตั้งแต่ปีก่อน'],
          'ภาพครึ่งตัวเจมส์หน้าตกใจในทางเดินมืด มีโน้ตเพลงลอยออกมาจากขอบประตูทางขวา แสงจอสีขาวอมฟ้าลอดออกมา', sD,
          callout(30, 120, 'เพลงเรียกเข้าเครื่องเก่า', 420, 300, 'เครื่องที่หายไปเมื่อปีก่อน', 270)),
}
# old entries: (title, line, subs, note, svg, info)
notes8 = A['notes']
svgs8 = [A['s1'], A['s2'], A['s3'], s4, s5, s6, A['s7'], A['s8']]
OLD = [(old[i][0], old[i][1], SUBS[i], notes8[i], svgs8[i], INFO[i]) for i in range(8)]
OLD[3] = OLD[3][:3] + ('ตะวันชูโน้ตวงเลขหลักสุดท้ายสีแดง ตัวแรกเป็นศูนย์ ตัวตะวันสว่างชัด โต๊ะเป็นโทนมืด โคมทางขวามีฝุ่นในลำแสง',) + OLD[3][4:]
OLD[4] = OLD[4][:3] + ('โคลสอัปมือตะวันกดโทร นิ้วจับขอบมือถือ นิ้วโป้งกดปุ่มโทร เบอร์ถูกปิดบางส่วน พื้นหลังเป็นผ้าห่มเบลอ',) + OLD[4][4:]
OLD[5] = OLD[5][:3] + ('มุมต่ำในทางเดินมืด แมวตัวเล็กลงยืนในลำแสงจากห้องนอน ตาเบิก จ้องประตูห้องเก็บของ',) + OLD[5][4:]
ORDER = [OLD[0], OLD[1], OLD[2], NEW['A'], NEW['B'], OLD[3], OLD[4], NEW['C'], OLD[5], OLD[6], NEW['D'], OLD[7]]


EN = [
    ['If someone sent money to your account', 'at 4 a.m. every night,', 'would you still think it was a mistake?'],
    ['The first night, I thought it was a typo.', 'It was only 333 baht and a few satang.'],
    ['I reported it, but the next night it came again', 'at 4 a.m. sharp. Only the satang changed.'],
    ['After that, the money came every night', 'at exactly 4 a.m., never a minute late.'],
    ['Around then, my orange cat started waiting', 'by the storage room every night at 4 a.m.'],
    ['After ten nights, my girlfriend lined up', 'the last digit of each amount.', 'It started with a zero.'],
    ['Thai mobile numbers have exactly ten digits,', 'so she tried calling it.'],
    ['I tried to stop her,', 'but she had already pressed call.'],
    ['Before we even heard it ring, my cat got up', 'and stared at the storage room door.'],
    ['Then a phone rang inside that room,', 'while we both stood at the door', 'holding our own phones.'],
    ['And that ringtone was the same song', 'as my old phone, the one I lost last year.'],
    ['If you were me, would you open the door,', 'or get my girlfriend and the cat out first?', 'Tell me in the comments.'],
]


def sub(ls, en):
    n = len(ls); m = len(en); big = max(wlen(l) for l in ls)
    fs = 21 if n <= 3 and big <= 27 else (20 if n <= 3 else 19)
    lh = fs + 8; efs = 13; elh = 17; gap = 7
    total = n * lh + gap + m * elh
    top = 712 - total / 2
    th = ''.join(f'<text x="270" y="{top + fs + i*lh:.0f}">{l}</text>' for i, l in enumerate(ls))
    ey = top + n * lh + gap
    eh = ''.join(f'<text x="270" y="{ey + efs + i*elh:.0f}">{l}</text>' for i, l in enumerate(en))
    return (f'<g class="subs" {FT} text-anchor="middle" stroke="#0b0812" stroke-linejoin="round" paint-order="stroke">'
            f'<g font-weight="600" font-size="{fs}" fill="#ffd84a" stroke-width="7">{th}</g>'
            f'<g font-family="Inter, IBM Plex Sans Thai, sans-serif" font-weight="500" font-size="{efs}" fill="#ffffff" stroke-width="4.5">{eh}</g></g>')


cards = ''
for i, (t, line, ls, note, svg, info) in enumerate(ORDER, 1):
    cards += (f'<figure><svg viewBox="0 0 540 960" role="img" aria-label="ช็อต {i}: {t}">{svg}<g class="info">{info}</g>{sub(ls, EN[i-1])}'
              f'<g class="guide"><rect x="24" y="620" width="492" height="186" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/></g></svg>'
              f'<figcaption><span class="n">ช็อต {i}</span><b>{t}</b><q>{line}</q><small>{note}</small></figcaption></figure>\n')

page = open('storyboard2.html').read()
start = page.index('<div class="grid">') + len('<div class="grid">')
end = page.index('</div></div>\n<script>')
page = page[:start] + cards + page[end:]
page = page.replace('Odd Hours · ร่างที่ 3 · ภาพนิ่ง 8 ช็อต · ซับและกราฟิก · ยังไม่พากย์', 'Odd Hours · ร่างที่ 4 · ภาพนิ่ง 12 ช็อต · ซับและกราฟิก · ยังไม่พากย์')
page = page.replace('</defs></svg><div class="wrap"', BRIGHT + '</defs></svg><div class="wrap"', 1)
assert BRIGHT in page
page = page.replace('family=IBM+Plex+Sans+Thai:wght@400;500;600&', 'family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Inter:wght@500&', 1)
open('storyboard3.html', 'w').write(page)
open('script12.md', 'w').write('# ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน (ร่างบท 12 ช็อต)\n\n' + '\n'.join(f'{i}. {o[1]}' for i, o in enumerate(ORDER, 1)) + '\n')
print('built 12')
