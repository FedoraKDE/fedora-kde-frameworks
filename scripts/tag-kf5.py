#!/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (C) 2014, 2015  Daniel Vrátil <dvratil@redhat.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
#


import argparse
import subprocess
import os

from distutils.version import LooseVersion

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--srcTag', action='store', required = True,
                        help='Current tag the packages are tagged into')
    parser.add_argument('--destTag', action='store', required = True,
                        help='New tag to tag the packages into')
    parser.add_argument('--version', action='store', required = True,
                        help='KDE Frameworks 5 version number')
    parser.add_argument('--pkgroot', action='store', default=os.getcwd(),
                        help='Root directory where all fedpkg clones are')
    args = parser.parse_args()

    proc = subprocess.Popen([ 'koji', 'list-tagged', args.srcTag ], stdout=subprocess.PIPE)
    out = proc.communicate()
    outs = out[0].decode('UTF-8').split('\n');
    allSrcPkgs = []
    for out in outs[2:]: # skip first two lines of headers
        pkg = out.split(' ')[0]
        pkgParts = pkg.rsplit('-', 2)
        if len(pkgParts) < 3:
            continue

        allSrcPkgs.append(( pkgParts[0], pkgParts[1], pkgParts[2] ))

    srcPkgs = os.listdir('%s/tier1' % args.pkgroot) \
            + os.listdir('%s/tier2' % args.pkgroot) \
            + os.listdir('%s/tier3' % args.pkgroot) \
            + os.listdir('%s/tier4' % args.pkgroot)
    srcPkgs.append('kf5')
    srcPkgs.append('extra-cmake-modules')

    destPkgs = {}
    for srcPkg in allSrcPkgs:
        if srcPkg[0] in srcPkgs:
            # Check kf5-* version
            if (srcPkg[0] == 'extra-cmake-modules' or srcPkg[0].startswith('kf5')) and srcPkg[1] != args.version:
                continue

            # We already met package of this name...
            if srcPkg[0] in destPkgs:
                # Is this package newer than the one we met before? If yes, then
                # remove the old version from destPkgs
                if LooseVersion(srcPkg[2]) > LooseVersion(destPkgs[srcPkg[0]][2]):
                    del destPkgs[srcPkg[0]]

            destPkgs[srcPkg[0]] = srcPkg

    nvbs = []
    for pkgname in destPkgs:
        nvbs.append("%s-%s-%s" % (destPkgs[pkgname][0], destPkgs[pkgname][1], destPkgs[pkgname][2]))

    print("Tag from: %s" % args.srcTag)
    print("Tag into: %s" % args.destTag)
    print("Tag packages: %s" % nvbs)

    proceed = input('Proceed? [Y/n] ')
    if proceed.lower() == 'n':
        return

    proc = subprocess.Popen([ 'koji', 'tag-build', args.destTag ] + nvbs)
    proc.wait()

    proceed = input('Create Bodhi update? [Y/n] ')
    if proceed.lower() == 'n':
        return

    proc = subprocess.Popen([ 'bodhi', '-n', '-t', 'bugfix', '-N', 'KDE Frameworks %s' % args.version ] + nvbs)
    proc.communicate()


if __name__ == "__main__":
    main()
