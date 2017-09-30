#!/usr/bin/env bash

cd

RUN=$1

echo "Running a $1 from `pwd` at `date`"

if [ -f .working_lock ]; then
    echo Was working already: `date`
    exit
fi
touch .working_lock

echo Downloading...
dotnet /alpacka-meta/out/alpacka-meta.dll download -o /data --filter None ${RUN}

echo Python magic...
python3 -m CurseMeta all /data /www
python3 CurseMeta/CurseMetaDB/CleanInjest.py /data/addon/ /data/cleaned.json

function json {
    local file=$1
    local out_dir=$2
    local filename=`basename $file`
    cp $file $out_dir/raw_$filename
    gzip < $file > $out_dir/raw_$filename.gz
    bzip2 < $file > $out_dir/raw_$filename.bz2
    xz < $file > $out_dir/raw_$filename.xz
}

for f in /data/*.json; do
    json $f /www
done

rm .working_lock

exit 0
