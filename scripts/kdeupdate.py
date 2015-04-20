#!/bin/env python3
# -*- coding: utf-8 -*-

#
# Copyright (C) 2015  Daniel Vrátil <dvratil@redhat.com>
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

import subprocess
import os.path
import argparse
import fnmatch
from prettytable import PrettyTable

from KDEProject import *
from SPECFile import *

_IgnoredKDEProjects = [
    "user-manager",
    "kde-gtk-config",
    "muon"
]

_KDEToFedoraNamesMap = {
    # Plasma 5
    "baloo": "kf5-baloo",
    "breeze": "plasma-breeze",
    "kcm-touchpad": "kcm_touchpad",
    "libkscreen": "libkscreen-qt5",
    "kfilemetadata": "kf5-kfilemetadata",
    "oxygen": "plasma-oxygen",
    "polkit-kde-agent-1": "polkit-kde",
    "systemsettings": "plasma-systemsettings",
    "kwayland": "kf5-kwayland",
    "milou": "plasma-milou",

    # KF5
    "plasma-framework": " kf5-plasma"
}



def clonePackages(fedoraPkgs):
    for pkg in fedoraPkgs:
        if os.path.exists(pkg):
            print("Skipping %s, because it already exists" % pkg)
            continue

        p = subprocess.Popen(['fedpkg', 'clone', pkg])
        p.wait()


class KDEUpdate():
    _argParser = None
    _args = None

    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--pkgroot', action='store', default=os.getcwd(),
                            help='Root directory where all fedpkg clones are')
        parser.add_argument('--product', action='store', choices = [ 'frameworks', 'workspace', 'applications' ],
                            help='KDE product to work with')
        self._argParser = parser

    def parseArguments(self, args):
        self._args = self._argParser.parse_args(args)

    def run(self):
        raise Exception("This should not ever be called, missing reimplementation maybe?")

    def _listKDEProjects(self):
        parser = KDEProjectXMLParser()
        if self._args.product == 'frameworks':
            return parser.listFrameworks()
        elif self._args.product == 'workspace':
            return parser.listWorkspace()
        elif self._args.product == 'applications':
            return parser.listApplications()
        else:
            return []

    def _listSpecFiles(self):
        specFiles = []

        # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        for root, dirnames, filenames in os.walk(self._args.pkgroot):
            for filename in fnmatch.filter(filenames, '*.spec'):
                path = os.path.join(root, filename)
                specFiles.append(SPECFile(path, pullDistGit = False))

        return specFiles



class KDEUpdateNewVersion(KDEUpdate):

    def __init__(self, args):
        super(KDEUpdateNewVersion, self).__init__()
        self._argParser.add_argument('--version', action='store',
                                     help='New version')
        self._argParser.add_argument('--altVersion', action='store',
                                     help='Alternative version')
        self._argParser.add_argument('--release', action='store',
                                     default='1', help='Release')
        self._argParser.add_argument('--author', action='store',
                                     default='Daniel Vrátil <dvratil@redhat.com>',
                                     help='Default author (for changelog entry)')
        self._argParser.add_argument('--changelog', action='store',
                                     help='Changelog entry (defaults to "%projectname - %version")')
        self.parseArgs(args)

    def run(self):
        # 1) get projects XML list
        kdeProjects = self._listKDEProjects()

        # 2) list local fedpkg clones
        specFiles = self._listSpecFiles()

        # TODO
        # 3) compare them
        #   3a) update existing
        #   3b) clone missing
        #   3c) move moved
        #   3d) remove removed/disabled projects (?)

        # 4) update spec files interactively and upload source tarballs
        for specFile in specFiles:
            specFile.interactiveUpdate(version = self._args.version,
                                       release = self._args.release,
                                       author = self._args.author,
                                       changelog = self._args.changelog)

        # 5) confirm changes
        table = PrettyTable(['Package', 'Old Version', 'New Version', 'Removed patches'])
        table.align = 'l'
        for specFile in specFiles:
            table.add_row([specFile.name,
                           "%s-%s" % (specFile.version, specFile.release),
                           "%s-%s" % (specFile.newVersion, specFile.newRelease),
                           '\n'.join(list(map(lambda x: os.path.split(x)[-1], specFile.removedPatches)))])
        print(table.get_string(sortby='Package'))

        proceed = input('Write changes and push? [Y/n] ')
        if proceed.lower() == 'n':
            return


        for specFile in specFiles:
            specFile.save()
            specFile.uploadSources()
            specFile.commit(self._args.changelog)

        # 6) push changes to distgit
        for specFile in specFiles:
            specFile.pushToDistGit()

