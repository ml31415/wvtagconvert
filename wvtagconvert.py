# -*- coding: utf-8 -*-
'''
Wikivoyage format converter

License: GPLv3

Michael Loeffler
'''
from __future__ import division

import re
import string
from collections import defaultdict
from lxml import etree, html


class TolerantFormatter(string.Formatter):
    """ In case of missing arguments: Ignore them and insert an empty string """
    def get_value(self, key, args, kwargs):
        try:
            return string.Formatter.get_value(self, key, args, kwargs)
        except KeyError:
            return ''

string_formatter = TolerantFormatter()
html_parser = etree.HTMLParser()

def squeeze(s):
    return re.sub(r'\s+', ' ', s.strip())

def find_any(haystack, *needles):
    for needle in needles:
        if needle in haystack:
            return True
    return False

singular_exceptions = set(('goods', 'tapas', 'jeans', 'smoothies', 'trousers', 'pants'))
def singular(w):
    if w.endswith('ies'):
        return w[-3] + 'y'
    elif w.endswith('s') and not w.endswith('ss') and w not in singular_exceptions:
        if w[:-3] == 'hes':
            return w[:-2]
        else:
            return w[:-1]
    else:
        return w


tag_vcard_type_translation = dict(eat='restaurant', drink='bar', buy='shop', do='activity', see='sight', sleep="hotel")
tag_template = '<{type} name="{name}" address="{address}" phone="{phone}" email="{email}" fax="{fax}" url="{url}" hours="{hours}" price="{price}" lat="{lat}" long="{long}">{description}</{type}>'
tag_search = r'(<(%s).+>.*?</\2>)' % '|'.join(sorted(tag_vcard_type_translation.keys()))

vcard_search = r'{{vcard\s*\|.+}}.*$'
vcard_fields = ("type subtype name alt comment address directions intl-area-code phone mobile "
               "fax fax-mobile email email2 email3 url facebook google twitter skype hours "
               "checkin checkout price credit-cards lat long description").split()
vcard_number_fields = 'phone', 'mobile', 'fax', 'fax-mobile'


