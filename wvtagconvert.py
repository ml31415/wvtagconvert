# -*- coding: utf-8 -*-
'''
Wikivoyage format converter

License: GPLv3

Michael Löffler
'''
import re
from string import Formatter
from bottle import route, run, request, template
from lxml import etree, html


class TolerantFormatter(Formatter):
    """ In case of missing arguments: Ignore them and insert an empty string """
    def get_value(self, key, args, kwargs):
        try:
            return Formatter.get_value(self, key, args, kwargs)
        except KeyError:
            return ''

string_formatter = TolerantFormatter()
html_parser = etree.HTMLParser()


tag_samples = ['<eat name="Al Forno Ristorante" address="Nördliche Ringstraße 37" phone="+49 9141 920420" email="" fax="" url="2" hours="" price="" lat="" long=""></eat>',
'<eat name="Andreas Stuben" address="Rosenstraße 18" phone="+49 9141 8737919" email="" fax="+49 9141 8737920" url="http://www.andreas-stuben.de" hours="" price="" lat="" long=""></eat>',
'<eat name="Antichi Sapori Romani" address="Judengasse 25" phone="+49 9141 9239172" url="http://www.facebook.com/pages/Antichi-Sapori-Romani/417927868249147" hours="" price="" lat="" long=""></eat>',
'<eat name="Bräustüberl Zur Kanne" address="Bachgasse 15" phone="+49 9141 3844" email="" url="http://schneider-bier.de/gaststaetten_02_kanne.php" hours="Tu-So 10.30–14.00 and 17.30–24.00" price="">Original interior nearly untouched since 1890.</eat>',
'<eat name="Hotel Restaurant Goldener Adler" address="Marktplatz 5" phone="+49 9141 85560" email="" fax="+49 9141 855633" url="http://www.hotel-goldener-adler.de" hours="" price="" lat="" long=""></eat>',
'<eat name="Hotel Restaurant Schwarzer Bär" address="Marktplatz 13" phone="+49 9141 92426" email="" fax="+49 9141 92443" url="http://www.derschwarzebaer.de" hours="" price="" lat="" long=""></eat>',
'<eat name="Löwengarten Restaurant" address="Westliche Ringstr. 36" phone="+49 9141 8731963">Greek and German food.</eat>',
'<eat name="Mai Thai" address="Bismarckanlage 16" phone="+49 9141 995759" email="" fax="" url=""></eat>',
'<eat name="Steakhaus El Toro" address="Obertorstr. 5" phone="+49 9141 922730"></eat>',
'<eat name="Silbermühle - vino y tapa Restaurant" address="Silbermühle 4" phone="+49 9141 9744001" email="silbermuehle@web.de" fax="" url="http://www.die-silbermuehle.de" hours="" price="" lat="" long=""></eat>',
]

