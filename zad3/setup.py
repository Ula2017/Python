#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='analyzer',
    version='0.1.0',
    install_requires=[
        "bs4",
        "fuzzywuzzy",
        "google",
    ],
    description="This project analyzes whether the given sentence is true or false",
    author="Urszula Sobon",
    author_email='urszulasobon1996@gmail.com',
    url='https://github.com/Ula2017/complexity',
    packages=['analyzer'],
    include_package_data=True,
    license="GNU General Public License v3",
    zip_safe=False,

)
