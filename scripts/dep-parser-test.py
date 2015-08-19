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

from inspect import currentframe, getframeinfo

from DependencyScanner import *


def COMPARE(act, exp):
    cf = currentframe()
    line = cf.f_back.f_lineno

    if act != exp:
        print("FAIL: '%s' != '%s' (line %d)" % (act, exp, line))
    else:
        print("PASS: '%s' == '%s' (line %d)" % (act, exp, line))


def main():
    dep = Dependency("kf5-ki18n-devel")
    COMPARE(dep.name(), "kf5-ki18n-devel")
    COMPARE(dep.version(), None)
    COMPARE(dep.isKF5(), True)

    dep = Dependency("kf5-ki18n-devel >= 5.13.0")
    COMPARE(dep.name(), "kf5-ki18n-devel")
    COMPARE(dep.version(), "5.13.0")
    COMPARE(dep.versionCond(), ">=")
    COMPARE(dep.isKF5(), True)

    dep = Dependency("kf5-ki18n-devel >= %{_kf5_version}")
    COMPARE(dep.name(), "kf5-ki18n-devel")
    COMPARE(dep.version(), "%{_kf5_version}")
    COMPARE(dep.versionCond(), ">=")
    COMPARE(dep.isKF5(), True)


if __name__ == "__main__":
    main()
