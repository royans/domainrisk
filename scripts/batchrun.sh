#!/bin/bash

cd ../
ps -aef | grep updatedb | awk '{print $2}' | xargs kill -9

load1m=`uptime | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`
load5m=`uptime | cut -d':' -f5 | awk '{print $2}' | cut -d',' -f1`

while awk "BEGIN { exit $load1m > 1.5 }"
do
	echo $load1m
	if awk "BEGIN { exit $load1m > 1.0 }"
	then
		if awk "BEGIN { exit $load5m > 1.5 }"
		then
      echo "Starting a new thread"
			python3 updatedb.py &
		fi
	fi
	sleep 15
	load1m=`uptime | cut -d':' -f5 | awk '{print $1}' | cut -d',' -f1`
	load5m=`uptime | cut -d':' -f5 | awk '{print $2}' | cut -d',' -f1`
done
