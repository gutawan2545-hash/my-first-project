import re,sys
import os
D=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'oddhours') + os.sep
J=open(D+'james.html').read(); T=open(D+'tawan.html').read(); C=open(D+'cat.html').read()
def between(src,start,end,inc=True):
    a=src.index(start); b=src.index(end,a)
    return src[a:b+len(end)] if inc else src[a+len(start):b]
def inner_group(src,opener):
    a=src.index(opener)+len(opener); depth=1; i=a
    while depth:
        o=src.find('<g',i); c=src.find('</g>',i)
        if o!=-1 and o<c and src[o+2] in ' >': depth+=1; i=o+2
        else: depth-=1; i=c+4
    return src[a:i-4]
def ren(s,pairs):
    for a,b in pairs: s=s.replace('id="%s"'%a,'id="%s"'%b).replace('url(#%s)'%a,'url(#%s)'%b)
    return s
# James defs
jd=between(J,'  <clipPath id="face">','</clipPath>')+between(J,'  <clipPath id="eyeL">','</clipPath>')+between(J,'  <clipPath id="eyeR">','</clipPath>')
jd+=J[J.index('  <g id="jhead">'):J.index('  </g>\n</defs>')+6]
jd=ren(jd,[('face','jface'),('eyeL','jeyeL'),('eyeR','jeyeR')])
jbody=inner_group(J,'<g transform="translate(200,130) scale(1.4)">')
td=between(T,'  <clipPath id="face">','</clipPath>')+between(T,'  <clipPath id="eyeL">','</clipPath>')+between(T,'  <clipPath id="eyeR">','</clipPath>')
td+=T[T.index('  <g id="tback">'):T.index('  </g>\n</defs>')+6]
td=ren(td,[('face','tface'),('eyeL','teyeL'),('eyeR','teyeR')])
tbody=inner_group(T,'<g transform="translate(200,138) scale(1.4)">')
cd=C[C.index('  <clipPath id="chead">'):C.index('</defs>')]
# James pajamas: drop the tee logo, add notched collar, piping, buttons, plaid pants
for o in ['<path d="M -26,86 h12 v3 h3 v6 h-18 v-6 h3 Z" fill="#7d74e6"/>','<rect x="-23" y="91" width="2" height="2" fill="#2b3768"/>','<rect x="-16" y="91" width="2" height="2" fill="#2b3768"/>']:
    assert o in jbody; jbody=jbody.replace(o,'')
