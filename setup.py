#!/usr/bin/env python3

import os
import setuptools

from syncplay import projectURL, version as syncplay_version

def read(fname):
    with open(fname, 'r') as f:
        return f.read()

installRequirements = read('requirements.txt').splitlines()
guiRequirements = read('requirements_gui.txt').splitlines()

setuptools.setup(
    name="syncplay",
    version=syncplay_version,
    author="Syncplay",
    author_email="dev@syncplay.pl",
    description=' '.join([
        'Client/server to synchronize media playback',
        'on mpv/VLC/MPC-HC/MPC-BE on many computers'
    ]),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    url=projectURL,
    download_url=projectURL + 'download/',
    packages=setuptools.find_packages(),
    install_requires=installRequirements,
    extras_require={
        'gui': guiRequirements,
    },
    python_requires=">=3.4",
    entry_points={
        'console_scripts': [
            'syncplay-server = syncplay.ep_server:main',
        ],
        'gui_scripts': [
            'syncplay = syncplay.ep_client:main [gui]',
        ]
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X :: Cocoa",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Framework :: Twisted",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: English",
        "Natural Language :: German",
        "Natural Language :: Italian",
        "Natural Language :: Russian",
        "Natural Language :: Spanish",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video"
    ],
)
