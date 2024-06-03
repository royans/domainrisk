#!/bin/bash

echo "The 10M pagerank data (top10milliondomains.csv) is from domcop: https://www.domcop.com/openpagerank/what-is-openpagerank"
rm -f top10milliondomains.csv.zip 
wget https://www.domcop.com/files/top/top10milliondomains.csv.zip
unzip top10milliondomains.csv.zip 
python3 domains_load.py
