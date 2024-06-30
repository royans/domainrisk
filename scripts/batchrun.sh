#!/bin/bash

cd ../
ps -aef | grep updatedb | awk '{print $2}' | xargs kill -9


python3 updatedb.py 1 &
python3 updatedb.py 3 &
python3 updatedb.py 5 &
python3 updatedb.py 7 &
python3 updatedb.py 11 &
python3 updatedb.py 13 &
python3 updatedb.py 17 &
python3 updatedb.py 19 &
python3 updatedb.py 23 &
python3 updatedb.py 29 &
python3 updatedb.py 31 &
python3 updatedb.py 37 &
python3 updatedb.py 41 &
python3 updatedb.py 43 &
python3 updatedb.py 47 &
python3 updatedb.py 53 &
python3 updatedb.py 59 &
python3 updatedb.py 61 &
python3 updatedb.py 67 &
python3 updatedb.py 71 &
python3 updatedb.py 73 &
python3 updatedb.py 79 &
python3 updatedb.py 83 &
python3 updatedb.py 89 &
python3 updatedb.py 97 &
