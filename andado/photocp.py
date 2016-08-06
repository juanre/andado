# -*- coding: utf-8 -*-
"""import

"""
from __future__ import division

import os
import shutil
import subprocess
import pickle


def photocp(fromdir, todir, copied_pickle):
    if not os.path.exists(todir):
        os.makedirs(todir)
    if os.path.exists(copied_pickle):
        with open(copied_pickle, 'r') as fin:
            copied = pickle.load(fin)
    else:
        copied = {}
    n_copied = 0
    for root, dirs, files in os.walk(fromdir):
        if not '.Trashes' in root:
            for fname in files:
                base, ext = os.path.splitext(fname)
                if ext.lower() == '.jpg' and fname[0] != '.':
                    fullname = os.path.join(root, fname)
                    md5 = subprocess.check_output(['md5', '-q',
                                                   fullname]).strip()
                    if md5 not in copied:
                        n_copied += 1
                        copied[md5] = fullname
                        print fullname, '->'
                        shutil.copy(fullname, todir)

    if n_copied:
        print 'Updating copied cache', copied_pickle
        with open(copied_pickle, 'w') as fout:
            pickle.dump(copied, fout)


def main():
    todir = os.path.expanduser('~/tmp/dock')
    photocp('/Volumes/Untitled', todir,
            os.path.expanduser('~/Dropbox/master/copied.pkl'))
    subprocess.call(['open', todir])


if __name__ == '__main__':
    main()
