# -*- coding: utf-8 -*-
"""import

"""
from __future__ import division

import os
import shutil
import subprocess
import pickle

import meta


def photocp(fromdir, todir, copied_pickle, rawdir='', newname=False):
    # if not os.path.exists(todir):
    #     os.makedirs(todir)
    raw_todir = os.path.join(todir, 'raw')
    # if not os.path.exists(raw_todir):
    #     os.makedirs(raw_todir)
    if os.path.exists(copied_pickle):
        with open(copied_pickle, 'r') as fin:
            copied = pickle.load(fin)
    else:
        copied = {}
    n_copied = 0
    for root, dirs, files in os.walk(fromdir):
        if '.Trashes' not in root:
            for fname in files:
                base, ext = os.path.splitext(fname)
                if ext.lower() == '.jpg' and fname[0] != '.':
                    fullname = os.path.join(root, fname)
                    md5 = subprocess.check_output(['md5', '-q',
                                                   fullname]).strip()
                    if md5 not in copied:
                        n_copied += 1
                        copied[md5] = fullname

                        tofile = os.path.join(todir, 'cp')
                        raw_tofile = raw_todir
                        if newname:
                            baseout = meta.photo_fname(fullname, [], '', '')
                            tofile = os.path.join(todir, baseout + '.jpg')
                            raw_tofile = os.path.join(raw_todir,
                                                      baseout + '.raf')
                        # else:
                        #     if not os.path.exists(os.path.dirname(tofile)):
                        #         os.makedirs(os.path.dirname(tofile))
                        #     if not os.path.exists(raw_todir):
                        #         os.makedirs(raw_todir)

                        print fullname, '->', tofile,

                        if not os.path.exists(os.path.dirname(tofile)):
                            os.makedirs(os.path.dirname(tofile))
                        shutil.copy(fullname, tofile)
                        if newname:
                            subprocess.call(['chmod', '-x', tofile])

                        rawname = os.path.join(root, rawdir, base + '.RAF')
                        if os.path.exists(rawname):
                            if newname:
                                print os.path.dirname(raw_tofile)
                            else:
                                print raw_tofile
                            if not os.path.exists(os.path.dirname(raw_tofile)):
                                os.makedirs(os.path.dirname(raw_tofile))
                            shutil.copy(rawname, raw_tofile)
                            if newname:
                                subprocess.call(['chmod', '-x', raw_tofile])
                        else:
                            print
                    else:
                        print "** Already copied", fullname

    if n_copied:
        print 'Updating copied cache', copied_pickle
        with open(copied_pickle, 'w') as fout:
            pickle.dump(copied, fout)


def main_photocp():
    import sys
    fromdir = '/Volumes/Untitled'
    if len(sys.argv) == 2:
        fromdir = sys.argv[1]
    todir = os.path.expanduser('~/tmp/dock')
    photocp(fromdir, todir,
            os.path.expanduser('~/Dropbox/master/photos/copied.pkl'))
    subprocess.call(['open', todir])


def main_photoimport():
    import sys
    fromdir = os.path.expanduser('~/Desktop/photo-export')
    if len(sys.argv) == 2:
        fromdir = sys.argv[1]
    todir = os.path.expanduser('~/Dropbox/master/photos')
    photocp(fromdir, todir,
            os.path.expanduser('~/Dropbox/master/photos/imported.pkl'),
            rawdir='raw', newname=True)


if __name__ == '__main__':
    main_photoimport()
