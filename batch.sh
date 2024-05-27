#!/bin/bash

if [ -f $1 ]
then
	for host in `cat $1`
	do
		echo -n "$host :"; 
		python3 domainrisk.py $host 2> /dev/null | grep -v Error | tee  /tmp/domain_risk.$host.out | wc -l 
	done
else

for domain in $@ ; 
do 
	echo -n "$domain :"; 
	python3 domainrisk.py $domain 2> /dev/null | grep -v Error | tee  /tmp/domain_risk.$domain.out | wc -l 
done

fi
