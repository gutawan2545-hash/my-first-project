#!/usr/bin/env bash
# Encode frames_rosa/ (24 fps, 1080x1920) with a temporary ambient bed into rosa_tears.mp4.
# The ambient bed is a placeholder until the voices are dubbed (dubbing needs ElevenLabs credits, ask first).
set -euo pipefail
cd "$(dirname "$0")"
DUR=17
ffmpeg -y -loglevel error \
  -f lavfi -i "anoisesrc=color=pink:amplitude=0.25:duration=${DUR}:sample_rate=48000" \
  -f lavfi -i "sine=frequency=196:duration=${DUR}:sample_rate=48000" \
  -f lavfi -i "sine=frequency=233:duration=${DUR}:sample_rate=48000" \
  -f lavfi -i "anoisesrc=color=white:amplitude=0.6:duration=0.35:sample_rate=48000" \
  -filter_complex "\
[0]highpass=f=180,lowpass=f=1100,volume=0.35,tremolo=f=0.15:d=0.6[wind];\
[1]volume=0.05,tremolo=f=0.3:d=0.5[d1];[2]volume=0.035,tremolo=f=0.22:d=0.5[d2];\
[3]highpass=f=500,lowpass=f=2500,afade=t=out:st=0.05:d=0.3,volume=0.5,adelay=7650|7650[puff];\
[wind][d1][d2][puff]amix=inputs=4:normalize=0,afade=t=in:d=1.2,afade=t=out:st=$((DUR-1)):d=1,alimiter=limit=0.8[a]" \
  -map "[a]" -c:a pcm_s16le ambient_rosa.wav
ffmpeg -y -loglevel error -framerate 24 -i frames_rosa/%04d.png -i ambient_rosa.wav \
  -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium -c:a aac -b:a 160k -shortest -movflags +faststart rosa_tears.mp4
ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact rosa_tears.mp4
