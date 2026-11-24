"""คลิปร่างตอน "ถ้าฮอกวอตส์มาเปิดสาขาที่ไทย" (บท v10)
- เสียงพากย์ชั่วคราว: espeak-ng ภาษาไทย ปรับระดับเสียง/ความเร็วต่อตัวละคร (ไม่ใช้เครดิต ElevenLabs)
- จัดเวลาแต่ละช็อตตามความยาวเสียง (ไม่สั้นกว่าเวลาในบท)
- ดนตรีและเสียงประกอบสร้างด้วยตัวเลข ย่านเสียงกลาง ดนตรีเบากว่าเสียงพูดราว 9 dB
- ภาพนิ่งแต่ละช็อตซูมช้า ๆ ซับ/กราฟิกค่อย ๆ ขึ้น ตัดแบบภาพจางซ้อน · เข้าโลกเวทมนตร์ใช้ซูมเบลอ · กล้องสั่นตอนไก่ขัน
- การ์ดโหวตไฮไลต์วน A B C D พร้อมเสียงคลิก · ต่อท้ายด้วยโลโก้ปิดท้ายของช่อง
ได้ไฟล์ out/clip_draft.mp4 1080x1920 30fps"""
import re, os, json, subprocess, pathlib, wave
import numpy as np

HERE = pathlib.Path(__file__).parent
EP = HERE.parent
OUTRO = EP.parent.parent / "pipeline" / "v2" / "outro.mp4"
SR, FPS, XF = 48000, 30, 0.3
os.chdir(HERE)
for d in ("vo", "seg", "out"):
    os.makedirs(d, exist_ok=True)

# ---------- 1. แผนเสียงพากย์จาก script.md ----------
VOICES = {  # espeak-ng: variant, pitch, speed
    "ซิ่ง": ("th+m3", 52, 265), "อาม้า": ("th+f2", 64, 250), "ลุงเปี๊ยก": ("th+m7", 34, 262),
    "ลุงโต": ("th+m1", 18, 230), "ป้าแต๋ว": ("th+f4", 72, 275), "ต้น": ("th+m4", 50, 258),
    "เดรโก": ("th+m2", 62, 255), "หมวก": ("th+croak", 26, 228), "ไก่": ("th+m2", 80, 260),
}
def who_of(s):
    s = s.replace("หมวกคัดสรร", "หมวก")
    for k in VOICES:
        if k in s:
            return k
    return None

shots = []
for line in (EP / "script.md").read_text().splitlines():
    if not re.match(r"^\| \d+ \|", line):
        continue
    c = [x.strip() for x in line.strip("|").split("|")]
    n, dur, spk, th = int(c[0]), float(c[1]), c[2], c[3]
    turns = []
    parts = [p.strip() for p in th.split("·")]
    for p in parts:
        m = re.match(r"^\(([^)]+)\)\s*(.+)$", p)
        if m and who_of(m.group(1)):
            turns.append((who_of(m.group(1)), m.group(2)))
        else:
            txt = re.sub(r"\([^)]*\)", "", p).strip()
            if txt:
                turns.append((who_of(spk.split("→")[0]) or "ซิ่ง", txt))
    shots.append(dict(n=n, dur=dur, turns=turns))

def read_wav(path):
    with wave.open(str(path)) as w:
        sr, ch, raw = w.getframerate(), w.getnchannels(), w.readframes(w.getnframes())
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    if ch == 2:
        x = x.reshape(-1, 2).mean(1)
    if sr != SR:
        t = np.arange(int(len(x) * SR / sr)) * sr / SR
        x = np.interp(t, np.arange(len(x)), x)
    return x.astype(np.float32)

def say(key, who, text):
    el = HERE / "vo_fast" / f"{key}.wav"
    if el.exists():
        x = read_wav(el); nz = np.where(np.abs(x) > 0.012)[0]
        x = x[max(0, nz[0] - 800):nz[-1] + 2400] if len(nz) else x
        return x / (np.abs(x).max() + 1e-6) * 0.8
    v, p, s = VOICES[who]
    clean = re.sub(r"[“”\"!?]", "", text).replace("…", ", ")
    path = HERE / "vo" / f"{key}.wav"
    subprocess.run(["espeak-ng", "-v", v, "-p", str(p), "-s", str(s), "-w", str(path), clean], check=True)
    x = read_wav(path)
    nz = np.where(np.abs(x) > 0.01)[0]
    x = x[nz[0]:nz[-1] + 1] if len(nz) else x
    return x / (np.abs(x).max() + 1e-6) * 0.8

