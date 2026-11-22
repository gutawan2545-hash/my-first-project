import re,runpy,sys
S=runpy.run_path('style.py')          # builds styletest + gives helpers
G=runpy.run_path('build.py')          # characters, phone(), pad, arm
FONT=G['FONT']; phone=G['phone']; dust=S['dust']; shadow=S['shadow']
DEFS=S['DEFS']; extra=S['extra']; VIG=S['VIG']; TEX=S['TEX']
jd=G['jd']; td=G['td']; jbody=G['jbody']; tbody=G['tbody']
# ---- frightened faces ----
a=jd.index('  <g id="jhead">'); jh=jd[a:]
jh=jh.replace('id="jhead"','id="jheadScared"')
jh=jh.replace('<path d="M -22,-12.5 L -7,-12 L -7,-9.2 L -21,-9.4 Z" fill="#17151d"/>','<path d="M -22,-10 L -7,-14.6 L -7,-11.6 L -21,-7.2 Z" fill="#17151d"/>')
jh=jh.replace('<path d="M 22,-14.6 C 17,-16 11,-14.6 7,-12.6 L 7,-9.8 C 11,-11.6 17,-12.6 21,-11.4 Z" fill="#17151d"/>','<path d="M 22,-10 L 7,-14.6 L 7,-11.6 L 21,-7.2 Z" fill="#17151d"/>')
m0=jh.index('    <!-- mouth: lopsided smirk -->'); m1=jh.index('    <!-- hair',m0)
jh=jh[:m0]+'    <ellipse cx="0" cy="25" rx="4.2" ry="5" fill="#6b3a3a"/><ellipse cx="0" cy="27" rx="2.6" ry="2" fill="#b0605a"/>\n'+jh[m1:]
a=td.index('  <g id="thead">'); b=td.index('  </g>',td.index('<!-- straight front panels',a))+6; th=td[a:b]
th=th.replace('id="thead"','id="theadScared"')
th=th.replace('<path d="M -22,-13 C -17,-17 -10,-17 -5,-14"','<path d="M -22,-12 C -17,-13 -10,-15.5 -5,-17.5"').replace('<path d="M 5,-14 C 10,-17 17,-17 22,-13"','<path d="M 5,-17.5 C 10,-15.5 17,-13 22,-12"')
m0=th.index('    <!-- gentle smile -->'); m1=th.index('    <!--',m0+10)
th=th[:m0]+'    <ellipse cx="0" cy="24" rx="4" ry="5.2" fill="#7a3434"/><ellipse cx="0" cy="26.4" rx="2.4" ry="2" fill="#d27a74"/>\n'+th[m1:]
jbS=jbody.replace('<use href="#jhead"/>','<use href="#jheadScared"/>'); tbS=tbody.replace('<use href="#thead"/>','<use href="#theadScared"/>')
assert jbS!=jbody and tbS!=tbody
more='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'+jh+th+'<g id="jbodyS">'+jbS+'</g><g id="tbodyS">'+tbS+'''</g>
<linearGradient id="hallWall" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="540" y2="960"><stop offset="0" stop-color="#2a2236"/><stop offset="1" stop-color="#141020"/></linearGradient>
<linearGradient id="spill" gradientUnits="userSpaceOnUse" x1="0" y1="300" x2="420" y2="700"><stop offset="0" stop-color="#fff0e4" stop-opacity=".34"/><stop offset="1" stop-color="#fff0e4" stop-opacity="0"/></linearGradient>
<radialGradient id="coolPool" gradientUnits="userSpaceOnUse" cx="270" cy="760" r="240"><stop offset="0" stop-color="#e2ecff" stop-opacity=".5"/><stop offset="1" stop-color="#9fb4ff" stop-opacity="0"/></radialGradient>
<linearGradient id="crack" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#e2ecff" stop-opacity=".0"/><stop offset=".5" stop-color="#e2ecff" stop-opacity=".9"/><stop offset="1" stop-color="#e2ecff" stop-opacity="0"/></linearGradient>
<linearGradient id="duvet" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="540" y2="960"><stop offset="0" stop-color="#8a7a9e"/><stop offset="1" stop-color="#3a3050"/></linearGradient>
</defs></svg>'''
s1=S['s1']; s2=S['s2']
# bedroom background taken from shot 2
bg=s2[s2.index('<g filter="url(#dof)">'):s2.index('<g filter="url(#tintWarm)">')]
room_top='<rect width="540" height="960" fill="url(#room)"/>'
desk_end=s2[s2.index('<rect width="540" height="960" fill="url(#dark)"'):]
# ---- shot 3: same angle, James on the phone, new alert, wall clock ----
clock='<g filter="url(#dof)"><circle cx="182" cy="236" r="24" fill="#d9c9bc"/><circle cx="182" cy="236" r="20" fill="#2f2236"/><path d="M182,236 L182,220 M182,236 L196,244" stroke="#f0e4dc" stroke-width="3" stroke-linecap="round"/></g>'
bg3=bg.replace('<rect x="160" y="200" width="44" height="58" fill="#d9c9bc"/><rect x="165" y="205" width="34" height="48" fill="#a86a7a"/>','')
s3=room_top+bg3+clock+'<g filter="url(#tintWarm)"><g transform="translate(262,320) scale(1.7)"><use href="#jbody"/>'+G['arm']+'<rect x="-36" y="54" width="18" height="34" rx="3" fill="#0c0d14"/><rect x="-34" y="57" width="14" height="27" rx="2" fill="#3a4a8a"/></g></g>'+desk_end
s3=s3.replace('<rect x="-33" y="-65" width="66" height="130" rx="9" fill="#2c2f78"/>','<rect x="-33" y="-65" width="66" height="130" rx="9" fill="#1a1c3a"/>')
s3=s3.replace(VIG+TEX,'')+f'''<g {FONT}><rect x="20" y="70" width="230" height="66" rx="14" fill="#eef0f8" fill-opacity=".94"/>
<text x="36" y="93" font-size="11" fill="#4a5070">ธนาคาร · 04:00</text><text x="36" y="116" font-size="16" font-weight="500" fill="#14172b">เงินเข้า +333.41 บาท</text><text x="36" y="129" font-size="10" fill="#4a5070">อีกแล้ว</text></g>'''+VIG+TEX
# ---- shot 4: Tawan with the notepad under her lamp ----
lamp='''<g><path d="M470,690 L520,690 L512,682 L478,682 Z" fill="#2a1e30"/><path d="M494,684 L500,600 L470,560" stroke="#2a1e30" stroke-width="7" fill="none" stroke-linecap="round"/>
<path d="M446,548 L486,530 L500,566 L452,578 Z" fill="#4a3a52"/><path d="M452,578 L500,566 L496,574 L456,584 Z" fill="#fff2e4"/></g>
<path d="M452,580 L500,568 L300,700 L150,700 Z" fill="url(#monBeam)" opacity=".55" filter="url(#haze)" style="mix-blend-mode:screen"/>
<circle cx="476" cy="574" r="110" fill="#ffe6da" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/>'''
s4=room_top+bg+'<g filter="url(#tintWarm)"><use href="#tbody" transform="translate(270,250) scale(1.9)"/></g><rect width="540" height="960" fill="#ffeee4" opacity=".07" style="mix-blend-mode:screen"/>'
s4+='<circle cx="290" cy="270" r="130" fill="#ffe9dc" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/><circle cx="290" cy="250" r="80" fill="#fff2ea" opacity=".18" filter="url(#haze)" style="mix-blend-mode:screen"/><rect x="0" y="690" width="540" height="270" fill="#21152a"/><rect x="0" y="690" width="540" height="6" fill="#3a2634"/>'+lamp+G['pad']+'<g filter="url(#tintWarm)"><ellipse cx="172" cy="520" rx="14" ry="20" fill="#f8d2ab"/><ellipse cx="370" cy="500" rx="14" ry="20" fill="#e8b08a"/></g>'
s4+=dust(31,(330,200,520,560),18)+'<g transform="translate(120,820) rotate(-8)"><rect x="-70" y="-50" width="140" height="100" rx="6" fill="#efe2cc" opacity=".85"/><path d="M-50,-20 C-20,-40 10,0 40,-20 M-50,10 L30,10" stroke="#9b8670" stroke-width="2" fill="none"/></g><g transform="translate(400,830) rotate(20)"><rect x="-6" y="-60" width="12" height="120" rx="3" fill="#c0392b"/></g>'+VIG+TEX
# ---- shot 5: dialing over the duvet ----
folds=''.join(f'<path d="M-20,{y} C120,{y-40} 260,{y+30} 560,{y-20}" stroke="#2a2240" stroke-width="10" fill="none" opacity=".35"/>' for y in range(120,960,140))
s5f=f'''<rect width="540" height="960" fill="url(#duvet)"/><g filter="url(#dof2)">{folds}<rect x="300" y="-20" width="260" height="200" rx="40" fill="#d6cce2"/></g>
<circle cx="500" cy="60" r="200" fill="#ffe6da" opacity=".3" filter="url(#haze)" style="mix-blend-mode:screen"/>{dust(41,(330,10,540,260),16)}
<circle cx="270" cy="320" r="230" fill="#9fb0ff" opacity=".16" filter="url(#haze)" style="mix-blend-mode:screen"/>
<g><path d="M300,960 L420,960 L360,600 L300,590 Z" fill="#c99486"/><path d="M380,960 L420,960 L360,600 L350,600 Z" fill="#a87a74"/><ellipse cx="330" cy="540" rx="60" ry="62" fill="#c99486"/></g>'''
s5f+=phone(170,110,200,420,'''<text x="270" y="180" text-anchor="middle" font-size="12" fill="#9aa3c8">กำลังโทร…</text>
<circle cx="270" cy="236" r="34" fill="#2e3566"/><text x="270" y="249" text-anchor="middle" font-size="34" fill="#9aa3c8">?</text>
<text x="270" y="310" text-anchor="middle" font-size="22" font-weight="500" fill="#e8ecff" letter-spacing="1">094-71•-••••</text>
<text x="270" y="332" text-anchor="middle" font-size="11" fill="#9aa3c8">ไม่มีชื่อในรายชื่อติดต่อ</text>
<circle cx="270" cy="470" r="24" fill="#e0574a"/><path d="M258,472 Q270,462 282,472" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>''')
s5f+='<g><path d="M200,620 C214,570 240,510 258,478 C264,470 274,474 272,484 C262,516 248,572 236,620 Z" fill="#e2b2a0"/><ellipse cx="372" cy="300" rx="11" ry="18" fill="#c99486"/><ellipse cx="374" cy="348" rx="11" ry="17" fill="#c99486"/><ellipse cx="372" cy="394" rx="10" ry="15" fill="#b88478"/></g>'+VIG+TEX
# ---- hallway helper ----
def hall(floor,door):
    x0,y0,x1,y1=door
    pl=''.join(f'<line x1="{270+(x-270)*0.35:.0f}" y1="{floor}" x2="{x}" y2="960" stroke="#0e0a14" stroke-opacity=".5" stroke-width="1.5"/>' for x in range(-200,760,60))
    return f'''<rect width="540" height="960" fill="url(#hallWall)"/><rect y="{floor}" width="540" height="{960-floor}" fill="#231a26"/>{pl}<rect y="{floor-10}" width="540" height="10" fill="#120e18"/>
<rect x="{x0-12}" y="{y0-12}" width="{x1-x0+24}" height="{y1-y0+12}" fill="#2e2228"/><rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#3a2c32"/>
<rect x="{x0+16}" y="{y0+20}" width="{x1-x0-32}" height="{(y1-y0)*0.4:.0f}" fill="none" stroke="#2a1e24" stroke-width="3"/><rect x="{x0+16}" y="{y0+40+(y1-y0)*0.4:.0f}" width="{x1-x0-32}" height="{(y1-y0)*0.4:.0f}" fill="none" stroke="#2a1e24" stroke-width="3"/>
<circle cx="{x1-18}" cy="{(y0+y1)/2+20:.0f}" r="6" fill="#9a96a0"/>'''
# ---- shot 6: cat in the spill of light ----
s6=hall(560,(330,170,490,560))+'<path d="M0,300 L130,300 L420,960 L0,960 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
s6+='<use href="#catSideAlert" transform="translate(150,452) scale(1.05)"/><rect x="330" y="552" width="160" height="8" fill="#08060c"/>'+dust(51,(10,300,260,620),18)+VIG+TEX
# ---- shot 7: frightened, phone rings behind the door ----
s7=hall(760,(195,150,345,760))+'<rect x="195" y="752" width="150" height="8" fill="#e2ecff"/><rect width="540" height="960" fill="url(#coolPool)" style="mix-blend-mode:screen"/>'
s7+='<g fill="none" stroke="#e2ecff" stroke-width="3" stroke-linecap="round" opacity=".8"><path d="M300,420 q14,20 0,40"/><path d="M314,408 q22,32 0,64"/><path d="M240,420 q-14,20 0,40"/><path d="M226,408 q-22,32 0,64"/></g>'
s7+='<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(110,250) scale(1.25)"/><use href="#tbodyS" transform="translate(430,290) scale(1.25)"/></g>'
s7+='<rect x="42" y="554" width="16" height="28" rx="2" fill="#0c0d14"/><rect x="44" y="556" width="12" height="23" rx="1.5" fill="#9fb4ff"/><rect x="480" y="578" width="16" height="28" rx="2" fill="#0c0d14"/><rect x="482" y="580" width="12" height="23" rx="1.5" fill="#9fb4ff"/>'
s7+=dust(61,(150,620,400,770),16,'#eef4ff')+VIG+TEX
# ---- shot 8: door ajar ----
s8=f'''<rect width="540" height="960" fill="#16121e"/>
<rect x="170" y="0" width="370" height="960" fill="#3a2c32"/><rect x="210" y="60" width="290" height="360" fill="none" stroke="#2a1e24" stroke-width="4"/><rect x="210" y="480" width="290" height="380" fill="none" stroke="#2a1e24" stroke-width="4"/>
<rect x="150" y="0" width="20" height="960" fill="#050408"/><rect x="152" y="280" width="16" height="460" fill="url(#crack)" filter="url(#bokeh)"/><rect x="159" y="360" width="1.5" height="260" fill="#ffffff"/>
<path d="M150,300 L170,300 L60,760 L0,760 L0,640 Z" fill="#e2ecff" opacity=".12" filter="url(#haze)"/>
<circle cx="214" cy="470" r="14" fill="#9a96a0"/><circle cx="210" cy="466" r="5" fill="#d9d6e0"/>
<g filter="url(#tintNight)"><path d="M0,520 C60,500 130,480 180,470 L188,494 C140,510 70,540 0,560 Z" fill="#2b3768"/><path d="M0,520 C60,500 130,480 180,470" fill="none" stroke="#a9b8e8" stroke-width="3"/><ellipse cx="192" cy="482" rx="14" ry="11" fill="#fbe7d8"/></g>
<g filter="url(#tintNight)"><g transform="translate(96,830) scale(0.85)"><use href="#sitBody"/><g transform="translate(-2,-12) rotate(-6)"><use href="#headBase"/><use href="#eyesAlert"/></g></g></g>
{dust(71,(20,360,170,700),14,'#eef4ff')}{VIG}{TEX}'''

