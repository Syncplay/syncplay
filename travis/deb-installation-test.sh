#!/bin/sh

sudo apt install /tmp/syncplay.deb -y
syncplay --no-gui
sudo apt remove syncplay