vcard_samples = [
'{{vCard|type=Restaurant|name=Bräustüberl “Zur Kanne”|address=Bachgasse 15, 91781 Weißenburg|phone= +49 (0)9141/3844|email=|fax=|url=http://schneider-bier.de/gaststaetten_02_kanne.php|hours=Dienstag bis Sonntag von 10.30 – 14.00 und 17.30 – 24.00, Montag Ruhetag |price=|lat=|long=}}, dieser Gasthof könnte auch unter Sehenswürdigkeiten stehen, der Gastraum ist im Wesentlichem im Zustand von 1890.',
'{{vCard|type=Restaurant|name=Antichi Sapori Romani|address=Judengasse 25, 91781 Weißenburg|phone= +49 (0)9141/9239172|email=|fax=|url=http://www.facebook.com/pages/Antichi-Sapori-Romani/417927868249147|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Mai Thai|address=Bismarckanlage 16, 91781 Weißenburg|phone= +49 (0)9141/995759|email=|fax=|url=|hours=|price=|lat=|long=}},',
'{{vCard|type=Restaurant|name=Löwengarten Griechisches Restaurant|address=Westliche Ringstr. 36, 91781 Weißenburg|phone= +49 (0)9141/8731963|email=|fax=|url=|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Steakhaus El Toro|address=Obertorstr. 5, 91781 Weißenburg|phone= +49 (0)9141/922730|email=|fax=|url=|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Silbermühle - vino y tapa Restaurant|address=Silbermühle 4, 91781 Weißenburg|phone= +49 (0)9141/9744001|email=silbermuehle@web.de|fax=|url=http://www.die-silbermuehle.de|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Al Forno Ristorante|address=Nördliche Ringstraße 37, 91781 Weißenburg|phone= +49 (0)9141/920420|email=|fax=|url=|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Hotel Restaurant Schwarzer Bär|address=Marktplatz 13, 91781 Weißenburg|phone= +49 (0)9141/92426|email=|fax= +49 (0)9141/92443|url=http://www.derschwarzebaer.de|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Hotel Restaurant Goldener Adler|address=Marktplatz 5, 91781 Weißenburg|phone= +49 (0)9141/85560|email=|fax= +49 (0)9141/855633|url=http://www.hotel-goldener-adler.de|hours=|price=|lat=|long=}}',
'{{vCard|type=Restaurant|name=Andreas Stuben|address=Rosenstraße 18, 91781 Weißenburg|phone= +49 (0)9141/8737919|email=|fax= +49 (0)9141/8737920|url=http://www.andreas-stuben.de|hours=|price=|lat=|long=}}',
'{{VCard | type= hostel | subtype= budget | name= Jugendgästehaus Haus International München | comment= keine Altersbeschränkung, kein Jugendherbergsausweis nötig | url= http://www.haus-international.de/ | address= Elisabethstr. 87, 80797 München | directions= MVV: Tram Linie 12 "Barbarastraße" | intl-area-code= +49 | phone= (0)89 / 12 00 6-0 | fax= (0)89 / 12 00 6-630 | price= EZ 49,00 €; DZ D/WC 39,00 € }}',
'{{VCard | type= restaurant | name= Nabucco Ristorante | comment= "feiner" aber noch bezahlbarer Italiener | url= http://www.nabucco.de/ | address= Erich-Kästner-Straße 21, 80796 München | directions= Schwabing West, Nähe Hohenzollernplatz; MVV: U2 | intl-area-code= +49 | phone= (0)89 / 30 00 22 33 | mobile= (0)89 / 30 00 22 34 | hours= So., Die. bis Fr. 12 bis 15 und 18 bis 01 Uhr, Sa. 18 bis 01 Uhr }}. MVV: U2, Hohenzollernplatz',
'{{VCard | type= restaurant | name= OHAYOU | comment= Sushi Restaurant, traditionelles japanisches Restaurant | url= http://www.ohayou.de/ | address= Belgradstr. 71, 80804 München | directions= "Ecke" Karl-Theodor-Str. | lat= 48.16726 | long= 11.57360 | phone= 089 / 32667604 | hours= Di. - Sa. 11.30 - 14.30, 17.30 - 23.00 Uhr; So. 17.00 - 22.00 Uhr}}. MVV: U3, Scheidplatz und Bonner Platz.',
]


vcard_tag_type_translation = {
    'hostel': 'sleep',
    'hotel': 'sleep',
    'guest house': 'sleep',
    'shop': 'buy',
    'gallery': 'buy',
    'bar': 'drink',
    'cafe': 'drink',
    'restaurant and bar': 'eat',
    'restaurant': 'eat',
    'museum': 'see',
    'library': 'see',
    'swimming pool': 'do',
    'theater': 'do',
    'cinema': 'do',
    'festival': 'do',
}

tag_vcard_type_translation = dict(eat='restaurant', drink='bar', buy='shop', do='activity', see='sight')
tag_search = r'(<(%s).+>.*</\2>)' % '|'.join(sorted(tag_vcard_type_translation.keys()))

