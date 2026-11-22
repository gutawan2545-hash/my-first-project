"""Lays out the episode timeline from the voice-line lengths, mixes the preview soundtrack
(temporary voices, drone, muffled/clear ringtone, pen scratches, hard cut at the end) and
writes per-frame mouth-open flags for James (J) and Tawan (T)."""
import json, wave
import numpy as np

SR = 48000; FPS = 24


def load(name):
    with wave.open(f'vo2/{name}.wav') as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a


VO = {n: load(n) for n in ['J1', 'J2', 'J2b', 'T1', 'J3a', 'J3b', 'T2a', 'T2b', 'J4', 'J5a', 'J5b', 'J5', 'J6']}
L = {n: len(a) / SR for n, a in VO.items()}

shots = []          # dicts: key, dur
events = []         # (abs_time, line)
t = 0.0


def shot(key, dur, ev=(), **extra):
    global t
    for line, rel in ev:
        events.append((t + rel, line))
    shots.append(dict(key=key, start=round(t, 3), dur=round(dur, 3), **extra))
    t += dur


shot('hook', 0.3 + L['J1'] + 0.45, [('J1', 0.3)])
shot('headphones', max(4.6, 0.55 + L['J2'] + 0.35), [('J2', 0.55)])
a = 0.2; b = a + L['J2b'] + 0.25
shot('scroll', b + L['T1'] + 0.35, [('J2b', a), ('T1', b)], stop=round(b + L['T1'] * 0.35, 2))
a = 0.45; b = a + L['J3a'] + 0.55
shot('read', b + L['J3b'] + 0.55, [('J3a', a), ('J3b', b)])
shot('write', 3.2, [], pens=[0.25 + k * 0.24 for k in range(10)])
a = 0.35; b = a + L['T2a'] + 0.5
shot('realize', b + L['T2b'] + 0.45, [('T2a', a), ('T2b', b)])
shot('dialpad', 2.7, [], taps=[round(0.25 + k * 0.17, 2) for k in range(10)], call=2.2)
shot('dial', 1.6)                                  # Tawan dials; the ring starts on the cut to Dean
shot('dean', 1.9)                                  # muffled ring, Dean lifts his head at once
shot('tawanlook', 1.6)                             # hang-up on the cut: ring stops, smile drops, eyes up to James, hold
shot('whisper', 0.25 + L['J4'] + 0.35, [('J4', 0.25)])
shot('door', 2.0)                                  # second call: clear ring behind the closed door
shot('ots', 3.6)                                   # over James's shoulder, his hand creeps toward the knob
shot('oldtone', 0.25 + L['J6'] + 0.4, [('J6', 0.25)])
shot('choice', 0.3 + L['J5'] + 1.6, [('J5', 0.3)], hand_stop=1.0, card_in=0.2)
TOTAL = t
S = {s['key']: s for s in shots}

# ---------------- audio ----------------
N = int(TOTAL * SR) + 1
mixJ = np.zeros(N, np.float32); mixT = np.zeros(N, np.float32)
for at, line in events:
    i = int(at * SR); a = VO[line]
    (mixT if line.startswith('T') else mixJ)[i:i + len(a)] += a[:max(0, N - i)]
voice = mixJ + mixT
tt = np.arange(N) / SR


def lowpass(x, fc):
    a = np.exp(-2 * np.pi * fc / SR); y = np.zeros_like(x); acc = 0.0
    for k in range(len(x)):
        acc = (1 - a) * x[k] + a * acc; y[k] = acc
    return y


# ---- eerie score ----
rng = np.random.default_rng(4)
def ramp(t0, t1):
    return np.clip((tt - t0) / max(1e-3, t1 - t0), 0, 1).astype(np.float32)
