# -*- coding: utf-8 -*-
'''
Created on 10.05.2013

@author: nimrod
'''
from translation.common import vcard_fields, categories_buzz, subcategories_buzz, OrderedDict

mandatory_fields = set(vcard_fields) - set(['fax-mobile', 'email2', 'email3', 'facebook', 'google', 'twitter',
                        'skype', 'credit-cards', 'checkin', 'checkout', 'intl-area-code', 'subtype', 'mobile'])
tagtype_translation = dict(eat='restaurant', drink='bar', buy='shop', do='activity', see='sight', sleep="hotel")

def translate_vcard(vcard):
    default_tag = vcard['type'].lower()
    # vcard['type'] = tagtype_translation.get(default_tag, default_tag)
    # if vcard['type'] == vcard.get('subtype'):
    vcard.pop('subtype', None)

    ret = OrderedDict()
    ret['tag'] = default_tag
    for key in vcard_fields:
        val = vcard.get(key, '')
        if val:
            ret[key] = val
        elif key in mandatory_fields:
            ret[key] = val
        elif vcard['type'] == 'hotel' and key in ('checkin', 'checkout'):
            ret[key] = val
    return ret


# Common abbreviations found in addresses
abbreviations = 'ave bldg blvd dr expy fwy hwy ln pkwy pl rd st jl th tel nr no'.split()

# Translation for categories and subcategories as they appear in the vcard tag
categories = dict(sleep='sleep', eat='eat', drink='drink', do='do', see='see', buy='buy')

