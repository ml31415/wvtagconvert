wvtagconvert
============

Wikivoyage formatting converter. Converts unformatted or tagged list entries
(Eat / Sleep / Do sections) to vcard or tag format. A demo is 
[available here](http://dev.mldesign.net/wvtagconvert/wvtagconvert.py). If 
you notice any parsing errors, please [write me a comment about 
it](https://github.com/ml31415/wvtagconvert/issues/1).

* [Vcard specification](http://de.wikivoyage.org/wiki/Vorlage:VCard)
* [Listing tag specification](https://en.wikivoyage.org/wiki/Wikivoyage:Listings)


Run
===
For local testing: 
```sh
python -m bottle websrv
```
Somewhere remote, either run it as a CGI script or:
```sh
python -m bottle --server gevent -b <external_ipaddress> websrv
```
And then direct your browser to localhost:8080 or &lt;external_ipaddress&gt;:8080


Requirements
============
* Python 2.6+
* [bottle](http://pypi.python.org/pypi/bottle) (for standalone usage only)
* [gevent](http://http://www.gevent.org/) (optional)


Todo
====
- [x] Heuristics for most common cases
- [ ] Automatic currency symbol conversion according to style guides
- [ ] Reading a page directly by specifying URL
