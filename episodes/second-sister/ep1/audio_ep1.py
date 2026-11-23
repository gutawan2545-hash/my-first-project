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
# master revision: music follows the situation
MOOD.update({"school": "calm", "grotto": "grotto", "steps": "tension", "doll": "tension", "police": "police", "question": "choice",
             "call_mek": "eerie", "tower_night": "eerie"})
#            organ choir piano box  pedal
GAIN = {"calm":   (.30, .00, .55, .00, .25),
        "sacred": (.75, .70, .00, .00, .60),
        "eerie":  (.45, .60, .15, .00, .70),
        "memory": (.20, .00, .55, .45, .20),
        "shock":  (.85, .80, .00, .00, 1.0),
        "title":  (1.0, .70, .00, .00, 1.0),
        "grotto": (.32, .38, .10, .00, .30),     # still, sacred, a little mysterious
        "tension":(.18, .22, .00, .00, .95),     # finding the doll / Agnes: low pressure that builds
        "police": (.12, .00, .00, .00, .55),     # serious, almost no melody: the real-world sounds carry it
        "choice": (.10, .00, .00, .00, .50)}
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
hush = np.ones(nc)
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
for s in segs:
    for a, d in s.get("hush", []):
        hush[int((s["t0"] + a) * CR):int((s["t0"] + a + d) * CR)] = 0
for s in segs:
    if s.get("moves") and any(m.get("clip") for m in s["moves"]):          # Agnes peeks: tension build-up under her walk
        a, b = int(s["t0"] * CR), int((s["t0"] + s["dur"]) * CR)
        ramp = np.linspace(.6, 1.5, b - a)
        for k_, g_ in zip(LAYERS, GAIN["tension"]): ctrl[k_][a:b] = g_ * ramp
    for ts, amp in s.get("shakes", []):
        i0 = int((s["t0"] + ts - .9) * CR); hush[max(0, i0):int((s["t0"] + ts) * CR)] = 0
for k in LAYERS: ctrl[k] = smooth(ctrl[k] * build, 1.6)
hush_s = np.minimum(hush, smooth(hush, .5))      # cut fast, come back softly
for k in LAYERS: ctrl[k] = ctrl[k] * hush_s
def gain_at(layer, t): return float(ctrl[layer][min(nc - 1, int(t * CR))])
def gain_curve(layer, t0, n): return np.interp(t0 + np.arange(n) / SR, np.arange(nc) / CR, ctrl[layer]).astype(np.float32)

# two buses: music (organ, choir, piano, box) and effects (bells, hits, puff); music sits lower than the effects
BUSES = {k: [np.zeros(N, np.float32), np.zeros(N, np.float32)] for k in ("music", "fx", "bell", "amb")}
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
def bell(dur=9.0, f0=131.0):
    """Big cast church bell: hum, prime, minor-third tierce, quint, nominal + upper partials, each as a slightly
    detuned pair so the tone warbles like a real bell, plus a bright metallic strike at the start."""
    n = int(dur * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for ratio, amp, dec in [(.5, .9, .22), (1, 1, .35), (1.183, .8, .45), (1.506, .55, .6), (2, .75, .5), (2.514, .4, .9),
                            (2.662, .45, 1.0), (3.011, .35, 1.3), (4.166, .25, 1.9), (5.433, .18, 2.6), (6.796, .12, 3.4)]:
        f = f0 * ratio
        s += amp * (np.sin(2 * np.pi * f * t + ratio) + np.sin(2 * np.pi * (f + .7 + ratio * .25) * t)) * .5 * np.exp(-t * dec)
    strike = np.zeros(n); m = int(.25 * SR); tt = t[:m]
    for f in (2793, 3317, 3951, 4699, 5588):
        strike[:m] += np.sin(2 * np.pi * f * tt + f) * np.exp(-tt * 28)
    strike[:m] += .5 * rng.standard_normal(m) * np.exp(-tt * 60)
    s = s + .45 * strike
    s *= np.minimum(1, t / .002)
    s = np.tanh(1.8 * s / np.abs(s).max()) / np.tanh(1.8)   # dense, loud body
    return s.astype(np.float32)
def bandnoise(n, lo, hi, seed=0):
    x = np.random.default_rng(seed).standard_normal(n); X = np.fft.rfft(x); f = np.fft.rfftfreq(n, 1 / SR)
    X[(f < lo) | (f > hi)] = 0; y = np.fft.irfft(X, n); return (y / (np.abs(y).max() + 1e-9)).astype(np.float32)
BELL = bell()
# eerie version (user: loud and haunting, three tolls): a ghost copy a little flat and late so the tone beats and wavers,
# a low swell rising into the first strike, and a cold high shimmer hanging in the tail
def ghost_bell():
    b = BELL; n = len(b); idx = np.arange(n) * .972               # 2.8 % flat
    g = np.interp(idx, np.arange(n), b).astype(np.float32)
    g = np.concatenate([np.zeros(int(.045 * SR), np.float32), g])[:n]
    t = np.arange(n) / SR
    shimmer = (np.sin(2 * np.pi * 1863 * t) * .5 + np.sin(2 * np.pi * 1971 * t) * .5) * np.minimum(1, t / 1.2) * np.exp(-t * .45) * .12
    return (b + .55 * g + shimmer).astype(np.float32)
GBELL = ghost_bell()
def swell(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 41 * t) * (t / dur) ** 2 * .6 + bandnoise(n, 60, 300, 21) * (t / dur) ** 3 * .25).astype(np.float32)
BUS = "bell"
BELL_TIMES = []
for s in segs:
    for b, cnt, bv in s.get("bells", []):
        t0 = s["t0"] + b
        add(swell(), max(0, t0 - 1.6), vol=.8)
        for rep in range(3):                                         # always three tolls, slow and heavy
            add(GBELL, t0 + rep * 3.1, pan=(-.15, .15, 0)[rep], vol=1.4 * max(bv, .9))
            BELL_TIMES.append(t0 + rep * 3.1)