tag_template = '<{type} name="{name}" address="{address}" phone="{phone}" email="{email}" fax="{fax}" url="{url}" hours="{hours}" price="{price}" lat="{lat}" long="{long}">{description}</{type}>'
vcard_fields = ("type subtype name alt comment address directions intl-area-code phone mobile "
               "fax fax-mobile email email2 email3 url facebook google twitter skype hours "
               "checkin checkout price credit-cards lat long description").split()

def read_vcard(vcard_str):
    vcard_str, description = unicode(vcard_str).split('}}', 1)
    pts = [pt.split('=') for pt in vcard_str.strip('{},. ').split('|')[1:]]
    d = dict((p[0].strip().lower(), p[1].strip()) for p in pts)
    description = description.lstrip('., ').strip()
    if description:
        d['description'] = description[0].capitalize() + description[1:]
    return d

def read_tag(tag_str):
    t = html.fromstring(unicode(tag_str), parser=html_parser)
    d = dict(t.items())
    d['type'] = t.tag
    d['description'] = t.text.lstrip('., ').strip() if t.text else ''
    return d
    
def make_vcard(d):
    d = d.copy()
    d['type'] = tag_vcard_type_translation.get(d['type'].lower(), d['type'])
    content = []
    for key in vcard_fields:
        if key in d and d[key]:
            content.append("%s=%s" % (key, d[key]))
    return '{{vCard| %s}}' % '| '.join(content)

def make_tag(d):
    d = d.copy()
    type_lower = d['type'].lower()
    if type_lower not in tag_vcard_type_translation:
        d['type'] = vcard_tag_type_translation.get(type_lower, 'listing')
    phone_prefix = d.get('intl-area-code')
    if phone_prefix:
        for item in ('phone', 'mobile', 'fax', 'fax-mobile'):
            if item in d:
                d[item] = phone_prefix + d[item].lstrip('0')
    return string_formatter.format(tag_template, **d)

def parse_input(input_str):
    vlst = re.findall(r'{{vcard\s*\|.+}}.*$', input_str, flags=re.MULTILINE|re.IGNORECASE)
    vlst = [read_vcard(l) for l in vlst]
    
    tlst = re.findall(tag_search, input_str, flags=re.MULTILINE|re.IGNORECASE)
    tlst = [read_tag(l[0]) for l in tlst]
    return [make_tag(l) for l in vlst] + [make_vcard(l) for l in tlst]


html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<title>Wikivoyage Vcard-Tag Converter</title>
</head>
<body>
<div id="main">
    <h1>Wikivoyage Vcard-Tag Converter</h1>
    <div>
        <p>Enter text to parse and convert formatting from <a href="http://de.wikivoyage.org/wiki/Vorlage:VCard">vCard</a>
             to <a href="https://en.wikivoyage.org/wiki/Wikivoyage:Listings">listing tag</a> or vice versa</p>
        <form action="/" id="converter" method="post">
            <textarea name="convertinput" rows="10" cols="150">{default_input}</textarea>
            <br />
            <button type="submit" name="button" title="Submit">Submit</button>
        </form>
    </div>
    
    {output_template}
</div>
</body>
</html>
"""

div_output = """<div id="output">
    <h3>Parsed output</h3>
    <textarea rows="10" cols="150">{output}</textarea>
</div>
"""


@route('/', method=['GET', 'POST'])
def serve():
    input = request.forms.get('convertinput', '')
    output = '\n\n* '.join(parse_input(input)) if input else None
    output = div_output.format(output='* ' + output) if output else ''
    return string_formatter.format(html_template, output_template=output, default_input=input)

def debug_main():
    teststr = '\n* '.join(tag_samples) + '\n' + '\n* '.join(vcard_samples)
    res = parse_input(teststr)
    for l in res:
        print l


if __name__ == '__main__':
    #debug_main()  
    run(reloader=True, host='localhost', port=8080)
