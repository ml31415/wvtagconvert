wvtagconvert
============

Wikivoyage formatting converter. Converts unformatted or tagged list entries
(Eat / Sleep / Do sections) to vcard or tag format.

* [Vcard specification](http://de.wikivoyage.org/wiki/Vorlage:VCard)
* [Listing tag specification](https://en.wikivoyage.org/wiki/Wikivoyage:Listings)

Description text following a vcard without a description field is treated
as description for that tag, delimited by a newline.

intl-area-code fields in vcards are evaluated, when converting phone and
fax numbers to tags.

url field is prefixed with http://, in case that was missing.

Best effort is made to convert vcard-type fields to an according tag, but
there are surely some more specific cases missing. The tag type is used 
to create a vcard type, though this leads to quite poor generic
results. This could need some more effort for auto detection of common 
cases.


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