# Max 3 spaces in beginning, bold written name, 3-40 chars, comma or dot delimited
untagged_search = r"""^\*:*?\s{0,3}'''.{3,40}'''[,. ].{20,2000}\."""
untagged_buzzwords = dict(
    sleep = ['room', 'lodge', 'lodging', 'aircon', 'a/c',
             'tv', 'wifi', 'shower', 'breakfast', 'clean',
             'laundry', 'balcony', 'window', 'baggage', 'cable',
             'bed', 'fan', 'fridge', 'bathroom', 'lobby',
             'accomodate', 'guest', 'price'],
    hotel = ['hotel', 'hyatt', 'novotel', 'sofitel', 'hilton',
             'sheraton', 'kingsize', 'airport pickup', 'minibar',
             'jacuzzi', 'spa', 'safe', 'plaza', 'private safe',
             'square', 'star', 'sauna', 
             'residence', 'resort', 'buffet', 'fitness room', 
             'suite', 'reservation', 'exclusive', 'elegant'],
    hostel = ['hostel', 'dorm', 'dormitory', 'backpacker', 'shared'],
    guesthouse = ['guesthouse', 'guest house', 'house', 'homely'],
    
    restaurant = ['restaurant', 'eat', 'food', 'kitchen', 'cuisine',  
            'breakfast', 'wine', 'culinary', 'noodle', 'meal', 
            'kebab', 'soup', 'egg', 'buffet',
            'vegetarian', 'beef', 'chicken', 'pork', 'portion',
            'salad', 'fruit', 'lunch', 'dinner', 'dish', 'chef',
            'tapas', 'dining', 'halal',
            'dumpling', 'duck', 'specialities', 'wifi'],
    fastfood = ['fastfood', 'burger', 'hot dog', 'french fries',
                'chicken wings', 'kfc', 'mcdonalds', 'sandwich',
                'baguette', 'bistro'],
    seafood = ['seafood', 'fish', 'crab', 'oyster'],
    asian = ['asian', 'curry', 'suckling pig', 'vietnamese', 
             'chinese', 'spring roll', 'rice', 'spicy',
             'thai', 'pho', 'filipino'],
    italian = ['italian', 'pizza', 'pasta', 'spaghetti',
               'bolognese', 'fettuccine', 'risotto'],
    
    cafe = ['cafe', u'café', 'coffee', 'drink', 'latte', 'tea', 'ice cream', 
            'juice', 'bistro', 'smoothies', 'yoghurt', 'ca phe', 'waffle', 
            'egg', 'pancake', 'cappuccino', 'donut'],
    bar = ['bar', 'drink', 'beer', 'draft', 'music', 'live', 
           'crowd', 'brewery', 'billiard', 'pool', 
           'late', 'evening', 'rooftop', 'pub', 'quiz', 'guitar',
           'band', 'girl', 'jazz', 'smokey', 'dart', 'tv', 'sport'],
    nightclub = ['club', 'drink', 'cocktail', 'wine', 'lounge', 'music', 'dj', 
                 'disco', 'discotheque', 'crowd', 'late', 'floor', 
                 'night', 'girl', 'couch', 'jazz', 'open air',
                 'meat market'],
    
    see = ['museum', 'library', 'exhibition', 'collection'],
    religious = ['pagoda', 'cathedral', 'church', 'mosque', 'dome',
                 'temple', 'old', 'goddess', 'holy', 'saint', 'monk',
                 'nun', 'pray', 'spirit', 'meditation', 'diocese',
                 'worship', 'god', 'buddhist', 'buddha', 'budhism', 
                 'allah', 'moslem', 'muslim', 'islam', 'islamic', 'order',
                 'shrine'],
    art = ['art', 'gallery', 'paint', 'oil', 'statue', 'wood',
           'decor', 'contemporary'],
    nature = ['park', 'garden', 'green', 'walk', 'forrest', 'tree',
              'lake', 'beach', 'nature', 'untouched', 'view',
              'national park', 'fountain', 'waterfall'],
    historical = ['historical', 'history',
           'palace', 'war', 'tour', 'hall', 'monument', 'tower',
           'emperor', 'king', 'queen', 'prince', 'castle', 'fortress',
           'dynasty', 'epoche', 'century', 'ancient', 'baroque',
           'structure', 'building', 'court', 'government',
           'reconstructed', 'neoclassical', 'president',
           'residence', 'settlement', 'wall', 'ruin',
           'freedom', 'forces', 'honour', 'struggled',
           'fought', 'country', 'official', 'republic',
           'independence', 'occupation', 'occupied',
           'headquarter', 'first lady'],
                          
    buy = ['buy', 'cheap', 'shop', 'market', 'goods', 'item', 
           'money', 'price', 'save', 'bargain', 'bargaining'
           'cash', 'haggle', 'haggling', 'sell', 'store',
           'shopping', 'expensive', 'overpriced'],
    cloth = ['cloth', 'jeans', 'shirt', 'wear', 'accessory',
             'dress', 'hats', 'leather', 'suit', 'coat', 'tailor',
             'wardrobe', 'trousers', 'pants', 'jacket', 'polyester',
             'wool', 'cotton', 'silk', 'tie', 'belt'],
    books = ['paper', 'book', 'magazin', 'journal', 'print', 
             'newspaper'],
    touristy = ['souvenir', 'watch', 'jewelry', 'present', 'dvd',
                'kitsch', 'antiquity', 'exotic'],
                          
    do = ['guide', 'kid', 'event', 'swimming pool'],
    outdoor = ['outdoor', 'dive', 'diving', 'snorkel', 'hike', 'hiking', 'bike', 
          'biking', 'fishing', 'swim', 'go', 'ride',
          'adventure', 'tour'],
    indoor = ['cinema', 'cineplex', 'badminton', 'aerobic',
          'cooking', 'concert', 'theater', 'dolphinarium', 
          'festival', 'opera', 'zoo'],
    learn = ['learn', 'university', 'teach', 'student', 'language', 
             'cooking'],
                          
)
untagged_buzzwords = dict((key, set(val)) for key, val in untagged_buzzwords.iteritems())
untagged_buzzword_filter = set(string.ascii_letters + u" /éäöüß")

# First: common items, second: Items in subclasses
untagged_categories = dict(
    sleep = ['sleep', ['hotel', 'guesthouse', 'hostel']],
    eat = ['restaurant', ['seafood', 'asian', 'fastfood', 'italian']],
    drink = [None, ['cafe', 'bar', 'nightclub']],
    see = ['see', ['religious', 'historical', 'nature', 'art']],
    buy = ['buy', ['cloth', 'books', 'touristy', 'art']],
    do = ['do', ['outdoor', 'indoor', 'learn']],
)
untagged_category_sets = dict()
untagged_subcategories = dict()
for key, val in untagged_categories.items():
    untagged_subcategories[key] = dict((k, untagged_buzzwords[k]) for k in val[1])
    untagged_category_sets[key] = set.union(untagged_buzzwords[val[0]] if val[0] else set(), 
                                   *untagged_subcategories[key].values())

