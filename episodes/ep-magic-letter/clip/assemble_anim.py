"""ต่อคลิปแอนิเมชัน: เฟรม 24fps ของแต่ละช็อต + ชั้นซับ/กราฟิก (ค่อย ๆ ขึ้น) -> ภาพจางซ้อนตาม timeline
ช็อตสุดท้ายเป็นการ์ดโหวตไฮไลต์วน · ใส่เสียง out/mix.wav · ต่อโลโก้ปิดท้าย -> out/clip_anim.mp4"""
import json, os, subprocess, pathlib
HERE = pathlib.Path(__file__).parent; os.chdir(HERE)
OUTRO = HERE.parent.parent.parent / "pipeline" / "v2" / "outro.mp4"
FPS, XF, STEP = 24, 0.3, 0.75
TL = json.load(open("out/timeline.json"))
os.makedirs("seg24", exist_ok=True)
run = lambda c: subprocess.run(c, check=True)
ov = "[1:v]format=rgba,fade=t=in:st=0.25:d=0.35:alpha=1[ov];[bg][ov]overlay=0:0:format=auto,format=yuv420p[v]"
segs = []
for i, sh in enumerate(TL):
    n, d = sh["n"], sh["dur"]; out = f"seg24/s{n:02d}.mp4"
    if i == len(TL) - 1:
        k = int(d / STEP) + 1; lst = pathlib.Path("seg24/vote.txt")
        lst.write_text("".join(f"file '{HERE}/frames/v{j % 4}.png'\nduration {STEP}\n" for j in range(k)) + f"file '{HERE}/frames/v{(k-1) % 4}.png'\n")
        src = ["-f", "concat", "-safe", "0", "-i", str(lst)]
        vf = f"[0:v]fps={FPS},scale=1080:1920,setsar=1[bg];" + ov
    else:
        src = ["-framerate", str(FPS), "-i", f"anim/fr/s{n:02d}/%04d.jpg"]
        vf = "[0:v]scale=1080:1920,setsar=1[bg];" + ov
    run(["ffmpeg", "-y", "-loglevel", "error"] + src + ["-loop", "1", "-t", str(d), "-i", f"frames/o{n:02d}.png",
         "-filter_complex", vf, "-map", "[v]", "-t", str(d), "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", out])
    segs.append(out)
inputs = sum((["-i", f] for f in segs), [])
fc = ""; prev = "[0:v]"
for i in range(1, len(segs)):
    trans = "zoomin" if TL[i]["n"] == 8 else "fade"
    fc += f"{prev}[{i}:v]xfade=transition={trans}:duration={XF}:offset={TL[i]['start']:.3f}[x{i}];"; prev = f"[x{i}]"
fc += f"{prev}eq=contrast=1.04:saturation=1.06:gamma=1.02,noise=c0s=4:c0f=t+u,format=yuv420p[v]"
run(["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-i", "out/mix.wav", "-filter_complex", fc, "-map", "[v]", "-map", f"{len(segs)}:a",
     "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", "out/body_anim.mp4"])
run(["ffmpeg", "-y", "-loglevel", "error", "-i", "out/body_anim.mp4", "-i", str(OUTRO), "-filter_complex",
     f"[1:v]fps={FPS},scale=1080:1920,setsar=1[o];[1:a]aresample=48000[oa];[0:v]setsar=1[b];[b][0:a][o][oa]concat=n=2:v=1:a=1[v][a]",
     "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-c:a", "aac", "-b:a", "160k",
     "-movflags", "+faststart", "out/clip_anim.mp4"])
print("done")
