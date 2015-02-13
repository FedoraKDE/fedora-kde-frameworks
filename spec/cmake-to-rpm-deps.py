#!/bin/env python3

import argparse
import io
import os
import os.path
import re
import subprocess
import tempfile

# Those are frameworks that don't have "K" prefix
_KExceptions = [ "attica", "frameworkintegration", "solid", "sonnet", "threadweaver" ]

_IgnoredDeps = [ "kf5-rpm-macros", "kf5-filesystem", "extra-cmake-modules", "qt5-qtwinextras-devel", "qt5-qtmacextas-devel" ]

_NoDevelSuffix = [ "qt5-qttools-static" ]

# http://www.cmake.org/cmake/help/v3.0/command/find_package.html
_FindPackageKeywords = [ "EXACT", "QUIET", "MODULE", "REQUIRED",  "COMPONENTS",
                         "CONFIG", "NO_MODULE", "OPTIONAL_COMPONENTS", "NO_POLICY_SCOPE" ]

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
        fwname = cmakeName

    if prefix == "kf5":
        if (not fwname in _KExceptions) and (not fwname[0] == 'k'):
            fwname = "k%s" % fwname

        return "kf5-%s" % fwname

    elif prefix == "qt5":
        # Fedora-specific mapping of Qt5 modules to package names
        if fwname in [ "concurrent", "core", "dbus", "gui", "network", "sql", "widgets", "xml", "test" ]:
            fwname = "qtbase"
        elif fwname in [ "qml", "quick", "quickwidgets" ]:
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
    subprocess.call([ "rm", "-rf", sourceDir ])


def findCMakeConfigFile(sources, moduleName):
    name = "%sConfig.cmake.in" % moduleName
    for dirpath, dirnames, filenames in os.walk(sources):
        if name in filenames:
            return os.path.join(dirpath, name)
    return None

def findCMakeListsFile(sources):
    name = "CMakeLists.txt"
    for dirpath, dirnames, filenames in os.walk(sources):
        if name in filenames:
            return os.path.join(dirpath, name)
    return None


def parseRequires(requires, buildRequires = False):
    if buildRequires:
        keyword = "BuildRequires"
    else:
        keyword = "Requires"

    matches = re.match(r"%s:[\ ]*([\w0-9\-_]+)[.]*" % keyword, requires)
    if matches:
        match = matches.groups(1)[0]
        return match

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
        if line.startswith("%package") and line.endswith("devel"):
            inMain = False
            inDevel = True
        elif line.startswith("%package") and not line.endswith("devel"):
            inMain = False
            inDevel = False

        if inMain:
            if line.startswith("BuildRequires:"):
                br = parseRequires(line, True)
                if br:
                    if br.startswith("kf5-"):
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

                inMain = False
                inKF5Requires = False
            else:
                out.append(origLine)

        elif inDevel:
            if line.startswith("Requires:"):
                br = parseRequires(line)
                if br:
                    if br.startswith("kf5-"):
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


def parseBuildDeps(cmakeFile):
    f = open(cmakeFile, 'r')
    deps = []
    for line in f:
        line = line.strip()
        if line.startswith("find_package("):
            macro = "find_package"
        elif line.startswith("find_dependency("):
            macro = "find_dependency"
        else:
            macro = None

        if macro and line.startswith("%s(KF5 " % macro) or line.startswith("%s(Qt5 " % macro):
            if line.startswith("%s(KF5 " % macro):
                prefix = "kf5"
            else:
                prefix = "qt5"
            matches = re.search(r"%s\((.*)\)" % macro, line)
            if matches:
                match = matches.groups(1)[0]
                matchList = match.split(' ')
                for m in matchList:
                    # First regexp: match @FOO@ or ${FOO}, also with quotes when present
                    # Second regexp: match version number
                    if not (m == "KF5" or m == "Qt5" or m in _FindPackageKeywords or re.match(r"[\"]*(?:@|\${)[a-zA-Z0-9\-\_]*(?:@|})[\"]*", m) or re.match(r"[0-9\.]+", m)):
                        name = cmakeName2PkgName(m, prefix)
                        if not name in _NoDevelSuffix:
                            name = "%s-devel" % name
                        if name not in _IgnoredDeps:
                            deps.append(name)

        elif macro and line.startswith("%s(KF5" % macro) or line.startswith("%s(Qt5" % macro):
            matches = re.search(r"%s\(([\w0-9]+)\ .*\)" % macro, line)
            if matches:
                match = matches.groups(1)[0]
                name = cmakeName2PkgName(match)
                if not name in _NoDevelSuffix:
                    name = "%s-devel" % name
                if name not in _IgnoredDeps:
                    deps.append(name)

    return deps



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specfile', metavar='SPEC')
    args = parser.parse_args()


    f = open(args.specfile, 'r')
    inFilesDevel = False
    inPkgDevel = False
    cmakeName = None
    currentDeps = [];
    currentDevelDeps = []

    for line in f:
        line = line.strip()
        if line.startswith("BuildRequires:"):
            dep = line.rsplit(' ', 1)[1]
            if dep.startswith("qt5-") or dep.startswith("kf5-") and dep not in _IgnoredDeps:
                currentDeps.append(dep);
            continue

        if not inPkgDevel:
            if line.startswith("%package") and line.endswith("devel"):
                inPkgDevel = True
                continue
        else:
            if line.startswith("Requires:"):
                dep = line.rsplit(' ', 1)[1]
                if dep.startswith("qt5-") or dep.startswith("kf5-"):
                    currentDevelDeps.append(dep);
            elif line.startswith("%description"):
                inPkgDevel = False

        if not inFilesDevel:
            if line.startswith("%files devel"):
                inFilesDevel = True
                continue
        else:
            if line.startswith("%{_kf5_libdir}/cmake/"):
                if line.endswith('/'):
                    line = line[0:-1]
                cmakeName = line.rsplit('/', 1)[1]
                break;
            elif line.startswith("%files") or line.startswith("%changelog"):
                inFilesDevel = False

    if not cmakeName:
        print("Failed to detect CMake name for %s" % args.specfile)
        return


    srcFile = getSource(args.specfile)
    if not srcFile:
        print("Failed to detect source")
        return

    srcDir = extractSource(srcFile)

    cmakeConfigFile = findCMakeConfigFile(srcDir, cmakeName)
    if not cmakeConfigFile:
        print("Failed to find CMake config file")
        return

    cmakeListsFile = findCMakeListsFile(srcDir)
    if not cmakeListsFile:
        print("Failed to find CMakeLists.txt file")
        return

    develDeps = parseBuildDeps(cmakeConfigFile)
    deps = parseBuildDeps(cmakeListsFile)

    cleanupSource(srcDir)

    print(cmakeName)
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

