"""เพลงประกอบทั้งเรื่อง (สังเคราะห์เอง ไม่ใช้เครดิต) สร้างจากธีมเดียว: ทำนอง Bridal Chorus
ใช้ซ้ำแล้วเปลี่ยนไปตามสถานการณ์
  wedding   ออร์แกน Bridal Chorus เมเจอร์ (ใช้ของเดิมใน audiolib)
  intrude   ปังแล้วเงียบ ตามด้วยกล่องดนตรีเล่นธีมเดิมแบบไมเนอร์เพี้ยน ๆ กับเสียงสายต่ำ
  words     ธีมกล่องดนตรีต่อ + สายสั่นรัว (tremolo) + เสียงหัวใจเต้นเบา ๆ
  confront  สายดีดเป็นจังหวะเร่ง (ostinato) + กลองทิมปานีตอนเจ้าบ่าวชี้ + ธีมบนเชลโล
  reveal    ทุกอย่างหายเหลือไวโอลินเสียงสูงค้าง + ธีมเปียโนต่ำช้า ๆ
  dread     คอร์ดกระด้างค่อย ๆ ดังขึ้นจนจบ
cue(name, N, t0, t1) คืนสัญญาณ mono ของช่วงนั้น · build(N, marks) รวมทั้งเรื่อง"""
import numpy as np
import audiolib as A
SR = A.SR
rng = np.random.default_rng(11)
hz = A.hz

# ธีม: "Here comes the bride" ไมเนอร์ + ขั้นสองต่ำ (Db) ให้ดูผิดเพี้ยน  (โน้ต MIDI, จังหวะ)
THEME = [(67, 1), (72, .75), (72, .25), (72, 2), (67, 1), (73, .75), (71, .25), (72, 2),
         (67, 1), (72, 1), (77, .75), (77, .25), (75, 1), (74, .75), (72, .25), (71, 1), (72, .75), (73, .25), (72, 3)]

def _t(n): return np.arange(n) / SR
def fade(x, a=.05, r=.3):
    n = len(x); na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na: x[:na] *= np.linspace(0, 1, na)
    if nr: x[-nr:] *= np.linspace(1, 0, nr)
    return x

def musicbox(f, dur=2.2, v=1.0):
    n = int(dur * SR); t = _t(n); dt = 1 + rng.uniform(-.004, .004)   # เพี้ยนเล็กน้อยแบบกล่องดนตรีเก่า
    y = (np.sin(2 * np.pi * f * dt * t) * np.exp(-t * 2.2) + .45 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6)
         + .2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 11) + .15 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 4))
    y[:int(.002 * SR)] *= np.linspace(0, 1, int(.002 * SR))
    return (y * v * .25).astype(np.float32)

def strings(freqs, dur, v=1.0, att=1.2, rel=1.5, trem=0.0, bright=2200):
    """กลุ่มเครื่องสาย: saw หลายตัวเพี้ยนกันเล็กน้อย กรองความถี่สูง สั่นได้"""
    n = int(dur * SR); t = _t(n); y = np.zeros(n)
    for f in freqs:
        for d in (-.006, 0, .007):
            ff = f * (1 + d); ph = rng.uniform(0, 6.28); vib = 1 + .003 * np.sin(2 * np.pi * 5.3 * t + ph)
            for h in range(1, 14):
                if ff * h > 9000: break
                y += np.sin(2 * np.pi * ff * h * t * vib + ph * h) / h * (1 / (1 + (ff * h / bright) ** 2))
    y /= max(1, len(freqs) * 3)
    if trem: y *= .55 + .45 * np.abs(np.sin(np.pi * trem * t))
    e = np.ones(n); na, nr = min(n, int(att * SR)), min(n, int(rel * SR))
    e[:na] = np.linspace(0, 1, na) ** 1.5; e[-nr:] *= np.linspace(1, 0, nr)
    return (y * e * v * .12).astype(np.float32)

def pluck(f, dur=.5, v=1.0):
    n = int(dur * SR); t = _t(n); y = np.zeros(n)
    for h in range(1, 10): y += np.sin(2 * np.pi * f * h * t) / h * np.exp(-t * (5 + h * 2.5))
    return (y * v * .18).astype(np.float32)

def piano(f, dur=3.0, v=1.0):
    n = int(dur * SR); t = _t(n); y = np.zeros(n)
    for h, a in ((1, 1), (2, .5), (3, .25), (4, .12), (5, .06)): y += a * np.sin(2 * np.pi * f * h * (1 + .0004 * h * h) * t) * np.exp(-t * (1.1 + h * .7))
    y[:int(.004 * SR)] *= np.linspace(0, 1, int(.004 * SR))
    return (y * v * .2).astype(np.float32)

def timpani(f=55, v=1.0):
    n = int(2.5 * SR); t = _t(n)
    y = np.sin(2 * np.pi * f * (1 + .15 * np.exp(-t * 20)) * t) * np.exp(-t * 2) + .3 * A.lp(rng.standard_normal(n).astype(np.float32), 300) * np.exp(-t * 14)
    return (y * v * .5).astype(np.float32)

