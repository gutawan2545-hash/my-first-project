"""Loudness envelopes (50 per second, 0..1) from the dub files, for lip sync in oddmotion.js."""
import json, os, wave
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def env(path, fps=50):
    w = wave.open(path)
    sr, n = w.getframerate(), w.getnframes()
    x = np.frombuffer(w.readframes(n), dtype=np.int16).astype(np.float32) / 32768
    hop = sr // fps
    frames = len(x) // hop
    rms = np.sqrt(np.array([np.mean(x[i * hop:(i + 1) * hop] ** 2) for i in range(frames)]) + 1e-9)
    db = 20 * np.log10(rms)
    p95 = np.percentile(db, 95)
    base = np.clip((db - (p95 - 28)) / 28, 0, 1)          # loudness relative to this take
    k = np.ones(15) / 15                                   # ~0.3 s syllable baseline
    mod = np.clip((db - np.convolve(db, k, mode='same')) / 9 + .5, 0, 1)
    v = base * (.3 + .7 * mod)                             # opens on syllable peaks, closes in the dips
    v = np.convolve(v, [.25, .5, .25], mode='same')
    return [round(float(a), 2) for a in v]


if __name__ == '__main__':
    out = {os.path.splitext(f)[0]: env(os.path.join(HERE, 'vo', f)) for f in sorted(os.listdir(os.path.join(HERE, 'vo'))) if f.endswith('.wav')}
    json.dump(out, open(os.path.join(HERE, 'vo', 'env.json'), 'w'), separators=(',', ':'))
    print({k: (len(v), round(sum(1 for a in v if a > .42) / len(v), 2), round(sum(1 for a in v if a < .14) / len(v), 2)) for k, v in out.items() if k[0] in 'JGUSEF'})
