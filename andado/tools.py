# -*- coding: utf-8 -*-
"""tools

"""
from __future__ import division

import os
import googlemaps
from datetime import timedelta, datetime
import time
# import ConfigParser


def read_config():
    pass


def meta_fname(timestamp, keywords, dirname, nkeywords=5):
    if len(keywords) > nkeywords:
        keywords = keywords[:nkeywords]
    sep = '--' if keywords else ''
    return os.path.join(dirname, timestamp.strftime('%Y-%m-%d-%H%M%S') + sep +
                        '-'.join(keywords))


def local_to_utc(lat, lng, local_timestamp, sleep_after_call=True):
    """Compute the UTC datetime from the local datetime and the location,
    using Googlemaps Timezone API:

    https://developers.google.com/maps/documentation/timezone/intro

    It requires a valid API key in the environment variable
    ANDADO_GOOGLE_API.

    https://developers.google.com/maps/documentation/timezone/get-api-key

    It is inaccurate in the hours just before and after the time at
    which daylight savings starts and ends in the location of
    interest.

    >>> print local_to_utc(41.2, 1.01, datetime(2004, 7, 9, 7, 2, 4))
    2004-07-09 05:02:04
    >>> print local_to_utc(41.2, 1.01, datetime(2004, 1, 9, 6, 2, 4))
    2004-01-09 05:02:04
    """
    # https://github.com/googlemaps/google-maps-services-python
    gmaps_key = os.environ.get('ANDADO_GOOGLE_API')
    if gmaps_key is None:
        raise RuntimeError('Expected to find a valid Googlemaps API key ' +
                           'in the ANDADO_GOOGLE_API environment variable')
    gm = googlemaps.Client(key=gmaps_key)
    tz = gm.timezone((lat, lng), local_timestamp)
    if sleep_after_call:
        # The free google api allows up to 10 calls per second.
        time.sleep(0.101)
    if not tz['status'] == 'OK':
        raise RuntimeError('Call to Googlemaps API failed')

    return local_timestamp - timedelta(seconds=(tz['dstOffset'] +
                                                tz['rawOffset']))


def _doctest():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _doctest()