COMB=set('ัิีึืฺุู็่้๊๋์ํ')
def wlen(t): return sum(0 if c in COMB else 1 for c in t)
def wrap(text,limit=22):
    out=[];cur=''
    for w in text.split(' '):
        t=(cur+' '+w).strip()
        if wlen(t)<=limit or not cur: cur=t
        else: out.append(cur); cur=w
    out.append(cur); return out
SUBS=[['ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน','คุณจะยังคิดว่าเขาโอนผิดไหมครับ'],
['คืนแรกผมนึกว่าเขากดผิด','เพราะยอดแค่สามร้อยสามสิบสามบาท','กับอีกไม่กี่สตางค์'],
['ผมแจ้งธนาคารแล้ว','แต่คืนถัดมาเงินก็ยังเข้าตอนตีสี่ตรง','ต่างกันแค่ยอดสตางค์'],
['พอครบสิบคืน แฟนของผม','ลองจดเลขหลักสุดท้ายของแต่ละยอด','แล้วเห็นว่ามันขึ้นต้นด้วยเลขศูนย์'],
['เบอร์มือถือไทยมีสิบหลักพอดี','เธอเลยลองกดโทรดู'],
['ยังไม่ทันได้ยินเสียงรอสาย','แมวส้มของผมก็ลุกขึ้น','จ้องประตูห้องเก็บของ'],
['แล้วเสียงโทรศัพท์ก็ดังขึ้น','จากในห้องนั้น ทั้งที่เราสองคน','ยืนถือมือถือของตัวเอง','อยู่หน้าประตู'],
['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน','หรือพาแฟนกับแมวออกจากบ้านก่อน','คอมเมนต์บอกผมหน่อยครับ']]
def subtitle(i):
    ls=SUBS[i]; n=len(ls); big=max(wlen(l) for l in ls)
    fs=27 if n<=3 and big<=27 else (25 if big<=30 else 22); lh=fs+11; y0=648-(n-1)*lh/2+fs*0.38
    return f'<g class="subs" font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif" font-weight="600" font-size="{fs}" text-anchor="middle" fill="#ffffff" stroke="#0b0812" stroke-width="7" stroke-linejoin="round" paint-order="stroke">'+''.join(f'<text x="270" y="{y0+i*lh:.0f}">{l}</text>' for i,l in enumerate(ls))+'</g>'
