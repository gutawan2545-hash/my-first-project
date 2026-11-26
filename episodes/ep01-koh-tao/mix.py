"""EP.01 soundtrack: dub on the global timeline + synthesized cha-cha score (mid-range, ducked ~9 dB under the voice)
+ sound effects (whooshes at the two time jumps, scooter pass, rain, waves, gecko call, UI clicks on the A/B card).
Run: python3 mix.py -> mix.wav (48 kHz stereo)"""
import json, os, wave
import numpy as np
from clip_timeline import T, at, TOTAL

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
N = int((TOTAL + .2) * SR)
rng = np.random.default_rng(7)


def load(path):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    sr = w.getframerate()
    if w.getnchannels() == 2:
        x = x.reshape(-1, 2).mean(1)
    if sr != SR:                                   # linear resample is fine for speech
        t = np.arange(int(len(x) * SR / sr)) * sr / SR
        x = np.interp(t, np.arange(len(x)), x)
    return x


def place(buf, x, t, gain=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if j > i:
        buf[i:j] += x[:j - i] * gain


def movavg(x, k):
    c = np.cumsum(np.concatenate([[0], x.astype(np.float64)]))
    y = (c[k:] - c[:-k]) / k
    pad = k // 2
    return np.concatenate([np.full(pad, y[0]), y, np.full(len(x) - len(y) - pad, y[-1])]).astype(np.float32)


def db(v):
    return 10 ** (v / 20)


def onepole_lp(x, fc):
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):                      # used on short buffers only
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def fft_band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))


# ---------------------------------------------------------------- voice
voice = np.zeros(N, np.float32)
for k, (a, b) in T.items():
    v = load(os.path.join(HERE, 'vo', k + '.wav'))
    v = v / (np.sqrt(np.mean(v ** 2)) + 1e-9) * db(-19)        # every line at the same loudness (~ -19 dBFS RMS)
    if k == 'S01':                                              # phone line: band-limited
        v = fft_band(v, 300, 3400) * 1.25
    place(voice, v, a)


# ---------------------------------------------------------------- instruments (mid-range, soft attacks)
def env_adsr(n, a=.005, d=.12, s=.35, r=.15):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * (s + (1 - s) * np.exp(-np.maximum(0, t - a) / d))
    rel = int(r * SR)
    if n > rel:
        e[-rel:] *= np.linspace(1, 0, rel)
    return e


def marimba(f, dur, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + .28 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 18) + .12 * np.sin(2 * np.pi * f * 2.01 * t)
    return (x * np.exp(-t * 5.5) * np.minimum(1, t / .003) * vel).astype(np.float32)


def pluck_bass(f, dur, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) + .15 * np.sin(2 * np.pi * 3 * f * t)
    return (x * env_adsr(n, .004, .18, .25, .06) * vel).astype(np.float32)


def pad(freqs, dur, vel=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + i) + .3 * np.sin(2 * np.pi * f * 1.003 * t) for i, f in enumerate(freqs)) / len(freqs)
    e = np.minimum(1, t / .25) * np.minimum(1, (dur - t) / .3)
    return (x * e * vel).astype(np.float32)


def shaker(dur=.06, vel=1.0):
    n = int(dur * SR)
    x = rng.standard_normal(n).astype(np.float32)
    x = np.diff(np.concatenate([[0], x]))                       # bright but quiet
    return x * np.exp(-np.arange(n) / SR * 60) * .18 * vel


def clave(vel=1.0):
    n = int(.08 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2300 * t) * np.exp(-t * 70) * .35 * vel).astype(np.float32)


def conga(f=196, vel=1.0):
    n = int(.25 * SR)
    t = np.arange(n) / SR
    fr = f * (1 + .5 * np.exp(-t * 40))
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 14) * .6 * vel).astype(np.float32)


NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)
# I – IV – V – I in F major, cha-cha melody (playful, sticks to the middle register)
CHORDS = [(53, (65, 69, 72)), (58, (70, 74, 77)), (60, (72, 76, 79)), (53, (65, 69, 72))]
MEL = [[77, None, 76, 74, 72, None, 72, 72], [74, None, 77, 76, 74, None, 70, 70], [72, None, 76, 79, 77, None, 76, 76], [77, 76, 74, 72, 69, None, 72, 72]]


