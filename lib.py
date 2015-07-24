# -*- coding: utf8 -*-
import argparse
from calendar import TimeEncoding, month_name
from datetime import datetime


def get_local_month(m, locale='ru_RU'):
    with TimeEncoding(locale):
        return month_name[m].decode('utf8')


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)
