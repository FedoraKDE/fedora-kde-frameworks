/* 
   01-fedora-plasma-nm.js - Add NM plasmoid to the systray
   Copyright (C) 2010 Kevin Kofler <kevin.kofler@chello.at>
   Copyright (C) 2013 Jan Grulich <jgrulich@redhat.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.

   Portions lifted from 06-delete-networkmanagement.js:
   Copyright Jonathan Riddell, jriddell@ubuntu.com 2013-09-13
   may be copied under the GNU GPL 2 or later
*/

nmAppletFound = false
pids = panelIds;
for (i = 0; i < pids.length; ++i) { //search through the panels
  panel = panelById(pids[i]);
  if (!panel) continue;
  ids = panel.widgetIds;
  for (j = 0; j < ids.length; ++j) { //search through the widgets for systray
    widget = panel.widgetById(ids[j]);
    if (!widget || widget.type != "systemtray") {
      continue;
    }
    //widget var is now the systray
    widget.currentConfigGroup = Array("Applets");
    noOfApplets = widget.configGroups.length;
    var groups = new Array();
    for (k = 0; k < noOfApplets; ++k) {
      groups.push(widget.configGroups[k])
    }
    for (k = 0; k < noOfApplets; ++k) {
      widget.currentConfigGroup = new Array("Applets", groups[k]);
      if (widget.readConfig("plugin") == "org.kde.plasma-nm") {
	nmAppletFound = true;
        widget.writeConfig("plugin","org.kde.networkmanagement"); //found it at last
	break;
      } else if (widget.readConfig("plugin") == "org.kde.networkmanagement") {
        nmAppletFound = true;
	break;
      }
    }
  }
}

if (!nmAppletFound) {
  systrayFound = false;
  for (i = 0; i < pids.length; ++i) { //search through the panels
    panel = panelById(pids[i]);
    if (!panel) continue;
    ids = panel.widgetIds;
    for (j = 0; j < ids.length; ++j) { //search through the widgets for systray
      widget = panel.widgetById(ids[j]);
      if (!widget || widget.type != "systemtray") {
	continue;
      }
      systrayFound = true;
      //widget var is now the systray
      widget.currentConfigGroup = Array("Applets");
      noOfApplets = widget.configGroups.length;
      widget.currentConfigGroup = new Array("Applets", noOfApplets + 1);
      widget.writeConfig("plugin", "org.kde.networkmanagement");
      print("Network management plasmoid added to the systray");
      break;
    }
    if (systrayFound) break;
  }
}
