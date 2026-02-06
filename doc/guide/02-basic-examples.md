# Basic Examples

This section describes basics of Tenjin.

## Template Syntax

Notation:

**`<?py ... ?>`**
: Python statements

**`${...}` or `{=...=}`**
: Python expression (with HTML escape)

**`#{...}` or `{==...==}`**
: Python expression (without HTML escape)

> **NOTE:**
>
> Since version 1.0.0, pyTenjin provides `{=...=}` and `{==...==}` for embedded expression as well as `${...}` and `#{...}`. This is for:
>
> - ~~Conveniency: `${_('Hello {}!').format(name)}` is NG (because '}' appears in `${...}`) but `{=_('Hello {}!').format(name)=}` is OK.~~ Since pyTenjin 1.1.0, it is possible to include pair of `{` and `}` inside of `${...}` or `#{...}`.
> - Security: you may take a mistake to write `#{...}` instead of `${...}` easily because they are similar, but you will not confuse between `{=...=}` and `{==...==}` because the latter is MUCH longer then the former!

> **NOTE:**
>
> Since version 1.1.0, `${...}` and `#{...}` can contain pair of `{` and `}` limitedly. See the following example::
>
> ```
> ## OK
> ${foo({'x':1})}
> ${foo({'x':1}) + bar({'y':2})}
> ${foo({}, {}, {})}
> ## NG
> ${foo({'x': {'y': {}}})}
> ```

**views/page.pyhtml: html template**

```html
<h2>${title}</h2>
<table>
  <?py i = 0 ?>
  <?py for item in items: ?>
  <?py     i += 1 ?>
  <?py     klass = i % 2 and 'odd' or 'even' ?>
  <tr class="#{klass}">
    <td>${item}</td>
  </tr>
  <?py #endfor ?>
</table>
```

You can write any Python statements or expression in yor template file, but there are several restrictions.

- **It is necessary to close 'for', 'if', 'while', ... by corresponding '#endfor', '#endif', '#endwhile', and so on.** Notice that '#end' is almighty closer.
- **Indentation is not necessary** since version 1.0.0.
- Conditional expression of 'if', 'while', ... should be in a line.
- '#' (comment) after ':' or '#endXXX' are not allowed.

**Examples**

```html
## [OK] Indentation is not necessary.
<?py for x in nums: ?>
<?py if x > 0: ?>
<p>Positive.</p>
<?py elif x < 0: ?>
<p>Negative.</p>
<?py else: ?>
<p>Zero.</p>
<?py #endif ?>
<?py #endfor ?>

## [NG] conditional expression of 'if' is not in a line
<?py if re.search(r'^\[(\w+)\]',?>
<?py              line, re.M): ?>
<p>matched.</p>
<?py #endif ?>

## [NG] there is a comment after ':' and '#endfor'
<ul>
<?py if item in items:   ## beginning of loop ?>
  <li>${item}</li>
<?py #endfor             ## end of loop ?>
</ul>
```

> **TIPS:**
>
> You can check template syntax by 'pytenjin -z'.
>
> **Syntax check of template files**
>
> ```console
> $ pytenjin -z views/*.pyhtml
> views/page.pyhtml - ok.
> ```

## Render Template

This is an example code to render template file.

**main.py: main program**

```python
## import modules and helper functions
import tenjin
#tenjin.set_template_encoding('cp932')   # template encoding
from tenjin.helpers import *

## context data
context = {
    'title': 'Tenjin Example',
    'items': ['<AAA>', 'B&B', '"CCC"'],
}

## create engine object
engine = tenjin.Engine(path=['views'])

## render template with context data
html = engine.render('page.pyhtml', context)
print(html)
```

**result**

```console
$ python main.py
<h2>Tenjin Example</h2>
<table>
  <tr class="odd">
    <td>&lt;AAA&gt;</td>
  </tr>
  <tr class="even">
    <td>B&amp;B</td>
  </tr>
  <tr class="odd">
    <td>&quot;CCC&quot;</td>
  </tr>
</table>
```