PANTS='M -41,228 L 41,228 L 44,300 L 37,462 L 9,462 L 2,292 L -2,292 L -9,462 L -37,462 L -44,300 Z'
plaid=''.join(f'<line x1="{x}" y1="220" x2="{x}" y2="470"/>' for x in range(-44,46,11))+''.join(f'<line x1="-50" y1="{y}" x2="50" y2="{y}"/>' for y in range(236,470,13))
jpj=f'''<clipPath id="jpants"><path d="{PANTS}"/></clipPath>'''
jover=f'''<g clip-path="url(#jpants)"><rect x="-50" y="220" width="100" height="250" fill="#3d4f8a" opacity=".45"/><g stroke="#7d8cc8" stroke-width="1.6" opacity=".55">{plaid}</g></g>
<path d="M -10,49 L 0,80 L 10,49 Z" fill="#efc7b0"/>
<path d="M -12,48 L -27,53 L -16,71 L 0,81 Z" fill="#34417c"/><path d="M -27,53 L -16,71 L 0,81" fill="none" stroke="#a9b8e8" stroke-width="1.6"/>
<path d="M 12,48 L 27,53 L 16,71 L 0,81 Z" fill="#1f2852"/><path d="M 27,53 L 16,71 L 0,81" fill="none" stroke="#7f8ec4" stroke-width="1.6"/>
<path d="M 0,81 L 0,233" stroke="#1a2147" stroke-width="1.2"/>
<g fill="#a9b8e8"><circle cx="2.5" cy="104" r="2.2"/><circle cx="2.5" cy="138" r="2.2"/><circle cx="2.5" cy="172" r="2.2"/><circle cx="2.5" cy="206" r="2.2"/></g>
<rect x="-34" y="94" width="17" height="19" fill="#34417c"/><path d="M -34,94 L -17,94" stroke="#a9b8e8" stroke-width="1.6"/>
<path d="M -57,116 L -40,122 M 57,116 L 40,122 M -42,232 L 42,232" stroke="#a9b8e8" stroke-width="2"/>'''
jbody=jbody+jover
# Tawan pajamas: cream button set with rose piping, long pants, slippers; front hair redrawn on top
tpanels=T[T.index('    <!-- straight front panels over the shoulders -->'):T.index('  </g>\n</defs>')]
tover='''<path d="M -42,158 L 42,158 L 46,200 L 50,442 L 8,442 L 3,252 L -3,252 L -8,442 L -50,442 Z" fill="#efe0c6"/>
<path d="M -42,158 L -26,158 L -28,200 L -32,442 L -50,442 L -46,200 Z" fill="#fff3df"/>
<path d="M 24,160 L 42,158 L 46,200 L 50,442 L 34,442 C 34,360 30,250 24,160 Z" fill="#cdb08a"/>
<path d="M -50,438 L -8,438 M 8,438 L 50,438" stroke="#c98a7a" stroke-width="2"/>
<path d="M -57,440 L -10,440 C -6,448 -7,458 -11,464 L -58,464 C -62,456 -61,446 -57,440 Z" fill="#d79a96"/><path d="M -56,440 L -11,440 L -12,447 L -57,447 Z" fill="#efc1b8"/>
<path d="M 57,440 L 10,440 C 6,448 7,458 11,464 L 58,464 C 62,456 61,446 57,440 Z" fill="#b97a78"/><path d="M 56,440 L 11,440 L 12,447 L 57,447 Z" fill="#d79a96"/>
<path d="M -14,50 L 14,50 C 26,52 36,56 40,64 L 50,98 L 38,102 L 41,204 L -41,204 L -38,102 L -50,98 L -40,64 C -36,56 -26,52 -14,50 Z" fill="#f3e6cf"/>
<path d="M -40,64 C -36,56 -26,52 -16,51 C -22,74 -26,130 -24,204 L -41,204 L -38,102 L -50,98 Z" fill="#fff6e6"/>
<path d="M 18,51 C 28,53 37,57 40,64 L 50,98 L 38,102 L 41,204 L 26,204 C 27,140 24,80 18,51 Z" fill="#d6bf9c"/>
<g fill="#e9a99a" opacity=".8"><circle cx="-20" cy="120" r="2"/><circle cx="10" cy="134" r="2"/><circle cx="-8" cy="160" r="2"/><circle cx="18" cy="178" r="2"/><circle cx="-26" cy="186" r="2"/><circle cx="24" cy="112" r="2"/></g>
<path d="M -10,50 L 0,76 L 10,50 Z" fill="#e8b08a"/>
<path d="M -12,49 L -25,54 L -15,70 L 0,77 Z" fill="#f7ecd8"/><path d="M -25,54 L -15,70 L 0,77" fill="none" stroke="#c98a7a" stroke-width="1.6"/>
<path d="M 12,49 L 25,54 L 15,70 L 0,77 Z" fill="#d9c3a2"/><path d="M 25,54 L 15,70 L 0,77" fill="none" stroke="#b67868" stroke-width="1.6"/>
<path d="M 0,77 L 0,203" stroke="#cdb08a" stroke-width="1.2"/>
<g fill="#c98a7a"><circle cx="2.5" cy="100" r="2"/><circle cx="2.5" cy="132" r="2"/><circle cx="2.5" cy="164" r="2"/></g>
<path d="M -50,98 L -38,102 M 50,98 L 38,102 M -41,203 L 41,203" stroke="#c98a7a" stroke-width="2"/>
'''+tpanels
tbody=tbody+tover