FT='font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
def tag(x,y,text,w=None):
    w=w or 26+wlen(text)*11.5
    return f'<g {FT}><rect x="{x}" y="{y}" width="{w:.0f}" height="38" rx="19" fill="#120e1c" fill-opacity=".82" stroke="#9a86ff" stroke-opacity=".7"/><circle cx="{x+19}" cy="{y+19}" r="5" fill="#9a86ff"/><text x="{x+32}" y="{y+25}" font-size="16" font-weight="500" fill="#f2eefa">{text}</text></g>'
def callout(x,y,text,tx,ty,sub=None,w=None):
    w=w or 28+wlen(text)*12.5; h=46 if not sub else 64
    ax=x+w/2 if abs(tx-(x+w/2))<w/2 else (x if tx<x else x+w); ay=y+h if ty>y+h else (y if ty<y else y+h/2)
    g=f'<g {FT}><path d="M{ax:.0f},{ay:.0f} L{tx},{ty}" stroke="#ffffff" stroke-width="2" stroke-dasharray="4 4" opacity=".85"/><circle cx="{tx}" cy="{ty}" r="5" fill="#ffffff"/><circle cx="{tx}" cy="{ty}" r="10" fill="none" stroke="#ffffff" stroke-opacity=".5"/>'
    g+=f'<rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="12" fill="#f6f2fb" fill-opacity=".95"/><text x="{x+14}" y="{y+30}" font-size="18" font-weight="600" fill="#1a1626">{text}</text>'
    if sub: g+=f'<text x="{x+14}" y="{y+52}" font-size="13" fill="#5a5470">{sub}</text>'
    return g+'</g>'