# Translation for the different heuristical recognizers
buzzwords = dict(
    sleep=dict(
        general=set(['room', 'lodge', 'lodging', 'aircon', 'a/c',
                 'tv', 'wifi', 'shower', 'breakfast', 'clean',
                 'laundry', 'balcony', 'window', 'baggage', 'cable',
                 'bed', 'fan', 'fridge', 'bathroom', 'lobby',
                 'accomodate', 'guest', 'price', 'accomodation',
                 'smell', 'cleaned', 'staff', 'service']),
        hotel=set(['hotel', 'hyatt', 'novotel', 'sofitel', 'hilton',
               'sheraton', 'kingsize', 'airport pickup', 'minibar',
               'jacuzzi', 'spa', 'safe', 'plaza', 'private safe',
               'square', 'star', 'sauna', 'taxi',
               'residence', 'resort', 'buffet', 'fitness room',
               'suite', 'reservation', 'exclusive', 'elegant']),
        hostel=set(['hostel', 'dorm', 'dormitory', 'backpacker', 'shared',
                'budget', 'cheap']),
        guesthouse=set(['guesthouse', 'guest house', 'house', 'homely',
                    'cheap', 'budget', 'traditional'])),

    eat=dict(
        general=set(['restaurant', 'eat', 'food', 'kitchen', 'cuisine',
                'breakfast', 'wine', 'culinary', 'noodle', 'meal',
                'kebab', 'soup', 'egg', 'buffet',
                'vegetarian', 'beef', 'chicken', 'pork', 'portion',
                'salad', 'fruit', 'lunch', 'dinner', 'dish', 'chef',
                'dining', 'halal', 'dumpling', 'duck', 'specialities', 'wifi']),
        fastfood=set(['fastfood', 'burger', 'hot dog', 'french fries',
                  'chicken wings', 'kfc', 'mcdonalds', 'sandwich',
                  'baguette', 'bistro']),
        indian=set(['indian', 'curry', 'masala', 'tikki', 'tandoori',
                'samosa', 'biryani', 'kerala']),
        seafood=set(['seafood', 'fish', 'crab', 'oyster', 'tuna',
                 'salmon', 'squid', 'lobster', 'octopus', 'shrimp',
                 'scampi', 'herring', 'shark', 'rollmops', 'snapper']),
        asian=set(['asian', 'curry', 'suckling pig', 'vietnamese',
               'chinese', 'spring roll', 'rice', 'spicy',
               'thai', 'pho', 'filipino']),
        italian=set(['italian', 'pizza', 'pasta', 'spaghetti',
                 'bolognese', 'fettuccine', 'risotto',
                 'ristorante', 'minestrone', 'prosciutto', 'insalata',
                 'caprese', 'bruschetta', 'ciabatta', 'calzone', 'penne',
                 'gnocchi', 'lasagna', 'ravioli', 'tagliatelle',
                 'tortellini', 'carbonara', 'arrabiata', 'panzanella',
                 'mascarpone', 'tiramisu', 'zabaglione']),
        german=set(['german', 'wiener', 'schnitzel', 'sausage', 'kraut',
                'bavarian', 'pretzel', 'eintopf', 'cabbage', 'knoedel',
                'dumpling', 'maultaschen', 'spaetzle', 'braten',
                'bratwurst', 'frankfurter', 'frikadellen', 'leberkaese',
                'thueringer', 'roulade']),
        french=set(['baguette', 'bistro', 'crepe', 'quiche', 'croissant',
                'macaroon', 'pot au feu', 'andouillette', 'raclette',
                'cassoulet', 'trinxat', 'aubergine', 'ratatouille',
                'truffle', 'wine']),
        mexican=set(['mexican', 'quesadilla', 'tortilla', 'taquito',
                 'taco', 'empanada', 'enchilada', 'tequila', 'mole',
                 'salsa'])),

    drink=dict(
        cafe=set(['cafe', u'café', 'coffee', 'drink', 'latte', 'tea', 'ice cream',
              'juice', 'bistro', 'smoothies', 'yoghurt', 'ca phe', 'waffle',
              'egg', 'pancake', 'cappuccino', 'donut']),
        bar=set(['bar', 'drink', 'beer', 'draft', 'music', 'live',
             'crowd', 'brewery', 'billiard', 'pool',
             'late', 'evening', 'rooftop', 'pub', 'quiz', 'guitar',
             'band', 'girl', 'jazz', 'smokey', 'dart', 'tv', 'sport']),
        nightclub=set(['club', 'drink', 'cocktail', 'wine', 'lounge', 'music', 'dj',
                   'disco', 'discotheque', 'crowd', 'late', 'floor',
                   'night', 'girl', 'couch', 'jazz', 'open air',
                   'meat market'])),

    see=dict(
        general=set(['museum', 'library', 'exhibition', 'collection', 'sight']),
        religious=set(['pagoda', 'cathedral', 'church', 'mosque', 'dome',
                   'temple', 'old', 'goddess', 'holy', 'saint', 'monk',
                   'nun', 'pray', 'spirit', 'meditation', 'diocese',
                   'worship', 'god', 'buddhist', 'buddha', 'budhism',
                   'allah', 'moslem', 'muslim', 'islam', 'islamic', 'order',
                   'shrine', 'monastery']),
        art=set(['art', 'gallery', 'paint', 'oil', 'statue', 'wood',
             'decor', 'contemporary']),
        nature=set(['park', 'garden', 'green', 'walk', 'forest', 'forrest',
                'lake', 'beach', 'nature', 'untouched', 'view',
                'national park', 'fountain', 'waterfall', 'fall',
                'mountain', 'valley', 'scenery', 'tree']),
        historical=set(['historical', 'history',
               'palace', 'war', 'tour', 'hall', 'monument', 'tower',
               'emperor', 'king', 'queen', 'prince', 'castle', 'fortress',
               'dynasty', 'epoche', 'century', 'ancient', 'baroque',
               'structure', 'building', 'court', 'government',
               'reconstructed', 'neoclassical', 'president',
               'residence', 'settlement', 'wall', 'ruin',
               'freedom', 'forces', 'honour', 'struggled',
               'fought', 'country', 'official', 'republic',
               'independence', 'occupation', 'occupied',
               'headquarter', 'first lady'])),

    buy=dict(
        general=set(['buy', 'cheap', 'shop', 'market', 'goods', 'item',
                'money', 'price', 'save', 'bargain', 'bargaining'
                'cash', 'haggle', 'haggling', 'sell', 'store',
                'shopping', 'expensive', 'overpriced']),
        cloth=set(['cloth', 'jeans', 'shirt', 'wear', 'accessory',
               'dress', 'hats', 'leather', 'suit', 'coat', 'tailor',
               'wardrobe', 'trousers', 'pants', 'jacket', 'polyester',
               'wool', 'cotton', 'silk', 'tie', 'belt']),
        books=set(['paper', 'book', 'magazin', 'journal', 'print',
               'newspaper']),
        touristy=set(['souvenir', 'watch', 'jewelry', 'present', 'dvd',
                  'kitsch', 'antiquity', 'exotic', 'speciality'])),

    do=dict(
        general=set(['guide', 'kid', 'event', 'swimming pool']),
        outdoor=set(['outdoor', 'dive', 'scuba', 'diving', 'snorkel', 'hike', 'hiking', 'bike',
                 'biking', 'fishing', 'swim', 'go', 'ride',
                 'adventure', 'tour', 'climbing', 'riding',
                 'horse', 'rafting', 'bungee', 'kite', 'kitesurfing', 'windsurfing',
                 'surfing', 'paragliding', 'helicopter', 'paintball',
                 'karting', 'motocross', 'sandboarding', 'sightseeing',
                 'canoeing', 'kayaking', 'sailing']),
        indoor=set(['cinema', 'cineplex', 'badminton', 'aerobic',
                'cooking', 'concert', 'theater', 'dolphinarium',
                'festival', 'opera', 'zoo']),
        learn=set(['learn', 'university', 'teach', 'student', 'language',
               'cooking']))
)

