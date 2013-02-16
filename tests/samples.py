# -*- coding: utf-8 -*-
'''
Created on 11.02.2013

@author: nimrod
'''

tags = [
    '<eat name="Al Forno Ristorante" address="Nördliche Ringstraße 37" phone="+49 9141 920420" email="" fax="" url="www.blafasel.com" hours="" price="" lat="" long=""></eat>',
    '<eat name="Andreas Stuben" address="Rosenstraße 18" phone="+49 9141 8737919" email="" fax="+49 9141 8737920" url="http://www.andreas-stuben.de" hours="" price="" lat="" long=""></eat>',
    '<eat name="Antichi Sapori Romani" address="Judengasse 25" phone="+49 9141 9239172" url="http://www.facebook.com/pages/Antichi-Sapori-Romani/417927868249147" hours="" price="" lat="" long=""></eat>',
    '<eat name="Bräustüberl Zur Kanne" address="Bachgasse 15" phone="+49 9141 3844" email="" url="http://schneider-bier.de/gaststaetten_02_kanne.php" hours="Tu-So 10.30–14.00 and 17.30–24.00" price="">Original interior nearly untouched since 1890.</eat>',
    '<eat name="Hotel Restaurant Goldener Adler" address="Marktplatz 5" phone="+49 9141 85560" email="" fax="+49 9141 855633" url="http://www.hotel-goldener-adler.de" hours="" price="" lat="" long=""></eat>',
    '<eat name="Hotel Restaurant Schwarzer Bär" address="Marktplatz 13" phone="+49 9141 92426" email="" fax="+49 9141 92443" url="http://www.derschwarzebaer.de" hours="" price="" lat="" long=""></eat>',
    '<eat name="Löwengarten Restaurant" address="Westliche Ringstr. 36" phone="+49 9141 8731963">Greek and German food.</eat>',
    '<eat name="Mai Thai" address="Bismarckanlage 16" phone="+49 9141 995759" email="" fax="" url=""></eat>',
    '<eat name="Steakhaus El Toro" address="Obertorstr. 5" phone="+49 9141 922730"></eat>',
    '<eat name="Silbermühle - vino y tapa Restaurant" address="Silbermühle 4" phone="+49 9141 9744001" email="silbermuehle@web.de" fax="" url="http://www.die-silbermuehle.de" hours="" price="" lat="" long=""></eat>',
    """<sleep name="Jugendgästehaus Haus International München" address="Elisabethstr. 87, 80797 München" phone="+49 89 12 00 6 0" email="" fax="+49 89 12 00 6 630" url="www.haus-international.de/" hours="" price="EZ 49,00 €; DZ D/WC 39,00 €" lat="" long="">',</sleep>""",
    """<sleep name="Hyatt Hotel and Casino Manila" 
address="1588 Pedro Gil Corner MH Del Pilar" 
phone="+63 2 245 1234" 
email="reservations.mn@hyatt.com" 
url="http://www.manila.casino.hyatt.com"
>5 star hotel with views of Manila Bay. Has a Casino and a spa.</sleep>""",
]

