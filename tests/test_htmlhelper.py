# -*- coding: utf-8 -*-

###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

import pytest
import re as _re
import sys, os, re

python2 = sys.version_info[0] == 2
python3 = sys.version_info[0] == 3

from testcase_helper import *
import tenjin
from tenjin.helpers import escape, to_str
from tenjin.html import *

if python2:
    from tenjin.escaped import as_escaped, EscapedStr, EscapedUnicode
    def u(s):
        return s.decode('utf-8')
else:
    from tenjin.escaped import as_escaped, EscapedStr, EscapedBytes
    def u(s):
        return s


class TestHtmlHelper:

    def test_escape_html(self):
        assert escape_html('<>&"\'') == '&lt;&gt;&amp;&quot;&#39;'
        assert escape_html('[SOS]') == '[SOS]'
        def f(): escape_html(123)
        #with pytest.raises(Exception): f()
        with pytest.raises(AttributeError, match=_re.escape("'int' object has no attribute 'replace'")):
            f()

    def test_tagattr(self):
        assert tagattr('size', 20)           == ' size="20"'
        assert tagattr('size', 0)            == ' size="0"'
        assert tagattr('size', '')           == ''
        assert tagattr('size', 20, 'large')  == ' size="large"'
        assert tagattr('size',  0, 'zero')   == ' size="zero"'
        assert tagattr('size', '', 'empty')  == ''
        assert tagattr('title', '<>&"')      == ' title="&lt;&gt;&amp;&quot;"'
        assert tagattr('title', '<>&"', escape=False) == ' title="<>&""'
        #
        assert isinstance(tagattr('size', 20), EscapedStr)
        assert isinstance(tagattr('size', ''), EscapedStr)

    def test_tagattrs(self):
        assert tagattrs(src="img.png", size=20) == ' src="img.png" size="20"'
        assert tagattrs(src='', size=0)         == ' size="0"'
        assert tagattrs(klass='error')          == ' class="error"'    # klass='error' => class="error"
        assert tagattrs(checked='Y')            == ' checked="checked"'
        assert tagattrs(selected=1)             == ' selected="selected"'
        assert tagattrs(disabled=True)          == ' disabled="disabled"'
        assert tagattrs(checked='', selected=0, disabled=None) == ''
        #
        assert isinstance(tagattrs(size=20), EscapedStr)
        assert isinstance(tagattrs(size=None), EscapedStr)
        #
        assert tagattrs(name="<foo>")    == ' name="&lt;foo&gt;"'
        assert tagattrs(name=u("<foo>")) == ' name="&lt;foo&gt;"'
        assert tagattrs(name=as_escaped("<foo>"))    == ' name="<foo>"'
        assert tagattrs(name=as_escaped(u("<foo>"))) == ' name="<foo>"'

    def test_checked(self):
        assert checked(1==1) == ' checked="checked"'
        assert checked(1==0) == ''
        #
        assert isinstance(checked(1==1), EscapedStr)
        assert isinstance(checked(1==0), EscapedStr)

    def test_selected(self):
        assert selected(1==1) == ' selected="selected"'
        assert selected(1==0) == ''
        #
        assert isinstance(selected(1==1), EscapedStr)
        assert isinstance(selected(1==0), EscapedStr)

    def test_disabled(self):
        assert disabled(1==1) == ' disabled="disabled"'
        assert disabled(1==0) == ''
        #
        assert isinstance(disabled(1==1), EscapedStr)
        assert isinstance(disabled(1==0), EscapedStr)

    def test_nl2br(self):
        s = """foo\nbar\nbaz\n"""
        assert nl2br(s) == "foo<br />\nbar<br />\nbaz<br />\n"
        #
        assert isinstance(nl2br(s), EscapedStr)

    def test_text2html(self):
        s = """FOO\n    BAR\nBA     Z\n"""
        expected = "FOO<br />\n &nbsp; &nbsp;BAR<br />\nBA &nbsp; &nbsp; Z<br />\n"
        assert text2html(s) == expected
        expected = "FOO<br />\n    BAR<br />\nBA     Z<br />\n"
        assert text2html(s, False) == expected
        #
        assert isinstance(text2html(s), EscapedStr)

    def test_nv(self):
        assert nv('rank', 'A')       == 'name="rank" value="A"'
        assert nv('rank', 'A', '.')  == 'name="rank" value="A" id="rank.A"'
        assert nv('rank', 'A', klass='error') == 'name="rank" value="A" class="error"'
        assert nv('rank', 'A', checked=True)  == 'name="rank" value="A" checked="checked"'
        assert nv('rank', 'A', disabled=10)   == 'name="rank" value="A" disabled="disabled"'
        assert nv('rank', 'A', style="color:red") == 'name="rank" value="A" style="color:red"'
        #
        assert isinstance(nv('rank', 'A'), EscapedStr)
        #
        #assert nv(u("名前"), u("なまえ")) == u('name="名前" value="なまえ"')
        assert nv(u("名前"), u("なまえ")) == 'name="名前" value="なまえ"'
        if python2:
            assert isinstance(nv(u("名前"), u("なまえ")), EscapedStr)  # not EscapedUnicode!

    def test_js_link(self):
        html = js_link("<b>SOS</b>", "alert('Haru&Kyon')")
        assert html == '''<a href="javascript:undefined" onclick="alert(&#39;Haru&amp;Kyon&#39;);return false">&lt;b&gt;SOS&lt;/b&gt;</a>'''
        #
        html = js_link(as_escaped("<b>SOS</b>"), as_escaped("alert('Haru&Kyon')"))
        assert html == '''<a href="javascript:undefined" onclick="alert('Haru&Kyon');return false"><b>SOS</b></a>'''
        #
        html = js_link("<b>SOS</b>", "alert('Haru&Kyon')", klass='<sos2>')
        assert html == '''<a href="javascript:undefined" onclick="alert(&#39;Haru&amp;Kyon&#39;);return false" class="&lt;sos2&gt;">&lt;b&gt;SOS&lt;/b&gt;</a>'''
