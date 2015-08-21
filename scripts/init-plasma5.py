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

_IgnoredKDEProjects = [
    "user-manager",
    "kde-gtk-config",
    "muon"
]        

_KDEToFedoraNamesMap = {
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
    "bluez-qt": "kf5-bluez-qt"
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

    projects = []
    for project in workspaceModule.iterfind("project"):
        projectName = project.get("identifier")
        if projectName in _IgnoredKDEProjects:
            print("\tIgnoring kde/workspace/%s" % projectName, flush = True)
            continue

        print("\tFound project kde/workspace/%s" % projectName, flush = True)
        projects.append(projectName)
            
    print("Done", flush = True)
    return projects

def mapKDEProjectsToFedoraPkgs(kdeProjects):
    fedoraPkgs = []
    for kdeProject in kdeProjects:
        if kdeProject in _KDEToFedoraNamesMap:
            pkgName = _KDEToFedoraNamesMap[kdeProject]
        else:
            pkgName = kdeProject
            
        fedoraPkgs.append(pkgName)
    
    return fedoraPkgs

def clonePackages(fedoraPkgs):
    for pkg in fedoraPkgs:
        if os.path.exists(pkg):
            print("Skipping %s, because it already exists" % pkg)
            continue

        p = subprocess.Popen(['fedpkg', 'clone', pkg])
        p.wait()

def main():
    metadata = downloadKDEMetaData()
    kdeProjects = parseKDEMetaData(metadata)
    fedoraPkgs = mapKDEProjectsToFedoraPkgs(kdeProjects)
    clonePackages(fedoraPkgs)

if __name__ == "__main__":
    main()
