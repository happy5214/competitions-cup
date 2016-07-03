# -*- coding: utf-8  -*-
"""A setuptools based setup module."""

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='competitions-cup',
    version='0.3.2',

    description='Generic cup competitions',
    long_description=long_description,

    url='https://github.com/happy5214/competitions-cup',

    author='Alexander Jones',
    author_email='happy5214@gmail.com',

    license='LGPLv3+',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='competitions cups knockout elimination',

    packages=find_packages(exclude=['docs', 'tests*']),

    namespace_packages=['competitions'],

    test_suite='tests',

    install_requires=['competitions-match>=0.1.3'],

    entry_points={
        'competitions.cup.types': [
            ('competitions.poweroftwo_single = '
             'competitions.cup.default.PowerOfTwoSingleEliminationCup:'
             'PowerOfTwoSingleEliminationCup'),
            ('competitions.poweroftwo_double = '
             'competitions.cup.default.PowerOfTwoDoubleEliminationCup:'
             'PowerOfTwoDoubleEliminationCup'),
            ('competitions.stepladder = '
             'competitions.cup.default.StepladderCup:'
             'StepladderCup')
        ]
    },
)
