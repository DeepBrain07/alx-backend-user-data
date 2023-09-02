#!/usr/bin/env python3
""" This module defines a 'filter_datum' function
"""
import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """ This function returns the log message obfuscated """
    for m in message.split(separator):
        if m.split('=')[0] in fields:
            message = re.sub(r""+m.split('=')[1], redaction, message)
    return message
