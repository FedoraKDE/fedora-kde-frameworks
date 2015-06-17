#!/bin/sh
OPENGL_VERSION=`LANG=C glxinfo | grep '^OpenGL version string: ' | sed -e 's/^OpenGL version string: \([0-9]\).*$/\1/g'`
if [ "$OPENGL_VERSION" -lt 2 ]; then
  QT_XCB_FORCE_SOFTWARE_OPENGL=1
  export QT_XCB_FORCE_SOFTWARE_OPENGL
fi
