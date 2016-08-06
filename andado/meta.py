# -*- coding: utf-8 -*-
"""meta

Extract date, coordinates and MD5 from files.
"""
from __future__ import division

import subprocess
import os
from dateutil.parser import parse as parse_date


def from_photo(fname):
    exifpars = ['exiftool', '-ee', '-s', '-S',
                '-d', '%Y-%m-%d %H:%m:%S', '-c', '%+.6f']

    def _date(fname):
        for tag in ['-DateTimeOriginal', '-CreateDate']:
            dt = subprocess.check_output(exifpars + [tag, fname]).strip()
            if dt:
                return parse_date(dt)
        return None

    def _position(fname):
        coords = subprocess.check_output(exifpars +
                                         ['-GPSPosition', fname]).strip()
        if coords:
            return [float(c) for c in coords.split(', ')]
        return None

    def _md5(fname):
        # Should look for a tag containing it in the file, and only compute
        # if if the tag is not there.
        return subprocess.check_output(['md5', '-q', fname]).strip()

    return _date(fname), _position(fname), _md5(fname)


def meta_fname(date, keywords, dirname, ext):
    if len(keywords) > 3:
        keywords = keywords[:3]
    dirname = os.path.join(dirname, date.strftime('%Y'))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    if ext:
        ext = '.' + ext
    return os.path.join(dirname,
                        date.strftime('%Y-%m-%d-%H%M%S') +
                        '-'.join([''] + keywords)) + ext


def photo_fname(org_fname, keywords, dirname, ext):
    return meta_fname(from_photo(org_fname)[0], keywords, dirname, ext)

def main():
    import sys
    print from_photo(sys.argv[1])
    print meta_fname(from_photo(sys.argv[1])[0], [], '.')


if __name__ == '__main__':
    main()
