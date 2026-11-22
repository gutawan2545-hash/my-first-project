import runpy,sys
sys.argv=['b','_tmp.html']
G=runpy.run_path('build.py')
DEFS=G['DEFS']; FONT=G['FONT']
extra='''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="stipple" filterUnits="userSpaceOnUse" x="0" y="0" width="540" height="960"><feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="3"/><feColorMatrix type="saturate" values="0"/><feComponentTransfer><feFuncR type="discrete" tableValues="0 0 1"/><feFuncG type="discrete" tableValues="0 0 1"/><feFuncB type="discrete" tableValues="0 0 1"/></feComponentTransfer></filter>
<filter id="moteBlur" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.1"/></filter>
<filter id="moteGlow" x="-300%" y="-300%" width="700%" height="700%"><feGaussianBlur stdDeviation="1.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<linearGradient id="beam" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="300" y2="520"><stop offset="0" stop-color="#fff2e8" stop-opacity=".22"/><stop offset="1" stop-color="#fff2e8" stop-opacity="0"/></linearGradient>
<linearGradient id="monBeam" gradientUnits="userSpaceOnUse" x1="200" y1="480" x2="250" y2="260"><stop offset="0" stop-color="#ffe6da" stop-opacity=".3"/><stop offset="1" stop-color="#ffe6da" stop-opacity="0"/></linearGradient>
<linearGradient id="night" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#151a3a"/><stop offset="1" stop-color="#2c2f5c"/></linearGradient>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="4"/></filter>
<filter id="tintWarm" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values="1.0 0 0 0 0.02  0 0.92 0 0 0.0  0 0 0.86 0 0.01  0 0 0 1 0"/></filter>
<linearGradient id="wood" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="540" y2="960"><stop offset="0" stop-color="#d8a58c"/><stop offset=".35" stop-color="#a86a64"/><stop offset=".7" stop-color="#6c3b4e"/><stop offset="1" stop-color="#36203a"/></linearGradient>
<radialGradient id="pool" gradientUnits="userSpaceOnUse" cx="120" cy="140" r="520"><stop offset="0" stop-color="#ffeedd" stop-opacity=".45"/><stop offset="1" stop-color="#f3c9b8" stop-opacity="0"/></radialGradient>
<radialGradient id="scrGlow" gradientUnits="userSpaceOnUse" cx="250" cy="360" r="210"><stop offset="0" stop-color="#cfd8ff" stop-opacity=".45"/><stop offset="1" stop-color="#9fb0ff" stop-opacity="0"/></radialGradient>
<linearGradient id="phoneBody" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a3f58"/><stop offset="1" stop-color="#161827"/></linearGradient>
<linearGradient id="scr2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3b3f8a"/><stop offset=".55" stop-color="#232665"/><stop offset=".56" stop-color="#2c2f78"/><stop offset="1" stop-color="#1a1c48"/></linearGradient>
<radialGradient id="coffee" cx=".4" cy=".35" r=".7"><stop offset="0" stop-color="#a9683a"/><stop offset="1" stop-color="#3f1f14"/></radialGradient>
<linearGradient id="mugG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff4e4"/><stop offset="1" stop-color="#c9a78f"/></linearGradient>
<linearGradient id="room" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="540" y2="960"><stop offset="0" stop-color="#2f2236"/><stop offset=".6" stop-color="#221a2c"/><stop offset="1" stop-color="#15101e"/></linearGradient>
<linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3f6a"/><stop offset="1" stop-color="#5a5a86"/></linearGradient>
<radialGradient id="faceLight" gradientUnits="userSpaceOnUse" cx="250" cy="420" r="230"><stop offset="0" stop-color="#ffd7c2" stop-opacity=".45"/><stop offset=".6" stop-color="#e8a8a0" stop-opacity=".14"/><stop offset="1" stop-color="#e8a8a0" stop-opacity="0"/></radialGradient>
<linearGradient id="monBack" gradientUnits="userSpaceOnUse" x1="0" y1="520" x2="340" y2="760"><stop offset="0" stop-color="#b9a8b8" stop-opacity=".92"/><stop offset=".7" stop-color="#8a7488" stop-opacity=".92"/><stop offset="1" stop-color="#f0c0b0" stop-opacity=".9"/></linearGradient>
<linearGradient id="dark" gradientUnits="userSpaceOnUse" x1="540" y1="200" x2="200" y2="700"><stop offset="0" stop-color="#12060e" stop-opacity=".65"/><stop offset="1" stop-color="#12060e" stop-opacity="0"/></linearGradient>
</defs></svg>'''
TEX='<rect width="540" height="960" filter="url(#stipple)" opacity=".10" style="mix-blend-mode:overlay"/><rect width="540" height="960" filter="url(#grain)" opacity=".05" style="mix-blend-mode:screen"/>'
VIG='<rect width="540" height="960" fill="url(#gVig)"/>'
def dust(seed,box,n,col='#fff6ec'):
    import random
    r=random.Random(seed); x0,y0,x1,y1=box; near=''; far=''
    for i in range(n):
        x=r.uniform(x0,x1); y=r.uniform(y0,y1); z=r.random()
        if z<0.45: far+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.4,2.4):.1f}" opacity="{r.uniform(.25,.45):.2f}"/>'
        else: near+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(.6,1.5):.1f}" opacity="{r.uniform(.55,.95):.2f}"/>'
    return f'<g fill="{col}"><g filter="url(#moteBlur)">{far}</g><g filter="url(#moteGlow)">{near}</g></g>'
