#!/bin/bash

echo "Domain <unique hosts>, <unique domains>"
if [ -f $1 ]
then
	for host in `cat $1`
	do
		timeout 14 python3 domainrisk.py $host 2> /dev/null | grep -v Error | tee  /tmp/domain_risk.$host.out  | grep \,
	done
else

for domain in $@ ; 
do 
	timeout 14 python3 domainrisk.py $domain 2> /dev/null | grep -v Error | tee  /tmp/domain_risk.$domain.out  | grep \,
done

fi
