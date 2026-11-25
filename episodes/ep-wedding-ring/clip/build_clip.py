"""ตัดต่อคลิปตอนงานแต่ง (แอนิแมติกจากสตอรีบอร์ด) พร้อมเสียงพากย์ ดนตรี และเสียงประกอบ
ดนตรีและเสียงประกอบสังเคราะห์เองทั้งหมด (ไม่ใช้เครดิต):
- ช่วงงานแต่ง (ช็อต 1-3): Bridal Chorus ของ Wagner (บทเพลงสาธารณสมบัติ) เรียบเรียงใหม่เป็นเสียงออร์แกนนุ่ม ๆ มีเสียงแขกปรบมือในช็อต 2
- ช็อต 4: ประตูเปิดเสียงดังปัง ดนตรีหยุด ตามด้วยฟ้าร้องและฝนตก (ฝนต่อไปถึงท้ายเรื่อง)
- จากช็อต 6: ดนตรีระทึกขวัญค่อย ๆ หนักขึ้น มีเสียงทุ้มกระแทกตอนหักมุม ลิฟต์ดัง ติ๊ง โทรศัพท์สั่น เคาะประตูสามครั้ง คลิกตอนสลับตัวเลือก
ภาพ: ซูมช้าทุกช็อต ภาพจางซ้อน 0.4 วิ ซูมเบลอพร้อมเสียงวูบตอนเปลี่ยนสถานที่ กล้องสั่นตอนประตูปังและตอนหักมุม ฟ้าแลบ ลายน้ำดวงตามุมขวาบน ต่อด้วยโลโก้ปิดท้าย
รัน: python3 build_clip.py -> out/clip_wedding.mp4"""
import json, os, subprocess, math, random
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
FPS = 24
W, H = 1080, 1920
OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

# ---------------------------------------------------------------- เสียงพากย์
rep = json.load(open(os.path.join(HERE, 'vo', 'report.json')))['lines']
def load_mp3(path):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    # ตัดเงียบหัวท้าย แล้วปรับความดังให้เท่ากัน (ผู้หญิงชุดดำกระซิบเบากว่า)
    a = np.abs(x); thr = 0.01
    idx = np.where(a > thr)[0]
    if len(idx): x = x[max(0, idx[0] - int(.03 * SR)):idx[-1] + int(.12 * SR)]
    rms = np.sqrt(np.mean(x ** 2) + 1e-9)
    return x * (0.12 / rms)
VO = {}
for key, d in rep.items():
    VO.setdefault(d['shot'], []).append((d['who'], load_mp3(os.path.join(HERE, 'vo', d['best']['path']))))

# ---------------------------------------------------------------- ไทม์ไลน์
LEAD, TAIL, XF = 0.45, 0.6, 0.4
EXTRA_LEAD = {4: 1.6, 5: 0.3, 6: 0.4, 9: 0.5, 15: 0.5, 20: 0.6, 24: 0.2, 25: 0.6}
EXTRA_TAIL = {19: 0.6, 24: 2.0, 25: 0.4}
shots = []
t = 0.0
for n in range(1, 28):
    if n in VO:
        vdur = sum(len(v) for _, v in VO[n]) / SR
        lead = LEAD + EXTRA_LEAD.get(n, 0)
        dur = lead + vdur + TAIL + EXTRA_TAIL.get(n, 0)
    elif n == 26:
        lead, dur = 0, 3.4
    else:
        lead, dur = 0, 6.4
    shots.append(dict(n=n, start=t, dur=dur, lead=lead))
    t += dur - XF
TOTAL = shots[-1]['start'] + shots[-1]['dur']
N = int(TOTAL * SR) + SR
S = {s['n']: s for s in shots}
print(f'total {TOTAL:.1f}s')

voice = np.zeros(N, np.float32)
for s in shots:
    if s['n'] in VO:
        i = int((s['start'] + s['lead']) * SR)
        for who, v in VO[s['n']]:
            voice[i:i + len(v)] += v; i += len(v) + int(.25 * SR)

def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf): return
    n = min(len(sig), len(buf) - i)
    buf[i:i + n] += sig[:n] * g