def shadow(shape): return f'<g transform="translate(16,20)" filter="url(#sh)" opacity=".45">{shape.replace("fill=","data-f=").replace("<path ","<path fill=\"#2a0e1c\" ").replace("<rect ","<rect fill=\"#2a0e1c\" ").replace("<circle ","<circle fill=\"#2a0e1c\" ").replace("<ellipse ","<ellipse fill=\"#2a0e1c\" ")}</g>'
# ---------- shot 1: top-down desk ----------
planks=''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="960" stroke="#5a2030" stroke-opacity=".28" stroke-width="2"/>' for x in range(-10,560,46))
phone_shape='<rect x="-82" y="-160" width="164" height="320" rx="24"/>'
phone=f'''<g transform="translate(250,350) rotate(-9)">
{shadow(phone_shape)}
<rect x="-82" y="-160" width="164" height="320" rx="24" fill="url(#phoneBody)"/>
<rect x="-74" y="-152" width="148" height="304" rx="18" fill="url(#scr2)"/>
<g {FONT}><text x="0" y="-92" text-anchor="middle" font-size="40" font-weight="500" fill="#eef0ff">04:00</text>
<text x="0" y="-70" text-anchor="middle" font-size="10" fill="#a9b0dc">วันพฤหัสบดี</text>
<rect x="-62" y="-50" width="124" height="54" rx="11" fill="#eef0f8" fill-opacity=".94"/>
<text x="-52" y="-32" font-size="8.5" fill="#4a5070">ธนาคาร · ตอนนี้</text>
<text x="-52" y="-15" font-size="11.5" font-weight="500" fill="#14172b">เงินเข้า +333.07 บาท</text>
<text x="-52" y="-3" font-size="8" fill="#4a5070">จากบัญชีที่ไม่รู้จัก</text></g>
<path d="M -74,60 L 74,-20 L 74,40 L -74,120 Z" fill="#ffffff" opacity=".05"/>
<rect x="-82" y="-160" width="164" height="320" rx="24" fill="none" stroke="#6a6f90" stroke-width="2"/>
</g>'''
mug_shape='<circle cx="0" cy="0" r="62"/>'
mug=f'''<g transform="translate(430,170)">{shadow(mug_shape)}
<circle r="62" fill="url(#mugG)"/><circle r="50" fill="#e9d3c0"/><circle r="44" fill="url(#coffee)"/>
<path d="M 46,-18 C 84,-22 86,22 48,20" fill="none" stroke="#e9d3c0" stroke-width="12"/>
<ellipse cx="-14" cy="-14" rx="14" ry="6" fill="#d9a070" opacity=".5" transform="rotate(-30)"/></g>'''
kb_shape='<rect x="-230" y="-60" width="460" height="120" rx="12"/>'
keys=''.join(f'<rect x="{-216+i*30}" y="{-46+j*28}" width="24" height="22" rx="4" fill="#4a5070"/>' for i in range(15) for j in range(4))
kb=f'''<g transform="translate(250,30) rotate(4)">{shadow(kb_shape)}<rect x="-230" y="-60" width="460" height="120" rx="12" fill="#2c3048"/>{keys}<rect x="-230" y="52" width="460" height="6" fill="#ff5fa2" opacity=".6"/></g>'''
hp_shape='<path d="M -90,0 C -90,-90 90,-90 90,0" stroke-width="18" fill="none"/>'
headphones=f'''<g transform="translate(140,830) rotate(-18)">
<g transform="translate(16,20)" filter="url(#sh)" opacity=".45"><path d="M -90,0 C -90,-90 90,-90 90,0" stroke="#2a0e1c" stroke-width="18" fill="none"/><ellipse cx="-90" cy="16" rx="34" ry="40" fill="#2a0e1c"/><ellipse cx="90" cy="16" rx="34" ry="40" fill="#2a0e1c"/></g>
<path d="M -90,0 C -90,-90 90,-90 90,0" stroke="#22202e" stroke-width="18" fill="none"/><path d="M -84,-14 C -78,-74 0,-84 40,-74" stroke="#5a5480" stroke-width="4" fill="none"/>
<ellipse cx="-90" cy="16" rx="34" ry="40" fill="#2e2c44"/><ellipse cx="-90" cy="16" rx="22" ry="27" fill="#18171f"/>
<ellipse cx="90" cy="16" rx="34" ry="40" fill="#24223a"/><ellipse cx="90" cy="16" rx="22" ry="27" fill="#18171f"/><circle cx="100" cy="44" r="4" fill="#b18cff"/></g>'''
ctrl=f'''<g transform="translate(430,840) rotate(14)">
<g transform="translate(16,20)" filter="url(#sh)" opacity=".45"><path d="M -80,-30 C -60,-50 60,-50 80,-30 C 100,0 104,50 80,56 C 60,60 46,24 30,20 L -30,20 C -46,24 -60,60 -80,56 C -104,50 -100,0 -80,-30 Z" fill="#2a0e1c"/></g>
<path d="M -80,-30 C -60,-50 60,-50 80,-30 C 100,0 104,50 80,56 C 60,60 46,24 30,20 L -30,20 C -46,24 -60,60 -80,56 C -104,50 -100,0 -80,-30 Z" fill="#e9e4f0"/>
<path d="M -80,-30 C -60,-50 60,-50 80,-30 C 70,-36 -70,-36 -80,-30 Z" fill="#ffffff"/>
<circle cx="-46" cy="-6" r="14" fill="#2c3048"/><circle cx="26" cy="12" r="12" fill="#2c3048"/>
<g fill="#ff6fa8"><circle cx="54" cy="-20" r="5"/></g><g fill="#6fd6ff"><circle cx="66" cy="-8" r="5"/></g><g fill="#ffd27a"><circle cx="42" cy="-8" r="5"/></g><g fill="#9a86ff"><circle cx="54" cy="4" r="5"/></g></g>'''
note=f'''<g transform="translate(96,520) rotate(-6)"><g transform="translate(10,14)" filter="url(#sh)" opacity=".4"><rect x="-56" y="-56" width="112" height="112" fill="#2a0e1c"/></g><rect x="-56" y="-56" width="112" height="112" fill="#ffd972"/><path d="M -56,40 L 56,40 L 56,56 L 40,56 Z" fill="#f0c45a"/>
<g {FONT}><text x="-40" y="-22" font-size="18" fill="#7a4a20">333.07</text><text x="-40" y="4" font-size="18" fill="#7a4a20">333.41 ?</text></g></g>'''
paw=f'''<g transform="translate(540,560)"><g transform="translate(14,18)" filter="url(#sh)" opacity=".45"><path d="M 0,-40 L -70,-40 C -100,-40 -122,-20 -122,4 C -122,28 -100,44 -70,44 L 0,44 Z" fill="#2a0e1c"/></g>
<path d="M 0,-40 L -70,-40 C -100,-40 -122,-20 -122,4 C -122,28 -100,44 -70,44 L 0,44 Z" fill="#e8964a"/>
<path d="M 0,-40 L -70,-40 C -96,-40 -114,-26 -119,-8 C -100,-24 -60,-28 0,-26 Z" fill="#f7b874"/>
<circle cx="-112" cy="-18" r="15" fill="#f7e3c4"/><circle cx="-122" cy="4" r="15" fill="#f7e3c4"/><circle cx="-112" cy="26" r="15" fill="#efd4b0"/>
<path d="M -98,-8 L -128,-8 M -98,15 L -128,15" stroke="#d9b48a" stroke-width="2"/>
<path d="M -40,-40 L -34,-20 M -14,-40 L -10,-22" stroke="#c46e2e" stroke-width="3" opacity=".6"/></g>'''
s1=f'''<rect width="540" height="960" fill="url(#wood)"/>{planks}
<rect width="540" height="960" fill="url(#pool)" style="mix-blend-mode:screen"/>
{kb}{mug}{note}{headphones}{ctrl}{paw}
<circle cx="250" cy="350" r="210" fill="url(#scrGlow)" style="mix-blend-mode:screen"/>
{phone}
<path d="M0,0 L380,0 L60,700 L0,760 Z" fill="url(#beam)" filter="url(#haze)" style="mix-blend-mode:screen"/>
<path d="M540,0 L540,300 L260,960 L80,960 Z" fill="#1a0814" opacity=".38"/>
{dust(11,(10,90,330,560),22)}
{VIG}{TEX}'''
# ---------- shot 2: behind the screen ----------
s2=f'''<rect width="540" height="960" fill="url(#room)"/>
<g filter="url(#dof)">
<rect x="0" y="90" width="150" height="600" fill="#3a2a3e"/><rect x="6" y="98" width="66" height="584" fill="#45334a"/><rect x="78" y="98" width="66" height="584" fill="#3e2e44"/><rect x="64" y="360" width="4" height="40" rx="2" fill="#b9a8c0"/><rect x="82" y="360" width="4" height="40" rx="2" fill="#b9a8c0"/><rect x="0" y="90" width="150" height="10" fill="#2a1e30"/>
<rect x="180" y="104" width="124" height="86" fill="#d9c9bc"/><rect x="188" y="112" width="108" height="70" fill="#4a5a86"/><path d="M188,182 L230,140 L262,170 L280,152 L296,170 L296,182 Z" fill="#7d8cc8"/><circle cx="270" cy="128" r="8" fill="#f0d8c8"/>
<rect x="160" y="200" width="44" height="58" fill="#d9c9bc"/><rect x="165" y="205" width="34" height="48" fill="#a86a7a"/>
<rect x="330" y="120" width="200" height="300" fill="#2a1e30"/><rect x="342" y="132" width="176" height="276" fill="url(#night)"/><rect x="342" y="257" width="26" height="151" fill="#1a1d42"/><rect x="346" y="279" width="3" height="4" fill="#cfe0ff" opacity="0.85"/><rect x="354" y="279" width="3" height="4" fill="#ffe2a8" opacity="0.91"/><rect x="362" y="279" width="3" height="4" fill="#cfe0ff" opacity="0.89"/><rect x="354" y="293" width="3" height="4" fill="#ffe2a8" opacity="0.51"/><rect x="362" y="293" width="3" height="4" fill="#cfe0ff" opacity="0.58"/><rect x="346" y="321" width="3" height="4" fill="#ffd0a0" opacity="0.78"/><rect x="354" y="321" width="3" height="4" fill="#ffe2a8" opacity="0.94"/><rect x="362" y="321" width="3" height="4" fill="#ffe2a8" opacity="0.93"/><rect x="346" y="335" width="3" height="4" fill="#ffe2a8" opacity="0.63"/><rect x="354" y="349" width="3" height="4" fill="#ffd0a0" opacity="0.59"/><rect x="354" y="363" width="3" height="4" fill="#cfe0ff" opacity="0.57"/><rect x="362" y="363" width="3" height="4" fill="#ffe2a8" opacity="0.65"/><rect x="354" y="391" width="3" height="4" fill="#cfe0ff" opacity="0.87"/><rect x="371" y="225" width="23" height="183" fill="#141838"/><rect x="383" y="233" width="3" height="4" fill="#ffe2a8" opacity="0.93"/><rect x="375" y="317" width="3" height="4" fill="#ffe2a8" opacity="0.92"/><rect x="375" y="359" width="3" height="4" fill="#ffd0a0" opacity="0.85"/><rect x="383" y="387" width="3" height="4" fill="#ffd0a0" opacity="0.77"/><rect x="399" y="269" width="20" height="139" fill="#1a1d42"/><rect x="411" y="277" width="3" height="4" fill="#ffe2a8" opacity="0.78"/><rect x="403" y="319" width="3" height="4" fill="#ffd0a0" opacity="0.74"/><rect x="403" y="333" width="3" height="4" fill="#ffd0a0" opacity="0.65"/><rect x="411" y="333" width="3" height="4" fill="#ffd0a0" opacity="0.69"/><rect x="403" y="347" width="3" height="4" fill="#ffd0a0" opacity="0.51"/><rect x="411" y="361" width="3" height="4" fill="#ffd0a0" opacity="0.75"/><rect x="403" y="375" width="3" height="4" fill="#cfe0ff" opacity="0.55"/><rect x="403" y="389" width="3" height="4" fill="#cfe0ff" opacity="0.63"/><rect x="424" y="224" width="32" height="184" fill="#1a1d42"/><rect x="436" y="246" width="3" height="4" fill="#cfe0ff" opacity="0.87"/><rect x="428" y="260" width="3" height="4" fill="#cfe0ff" opacity="0.89"/><rect x="436" y="260" width="3" height="4" fill="#cfe0ff" opacity="0.62"/><rect x="444" y="344" width="3" height="4" fill="#ffd0a0" opacity="0.85"/><rect x="436" y="358" width="3" height="4" fill="#cfe0ff" opacity="0.87"/><rect x="459" y="312" width="28" height="96" fill="#1a1d42"/><rect x="471" y="320" width="3" height="4" fill="#cfe0ff" opacity="0.92"/><rect x="463" y="348" width="3" height="4" fill="#ffd0a0" opacity="0.73"/><rect x="479" y="362" width="3" height="4" fill="#ffe2a8" opacity="0.59"/><rect x="479" y="376" width="3" height="4" fill="#ffd0a0" opacity="0.58"/><rect x="489" y="314" width="19" height="94" fill="#0f1230"/><rect x="501" y="322" width="3" height="4" fill="#ffe2a8" opacity="0.75"/><rect x="501" y="350" width="3" height="4" fill="#ffe2a8" opacity="0.61"/><rect x="501" y="364" width="3" height="4" fill="#cfe0ff" opacity="0.93"/><rect x="509" y="324" width="27" height="84" fill="#141838"/><rect x="513" y="374" width="3" height="4" fill="#ffd0a0" opacity="0.67"/><rect x="529" y="374" width="3" height="4" fill="#ffe2a8" opacity="0.77"/><rect x="529" y="388" width="3" height="4" fill="#ffe2a8" opacity="0.65"/>
<rect x="426" y="132" width="6" height="276" fill="#2a1e30"/><rect x="342" y="266" width="176" height="6" fill="#2a1e30"/>
<path d="M320,470 L540,452 L540,690 L320,690 Z" fill="#3a2e4e"/><path d="M320,470 C380,456 450,474 540,452 L540,560 C450,572 380,566 320,560 Z" fill="#6a5a8a"/><rect x="452" y="414" width="88" height="48" rx="16" fill="#cfc4dc"/><rect x="380" y="430" width="80" height="40" rx="14" fill="#b8acc8"/>
<path d="M330,540 C390,520 460,548 540,528" fill="none" stroke="#3a2e4e" stroke-width="5"/>
</g>
<g filter="url(#tintWarm)"><use href="#jbody" transform="translate(262,320) scale(1.7)"/></g>
<rect width="540" height="960" fill="url(#dark)" style="mix-blend-mode:multiply"/>
<circle cx="250" cy="420" r="230" fill="url(#faceLight)" style="mix-blend-mode:screen"/>
<path d="M40,500 L330,470 L330,250 L150,250 Z" fill="url(#monBeam)" filter="url(#haze)" style="mix-blend-mode:screen"/>
{dust(23,(110,250,380,480),20)}
<rect x="0" y="690" width="540" height="270" fill="#2a1a2a"/><path d="M0,690 L540,690 L540,960 L0,960 Z" fill="url(#faceLight)" opacity=".5"/><rect x="0" y="690" width="540" height="6" fill="#4a2e3a"/>
<g><rect x="372" y="626" width="130" height="30" rx="3" fill="#3a3f6a"/><rect x="380" y="654" width="140" height="36" rx="3" fill="#2c3050"/><rect x="380" y="666" width="140" height="4" fill="#5a6aa0"/>
<path d="M398,560 L466,560 L460,626 L404,626 Z" fill="#d9874a"/><path d="M398,560 L420,560 L418,626 L404,626 Z" fill="#f0a868"/><path d="M466,574 q26,4 20,26 q-4,14 -24,12" fill="none" stroke="#c46e3a" stroke-width="7"/>
<path d="M404,574 l8,-6 l8,6 l8,-6 l8,6 l8,-6 l8,6" fill="none" stroke="#8a3a2a" stroke-width="2"/></g>
<path d="M-10,500 L340,466 L368,700 L-10,700 Z" fill="url(#monBack)"/>
<path d="M120,600 l16,-14 l16,14 l-16,14 Z" fill="#d9c6d6" opacity=".7"/>
<path d="M340,466 L368,700 L360,700 L334,468 Z" fill="#f6d2c4"/>

<rect x="0" y="696" width="340" height="10" fill="#f0c0b0" opacity=".5" filter="url(#bokeh)"/>
<g transform="translate(150,800) rotate(-4)"><rect x="-150" y="-30" width="300" height="70" rx="8" fill="#211a2c"/>{''.join(f'<rect x="{-140+i*28}" y="{-22+j*20}" width="22" height="15" rx="3" fill="#3a3050"/>' for i in range(10) for j in range(3))}<rect x="-150" y="34" width="300" height="5" fill="#9a86ff" opacity=".7"/></g>
<g transform="translate(430,820) rotate(12)"><rect x="-38" y="-70" width="76" height="140" rx="12" fill="#14152a"/><rect x="-33" y="-65" width="66" height="130" rx="9" fill="#2c2f78"/><rect x="-28" y="-36" width="56" height="26" rx="6" fill="#eef0f8" opacity=".92"/><rect x="-22" y="-28" width="40" height="4" fill="#4a5070"/><rect x="-22" y="-20" width="30" height="4" fill="#14172b"/></g>
<circle cx="430" cy="820" r="90" fill="#9fb0ff" opacity=".18" filter="url(#haze)" style="mix-blend-mode:screen"/>
{VIG}{TEX}'''
frames=[('ช็อต 1 · มุมบนลงโต๊ะ','มุมบนลงโต๊ะเกมตอนตีสี่ มือถือวางอยู่กลางโต๊ะ จอขึ้น 04:00 กับแจ้งเตือนเงินเข้า รอบ ๆ มีคีย์บอร์ด แก้วกาแฟ หูฟัง จอย และโน้ตจดยอดเงิน อุ้งเท้าแมวยื่นเข้ามาจากขอบขวา ฝุ่นเล็ก ๆ ลอยในแสงโคม',s1),
        ('ช็อต 2 · มุมหลังจอ','มองจากหลังจอเกมเข้าหาเจมส์ หน้าโดนแสงจออุ่นอ่อน ๆ ด้านหลังมีตู้เสื้อผ้า กรอบรูปแขวนผนัง หน้าต่างเห็นวิวตึกตอนกลางคืน และเตียงนอน ฝุ่นเล็ก ๆ ลอยอยู่ในแสงจอ',s2)]
