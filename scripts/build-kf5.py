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

from Package import *


def findAllPackages(args):
    pkgs =  [ Package('%s/kf5/kf5.spec' % args.pkgroot, args),
              Package('%s/extra-cmake-modules/extra-cmake-modules.spec' % args.pkgroot, args) ]
    for tier in [ 1, 2, 3, 4 ]:
        fws = os.listdir('%s/tier%d' % (args.pkgroot, tier));
        fws = map(lambda x: Package("%s/tier%d/%s/%s.spec" % (args.pkgroot, tier, x, x), args), fws)
        pkgs += fws

    return pkgs

def allDepsAnalyzed(package, groups):
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

    #print('Package %s missing deps: %s' % (package.name, deps))
    return False

def findHighestDepBuildGroup(package, groups):
    if not package.kf5BuildRequiresNames:
        return -1

    maxGroupIndex = 0
    for dep in package.kf5BuildRequiresNames:
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
        #print("Added %s to group %d" % (package.name, destGroup))

    return groups


def buildInCopr(args, groups):

    buildGroups = []
    buildGroup = []

    names = []
    for group in groups:
        buildGroup = []
        for pkg in group:
            buildGroup.append('http://pub.dvratil.cz/kf5/srpm/%s/%s-%s-%s.src.rpm'
                               % (pkg.version, pkg.name, pkg.version, pkg.release))
            names.append(pkg.name)

        names.append(':')
        buildGroups.append(buildGroup)

    print('Packages to build: %s' % ' '.join(names))
    print('Copr: %s' % args.copr)
    print('Build URLs: %s' % buildGroups)
    print('!! WARNING !! HAVE YOU DISABLED BUILD PUBLISHING?')
    proceed = input('Proceed? [Y/n] ')
    if proceed.lower() == 'n':
        return

    for buildGroup in buildGroups:
        p = subprocess.Popen(['copr-cli', 'build', args.copr] + buildGroup)
        p.wait()


def buildInKoji(args, packages):

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
    repo.git_pull()

    p = subprocess.Popen(['fedpkg', 'chain-build', '--target=%s' % args.target] + packages,
                     cwd = '%s/%s' % (args.pkgroot, lastPkg))
    p.wait()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pkgroot', action='store', default=os.getcwd(),
                        help='Root directory where all fedpkg clones are')
    parser.add_argument('--resume-from',
                        help='Resume build from specified package, skipping all previous packages')
    parser.add_argument('-x', '--exclude', action='append',
                        help='Exclude certain package from build. Can be used multiple times. Can be combined with --resume-from')
    parser.add_argument('--target', action='store',
                        help='Koji target to build into')
    parser.add_argument('--branch',
                        help='Distgit branch to build from')
    parser.add_argument('--copr', action='store',
                        help='Copr to build in')
    parser.add_argument('--dist', action='store', default='fc21')
    args = parser.parse_args()

    packages = findAllPackages(args)
    groups = createBuildGroups(packages)

    i = 0
    for group in groups:
        print("Group %i: %s" % (i, group))
        i += 1


    if args.copr:
        buildInCopr(args, groups)
    else:
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
                    if args.resume_from == pkg.name:
                        skipPackages = False
                    else:
                        continue

                if args.exclude and pkg.name in args.exclude:
                    continue

                buildChain.append(pkg)
            if len(buildChain) > 0:
                if buildChain[-1] != ':':
                    buildChain.append(':')


        buildInKoji(args, buildChain);


if __name__ == "__main__":
    main()
