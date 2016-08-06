# -*- coding: utf-8 -*-
"""tagtext

Tagged text files.
"""
from __future__ import division

import hashlib
import os
import datetime

from andado.meta import meta_fname


class TagText(object):
    def __init__(self, date, lat, lng, text, md5=None):
        self._date = date
        self._lat, self._lng = lat, lng
        self.text = text
        if md5 is None:
            m = hashlib.md5()
            m.update(text + str(date) + str(lat) + str(lng))
            md5 = m.hexdigest()
        self._md5 = md5

    def fname(self, dirname='.'):
        """

        >>> TagText(datetime.datetime(2004, 7, 9, 21, 32, 44),
        ...         41.2, 1.01, 'This text with  words').fname()
        './2004/2004-07-09-213244-this-text-with.txt'
        """
        return meta_fname(self._date,
                          self.text.replace('\n', ' ').lower().split(),
                          dirname, 'txt')


def _doctest():
    import doctest
    doctest.testmod()


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    # https://docs.python.org/3.3/howto/argparse.html
    parser.add_argument('-t', '--test', help='run tests', action="store_true")
    args = parser.parse_args()
    if args.test:
        _doctest()


if __name__ == '__main__':
    main()
