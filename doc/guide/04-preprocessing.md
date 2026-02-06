# Preprocessing

Tenjin supports template preprocessing.

## What is Preprocessing?

Preprocessing is a mechanism to manipulate template content when loading template file.

For example, Tenjin provides TrimPreprocessor class which trims spaces in HTML templates. Using it, you can elminiate size of html output.

**Preprocessing example by TrimPreprocessor**

```html
## Original html template
<div>
  <ul>
    <?py for item in items: ?>
    <li>${item}</li>
    <?py #endfor ?>
  </ul>
</div>

## Preprocessed template when loading
<div>
<ul>
<?py for item in items: ?>
<li>${item}</li>
<?py #endfor ?>
</ul>
</div>

## Output example
<div>
<ul>
<li>Foo</li>
<li>Bar</li>
<li>Baz</li>
</ul>
</div>
```

Tenjin provides the following preprocessor classses. See the succeeding sections for details about these classes.

**TemplatePreprocessor**
: Execute any logic or code in advance. Same as 'preprocess' option.

**TrimPreprocessor**
: Trims spaces at the beginning of lines.

**PrefixedLinePreprocessor**
: Converts '`:: ...`' lines into '`<?py ... ?>`'.

**JavaScriptPreprocessor**
: Generates client-side template code.

If you want preprocessing, pass instance objects of these classes to engine object.

**How to use preprocessors**

```python
import tenjin
from tenjin.helpers import *
pp = [
  tenjin.TemplatePreprocessor(),      # same as preprocess=True
  tenjin.TrimPreprocessor(),          # trim spaces before tags
  tenjin.PrefixedLinePreprocessor(),  # convert ':: ...' into '<?py ... ?>'
  tenjin.JavaScriptPreprocessor(),    # allow to embed client-side template
]
engine = tenjin.Engine(pp=pp)
context = {'items': ["Haruhi", "Mikuru", "Yuki"]}
html = engine.render('example.pyhtml', context)
```

## TrimPreprocessor class

TrimPreprocessor trims spaces before tags in order to eliminate size of output.

For examle, the follwoing template file:

```html
<div>
  <ul>
    <?py for item in items: ?>
    <li>${item}</li>
    <?py #endfor ?>
  </ul>
</div>
```

will generate the following output:

```
<div>
<ul>
<li>Haruhi</li>
<li>Mikuru</li>
<li>Yuki</li>
</ul>
</div>
```

with the following code:

```python
import tenjin
from tenjin.helpers import *
pp = [ tenjin.TrimPreprocessor() ]
engine = tenjin.Engine(pp=pp)
context = { 'items': ["Haruhi", "Mikuru", "Yuki"] }
html = engine.render('example.pyhtml', context)
print(html)
```

> **NOTE:**
>
> The default of TrimPreprocessor trims spaces on lines which starts with '<'.
>
> ```html
> <div>
>   <pre>       ## spaces will be trimmed
>     x = 10    ## spaces will NOT be trimmed
>   </pre>      ## spaces will be trimmed
> </pre>
> ```
>
> If you want to trim all spaces, try `TrimPreprocessor(True)`.

## PrefixedLinePreprocessor class

PrefixedLinePreprocessor converts '`:: ...`' into '`<?py ... ?>`'.

For examle, the follwoing template file:

```html
<div>
  <ul>
    :: for item in items:
    <li>${item}</li>
    :: #endfor
  </ul>
</div>
```

is converted into:

```html
<div>
  <ul>
    <?py for item in items: ?>
    <li>${item}</li>
    <?py #endfor ?>
  </ul>
</div>
```

and will generate the following output:

```
<div>
  <ul>
    <li>Haruhi</li>
    <li>Mikuru</li>
    <li>Yuki</li>
  </ul>
</div>
```

with the following code:

```python
import tenjin
from tenjin.helpers import *
pp = [ tenjin.PrefixedLinePreprocessor() ]
engine = tenjin.Engine(pp=pp)
context = { 'items': ["Haruhi", "Mikuru", "Yuki"] }
html = engine.render('example.pyhtml', context)
print(html)
```

> **NOTE:**
>
> Notice that space after '::' is necessary!
>
> ```
> :: x = 10    # OK
> ::x = 10     # NG
> ```

## JavaScriptPreprocessor class

JavaScriptPreprocessor class enables you to embed client-side template code in your template file.

