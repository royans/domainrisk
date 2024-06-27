# DomainRisk

**DomainRisk - signals to understand how mature a website may be**

Supply chain attacks are the new normal. Every site which includes scripts/assets from another site compounds the risk because it not only has to secure its own infrastructure, it also has to track and ensure that its suppliers are secure as well. And if its suppliers are using other services (like CDN) even those need to be protected. 

DomainRisk does a simple check - it checks how many unique hostnames are included in the script section of the top level website and counts them out. Most of the very mature sites, which care about security should generally have less than 5 to 6 unique hosts. But unfortunately, some have dozens.

**Usage** : ./batch.sh "list of domain names"
<pre>
./batch.sh google.com facebook.com kark.com fox16.com fox40.com cbs17.com 
Domain UniqueHosts,UniqueDomains,CertExpiry,CertProvider
google.com,0,0,2024/08/26,Google Trust Services
facebook.com,0,0,2024/07/04,DigiCert Inc
kark.com,19,18,2024/07/30,Let's Encrypt
fox16.com,18,17,2024/07/30,Let's Encrypt
fox40.com,18,17,2024/07/30,Let's Encrypt
cbs17.com,17,16,2024/07/30,Let's Encrypt
</pre>

**Usage** : python3 domainrisk.py "domainname.com"
<pre>
$ python3 domainrisk.py fox16.com
Domain UniqueHosts,UniqueDomains,Cert expiry, Cert issuer
fox16.com,18,17,2024/07/30,Let's Encrypt

List of hosts this site connects to using script:
cdn.cookielaw.org
htlbid.com
cdn.bestreviews.com
static.chartbeat.com
segment.psg.nexstardigital.net
cdn.cityspark.com
blue.fox16.com
assets.adobedtm.com
nxst.megpxs.com
get.civicscience.com
imasdk.googleapis.com
cdn.onesignal.com
www.fox16.com
d3plfjw9uod7ab.cloudfront.net
ak.sail-horizon.com
stats.wp.com
3a6b0682-f3e1-4576-a706-5eb4101b9cc3.edge.permutive.app
cdn.confiant-integrations.net
</pre>
