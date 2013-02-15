'''
Created on 11.02.2013

@author: nimrod
'''
from bottle import route, run, request

from wvtagconvert import create_html
from utils import fake_agent_readurl

icon = None

@route('/', method=['GET', 'POST'])
def serve_page():
    outputformat = request.forms.get('outputformat', 'vcard')
    input_str = request.forms.get('convertinput', '')
    return create_html(input_str, outputformat)

@route('/favicon.ico')
def serve_icon():
    global icon
    if not icon:
        icon = fake_agent_readurl('http://en.wikivoyage.org/favicon.ico')
    return icon

if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080)
