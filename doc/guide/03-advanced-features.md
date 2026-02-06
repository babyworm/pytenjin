# Advanced Features

## Auto-escaping

Tenjin provides `SafeTemplate` and `SafeEngine` class which enforces HTML escape. These are similar to Django's feature or Jinja2's autoescape feature.

**The point of these classes is that you can control whether escape html or not by data type, not by embedded notation.**

See the following example.

**safe-test.py**

```python
import tenjin
from tenjin.helpers import *
from tenjin.escaped import is_escaped, as_escaped, to_escaped

## both are same notation
input = r"""
a = ${a}
b = ${b}
"""

## but passed different data type
context = {
    "a": "<b>SOS</b>",
    "b": as_escaped("<b>SOS</b>"),
}

## SafeTemplate will escape 'a' but not 'b'
template = tenjin.SafeTemplate(input=input)
print(template.script)
print("---------------------")
print(template.render(context))
```

The follwoing output shows that:

- `SafeTemplate` and `SafeEngine` classes uses `to_escaped()` instead of `escape()` to escape value.
- Normal string (= `"<b>SOS</b>"`) is escaped automatically, but the other string which is marked as escaped (= `as_escaped("<b>SOS</b>")`) is not escaped. This means that you can controll escape by data type, not embedded notation.

**Output example**

```console
$ python safe-test.py
_extend=_buf.extend;_to_str=to_str;_escape=to_escaped; _extend(('''
a = ''', _escape(a), '''
b = ''', _escape(b), '''\n''', ));

---------------------

a = &lt;b&gt;SOS&lt;/b&gt;
b = <b>SOS</b>
```

