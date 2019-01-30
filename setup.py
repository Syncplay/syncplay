#!/usr/bin/env python3

import setuptools
import sys

from syncplay import version as syncplay_version

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="syncplay-distutil-test-2",
    version=syncplay_version,
    author="Syncplay",
    author_email="dev@syncplay.pl",
    description="Client/server to synchronize media playback on mpv/MPC-HC/MPC-BE/VLC on many computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.syncplay.pl",
    packages=setuptools.find_packages(),
    install_requires=["twisted", "pyside2", "requests", 'zope.inteface; platform_system=="Windows"',
        'pypiwin32; platform_system=="Windows"', 'appnope; platform_system=="Darwin"'
        ],
    python_requires=">=3.4",
    scripts=['syncplayClient.py', 'syncplayServer.py'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X :: Cocoa",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Multimedia :: Video"
    ],
)