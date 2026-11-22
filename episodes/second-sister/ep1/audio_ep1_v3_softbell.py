#!/usr/bin/env python3
"""Church-style score for the subtitle-only cut of EP1 (no voices yet). All sounds are synthesised here.
Layers: pipe organ chords + pedal, monastic chant choir ('aah/ooh', modal melody), piano, music box lullaby 'ลูกนกน้อย',
church bells, low hits on shocks, all sent through a large stone-church reverb.
Each scene gets a mood (calm / sacred / eerie / memory / shock / title) that sets how loud each layer is, so the music
swells and drops with the story; every scene also builds a little toward its end.
Output: music_ep1.wav (stereo 48 kHz). Wind is mixed under it in assemble_ep1.sh.
"""
import json, os, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(HERE, "ep1_timeline.json")))
SR = 48000
TOTAL = TL["total"]
N = int((TOTAL + 6) * SR)
rng = np.random.default_rng(7)
def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

# ---------------- moods per stage ----------------
MOOD = {}
for st in "refectory condo call email gate guestroom kitchen veranda dawn_walk path_dawn garden".split(): MOOD[st] = "calm"
for st in "mass chapel_v1".split(): MOOD[st] = "sacred"
for st in "tower_fog tower_night rosa_bed rosa_room oldwing chapel_night thana_night archive cemetery cemetery_wide drain steps sisters_ext clock rules1 rules7 note count".split(): MOOD[st] = "eerie"
for st in "flash_dorm dream album doll tag music".split(): MOOD[st] = "memory"
for st in "body_sheet police evidence_wall hand lefthand question".split(): MOOD[st] = "shock"
MOOD["title"] = "title"
#            organ choir piano box  pedal
GAIN = {"calm":   (.30, .00, .55, .00, .25),
        "sacred": (.75, .70, .00, .00, .60),
        "eerie":  (.45, .60, .15, .00, .70),
        "memory": (.20, .00, .55, .45, .20),
        "shock":  (.85, .80, .00, .00, 1.0),
        "title":  (1.0, .70, .00, .00, 1.0)}
LAYERS = ["organ", "choir", "piano", "box", "pedal"]

CR = 50  # control rate (Hz)
nc = int((TOTAL + 6) * CR)
ctrl = {k: np.zeros(nc) for k in LAYERS}
segs = [s for s in TL["segments"]]
mood_at = []
for s in segs:
    m = "eerie" if s["type"] == "video" else MOOD.get(s["stage"], "calm")
    s["mood"] = m
    a, b = int(s["t0"] * CR), int((s["t0"] + s["dur"]) * CR)
    for k, g in zip(LAYERS, GAIN[m]): ctrl[k][a:b] = g
# each scene builds toward its end (cliffhanger) by up to +40 %
scenes = {}
for s in segs: scenes.setdefault(s["scene"], [s["t0"], 0]); scenes[s["scene"]][1] = s["t0"] + s["dur"]
build = np.ones(nc)
for sc, (a, b) in scenes.items():
    ia, ib = int(a * CR), int(b * CR)
    x = np.linspace(0, 1, ib - ia)
    build[ia:ib] = 1 + .4 * np.clip((x - .6) / .4, 0, 1) ** 2
# last scene of the episode: full swell
build[int(scenes[max(scenes)][0] * CR):] *= 1.25
def smooth(v, sec):
    k = int(sec * CR); c = np.cumsum(np.concatenate([np.zeros(k), v, np.full(k, v[-1])]))
    return (c[2 * k:] - c[:-2 * k])[:len(v)] / (2 * k) if k else v
hush = np.ones(nc)
for s in segs:
    for a, d in s.get("hush", []):
        hush[int((s["t0"] + a) * CR):int((s["t0"] + a + d) * CR)] = 0
for k in LAYERS: ctrl[k] = smooth(ctrl[k] * build, 1.6)
hush_s = np.minimum(hush, smooth(hush, .5))      # cut fast, come back softly
for k in LAYERS: ctrl[k] = ctrl[k] * hush_s
def gain_at(layer, t): return float(ctrl[layer][min(nc - 1, int(t * CR))])
def gain_curve(layer, t0, n): return np.interp(t0 + np.arange(n) / SR, np.arange(nc) / CR, ctrl[layer]).astype(np.float32)

