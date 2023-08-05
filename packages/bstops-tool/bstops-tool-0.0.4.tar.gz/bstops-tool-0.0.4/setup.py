#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name = 'bstops-tool',
    version = '0.0.4',
    keywords = ['pip', 'tool', 'bstops'],
    description = 'Tool package',
    license = 'MIT Licence',

    url = 'https://github.com/viger1228/bstops-tool',
    author = 'walker',
    author_email = 'walkerIVI@gmail.com',

    packages = find_packages(),
    include_package_data = True,
    platforms = 'any',
    install_requires = [
        'requests',
        'prettytable',
        'bitarray',
    ]
)
