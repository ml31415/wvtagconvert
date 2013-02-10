wvtagconvert
============

Wikivoyage formatting converter. Converts list entries from tag listing 
format used in English wikivoyage to vcard format used in German version.

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

* Vcard specification: http://de.wikivoyage.org/wiki/Vorlage:VCard
* Listing tag specification: https://en.wikivoyage.org/wiki/Wikivoyage:Listings

Todo
====
* Automatic currency symbol conversion according to style guides
