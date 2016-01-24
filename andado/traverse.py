# -*- coding: utf-8 -*-
"""traverse

Search files containing location and date.
"""
from __future__ import division


def _doctest():
    import doctest
    doctest.testmod()


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)

    # https://docs.python.org/3.3/howto/argparse.html
    parser.add_argument('-t', '--test', help='run tests', action="store_true")
    parser.add_argument('-n', '--number', help='a number', type=int)
    parser.add_argument('astring', help='a positional (mandatory) argument')
    args = parser.parse_args()
    if args.test:
        _doctest()
    else:
        print args.astring


if __name__ == '__main__':
    main()
