###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

import pytest
import re as _re
from unittest.mock import MagicMock
import sys, os, re

import tenjin
from tenjin.helpers import *
from tenjin.escaped import *

python2 = sys.version_info[0] == 2
python3 = sys.version_info[0] == 3

lvars = "_extend=_buf.extend;_to_str=to_str;_escape=to_escaped; "


if python2:
    from tenjin.escaped import Escaped, EscapedStr, EscapedUnicode
    def u(s):
        return s.decode('utf-8')
    def b(s):
        return s
else:
    from tenjin.escaped import Escaped, EscapedStr, EscapedBytes
    def u(s):
        return s
    def b(s):
        return s.encode('utf-8')


class TestEscapedStr:

    def test_is_escaped(self):
        if "arg is an instance of Escaped class then return True.":
            assert is_escaped(EscapedStr("sos")) == True
            if python2:
                assert is_escaped(EscapedUnicode(u("sos"))) == True
            elif python3:
                assert is_escaped(EscapedBytes(b("sos"))) == True
            #end
        if "arg is not an instance of Escaped class then return False.":
            assert is_escaped("sos") == False
            if python2:
                assert is_escaped(u("sos")) == False
            elif python3:
                assert is_escaped(b("sos")) == False
            #end

    def test_as_escaped(self):
        if "arg is a str then returns EscapedStr object.":
            assert isinstance(as_escaped("<foo>"), EscapedStr)
        if python2:
            if "arg is a unicode then returns EscapedUnicode object.":
                assert isinstance(as_escaped(u("<foo>")), EscapedUnicode)
        elif python3:
            if "arg is a bytes then returns EscapedBytes object.":
                assert isinstance(as_escaped(b("<foo>")), EscapedBytes)
        if "arg is not a basestring then returns TypeError.":
            def f(): as_escaped(123)
            if python2:
                with pytest.raises(TypeError, match=_re.escape("as_escaped(123): expected str or unicode.")):
                    f()
            elif python3:
                with pytest.raises(TypeError, match=_re.escape("as_escaped(123): expected str or bytes.")):
                    f()
        if "arg is never escaped.":
            assert as_escaped("<foo>") == "<foo>"
            assert as_escaped(u("<foo>")) == u("<foo>")

    def test_to_escaped(self):
        if "arg is escaped then returns it as-is.":
            obj = EscapedStr("<foo>")
            #assert to_escaped(obj) is obj
            assert to_escaped(obj) == obj
            if python2:
                obj = EscapedUnicode(u("<foo>"))
                #assert to_escaped(obj) is obj
                assert to_escaped(obj) == obj
            elif python3:
                obj = EscapedBytes(b("<foo>"))
                #assert to_escaped(obj) is obj
                assert to_escaped(obj) == EscapedStr("<foo>")
        if "arg is not escaped then escapes it and returns escaped object.":
            ret = to_escaped("<foo>")
            assert ret == "&lt;foo&gt;"
            assert isinstance(ret, EscapedStr)
            #
            if python2:
                ret = to_escaped(u("<foo>"))
                assert ret == u("&lt;foo&gt;")
                assert isinstance(ret, EscapedStr)     # not EscapedUnicode!
            elif python3:
                #ret = to_escaped(b("<foo>"))
                #assert ret == b("&lt;foo&gt;")
                #assert isinstance(ret, EscapedBytes)
                ret = to_escaped(to_str(b("<foo>")))
                assert ret == "&lt;foo&gt;"
                assert isinstance(ret, EscapedStr)
        if "arg is not a basestring then calls to_str() and escape(), and returns EscapedStr":
            ret = to_escaped(None)
            assert ret == ""
            assert isinstance(ret, EscapedStr)
            ret = to_escaped(123)
            assert ret == "123"
            assert isinstance(ret, EscapedStr)
        if "arg has __html__() method then calls it.":
            obj = MagicMock()
            obj.__html__ = MagicMock(return_value="<b>OK</b>")
            ret = to_escaped(obj)
            assert ret == "&lt;b&gt;OK&lt;/b&gt;"
            assert isinstance(ret, EscapedStr)
            obj.__html__.assert_called_once()
            #
            obj = MagicMock()
            obj.__html__ = MagicMock(return_value=as_escaped("<b>WaWaWa</b>"))
            ret = to_escaped(obj)
            assert ret == "<b>WaWaWa</b>"
            assert isinstance(ret, EscapedStr)
            obj.__html__.assert_called_once()