cside=inner_group(C,'<g transform="translate(-14,10)">')
eyeAlertSide='<path d="M 25,-14 C 28,-21.5 39,-20.5 42,-12 C 39,-7 29,-7 25,-14 Z" fill="#e4ad46"/><ellipse cx="36.5" cy="-13.5" rx="2.8" ry="4.4" fill="#3a2412"/><circle cx="35" cy="-15.5" r="1.1" fill="#fff6e0"/><path d="M 24.5,-15 C 28,-21.5 39,-21 42.5,-12.5" fill="none" stroke="#5a3420" stroke-width="1.6" stroke-linecap="round"/>'
cside_alert=cside.replace('<g transform="translate(100,-50) scale(1.2)"><use href="#headSide"/></g>','<g transform="translate(100,-50) scale(1.2)"><use href="#headSide"/>'+eyeAlertSide+'</g>')
assert cside_alert!=cside
FONT='font-family="IBM Plex Sans Thai, Noto Sans Thai, sans-serif"'
fx='''
<filter id="dof" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="dof2" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="6"/></filter>
<filter id="bokeh" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="haze" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="10"/></filter>
<filter id="grain" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="7" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="tintBlue" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.80 0 0 0 0.02  0 0.78 0 0 0.03  0 0 0.96 0 0.10  0 0 0 1 0"/></filter>
<filter id="tintNight" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="0.62 0 0 0 0.01  0 0.62 0 0 0.02  0 0 0.80 0 0.07  0 0 0 1 0"/></filter>
<filter id="tintAmber" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1 0 0 0 0.03  0 0.92 0 0 0.01  0 0 0.78 0 0  0 0 0 1 0"/></filter>
<radialGradient id="gVig" gradientUnits="userSpaceOnUse" cx="270" cy="420" r="640"><stop offset=".5" stop-color="#05060a" stop-opacity="0"/><stop offset="1" stop-color="#05060a" stop-opacity=".78"/></radialGradient>
<radialGradient id="gViolet" gradientUnits="userSpaceOnUse" cx="60" cy="420" r="300"><stop offset="0" stop-color="#b3a9ff" stop-opacity=".55"/><stop offset="1" stop-color="#5a4fd0" stop-opacity="0"/></radialGradient>
<radialGradient id="gAmber" gradientUnits="userSpaceOnUse" cx="480" cy="300" r="300"><stop offset="0" stop-color="#ffd18a" stop-opacity=".6"/><stop offset="1" stop-color="#ff9a3c" stop-opacity="0"/></radialGradient>
<radialGradient id="gPhone" gradientUnits="userSpaceOnUse" cx="270" cy="700" r="220"><stop offset="0" stop-color="#d8e6ff" stop-opacity=".55"/><stop offset="1" stop-color="#8fb0ff" stop-opacity="0"/></radialGradient>
<linearGradient id="gScreen" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#232a4f"/><stop offset="1" stop-color="#121530"/></linearGradient>
'''
DEFS='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'+jd+td+cd+fx+jpj+'<g id="jbody">'+jbody+'</g><g id="tbody">'+tbody+'</g><g id="catSide">'+cside+'</g><g id="catSideAlert">'+cside_alert+'</g></defs></svg>'
FIN='<rect width="540" height="960" fill="url(#gVig)"/><rect width="540" height="960" filter="url(#grain)" opacity=".055" style="mix-blend-mode:screen"/><rect width="540" height="960" filter="url(#grain)" opacity=".04" style="mix-blend-mode:overlay"/>'
def purple_room(extra=''):
    return f'''<g filter="url(#dof)">
<rect width="540" height="960" fill="#1e1c3e"/>
<path d="M0,0 L300,0 L380,960 L0,960 Z" fill="#29275a"/>
<rect y="96" width="540" height="4" fill="#9a86ff"/><path d="M0,100 L540,100 L540,124 L0,118 Z" fill="#2f2c66"/>
<rect x="378" y="150" width="90" height="120" fill="#121027"/><path d="M423,172 L452,226 L394,226 Z" fill="none" stroke="#ff6fb4" stroke-width="3"/><circle cx="423" cy="210" r="9" fill="#6fd6ff"/>
<rect x="160" y="140" width="150" height="190" fill="#141331"/><rect x="166" y="146" width="138" height="178" fill="#232a55"/><circle cx="270" cy="190" r="16" fill="#cfd6ff" opacity=".8"/>
<g fill="#30346a"><rect x="166" y="250" width="22" height="74"/><rect x="196" y="230" width="18" height="94"/><rect x="222" y="262" width="26" height="62"/><rect x="256" y="240" width="20" height="84"/><rect x="282" y="270" width="22" height="54"/></g>
<g fill="#ffd27a" opacity=".55"><rect x="200" y="240" width="4" height="4"/><rect x="226" y="272" width="4" height="4"/><rect x="262" y="252" width="4" height="4"/><rect x="290" y="280" width="4" height="4"/></g>
<g stroke="#1b1a3a" stroke-width="5"><line x1="166" y1="160" x2="304" y2="160"/><line x1="166" y1="176" x2="304" y2="176"/><line x1="166" y1="192" x2="304" y2="192"/><line x1="166" y1="208" x2="304" y2="208"/><line x1="166" y1="224" x2="304" y2="224"/><line x1="166" y1="240" x2="304" y2="240"/><line x1="166" y1="256" x2="304" y2="256"/><line x1="166" y1="272" x2="304" y2="272"/><line x1="166" y1="288" x2="304" y2="288"/><line x1="166" y1="304" x2="304" y2="304"/><line x1="166" y1="320" x2="304" y2="320"/></g>
<rect x="20" y="250" width="120" height="8" fill="#3a3672"/><rect x="28" y="214" width="16" height="36" rx="3" fill="#ff7ad1" opacity=".7"/><rect x="50" y="222" width="22" height="28" rx="4" fill="#6fd6ff" opacity=".7"/><circle cx="96" cy="234" r="14" fill="#8f86ff" opacity=".7"/><rect x="116" y="226" width="14" height="24" fill="#c9c0ff" opacity=".6"/>
<path d="M300,470 L540,440 L540,640 L300,660 Z" fill="#2b2860"/><path d="M300,470 C360,450 420,470 470,452 C500,442 520,446 540,440 L540,520 C480,530 400,540 300,540 Z" fill="#4a4596"/><rect x="460" y="410" width="80" height="44" rx="14" fill="#6a63c0"/><rect x="400" y="424" width="70" height="38" rx="12" fill="#5a54b0"/>
<path d="M330,520 C380,500 440,530 500,510" fill="none" stroke="#2b2860" stroke-width="5"/>
<path d="M16,560 C10,500 30,460 60,450 C50,500 52,530 56,560 Z" fill="#2f5a48"/><path d="M60,560 C60,500 80,470 108,466 C92,500 88,530 90,560 Z" fill="#24493a"/><rect x="22" y="556" width="74" height="40" fill="#3a3672"/>
{extra}</g>
<g filter="url(#bokeh)" opacity=".5"><circle cx="40" cy="140" r="7" fill="#ff7ad1"/><circle cx="110" cy="150" r="6" fill="#8f86ff"/><circle cx="180" cy="156" r="7" fill="#6fd6ff"/><circle cx="250" cy="158" r="6" fill="#ff7ad1"/><circle cx="320" cy="154" r="7" fill="#8f86ff"/><circle cx="500" cy="140" r="6" fill="#6fd6ff"/></g>'''
def amber_room():
    return '''<g filter="url(#dof)">
<rect width="540" height="960" fill="#35221b"/>
<path d="M200,0 L540,0 L540,960 L120,960 Z" fill="#553422"/>
<path d="M380,120 L540,80 L540,960 L260,960 C300,700 350,400 380,120 Z" fill="#7a4a2a"/>
<rect x="40" y="130" width="130" height="104" fill="#3e2617"/><rect x="46" y="136" width="118" height="92" fill="#8a5a32"/>
<path d="M56,146 L104,142 L108,198 L60,202 Z" fill="#efe2cc"/><rect x="116" y="150" width="14" height="14" fill="#e5735f"/><rect x="134" y="150" width="14" height="14" fill="#f2c15a"/><rect x="116" y="168" width="14" height="14" fill="#6ea6a0"/>
<rect x="360" y="110" width="150" height="200" fill="#2a1a12"/><path d="M366,116 L504,116 L504,304 L366,304 Z" fill="#3a2a40"/><path d="M366,116 C380,180 372,250 392,304 L366,304 Z" fill="#c9a07a"/><path d="M504,116 C490,180 498,250 478,304 L504,304 Z" fill="#b08660"/>
<rect x="40" y="290" width="150" height="8" fill="#5a3826"/><g><rect x="50" y="250" width="12" height="40" fill="#e5735f"/><rect x="64" y="256" width="10" height="34" fill="#6ea6a0"/><rect x="76" y="246" width="14" height="44" fill="#f2c15a"/><rect x="92" y="258" width="10" height="32" fill="#efe2cc"/></g>
<path d="M140,290 C130,262 142,246 156,240 C152,262 156,276 160,290 Z" fill="#5f8a5a"/><path d="M160,290 C164,262 176,252 188,250 C178,270 176,282 176,290 Z" fill="#4c7449"/><rect x="138" y="286" width="44" height="6" fill="#7a4a2a"/>
<path d="M0,600 L230,580 L240,960 L0,960 Z" fill="#6a4630"/><path d="M0,600 C60,580 140,598 230,580 L232,660 C150,672 70,670 0,676 Z" fill="#c9a07a"/><rect x="20" y="556" width="110" height="46" rx="16" fill="#efe2cc"/>
</g>'''
def hallway(floor=620, door=None):
    s=f'''<rect width="540" height="960" fill="#191d26"/><rect width="540" height="40" fill="#12151c"/><rect y="40" width="540" height="5" fill="#232835"/>
<rect y="{floor}" width="540" height="{960-floor}" fill="#1b1716"/><rect y="{floor-12}" width="540" height="12" fill="#101318"/>
<g stroke="#000" stroke-opacity=".38" stroke-width="1.5">'''
    for x in range(-200,760,60):
        s+=f'<line x1="{270+(x-270)*0.35:.0f}" y1="{floor}" x2="{x}" y2="960"/>'
    s+='</g>'
    if door:
        x0,y0,x1,y1=door
        s+=f'''<rect x="{x0-12}" y="{y0-12}" width="{x1-x0+24}" height="{y1-y0+12}" fill="#2b231f"/>
<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="#2a2420"/>
<rect x="{x0+16}" y="{y0+20}" width="{x1-x0-32}" height="{(y1-y0)*0.4:.0f}" fill="none" stroke="#1d1814" stroke-width="3"/>
<rect x="{x0+16}" y="{y0+40+(y1-y0)*0.4:.0f}" width="{x1-x0-32}" height="{(y1-y0)*0.4:.0f}" fill="none" stroke="#1d1814" stroke-width="3"/>
<circle cx="{x1-18}" cy="{(y0+y1)/2+20:.0f}" r="6" fill="#8d8a86"/><circle cx="{x1-20}" cy="{(y0+y1)/2+18:.0f}" r="2" fill="#c9c6c0"/>'''
    return s