tension = ramp(S['realize']['start'] - 1.0, S['realize']['start'] + 1.0)          # glassy layer comes in with the clue
calls = ramp(S['dialpad']['start'], S['dialpad']['start'] + 0.8)
low = (0.6 * np.sin(2 * np.pi * 41.2 * tt) + 0.5 * np.sin(2 * np.pi * 43.65 * tt)) * (0.7 + 0.3 * np.sin(2 * np.pi * 0.06 * tt))
pad = (np.sin(2 * np.pi * 196.0 * tt) + 0.8 * np.sin(2 * np.pi * 207.65 * tt + 1.1)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.09 * tt + 2)) * (0.75 + 0.25 * np.sin(2 * np.pi * 5.2 * tt))
vib = 6 * np.sin(2 * np.pi * 4.3 * tt)
glass = (np.sin(2 * np.pi * (1568 + vib) * tt) + 0.7 * np.sin(2 * np.pi * (1661 + vib) * tt)) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.13 * tt))
noise = rng.standard_normal(N).astype(np.float32)
air = np.convolve(noise, np.ones(600) / 600, mode='same') * 3.5
bed = (low * 0.11 + pad * 0.028 * (0.6 + 0.4 * calls) + glass * 0.006 * tension + air * 0.03).astype(np.float32)
# reverse swells into the two twists
for at in [[e for e, l in events if l == 'T2b'][0], S['door']['start']]:
    n = int(1.6 * SR); i0 = int((at - 1.6) * SR); x = np.arange(n) / SR
    sw = (np.sin(2 * np.pi * (220 + 260 * x / 1.6) * x) * 0.4 + np.convolve(rng.standard_normal(n), np.ones(80) / 80, mode='same') * 2.5) * (x / 1.6) ** 2.5
    bed[i0:i0 + n] += (sw * 0.07).astype(np.float32)[:max(0, N - i0)]
# heartbeat from the first ring to the reach (speeds up a little)
hb0 = S['dean']['start']; hb1 = S['ots']['start'] + S['ots']['dur']
t_ = hb0
while t_ < hb1:
    for off, amp in [(0.0, 1.0), (0.22, 0.6)]:
        i0 = int((t_ + off) * SR); n = int(0.18 * SR); x = np.arange(n) / SR
        bed[i0:i0 + n] += (np.sin(2 * np.pi * 52 * x) * np.exp(-x * 26) * 0.22 * amp).astype(np.float32)[:max(0, N - i0)]
    t_ += 0.86 - 0.18 * (t_ - hb0) / (hb1 - hb0)
# floor creak on James's step
i0 = int((S['ots']['start'] + 1.35) * SR); n = int(0.7 * SR); x = np.arange(n) / SR
creak = np.sign(np.sin(2 * np.pi * (180 + 90 * np.sin(2 * np.pi * 1.3 * x)) * x)) * np.exp(-x * 3) * (np.sin(2 * np.pi * 23 * x) > 0)
bed[i0:i0 + n] += (np.convolve(creak, np.ones(30) / 30, mode='same') * 0.05).astype(np.float32)
# level: duck under voices, dip under the clear ring, a touch up on the choice card
venv = np.convolve(np.abs(mixJ + mixT), np.ones(4800) / 4800, mode='same')
duck = 1.0 - 0.45 * np.clip(venv / 0.04, 0, 1)
lvl = np.ones(N, np.float32)
d0 = S['door']['start']; e0 = S['choice']['start']
lvl[int((d0 - 0.15) * SR):] = 0.45
lvl[int(e0 * SR):] = 0.6
lvl = np.convolve(lvl, np.ones(2400) / 2400, mode='same')
bed *= (lvl * duck).astype(np.float32)


# ringtone: short marimba-like phrase that loops
def note(f, dur, amp=1.0):
    n = int(dur * SR); x = np.arange(n) / SR
    env = np.exp(-x * 9)
    return amp * env * (np.sin(2 * np.pi * f * x) + 0.35 * np.sin(2 * np.pi * 2 * f * x) + 0.12 * np.sin(2 * np.pi * 3.01 * f * x))


phrase = np.zeros(int(1.6 * SR), np.float32)
for k, f in enumerate([1318.5, 987.8, 1174.7, 1318.5, 987.8, 783.99]):
    s = int(k * 0.16 * SR); nt = note(f, 0.5)
    phrase[s:s + len(nt)] += nt[:len(phrase) - s]
ring_loop = np.tile(phrase, 40)
ring = np.zeros(N, np.float32)
# muffled ring: from dial+ring_from until hang-up
m0 = S['dean']['start']; m1 = S['tawanlook']['start']
seg = ring_loop[:int((m1 - m0) * SR)]
muff = lowpass(seg, 650) * 0.5
ring[int(m0 * SR):int(m0 * SR) + len(muff)] += muff
# clear ring: from the door shot to the very end (cut mid-ring)
c0 = S['door']['start']
seg = ring_loop[:N - int(c0 * SR)] * 0.42
seg[int((S['choice']['start'] - c0) * SR):] *= 0.5      # a little lower under the question
ring[int(c0 * SR):int(c0 * SR) + len(seg)] += seg

