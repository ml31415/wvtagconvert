# -*- coding: utf-8 -*-
'''
Created on 11.02.2013

@author: nimrod
'''
import unittest
from itertools import izip_longest

from heuristics import classify_chunk, determine_tagtype, chunkify, parse_phonefax
from wvtagconvert import Untagged
from samples import untaggeds


class TestCategorizeItems(unittest.TestCase):
    test_arr = [
        ('drink', 'bar'),
        ('drink', 'cafe'),
        ('see', 'religious'),
        ('see', 'religious'),
        ('see', 'religious'),
        ('see', 'religious'),
        ('sleep', 'hotel'),
        ('eat', 'asian'),
        ('drink', 'bar'),
        ('sleep', 'hotel'),
        ('see', 'nature'),
        ('see', 'historical'),
        ('buy', 'touristy'),
        ('see', 'historical'),
        ('see', 'religious'),
        ('see', 'historical'),
        ('see', 'historical'),
        ('sleep', 'hotel'),
        ('sleep', 'hotel'),
        ('sleep', 'guesthouse'),
        ('sleep', 'hotel'),
    ]
    
    def runTest(self):
        for cnt, (item, comp) in enumerate(zip(untaggeds, self.test_arr)):
            tagtype = determine_tagtype(item)
            self.assertEqual(tagtype, comp, "Test %d: %s != %s: %s" % (
                            cnt, tagtype, comp, item))


class TestParsePhonefax(unittest.TestCase):
    test_arr = [
        ("""Colmore Row, ''+44 121'' 262 1840""", ['Colmore Row', "''+44 121'' 262 1840"]),
        ("""Graham St, ''+44 121'' 235 5435.""", ["Graham St", "''+44 121'' 235 5435."]),
        ("""Phone Number: +63(0)2 400-8547 or +63(0)916 644-4157 / e-mail: mailto:lagundian@gmail.com.""",
            ['Phone : +63(0)2 400-8547 or +63(0)916 644-4157 /', 'e-mail : mailto:lagundian@gmail.com.']),
    ]
    
    def runTest(self):
        for val, check in self.test_arr:
            res = parse_phonefax(val, verbose=True)
            self.assertEqual(res, check)


