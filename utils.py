'''
Created on 14.02.2013

@author: nimrod
'''
import re
import string

__all__ = ['squeeze', 'find_any', 'singular', 'TolerantFormatter']


def squeeze(s):
    return re.sub(r'\s+', ' ', s.strip())

def find_any(haystack, *needles):
    for needle in needles:
        if needle in haystack:
            return True
    return False

_singular_exceptions = set(('goods', 'tapas', 'jeans', 'smoothies', 'trousers', 'pants'))
def singular(w):
    if w.endswith('ies'):
        return w[-3] + 'y'
    elif w.endswith('s') and not w.endswith('ss') and w not in _singular_exceptions:
        if w[:-3] == 'hes':
            return w[:-2]
        else:
            return w[:-1]
    else:
        return w


class TolerantFormatter(string.Formatter):
    """ In case of missing arguments: Ignore them and insert an empty string """
    def get_value(self, key, args, kwargs):
        try:
            return string.Formatter.get_value(self, key, args, kwargs)
        except KeyError:
            return ''