# scare stinger: sub boom + bright dissonant string-like stab
def stinger(dur=2.6):
    n = int(dur * SR); t = np.arange(n) / SR; out = boom(dur) * .9
    for f in (622.3, 659.3, 698.5, 1244.5):
        out += .12 * np.sign(np.sin(2 * np.pi * f * t + f)) * np.exp(-t * 2.2) * np.minimum(1, t / .01)
    return out.astype(np.float32)
STING = stinger()
BUS = "fx"
for s in segs:
    for a in s.get("stingers", []):
        add(STING, s["t0"] + a, vol=.75)

# candle puff in the Rosa clip
for s in segs:
    if s["type"] == "video":
        n = int(.35 * SR)
        add((rng.standard_normal(n) * np.exp(-np.arange(n) / SR * 9)).astype(np.float32), s["t0"] + 7.65, vol=.05)

# ---------------- master revision: sound effects tied to the picture ----------------
def whoosh(dur=.6, seed=1):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    env = np.sin(np.pi * np.clip(t / .75, 0, 1)) ** 2 * np.where(t > .75, np.exp(-(t - .75) * 14), 1)
    return (bandnoise(n, 250, 5200, seed) * env).astype(np.float32)
def click():
    n = int(.06 * SR); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1350 * t) * np.exp(-t * 90) * .7 + np.sin(2 * np.pi * 2700 * t) * np.exp(-t * 160) * .25).astype(np.float32)
def impact(dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 30 + 30 * np.exp(-t * 5); body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.4)
    return (body + .35 * bandnoise(n, 40, 400, 9) * np.exp(-t * 9)).astype(np.float32)
def siren(dur, seed=3):   # far-off siren wail + police radio chatter + an idling engine
    n = int(dur * SR); t = np.arange(n) / SR
    f = 760 + 280 * np.sin(2 * np.pi * t / 1.7)
    wail = np.sin(2 * np.pi * np.cumsum(f) / SR) * .25 * (np.clip(1 - t / dur, 0, 1) ** .5)
    eng = np.sin(2 * np.pi * 31 * t) * (.5 + .5 * np.sin(2 * np.pi * 7 * t)) * .25 + bandnoise(n, 30, 160, seed) * .25
    radio = np.zeros(n, np.float32); r = np.random.default_rng(seed)
    for _ in range(int(dur / 4)):
        a = int(r.uniform(.5, dur - 2) * SR); d = int(r.uniform(.8, 1.8) * SR)
        burst = bandnoise(d, 500, 2800, int(a)) * (.5 + .5 * np.sign(np.sin(2 * np.pi * r.uniform(5, 9) * np.arange(d) / SR)))
        radio[a:a + d] += burst * .45; radio[a:a + 300] += .8; radio[a + d - 300:a + d] += .6   # squelch clicks
    return (wail + eng + radio).astype(np.float32)