class TestParseUntaggedInput(unittest.TestCase):
    test_splits = [
        """B4 Bar-Café || 75 D Ben Nghe || A charming Belgian-Vietnamese owned bar, with a welcoming interior and free pool""",
        """Café on Thu Wheels || 1/2 D Nguyen Tri Phuong || It's a little bar owned by the charming lady Thu.""",
        """Birmingham Buddhist Centre || 11 Park Rd, Moseley || ''#1, #35 or #50 bus'' || ''+44 121'' 449 5279 || ''[mailto:info@birminghambuddhistcentre.org.uk info@birminghambuddhistcentre.org.uk]'' || http://www.birminghambuddhistcentre.org.uk/ || A centre run by the Friends of the Western Buddhist Order'' .""",
        """Birmingham Cathedral || a.k.a. '''St Philip's Cathedral''' || Colmore Row || ''+44 121'' 262 1840 || ''[mailto:enquiries@birminghamcathedral.com enquiries@birminghamcathedral.com]'' || http://www.birminghamcathedral.com/ || M-F 7:30AM-6:30PM || ''5PM from late Jul to early Sep'' || Sa Su 8:30AM-5PM || Church of England cathedral || built between 1709 and 1715 and the centre of the Diocese of Birmingham || Grade 1 listed building in the UK, designed as a parish church in the Baroque style by Thomas Archer || Contains four spectacular pre-Raphaelite stained glass windows.""",
        """Birmingham Peace Pagoda || Osler St, Ladywood ||  ''+44 121'' 455-0650 || http://www.chezpaul.org.uk/buddhism/uk/talaka.htm || The pagoda is designed as symbol of peace, compassion and the noble exemplary qualities of the Buddha.""",
        """Ramgarhia Sikh Temple || Graham St || ''+44 121'' 235 5435.""",
        """Sohotel || 2016 M H del Pilar Street, Malate ||  Tel No +63 (2) 521-4341 to 44 || This seedy Manila hotel accepts online reservations via the || http://www.sohotelmalate.com Sohotel official website || They, however, lose the reservations, and ask for proof that you made the reservation ||  then charge you extra || They run a 'service car' that charges you afterwards, with a high price above normal taxi fares || This hotel features 24-hour room service that takes over an hour to arrive and themed rooms that can also accommodate parties and other celebrations || The rooms smell and are not cleaned well, and the staff are dishonest.""",
        """Kamayan || 523 Merchant Bldg, Padre Faura St ||  +632-528-1723 to 24 || Kamayan literally means to eat with your hands in Filipino || Their native buffet has a wide range of Filipino food to offer for just under 10 US$/person || Specialties include the lechon || suckling pig || and grilled seafood || Kamayan also has branches in Makati and Quezon City and is usually located alongside its sister restaurants Dad's || Western food buffet || and Saisaki || Japanese food buffet""",
        """Manila Bay Cafe || The district's biggest 'meat market' || It's open 24 hours per day || Two Floors, Live Bands/Music ||  TV Screens || Good food, drinks and music.""",
        """Hotel Indah Manila || 350 A J Villegas St || Tel : ''+63 2'' 5361188, 5362288 || http://www.hotelindah.com/ || Rates start at ₱2000 for this modest 76-room hotel || Facilities include Café Indah and conference and function rooms || Airport and city transfers, tour assistance ||  and laundry service are available.""",
        """Baywalk || South of the Luneta is the renovated '''Baywalk''' a linear park adjacent to Manila Bay || Restaurants formerly on the actual baywalk have been moved inwards to allow a clear view of Manila's legendary sunsets.""",
        """Bonifacio Shrine || A shrine in honour of Andres Bonifacio who was one of the Filipinos who struggled and fought for freedom for the country against the Spanish forces.""",
        """[[Manila/Binondo|Chinatown]] || Manila has one of the largest Chinatowns in the world, where one can find exotic Chinese goods and delicious cuisine.""",
        """Coconut Palace || a residence commissioned and built along the waterfront by First Lady Imelda Marcos for Pope John Paul II's visit in 1981 || While open to the public at some point, it is currently || as of June 2011 || occupied by the current Vice President and still open for public visits || by appointment by calling the Office of the Vice President, leaving a return call number and waiting for a confirmation""",
        """[[Manila/Intramuros|Intramuros]] || At the northern end of the Bay lies the remnants of the old walled Spanish settlement of Manila, Intramuros || Spanish for 'within the walls' || Intramuros contains some of the city's most interesting museums, ruins, and churches including the '''Manila Cathedral''' ||  the most important church in the country.""",
        """Mabini Shrine || Apolinario Mabini's former home || Mabini was a Lawyer and fought for Philippine Independence || During the American Occupation, this home became the first intellectual headquarters of the First Philippine Republic.""",
        """Malacañan Palace || Manila is the host of the official residence of the president of the Philippines || While heading your way here, you will see wonderful places || People can roam the garden afterward.""",
        """Manila Hotel || Just outside Intramuros and on the edge of Manila Bay is the beautiful and historic Manila Hotel, a legacy of the American colonial era and the place where General Douglas MacArthur made his home before World War II.""",
        """White Beach Puerto Galera || http://www.puertogaleratour.com  || has a prime location at the center of White Beach || It offers modestly furnished but comfortable rooms || Each room is air-conditioned and comes with a private toilet and bath with shower and tub, cable TV ||  and room safe || The hotel also has an Internet cafe, bar and restaurant, Jacuzzi ||  and conference room || Water sports are available || that tourists can choose from.""",
        """Lagundian Hills Lodging House || http://www.puerto-galera.isgreat.com || at White Beach || Phone : +63(0)2 400-8547 or +63(0)916 644-4157 / || e-mail : mailto:lagundian@gmail.com || All rooms are well maintained and have views of the beach || Some rooms can accommodate up to eight guests, some have kitchen.""",
        """Aninuan Beach Resort || http://www.aninuanbeach.com/ || Price: USD $50 || Phone : +63920 931 8946 or +63920 931 8924""",
        """deciBel Lounge || http://www.decibel.vn/ || 79/2/5 Phan Ke Binh - Quan 1 HCMC || ☎ +84 8 627 0115 || Close to the Jade Emperor Pagoda || The restaurant cafe deciBel Lounge is a place where you can find monthly art exhibition, a nice range of Mediterranean food and Vietnamese breakfast and lunch set menu || Open from 7am to 12am || Price range 20.000vnd (1$) to 200.000vnd (10$).""",
    ]
    
    test_classification = [
        "name || address || description",
        "name || address || description",
        "name || address || directions || phone || email || url || description",
        "name || alt || address || phone || email || url || hours || hours || hours || description || description || description || description",
        "name || address || phone || url || description",
        "name || address || phone",        
        "name || address || phone || description || url || description || description || description || description || description",
        "name || address || phone || description || description || description || description || description || description || description || description || description",
        "name || description || hours || description || description || description",
        "name || address || phone || url || price || description || description || description",
        "name || description || description",
        "name || description",
        "name || description",
        "name || description || description || description || description || description",
        "name || description || description || description || description",
        "name || alt || description || description",
        "name || description || description || description",
        "name || description",
        "name || url || description || description || description || description || description || description || description || description",
        "name || url || directions || phone || email || description || description",
        "name || url || price || phone",   
        "name || url || address || phone || description || description || hours || price",
    ]
    
    def runTest(self):
        for cnt, (item, check, check_classify) in enumerate(izip_longest(untaggeds, self.test_splits, 
                                                        self.test_classification)):
            chunks = chunkify(item, verbose=not check)
            chunk_str = ' || '.join(chunks)
            if check:
                self.assertEqual(chunk_str, check, 
                        "Test %s\nItem: %s\nRslt: %s\nChck: %s" % (cnt, item, chunk_str, check))
            else:
                print item, '\n', ' || '.join(chunks), '\n'
            chunk_types = map(classify_chunk, chunks, range(len(chunks)))
            chunk_type_str = ' || '.join(chunk_types)
            if check_classify:
                self.assertEqual(chunk_type_str, check_classify, 
                        "Test %s\nRslt: %s\nClss: %s\nChck: %s\n%s" % (
                            cnt, chunk_str, chunk_type_str, check_classify, 
                            '\n'.join(str(classify_chunk(x, pos, full_list=True)) for pos, x in enumerate(chunks))))
            else:
                print chunk_str
                print chunk_type_str

            #print Untagged.read(item) 
            
            

if __name__ == "__main__":
    unittest.main(verbosity=2)