**example.pyhtml**

```html
<html>
  <body>
    <div id="placeholder">
      <!-- #JS: render_table(items) -->
      <table>
        <tbody>
          <?js for (var i = 0, n = items.length; i < n; i++) { ?>
          <?js     var klass = i % 2 ? 'even' : 'odd'; ?>
          <tr class="#{klass}">
            <td>${items[i]}</td>
          </tr>
          <?js } ?>
        </tbody>
      </table>
      <!-- #/JS -->
    </div>
    <script>#{tenjin.JS_FUNC}</script>
    <script>
/// example code to render table
(function() {
   var items = ["Haruhi", "Mikuru", "Yuki"];
   var e = document.getElementById('placeholder');
   e.innerHTML = render_table(items);
 })();
    </script>
  </body>
</html>
```

**Example (pp-javascript.py)**

```python
import tenjin
from tenjin.helpers import *
pp = [ tenjin.JavaScriptPreprocessor() ]
## or pp = [ tenjin.JavaScriptPreprocessor(type='text/javascript') ]
engine = tenjin.Engine(pp=pp)
context = { 'items': ["Haruhi", "Mikuru", "Yuki"] }
html = engine.render('example.pyhtml', context)
print(html)
```

**Output example**

```console
$ python pp-javascript.py
<html>
  <body>
    <div id="placeholder">
      <script>function render_table(items){var _buf='';
_buf+='      <table>\n\
        <tbody>\n';
           for (var i = 0, n = items.length; i < n; i++) {
               var klass = i % 2 ? 'even' : 'odd';
_buf+='          <tr class="'+_S(klass)+'">\n\
            <td>'+_E(items[i])+'</td>\n\
          </tr>\n';
           }
_buf+='        </tbody>\n\
      </table>\n';
      return _buf;};</script>
    </div>
    <script>function _S(x){return x==null?'':x;}
function _E(x){return x==null?'':typeof(x)!=='string'?x:x.replace(/[&<>"']/g,_EF);}
var _ET={'&':"&amp;",'<':"&lt;",'>':"&gt;",'"':"&quot;","'":"&#039;"};
function _EF(c){return _ET[c];};</script>
    <script>
/// example code to render table
(function() {
   var items = ["Haruhi", "Mikuru", "Yuki"];
   var e = document.getElementById('placeholder');
   e.innerHTML = render_table(items);
 })();
    </script>
  </body>
</html>
```

According to HTML syntax, `<script>` tag can be appeared in limited place. But client-side template code will work well even in the case that `<script>` is appeared in non-valid place.

```html
### OK (valid as HTML)
<div>
  <script>function render_table(items){var _buf='';
 _buf += '  <table>\n\
    <tbody>\n';
    ....
 _buf += '    </tbody>\n\
  </table>\n';
  return _buf;</script>
</div>

### NG (not valid as HTML because <script> tag can't be appreared
### in <table> or <tbody> tag, but this code works well in browser)
<div>
  <table>
    <tbody>
      <script>function render_table(items) {var _buf='';
    ....
  return _buf;</script>
    </tbody>
  </table>
</div>
```

In this moment it is not possible to nest client-side template code.

```html
## NOT AVAILABLE!!
<!-- #JS: render_table(items) -->
<table>
  <tbody>
    <?js for (var i = 0, n = items.length; i < n; i++) { ?>
    <!-- #JS: render_raw(item) -->
    <tr>
      <td>${item}</td>
    </tr>
    <!-- #/JS -->
    <?js } ?>
  </tbody>
</table>
<!-- #/JS -->
```

## TemplatePreprocessor class

`TemplatePreprocessor` class allows you to execute some logics when templates are compiled into script, and these logics are not executed when rendering.

> **NOTE:**
>
> `preprocess` option for Engine class is still available for backward compatibility.

`TemplatePreprocessor` class makes your application faster, because some logics are executed on compiling stage, not on rendering stage.

Notation of preprocessing with `TemplatePreprocessor` class:

**`<?PY ... ?>`**
: Preprocessing statement.

**`${{...}}` or `{#=...=#}`**
: Preprocessing expression (with HTML escape)

**`#{{...}}` or `{#==...==#}`**
: Preprocessing expression (without HTML escape)

The following shows difference between `${...}` and `${{...}}`.

**views/pp-example1.pyhtml**

