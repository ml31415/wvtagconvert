# -*- coding: utf-8 -*-
'''
Created on 14.02.2013

@author: nimrod
'''
from __future__ import division

import sys
import re
import string
from datetime import datetime
from collections import defaultdict

from utils import find_any


__all__ = ['determine_tagtype', 'chunkify', 'classify_chunk', 'merge_chunks']


buzzwords = dict(
    sleep = ['room', 'lodge', 'lodging', 'aircon', 'a/c',
             'tv', 'wifi', 'shower', 'breakfast', 'clean',
             'laundry', 'balcony', 'window', 'baggage', 'cable',
             'bed', 'fan', 'fridge', 'bathroom', 'lobby',
             'accomodate', 'guest', 'price', 'accomodate',
             'smell', 'cleaned', 'staff', 'service'],
    hotel = ['hotel', 'hyatt', 'novotel', 'sofitel', 'hilton',
             'sheraton', 'kingsize', 'airport pickup', 'minibar',
             'jacuzzi', 'spa', 'safe', 'plaza', 'private safe',
             'square', 'star', 'sauna', 'taxi',
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
buzzwords = dict((key, set(val)) for key, val in buzzwords.iteritems())
buzzword_filter = set(string.ascii_letters + u" /éäöüß")

# First: common items, second: Items in subclasses
categories = dict(
    sleep = ['sleep', ['hotel', 'guesthouse', 'hostel']],
    eat = ['restaurant', ['seafood', 'asian', 'fastfood', 'italian']],
    drink = [None, ['cafe', 'bar', 'nightclub']],
    see = ['see', ['religious', 'historical', 'nature', 'art']],
    buy = ['buy', ['cloth', 'books', 'touristy', 'art']],
    do = ['do', ['outdoor', 'indoor', 'learn']],
)
category_sets = dict()
subcategories = dict()
for key, val in categories.items():
    subcategories[key] = dict((k, buzzwords[k]) for k in val[1])
    category_sets[key] = set.union(buzzwords[val[0]] if val[0] else set(), 
                                   *subcategories[key].values())

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
    utl = ''.join(c if c in buzzword_filter else ' ' for c in utl)
    utl_splt = utl.split()
    category = determine_category(utl_splt, category_sets) or 'listing'
    if subcategories[category] and category != 'listing':
        subcategory = determine_category(utl_splt, subcategories[category])
    else:
        subcategory = None
    return category, subcategory


phone_splitter = set(['tel', 'nr', 'no', 'phone', 'number', 'fax', 'e-mail', 'email', u'☎'])
phone_splitter_26 = phone_splitter | set([x.capitalize() for x in phone_splitter] + ['E-Mail'])
def parse_phonefax(s, verbose=False):
    """ Split strings like 'phone 2343434 Fax +343434 tel 3000777', 
        which don't have any helping punctuation.
    """
    if sys.version_info[:2] < (2, 7):
        pts = re.split(r'(%s)' % '|'.join(phone_splitter_26), s)
    else:
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
    
    
abbreviations = 'ave bldg blvd dr expy fwy hwy ln pkwy pl rd st jl th tel nr no'.split()
abbreviations_26 = [abbr.capitalize() for abbr in abbreviations]
abbreviations_filter_base = r'\s(\w|%s)\.'
abbreviations_filter = abbreviations_filter_base % '|'.join(abbreviations)
abbreviations_filter_26 = abbreviations_filter_base % '|'.join(abbreviations + abbreviations_26)
closing_delimiter = {'(': ')', '[': ']'}
def chunkify(s, verbose=False):
    """ Split the string into meaningful chunks determined by
        syntactical parts found inside the string.
    """
    s = s.lstrip('* ')
    # Remove irrelevant dots, which disturb parsing
    s = re.sub(r'\.\s*,', ',', s)
    s = re.sub(r'\.\s*:', '', s)
    
    if sys.version_info[:2] < (2, 7):
        s = re.sub(abbreviations_filter_26, r' \1', s)
    else:
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
        
chunk_type_categories = dict(
    address = set(['avenue', 'ave', 'building', 'bldg', 'boulevard', 'blvd',
                   'drive', 'dr', 'expressway', 'expy', 'freeway', 'fwy',
                   'highway', 'hwy', 'lane', 'ln', 'parkway', 'pkwy',
                   'place', 'pl', 'road', 'rd', 'street', 'st',
                   'jalan', 'jl', 'soi', 'thanon', 'th', # Indonesia, Thailand
                   ]),
    directions = set(['intersection', 'corner', 'opposite', 'nearby',
                  'near', 'inside', 'behind', 'left', 'right', 'bus',
                  'train', 'station', 'taxi', 'stop', 'next', 'at',
                  'between']),
    alt = set(['aka', 'also', 'known', 'former']),
    phone = set(['tel', 'nr', 'phone', 'number', u'☎']),
    email = set(['email', 'e-mail', 'mail', 'mailto']),
    hours = set(['hours', 'day', 'from', 'to', 'open', 'until', 'daily', 'm', 'tu', 'w', 'th', 'f', 'sa', 'su',
                 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
                 '24', 'late', 'noon', 'midnight']),
    fax = set(['fax', 'number']),
    price = set(['rates', 'start', 'only', 'cheap', 'from', 'to', 'euro'])
)

chunk_type_categories_partly = dict(
    url = set(['http://', 'www.', '.com', '.org', '.net', '.htm', '.php']),
    alt = set(["'''"]),
    phone = set(['+']),
    fax = set(['+']),
    email = set(['@', '.com', '.org', '.net']),
    hours = set(['AM', 'PM']),
    price = set(['$', 'USD', 'dollar', u'€', 'EUR',
                 u'¥', 'JPY', u'£', 'GBP', 
                 u'¥', 'RMB', 'yuan', u'₹', 'INR', 'rupees'
                 u'₱', 'PHP', 'pesos', u'₪', 'NIS', 'shekels',
                 u'₩', 'KRW', u'฿', 'baht',
                 'RM',' MYR', 'ringgit', 'Rp', 'IDR', 'rupiah',
                 'rubles', 'dong', 'DKK', 'NOK', 'SEK'])
)

chunk_combined_set = set.intersection(*chunk_type_categories.values())
chunk_type_filter = set(string.ascii_letters + u""" +☎-@€¥£₹₱₪₩฿""")
chunk_word_filter = set(string.digits + string.ascii_letters)
chunk_description_fuzz = set(['location', 'prime', 'beach'])
def classify_chunk(chunk, position=None, wc_offset=5, full_list=False):
    """ Name, address, directions, url, email, price, hours or description """
    scores = defaultdict(float)
    # If it doesn't triger anything else, it's description
    scores['description'] += 0.1
    if len(chunk) > 140:
        scores['address'] -= 1.5
        scores['description'] += 0.35
        scores['directions'] -= 0.4
        scores['alt'] -= 0.9
    elif len(chunk) > 70:
        scores['description'] += 0.25
        scores['address'] -= 0.7
        scores['directions'] -= 0.2
        scores['alt'] -= 0.6
    elif len(chunk) > 25:
        scores['address'] -= 0.5
    
    if len(chunk) > 25:
        # Fresh, as for all options > 25
        scores['price'] -= 0.15
    else:
        scores['description'] -= 0.1

    if position == 0:
        # No need for further heuristics
        return 'name'
    elif 1 <= position <= 2:
        scores['address'] += 0.5
        scores['directions'] += 0.15
        scores['alt'] += 0.1
        scores['hours'] -= 0.3
    elif position >= 3:
        scores['address'] -= 0.6
        scores['description'] += 0.3

    digit_cnt = sum(1 for c in chunk if c in string.digits)
    if digit_cnt == 0:
        scores['address'] -= 0.3
        scores['price'] -= 1
        scores['fax'] -= 1
        scores['phone'] -= 1
        scores['hours'] -= 0.7
    else:
        zero_cnt = sum(1 for c in chunk if c in '0')
        if zero_cnt > 3:
            scores['price'] += zero_cnt * 0.25
            scores['phone'] -= 0.3
            scores['fax'] -= 0.3
        continuous = re.findall(r'\d+', ''.join(c for c in chunk if c in chunk_word_filter))
        continuous_len = max(len(x) for x in continuous)
        if continuous_len > 5:
            scores['phone'] += 1.4
            scores['fax'] += 1.3
        elif continuous_len <= 4:
            scores['address'] += 0.5
        continuous = [int(x) for x in continuous]
        if any(1700 < x < 2050 for x in continuous):
            # Probably historical date, not price
            scores['price'] -= 0.5
            scores['address'] -= 0.3
        year = datetime.now().year
        if any(year-5 <= x <= year+1 for x in continuous):
            # Probably recent date
            scores['hours'] += 0.1

    # Do exact matching on unmodified string     
    c_len = len(chunk) * 2
    for chunk_type, words in chunk_type_categories_partly.items():
        for word in words:
            pos = chunk.find(word)
            if pos != -1:
                # Upscale the partly matches as they are quite
                # Good indicators
                scores[chunk_type] += (c_len - pos) / c_len * 1.2
                
    cl = ''.join(c for c in chunk.lower() if c in chunk_type_filter)
    cl_splt = cl.split()
    wc = len(cl_splt) + wc_offset
    for cnt, word in enumerate(cl_splt):
        for chunk_type in chunk_type_categories.keys():
            if word in chunk_type_categories[chunk_type]:
                # Rate words by their position in the
                # string, the later, the less important
                scores[chunk_type] += (wc - cnt) / wc
        if word not in chunk_combined_set:
            scores['description'] += 0.07
        if word in chunk_description_fuzz:
            scores['description'] += 0.1

    # Sort by score, highest first
    results = sorted(scores.iteritems(), key=lambda x: x[1], reverse=True)
    # print position, ':', chunk, '     |', ', '.join('%s: %.2f' % nf for nf in results)
    if full_list:
        return results
    return results[0][0]

def merge_chunks(chunks, origin):
    separators = []
    for chunk in chunks:
        pos = origin.find(chunk)
        if pos == -1:
            separators.append('.')
        else:
            pos += len(chunk)
            m = re.search(r'\S', origin[pos:])
            if not m:
                separators.append('.')
            else:
                c = origin[pos+m.start()]
                separators.append(c if c in '.,()' else '.')

    if separators[-1] == '(':
        separators[-1] = '.'
    elif separators[-1] == ')' and not '(' in separators[:-1]:
        separators[-1] = '.'
        
    res = ''
    for cnt, (chunk, sep) in enumerate(zip(chunks, separators)):
        res += chunk
        if cnt < len(chunks) - 1:
            if sep in '.,)':
                res += sep + ' '
            elif sep == '(':
                res += ' ' + sep
        else:
            # Last entry
            if sep in ',)':
                res += sep
    return res
    