# pen scratches while she writes
sfx = np.zeros(N, np.float32)
for p in S['write']['pens']:
    i = int((S['write']['start'] + p) * SR); n = int(0.16 * SR)
    sc = rng.standard_normal(n).astype(np.float32) * np.hanning(n)
    sc = sc - np.convolve(sc, np.ones(30) / 30, mode='same')
    sfx[i:i + n] += sc * 0.12
# key taps (short two-tone beeps) and the call press on the dial pad
for k, tp in enumerate(S['dialpad']['taps'] + [S['dialpad']['call']]):
    i = int((S['dialpad']['start'] + tp) * SR); n = int(0.07 * SR); x = np.arange(n) / SR
    f1, f2 = [(941, 1336), (852, 1336), (697, 1209), (770, 1336), (770, 1209), (852, 1477), (697, 1336), (852, 1209), (770, 1477), (770, 1336), (600, 900)][k]
    sfx[i:i + n] += ((np.sin(2 * np.pi * f1 * x) + np.sin(2 * np.pi * f2 * x)) * np.hanning(n) * 0.05).astype(np.float32)
# soft phone buzz when the screen lights up in the headphones shot
i = int((S['headphones']['start'] + 0.15) * SR); n = int(0.35 * SR)
sfx[i:i + n] += (np.sign(np.sin(2 * np.pi * 150 * np.arange(n) / SR)) * np.hanning(n) * 0.05).astype(np.float32)

# whoosh on the zoom-blur cuts: band-limited noise rising into the cut, then falling
ZB = ['headphones', 'dean', 'door']          # shots that start with a zoom-blur cut
for k in ZB:
    c = S[k]['start']; S[k]['zb'] = True
    n = int(0.6 * SR); i = int((c - 0.32) * SR)
    x = rng.standard_normal(n).astype(np.float32)
    env = np.concatenate([np.linspace(0, 1, int(n * 0.55)) ** 2, np.linspace(1, 0, n - int(n * 0.55)) ** 1.5]).astype(np.float32)
    y = lowpass(x, 900) * 2.2 - lowpass(x, 120) * 1.5
    sfx[i:i + n] += (y * env * 0.5)[:max(0, N - i)]
# low hit under the two twist moments (camera shake)
for k, rel in [('realize', None), ('door', 0.0)]:
    s = S[k]; at = s['start'] + (rel if rel is not None else [r for r, l in [(e[0] - s['start'], e[1]) for e in events] if l == 'T2b'][0])
    s['shake'] = round(at - s['start'], 2)
    n = int(0.9 * SR); i = int(at * SR); x = np.arange(n) / SR
    sfx[i:i + n] += (np.sin(2 * np.pi * 48 * x) * np.exp(-x * 4.5) * 0.35).astype(np.float32)

# ======== scary layer ========
def reverb(x, dec=1.6, wet=0.35, seed=7):
    n = int(dec * SR); r = np.random.default_rng(seed)
    ir = r.standard_normal(n).astype(np.float32) * np.exp(-np.arange(n) / SR * (6.9 / dec)).astype(np.float32)
    ir /= np.sqrt(np.sum(ir ** 2))
    L_ = len(x) + n; F = 1 << int(np.ceil(np.log2(L_)))
    y = np.fft.irfft(np.fft.rfft(x, F) * np.fft.rfft(ir, F), F)[:len(x)].astype(np.float32)
    return x * (1 - wet) + y * wet
def put(buf, at, sig):
    i0 = int(at * SR)
    if i0 >= len(buf): return
    sig = sig[:len(buf) - i0]; buf[i0:i0 + len(sig)] += sig
def tone(f, dur, decay=3.0, amp=1.0):
    n = int(dur * SR); x = np.arange(n) / SR
    return (amp * np.sin(2 * np.pi * f * x) * np.exp(-x * decay)).astype(np.float32)
