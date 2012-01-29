from setuptools import setup, find_packages
import sys

if sys.version_info < (3,):
    print('Sorry, this package is developed for Python 3')
    exit(1)

setup(
    name = 'pyhaa',
    version = '0.0',
    packages = find_packages(exclude=['tests']),
    author = 'Tomasz Kowalczyk',
    author_email = 'code@fluxid.pl',
    description = 'Standalone templating system inspired by HAML',
    keywords = 'haml templating',
    tests_require = ['nose'],
    test_suite = 'nose.collector',
)