cards=''.join(f'<figure><svg viewBox="0 0 540 960" role="img" aria-label="{t}">{svg}<g class="guide"><rect x="24" y="576" width="492" height="144" fill="none" stroke="#fff" stroke-opacity=".7" stroke-dasharray="6 5" stroke-width="1.5"/></g></svg><figcaption><b>{t}</b><small>{n}</small></figcaption></figure>' for t,n,svg in frames)
html=open('storyboard.html').read()
head=html[:html.index('<svg width="0"')].replace('<title>Odd Hours ตอนโอนตีสี่</title>','<title>Odd Hours ทดสอบโทนภาพ</title>').replace('repeat(4,minmax(0,1fr))','repeat(2,minmax(0,1fr))').replace('max-width:1180px','max-width:860px')
page=head+DEFS+extra+f'''<div class="wrap" id="wrap"><header><h1>ทดสอบโทนสีและมุมภาพ<span>Odd Hours · ตอนโอนตีสี่ · ช็อต 1–2 แบบใหม่</span></h1><button id="toggle" type="button" aria-pressed="false">แสดงพื้นที่ซับ</button></header><div class="grid">{cards}</div></div>
<script>const b=document.getElementById('toggle'),w=document.getElementById('wrap');b.addEventListener('click',()=>{{const on=w.classList.toggle('show-guide');b.setAttribute('aria-pressed',String(on));b.textContent=on?'ซ่อนพื้นที่ซับ':'แสดงพื้นที่ซับ';}});</script>'''
open('styletest.html','w').write(page); print('ok')
