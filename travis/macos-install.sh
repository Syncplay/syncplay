#!/usr/bin/env bash

set -ex

brew install python3
which python3
python3 --version
which pip3
pip3 --version
brew install pyside
python3 -c "from PySide2 import __version__; print(__version__)"
python3 -c "from PySide2.QtCore import __version__; print(__version__)" 
pip3 install py2app
python3 -c "from py2app.recipes import pyside2"
pip3 install twisted[tls] appnope requests certifi