If you want to specify template encoding, call `tenjin.set_template_encoding()`. Default encoding is 'utf-8'. See [Template Encoding](#template-encoding) section for details.

## Show Converted Source Code

pyTenjin converts template files into Python script and executes it. Compiled Python script is saved into cache file automatically in text format.

**Show cached file**

```console
$ ls views/page.pyhtml*
views/page.pyhtml       views/page.pyhtml.cache
$ file views/page.pyhtml.cache
views/page.pyhtml.cache: text
```

You can get converted script by '`pytenjin -s`'.

**Show Python code**

```console
$ pytenjin -s views/page.pyhtml
_buf = []; _extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<h2>''', _escape(_to_str(title)), '''</h2>
<table>\n''', ));
i = 0
for item in items:
    i += 1
    klass = i % 2 and 'odd' or 'even'
    _extend(('''  <tr class="''', _to_str(klass), '''">
    <td>''', _escape(_to_str(item)), '''</td>
  </tr>\n''', ));
#endfor
_extend(('''</table>\n''', ));
print(''.join(_buf))
```

If you specify '`-sb`' instead of '`-s`', neither preamble (= '`_buf = [];`') nor postamble (= '`print("".join(_buf))`') are printed. See [Retrieve Embedded Code](#command-retrieve) section for more information.

Or:

**How to convert template file into Python script**

```python
import tenjin
template = tenjin.Template('views/page.pyhtml')
print(template.script)

### or:
#template = tenjin.Template()
#with open('views/page.pyhtml') as f:
#    print(template.convert(f.read(), 'views/page.pyhtml'))

### or:
#engine = tenjin.Engine(path=['views'])
#print(engine.get_template('page.pyhtml').script)
```

## Layout Template

Layout template will help you to use common HTML design for all pages.

**views/\_layout.pyhtml**

```html
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${title}</title>
  </head>
  <body>
#{_content}
  </body>
</html>
```

**main.py**

```python
## import modules and helper functions
import tenjin
from tenjin.helpers import *

## context data
context = {
    'title': 'Tenjin Example',
    'items': ['<AAA>', 'B&B', '"CCC"'],
}

## cleate engine object
engine = tenjin.Engine(path=['views'], layout='_layout.pyhtml')

## render template with context data
html = engine.render('page.pyhtml', context)
print(html)
```

**Result**

```console
$ python main.py
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Tenjin Example</title>
  </head>
  <body>
<h2>Tenjin Example</h2>
<table>
  <tr class="odd">
    <td>&lt;AAA&gt;</td>
  </tr>
  <tr class="even">
    <td>B&amp;B</td>
  </tr>
  <tr class="odd">
    <td>&quot;CCC&quot;</td>
  </tr>
</table>

  </body>
</html>
```

You can specify other layout template file with `render()` method.

```python
## use other layout template file
engine.render('page.pyhtml', context, layout='_other_layout.pyhtml')

## don't use layout template file
engine.render('page.pyhtml', context, layout=False)
```

Tenjin supports nested layout template. See [Nested Layout Template](#nested-layout-template) section for details.

## Context Variables

'`_context`' dictionary contains context data which are passed from main program into template file.

Using '`_context`' dictionary, you can pass any data from template file to main program or layout template file.

**views/\_layout.pyhtml**

```html
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${page_title}</title>
  </head>
  <body>
#{_content}
  </body>
</html>
```

**views/page.pyhtml: pass page title date from template to layout template**

```html
<?py _context['page_title'] = 'Tenjin: Layout Template Example' ?>
<h2>${title}</h2>
<table>
<?py i = 0 ?>
<?py for item in items: ?>
<?py     i += 1 ?>
<?py     klass = i % 2 and 'odd' or 'even' ?>
  <tr class="#{klass}">
    <td>${item}</td>
  </tr>
<?py #endfor ?>
</table>
```

**Result**

```console
$ python main.py
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Tenjin: Layout Template Example</title>
  </head>
  <body>
<h2>Tenjin Example</h2>
<table>
  <tr class="odd">
    <td>&lt;AAA&gt;</td>
  </tr>
  <tr class="even">
    <td>B&amp;B</td>
  </tr>
  <tr class="odd">
    <td>&quot;CCC&quot;</td>
  </tr>
</table>

  </body>
</html>
```

## Template Arguments

For readability, it is recommended to declare context variables in your template files.

**views/page.pyhtml**

```html
<?py #@ARGS title, items ?>
<?py _context['page_title'] = 'Tenjin: Layout Template Example' ?>
<h2>${title}</h2>
<table>
<?py i = 0 ?>
<?py for item in items: ?>
<?py     i += 1 ?>
<?py     klass = i % 2 and 'odd' or 'even' ?>
  <tr class="#{klass}">
    <td>${item}</td>
  </tr>
<?py #endfor ?>
</table>
```

**Converted Python script**

```console
$ pytenjin -sb views/page.pyhtml
_extend=_buf.extend;_to_str=to_str;_escape=escape; title = _context.get('title'); items = _context.get('items');
_context['page_title'] = 'Tenjin: Layout Template Example'
_extend(('''<h2>''', _escape(_to_str(title)), '''</h2>
<table>\n''', ));
i = 0
for item in items:
    i += 1
    klass = i % 2 and 'odd' or 'even'
    _extend(('''  <tr class="''', _to_str(klass), '''">
    <td>''', _escape(_to_str(item)), '''</td>
  </tr>\n''', ));
#endfor
_extend(('''</table>\n''', ));
```

**views/\_layout.pyhtml**

```html
<?py #@ARGS _content, page_title ?>
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${page_title}</title>
  </head>
  <body>
#{_content}
  </body>
</html>
```

**Converted Python script**

```console
$ pytenjin -sb views/_layout.pyhtml
_content = _context.get('_content'); page_title = _context.get('page_title');
_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>''', _escape(_to_str(page_title)), '''</title>
  </head>
  <body>
''', _to_str(_content), '''
  </body>
</html>\n''', ));
```

> **TIPS:**
>
> If you want to specify default value of context variable, try `_context.get('varname', defaultvalue)`.
>
> ```html
> <?py
> ## if username is not specified, use 'World' as default.
> username = _context.get('username', 'World')
> ?>
> <p>Hello ${username}</p>
> ```

## Include Partial Template

You can include other template files by `include()` helper function.

**include(*template-name*, *\*\*kwargs*)**
: Include other template. *template-name* can be file name or template short name. *kwargs* is passed to template as local variables.

In the following example, layout template includes header and footer templates into it.

**views/\_layout.pyhtml**

```html
<?py #@ARGS _content, page_title ?>
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${page_title}</title>
  </head>
  <body>
<?py include('_header.pyhtml', title=page_title) ?>
#{_content}
<?py include('_footer.pyhtml') ?>
  </body>
</html>
```

**views/\_header.pyhtml**

```html
<?py #@ARGS title ?>
<div class="header">
  <h1>${title}</h1>
</div>
```

**views/\_footer.pyhtml**

```html
<?py #@ARGS ?>
<address>
  copyright(c) 2010 kuwata-lab.com all rights reserved
</address>
```

Output result shows that header and footer templates are included as you expect.

**Result**

```console
$ python main.py
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Tenjin: Layout Template Example</title>
  </head>
  <body>
<div class="header">
  <h1>Tenjin: Layout Template Example</h1>
</div>
<h2>Tenjin Example</h2>
<table>
  <tr class="odd">
    <td>&lt;AAA&gt;</td>
  </tr>
  <tr class="even">
    <td>B&amp;B</td>
  </tr>
  <tr class="odd">
    <td>&quot;CCC&quot;</td>
  </tr>
</table>

<address>
  copyright(c) 2010 kuwata-lab.com all rights reserved
</address>
  </body>
</html>
```

## Template Short Name

If you set template postfix, you can specify template by short name such as '`:page`' instead of '`page.pyhtml`'. Notice that template short name should start with '`:`'.

**main.py**

```python
## import modules and helper functions
import tenjin
from tenjin.helpers import *

## context data
context = {
    'title': 'Tenjin Example',
    'items': ['<AAA>', 'B&B', '"CCC"'],
}

## cleate engine object
engine = tenjin.Engine(path=['views'], postfix='.pyhtml', layout=':_layout')

## render template with context data
html = engine.render(':page', context)
print(html)
```

**views/\_layout.pyhtml**

```html
<?py #@ARGS _content, page_title ?>
<!DOCTYPE>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>${page_title}</title>
  </head>
  <body>
<?py include(':_header', title=page_title) ?>
#{_content}
<?py include(':_footer') ?>
  </body>
</html>
```

## Template Encoding

If you want to specify encoding name, call `tenjin.set_template_encoding('utf-8')` in your main program or add magic comment into template file.

See the following description.

### Python 2.x

> **NOTE:** This section describes Python 2.x behavior and is kept for historical reference only. PyTenjin requires Python 3.8+, where all strings are unicode by default.

> **NOTE:**
>
> It is planned to change pyTenjin to be unicode-based templates in the future release. This is because a lot of O/R Mapper or helper libraries assume string to be unicode object. However pyTenjin will provides users to select str-based or uicode-based by `tenjin.set_template_encoding()` function.

Tenjin provides two approaches for encoding in Python 2.x.

**(A) Binary-based approach (default)**

Tenjin converts templates into binary string. You can see that converted script uses str instead of unicode.

```python
_extend(('''Hello ''', _to_str(name), '''!''', ))
```

If you got troubles around encoding in this approach, add magic comment into template files.

```python
<?py # -*- coding: utf-8 -*- ?>
<h1>Hello</h1>
```

If you want to specify encoding name such as euc-jp or cp932, call `tenjin.set_template_encoding(encode='cp932')` before importing helper functions.

```python
import tenjin
tenjin.set_template_encoding(encode='cp932')   # or shift_jis
from tenjin.helpers import *
   # ex. to_str(u'日本語') => '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
```

In this approach, unicode object should be converted into str and this is done by `to_str()` automatically. `tenjin.set_template_encoding()` generates correct `to_str()` function therefore you must call it before importing helper functions.

> **NOTE:**
>
> When you called `tenjin.set_template_encoding()`, it is strongly recommened to touch template files (= update timestamp of template files) in order to clear template caches.

**(B) Unicode-based approach**

You can specify pyTenjin to convert template files into unicode object, such as:

```python
_extend((u'''Hello ''', _to_str(name), u'''!''', ))
```

If you prefer this approach, call `tenjin.set_template_encoding()` before importing helper functions.

```python
import tenjin
tenjin.set_template_encoding('utf-8')   # or decode='utf-8'
from tenjin.helpers import *
   # ex. to_str('日本語')  #=> u'\u65e5\u672c\u8a9e'
```

In this approach, str object should be converted into unicode and this is done by `to_str()` automatically. `tenjin.set_template_encoding()` generates correct `to_str()` function therefore you must call it before importing helper functions.

In addition, you must convert output into str object because output will be unicode object.

```python
import tenjin
tenjin.set_template_encoding(decode='utf-8')
from tenjin.helpers import *
engine = tenjin.Engine()
output = engine.render('index.pyhtml')
if isinstance(output, unicode):
    output = output.encode('utf-8')
print(html)
```

You should not add magic comment in your templates, or you will get the following SyntaxError.

```python
## SyntaxError: encoding declaration in Unicode string
<?py # -*- coding: utf-8 -*- ?>
```

> **NOTE:**
>
> When you called `tenjin.set_template_encoding()`, it is strongly recommened to touch template files (= update timestamp of template files) in order to clear template caches.

### Python 3.x

In Python 3.x, string is treated as unicode object. So pyTenjin handles all templates in string base (= unicode base), and bytes data is converted into str by `to_str()` function. If you don't specify any encoding, Tenjin uses 'utf-8' encoding as default.

```python
import tenjin
tenjin.set_template_encoding('cp932')   # or shift_jis
from tenjin.helpers import *
```


## Helper Function

Tenjin provides some modules for helper functions.

### tenjin.helpers module

Module `tenjin.helpers` provides basic helper functions.

**to_str(*value*)**
: Converts value into string. **None is converted into empty string instead of "None".** Unicode object is encoded into string with 'utf-8' encoding name. If you want to use other encoding name, use generate_tostr_func().

  ```python
  >>> from tenjin.helpers import to_str
  >>> to_str(123)
  '123'
  >>> to_str(None)       # None is converted into empty string
  ''
  >>> to_str(u'日本語')  # unicode object is encoded into str
  '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
  ```

  > **NOTE:** The `u'...'` unicode prefix examples above are Python 2.x specific. In Python 3, all strings are unicode by default, so the `u` prefix is unnecessary and `to_str()` simply converts values to `str`.

**escape(*str*)**
: Escape HTML special characters. This is same as `tenjin.html.escape_html()`.

  ```python
  >>> from tenjin.helpers import escape
  >>> escape('< > & " \' ')
  '&lt; &gt; &amp; &quot; &#39; '
  ```

**generate_tostrfunc(*encode*=*encoding*, *decode*=*encoding*)**
: Generate to_str() function with enoding name. (Since version 1.0.0, you don't need to call this directly. Call `tenjin.set_template_encoding()` instead.)

  ```python
  >>> from tenjin.helpers import generate_tostrfunc
  >>> ## generate to_str() function which encodes unicode into binary(=str).
  >>> to_str = generate_tostrfunc(encode='utf-8')
  >>> to_str(u'SOS')
  'SOS'
  >>> ## generate to_str() function which decodes binary(=str) into unicode.
  >>> to_str = generate_tostrfunc(decode='utf-8')
  >>> to_str('SOS')
  u'SOS'
  ```

**echo(*value*)**
: Add value string into _buf. This is similar to echo() function of PHP.

  ```html
  ## add _content into here
  <?py echo(_content) ?>
  ## this is same as #{...} or {==...==}
  #{_content}
  ```

**new_cycle(\**values*)**
: Generates cycle object.

  ```python
  >>> from tenjin.helpers import new_cycle
  >>> cycle = new_cycle('odd', 'even')
  >>> cycle()
  'odd'
  >>> cycle()
  'even'
  >>> cycle()
  'odd'
  >>> cycle()
  'even'
  ```

**cache_as(*key*, *lifetime=0*)**
: Caches fragment of output. See [Fragment Cache](#fragment-cache) for details.

**not_cached(*key*, *lifetime=0*)**
: (OBSOLETE; use cache_as() instead) If fragment is expired or not cached, start caching fragment with *key* and *lifetime* (seconds), and returns True. If fragment is already cached with *key*, returns False. See [Fragment Cache](#fragment-cache) for details.

**echo_cached()**
: (OBSOLETE; use cache_as() instead) Echo cached fragment. If caching is started by not_cached, stop and cache it. This function should be used with not_cached(). See [Fragment Cache](#fragment-cache) for details.

**capture_as(*name*)**
: Capture a part of template. See [Capturing](#capturing) section for details.

**captured_as(*name*)**
: Return True if captured with name. See [Capturing](#capturing) section for details.

**start_capture(*name*), stop_capture()**
: (OSOLETE; use capture_as() instead) Start capturing with specified name. See [Capturing](#capturing) section for details.

**\_P(*value*), \_p(*value*)**
: Helper method for preprocessing. See [Preprocessing](#preprocessing) section for details.

### tenjin.escaped module

Module `tenjin.escaped` provides auto-escaping helpers and classes.

**as_escaped(*string*)**
: Mark *string* as escaped and returns marked string. **Notice that this doesn't escape string at all.** This function just mark string as escaped. See [Auto-escaping](#auto-escaping) section for details.

  ```python
  >>> s = '<p>Hello</p>'
  >>> as_escaped(s)              # not changes string content
  '<p>Hello</p>'
  >>> type(as_escaped(s))        # marks string as escaped
  <class 'tenjin.escaped.EscapedStr'>
  >>> as_escaped(s) == s         # returned value is also string
  True
  ```

**is_escaped(*value*):**
: Return True if *value* is marked as escaped, else False. See [Auto-escaping](#auto-escaping) section for details.

  ```python
  >>> s = '<p>Hello</p>'
  >>> is_escaped(s)              # returns False if string is not marked
  False
  >>> s = as_escaped('<p>Hello</p>')
  >>> is_escaped(s)              # returns True if string is marked as escaped
  True
  ```

**to_escaped(*value*):**
: Convert *value* into string, escape it, and return string which is marked as escaped. If *value* is already escaped, this helper function doesn't escape it any more. See [Auto-escaping](#auto-escaping) section for details.

  ```python
  >>> s = '<p>Hello</p>'
  >>> to_escaped(s)              # escapes html special characters
  '&lt;p&gt;Hello&lt;/p&gt;'
  >>> is_escaped(to_escaped(s))  # returned value is marked as escaped
  True
  >>> to_escaped(123)            # converts any value into string
  '123'
  >>> to_escaped(None)           # converts None into empty string
  ''
  ```

### tenjin.html module

Module `tenjin.html` provides HTML specific helper functions.

**escape_html(*str*)**
: Escapes HTML special characters. Same as `tejin.helpers.escape()`.

  ```python
  >>> escape_html('<>&"')
  '&lt;&gt;&amp;&quot;'
  ```

**checked(*value*)**
: Returns `' checked="checked"'` if value is true value, else returns empty string.

  ```python
  >>> checked(1+1==2)
  ' checked="checked"'
  >>> checked(1+1==3)
  ''
  ```

**selected(*value*)**
: Returns `' selected="selected"'` if value is true value, else returns empty string.

  ```python
  >>> selected(1+1==2)
  ' selected="selected"'
  >>> selected(1+1==3)
  ''
  ```

**disabled(*value*)**
: Returns `' disabled="disabled"'` if value is true value, else returns empty string.

  ```python
  >>> disabled(1+1==2)
  ' disabled="disabled"'
  >>> disabled(1+1==3)
  ''
  ```

**nl2br(*str*)**
: Replaces `"\n"` into `"<br />\n"`.

  ```python
  >>> nl2br("foo\nbar\nbaz\n")
  'foo<br />\nbar<br />\nbaz<br />\n'
  ```

**text2html(*str*)**
: (experimental) Escapes xml characters and replace `"\n"` into `"<br />\n"`.

  ```python
  >>> text2html('<AAA>\nB&B\n"CCC"\n')
  '&lt;AAA&gt;<br />\nB&amp;B<br />\n&quot;CCC&quot;<br />\n'
  ```

**tagattr(*name*, *expr*, *value*=None, *escape*=True)**
: **(experimental)** Returns `' name="value"'` if *expr* is true value, else `''` (empty string). If *value* is not specified, *expr* is used as value instead.

  ```python
  >>> tagattr('name', 'account')
  ' name="account"'
  >>> tagattr('name', None)
  ''
  >>> tagattr('checked', True, 'checked')
  ' checked="checked"'
  ```

**tagattrs(\*\**kwargs*)**
: **(experimental)** Builds html tag attribtes.

  ```python
  >>> tagattrs(klass='main', size=20)
  ' class="main" size="20"'
  >>> tagattrs(klass='', size=0)
  ''
  ```

**nv(*name*, *value*, *sep*=None, \*\**kwargs*)**
: **(experimental)** Builds name and value attributes.

  ```python
  >>> nv('rank', 'A')
  'name="rank" value="A"'
  >>> nv('rank', 'A', '-')
  'name="rank" value="A" id="rank-A"'
  >>> nv('rank', 'A', '-', checked=True)
  'name="rank" value="A" id="rank-A" checked="checked"'
  >>> nv('rank', 'A', '-', klass='error', style='color:red')
  'name="rank" value="A" id="rank-A" class="error" style="color:red"'
  ```

**js_link(*label*, *onclick*, \*\**kwargs*)**
: **(experimental)** Builds `<a onclick="..."></a>` link.

  ```python
  >>> js_link('click', 'alert("OK")', klass='link')
  '<a href="javascript:undefined" onclick="alert(&quot;OK&quot;);return false" class="link">click</a>'
  ```

> **NOTE:**
>
> `tenjin.html` module is renamed to `tenjin.html` since version 1.0.0. But old module name is still available for backward compatibility.
