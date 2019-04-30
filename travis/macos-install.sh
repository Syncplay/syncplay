#!/usr/bin/env bash

brew update
brew upgrade python
which python3
python3 --version
which pip3
pip3 --version
curl -L https://raw.githubusercontent.com/Homebrew/homebrew-core/dd6c67c1ba664c8910fe96aeb58f9938d97d9a53/Formula/pyside.rb -o pyside.rb
brew install ./pyside.rb
python3 -c "from PySide2 import __version__; print(__version__)"
python3 -c "from PySide2.QtCore import __version__; print(__version__)" 
pip3 install py2app
python3 -c "from py2app.recipes import pyside2"
pip3 install twisted[tls] appnope requests certifi