def digits(x,y,known,label):
    g=f'<g {FT}><rect x="{x-14}" y="{y-34}" width="{10*40+18}" height="96" rx="14" fill="#120e1c" fill-opacity=".82"/><text x="{x}" y="{y-12}" font-size="15" font-weight="500" fill="#f2eefa">{label}</text>'
    for i in range(10):
        d=known[i] if i<len(known) else ''
        g+=f'<rect x="{x+i*40}" y="{y}" width="34" height="42" rx="7" fill="{"#f6f2fb" if d else "none"}" stroke="#9a86ff" stroke-width="1.6"/>'
        g+=f'<text x="{x+i*40+17}" y="{y+30}" text-anchor="middle" font-size="22" font-weight="600" fill="{"#c0392b" if i==0 else "#1a1626"}">{d}</text>' if d else f'<text x="{x+i*40+17}" y="{y+29}" text-anchor="middle" font-size="18" fill="#9a86ff">•</text>'
    return g+'</g>'
INFO=[
 tag(20,20,'คืนที่ 1 · 04:00')+callout(330,420,'+333.07 บาท',318,345,'เงินเข้าจากบัญชีที่ไม่รู้จัก',196),
 tag(20,20,'คืนที่ 1')+callout(200,840,'แค่ 333 บาท…',400,812,'คงกดผิดมั้ง',170),
 tag(330,20,'คืนที่ 2 · 04:00')+callout(20,150,'.07 → .41',36,118,'เปลี่ยนแค่สตางค์',160)+tag(40,470,'แจ้งธนาคารแล้ว'),
 tag(20,20,'คืนที่ 10')+callout(380,404,'หลักสุดท้าย',304,440,'ของแต่ละคืน',148),
 digits(70,60,'09471','เบอร์มือถือไทยมี 10 หลัก'),
 tag(20,20,'ยังไม่มีเสียงรอสาย')+callout(320,92,'ห้องเก็บของ',410,170,None,150),
 callout(170,70,'เสียงดังจากในห้อง',270,190,'แต่มือถือเราอยู่ในมือทั้งคู่',230)+tag(10,500,'มือถือเจมส์',130)+tag(400,526,'มือถือตะวัน',132),
 '<g '+FT+'><rect x="40" y="40" width="460" height="190" rx="18" fill="#120e1c" fill-opacity=".86" stroke="#9a86ff" stroke-opacity=".6"/><text x="270" y="82" text-anchor="middle" font-size="22" font-weight="600" fill="#f2eefa">ถ้าเป็นคุณ จะเลือกทางไหน?</text><rect x="64" y="104" width="412" height="48" rx="12" fill="#f6f2fb"/><text x="84" y="135" font-size="19" font-weight="600" fill="#9a86ff">A</text><text x="110" y="135" font-size="18" font-weight="500" fill="#1a1626">เปิดประตูดูว่าใครอยู่ข้างใน</text><rect x="64" y="162" width="412" height="48" rx="12" fill="#f6f2fb"/><text x="84" y="193" font-size="19" font-weight="600" fill="#e0574a">B</text><text x="110" y="193" font-size="18" font-weight="500" fill="#1a1626">พาแฟนกับแมวออกจากบ้านก่อน</text></g>']
