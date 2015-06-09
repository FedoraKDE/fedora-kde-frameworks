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

import argparse
import io
import os
import os.path
import re
import subprocess
import tempfile

# Those are frameworks that don't have "K" prefix
_KExceptions = [ "attica", "frameworkintegration", "solid", "sonnet", "threadweaver", "plasma", "networkmanager-qt" ]

# Stuff that matches our filters, but must be ommitted
# - kf5-kdelibs4support-devel is listed because no frameworks are allowed to depend on KDELibs4Support,
#   but from time to time there's a dep in a disabled (unported) subfolder, which we cannot distinguish easilly
_IgnoredDeps = [ "kf5-rpm-macros", "kf5-filesystem", "extra-cmake-modules", "qt5-qtwinextras-devel",
                 "qt5-qtmacextras-devel", "kf5-kdelibs4support-devel", "qt5-qttexttospeech-devel" ]

# Stuff that breaks our assumption that all BR must have -devel suffix
_NoDevelSuffix = [ "qt5-qttools-static" ]

# http://www.cmake.org/cmake/help/v3.0/command/find_package.html + some more custom keywords
_FindPackageKeywords = [ "EXACT", "QUIET", "MODULE", "REQUIRED",  "COMPONENTS",
                         "CONFIG", "NO_MODULE", "OPTIONAL_COMPONENTS", "NO_POLICY_SCOPE" ]


class DependencyException(Exception):
    def __init__(self, reason):
        super(DependencyException, self).__init__(reason)

class Dependency:
    _pkgname = None
    _isa = None
    _versionCond = None
    _version = None

    def __init__(self, dep):
        parts = re.search(r'([\w-]+)[\ ]*(\([\w]+\)){0,1}[\ ]*([\<\>\=]*){1}[\ ]*([0-9\.\-\w]*){1}', dep)
        if not parts or len(parts.groups()) < 4:
            raise DependencyException("'%s' is not a valid dependency string" % dep)

        groups = parts.groups()
        self._pkgname = groups[0]
        self._isa = groups[1]
        self._versionCond = groups[2] if groups[2] else None
        self._version = groups[3] if groups[3] else None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self._isa:
            name = '%s%s' % (self._pkgname, self._isa)
        else:
            name = self._pkgname

        if self._versionCond and self._version:
            return '%s %s %s' % (name, self._versionCond, self._version)
        else:
            return name

    def __eq__(self, other):
        return self._pkgname == other.name()

    def __lt__(self, other):
        return self._pkgname < other.name()

    def __hash__(self):
        return self._pkgname.__hash__()

    def name(self):
        return self._pkgname

    def isa(self):
        return self._isa

    def versionCond(self):
        return self._versionCond

    def version(self):
        return self._version

    def isIgnored(self):
        return self._pkgname in _IgnoredDeps

    def isQt5(self):
        return self._pkgname.startswith('qt5-')

    def isKF5(self):
        return self._pkgname.startswith('kf5-')

    def isQt5OrKF5(self):
        return self.isQt5() or self.isKF5()




def cmakeName2PkgName(cmakeName, prefix = None):
    cmakeName = cmakeName.lower()
    if not prefix:
        if cmakeName.startswith("kf5"):
            prefix = "kf5"
            fwname = cmakeName[3:]
        elif cmakeName.startswith("qt5"):
            prefix = "qt5"
            fwname = cmakeName[3:]
        else:
            fwname = cmakeName
    else:
        prefix = prefix.lower()
        fwname = cmakeName

    if prefix == "kf5":
        # Handle legacy KDE4Support -> KdeLibs4Support rename
        if fwname == "kde4support":
            fwname = "kdelibs4support"
        # Handle "KF5Su" -> "KF5KDESu"
        elif fwname == "su":
            fwname ="kdesu"

        if (not fwname in _KExceptions) and (not fwname[0] == 'k'):
            fwname = "k%s" % fwname

        return "kf5-%s" % fwname

    elif prefix == "qt5":
        # Fedora-specific mapping of Qt5 modules to package names
        if fwname in [ "concurrent", "core", "dbus", "gui", "network", "sql", "widgets", "xml", "test", "printsupport" ]:
            fwname = "qtbase"
        elif fwname in [ "qml", "quick", "quickwidgets", "quicktest" ]:
            fwname = "qtdeclarative"
        elif fwname == "declarative":
            fwname = "qtquick1"
        elif fwname == "webkitwidgets":
            fwname = "qtwebkit"
        elif fwname == "uitools":
            fwname = "qttools-static"
        elif fwname == "designer":
            fwname = "qttools"
        else:
            fwname = "qt%s" % fwname

        return "qt5-%s" % fwname

    else:
        return None


