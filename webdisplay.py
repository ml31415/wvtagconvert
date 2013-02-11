'''
Created on 11.02.2013

@author: nimrod
'''
from bottle import route, run, request, template

from wvtagconvert import parse_input, string_formatter

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
    params = dict(output_template=output, default_input=input)
    params[outputformat + '_selected'] = 'selected="selcted"'
    return string_formatter.format(html_template, **params)


if __name__ == '__main__':
    run(reloader=True, host='localhost', port=8080)