```html
## normal expression
value = ${value}
## with preprocessing
value = ${{value}}
```

**pp-example1.py**

```python
value = 'My Great Example'

## create engine object with preprocessing enabled
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine(path=['views'], preprocess=True)

## print Python script code
print("------ converted script ------")
print(engine.get_template('pp-example1.pyhtml').script)

## render html
html = engine.render('pp-example1.pyhtml', {})
print("------ rendered html ------")
print(html)
```

**Result: notice that `${{...}}` is evaluated at template converting stage.**

```console
$ python pp-example1.py
------ converted script ------
_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''## normal expression
value = ''', _escape(_to_str(value)), '''
## with preprocessing
value = My Great Example\n''', ));

------ rendered html ------
## normal expression
value = My Great Example
## with preprocessing
value = My Great Example
```

You can confirm preprocessed template by '`pytenjin -P`' command.

**Preprocessed template**

```console
$ pytenjin -P -c 'value="My Great Example"' views/pp-example1.pyhtml
## normal expression
value = ${value}
## with preprocessing
value = My Great Example
```

If you want to see preprocessing script (not preprocessed script), use '`pytenjin -sP`' command.

```console
$ pytenjin -sP -c 'value="My Great Example"' views/pp-example1.pyhtml
_buf = []; _extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''## normal expression
value = ${value}
## with preprocessing
value = ''', _escape(_to_str(_decode_params(value))), '''\n''', ));
print(''.join(_buf))
```

### Loop Expantion

It is possible to evaluate some logics by '`<?PY ... ?>`' when convert template into Python script code. For example, you can expand loop in advance to improve performance.

**views/pp-example2.pyhtml**

```html
<?PY states = { "CA": "California", ?>
<?PY            "NY": "New York", ?>
<?PY            "FL": "Florida",  ?>
<?PY            "TX": "Texas",  ?>
<?PY            "HI": "Hawaii", } ?>
<?PY # ?>
<?py chk = { params['state']: ' selected="selected"' } ?>
<?PY codes = list(states.keys()) ?>
<?PY codes.sort() ?>
<select name="state">
  <option value="">-</option>
  <?PY for code in codes: ?>
  <option value="#{{code}}"#{chk.get('#{{code}}', '')}>${{states[code]}}</option>
  <?PY #endfor ?>
</select>
```

Preprocessed script code shows that loop is expanded in advance. It means that loop is not executed when rendering template.

**Preprocessed template**

```console
$ pytenjin -P views/pp-example2.pyhtml
<?py chk = { params['state']: ' selected="selected"' } ?>
<select name="state">
  <option value="">-</option>
  <option value="CA"#{chk.get('CA', '')}>California</option>
  <option value="FL"#{chk.get('FL', '')}>Florida</option>
  <option value="HI"#{chk.get('HI', '')}>Hawaii</option>
  <option value="NY"#{chk.get('NY', '')}>New York</option>
  <option value="TX"#{chk.get('TX', '')}>Texas</option>
</select>
```

### Parameters

Assume that link_to() is a helper method which takes label and url and generate `<a></a>` tag. In this case, label and url can be parameterized by `_p("...")` and `_P("...")`. The former is converted into #{...} and the latter converted into ${...} by preprocessor.

**views/pp-example3.pyhtml**

```html
<?PY
## ex. link_to('Show', '/show/1')  => <a href="/show/1">Show</a>
def link_to(label, url):
    try:    from urllib.parse import quote
    except: from urllib import quote
    return '<a href="%s">%s</a>' % (quote(url), label)
#enddef
?>
#{{link_to('Show '+_P('params["name"]'), '/items/show/'+_p('params["id"]'))}}
```

The following shows that `_P('...')` and `_p('...')` are converted into `${...}` and `#{...}` respectively.

**Preprocessed template:**

```console
$ pytenjin -P views/pp-example3.pyhtml
<a href="/items/show/#{params["id"]}">Show ${params["name"]}</a>
```

There are many web-application framework and they provides helper functions. These helper functions are divided into two groups. link_to() or _() (function for M17N) return the same result when the same arguments are passed. These functions can be expanded by preprocessor. Some functions return the different result even if the same arguments are passed. These functions can't be expaned by preprocessor.

Preprocessor has the power to make view-layer much faster, but it may make the debugging difficult. You should use it carefully.
