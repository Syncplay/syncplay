#!/usr/bin/env bash

rm -rf build dist dist_dmg
python3 buildPy2app.py py2app
mkdir dist_dmg
cp resources/macOS_legacy_readme.pdf resources/.macOS_readme.pdf
export VER="$(cat syncplay/__init__.py | awk '/version/ {gsub("\047", "", $3); print $NF}')"
dmgbuild -s appdmg.py "Syncplay" dist_dmg/Syncplay_${VER}_macOS_legacy.dmg