def section(t0, t1, bpm=124, mood='main', vel=1.0):
    out = np.zeros(N, np.float32)
    beat = 60 / bpm
    bar = 4 * beat
    nb = int(np.ceil((t1 - t0) / bar))
    for b in range(nb):
        bt = t0 + b * bar
        root, ch = CHORDS[b % 4]
        mel = MEL[b % 4]
        if mood in ('main', 'bright'):
            for i, m in enumerate(mel):                         # eighth-note melody
                if m and bt + i * beat / 2 < t1:
                    place(out, marimba(NOTE(m), .5, .55), bt + i * beat / 2)
            for i, (bn, d) in enumerate(((root, 1.0), (root + 7, 1.0), (root, .5), (root + 7, .5), (root + 12, .5))):
                tt = bt + (0, 1, 2, 2.5, 3)[i] * beat
                if tt < t1:
                    place(out, pluck_bass(NOTE(bn), d * beat * .9, .5), tt)
            for k in range(8):                                  # shaker 8ths, clave on 2 and 3&, congas on 4 & 4&
                tt = bt + k * beat / 2
                if tt < t1:
                    place(out, shaker(vel=.9 if k % 2 == 0 else .6), tt)
            for tt, v in ((1, .8), (2.5, .7)):
                if bt + tt * beat < t1:
                    place(out, clave(v), bt + tt * beat)
            for tt, f in ((3, 220), (3.5, 196), (0, 165)):
                if bt + tt * beat < t1:
                    place(out, conga(f, .7), bt + tt * beat)
            if mood == 'bright' and bt < t1:
                place(out, pad([NOTE(n) for n in ch], bar, .18), bt)
        elif mood == 'past':                                    # muted, sparse, "memory" colour
            place(out, pad([NOTE(n - 12) for n in ch], bar, .28), bt)
            for i, m in enumerate(mel[::2]):
                if m and bt + i * beat < t1:
                    place(out, marimba(NOTE(m - 12), .9, .35), bt + i * beat)
            for k in range(4):
                if bt + k * beat < t1:
                    place(out, shaker(vel=.5), bt + k * beat + beat / 2)
        elif mood == 'warm':                                    # ending: slow pads + gentle marimba
            place(out, pad([NOTE(n) for n in ch] + [NOTE(root)], bar, .32), bt)
            for i, m in enumerate(mel[::2]):
                if m and bt + i * beat < t1:
                    place(out, marimba(NOTE(m), 1.2, .3), bt + i * beat)
    # fades so section changes never cut abruptly
    i0, i1 = int(t0 * SR), int(min(t1, TOTAL) * SR)
    fade = int(.35 * SR)
    out[i0:i0 + fade] *= np.linspace(0, 1, fade)
    out[max(i0, i1 - fade):i1] *= np.linspace(1, 0, min(fade, i1 - i0))
    out[i1:] = 0
    return out * vel


music = np.zeros(N, np.float32)
music += section(0, at('N02') - .3, 124, 'bright')
music += section(at('N02') - .3, at('J02'), 104, 'past', .9)
title = at('J02', 1) + .1
for i, tt in enumerate((title, title + .24, title + .48)):          # "ชะ ชะ ช่า" hits for the title
    place(music, conga(196 + i * 30, 1.0), tt)
    place(music, clave(.9), tt)
    for f in (65, 69, 72):
        place(music, marimba(NOTE(f + (5 if i == 2 else 0)), .6, .5), tt)
music += section(at('N04') - .1, at('F01', 1) + .02, 124, 'main')
punch = at('F01', 1) + .55
for i, tt in enumerate((punch, punch + .2, punch + .4)):           # the punchline sting after the silence
    place(music, conga(220 + i * 25, 1.0), tt)
    place(music, marimba(NOTE((72, 76, 79)[i]), .5, .6), tt)
music += section(at('N12') - .1, at('N13') - .2, 124, 'main', .9)
music += section(at('N13') - .2, TOTAL, 84, 'warm')

# side-chain duck: music sits ~9 dB under the voice while anyone talks
venv = np.abs(voice)
k = int(.08 * SR)
venv = movavg(venv, k)
talking = (venv > db(-40)).astype(np.float32)
sm = int(.25 * SR)
talking = movavg(talking, sm)
music = music / (np.sqrt(np.mean(music[music != 0] ** 2)) + 1e-9) * db(-26)
music *= (1 - .3 * np.clip(talking, 0, 1))                        # -26 dB in gaps, ~ -29 under speech (voice ~ -19): 9-10 dB below