def env_adsr(n, a=.01, r=.3):
    e = np.ones(n, np.float32); na = max(1, int(a * SR)); nr = max(1, min(n - na, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr)
    return e

def lowpass(x, cut):
    a = math.exp(-2 * math.pi * cut / SR); y = np.empty_like(x); acc = 0.0
    # หนึ่งขั้ว (ใช้ cumulative trick ไม่ได้ เลยวนแบบเร็วด้วย lfilter แบบเขียนเอง)
    from itertools import accumulate
    b = 1 - a
    acc = 0.0
    for i in range(len(x)):
        acc = acc * a + x[i] * b; y[i] = acc
    return y

def lp_fast(x, cut):
    # กรองต่ำผ่านแบบ FFT (เร็วกว่าลูป)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / cut) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)

def bp_fast(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / hi) ** 4))
    return np.fft.irfft(X, len(x)).astype(np.float32)

def reverb(x, decay=1.6, mix=.3):
    n = int(decay * SR); ir = (rng.standard_normal(n) * np.exp(-np.linspace(0, 6, n))).astype(np.float32) * .05
    L = len(x) + n; F = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)].astype(np.float32)
    return x * (1 - mix) + y * mix * 3

# ---------------------------------------------------------------- Bridal Chorus (เรียบเรียงใหม่ ออร์แกนนุ่ม)
def organ(f, dur, vel=1.0):
    n = int(dur * SR); x = np.arange(n) / SR
    sig = (np.sin(2 * np.pi * f * x) + .55 * np.sin(4 * np.pi * f * x) + .3 * np.sin(6 * np.pi * f * x) + .12 * np.sin(8 * np.pi * f * x))
    vib = 1 + .004 * np.sin(2 * np.pi * 5.2 * x)
    sig = sig * vib
    return (sig * env_adsr(n, .06, min(.35, dur * .4)) * vel * .18).astype(np.float32)
def hz(m): return 440 * 2 ** ((m - 69) / 12)
G4, A4, B4, C5, D5, E5, F5, G5 = 67, 69, 71, 72, 74, 76, 77, 79
C3, G2, F2, E3, C4, E4, G3, F3, A3, B3, D4 = 48, 43, 41, 52, 60, 64, 55, 53, 57, 59, 62
BEAT = .78
melody = [(G4, 1), (C5, .75), (C5, .25), (C5, 2), (G4, 1), (D5, .75), (B4, .25), (C5, 2),
          (G4, 1), (C5, 1), (F5, .75), (F5, .25), (E5, 1), (D5, .75), (C5, .25), (B4, 1), (C5, .75), (D5, .25), (C5, 2),
          (G4, 1), (C5, .75), (C5, .25), (C5, 2), (G4, 1), (D5, .75), (B4, .25), (C5, 2),
          (G4, 1), (C5, 1), (E5, .75), (G5, .25), (G5, 1), (E5, .75), (C5, .25), (A4, 1), (C5, .75), (D5, .25), (C5, 3)]
chords = [((C3, E3, G3), 4), ((G2, D4 - 12, F3), 2), ((C3, E3, G3), 2), ((C3, E3, G3), 2), ((F2, A3, C4), 2), ((G2, B3, D4), 2), ((C3, E3, G3), 2),
          ((C3, E3, G3), 4), ((G2, D4 - 12, F3), 2), ((C3, E3, G3), 2), ((C3, E3, G3), 2), ((A3 - 12, C4 - 12, E3), 2), ((F2, A3, C4), 2), ((C3, E3, G3), 4)]
wedding = np.zeros(N, np.float32)
end_wed = S[4]['start'] + .05          # ดนตรีหยุดตรงเสียงปัง
tt = .3
for m, b in melody:
    if tt >= end_wed: break
    add(wedding, tt, organ(hz(m), b * BEAT * 1.02, 1.0)); add(wedding, tt, organ(hz(m + 12), b * BEAT, .25))
    tt += b * BEAT
tt = .3
for ch, b in chords:
    if tt >= end_wed: break
    for m in ch: add(wedding, tt, organ(hz(m + 12), b * BEAT, .38))
    add(wedding, tt, organ(hz(ch[0]), b * BEAT, .28))
    tt += b * BEAT
cut = int(end_wed * SR); wedding[cut:] = 0
wedding[:cut] *= np.minimum(1, np.arange(cut) / (.8 * SR))
wedding = reverb(wedding, 2.4, .35)
wedding[cut + int(.25 * SR):] *= 0                        # หางเสียงสั้น ๆ หลังปัง

