"""บ้านตรงข้าม · ดนตรีและเสียงเอฟเฟกต์ (สังเคราะห์ด้วย numpy ไม่มีเสียงพากย์) -> clip/audio.wav
ดนตรีอยู่ย่านกลาง (ลำโพงมือถือ) เปลี่ยนตามฉาก: เล่าเรื่องเบา ๆ · สืบ/ลึกลับ · กดดัน · ตกใจกระแทกเฉพาะจังหวะ · งานเลี้ยงสดใส · ปิดท้ายหลอน"""
import json, wave, numpy as np

SR = 44100; XF = .4; OUTRO = 2.6
shots = json.load(open('shots.json', encoding='utf-8'))
start = []; t = 0.0
for i, s in enumerate(shots):
    start.append(t); t += s['dur'] - (XF if i < len(shots) - 1 else 0)
TOTAL = t + OUTRO - XF + .2
N = int(TOTAL * SR)
mus = np.zeros(N, np.float32); sfx = np.zeros(N, np.float32)
rng = np.random.default_rng(7)

def at(n, off=0.0): return start[n - 1] + off
def span(n): return start[n - 1], start[n - 1] + shots[n - 1]['dur']
def add(buf, sig, t0, g=1.0):
    i0 = int(t0 * SR)
    if i0 >= N: return
    seg = sig[:N - i0] * g; buf[i0:i0 + len(seg)] += seg
def env(n, a=.01, r=.3):
    x = np.arange(n) / SR; e = np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / max(r, 1e-4)); return e
def tone(f, d, kind='sine', a=.01, r=.5, det=0.0):
    n = int(d * SR); x = np.arange(n) / SR
    ph = 2 * np.pi * f * x
    if kind == 'sine': s = np.sin(ph)
    elif kind == 'pno': s = np.sin(ph) + .45 * np.sin(2 * ph) * np.exp(-x * 1.5) + .18 * np.sin(3.01 * ph) * np.exp(-x * 3)
    elif kind == 'pluck': s = np.sin(ph) + .5 * np.sin(2 * ph) + .25 * np.sin(3 * ph)
    elif kind == 'pad': s = np.sin(ph) + np.sin(2 * np.pi * f * (1 + det) * x) + .4 * np.sin(2 * ph * 1.002)
    elif kind == 'bell': s = np.sin(ph) + .6 * np.sin(2.76 * ph) * np.exp(-x * 2) + .3 * np.sin(5.4 * ph) * np.exp(-x * 4)
    return (s * env(n, a, r)).astype(np.float32)
def pad(freqs, d, swell=1.2, g=.12):
    n = int(d * SR); x = np.arange(n) / SR
    e = np.minimum(1, x / swell) * np.minimum(1, (d - x) / swell)
    s = sum(np.sin(2 * np.pi * f * x) + .7 * np.sin(2 * np.pi * f * 1.004 * x + 1) + .25 * np.sin(4 * np.pi * f * x) for f in freqs)
    return (s * e * g / len(freqs)).astype(np.float32)
def noise(d, lp=.0, a=.005, r=.2):
    n = int(d * SR); s = rng.standard_normal(n).astype(np.float32)
    if lp:
        k = int(lp); s = np.convolve(s, np.ones(k) / k, 'same').astype(np.float32)
    return s * env(n, a, r).astype(np.float32)
def reverb(sig, t60=1.6, mix=.3):
    n = int(t60 * SR); ir = rng.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / SR * 6.9 / t60).astype(np.float32)
    ir /= np.sqrt((ir ** 2).sum())
    L = len(sig) + n; F = 1 << (L - 1).bit_length()
    wet = np.fft.irfft(np.fft.rfft(sig, F) * np.fft.rfft(ir, F), F)[:len(sig)].astype(np.float32)
    return sig * (1 - mix) + wet * mix * 3

A3, B3, C4, D4, E4, F4, G4, A4, B4, C5, D5, E5 = 220, 246.9, 261.6, 293.7, 329.6, 349.2, 392, 440, 493.9, 523.3, 587.3, 659.3
G3, F3, E3, Eb4, Bb3 = 196, 174.6, 164.8, 311.1, 233.1

# ---- music by section ----
def section(a, b): return start[a - 1], start[b - 1] + shots[b - 1]['dur']
# 1-8: narration bed: soft minor piano + pad, a ticking pluck from shot 5 (the bored detective, comic curiosity)
t0, t1 = section(1, 8)
motif = [A3, E4, C4, E4, A3, F4, E4, D4]; k = 0; tt = t0 + .2
while tt < t1 - 1:
    add(mus, tone(motif[k % 8], 2.2, 'pno', r=.9), tt, .16); k += 1; tt += .9