scary = np.zeros(N, np.float32)
dry = np.zeros(N, np.float32)
r2 = np.random.default_rng(13)
half = ramp(S['realize']['start'], TOTAL)
# sub-bass dread (felt more than heard), heavier in the second half
sub = (np.sin(2 * np.pi * 31 * tt) + 0.6 * np.sin(2 * np.pi * 33.5 * tt)) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.05 * tt)) * (0.35 + 0.65 * half)
dry += (sub * 0.16).astype(np.float32)
# ticking clock from 04:00 until the dial pad
t_ = 0.4
while t_ < S['dialpad']['start']:
    n = int(0.03 * SR); x = np.arange(n) / SR
    clk = (r2.standard_normal(n) * np.exp(-x * 220) + np.sin(2 * np.pi * 3200 * x) * np.exp(-x * 160) * 0.6).astype(np.float32)
    put(scary, t_, clk * (0.05 if int(t_) % 2 == 0 else 0.035))
    t_ += 1.0
# ghost whispers: band-passed noise with a breathy envelope, panned low under the clue and the reach
def whisper(dur):
    n = int(dur * SR); x = np.arange(n) / SR
    w = r2.standard_normal(n).astype(np.float32)
    w = np.convolve(w, np.ones(6) / 6, mode='same') - np.convolve(w, np.ones(40) / 40, mode='same')
    env = np.clip(np.sin(np.pi * x / dur), 0, 1) ** 2 * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * x) ** 2)
    return (w * env).astype(np.float32)
for at in [S['scroll']['start'] + 1.5, S['scroll']['start'] + 6.5, S['realize']['start'] + 0.4, S['ots']['start'] + 0.6, S['oldtone']['start'] + 2.0]:
    put(scary, at, whisper(1.6) * 0.07)
# rising dissonant string cluster from the dial pad to the door (pitch creeps up)
c0, c1 = S['dialpad']['start'], S['door']['start'] + 0.1
n = int((c1 - c0) * SR); x = np.arange(n) / SR; rise = x / (c1 - c0)
cl = np.zeros(n, np.float32)
for f0 in (220.0, 233.1, 246.9, 311.1):
    ph = 2 * np.pi * np.cumsum(f0 * (1 + 0.12 * rise ** 2) * (1 + 0.004 * np.sin(2 * np.pi * 5.5 * x + f0))) / SR
    cl += (np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)).astype(np.float32)
cl *= (rise ** 1.6 * 0.022).astype(np.float32)
cl[-int(0.05 * SR):] *= np.linspace(1, 0, int(0.05 * SR)).astype(np.float32)      # cut dead on the door
put(scary, c0, cl)
# stingers: deep boom + metallic screech + reverse cymbal into it
def stinger(big=1.0):
    n = int(2.2 * SR); x = np.arange(n) / SR
    boom = (np.sin(2 * np.pi * (60 * np.exp(-x * 1.5) + 28) * x) * np.exp(-x * 2.2)).astype(np.float32)
    scr = np.zeros(n, np.float32)
    for f in (1873, 2311, 2957):
        scr += np.sin(2 * np.pi * f * x * (1 - 0.03 * x)) * np.exp(-x * 2.8)
    noise_ = r2.standard_normal(n).astype(np.float32) * np.exp(-x * 9)
    return (boom * 0.5 + scr * 0.03 + noise_ * 0.06) * big
def reverse_cym(dur=1.2):
    n = int(dur * SR); x = np.arange(n) / SR
    w = r2.standard_normal(n).astype(np.float32); w = w - np.convolve(w, np.ones(12) / 12, mode='same')
    return (w * (x / dur) ** 3).astype(np.float32)
T2B = [e for e, l in events if l == 'T2b'][0]
for at, big in [(T2B, 0.8), (S['dean']['start'], 0.6), (S['door']['start'], 1.0), (S['oldtone']['start'] + 0.15, 1.0)]:
    put(scary, at - 1.2, reverse_cym() * 0.09 * big)
    put(scary, at, stinger(big))
