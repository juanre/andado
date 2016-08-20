# -*- coding: utf-8 -*-
"""tagtext

Tagged text files.
"""
from __future__ import division

import hashlib
import os
import datetime
from dateutil.parser import parse as parse_date

import andado.tools as T


class TagText(object):
    def __init__(self, timestamp, lat, lng, text, md5=None, utc_timestamp=None):
        self._timestamp = timestamp
        self._lat, self._lng = lat, lng

        if utc_timestamp is None:
            utc_timestamp = T.local_to_utc(lat, lng, timestamp)
        self._utc_timestamp = utc_timestamp

        self.text = text
        if md5 is None:
            m = hashlib.md5()
            m.update(text + str(timestamp) + str(lat) + str(lng))
            md5 = m.hexdigest()
        self._md5 = md5

    @classmethod
    def load(cls, fname):
        lines = open(fname, 'r').readlines()
        def _header():
            i = 0
            for l in lines:
                if l.strip():
                    i += 1
                else:
                    return lines[0:i], lines[i+1:]
        header, text = _header()

        lat, lng, timestamp, utc, md5 = None, None, None, None, None
        for l in header:
            tag, data = l.split(': ')
            if tag.lower() == 'lat, long':
                lat, lng = (float(c) for c in data.split(','))
            elif tag.lower() == 'local datetime':
                timestamp = parse_date(data)
            elif tag.lower() == 'utc datetime':
                utc = parse_date(data)
            elif tag.lower() == 'md5':
                md5 = data

        assert lat is not None
        assert lng is not None
        assert timestamp is not None

        return cls(timestamp, lat, lng, ''.join(text), md5, utc)

    def file_name(self, dirname):
        """Build a standard file name for the tagged text.

        >>> TagText(datetime.datetime(2004, 7, 9, 21, 32, 44),
        ...         41.2, 1.01, 'This text with  words and more').file_name('.')
        './2004-07-09-213244--this-text-with-words.txt'
        """
        return T.meta_fname(self._timestamp,
                            self.text.replace('\n', ' ').lower().split(),
                            dirname, nkeywords=4) + '.txt'

    def save(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(self.file_name(dirname), 'w') as fout:
            fout.write('lat, long: %.6f, %.6f\n' % (self._lat, self._lng))
            fout.write('local datetime: %s\n' % str(self._timestamp))
            if self._utc_timestamp is not None:
                fout.write('UTC datetime: %s\n' % str(self._utc_timestamp))
            fout.write('MD5: %s\n\n' % self._md5)
            fout.write(self.text)


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

        TagText(datetime.datetime(2004, 7, 9, 7, 2, 4),
                41.2, 1.01, 'This text with  words and more').save('.')

        TagText.load('otro.txt').save('.')


if __name__ == '__main__':
    main()
