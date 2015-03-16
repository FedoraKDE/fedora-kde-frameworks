#!/bin/sh

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

# TODO: Make this a smarter python script


if [ "$#" -eq 1 ]; then
        target=$1;
        if [ "$target" == "f23" ]; then
            branch="master";
        else
            branch="$target"
            target="$target-kde"
        fi
        echo "Building for target $target from branch $branch";
else
        echo "Please specify a valid target (f20, f21, rawhide, ...)"
        exit 1;
fi

echo "Target: $target";

pushd tier1
tier1=`echo *`
popd

pushd tier2
tier2=`echo *`
popd

#
# WARNING: This is rather fragile and might break when deps change.
# TODO: Write a script with automatic deps analysis (maybe joined with cmake-to-rpm-deps?
#
tier3="kf5-kjs : \
kf5-kconfigwidgets kf5-kservice kf5-kjsembed kf5-kpackage : \
kf5-kiconthemes kf5-kdesu kf5-kemoticons : \
kf5-knotifications kf5-ktextwidgets kf5-kglobalaccel : \
kf5-kxmlgui kf5-kwallet : \
kf5-kbookmarks kf5-kcmutils : \
kf5-kio : \
kf5-kxmlrpcclient kf5-kpeople kf5-kdeclarative kf5-kparts kf5-kinit kf5-knotifyconfig kf5-knewstuff : \
kf5-kactivities : \
kf5-ktexteditor kf5-kdewebkit kf5-kded kf5-kross kf5-kmediaplayer kf5-plasma : \
kf5-kdesignerplugin kf5-krunner"

# Tier4 is not listing kf5-khtml, because that's the last pkg that we will call fedpkg
# from, so it will be automatically appended to the chain
tier4="kf5-frameworkintegration kf5-kapidox kf5-kdelibs4support"

pushd tier4/kf5-khtml
git checkout $branch
#fedpkg chain-build --target $target kf5 extra-cmake-modules : $tier1 : $tier2 : $tier3 : $tier4
fedpkg chain-build --target $target $tier3 : $tier4
popd