# detuned music box playing the ringtone phrase under the old-phone reveal
mb = np.zeros(int(S['oldtone']['dur'] * SR), np.float32)
notes = [1318.5, 987.8, 1174.7, 1318.5, 987.8, 783.99]
for rep_ in range(4):
    for k, f in enumerate(notes):
        at = 0.6 + rep_ * 1.25 + k * 0.2
        f2 = f * (1 - 0.018 * rep_ - 0.006 * k) * 0.5
        i0 = int(at * SR)
        if i0 >= len(mb): break
        nt = tone(f2, 0.9, 4.5) + tone(f2 * 2.01, 0.9, 7, 0.3) + tone(f2 * 3.0, 0.9, 12, 0.1)
        mb[i0:i0 + len(nt)] += nt[:len(mb) - i0]
put(scary, S['oldtone']['start'], mb * 0.06)
# static / glitch bursts on the zoom-blur cuts
for k in ZB:
    n = int(0.22 * SR); x = np.arange(n) / SR
    st_ = r2.standard_normal(n).astype(np.float32) * (np.sin(2 * np.pi * 37 * x) > 0) * np.exp(-x * 9)
    put(scary, S[k]['start'] - 0.05, st_ * 0.06)
scary = reverb(scary, 1.8, 0.4)
scary *= (1.0 - 0.35 * np.clip(venv / 0.04, 0, 1)).astype(np.float32)        # keep the voices clear
# ======== audible creepy music (mid range) ========
def piano(f, dur=2.4):
    n = int(dur * SR); x = np.arange(n) / SR
    env = np.exp(-x * 1.8) * (1 - np.exp(-x * 300))
    sig = (np.sin(2 * np.pi * f * x) + 0.45 * np.sin(2 * np.pi * 2 * f * x) * np.exp(-x * 1.2)
           + 0.2 * np.sin(2 * np.pi * 3.01 * f * x) * np.exp(-x * 2.5) + 0.08 * np.sin(2 * np.pi * 4.02 * f * x) * np.exp(-x * 4))
    return (sig * env).astype(np.float32)
A3, C4, D4, E4, Eb4, F4, G3, Bb3, A4 = 220.0, 261.6, 293.7, 329.6, 311.1, 349.2, 196.0, 233.1, 440.0
motif = [(A3, 0.0), (E4, 0.9), (C4, 1.8), (Eb4, 2.7), (A3, 3.6), (F4, 4.5), (E4, 5.4), (Bb3, 6.3)]   # minor with a tritone/♭ bite
music = np.zeros(N, np.float32)
bar = 7.2; t_ = 0.2
while t_ < TOTAL:
    for f, off in motif:
        at = t_ + off
        if at >= TOTAL: break
        i0 = int(at * SR); nt = piano(f) * 0.9
        music[i0:i0 + len(nt)] += nt[:max(0, N - i0)]
        if f in (Eb4, Bb3):                                   # a quiet high ghost note on the wrong notes
            g = piano(f * 2.0, 1.6) * 0.35; music[i0:i0 + len(g)] += g[:max(0, N - i0)]
    t_ += bar
# soft pad: A minor -> F -> A minor -> E (with a slow swell), mid register
chords = [(A3, C4, E4), (F4 / 2, A3, C4), (A3, C4, E4), (E4 / 2, G3 * 1.0, Bb3)]
pad2 = np.zeros(N, np.float32); seg = 3.6
for k in range(int(TOTAL / seg) + 1):
    c = chords[k % 4]; i0 = int(k * seg * SR); n = int((seg + 1.0) * SR); x = np.arange(n) / SR
    env = np.clip(x / 1.2, 0, 1) * np.clip((seg + 1.0 - x) / 1.2, 0, 1)
    sig = sum(np.sin(2 * np.pi * f * x * (1 + 0.002 * np.sin(2 * np.pi * 0.3 * x))) + 0.3 * np.sin(2 * np.pi * 2 * f * x) for f in c)
    seg_sig = (sig * env * (0.75 + 0.25 * np.sin(2 * np.pi * 4.5 * x))).astype(np.float32)
    pad2[i0:i0 + n] += seg_sig[:max(0, N - i0)]
