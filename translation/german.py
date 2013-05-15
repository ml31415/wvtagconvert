# -*- coding: utf-8 -*-
'''
Created on 10.05.2013

@author: nimrod
'''
from collections import OrderedDict

from translation.common import vcard_fields, merge_buzzwords, categories_buzz, subcategories_buzz
import translation.english as english

mandatory_fields = english.mandatory_fields

# Common abbreviations found in addresses
#abbreviations = 'ave bldg blvd dr expy fwy hwy ln pkwy pl rd st jl th tel nr no'
abbreviations = 'st pl tel nr no'.split()

# Translation for categories and subcategories as they appear in the vcard tag
categories = dict(sleep='accomodation', eat='restaurant', drink='bar', do='do',
                  see='see', learn='learn', buy='shop', listing='listing')

def translate_vcard(vcard):
    default_type = vcard['type']
    vcard['type'] = categories.get(default_type, default_type)
    subtype = vcard.get('subtype')
    if vcard['type'] == subtype:
        vcard.pop('subtype', None)
    elif subtype:
        vcard['type'] = subtype
        vcard.pop('subtype', None)

    ret = OrderedDict()
    ret['tag'] = default_type
    for key in vcard_fields:
        val = vcard.get(key, '')
        if val:
            ret[key] = val
        elif key in mandatory_fields:
            ret[key] = val
        elif vcard['type'] == 'hotel' and key in ('checkin', 'checkout'):
            ret[key] = val
    return ret