def phone(x,y,w,h,screen):
    return f'''<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*0.14:.0f}" fill="#0c0d14"/>
<rect x="{x+6}" y="{y+6}" width="{w-12}" height="{h-12}" rx="{w*0.11:.0f}" fill="url(#gScreen)"/>
<g {FONT}>{screen}</g>'''
shots=[]
# 1 hook: phone close-up at 04:00
s1=purple_room()+f'''
<circle cx="60" cy="420" r="300" fill="url(#gViolet)" style="mix-blend-mode:screen"/>
<g filter="url(#dof2)"><rect x="0" y="770" width="540" height="190" fill="#2a2650"/><rect x="60" y="800" width="300" height="18" rx="3" fill="#14122a"/><rect x="66" y="812" width="96" height="3" fill="#ff5fa2"/><rect x="162" y="812" width="96" height="3" fill="#8a7bff"/><rect x="258" y="812" width="96" height="3" fill="#3fd0ff"/></g>
<circle cx="270" cy="330" r="260" fill="#8fb0ff" opacity=".08" filter="url(#haze)"/>
<g filter="url(#tintBlue)"><path d="M120,960 L250,960 L250,600 L176,566 Z" fill="#fbe7d8"/><path d="M210,960 L250,960 L250,600 L226,590 Z" fill="#efc7b0"/><ellipse cx="226" cy="520" rx="64" ry="66" fill="#fbe7d8"/></g>
'''+phone(170,120,200,420,'''<text x="270" y="200" text-anchor="middle" font-size="44" font-weight="500" fill="#e8ecff">04:00</text>
<text x="270" y="224" text-anchor="middle" font-size="12" fill="#9aa3c8">วันพฤหัสบดี</text>
<rect x="188" y="252" width="164" height="62" rx="12" fill="#e9ecf7" fill-opacity=".92"/>
<text x="200" y="272" font-size="10" fill="#4a5070">ธนาคาร · ตอนนี้</text>
<text x="200" y="292" font-size="13" font-weight="500" fill="#14172b">เงินเข้า +333.07 บาท</text>
<text x="200" y="306" font-size="9.5" fill="#4a5070">จากบัญชีที่ไม่รู้จัก</text>''')+'''
<g filter="url(#tintBlue)"><path d="M160,540 C150,486 158,430 176,404 C184,398 192,406 188,418 C180,444 180,494 192,540 Z" fill="#fbe7d8"/><ellipse cx="370" cy="300" rx="11" ry="18" fill="#efc7b0"/><ellipse cx="372" cy="348" rx="11" ry="17" fill="#efc7b0"/><ellipse cx="370" cy="394" rx="10" ry="15" fill="#e4b49c"/></g>
'''+FIN
shots.append(('ฮุก · ตีสี่ตรง เงินเข้าครั้งแรก','ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน คุณจะยังคิดว่าเขาโอนผิดไหมครับ','โคลสอัปมือถือในมือเจมส์ จอขึ้นเวลา 04:00 กับแจ้งเตือนเงินเข้า พื้นหลังเป็นห้องเกมเบลอ',s1))
# 2 night one: shrug at desk
def desk_purple(y=560):
    return f'''<path d="M0,{y} L540,{y} L540,960 L0,960 Z" fill="#363262"/><path d="M0,{y} L260,{y} L220,960 L0,960 Z" fill="#433e80"/><rect y="{y+28}" width="540" height="10" fill="#1a1834"/>
<path d="M20,{y-170} L120,{y-180} L124,{y-6} L24,{y} Z" fill="#100e1f"/><path d="M118,{y-180} L124,{y-180} L128,{y-6} L122,{y-6} Z" fill="#cbbfff"/>
<rect x="140" y="{y+6}" width="96" height="12" rx="2" fill="#14122a"/><rect x="144" y="{y+14}" width="88" height="2" fill="#8a7bff"/><ellipse cx="372" cy="{y+12}" rx="11" ry="6" fill="#14122a"/>
<rect x="20" y="{y-36}" width="26" height="32" rx="3" fill="#2a2850"/><path d="M46,{y-28} q12,0 12,10 q0,10 -12,10" fill="none" stroke="#2a2850" stroke-width="4"/><path d="M28,{y-44} q6,-8 0,-16 M38,{y-44} q6,-8 0,-16" fill="none" stroke="#c9c0ff" stroke-width="2" opacity=".35"/>
<rect x="488" y="{y-52}" width="20" height="48" rx="4" fill="#3fd0ff"/><rect x="488" y="{y-40}" width="20" height="12" fill="#1a1834"/>
<rect x="400" y="{y-34}" width="70" height="30" rx="4" fill="#0f0d1e"/><text x="435" y="{y-13}" text-anchor="middle" font-family="ui-monospace, monospace" font-size="16" fill="#56d8ff">04:00</text>'''
s2=purple_room()+'''<circle cx="60" cy="420" r="300" fill="url(#gViolet)" style="mix-blend-mode:screen"/>
<g filter="url(#tintBlue)"><use href="#jbody" transform="translate(270,290) scale(1.55)"/></g>
'''+desk_purple()+phone(250,568,80,24,'')+'''<rect x="256" y="572" width="68" height="16" rx="3" fill="#7d8cff" opacity=".9"/><text x="290" y="584" text-anchor="middle" font-size="9" fill="#fff" '''+FONT+'''>+333.07</text>
<ellipse cx="290" cy="560" rx="70" ry="30" fill="#9fb4ff" opacity=".18" filter="url(#haze)"/>'''+FIN
shots.append(('คืนแรก · คิดว่าเขากดผิด','คืนแรกผมนึกว่าเขากดผิด เพราะยอดแค่สามร้อยสามสิบสามบาทกับอีกไม่กี่สตางค์','เจมส์นั่งหลังโต๊ะเกม มือถือวางบนโต๊ะ จอขึ้นยอด +333.07 สีหน้ายังชิล นาฬิกาบนโต๊ะขึ้น 04:00',s2))
# 3 calls bank, next night again 04:00
arm='''<path d="M -57,64 C -64,72 -70,90 -72,108 L -55,114 L -46,74 Z" fill="#2b3768"/><path d="M -71,104 L -56,112 L -28,96 L -36,84 Z" fill="#fbe7d8"/><ellipse cx="-30" cy="88" rx="9" ry="8" fill="#fbe7d8"/>'''
s3=purple_room('<circle cx="80" cy="200" r="46" fill="#14122a"/><circle cx="80" cy="200" r="40" fill="#25224a"/><path d="M80,200 L80,170 M80,200 L104,214" stroke="#cbbfff" stroke-width="4" stroke-linecap="round"/>')+'''<circle cx="60" cy="420" r="300" fill="url(#gViolet)" style="mix-blend-mode:screen"/>
<g filter="url(#tintBlue)"><g transform="translate(270,290) scale(1.55)"><use href="#jbody"/>'''+arm+'''<rect x="-36" y="54" width="18" height="34" rx="3" fill="#0c0d14"/><rect x="-34" y="57" width="14" height="27" rx="2" fill="#3a4a8a"/></g></g>
'''+desk_purple()+f'''<g {FONT}><rect x="300" y="110" width="214" height="64" rx="14" fill="#e9ecf7" fill-opacity=".94"/>
<text x="314" y="132" font-size="11" fill="#4a5070">ธนาคาร · 04:00</text><text x="314" y="154" font-size="15" font-weight="500" fill="#14172b">เงินเข้า +333.41 บาท</text><text x="314" y="167" font-size="10" fill="#4a5070">อีกแล้ว</text></g>'''+FIN
shots.append(('คืนถัดมา · แจ้งธนาคารแล้วก็ยังเข้า','ผมแจ้งธนาคารแล้ว แต่คืนถัดมาเงินก็ยังเข้าตอนตีสี่ตรง ต่างกันแค่ยอดสตางค์','เจมส์ถือมือถือคุยกับธนาคาร นาฬิกาบนผนังชี้สี่โมง แจ้งเตือนใหม่เด้งขึ้น ยอด +333.41',s3))
# 4 Tawan's notepad
lines=[('333.1','0'),('333.4','9'),('333.0','4'),('333.2','7'),('333.8','1')]
pad=f'<g {FONT} transform="rotate(-3 270 500)"><rect x="170" y="398" width="200" height="196" rx="4" fill="#f4ead8"/><rect x="170" y="398" width="200" height="22" rx="4" fill="#e5735f"/>'
pad+='<text x="182" y="414" font-size="11" fill="#fff">เงินเข้า ตีสี่</text>'
for i,(a,d) in enumerate(lines):
    y=444+i*24
    pad+=f'<text x="184" y="{y}" font-size="13" fill="#5a4636">คืน {i+1}</text><text x="250" y="{y}" font-size="15" fill="#2e241c">{a}</text><text x="296" y="{y}" font-size="15" font-weight="500" fill="#c0392b">{d}</text><circle cx="300.5" cy="{y-5}" r="9" fill="none" stroke="#c0392b" stroke-width="1.4"/>'
