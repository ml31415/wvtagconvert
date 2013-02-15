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
        <p>Enter wikicode listings to parse and convert formatting to either <a href="http://de.wikivoyage.org/wiki/Vorlage:VCard">vCard</a>
             or <a href="https://en.wikivoyage.org/wiki/Wikivoyage:Listings">listing tag</a> format. Please  
             <a href="https://github.com/ml31415/wvtagconvert/issues/1">report parsing errors</a>. 
             <a href="https://github.com/ml31415/wvtagconvert">Source code</a> is available.
        </p>
        <form action="{script_path}" id="converter" method="post">
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

def create_page(input_str, output, outputformat='vcard', script_path='/'):
    output = u'\n\n* '.join(output) if input else None
    output = div_output.format(output='* ' + output) if output else ''
    params = dict(output_template=output, default_input=input_str or defaultinput,
                  script_path=script_path)
    params[outputformat + '_selected'] = u'selected="selcted"'
    return formatter.format(html_template, **params)