untagged_split_categories = dict(
    address = set(['avenue', 'ave', 'building', 'bldg', 'boulevar', 'blvd',
                   'drive', 'dr', 'expressway', 'expy', 'freeway', 'fwy',
                   'highway', 'hwy', 'lane', 'ln', 'parkway', 'pkwy',
                   'place', 'pl', 'road', 'rd', 'street', 'st',
                   'jalan', 'jl', 'soi', 'thanon', 'th', # Indonesia, Thailand
                   ]),
    directions = set(['intersection', 'corner', 'opposite', 'nearby',
                  'near', 'inside', 'behind', 'left', 'right', 'bus',
                  'train', 'station', 'taxi', 'stop', 'next', 'at']),
    alt = set(['a.k.a', 'aka', 'also known']),
    phone = set(['tel', 'nr', 'phone', 'number', u'☎'])
)
#for key, val in untagged_sets.items():
#    print key, val

def determine_category(word_list, category_dict, wc_offset=10, full_list=False):
    # Give it an offset, so that words in the end are
    # not totally meaningless, maybe needs some more
    # calibration
    wc = len(word_list) + wc_offset
    scores = defaultdict(float)
    for category in category_dict.keys():
        for cnt, word in enumerate(word_list):
            if word in category_dict[category]:
                # Rate words by their position in the
                # string, the later, the less important
                scores[category] += (wc - cnt) / wc
    # Sort by score, highest first
    results = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    if full_list:
        return results
    try:
        return results[0][0]
    except IndexError:
        return

def determine_tagtype(untagged_str):
    """ Rate the whole string, if it fits into some category. 
        Count occurences of topic related words.
        Prefer word hits closer to the beginning of the string.
    """
    utl = untagged_str.lower()
    utl = ''.join(c for c in utl if c in untagged_buzzword_filter)
    utl_splt = utl.split()
    category = determine_category(utl_splt, untagged_category_sets) or 'listing'
    if untagged_subcategories[category] and category != 'listing':
        subcategory = determine_category(utl_splt, untagged_subcategories[category])
    else:
        subcategory = None
    return category, subcategory


abbreviations = 'ave bldg blvd dr expy fwy hwy ln pkwy pl rd st jl th tel nr no'.split()
phone_splitter = set(['tel', 'nr', 'no', 'phone', 'number', 'fax', 'e-mail', 'email', u'☎'])
def parse_phonefax(s, verbose=False):
    """ Split something like 'phone 2343434 Fax +343434 tel 3000777' """
    pts = re.split(r'(%s)' % '|'.join(phone_splitter), s, flags=re.IGNORECASE)
    parsed_pts = []
    for pt in pts:
        pt = pt.strip()
        if not pt:
            continue
        elif parsed_pts and parsed_pts[-1].lower() in phone_splitter:
            if pt.lower() not in phone_splitter:
                parsed_pts[-1] += ' ' + pt
        else:
            parsed_pts.append(pt)
    if len(parsed_pts) == 1 and not find_any(parsed_pts[0].lower(), *phone_splitter):
        return [pt.strip() for pt in parsed_pts[0].rsplit(',', 1)]
    return parsed_pts
    
abbreviations_filter = r'\s(\w|%s)\.' % '|'.join(abbreviations)
closing_delimiter = {'(': ')', '[': ']'}
def chunkify(s, verbose=False):
    """ Split the string into meaningful chunks determined by
        syntactical parts found inside the string.
    """
    s = s.lstrip('* ')
    # Remove irrelevant dots, which disturb parsing
    s = re.sub(r'\.\s*,', ',', s)
    s = re.sub(r'\.\s*:', '', s)
    s = re.sub(abbreviations_filter, r' \1', s, flags=re.IGNORECASE)
    if s.startswith("'''"):
        # We know, that fat is only a relevant block if it is
        # used right in the beginning, so exclude this from
        # the loop
        val = re.findall(r"""'''(.*?)'''""", s, flags=re.IGNORECASE)[0]
        s = s[len(val) + 6:].lstrip(',. ')
        chunks = [val]
    else:
        chunks = []

    while s:
        s = s.lstrip(',. -')
        # Dot and bracket only if not followed by digit or not part of
        # an email ending
        m = re.search(r'(\.[\sA-Z]|\.[a-z]{5,10}|\(\s{0,2}\D|\[)', s)
        split_pos = m.start() if m else None
        if split_pos is None:
            s = s.strip()
            subchunks = [s] if s else []
            s = '' # We're done, so end the loop afterwards
        else:
            delimiter = s[split_pos]
            if delimiter == '.':
                subchunk1 = s[:split_pos].rstrip(', -')
                subchunks = [subchunk1] if subchunk1 else []
                s = s[split_pos+1:]
            else:
                subchunk1 = s[:split_pos].rstrip(', -')
                subchunk2, s = s[split_pos+1:].split(closing_delimiter[delimiter], 1)
                subchunk2 = subchunk2
                if subchunk1:
                    subchunks = [subchunk1, subchunk2]
                else:
                    subchunks = [subchunk2]

        # Do we need to break down it further?
        if subchunks and len(subchunks[0]) > 25:
            if subchunks[0].count(',') > 1:
                subchunks = subchunks[0].rsplit(',', 1) + subchunks[1:]
            elif sum(1 for c in subchunks[0] if c in '123456789') > 6:
                # No zeros, to avoid mistakes with money statements
                subchunks = parse_phonefax(subchunks[0]) + subchunks[1:]
                        
        chunks += subchunks
    return chunks
        
    
