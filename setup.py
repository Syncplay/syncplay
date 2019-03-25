#!/usr/bin/env python

from os.path import dirname, join
from setuptools import find_packages, setup
from setuptools.command import build_py, install_scripts
from syncplay import projectURL, version


def setup_dir(*args):
    return join(dirname(__file__), *args)


def read(fname):
    with open(setup_dir(fname), 'r') as f:
        return f.read()


class BuildPy(build_py.build_py):
    def run(self):
        self.copy_tree(
            setup_dir('resources'),
            setup_dir('syncplay', 'resources')
        )
        build_py.build_py.run(self)


class InstallScripts(install_scripts.install_scripts):
    def run(self):
        install_scripts.install_scripts.run(self)
        scripts = []
        for script in self.outfiles:
            old_suff = script[-9:]
            new_suff = '-server' if old_suff == 'Server.py' else ''
            new_script = script.replace(old_suff, new_suff)
            self.move_file(script, new_script)
            scripts.append(new_script)
        self.outfiles = scripts


setup(
    name='Syncplay',
    version=version,
    license='Apache 2.0',
    author='Uriziel',
    maintainer='Et0h',
    url=projectURL,
    download_url=projectURL + 'download/',
    description=' '.join([
        'Client/server to synchronize media playback',
        'on mpv/VLC/MPC-HC/MPC-BE on many computers'
    ]),
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    package_data={'syncplay': ['resources/*']},
    python_requires='>=3.4',
    scripts=['syncplayClient.py', 'syncplayServer.py'],
    install_requires=read('requirements.txt').splitlines(),
    cmdclass={
        'build_py': BuildPy,
        'install_scripts': InstallScripts
    },
    extras_require={
        'gui': read('requirements_gui.txt').splitlines(),
        'tls': read('requirements_tls.txt').splitlines()
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications :: Qt',
        'Framework :: Twisted',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Natural Language :: German',
        'Natural Language :: Italian',
        'Natural Language :: Russian',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Multimedia',
    ]
)

