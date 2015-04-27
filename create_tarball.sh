#! /bin/sh

if [ $# -eq 0 -o $# -gt 1 ]; then
    echo "$0: Creates a tarball of cerbero and cerbero/sources/local"
    echo "Usage:"
    echo "$0 <output-filename>"
    echo "This results in <output-filename>.tar.bz2"
    exit 0
fi

FILENAME=$1
git archive -v --format=tar --prefix=$FILENAME/cerbero/ HEAD > $FILENAME.tar && \
    tar rvf $FILENAME.tar -s ",^sources,$FILENAME/cerbero/sources," sources/local/ && \
    bzip2 $FILENAME.tar
