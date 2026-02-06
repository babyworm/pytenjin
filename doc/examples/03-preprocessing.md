# Preprocessing

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