# Translation for the different heuristical recognizers
buzzwords = dict(
    sleep=dict(
        general={'zimmer', 'unterkunft', 'klimaanlage', 'fernseher',
                 'wlan', 'dusche', 'frühstück', 'sauber',
                 'wäsche', 'balkon', 'fenster', 'gepäck', 'kabel',
                 'bett', 'ventilator', 'kühlschrank', 'bad', 'lobby',
                 'beherbergen', 'gast', 'preis', 'geruch', 'gereinigt',
                 'staff', 'personal', 'service', 'internet'},
        hotel={'schließfach', 'platz', 'exklusiv', 'fitnessraum',
               'reservierung', 'empfang', 'anmeldung', 'gehoben'},
        hostel={'günstig', 'preiswert', 'herberge', 'jugendherberge'},
        guesthouse={'gasthaus', 'familiär'}),

    eat=dict(
        general={'restaurant', 'essen', 'küche', 'kulinarisch',
                'frühstück', 'wein', 'nudeln', 'mahl', 'mahlzeit',
                'suppe', 'eier', 'salat',
                'vegetarisch', 'rind', 'hühnchen', 'schwein',
                'frucht', 'früchte', 'abendessen', 'speise', 'koch',
                'knödel', 'ente', 'spezialitäten'},
        fastfood={'fastfood', 'burger', 'hot dog', 'french fries',
                    'chicken wings', 'kfc', 'mcdonalds', 'sandwich',
                    'baguette', 'bistro'},
        indian={'indisch'},

        # TODO: hier weitermachen
        seafood={'seafood', 'fish', 'crab', 'oyster', 'tuna',
                   'salmon', 'squid', 'lobster', 'octopus', 'shrimp',
                   'scampi', 'herring', 'shark', 'rollmops', 'snapper'},
        asian={'asian', 'curry', 'suckling pig', 'vietnamese',
                 'chinese', 'spring roll', 'rice', 'spicy',
                 'thai', 'pho', 'filipino'},
        italian={'italian', 'pizza', 'pasta', 'spaghetti',
                   'bolognese', 'fettuccine', 'risotto',
                   'ristorante', 'minestrone', 'prosciutto', 'insalata',
                   'caprese', 'bruschetta', 'ciabatta', 'calzone', 'penne',
                   'gnocchi', 'lasagna', 'ravioli', 'tagliatelle',
                   'tortellini', 'carbonara', 'arrabiata', 'panzanella',
                   'mascarpone', 'tiramisu', 'zabaglione'},
        german={'german', 'wiener', 'schnitzel', 'sausage', 'kraut',
                  'bavarian', 'pretzel', 'eintopf', 'cabbage', 'knoedel',
                  'dumpling', 'maultaschen', 'spaetzle', 'braten',
                  'bratwurst', 'frankfurter', 'frikadellen', 'leberkaese',
                  'thueringer', 'roulade'},
        french={'baguette', 'bistro', 'crepe', 'quiche', 'croissant',
                  'macaroon', 'pot au feu', 'andouillette', 'raclette',
                  'cassoulet', 'trinxat', 'aubergine', 'ratatouille',
                  'truffle', 'wine'},
        mexican={'mexican', 'quesadilla', 'tortilla', 'taquito',
                   'taco', 'empanada', 'enchilada', 'tequila', 'mole',
                   'salsa'})

#    drink = dict(
#        cafe={'cafe', u'café', 'coffee', 'drink', 'latte', 'tea', 'ice cream',
#                'juice', 'bistro', 'smoothies', 'yoghurt', 'ca phe', 'waffle',
#                'egg', 'pancake', 'cappuccino', 'donut'},
#        bar={'bar', 'drink', 'beer', 'draft', 'music', 'live',
#               'crowd', 'brewery', 'billiard', 'pool',
#               'late', 'evening', 'rooftop', 'pub', 'quiz', 'guitar',
#               'band', 'girl', 'jazz', 'smokey', 'dart', 'tv', 'sport'},
#        nightclub={'club', 'drink', 'cocktail', 'wine', 'lounge', 'music', 'dj',
#                     'disco', 'discotheque', 'crowd', 'late', 'floor',
#                     'night', 'girl', 'couch', 'jazz', 'open air',
#                     'meat market'})
#    
#    see = dict(
#        general={'museum', 'library', 'exhibition', 'collection', 'sight'},
#        religious={'pagoda', 'cathedral', 'church', 'mosque', 'dome',
#                     'temple', 'old', 'goddess', 'holy', 'saint', 'monk',
#                     'nun', 'pray', 'spirit', 'meditation', 'diocese',
#                     'worship', 'god', 'buddhist', 'buddha', 'budhism',
#                     'allah', 'moslem', 'muslim', 'islam', 'islamic', 'order',
#                     'shrine', 'monastery'},
#        art={'art', 'gallery', 'paint', 'oil', 'statue', 'wood',
#               'decor', 'contemporary'},
#        nature={'park', 'garden', 'green', 'walk', 'forest', 'forrest',
#                  'lake', 'beach', 'nature', 'untouched', 'view',
#                  'national park', 'fountain', 'waterfall', 'fall',
#                  'mountain', 'valley', 'scenery', 'tree'},
#        historical={'historical', 'history',
#               'palace', 'war', 'tour', 'hall', 'monument', 'tower',
#               'emperor', 'king', 'queen', 'prince', 'castle', 'fortress',
#               'dynasty', 'epoche', 'century', 'ancient', 'baroque',
#               'structure', 'building', 'court', 'government',
#               'reconstructed', 'neoclassical', 'president',
#               'residence', 'settlement', 'wall', 'ruin',
#               'freedom', 'forces', 'honour', 'struggled',
#               'fought', 'country', 'official', 'republic',
#               'independence', 'occupation', 'occupied',
#               'headquarter', 'first lady'})
#    
#    buy = dict(
#        general={'buy', 'cheap', 'shop', 'market', 'goods', 'item',
#               'money', 'price', 'save', 'bargain', 'bargaining'
#               'cash', 'haggle', 'haggling', 'sell', 'store',
#               'shopping', 'expensive', 'overpriced'},
#        cloth={'cloth', 'jeans', 'shirt', 'wear', 'accessory',
#                 'dress', 'hats', 'leather', 'suit', 'coat', 'tailor',
#                 'wardrobe', 'trousers', 'pants', 'jacket', 'polyester',
#                 'wool', 'cotton', 'silk', 'tie', 'belt'},
#        books={'paper', 'book', 'magazin', 'journal', 'print',
#                 'newspaper'},
#        touristy={'souvenir', 'watch', 'jewelry', 'present', 'dvd',
#                    'kitsch', 'antiquity', 'exotic', 'speciality'})
#    
#    do = dict(
#        general={'guide', 'kid', 'event', 'swimming pool'},
#        outdoor={'outdoor', 'dive', 'scuba', 'diving', 'snorkel', 'hike', 'hiking', 'bike',
#              'biking', 'fishing', 'swim', 'go', 'ride',
#              'adventure', 'tour', 'climbing', 'riding',
#              'horse', 'rafting', 'bungee', 'kite', 'kitesurfing', 'windsurfing',
#              'surfing', 'paragliding', 'helicopter', 'paintball',
#              'karting', 'motocross', 'sandboarding', 'sightseeing',
#              'canoeing', 'kayaking', 'sailing'},
#        indoor={'cinema', 'cineplex', 'badminton', 'aerobic',
#              'cooking', 'concert', 'theater', 'dolphinarium',
#              'festival', 'opera', 'zoo'},
#        learn={'learn', 'university', 'teach', 'student', 'language',
#                 'cooking'})
)
buzzwords = merge_buzzwords(buzzwords, english.buzzwords)
categories_dict = categories_buzz(buzzwords)
subcategories_dict = subcategories_buzz(buzzwords)


