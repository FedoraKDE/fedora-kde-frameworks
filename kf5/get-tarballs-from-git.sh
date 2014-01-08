#!/bin/sh

version="5.0.0"
snapshot="20140108"
destdir=`rpm --eval="%_sourcedir"`

frameworks=`grep -v '^#' < frameworks.list`

for fw in $frameworks; do
        if [ -z "${fw}" ]; then
                continue;
        fi

        echo "Downloading ${fw}"
        git archive --format=tar \
                    --prefix=kf5-${fw}-${version}/ \
                    --remote=git://anongit.kde.org/${fw}.git master \
        | gzip -c > ${destdir}/kf5-${fw}-${snapshot}.tar.gz
done