# two buses: music (organ, choir, piano, box) and effects (bells, hits, puff); music sits lower than the effects
BUSES = {"music": [np.zeros(N, np.float32), np.zeros(N, np.float32)], "fx": [np.zeros(N, np.float32), np.zeros(N, np.float32)]}
BUS = "music"
def add(sig, t0, pan=0.0, vol=1.0):
    L, Rr = BUSES[BUS]
    i = int(t0 * SR)
    if i >= N: return
    sig = sig[:N - i] * vol
    L[i:i + len(sig)] += sig * (1 - pan) * .5 ** .5 * 1.41 / 2 + sig * .35 * (1 - abs(pan))
    Rr[i:i + len(sig)] += sig * (1 + pan) * .5 ** .5 * 1.41 / 2 + sig * .35 * (1 - abs(pan))

def env_adsr(n, a, r):
    e = np.ones(n, np.float32); na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na); e[n - nr:] *= np.linspace(1, 0, nr); return e

# ---------------- organ: chord progression (D aeolian/dorian), 6 s per chord, 1.5 s overlap ----------------
PROG = [[50, 57, 62, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 60], [43, 50, 55, 58], [50, 57, 62, 64, 65]]
DRAW = [(1, 1), (2, .55), (3, .28), (4, .3), (6, .12), (8, .12)]
def organ_note(f, dur, trem=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    s = sum(a * np.sin(2 * np.pi * f * h * t + h) for h, a in DRAW)
    if trem: s *= 1 + trem * np.sin(2 * np.pi * 5.2 * t)
    return (s * env_adsr(n, .35, 1.2)).astype(np.float32)
STEP, OV = 6.0, 1.5
t = 0.0; ci = 0
while t < TOTAL:
    g = gain_curve("organ", t, int((STEP + OV) * SR))
    if g.max() > .02:
        trem = .12 if gain_at("choir", t) > .3 else 0
        for m in PROG[ci % len(PROG)]:
            add(organ_note(hz(m), STEP + OV, trem) * g, t, pan=(m - 56) / 30, vol=.022)
    gp = gain_curve("pedal", t, int((STEP + OV) * SR))
    if gp.max() > .02:
        root = PROG[ci % len(PROG)][0] - 12
        add((organ_note(hz(root), STEP + OV) + .6 * organ_note(hz(root - 12), STEP + OV)) * gp, t, vol=.03)
    t += STEP; ci += 1

# ---------------- chant choir: modal plainchant-style melody, sung 'aah'/'ooh' by 4 voices ----------------
VOWELS = {"a": [(700, 1, 110), (1150, .5, 120), (2800, .12, 200)], "o": [(450, 1, 90), (800, .45, 100), (2830, .08, 200)]}
def choir_note(f, dur, vowel, seed):
    n = int(dur * SR); t = np.arange(n) / SR; out = np.zeros(n)
    r = np.random.default_rng(seed)
    for v in range(4):
        fv = f * 2 ** (r.uniform(-8, 8) / 1200); vr = r.uniform(4.6, 5.6); vd = .006
        ph0 = 2 * np.pi * fv * (t - vd / (2 * np.pi * vr) * np.cos(2 * np.pi * vr * t + r.uniform(0, 6)))
        for k in range(1, 22):
            fk = fv * k
            if fk > 4500: break
            amp = sum(A / (1 + ((fk - F) / BW) ** 2) for F, A, BW in VOWELS[vowel]) / k ** .3
            out += amp * np.sin(k * ph0 + r.uniform(0, 6))
    return (out * env_adsr(n, .25, .45) / 10).astype(np.float32)
# D dorian, men's range; phrases rise and fall step-wise and close on D or A
SCALE = [48, 50, 52, 53, 55, 57, 59, 60, 62]
PHRASES = [[1, 2, 3, 2, 1, 1], [1, 3, 4, 5, 4, 3, 2, 3], [5, 5, 4, 5, 6, 5, 4, 3, 1], [3, 4, 5, 6, 5, 4, 4], [1, 2, 3, 4, 3, 2, 1]]
DURS = [1.6, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.6]
t = 0.0; pi = 0; seed = 0
while t < TOTAL:
    if gain_at("choir", t) < .03 and gain_at("choir", t + 3) < .03: t += 1.0; continue
    ph = PHRASES[pi % len(PHRASES)]; pi += 1
    vowel = "a" if pi % 3 else "o"
    # drone on D underneath the phrase ("mmm" -> 'o' vowel, octave below)
    ptot = sum(DURS[min(i, len(DURS) - 1)] if i < len(ph) - 1 else 2.6 for i in range(len(ph)))
    add(choir_note(hz(38), ptot + 1, "o", seed) * gain_curve("choir", t, int((ptot + 1) * SR)), t, vol=.5); seed += 1
    for i, deg in enumerate(ph):
        d = 2.6 if i == len(ph) - 1 else DURS[min(i, len(DURS) - 1)]
        add(choir_note(hz(SCALE[deg]), d + .35, vowel, seed) * gain_curve("choir", t, int((d + .35) * SR)), t, pan=-.15, vol=.75)
        seed += 1; t += d
    t += 1.8

# ---------------- piano ----------------
def piano_note(f, dur=4.0, vel=1.0):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n); B = .0004
    for k in range(1, 10):
        fk = k * f * np.sqrt(1 + B * k * k)
        if fk > 9000: break
        dec = .9 + .55 * k + f / 600
        for det in (-.6, .6):
            s += (vel / k ** 1.1) * np.sin(2 * np.pi * (fk + det) * t + k) * np.exp(-t * dec)
    s *= np.minimum(1, t / .003)
    return (s / 4).astype(np.float32)
