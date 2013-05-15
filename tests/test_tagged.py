'''
Created on 11.02.2013

@author: nimrod
'''
import unittest

from wvtagconvert import parse_wikicode
from utils import html_decode

from samples import vcards, tags, dalat

class TestVcardParser(unittest.TestCase):
    """ Some very lousy initial test cases """
    def runTest(self):
        teststr = '\n* '.join(vcards)
        res = parse_wikicode(teststr, outputformat='vcard')
        self.assertEqual(len(res), len(vcards))
        for r in res:
            self.assertIn('type', r)
            self.assertIn('name', r)


class TestTagParser(unittest.TestCase):
    def runTest(self):
        teststr = '\n* '.join(tags)
        res = parse_wikicode(teststr, outputformat='tag')
        self.assertEqual(len(res), len(tags))
        for r in res:
            self.assertIn('address', r)
            self.assertIn('name', r)


class TestTagParsingHtmlEntities(unittest.TestCase):
    def runTest(self):
        teststr = dalat
        res = parse_wikicode(teststr, outputformat='tag')
        self.assertEqual(teststr.count('*'), len(res))
        for r in res:
            self.assertIn('name', r)


class TestHtmlDecode(unittest.TestCase):
    test_data = """* &lt;see name="Da Lat market">Filled with local specialities: strawberry jam, fruits conserves, avocado, artichoke.&lt;/see>
* &lt;see name="Nha Tho Domaine de Marie" address="Ngo Quyen" directions="1 km from where Hai Thuong and Ba Trang Hai (3 Trang Hai) meets">A pink church on top of a hill, with a store selling various dried fruits and snacks from the local orchards run by the nuns of the monastery.&lt;/see>
* &lt;see name="Da Lat train station">Take the steam train through the 7km historical line to Trai Mat, from there you can visit the Linh Phuong pagoda. Price for a return ticket with the train is 106,000&amp;nbsp;dong.&lt;/see>
* &lt;see name="Golden Spring lake" alt="Ho Suoi Vang">Rather unspoiled scenery.&lt;/see>"""
    def runTest(self):
        res = html_decode(self.test_data)
        self.assertGreater(len(res), len(self.test_data) / 2)
        self.assertNotIn('&lt;', res)
        self.assertEqual(res.count('<see name="'), 4)
        self.assertEqual(res.count('</see>'), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
