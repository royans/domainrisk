#!/bin/bash

echo "Domain UniqueHosts,UniqueDomains,CertExpiry,CertProvider"
if [ -f $1 ]
then
	for host in `cat $1`
	do
		timeout 14 python3 domainrisk.py $host 2> /dev/null | grep -v Error| grep -v UniqueHost | tee  /tmp/domain_risk.$host.out  | grep \,
	done
else

for domain in $@ ; 
do 
	timeout 14 python3 domainrisk.py $domain 2> /dev/null | grep -v Error | grep -v UniqueHost | tee  /tmp/domain_risk.$domain.out  | grep \,
done

fi
