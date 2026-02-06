# Troubleshooting

## I got an SyntaxError exception.

Command-line option '-z' checks syntax of template file. You should check template by it.

File 'syntaxerr.pyhtml':

```html
<?py #@ARGS ?>
<?py for i in range(0, 10): ?>
<?py     if i % 2 == 0: ?>
{==i==} is even.
<?py     else ?>
{==i==} is odd.
<?py     #endif ?>
<?py #endfor ?>
```

Result:

```console
$ pytenjin -z syntaxerr.pyhtml
syntaxerr.pyhtml:5:12: invalid syntax
  5:         else
                ^
```

## I got 'SyntaxError: encoding declaration in Unicode string'

> **NOTE:** This issue is primarily relevant to Python 2.x. In Python 3, templates are always unicode-based, so encoding declarations in templates are generally unnecessary.

This is because you added magic comment (such as `<?py # -*- coding: utf-8 -*- ?>`) in template file AND you specified template encoding by `tenjin.set_template_encoding()` or pass encoding option to `tenjin.Engine()`.

Solution:

- If you called `tenjin.set_template_encoding()`, remove magic comment.
- If you want to add magic comment, call `tenjin.set_template_encoding()` with `encode` option, or don't call it.

## I got UnicodeDecodeError, but I can't find what is wrong

> **NOTE:** This issue is primarily relevant to Python 2.x, where mixing `str` and `unicode` types frequently caused encoding errors. In Python 3, strings are always unicode, making these errors much less common.

If you got UnicodeDecodeError, you should do the following solutions.

- Set logger to `tenjin.logger`. If you set, Tenjin will report the content of `_buf`.

  ```python
  import logging
  logging.basicConfig(level=logging.DEBUG)
  tenjin.logger = logging
  ```

- Render tempalte with specifying `_buf` and check it directly.

  ```python
  _buf = []
  try:
      engine.get_template("index.pyhtml").render(context, _buf=_buf)
      print(''.join(_buf))
  except UnicodeDecodeError:
      for item in _buf:
          if isinstance(item, str):
              try:
                  str.decode('ascii')
              except UnicodeDecodeError:
                  print("*** failed to decode: %s" % repr(item))
  ```

## NameError: global name 'xxxx' is not defined

Assume the following template file.

```html
<?py

values = {'A': 10, 'B': 20}

def getval(key):
  return values.get(key, None)
#end

?>
<p>getval('A') = {=getval('A')=}</p>
```

This will raise NameError, such as:

```console
$ python ex.py
Traceback (most recent call last):
  File "ex.py", line 5, in <module>
    output = engine.render('ex.pyhtml', context)
  File "tenjin.py", line 1582, in render
    content  = template.render(context, globals)
  File "tenjin.py", line 941, in render
    exec(self.bytecode, globals, locals)
  File "ex.pyhtml", line 10, in <module>
    <p>getval('A') = ${getval('A')}</p>
  File "ex.pyhtml", line 6, in getval
    return values.get(key, None)
 NameError: global name 'values' is not defined
```

This is a restriction of Tenjin.

Workaround:

- Pass values as default value of argument.

```html
<?py

values = {'A': 10, 'B': 20}

def getval(key, _values=values):   # works very well!
  return _values.get(key, None)
#end

?>
<p>getval('A') = {=getval('A')=}</p>
```
