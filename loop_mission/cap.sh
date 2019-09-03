#!/bin/bash

set -e

ADB=/home/luzi82/Android/Sdk/platform-tools/adb
T=`date +%Y%m%d%H%M%S`

${ADB} exec-out screencap -p > 0.png
convert 0.png -resize 90x160 1.png
mv 1.png ${T}.png

rm 0.png
