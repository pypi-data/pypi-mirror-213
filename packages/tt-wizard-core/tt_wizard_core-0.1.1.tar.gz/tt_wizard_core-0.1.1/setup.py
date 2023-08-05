#!/usr/bin/env python

from setuptools import setup
import setuptools

with open("README.md", "r", encoding='utf-8') as file:
    long_description = file.read()

setup(
    name = 'tt_wizard_core',
    version = '0.1.1',
    description = 'Tool to download and manage gme-files. Core of TT_WIZARD.',
    long_description = long_description,
    long_description_content_type='text/markdown',

    py_modules = ["tt_wizard_core"],
    package_dir = {'': 'src'},

    author="BumblebeeMan (Dennis Schweer)", 
    author_email="dennis@bumblebeeman.engineer",     
    url="https://github.com/BumblebeeMan/tt_wizard_core",

    install_requires=["requests >= 2.30.0"],

    python_requires=">=3.7",

    keywords=["TipToi", "TipTio", "tip", "toi", "tio"],

    classifiers=["Development Status :: 4 - Beta",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Operating System :: OS Independent",
                 "Programming Language :: Python :: 3",
                 "Programming Language :: Python :: 3 :: Only",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Programming Language :: Python :: 3.11",
                 "Topic :: Multimedia",
                 "Topic :: Multimedia :: Sound/Audio",
                 ]  
)