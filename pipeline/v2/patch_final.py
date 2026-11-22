"""Mouth B for James, new subtitles for the two re-recorded lines, sparse dust in the air of every shot
(some motes catch the light), finer film grain that shows in the darks, a slightly brighter grade."""


def rep(s, o, n):
    assert o in s, o[:110]
    return s.replace(o, n, 1)


p = 'v2.py'; s = open(p).read()
# James mouth B + warm-brown open mouth
s = rep(s, "for o, n in [('#a05a50', '#d29a8a'), ('#6b3a3a', '#c07f74'), ('#b0605a', '#ecbcae'),",
"""SM = '<path d="M -6,24.4 Q 1,25.6 7.5,21.4" fill="none" stroke="#a05a50" stroke-width="1.8" stroke-linecap="round"/><path d="M 7.5,21.4 L 9,20.4" stroke="#d29d86" stroke-width="1.2" stroke-linecap="round"/>'
LIP = '<path d="M -3.5,27.4 Q 0,28.8 3.5,27.4" fill="none" stroke="#efc7b0" stroke-width="1.4" stroke-linecap="round"/>'
assert SM in html and LIP in html, 'james mouth'
html = html.replace(SM, '<path d="M -6.5,24.6 Q 0,25.6 6.5,24.2" fill="none" stroke="#a87466" stroke-width="1.7" stroke-linecap="round"/>')
html = html.replace(LIP, '<path d="M -2.6,28.8 Q 0,29.6 2.6,28.8" fill="none" stroke="#e6bea8" stroke-width="1.3" stroke-linecap="round"/>')
for o, n in [('#a05a50', '#a87466'), ('#6b3a3a', '#9a6a60'), ('#b0605a', '#c99a8c'),""")
# subtitles for the re-recorded lines
s = rep(s, "    'T1': (['เจม ดูตรงสตางค์สิ…', 'อ่านตัวสุดท้ายให้ฟังหน่อย', 'เริ่มจากคืนแรกนะ'], ['James, look at the satang…', 'Read me the last digits,', 'starting from the first night.']),",
           "    'T1': (['เจม ลองดูยอดเงินแต่ละคืนสิ…', 'เอาแค่ตัวเลขหลักสุดท้าย อ่านให้ฟังหน่อย', 'เริ่มจากคืนแรกนะ'], ['James, look at each night\\'s amount…', 'Just read me the last digit of each,', 'starting from the first night.']),")
s = rep(s, "    'J4': (['ลองโทรอีกทีดิ'], ['Call it again.']),", "    'J4': (['ลองโทรไปอีกรอบไหม'], ['Should we call it again?']),")
# sparse dust in the air of every shot
s = rep(s, "f'<g class=\"cam\" filter=\"url(#zb{i})\">{SV[k]}{VIG}{TEX}</g>",
           "f'<g class=\"cam\" filter=\"url(#zb{i})\">{SV[k]}{dust(700 + i, (20, 80, 520, 900), 9)}{VIG}{GRAIN}</g>")
s = rep(s, "cards = ''\ncfg = []",
"""GRAIN = ('<rect width="540" height="960" filter="url(#stipple)" opacity=".10" style="mix-blend-mode:overlay"/>'
         '<rect width="540" height="960" filter="url(#grainF)" opacity=".085" style="mix-blend-mode:screen"/>')
cards = ''
cfg = []""")
s = rep(s, "+ '<filter id=\"tintDim\"", "+ '<filter id=\"grainF\" filterUnits=\"userSpaceOnUse\" x=\"0\" y=\"0\" width=\"540\" height=\"960\"><feTurbulence type=\"fractalNoise\" baseFrequency=\"2.2\" numOctaves=\"1\" seed=\"11\"/><feColorMatrix type=\"saturate\" values=\"0\"/></filter>' + '<filter id=\"tintDim\"")
open(p, 'w').write(s)

# dust: occasional glint when a mote catches the light
p = 'v2.js'; j = open(p).read()
j = rep(j, "p.c.setAttribute('opacity', (p.o * (0.55 + 0.45 * Math.sin(t * 2.2 + k * 2.3))).toFixed(2));",
           "const glint = Math.max(0, Math.sin(t * 1.3 + k * 4.1) - 0.93) * 9; p.c.setAttribute('opacity', Math.min(1, p.o * (0.55 + 0.45 * Math.sin(t * 2.2 + k * 2.3)) + glint * 0.5).toFixed(2));")
open(p, 'w').write(j)

# grade: a little brighter and more vivid; fine temporal grain on top
p = 'assemble.sh'; a = open(p).read()
a = rep(a, 'GRADE="eq=contrast=1.07:saturation=0.9:gamma=0.98,colorbalance=rs=-0.04:gs=-0.01:bs=0.05:rh=0.04:gh=0.01:bh=-0.03,curves=all=\'0/0.02 0.5/0.48 1/0.97\'"',
        'GRADE="eq=contrast=1.05:saturation=1.08:gamma=1.04:brightness=0.015,colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02,curves=all=\'0/0.03 0.5/0.51 1/0.98\',noise=c0s=7:c0f=t+u"')
open(p, 'w').write(a)
print('patched final look')
