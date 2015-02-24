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
import io
import re

import gitapi
import subprocess

from prettytable import PrettyTable

# Utils
def replaceVars(inStr, globalVars):
    outStr = inStr
    for var, val in globalVars.items():
        if outStr.find('%%{%s}' % var) > -1:
            outStr = outStr.replace('%%{%s}' % var, val)

    return outStr


class SillyException(Exception):
    def __init__(self, message):
        self.message = message


class Package(object):
    name = None
    version = None
    rawVersion = None
    newVersion = None
    release = None
    rawRelease = None
    newRelease = None

    _specFilePath = None
    _args = None

    _globalVars = None

    _lines = []

    def __init__(self, specFilePath, args):
        super(Package, self).__init__()
        self._specFilePath = specFilePath
        self._args = args
        self._lines = []
        self._load()

    def _load(self):
        specFile = open(self._specFilePath, mode='r')

        globalVars = { '?dist' : '.%s' % self._args.dist }

        for line in specFile.readlines():
            self._lines.append(line)

            if line.startswith('%global') or line.startswith('%define'):
                r = line.split()
                if (len(r) != 3):
                    continue
                globalVars[r[1]] = r[2]
                continue

            r = line.split(':', 2)
            if (len(r) < 2):
                continue

            if r[0] == 'Name':
                self.name = replaceVars(r[1].strip(), globalVars)
            elif r[0] == 'Version':
                self.rawVersion = r[1].strip()
                self.version = replaceVars(self.rawVersion, globalVars)
            elif r[0] == 'Release':
                self.rawRelease = r[1].strip()
                self.release = replaceVars(self.rawRelease, globalVars)

        specFile.close()
        self._globalVars = globalVars

    def gitUpdate(self):
        repo = gitapi.Repo("%s/%s" % (os.getcwd(), self.name))
        repo.git_checkout('master')
        repo.git_pull('origin')


    def updateSpec(self):
        isGit = ('git_date' in self._globalVars and 'git_version' in self._globalVars)

        for i in range(len(self._lines)):
            line = self._lines[i]
            if line.startswith('Version:'):
                if self.name == 'kf5-baloo' or self.name == 'kf5-kfilemetadata':
                    self.newVersion = self._args.kf5version
                else:
                    self.newVersion = self._args.version

                line = line.replace(self.version, self.newVersion)

            elif line.startswith('Release:'):
                if isGit and self._args.keep_git_version:
                    self.newRelease = re.sub(r'^([0-9]+)(\.[0-9a-zA-Z]*)', r'%s' % self._args.release, self.rawRelease)
                else:
                    self.newRelease = '%s%%{?dist}' % self._args.release

                line = line.replace(self.rawRelease, self.newRelease)

            elif line.startswith('%changelog'):
                date = datetime.now().strftime('%a %b %d %Y')
                self._lines[i] = line
                self._lines.insert(i + 1, '* %s %s - %s-%s\n' % (date,
                                                                 self._args.author,
                                                                 self.newVersion,
                                                                 self.newRelease[:-len('%{?dist}')]))
                self._lines.insert(i + 2, '- %s\n' % self._args.changelog)
                self._lines.insert(i + 3, '\n')
                continue

            self._lines[i] = line


    def writeSpec(self):
        specFile = open(self._specFilePath, 'w')
        for line in self._lines:
            specFile.write(line)
        specFile.close()


    def updateSources(self):
        specDir = "%s/%s" % (os.getcwd(), self.name)
        p = subprocess.Popen(['spectool', '-s', '0', self._specFilePath],
                             cwd = specDir,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        com = p.communicate()
        if com[1]:
            raise SillyException(com[1].decode('UTF-8'))

        srcFileName = com[0].decode('UTF-8').rsplit('/', 2)[-1]
        srcFile = os.path.expanduser('~/rpmbuild/SOURCES/%s' % srcFileName).strip()

        if not os.path.exists(srcFile):
            p = subprocess.Popen(['spectool', '-g', '-R', self._specFilePath],
                                 cwd = specDir,
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE)
            com = p.communicate()
            if com[1]:
                raise SillyException(com[1].decode('UTF-8'))

        p = subprocess.Popen(['fedpkg', 'new-sources', srcFile],
                             cwd = specDir,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        com = p.communicate()
        if com[1]:
            raise SillyException(com[1].decode('UTF-8'))

    def commit(self):
        repo = gitapi.Repo( "%s/%s" % (os.getcwd(), self.name))
        repo.git_add('.')
        repo.git_commit(self._args.changelog)
        repo.git_checkout('f22')
        repo.git_merge('master')
        repo.git_checkout('master')

    def push(self):
        repo = gitapi.Repo("%s/%s" % (os.getcwd(), self.name))
        repo.git_push("origin")


def main():
    parser = ArgumentParser(description = 'Update Plasma 5 spec files to new version.')
    parser.add_argument('-v', '--version', required=True,
                        help='New version of Plasma 5')
    parser.add_argument('-k', '--kf5version', required=True,
                        help='Version of KDE Frameworks (for Baloo)')
    parser.add_argument('-r', '--release', default=1,
                        help='Package release version')
    parser.add_argument('-d', '--dist', default='fc21',
                        help='Distribution version')
    parser.add_argument('-c', '--changelog',
                        help='Changelog entry.')
    parser.add_argument('-a', '--author', default='Daniel Vrátil <dvratil@redhat.com>',
                        help='Update author')
    parser.add_argument('-g', '--keep-git-version', default=False, action='store_true',
                        help='Keep git snapshot reference in Release attribute')
    parser.add_argument('-s', '--skip-git-update', default=False, action='store_true',
                        help='Skip git update')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Skip updating this package. Can be used multiple times')
    parser.add_argument('-i', '--include', action='append',
                        help='Only update this package. Can be used multiple times')

    args = parser.parse_args()

    if not args.changelog:
        args.changelog = 'Plasma %s' % args.version

    p = subprocess.Popen(['ssh-add', '~/.ssh/id_rsa.redhat'])
    p.communicate()


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
        except SillyException as e:
            print('Error: %s' % e.message)
            return
        print('Done')
        print('Updating sources...', end = '', flush = True)
        try:
            pkg.updateSources()
        except SillyException as e:
            print('Error: %s' % e.message)
            return
        print('Done')
        print('Commiting changes...', end = '', flush = True)
        try:
            pkg.commit()
        except SillyException as e:
            print('Error: %s' % e.message)
            return
        print('Done')
        print('\n')

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