vcards = [
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

untaggeds = [
    """'''B4 Bar-Café''', 75 D Ben Nghe. A charming Belgian-Vietnamese owned bar, with a welcoming interior and free pool. """,
    """'''Café on Thu Wheels''', 1/2 D Nguyen Tri Phuong. It's a little bar owned by the charming lady Thu.""",
    """'''Birmingham Buddhist Centre''', 11 Park Rd, Moseley (''#1, #35 or #50 bus''), ''+44 121'' 449 5279 (''[mailto:info@birminghambuddhistcentre.org.uk info@birminghambuddhistcentre.org.uk]''), [http://www.birminghambuddhistcentre.org.uk/]. A centre run by the Friends of the Western Buddhist Order'' .""",
    """'''Birmingham Cathedral''' (a.k.a. '''St Philip's Cathedral'''), Colmore Row, ''+44 121'' 262 1840 (''[mailto:enquiries@birminghamcathedral.com enquiries@birminghamcathedral.com]''), [http://www.birminghamcathedral.com/]. M-F 7:30AM-6:30PM (''5PM from late Jul to early Sep''), Sa Su 8:30AM-5PM. Church of England cathedral, built between 1709 and 1715 and the centre of the Diocese of Birmingham. Grade 1 listed building in the UK, designed as a parish church in the Baroque style by Thomas Archer. Contains four spectacular pre-Raphaelite stained glass windows.""",
    """'''Birmingham Peace Pagoda''', Osler St, Ladywood, ''+44 121'' 455-0650, [http://www.chezpaul.org.uk/buddhism/uk/talaka.htm]. The pagoda is designed as symbol of peace, compassion and the noble exemplary qualities of the Buddha.""",
    """'''Ramgarhia Sikh Temple''', Graham St, ''+44 121'' 235 5435.""",
    """'''Sohotel''' 2016 M. H. del Pilar Street, Malate, Tel. No.: +63 (2) 521-4341 to 44. This seedy Manila hotel accepts online reservations via the [http://www.sohotelmalate.com Sohotel official website]. They, however, lose the reservations, and ask for proof that you made the reservation, then charge you extra. They run a 'service car' that charges you afterwards, with a high price above normal taxi fares. This hotel features 24-hour room service that takes over an hour to arrive and themed rooms that can also accommodate parties and other celebrations. The rooms smell and are not cleaned well, and the staff are dishonest.""",
    """'''Kamayan''', 523 Merchant Bldg., Padre Faura St., +632-528-1723 to 24. Kamayan literally means to eat with your hands in Filipino. Their native buffet has a wide range of Filipino food to offer for just under 10 US$/person. Specialties include the lechon (suckling pig) and grilled seafood. Kamayan also has branches in Makati and Quezon City and is usually located alongside its sister restaurants Dad's (Western food buffet) and Saisaki (Japanese food buffet).""",
    """'''Manila Bay Cafe''' - The district's biggest 'meat market'. It's open 24 hours per day. Two Floors, Live Bands/Music, TV Screens. Good food, drinks and music.""",
    """'''Hotel Indah Manila''' 350 A J Villegas St. Tel: ''+63 2'' 5361188, 5362288. [http://www.hotelindah.com/]  Rates start at ₱2000 for this modest 76-room hotel.  Facilities include Café Indah and conference and function rooms.  Airport and city transfers, tour assistance, and laundry service are available.""",
    """'''Baywalk''' - South of the Luneta is the renovated '''Baywalk''' a linear park adjacent to Manila Bay. Restaurants formerly on the actual baywalk have been moved inwards to allow a clear view of Manila's legendary sunsets.""",
    """'''Bonifacio Shrine''' - A shrine in honour of Andres Bonifacio who was one of the Filipinos who struggled and fought for freedom for the country against the Spanish forces.""",
    """'''[[Manila/Binondo|Chinatown]]''' - Manila has one of the largest Chinatowns in the world, where one can find exotic Chinese goods and delicious cuisine.""",
    """'''Coconut Palace''' - a residence commissioned and built along the waterfront by First Lady Imelda Marcos for Pope John Paul II's visit in 1981. While open to the public at some point, it is currently (as of June 2011) occupied by the current Vice President and still open for public visits (by appointment by calling the Office of the Vice President, leaving a return call number and waiting for a confirmation).""",
    """'''[[Manila/Intramuros|Intramuros]]''' - At the northern end of the Bay lies the remnants of the old walled Spanish settlement of Manila, Intramuros (Spanish for 'within the walls').  Intramuros contains some of the city's most interesting museums, ruins, and churches including the '''Manila Cathedral''', the most important church in the country.""",
    """'''Mabini Shrine''' - Apolinario Mabini's former home. Mabini was a Lawyer and fought for Philippine Independence. During the American Occupation, this home became the first intellectual headquarters of the First Philippine Republic.""",
    """'''Malacañan Palace''' - Manila is the host of the official residence of the president of the Philippines. While heading your way here, you will see wonderful places. People can roam the garden afterward.""",
    """'''Manila Hotel''' - Just outside Intramuros and on the edge of Manila Bay is the beautiful and historic Manila Hotel, a legacy of the American colonial era and the place where General Douglas MacArthur made his home before World War II.""",
    """'''White Beach Puerto Galera''' [http://www.puertogaleratour.com ] has a prime location at the center of White Beach. It offers modestly furnished but comfortable rooms. Each room is air-conditioned and comes with a private toilet and bath with shower and tub, cable TV, and room safe. The hotel also has an Internet cafe, bar and restaurant, Jacuzzi, and conference room. Water sports are available.  that tourists can choose from.""", 
    """'''Lagundian Hills Lodging House''' [http://www.puerto-galera.isgreat.com] at White Beach.  Phone Number: +63(0)2 400-8547 or +63(0)916 644-4157 / e-mail: mailto:lagundian@gmail.com.  All rooms are well maintained and have views of the beach.  Some rooms can accommodate up to eight guests, some have kitchen.""",
    """'''Aninuan Beach Resort''' [http://www.aninuanbeach.com/] Price: USD $50. Phone Number: +63920 931 8946 or +63920 931 8924. """,
    """'''deciBel Lounge''' [http://www.decibel.vn/], 79/2/5 Phan Ke Binh - Quan 1. HCMC  ☎+84 8 627 0115. Close to the Jade Emperor Pagoda. The restaurant cafe deciBel Lounge is a place where you can find monthly art exhibition, a nice range of Mediterranean food and Vietnamese breakfast and lunch set menu. Open from 7am to 12am. Price range 20.000vnd (1$) to 200.000vnd (10$).""",
    """'''Barbecue Garden''' [http://www.barbecuegarden.com/], 135A Nam Ky Khoi Nghia - Quan 1. HCMC  ☎+84 8 823 3340. Located 100 m from Ben Thanh Market, behind the General Sciences Library. US$5-7 range. The restaurant is a barbecue specialist with both Vietnamese and International recipes.""",
]

dalat = """* <see name="Colonial palaces">The three palaces and summer home of the colonial-era, last emperor of Vietnam Bao Dai, which is of great interest once you visit these three heritage sites, named as Palace I, II and III, the Dalat Palace Hotel being one of them, with its adjacent Dalat Du Park Hotel, all from the 1922's, together with the Dalat Palace Golf Club, which was built in 1922, to give his majesty the opportunity to practice his golf skills picked up during his years of study in France. The golf course is a awesome site, whether you enjoy the swinging and putting or not, as the coffee shop at the golf course has some wholesome meals of Asian and European making, with great view of the deep green fairways and classy environment. The Palace I is located on the same street when you walk to the Crazy House. It is about 15-30 minutes walk depending on your pace (1.1 km. from Tran Phu, 47 metres elevation gain). Palace II is located on Tran Hung Dao, not far from the Xuan Huong Lake (next to Yersin Park).</see>

[[Image:Hang_Nga_guesthouse_01.jpg|thumb|300px|Crazy House]]
* <see name="Crazy House" url="http://www.crazyhouse.vn/" price="35,000&nbsp;dong" address="Huỳnh Thúc Kháng, Phường 4" directions="about 0.3 km off Duy Tan St">A striking, not-quite-finished fantasy house designed by the daughter of an independence war hero. Well worth a visit, even if you are not too much interested in architecture.</see>

* <see name="Flower Garden" directions="on the northwestern end of the Xuan Huong Lake" price="10,000&nbsp;dong">A set of flower gardens centered around a re-constructed traditional Vietnamese teakwood house. If you go for a stroll around the lake, it can be visited as a stop.</see>

* <see name="Hill-top pagoda">Best to visit coupled with a brief cable car ride over the pine forest.</see>

* <see name="Langbiang mountain">Best to go there with a Land Rover ride, with spectacular views of Dalat and the surrounding mountains and valleys.</see>

[[Image:Xuan_Huong_Lake_08.jpg|thumb|300px|Xuan Huong Lake]]
* <see name="Xuan Huong lake" alt="Hồ Xuân Hương" directions="center of town">Public lake in the center. Approximately 5km in length, this lake was made after two dams on the Camly river were destroyed during a storm in the 1930s. Now, Xuan Huong lake is one of the main draws of Da Lat, and you can see honeymooners and locals strolling its banks. Many nice hotels have a view of the lake. The lake was drained in 2010, but is now filled again. Boats can be rented on both sides of the lake.</see>

* <see name="Da Lat market">Filled with local specialities: strawberry jam, fruits conserves, avocado, artichoke.</see>

* <see name="Nha Tho Domaine de Marie" address="Ngo Quyen" directions="1 km from where Hai Thuong and Ba Trang Hai (3 Trang Hai) meets">A pink church on top of a hill, with a store selling various dried fruits and snacks from the local orchards run by the nuns of the monastery.</see>

* <see name="Da Lat train station">Take the steam train through the 7km historical line to Trai Mat, from there you can visit the Linh Phuong pagoda. Price for a return ticket with the train is 106,000&nbsp;dong.</see>

* <see name="Golden Spring lake" alt="Ho Suoi Vang">Rather unspoiled scenery.</see>

* <see name="Thien Vien Truc Lam Monastery" directions="at the top of where the cable car drops you off" price="Free">The monastery has a magnificent view over the dams below and its gardens are full of landscaped shrubs in animal form. Extremely peaceful - a great place to relax and soak in the tranquility. People who do not want to complete the round trip could opt for a 4.1 km walk back to Tran Phu. Be sure to bring a map. On the walk back you can go down to Tuyen Lam lake (see below), visit nearby Dalanta waterfall and take the bus back to town. The cable car to the monastery costs you 50,000&nbsp;dong single way, return 70,000.</see>

* <see name="Lang Biang mountain">The 1,900&nbsp;m peak is reachable by a steep paved path, ideal for a 3 hours hike, or you can ride in a jeep for 40,000&nbsp;dong. Also visit the minorities village under the mountain foot.</see>

[[Image:The Valley of Love in Dalat, Vietnam.jpg|thumb|300px|The Valley of Love]]
* <see name="Valley of Love" alt="Thung Lũng Tình Yêu" address="Phu Dong Thien Vuong St">Open daily until 5PM. Admission fee under US$1. About 5km outside of town, the Valley of Love is common stop on Dalat tours and is very popular with honeymooners. The Valley of Love is also a great spot for canyoning. See contact info below for canyoning operators.</see>

* <see name="Lake of Sorrow" alt="Lake of Sighs" directions="5km northeast of town on Ho Xuan Huong road">The Lake of Sorrow is another common destination in Dalat. The Lake of Sorrow is so-named because of a tale of two lovers, one who committed suicide after the other was called up to serve in the army.</see>

* <see name="Tuyen Lam Lake" alt="Hồ Tuyền Lâm" directions="5km south of town on highway 20">Its clean green waters flow from the beautiful Tia Spring and from the Da Tam River, which flows down from Voi mountain. Its waters stretch over an immense 350 hectares and because of its various sources, Tuyen Lam is known as the lake where rivers, springs and forests meet. The lake was built in the 80s. It is one of the largest and most beautiful lakes in town. The other side of the lake is the Voi mountain which is a good place for hiking.</see>

* <see name="Prenn Falls" directions="at the foot of Prenn Pass, about 10km outside of town">Open daily until 5PM. A very common stop on a typical Dalat tour, Prenn Falls is quite beautiful but is a lot more fun when you're hiking it than just taking pictures of it.</see>

* <see name="Pongour Falls" directions="30km south of town on highway 20">It's one of the largest and widest waterfalls in Vietnam and during the wet season is a magnificent sight. Although a dam built nearby has reduced the water flow recently.</see>
"""


for lst in (tags, vcards, untaggeds):
    for cnt, val in enumerate(lst):
        lst[cnt] = val.decode('utf8')
        