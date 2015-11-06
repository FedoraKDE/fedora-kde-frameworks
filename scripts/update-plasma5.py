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


from argparse import ArgumentParser
from datetime import datetime

import os
import subprocess

from prettytable import PrettyTable

from Package import *

def main():
    parser = ArgumentParser(description = 'Update Plasma 5 spec files to new version.')
    parser.add_argument('-v', '--version', required=True,
                        help='New version of Plasma 5')
    parser.add_argument('-r', '--release', default=1,
                        help='Package release version')
    parser.add_argument('-d', '--dist', default='fc21',
                        help='Distribution version')
    parser.add_argument('-c', '--changelog',
                        help='Changelog entry.')
    parser.add_argument('-a', '--author', default='Daniel Vrátil <dvratil@fedoraproject.org>',
                        help='Update author')
    parser.add_argument('-g', '--keep-git-version', default=False, action='store_true',
                        help='Keep git snapshot reference in Release attribute')
    parser.add_argument('-s', '--skip-git-update', default=False, action='store_true',
                        help='Skip git update')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Skip updating this package. Can be used multiple times')
    parser.add_argument('-i', '--include', action='append',
                        help='Only update this package. Can be used multiple times')
    parser.add_argument('-u', '--no-upload', action='store_true', default=False,
                        help='Skip uploading tarballs to look-aside cache')
    parser.add_argument('--no-commit', action='store_true', default=False,
                        help='Don\'t commit and push the changes')

    args = parser.parse_args()

    if not args.changelog:
        args.changelog = 'Plasma %s' % args.version

    #p = subprocess.Popen(['ssh-add', '/home/dvratil/.ssh/id_rsa.fedoraproject'])
    #p.communicate()


    pkgs = []
    if args.include:
        names = args.include
    else:
        names = os.listdir(os.getcwd())
    for name in names:
        if args.exclude and name in args.exclude:
            print("Skipping %s" % name)
            continue

        if not os.path.isdir('%s/%s' % (os.getcwd(), name)):
            continue

        print('Loading %s...' % name, end = '', flush = True)
        pkg = Package("%s/%s/%s.spec" % (os.getcwd(), name, name), args)
        if not args.skip_git_update:
            pkg.gitUpdate()

        if pkg.patches and not pkg.hasAutoSetup:
            print('WARNING: package has patches, but does not use %%autosetup')
        elif pkg.patches:
            for patch in pkg.patches:
                remove = input('Remove patch %s? [Y/n] ' % patch)
                if remove.lower() == 'y':
                    pkg.removePatch(patch)

        pkg.updateSpec()
        pkgs.append(pkg)
        print('Done')

    table = PrettyTable(['Package', 'Old Version', 'New Version'])
    table.align = 'l'
    for pkg in pkgs:
        table.add_row([pkg.name,
                      "%s-%s" % (pkg.rawVersion, pkg.rawRelease),
                      "%s-%s" % (pkg.newVersion, pkg.newRelease)])
    print(table.get_string(sortby='Package'))

    proceed = input("Proceed? [Y/n] ")
    if proceed.lower() == 'n':
        return

    for pkg in pkgs:
        print(pkg.name)
        print('-'.ljust(len(pkg.name), '-'))
        print('Updating SPEC file...', end = '', flush = True)
        try:
            pkg.writeSpec()
        except PackageException as e:
            print('Error: %s' % e.message)
            return
        print('Done')
        if not args.no_upload:
            print('Updating sources...', end = '', flush = True)
            try:
                pkg.updateSources()
            except PackageException as e:
                print('Error: %s' % e.message)
                return
            print('Done')
        if not args.no_commit:
            print('Commiting changes...', end = '', flush = True)
            try:
                pkg.commit()
            except PackageException as e:
                print('Error: %s' % e.message)
                return
        print('Done')
        print('\n')

    if not args.no_commit:
        proceed = input("Push changes to distgit? [Y/n] ")
        if proceed.lower() == 'n':
            return

        for pkg in pkgs:
            print('Pushing %s...' % pkg.name, end = '', flush = True)
            pkg.push()
            print('Done')


    print('We are done and this lousy script did not screw anything up \o/ Open the champagne!')
    print('See you around.')
    print('')


if __name__ == "__main__":
    main()

