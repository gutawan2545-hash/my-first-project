#!/bin/bash
# frames + preview mix -> body (film grade, ring cut, 0.3 s black) ; then + reusable outro -> ep01_v2_preview.mp4
set -e
cd "$(dirname "$0")"
GRADE="eq=contrast=1.05:saturation=1.08:gamma=1.04:brightness=0.015,colorbalance=rs=-0.02:bs=0.03:rh=0.03:bh=-0.02,curves=all='0/0.03 0.5/0.51 1/0.98',noise=c0s=7:c0f=t+u"
ffmpeg -y -loglevel error -framerate 24 -i fr/%05d.jpg -i mix.wav \
  -vf "scale=1080:1920,${GRADE},tpad=stop_mode=add:stop_duration=0.3:color=black,format=yuv420p" \
  -af "apad=pad_dur=0.3,aresample=48000" -map 0:v -map 1:a -c:v libx264 -preset medium -crf 19 -r 24 \
  -c:a aac -b:a 160k -ar 48000 -ac 2 -shortest body.mp4
ffmpeg -y -loglevel error -i body.mp4 -i outro.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 19 -r 24 -c:a aac -b:a 160k -movflags +faststart ep01_v2_preview.mp4
ffprobe -v error -show_entries format=duration,size -of compact ep01_v2_preview.mp4
