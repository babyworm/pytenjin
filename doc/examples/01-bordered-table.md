# Bordered Table

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
