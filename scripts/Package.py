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


import os
import re
import subprocess
import gitapi
from datetime import datetime

class PackageException(Exception):
    def __init__(self, message):
        self.message = message

class Package(object):

    _MapDeps = { 'kf5-rpm-macros' : 'kf5' }

    name = None
    version = None
    plasmaVersion = None
    rawVersion = None
    newVersion = None
    release = None
    rawRelease = None
    newRelease = None
    patches = None
    hasAutoSetup = False
    otherBuildRequiresNames = None
    kf5BuildRequiresNames = None

    specFilePath = None

    _args = None

    _globalVars = None

    _lines = None

    _patchesToRemove = None

    def __init__(self, specFilePath, args):
        super(Package, self).__init__()
        self.specFilePath = specFilePath
        self._args = args

        self.load()

        if 'plasma_version' in self._globalVars:
            self.plasmaVersion = self._globalVars['plasma_version']
        else:
            self.plasmaVersion = self.version

    def __repr__(self):
        return "<Package %s>" % self.name

    def _replaceVars(self, inStr, globalVars):
        outStr = inStr
        for var, val in globalVars.items():
            if outStr.find('%%{%s}' % var) > -1:
                outStr = outStr.replace('%%{%s}' % var, val)

        return outStr

    def load(self):
        self.otherBuildRequiresNames = []
        self.kf5BuildRequiresNames = []
        self.patches = []
        self._patchesToRemove = []
        self._lines = []

        specFile = open(self.specFilePath, mode='r')

        globalVars = { '?dist' : '.%s' % self._args.dist }

        for line in specFile.readlines():
            self._lines.append(line)
            line = line.strip()

            if line.startswith('#'):
                continue

            if line.startswith('%global') or line.startswith('%define'):
                r = line.split()
                if len(r) != 3:
                    continue
                globalVars[r[1]] = r[2]
                continue

            if line.startswith('Patch'):
                r = line.split(':');
                if len(r) != 2:
                    continue
                self.patches += [ r[1].strip() ]
                continue

            if line.startswith('%autosetup'):
                self.hasAutoSetup = True
                continue

            r = line.split(':', 2)
            if len(r) < 2:
                continue

            if r[0] == 'Name':
                self.name = self._replaceVars(r[1].strip(), globalVars)
            elif r[0] == 'Version':
                self.rawVersion = r[1].strip()
                self.version = self._replaceVars(self.rawVersion, globalVars)
            elif r[0] == 'Release':
                self.rawRelease = r[1].strip()
                self.release = self._replaceVars(self.rawRelease, globalVars)
            elif r[0] == 'BuildRequires':
                brName = r[1].strip()
                # Remove potential versioned dependency
                index = brName.find(' ')
                if index > -1:
                    brName = brName[0:index]
                if brName.startswith('kf5') or brName == 'extra-cmake-modules':
                    if brName.endswith('-devel'):
                        brName = brName[0:-6]
                    if brName in self._MapDeps:
                        self.kf5BuildRequiresNames.append(self._MapDeps[brName])
                    else:
                        self.kf5BuildRequiresNames.append(brName)
                elif brName.endswith('-devel'):
                    brName = brName[0:-6]
                    if brName in self._MapDeps:
                        self.otherBuildRequiresNames.append(self._MapDeps[brName])
                    else:
                        self.otherBuildRequiresNames.append(brName)
                continue

        specFile.close()
        self._globalVars = globalVars

    def gitUpdate(self):
        repo = gitapi.Repo("%s/%s" % (os.getcwd(), self.name))
        repo.git_checkout('master')
        repo.git_pull('origin')

        # Reparse
        self.load()

    def removePatch(self, patch):
        self._patchesToRemove += [ patch ]


    def updateSpec(self):
        isGit = ('git_date' in self._globalVars and 'git_version' in self._globalVars)

        i = 0
        inChangelog = False
        while (i < len(self._lines)):
            line = self._lines[i]
            if line.startswith('Version:') and not inChangelog:
                if self.name == 'kf5-baloo' or self.name == 'kf5-kfilemetadata':
                    self.newVersion = self._args.kf5version
                else:
                    self.newVersion = self._args.version

                self._lines[i] = line.replace(self.version, self.newVersion)

            elif line.startswith('Release:') and not inChangelog:
                if isGit and self._args.keep_git_version:
                    self.newRelease = re.sub(r'^([0-9]+)(\.[0-9a-zA-Z]*)', r'%s' % self._args.release, self.rawRelease)
                else:
                    self.newRelease = '%s%%{?dist}' % self._args.release

                self._lines[i] = line.replace(self.rawRelease, self.newRelease)

            elif line.startswith('Patch') and not inChangelog:
                r = line.split(':')
                if len(r) == 2:
                    if r[1].strip() in self._patchesToRemove:
                        del self._lines[i]
                        continue

            elif line.startswith('%changelog') and not inChangelog:
                date = datetime.now().strftime('%a %b %d %Y')
                self._lines[i] = line
                self._lines.insert(i + 1, '* %s %s - %s-%s\n' % (date,
                                                                 self._args.author,
                                                                 self.newVersion,
                                                                 self.newRelease[:-len('%{?dist}')]))
                self._lines.insert(i + 2, '- %s\n' % self._args.changelog)
                self._lines.insert(i + 3, '\n')
                inChangelog = True

            else:
                self._lines[i] = line

            i = i + 1


    def writeSpec(self):
        specFile = open(self.specFilePath, 'w')
        for line in self._lines:
            specFile.write(line)
        specFile.close()


    def updateSources(self):
        specDir = "%s/%s" % (os.getcwd(), self.name)
        p = subprocess.Popen(['spectool', '-s', '0', self.specFilePath],
                             cwd = specDir,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        com = p.communicate()
        if com[1]:
            raise PackageException(com[1].decode('UTF-8'))

        srcFileName = com[0].decode('UTF-8').rsplit('/', 2)[-1]
        srcFile = os.path.expanduser('~/rpmbuild/SOURCES/%s' % srcFileName).strip()

        if not os.path.exists(srcFile):
            p = subprocess.Popen(['spectool', '-g', '-R', self.specFilePath],
                                 cwd = specDir,
                                 stdout = subprocess.PIPE,
                                 stderr = subprocess.PIPE)
            com = p.communicate()
            if com[1]:
                raise PackageException(com[1].decode('UTF-8'))

        p = subprocess.Popen(['fedpkg', 'new-sources', srcFile],
                             cwd = specDir,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE)
        com = p.communicate()
        if com[1]:
            raise PackageException(com[1].decode('UTF-8'))

    def commit(self, branches = ['master']):
        repo = gitapi.Repo( "%s/%s" % (os.getcwd(), self.name))
        repo.git_add('.')
        repo.git_commit(self._args.changelog)
        for branch in branches:
            if branch == 'master':
                continue
            repo.git_checkout(branch)
            repo.git_merge('master')

        repo.git_checkout('master')

    def push(self):
        repo = gitapi.Repo("%s/%s" % (os.getcwd(), self.name))
        repo.git_push("origin")

