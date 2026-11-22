def rep(s, o, n):
    assert o in s, o[:90]
    return s.replace(o, n, 1)

p = 'all12.py'
s = open(p).read()
# shot 8: same light level as the notepad shot (6): bright people, dark foreground, no extra glow
s = rep(s, "sC = room_top + bg + '<g filter=\"url(#tintWarm)\"><g transform=\"translate(150,330) scale(1.5)\"><use href=\"#jbodyS\"/>' + armJ + '</g>'",
           "sC = room_top + bg + '<g filter=\"url(#bright)\"><g transform=\"translate(150,330) scale(1.5)\"><use href=\"#jbodyS\"/>' + armJ + '</g>'")
s = rep(s, "sC += '<rect width=\"540\" height=\"960\" fill=\"url(#dark)\" style=\"mix-blend-mode:multiply\"/>'\n", "")
s = rep(s, '<path d="M-20,740 C120,700 300,760 560,710 L560,960 L-20,960 Z" fill="#5a4a76"/><path d="M-20,740 C120,700 300,760 560,710 L560,770 C300,800 120,760 -20,800 Z" fill="#7a6a9a"/>',
           '<path d="M-20,740 C120,700 300,760 560,710 L560,960 L-20,960 Z" fill="#21152a"/><path d="M-20,740 C120,700 300,760 560,710 L560,750 C300,780 120,740 -20,780 Z" fill="#3a2634"/>')
s = rep(s, "sC += '<circle cx=\"430\" cy=\"300\" r=\"160\" fill=\"#ffe6da\" opacity=\".14\" filter=\"url(#haze)\" style=\"mix-blend-mode:screen\"/>' + dust(91",
           "sC += dust(91")
# shot 11: head AND body (bust), not a floating head
s = rep(s, "sD += '<g filter=\"url(#tintNight)\"><g transform=\"translate(220,360) scale(3.1)\"><use href=\"#jheadScared\"/></g></g>' + notes",
           "sD += '<g filter=\"url(#tintNight)\"><use href=\"#jbodyS\" transform=\"translate(230,300) scale(2.3)\"/></g>' + notes")
s = s.replace('โคลสอัปหน้าเจมส์ตกใจในทางเดินมืด', 'ภาพครึ่งตัวเจมส์หน้าตกใจในทางเดินมืด')
s = s.replace("'ในห้องนอน เจมส์หน้าตกใจเอื้อมมือไปห้าม", "'ในห้องนอน ความสว่างเท่าช็อต 6 เจมส์หน้าตกใจเอื้อมมือไปห้าม")
open(p, 'w').write(s)
print('patched')
