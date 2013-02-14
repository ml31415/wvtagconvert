'''
Created on 11.02.2013

@author: nimrod
'''
import unittest

from wvtagconvert import parse_wikicode

from samples import vcards, tags

class TestVcardParser(unittest.TestCase):
    """ Some very lousy initial test cases """
    def runTest(self):
        teststr = '\n* '.join(vcards)
        res = parse_wikicode(teststr, 'vcard')
        self.assertEqual(len(res), len(vcards))
        for r in res:
            self.assertIn('type', r)
            self.assertIn('name', r)


class TestTagParser(unittest.TestCase):
    def runTest(self):
        teststr = '\n* '.join(tags)
        res = parse_wikicode(teststr, 'vcard')
        self.assertEqual(len(res), len(tags))
        for r in res:
            self.assertIn('type', r)
            self.assertIn('name', r)
            

if __name__ == "__main__":
    unittest.main(verbosity=2)