# เสียงแขกปรบมือในช็อต 2
claps = np.zeros(N, np.float32)
s2 = S[2]
for k in range(900):
    at = s2['start'] + rng.uniform(.2, s2['dur'] - .3)
    n = int(.03 * SR); c = rng.standard_normal(n).astype(np.float32) * np.exp(-np.linspace(0, 9, n))
    add(claps, at, c, rng.uniform(.02, .06))
claps = bp_fast(claps, 800, 5000)
e = np.zeros(N, np.float32); i0, i1 = int(s2['start'] * SR), int((s2['start'] + s2['dur']) * SR)
e[i0:i1] = np.sin(np.linspace(0, np.pi, i1 - i0)) ** .6
claps *= e

# ---------------------------------------------------------------- เสียงประกอบ
sfx = np.zeros(N, np.float32)
def boom(dur=2.2, f0=55):
    n = int(dur * SR); x = np.arange(n) / SR
    s = np.sin(2 * np.pi * (f0 * x + 25 * (1 - np.exp(-x * 8)) / 8)) * np.exp(-x * 2.2)
    s += .5 * np.sin(2 * np.pi * f0 * 2 * x) * np.exp(-x * 3)             # ฮาร์มอนิกให้ลำโพงมือถือได้ยิน
    return s.astype(np.float32)
def door_bang():
    n = int(1.4 * SR); x = np.arange(n) / SR
    thump = boom(1.4, 62) * 1.1
    crack = rng.standard_normal(n).astype(np.float32) * np.exp(-x * 28)
    crack = bp_fast(crack, 300, 4000) * 1.6
    return reverb(thump + crack, 1.8, .4)
def thunder(dur=4.5, dist=1.0):
    n = int(dur * SR); x = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    rumble = lp_fast(noise, 160) * 6
    crackle = bp_fast(noise, 900, 4500) * np.exp(-x * 5) * (1.2 / dist)
    env = (1 - np.exp(-x * 9)) * np.exp(-x * .75) * (1 + .5 * np.sin(2 * np.pi * .9 * x) ** 2)
    return ((rumble + crackle) * env * (.9 / dist)).astype(np.float32)
def knock():
    n = int(.25 * SR); x = np.arange(n) / SR
    s = np.sin(2 * np.pi * 180 * x) * np.exp(-x * 40) + .6 * np.sin(2 * np.pi * 420 * x) * np.exp(-x * 60)
    s += bp_fast(rng.standard_normal(n).astype(np.float32), 400, 3000) * np.exp(-x * 70) * .8
    return reverb(s.astype(np.float32), .6, .25) * .9
def ding(f=1318.5):
    n = int(1.6 * SR); x = np.arange(n) / SR
    return ((np.sin(2 * np.pi * f * x) + .4 * np.sin(2 * np.pi * f * 2.76 * x) * np.exp(-x * 4)) * np.exp(-x * 2.5) * .22).astype(np.float32)
def buzz(dur=.5):
    n = int(dur * SR); x = np.arange(n) / SR
    s = np.sign(np.sin(2 * np.pi * 150 * x)) * .5 + np.sin(2 * np.pi * 300 * x)
    return (bp_fast(s.astype(np.float32), 120, 1500) * env_adsr(n, .02, .05) * .12).astype(np.float32)
def whoosh(dur=.6):
    n = int(dur * SR); x = np.arange(n) / SR
    s = bp_fast(rng.standard_normal(n).astype(np.float32), 300, 2500) * np.sin(np.pi * x / dur) ** 2
    return (s * .5).astype(np.float32)
def click():
    n = int(.04 * SR); x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2200 * x) * np.exp(-x * 160) * .35).astype(np.float32)

add(sfx, S[4]['start'], door_bang(), 1.0)
add(sfx, S[4]['start'] + .75, thunder(5.0, 1.0), 1.0)
add(sfx, S[9]['start'] + .2, thunder(4.0, 1.8), .8)
add(sfx, S[20]['start'] + .3, thunder(4.0, 2.2), .6)
for at in (S[17]['start'] + .25, S[19]['start'] + .25):
    add(sfx, at, boom(2.4, 50), .9)
for at in (S[15]['start'], S[20]['start']):
    add(sfx, at - .25, whoosh(), .9)
for k in range(3):
    add(sfx, S[20]['start'] + .2 + k * 1.8, ding(), 1.0)
for k in range(4):
    add(sfx, S[21]['start'] + .1 + k * .9, buzz(.45), 1.0)
kt = S[24]['start'] + S[24]['lead'] + sum(len(v) for _, v in VO[24]) / SR + .25
for k in range(3):
    add(sfx, kt + k * .55, knock(), 1.0)
