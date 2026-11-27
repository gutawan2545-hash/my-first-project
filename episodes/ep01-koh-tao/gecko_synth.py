"""Procedural Tokay-gecko call following the owner's description: "ตุ๊ก ตุ๊ก ตุ๊ก ตุ๊ก ตุ๊ก ตุ๊ก แก" (croaky clicks speeding up, then a long nasal 'kae')."""
import numpy as np, wave
SR = 48000


def resonator(x, f, bw):
    r = np.exp(-np.pi * bw / SR); th = 2 * np.pi * f / SR
    a1, a2 = -2 * r * np.cos(th), r * r
    y = np.zeros_like(x); y1 = y2 = 0.0
    for i, v in enumerate(x):
        y0 = v - a1 * y1 - a2 * y2
        y[i] = y0; y2, y1 = y1, y0
    return y


def voiced(dur, f0a, f0b, formants, rough=.35):
    n = int(dur * SR); t = np.arange(n) / SR
    f0 = np.linspace(f0a, f0b, n) * (1 + .03 * np.sin(2 * np.pi * 23 * t))
    ph = np.cumsum(f0) / SR
    src = (np.mod(ph, 1) < .12).astype(float) + rough * np.random.default_rng(3).standard_normal(n) * .3   # pulsy, raspy source
    out = sum(g * resonator(src, f, bw) for f, bw, g in formants)
    return out / (np.max(np.abs(out)) + 1e-9)


def env(n, a, r):
    e = np.ones(n); A, Rr = int(a * SR), int(r * SR)
    e[:A] = np.linspace(0, 1, A); e[-Rr:] *= np.linspace(1, 0, Rr) ** 1.5
    return e


call = np.zeros(int(3.2 * SR))
t = .15
gaps = [.24, .21, .19, .17, .155, .14]
for i, g in enumerate(gaps):                         # "ตุ๊ก" x6: short, low, throaty, getting quicker and a bit louder
    x = voiced(.075, 150, 120, [(420, 120, 1), (1050, 180, .5), (2400, 300, .15)])
    x *= env(len(x), .004, .05) * (.55 + .07 * i)
    i0 = int(t * SR); call[i0:i0 + len(x)] += x; t += g
t += .06
x = voiced(.55, 165, 95, [(760, 110, 1), (1750, 160, .7), (2600, 260, .25), (280, 80, .35)])   # "แก": open 'ae', nasal, pitch falls
x *= env(len(x), .025, .3)
i0 = int(t * SR); call[i0:i0 + len(x)] += x * 1.1
call = np.convolve(call, np.exp(-np.arange(int(.03 * SR)) / (.006 * SR)) * .25, mode='full')[:len(call)] + call   # small wooden-room body
call /= np.max(np.abs(call)); call *= .9
out = np.concatenate([call, np.zeros(int(.5 * SR)), call * .85])
w = wave.open('sfx/gecko_synth.wav', 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((out * 32767).astype(np.int16).tobytes()); w.close()
print('ok', len(out) / SR)
