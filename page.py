'''
Created on 14.02.2013

@author: nimrod
'''
from utils import TolerantFormatter
from tests.samples import vcards, tags, untaggeds


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
            <textarea name="convertinput" rows="12" cols="150">{default_input}</textarea>
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
    <textarea rows="12" cols="150">{output}</textarea>
</div>
"""

formatter = TolerantFormatter()
defaultinput = u'Some samples:\n* ' + '\n* '.join((untaggeds[2], untaggeds[9], tags[0], vcards[0]))

def create_page(input_str, output, outputformat='vcard'):
    output = u'\n\n* '.join(output) if input else None
    output = div_output.format(output='* ' + output) if output else ''
    params = dict(output_template=output, default_input=input_str or defaultinput)
    params[outputformat + '_selected'] = u'selected="selcted"'
    return formatter.format(html_template, **params)