def water(dur, seed=4):   # canal lapping against stone steps, drips, soft wind
    n = int(dur * SR); t = np.arange(n) / SR
    lap = bandnoise(n, 60, 900, seed) * (.45 + .4 * np.sin(2 * np.pi * .35 * t) ** 2)
    wind = bandnoise(n, 120, 700, seed + 1) * .25 * (.6 + .4 * np.sin(2 * np.pi * .08 * t))
    out = lap + wind; r = np.random.default_rng(seed)
    for _ in range(int(dur * .7)):
        a = int(r.uniform(0, dur - .3) * SR); m = int(.25 * SR); tt = np.arange(m) / SR
        out[a:a + m] += np.sin(2 * np.pi * r.uniform(1100, 2100) * tt * (1 - tt)) * np.exp(-tt * 22) * .4
    return out.astype(np.float32)
def kids(dur, seed=5):    # far-away schoolchildren fading out, wind, one gecko call
    n = int(dur * SR); t = np.arange(n) / SR
    chat = bandnoise(n, 300, 2600, seed) * (.5 + .5 * np.sin(2 * np.pi * 5.3 * t) * np.sin(2 * np.pi * 3.1 * t)) * np.clip(1 - t / dur, 0, 1) * .5
    wind = bandnoise(n, 100, 600, seed + 2) * .2
    out = chat + wind
    g0 = int(min(dur - 1.6, dur * .6) * SR)
    for k in range(4):   # "tok-kae": two-tone croak, repeated
        a = g0 + int(k * .32 * SR); m = int(.16 * SR); tt = np.arange(m) / SR
        tone = np.sign(np.sin(2 * np.pi * (330 if k % 2 == 0 else 260) * tt)) * np.exp(-tt * 18) * .35
        out[a:a + m] += tone[:max(0, min(m, n - a))]
    return out.astype(np.float32)
def clatter(seed=11):   # a metal tray dropped on a tiled floor: hit, two bounces, a rattle that settles
    n = int(1.4 * SR); t = np.arange(n) / SR; out = np.zeros(n, np.float32); r = np.random.default_rng(seed)
    for at, g in ((0, 1.0), (.17, .55), (.29, .35), (.37, .2)):
        a = int(at * SR); m = n - a; tt = np.arange(m) / SR
        ring = sum(np.sin(2 * np.pi * f * tt + r.uniform(0, 6)) * np.exp(-tt * d) for f, d in ((1240, 9), (1873, 11), (2710, 14), (3420, 18), (610, 7)))
        out[a:] += (ring * .22 + bandnoise(m, 1500, 8000, seed + a) * np.exp(-tt * 40) * .8) * g
    rat = int(.42 * SR); m = n - rat; tt = np.arange(m) / SR
    out[rat:] += bandnoise(m, 2000, 6000, seed + 7) * (.5 + .5 * np.sign(np.sin(2 * np.pi * (28 + 30 * tt) * tt))) * np.exp(-tt * 6) * .25
    return out
BUS = "fx"
for i_, s in enumerate(segs):
    if s.get("zb"): add(whoosh(seed=i_), max(0, s["t0"] - .3), pan=0, vol=.5)               # zoom-blur cut
    for ts, amp in s.get("shakes", []): add(impact(), s["t0"] + ts, vol=.9 * amp)            # bass hit on the shake
    if s.get("clatter") is not None: add(clatter(), s["t0"] + s["clatter"], pan=.35, vol=.75)   # tray dropped outside the kitchen door
    if s.get("blow"):   # the child blows her candle out: a soft breath "fuu", then the wick's tiny hiss
        n = int(.7 * SR); t = np.linspace(0, 1, n)
        puff = bandnoise(n, 500, 4200, 77) * np.sin(np.pi * np.clip(t / .35, 0, 1)) ** 2 * np.where(t > .35, np.exp(-(t - .35) * 7), 1)
        add(puff.astype(np.float32), s["t0"] + s["blow"]["blow"] - .15, pan=0, vol=.18)   # faint, like a breath from nowhere
        m = int(.5 * SR); add((bandnoise(m, 2500, 7000, 78) * np.exp(-np.arange(m) / SR * 8)).astype(np.float32), s["t0"] + s["blow"]["blow"] + .3, vol=.12)
