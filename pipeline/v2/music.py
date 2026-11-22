"""Adds an audible soft, creepy music track (mid range, plays on phone speakers): a slow minor piano motif
with an unsettling note, a soft pad, reverb, light ducking under the voices."""
p = 'timeline.py'; s = open(p).read()
anchor = 'mix = voice * 0.95 + bed + ring + sfx + scary + dry'
assert anchor in s
block = r'''# ======== audible creepy music (mid range) ========
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
music = reverb(music * 0.10 + pad2 * 0.022, 2.6, 0.5, seed=21)
# levels: present the whole way, a little lower under voices, dips under the clear ring, stops dead on the final cut
mlvl = np.ones(N, np.float32)
mlvl[int((S['door']['start'] - 0.1) * SR):int(S['oldtone']['start'] * SR)] = 0.55
mlvl = np.convolve(mlvl, np.ones(2400) / 2400, mode='same')
music *= (mlvl * (1.0 - 0.3 * np.clip(venv / 0.04, 0, 1))).astype(np.float32)
'''
s = s.replace(anchor, block + 'mix = voice * 0.95 + bed + ring + sfx + scary + dry + music')
open(p, 'w').write(s)
print('music in')