# ผู้ใช้สั่ง: ตอนจบ หลังสามีเคาะประตูเรียกจบประโยค ให้ฟ้าผ่าอีกครั้ง (ใช้เสียงฟ้าผ่าจริงถ้ามี) แล้วเข้าช็อตนางเอกตกใจ
if os.path.exists(os.path.join(HERE, 'sfx', 'thunder.mp3')):
    import audiolib as _A
    add(sfx, S[26]['start'] - .15, _A.load_voice(os.path.join(HERE, 'sfx', 'thunder.mp3'), .1) * 3.5, 1.0)
else:
    add(sfx, S[26]['start'] - .15, thunder(5.0, .9), 1.0)
add(sfx, S[26]['start'] + .1, boom(2.8, 45), .7)
for k in range(1, 4):
    add(sfx, S[27]['start'] + k * 1.6, click(), 1.0)

# ฝนตก: เริ่มหลังฟ้าร้อง ต่อเนื่องถึงท้ายเรื่อง
rain = np.zeros(N, np.float32)
r0 = S[4]['start'] + .9
nr = N - int(r0 * SR)
base = bp_fast(rng.standard_normal(nr).astype(np.float32), 1200, 7000) * .5
drops = np.zeros(nr, np.float32)
for k in range(int(nr / SR * 40)):
    i = rng.integers(0, nr - 400); drops[i:i + 400] += rng.standard_normal(400).astype(np.float32) * np.exp(-np.linspace(0, 12, 400)) * rng.uniform(.1, .4)
drops = bp_fast(drops, 1500, 8000)
rain[int(r0 * SR):] = (base + drops) * np.minimum(1, np.arange(nr) / (2.0 * SR))
# ห้องพักกับลิฟต์ฝนดังขึ้นนิด (ใกล้หน้าต่าง)
rain_g = np.full(N, .55, np.float32)
for n_ in (20, 21, 22, 23, 24, 25, 26):
    i0 = int(S[n_]['start'] * SR); i1 = int((S[n_]['start'] + S[n_]['dur']) * SR); rain_g[i0:i1] = .8
rain *= lp_fast(rain_g, 2)

# ---------------------------------------------------------------- ดนตรีระทึกขวัญ (ค่อย ๆ หนักขึ้น)
thr = np.zeros(N, np.float32)
x = np.arange(N) / SR
def tone(f, amp):
    return (np.sin(2 * np.pi * f * x) + .5 * np.sin(4 * np.pi * f * x) + .25 * np.sin(6 * np.pi * f * x)) * amp
drone = tone(hz(45), 1) + tone(hz(46), .7) + tone(hz(57), .5) + tone(hz(58), .35)      # A2/Bb2 ไม่ลงกัน + อ็อกเทฟให้มือถือได้ยิน
drone *= 1 + .3 * np.sin(2 * np.pi * .13 * x)
strings = tone(hz(81), .35) + tone(hz(82), .3) + tone(hz(88), .2)                       # คลัสเตอร์สูงสั่นเครือ
strings *= 1 + .5 * np.sin(2 * np.pi * 7 * x)
pulse = np.zeros(N, np.float32)
bt = S[10]['start']
while bt < TOTAL:
    for o in (0, .28):
        add(pulse, bt + o, boom(.5, 52), .45 if o == 0 else .3)
    bt += 1.1
piano_m = np.zeros(N, np.float32)
motif = [57, 60, 64, 63, 57, 65, 64, 58]
tt = S[6]['start']
while tt < S[26]['start']:
    for k, m in enumerate(motif):
        add(piano_m, tt + k * .9, (np.sin(2 * np.pi * hz(m) * np.arange(int(2 * SR)) / SR) * np.exp(-np.arange(int(2 * SR)) / SR * 1.8) * .3).astype(np.float32))
    tt += 7.2
def level_curve(points):
    c = np.zeros(N, np.float32)
    pts = sorted(points)
    for (t0, v0), (t1, v1) in zip(pts, pts[1:]):
        i0, i1 = int(t0 * SR), int(t1 * SR); c[i0:i1] = np.linspace(v0, v1, max(1, i1 - i0))
    c[int(pts[-1][0] * SR):] = pts[-1][1]
    return c
