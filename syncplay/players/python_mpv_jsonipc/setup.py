from setuptools import setup
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='python-mpv-jsonipc',
    version='1.1.11',
    author="Ian Walton",
    author_email="iwalton3@gmail.com",
    description="Python API to MPV using JSON IPC",
    license='Apache-2.0',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iwalton3/python-mpv-jsonipc",
    py_modules=['python_mpv_jsonipc'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