BUS = "amb"
for i_, s in enumerate(segs):
    st = s.get("stage")
    if st == "police":   # loud as the police pull in, then down low under the talk (user)
        sr = siren(s["dur"], i_); tt = np.arange(len(sr)) / SR
        sr *= np.interp(tt, [0, 3.5, 6.5, s["dur"]], [1.0, 1.0, .25, .18]).astype(np.float32)
        add(sr, s["t0"], pan=-.3, vol=.42)
    elif st == "grotto": add(water(s["dur"], i_), s["t0"], vol=.22)
    elif st == "school": add(kids(s["dur"], i_), s["t0"], pan=.2, vol=.2)
    for c in s.get("clicks", []): add(click(), s["t0"] + c, pan=.1, vol=.3)                  # choice UI clicks, dry and close

# ---------------- AI score (user): ElevenLabs Music cues replace the synth layers; loudness rises and falls all the time ----------------
AI_DIR = os.path.join(HERE, "music_ai")
AI_TRACK = {"calm": "calm", "grotto": "calm", "sacred": "test_chant", "title": "test_chant", "eerie": "test_night",
            "memory": "memory", "tension": "tension", "shock": "tension", "police": "aftermath", "choice": "ending"}
AI_LEVEL = {"calm": .5, "grotto": .5, "sacred": .85, "title": 1.0, "eerie": .7, "memory": .65, "tension": .8, "shock": 1.0, "police": .5, "choice": .9}
AI = all(os.path.exists(os.path.join(AI_DIR, f + ".mp3")) for f in set(AI_TRACK.values()))
if AI:
    import subprocess as _sp
    def _load(name):
        raw = _sp.run(["ffmpeg", "-v", "error", "-i", os.path.join(AI_DIR, name + ".mp3"), "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).reshape(-1, 2).copy()
        x = x[int(.3 * SR):len(x) - int(1.2 * SR)]                       # skip the silent lead-in and the fade at the end
        return x / max(1e-4, np.sqrt(np.mean(x ** 2)))                  # one loudness for every cue
    TR = {n: _load(n) for n in set(AI_TRACK.values())}
    def _loop(x, n, off, xf=int(2.0 * SR)):
        out = np.zeros((n, 2), np.float32); pos = 0; i = off % (len(x) - xf)
        while pos < n:
            take = min(len(x) - i, n - pos)
            piece = x[i:i + take].copy()
            if pos > 0:
                k = min(xf, take); piece[:k] *= np.linspace(0, 1, k)[:, None]
            if take == len(x) - i and pos + take < n:
                k = min(xf, take); piece[-k:] *= np.linspace(1, 0, k)[:, None]
            out[pos:pos + take] += piece
            pos += take - (xf if take == len(x) - i else 0); i = 0
        return out
    runs = []
    for sg in segs:
        tr = AI_TRACK.get(sg["mood"], "calm")
        if runs and runs[-1][0] == tr: runs[-1][2] = sg["t0"] + sg["dur"]
        else: runs.append([tr, sg["t0"], sg["t0"] + sg["dur"], sg["mood"]])
    mus = np.zeros((N, 2), np.float32); rr = np.random.default_rng(9)
    for tr, a, b, md in runs:
        i0 = int(max(0, a - .8) * SR); i1 = min(N, int((b + 1.2) * SR)); n = i1 - i0
        if n <= 0: continue
        x = _loop(TR[tr], n, int(rr.uniform(0, len(TR[tr]) * .6)))
        fi, fo = min(n, int(1.6 * SR)), min(n, int(2.0 * SR))
        x[:fi] *= np.linspace(0, 1, fi)[:, None]; x[-fo:] *= np.linspace(1, 0, fo)[:, None]
        mus[i0:i1] += x * AI_LEVEL.get(md, .6)
    tt = np.arange(N) / SR
    wave_ = 10 ** ((5 * np.sin(2 * np.pi * tt / 23) + 2.5 * np.sin(2 * np.pi * tt / 9.5 + 1.1)) / 20)   # always rising or falling, never one flat level
    cur = np.interp(tt, np.arange(nc) / CR, smooth(build, 1.6) * hush_s).astype(np.float32)          # scene build-ups and the silences before scares
    mus *= (wave_ * cur)[:, None].astype(np.float32)
    BUSES["music"] = [mus[:, 0].copy(), mus[:, 1].copy()]; del mus
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
# levels (user): bells very loud and clear, scares at full level, music clearly underneath
def wet(bus, dry=.62, rev=.55):
    l, r = BUSES[bus]; return dry * l + rev * convolve(l, ir(1)), dry * r + rev * convolve(r, ir(2))
bl, br = wet("bell", .8, .45); fl, fr = wet("fx"); ml, mr = wet("music", 1.0, .12) if AI else wet("music"); al, ar = BUSES["amb"]   # the AI cues bring their own church room
# ---- dialogue (ElevenLabs takes listed in the timeline): per-line loudness matched, a touch of room, music ducks under it
import subprocess
vo = np.zeros(N, np.float32)
for sg in TL["segments"]:
    items = [list(v) + [0] * (4 - len(v)) for v in sg.get("vo", [])] if sg["type"] == "video" else [[sh["t0"] + sh["vo"][0], sh["vo"][1], sh["vo"][2], (sh["vo"][3] if len(sh["vo"]) > 3 else 0)] for sh in sg["shots"] if sh.get("vo")]
    for at, _, f, gdb in items:
        fp = os.path.join(HERE, f)
        if not os.path.exists(fp): continue
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", fp, "-af", f"atempo={TL.get('vo_tempo', 1)}", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
        x = np.frombuffer(raw, np.float32).copy()
        if not len(x): continue
        rms = np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) if (np.abs(x) > .01).any() else 1
        x *= .16 / max(rms, 1e-4) * 10 ** (gdb / 20)    # one speech level, then the line's own loudness (whisper well under, a cry out above)
        i0 = int((sg["t0"] + at) * SR); i1 = min(N, i0 + len(x))
        if i0 < N: vo[i0:i1] += x[:i1 - i0]
HAS_VO = np.abs(vo).max() > 0
if HAS_VO:
    env = np.convolve(np.abs(vo), np.ones(int(.25 * SR), np.float32) / int(.25 * SR), "same")
    duck = 1 - .6 * np.clip(env / .04, 0, 1)       # music steps well back under the voices
    ml, mr = ml * duck, mr * duck
    vr = convolve(vo, ir(3, .45)); vol_, vor_ = .96 * vo + .035 * vr, .96 * vo + .035 * vr   # just a little room, no echo
bduck = np.ones(N, np.float32)
for bt in BELL_TIMES:
    i0 = int(max(0, bt - .2) * SR); i1 = min(N, int((bt + 2.6) * SR))
    if i0 < N: bduck[i0:i1] = np.minimum(bduck[i0:i1], .35)
bduck = np.convolve(bduck, np.ones(int(.3 * SR), np.float32) / int(.3 * SR), "same")
ml, mr, fl, fr = ml * bduck, mr * bduck, fl * (.5 + .5 * bduck), fr * (.5 + .5 * bduck)

del BUSES
bpk = max(np.abs(bl).max(), np.abs(br).max(), 1e-6)
rest_pk = max(np.abs(ml).max(), np.abs(fl).max(), 1e-6)
if AI:   # level the AI score on its own: music RMS ~ -22 dBFS before ducking; effects keep their own peak level
    rest_pk = max(np.abs(fl).max(), 1e-6)
    _m = np.sqrt(np.mean(ml[np.abs(ml) > 1e-4] ** 2)) if (np.abs(ml) > 1e-4).any() else 1
    ml, mr = ml * (.055 * rest_pk / .38 / _m), mr * (.055 * rest_pk / .38 / _m)   # user: music a little lower (-3 dB)
k = .95 / bpk                                    # bells reach full scale
outL = bl * k + (fl * .80 + ml * .38) / rest_pk + al * .9
outR = br * k + (fr * .80 + mr * .38) / rest_pk + ar * .9
if HAS_VO: outL, outR = outL + vol_, outR + vor_
outL, outR = np.tanh(outL * 1.1) / np.tanh(1.1), np.tanh(outR * 1.1) / np.tanh(1.1)
peak = max(np.abs(outL).max(), np.abs(outR).max())
scale = .95 / peak
pcm = (np.stack([outL, outR], 1) * scale * 32767).astype(np.int16)
with wave.open(os.path.join(HERE, "music_ep1.wav"), "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"music_ep1.wav {TOTAL / 60:.1f} min stereo, normalised x{scale:.2f}")
