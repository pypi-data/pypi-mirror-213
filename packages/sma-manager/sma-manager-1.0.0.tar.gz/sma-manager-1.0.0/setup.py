#!/usr/bin/env python3
#  Copyright (c) 2023.
#  All rights reserved to the creator of the following script/program/app, please do not
#  use or distribute without prior authorization from the creator.
#  Creator: Antonio Manuel Nunes Goncalves
#  Email: amng835@gmail.com
#  LinkedIn: https://www.linkedin.com/in/antonio-manuel-goncalves-983926142/
#  Github: https://github.com/DEADSEC-SECURITY

from setuptools import find_packages, setup
import pathlib

README = (pathlib.Path(__file__).parent / "README.md").read_text(encoding='utf8')

setup(
    name='sma-manager',
    packages=find_packages(),
    version='1.0.0',
    description='Package for collecting information from the SMA Manager device of solar panels.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='DeadSec-Security',
    author_email='amng835@gmail.com',
    url='https://github.com/DEADSEC-SECURITY/sma-manager',
    keywords=[
        'sma',
        'sma-manager',
        'manager',
        'sunny-portal',
        'sunny'
    ],
    license='MIT',
    python_requires='>=3.8'
)
