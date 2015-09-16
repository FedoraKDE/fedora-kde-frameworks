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

from prettytable import PrettyTable, ALL

from Package import *
from DependencyScanner import *

def main():
    parser = ArgumentParser(description = 'Update KF5 spec files to new version.')
    parser.add_argument('-v', '--version', required=True,
                        help='New version')
    parser.add_argument('-r', '--release', default=1,
                        help='Package release version')
    parser.add_argument('-d', '--dist', default='fc22',
                        help='Distribution version')
    parser.add_argument('-c', '--changelog',
                        help='Changelog entry.')
    parser.add_argument('-a', '--author', default='Daniel Vrátil <dvratil@redhat.com>',
                        help='The update author')
    parser.add_argument('--no-pull', action='store_true',
                        help='Don\'t pull updates from distgit')
    parser.add_argument('--no-upload', action='store_true', default=False,
                        help='Skip uploading tarballs to look-aside cache')
    parser.add_argument('--no-update', action='store_true',
                        help='Don\'t update SPEC files (dry run)')
    parser.add_argument('--no-commit', action='store_true', default=False,
                        help='Don\'t commit the changes')
    parser.add_argument('--no-push', action='store_true', default=False,
                        help='Don\'t push changes to distgit')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Skip updating this package. Can be used multiple times')
    parser.add_argument('--resume-from', action='store',
                        help='Resume update from specified package')
    parser.add_argument('--pkgroot', action='store', default=os.getcwd(),
                        help='Root dist with distgit clones (see clone-packages.py)')
    args = parser.parse_args()

    if not args.changelog:
        args.changelog = 'KDE Frameworks %s' % args.version

    if not os.getenv('SSH_AGENT_PID'):
        print("Warning: ssh-agent is not running, you will have to type in your password all the time!");
        proceed = input("Continue? [Y/n] ")
        if proceed.lower() == 'n':
            return

    p = subprocess.Popen(['ssh-add', '-l'], stdout = subprocess.PIPE)
    out, _ = p.communicate()
    if not "/home/dvratil/.ssh/id_rsa.redhat" in out.decode('UTF-8'):
        p = subprocess.Popen(['ssh-add', '/home/dvratil/.ssh/id_rsa.redhat'])
        p.communicate()


    pkgs = []
    names = os.listdir(args.pkgroot)
    shouldSkip = not (args.resume_from == None)
    for name in names:
        if args.exclude and name in args.exclude:
            print("Skipping %s" % name)
            continue
        if shouldSkip:
            if name == args.resume_from:
                shouldSkip = False
            else:
                print("Skipping %s" % name)
                continue

        if not os.path.isdir('%s/%s' % (args.pkgroot, name)):
            continue

        print('Loading %s...' % name, end = '', flush = True)
        pkg = Package("%s/%s/%s.spec" % (args.pkgroot, name, name), args)
        print('Done')
        print('Updating %s...' % name, end = '', flush = True)
        if not args.no_pull:
            pkg.gitUpdate()

        if pkg.patches and not pkg.hasAutoSetup:
            print('WARNING: package has patches, but does not use %%autosetup')
        elif pkg.patches:
            print("\n")
            for patch in pkg.patches:
                remove = input('\tRemove patch %s? [Y/n] ' % patch)
                if remove.lower() == 'y':
                    pkg.removePatch(patch)

        if not args.no_update:
            pkg.updateSpec()

        scanner = DependencyScanner(pkg)
        if scanner.load():
            pkg.scanner = scanner
        else:
            pkg.scanner = None

        pkgs.append(pkg)
        print('Done')


    table = PrettyTable(['Package', 'Old Version', 'New Version', 'Added deps', 'Removed deps', 'Added devel deps', 'Removed devel deps'])
    table.align = 'l'
    table.hrules = ALL
    for pkg in pkgs:
        table.add_row([pkg.name,
                      "%s-%s" % (pkg.rawVersion, pkg.rawRelease),
                      "%s-%s" % (pkg.newVersion, pkg.newRelease),
                      '\n'.join(list(map(lambda x : x.name(), pkg.scanner.depsAdd))) if pkg.scanner else "[error]",
                      '\n'.join(list(map(lambda x : x.name(), pkg.scanner.depsRemove))) if pkg.scanner else "[error]",
                      '\n'.join(list(map(lambda x : x.name(), pkg.scanner.develDepsAdd))) if pkg.scanner else "[error]",
                      '\n'.join(list(map(lambda x : x.name(), pkg.scanner.develDepsRemove))) if pkg.scanner else "[error]"])
    print(table.get_string(sortby='Package'))

    proceed = input("Proceed? [Y/n] ")
    if proceed.lower() == 'n':
        return

    for pkg in pkgs:
        print(pkg.name)
        print('-'.ljust(len(pkg.name), '-'))
        if not args.no_update:
            print('Updating SPEC file...', end = '', flush = True)
            try:
                # Always rewrite with scanner (if available)
                if pkg.scanner:
                    pkg.scanner.write()
                else:
                    pkg.writeSpec()
            except (PackageException, DependencyException) as e:
                print('Error: %s' % e.message)

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

        if not args.no_commit or not args.no_push:
            proceed = input("Push changes to distgit? [Y/n] ")
            if proceed.lower() == 'n':
                return

            for pkg in pkgs:
                print('Pushing %s...' % pkg.name, end = '', flush = True)
                pkg.push()

            print('Done')

        print('\n')

    print('We are done and this lousy script did not screw anything \o/!')
    print('See you around.')
    print('')


if __name__ == "__main__":
    main()