class KDEUpdateBuild(KDEUpdate):

    def __init__(self, args):
        super(KDEUpdateBuild, self).__init__()
        self._argParser.add_argument('--copr', action='store_true',
                                     help='Build in COPR (otherwise build in Koji)')
        self._argParser.add_argument('-x', '--exclude', action='append',
                                     help='Exclude specified package from build chain (can be used mutliple times)')
        self._argParser.add_argument('--resume-from', action='store',
                                     help='Resume build from specified package (can be combined with --exclude)')
        self._argParser.add_argument('--target', action='store',
                                     help='Koji target to build into (ignored when building in COPR)')
        self._argParser.add_argument('--branch', action='store', default='master',
                                     help='Branch from which to build')
        self.parseArguments(args)

        if not self._args.copr and not self._args.target:
            raise Exception('Koji target must be specified when building in Koji')


    def run(self):
        # 1) get projects XML list
        # TODO

        # 2) list local fedpkg clones
        specFiles = self._listSpecFiles()

        # 3) compare them, abort on mismatch
        # TODO

        # 4) create build groups
        groups = self._createBuildGroups(specFiles)
        i = 0
        for group in groups:
            pkgs = list(map(lambda x: x.name if isinstance(x, SPECFile) else x, group))
            print("Group %i: %s" % (i, pkgs))
            i += 1

        # 5) confirm build
        # 6) build in COPR or Koji
        if (self._args.copr):
            pass
            #TODO
            #groups = self._prepareCoprBuild(groups)
            #if self._confirmCoprBuild(groups):
            #    self._runCoprBuild(groups)
        else:
            buildChain = self._prepareKojiChainbuild(groups)
            if self._confirmKojiChainbuild(buildChain):
                self._runKojiChainbuild(buildChain)


    def _listSpecFiles(self):
        specFiles = []

        # http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
        for root, dirnames, filenames in os.walk(self._args.pkgroot):
            for filename in fnmatch.filter(filenames, '*.spec'):
                path = os.path.join(root, filename)
                specFiles.append(SPECFile(path, pullDistGit = False))

        return specFiles

    def _prepareKojiChainbuild(self, groups):
        buildChain = []
        skipPackages = (self._args.resume_from != None)
        for group in groups:
            for pkg in group:
                if skipPackages:
                    if self._args.resume_from == pkg.name:
                        skipPackages = False
                    else:
                        continue

                if self._args.exclude and pkg.name in self._args.exclude:
                    continue

                buildChain.append(pkg)

            if len(buildChain) > 0:
                if buildChain[-1] != ':':
                    buildChain.append(':')

        # Drop the trailing colon
        buildChain.pop()
        return buildChain


    def _confirmKojiChainbuild(self, buildChain):
        # Get the last pkg: we'll run chainbuild from there
        lastPkg = buildChain[-1]
        lastPkgRepo = os.path.split(lastPkg.specFilePath)[0]

        buildChainNames = list(map(lambda x: x.name if isinstance(x, SPECFile) else x, buildChain))
        print('Build chain: %s' % ' '.join(buildChainNames))
        print('Koji Target: %s' % self._args.target)
        print('Branch: %s' % self._args.branch)
        print('Chainbuild package: %s' % lastPkgRepo)

        proceed = input('Proceed? [Y/n] ')
        if proceed.lower() == 'n':
            return False

        return True


    def _runKojiChainbuild(self, buildChain):
        # Get the last pkg: we'll run chainbuild from there
        lastPkg = buildChain.pop()
        lastPkgRepo = os.path.split(lastPkg.specFilePath)[0]

        repo = gitapi.Repo(lastPkgRepo)
        repo.git_checkout(self._args.branch)

        buildChainNames = list(map(lambda x: x.name if isinstance(x, SPECFile) else x, buildChain))
        p = subprocess.Popen(['fedpkg', 'chain-build', '--target=%s' % self._args.target] + buildChainNames,
                             cwd = lastPkgRepo)
        p.wait()

    def _createBuildGroups(self, specFiles):
        def _allDepsAnalyzed(package, groups):
            deps = package.kf5BuildRequiresNames.copy()
            if not deps:
                return True
            for group in groups:
                for pkg in group:
                    if pkg.name in deps:
                        deps.remove(pkg.name)
                        if not deps:
                            return True
            if not deps:
                return True
            return False

        def _findHighestDepBuildGroup(specFile, groups):
            if not specFile.kf5BuildRequiresNames:
                return -1

            maxGroupIndex = 0
            for dep in specFile.kf5BuildRequiresNames:
                groupIndex = 0
                for group in groups:
                    matched = False
                    for pkg in group:
                        if pkg.name == dep:
                            matched = True
                            break
                    if matched:
                        break
                    groupIndex += 1
                if groupIndex > maxGroupIndex:
                    maxGroupIndex = groupIndex

            return maxGroupIndex

        groups = [[]]
        while specFiles:
            specFile = specFiles.pop(0)
            if not _allDepsAnalyzed(specFile, groups):
                specFiles.append(specFile)
                continue

            highestDepGroup = _findHighestDepBuildGroup(specFile, groups)
            destGroup = highestDepGroup + 1
            if len(groups) - 1 < destGroup:
                groups.insert(destGroup, [ specFile ])
            else:
                groups[destGroup].append(specFile)

        return groups


class KDEUpdateTag(KDEUpdate):

    def __init__(self, args):
        super(KDEUpdateTag, self).__init__(args)

    def run(self):
        # 1) get projects XML list
        # 2) list local fedpkg clones
        # 3) compare them, abort on mismatch
        # 4) list all builds in koji source tag
        # 5) compare local packages to builds in source tag
        #   5a) find packages to tag into dest tag
        # 6) confirm list of packages to tag
        # 7) tag builds from source to dest tag
        # 8) (optional) create a Bodhi update
        pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', action='store',
                        choices = [ 'new-version', 'build', 'tag' ],
                        help='Operation to perform')
    (args, other) = parser.parse_known_args()

    task = None
    if args.command == 'new-version':
        task = KDEUpdateNewVersion(other)
    elif args.command == 'build':
        task = KDEUpdateBuild(other)
    elif args.command == 'tag':
        task = KDEUpdateTag(other)
    else:
        raise Exception('Unexpected command %s' % args.command)

    task.run()

if __name__ == "__main__":
    main()