###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

import sys, os, re, time
from glob import glob
import pytest

import tenjin
#from tenjin.helpers import escape, to_str
from tenjin.helpers import *

lvars = "_extend=_buf.extend;_to_str=to_str;_escape=escape; "


class TestPreprocessor(object):

    INPUT = r"""
<?PY WEEKDAY = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'] ?>
<select>
<?py curr = params.get('wday') ?>
<?PY for i, wday in enumerate(WEEKDAY): ?>
  <option value="#{{i}}"#{selected(curr==#{{i}})}>${{wday}}</option>
<?PY #endfor ?>
</select>
"""[1:].replace("\t", "")
    SCRIPT = lvars + r"""
WEEKDAY = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
_extend(('''<select>
<?py curr = params.get(\'wday\') ?>\n''', ));
for i, wday in enumerate(WEEKDAY):
    _extend(('''  <option value="''', _to_str(_decode_params(i)), '''"#{selected(curr==''', _to_str(_decode_params(i)), ''')}>''', _escape(_to_str(_decode_params(wday))), '''</option>\n''', ));
#endfor
_extend(('''</select>\n''', ));
"""[1:].replace("\t", "")
    OUTPUT = r"""
<select>
<?py curr = params.get('wday') ?>
  <option value="0"#{selected(curr==0)}>Sun</option>
  <option value="1"#{selected(curr==1)}>Mon</option>
  <option value="2"#{selected(curr==2)}>Tue</option>
  <option value="3"#{selected(curr==3)}>Wed</option>
  <option value="4"#{selected(curr==4)}>Thu</option>
  <option value="5"#{selected(curr==5)}>Fri</option>
  <option value="6"#{selected(curr==6)}>Sat</option>
</select>
"""[1:].replace("\t", "")

    def test_preprocessor_class(self):
        input = self.INPUT
        script = self.SCRIPT
        output = self.OUTPUT
        filename = 'test_preprocess1.pyhtml'
        try:
            f = open(filename, 'w'); f.write(input); f.close()
            preprocessor = tenjin.Preprocessor(filename)
            assert preprocessor.script == script
            assert preprocessor.render() == output
        finally:
            for x in [filename, filename + '.cache']:
                if os.path.isfile(x):
                    os.unlink(x)

    def test_curly_braces_available_in_expressions(self):
        """'{}' is available in '${{}}' or '#{}}}', such as '${{foo({'x':1})}}'"""
        input = """
<p>${{f({'a':1})+g({'b':2})}}</p>
<p>#{{f({'c':3})+g({'d':4})}}</p>
"""
        expected = r"""_extend=_buf.extend;_to_str=to_str;_escape=escape; _extend(('''
<p>''', _escape(_to_str(_decode_params(f({'a':1})+g({'b':2})))), '''</p>
<p>''', _to_str(_decode_params(f({'c':3})+g({'d':4}))), '''</p>\n''', ));
"""
        t = tenjin.Preprocessor()
        script = t.convert(input)
        assert script == expected



class TestTemplatePreprocessor(object):

    INPUT = r"""
<div>
  <?PY for item in items: ?>
  <?py for item in items: ?>
    <i>#{item}</i>
    <i>${item}</i>
    <b>#{{item}}</b>
    <b>${{item}}</b>
  <?py #endfor ?>
  <?PY #endfor ?>
</div>
"""[1:]

    EXPECTED = r"""
<div>
  <?py for item in items: ?>
    <i>#{item}</i>
    <i>${item}</i>
    <b><AAA></b>
    <b>&lt;AAA&gt;</b>
  <?py #endfor ?>
  <?py for item in items: ?>
    <i>#{item}</i>
    <i>${item}</i>
    <b>B&B</b>
    <b>B&amp;B</b>
  <?py #endfor ?>
</div>
"""[1:]

    def test_call(self):
        input, expected = self.INPUT, self.EXPECTED
        context = { 'items': ["<AAA>", "B&B"] }
        pp = tenjin.TemplatePreprocessor()
        assert pp(input, filename="foobar.rhtml", context=context) == expected

    def test_init_takes_preprocessor_class(self):
        """#__init__(): takes preprocessor class."""
        pp = tenjin.TemplatePreprocessor(tenjin.SafePreprocessor)
        assert pp.factory == tenjin.SafePreprocessor

    def test_init_default_preprocessor_class(self):
        """#__init__(): default preprocessor class is tenjin.Preprocessor."""
        pp = tenjin.TemplatePreprocessor()
        assert pp.factory == tenjin.Preprocessor

    def test_call_creates_preprocessor_object_with_specified_class(self):
        """#__call__(): creates preprocessor object with specified class."""
        input = self.INPUT
        context = { 'items': ["<AAA>", "B&B"] }

        pp = tenjin.TemplatePreprocessor(tenjin.Preprocessor)
        pp(input, filename="foobar.pyhtml", context=context)

        pp = tenjin.TemplatePreprocessor(tenjin.SafePreprocessor)
        with pytest.raises(tenjin.TemplateSyntaxError, match=re.escape("#{{item}}: '#{{}}' is not allowed with SafePreprocessor.")):
            pp(input, filename="foobar.pyhtml", context=context)


