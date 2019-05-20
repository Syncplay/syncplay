#! /bin/bash

set -x
set -e

# use RAM disk if possible
if [ "$CI" == "" ] && [ -d /dev/shm ]; then
    TEMP_BASE=/dev/shm
else
    TEMP_BASE=/tmp
fi

BUILD_DIR=$(mktemp -d -p "$TEMP_BASE" appimagelint-build-XXXXXX)

cleanup () {
    if [ -d "$BUILD_DIR" ]; then
        rm -rf "$BUILD_DIR"
    fi
}

trap cleanup EXIT

# store repo root as variable
REPO_ROOT=$(readlink -f $(dirname $(dirname "$0")))
#REPO_ROOT="."
OLD_CWD=$(readlink -f .)

pushd "$BUILD_DIR"

wget https://github.com/TheAssassin/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
wget https://raw.githubusercontent.com/linuxdeploy/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh

chmod +x linuxdeploy*.AppImage
chmod +x linuxdeploy*.sh

# set up custom AppRun script
cat > AppRun.sh <<\EAT
#! /bin/sh
# make sure to set APPDIR when run directly from the AppDir
if [ -z $APPDIR ]; then APPDIR=$(readlink -f $(dirname "$0")); fi
export LD_LIBRARY_PATH="$APPDIR"/usr/lib
export PATH="$PATH":"$APPDIR"/usr/bin

exec "$APPDIR"/usr/bin/python "$APPDIR"/usr/bin/syncplay "$@"
EAT
chmod +x AppRun.sh

#export CONDA_PACKAGES="Pillow"
export PIP_REQUIREMENTS="."
export PIP_WORKDIR="$REPO_ROOT"
export VERSION="$(cat $REPO_ROOT/syncplay/__init__.py | awk '/version/ {gsub("\047", "", $3); print $NF}')"
export OUTPUT=Syncplay-$VERSION-x86_64.AppImage

./linuxdeploy-x86_64.AppImage --appdir AppDir --plugin conda \
    -e $(which readelf) \
    -i "$REPO_ROOT"/syncplay/resources/syncplay.png -d "$REPO_ROOT"/syncplay/resources/syncplay.desktop \
    --output appimage --custom-apprun AppRun.sh

mv Syncplay*.AppImage "$OLD_CWD"