music = reverb(music * 0.42 + pad2 * 0.09, 2.6, 0.5, seed=21)
# levels: present the whole way, a little lower under voices, dips under the clear ring, stops dead on the final cut
mlvl = np.ones(N, np.float32)
mlvl[int((S['door']['start'] - 0.1) * SR):int(S['oldtone']['start'] * SR)] = 0.55
mlvl = np.convolve(mlvl, np.ones(2400) / 2400, mode='same')
music *= (mlvl * (1.0 - 0.3 * np.clip(venv / 0.04, 0, 1))).astype(np.float32)
# ======== dynamics: light <-> heavy, following the story ========
T2B_ = [e for e, l in events if l == 'T2b'][0]
pts = [(0, .30), (S['scroll']['start'], .35), (S['read']['start'], .48), (S['realize']['start'], .55),
       (T2B_ - .05, .85), (T2B_ + 1.2, .55), (S['dialpad']['start'], .60), (S['dean']['start'], .80),
       (S['tawanlook']['start'], .25), (S['whisper']['start'] + 0.6, .40), (S['door']['start'] - 0.05, .45),
       (S['door']['start'], 1.0), (S['ots']['start'], .90), (S['oldtone']['start'], 1.0),
       (S['choice']['start'] + 0.5, .70), (TOTAL, .70)]
px, py = zip(*pts)
I = np.interp(tt, px, py).astype(np.float32)
I = np.convolve(I, np.ones(4800) / 4800, mode='same').astype(np.float32)
# heavy layer: low drum hits (80 bpm) + bowed low strings, only really there when intensity is high
heavy = np.zeros(N, np.float32)
beat = 60 / 80; t_ = S['dialpad']['start']
while t_ < TOTAL:
    n = int(0.6 * SR); x = np.arange(n) / SR
    hit = (np.sin(2 * np.pi * (70 * np.exp(-x * 6) + 42) * x) * np.exp(-x * 7) + rng.standard_normal(n) * np.exp(-x * 40) * 0.15).astype(np.float32)
    i0 = int(t_ * SR); heavy[i0:i0 + n] += hit[:max(0, N - i0)]
    t_ += beat
strings = sum(np.sin(2 * np.pi * f * tt + k) + 0.5 * np.sin(4 * np.pi * f * tt) for k, f in enumerate((110.0, 116.5, 164.8))).astype(np.float32)
strings *= (0.7 + 0.3 * np.sin(2 * np.pi * 6 * tt)).astype(np.float32)
hw = np.clip((I - 0.55) / 0.45, 0, 1) ** 1.5
heavy = reverb(heavy * 0.28 * hw + strings * 0.02 * hw, 1.8, 0.35, seed=31)
# end: everything musical fades out slowly over the last seconds of the end card
fade = np.ones(N, np.float32)
f0 = TOTAL - 4.0
fade[int(f0 * SR):] = np.linspace(1, 0, N - int(f0 * SR)) ** 1.6
music = music * (0.45 + 0.9 * I) * fade
bed = bed * (0.55 + 0.7 * I) * fade
scary = scary * (0.6 + 0.6 * I) * fade
dry = dry * (0.5 + 0.7 * I) * fade
heavy = heavy * fade
ring_fade = np.ones(N, np.float32); r0 = TOTAL - 2.5
ring_fade[int(r0 * SR):] = np.linspace(1, 0.0, N - int(r0 * SR)) ** 1.2
ring = ring * ring_fade
mix = voice * 0.95 + bed + ring + sfx + scary + dry + music + heavy
mix = np.tanh(mix * 1.1) * 0.9
mix[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))   # soft tail, no click
pcm = (np.clip(mix, -1, 1) * 32767).astype(np.int16)
np.save('music_stem.npy', music); np.save('voice_stem.npy', voice)
with wave.open('mix.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


# ---------------- mouth flags per frame ----------------
def flags(x):
    out = []
    hop = SR // FPS
    for f in range(int(TOTAL * FPS) + 1):
        seg = x[f * hop:(f + 1) * hop]
        out.append(1 if len(seg) and np.sqrt(np.mean(seg ** 2)) > 0.03 else 0)
    return out


FJ = flags(mixJ); FT = flags(mixT)
for s in shots:
    f0 = int(round(s['start'] * FPS)); n = int(round(s['dur'] * FPS))
    s['frames'] = n; s['mJ'] = FJ[f0:f0 + n]; s['mT'] = FT[f0:f0 + n]
json.dump(dict(total=TOTAL, shots=shots, events=[(round(a, 3), l) for a, l in events]), open('timeline.json', 'w'))
print('total %.1fs' % TOTAL)
for s in shots:
    print(f"{s['key']:10s} {s['start']:6.2f} {s['dur']:5.2f}")
