"""EP.01 score: sunny Koh Tao summer groove (steel pan lead, ukulele off-beat strums, soft bass, kick, shaker, congas).
Mid-range by design so it sits under the voice. Moods: 'summer' (main), 'past' (muted Bangkok memory), 'warm' (ending)."""
import numpy as np

SR = 48000
rng = np.random.default_rng(11)
NOTE = lambda m: 440 * 2 ** ((m - 69) / 12)


def _t(dur):
    return np.arange(int(dur * SR)) / SR


def steelpan(f, dur=.7, vel=1.0):
    t = _t(dur)
    parts = ((1, 1, 3.2), (2, .55, 5.0), (3.0, .22, 8.0), (4.07, .12, 11), (5.98, .05, 16))   # slightly inharmonic, bell-like
    x = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * d) for k, a, d in parts)
    att = np.minimum(1, t / .004)
    return (x * att * vel * .5).astype(np.float32)


def uke_note(f, dur=.5, vel=1.0):
    t = _t(dur)
    x = sum((1 / k) * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (6 + 5 * k)) for k in range(1, 8))
    return (x * np.minimum(1, t / .002) * vel).astype(np.float32)


def strum(chord, dur=.25, vel=1.0, down=True):
    notes = chord if down else chord[::-1]
    n = int(dur * SR)
    out = np.zeros(n + int(.05 * SR), np.float32)
    for i, m in enumerate(notes):
        x = uke_note(NOTE(m), dur, vel * .35)
        o = int(i * .012 * SR)
        out[o:o + len(x)] += x[:len(out) - o]
    return out


def bass(f, dur, vel=1.0):
    t = _t(dur)
    x = np.sin(2 * np.pi * f * t) + .3 * np.sin(2 * np.pi * 2 * f * t)
    e = np.minimum(1, t / .006) * np.exp(-t * 3.5)
    return (x * e * vel * .55).astype(np.float32)


def kick(vel=1.0):
    t = _t(.22)
    f = 55 + 70 * np.exp(-t * 30)
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 16) * vel * .7).astype(np.float32)


def shaker(vel=1.0):
    n = int(.07 * SR)
    x = np.diff(np.concatenate([[0], rng.standard_normal(n)])).astype(np.float32)
    return x * np.exp(-np.arange(n) / SR * 55) * .12 * vel


def conga(f=200, vel=1.0):
    t = _t(.25)
    fr = f * (1 + .4 * np.exp(-t * 40))
    return (np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 15) * .45 * vel).astype(np.float32)


def pad(freqs, dur, vel=1.0):
    t = _t(dur)
    x = sum(np.sin(2 * np.pi * f * t + i) + .3 * np.sin(2 * np.pi * f * 1.004 * t) for i, f in enumerate(freqs)) / len(freqs)
    e = np.minimum(1, t / .3) * np.minimum(1, (dur - t) / .3)
    return (x * e * vel).astype(np.float32)


def place(buf, x, t, g=1.0):
    i = int(t * SR)
    j = min(len(buf), i + len(x))
    if 0 <= i < j:
        buf[i:j] += x[:j - i] * g


# D major, bright: D – G – A – D / Bm – G – A – D
PROG = [(50, (62, 66, 69, 74)), (55, (62, 67, 71, 74)), (57, (61, 64, 69, 73)), (50, (62, 66, 69, 74)),
        (47, (62, 66, 71, 74)), (55, (62, 67, 71, 74)), (57, (61, 64, 69, 73)), (50, (62, 66, 69, 74))]
MEL = [[78, None, 76, 74, 76, None, 78, 81], [79, None, 78, 76, 74, None, None, 74], [76, 78, 79, 76, 73, None, 69, None], [74, None, None, 78, 76, 74, 76, None],
       [78, None, 81, 78, 76, None, 74, 76], [79, 78, 76, None, 74, None, 79, None], [81, None, 79, 78, 76, None, 73, 76], [74, None, None, None, 78, 81, 78, None]]


