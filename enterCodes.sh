#! /bin/sh

if [ $# != 3 ]; then
    echo "Usage: $0 <codes_caps_file> <codes_cardboard_file> <credentials_file>" 1>&2;
    exit 1;
else
    echo "Congratulations, you won!"
    ./mycoke2.py $1 $2 < $3 1> output 2> errput
fi
