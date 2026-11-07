#!/usr/bin/env bash
# Encode the rendered HyperFrames layers into the CapCut pack.
#
#   cd teaser
#   python3 tools/make_layer_files.py
#   npx hyperframes render -c capcut-graphics.html --format png-sequence -q delivery -o renders/graphics_png
#   npx hyperframes render -c capcut-base.html -q delivery -o renders/base_footage.mp4
#   npx hyperframes render -q delivery -o renders/full_reference.mp4      (or the draft preview)
#   bash tools/encode_overlays.sh
#
# Writes (into ../capcut_pack):
#   02_BASE_FOOTAGE_WITH_MOTION/base_footage_full.mp4
#   03_GRAPHICS_OVERLAY_ALPHA/NN_*.mov      ProRes 4444 with alpha, one per scene (CapCut desktop)
#   03b_GRAPHICS_GREENSCREEN/NN_*.mp4       same graphics on pure green for Chroma Key (CapCut mobile)
set -euo pipefail
cd "$(dirname "$0")/.."
PACK=../capcut_pack
PNG=renders/graphics_png
mkdir -p "$PACK/02_BASE_FOOTAGE_WITH_MOTION" "$PACK/03_GRAPHICS_OVERLAY_ALPHA" "$PACK/03b_GRAPHICS_GREENSCREEN" "$PACK/00_REFERENCE"

first=$(ls "$PNG" | grep -E '\.png$' | sort | head -1)
pattern=$(echo "$first" | sed -E 's/[0-9]+\.png$//')
digits=$(echo "$first" | sed -E 's/.*[^0-9]([0-9]+)\.png$/\1/' | tr -d '\n' | wc -c)
startnum=$((10#$(echo "$first" | sed -E 's/.*[^0-9]([0-9]+)\.png$/\1/')))
IN=(-framerate 30 -start_number "$startnum" -i "$PNG/${pattern}%0${digits}d.png")

# scene segments: number, label, start, duration (must match index.html)
SEGS="01 hook 0.0 3.0
02 peek 3.0 2.4
03 notice 5.4 2.4
04 poster_flash 7.8 2.4
05 title_card 10.2 3.6
06 page_wipe_stairs 13.8 2.4
07 explore 16.2 2.4
08 discover 18.6 2.4
09 get_lost 21.0 2.4
10 uncover 23.4 2.4
11 where_when 25.8 4.8
12 end_card 30.6 4.8"

while read -r n label ss dur; do
  # ProRes 4444 + alpha. qscale keeps the files small; the graphics are flat colour so quality holds.
  ffmpeg -nostdin -v error -y "${IN[@]}" -ss "$ss" -t "$dur" -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le \
    -alpha_bits 8 -qscale:v 9 -vendor apl0 "$PACK/03_GRAPHICS_OVERLAY_ALPHA/${n}_${label}.mov"
  ffmpeg -nostdin -v error -y -f lavfi -i "color=c=0x00FF00:s=1920x1080:r=30" "${IN[@]}" -ss 0 -t "$dur" \
    -filter_complex "[1:v]trim=start=${ss}:duration=${dur},setpts=PTS-STARTPTS[g];[0:v][g]overlay=format=auto:shortest=1,format=yuv420p" \
    -c:v libx264 -crf 14 -preset medium -an -movflags +faststart "$PACK/03b_GRAPHICS_GREENSCREEN/${n}_${label}_green.mp4"
  echo "segment $n $label"
done <<< "$SEGS"

ffmpeg -nostdin -v error -y -i renders/base_footage.mp4 -an -c:v copy -movflags +faststart \
  "$PACK/02_BASE_FOOTAGE_WITH_MOTION/base_footage_full.mp4"
# card backgrounds (navy gradient) complete the numbered main-track clips
ffmpeg -nostdin -v error -y -ss 10.2 -i renders/base_footage.mp4 -t 3.6 -an -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart \
  "$PACK/01_FOOTAGE_CLIPS/05_title_card_background.mp4"
ffmpeg -nostdin -v error -y -ss 30.6 -i renders/base_footage.mp4 -t 4.8 -an -c:v libx264 -crf 16 -pix_fmt yuv420p -movflags +faststart \
  "$PACK/01_FOOTAGE_CLIPS/12_end_card_background.mp4"
if [ -f renders/PREVIEW-720p.mp4 ]; then cp renders/PREVIEW-720p.mp4 "$PACK/00_REFERENCE/reference_preview_720p.mp4"; fi
du -sh "$PACK"/*
