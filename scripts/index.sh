#!/bin/sh -e
# index.sh: Android SDK indexer
# Copyright (C) 2013 Takahiro Yoshimura <altakey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
if test -z "$1" || test -z "$2"; then
  echo "usage: $0 <root> <target>"
  exit 1
fi

wc=`pwd`
root=$1
target="android-$2"
alvitr_root=`perl -e "use File::Basename (dirname); use Cwd 'realpath'; print dirname(realpath('$0'))"`

echo 'Loading docs:'
(cd $root && find docs -type f -name '*.html' | python $alvitr_root/load.py -d docs) | psql
echo 'Loading examples:'
(cd $root && find samples/$target -type f | python $alvitr_root/load.py -v examples) | psql
echo 'Loading sources:'
(cd $root && find sources/$target -type f | python $alvitr_root/load.py -v sources) | psql
echo 'Fixing up'
cat $alvitr_root/create.sql | psql
