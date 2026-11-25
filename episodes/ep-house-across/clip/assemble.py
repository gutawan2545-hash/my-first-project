"""ต่อช็อตเป็นคลิป: เฟรม -> mp4 ต่อช็อต -> ตัดต่อภาพจางซ้อน (ซูมเบลอเฉพาะเปลี่ยนสถานที่/ย้อนอดีต) -> โลโก้ปิดท้าย -> ใส่เสียง
ผลลัพธ์: clip/house_across_preview.mp4 (1080x1920, 24fps)"""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
shots = json.load(open('shots.json', encoding='utf-8')); tl = json.load(open('timeline.json'))
FPS, XF = 24, .4
OUTRO = os.path.join(HERE, '..', '..', 'ep-4am-transfer', 'v2', 'outro.mp4')
os.makedirs('shots', exist_ok=True)
for s in shots:
    out = f'shots/s{s["n"]:02d}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(FPS), '-i', f'frames/s{s["n"]:02d}/%05d.jpg',
                    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], check=True)
ZOOM_IN = {2, 3, 29}   # transitions INTO these shots use the zoom-blur
inputs = []; [inputs.extend(['-i', f'shots/s{s["n"]:02d}.mp4']) for s in shots]
inputs.extend(['-i', OUTRO, '-i', 'audio.wav'])
fc = []; last = '[0:v]'
for i in range(1, len(shots) + 1):
    src = f'[{i}:v]'
    if i < len(shots):
        off = tl['start'][i]; tr = 'zoomin' if (i + 1) in ZOOM_IN else ('fadeblack' if i + 1 == 24 else 'fade')
        d = XF
    else:
        off = tl['start'][-1] + shots[-1]['dur'] - XF; tr = 'fade'; d = XF
    fc.append(f'{last}{src}xfade=transition={tr}:duration={d}:offset={off:.3f}[v{i}]'); last = f'[v{i}]'
fc.append(f'{last}format=yuv420p[vout]')
audio_idx = len(shots) + 1
subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, '-filter_complex', ';'.join(fc), '-map', '[vout]', '-map', f'{audio_idx}:a',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-c:a', 'aac', '-b:a', '192k', '-shortest', 'house_across_preview.mp4'], check=True)
d = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', 'house_across_preview.mp4'], capture_output=True, text=True).stdout
print('done', d.strip(), 's')
