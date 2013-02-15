#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Wikivoyage format converter

License: GPLv3

Michael Loeffler
'''
import re
import string
import sys
import json
import os
import operator
from itertools import groupby
from xml.etree import ElementTree

import heuristics
from utils import TolerantFormatter, squeeze, fake_agent_readurl, html_encode, html_decode
from page import create_page


class Wikiparser(object):
    """ Fixes parsed information """
    item_lookup = {'phone': 'numbers', 
                   'mobile': 'numbers', 
                   'fax': 'numbers', 
                   'fax-mobile': 'numbers'}

    @classmethod
    def description(cls, description):
        description = description.lstrip(""";., """)
        if description:
            description = description[0].upper() + description[1:]
            for err_str in ("'''", "''"):
                if description.count(err_str) == 1:
                    description = description.replace(err_str, '')
            if description[-1] not in '.!?':
                description += '.'
        return description

    @classmethod    
    def directions(cls, directions):
        return directions.replace("'", '').strip()
    
    @classmethod
    def numbers(cls, number):
        number = number.lstrip(';., ')
        if '+' in number:
            number = '+' + number.split('+', 1)[1]
        elif not number.startswith(tuple('+(0123456789'.split())):
            number = number.lstrip((string.ascii_letters + ' :/'))
        if number:
            if not number.startswith('('):
                # Remove (0) things including the 0 inside strings
                number = re.sub(r'\(\s*0\s*\)', ' ', number)
            number = re.sub(r'[()/.\\-]', ' ', number)
            number = squeeze(number)
            # Avoid single leading zeros
            if number[0] == '0' and number[1] == ' ':
                number = '0' + number[2:]
            number = number.replace("'", '')
        return number
    
    @classmethod
    def url(cls, url):
        if url.startswith('['):
            # Remove wiki syntax and trailing link text
            url = url.strip('[] ')
            if ' ' in url:
                url = url.split(' ', 1)[0]
        if not url.startswith('http://') and not '//' in url:
            url = 'http://' + url
        return url
            
    @classmethod
    def email(cls, email):
        if ':' in email:
            # Remove mailto: and email: things
            email = email.split(':', 1)[1].strip()
        return email.split(' ')[0].replace("'", '')
    
    @classmethod
    def price(cls, price):
        return price[0].upper() + price[1:].rstrip('., ')

    @classmethod
    def default(cls, val):
        return val

    @classmethod
    def sanitize_item(cls, key, val):
        key = squeeze(key)
        val = squeeze(val)
        if val:
            func_name = cls.item_lookup.get(key, key)
            if func_name.startswith('sanitize'):
                func_name = 'default'
            val = getattr(cls, func_name, cls.default)(val)
        return key, val

    @classmethod
    def sanitize(cls, d):
        return dict(cls.sanitize_item(key, val) for key, val in d.iteritems())


class Untagged(Wikiparser):
    # Search criteria: Max 3 spaces in beginning, bold written name, 3-40 chars, comma or dot delimited
    search = r"""^(?:\*[:*]*\s{0,3})?'''.{3,40}'''[,. ].{20,2000}"""
    unique_items = set(['name', 'address', 'phone', 'fax', 'email', 'url'])
    
    @classmethod
    def read(cls, untagged_str):
        """ Determine type of tag by counting buzz words. Separate string into chunks and analyze
            the chunks separately. Determine the type (name, address, direction, description)
            of the chunk by counting characteristics (http found, mailto found, type of 
            encapsulation, ...).
        """
        tag_type = heuristics.determine_tagtype(untagged_str)
        chunks = heuristics.chunkify(untagged_str)
        chunk_types = map(heuristics.classify_chunk, chunks, range(len(chunks)))
        # Group all identified parts
        d = dict((k, (g.next()[1] if k in cls.unique_items else 
                      heuristics.merge_chunks(list(i[1] for i in g), untagged_str)))  
                 for k, g in groupby(sorted(zip(chunk_types, chunks), 
                                key=operator.itemgetter(0)), key=operator.itemgetter(0)))
        d['type'] = tag_type[0]
        d['subtype'] = tag_type[1]
        return cls.sanitize(d)
    
    @classmethod
    def parse(cls, line):
        lst = re.findall(cls.search, line, flags=re.MULTILINE)
        return [cls.read(l) for l in lst]
    

class Vcard(Wikiparser):
    search = r'{{vcard\s*\|.+}}.*$'
    fields = ("type subtype name alt comment address directions intl-area-code phone mobile "
               "fax fax-mobile email email2 email3 url facebook google twitter skype hours "
               "checkin checkout price credit-cards lat long description").split()
    number_fields = 'phone', 'mobile', 'fax', 'fax-mobile'
    tagtype_translation = dict(eat='restaurant', drink='bar', buy='shop', do='activity', see='sight', sleep="hotel")

    @classmethod
    def read(cls, vcard_str):
        vcard_str, description = vcard_str.split('}}', 1)
        pts = [pt.split('=') for pt in vcard_str.strip('{},. ').split('|')[1:]]
        d = dict((p[0].strip().lower(), p[1]) for p in pts)
        description = d.setdefault('description', description)
        if not d.get('subtype') and description:
            d['subtype'] = heuristics.determine_tagtype(d.get('name', '') + ' ' + description)[1]
        return cls.sanitize(d)

    @classmethod
    def tostring(cls, d):
        d = d.copy()
        d['type'] = cls.tagtype_translation.get(d['type'].lower(), d['type'])
        if d['type'] == d.get('subtype'):
            d.pop('subtype', None)
        content = []
        for key in cls.fields:
            content.append("%s=%s" % (key, d.get(key, '')))
        return '{{vCard| %s}}' % '| '.join(content)

    @classmethod
    def parse(cls, line):
        lst = re.findall(Vcard.search, line, flags=re.MULTILINE|re.IGNORECASE)
        return [cls.read(l) for l in lst]