pad+='<path d="M184,570 C210,566 236,574 262,568 C288,562 310,572 340,566" fill="none" stroke="#9b8670" stroke-width="1.5"/><text x="184" y="590" font-size="11" fill="#7a6656">…อีกห้าคืน</text></g>'
s4=amber_room()+'''<circle cx="480" cy="300" r="300" fill="url(#gAmber)" style="mix-blend-mode:screen"/>
<g filter="url(#tintAmber)"><use href="#tbody" transform="translate(270,250) scale(1.9)"/></g>
'''+pad+'''<g filter="url(#tintAmber)"><ellipse cx="172" cy="520" rx="14" ry="20" fill="#f8d2ab"/><ellipse cx="370" cy="500" rx="14" ry="20" fill="#e8b08a"/></g>'''+FIN
shots.append(('ครบสิบคืน · เลขตัวแรกคือศูนย์','พอครบสิบคืน แฟนของผมลองจดเลขหลักสุดท้ายของแต่ละยอดเรียงกัน แล้วเห็นว่ามันขึ้นต้นด้วยเลขศูนย์','ตะวันชูโน้ตใต้แสงโคม วงเลขหลักสุดท้ายของแต่ละคืนสีแดง ตัวแรกเป็นเลขศูนย์ เห็นแค่ห้าคืน ที่เหลือเป็นรอยขีด',s4))
# 5 Tawan dials
s5=f'''<rect width="540" height="960" fill="#151821"/>
<g filter="url(#dof2)"><rect x="40" y="200" width="160" height="520" fill="#3b3884"/><rect x="340" y="200" width="160" height="520" fill="#8a5630"/><rect x="200" y="200" width="140" height="520" fill="#13161d"/></g>
<circle cx="120" cy="420" r="160" fill="#7d6ff0" opacity=".25" filter="url(#haze)"/><circle cx="420" cy="420" r="160" fill="#ffab4f" opacity=".2" filter="url(#haze)"/>
<g filter="url(#tintNight)"><path d="M300,960 L420,960 L360,600 L300,590 Z" fill="#e8b08a"/><ellipse cx="330" cy="540" rx="60" ry="62" fill="#e8b08a"/></g>
'''+phone(170,110,200,420,'''<text x="270" y="180" text-anchor="middle" font-size="12" fill="#9aa3c8">กำลังโทร…</text>
<circle cx="270" cy="236" r="34" fill="#2e3566"/><text x="270" y="249" text-anchor="middle" font-size="34" fill="#9aa3c8">?</text>
<text x="270" y="310" text-anchor="middle" font-size="22" font-weight="500" fill="#e8ecff" letter-spacing="1">094-71•-••••</text>
<text x="270" y="332" text-anchor="middle" font-size="11" fill="#9aa3c8">ไม่มีชื่อในรายชื่อติดต่อ</text>
<circle cx="270" cy="470" r="24" fill="#e0574a"/><path d="M258,472 Q270,462 282,472" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/>''')+'''

<g filter="url(#tintNight)"><path d="M200,620 C214,570 240,510 258,478 C264,470 274,474 272,484 C262,516 248,572 236,620 Z" fill="#f8d2ab"/><ellipse cx="372" cy="300" rx="11" ry="18" fill="#e8b08a"/><ellipse cx="374" cy="348" rx="11" ry="17" fill="#e8b08a"/><ellipse cx="372" cy="394" rx="10" ry="15" fill="#d99f7c"/></g>'''+FIN

