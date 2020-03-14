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

# Workaround for deployment issues with newer openssl.
# See https://travis-ci.community/t/ruby-openssl-python-deployment-fails-on-osx-image/6753/9
for lib in ssl crypto; do ln -s /usr/local/opt/openssl{@1.0,}/lib/lib${lib}.1.0.0.dylib; done
rvm reinstall $(travis_internal_ruby) --disable-binary
for lib in ssl crypto; do rm /usr/local/opt/openssl/lib/lib${lib}.1.0.0.dylib; done
