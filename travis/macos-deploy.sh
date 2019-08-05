#!/usr/bin/env bash

mkdir dist/Syncplay.app/Contents/Resources/English.lproj
mkdir dist/Syncplay.app/Contents/Resources/en_AU.lproj
mkdir dist/Syncplay.app/Contents/Resources/en_GB.lproj
mkdir dist/Syncplay.app/Contents/Resources/German.lproj
mkdir dist/Syncplay.app/Contents/Resources/Italian.lproj
mkdir dist/Syncplay.app/Contents/Resources/ru.lproj
mkdir dist/Syncplay.app/Contents/Resources/Spanish.lproj
mkdir dist/Syncplay.app/Contents/Resources/es_419.lproj
pip3 install dmgbuild
mv syncplay/resources/macOS_readme.pdf syncplay/resources/.macOS_readme.pdf
dmgbuild -s appdmg.py "Syncplay" dist_bintray/Syncplay_${VER}.dmg
