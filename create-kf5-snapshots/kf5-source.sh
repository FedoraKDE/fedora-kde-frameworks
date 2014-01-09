# siddharths@fedoraproject.org 
#!/bin/bash

cd  ~/kde/src/kf5-snapshots
mv  latest/* archive/
snapshot=$(date +"%m%d%y%H%M%S"); mkdir latest/tarballs-$(date +"%m%d%y%H%M%S")

for pkg in `cat kf5.list`
do

    cd ~/kde/src/frameworks/$pkg
    echo "Creating tarball .::. kf5-$pkg-$snapshot.tar.bz2"

    git pull
    git archive --format=tar master | bzip2 -c > ~/kde/src/kf5-snapshots/latest/tarballs-$snapshot/kf5-$pkg-git$snapshot.tar.bz2

    cd      ~/kde/src/kf5-snapshots/latest/tarballs-$snapshot
    mkdir   kf5-$pkg-git$snapshot
    cd      kf5-$pkg-git$snapshot
    tar xvf ../kf5-$pkg-git$snapshot.tar.bz2 &>/dev/null
    cd      ../ ; tar cjf kf5-$pkg-git$snapshot.tar.bz2 kf5-$pkg-git$snapshot &>/dev/null
    rm -fr  kf5-$pkg-git$snapshot

done

cd  ~/kde/src/kf5-snapshots 

for pkg in `cat kde.list`
do

    cd ~/kde/src/$pkg
    echo "Creating tarball .::. $pkg-$snapshot.tar.bz2"
	
    git pull
    git archive --format=tar master | bzip2 -c > ~/kde/src/kf5-snapshots/latest/tarballs-$snapshot/$pkg-git$snapshot.tar.bz2
    
    cd      ~/kde/src/kf5-snapshots/latest/tarballs-$snapshot
    mkdir   $pkg-git$snapshot
    cd      $pkg-git$snapshot
    tar xvf ../$pkg-git$snapshot.tar.bz2 &>/dev/null
    cd      ../ ; tar cjf $pkg-git$snapshot.tar.bz2 $pkg-git$snapshot &>/dev/null
    rm -fr  $pkg-git$snapshot

done

    cd ~/kde/src/libdbusmenu-qt
    echo "Creating tarball .::. libdbusmenu-qt-$snapshot.tar.bz2"
    bzr up
    bzr export --root=libdbusmenu-qt-git$snapshot ~/kde/src/kf5-snapshots/latest/tarballs-$snapshot/libdbusmenu-qt-git$snapshot.tar.gz