# ---------- 2. จัดเวลา ----------
t = 0.0; plan = []
for sh in shots:
    clips = []; cur = 0.25
    for i, (who, text) in enumerate(sh["turns"]):
        a = say(f"s{sh['n']:02d}_{i}", who, text)
        clips.append(dict(who=who, text=text, at=cur, len=len(a) / SR, audio=a))
        cur += len(a) / SR + 0.06
    d = max(sh["dur"] * 0.7, cur + 0.35)
    if sh["n"] == 2:                               # ให้มีเวลาไก่ขันแล้วซิ่งล้ม
        d = max(d, cur + 1.9)
    if sh["n"] == len(shots):
        d += 1.2                                   # ค้างการ์ดโหวตให้ตัดสินใจ
    plan.append(dict(n=sh["n"], start=t, dur=round(d, 2), clips=clips))
    t += d - XF
TOTAL = t + XF
N = int(TOTAL * SR) + SR

# ---------- 3. เสียง ----------
def env(n, a=0.005, r=0.2):
    e = np.ones(n, np.float32); ai, ri = int(a * SR), int(r * SR)
    e[:ai] = np.linspace(0, 1, ai); e[-ri:] *= np.linspace(1, 0, ri); return e
def tone(f, d, kind="sine", dec=3.0):
    x = np.arange(int(d * SR)) / SR
    if kind == "pluck":
        s = np.sin(2*np.pi*f*x) + .4*np.sin(4*np.pi*f*x)*np.exp(-x*6) + .15*np.sin(6*np.pi*f*x)*np.exp(-x*9)
    elif kind == "saw":
        s = 2 * ((f * x) % 1) - 1
    else:
        s = np.sin(2*np.pi*f*x)
    return (s * np.exp(-x * dec) * env(len(x), .004, .05)).astype(np.float32)
def add(buf, x, at, g=1.0):
    i = int(at * SR); j = min(len(buf), i + len(x))
    if i < len(buf): buf[i:j] += x[:j - i] * g

voice = np.zeros(N, np.float32)
for sh in plan:
    for c in sh["clips"]:
        add(voice, c["audio"], sh["start"] + c["at"])

# ดนตรี: สนุก ม่วน ๆ · ช่วงกรุงเทพจังหวะเด้ง (ช็อต 1-7) · ตลาดเวทมนตร์มีระฆัง (9-10)
# ช่วงต้น (11-13) เป็นลายอีสาน: แคนเสียงยืน + พิณดีดรัว + กลองตุ๊บ ๆ + ฉิ่งฉับ · ลุ้น (14) แล้วหยุดก่อน "เช็กเกลียว"
music = np.zeros(N, np.float32)
def noise_hit(d, dec, g):
    n = int(d * SR); return (np.random.randn(n) * np.exp(-np.arange(n) / SR * dec) * g).astype(np.float32)
def kick(at): x = np.arange(int(.22*SR))/SR; add(music, (np.sin(2*np.pi*(150*np.exp(-x*18)+70)*x)*np.exp(-x*14)).astype(np.float32), at, .55)
def snare(at): add(music, noise_hit(.16, 28, .28), at); add(music, tone(330, .12, "sine", 25), at, .2)
def hat(at, g=.07): y = noise_hit(.04, 120, g); add(music, y - np.concatenate([[0], y[:-1]]), at)
def thai_comic(t0, t1, bpm=132, root=1.0, light=False):
    """เพลงตลกแบบไทย: ระนาดเดินทำนองตีคู่แปด เบสเด้งแบบอุ้มปา ฉิ่งฉับ กลองโทน และแคนกระแทกเป็นช่วง ๆ"""
    b = 60 / bpm; k = 0; tt = t0
    pent = [1, 9/8, 5/4, 3/2, 5/3, 2, 9/4]
    mel = [4, 3, 2, 3, 4, 5, 4, 2, 1, 2, 3, 2, 1, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 4, 2, 1, 0, 1, 2, 3, 2, 0]
    def ranat(f, at, g):
        x = np.arange(int(.22 * SR)) / SR
        y = (np.sin(2*np.pi*f*x) + .35*np.sin(2*np.pi*3.98*f*x)*np.exp(-x*30)) * np.exp(-x*14) * env(len(x), .002, .03)
        add(music, y.astype(np.float32), at, g)
    while tt < t1:
        bass = C/2*root * (1 if k % 2 == 0 else 3/2)
        add(music, tone(bass, .28, "pluck", 9), tt, .55 if not light else .35)          # เบสอุ้มปา
        add(music, tone(bass*2, .12, "pluck", 18), tt + b/2, .18)
        for sub in range(2):                                                             # ระนาดตีคู่แปด
            n = mel[(k*2 + sub) % len(mel)]; f = C*2*root*pent[n]
            ranat(f, tt + sub*b/2, .26 if not light else .16); ranat(f*2, tt + sub*b/2 + .012, .1)
        if k % 2 == 0: add(music, tone(3520, .4, "sine", 7), tt, .09)                    # ฉิ่ง
        else: add(music, noise_hit(.05, 70, .13), tt)                                    # ฉับ
        if not light:
            if k % 4 == 0: add(music, tone(140, .2, "sine", 16), tt, .5)                 # กลองโทน ตุ๊บ
            if k % 4 == 2: add(music, tone(230, .1, "sine", 26), tt + b/2, .35)          # ป๊ะ
        if k % 8 == 3 and not light:                                                     # แคนกระแทก
            xx = np.arange(int(.45*SR))/SR
            for ff in (C*root, C*root*3/2, C*2*root):
                ph = 2*np.pi*ff*xx + .25*np.sin(2*np.pi*6*xx)
                add(music, ((np.sign(np.sin(ph))*.3 + np.sin(ph)*.7)*env(len(xx), .02, .15)).astype(np.float32), tt + b/2, .07)
        tt += b; k += 1