g_drone = level_curve([(0, 0), (S[5]['start'] + 1, 0), (S[6]['start'], .35), (S[10]['start'], .5), (S[15]['start'], .65), (S[20]['start'], .8), (S[25]['start'], .95), (S[26]['start'], .95), (S[26]['start'] + .3, .4), (S[27]['start'], .25), (TOTAL, .15)])
g_str = level_curve([(0, 0), (S[14]['start'], 0), (S[16]['start'], .4), (S[20]['start'], .7), (S[25]['start'] + 2, 1.0), (S[26]['start'], 0), (TOTAL, 0)])
g_pulse = level_curve([(0, 0), (S[10]['start'], 0), (S[12]['start'], .5), (S[19]['start'], .8), (S[24]['start'], 1.0), (S[26]['start'], 1.0), (S[26]['start'] + .1, 0), (TOTAL, 0)])
g_pno = level_curve([(0, 0), (S[6]['start'], 0), (S[7]['start'], .7), (S[20]['start'], .8), (S[26]['start'], 0), (TOTAL, 0)])
thr = drone * .05 * g_drone + strings * .03 * g_str + pulse * .5 * g_pulse + piano_m * .6 * g_pno
thr = reverb(thr.astype(np.float32), 2.2, .3)
# เงียบก่อนเหตุการณ์น่ากลัว: ก่อนเคาะประตู
i0, i1 = int((kt - 1.4) * SR), int(kt * SR)
thr[i0:i1] *= np.linspace(1, .15, i1 - i0)

# ---------------------------------------------------------------- มิกซ์ (ดนตรีเบากว่าเสียงพูดราว 8-10 dB และหลบใต้เสียงพูด)
venv = lp_fast(np.abs(voice), 4)
duck = 1 - .45 * np.clip(venv / (venv.max() * .25 + 1e-6), 0, 1)
def rms(x): return float(np.sqrt(np.mean(x ** 2)) + 1e-9)
v_rms = rms(voice[np.abs(voice) > 1e-4])
def to_db_below(x, seg, db):
    i0, i1 = int(seg[0] * SR), int(seg[1] * SR)
    return x * (v_rms * 10 ** (-db / 20) / rms(x[i0:i1]))
