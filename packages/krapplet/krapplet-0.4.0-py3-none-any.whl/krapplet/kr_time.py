#!/usr/bin/env python3

"""
kr_time: functions for time manipulation
(c) 2020-2023 Johannes Willem Fernhout, BSD 3-Clause License applies.
"""

import locale
from datetime import datetime


# remap some datetime functions
now = datetime.now
#timedelta = datetime.timedelta



def timestamp(since_epoch):
    """returns a string according to local locale
    based on seconds since epoch 1-JAN-1970
    if since_epoch is none, an empty string is returned"""
    if since_epoch:
        from_timestamp = datetime.fromtimestamp(since_epoch)
        date_string = from_timestamp.strftime(
            locale.nl_langinfo(locale.D_T_FMT))
        return date_string
    return ""




