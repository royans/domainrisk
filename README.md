# DomainRisk

**DomainRisk - signals to understand how mature a website may be**

Supply chain attacks are the new normal. Every site which includes scripts/assets from another site compounds the risk because it not only has to secure its own infrastructure, it also has to track and ensure that its suppliers are secure as well. And if its suppliers are using other services (like CDN) even those need to be protected. 

DomainRisk does a simple check - it checks how many unique hostnames are included in the script section of the top level website and counts them out. Most of the very mature sites, which care about security should generally have less than 5 to 6 unique hosts. But unfortunately, some have dozens.

**Usage** : ./batch.sh "list of domain names"
<pre>
./batch.sh google.com facebook.com slashdot.org techmeme.com cnn.com bedbathandbeyond.com xda-developers.com mlb.com
Domain UniqueHosts,UniqueDomains
google.com 4,2
facebook.com 2,2
slashdot.org 6,4
techmeme.com 2,2
cnn.com 76,44
bedbathandbeyond.com 26,18
xda-developers.com 14,10
mlb.com 60,37
</pre>

**Usage** : python3 domainrisk.py "domainname.com"
<pre>
$ python3 domainrisk.py "cnn.com" 
Domain Namne - Unique hosts - Unique domains
cnn.com 76,44
arkoselabs.com
ntv.io
optimizely.com
publicgood.com
youtube.com
turnerapps.com
axios-http.com
s-onetag.com
ngtv.io
pledge.to
rezync.com
google.com
identityservices.io
amazonaws.com
dianomi.com
twitter.com
adnxs.com
aswpsdkus.com
handlebarsjs.com
rubiconproject.com
turner.com
cookielaw.org
spot.im
datadoghq-browser-agent.com
cnn.com
cloudfront.net
facebook.com
github.com
tremorhub.com
spotxchange.com
npms.io
schema.org
datad0g-browser-agent.com
cnn.io
chartbeat.com
jsrdn.com
bounceexchange.com
rlcdn.com
git.io
fwmrm.net
pubmatic.com
wbdprivacy.com
w3.org
instagram.com
</pre>