def groove(t0, t1, bpm=124, root=1.0, bells=False, light=False):
    b = 60 / bpm; k = 0; tt = t0
    prog = [1, 4/3, 3/2, 4/3]
    mel = [5, 3, 2, 3, 1, 2, 3, 5, 6, 5, 3, 2, 1, 2, 3, 1]
    deg = {1: 1, 2: 9/8, 3: 5/4, 5: 3/2, 6: 5/3}
    while tt < t1:
        ch = prog[(k // 8) % 4] * root
        if not light:
            if k % 2 == 0: kick(tt)
            if k % 4 == 2: snare(tt)
        hat(tt + b/2, .05 if light else .07)
        add(music, tone(C/2*ch, .3, "pluck", 9), tt, .55)                               # เบสเด้ง
        add(music, tone(C/2*ch*1.5, .2, "pluck", 12), tt + b/2, .3)
        if k % 2 == 1:                                                                   # คอร์ดตบจังหวะยก
            for r in (1, 5/4, 3/2): add(music, tone(C*ch*r, .18, "pluck", 14), tt + b/2, .12)
        add(music, tone(C*2*deg[mel[k % 16]]*root, .28, "pluck", 8), tt, .22 if k % 2 == 0 else .14)   # ทำนอง
        if bells and k % 4 == 0: add(music, tone(C*4*deg[mel[k % 16]], 1.0, "sine", 3), tt, .1)
        tt += b; k += 1
def isan(t0, t1, bpm=138):
    b = 60 / bpm; A = 220.0
    pent = [1, 6/5, 4/3, 3/2, 9/5, 2]                       # A C D E G A (ลายอีสาน)
    # แคน: เสียงยืนลิ้นหลายลูก สั่นเบา ๆ
    x = np.arange(int((t1 - t0) * SR)) / SR
    khaen = np.zeros(len(x), np.float32)
    for f, g in ((A, .5), (A*3/2, .35), (A*2, .3), (A*2*6/5, .18)):
        ph = 2*np.pi*f*x + .3*np.sin(2*np.pi*5.5*x)
        khaen += (np.sign(np.sin(ph)) * .35 + np.sin(ph) * .65).astype(np.float32) * g
    khaen *= (1 + .25*np.sin(2*np.pi*2.3*x)) * .22
    khaen[:int(.4*SR)] *= np.linspace(0, 1, int(.4*SR)); khaen[-int(.3*SR):] *= np.linspace(1, 0, int(.3*SR))
    add(music, khaen, t0)
    riff = [0, 2, 3, 2, 0, 2, 3, 4, 3, 2, 0, 1, 0, 2, 0, 3]
    k = 0; tt = t0
    while tt < t1:
        for sub in range(2):                                 # พิณดีดรัว (โน้ตละครึ่งจังหวะ)
            n = riff[(k * 2 + sub) % 16]; f = A * 2 * pent[n]
            add(music, tone(f, .22, "pluck", 11), tt + sub*b/2, .26); add(music, tone(f*2, .15, "pluck", 16), tt + sub*b/2, .1)
        if k % 2 == 0: kick(tt)                              # กลองหาง ตุ๊บ
        else: add(music, tone(180, .12, "sine", 20), tt, .35)
        if k % 2 == 0: add(music, tone(3520, .5, "sine", 6), tt, .1); add(music, tone(4180, .4, "sine", 8), tt, .05)   # ฉิ่ง
        else: add(music, noise_hit(.06, 60, .14), tt)                                                   # ฉับ
        tt += b; k += 1
s = {p["n"]: p for p in plan}
C = 261.6
# ===== เรียบเรียงให้มีน้ำหนัก ขึ้นลง: เกริ่น → เต็มวง → เบรก → ไต่ขึ้น → กระแทก → หยุดรับมุก =====
def kick2(at, g=.9):
    x = np.arange(int(.3*SR))/SR
    y = np.sin(2*np.pi*(170*np.exp(-x*22)+58)*x)*np.exp(-x*9) + np.sin(2*np.pi*120*x)*np.exp(-x*20)*.5
    add(music, y.astype(np.float32), at, g); add(music, noise_hit(.012, 300, .25), at)          # คลิกให้ได้ยินในลำโพงมือถือ
def snare2(at, g=.5):
    add(music, noise_hit(.22, 22, g), at); add(music, tone(200, .14, "sine", 22), at, g*.7); add(music, tone(330, .1, "sine", 30), at, g*.4)
def crash(at, g=.35):
    n = int(1.6*SR); y = np.random.randn(n).astype(np.float32); y = y - np.concatenate([[0], y[:-1]])
    add(music, (y*np.exp(-np.arange(n)/SR*2.6)*g*.6).astype(np.float32), at); kick2(at, 1.0)
def impact(at):
    x = np.arange(int(1.0*SR))/SR; add(music, (np.sin(2*np.pi*(90*np.exp(-x*4)+45)*x)*np.exp(-x*3)).astype(np.float32), at, .9); crash(at, .3)
def riser(t0, t1, g=.25):
    n = int((t1-t0)*SR); x = np.arange(n)/SR; r = np.linspace(0, 1, n)
    y = np.random.randn(n).astype(np.float32); y = y - np.concatenate([[0], y[:-1]])
    tonal = np.sin(2*np.pi*np.cumsum(300 + 900*r**2)/SR)
    add(music, ((y*.5 + tonal*.4)*r**2*g).astype(np.float32), t0)
def drums(t0, t1, bpm, level, fill=False):
    b = 60/bpm; k = 0; tt = t0
    while tt < t1 - 1e-3:
        bt = k % 4
        if level >= 3:
            if bt in (0, 2): kick2(tt)
            if bt == 2: kick2(tt + b*.75, .6)
            if bt in (1, 3): snare2(tt)
            for q in range(2): hat(tt + q*b/2, .09 if q else .05)
            if bt == 3: hat(tt + b*.75, .12)
        elif level == 2:
            if bt == 0: kick2(tt, .75)
            if bt == 2: kick2(tt, .55)
            if bt == 3: snare2(tt, .3)
            hat(tt + b/2, .07)
        else:
            hat(tt + b/2, .04)
        tt += b; k += 1
    if fill:                                                     # กลองรัวก่อนขึ้นขั้นใหม่
        n = 8
        for i in range(n):
            snare2(t1 - b*2 + i*b/4, .18 + .32*i/n)
def stopgate(t, dur=.75):                                        # หยุดดนตรีรับมุก แล้วค่อยกลับมา
    i0, i1 = int(t*SR), int((t+dur)*SR); f = int(.04*SR); r = int(.25*SR)
    g = np.ones(N, np.float32); g[i0:i1] = 0
    g[max(0, i0-f):i0] = np.linspace(1, 0, min(f, i0)); g[i1:i1+r] = np.linspace(0, 1, len(g[i1:i1+r]))
    return g

S = lambda n: s[n]["start"]
_rooster = S(2) + next(c["at"] for c in s[2]["clips"] if c["who"] == "ไก่")
def endof(n): c = s[n]["clips"][-1]; return S(n) + c["at"] + c["len"]

# ===== แต่ละช่วงมีเพลงของตัวเอง (ไม่ใช่ลูปเดียวทั้งคลิป) =====
MAJ = [1, 9/8, 5/4, 3/2, 5/3, 2, 9/4, 5/2]                    # เพนทาโทนิกเมเจอร์ (ไทย)
MIN = [1, 6/5, 4/3, 3/2, 9/5, 2, 12/5, 8/3]                    # เพนทาโทนิกไมเนอร์ (อีสาน/ลึกลับ)
def inst_ranat(f, d, g, at):
    x = np.arange(int(min(d, .3)*SR))/SR
    y = (np.sin(2*np.pi*f*x) + .35*np.sin(2*np.pi*3.98*f*x)*np.exp(-x*30))*np.exp(-x*13)*env(len(x), .002, .03)
    add(music, y.astype(np.float32), at, g); add(music, y.astype(np.float32), at + .012, g*.35)
def inst_phin(f, d, g, at):
    x = np.arange(int(min(d, .4)*SR))/SR
    y = (np.sin(2*np.pi*f*x) + .5*np.sin(4*np.pi*f*x)*np.exp(-x*8) + .3*np.sin(6*np.pi*f*x)*np.exp(-x*14))*np.exp(-x*7)*env(len(x), .002, .04)
    add(music, y.astype(np.float32), at, g)
def inst_khaen(f, d, g, at):
    x = np.arange(int(d*SR))/SR
    y = 0
    for r, gg in ((1, 1), (3/2, .6), (2, .5)):
        ph = 2*np.pi*f*r*x + .25*np.sin(2*np.pi*6*x); y = y + (np.sign(np.sin(ph))*.3 + np.sin(ph)*.7)*gg
    add(music, (y*env(len(x), .03, min(.15, d*.4))).astype(np.float32), at, g*.45)
def inst_bell(f, d, g, at):
    x = np.arange(int(1.2*SR))/SR
    add(music, ((np.sin(2*np.pi*f*x) + .4*np.sin(2*np.pi*2.76*f*x)*np.exp(-x*4))*np.exp(-x*3.2)).astype(np.float32), at, g)
def inst_horn(f, d, g, at):
    x = np.arange(int(min(d, .25)*SR))/SR; y = 0
    for r in (1, 5/4, 3/2):
        y = y + (2*((f*r*x) % 1) - 1)
    add(music, (y/3*env(len(x), .01, .06)).astype(np.float32), at, g)
def seq(t0, t1, bpm, notes, inst, g, base, scale=MAJ, loop=True):
    """notes = [(ดีกรี หรือ None, จังหวะ), ...] วนจนจบช่วง"""
    b = 60/bpm; tt = t0; i = 0
    while tt < t1 - 1e-3:
        deg, beats = notes[i % len(notes)]
        if deg is not None:
            oct_, d_ = divmod(deg, len(scale) - 3) if deg >= 0 else (0, deg)
            inst(base * scale[deg] if deg < len(scale) else base * 2 * scale[deg - 5], beats*b, g, tt)
        tt += beats*b; i += 1
        if not loop and i >= len(notes): break
def bass(t0, t1, bpm, pattern, base, g=.55, scale=MAJ):
    b = 60/bpm; tt = t0; i = 0
    while tt < t1 - 1e-3:
        deg, beats = pattern[i % len(pattern)]
        if deg is not None: add(music, tone(base*scale[deg], min(.35, beats*b), "pluck", 8), tt, g)
        tt += beats*b; i += 1
def pad(t0, t1, freqs, g=.12):
    n = int((t1-t0)*SR); x = np.arange(n)/SR; y = sum(np.sin(2*np.pi*f*x + .3*np.sin(2*np.pi*.3*x)) for f in freqs)
    e = np.minimum(1, np.minimum(x/1.0, (x[-1]-x)/0.6 + 1e-3)); add(music, (y*e*g/len(freqs)).astype(np.float32), t0)
def chingchab(t0, t1, bpm, g=1.0):
    b = 60/bpm; tt = t0; k = 0
    while tt < t1 - 1e-3:
        if k % 2 == 0: add(music, tone(3520, .4, "sine", 7), tt, .08*g)
        else: add(music, noise_hit(.05, 70, .12*g), tt)
        tt += b; k += 1

# ท่อนฮุก (จำง่าย): ซล ลา ซล มี | เร มี ซล - | ลา โด' ลา ซล | มี เร โด -
HOOK = [(3, .5), (4, .5), (3, .5), (2, .5), (1, .5), (2, .5), (3, 1), (4, .5), (5, .5), (4, .5), (3, .5), (2, .5), (1, .5), (0, 1)]
HOOK_ISAN = [(3, .5), (4, .5), (3, .5), (1, .5), (0, .5), (1, .5), (3, 1), (4, .5), (5, .5), (4, .5), (3, .5), (1, .5), (0, .5), (0, 1)]

# 1) เปิดเรื่อง: ท่อนฮุกระนาดเดี่ยว แล้วไต่ขึ้น
seq(0, S(2), 128, HOOK, inst_ranat, .3, C*2); chingchab(0, S(2), 128, .6); riser(S(2) - 1.4, S(2))
# 2) ขั้น 1 ห้องนอน: เด้งดึ๋ง ถามตอบ (ระนาดถาม แคนตอบ) เบสอุ้มปา
crash(S(2))
VERSE = [(0, .5), (None, .5), (2, .5), (None, .5), (4, .25), (3, .25), (2, .5), (None, 1), (5, .5), (None, .5), (4, .5), (2, .5), (3, 1), (None, 1)]
seq(S(2), S(4), 132, VERSE, inst_ranat, .28, C*2)
seq(S(2), S(4), 132, [(None, 3), (4, .5), (3, .5), (None, 3), (1, .5), (0, .5)], inst_khaen, .5, C)
bass(S(2), S(4), 132, [(0, 1), (3, 1)], C/2); chingchab(S(2), S(4), 132); drums(S(2), S(3), 132, 3); drums(S(3), S(4), 132, 2, fill=True)
# 3) ขั้น 2 ตุ๊กตุ๊ก: ท่อนซิ่ง เร็ว เบสวิ่ง เครื่องเป่าตบ
crash(S(4))
ROAD = [(0, .25), (1, .25), (2, .25), (3, .25), (4, .5), (3, .5), (5, .25), (4, .25), (3, .25), (2, .25), (1, .5), (2, .5)]
seq(S(4), S(6), 150, ROAD, inst_ranat, .24, C*2*9/8)
seq(S(4), S(6), 150, [(None, .5), (0, .5), (None, .5), (0, .5), (None, .5), (3, .5), (None, .5), (3, .5)], inst_horn, .16, C*9/8)
bass(S(4), S(6), 150, [(0, .5), (0, .5), (5, .5), (0, .5), (3, .5), (3, .5), (4, .5), (3, .5)], C/2*9/8, .5)
drums(S(4), S(6), 150, 3)
# 4) ศาลพระภูมิ: ลึกลับ ช้า ระฆัง ไม่มีกลอง แล้วไต่ขึ้นเข้าวูบ
pad(S(6), S(7), [220, 261.6, 329.6], .16)
seq(S(6), S(7), 84, [(0, 1), (2, 1), (4, 1.5), (3, .5), (1, 2)], inst_bell, .16, 440, MIN)
riser(S(7) - 1.6, S(7), .3); impact(S(7))
# 5) ขั้น 3 ตลาดเวทมนตร์: สามช่า ระฆังแก้วไล่โน้ต เบสดีด
crash(S(8))
seq(S(8), S(10), 126, [(0, 1/3), (2, 1/3), (4, 1/3), (5, 1/3), (4, 1/3), (2, 1/3), (1, 1/3), (3, 1/3), (5, 1/3), (6, 1/3), (5, 1/3), (3, 1/3)], inst_bell, .1, C*2*4/3)
seq(S(8), S(10), 126, [(4, 1), (None, .5), (3, .5), (2, 1), (None, 1), (5, 1), (4, .5), (3, .5), (2, 2)], inst_ranat, .22, C*2*4/3)
bass(S(8), S(10), 126, [(0, 1), (2, 1/3), (None, 2/3), (3, 1), (None, 1)], C/2*4/3, .5)
drums(S(8), S(10), 126, 2, fill=True)
# 6) ขั้น 4 ต้นมา: แคนกับพิณเกริ่นลายอีสาน
crash(S(10))
pad(S(10), S(11), [220, 330], .1)
seq(S(10), S(11), 138, [(0, .5), (2, .5), (3, .5), (2, .5), (0, .5), (2, .5), (3, .5), (4, .5)], inst_phin, .26, 440, MIN)
seq(S(10), S(11), 138, [(0, 2), (3, 2)], inst_khaen, .5, 220, MIN); chingchab(S(10), S(11), 138); drums(S(10), S(11), 138, 2, fill=True)
# 7) ฉากหมอลำ: ท่อนฮุกเวอร์ชันหมอลำ เต็มวง หนักสุด
crash(S(11))
seq(S(11), S(12), 140, HOOK_ISAN, inst_phin, .32, 440, MIN)
seq(S(11), S(12), 140, HOOK_ISAN, inst_khaen, .45, 220, MIN)
bass(S(11), S(12), 140, [(0, .5), (0, .5), (3, .5), (0, .5)], 110, .6, MIN); chingchab(S(11), S(12), 140, 1.2); drums(S(11), S(12), 140, 3, fill=True)
# 8) ขั้น 5 ต้นคัดบ้าน: อีสานเบาลง
crash(S(12))
seq(S(12), S(13), 132, [(0, .5), (2, .5), (3, .5), (2, .5)], inst_phin, .2, 440, MIN); seq(S(12), S(13), 132, [(0, 4)], inst_khaen, .4, 220, MIN)
drums(S(12), S(13), 132, 2)
# 9) ซิ่งคัดบ้าน: กลองรัวลุ้น โน้ตไต่ขึ้น แล้วหยุดเงียบรับมุก
cut13 = endof(13)
roll_end = S(13) + s[13]["clips"][-1]["at"]
tt = S(13)
while tt < roll_end - .05:
    snare2(tt, .1 + .3*min(1, (tt-S(13))/max(.1, roll_end-S(13)))); tt += .09
for i, f in enumerate([C, C*9/8, C*5/4, C*4/3, C*3/2, C*5/3]):
    a_ = S(13) + i*.4
    if a_ < roll_end: add(music, tone(f, 0.7, "saw", 1.6) * 0.2, a_, .35)
# 10) การ์ดโหวต: ท่อนฮุกกลับมา ปิดด้วยกระแทก
seq(S(14) + .2, TOTAL - .4, 124, HOOK, inst_ranat, .28, C*2); bass(S(14) + .2, TOTAL - .4, 124, [(0, 1), (3, 1)], C/2, .4)
chingchab(S(14) + .2, TOTAL - .4, 124); drums(S(14) + .2, TOTAL - .4, 124, 2); crash(TOTAL - .35, .25)

# หยุดดนตรีตรงจังหวะมุก
for t_, d_ in [(_rooster, 1.0), (endof(5), .8), (endof(9), .8), (endof(12), .8), (cut13 - .05, 1.2)]:
    music *= stopgate(t_, d_)

# เสียงประกอบ
sfx = np.zeros(N, np.float32)
def crow(at):
    for k, (f0, f1, d) in enumerate([(520, 760, .18), (760, 900, .16), (900, 980, .34), (980, 620, .5)]):
        x = np.arange(int(d * SR)) / SR; f = np.linspace(f0, f1, len(x)) * (1 + .03*np.sin(2*np.pi*28*x))
        ph = 2*np.pi*np.cumsum(f)/SR; sig = sum(np.sin(ph*h)/h for h in range(1, 7))
        add(sfx, (sig*env(len(x), .01, .05)*.45).astype(np.float32), at + [0, .17, .32, .64][k])
def thud(at):
    x = np.arange(int(.4*SR))/SR; add(sfx, (np.sin(2*np.pi*120*x)*np.exp(-x*12) + np.random.randn(len(x))*.15*np.exp(-x*30)).astype(np.float32), at, .8)
def boing(at):
    x = np.arange(int(.7*SR))/SR; f = 220 + 140*np.sin(2*np.pi*7*x)*np.exp(-x*3)
    add(sfx, (np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*3)).astype(np.float32), at, .5)
def ding(at, f=1760):
    add(sfx, tone(f, 1.0, "sine", 4), at, .3); add(sfx, tone(f*1.5, .8, "sine", 5), at, .12)
def whoosh(at, d=1.1):
    n = int(d*SR); x = np.random.randn(n).astype(np.float32); y = np.zeros(n, np.float32); a = 0.0
    for i in range(n):
        k = .02 + .5*(i/n); a += k*(x[i]-a); y[i] = a
    add(sfx, y*np.sin(np.linspace(0, np.pi, n))*1.6, at)
def sparkle(at):
    for i, f in enumerate([2093, 2637, 3136, 3520]): add(sfx, tone(f, .5, "sine", 6), at + i*.07, .12)
def clack(at):
    for i in range(3): add(sfx, (np.random.randn(int(.03*SR))*np.exp(-np.arange(int(.03*SR))/SR*120)).astype(np.float32), at + i*.14, .5)
def khaen(at):
    for f in (392, 523.3, 587.3, 784):
        x = np.arange(int(.9*SR))/SR; add(sfx, ((2*((f*x) % 1)-1)*(1+.3*np.sin(2*np.pi*6*x))*env(len(x), .05, .3)).astype(np.float32), at, .06)
def click(at):
    add(sfx, tone(2400, .05, "sine", 60), at, .35)

_cr = s[2]["start"] + next(c["at"] for c in s[2]["clips"] if c["who"] == "ไก่")   # เสียงคนร้อง "เอ้กอี๊เอ้ก" อยู่ในเสียงพากย์แล้ว
thud(_cr + .38)
for k in range(5): add(sfx, (np.random.randn(int(.04*SR))*np.exp(-np.arange(int(.04*SR))/SR*60)).astype(np.float32), _cr + .42 + k*.08, .35)   # ปีกตีพั่บ ๆ
thud(_cr + .86)
def slide(at, f0, f1, d=.6, g=.35):                               # นกหวีดสไลด์ (เสียงตลก)
    x = np.arange(int(d*SR))/SR; f = np.geomspace(f0, f1, len(x)) * (1 + .02*np.sin(2*np.pi*7*x))
    add(sfx, (np.sin(2*np.pi*np.cumsum(f)/SR)*env(len(x), .02, .08)).astype(np.float32), at, g)
def tung(at):                                                      # "ตึ่ง ตึ่ง" หลังมุก
    for k_, f in enumerate((196, 147)):
        x = np.arange(int(.3*SR))/SR; y = (np.sign(np.sin(2*np.pi*f*x))*.4 + np.sin(2*np.pi*f*x)*.6)*np.exp(-x*7)*env(len(x), .005, .05)
        add(sfx, y.astype(np.float32), at + k_*.28, .3)
def end_of(n, i=-1): c = s[n]["clips"][i]; return s[n]["start"] + c["at"] + c["len"]
slide(_cr + .3, 1400, 320, .5)                                      # ซิ่งล้ม
tung(end_of(5) + .1)                                                # ลุงเปี๊ยก คิดสองที่
slide(s[7]["start"] - .3, 300, 1500, .7)                            # ดูดเข้าศาล
tung(end_of(9) + .1)                                                # ไม้ลูกชิ้น
tung(end_of(12) + .05)                                              # ตำปลาแดก
tung(end_of(13) + .1)                                               # เกรดหนึ่งจุดห้า
for i in range(3): add(sfx, tone(1500 + 300*i, .3, "sine", 8), s[3]["start"] + .3 + i*.12, .12)
boing(s[4]["start"] + s[4]["clips"][-1]["at"] + 1.2); ding(s[5]["start"] + .5, 2200)
whoosh(s[7]["start"] - .4, 1.3)
sparkle(s[9]["start"] + .3); clack(s[9]["start"] + s[9]["dur"] - 1.0)
khaen(s[10]["start"] + .1)
for st in (2, 4, 8, 10, 12):                                   # ป๊อปตอนขึ้นขั้นใหม่
    add(sfx, tone(880, .12, "sine", 18), s[st]["start"] + .05, .35); add(sfx, tone(1320, .15, "sine", 14), s[st]["start"] + .12, .3)
VOTE_STEP = 0.75
for i in range(int((s[14]["dur"] - .4) / VOTE_STEP)):
    click(s[14]["start"] + .3 + i * VOTE_STEP)

def rms(x):
    m = np.abs(x) > 1e-4; return float(np.sqrt(np.mean(x[m]**2))) if m.any() else 1e-6
music *= rms(voice) / rms(music) * 10**(-8.0/20)                  # ดนตรีเบากว่าเสียงพูด 9 dB
act = np.convolve((np.abs(voice) > .02).astype(np.float32), np.ones(int(.25*SR))/int(.25*SR), "same")
music *= 1 - .35*np.clip(act*3, 0, 1)                           # หลบเสียงพูดเพิ่มอีกนิด
mix = voice + music + sfx * .8
mix = mix[:int(TOTAL*SR)]
mix = mix / (np.abs(mix).max() + 1e-6) * .89
pcm = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open("out/mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

if os.environ.get("AUDIO_ONLY"):
    json.dump([dict(n=p["n"], start=round(p["start"], 2), dur=p["dur"], lines=[(c["who"], c["text"], round(c["at"], 2), round(c["len"], 2)) for c in p["clips"]]) for p in plan], open("out/timeline.json", "w"), ensure_ascii=False, indent=1)
    print("audio only, TOTAL", round(TOTAL, 2)); raise SystemExit

# ---------- 4. ภาพ ----------
def run(cmd):
    subprocess.run(cmd, check=True)
segs = []
for p in plan:
    n, d = p["n"], p["dur"]; fr = int(round(d * FPS)); seg = f"seg/s{n:02d}.mp4"
    zin = n % 2 == 1
    z = f"1+0.05*on/{fr}" if zin else f"1.05-0.05*on/{fr}"
    sx = sy = ""
    if n == 2:                                                  # กล้องสั่นตอนไก่ขัน
        c0 = p["clips"][0]; a0 = int((c0["at"] + c0["len"]) * FPS); a1 = a0 + int(.5*FPS)
        sx = f"+if(between(on,{a0},{a1}),18*sin(on*2.3),0)"; sy = f"+if(between(on,{a0},{a1}),14*cos(on*3.1),0)"
    if n == len(plan):                                          # การ์ดโหวต: ไฮไลต์วน
        lst = HERE / "seg" / "vote.txt"
        k = int(d / VOTE_STEP) + 1
        lst.write_text("".join(f"file '{HERE}/frames/v{i % 4}.png'\nduration {VOTE_STEP}\n" for i in range(k)) + f"file '{HERE}/frames/v{(k-1) % 4}.png'\n")
        base = ["-f", "concat", "-safe", "0", "-i", str(lst)]
        vf = f"[0:v]fps={FPS},scale=1080:1920,setsar=1[bg];[1:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[ov];[bg][ov]overlay=0:0,format=yuv420p[v]"
    else:
        base = ["-loop", "1", "-t", str(d), "-i", f"frames/b{n:02d}.png"]
        vf = (f"[0:v]scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2){sx}':y='ih/2-(ih/zoom/2){sy}':d={fr}:s=1080x1920:fps={FPS}[bg];"
              f"[1:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[ov];[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]")
    run(["ffmpeg", "-y", "-loglevel", "error"] + base + ["-loop", "1", "-t", str(d), "-i", f"frames/o{n:02d}.png",
         "-filter_complex", vf, "-map", "[v]", "-t", str(d), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", seg])
    segs.append(seg); print("segment", n, d, flush=True)

inputs = sum((["-i", f] for f in segs), [])
fc = ""; prev = "[0:v]"; tt = plan[0]["dur"]
for i in range(1, len(segs)):
    trans = "zoomin" if plan[i]["n"] == 7 else "fade"
    xd = .45 if trans == "zoomin" else XF
    off = tt - xd
    fc += f"{prev}[{i}:v]xfade=transition={trans}:duration={xd}:offset={off:.3f}[x{i}];"
    prev = f"[x{i}]"; tt = off + plan[i]["dur"]
GRADE = "eq=contrast=1.04:saturation=1.06:gamma=1.02,noise=c0s=5:c0f=t+u"
fc += f"{prev}{GRADE},format=yuv420p[v]"
run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-i", "out/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{len(segs)}:a",
     "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", "out/body.mp4"])

# ---------- 5. ต่อโลโก้ปิดท้าย ----------
run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/body.mp4", "-i", str(OUTRO), "-filter_complex",
     f"[1:v]fps={FPS},scale=1080:1920,setsar=1[ov];[1:a]aresample=48000[oa];[0:v]setsar=1[bv];[bv][0:a][ov][oa]concat=n=2:v=1:a=1[v][a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "160k",
     "-movflags", "+faststart", "out/clip_draft.mp4"])
json.dump([dict(n=p["n"], start=round(p["start"], 2), dur=p["dur"], lines=[(c["who"], c["text"], round(c["at"], 2), round(c["len"], 2)) for c in p["clips"]]) for p in plan],
          open("out/timeline.json", "w"), ensure_ascii=False, indent=1)
print("TOTAL body", round(TOTAL, 2))
