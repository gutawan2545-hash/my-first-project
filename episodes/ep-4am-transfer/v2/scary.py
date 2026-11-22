"""Adds a scarier layer to timeline.py's mix: sub-bass dread, ticking clock, ghost whispers, a rising
dissonant string cluster, big stingers on the four reveals, a detuned music box under the old-phone
reveal, and static bursts on the zoom-blur cuts. Everything goes through a shared reverb."""
p = 'timeline.py'; s = open(p).read()
anchor = 'mix = voice * 0.95 + bed + ring + sfx'
assert anchor in s
block = r'''# ======== scary layer ========
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
        nt = tone(f2, 0.9, 4.5) + tone(f2 * 2.01, 0.6, 7, 0.3) + tone(f2 * 3.0, 0.3, 12, 0.1)
        mb[i0:i0 + len(nt)] += nt[:len(mb) - i0]
put(scary, S['oldtone']['start'], mb * 0.06)
# static / glitch bursts on the zoom-blur cuts
for k in ZB:
    n = int(0.22 * SR); x = np.arange(n) / SR
    st_ = r2.standard_normal(n).astype(np.float32) * (np.sin(2 * np.pi * 37 * x) > 0) * np.exp(-x * 9)
    put(scary, S[k]['start'] - 0.05, st_ * 0.06)
scary = reverb(scary, 1.8, 0.4)
scary *= (1.0 - 0.35 * np.clip(venv / 0.04, 0, 1)).astype(np.float32)        # keep the voices clear
'''
s = s.replace(anchor, block + 'mix = voice * 0.95 + bed + ring + sfx + scary + dry')
open(p, 'w').write(s)
print('scary layer in')