# ---------------------------------------------------------------- effects
sfx = np.zeros(N, np.float32)


def whoosh(dur=.6, up=True):
    n = int(dur * SR)
    x = rng.standard_normal(n).astype(np.float32)
    t = np.linspace(0, 1, n)
    out = np.zeros(n, np.float32)
    seg = 2048
    for s0 in range(0, n, seg):                                 # sweeping band
        s1 = min(n, s0 + seg)
        c = 300 + (2400 if up else -0) * (t[s0] if up else 1 - t[s0]) + 200
        out[s0:s1] = fft_band(x[s0:s1], c * .6, c * 1.6)
    e = np.sin(np.pi * t) ** 1.5
    return out * e * .9


def ambience(dur, lo, hi, level):
    n = int(dur * SR)
    x = fft_band(rng.standard_normal(n).astype(np.float32), lo, hi)
    x = x / (np.sqrt(np.mean(x ** 2)) + 1e-9) * db(level)
    f = int(.4 * SR)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    return x


place(sfx, whoosh(.55), at('N02') - .45, db(-14))                  # into the past
place(sfx, whoosh(.55, False), at('N13') - .62, db(-14))           # back to now
# scooter pass (buzz with a little doppler)
pass0, pass1 = at('J04') - 1.3 + .1, at('J04') - .05
n = int((pass1 - pass0 + .4) * SR)
t = np.arange(n) / SR
fr = 92 * (1.08 - .16 * t / t[-1])
buzz = np.sign(np.sin(2 * np.pi * np.cumsum(fr) / SR)) * .5 + .3 * np.sin(4 * np.pi * np.cumsum(fr) / SR)
buzz = fft_band(buzz.astype(np.float32), 120, 2500) * np.sin(np.pi * t / t[-1]) ** 2
place(sfx, buzz, pass0, db(-24))
# rain for the call, the phone, the deadpan and the outage
r0, r1 = at('J05') - .5, at('N10') - .1
place(sfx, ambience(r1 - r0, 900, 7000, -34), r0)
# sea for the vista + rough sea (louder on the rough shot)
place(sfx, ambience(at('N15') - (at('N13') - .3), 150, 1400, -36), at('N13') - .3)
place(sfx, ambience(T['J08'][1] - T['J08'][0] + .8, 120, 2000, -30), at('J08') - .3)
# kitchen sizzle under the flashback
place(sfx, ambience(at('N03', .56) - at('N02') + .3, 2500, 9000, -38), at('N02') - .3)
place(sfx, ambience(at('N04') - at('J02') + .2, 2500, 9000, -40), at('J02') - .3)
# gecko call "ตุ๊ก-แก" at the end of N06 (two short croaks)
for i, tt in enumerate((at('N06', 1) + .05, at('N06', 1) + .38)):
    n = int(.18 * SR)
    t = np.arange(n) / SR
    f0 = 520 if i == 0 else 380
    g = np.sin(2 * np.pi * f0 * t + 3 * np.sin(2 * np.pi * 38 * t)) * np.exp(-t * 14)
    place(sfx, g.astype(np.float32), tt, db(-22))
# UI clicks on the A/B highlight changes
tt = at('N15', 1) + .1
while tt < TOTAL - .4:
    n = int(.03 * SR)
    t = np.arange(n) / SR
    c = (np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 220) + .5 * rng.standard_normal(n) * np.exp(-t * 400)).astype(np.float32)
    place(sfx, c, tt, db(-18))
    tt += .9

mix = voice + music + sfx
peak = np.max(np.abs(mix))
mix = np.where(np.abs(mix) > .8, np.sign(mix) * (.8 + .18 * np.tanh((np.abs(mix) - .8) / .18)), mix)   # soft limiter
st = np.stack([mix, mix], 1)
st = (np.clip(st, -1, 1) * 32767).astype(np.int16)
w = wave.open(os.path.join(HERE, 'mix.wav'), 'wb')
w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
w.writeframes(st.tobytes())
w.close()
rms = lambda x: 20 * np.log10(np.sqrt(np.mean(x[x != 0] ** 2)) + 1e-9)
print('voice rms', round(rms(voice), 1), 'music rms', round(rms(music), 1), 'peak', round(float(peak), 2), 'seconds', round(N / SR, 2))
