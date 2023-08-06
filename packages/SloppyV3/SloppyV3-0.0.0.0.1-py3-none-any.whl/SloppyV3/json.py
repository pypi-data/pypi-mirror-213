#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# File: json.py
# Project: Sloppy
# Created Date: 2022-07-18, 09:17:33
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Thu Jun 08 2023
# Modified By: Chungman Kim
# Copyright (c) 2022 Unipark
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""
import json

from common import Message


class Json:
    def read_jsonfile(p_json_filename):
        """[json 파일 읽기]

        Args:
            p_json_filename ([String]): [JSON 파일명]

        Returns:
            [dict]: [Json Data]
        """
        try:
            with open(p_json_filename, "r", encoding="utf-8") as f:
                json_data = json.load(f)
        except FileNotFoundError:
            Message.print_msg("JSON File Not Found..", 1, "-", "red", True)

        return json_data

    def update_jsonfile(p_json_data, p_update_filepath):
        """[Update JSON file]

        Args:
            json_data ([dict]): [JSON Data]
            update_filepath ([string]): [JSON File path & Name]
        """
        try:
            with open(p_update_filepath, "w", encoding="utf-8") as update_jsonfile:
                update_jsonfile.write(
                    json.dumps(p_json_data, indent=3, ensure_ascii=False)
                )
        except FileNotFoundError:
            Message.print_msg("JSON File Not Found..", 1, "-", "red", True)
