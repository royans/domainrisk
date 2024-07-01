#!/bin/bash

cd ../
ps -aef | grep updatedb | awk '{print $2}' | xargs kill -9

L=`wget -q -O - 'https://toolbox.tharakan.org/up.txt'`
export L

load1m=`echo $L | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`
load5m=`echo $L | cut -d':' -f5 | awk '{print $2}' | cut -d',' -f1`

while awk "BEGIN { exit $load1m > 3 }"
do
	echo $load1m
	if awk "BEGIN { exit $load1m > 1.5 }"
	then
		if awk "BEGIN { exit $load5m > 1.5 }"
		then
      echo "==============  Starting a new thread ============"
			python3 updatedb.py &
		fi
	fi
	sleep 60
	L=`wget -q -O - 'https://toolbox.tharakan.org/up.txt'`
	load1m=`echo $L | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`
	load5m=`echo $L | cut -d':' -f5 | awk '{print $2}' | cut -d',' -f1`
done
