'''
Created on 14.02.2013

@author: nimrod
'''
from utils import TolerantFormatter
from tests.samples import vcards, tags, untaggeds


html_template = u"""<!DOCTYPE html>
<html lang="en">
<head>
<title>Wikivoyage Vcard-Tag Converter</title>{jscript}
</head>

<body>
<div id="main">
    <h1>Wikivoyage Vcard-Tag Converter</h1>
    <div>
        <p>Enter wikicode listings (or a URL) to parse and convert formatting to either <a href="http://de.wikivoyage.org/wiki/Vorlage:VCard">vCard</a>
             or <a href="https://en.wikivoyage.org/wiki/Wikivoyage:Listings">listing tag</a> format. Please  
             <a href="https://github.com/ml31415/wvtagconvert/issues/1">report parsing errors</a>. 
             <a href="https://github.com/ml31415/wvtagconvert">Source code</a> is available.
        </p>
        <form action="{script_path}" id="converter" method="post">
            <textarea id="convertinput" name="convertinput" rows="12" cols="150">{default_input}</textarea>
            <p>Output type:
                <select name="outputformat">
                    <option name="vcard"{vcard_selected}>vCard</option>
                    <option name="tag"{tag_selected}>Tag</option>
                    <option name="json"{json_selected}>json</option>
                </select>
                Language:
                <select name="language">
                    <option name="English"{english_selected}>English</option>
                    <option name="German"{german_selected}>German</option>
                    <option name="Portuguese"{portuguese_selected}>Portuguese</option>
                </select>
                <button type="button" onclick="area = document.getElementById('convertinput'); area.value = ''; area.focus()" title="Clear input area">Clear</button>
                <button type="submit" name="parse" title="Parse input data">Parse</button>
                {output_button}
            </p>
        </form>
    </div>
    {output_template}
</div>
</body>
</html>
"""

jscript = u"""
<script type="text/javascript">
    function select_text(id)
    {
       area = document.getElementById(id);
       area.focus();
       area.select();
       copied = document.selection.createRange();
       copied.execCommand("Copy");
    }
</script>
"""

output_button = """<button type="button" name="selectall" onclick="select_text('outputarea')" title="Select all output (and copy on IE)">Select all</button>"""

div_output = u"""<div id="output">
    <h3>Parsed output</h3>
    <textarea id="outputarea" rows="12" cols="150">{output}</textarea>
    <p>
    </p> 
</div>
"""

formatter = TolerantFormatter()
defaultinput = u'Some samples:\n* ' + '\n* '.join((untaggeds[2], untaggeds[9], tags[0], vcards[0]))

def create_page(input_str, output, outputformat='vcard', language='english', script_path='/'):
    output = div_output.format(output=output) if output else ''
    params = dict(output_template=output, default_input=input_str or defaultinput,
                  script_path=script_path, jscript=jscript,
                  output_button=output_button if output else '')
    params[outputformat.lower() + '_selected'] = u'selected="selcted"'
    params[language.lower() + '_selected'] = u'selected="selcted"'
    return formatter.format(html_template, **params)
