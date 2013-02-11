'''
Created on 11.02.2013

@author: nimrod
'''
import unittest

from wvtagconvert import classify_chunk, determine_tagtype
from samples import untaggeds

class TestCategorizeItems(unittest.TestCase):
    def runTest(self):
        for item in untaggeds:
            print item
            print determine_tagtype(item)


if __name__ == "__main__":
    unittest.main(verbosity=2)