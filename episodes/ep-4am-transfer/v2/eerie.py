"""Replaces the music bed in timeline.py with a creepier score: dissonant low drone, minor-second pad,
thin glassy tones once the clue lands, reverse swells into the twists, a heartbeat during the calls,
a floor creak on James's step, and ducking under the voices."""
p = 'timeline.py'; s = open(p).read()
a = s.index('# drone bed: two low tones with slow movement + soft filtered noise')
b = s.index('bed *= lvl') + len('bed *= lvl')
new = r'''# ---- eerie score ----
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
for at in [S['realize']['start'] + S['realize']['shake'], S['door']['start']]:
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
bed *= (lvl * duck).astype(np.float32)'''
s = s[:a] + new + s[b:]
open(p, 'w').write(s)
print('eerie score in')
