#!/usr/bin/env python3
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
import gitapi
import os

group1 = [ 'libbluedevil',
           'libkscreen-qt5',
           'kdecoration',
           'kde-cli-tools',
           'kf5-kfilemetadata',
           'libksysguard',
           'kf5-kwayland',
           'kf5-modemmanager-qt',
           'khelpcenter',
           'kio-extras',
           'kmenuedit',
           'kwrited',
           'plasma-workspace-wallpapers',
           'polkit-kde',
           'sddm-kcm',
           'kdeplasma-addons',
           'plasma-systemsettings'
         ]

group2 = [ 'kwin',
           'kinfocenter',
           'plasma-breeze',
           'plasma-nm',
#           'kde-gtk-config',
           'kscreen',
           'ksysguard',
           'kf5-baloo',
           'bluedevil'
         ]

group3 = [ 'plasma-oxygen',
           'plasma-workspace',
           'plasma-milou'
         ]

group4 = [ 'plasma-desktop',
           'khotkeys',
           'powerdevil'
         ]

groups = [ group1,
           group2,
           group3,
           group4 ]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pkgroot', default=os.getcwd(),
                        help='Root directory where all fedpkg clones are')
    parser.add_argument('--resume-from',
                        help='Resume build from specified package, skipping all previous packages')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Exclude certain package from build. Can be used multiple times. Can be combined with --resume-from')
    parser.add_argument('target',
                        help='Koji target to build into')
    parser.add_argument('--branch',
                        help='Distgit branch to build from')

    args = parser.parse_args()

    branch = args.branch
    if not branch:
        if args.target.startswith('f23'):
            branch = 'master'
        else:
            branch = args.target

    packages = []
    skipPackages = (args.resume_from != None)
    for group in groups:
        for pkg in group:
            if skipPackages:
                if args.resume_from == pkg:
                    skipPackages = False
                else:
                    continue

            if args.exclude and pkg in args.exclude:
                continue

            packages.append(pkg)
        if len(packages) > 0:
            if packages[-1] != ':':
                packages.append(':')

    # Drop the trailing colon
    packages.pop()
    # Get the last pkg: we'll run chainbuild from there
    lastPkg = packages.pop()

    print('Packages to build: %s' % ' '.join(packages))
    print('Koji Target: %s' % args.target)
    print('Branch: %s' % branch)
    print('Chainbuild package: %s/%s' % (args.pkgroot, lastPkg))

    proceed = input('Proceed? [Y/n] ')
    if proceed.lower() == 'n':
        return

    repo = gitapi.Repo('%s/%s' % (args.pkgroot, lastPkg))
    repo.git_checkout(branch)

    p = subprocess.Popen(['fedpkg', 'chain-build', '--target=%s' % args.target] + packages,
                     cwd = '%s/%s' % (args.pkgroot, lastPkg))
    p.wait()

if __name__ == '__main__':
    main()
