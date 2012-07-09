#!/bin/sh

NV=$(rpm -q --specfile *.spec --qf "%{name}-%{version}")

svn co http://src.chromium.org/chrome/branches/1132_43/src/ $NV/

tar cavf $NV.tar.xz $NV --exclude=.svn
