# -*- coding: utf-8 -*-
"""andado

Manage files containing location and date.
"""
from __future__ import division

import os
import date


def parse_waypoints(waypoint_file, md5_file):
    return []

https://picasaweb.google.com/joanmg/GeoPostr2011?authkey=Gv1sRgCILM2O3d4vLJ8wE#5625502956655741890
https://lh3.googleusercontent.com/-ofl3rtNrATw/ThHNIkZgC8I/AAAAAAAACXE/djmto1Obe3g/I-Ic42/2011-07-02-18-06-21-sm.jpg

class Waypoint(object):
    def __init__(self, timestamp, lat, lng, md5, source):
        self.timestamp = timestamp
        self.lat, self.lng = lat, lng
        self.md5 = md5
        if not os.path.exists(source):
            source = ''
        self.source = source

    def format(self):
        return '|'.join([self.timestamp.strftime('%Y-%m-%d-%H%M%S'),
                         self.lat, self.lng, self.md5])


class Andado(object):
    def __init__(self, waypoints, sources):
        """Waypoints is a list of Waypoint objects.  Sources is a dictionary
        indexed by the MD5 that contains a list of all the files from
        which the waypoint has been extracted (which, if all goes
        well, will be the same file in several locations.)
        """
        self._waypoints = waypoints
        self._sources = sources

    def update_sources(self):
        for waypoint in self._waypoints:
            if waypoint.md5 in self._sources:
                if not waypoint.source in self._sources[waypoint.md5]:
                    self._sources[waypoint.md5].append(waypoint.source)
            else:
                self._sources[waypoint.md5] = [waypoint.source]

    def prune_sources(self):
        for md5 in self._sources.keys():
            self._sources[md5] = [f for f in self._sources[md5]
                                  if os.path.exists(f)]

    def save_waypoints(self, waypoint_file):
        with open(waypoint_file, 'w') as wf:
            for waypoint in sorted(self._waypoints, key=lambda w: w.timestamp):
                wf.write(waypoint.format() + '\n')

    def save_sources(self, sources_file):
        with open(sources_file, 'w') as sf:
