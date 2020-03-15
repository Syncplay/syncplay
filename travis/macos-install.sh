#!/usr/bin/env bash

set -ex

export HOMEBREW_NO_INSTALL_CLEANUP=1

# Python 3.7.4 with 10.12 bottle
brew upgrade https://raw.githubusercontent.com/Homebrew/homebrew-core/e9004bd764c9436750a50e0b428548f68fe6a38a/Formula/python.rb

which python3
python3 --version
which pip3
pip3 --version

# Explicitly install Qt 5.13.1 as that has both 10.12 compatibility, and a pre-built bottle
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/dcc34dd3cb24cb4f7cfa0047ccdb712d7cc4c6e4/Formula/qt.rb

brew install albertosottile/syncplay/pyside
python3 -c "from PySide2 import __version__; print(__version__)"
python3 -c "from PySide2.QtCore import __version__; print(__version__)" 
pip3 install py2app
python3 -c "from py2app.recipes import pyside2"
pip3 install twisted[tls] appnope requests certifi
