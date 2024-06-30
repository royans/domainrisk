#!/bin/bash

cd ../
ps -aef | grep updatedb | awk '{print $2}' | xargs kill -9

load=`uptime | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`

while awk "BEGIN { exit $load > 0.9 }"
do
	echo $load
	if awk "BEGIN { exit $load > 0.2 }"
	then
		python3 updatedb.py &
	fi
	sleep 60
	load=`uptime | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`
done
