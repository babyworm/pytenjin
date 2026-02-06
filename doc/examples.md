# pyTenjin Examples

release: 1.1.1

Table of Contents:

- [Bordered Table](#bordered-table)
- [Form](#form)
- [Preprocessing](#preprocessing)
- [Google App Engine](#google-app-engine)

## Bordered Table

**Template: 'table.pyhtml'**

```html
<html>
  <body>
    <h1>${title}</h1>
    <table>
<?py i = 0 ?>
<?py for item in items: ?>
<?py     i += 1 ?>
<?py     color = i % 2 == 0 and '#FFCCCC' or '#CCCCFF' ?>
      <tr bgcolor="#{color}">
        <td>#{i}</td>
        <td>${item}</td>
      </tr>
<?py #endfor ?>
    </table>
  </body>
</html>
```

**Convert into Python script:**

```
$ pytenjin -a convert table.pyhtml
_buf = []; _extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<html>
  <body>
    <h1>''', _escape(_to_str(title)), '''</h1>
    <table>\n''', ));
i = 0
for item in items:
    i += 1
    color = i % 2 == 0 and '#FFCCCC' or '#CCCCFF'
    _extend(('''      <tr bgcolor="''', _to_str(color), '''">
        <td>''', _to_str(i), '''</td>
        <td>''', _escape(_to_str(item)), '''</td>
      </tr>\n''', ));
#endfor
_extend(('''    </table>
  </body>
</html>\n''', ));
print(''.join(_buf))
```

**Main program: 'table.py'**

```python
## create Engine object
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine()

## render template with context data
context = { 'title': 'Bordered Table Example',
            'items': [ '<AAA>', 'B&B', '"CCC"' ] }
output = engine.render('table.pyhtml', context)
print(output)
```

**Result:**

```
$ python table.py
<html>
  <body>
    <h1>Bordered Table Example</h1>
    <table>
      <tr bgcolor="#CCCCFF">
        <td>1</td>
        <td>&lt;AAA&gt;</td>
      </tr>
      <tr bgcolor="#FFCCCC">
        <td>2</td>
        <td>B&amp;B</td>
      </tr>
      <tr bgcolor="#CCCCFF">
        <td>3</td>
        <td>&quot;CCC&quot;</td>
      </tr>
    </table>
  </body>
</html>
```

## Form

**Template: 'form.pyhtml':**

```html
<?py #@ARGS action, params, label ?>
<form action="${action}" method="post">
  <p>
    <label>Name:</label>
    <input type="text" name="name" value="${params.get('name')}" />
  </p>
  <p>
    <label>Gender:</label>
<?py gender = params.get('gender') ?>
<?py checked = {True:' checked="checked"', False:''} ?>
    <input type="radio" name="gender" value="M" #{checked[gender=='M']} />Man
    <input type="radio" name="gender" value="W" #{checked[gender=='W']} />Woman
  </p>
  <input type="submit" value="${label}" />
</form>
```

**Template: 'create.pyhtml':**

```html
<?py _context['title'] = 'Create user' ?>
<?py _context['label'] = 'Create' ?>
<?py _context['action'] = 'action.cgi' ?>
<?py include(':form') ?>
```

**Template: 'update.pyhtml':**

```html
<?py _context['title'] = 'Update user' ?>
<?py _context['label'] = 'Update' ?>
<?py _context['action'] = 'update.cgi' ?>
<?py include(':form') ?>
```

**Layout template: 'layout.pyhtml'**

```html
<html>
 <body>
  <h1>${title}</h1>
  <div class="main-content">
#{_content}
  </div>
 </body>
</html>
```

**Main program: 'main.py':**

```python
## create Engine object
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine(postfix='.pyhtml', layout='layout.pyhtml')

## render template with context data
params = { 'name': 'Foo', 'gender': 'M' }
context = { 'params': params }
output = engine.render(':update', context)   # ':update' == 'update'+postfix
print(output)
```

**Result:**

```
$ python main.py
<html>
 <body>
  <h1>Update user</h1>
  <div class="main-content">
<form action="update.cgi" method="post">
  <p>
    <label>Name:</label>
    <input type="text" name="name" value="Foo" />
  </p>
  <p>
    <label>Gender:</label>
    <input type="radio" name="gender" value="M"  checked="checked" />Man
    <input type="radio" name="gender" value="W"  />Woman
  </p>
  <input type="submit" value="Update" />
</form>

  </div>
 </body>
</html>
```

## Preprocessing

**Library: 'helper.py'**

```python
languages = [
  ('en', 'Engilish'),
  ('fr', 'French'),
  ('de', 'German'),
  ('es', 'Spanish'),
  ('ch', 'Chinese'),
  ('ja', 'Japanese'),
]

import urllib
try:
    from urllib import unquote
except:
    from urllib.parse import unquote

def link_to(label, action=None, id=None):
    buf = ['/app']
    if action: buf.append(action)
    if id: buf.append(id)
    return '<a href="%s">%s</a>' % (unquote('/'.join(buf)), label)
```

**Template: 'select.pyhtml'**

```html
<?PY import helper ?>
<?PY from helper import * ?>
<form>
  <label>Select your language:</label>
  <select name="lang">
<?py table = { params['lang']: ' selected="selected"' } ?>
<?PY for val, name in languages: ?>
    <option value="${{val}}" #{table.get(#{{repr(val)}}, '')}>${{name}}</option>
<?PY #endfor ?>
  </select>
  <input type="submit" value="OK" />
</form>
<p>
  #{{link_to('Back', action='index')}} |
  #{{link_to('Show '+_P('params["name"]'), action='show', id=_p('params["id"]'))}}
</p>
```

**Preprocessed code:**

```
$ pytenjin -a preprocess select.pyhtml
<form>
  <label>Select your language:</label>
  <select name="lang">
<?py table = { params['lang']: ' selected="selected"' } ?>
    <option value="en" #{table.get('en', '')}>Engilish</option>
    <option value="fr" #{table.get('fr', '')}>French</option>
    <option value="de" #{table.get('de', '')}>German</option>
    <option value="es" #{table.get('es', '')}>Spanish</option>
    <option value="ch" #{table.get('ch', '')}>Chinese</option>
    <option value="ja" #{table.get('ja', '')}>Japanese</option>
  </select>
  <input type="submit" value="OK" />
</form>
<p>
  <a href="/app/index">Back</a> |
  <a href="/app/show/#{params["id"]}">Show ${params["name"]}</a>
</p>
```

**Main program: 'main.py'**

```python
import helper

## create engine
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine(postfix='.pyhtml', preprocess=True)

## render template with context data
params = { 'id': 1234, 'name': 'Foo', 'lang': 'ch' }
context = { 'params': params }
output = engine.render(':select', context);
print(output)
```

**Result:**

```
$ python main.py
<form>
  <label>Select your language:</label>
  <select name="lang">
    <option value="en" >Engilish</option>
    <option value="fr" >French</option>
    <option value="de" >German</option>
    <option value="es" >Spanish</option>
    <option value="ch"  selected="selected">Chinese</option>
    <option value="ja" >Japanese</option>
  </select>
  <input type="submit" value="OK" />
</form>
<p>
  <a href="/app/index">Back</a> |
  <a href="/app/show/1234">Show Foo</a>
</p>
```

## Google App Engine

**app.yaml**

```yaml
application: pytenjin-example
version: 1
runtime: python
api_version: 1

handlers:
- url: .*
  script: main.py
```

**main.py**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
### Example application for Google App Engine
###
### Before trying this example, copy 'tenjin.py' to 'lib' folder.
###
###     $ mkdir lib
###     $ cp ../../lib2/tenjin.py lib
###

from __future__ import with_statement

import sys, os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

is_dev = (os.environ.get("SERVER_SOFTWARE") or "").startswith("Devel")

##
## import tenjin module and helper functions
##
sys.path.insert(0, "lib")        # necessary to import library under 'lib'
import tenjin
#tenjin.set_template_encoding("utf-8")            # if you like
from tenjin import *
from tenjin.helpers import *
from tenjin.helpers.html import *
import tenjin.gae; tenjin.gae.init()              # DON'T FORGET THIS LINE!

##
## engine object
##
tenjin_config = {
    "path":   ["templates"],
    "layout": "_layout.pyhtml",
}
engine = tenjin.Engine(**tenjin_config)
#engine = tenjin.SafeEngine(**tenjin_config)      # if you like

##
## logger
##
import logging
logger = logging.getLogger()
if is_dev:
    logger.setLevel(logging.DEBUG)
tenjin.logger = logger                            # set tenjin logger

##
## handler class
##
class MainHandler(webapp.RequestHandler):
    def get(self):
        context = { "page_title": "Tenjin Example in Google App Engine",
                    "environ": self.request.environ }
        html = engine.render("index.pyhtml", context)
        self.response.out.write(html)

##
## WSGI application
##
mappings = [
    ("/", MainHandler),
]

def main():
    app = webapp.WSGIApplication(mappings, debug=is_dev)
    util.run_wsgi_app(app)


if __name__ == "__main__":
    main()
```

**templates/index.pyhtml**

```html
<?py #@ARGS page_title, environ ?>

<h1>${page_title}</h1>

<table class="list">
  <tbody>
    <?py cycle = new_cycle('odd', 'even') ?>
    <?py for key in sorted(environ.keys()): ?>
    <tr class="${cycle()}">
      <th>${key}</th><td>${repr(environ[key])}</td>
    </tr>
    <?py #endfor ?>
  </tbody>
</table>
```

**templates/_layout.pyhtml**

```html
<?py #@ARGS _content, page_title ?>
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta http-equiv="Content-Style-Type" content="text/css">
    <meta http-equiv="Content-Script-Type" content="text/javascript">
    <title>${page_title}</title>
    <style type="text/css">
      .odd  {
        background: #FFE;
      }
      .even {
        background: #EFF;
      }
      table.list {
        border-collapse: collapse;
      }
      table.list th, table.list td {
        border: solid 1px #DDD;
        text-align: left;
        vertical-align: top;
        padding: 2px 5px;
      }
    </style>
  </head>
  <body>

{== _content ==}

  </body>
</html>
```