shots.append(('สิบหลักพอดี · ลองกดโทร','เบอร์มือถือไทยมีสิบหลักพอดี เธอเลยลองกดโทรดู','โคลสอัปมือถือในมือตะวัน หน้าจอกำลังโทร เบอร์ถูกปิดไว้บางส่วน พื้นหลังเป็นทางเดินมืดกับแสงสองห้องเบลอ',s5))
# 6 cat stares at storage door
s6=hallway(560,(330,170,490,560))+'''<path d="M0,560 L200,560 L120,960 L0,960 Z" fill="#2c2948" opacity=".6" filter="url(#haze)"/>
<g filter="url(#tintNight)"><use href="#catSideAlert" transform="translate(150,452) scale(1.05)"/></g>
<rect x="330" y="552" width="160" height="8" fill="#08090c"/>'''+FIN
shots.append(('แมวลุกขึ้นจ้องประตู','ยังไม่ทันได้ยินเสียงรอสาย แมวส้มของผมก็ลุกขึ้นจ้องประตูห้องเก็บของ','มุมต่ำระดับแมว แมวส้มยืนด้านข้างหันไปทางประตูห้องเก็บของ ตาเบิก ทางเดินยังมืด ใต้ประตูยังไม่มีแสง',s6))
# 7 phone rings inside
s7=hallway(700,(195,200,345,700))+'''<rect x="195" y="692" width="150" height="8" fill="#dfe9ff"/>
<path d="M150,700 L390,700 L470,860 L70,860 Z" fill="url(#gPhone)" filter="url(#haze)"/>
<g fill="none" stroke="#dfe9ff" stroke-width="3" stroke-linecap="round" opacity=".8"><path d="M300,430 q14,20 0,40"/><path d="M314,418 q22,32 0,64"/><path d="M240,430 q-14,20 0,40"/><path d="M226,418 q-22,32 0,64"/></g>
<g filter="url(#tintNight)"><use href="#jbody" transform="translate(110,300)"/><use href="#tbody" transform="translate(430,330)"/></g>
<rect x="56" y="534" width="14" height="24" rx="2" fill="#0c0d14"/><rect x="58" y="536" width="10" height="19" rx="1.5" fill="#9fb4ff"/>
<rect x="470" y="552" width="14" height="24" rx="2" fill="#0c0d14"/><rect x="472" y="554" width="10" height="19" rx="1.5" fill="#9fb4ff"/>'''+FIN
shots.append(('เสียงดังจากในห้อง','แล้วเสียงโทรศัพท์ก็ดังขึ้นจากในห้องนั้น ทั้งที่เราสองคนยืนถือมือถือของตัวเองอยู่หน้าประตู','เจมส์กับตะวันยืนสองข้างประตู ถือมือถือของตัวเองคนละเครื่อง แสงจอลอดใต้ประตู มีเส้นเสียงสั่นออกมาจากในห้อง',s7))
# 8 door ajar, hand reaching, cat peeks
s8=f'''<rect width="540" height="960" fill="#12151c"/>
<rect x="170" y="0" width="370" height="960" fill="#2a2420"/><rect x="210" y="60" width="290" height="360" fill="none" stroke="#1d1814" stroke-width="4"/><rect x="210" y="480" width="290" height="380" fill="none" stroke="#1d1814" stroke-width="4"/>
<rect x="150" y="0" width="20" height="960" fill="#050608"/><rect x="158" y="300" width="3" height="420" fill="#dfe9ff" opacity=".7" filter="url(#bokeh)"/><rect x="159" y="380" width="1.5" height="220" fill="#ffffff"/>
<circle cx="214" cy="470" r="14" fill="#8d8a86"/><circle cx="210" cy="466" r="5" fill="#c9c6c0"/>
<g filter="url(#tintNight)"><path d="M0,520 C60,500 130,480 180,470 L188,494 C140,510 70,540 0,560 Z" fill="#2b3768"/><ellipse cx="192" cy="482" rx="14" ry="11" fill="#fbe7d8"/></g>
<g filter="url(#tintNight)"><g transform="translate(96,830) scale(0.85)"><use href="#sitBody"/><g transform="translate(-2,-12) rotate(-6)"><use href="#headBase"/><use href="#eyesAlert"/></g></g></g>'''+FIN
shots.append(('คำถามปิดท้าย','ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน หรือพาแฟนกับแมวออกจากบ้านก่อน คอมเมนต์บอกผมหน่อยครับ','ประตูห้องเก็บของแง้มอยู่ ในช่องประตูมีแสงจอโทรศัพท์ มือเจมส์เอื้อมไปจับลูกบิด แมวโผล่หน้ามาจ้องจากมุมล่าง',s8))

