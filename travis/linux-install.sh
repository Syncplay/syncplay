#!/usr/bin/env bash

sudo groupadd --system lxd
sudo usermod -a -G lxd $USER
sudo apt-get -qq update
sudo apt-get -y install snapd
sudo snap install lxd
sudo lxd.migrate -yes
sudo lxd waitready
sudo lxd init --auto --storage-backend dir
sudo snap install snapcraft --classic
