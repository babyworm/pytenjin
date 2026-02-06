# Customization Examples

This section shows how to customize pyTenjin.

**Notice that these customization may be changed in the future release.**

## Template Encoding

```python
tenjin.set_template_encoding('cp932')   # or shift_jis
```

## Escaping Function

```python
tenjin.Template.escapefunc = 'html.escape'
## or
engine = tenjin.Engine(escapefunc='html.escape')
```

## Change Behaviour of `to_str()`

> **NOTE:** The examples below using `u'...'` unicode prefix and the distinction between `str` and `unicode` types are Python 2.x specific. In Python 3, all strings are unicode by default, and `to_str()` simply converts values to `str`.

```python
## encode unicode into str, and unchange str.
to_str = tenjin.helpers.generate_tostrfunc(encode='utf-8')
  # ex.
  #   >>> to_str('日本語')
  #   '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'
  #   >>> to_str(u'日本語')
  #   '\xe6\x97\xa5\xe6\x9c\xac\xe8\xaa\x9e'

## decode str into unicode, and unchange unicode.
to_str = tenjin.helpers.generate_tostrfunc(decode='utf-8')
  # ex.
  #   >>> to_str("日本語")
  #   u'\u65e5\u672c\u8a9e'
  #   >>> to_str(u"日本語")
  #   u'\u65e5\u672c\u8a9e'
```

> **NOTE:**
>
> It is recommended to call `tenjin.set_template_encoding()` instead of calling `tenjin.helpers.generate_tostrfunc()` directly because the former calls the latter internally.

## Embedded Notation

```python
class MyTemplate(tenjin.Template):

    STMT_PATTERN = re.compile(r'<\?py( |\t|\r?\n)(.*?) ?\?>([ \t]*\r?\n)?', re.S)

    def stmt_pattern(self):
        return self.STMT_PATTERN

    EXPR_PATTERN = re.compile(r'([#\$])\{(.*?)\}', re.S)

    def expr_pattern(self):
        return self.EXPR_PATTERN

    def get_expr_and_flags(self, match):
        prefix, expr = match.groups()
        flag_tostr  = True
        flag_escape = prefix == "$"   # escape if prefix is "$"
        return expr, (flag_escape, flag_tostr)

    def add_expr(self, buf, code, *flags):
        flag_escape, flag_tostr = flags
        if   flag_escape: buf.extend(("_escape(_to_str(", code, ")), "))
        elif flag_tostr:  buf.extend((        "_to_str(", code, "), "))
        else:             buf.extend((               "(", code, "), "))

tenjin.Engine.templateclass = MyTemplate
```

## Custom Safe Template

For example you want to use [MarkupSafe](http://pypi.python.org/pypi/MarkupSafe) module[*2](#fnref2):

```python
import tenjin
tenjin.set_template_encoding('utf-8')  # change templates to be unicode-base
from tenjin.helpers import *
from tenjin.html import *

## import Markup
from markupsafe import Markup, escape_silent

## change SafeTemplate to use Markup
tenjin.SafeTemplate.tostrfunc      = 'Markup'
tenjin.SafeTemplate.escapefunc     = 'Markup.escape' # or 'escape_silent'
tenjin.SafePreprocessor.tostrfunc  = 'Markup'
tenjin.SafePreprocessor.escapefunc = 'Markup.escape' # or 'escape_silent'

## change safe helpers to use Markup
import tenjin.escape
tenjin.escaped.is_escaped = lambda x: isinstance(x, Markup)
tenjin.escaped.as_escaped = Markup
tenjin.escaped.to_escaped = Markup.escape # or escape_silent
from tenjin.escaped import is_escaped, as_escaped, to_escaped
```

> **NOTE:**
>
> You must call `tenjin.set_template_encoding()` to change pyTenjin to be unicode-based because MarkupSafe requires it.

<a name="fnref2"></a>(*2) MarkupSafe is a module to enable auto-escape on Jinja2 or other python products.

## Custom Html Helper Function

```python
from tenjin.escaped import as_escaped, to_escaped

def js_link(label, onclick):
    html = '<a href="javascript:undefined" onclick="%s;return false">%s</a>' % \
              (to_escaped(onclick), to_escaped(label))
    return as_escaped(html)
```

## Switch Default Template Class

```python
tenjin.Engine.templateclass = MyTemplate
tenjin.Engine.preprocessorclass = MyPreprocessor
#
tenjin.SafeEngine.templateclass = MySafeTemplate
tenjin.SafeEngine.preprocessorclass = MySafePreprocessor
```

## Change Template Loader

```python
class MyFileSystemLoader(tenjin.FileSystemLoader):
   def load(self, filepath):
     ...

tenjin.Engine.loader = MyFileSystemLoader()
## or
engine = tenjin.Engine(finder=MyFileSystemLoader())
```

## Change Template Cache Storage

```python
tenjin.Engine.cache = tenjin.MemoryCacheStorage()
## or
engine = tenjin.Engine(cache=tenjin.MemoryCacheStorage())
```

## Change Fragment Cache Store

```python
if not os.path.isdir('cache.d'):
    os.mkdir('cache.d')
kv_store = tenjin.FileBaseStore('cache.d')      # file based
tenjin.helpers.fragment_cache.store = kv_store
```
