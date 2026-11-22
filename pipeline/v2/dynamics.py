"""Gives the score light-and-heavy dynamics that follow the story, adds a heavy low drum/strings layer in
the intense parts, and fades everything out gradually over the end card."""
p = 'timeline.py'; s = open(p).read()
anchor = 'mix = voice * 0.95 + bed + ring + sfx + scary + dry + music'
assert anchor in s
block = r'''# ======== dynamics: light <-> heavy, following the story ========
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
'''
s = s.replace(anchor, block + 'mix = voice * 0.95 + bed + ring + sfx + scary + dry + music + heavy')
s = s.replace("mix[-int(0.02 * SR):] = 0                      # hard cut at the very end", "mix[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))   # soft tail, no click")
open(p, 'w').write(s)
print('dynamics in')
