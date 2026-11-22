def rep(s, o, n):
    assert o in s, o[:90]
    return s.replace(o, n, 1)

p = 'all12.py'
s = open(p).read()
old = """sB += '<path d="M0,170 L60,170 L60,560 L0,560 Z" fill="#2e2228"/><path d="M0,182 L48,182 L48,560 L0,560 Z" fill="#fff0e4" opacity=".55"/>'
sB += '<path d="M48,300 L120,300 L420,960 L0,960 L0,560 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
sB += '<g filter="url(#tintNight)"><g transform="translate(36,300) scale(1.1)"><use href="#jhead"/></g></g><path d="M0,170 L18,170 L18,560 L0,560 Z" fill="#2e2228"/>'
"""
new = """sB += '<rect x="0" y="140" width="150" height="420" fill="#2e2228"/><rect x="0" y="152" width="136" height="408" fill="#6a5560"/><rect x="0" y="152" width="136" height="408" fill="#fff0e4" opacity=".45"/>'
sB += '<path d="M136,300 L200,300 L460,960 L0,960 L0,560 Z" fill="url(#spill)" filter="url(#haze)" style="mix-blend-mode:screen"/>'
sB += '<g filter="url(#tintNight)"><use href="#jbodyS" transform="translate(76,236) scale(0.65)"/></g>'
sB += '<rect x="136" y="140" width="14" height="420" fill="#2e2228"/><rect x="0" y="140" width="150" height="12" fill="#2e2228"/>'
"""
s = rep(s, old, new)
s = s.replace('เจมส์โผล่หน้าออกมาแอบดูจากประตูห้องนอนที่มีแสงลอดออกมา', 'เจมส์ยืนเต็มตัวอยู่ที่ประตูห้องนอน แอบมองแมวด้วยสีหน้ากังวล แสงจากห้องส่องออกมาด้านหลัง')
open(p, 'w').write(s)
print('patched')