def heartbeat(N, t0, t1, bpm=62, v=1.0):
    out = np.zeros(N, np.float32); tt = t0
    while tt < t1:
        A.add(out, tt, timpani(48, .5 * v)[:int(.5 * SR)]); A.add(out, tt + .22, timpani(44, .35 * v)[:int(.5 * SR)]); tt += 60 / bpm
    return A.lp(out, 180)

def theme_on(inst, N, t0, t1, beat, transpose=0, v=1.0, dur=None):
    out = np.zeros(N, np.float32); tt = t0
    while tt < t1:
        for m, b in THEME:
            if tt >= t1: break
            A.add(out, tt, inst(hz(m + transpose), dur or max(1.2, b * beat * 2.2), v)); tt += b * beat
        tt += beat * 2
    return out

def build(N, M):
    """M = เวลาสำคัญ: bang, s5, s6, s6r, s7a, s7b, s8, s9, s9r, end"""
    mus = np.zeros(N, np.float32)
    def put(x, a, b, fi=.6, fo=1.2):
        """ใส่สัญญาณเฉพาะช่วง a..b แบบค่อย ๆ เข้า/ออก"""
        i0, i1 = int(a * SR), min(N, int(b * SR)); seg = x[i0:i1].copy()
        mus[i0:i1] += fade(seg, fi, fo)

    # intrude: ปังแล้วเงียบ 1.4 วิ ค่อยมีสายต่ำ C + กล่องดนตรีเล่นธีมไมเนอร์ช้า
    t_in = M['bang'] + 1.4
    low = np.zeros(N, np.float32); A.add(low, t_in, strings([hz(36), hz(43)], M['s7a'] - t_in + 1.5, 1.0, 2.5, 1.5, bright=900))
    put(low, t_in, M['s7a'] + 1.0, 2.0, 1.2)
    mb = theme_on(musicbox, N, t_in + 1.0, M['s7a'], .62, 0, 1.0)
    put(A.reverb(mb, 2.4, .45), t_in, M['s7a'] + .8, .3, 1.0)
    # words: สายสั่นรัวเสียงกลางเข้ามาเพิ่ม + หัวใจเต้น
    tr = np.zeros(N, np.float32); A.add(tr, M['s6'], strings([hz(60), hz(63), hz(66)], M['s7a'] - M['s6'] + 1, .8, 3.0, 1.0, trem=7))
    put(tr, M['s6'], M['s7a'] + .4, 1.5, .6)
    put(heartbeat(N, M['s6'] + 1.5, M['s7a'], 64, 1.0), M['s6'], M['s7a'] + .3, 1.0, .3)
    # confront: ostinato เร่ง 104 bpm (C C Db C) + ทิมปานีตอนชี้ + ธีมบนเชลโล
    ost = np.zeros(N, np.float32); beat = 60 / 104 / 2; tt = M['s7a'] + .5; pat = [36, 48, 36, 49, 36, 48, 36, 47]; k = 0
    while tt < M['s9']:
        acc = 1.2 if k % 4 == 0 else .8; A.add(ost, tt, pluck(hz(pat[k % 8]), .45, acc)); tt += beat; k += 1
    put(ost, M['s7a'] + .3, M['s9'] + .2, .4, .4)
    tp = np.zeros(N, np.float32); A.add(tp, M['s7a'] + .55, timpani(44, 1.2)); A.add(tp, M['s7b'] + 2.2, timpani(41, .9)); A.add(tp, M['s8'] + .2, timpani(44, .7))
    mus += tp
    cel = np.zeros(N, np.float32)
    for (m, b), tt in zip(THEME[:8], np.cumsum([0] + [b * .5 for _, b in THEME[:7]]) + M['s7b']):
        A.add(cel, tt, strings([hz(m - 24)], b * .5 + .4, .9, .08, .3, bright=1400))
    put(cel, M['s7b'], M['s9'], .2, .5)
    hi = np.zeros(N, np.float32); A.add(hi, M['s7a'], strings([hz(72), hz(73)], M['s9'] - M['s7a'] + 1, .45, 4, 1, trem=11, bright=4000))
    put(hi, M['s7a'], M['s9'] + .3, 3.0, .3)
    # reveal: ทุกอย่างหาย เหลือไวโอลินสูงค้าง + ธีมเปียโนต่ำช้า ๆ
    vl = np.zeros(N, np.float32); A.add(vl, M['s9'], strings([hz(84), hz(85)], M['end'] - M['s9'] + 1, .55, 1.5, 1, bright=5000))
    put(vl, M['s9'], M['end'], 1.0, .8)
    pn = theme_on(piano, N, M['s9'] + .3, M['s9r'], .9, -24, 1.4, 3.5)
    put(A.reverb(pn, 2.5, .4), M['s9'], M['s9r'] + 1.5, .1, 1.5)
    # dread: คอร์ดกระด้างดังขึ้นจนจบ
    cl = np.zeros(N, np.float32); A.add(cl, M['s9r'] - .3, strings([hz(48), hz(49), hz(55), hz(56), hz(61)], M['end'] - M['s9r'] + 1.2, 1.4, 2.4, .6, trem=13, bright=3000))
    put(cl, M['s9r'] - .3, M['end'], 1.5, .5)
    return A.reverb(mus, 1.8, .25)