def classify_chunk(chunk, position=None):
#        if '.' in untagged_str:
#            data, description = untagged_str.split('.', 1)
#        else:
#            data, description = untagged_str, ''
#        if not '.' in data and not ',' in data and not '(' in data and len(data) < 50:
#            address = data
#            direction = ''
#            data = ''
#        else:
#            if '(' in data and ')' in data:
#                add_dir, data = data.split(')', 1)
#                address, direction = add_dir.split('(', 1)
#                diretion = direction.strip("',. ")
#                address = address.strip("',. ")
#            else:
#                pass
#        print ';'.join((name, address, direction, data, description))

    d = dict()
    return d

def read_untagged(untagged_str):
    """ Determine type of tag by counting buzz words. Separate string into chunks and analyze
        the chunks separately. Determine the type (name, address, direction, description)
        of the chunk by counting characteristics (http found, mailto found, type of encapsulation, ...).
        
    """
    tag_type = determine_tagtype(untagged_str)
    chunks = chunkify(untagged_str)
    cl = len(chunks) + 3 # Offset
    positions = [(cl - i)  /  cl for i in xrange(len(chunks))]
    chunk_types = map(classify_chunk, chunks, positions)
    # TODO: Merge all identified parts grouped by their chunk_type in order
    d = dict()
    d['type'] = tag_type
    return d
    
def read_vcard(vcard_str):
    vcard_str, description = unicode(vcard_str).split('}}', 1)
    pts = [pt.split('=') for pt in vcard_str.strip('{},. ').split('|')[1:]]
    d = dict((p[0].strip().lower(), p[1].strip()) for p in pts)
    if 'description' not in d and description:
        d['description'] = description
    return sanitize(d)

def read_tag(tag_str):
    t = html.fromstring(unicode(tag_str), parser=html_parser)
    d = dict(t.items())
    d['type'] = t.tag
    if t.text:
        d['description'] = t.text
    return sanitize(d)
    
def sanitize(d):
    """ Fix usual listing errors """
    d = dict((squeeze(key), squeeze(val)) for key, val in d.iteritems())
    description = d.get('description', '').lstrip(""";., """)
    if description:
        d['description'] = description[0].upper() + description[1:]
    else:
        d.pop('description', None)
    for number_item in vcard_number_fields:
        number = d.get(number_item, '').lstrip(';., ').strip()
        if number:
            if not number.startswith('('):
                # Remove (0) things including the 0 inside strings
                number = re.sub(r'\(\s*0\s*\)', ' ', number)
            number = re.sub(r'[()/.,\\-]', ' ', number)
            number = squeeze(number)
            # Avoid single leading zeros
            if number[0] == '0' and number[1] == ' ':
                number = '0' + number[2:]
            d[number_item] = number
        else:
            d.pop(number_item, None)
    url = d.get('url', '')
    if url and not url.startswith('http://') and not '//' in url:
        url = 'http://' + url
        d['url'] = url
    price = d.get('price', '')
    if price:
        d['price'] = price[0].upper() + price[1:].rstrip('., ')
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
        d['type'] = determine_tagtype(type_lower)[0]
    phone_prefix = d.get('intl-area-code')
    if phone_prefix:
        phone_prefix += ' '
        for item in vcard_number_fields:
            if item in d and not d[item].startswith(('+', '00')):
                d[item] = phone_prefix + d[item].lstrip('0')
    return string_formatter.format(tag_template, **d)

def parse_input(input_str, format):
    found = []
    for line in input_str.split('\n*'):
        lst = re.findall(vcard_search, line, flags=re.MULTILINE|re.IGNORECASE)
        found += [read_vcard(l) for l in lst]
        lst = re.findall(tag_search, line, flags=re.DOTALL|re.IGNORECASE)
        found += [read_tag(l[0]) for l in lst]
        lst = re.findall(untagged_search, line, flags=re.IGNORECASE)
        found += [read_untagged(l) for l in lst]
    
    if format == 'tag':
        return [make_tag(l) for l in found]
    elif format == 'vcard':
        return [make_vcard(l) for l in found]
    else:
        raise ValueError('Invalid output format: %s' % format)