See [tenjin.escaped module](#tenjin-escaped) section for details about `as_escaped()` and `to_escaped()`.

In addition, `SafeTemplate`/`SafeEngine` classes inhibits `#{...}` because some people mistake it with `${...}` and it can be XSS security hole in the result. Use `{==...==}` instead of `#{...}`.

|                | Template, Engine          | SafeTemplate, SafeEngine  |
|----------------|---------------------------|---------------------------|
| Escape html    | `${...}` or `{=...=}`    | `${...}` or `{=...=}`    |
| Not escape     | `#{...}` or `{==...==}`  | only `{==...==}`          |

## Nested Layout Template

It is able to nest several layout template files.

**views/\_site\_layout.pyhtml**

```html
<?py #@ARGS _content ?>
<html>
  <body>
#{_content}
  </body>
</html>
```

**views/\_blog\_layout.pyhtml**

```html
<?py #@ARGS _content, title ?>
<?py _context['_layout'] = '_site_layout.pyhtml' ?>
<h2>${title}</h2>
<!-- content -->
#{_content}
<!-- /content -->
```

**views/blog\_post.pyhtml**

```html
<?py #@ARGS post_content ?>
<?py _context['_layout'] = '_blog_layout.pyhtml' ?>
<div class="article">
#{text2html(post_content)}
</div>
```

**main.py**

```python
import tenjin
from tenjin.helpers import *
from tenjin.html import text2html
engine = tenjin.Engine(path=['views'])
context = {
    'title': 'Blog Post Test',
    'post_content': "Foo\nBar\nBaz",
}
html = engine.render('blog_post.pyhtml', context)
print(html)
```

**Result**

```console
$ python main.py
<html>                        # by _layout.pyhtml
  <body>                      #       :
<h2>Blog Post Test</h2>       #   by _blog_layout.pyhtml
<!-- content -->              #         :
<div class="article">         #     by blog_post.pyhtml
Foo<br />                     #           :
Bar<br />                     #           :
Baz                           #           :
</div>                        #           :
                              #           :
<!-- /content -->             #   by _blog_layout.pyhtml
                              #         :
  </body>                     # by _layout.pyhtml
</html>                       #       :
```

## Trace Templates

If you pass '`trace=True`' to tenjin.Template class or tenjin.Engine class, Template class will print template file name at the beginning and end of output.

For example:

**trace-example.py**

```python
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine(layout='layout.pyhtml', trace=True)
output = engine.render('main.pyhtml', {'items': ['A','B','C']})
print(output)
```

Will print:

```console
$ python trace-example.py
<!-- ***** begin: layout.pyhtml ***** -->
<html>
  <body>
    <div class="content">
<!-- ***** begin: main.pyhtml ***** -->
<ul>
  <li>A</li>
  <li>B</li>
  <li>C</li>
</ul>
<!-- ***** end: main.pyhtml ***** -->
    </div>
  </body>
</html>
<!-- ***** end: layout.pyhtml ***** -->
```

This feature is very useful when debugging to detect template file name from HTML output.

If you like it, you can make it always enabled.

```python
## trace is always enabled
tenjin.Engine.trace = True
```

## Capturing

It is able to capture parital of output. You can use this feature as an alternative of Django's template-inheritance.

**views/blog-post.pyhtml : one partial capture ('sidebar')**

```html
<?py ## from __future__ import with_statement  -- Not needed in Python 3 ?>
<?py #@ARGS blog_post, recent_posts ?>
<h2>#{blog_post['title']}</h2>
<div class="blog-post">
#{text2html(blog_post['content'])}
</div>

<?py with capture_as('sidebar'): ?>
<h3>Recent Posts</h3>
<ul>
<?py for post in recent_posts: ?>
  <a href="/blog/#{post['id']}">${post['title']}</a>
<?py #endfor ?>
</ul>
<?py #endwith ?>
```

> **NOTE:**
>
> `capture_as()` supports both with-statement and for-statement. If you are using Python 2.4, change `with capture_as("sidebar"): ... #endwith` to `for _ in capture_as("sidebar"): ... #endfor`.

**views/\_layout.pyhtml : two placeholders ('header' and 'sidebar')**

```html
<html>
  <body>
    <div id="header-part">
    <?py if not captured_as('header'): ?>
      <h1>My Great Blog</h1>
    <?py #endif ?>
    </div>
    <div id="main-content">
#{_content}
    </div>
    <div id="sidebar-part">
    <?py if not captured_as('sidebar'): ?>
      <h3>Links</h3>
      <ul>
        <a href="http://google.com/">Google</a>
        <a href="http://yahoo.com/">Yahoo!</a>
      </ul>
    <?py #endif ?>
    </div>
  </body>
</html>
```

**main.py**

```python
## context data
blog_post = {
  'title': 'Tenjin is Great',
  'content': """
Tenjin has great features.
- Very Fast
- Full Featured
- Easy to Use
"""[1:]
}
recent_posts = [
  {'id': 1, 'title': 'Tenjin is Fast' },
  {'id': 2, 'title': 'Tenjin is Full-Featured' },
  {'id': 3, 'title': 'Tenjin is Easy-to-Use' },
]
context = {
  'blog_post': blog_post,
  'recent_posts': recent_posts,
}

## render template
import tenjin
from tenjin.helpers import *
from tenjin.html import text2html
engine = tenjin.Engine(path=['views'], layout='_layout.pyhtml')
html = engine.render('blog-post.pyhtml', context)
print(html)
```

The result shows that captured string (with name 'sidebar') overwrites layout template content.

**Result : only 'sidebar' placeholder is overwritten by capturing.**

```
$ python main.py
<html>
  <body>
    <div id="header-part">
      <h1>My Great Blog</h1>
    </div>
    <div id="main-content">
<h2>Tenjin is Great</h2>
<div class="blog-post">
Tenjin has great features.<br />
- Very Fast<br />
- Full Featured<br />
- Easy to Use<br />

</div>


    </div>
    <div id="sidebar-part">
<h3>Recent Posts</h3>
<ul>
  <a href="/blog/1">Tenjin is Fast</a>
  <a href="/blog/2">Tenjin is Full-Featured</a>
  <a href="/blog/3">Tenjin is Easy-to-Use</a>
</ul>
    </div>
  </body>
</html>
```

> **NOTE:**
>
> `start_capture()` and `stop_capture()` are still available but obsolete.

## Template Cache

Tenjin converts template file into Python script and save it as cache file. By default, it is saved as template-filename + '.cache' in bytecode format. You can change this behaviour by setting `tenjin.Engine.cache` or passing cache object to `tenjin.Engine` object.

For example, if you want to cache template object but want not to create '*.cache' file, use `tenjin.MemoryCacheStorage` object.

**example to change template caching**

```python
import tenjin
from tenjin.helpers import *

## change to store template cache into memory instead of file system
tenjin.Engine.cache = tenjin.MemoryCacheStorage()
engine = tenjin.Engine()

## or
engine = tenjin.Engine(cache=tenjin.MemoryCacheStorage())
```

## Fragment Cache

You can cache a certain part of HTML to improve performance. This is called as Fragment Cache.

**views/items.pyhtml**

```html
<?py #@ARGS get_items ?>
<div>
  <?py # fragment cache with key ('items/1') and lifetime (60sec) ?>
  <?py for _ in cache_as('items/1', 60): ?>
  <ul>
    <?py     for item in get_items(): ?>
    <li>${item}</li>
    <?py     #endfor ?>
  </ul>
  <?py #endfor ?>
</div>
```

Tenjin stores fragments caches into memory by default. If you want to change or customize cache store, see the following example.

**main.py**

```python
import os, tenjin
from tenjin.helpers import *

## create key-value store object
if not os.path.isdir('cache.d'): os.mkdir('cache.d')
kv_store = tenjin.FileBaseStore('cache.d')      # file based

## set key-value store into tenjin.helpers.fagment_cache object
tenjin.helpers.fragment_cache.store = kv_store

## context data
## (it is strongly recommended to create function object
##  to provide pull-style context data)
def get_items():   # called only when cache is expired
    return ['AAA', 'BBB', 'CCC']
context = {'get_items': get_items}

## render html
engine = tenjin.Engine(path=['views'])
html = engine.render('items.pyhtml', context)
print(html)
```

**Result**

```console
$ python main.py
<div>
  <ul>
    <li>AAA</li>
    <li>BBB</li>
    <li>CCC</li>
  </ul>
</div>
```

You'll find that HTML fragment is cached into cache directory. This cache data will be expired at 60 seconds after.

```console
$ cat cache.d/items/1
  <ul>
    <li>AAA</li>
    <li>BBB</li>
    <li>CCC</li>
  </ul>
```

> **NOTE:**
>
> `not_cached()` and `echo_cached()` are still available but obsolete.

## Logging

If you set logging object to `tenjin.logger`, pyTenjin will report loading template files.

For example:

**ex-logger.py**

```python
import tenjin
from tenjin.helpers import *

## set logging object
import logging
logging.basicConfig(level=logging.INFO)
tenjin.logger = logging

engine = tenjin.Engine()
context = {'name': 'World'}
html = engine.render('example.pyhtml', context)
#print(html)
```

If you run it first time, Tenjin will report that template object is stored into cache file.

```console
$ python ex-logger.py
INFO:root:[tenjin.TextCacheStorage] store cache (file='/home/user/example.pyhtml.cache')
```

And if you run it again, Tenjin will report that template object is loaded from cache file.

```console
$ python ex-logger.py
INFO:root:[tenjin.TextCacheStorage] load cache (file='/home/user/example.pyhtml.cache')
```

## Google App Engine Support

> **NOTE:** Google App Engine's legacy runtime (webapp framework) used in these examples is no longer supported. This section is kept for historical reference. The `tenjin.gae` module may not work with modern App Engine environments.

Tenjin supports Google App Engine. All you have to do is just call `tenjin.gae.init()`.

```python
import tenjin
from tenjin.helpers import *
import tenjin.gae; tenjin.gae.init()

## it is recommended to configure logging
import logging
logging.basicConfig(level=logging.DEBUG)
tenjin.logger = logging
```

You can see [source code](examples.html#gae) of GAE example using Tenjin.

`tenjin.gae.init()` do the followings internally.

```python
## change tenjin.Engine to cache template objects into memcache service
## (using CURRENT_VERSION_ID as namespace).
ver = os.environ.get('CURRENT_VERSION_ID', '1.1')#.split('.')[0]
Engine.cache = tenjin.gae.GaeMemcacheCacheStorage(namespace=ver)
## change fragment cache store to use memcache service
fragcache = tenjin.helpers.fragment_cache
fragcache.store    = tenjin.gae.GaeMemcacheStore(namespace=ver)
fragcache.lifetime = 60    #  1 minute
fragcache.prefix   = 'fragment.'
```

> **NOTE:**
>
> Google App Engine shares memcache in any version. In other words, Google App Engine doesn't allow to separate memcache for each version. This means that **memcache data can be conflict between old and new version application in Google App Engine**. Tenjin avoids this confliction by using version id as namespace.

## M17N Page

If you have M17N site, you can make your site faster by Tenjin.

In M17N-ed site, message translation function (such as `_('message-key')`) is called many times. Therefore if you can eliminate calling that function, your site can be faster.

> **NOTE:**
>
> This feature is implemented with preprocessing feature. See [this section](#preprocessing) for details about preprocessing.

The points are:

- Change cache filename according to language. For example, create cache file 'file.pyhtml.en.cache', 'file.pyhtml.fr.cache', 'file.pyhtml.it.cache', and so on from a template file 'file.pyhtml'. This is done by Tenjin automatically if you pass '`lang="en"`' or '`lang="fr"`' option to Engine class.
- Create Engine object for each language and pass `lang` option respectively.
- Enable preprocessing to create different cache content for each language.

The following is an example to generate M17N pages from a template file.

**m17n.pyhtml:**

```html
<div>
<?PY ## '_()' represents translator method ?>
 <p>${{_('Hello')}} ${username}!</p>
</div>
```

**m17n.py:**

```python
# -*- coding: utf-8 -*-
import tenjin
from tenjin.helpers import *
import re

##
## message catalog to translate message
##
MESSAGE_CATALOG = {
    'en': { 'Hello': 'Hello',
            'Good bye': 'Good bye',
          },
    'fr': { 'Hello': 'Bonjour',
            'Good bye': 'Au revoir',
          },
}

##
## create translation function and return it.
## ex.
##    _ = create_m17n_func('fr')
##    print _('Hello')   #=> 'Bonjour'
##
def create_m17n_func(lang):
    dct = MESSAGE_CATALOG.get(lang)
    if not dct:
        raise ValueError("%s: unknown lang." % lang)
    def _(message_key):
        return dct.get(message_key)
    return _
    # or return dct.get

##
## test program
##
if __name__ == '__main__':

    ## render html for English
    engine_en = tenjin.Engine(preprocess=True, lang='en')
    context = { 'username': 'World' }
    context['_'] = create_m17n_func('en')
    html = engine_en.render('m17n.pyhtml', context)
    print("--- lang: en ---")
    print(html)

    ## render html for French
    engine_fr = tenjin.Engine(preprocess=True, lang='fr')
    context = { 'username': 'World' }
    context['_'] = create_m17n_func('fr')
    html = engine_fr.render('m17n.pyhtml', context)
    print("--- lang: fr ---")
    print(html)
```

**Result:**

```console
$ python m17n.py
--- lang: en ---
<div>
 <p>Hello World!</p>
</div>

--- lang: fr ---
<div>
 <p>Bonjour World!</p>
</div>
```

After that, you can find two cache files are created.

```console
$ ls m17n.pyhtml*
m17n.pyhtml    m17n.pyhtml.en.cache    m17n.pyhtml.fr.cache
```

And each cache files have different content.

**`_('Hello')` is translated into "Hello" in Engilish cache file**

```console
$ cat m17n.pyhtml.en.cache
timestamp: 1329291933.0

_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<div>
 <p>Hello ''', _escape(_to_str(username)), '''!</p>
</div>\n''', ));
```

**`_('Hello')` is translated into "Bonjour" in French cache file**

```console
$ cat m17n.pyhtml.fr.cache
timestamp: 1329291933.0

_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<div>
 <p>Bonjour ''', _escape(_to_str(username)), '''!</p>
</div>\n''', ));
```
