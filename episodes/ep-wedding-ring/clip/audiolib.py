"""ชุดสังเคราะห์เสียงที่ใช้ร่วมกัน (ดนตรีงานแต่ง เสียงประกอบ ดนตรีระทึกขวัญ) ไม่ใช้เครดิต"""
import math, subprocess
import numpy as np
SR = 48000
rng = np.random.default_rng(7)

def hz(m): return 440 * 2 ** ((m - 69) / 12)
def add(buf, at, sig, g=1.0):
    i = int(at * SR)
    if i >= len(buf) or i + len(sig) <= 0: return
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), len(buf) - i); buf[i:i + n] += sig[:n] * g
def env_adsr(n, a=.01, r=.3):
    e = np.ones(n, np.float32); na = max(1, int(a * SR)); nr = max(1, min(n - na, int(r * SR)))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def lp(x, cut):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X *= 1 / (1 + (f / cut) ** 4)
    return np.fft.irfft(X, len(x)).astype(np.float32)
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / hi) ** 4))
    return np.fft.irfft(X, len(x)).astype(np.float32)
def reverb(x, decay=1.6, mix=.3):
    n = int(decay * SR); ir = (rng.standard_normal(n) * np.exp(-np.linspace(0, 6, n))).astype(np.float32) * .05
    L = len(x) + n; F = 1 << (L - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)].astype(np.float32)
    return x * (1 - mix) + y * mix * 3
def load_voice(path, target=.12):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '1', '-ar', str(SR), '-'], capture_output=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
    idx = np.where(np.abs(x) > .01)[0]
    if len(idx): x = x[max(0, idx[0] - int(.03 * SR)):idx[-1] + int(.15 * SR)]
    return x * (target / (np.sqrt(np.mean(x ** 2)) + 1e-9))

def organ(f, dur, vel=1.0):
    n = int(dur * SR); x = np.arange(n) / SR
    s = (np.sin(2 * np.pi * f * x) + .55 * np.sin(4 * np.pi * f * x) + .3 * np.sin(6 * np.pi * f * x) + .12 * np.sin(8 * np.pi * f * x)) * (1 + .004 * np.sin(2 * np.pi * 5.2 * x))
    return (s * env_adsr(n, .06, min(.35, dur * .4)) * vel * .18).astype(np.float32)
G4, A4, B4, C5, D5, E5, F5, G5 = 67, 69, 71, 72, 74, 76, 77, 79
C3, G2, F2, E3, C4, G3, F3, A3, B3, D4 = 48, 43, 41, 52, 60, 55, 53, 57, 59, 62
MELODY = [(G4, 1), (C5, .75), (C5, .25), (C5, 2), (G4, 1), (D5, .75), (B4, .25), (C5, 2),
          (G4, 1), (C5, 1), (F5, .75), (F5, .25), (E5, 1), (D5, .75), (C5, .25), (B4, 1), (C5, .75), (D5, .25), (C5, 2)] * 2
CHORDS = [((C3, E3, G3), 4), ((G2, D4 - 12, F3), 2), ((C3, E3, G3), 2), ((C3, E3, G3), 2), ((F2, A3, C4), 2), ((G2, B3, D4), 2), ((C3, E3, G3), 2)] * 2
def bridal_chorus(N, t0, t_end, beat=.78):
    w = np.zeros(N, np.float32); tt = t0
    for m, b in MELODY:
        if tt >= t_end: break
        add(w, tt, organ(hz(m), b * beat * 1.02)); add(w, tt, organ(hz(m + 12), b * beat, .25)); tt += b * beat
    tt = t0
    for ch, b in CHORDS:
        if tt >= t_end: break
        for m in ch: add(w, tt, organ(hz(m + 12), b * beat, .38))
        add(w, tt, organ(hz(ch[0]), b * beat, .28)); tt += b * beat
    c = int(t_end * SR); w[c:] = 0
    w = reverb(w, 2.4, .35); w[c + int(.2 * SR):] = 0
    return w
