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
    "เดรโก": ("th+m2", 62, 255), "หมวก": ("th+croak", 26, 228),
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
        cur += len(a) / SR + 0.14
    d = max(sh["dur"] * 0.9, cur + 0.35)
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

# ดนตรี: ช่วงกรุงเทพสดใส (ช็อต 1-7) · โลกเวทมนตร์มีระฆัง (9-13) · ลุ้น (14) แล้วหยุดตอน "เช็กเกลียว" · การ์ดโหวตเบา ๆ
music = np.zeros(N, np.float32)
C = 261.6; scale = [1, 9/8, 5/4, 3/2, 5/3, 2]
beat = 60 / 112
def section(t0, t1, root=1.0, bells=False, sparse=False):
    k = 0; tt = t0
    while tt < t1:
        prog = [1, 4/3, 3/2, 4/3][(k // 8) % 4] * root
        if k % 2 == 0:
            add(music, tone(C/2*prog, .5, "pluck", 5), tt, .5)
        if not sparse or k % 2 == 0:
            add(music, tone(C*prog*scale[(k*3) % 6], .35, "pluck", 7), tt + (beat/2 if k % 4 == 3 else 0), .32)
        if bells and k % 4 == 0:
            add(music, tone(C*4*prog*scale[k % 5], 1.2, "sine", 2.5), tt, .14)
        tt += beat; k += 1
s = {p["n"]: p for p in plan}
section(0, s[8]["start"], 1.0)
section(s[9]["start"], s[14]["start"], 9/8, bells=True)
# ลุ้นช็อต 14: โน้ตยาวไต่ขึ้น หยุดเงียบก่อนประโยค "เช็กเกลียว"
cut14 = s[14]["start"] + s[14]["clips"][-1]["at"] - 0.1
for i, f in enumerate([C, C*9/8, C*5/4, C*4/3, C*3/2]):
    a = s[14]["start"] + i * 0.5
    if a < cut14:
        add(music, tone(f, 0.9, "saw", 1.2) * 0.25, a, .35)
section(s[15]["start"] + 0.2, TOTAL, 1.0, sparse=True)

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

crow(s[2]["start"] + s[2]["clips"][0]["at"] + s[2]["clips"][0]["len"] + .05); thud(s[2]["start"] + s[2]["dur"] - 1.0)
for i in range(3): add(sfx, tone(1500 + 300*i, .3, "sine", 8), s[3]["start"] + .3 + i*.12, .12)
ding(s[4]["start"] + s[4]["clips"][-1]["at"])
boing(s[5]["start"] + .6); ding(s[6]["start"] + .5, 2200)
whoosh(s[8]["start"] - .4, 1.3)
sparkle(s[10]["start"] + .3); clack(s[10]["start"] + s[10]["dur"] - 1.0)
khaen(s[11]["start"] + .1)
VOTE_STEP = 0.75
for i in range(int((s[15]["dur"] - .4) / VOTE_STEP)):
    click(s[15]["start"] + .3 + i * VOTE_STEP)

def rms(x):
    m = np.abs(x) > 1e-4; return float(np.sqrt(np.mean(x[m]**2))) if m.any() else 1e-6
music *= rms(voice) / rms(music) * 10**(-9/20)                  # ดนตรีเบากว่าเสียงพูด 9 dB
act = np.convolve((np.abs(voice) > .02).astype(np.float32), np.ones(int(.25*SR))/int(.25*SR), "same")
music *= 1 - .35*np.clip(act*3, 0, 1)                           # หลบเสียงพูดเพิ่มอีกนิด
mix = voice + music + sfx * .8
mix = mix[:int(TOTAL*SR)]
mix = mix / (np.abs(mix).max() + 1e-6) * .89
pcm = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
with wave.open("out/mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())

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
    trans = "zoomin" if plan[i]["n"] == 8 else "fade"
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
