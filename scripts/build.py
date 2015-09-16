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
import itertools

from Package import *


def findAllPackages(args):
    pkgs = []
    fws = os.listdir(args.pkgroot);
    fws = map(lambda x: Package("%s/%s/%s.spec" % (args.pkgroot, x, x), args), fws)
    pkgs += fws

    return pkgs

def allDepsAnalyzed(package, groups, allPackagesNames, debug = False):
    deps = list(set(package.otherBuildRequiresNames.copy() + package.kf5BuildRequiresNames.copy() + package.kf5RequiresNames.copy()))
    if not deps:
        return True

    ourDeps = []
    for dep in deps:
        if dep in allPackagesNames:
            ourDeps.append(dep)

    for group in groups:
        for pkg in group:
            if pkg.name in ourDeps:
                ourDeps.remove(pkg.name)
                if not ourDeps:
                    return True

    if not ourDeps:
        return True

    if debug:
        print('Package %s missing deps: %s' % (package.name, ourDeps))

    return False

def findHighestDepBuildGroup(package, groups, allPackagesNames, debug = False):
    deps = list(set(package.otherBuildRequiresNames.copy() + package.kf5BuildRequiresNames.copy() + package.kf5RequiresNames.copy()))
    if not deps:
        return -1;

    ourDeps = []
    for dep in deps:
        if dep in allPackagesNames:
            ourDeps.append(dep)

    maxGroupIndex = 0
    for dep in ourDeps:
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

def createBuildGroups(packages, allPackagesNames, debug = False):
    groups = [[]]
    while packages:
        package = packages.pop(0)
        if not allDepsAnalyzed(package, groups, allPackagesNames, debug):
            packages.append(package)
            continue

        highestDepGroup = findHighestDepBuildGroup(package, groups, allPackagesNames, debug)
        destGroup = highestDepGroup + 1
        if len(groups) - 1 < destGroup:
            groups.insert(destGroup, [ package ])
        else:
            groups[destGroup].append(package)

        if debug:
            print("Added %s to group %d" % (package.name, destGroup))

    return groups


def buildInCopr(args, packages):

    buildGroups = []
    buildGroup = []
    names = []
    for pkg in packages:
        if isinstance(pkg, Package):
            buildGroup.append('%s/%s-%s-%s.src.rpm'
                               % (args.url, pkg.name, pkg.version, pkg.release))
            names.append(pkg.name)
        elif pkg == ':':
            buildGroups.append(buildGroup)
            buildGroup = []
            names.append(':')

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

    pkgnames = list(map(lambda x: x.name if isinstance(x, Package) else x, packages))

    print('Packages to build: %s' % ' '.join(pkgnames))
    print('Koji Target: %s' % args.target)
    print('Branch: %s' % args.branch)
    print('Chainbuild package: %s/%s' % (args.pkgroot, lastPkg.name))

    proceed = input('Proceed? [Y/n] ')
    if proceed.lower() == 'n':
        return

    repo = gitapi.Repo('%s/%s' % (args.pkgroot, lastPkg.name))
    repo.git_checkout(args.branch)
    repo.git_pull()

    p = subprocess.Popen(['fedpkg', 'chain-build', '--target=%s' % args.target] + pkgnames,
                     cwd = '%s/%s' % (args.pkgroot, lastPkg.name))
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
    parser.add_argument('--url', action='store', default='http://pub.dvratil.cz/srpm/kf5/5.12/',
                        help='Base URL for SRPMS for Copr builds')
    parser.add_argument('--dist', action='store', default='fc22')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Debug dependency solver')

    args = parser.parse_args()

    packages = findAllPackages(args)
    packageNames = list(map(lambda x : x.name, packages))
    print("Found packages: %s" % packageNames)

    groups = createBuildGroups(packages, packageNames,args.debug)

    i = 0
    for group in groups:
        print("Group %i: %s" % (i, list(map(lambda x : x.name, group))))
        i += 1

    branch = args.branch
    if not branch:
        if args.target.startswith('f24'):
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

    if args.copr:
        buildInCopr(args, buildChain)
    else:
        buildInKoji(args, buildChain)


if __name__ == "__main__":
    main()
