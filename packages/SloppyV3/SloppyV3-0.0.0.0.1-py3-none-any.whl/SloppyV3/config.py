#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: config.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:16:18
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Wed Aug 17 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''
from configparser import ConfigParser


class Config:
    def __init__(self, cfg_file="config.ini"):
        self.cfg_file = cfg_file
        self.cfg_data = ConfigParser()
        self.cfg_data.read(cfg_file, encoding="utf-8")

    def write_config(self):
        with open(self.cfg_file, "w", encoding="utf-8") as self.cfg_file:
            self.cfg_data.write(self.cfg_file)

    def find_data(self, section, key):
        retval = self.cfg_data[section][key]
        return retval
