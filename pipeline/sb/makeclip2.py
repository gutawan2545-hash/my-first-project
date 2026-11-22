"""Assembles the animated frames into clip_anim.mp4: each shot from aframes/sNN, soft crossfades, silent track."""
import os, glob, subprocess
FPS = 24; XF = 0.4
os.makedirs('seg2', exist_ok=True)
durs = []
for i in range(1, 13):
    d = f'aframes/s{i:02d}'
    n = len(glob.glob(f'{d}/f*.jpg'))
    assert n > 0, d
    durs.append(n / FPS)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{d}/f%04d.jpg',
                    '-vf', 'scale=1080:1920,format=yuv420p', '-c:v', 'libx264', '-preset', 'medium', '-crf', '18',
                    '-r', str(FPS), f'seg2/s{i:02d}.mp4'], check=True)
inputs = []
for i in range(1, 13):
    inputs += ['-i', f'seg2/s{i:02d}.mp4']
fc = ''; prev = '[0:v]'; t = durs[0]
for i in range(1, 12):
    off = t - XF
    fc += f'{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={off:.3f}[x{i}];'
    prev = f'[x{i}]'; t = off + durs[i]
fc += f'{prev}format=yuv420p[v]'
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error'] + inputs +
               ['-f', 'lavfi', '-t', f'{t:.2f}', '-i', 'anullsrc=r=48000:cl=stereo', '-filter_complex', fc,
                '-map', '[v]', '-map', '12:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '19',
                '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', 'clip_anim.mp4'], check=True)
print('clip_anim.mp4', round(t, 1), 's')
