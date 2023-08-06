#!/usr/bin/env python3
# -*- coding:utf-8 -*-
'''
# File: error.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:17:04
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Mon Jul 18 2022
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
'''


class EmptyValueError(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value


class ConfirmPasswordError(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value


class ParameterCountError(Exception):
    # 생성할때 value 값을 입력 받는다.
    def __init__(self, value):
        self.value = value

    # 생성할때 받은 value 값을 확인 한다.
    def __str__(self):
        return self.value
