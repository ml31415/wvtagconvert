'''
Created on 14.02.2013

@author: nimrod
'''
import re
import urllib2
import string
import htmlentitydefs


__all__ = ['squeeze', 'find_any', 'singular', 'html_encode', 'html_decode',
           'fake_agent_readurl', 'TolerantFormatter']


def squeeze(s):
    return re.sub(r'\s+', ' ', s.strip())

def find_any(haystack, *needles):
    for needle in needles:
        if needle in haystack:
            return True
    return False

def fake_agent_readurl(url, user_agent='Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.17) '
                                'Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17'):
    req = urllib2.Request(url, 
        headers={'User-Agent': user_agent})
    try:
        return urllib2.urlopen(req).read()
    except Exception:
        pass

def html_encode(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#39;')

def html_decode(s):
    # http://effbot.org/zone/re-sub.htm#unescape-html
    def fixup(m):
        s = m.group(0)
        if s[:2] == "&#":
            # character reference
            try:
                if s[:3] == "&#x":
                    return unichr(int(s[3:-1], 16))
                else:
                    return unichr(int(s[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                s = unichr(htmlentitydefs.name2codepoint[s[1:-1]])
            except KeyError:
                pass
        return s # leave as is
    return re.sub("&#?\w+;", fixup, s)

_singular_exceptions = set(('goods', 'jeans', 'smoothies', 'trousers', 'pants'))
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

