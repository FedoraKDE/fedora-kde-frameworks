#!/bin/sh

for tier in tier1 tier2 tier3 tier4; do
        frameworks=`ls ${tier}`
        for fw in ${frameworks}; do
                rpmbuild -bs ${tier}/${fw}
        done
done