def section(n_total, t0, t1, mood='summer', bpm=116, vel=1.0):
    out = np.zeros(n_total, np.float32)
    beat = 60 / bpm
    bar = 4 * beat
    for b in range(int(np.ceil((t1 - t0) / bar))):
        bt = t0 + b * bar
        root, ch = PROG[b % 8]
        mel = MEL[b % 8]
        if mood == 'summer':
            for i, m in enumerate(mel):
                tt = bt + i * beat / 2 + (.02 if i % 2 else 0)            # light swing
                if m and tt < t1:
                    place(out, steelpan(NOTE(m), .8, .8), tt)
            for k in range(4):                                         # ukulele chucks on the off-beats + a down-up on 4
                tt = bt + k * beat + beat / 2
                if tt < t1:
                    place(out, strum(ch, .22, .9, True), tt)
                if k == 3 and bt + k * beat < t1:
                    place(out, strum(ch, .18, .6, False), bt + k * beat + beat * .75)
            for tt, n, d in ((0, root, 1.2), (1.5, root + 7, .5), (2, root, 1.0), (3.5, root + 12, .5)):
                if bt + tt * beat < t1:
                    place(out, bass(NOTE(n), d * beat, .9), bt + tt * beat)
            for k in (0, 2):
                if bt + k * beat < t1:
                    place(out, kick(.8), bt + k * beat)
            for k in range(8):
                if bt + k * beat / 2 < t1:
                    place(out, shaker(1 if k % 2 else .6), bt + k * beat / 2)
            for tt, f in ((3, 240), (3.5, 200), (1.5, 260)):
                if bt + tt * beat < t1:
                    place(out, conga(f, .7), bt + tt * beat)
        elif mood == 'past':                                          # Bangkok memory: muted, slower, no drums
            place(out, pad([NOTE(n - 12) for n in ch[:3]], bar, .3), bt)
            for k in (1, 3):
                if bt + k * beat < t1:
                    place(out, strum([n - 12 for n in ch], .3, .5), bt + k * beat)
            for i, m in enumerate(mel[::2]):
                if m and bt + i * beat < t1:
                    place(out, steelpan(NOTE(m - 12), 1.0, .4), bt + i * beat)
        elif mood == 'warm':                                          # ending: sunset, gentle
            place(out, pad([NOTE(n) for n in ch[:3]] + [NOTE(root)], bar, .3), bt)
            for k in range(4):
                if bt + k * beat + beat / 2 < t1:
                    place(out, strum(ch, .3, .45), bt + k * beat + beat / 2)
            for i, m in enumerate(mel[::2]):
                if m and bt + i * beat < t1:
                    place(out, steelpan(NOTE(m), 1.2, .45), bt + i * beat)
            if bt < t1:
                place(out, bass(NOTE(root), bar * .9, .6), bt)
    i0, i1 = int(t0 * SR), min(n_total, int(t1 * SR))
    f = int(.4 * SR)
    out[i0:i0 + f] *= np.linspace(0, 1, f)
    out[max(i0, i1 - f):i1] *= np.linspace(1, 0, min(f, i1 - i0))
    out[i1:] = 0
    return out * vel


def stinger(n_total, t, kind='chacha'):
    out = np.zeros(n_total, np.float32)
    for i, dt in enumerate((0, .22, .44)):
        place(out, conga(220 + i * 30, 1.1), t + dt)
        place(out, steelpan(NOTE((74, 78, 81)[i]), .6, .9), t + dt)
        place(out, strum((62, 66, 69, 74), .2, .9), t + dt)
    return out


if __name__ == '__main__':
    import wave, os, subprocess
    H = os.path.dirname(os.path.abspath(__file__))
    n = int(40 * SR)
    x = section(n, 0, 15, 'summer') + section(n, 15, 25, 'past', 100) * .9 + stinger(n, 25.2) + section(n, 26, 40, 'warm', 84)
    x = x / np.max(np.abs(x)) * .8
    w = wave.open(os.path.join(H, 'music_preview.wav'), 'wb')
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close()
    print('ok')