class Tag(Wikiparser):
    fields = 'eat', 'drink', 'buy', 'do', 'see', 'sleep', 'tollfree'
    search = r'(<(%s).+>.*?</\2>)' % '|'.join(sorted(fields))
    template = ('<{type} name="{name}" address="{address}" phone="{phone}" email="{email}" '
                'fax="{fax}" url="{url}" hours="{hours}" price="{price}" tollfree="{tollfree}" '
                'lat="{lat}" long="{long}">{description}</{type}>')
    xml_header = u'<?xml version="1.0" encoding="UTF-8" ?>\n'
    formatter = TolerantFormatter()
    
    @classmethod
    def read(cls, tag_str):
        tag_str = tag_str.lstrip('*: ')
        if sys.version_info[:2] < (2, 7):
            tag_str =  cls.xml_header + tag_str
            t = ElementTree.fromstring(tag_str.encode('utf8'))
        else:
            t = ElementTree.fromstring(tag_str)
        d = dict(t.items())
        d['type'] = t.tag
        if t.text:
            d['description'] = t.text
            d['subtype'] = heuristics.determine_tagtype(d['name'] + ' ' + d['description'])[1]
        return cls.sanitize(d)
    
    @classmethod
    def tostring(cls, d):
        d = d.copy()
        type_lower = d['type'].lower()
        if type_lower not in cls.fields:
            d['type'] = heuristics.determine_tagtype(type_lower)[0]
        phone_prefix = d.get('intl-area-code')
        if phone_prefix:
            phone_prefix += ' '
            for item in Vcard.number_fields:
                if item in d and d[item] and not d[item].startswith(('+', '00')):
                    d[item] = phone_prefix + d[item].lstrip('0')
        return cls.formatter.format(cls.template, **d)

    @classmethod
    def parse(cls, line):
        lst = re.findall(cls.search, line, flags=re.DOTALL|re.IGNORECASE)
        return [cls.read(l[0]) for l in lst]
    

def parse_wikicode(input_str, outputformat='vcard'):
    input_str = html_decode(input_str)
    found = []
    for line in input_str.split('\n*'):
        line = '*' + line
        for cls in [Tag, Vcard, Untagged]:
            try:
                found += cls.parse(line)
            except ValueError:
                pass
    
    if outputformat == 'raw':
        return found
    elif outputformat == 'json':
        return [json.dumps(l) for l in found]
    elif outputformat == 'tag':
        return [Tag.tostring(l) for l in found]
    elif outputformat == 'vcard':
        return [Vcard.tostring(l) for l in found]
    else:
        raise ValueError('Invalid output outputformat: %s' % outputformat)
    

def get_from_link(input_str):
    input_str = input_str.strip()
    if (input_str.count('\n') <= 1 and input_str.startswith('http://') and 
            'action=edit' in input_str and 'wikivoyage' in input_str):
        input_str = fake_agent_readurl(input_str).decode('utf8')
        try:
            t = ElementTree.fromstring(input_str)
        except Exception:
            try:
                input_str = re.findall(r'<textarea [^>]*id="wpTextbox1".*?>(.*?)</textarea>', input_str, flags=re.DOTALL)[0]
            except IndexError:
                raise ValueError('No textarea found in the linked page')
        else:
            try:
                input_str = t.xpath("//textarea[@id='wpTextbox1']").text
            except Exception:
                raise ValueError("No wiki edit field found in the linked page")
        return html_decode(input_str)
    return input_str


def create_html(input_str, outputformat='vcard', script_path='/'):
    outputformat = outputformat.lower()
    input_str = input_str.decode('utf8')
    try:
        input_str = get_from_link(input_str)
    except ValueError as e:
        output = str(e)
    else:
        output = parse_wikicode(input_str, outputformat)

    if not input_str:
        output = None
    elif outputformat in ('vcard', 'tag'):
        output = u'* ' + u'\n\n* '.join(output)
    elif outputformat == 'json':
        output = u'[%s]' % u',\n'.join(output)
    else:
        output = u'No entries found.'
    return create_page(html_encode(input_str), output, outputformat, 
                       script_path=script_path).encode('utf8')


def cgi_serve_page():
    import cgi
    import cgitb

    cgitb.enable()
    form = cgi.FieldStorage()
    outputformat = form.getfirst('outputformat', 'vcard')
    input_str = form.getfirst('convertinput', '')
    page = create_html(input_str, outputformat, script_path=os.path.basename(__file__).rstrip('c'))
    header =  "Content-Type: text/html; charset=utf-8\nContent-Length: %s\n\n" % len(page)
    sys.stdout.write(header)
    sys.stdout.write(page)
    sys.stdout.flush()


if __name__ == '__main__':
    cgi_serve_page()
