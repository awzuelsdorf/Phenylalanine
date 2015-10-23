#! /bin/sh

if [ $# != 2 ]; then
    echo "Usage: $0 <codes_file> <credentials_file>" 1>&2;
    exit 1;
else
    echo "Congratulations, you won!"
    ./mycoke2.py $1 < $2 1> output 2> errput
fi