LULL = [(69, 1), (72, 1), (71, .5), (69, .5), (67, 1), (64, 2), (65, 1), (67, 1), (69, .5), (67, .5), (65, 1), (64, 2),
        (69, 1), (72, 1), (76, 1.5), (74, .5), (72, 1), (71, 1), (69, 3)]
BEAT = .6
# calm / eerie: sparse falling arpeggios on the current organ chord; memory: the lullaby, music box doubling an octave up
for s in segs:
    m = s["mood"]
    if m in ("calm", "eerie") and s["type"] == "html":
        t = s["t0"] + .3
        while t < s["t0"] + s["dur"] - .5:
            g = gain_at("piano", t)
            chord = PROG[int(t // STEP) % len(PROG)]
            notes = [chord[-1] + 12, chord[2] + 12, chord[1] + 12, chord[2] + 12] if m == "calm" else [chord[0] + 24, chord[0] + 25]
            for k, mm in enumerate(notes):
                add(piano_note(hz(mm), 3.5, .8 if k == 0 else .55) * g, t + k * (.75 if m == "calm" else 1.4), pan=(mm - 64) / 24, vol=.6)
            t += 4.5 if m == "calm" else 7.5
    if m == "memory":
        t = s["t0"] + .4; end = s["t0"] + s["dur"] - .4
        while t < end:
            for mm, beats in LULL:
                if t >= end: break
                g = gain_at("piano", t)
                add(piano_note(hz(mm), 3.0, .9) * g, t, pan=.05, vol=.7)
                bass = [45, 41, 48, 40][int((t - s["t0"]) // (4 * BEAT)) % 4]
                if beats >= 1: add(piano_note(hz(bass), 3.0, .5) * g, t, pan=-.3, vol=.45)
                n_ = int(1.6 * SR); tt = np.arange(n_) / SR; f = hz(mm + 24)
                box = (np.sin(2 * np.pi * f * tt) + .3 * np.sin(2 * np.pi * 4.02 * f * tt) * np.exp(-tt * 9)) * np.exp(-tt * 2.8)
                add(box.astype(np.float32) * gain_at("box", t), t, pan=.35, vol=.12)
                t += beats * BEAT
            t += 2 * BEAT

# ---------------- shock hits: low boom + organ cluster swell at the start of each shock segment ----------------
def boom(dur=3.0):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 34 + 26 * np.exp(-t * 3)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 1.6)
    noise = np.convolve(rng.standard_normal(n), np.ones(40) / 40, "same") * np.exp(-t * 6)
    return (s + .5 * noise).astype(np.float32)
BUS = "fx"
prev = None
for s in segs:
    if s["mood"] in ("shock", "title") and prev != s["mood"]:
        add(boom(), s["t0"], vol=.55)
        for m in (38, 39, 50):
            add(organ_note(hz(m), 4.0) * np.linspace(.2, 1, int(4 * SR)).astype(np.float32), s["t0"], vol=.03)
    prev = s["mood"]

# ---------------- church bells (louder, deep, three tolls) ----------------
def bell(dur=8.0, f0=147.0):
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for ratio, amp, dec in [(.5, .7, .3), (1, 1, .45), (1.2, .6, .7), (1.5, .5, .8), (2, .45, 1.0), (2.5, .25, 1.5), (2.67, .3, 1.6), (3.0, .2, 2.0), (4.0, .12, 2.8)]:
        s += amp * np.sin(2 * np.pi * f0 * ratio * t + ratio) * np.exp(-t * dec) * (1 + .08 * np.sin(2 * np.pi * 1.3 * t))
    s *= np.minimum(1, t / .003)
    clang = rng.standard_normal(int(.05 * SR)) * np.exp(-np.arange(int(.05 * SR)) / SR * 80)
    s[:len(clang)] += .4 * clang
    return (s / 2.6).astype(np.float32)
BELL = bell()
for s in segs:
    for b, cnt, bv in s.get("bells", []):
        for rep in range(cnt):
            add(BELL, s["t0"] + b + rep * 2.6, pan=.1, vol=1.15 * bv)

# scare stinger: sub boom + bright dissonant string-like stab
def stinger(dur=2.6):
    n = int(dur * SR); t = np.arange(n) / SR; out = boom(dur) * .9
    for f in (622.3, 659.3, 698.5, 1244.5):
        out += .12 * np.sign(np.sin(2 * np.pi * f * t + f)) * np.exp(-t * 2.2) * np.minimum(1, t / .01)
    return out.astype(np.float32)
STING = stinger()
for s in segs:
    for a in s.get("stingers", []):
        add(STING, s["t0"] + a, vol=.75)

# candle puff in the Rosa clip
for s in segs:
    if s["type"] == "video":
        n = int(.35 * SR)
        add((rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 9)).astype(np.float32), s["t0"] + 7.65, vol=.05)

# ---------------- stone-church reverb (FFT convolution, decorrelated L/R) ----------------
def ir(seed, rt=3.6):
    n = int(rt * SR); t = np.arange(n) / SR; r = np.random.default_rng(seed)
    e = r.standard_normal(n) * np.exp(-6.9 * t / rt)
    e = np.convolve(e, np.ones(6) / 6, "same")            # darker tail
    e[:int(.02 * SR)] = 0                                  # pre-delay
    return (e / np.sqrt((e ** 2).sum())).astype(np.float32)
def convolve(x, h, block=1 << 20):
    nfft = 1 << int(np.ceil(np.log2(block + len(h))))
    H = np.fft.rfft(h, nfft); y = np.zeros(len(x) + len(h), np.float32)
    for i in range(0, len(x), block):
        seg = x[i:i + block]
        y[i:i + nfft] += np.fft.irfft(np.fft.rfft(seg, nfft) * H, nfft)[:min(nfft, len(y) - i)].astype(np.float32)
    return y[:len(x)]
MUSIC_LEVEL = .5   # user: music softer, effects at full level
mL, mR = BUSES["music"]; fL, fR = BUSES["fx"]
L, Rr = MUSIC_LEVEL * mL + fL, MUSIC_LEVEL * mR + fR
del BUSES
wetL, wetR = convolve(L, ir(1)), convolve(Rr, ir(2))
outL, outR = .62 * L + .55 * wetL, .62 * Rr + .55 * wetR
peak = max(np.abs(outL).max(), np.abs(outR).max())
scale = .89 / peak
pcm = (np.stack([outL, outR], 1) * scale * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "music_ep1.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"music_ep1.wav {TOTAL / 60:.1f} min stereo, normalised x{scale:.2f}")
