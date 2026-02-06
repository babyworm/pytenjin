# pytenjin Command

See '`pytenjin -h`' for details.

## Syntax Check

Command-line option '`-z`' checks syntax of template files.

**example.pyhtml**

```html
<ul>
<?py for item in items: ?>
 <li>{=item=}</li>
<?py #endif ?>
</ul>
```

**Result:**

```console
$ pytenjin -z example.pyhtml
example.pyhtml:4:1: '#endfor' expected but got '#endif'.
   4: #endif
      ^
```

Error message is the same format as gcc compiler or java compiler. Error jump in Emacs or other editor is available.

Command-line option '-q' (quiet-mode) prints nothing if there are no syntax errors.

## Convert Template into Python Script

Command-line option '-s' converts template file into Python script code.

**example.pyhtml**

```html
<ul>
  <?py for item in items: ?>
  <li>{=item=}</li>
  <?py #endfor ?>
</ul>
```

**Result (-s)**

```console
$ pytenjin -s example.pyhtml
_buf = []; _extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<ul>\n''', ));
for item in items:
    _extend(('''  <li>''', _escape(_to_str(item)), '''</li>\n''', ));
#endfor
_extend(('''</ul>\n''', ));
print(''.join(_buf))
```

Option '-b' removes preamble ('`_buf = []`') and postamble ('`print "".join(_buf))`').

**Result (-sb)**

```console
$ pytenjin -sb example.pyhtml
_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''<ul>\n''', ));
for item in items:
    _extend(('''  <li>''', _escape(_to_str(item)), '''</li>\n''', ));
#endfor
_extend(('''</ul>\n''', ));
```

## Retrieve Embedded Code

Tenjin allows you to retrieve embedded code from template files in order to help template debugging.

It is hard to debug large template files because HTML and embedded code are mixed in a file. Retrieving embedded code from template files will help you to debug large template files.

Assume the following template file.

**example.pyhtml**

```html
<table>
  <?py i = 0 ?>
  <?py for item in items: ?>
  <?py     i += 1 ?>
  <tr>
    <td>{==i==}</td>
    <td>{=item=}</td>
  </tr>
  <?py #endfor ?>
</table>
```

Option '-S' (or '-a retrieve') retrieves embedded codes.

**Result (-Sb)**

```console
$ pytenjin -Sb example.pyhtml
_extend=_buf.extend;_to_str=to_str;_escape=escape;
i = 0
for item in items:
    i += 1

    _to_str(i);
    _escape(_to_str(item));

#endfor
```

Option '-X' (or '-a statements') retrieves only statements.

**Result (-Xb)**

```console
$ pytenjin -Xb example.pyhtml
_extend=_buf.extend;_to_str=to_str;_escape=escape;
i = 0
for item in items:
    i += 1




#endfor
```

Option '-N' adds line numbers.

**Result (-NXb)**

```console
$ pytenjin -NXb example.pyhtml
    1:  _extend=_buf.extend;_to_str=to_str;_escape=escape;
    2:  i = 0
    3:  for item in items:
    4:      i += 1
    5:
    6:
    7:
    8:
    9:  #endfor
   10:
```

Option '-U' (unique) compress empty lines.

**Result (-UNXb)**

```console
$ pytenjin -UNXb example.pyhtml
    1:  _extend=_buf.extend;_to_str=to_str;_escape=escape;
    2:  i = 0
    3:  for item in items:
    4:      i += 1

    9:  #endfor
```

Option '-C' (compact) removes empty lines.

**Result (-CNXb)**

```console
$ pytenjin -CNXb example.pyhtml
    1:  _extend=_buf.extend;_to_str=to_str;_escape=escape;
    2:  i = 0
    3:  for item in items:
    4:      i += 1
    9:  #endfor
```

## Execute Template File

You can execute template file in command-line.

**example.pyhtml**

```html
<?py items = ['<AAA>', 'B&B', '"CCC"'] ?>
<ul>
  <?py for item in items: ?>
  <li>{=item=}</li>
  <?py #endfor ?>
</ul>
```

**Result**

```console
$ pytenjin example.pyhtml
<ul>
  <li>&lt;AAA&gt;</li>
  <li>B&amp;B</li>
  <li>&quot;CCC&quot;</li>
</ul>
```

## Context Data

You can specify context data with command-line option '`-c`'.

**example.pyhtml**

```html
<ul>
  <?py for item in items: ?>
  <li>{=item=}</li>
  <?py #endfor ?>
</ul>
```

**Result**

```console
$ pytenjin -c 'items=["A","B","C"]' example.pyhtml
<ul>
  <li>A</li>
  <li>B</li>
  <li>C</li>
</ul>
```

If you want to specify several values, separate them by ';' such as '-c "x=10; y=20"'.

If you installed PyYAML library, you can specify context data in YAML format. Tenjin regards context data string as YAML format if it starts with '{'.

**Result**

```console
$ pytenjin -c '{items: [A, B, C]}' example.pyhtml
<ul>
  <li>A</li>
  <li>B</li>
  <li>C</li>
</ul>
```

In addition, Tenjin supports context data file in Python format or YAML format.

**context.py**

```python
items = [
   "AAA",
   123,
   True,
]
```

**Result**

```console
$ pytenjin -f context.py example.pyhtml
<ul>
  <li>AAA</li>
  <li>123</li>
  <li>True</li>
</ul>
```

**context.yaml**

```yaml
items:
  - AAA
  - 123
  - true
```

**Result**

```console
$ pytenjin -f context.yaml example.pyhtml
<ul>
  <li>AAA</li>
  <li>123</li>
  <li>True</li>
</ul>
```
