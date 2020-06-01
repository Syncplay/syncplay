#!/bin/sh

set -x
set -e

mkdir -p /tmp/syncplay/DEBIAN

echo "Package: syncplay
Version: "$(sed -n -e "s/^.*version = //p" syncplay/__init__.py | sed "s/'//g")""$(git describe --exact-match --tags HEAD &>/dev/null && echo -git-$(date -u +%y%m%d%H%M))"
Architecture: all
Maintainer: <dev@syncplay.pl>
Depends: python3 (>= 3.4), python3-pyside2.qtwidgets (>= 5.12.0), python3-twisted (>= 16.4.0), python3-certifi, mpv (>= 0.23) | vlc (>= 2.2.1)
Homepage: https://syncplay.pl
Section: web
Priority: optional
Description: Solution to synchronize video playback across multiple instances of mpv, VLC, MPC-HC and MPC-BE over the Internet.
 Syncplay synchronises the position and play state of multiple media players so that the viewers can watch the same thing at the same time. This means that when one person pauses/unpauses playback or seeks (jumps position) within their media player then this will be replicated across all media players connected to the same server and in the same 'room' (viewing session). When a new person joins they will also be synchronised. Syncplay also includes text-based chat so you can discuss a video as you watch it (or you could use third-party Voice over IP software to talk over a video)." \
> /tmp/syncplay/DEBIAN/control
echo "#!/bin/sh
py3clean -p syncplay
"
> /tmp/syncplay/DEBIAN/prerm
chmod 555 /tmp/syncplay/DEBIAN/prerm

make install DESTDIR=/tmp/syncplay
dpkg -b /tmp/syncplay/

