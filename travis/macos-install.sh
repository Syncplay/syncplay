#!/usr/bin/env bash

set -ex

export HOMEBREW_NO_INSTALL_CLEANUP=1
brew update

# An error occurs when upgrading Python, but appears to be benign, hence the "|| true"
#
# Error: undefined method `any?' for nil:NilClass
# /usr/local/Homebrew/Library/Homebrew/cmd/upgrade.rb:227:in `depends_on'
brew upgrade python || true

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
