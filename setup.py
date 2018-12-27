#!/usr/bin/env python
"""
Created : 27-12-2018
Last Modified : Thu 27 Dec 2018 05:50:10 PM EST
Created By : Enrique D. Angola
"""

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="FieldDataAnalysisLibrary",
    version="0.0.1",
    author="NRG Systems",
    author_email="eda@nrgsystems.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/eangola/analysislibrary",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    setup_requires=["pytest-runner"],
    test_require=["pytest"])

