** DomainRisk - signals to understand how mature a website may be **

Supply chain attacks are the new normal. Every site which includes scripts/assets from another site compounds the risk because it not only has to secure its own infrastructure, it also has to track and ensure that its suppliers are secure as well. And if its suppliers are using other services (like CDN) even those need to be protected. 

DomainRisk does a simple check - it checks how many unique hostnames are included in the script section of the top level website and counts them out. Most of the very mature sites, which care about security should generally have less than 5 unique hosts. But unfortunately, some have dozens.

Usage: python3 domainrisk.py "<domainname>"
<pre>
$ python3 domainrisk.py "cnn.com" | wc -l
76
</pre>