for j, ch in enumerate([(A3, C4, E4), (F3, A3, C4), (C4, E4, G4), (E3, G3, B3)] * 6):
    ts = t0 + j * 3.6
    if ts > t1 - 1: break
    add(mus, pad(ch, 4.4), ts, .9)
tt = start[4]
while tt < t1 - .5:
    add(mus, tone(A4 if int((tt - start[4]) / .45) % 4 else E5, .3, 'pluck', r=.06), tt, .05); tt += .45
# 9-11: the fight: low drone + slow pulse, then near silence on the dark window
t0, t1 = section(9, 10)
add(mus, pad((A3 / 2 * 2, Eb4 / 2, A3), t1 - t0 + .6, swell=1.0, g=.16), t0)
tt = t0
while tt < t1:
    add(mus, tone(110, .5, 'sine', r=.25), tt, .22); tt += .75
add(mus, pad((A3,), shots[10]['dur'], swell=.8, g=.05), start[10])
# 12-14: suspense: high string drone + heartbeat, rising
t0, t1 = section(12, 14)
add(mus, pad((A4, Bb3 * 2), t1 - t0, swell=2.0, g=.08), t0)
tt = t0
while tt < t1:
    add(mus, tone(70, .18, 'sine', r=.08), tt, .5); add(mus, tone(66, .2, 'sine', r=.1), tt + .22, .4); tt += 1.1
# 15-19: investigation + the message + the pounding: clock tick, eerie bell, pressure
t0, t1 = section(15, 19)
tt = t0
while tt < t1:
    add(mus, noise(.03, lp=3, r=.01), tt, .05); tt += .5
for j, f in enumerate([E5, C5, Eb4 * 2, B4]):
    add(mus, tone(f, 3.0, 'bell', r=1.2), start[14] + j * 1.6, .06)
add(mus, pad((A3, C4, Eb4), section(16, 17)[1] - start[15], swell=1.5, g=.14), start[15])
add(mus, pad((F3, A3, C4), section(18, 19)[1] - start[17], swell=1.0, g=.1), start[17])
# 20-23: tension rises: pulse speeds up, low strings, silence just before the door
t0, t1 = section(20, 23)
add(mus, pad((A3 / 2 * 2, E4 / 2, Bb3), t1 - t0 - 1.0, swell=2.5, g=.15), t0)
tt = t0; gap = .8
while tt < t1 - 1.2:
    add(mus, tone(70, .18, 'sine', r=.08), tt, .55); add(mus, tone(66, .2, 'sine', r=.1), tt + .2, .45); tt += gap; gap = max(.45, gap * .97)
# 24-27: SURPRISE: bright major bounce (plucks + bells + bass)
t0, t1 = section(24, 27)
prog = [(C4, E4, G4), (F4, A4, C5), (G4, B4, D5), (C4, E4, G4)]
bt = .3; tt = t0 + .35; k = 0
while tt < t1:
    ch = prog[(k // 8) % 4]
    add(mus, tone(ch[k % 3] * (2 if k % 4 == 3 else 1), .35, 'pluck', r=.1), tt, .1)
    if k % 2 == 0: add(mus, tone(ch[0] / 2, .3, 'sine', r=.15), tt, .2)
    if k % 8 == 0: add(mus, pad(ch, 2.6, swell=.3, g=.08), tt)
    tt += bt; k += 1
# 28: laughter fades, music thins out
add(mus, pad((C4, E4, G4), shots[27]['dur'] + .5, swell=1.5, g=.07), start[27])
# 29: the watcher: eerie cluster + low hit at the cut to black
t0, t1 = section(29, 29)
add(mus, pad((A3, Bb3, E4), t1 - t0, swell=1.4, g=.16), t0)
for j in range(4): add(mus, tone([E5, Eb4 * 2, C5, B4][j], 2.2, 'bell', r=1.0), t0 + .4 + j * 1.0, .05)
# 30: A/B card: soft pulse
t0, t1 = section(30, 30)
add(mus, pad((A3, E4), t1 - t0 + OUTRO, swell=.8, g=.08), t0)

# ---- sound effects ----
def whoosh(d=.7):
    n = int(d * SR); x = np.arange(n) / SR; s = rng.standard_normal(n).astype(np.float32)
    k = 6; s = np.convolve(s, np.ones(k) / k, 'same')
    e = np.sin(np.pi * x / d) ** 2
    return (s * e).astype(np.float32)
def boom(d=1.6):
    n = int(d * SR); x = np.arange(n) / SR
    f = 55 * np.exp(-x * 1.2) + 35
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.2) + .3 * noise(d, lp=40, r=.15)[:n]).astype(np.float32)
def shatter():
    s = noise(1.2, lp=0, a=.001, r=.12) * .6
    for j in range(14):
        add_t = rng.uniform(0, .6); f = rng.uniform(2500, 5500)
        b = tone(f, .25, 'sine', a=.001, r=.05); i0 = int(add_t * SR); s[i0:i0 + len(b)] += b * rng.uniform(.2, .5)
    return s
