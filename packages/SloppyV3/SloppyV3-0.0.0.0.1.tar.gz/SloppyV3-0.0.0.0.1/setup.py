#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# File: setup.py
# Project: Sloppy
# Created Date: 2022-12-13, 09:28:34
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Mon May 15 2023
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
from glob import glob
from os.path import basename, splitext
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SloppyV3",
    version="0.0.0.0.01",
    author="Chungman Kim",
    author_email="h2noda@gmail.com",
    description="Python module - SloppyV3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "beautifulsoup4",
        "openpyxl",
        "rich",
        "python-dateutil",
        "paramiko",
        "cryptography",
    ],
    url="https://github.com/Cheung-man/SloppyV3.git",
    py_modules=[
        "SloppyV3/common",
        "SloppyV3/error",
        "SloppyV3/excel",
        "SloppyV3/json",
        "SloppyV3/database",
        "SloppyV3/config",
        "SloppyV3/log",
        "SloppyV3/remote",
        "SloppyV3/database",
    ],
    python_requires=">=3.11",
)
