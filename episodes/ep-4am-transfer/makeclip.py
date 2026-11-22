"""Builds the silent draft clip: slow push-in on each picture, subtitles + graphics fade in on top,
soft crossfades between shots, 1080x1920 @30fps, silent stereo track."""
import os, subprocess, runpy
from PIL import Image

os.makedirs('seg', exist_ok=True)
A = runpy.run_path('all12.py')
ORDER = A['ORDER']; wlen = A['wlen']
FPS = 30; XF = 0.4

# clean overlay alpha (drop the faint haze), force exact size
for i in range(1, 13):
    for k in 'bo':
        f = f'frames/{k}{i:02d}.png'
        im = Image.open(f)
        if im.size != (1080, 1920):
            im = im.crop((0, 0, 1080, 1920))
        if k == 'o':
            r, g, b, a = im.convert('RGBA').split()
            a = a.point(lambda v: 0 if v < 40 else min(255, int((v - 40) * 255 / 215)))
            im = Image.merge('RGBA', (r, g, b, a))
        im.save(f)

durs = []
for i, row in enumerate(ORDER, 1):
    line = row[1]
    d = max(3.4, wlen(line) / 11.0 + 1.4)
    if i == len(ORDER):
        d += 1.5            # hold the question card a little longer
    durs.append(round(d, 2))

for i, d in enumerate(durs, 1):
    frames = int(d * FPS)
    zin = i % 2 == 1        # alternate push-in / pull-out for variety
    z = f"1+0.06*on/{frames}" if zin else f"1.06-0.06*on/{frames}"
    vf = (f"[0:v]scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps={FPS}[bg];"
          f"[1:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[ov];[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-loop', '1', '-t', str(d), '-i', f'frames/b{i:02d}.png',
           '-loop', '1', '-t', str(d), '-i', f'frames/o{i:02d}.png',
           '-filter_complex', vf, '-map', '[v]', '-t', str(d), '-r', str(FPS),
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', f'seg/s{i:02d}.mp4']
    subprocess.run(cmd, check=True)
    print('segment', i, d)

# crossfade chain
inputs = []
for i in range(1, 13):
    inputs += ['-i', f'seg/s{i:02d}.mp4']
fc = ''; prev = '[0:v]'; t = durs[0]
for i in range(1, 12):
    off = t - XF
    out = f'[x{i}]'
    fc += f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.2f}{out};'
    prev = out; t = off + durs[i]
total = t
fc += f'{prev}format=yuv420p[v]'
cmd = ['ffmpeg', '-y', '-loglevel', 'error'] + inputs + ['-f', 'lavfi', '-t', f'{total:.2f}', '-i', 'anullsrc=r=48000:cl=stereo',
       '-filter_complex', fc, '-map', '[v]', '-map', '12:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
       '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', 'clip_draft.mp4']
subprocess.run(cmd, check=True)
print('total', round(total, 1), 's', durs)
