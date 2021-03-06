'''
Created on 15.05.2013

@author: nimrod
'''
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict #@UnusedImport

vcard_fields = ("type subtype name alt comment address directions intl-area-code phone mobile "
               "fax fax-mobile email email2 email3 url facebook google twitter skype hours "
               "checkin checkout price credit-cards lat long description").split()

number_fields = 'phone', 'mobile', 'fax', 'fax-mobile'

def merge_buzzwords(*buzzwordlist):
    categories = set.union(*[set(d) for d in buzzwordlist])
    ret = dict()
    for cat in categories:
        subcategories = set.union(*[set(d.get(cat, dict())) for d in buzzwordlist])
        ret[cat] = dict((subcat, set.union(*[d.get(cat, dict()).get(subcat, set()) for d in buzzwordlist]))
                        for subcat in subcategories)
    return ret

def merge_chunk_buzzwords(*buzzwordlist):
    categories = set.union(*[set(d) for d in buzzwordlist])
    return dict((cat, set.union(*[d.get(cat, set()) for d in buzzwordlist])) for cat in categories)

def categories_buzz(buzzwords):
    return dict((key, set.union(*buzzwords[key].values())) for key in buzzwords)

def subcategories_buzz(buzzwords):
    ret = buzzwords.copy()
    for subcat in ret.values():
        subcat.pop('general', None)
    return ret

def format_vcard(vcard):
    return u'{{%s |%s}}' % (vcard.pop('type', 'listing'), ' |'.join(u"%s=%s" % (key, val) for key, val in vcard.iteritems()))
