wvtagconvert
============

Wikivoyage formatting converter. Converts unformatted or tagged list entries
(Do / Eat / Drink / Sleep sections) to vcard or tag format by using a bunch of
heuristics. A sample installation for testing is [available here][1]. If you 
notice any parsing errors, please [write me a comment about it][2].

* [Vcard specification][3]
* [Listing tag specification][4]


Run
---
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
------------
* [Python][5] 2.6+
* [bottle][6] (for standalone usage only)
* [gevent][7] (optional)


Todo
----
- Usability improvements
- Reading a page directly by specifying URL
- Automatic currency symbol conversion according to style guides


License
-------
[GPLv3][8]

 [1]: http://dev.mldesign.net/wvtagconvert/wvtagconvert.py "Sample installation"
 [2]: https://github.com/ml31415/wvtagconvert/issues/1 "Parsing issue tracker"
 [3]: http://de.wikivoyage.org/wiki/Vorlage:VCard "VCard specification"
 [4]: https://en.wikivoyage.org/wiki/Wikivoyage:Listings "Listing tag specification"
 [5]: http://www.python.org/ "Python programming language"
 [6]: http://pypi.python.org/pypi/bottle "bottle Python package"
 [7]: http://http://www.gevent.org/ "gevent Python package"
 [8]: http://www.gnu.de/documents/gpl.en.html "GNU General Public License"
