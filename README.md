# DomainRisk

**DomainRisk - signals to understand how mature a website may be**

Supply chain attacks are the new normal. Every site which includes scripts/assets from another site compounds the risk because it not only has to secure its own infrastructure, it also has to track and ensure that its suppliers are secure as well. And if its suppliers are using other services (like CDN) even those need to be protected. 

DomainRisk does a simple check - it checks how many unique hostnames are included in the script section of the top level website and counts them out. Most of the very mature sites, which care about security should generally have less than 5 to 6 unique hosts. But unfortunately, some have dozens.

**Usage** : python3 domainrisk.py "domainname.com"
<pre>
$ python3 domainrisk.py "cnn.com" | wc -l
76

$ python3 domainrisk.py "slashdot.org" | wc -l
6

$ python3 domainrisk.py "facebook.com" | wc -l
2

$ python3 domainrisk.py "google.com" | wc -l
4

$ python3 domainrisk.py "cnn.com" 
registry.api.cnn.io
politics.api.cnn.io
www.dianomi.com
prod.pdx.api.cnn.io
bea4.v.fwmrm.net
fave-api.cnn.com
wopr.turnerapps.com
www.wbdprivacy.com
www.facebook.com
npms.io
tvem.cdn.turner.com
www.datadoghq-browser-agent.com
wbd-api.arkoselabs.com
ads.pubmatic.com
cdnjs.cloudflare.com
z.cdp-dev.cnn.com
i.cdn.turner.com
www.datad0g-browser-agent.com
pixel-us-east.rubiconproject.com
s.ntv.io
data.api.cnn.io
prod.di.api.cnn.io
www.pledge.to
get.s-onetag.com
api.business.cnn.io
amp.cnn.com
static.chartbeat.com
content.api.cnn.com
search.prod.di.api.cnn.io
lightning.cnn.com
turnip.cdn.turner.com
tag.bounceexchange.com
eq97f.publishers.tremorhub.com
aswpsdkus.com
cdn.cookielaw.org
audience.cnn.com
status.arkoselabs.com
politics-static.cnn.io
www.youtube.com
daltonmt1.qa.identityservices.io
www.instagram.com
dam2.cms.cnn.com
money.cnn.com
ite.api.tvemanager.ngtv.io
audience.qa.cnn.com
arkose.daex.qa.identityservices.io
a.jsrdn.com
twitter.com
ib.adnxs.com
d2otbl5v981rj6.cloudfront.net
production.dataviz.cnn.io
idsync.rlcdn.com
cdn.optimizely.com
agility.cnn.com
assets.publicgood.com
sync.search.spotxchange.com
schema.org
www.w3.org
git.io
live.rezync.com
daltonmt1.identityservices.io
launcher.spot.im
arkose.daex.identityservices.io
www.cnn.com
dynaimage.cdn.turner.com
media.cnn.com
cdn.cnn.com
markets.money.cnn.com
axios-http.com
atlas.cnn.io
sse01.cnn.com
handlebarsjs.com
fave.api.cnn.io
accounts.google.com
bvrmvkrkie.execute-api.us-east-1.amazonaws.com
github.com  
</pre>
