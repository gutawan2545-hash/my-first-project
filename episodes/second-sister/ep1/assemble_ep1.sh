#!/usr/bin/env bash
# Join the rendered segments (segments/seg_###.mp4 + rosa_tears.mp4), mix the temporary sound bed
# (wind + music_ep1.wav), append the outro.  ->  ep1_full_subs.mp4 (1080x1920, 24 fps)
# Usage: bash assemble_ep1.sh            -> whole episode
#        bash assemble_ep1.sh 0 7        -> only segments 0..7 (sample cut, no outro) -> ep1_sample.mp4
set -euo pipefail
cd "$(dirname "$0")"
FIRST=${1:-0}; LAST=${2:-}
python3 audio_ep1.py
read -r TOTAL NSEG < <(python3 -c "import json;t=json.load(open('ep1_timeline.json'));print(t['total'],len(t['segments']))")
LAST=${LAST:-$((NSEG-1))}
: > concat.txt
START=$(python3 -c "import json;t=json.load(open('ep1_timeline.json'));print(t['segments'][$FIRST]['t0'])")
for i in $(seq "$FIRST" "$LAST"); do
  f=$(python3 -c "import json;s=json.load(open('ep1_timeline.json'))['segments'][$i];print(s['file'] if s['type']=='video' else 'segments/seg_%03d.mp4'%$i)")
  [ -f "$f" ] || { echo "missing $f"; exit 1; }
  echo "file '$f'" >> concat.txt
done
# video only, re-timed cleanly
ffmpeg -y -loglevel error -f concat -safe 0 -i concat.txt -an -c:v libx264 -pix_fmt yuv420p -crf 19 -preset veryfast -r 24 joined.mp4
DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 joined.mp4)
ffmpeg -y -loglevel error -ss "$START" -t "$DUR" -i music_ep1.wav \
  -f lavfi -i "anoisesrc=color=pink:amplitude=0.25:duration=${DUR}:sample_rate=48000" \
  -filter_complex "[1]highpass=f=160,lowpass=f=900,volume=0.12,tremolo=f=0.12:d=0.6,pan=stereo|c0=c0|c1=c0[wind];[0]aresample=48000,aformat=channel_layouts=stereo[m];[m][wind]amix=inputs=2:normalize=0,afade=t=in:d=1.5,alimiter=limit=0.9[a]" \
  -map "[a]" -c:a pcm_s16le bed.wav
if [ "$FIRST" = 0 ] && [ "$LAST" = $((NSEG-1)) ]; then
  OUT=ep1_full_subs.mp4
  ffmpeg -y -loglevel error -i joined.mp4 -i bed.wav -i ../../ep-4am-transfer/v2/outro.mp4 -filter_complex \
    "[1]afade=t=out:st=$(python3 -c "print($DUR-1.5)"):d=1.5[b];[0:v][b][2:v][2:a]concat=n=2:v=1:a=1[v][a]" \
    -map "[v]" -map "[a]" -c:v libx264 -pix_fmt yuv420p -crf 20 -preset veryfast -c:a aac -b:a 160k -movflags +faststart "$OUT"
else
  OUT=ep1_sample.mp4
  ffmpeg -y -loglevel error -i joined.mp4 -i bed.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart "$OUT"
fi
rm -f joined.mp4 bed.wav concat.txt
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact "$OUT"
