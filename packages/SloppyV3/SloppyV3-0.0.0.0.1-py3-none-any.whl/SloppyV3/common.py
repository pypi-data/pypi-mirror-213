#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
# File: common.py
# Project: SloppyV3
# Created Date: 2023-02-03, 10:15:28
# Author: Chungman Kim(h2noda@unipark.kr)
# Last Modified: Mon May 15 2023
# Modified By: Chungman Kim
# Copyright 2023. Chungman Kim
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
"""

from datetime import date, timedelta, datetime
from dateutil.relativedelta import *
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.theme import Theme
from cryptography.fernet import Fernet


class Datetime:
    def get_today(format="%Y%m%d"):
        """금일 날짜 반환

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m%d".

        Returns:
            _type_: _description_
        """
        retval = date.today().strftime(format)

        return retval

    def get_now(format="%Y-%m-%d %H:%M:%S"):
        """Return Now Datetime

        Args:
            strformat (str, optional): Now. Defaults to "%Y-%m-%d %H:%M:%S".

        Returns:
            _type_: _description_
        """
        retval = datetime.now().strftime(format)

        return retval

    def get_thismonth(format="%Y%m"):
        """Return This month

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = date.today().strftime(format)

        return retval

    def get_yesterday(format="%Y%m%d"):
        """Return Yesterday

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = date.today() - timedelta(1)
        retval = retval.strftime(format)

        return retval

    def get_previousmonth(format="%Y%m"):
        """Return Previous month

        Args:
            strformat (str, optional): _description_. Defaults to "%Y%m".

        Returns:
            _type_: _description_
        """
        retval = datetime.today() + relativedelta(months=-1)
        retval = retval.strftime(format)

        return retval


class Message:
    def __init__(self):
        self.console = Console()

    def prefix(self, indent=0, indent_char="-"):
        retval = ""
        if indent != 0:
            retval = "  " * indent + indent_char + " "
        return retval

    def tagstyle(self, color, bold=False):
        """Tag Style of Text

        Args:
            color (String): Color of Text
            bold (bool, optional): Bold of Text. Defaults to False.

        Returns:
            String: bold + color
        """
        retval = color
        if bold == True:
            retval = "bold " + color
        return retval

    def repeat_char(self, char="#", repeat=35, color="green"):
        retval = char * repeat
        self.print_msg(retval, 0, "", color, True)

    def print_msg(self, messgae, indent_char="-", indent=0, color="white", bold=False):
        retstyle = self.tagstyle(color, bold)
        retval = (
            self.prefix(indent_char, indent)
            + "["
            + retstyle
            + "]"
            + messgae
            + "[/"
            + retstyle
            + "]"
        )

        self.console.print(retval, style="white")

    def blank(self):
        """Print message : Blank..."""
        Console.print()

    def copyright(self):
        """Print message : "Copyright" """
        self.console.print(
            "\n[bold yellow]Copylight 2023. Chungman Kim. All right reserved.[/bold yellow]\n"
        )

    def ok(self, indent=0, indent_char="-"):
        """Print message : "OK"

        Args:
            p_indent (int, optional): Indent level. Defaults to 0.
            p_indent_char (str, optional): Indent character. Defaults to "-".
        """
        strprefix = self.prefix(indent, indent_char)
        strstyle = self.tagstyle("dark_orange", False)
        print_txt = strprefix + "[" + strstyle + "]OK" + "[/" + strstyle + "]"
        self.console.print(print_txt, style="white")

    def title(self, message, color="green", prefix_char="#"):
        lenth_message = len(message)
        self.blank()
        self.repeat_char(prefix_char, lenth_message + 6, color)
        self.print_msg(
            prefix_char + "   " * lenth_message + "  " + prefix_char + " ",
            0,
            "",
            color,
            True,
        )
        self.print_msg("#  " + message + "  #", 0, "", color, True)
        self.print_msg("#  " + " " * lenth_message + "  #", 0, "", color, True)
        self.repeat_char(prefix_char, lenth_message + 6, color)
        self.blank()

    def input(self, val, indent=0, indent_char="-", color="white", bold=False):
        styletag = self.tagstyle(color, bold)
        strinput = (
            self.prefix(indent_char, indent)
            + "["
            + styletag
            + "]"
            + val
            + "[/"
            + styletag
            + "]"
        )
        return self.console.input(strinput)

    def input_passwd(self, val, indent=0, indent_char="-", color="white", bold=False):
        strprefix = self.prefix(indent, indent_char)
        styletag = self.tagstyle(color, bold)
        strinput = strprefix + "[" + styletag + "]" + val + "[/" + styletag + "]"
        return self.console.input(strinput, password=True)


class Security:
    def __init__(self):
        self.key = b"saaBmbqfWWEi8__MqR6Ly3nDUstkI8iLpDst9b0rkpM="
        self.f = Fernet(self.key)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    def encrypt_string(self, data, is_out_string=True):
        """바이트 형태이면 암호화, 아니면 인코딩 후  암호화 수행
            출력이 문자열이면 디코딩 후 리턴

        Args:
            data (_type_): _description_
            is_out_string (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        if isinstance(data, bytes):
            retval = self.f.encrypt(data)
        else:
            retval = self.f.encrypt(data.encode("utf-8"))
        if is_out_string is True:
            return retval.decode("utf-8")
        else:
            return retval

    def decrypt_string(self, data, is_out_string=True):
        """
            - 바이트 형태이면 즉시 복호화
            - 문자열이면 인코딩 후 복호화
            - retval이 문자열이며 디코딩 후 반환

        Args:
            data (_type_): _description_
            is_out_string (bool, optional): _description_. Defaults to True.
        Returns:
            _type_: _description_
        """
        if isinstance(data, bytes):
            retval = self.f.decrypt(data)
        else:
            retval = self.f.decrypt(data.encode("utf-8"))
        if is_out_string is True:
            return retval.decode("utf-8")
        else:
            return retval
