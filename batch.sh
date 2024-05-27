#!/bin/bash

for domain in $@ ; 
do 
	echo -n "$domain :"; 
	python3 domainrisk.py $domain | tee  /tmp/domain_risk.$domain.out | wc -l 
done