def getSource(specfile):
    # TODO: Download the file when necessary
    p = subprocess.Popen([ "spectool", "-s", "0", specfile ], stdout=subprocess.PIPE)
    out = p.communicate()
    filename = out[0].decode('UTF-8').strip().rsplit('/', 1)[1]

    srcname = os.path.expanduser("~/rpmbuild/SOURCES/%s" % filename)
    if not os.path.isfile(srcname):
        return None
    else:
        return srcname


def extractSource(source):
    tmpdir = tempfile.mkdtemp()
    subprocess.call([ "tar", "-xf", source, "-C", tmpdir ])
    return tmpdir

def cleanupSource(sourceDir):
    # TODO: Moar safety
    subprocess.call([ "rm", "-rf", sourceDir ])

def _findCMakeFile(sources, filename):
    matches = []
    for dirpath, dirnames, filenames in os.walk(sources):
        if filename in filenames:
            matches.append(os.path.join(dirpath, filename))
    return matches

def findCMakeConfigFile(sources, moduleName):
    matches = _findCMakeFile(sources, "%sConfig.cmake.in" % moduleName)
    return matches[0] if matches else None

def findCMakeListsFiles(sources):
    return _findCMakeFile(sources, "CMakeLists.txt")


def parseRequires(requires, buildRequires = False):
    if buildRequires:
        keyword = "BuildRequires"
    else:
        keyword = "Requires"

    matches = re.match(r"%s:[\ ]*([\w\-]+)[.]*" % keyword, requires)
    if matches:
        return Dependency(matches.groups(1)[0])

    return None


def updateSpecFile(specfile, depsAdd, depsRemove, develDepsAdd, develDepsRemove):
    out = []
    f = open(specfile, 'r')
    inMain = True
    inDevel = False
    inRequires = False
    inKF5Requires = False
    for line in f:
        origLine = line
        line = line.strip()

        # Copy commented lines as they are, don't attempt to parse them
        if line.startswith("#"):
            out.append(origLine)
            continue

        if line.startswith("%package") and line.endswith("devel"):
            inMain = False
            inDevel = True
        elif line.startswith("%package") and not line.endswith("devel"):
            inMain = False
            inDevel = False
        elif inMain and line.startswith("%description"):
            inMain = False

        if inMain:
            if line.startswith("BuildRequires:"):
                br = parseRequires(line, True)
                if br:
                    if br.isKF5():
                        inKF5Requires = True
                    if br in depsRemove:
                        continue

                out.append(origLine)

            elif inKF5Requires:
                if depsAdd:
                    for br in depsAdd:
                        out.append("BuildRequires:  %s\n" % br)
                    out.append("\n")
                    depsAdd = []
                else:
                    out.append(origLine)

                inKF5Requires = False
            else:
                out.append(origLine)

        elif inDevel:
            if line.startswith("Requires:"):
                br = parseRequires(line)
                if br:
                    if br.isKF5():
                        inKF5Requires = True

                    if br in develDepsRemove:
                        continue
                out.append(origLine)

            elif inKF5Requires or (not inKF5Requires and (not line or line.startswith("%description"))):
                if develDepsAdd:
                    for br in develDepsAdd:
                        out.append("Requires:       %s\n" % br)
                    out.append("\n")
                    develDepsAdd = []
                    if (not inKF5Requires and line.startswith("%description")):
                        out.append(origLine)
                else:
                    out.append(origLine)

                inDevel = False
                inKF5Requires = False
            else:
                out.append(origLine)
        else:
            out.append(origLine)

    f = open(specfile, 'w')
    for line in out:
        f.write(line)


