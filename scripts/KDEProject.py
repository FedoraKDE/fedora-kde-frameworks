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

import xml.etree.ElementTree as ET
import glob
import urllib3
import datetime
import time
import os

class ParsingException(Exception):
    pass

class KDEProject(object):
    _identifer = None
    _name = None
    _path = None
    _gitweb = None

    def __init__(self, xmlElement):
        #if xmlElement:
        self._identifer = xmlElement.get('identifier')
        name = xmlElement.find('name')
        if name != None:
            self._name = name.text
        path = xmlElement.find('path')
        if path != None:
            self._path = path.text
        gitweb = xmlElement.find('web[@type=\'gitweb\']')
        if gitweb != None:
            self._gitweb = gitweb.text

    def __repr__(self):
        return 'KDEProject(path=\'%s\')' % self._path

    def identifier(self):
        return self._identifer

    def name(self):
        return self._name

    def path(self):
        return self._path

    def gitweb(self):
        return self._gitweb


class KDEProjectXMLParser:

    _xmlMetaData = None

    def __init__(self):
        caches = glob.glob('kde_projects.xml.[0-9]*');
        if not caches:
            if not self._download():
                print('Error: failed to retrieve kde_projects.xml')
                return
        else:
            caches = sorted(caches)
            if not self._loadFromCache(caches[len(caches) - 1]):
                print('Error: failed to retrieve kde_project.xml')
                return

    def listFrameworks(self):
        return self.getKDEProjects('component[@identifier=\'frameworks\']/module')

    def listWorkspace(self):
        return self.getKDEProjects('component[@identifier=\'kde\']/module[@identifier=\'workspace\']/project')

    def listApplications(self):
        return self.getKDEProjects('component[@identifier=\'kde\']/module[@identifier=\'applications\']/project')

    def getKDEProjects(self, xPathFilter):
        root = ET.fromstring(self._xmlMetaData)
        if not root.tag == 'kdeprojects':
            raise ParsingException('Invalid XML: unexpected root element')

        projectListXML = root.findall(xPathFilter)
        kdeProjects = []
        for projectXML in projectListXML:
            kdeProjects.append(KDEProject(projectXML))

        return kdeProjects

    def _parseLastModifiedTS(self, header):
        return int(datetime.datetime.strptime(header, '%a, %d %b %Y %H:%M:%S %Z') \
                                    .replace(tzinfo = datetime.timezone.utc) \
                                    .timestamp())

    def _loadFromCache(self, cacheFile):
        timestamp = int(cacheFile.rsplit('.', 1)[1])

        pool = urllib3.PoolManager()
        # FIXME: use https
        try:
            response = pool.request('HEAD', 'http://projects.kde.org/kde_projects.xml')
        except urllib3.exceptions.RequestError as e:
            print('Error retrieving kde_projects.xml: %s' % e.message)
            return False

        if 'Last-Modified' in response.headers:
            lastModifiedTS = self._parseLastModifiedTS(response.headers['Last-Modified'])
            if lastModifiedTS > timestamp:
                return self._download()
            else:
                f = open(cacheFile, 'r')
                self._xmlMetaData = f.read()
                f.close()
                return True
        else:
            return self._download()



    def _download(self):
        pool = urllib3.PoolManager()
        # FIXME: use HTTPS
        try:
            response = pool.request('GET', 'http://projects.kde.org/kde_projects.xml')
        except urllib3.exceptions.RequestError as e:
            print('Error retrieving kde_project.xml: %s' % e.message)
            return False

        self._xmlMetaData = response.data

        # remove old cached files
        for cached in glob.glob('kde_projects.xml.[0-9]*'):
            os.remove(cached)

        if 'Last-Modified' in response.headers:
            lastModifiedTS = self._parseLastModifiedTS(response.headers['Last-Modified'])
            try:
                cacheFile = open('kde_projects.xml.%d' % lastModifiedTS, 'w')
                cacheFile.write(self._xmlMetaData.decode('utf-8'))
                cacheFile.close()
            except Exception:
                print('Warning: failed to store kde_projects.xml to a cache file')

        return True