class TestTrimPreprocessor(object):

    INPUT = r"""
<ul>
  <?py i = 0 ?>
  <?py for item in items:
         i += 1 ?>
    <li>${item}</li>
  <?py #endfor ?>
</ul>
"""[1:]

    def test_remove_spaces_before_lt_at_beginning_of_line(self):
        """remove spaces before '<' at beginning of line"""
        expected = r"""
<ul>
<?py i = 0 ?>
<?py for item in items:
         i += 1 ?>
<li>${item}</li>
<?py #endfor ?>
</ul>
"""[1:]
        input = self.INPUT
        pp = tenjin.TrimPreprocessor()
        assert pp(input) == expected

    def test_remove_all_spaces_when_all_is_true(self):
        """remove all spaces at beginning of line when argument 'all' is true"""
        expected = r"""
<ul>
<?py i = 0 ?>
<?py for item in items:
i += 1 ?>
<li>${item}</li>
<?py #endfor ?>
</ul>
"""[1:]
        input = self.INPUT
        pp = tenjin.TrimPreprocessor(True)
        assert pp(input) == expected


class TestPrefixedLinePreprocessor(object):

    def test_converts_prefixed_lines_into_php_tags(self):
        """converts lines which has prefix (':: ') into '<?py ... ?>'."""
        input = r"""
<ul>
:: i = 0
:: for item in items:
::     i += 1
  <li>${item}</li>
:: #endfor
</ul>
"""[1:]
        expected = r"""
<ul>
<?py i = 0 ?>
<?py for item in items: ?>
<?py     i += 1 ?>
  <li>${item}</li>
<?py #endfor ?>
</ul>
"""[1:]
        pp = tenjin.PrefixedLinePreprocessor()
        assert pp(input) == expected

    def test_able_to_mix_php_tags_and_prefix(self):
        """able to mix '<?py ... ?>' and ':: '."""
        input = r"""
<ul>
:: i = 0
<?py for item in items: ?>
  ::  i += 1
  <li>${item}</li>
<?py #endfor ?>
</ul>
"""[1:]
        expected = r"""
<ul>
<?py i = 0 ?>
<?py for item in items: ?>
  <?py  i += 1 ?>
  <li>${item}</li>
<?py #endfor ?>
</ul>
"""[1:]
        pp = tenjin.PrefixedLinePreprocessor()
        assert pp(input) == expected