old=G['shots']
notes=['มุมบนลงโต๊ะเกมตอนตีสี่ มือถือกลางโต๊ะขึ้น 04:00 กับแจ้งเตือนเงินเข้า อุ้งเท้าแมวยื่นเข้ามา ฝุ่นลอยในแสงโคม',
'มองจากหลังจอเข้าหาเจมส์ หน้าโดนแสงจออุ่นอ่อน ๆ ด้านหลังมีตู้เสื้อผ้า กรอบรูป วิวตึก และเตียง ฝุ่นลอยในแสงจอ',
'มุมเดิม เจมส์ถือมือถือคุยกับธนาคาร นาฬิกาบนผนังชี้สี่โมง แจ้งเตือน +333.41 เด้งขึ้นที่มุมซ้ายบน',
'ตะวันชูโน้ตวงเลขหลักสุดท้ายสีแดง ตัวแรกเป็นศูนย์ โคมโต๊ะทางขวาส่องแสงขาวอุ่น ฝุ่นลอยในลำแสงโคม',
'โคลสอัปมือตะวันกดโทร เบอร์ถูกปิดบางส่วน พื้นหลังเป็นผ้าห่มบนเตียงเบลอ มีแสงโคมหัวเตียงกับฝุ่นที่มุมขวาบน',
'มุมต่ำระดับแมวในทางเดินมืด แสงจากประตูห้องนอนส่องเฉียงลงพื้น แมวยืนในลำแสง ตาเบิก จ้องประตูห้องเก็บของ',
'เจมส์กับตะวันทำหน้าตกใจ ยืนถือมือถือของตัวเองสองข้างประตู แสงจอสีขาวอมฟ้าลอดใต้ประตู ฝุ่นลอยในแสงนั้น',
'ประตูแง้ม แสงจอจากในห้องลอดออกมาเป็นเส้น มือเจมส์เอื้อมจับลูกบิด แมวโผล่หน้าตาโตจ้องจากมุมล่าง']
svgs=[s1,s2,s3,s4,s5f,s6,s7,s8]
cards=''
for i,(o,n,svg) in enumerate(zip(old,notes,svgs),1):
    cards+=f'<figure><svg viewBox="0 0 540 960" role="img" aria-label="ช็อต {i}: {o[0]}">{svg}<g class="info">{INFO[i-1]}</g>{subtitle(i-1)}<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/></g></svg><figcaption><span class="n">ช็อต {i}</span><b>{o[0]}</b><q>{o[1]}</q><small>{n}</small></figcaption></figure>\n'
html=open('storyboard.html').read()
head=html[:html.index('<svg width="0"')].replace('wght@400;500&','wght@400;500;600&')
page=head+DEFS+extra+more+f'''<div class="wrap" id="wrap"><header><h1>ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน<span>Odd Hours · ร่างที่ 3 · ภาพนิ่ง 8 ช็อต · ซับและกราฟิก · ยังไม่พากย์</span></h1><div class="btns"><button id="tSub" type="button" aria-pressed="true">ซับ</button><button id="tInfo" type="button" aria-pressed="true">กราฟิก</button><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></div></header><div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});
for(const [id,cls] of [['tSub','hide-subs'],['tInfo','hide-info']]){{const el=document.getElementById(id);el.addEventListener('click',()=>{{const off=w.classList.toggle(cls);el.setAttribute('aria-pressed',String(!off));}});}}</script>
<style>.btns{{display:flex;gap:8px;flex-wrap:wrap}}.hide-subs .subs{{display:none}}.hide-info .info{{display:none}}</style>'''
open('storyboard2.html','w').write(page); print('built',len(page))
