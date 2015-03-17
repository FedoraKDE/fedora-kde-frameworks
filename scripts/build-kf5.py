#!/bin/python3
# -*- coding:utf-8 -*-

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

import argparse
import subprocess
import gitapi
import os

_MapDeps = { 'kf5-rpm-macros' : 'kf5' }

class Package:
    _name = None
    _deps = []
    _repo = None
    _spec = None

    def __init__(self, spec):
        paths = spec.rsplit('/', 2)
        self._spec = spec
        self._repo = '%s/%s' % (paths[0], paths[1])
        self._name = paths[1]
        self._parseDeps()

    def __repr__(self):
        return self._name

    def name(self):
        return self._name

    def deps(self):
        return self._deps

    def repo(self):
        return self._repo

    def spec(self):
        return self._spec

    def _parseDeps(self):
        f = open(self._spec, 'r')
        deps = []
        for line in f:
            line = line.strip()

            # Skip comments
            if line.startswith('#'):
                continue

            if line.startswith('BuildRequires:'):
                brs = line.split(':')
                brName = brs[1].strip()
                if brName.startswith('kf5') or brName == 'extra-cmake-modules':
                    if brName.endswith('-devel'):
                        brName = brName[0:-6]
                    if brName in _MapDeps:
                        deps.append(_MapDeps[brName])
                    else:
                        deps.append(brName)
                continue

            if line.startswith('%changelong'):
                break

        self._deps = deps



def findAllPackages(args):
    pkgs =  [ Package('%s/kf5/kf5.spec' % args.pkgroot),
              Package('%s/extra-cmake-modules/extra-cmake-modules.spec' % args.pkgroot) ]
    for tier in [ 1, 2, 3, 4 ]:
        fws = os.listdir('%s/tier%d' % (args.pkgroot, tier));
        fws = map(lambda x: Package("%s/tier%d/%s/%s.spec" % (args.pkgroot, tier, x, x)), fws)
        pkgs += fws

    return pkgs

def allDepsAnalyzed(package, groups):
    deps = package.deps().copy()
    if not deps:
        return True

    for group in groups:
        for pkg in group:
            if pkg.name() in deps:
                deps.remove(pkg.name())
                if not deps:
                    return True

    if not deps:
        return True

    #print('Package %s missing deps: %s' % (package.name(), deps))
    return False

def findHighestDepBuildGroup(package, groups):
    if not package.deps():
        return -1

    maxGroupIndex = 0
    for dep in package.deps():
        groupIndex = 0
        for group in groups:
            matched = False
            for pkg in group:
                if pkg.name() == dep:
                    matched = True
                    break

            if matched:
                break

            groupIndex += 1

        if groupIndex > maxGroupIndex:
            maxGroupIndex = groupIndex

    return maxGroupIndex

def createBuildGroups(packages):
    groups = [[]]
    while packages:
        package = packages.pop(0)
        if not allDepsAnalyzed(package, groups):
            packages.append(package)
            continue

        highestDepGroup = findHighestDepBuildGroup(package, groups)
        destGroup = highestDepGroup + 1
        if len(groups) - 1 < destGroup:
            groups.insert(destGroup, [ package ])
        else:
            groups[destGroup].append(package)
        #print("Added %s to group %d" % (package.name(), destGroup))

    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pkgroot', action='store', default=os.getcwd(),
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

    packages = findAllPackages(args)
    groups = createBuildGroups(packages)

    i = 0
    for group in groups:
        print("Group %i: %s" % (i, group))
        i += 1


    branch = args.branch
    if not branch:
        if args.target.startswith('f23'):
            branch = 'master'
        else:
            branch = args.target

    buildChain = []
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

            buildChain.append(pkg)
        if len(buildChain) > 0:
            if buildChain[-1] != ':':
                buildChain.append(':')

    # Drop the trailing colon
    buildChain.pop()
    # Get the last pkg: we'll run chainbuild from there
    lastPkg = buildChain.pop()

    buildChainNames = list(map(lambda x: x.name() if isinstance(x, Package) else x, buildChain))
    print('Build chain: %s' % ' '.join(buildChainNames))
    print('Koji Target: %s' % args.target)
    print('Branch: %s' % branch)
    print('Chainbuild package: %s' % lastPkg.repo())

    proceed = input('Proceed? [Y/n] ')
    if proceed.lower() == 'n':
        return

    repo = gitapi.Repo(lastPkg.repo())
    repo.git_checkout(branch)

    p = subprocess.Popen(['fedpkg', 'chain-build', '--target=%s' % args.target] + buildChainNames,
                         cwd = lastPkg.repo())
    p.wait()


if __name__ == "__main__":
    main()