class TestJavaScriptPreprocessor(object):

    INPUT = r"""
<table>
  <!-- #JS: render_table(items) -->
  <tbody>
    <?js for (var i = 0, n = items.length; i < n; i++) { ?>
    <tr>
      <td>#{i+1}</td>
      <td>${items[i]}</td>
    </tr>
    <?js } ?>
  </tbody>
  <!-- #/JS -->
</table>
<!-- #JS: show_user(username) -->
  <div>Hello ${username}!</div>
<!-- #/JS -->
"""[1:]

    OUTPUT = r"""
<table>
  <script>function render_table(items){var _buf='';
_buf+='  <tbody>\n';
     for (var i = 0, n = items.length; i < n; i++) {
_buf+='    <tr>\n\
      <td>'+_S(i+1)+'</td>\n\
      <td>'+_E(items[i])+'</td>\n\
    </tr>\n';
     }
_buf+='  </tbody>\n';
  return _buf;};</script>
</table>
<script>function show_user(username){var _buf='';
_buf+='  <div>Hello '+_E(username)+'!</div>\n';
return _buf;};</script>
"""[1:]

    def _make_pp(self):
        return tenjin.JavaScriptPreprocessor()

    def _make_fname(self):
        return "_test_pp.rbhtml"

    def test_converts_embedded_javascript_template_into_client_side_template_function(self):
        """converts embedded javascript template into client-side template function"""
        pp = self._make_pp()
        fname = self._make_fname()
        assert pp(self.INPUT, filename=fname) == self.OUTPUT

    def test_raises_error_when_extra_js_end_found(self):
        """raises error when extra '#/JS' found"""
        pp = self._make_pp()
        fname = self._make_fname()
        with pytest.raises(tenjin.ParseError, match=re.escape("unexpected '<!-- #/JS -->'. (file: _test_pp.rbhtml, line: 2)")):
            pp("foo\n<!-- #/JS -->\n", filename=fname)

    def test_raises_error_when_js_is_not_closed(self):
        """raises error when '#JS' is not closed"""
        pp = self._make_pp()
        fname = self._make_fname()
        with pytest.raises(tenjin.ParseError, match=re.escape("render_table(items) is not closed by '<!-- #/JS -->'. (file: %s, line: 2)" % (fname,))):
            pp("foo\n<!-- #JS: render_table(items) -->\nxxx", filename=fname)

    def test_raises_error_when_js_is_nested(self):
        """raises error when '#JS' is nested"""
        pp = self._make_pp()
        fname = self._make_fname()
        input = r"""
<!-- #JS: outer(items) -->
  <!-- #JS: inner(items) -->
  <!-- #/JS -->
<!-- #/JS -->
"""[1:]
        with pytest.raises(tenjin.ParseError, match=re.escape("inner(items) is nested in outer(items). (file: %s, line: 2)" % (fname,))):
            pp(input, filename=fname)

    def test_js_func_contains_js_functions_necessary(self):
        """JS_FUNC: contains JS functions necessary."""
        assert re.search(r'function _E\(.*?\)', tenjin.JS_FUNC)
        assert re.search(r'function _S\(.*?\)', tenjin.JS_FUNC)

    def test_js_func_is_a_escapedstr(self):
        """JS_FUNC: is a EscapedStr."""
        assert isinstance(tenjin.JS_FUNC, tenjin.escaped.EscapedStr)

    def test_init_can_take_attributes_of_script_tag(self):
        """#__init__(): can take attrubtes of <script> tag"""
        fname = self._make_fname()
        input = self.INPUT
        expected = self.OUTPUT.replace('<script>', '<script type="text/javascript">')
        pp = tenjin.JavaScriptPreprocessor(type='text/javascript')
        actual = pp(input, filename=fname)
        assert actual == expected

    def test_parse_converts_js_template_into_js_code(self):
        """#parse(): converts JS template into JS code."""
        pp = self._make_pp()
        input = r"""
<div>
  <!-- #JS: render_table(items) -->
  <table>
    <?js for (var i = 0, n = items.length; i < n; i++) {
         var item = items[i]; ?>
    <span><?js
      var klass = i % 2 ? 'odd' : 'even'; ?></span>
    <tr>
      <td>{=item=}</td>
    </tr>
    <?js	} ?>
  </table>
  <!-- #/JS -->
</div>
"""[1:]
        expected = r"""
<div>
  <script>function render_table(items){var _buf='';
_buf+='  <table>\n';
     for (var i = 0, n = items.length; i < n; i++) {
         var item = items[i];
_buf+='    <span>';
      var klass = i % 2 ? 'odd' : 'even';_buf+='</span>\n\
    <tr>\n\
      <td>'+_E(item)+'</td>\n\
    </tr>\n';
    	}
_buf+='  </table>\n';
  return _buf;};</script>
</div>
"""[1:]
        output = pp.parse(input)
        assert output == expected

    def test_parse_escapes_expr_but_not_double_expr(self):
        """#parse(): escapes {=expr=} but not {==expr==}."""
        pp = self._make_pp()
        input = r"""
<!-- #JS: render() -->
<b>{=var1=}</b><b>{==var2==}</b>
<!-- #/JS -->
"""[1:]
        expected = r"""
<script>function render(){var _buf='';
_buf+='<b>'+_E(var1)+'</b><b>'+_S(var2)+'</b>\n';
return _buf;};</script>
"""[1:]
        output = pp.parse(input)
        assert output == expected

    def test_parse_supports_both_dollar_and_hash_expr_in_addition_to_equals(self):
        """#parse(): supports both ${expr} and #{expr} in addition to {= =}."""
        pp = self._make_pp()
        input = r"""
<!-- #JS: render() -->
<b>${var1}</b><b>#{var2}</b>
<!-- #/JS -->
"""[1:]
        expected = r"""
<script>function render(){var _buf='';
_buf+='<b>'+_E(var1)+'</b><b>'+_S(var2)+'</b>\n';
return _buf;};</script>
"""[1:]
        output = pp.parse(input)
        assert output == expected

    def test_parse_can_parse_dollar_expr_with_curly_braces(self):
        """#parse(): can parse '${f({x:1})+f({y:2})}'."""
        pp = self._make_pp()
        input = r"""
<!-- #JS: render() -->
<p>${f({x:1})+f({y:2})}</p>
<!-- #/JS -->
"""[1:]
        expected = r"""
<script>function render(){var _buf='';
_buf+='<p>'+_E(f({x:1})+f({y:2}))+'</p>\n';
return _buf;};</script>
"""[1:]
        output = pp.parse(input)
        assert output == expected

    def test_parse_switches_to_function_assignment_when_function_name_contains_symbol(self):
        """#parse(): switches to function assignment when function name contains symbol."""
        pp = self._make_pp()
        input = r"""
<!-- #JS: $jQuery.render_title(title) -->
<h1>${title}</h1>
<!-- #/JS -->
"""[1:]
        expected = r"""
<script>$jQuery.render_title=function(title){var _buf='';
_buf+='<h1>'+_E(title)+'</h1>\n';
return _buf;};</script>
"""[1:]
        output = pp.parse(input)
        assert output == expected

    def test_parse_escapes_single_quotation_and_backslash(self):
        """#parse(): escapes single quotation and backslash."""
        pp = self._make_pp()
        input = r"""
<!-- #JS: render() -->
<h1>'Quote' and \Escape\n</h1>
<!-- #/JS -->
"""[1:]
        expected = r"""
<script>function render(){var _buf='';
_buf+='<h1>\'Quote\' and \\Escape\\n</h1>\n';
return _buf;};</script>
"""[1:]
        output = pp.parse(input)
        assert output == expected