def claps(N, t0, t1):
    c = np.zeros(N, np.float32)
    for k in range(int((t1 - t0) * 160)):
        n = int(.03 * SR); s = rng.standard_normal(n).astype(np.float32) * np.exp(-np.linspace(0, 9, n))
        add(c, rng.uniform(t0, t1), s, rng.uniform(.02, .06))
    c = bp(c, 800, 5000); e = np.zeros(N, np.float32); i0, i1 = int(t0 * SR), int(t1 * SR)
    e[i0:i1] = np.sin(np.linspace(0, np.pi, i1 - i0)) ** .6; return c * e
def boom(dur=2.2, f0=55):
    n = int(dur * SR); x = np.arange(n) / SR
    s = np.sin(2 * np.pi * (f0 * x + 25 * (1 - np.exp(-x * 8)) / 8)) * np.exp(-x * 2.2) + .5 * np.sin(2 * np.pi * f0 * 2 * x) * np.exp(-x * 3)
    return s.astype(np.float32)
def door_bang():
    n = int(1.4 * SR); x = np.arange(n) / SR
    crack = bp(rng.standard_normal(n).astype(np.float32) * np.exp(-x * 28), 300, 4000) * 1.6
    return reverb(boom(1.4, 62) * 1.1 + crack, 1.8, .4)
def thunder(dur=4.5, dist=1.0):
    n = int(dur * SR); x = np.arange(n) / SR; noise = rng.standard_normal(n).astype(np.float32)
    env = (1 - np.exp(-x * 9)) * np.exp(-x * .75) * (1 + .5 * np.sin(2 * np.pi * .9 * x) ** 2)
    return ((lp(noise, 160) * 6 + bp(noise, 900, 4500) * np.exp(-x * 5) * (1.2 / dist)) * env * (.9 / dist)).astype(np.float32)
def rain(N, t0):
    r = np.zeros(N, np.float32); nr = N - int(t0 * SR)
    base = bp(rng.standard_normal(nr).astype(np.float32), 1200, 7000) * .5; drops = np.zeros(nr, np.float32)
    for k in range(int(nr / SR * 40)):
        i = rng.integers(0, nr - 400); drops[i:i + 400] += rng.standard_normal(400).astype(np.float32) * np.exp(-np.linspace(0, 12, 400)) * rng.uniform(.1, .4)
    r[int(t0 * SR):] = (base + bp(drops, 1500, 8000)) * np.minimum(1, np.arange(nr) / (2 * SR)); return r
def footsteps(N, t0, t1, rate=1.8, g=.5):
    f = np.zeros(N, np.float32); t = t0
    while t < t1:
        n = int(.12 * SR); x = np.arange(n) / SR
        s = (np.sin(2 * np.pi * 900 * x) * np.exp(-x * 90) + bp(rng.standard_normal(n).astype(np.float32), 1500, 6000) * np.exp(-x * 60) * .6) * g
        add(f, t, s.astype(np.float32)); t += 1 / rate
    return reverb(f, .9, .3)
def sting():
    n = int(2.4 * SR); x = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * hz(m) * x) for m in (81, 82, 87)) * np.exp(-x * 1.2) * (1 - np.exp(-x * 40))
    return (s * .25).astype(np.float32) + boom(2.4, 48) * .8
def thriller(N, t0, t_end):
    x = np.arange(N) / SR
    def tone(f, a): return (np.sin(2 * np.pi * f * x) + .5 * np.sin(4 * np.pi * f * x) + .25 * np.sin(6 * np.pi * f * x)) * a
    drone = (tone(hz(45), 1) + tone(hz(46), .7) + tone(hz(57), .5) + tone(hz(58), .35)) * (1 + .3 * np.sin(2 * np.pi * .13 * x))
    pno = np.zeros(N, np.float32); motif = [57, 60, 64, 63, 57, 65, 64, 58]; tt = t0
    while tt < t_end:
        for k, m in enumerate(motif):
            n = int(2 * SR); y = np.arange(n) / SR
            add(pno, tt + k * .9, (np.sin(2 * np.pi * hz(m) * y) * np.exp(-y * 1.8) * .3).astype(np.float32))
        tt += 7.2
    g = np.clip((x - t0) / 4, 0, 1)
    return reverb(((drone * .05 + pno * .6) * g).astype(np.float32), 2.2, .3)
def envelope_fps(x, fps):
    hop = SR // fps; n = len(x) // hop
    e = np.array([np.sqrt(np.mean(x[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    return (e / (e.max() + 1e-9)).round(3).tolist()
