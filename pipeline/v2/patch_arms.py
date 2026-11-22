import re


def rep(s, o, n):
    assert o in s, o[:100]
    return s.replace(o, n, 1)


p = 'v2.py'
s = open(p).read()

# 1) arm-less body variants
s = rep(s, "extra = ('<svg width=\"0\" height=\"0\" style=\"position:absolute\" aria-hidden=\"true\"><defs>' + jhNH",
"""def drop(g, starts):
    for st in starts:
        g = re.sub(r'<path d="' + re.escape(st) + r'[^>]*/>', '', g)
    return g


LEFT_J = ['M -55,114', 'M -55,234', 'M -42,238']
LEFT_T = ['M -38,60', 'M -46,92', 'M -51,210']
RIGHT_T = ['M 38,60', 'M 46,92', 'M 51,210']
jbNHnoL = drop(jbNH, LEFT_J).replace('id="jbodyNH"', 'id="jbodyNHnoL"', 1)
tb = group_by_id(head, 'tbody'); tbS = group_by_id(head, 'tbodyS')
tbNoR = drop(tb, RIGHT_T).replace('id="tbody"', 'id="tbodyNoR"', 1)
tbSNoArms = drop(tbS, RIGHT_T + LEFT_T).replace('id="tbodyS"', 'id="tbodySNoArms"', 1)
tbSNoArms = re.sub(r'<ellipse cx="-4[57](\\.5)?" cy="20[45]"[^>]*/>', '', tbSNoArms)
assert jbNHnoL.count('M -55,114') == 0 and tbNoR.count('M 38,60') == 0 and tbSNoArms.count('M -38,60') == 0
extra = ('<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>' + jbNHnoL + tbNoR + tbSNoArms + jhNH""")
s = rep(s, "f'<g id=\"hp\">{hp}</g>", "f'<g id=\"hp\">{hp}</g>")

# 2) use them where an arm is raised
s = rep(s, "<g transform=\"translate(262,320) scale(1.7)\"><use href=\"#jbodyNH\"/>'", "<g transform=\"translate(262,320) scale(1.7)\"><use href=\"#jbodyNHnoL\"/>'")
s = rep(s, "'<g filter=\"url(#bright)\"><g transform=\"translate(160,330) scale(1.5)\"><use href=\"#jbodyNH\"/>' + armJphone", "'<g filter=\"url(#bright)\"><g transform=\"translate(160,330) scale(1.5)\"><use href=\"#jbodyNHnoL\"/>' + armJphone")
s = rep(s, "'<g transform=\"translate(400,345) scale(1.5)\"><use href=\"#tbody\"/>' + pad_t", "'<g transform=\"translate(400,345) scale(1.5)\"><use href=\"#tbodyNoR\"/>' + pad_t")
s = rep(s, """'<path d="M 18,150 L 30,120" stroke="#2a2a33" stroke-width="3" stroke-linecap="round"/><ellipse cx="22" cy="146" rx="7" ry="6" fill="#f8d2ab"/></g>')""",
           """'<path d="M 50,94 L 39,100 L 17,144 L 29,150 Z" fill="#e8b08a"/><path d="M 18,150 L 30,120" stroke="#2a2a33" stroke-width="3" stroke-linecap="round"/><ellipse cx="22" cy="146" rx="7" ry="6" fill="#f8d2ab"/></g>')""")
s = rep(s, "'<g filter=\"url(#bright)\"><use href=\"#tbodyS\" transform=\"translate(270,300) scale(2.0)\"/></g>'",
           "'<g filter=\"url(#bright)\"><g transform=\"translate(270,300) scale(2.0)\"><use href=\"#tbodySNoArms\"/><path d=\"M -50,96 L -38,100 L -47,134 L -61,131 Z\" fill=\"#f8d2ab\"/><path d=\"M 50,96 L 38,100 L 47,130 L 61,127 Z\" fill=\"#e8b08a\"/></g></g>'")
s = rep(s, "f'<g transform=\"translate(400,365) scale(1.9)\"><use href=\"#tbody\"/><g class=\"hangarm\">{armT}</g></g></g>'",
           "f'<g transform=\"translate(400,365) scale(1.9)\"><use href=\"#tbodyNoR\"/><g class=\"hangarm\">{armT}</g></g></g>'")
s = rep(s, "'<g filter=\"url(#tintNight)\"><g transform=\"translate(395,330) scale(1.15)\"><use href=\"#tbody\"/>' + armT",
           "'<g filter=\"url(#tintNight)\"><g transform=\"translate(395,330) scale(1.15)\"><use href=\"#tbodyNoR\"/>' + armT")

# 3) end card: old A/B choice card + subtitles; the logo moves to its own outro scene
a = s.index("                 f'<g class=\"q1\"")
b = s.index("')\n", a) + 2
s = s[:a] + "                 '<g class=\"choice\" opacity=\"0\">' + A8['INFO'][7] + '</g>')\n" + s[b:]
s = rep(s, "    'J4': (['ลองโทรอีกทีดิ'], ['Call it again.']),",
           "    'J4': (['ลองโทรอีกทีดิ'], ['Call it again.']),\n"
           "    'J5': (['ถ้าเป็นคุณ จะเปิดประตูไปดูว่าใครอยู่ข้างใน', 'หรือพาแฟนกับแมวออกจากบ้านก่อน', 'คอมเมนต์บอกผมหน่อยครับ'], ['If you were me, would you open the door,', 'or get my girlfriend and the cat out first?', 'Tell me in the comments.']),")
s = rep(s, "'hand_stop', 'card_in', 'logo_in', 'blink'", "'hand_stop'")
open(p, 'w').write(s)

j = open('v2.js').read()
a = j.index("    el('.q1')"); b = j.index("  }\n};", a)
j = j[:a] + "    el('.choice').setAttribute('opacity', clamp((t - 0.3) / 0.3).toFixed(2));\n" + j[b:]
open('v2.js', 'w').write(j)
print('patched')