categories_dict = categories_buzz(buzzwords)
subcategories_dict = subcategories_buzz(buzzwords)

chunk_buzzwords = dict(
    address=set(['avenue', 'ave', 'building', 'bldg', 'boulevard', 'blvd',
                   'drive', 'dr', 'expressway', 'expy', 'freeway', 'fwy',
                   'highway', 'hwy', 'lane', 'ln', 'parkway', 'pkwy',
                   'place', 'pl', 'road', 'rd', 'street', 'st',
                   'jalan', 'jl', 'soi', 'thanon', 'th', # Indonesia, Thailand
                   'quan', 'q', 'd', 'dist', 'district']), # Districts in Vietnam
    directions=set(['intersection', 'corner', 'opposite', 'nearby',
                  'near', 'inside', 'behind', 'left', 'right', 'bus',
                  'train', 'station', 'taxi', 'stop', 'next', 'at',
                  'between', 'tube', 'metro', 'subway', 'tram',
                  'located', 'm', 'from']),
    alt=set(['aka', 'also', 'known', 'former']),
    phone=set(['tel', 'nr', 'phone', 'number', u'☎']),
    email=set(['email', 'e-mail', 'mail', 'mailto']),
    hours=set(['hours', 'day', 'from', 'to', 'open', 'until', 'daily', 'm', 'tu', 'w', 'th', 'f', 'sa', 'su',
                 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'
                 '24', 'late', 'noon', 'midnight']),
    fax=set(['fax', 'number']),
    price=set(['rates', 'start', 'only', 'cheap', 'from', 'to', 'euro'])
)

chunk_buzzwords_partial = dict(
    url=set(['http://', 'www.', '.com', '.org', '.net', '.htm', '.php']),
    directions=set(['#']),
    alt=set(["'''"]),
    phone=set(['+']),
    fax=set(['+']),
    email=set(['@', '.com', '.org', '.net']),
    hours=set(['AM', 'PM']),
    price=set(['$', 'USD', 'dollar', u'€', 'EUR',
                 u'¥', 'JPY', u'£', 'GBP',
                 u'¥', 'RMB', 'yuan', u'₹', 'INR', 'rupees'
                 u'₱', 'PHP', 'pesos', u'₪', 'NIS', 'shekels',
                 u'₩', 'KRW', u'฿', 'baht',
                 'RM', ' MYR', 'ringgit', 'Rp', 'IDR', 'rupiah',
                 'rubles', 'dong', 'DKK', 'NOK', 'SEK'])
)

