#!/bin/sh

# Prepare the environment
export KDE5=/opt/kde5
export QTDIR=/usr/lib64
export XDG_DATA_DIRS=$KDE5/share:$XDG_DATA_DIRS:/usr/share
export XDG_CONFIG_DIRS=$KDE5/etc/xdg:$XDG_CONFIG_DIRS:/etc/xdg
export PATH=$KDE5/libexec:$KDE5/bin:$PATH
export LD_LIBRARY_PATH=$KDE5/lib64:$LD_LIBRARY_PATH
# FIXME: $KDE5/lib64 is in QT_PLUGIN_PATH, because plasma-shell is looking for dataengines
# in $QT_PLUGIN_PATH/kf5/plasma/dataengine/ instead of $QT_PLUGIN_PATH/plasma/dataengine
export QT_PLUGIN_PATH=$KDE5/lib64/:$KDE5/lib64/kf5:$KDE5/lib64/plugins:$KDE5/qt5/plugins:$QTDIR/lib64/qt5/plugins:$QT_PLUGIN_PATH
export QML2_IMPORT_PATH=$KDE5/lib64/qml:$QTDIR/qml:$QTDIR/qt5/qml
export KDE_SESSION_VERSION=5
export KDE_FULL_SESSION=true
export XDG_DATA_HOME=$HOME/.local5
export XDG_CONFIG_HOME=$HOME/.config5
export XDG_CACHE_HOME=$HOME/.cache5
export KDEHOME=$HOME/.kde5

# Call the real startkde
/opt/kde5/bin/startkde
