#!/bin/sh

VERSION="5.2.0"
KFVERSION="5.6.0"
RELEASE="1"
CHANGELOG="Plasma ${VERSION}"
AUTHOR="Daniel Vrátil <dvratil@redhat.com>"
DIST="fc21"

#REMOVE_DGROC_CHANGELOG="TRUE"

URL="http://pub.progdan.cz/pub/plasma/srpm/$VERSION"


dt=`date +'%a %b %d %Y'`

for pkg in `/usr/bin/ls -1 plasma-5`; do
  if [ "$pkg" == "kf5-baloo" ] || [ "$pkg" == "kf5-kfilemetadata" ]; then
    ver="$KFVERSION"
  else
    ver="$VERSION"
  fi


  sed -i 's/^Version:        [0-9\.]*$/Version:        '"$ver"'/' plasma-5/$pkg/$pkg.spec
  sed -i 's/^Release:        [0-9a-z\.]*/Release:        '"$RELEASE"'/' plasma-5/$pkg/$pkg.spec
#  sed -i 's/^Source0:        http:\/\/download.kde.org\/unstable\//Source0:        http:\/\/download.kde.org\/stable\//' plasma-5/$pkg/$pkg.spec
  sed -i 's/^\%changelog/\%changelog\n\* '"$dt"' '"$AUTHOR"' - '"$VERSION"'-'"$RELEASE"'\n- '"$CHANGELOG"'\n/' plasma-5/$pkg/$pkg.spec

  # This beast matches changelog lines generated by dgroc-kf5 and removes them
  if [ -n "$REMOVE_DGROC_CHANGELOG" ]; then
      sed  ':a;N;$!ba;s/\* \(Mon\|Tue\|Wed\|Thu\|Fri\|Sat\|Sun\) \(Jan\|Feb\|Mar\|Apr\|May\|Jun\|Jul\|Aug\|Sep\|Oct\|Nov\|Dec\) [0-9]* [0-9]* dvratil <dvratil@redhat.com> - \([0-9a-z\.-]*\)\n- [a-zA-Z0-9\:\ ]*\n\n//g'
  fi

  rpmbuild -bs plasma-5/$pkg/$pkg.spec
  scp $HOME/rpmbuild/SRPMS/$pkg-$ver-$RELEASE.$DIST.src.rpm dvratil@progdan.cz:~/pub/plasma/srpm/${VERSION}
done


for pkg in `/usr/bin/ls -1 plasma-5`; do
  if [ "$pkg" == "kf5-baloo" ] || [ "$pkg" == "kf5-kfilemetadata" ]; then
    ver="$KFVERSION"
  else
    ver="$VERSION"
  fi
  echo "http://pub.dvratil.cz/plasma/srpm/${VERSION}/${pkg}-${ver}-$RELEASE.${DIST}.src.rpm"
done
