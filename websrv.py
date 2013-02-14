'''
Created on 11.02.2013

@author: nimrod
'''
from bottle import route, run, request
import urllib2

from wvtagconvert import parse_wikicode
from page import create_page

icon = None

@route('/', method=['GET', 'POST'])
def serve_page():
    input_str = request.forms.get('convertinput', '').decode('utf8')
    outputformat = request.forms.get('outputformat', 'vcard').lower()
    output = parse_wikicode(input_str, outputformat)
    return create_page(input_str, output, outputformat)

@route('/favicon.ico')
def serve_icon():
    global icon
    if not icon:
        req = urllib2.Request('http://en.wikivoyage.org/favicon.ico', 
            headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686; de; rv:1.9.2.17) '
                                    'Gecko/20110422 Ubuntu/10.04 (lucid) Firefox/3.6.17'})
        try:
            icon = urllib2.urlopen(req).read()
        except Exception:
            pass
    return icon

if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080)
