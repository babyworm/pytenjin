# Tips

## Specify Function Names of escape() and to_str()

It is able to specify function names of `escape()` and `to_str()` which are used in converted Python script.

**main.py**

```python
import tenjin
from tenjin.helpers import *
import html
engine = tenjin.Engine(path=['views'], escapefunc="html.escape", tostrfunc="str")
print(engine.get_template('page.pyhtml').script)
```

**views/page.pyhtml**

```html
<p>
  escaped:     {=value=}
  not escaped: {==value==}
</p>
```

**Result**

```console
$ python main.py
_extend=_buf.extend;_to_str=str;_escape=html.escape; _extend(('''<p>
  escaped:     ''', _escape(_to_str(value)), '''
  not escaped: ''', _to_str(value), '''
</p>\n''', ));
```

If you need faster version of `to_str()` and `escape()`, see [next section](#tips-webext).

## Webext

I have to say that **bottleneck of Tenjin is calling `to_str()` and `escape()`, not string concatenation**. Therefore if you want to make Tenjin much faster, you must make `to_str()` and `escape()` faster (or eliminate calling them).

For example, using `str()` instead of `to_str()` will make Tenjin much faster. The following benchmark result shows that `str()`(= 'tenjin-str') is much faster than `to_str()`(= 'tenjin').

**`str()` is faster than `to_str()`**

```console
$ cd Tenjin-X.X.X/benchmark
$ python -V
Python 2.5.5
$ python bench.py -q -n 10000 tenjin tenjin-str
*** ntimes=10000
                                    utime     stime     total      real
tenjin                             3.7500    0.0400    3.7900    3.7936
tenjin-str                         2.4500    0.0300    2.4800    2.4857
```

But `str()` doesn't return empty string if argument is `None`. In addition `str()` raises UnicodeEncodeError frequently.

Other solution is [Webext](http://pypi.python.org/Webext/). [Webext](http://pypi.python.org/Webext/) is an extension module which implement `to_str()` and `escape()` in C language.

```python
import tenjin
from tenjin.helpers import *
from webext import to_str, escape    # use webext's functions instead of tenjin's
```

Benchmark script in Tenjin already supports Webext. It shows that Webext makes Tenjin much faster especially html escaping.

**Intel CoreDuo2 2GHz, Mac OS X 10.6, Python 2.5.5**

```console
### without html escape
$ cd Tenjin-X.X.X/
$ cd benchmark/
$ python bench.py -q -n 10000 tenjin tenjin-str tenjin-webext
*** ntimes=10000
                                    utime     stime     total      real
tenjin                             3.8100    0.0400    3.8500    3.8462
tenjin-str                         2.4500    0.0200    2.4700    2.4815
tenjin-webext                      2.4500    0.0300    2.4800    2.4825

## with html escape
$ python bench.py -e -q -n 10000 tenjin tenjin-str tenjin-webext
*** ntimes=10000
                                    utime     stime     total      real
tenjin                             7.2900    0.0500    7.3400    7.4669
tenjin-str                         5.7400    0.0400    5.7800    5.8202
tenjin-webext                      2.9700    0.0400    3.0100    3.0079
```

## Template Inheritance

Tenjin doesn't support Template Inheritance which Django template engine does. But you can emulate it by capturing[*1](#fnref1). See [this section](#capturing) for details.

<a name="fnref1"></a>(*1) Notice that capturing is useful but not so powerful than template inheritance.

## Template File Suffix

If you want to change template suffix rule, override Engine#to_filename().

```python
def to_filename(self, template_name):
    ### original
    #if template_name[0] == ':' :
    #    return self.prefix + template_name[1:] + self.postfix
    #return template_name
    ### customize suffix rule:
    ### - ':foo'     => 'foo.html.tjn'
    ### - 'foo.json' => 'foo.json.tjn'
    if template_name[0] == ':':
        return template_name + '.html.tjn'
    return template_name + '.tjn'

tenjin.Engine.to_filename = to_filename
```
