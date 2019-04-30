#!/usr/bin/env bash

pip3 install dmgbuild
mv syncplay/resources/macOS_readme.pdf syncplay/resources/.macOS_readme.pdf
dmgbuild -s appdmg.py "Syncplay" dist_bintray/Syncplay_${VER}.dmg
