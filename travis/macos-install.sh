#!/usr/bin/env bash

set -ex

export HOMEBREW_NO_INSTALL_CLEANUP=1

# Reinstall openssl to fix Python pip install issues
brew upgrade https://raw.githubusercontent.com/Homebrew/homebrew-core/e9004bd764c9436750a50e0b428548f68fe6a38a/Formula/openssl@1.1.rb

# Python 3.7.4 with 10.12 bottle
brew upgrade https://raw.githubusercontent.com/Homebrew/homebrew-core/e9004bd764c9436750a50e0b428548f68fe6a38a/Formula/python.rb

which python3
python3 --version
which pip3
pip3 --version

# Pyside 5.13.0 for 10.12 bottle
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/99219f0923014b24f33eae624fbfe83772c35f54/Formula/pyside.rb

# Explicitly upgrade Qt 5.13.1 as the pyside above needs it
brew upgrade https://raw.githubusercontent.com/Homebrew/homebrew-core/dcc34dd3cb24cb4f7cfa0047ccdb712d7cc4c6e4/Formula/qt.rb

python3 -c "from PySide2 import __version__; print(__version__)"
python3 -c "from PySide2.QtCore import __version__; print(__version__)" 
python3 -c "import ssl; print(ssl)"
pip3 install py2app
python3 -c "from py2app.recipes import pyside2"
pip3 install twisted[tls] appnope requests certifi
