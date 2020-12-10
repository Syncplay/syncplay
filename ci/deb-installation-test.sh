#!/bin/sh

set -x
set -e

sudo apt-get -qq update
sudo apt install /tmp/syncplay.deb -y
syncplay --no-gui
sudo apt remove syncplay
