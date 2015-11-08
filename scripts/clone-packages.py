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

import urllib.request as urllib
import xml.etree.ElementTree as ET
import subprocess
import os.path
import argparse
import yaml

_IgnoredKDEProjects = [
    "user-manager",
    "kde-gtk-config",
    "kwallet-pam",
    "kaccounts-mobile",
    "discover"
]

_KDEToFedoraNamesMap = {
# Plasma
    "breeze": "plasma-breeze",
    "kcm-touchpad": "kcm_touchpad",
    "libkscreen": "libkscreen-qt5",
    "kfilemetadata": "kf5-kfilemetadata",
    "oxygen": "plasma-oxygen",
    "polkit-kde-agent-1": "polkit-kde",
    "systemsettings": "plasma-systemsettings",
    "kwayland": "kf5-kwayland",
    "milou": "plasma-milou",
    "bluez-qt": "kf5-bluez-qt",
    "kgamma5": "kgamma",
# Frameworks
    "plasma-framework": "kf5-plasma"
}


class ParsingException(Exception):
    pass

def downloadKDEMetaData():
    print("Downloading KDE projects metadata...", end = '', flush = True)
    response = urllib.urlopen("https://projects.kde.org/kde_projects.xml")
    metadata = response.read()
    print("Done", flush = True)
    return metadata

def getProductComponent(root, product):
    if product == 'plasma':
        kdeComponent = None
        for component in root.iterfind("component"):
            if component.get("identifier") == "kde":
                kdeComponent = component
                break
        if not kdeComponent:
            raise ParsingException("Invalid XML: could not find KDE component")

        workspaceModule = None
        for module in kdeComponent.iterfind("module"):
            if module.get("identifier") == "workspace":
                workspaceModule = module
                break
        if not workspaceModule:
            raise ParsingException("Invalid XML: could not find workspace module")

        return workspaceModule

    elif product == 'frameworks':
        frameworksComponent = None
        for component in root.iterfind("component"):
            if component.get("identifier") == "frameworks":
                frameworksComponent = component
                break
        if not frameworksComponent:
            raise ParsingException("Invalid XML: could not find Frameworks component")

        return frameworksComponent

    else:
        raise ParsingException("Unknown product %s" % product)

    return None

def parseKDEMetaData(metadata, product):
    print("Parsing KDE projects metadata...", flush = True)
    root = ET.fromstring(metadata)
    if product == "frameworks":
        query = "./component[@identifier='frameworks']/module"
    else:
        query = "./component[@identifier='kde']/module[@identifier='workspace']/project"

    components = root.findall(query)
    projects = {}
    for project in components:
        name = project.get("identifier")
        if name in _IgnoredKDEProjects:
            print("\tIgnoring %s" % name, flush = True)
            continue

        repo = project.find("repo")
        if not repo:
            raise ParsingException("Invalid XML: could not find repo information for module %s" % name)

        gitweb = None
        for web in repo.iterfind("web"):
            if web.get("type") == "gitweb":
                gitweb = web.text
                break
        if not gitweb:
            raise ParsingException("Invalid XML: could not find gitweb information about module %s" % name)

        projects[name] = { "name": name,
                           "gitweb": gitweb
                         }

        print("\tFound project %s" % name, flush = True)

    print("Done", flush = True)
    return projects

def fetchYamlMetaData(modules):
    for moduleName in modules:
        print("Retrieving YAML metadata for %s..." % moduleName, end = '', flush = True)
        response = urllib.urlopen("http://gitweb.kde.org/?p=%s.git&a=blob&o=plain&f=metainfo.yaml" % moduleName)
        yamlData = yaml.load(response.read())
        if yamlData["release"] == False:
            print("Skipping module")
            del modules[moduleName]
            continue

        print("Done")

    return modules;

def mapKDEProjectsToFedoraPkgs(kdeProjects, product):
    fedoraPkgs = {}
    for projectName in kdeProjects:
        if projectName in _KDEToFedoraNamesMap:
            pkgName = _KDEToFedoraNamesMap[projectName]
        elif product == "frameworks":
            pkgName = "kf5-%s" % projectName
        else:
            pkgName = projectName

        fedoraPkgs[pkgName] = { "name": projectName,
                                "pkgname": pkgName }

    return fedoraPkgs


def clonePackages(fedoraPkgs):
    for pkg in fedoraPkgs:
        if os.path.exists(pkg):
            print("Skipping %s, because it already exists" % pkg)
            continue

        p = subprocess.Popen(['fedpkg', 'clone', pkg])
        p.wait()


def main():
    parser = argparse.ArgumentParser(description = 'Clone all Fedora packages into current directory.')
    parser.add_argument('product',
                        help='Product to clone (frameworks or plasma)')
    args = parser.parse_args()

    metadata = downloadKDEMetaData()
    modules = parseKDEMetaData(metadata, args.product)
    if args.product == 'frameworks':
        # Fetch YAML metadata for each module, skip modules that don't have
        # release flag set
        modules = fetchYamlMetaData(modules)
        modules["extra-cmake-modules"] = { "name": "extra-cmake-modulues",
                                           "pkgname": "extra-cmake-modules"
                                         }
        modules["kf5"] = { "name": "kf5",
                           "pkgname": "kf5"
                         }

    fedoraPkgs = mapKDEProjectsToFedoraPkgs(modules, args.product)
    clonePackages(fedoraPkgs)

if __name__ == "__main__":
    main()