def knock():
    return (tone(140, .25, 'sine', a=.001, r=.05) + noise(.25, lp=8, a=.001, r=.03) * .7).astype(np.float32)
def click(): return (tone(1800, .05, 'sine', a=.001, r=.012) + tone(900, .05, 'sine', a=.001, r=.02) * .5).astype(np.float32)
def buzz(d=.5):
    n = int(d * SR); x = np.arange(n) / SR
    return (np.sign(np.sin(2 * np.pi * 180 * x)) * .25 * (np.sin(2 * np.pi * 9 * x) > 0) * np.minimum(1, (d - x) * 20)).astype(np.float32)
def creak(d=1.0):
    n = int(d * SR); x = np.arange(n) / SR; f = 300 + 120 * np.sin(2 * np.pi * .9 * x) + rng.standard_normal(n).cumsum() * .02
    s = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * (np.sin(2 * np.pi * 37 * x) > .2)
    return (np.convolve(s, np.ones(5) / 5, 'same') * np.sin(np.pi * x / d) * .25).astype(np.float32)
def popper(): return (noise(.4, lp=2, a=.001, r=.06) * 1.2 + boom(.4)[:int(.4 * SR)] * .4).astype(np.float32)
def thud(): return (tone(80, .4, 'sine', a=.002, r=.1) + noise(.4, lp=20, a=.002, r=.06) * .8).astype(np.float32)
def switch(): return (noise(.06, lp=2, a=.0005, r=.01) + tone(1200, .06, 'sine', a=.0005, r=.008) * .4).astype(np.float32)
def steps(n, gap=.55):
    s = np.zeros(int((n * gap + .5) * SR), np.float32)
    for j in range(n):
        b = noise(.15, lp=12, a=.002, r=.03) * .6 + tone(95, .15, 'sine', a=.002, r=.04) * .5; i0 = int(j * gap * SR); s[i0:i0 + len(b)] += b
    return s

for n_ in (2, 3, 29):                              # zoom-blur transitions: location change / flashback
    add(sfx, whoosh(.8), start[n_ - 1] - .45, .35)
add(sfx, steps(6, .32), at(2, .2), .35)            # running in the alley
add(sfx, noise(2.5, lp=60, a=.5, r=2.0), at(3), .04)   # hospital room tone
add(sfx, shatter(), at(10, 1.5), .5)                # wine glass
add(sfx, switch(), at(11, .1), .5)                 # lights out
add(sfx, boom(), at(14, 2.6), .7)                  # he looks up and smiles
add(sfx, buzz(.5), at(16, .5), .35); add(sfx, buzz(.5), at(16, 1.3), .35)   # unknown message
for j in range(4): add(sfx, knock(), at(17, .35 + j * .32), .55)          # pounding the glass
add(sfx, shatter()[:int(.5 * SR)], at(17, 1.0), .25); add(sfx, boom(), at(17, 1.0), .7)
for j in range(3): add(sfx, thud(), at(21, .6 + j * .45), .45)             # struggle
add(sfx, switch(), at(21, shots[20]['dur'] - .5), .5)
add(sfx, steps(5, .7), at(22, .3), .3)             # crutches on the stairs
add(sfx, creak(1.3), at(23, .6), .4)               # front door
add(sfx, switch(), at(24, .28), .6); add(sfx, popper(), at(24, .35), .6); add(sfx, popper(), at(24, .55), .45)
add(sfx, boom(1.2), at(29, shots[28]['dur'] - .35), .6)                    # cut to black
for j in range(int(shots[29]['dur'] / .9) + 1): add(sfx, click(), at(30, j * .9), .35)   # A/B highlight switches

# ---- mix: music in the mid band, effects on top, gentle limiter ----
mus = reverb(mus, 1.8, .35); sfx = reverb(sfx, 1.0, .15)
hp = mus - np.convolve(mus, np.ones(200) / 200, 'same')       # cut sub-bass mud (mid range for phone speakers)
mix = .8 * hp + sfx
fi = int(.6 * SR); mix[:fi] *= np.linspace(0, 1, fi); fo = int(1.5 * SR); mix[-fo:] *= np.linspace(1, 0, fo)
mix = np.tanh(mix * 1.6) / np.tanh(1.6) * .85
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
with wave.open('audio.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
json.dump(dict(start=start, total=TOTAL), open('timeline.json', 'w'))
print('audio', round(TOTAL, 1), 's', 'peak', round(float(np.abs(mix).max()), 2))
