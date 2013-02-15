wvtagconvert
============

Wikivoyage formatting converter. Converts unformatted or tagged list entries
(Eat / Sleep / Do sections) to vcard or tag format. A demo is available at

http://dev.mldesign.net/wvtagconvert/wvtagconvert.py

* [Vcard specification](http://de.wikivoyage.org/wiki/Vorlage:VCard)
* [Listing tag specification](https://en.wikivoyage.org/wiki/Wikivoyage:Listings)


Run
===
For local testing: 

    python -m bottle websrv
   
Somewhere remote, either run it as a CGI script or:

    python -m bottle --server gevent -b <external_ipaddress> websrv

And then direct your browser to localhost:8080 or <external_ipaddress>:8080


Requirements
============
* Python 2.6+
* bottle package (for standalone usage only)
* gevent (optional)


Todo
====
* Automatic currency symbol conversion according to style guides