def parseBuildDeps(cmakeFile, variablesDict = None):
    f = open(cmakeFile, 'r')
    deps = []
    if not variablesDict:
        variablesDict = {}
    for line in f:
        line = line.strip()

        # Skip comments
        if line.startswith("#"):
            continue

        matchVariable = re.match(r"^set[\ ]*\(([\w\-]+)[\ ]+[\"]*([\w\.\-]+)[\"]*[\ ]*[.]*\)", line)
        if matchVariable:
            variablesDict[matchVariable.groups(1)[0]] = matchVariable.groups(1)[1]


        # The last group ([\ ]*) is important as we use it to distinguish find_package(Qt5Foo ...) and find_package(Qt5 ... Foo Bar)
        macroMatches = re.match(r"^(find_package|find_dependency)[\ ]*\([\ ]*(Qt5|KF5)([\ ]*)", line)
        if macroMatches:
            macro = macroMatches.groups(1)[0]
            prefix = macroMatches.groups(1)[1]
            isComponent = (macroMatches.groups(1)[2] == ' ')
        else:
            macro = None
            prefix = None
            isComponent = False

        # Handle find_package(Qt5 ... Foo Bar ...)
        if macro and prefix and isComponent:
            # Match the entire string within parenthesis, split it by space
            matches = re.search(r"%s[\ ]*\((.*)\)" % macro, line)
            if matches:
                match = matches.groups(1)[0]
                matchList = match.split(' ')
                for m in matchList:
                    # Skip CMake keywords, version numbers and variable names (that's the huge regexp
                    # to match ${FOO} and @FOO@ both with and without quotes
                    variableMatch = re.search(r"[\"]*((?:@|\${)([\w\-]+)(?:@|}))[\"]*", m)
                    if variableMatch:
                        varStr = variableMatch.group(1)[0]
                        varName = variableMatch.group(1)[1]
                        # TODO: Replace variables, parse versions from "m" and store
                        # touple (name, version) in deps.
                        # TODO: Also make sure that this method returns touple (deps, variablesDict),
                        # so that we can pass the variables again to next call
                        print("Group 1: %s" % variableMatch.groups(1)[0])
                        print("Group 2: %s" % variableMatch.groups(1)[1])

                    if not (m == "KF5" or m == "Qt5" or m in _FindPackageKeywords or re.match(r"[\"]*(?:@|\${)[\w\-]*(?:@|})[\"]*", m) or re.match(r"[0-9\.]+", m)):
                        name = cmakeName2PkgName(m, prefix)
                        if not name in _NoDevelSuffix:
                            name = "%s-devel" % name
                        if name not in _IgnoredDeps:
                            deps.append(Dependency(name))

        # Handle find_package(Qt5Foo ...)
        elif macro and prefix and not isComponent:
            # Match the first word in parenthesis, which is name of the module
            matches = re.search(r"%s[\ ]*\(([\w]+)\ .*\)" % macro, line)
            if matches:
                match = matches.groups(1)[0]
                name = cmakeName2PkgName(match)
                if not name in _NoDevelSuffix:
                    name = "%s-devel" % name
                if name not in _IgnoredDeps:
                    deps.append(Dependency(name))

        # Look for inclusion of ECMPoQmTools, which requires qt5-qttools-devel installed
        elif not macro and re.match("^include[\ ]*\([\ ]*ECMPoQmTools[\ ]*\)", line):
                deps.append(Dependency("qt5-qttools-devel"))


    return deps



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specfile', metavar='SPEC')
    args = parser.parse_args()

    providesSP = subprocess.Popen(['rpmspec', '-q', '--provides', args.specfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, errs = providesSP.communicate()
    if errs.decode('UTF-8'):
        print("Error processing %s: %s" % (args.specfile, errs.decode('UTF-8')))
        return
    provides = out.decode('UTF-8').split('\n')

    parsedSP = subprocess.Popen(['rpmspec', '-P', args.specfile], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, errs = parsedSP.communicate()
    if errs.decode('UTF-8'):
        print("Error processing %s: %s:" % (args.specfile, errs.decode('UTF-8')))
        return
    parsed = out.decode('UTF-8').split('\n')

    inFilesDevel = False
    inPkgDevel = False
    cmakeName = None
    currentDeps = [];
    currentDevelDeps = []
    pkgName = None

    # Parse the SPEC file
    for line in parsed:
        line = line.strip()

        # Skip comments
        if line.startswith("#"):
            continue;

        # Get package name
        if line.startswith("Name:"):
            pkgName = line.rsplit(' ', 1)[1]
            continue

        # Parse all BR that start with qt5- or kf5-
        if line.startswith("BuildRequires:"):
            try:
                dep = Dependency(line.rsplit(' ', 1)[1])
            except DependencyException:
                continue

            if not dep.isIgnored() and dep.isQt5OrKF5():
                currentDeps.append(dep)
            continue

        # Detect beginning of -devel subpackage
        if not inPkgDevel:
            if line.startswith("%package") and line.endswith("devel"):
                inPkgDevel = True
                continue
        else:
            # Parse all qt5- or kf5- Requires within -devel subpackage
            if line.startswith("Requires:"):
                dep = Dependency(line.rsplit(' ', 1)[1])
                if dep.isQt5OrKF5():
                    currentDevelDeps.append(dep);
            # Reaching %description macro within -devel subpackage means end of -devel
            elif line.startswith("%description"):
                inPkgDevel = False

        # Detect beginning of %files devel segment
        if not inFilesDevel:
            if re.match(r"%files[\ ]+devel", line):
                inFilesDevel = True
                continue
        else:
            # Don't attempt to parse %changelog, it can contain all kinds of tricky stuff
            # We can simply stop parsing the spec file here, as there nothing interesting
            # for us beyond %changelog.
            if line.startswith("%changelog"):
                break;

            # Match FooBar from %{_kf5_libdir}/cmake/FooBar
            # This is the only "clever" way how to get the name of the actual
            # CMake module.
            m = re.search(r"/usr/lib(|64)/cmake/([\w]+)[/]*", line)
            if m:
                cmakeName = m.groups(1)[1]
                # This is the last thing we need from this loop
                break


    if not cmakeName:
        print("Failed to detect CMake name for %s" % args.specfile)
        return

    print("%s => %s" % (pkgName, cmakeName))

    srcFile = getSource(args.specfile)
    if not srcFile:
        print("Failed to detect source")
        return

    srcDir = extractSource(srcFile)

    cmakeConfigFile = findCMakeConfigFile(srcDir, cmakeName)
    if not cmakeConfigFile:
        print("Failed to find CMake config file")
        return
    develDeps = parseBuildDeps(cmakeConfigFile)

    cmakeListsFiles = findCMakeListsFiles(srcDir)
    if not cmakeListsFiles:
        print("Failed to find CMakeLists.txt file")
        return

    deps = []
    # We need to iterate through all CMakeLists.txt files, since some
    # dependencies might be listed there too
    for cmakeListsFile in cmakeListsFiles:
        deps = deps + parseBuildDeps(cmakeListsFile)


    cleanupSource(srcDir)


    currentDeps = list(set(currentDeps))
    deps = list(set(deps))
    depsAdd = list(set(deps) - set(currentDeps))
    depsRemove = list(set(currentDeps) - set(deps))

    if not depsAdd and not depsRemove:
        print("\tBuild dependencies OK")
    else:
        print("\tDEPS ADD:          %s" % sorted(depsAdd))
        print("\tDEPS REMOVE:       %s" % sorted(depsRemove))

    currentDevelDeps = list(set(currentDevelDeps))
    develDeps = list(set(develDeps))
    develDepsAdd = list(set(develDeps) - set(currentDevelDeps))
    develDepsRemove = list(set(currentDevelDeps) - set(develDeps))

    if not develDepsAdd and not develDepsRemove:
        print("\tDevel dependencies OK")
    else:
        print("\tDEVEL DEPS ADD:    %s" % sorted(develDepsAdd))
        print("\tDEVEL DEPS REMOVE: %s" % sorted(develDepsRemove))


    if depsAdd or depsRemove or develDepsAdd or develDepsRemove:
        updateSpecFile(args.specfile, depsAdd, depsRemove, develDepsAdd, develDepsRemove)


if __name__ == "__main__":
    main();

