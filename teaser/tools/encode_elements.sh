#!/usr/bin/env bash
# Single-element transparent videos for the WHERE & WHEN scene.
#   python3 tools/make_layer_files.py && python3 tools/make_element_files.py info-head info-loc info-time
#   for el in info-head info-loc info-time; do
#     npx hyperframes render -c capcut-el-$el.html --format png-sequence -q delivery -o renders/el_$el; done
#   bash tools/encode_elements.sh
set -euo pipefail
cd "$(dirname "$0")/.."
P=../capcut_pack/06_ELEMENTS_WHERE_WHEN
mkdir -p "$P"
while read -r el name ss; do
  dur=$(python3 -c "print(round(30.6-$ss,2))")
  IN=(-framerate 30 -start_number 1 -i "renders/el_$el/frame_%06d.png")
  ffmpeg -nostdin -v error -y "${IN[@]}" -ss "$ss" -t "$dur" -c:v prores_ks -profile:v 4 -pix_fmt yuva444p10le \
    -alpha_bits 8 -qscale:v 9 -vendor apl0 "$P/$name.mov"
  ffmpeg -nostdin -v error -y -f lavfi -i "color=c=0x00FF00:s=1920x1080:r=30" "${IN[@]}" -t "$dur" \
    -filter_complex "[1:v]trim=start=$ss:duration=$dur,setpts=PTS-STARTPTS[g];[0:v][g]overlay=format=auto:shortest=1,format=yuv420p" \
    -c:v libx264 -crf 14 -an -movflags +faststart "$P/${name}_green.mp4"
  echo "$name start=$ss dur=$dur"
done <<'LIST'
info-head A_where_when_title 26.0
info-loc B_location_card 26.2
info-time C_time_card 26.7
LIST
