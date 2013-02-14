'''
Created on 11.02.2013

@author: nimrod
'''
from bottle import route, run, request, template
import urllib2

from wvtagconvert import parse_input, string_formatter
from tests.samples import vcards, tags, untaggeds

defaultinput = u'Some samples:\n* ' + '\n* '.join((untaggeds[2], untaggeds[9], tags[0], vcards[0]))

html_template = u"""<!DOCTYPE html>
<html lang="en">
<head>
<title>Wikivoyage Vcard-Tag Converter</title>
</head>
<body>
<div id="main">
    <h1>Wikivoyage Vcard-Tag Converter</h1>
    <div>
        <p>Enter text to parse and convert formatting from <a href="http://de.wikivoyage.org/wiki/Vorlage:VCard">vCard</a>
             to <a href="https://en.wikivoyage.org/wiki/Wikivoyage:Listings">listing tag</a> or vice versa</p>
        <form action="/" id="converter" method="post">
            <textarea name="convertinput" rows="10" cols="150">{default_input}</textarea>
            <p>Output type:
                <select name="outputformat">
                    <option name="vcard"{vcard_selected}>vCard</option>
                    <option name="tag"{tag_selected}>Tag</option>
                </select>
                <button type="submit" name="button" title="Submit">Submit</button>
            </p>
        </form>
    </div>
    
    {output_template}
</div>
</body>
</html>
"""

div_output = u"""<div id="output">
    <h3>Parsed output</h3>
    <textarea rows="10" cols="150">{output}</textarea>
</div>
"""


@route('/', method=['GET', 'POST'])
def serve():
    input = request.forms.get('convertinput', '').decode('utf8')
    outputformat = request.forms.get('outputformat', 'vcard').lower()
    output = u'\n\n* '.join(parse_input(input, outputformat)) if input else None
    output = div_output.format(output='* ' + output) if output else ''
    params = dict(output_template=output, default_input=input or defaultinput)
    params[outputformat + '_selected'] = u'selected="selcted"'
    return string_formatter.format(html_template, **params)


icon = None
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
