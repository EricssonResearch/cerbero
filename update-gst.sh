#! /bin/bash
for i in gstreamer gst-plugins-{base,good,bad,ugly}; do
    echo $i;
    master_commit=`git ls-remote git://anongit.freedesktop.org/git/gstreamer/$i | grep "master$" | awk '{print $1}'`
    echo $master_commit
    for j in -1.0{,-static}; do
        sed -E -i .bak "s/([ ]+commit = )'[0-9a-z]+'/\1'$master_commit'/" recipes/$i$j.recipe;
    done
done
