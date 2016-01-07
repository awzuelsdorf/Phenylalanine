#! /bin/sh

if [ $# != 2 ]; then
    echo "Usage: $0 <codes_caps_file> <codes_cardboard_file>" 1>&2;
    exit 1;
else
    ./mycoke2.py $1 $2 output errput
    doneTime=`date`
    echo "Finished at $doneTime"
fi
