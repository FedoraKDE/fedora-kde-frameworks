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
import yaml
import os.path
import subprocess

_KDEToFedoraNamesMap = {
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

def parseKDEMetaData(metadata):
    print("Parsing KDE projects metadata...", flush = True)
    root = ET.fromstring(metadata)
    if not root.tag == "kdeprojects":
        raise ParsingException("Invalid XML: unexpected root element")

    frameworksComponent = None
    for component in root.iterfind("component"):
        if component.get("identifier") == "frameworks":
            frameworksComponent = component
            break
    if not frameworksComponent:
        raise ParsingException("Invalid XML: could not find Frameworks component")


    modules = {}
    for module in frameworksComponent.iterfind("module"):
        name = module.get("identifier")
        repo = module.find("repo")
        if not repo:
            raise ParsingException("Invalid XML: could not find repo information for module %s" % name)

        gitweb = None
        for web in repo.iterfind("web"):
            if web.get("type") == "gitweb":
                gitweb = web.text
                break
        if not gitweb:
            raise ParsingException("Invalid XML: could not find gitweb information about module %s" % name)

        modules[name] = { "name": name,
                          "gitweb": gitweb
                        }
        print("\tFound module frameworks/%s" % name)

    print("Done")
    return modules

def mapKDEModuleNameToFedoraPkg(moduleName):
    if moduleName in _KDEToFedoraNamesMap:
        return _KDEToFedoraNamesMap[moduleName]

    return "kf5-%s" % moduleName

def fetchYamlMetaData(modules):
    for moduleName in modules:
        print("Retrieving YAML metadata for %s..." % moduleName, end = '', flush = True)
        response = urllib.urlopen("http://gitweb.kde.org/%s.git?a=blob&o=plain&f=metainfo.yaml" % moduleName)
        yamlData = yaml.load(response.read())
        if yamlData["release"] == False:
            print("Skipping module")
            del modules[moduleName]
            continue

        modules[moduleName]["pkgname"] = mapKDEModuleNameToFedoraPkg(moduleName)
        print("Done")

    return modules;

def cloneModules(modules):
    for moduleName in modules:
        module = modules[moduleName]
        if os.path.exists(module["pkgname"]):
            print("Skipping %s, because it already exists" % module["pkgname"])
            continue

        p = subprocess.Popen([ "fedpkg", "clone", module["pkgname"] ])
        p.wait()

def main():
    metadata = downloadKDEMetaData()
    modules = parseKDEMetaData(metadata)

    # Fetch YAML metadata for each module, skip modules that don't have
    # release flag set
    modules = fetchYamlMetaData(modules)

    modules["extra-cmake-modules"] = { "name": "extra-cmake-modulues",
                                       "pkgname": "extra-cmake-modules"
                                     }
    modules["kf5"] = { "name": "kf5",
                       "pkgname": "kf5"
                     }

    cloneModules(modules)

if __name__ == "__main__":
        main();