cards=''
for i,(t,line,note,svg) in enumerate(shots,1):
    cards+=f'''<figure>
<svg viewBox="0 0 540 960" role="img" aria-label="ช็อต {i}: {t}">{svg}
<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/></g></svg>
<figcaption><span class="n">ช็อต {i}</span><b>{t}</b><q>{line}</q><small>{note}</small></figcaption>
</figure>
'''
html=f'''<title>Odd Hours ตอนโอนตีสี่</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* Layout: storyboard grid of 9:16 stills, 4 across on desktop, 2 on tablet, 1 on phone. Single dark look by choice. */
:root {{ --stage:#0d0f14; --ink:#d4d6e0; --muted:#80849a; --line:#2a2e3a; --accent:#9a86ff; --font:"IBM Plex Sans Thai","Noto Sans Thai",system-ui,sans-serif; color-scheme:dark; }}
html,body {{ background:var(--stage); color:var(--ink); }}
body {{ font-family:var(--font); padding-left:max(16px,env(safe-area-inset-left,0px)); padding-right:max(16px,env(safe-area-inset-right,0px)); padding-block:24px 40px; }}
.wrap {{ max-width:1180px; margin:0 auto; display:grid; gap:18px; }}
header {{ display:flex; flex-wrap:wrap; gap:12px; align-items:baseline; justify-content:space-between; }}
h1 {{ font-size:18px; font-weight:500; margin:0; text-wrap:balance; }}
h1 span {{ color:var(--muted); font-weight:400; font-size:14px; margin-left:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:18px; }}
@media (max-width:980px) {{ .grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
@media (max-width:520px) {{ .grid {{ grid-template-columns:1fr; }} }}
figure {{ margin:0; min-width:0; display:grid; gap:8px; align-content:start; }}
figure svg {{ display:block; width:100%; height:auto; border-radius:6px; box-shadow:0 0 0 1px var(--line); }}
figcaption {{ display:grid; gap:4px; font-size:13px; line-height:1.55; }}
.n {{ font-size:11px; letter-spacing:.06em; color:var(--accent); }}
figcaption b {{ font-weight:500; }}
figcaption q {{ color:var(--ink); quotes:"“" "”"; }}
figcaption small {{ color:var(--muted); font-size:12px; }}
.guide {{ display:none; }}
.show-guide .guide {{ display:inline; }}
button {{ font:inherit; font-size:13px; color:var(--ink); background:transparent; border:1px solid var(--line); border-radius:6px; padding:6px 12px; cursor:pointer; }}
button:hover {{ border-color:var(--muted); }}
button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
button[aria-pressed="true"] {{ border-color:var(--accent); color:#fff; }}
</style>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Thai:wght@400;500&display=swap">
{DEFS}
<div class="wrap" id="wrap">
<header><h1>ถ้ามีคนโอนเงินเข้าบัญชีคุณตอนตีสี่ทุกคืน<span>Odd Hours · ร่างแรก · ภาพนิ่ง 8 ช็อต · ยังไม่พากย์</span></h1>
<button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header>
<div class="grid">
{cards}</div>
</div>
<script>
const b=document.getElementById('toggle'),w=document.getElementById('wrap');
b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});
</script>
'''
open(sys.argv[1],'w').write(html)
print('ok',len(html))
