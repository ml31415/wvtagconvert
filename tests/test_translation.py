'''
Created on 15.05.2013

@author: nimrod
'''
import unittest

import wvtagconvert
from translation import english, portuguese, german


class TestToString(unittest.TestCase):
    def runTest(self):
        testdict = {'description': u'A centre run by the Friends of the Western Buddhist Order.',
                    'subtype': 'religious', 'url': u'http://www.birminghambuddhistcentre.org.uk/',
                    'phone': u'+44 121 449 5279',
                    'address': u'11 Park Rd, Moseley',
                    'directions': u'#1, #35 or #50 bus',
                    'type': 'see',
                    'email': u'info@birminghambuddhistcentre.org.uk',
                    'name': u'Birmingham Buddhist Centre'}
        print wvtagconvert.Vcard.tostring(testdict, english)
        print wvtagconvert.Vcard.tostring(testdict, portuguese)
        print wvtagconvert.Vcard.tostring(testdict, german)


if __name__ == "__main__":
    unittest.main(verbosity=2)
