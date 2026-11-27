"""EP.01 soundtrack (round 2): dub on the global timeline + island summer score (music.py, mid-range, ~9-10 dB under the voice)
+ realistic sound effects from sfx/ (ElevenLabs sound generation): birds/beach, harbour, wok, Bangkok traffic, scooter,
rain + thunder, night insects, gecko, waves, whooshes, plus UI clicks on the A/B card.
Run: python3 mix.py -> mix.wav (48 kHz stereo)"""
import os, wave
import numpy as np
import music as MU
from clip_timeline import T, at, TOTAL

HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
N = int((TOTAL + .2) * SR)
rng = np.random.default_rng(7)


def load(path):
    w = wave.open(path)
    x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    sr, ch = w.getframerate(), w.getnchannels()
    x = x.reshape(-1, ch).mean(1)
    if sr != SR:
        t = np.arange(int(len(x) * SR / sr)) * sr / SR
        x = np.interp(t, np.arange(len(x)), x).astype(np.float32)
    return x


def db(v):
    return 10 ** (v / 20)


def rms(x):
    return np.sqrt(np.mean(x ** 2)) + 1e-9


def place(buf, x, t, gain=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if 0 <= i < j:
        buf[i:j] += x[:j - i] * gain


def movavg(x, k):
    c = np.cumsum(np.concatenate([[0], x.astype(np.float64)]))
    y = (c[k:] - c[:-k]) / k
    pad = k // 2
    return np.concatenate([np.full(pad, y[0]), y, np.full(len(x) - len(y) - pad, y[-1])]).astype(np.float32)


def fft_band(x, lo, hi):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x)).astype(np.float32)


# ---------------------------------------------------------------- voice
voice = np.zeros(N, np.float32)
for k, (a, b) in T.items():
    v = load(os.path.join(HERE, 'vo', k + '.wav'))
    v = v / rms(v) * db(-19)
    if k == 'S01':
        v = fft_band(v, 300, 3400) * 1.25
    place(voice, v, a)

# ---------------------------------------------------------------- score
past0, past1 = at('N02') - .45, at('N04') - .2
title = at('J02', 1) + .2
punch = at('N11b', 1) + .1
mus = (MU.section(N, 0, past0, 'summer', 116)
       + MU.section(N, past0, title, 'past', 100) * .9
       + MU.stinger(N, title)
       + MU.section(N, at('N04') - .3, at('F01', 1) + .05, 'summer', 116)      # music drops out for the punchline silence
       + MU.stinger(N, punch)
       + MU.section(N, punch + .7, at('N13') - .3, 'summer', 116) * .9
       + MU.section(N, at('N13') - .3, TOTAL, 'warm', 84))
mus = mus / rms(mus[mus != 0]) * db(-26)
venv = movavg(np.abs(voice), int(.08 * SR))
talking = movavg((venv > db(-40)).astype(np.float32), int(.25 * SR))
mus *= (1 - .3 * np.clip(talking, 0, 1))                   # -26 dB in gaps, ~ -29 dB under speech (voice -19): 9-10 dB below

# ---------------------------------------------------------------- sound effects (real recordings, looped beds where needed)
S = {k: load(os.path.join(HERE, 'sfx', k + '.wav')) for k in
     ('birds_beach', 'waves_rough', 'scooter_pass', 'thunder', 'rain_roof', 'gecko', 'wok_sizzle', 'bkk_traffic', 'harbor', 'night_insects', 'whoosh', 'gecko_real', 'power_down')}
sfx = np.zeros(N, np.float32)


def bed(name, t0, t1, level):
    """Loop a recording from t0 to t1 with crossfades, at a set RMS level."""
    x = S[name] / rms(S[name]) * db(level)
    n, f = int((t1 - t0) * SR), int(.5 * SR)
    out = np.zeros(n, np.float32)
    pos, step = 0, len(x) - f
    while pos < n:
        seg = x.copy()
        seg[:f] *= np.linspace(0, 1, f); seg[-f:] *= np.linspace(1, 0, f)
        j = min(n, pos + len(seg))
        out[pos:j] += seg[:j - pos]
        pos += step
    out[:f] *= np.linspace(0, 1, f); out[-f:] *= np.linspace(1, 0, f)
    place(sfx, out, t0)


def hit(name, t, level):
    place(sfx, S[name] / (np.max(np.abs(S[name])) + 1e-9) * db(level), t)


shots = {s['file'][3:-5]: (s['t0'], s['t1']) for s in __import__('json').load(open(os.path.join(HERE, 'clip_pages', 'shots.json')))['shots']}
g = lambda n: shots[n]
bed('birds_beach', 0, g('shop_thanks')[1], -33)                        # sunny street + shop
hit('whoosh', past0 - .1, -12)                                         # into the past
bed('wok_sizzle', *g('kitchen'), -31); bed('wok_sizzle', *g('kitchen_close'), -33)
bed('bkk_traffic', *g('taxi'), -30)
bed('wok_sizzle', *g('quit'), -36)
hit('whoosh', g('quit')[1] - .45, -11)                                 # kitchen -> the move (zoom-blur bridge)
bed('harbor', g('map')[0] - .1, g('pier_uncle')[1], -32)          # ferry horn + gulls carry us to the island
bed('birds_beach', g('stairs_agent')[0], g('stairs_climb')[1], -33)
bed('harbor', *g('island'), -34)
bed('night_insects', *g('gecko'), -32)
hit('gecko_real', at('N06', .45), -13)                                # real Tokay call: ตุ๊ก-แก
bed('birds_beach', g('scooter_wide')[0], g('aunt_pass')[1], -34)
hit('scooter_pass', at('J04') - 1.2, -10)
bed('rain_roof', g('calendar')[0], g('outage')[1], -31)
hit('thunder', g('calendar')[0] + .3, -10)
hit('thunder', g('outage')[0] + .2, -8)
hit('power_down', at('N09', .36) - .05, -9)                           # lights die on "ไฟก็ดับ" (comic wind-down)
hit('gecko_real', at('N09', .36) + 2.2, -20)                          # the roommate comments from the dark
bed('birds_beach', g('prices')[0], g('instructor')[1], -35)
hit('whoosh', at('N13') - .75, -12)                                    # back to now
bed('waves_rough', g('vista')[0], g('rough')[0], -36)
bed('waves_rough', *g('rough'), -28)
bed('birds_beach', g('vista_wide')[0], g('ab_card')[0] + 1, -36)
# UI clicks on the A/B highlight changes
tt = at('N15', 1) + .1
while tt < TOTAL - .4:
    n = int(.03 * SR)
    t = np.arange(n) / SR
    c = (np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 220) + .5 * rng.standard_normal(n) * np.exp(-t * 400)).astype(np.float32)
    place(sfx, c, tt, db(-18))
    tt += .9
sfx *= (1 - .45 * np.clip(talking, 0, 1))                              # effects step back under speech too

mix = voice + mus + sfx
peak = float(np.max(np.abs(mix)))
mix = np.where(np.abs(mix) > .8, np.sign(mix) * (.8 + .18 * np.tanh((np.abs(mix) - .8) / .18)), mix)
st = (np.clip(np.stack([mix, mix], 1), -1, 1) * 32767).astype(np.int16)
w = wave.open(os.path.join(HERE, 'mix.wav'), 'wb')
w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes()); w.close()
r = lambda x: round(20 * np.log10(rms(x[x != 0])), 1)
print('voice', r(voice), 'music', r(mus), 'sfx', r(sfx), 'peak', round(peak, 2), 'sec', round(N / SR, 1))
