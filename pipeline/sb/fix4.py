def rep(s, o, n):
    assert o in s, o
    return s.replace(o, n, 1)

p = 'all8.py'
s = open(p).read()
# calmer lamp on the desk
s = rep(s, '<circle cx="476" cy="574" r="200" fill="#ffe6da" opacity=".34" filter="url(#haze)" style="mix-blend-mode:screen"/><circle cx="300" cy="380" r="260" fill="#ffe2d4" opacity=".16" filter="url(#haze)" style="mix-blend-mode:screen"/>',
        '<circle cx="476" cy="574" r="110" fill="#ffe6da" opacity=".22" filter="url(#haze)" style="mix-blend-mode:screen"/>')
s = rep(s, '<path d="M452,580 L500,568 L300,700 L150,700 Z" fill="url(#monBeam)" filter="url(#haze)" style="mix-blend-mode:screen" transform="rotate(0)"/>',
        '<path d="M452,580 L500,568 L300,700 L150,700 Z" fill="url(#monBeam)" opacity=".55" filter="url(#haze)" style="mix-blend-mode:screen"/>')
# darker desk + soft key light on her face (drawn over her, under the notepad)
old_desk = '<rect x="0" y="690" width="540" height="270" fill="#2a1a2a"/><rect x="0" y="690" width="540" height="6" fill="#4a2e3a"/>\'+lamp'
new_desk = ('<circle cx="290" cy="260" r="150" fill="#ffe9dc" opacity=".30" filter="url(#haze)" style="mix-blend-mode:screen"/>'
            '<circle cx="290" cy="250" r="80" fill="#fff2ea" opacity=".18" filter="url(#haze)" style="mix-blend-mode:screen"/>'
            '<rect x="0" y="690" width="540" height="270" fill="#21152a"/><rect x="0" y="690" width="540" height="6" fill="#3a2634"/>\'+lamp')
s = rep(s, old_desk, new_desk)
s = rep(s, "s4+=dust(31,(200,520,500,690),18)", "s4+=dust(31,(330,200,520,560),18)")
open(p, 'w').write(s)
print('patched')
