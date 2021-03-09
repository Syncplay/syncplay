#! /bin/bash

wget https://github.com/TheAssassin/appimagelint/releases/download/continuous/appimagelint-x86_64.AppImage
chmod a+x appimagelint-x86_64.AppImage
./appimagelint-x86_64.AppImage Syncplay*.AppImage
mv Syncplay*.AppImage dist_actions/
