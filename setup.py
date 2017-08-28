#!/usr/bin/env python

import versioneer
from setuptools import setup, find_packages
from codecs import open
from os import path

# Get the long description from the relevant file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='photos3',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),

    description='Cloud-Native Personal Photo Album Experiment',
    long_description=long_description,

    url='https://github.com/tomislacker/photos3',

    author='tomislacker',
    author_email='tomislacker@users.noreply.github.com',

    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='photo-gallery cloud-native',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'boto3',
        'pillow',
        'pyaml',
    ],

    extras_require={
        'dev': [
            'terminaltables',
        ],
        'test': [
        ],
    },

    package_data={},
    data_files=[],
    entry_points={
        'console_scripts': [
        ],
    },
)