wedding = to_db_below(wedding, (0.5, S[4]['start']), 5.5)
thr = to_db_below(thr, (S[6]['start'], S[26]['start']), 6.5)
rain = to_db_below(rain, (S[5]['start'], TOTAL - 1), 22)
claps = to_db_below(claps, (S[2]['start'] + .5, S[2]['start'] + S[2]['dur'] - .5), 14)
music = (wedding + thr) * duck
mix = voice * 1.0 + music + claps + rain + sfx * .35
mix = np.tanh(mix * 1.3) / 1.3
mix = mix / (np.abs(mix).max() + 1e-6) * .9
wav = os.path.join(OUT, 'mix.wav')
import wave
with wave.open(wav, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    st = np.repeat((mix * 32767).astype(np.int16)[:, None], 2, axis=1)
    w.writeframes(st.tobytes())
vr = 20 * np.log10(v_rms); mr = 20 * np.log10(rms(music[int(S[6]['start'] * SR):int(S[26]['start'] * SR)])); wr = 20 * np.log10(rms(music[int(.5 * SR):int(S[4]['start'] * SR)]))
print(f'voice {vr:.1f} dB · wedding {wr:.1f} dB (diff {vr - wr:.1f}) · thriller {mr:.1f} dB (diff {vr - mr:.1f})')

# ---------------------------------------------------------------- ภาพ
def load(name):
    d = 'hd' if name.startswith('card') else 'hd_nosub'
    im = Image.open(os.path.join(HERE, d, name)).convert('RGB').resize((W, H))
    return im
FR = {n: load(f'{n:02d}.jpg') for n in range(1, 27)}
CARD = {k: load(f'card_{k}.jpg') for k in 'AB'}
logo = Image.open(os.path.join(HERE, '..', '..', '..', 'pipeline', 'v2', 'logo.png')).convert('RGBA')
eye = logo.crop((0, 0, logo.size[1], logo.size[1])).resize((86, 86))
ZOOM = {10: 1.12, 26: 1.14, 22: 1.08, 23: 1.08}
SHAKE = [(S[4]['start'], .6, 22), (S[17]['start'] + .25, .45, 12), (S[19]['start'] + .25, .45, 12), (S[26]['start'] + .1, .4, 10)]
FLASH = [(S[4]['start'] + .75, .18), (S[4]['start'] + 1.05, .12), (S[9]['start'] + .2, .12), (S[20]['start'] + .3, .1)]
BLUR_IN = {15, 20}

CH = json.load(open(os.path.join(HERE, 'subs', 'chunks.json')))
SUBS = []
for n, chs in CH.items():
    n = int(n); s0 = S[n]; vt = s0['start'] + s0['lead']; vd = sum(len(v) for _, v in VO[n]) / SR
    tot = sum(c['w'] for c in chs); acc = 0
    for k, c in enumerate(chs):
        a0 = vt + vd * acc / tot - (.15 if k == 0 else 0); acc += c['w']
        a1 = vt + vd * acc / tot + (.5 if k == len(chs) - 1 else 0)
        SUBS.append((a0, a1, Image.open(os.path.join(HERE, 'subs', f's{n:02d}_{k}.png')).convert('RGBA').resize((W, H))))
SUBS.sort(key=lambda t: t[0])

def frame_at(n, lt):
    s = S[n]
    if n == 27:
        im = CARD['A' if int(lt / 1.6) % 2 == 0 else 'B']
        return im
    im = FR[n]
    z = 1 + (ZOOM.get(n, 1.06) - 1) * (lt / s['dur'])
    if n in BLUR_IN and lt < .35:
        z += (.35 - lt) * .5
    cw, ch = W / z, H / z
    cx, cy = W / 2, H / 2 - (40 if n in (10, 26) else 0) * (z - 1) * 6
    box = (cx - cw / 2, cy - ch / 2, cx + cw / 2, cy + ch / 2)
    out = im.resize((W, H), Image.BILINEAR, box=box)
    if n in BLUR_IN and lt < .35:
        out = out.filter(ImageFilter.GaussianBlur((.35 - lt) * 40))
    return out

proc = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                         '-i', wav, '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                         '-shortest', os.path.join(OUT, 'body.mp4')], stdin=subprocess.PIPE)
nfr = int(TOTAL * FPS)
for f in range(nfr):
    T = f / FPS
    act = [s for s in shots if s['start'] <= T < s['start'] + s['dur']]
    a = act[-1]
    img = frame_at(a['n'], T - a['start'])
    if len(act) > 1 and a['n'] not in BLUR_IN:
        p = act[0]; k = (T - a['start']) / XF
        img = Image.blend(frame_at(p['n'], T - p['start']), img, min(1, k))
    dx = dy = 0
    for t0, d, amp in SHAKE:
        if t0 <= T < t0 + d:
            q = 1 - (T - t0) / d; dx = int(math.sin(T * 90) * amp * q); dy = int(math.cos(T * 77) * amp * q)
    if dx or dy:
        img = img.transform((W, H), Image.AFFINE, (1, 0, -dx, 0, 1, -dy), Image.BILINEAR)
    for t0, d in FLASH:
        if t0 <= T < t0 + d:
            img = ImageEnhance.Brightness(img).enhance(1 + .9 * (1 - (T - t0) / d))
    for t0, t1, simg in SUBS:
        if t0 <= T < t1:
            img = img.copy(); img.paste(simg, (0, 0), simg); break
    # ลายน้ำดวงตา จางออกตอนการ์ด
    op = 1.0
    if T > S[27]['start']: op = max(0, 1 - (T - S[27]['start']) / .6)
    if op > 0:
        e = eye.copy(); e.putalpha(e.getchannel('A').point(lambda v: int(v * .75 * op)))
        img = img.copy(); img.paste(e, (W - 86 - 40, 50), e)
    proc.stdin.write(img.tobytes())
    if f % 240 == 0: print(f'frame {f}/{nfr}', flush=True)
proc.stdin.close(); proc.wait()

# ต่อโลโก้ปิดท้าย
outro = os.path.join(HERE, '..', '..', '..', 'pipeline', 'v2', 'outro.mp4')
subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', os.path.join(OUT, 'body.mp4'), '-i', outro, '-filter_complex',
                '[0:v]fps=24,setsar=1[v0];[1:v]fps=24,scale=1080:1920,setsar=1[v1];[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[1:a]aresample=48000,aformat=channel_layouts=stereo[a1];[v0][a0][v1][a1]concat=n=2:v=1:a=1[v][a]',
                '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', os.path.join(OUT, 'clip_wedding.mp4')], check=True)
json.dump(dict(total=TOTAL, shots=shots), open(os.path.join(OUT, 'timeline.json'), 'w'), indent=1)
print('done', os.path.join(OUT, 'clip_wedding.mp4'))
