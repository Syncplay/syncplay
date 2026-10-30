#!/bin/bash

# Copyright (C) 2019 Syncplay
# This file is licensed under the MIT license - http://opensource.org/licenses/MIT

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

set -x
set -e

# first argument selects the fuse variant:
#   fuse2 -> Ubuntu 22.04 and older (libfuse2)
#   fuse3 -> Ubuntu 24.04 and newer (libfuse3)
# anything else (or no argument) builds both variants
FUSE_VARIANT="${1:-both}"

# use RAM disk if possible
if [ "$CI" == "" ] && [ -d /dev/shm ]; then
    TEMP_BASE=/dev/shm
else
    TEMP_BASE=/tmp
fi

BUILD_DIR=$(mktemp -d -p "$TEMP_BASE" appimage-build-XXXXXX)

cleanup () {
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
}

trap cleanup EXIT

# store repo root as variable
REPO_ROOT=$(readlink -f $(dirname $(dirname "$0")))
OLD_CWD=$(readlink -f .)

pushd "$BUILD_DIR"

wget https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
wget https://raw.githubusercontent.com/linuxdeploy/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage

chmod +x linuxdeploy*.AppImage
chmod +x linuxdeploy*.sh
chmod +x appimagetool*.AppImage

# set up custom AppRun script
cat > AppRun.sh <<\EAT
#!/bin/bash
# make sure to set APPDIR when run directly from the AppDir
if [ -z $APPDIR ]; then APPDIR=$(readlink -f $(dirname "$0")); fi
export LD_LIBRARY_PATH="$APPDIR"/usr/lib
export PATH="$PATH":"$APPDIR"/usr/bin

if [ "$1" == "--server" ]; then
    exec "$APPDIR"/usr/bin/python "$APPDIR"/usr/bin/syncplay-server "${@:2}"
else
    exec "$APPDIR"/usr/bin/python "$APPDIR"/usr/bin/syncplay "$@"
fi
EAT
chmod +x AppRun.sh

# add AppStream metadata
mkdir -p AppDir/usr/share/metainfo/
cat > pl.syncplay.syncplay.appdata.xml <<\EAT
<?xml version="1.0" encoding="UTF-8"?>
<component type="desktop-application">
    <id>pl.syncplay.syncplay</id>
    <metadata_license>MIT</metadata_license>
    <project_license>Apache-2.0</project_license>
    <name>Syncplay</name>
    <summary>Client/server to synchronize media playback on mpv/VLC/MPC-HC/MPC-BE on many computers</summary>
    <description>
        <p>Syncplay synchronises the position and play state of multiple media players so that the viewers can watch the same thing at the same time. This means that when one person pauses/unpauses playback or seeks (jumps position) within their media player then this will be replicated across all media players connected to the same server and in the same 'room' (viewing session). When a new person joins they will also be synchronised. Syncplay also includes text-based chat so you can discuss a video as you watch it (or you could use third-party Voice over IP software to talk over a video).</p>
    </description>
    <launchable type="desktop-id">pl.syncplay.syncplay.desktop</launchable>
    <url type="homepage">https://syncplay.pl/</url>
    <screenshots>
        <screenshot type="default">
            https://syncplay.pl/2019-05-26.png</image>
        </screenshot>
    </screenshots>
    <provides>
        <id>pl.syncplay.syncplay.desktop</id>
    </provides>
</component>
EAT
mv pl.syncplay.syncplay.appdata.xml AppDir/usr/share/metainfo/

# move and rename .desktop file
cp "$REPO_ROOT"/syncplay/resources/syncplay.desktop ./pl.syncplay.syncplay.desktop

#export CONDA_PACKAGES="Pillow"
export PIP_REQUIREMENTS="."
export PIP_WORKDIR="$REPO_ROOT"
export VERSION="$(cat $REPO_ROOT/syncplay/__init__.py | awk '/version/ {gsub("\047", "", $3); print $NF}')"

# build the AppDir with linuxdeploy (no --output appimage yet)
./linuxdeploy-x86_64.AppImage --appdir AppDir --plugin conda \
    -e $(which readelf) \
    -i "$REPO_ROOT"/syncplay/resources/syncplay.png -d pl.syncplay.syncplay.desktop \
    --custom-apprun AppRun.sh \
    -l /usr/lib/x86_64-linux-gnu/libgthread-2.0.so.0 \
    -l /usr/lib/x86_64-linux-gnu/libxkbcommon-x11.so.0 \
    -l /usr/lib/x86_64-linux-gnu/libxcb.so.1

# build a single appimage variant using appimagetool directly
build_appimage () {
    local type="$1"
    local suffix="$2"

    ./appimagetool-x86_64.AppImage --appimage-type="$type" AppDir "$OLD_CWD/Syncplay-$VERSION${suffix}-x86_64.AppImage"
}

# fuse2 appimage: runs on Ubuntu 22.04 and older
if [ "$FUSE_VARIANT" = "fuse2" ] || [ "$FUSE_VARIANT" = "both" ]; then
    build_appimage appimage-2.0 ""
fi

# fuse3 appimage: runs on Ubuntu 24.04 and newer
if [ "$FUSE_VARIANT" = "fuse3" ] || [ "$FUSE_VARIANT" = "both" ]; then
    build_appimage appimage-3.0 "-fuse3"
fi
