# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

from setuptools import find_packages, setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()


version = '0.1'

setup(
    name='iso4217parse',
    version=version,
    packages=find_packages(),
    install_requires=[],
    author='Tammo Ippen',
    author_email='tammo.ippen@posteo.de',
    description='Parse currencies (symbols and codes) from and to ISO4217.',
    long_description=long_description,
    url='https://github.com/tammoippen/iso4217parse',
    license='MIT',
    download_url='https://github.com/tammoippen/iso4217parse/archive/v{}.tar.gz'.format(version),
    keywords=[],
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ]
)
