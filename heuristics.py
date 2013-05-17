# -*- coding: utf-8 -*-
'''
Created on 14.02.2013

@author: nimrod
'''
from __future__ import division

import sys
import re
import string
import operator
from datetime import datetime
from collections import defaultdict

from utils import find_any
from translation import english

__all__ = ['determine_tagtype', 'chunkify', 'classify_chunk', 'merge_chunks']


buzzword_filter = set(string.ascii_letters + u" /éäöüß")


def determine_category(word_list, categories_dict, wc_offset=10, full_list=False):
    """ Take a whole string and see what it's all about by looking at 
        the single words in it. Try to fit the words into categories
        and give it some final rating. 
    """

    # Give it an offset, so that words in the end are
    # not totally meaningless, maybe needs some more
    # calibration
    wc = len(word_list) + wc_offset
    scores = defaultdict(float)
    for category in categories_dict.keys():
        for cnt, word in enumerate(word_list):
            if word in categories_dict[category]:
                # Rate words by their position in the
                # string, the later, the less important
                scores[category] += (wc - cnt) / wc
    # Sort by score, highest first
    results = sorted(scores.iteritems(), key=operator.itemgetter(1), reverse=True)
    if full_list:
        return results
    try:
        return results[0][0]
    except IndexError:
        return


def determine_tagtype(untagged_str, language):
    """ Rate the whole string, if it fits into some category. 
        Count occurences of topic related words.
        Prefer word hits closer to the beginning of the string.
        Also determine some more specific subtype.
    """
    utl = untagged_str.lower()
    utl = ''.join(c if c in buzzword_filter else ' ' for c in utl)
    utl_splt = utl.split()
    category = determine_category(utl_splt, language.categories_dict) or 'listing'
    if category != 'listing':
        subcategories = language.subcategories_dict.get(category, dict())
        subcategory = determine_category(utl_splt, subcategories) or ''
    else:
        subcategory = ''
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


def get_abbreviations_filter(language):
    abbreviations = getattr(language, 'abbreviations', english.abbreviations)
    abbreviations_filter_base = r'\s(\w|%s)\.'
    if sys.version_info[:2] < (2, 7):
        abbreviations_26 = [abbr.capitalize() for abbr in abbreviations]
        return abbreviations_filter_base % '|'.join(abbreviations + abbreviations_26)
    else:
        return abbreviations_filter_base % '|'.join(abbreviations)

closing_delimiter = {'(': ')', '[': ']'}
def chunkify(s, language, verbose=False):
    """ Split the string into meaningful chunks determined by
        the punctuation and bracketing found inside the string.
    """
    s = s.lstrip('* ')
    # Remove irrelevant dots, which disturb parsing
    s = re.sub(r'\.\s*,', ',', s)
    s = re.sub(r'\.\s*:', '', s)

    abbreviations_filter = get_abbreviations_filter(language)
    if sys.version_info[:2] < (2, 7):
        s = re.sub(abbreviations_filter, r' \1', s)
    else:
        s = re.sub(abbreviations_filter, r' \1', s, flags=re.IGNORECASE)
    if s.startswith("'''"):
        # We know, that bold markup is only a relevant block if it is
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
                s = s[split_pos + 1:]
            else:
                subchunk1 = s[:split_pos].rstrip(', -')
                subchunk2, s = s[split_pos + 1:].split(closing_delimiter[delimiter], 1)
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


def get_chunk_filter(language):
    c = dict()
    c['categories'] = getattr(language, 'chunk_buzzwords', english.chunk_buzzwords)
    c['categories_partly'] = getattr(language, 'chunk_buzzwords_partial', english.chunk_buzzwords_partial)
    c['combined_set'] = set.intersection(*c['categories'].values())
    c['type_filter'] = set(string.ascii_letters + u""" +☎-@€¥£₹₱₪₩฿""")
    c['word_filter'] = set(string.digits + string.ascii_letters)
    c['description_fuzz'] = set(['location', 'prime', 'beach', 'currently'])
    return c

def classify_chunk(chunk, chunk_filter, position=None, wc_offset=5, full_list=False):
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
    else:
        scores['address'] += 0.05
        scores['directions'] -= 0.05

    if len(chunk) > 25:
        # Fresh, as for all options > 25
        scores['price'] -= 0.15
    else:
        scores['description'] -= 0.1

    if position == 0:
        # No need for further heuristics
        return 'name'
    elif position == 1:
        scores['address'] += 0.4
        scores['directions'] += 0.15
        scores['alt'] += 0.3
        scores['hours'] -= 0.2
    elif position == 2:
        scores['address'] += 0.4
        scores['directions'] += 0.15
        scores['alt'] += 0.05
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
        continuous = re.findall(r'\d+', ''.join(c for c in chunk if c in chunk_filter['word_filter']))
        continuous_len = max(len(x) for x in continuous)
        if continuous_len > 5:
            scores['phone'] += 1.4
            scores['fax'] += 1.3
        elif continuous_len <= 4:
            if 1 <= position <= 2:
                scores['address'] += 1.1
            else:
                scores['address'] += 0.2
        continuous = [int(x) for x in continuous]
        if any(1700 < x < 2050 for x in continuous):
            # Probably historical date, not price
            scores['price'] -= 0.5
            scores['address'] -= 0.3
        year = datetime.now().year
        if any(year - 5 <= x <= year + 1 for x in continuous):
            # Probably recent date
            scores['hours'] += 0.1

    # Do exact matching on unmodified string     
    c_len = len(chunk) * 2
    for chunk_type, words in chunk_filter['categories_partly'].items():
        for word in words:
            pos = chunk.find(word)
            if pos != -1:
                # Upscale the partly matches as they are quite
                # good indicators
                scores[chunk_type] += (c_len - pos) / c_len * 1.2

    cl = ''.join(c for c in chunk.lower() if c in chunk_filter['type_filter'])
    cl_splt = cl.split()
    wc = len(cl_splt) + wc_offset
    for cnt, word in enumerate(cl_splt):
        for chunk_type in chunk_filter['categories'].keys():
            if word in chunk_filter['categories'][chunk_type]:
                # Rate words by their position in the
                # string, the later, the less important
                scores[chunk_type] += (wc - cnt) / wc
        if word not in chunk_filter['combined_set']:
            scores['description'] += 0.06
        if word in chunk_filter['description_fuzz']:
            scores['description'] += 0.1

    # Sort by score, highest first
    results = sorted(scores.iteritems(), key=operator.itemgetter(1), reverse=True)
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
                c = origin[pos + m.start()]
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