class TestSafeTemplate:

    input = ( "<?py for item in items: ?>\n"
              "<p>{=item=}</p>\n"
              "<?py #end ?>\n" )
    context = { 'items': [ '<>&"', as_escaped('<>&"') ] }
    expected = ( "<p>&lt;&gt;&amp;&quot;</p>\n"
                 "<p><>&\"</p>\n" )

    def test_get_expr_and_flags(self):
        t = tenjin.SafeTemplate()
        if "matched expression is '${...}' then returns expr string and True":
            m = t.expr_pattern().search("<p>${item}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (True, False))
        if "matched expression is '#{...}' then raises error":
            m = t.expr_pattern().search("<p>#{item}</p>")
            def f(): t.get_expr_and_flags(m)
            with pytest.raises(tenjin.TemplateSyntaxError,
                          match=_re.escape("#{item}: '#{}' is not allowed with SafeTemplate.")):
                f()
        if "matched expression is '{=...=}' then returns expr string and True":
            m = t.expr_pattern().search("<p>{=item=}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (True, False))
        if "matched expression is '{==...==}' then returns expr string and False":
            m = t.expr_pattern().search("<p>{==item==}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (False, True))

    def test_FUNCTEST_of_convert(self):
        if "converted then use 'to_escaped()' instead of 'escape()'":
            t = tenjin.SafeTemplate(input="<p>{=item=}</p>")
            assert t.script == lvars + "_extend(('''<p>''', _escape(item), '''</p>''', ));"
        if "{==...==} exists then skips to escape by to_escaped()":
            t = tenjin.SafeTemplate(input="<p>{==foo()==}</p>")
            assert t.script == lvars + "_extend(('''<p>''', _to_str(foo()), '''</p>''', ));"

    def test_FUNCTEST_of_render(self):
        if "rendered then avoid escaping of escaped object":
            input    = "var1: {=var1=}, var2: {=var2=}\n"
            context  = {'var1': '<>&"', 'var2': as_escaped('<>&"')}
            expected = "var1: &lt;&gt;&amp;&quot;, var2: <>&\"\n"
            t = tenjin.SafeTemplate(input=input)
            assert t.render(context) == expected
            #
            if python2:
                u = unicode
                input    = "var1: {=var1=}, var2: {=var2=}\n"
                context  = {'var1': u('<>&"'), 'var2': as_escaped(u('<>&"'))}
                expected = "var1: &lt;&gt;&amp;&quot;, var2: <>&\"\n"
                t = tenjin.SafeTemplate(input=input)
                assert t.render(context) == expected

    def test_FUNCTEST_with_engine(self):
        fname = 'test_safe_template.pyhtml'
        try:
            _tclass = tenjin.Engine.templateclass
            tenjin.Engine.templateclass = tenjin.SafeTemplate
            f = open(fname, 'w'); f.write(self.input); f.close()
            engine = tenjin.Engine()
            output = engine.render(fname, self.context.copy())
            assert output == self.expected
        finally:
            tenjin.Engine.templateclass = _tclass
            for x in [fname, fname+'.cache']:
                os.path.isfile(x) and os.unlink(x)


class TestSafePreprocessor:

    input = ( "<?PY for i in range(2): ?>\n"
              "<h1>{#=i=#}</h1>\n"
              "<?py for item in items: ?>\n"
              "<p>{=item=}</p>\n"
              "<?py #end ?>\n"
              "<?PY #end ?>\n" )
    context = { 'items': [ '<>&"', as_escaped('<>&"') ] }
    expected = ( "<h1>1</h1>\n"
                 "<?py for item in items: ?>\n"
                 "<p>{=item=}</p>\n"
                 "<?py #end ?>\n"
                 "<h1>2</h1>\n"
                 "<?py for item in items: ?>\n"
                 "<p>{=item=}</p>\n"
                 "<?py #end ?>\n" )
    expected_script = lvars + r"""
_extend(('''<h1>0</h1>\n''', ));
for item in items:
    _extend(('''<p>''', _escape(item), '''</p>\n''', ));
#end
_extend(('''<h1>1</h1>\n''', ));
for item in items:
    _extend(('''<p>''', _escape(item), '''</p>\n''', ));
#end
"""[1:]

    def test_get_expr_and_flags(self):
        t = tenjin.SafePreprocessor()
        if "matched expression is '${{...}}' then returns expr string and True":
            m = t.expr_pattern().search("<p>${{item}}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (True, False))
        if "matched expression is '#{{...}}' then raises error":
            m = t.expr_pattern().search("<p>#{{item}}</p>")
            def f(): t.get_expr_and_flags(m)
            with pytest.raises(tenjin.TemplateSyntaxError,
                          match=_re.escape("#{{item}}: '#{{}}' is not allowed with SafePreprocessor.")):
                f()
        if "matched expression is '{#=...=#}' then returns expr string and True":
            m = t.expr_pattern().search("<p>{#=item=#}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (True, False))
        if "matched expression is '{#==...==#}' then returns expr string and False":
            m = t.expr_pattern().search("<p>{#==item==#}</p>")
            ret = t.get_expr_and_flags(m)
            assert ret == ('item', (False, True))

    def test_FUNCTEST_with_engine(self):
        fname = 'test_safe_preprocessor.pyhtml'
        self._unlink = [fname, fname + '.cache']
        try:
            _backup = tenjin.Engine.templateclass
            tenjin.Engine.templateclass = tenjin.SafeTemplate
            f = open(fname, 'w'); f.write(self.input); f.close()
            engine = tenjin.Engine(preprocess=True, preprocessorclass=tenjin.SafePreprocessor)
            t = engine.get_template(fname)
            assert t.script == self.expected_script
        finally:
            tenjin.Engine.templateclass = _backup
            for x in [fname, fname+'.cache']:
                os.path.isfile(x) and os.unlink(x)


def _with_template(fname, content):
    def deco(func):
        def newfunc(*args):
            try:
                f = open(fname, 'w')
                f.write(content)
                f.close()
                func()
            finally:
                for x in [fname, fname+'.cache']:
                    if os.path.isfile(x):
                        os.unlink(x)
        return newfunc
    return deco


class TestSafeEngine:

    def test_FUNCTEST_render(self):
        fname = 'test_safe_engine_render.pyhtml'
        input = r"""
<p>v1={=v1=}</p>
<p>v2={=v2=}</p>
<p>v1={==v1==}</p>
<p>v2={==v2==}</p>
"""[1:]
        expected = r"""
<p>v1=&lt;&amp;&gt;</p>
<p>v2=<&></p>
<p>v1=<&></p>
<p>v2=<&></p>
"""[1:]
        @_with_template(fname, input)
        def f():
            engine = tenjin.SafeEngine()
            context = { 'v1': '<&>', 'v2': as_escaped('<&>'), }
            output = engine.render(fname, context)
            assert output == expected
        f()

    def test_FUNCTEST_preprocessing2(self):
        fname = 'test_safe_engine_preprocessing2.pyhtml'
        input = r'''
  <h1>{=title=}</h1>
  <ul>
  <?PY for wday in WDAYS: ?>
    <li>{#=wday=#}</li>
  <?PY #endfor ?>
  <ul>
  <div>{#=COPYRIGHT=#}</div>
'''[1:]
        expected_output = r'''
  <h1>SafeEngine Example</h1>
  <ul>
    <li>Su</li>
    <li>M</li>
    <li>Tu</li>
    <li>W</li>
    <li>Th</li>
    <li>F</li>
    <li>Sa</li>
  <ul>
  <div>copyright(c)2010 kuwata-lab.com</div>
'''[1:]
        expected_script = lvars + r"""
_extend(('''  <h1>''', _escape(title), '''</h1>
  <ul>
    <li>Su</li>
    <li>M</li>
    <li>Tu</li>
    <li>W</li>
    <li>Th</li>
    <li>F</li>
    <li>Sa</li>
  <ul>
  <div>copyright(c)2010 kuwata-lab.com</div>\n''', ));
"""[1:]
        @_with_template(fname, input)
        def f():
            f = open(fname, 'w')
            f.write(input)
            f.close()
            engine = tenjin.SafeEngine(preprocess=True)
            context = {
                'title': 'SafeEngine Example',
                'WDAYS': ['Su', 'M', 'Tu', 'W', 'Th','F', 'Sa'],
                'COPYRIGHT': 'copyright(c)2010 kuwata-lab.com',
            }
            output = engine.render(fname, context)
            assert output == expected_output
            assert engine.get_template(fname).script == expected_script
        f()
