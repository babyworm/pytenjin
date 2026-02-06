###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

import pytest
import re as _re
import sys, os, re, time, marshal, shutil
from glob import glob
try:    import cPickle as pickle
except: import pickle

from testcase_helper import *
import tenjin
#from tenjin.helpers import escape, to_str
from tenjin.helpers import *

lvars = "_extend=_buf.extend;_to_str=to_str;_escape=escape; "

JYTHON = hasattr(sys, 'JYTHON_JAR')


def _convert_data(data, lang='python'):
    if isinstance(data, dict):
        for k in list(data.keys()):
            v = data[k]
            if k[-1] == '*':
                assert isinstance(v, dict)
                data[k[:-1]] = v.get(lang)
            if isinstance(v, dict) and lang in v:
                data[k] = v[lang]
            else:
                _convert_data(v, lang)
    elif isinstance(data, list):
        for k, v in enumerate(data):
            if isinstance(v, dict) and lang in v:
                data[k] = v[lang]
            else:
                _convert_data(v, lang)


def _remove_files(basenames=[]):
    for basename in basenames:
        for filename in glob("%s*" % basename):
            os.unlink(filename)


def _with_dummy_files(func):
    """decorator for test functions"""
    def deco(self):
        isdir = os.path.isdir
        mkdir = os.mkdir
        try:
            if not isdir('_views'): mkdir('_views')
            if not isdir('_views/blog'): mkdir('_views/blog')
            pairs = [ ('_views/blog/index.pyhtml', 'xxx'),
                      ('_views/index.pyhtml', '<<#{{_DUMMY_VALUE}}>>'),
                      ('_views/layout.pyhtml', '<div>#{_content}</div>'), ]
            for fname, cont in pairs:
                f = open(fname, 'w')
                f.write(cont)
                f.close()
            func(self)
        finally:
            shutil.rmtree('_views')
    for x in ('func_name', '__name__', '__doc__'):
        if hasattr(func, x):
            setattr(deco, x, getattr(func, x))
    return deco


class DebugLogger(object):

    def __init__(self):
        self.messages = []

    def __str__(self):
        return "\n".join(self.messages)

    def f(name):
        def func(self, format, *args):
            msg = args and (format % args) or format
            self.messages.append("[%s] %s" % (name.upper(), msg))
        func.func_name = func.__name__ = name
        return func

    fatal, error, warn, info, debug, trace = \
        f('fatal'), f('error'), f('warn'), f('info'), f('debug'), f('trace')

    del f


class TestEngine:

    #code = TestCaseHelper.generate_testcode(__file__)
    #exec(code)
    datalist = TestCaseHelper.load_testdata(__file__)
    _testdata = dict([ (d['name'], d) for d in datalist ])
    _convert_data(_testdata, lang='python')
    data = _testdata['basic']
    for d in data['templates']:
        d['filename'] = d['filename'].replace('.xxhtml', '.pyhtml')
    templates = dict([(hash['filename'], hash['content']) for hash in data['templates']])
    expected  = dict([(hash['name'], hash['content']) for hash in data['expected']])
    contexts  = data['contexts']


    def setup_method(self):
        tenjin.Engine.cache.clear()
    #    testdata = TestEngine._testdata['basic']
    #    for hash in testdata['templates']:
    #        write_file(hash['filename'], hash['content'])


    #def teardown_method(self):
    #    for hash in TestEngine._testdata['basic']['templates']:
    #        filename = hash['filename']
    #        for fname in [filename, filename+'.cache', filename+'.marshal']:
    #            if os.path.exists(fname):
    #                os.unlink(fname)


    def _testname(self):
        try:
            return self._TestCase__testMethodName
        except AttributeError:
            return self._testMethodName

    def _test_basic(self):
        try:
            testdata = TestEngine._testdata['basic']
            for hash in testdata['templates']:
                write_file(hash['filename'], hash['content'])
            #
            testname = self._testname()
            lst = testname[len('test_basic'):].split('_')
            action   = lst[1]                # 'list', 'show', 'create', or 'edit'
            shortp   = lst[2] == 'short'     # 'short' or 'long'
            layoutp  = lst[3] != 'nolayout'  # 'nolayout' or 'withlayout'
            layout   = layoutp and 'user_layout.pyhtml' or None
            engine   = tenjin.Engine(prefix='user_', postfix='.pyhtml', layout=layout)
            context  = TestEngine.contexts[action].copy()
            key      = 'user_' + action + (layout and '_withlayout' or '_nolayout')
            expected = TestEngine.expected[key]
            filename = 'user_%s.pyhtml' % action
            tplname  = shortp and ':'+action or filename
            if layout:
                output = engine.render(tplname, context)
            else:
                output = engine.render(tplname, context, layout=False)
            assert output == expected
        finally:
            filenames = [ hash['filename'] for hash in TestEngine._testdata['basic']['templates'] ]
            _remove_files(filenames)
            #for hash in TestEngine._testdata['basic']['templates']:
            #    filename = hash['filename']
            #    for fname in [filename, filename+'.cache', filename+'.marshal']:
            #        if os.path.exists(fname):
            #            os.unlink(fname)


    ## long, nolayout

    def test_basic_list_long_nolayout(self):
        self._test_basic()

    def test_basic_show_long_nolayout(self):
        self._test_basic()

    def test_basic_create_long_nolayout(self):
        self._test_basic()

    def test_basic_edit_long_nolayout(self):
        self._test_basic()


    ## short, nolayout

    def test_basic_list_short_nolayout(self):
        self._test_basic()

    def test_basic_show_short_nolayout(self):
        self._test_basic()

    def test_basic_create_short_nolayout(self):
        self._test_basic()

    def test_basic_edit_short_nolayout(self):
        self._test_basic()


    ## long, withlayout

    def test_basic_list_long_withlayout(self):
        self._test_basic()

    def test_basic_show_long_withlayout(self):
        self._test_basic()

    def test_basic_create_long_withlayout(self):
        self._test_basic()

    def test_basic_edit_long_withlayout(self):
        self._test_basic()


    ## short, withlayout

    def test_basic_list_short_withlayout(self):
        self._test_basic()

    def test_basic_show_short_withlayout(self):
        self._test_basic()

    def test_basic_create_short_withlayout(self):
        self._test_basic()

    def test_basic_edit_short_withlayout(self):
        self._test_basic()


    ## ----------------------------------------


    def test_capture_and_echo(self):
        hash = TestEngine._testdata['test_capture_and_echo']
        layout = hash['layout']
        content = hash['content']
        expected = hash['expected']
        layout_filename = 'user_layout.pyhtml'
        content_filename = 'user_content.pyhtml'
        context = { 'items': ['AAA', 'BBB', 'CCC'] }
        try:
            write_file(layout_filename, layout)
            write_file(content_filename, content)
            engine = tenjin.Engine(prefix='user_', postfix='.pyhtml', layout=':layout')
            output = engine.render(':content', context)
            assert output == expected
        finally:
            _remove_files([layout_filename, content_filename])


    def test_capture_as(self):
        filename  = '.test.capture_as.pyhtml'
        content1  = ("<?py from __future__ import with_statement ?>\n"
                     "<div>\n"
                     "<?py with capture_as('sidemenu'): ?>\n"
                     "  <ul>\n"
                     "  <?py for item in items: ?>\n"
                     "    <li>${item}</li>\n"
                     "  <?py #endfor ?>\n"
                     "  </ul>\n"
                     "<?py #endwith ?>\n"
                     "</div>\n")
        content2  = ("<div>\n"
                     "<?py for _ in capture_as('sidemenu'): ?>\n"
                     "  <ul>\n"
                     "  <?py for item in items: ?>\n"
                     "    <li>${item}</li>\n"
                     "  <?py #endfor ?>\n"
                     "  </ul>\n"
                     "<?py #endfor ?>\n"
                     "</div>\n")
        expected1 = ("<div>\n"
                     "</div>\n")
        expected2 = ("  <ul>\n"
                     "    <li>A</li>\n"
                     "    <li>B</li>\n"
                     "    <li>C</li>\n"
                     "  </ul>\n")
        contents = (content1, content2)
        if sys.version < '2.5':
            contents = (content2, )
        for content in contents:
            # Replace dummy_file usage with manual file creation/cleanup
            f = open(filename, 'w'); f.write(content); f.close()
            try:
                context = {'items': ['A', 'B', 'C']}
                engine = tenjin.Engine()
                output = engine.render(filename, context)
                assert output == expected1
                assert context['sidemenu'] == expected2
            finally:
                if os.path.exists(filename): os.unlink(filename)

    def test_captured_as(self):
        hash = TestEngine._testdata['test_captured_as']
        files = ( ('content.pyhtml',      hash['content']),
                  ('customlayout.pyhtml', hash['customlayout']),
                  ('baselayout.pyhtml',   hash['baselayout']),
                  )
        context = hash['context']
        expected = hash['expected']
        try:
            for filename, content in files:
                write_file(filename, content)
            engine = tenjin.Engine(postfix='.pyhtml')
            output = engine.render(':content', context)
            assert output == expected
        finally:
            _remove_files([ t[0] for t in files ])


    def test_local_layout(self):
        hash = TestEngine._testdata['test_local_layout']
        context = hash['context']
        names = ['layout_html', 'layout_xhtml', 'content_html']
        def fname(base):
            return 'local_%s.pyhtml' % base
        try:
            interval = tenjin.Engine.timestamp_interval
            tenjin.Engine.timestamp_interval = 0
            for name in names:
                write_file(fname(name), hash[name])
            engine = tenjin.Engine(prefix='local_', postfix='.pyhtml', layout=':layout_html')
            ##
            def _test(expected, statement):
                content_html = hash['content_html'] + statement
                write_file(fname('content_html'), content_html)
                actual = engine.render(':content_html', context)
                assert actual == expected
            ##
            _test(hash['expected_html'], '')
            time.sleep(1)
            _test(hash['expected_xhtml'], "<?py _context['_layout'] = ':layout_xhtml' ?>\n")
            time.sleep(1)
            _test(hash['expected_nolayout'], "<?py _context['_layout'] = False ?>\n")
            ##
        finally:
            tenjin.Engine.timestamp_interval = interval
            #for name in names:
            #    for suffix in ['', '.cache', '.marshal']:
            #        filename = fname(name) + suffix
            #        if os.path.isfile(filename):
            #            os.unlink(filename)
            _remove_files([ fname(name) for name in names ])


    def test_cachefile(self):
        data = TestEngine._testdata['test_cachefile']
        filenames = { 'layout': 'layout.pyhtml',
                      'page': 'account_create.pyhtml',
                      'form': 'account_form.pyhtml',
                    }
        expected = data['expected']
        context = { 'params': { } }
        cache_filenames = ['account_create.pyhtml.cache', 'account_form.pyhtml.cache']
        try:
            for key, filename in filenames.items():
                write_file(filename, data[key])
            props = { 'prefix':'account_', 'postfix':'.pyhtml', 'layout':'layout.pyhtml' }
            ## no caching
            props['cache'] = False
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            assert output == expected
            for fname in cache_filenames: assert not os.path.exists(fname)
            ## marshal caching
            if not JYTHON:
                props['cache'] = tenjin.MarshalCacheStorage()
                engine = tenjin.Engine(**props)
                output = engine.render(':create', context)
                assert output == expected
                if   python2:  nullbyte = '\0'
                elif python3:  nullbyte = '\0'.encode('ascii')
                for fname in cache_filenames:
                    assert os.path.exists(fname)               # file created?
                    s = read_file(fname, 'rb')        # read binary file
                    assert s.find(nullbyte) >= 0        # binary file?
                    f = open(fname, 'rb')
                    fn = lambda: marshal.load(f)
                    try:
                        fn()           # marshal?
                    finally:
                        f.close()
                engine = tenjin.Engine(**props)
                output = engine.render(':create', context)
                assert output == expected               # reloadable?
            #
            for fname in glob('*.pyhtml.cache'): os.unlink(fname)
            for fname in cache_filenames:
                assert not os.path.exists(fname)
            ## pickle caching
            props['cache'] = tenjin.PickleCacheStorage()
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            assert output == expected
            if   python2:  nullbyte = '\0'
            elif python3:  nullbyte = '\0'.encode('ascii')
            for fname in cache_filenames:
                assert os.path.exists(fname)                         # file created?
                s = read_file(fname, 'rb')                       # read text file
                if python2:
                    assert s.find(nullbyte) < 0        # text file? (pickle protocol ver 2)
                elif python3:
                    assert s.find(nullbyte) >= 0       # binary file? (pickle protocol ver 3)
                f = open(fname, 'rb')
                fn = lambda: pickle.load(f)
                try:
                    fn()
                finally:
                    f.close()
                f = open(fname, 'rb')
                pickle.load(f)
                f.close()
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            assert output == expected               # reloadable?
            #
            for fname in glob('*.cache'): os.unlink(fname)
            for fname in cache_filenames:
                assert not os.path.exists(fname)
            ## text caching
            props['cache'] = tenjin.TextCacheStorage()
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            assert output == expected
            if   python2:  nullchar = '\0'
            elif python3:  nullchar = '\0'
            for fname in cache_filenames:
                assert os.path.exists(fname)                  # file created?
                s = read_file(fname, 'r')            # read text file
                assert s.find(nullchar) < 0            # text file?
                if JYTHON:
                    continue
                #fn = lambda: marshal.loads(s)
                f = open(fname, 'rb')
                fn = lambda: marshal.load(f)
                try:
                  if python3:
                    with pytest.raises((ValueError, EOFError)) as exc_info: fn()        # non-marshal?
                    ex = exc_info.value
                    if sys.version_info[1] == 0:     # python 3.0
                        assert str(ex) == "bad marshal data"
                    else:                            # python 3.1 or later
                        if isinstance(ex, ValueError):
                            assert str(ex) == "bad marshal data (unknown type code)"
                        # EOFError for Python 3.12+ is also acceptable
                  elif python2 and sys.version_info[1] >= 5:
                    with pytest.raises(EOFError, match=_re.escape("EOF read where object expected")): fn()  # non-marshal?
                finally:
                    f.close()
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            assert output == expected                  # reloadable?
        finally:
            _remove_files(filenames.values())

    def test_cachefile_timestamp(self):
        """engine should clear cache not only template is newer but also template is older than cache."""
        data = TestEngine._testdata['test_cachefile']
        filenames = { 'layout': 'layout.pyhtml',
                      'page': 'account_create.pyhtml',
                      'form': 'account_form.pyhtml',
                    }
        expected = data['expected']
        context = { 'params': { } }
        cache_filenames = ['account_create.pyhtml.cache', 'account_form.pyhtml.cache']
        try:
            interval = tenjin.Engine.timestamp_interval
            tenjin.Engine.timestamp_interval = 0
            for key, filename in filenames.items():
                write_file(filename, data[key])
            props = { 'prefix': 'account_', 'postfix':'.pyhtml', 'layout':'layout.pyhtml', 'cache':True }
            ## create cache files and check them
            time.sleep(1)
            curr_time = time.time()
            engine = tenjin.Engine(**props)
            output = engine.render(':create', context)
            for fname in filenames.values():
                assert os.path.exists(fname)                         # file created?
                assert engine.get_template(fname).timestamp < curr_time
                assert engine.get_template(fname).timestamp == os.path.getmtime(fname)
            ## save current cached object
            cached = {}
            for fname in filenames.values():
                cached[fname] = engine.get_template(fname)
            ## confirm that get_template() returns the same object
            for fname in filenames.values():
                assert cached[fname] is engine.get_template(fname)
            ## change timestamp of templates to be old
            for fname in filenames.values():
                atime = mtime = os.path.getmtime(fname) - 10
                os.utime(fname, (atime, mtime))
            ## check whether new caches are created
            for fname in filenames.values():
                t = engine.get_template(fname)
                assert cached[fname] is not t
                assert t.timestamp == os.path.getmtime(fname)
        finally:
            tenjin.Engine.timestamp_interval = interval
            _remove_files(filenames.values())


    def test_cachefile_unset(self):
        try:
            input = "<?py x = 10 ?>"
            template_name = "cachefile_delete.pyhtml"
            f = open(template_name, 'w'); f.write(input); f.close()
            storage = tenjin.MarshalCacheStorage()
            engine = tenjin.Engine(cache=storage)
            engine.render(template_name)
            fullpath = os.path.abspath(template_name)
            cachepath = engine.cachename(fullpath)
            assert cachepath in storage.items
            assert os.path.exists(template_name + '.cache')
            storage.unset(cachepath)
            assert cachepath not in storage.items
            assert not os.path.exists(template_name + '.cache')
            def f():
                storage.unset(fullpath)
            f()
        finally:
            _remove_files([template_name, template_name+'.cache'])


    def test_change_layout(self):
        data = TestEngine._testdata['test_change_layout']
        ## setup
        tenjin.Engine.cache.clear()
        basenames = ['baselayout', 'customlayout', 'content']
        for basename in basenames:
            write_file('%s.pyhtml' % basename, data[basename])
        ## body
        try:
            engine = tenjin.Engine(layout='baselayout.pyhtml')
            output = engine.render('content.pyhtml')
            expected = data['expected']
            assert output == expected
        ## teardown
        finally:
            _remove_files(basenames)


    def test_context_scope(self):
        data = TestEngine._testdata['test_context_scope']
        base = data['base']
        part = data['part']
        expected = data['expected']
        for basename in ('base', 'part'):
            write_file('%s.pyhtml' % basename, data[basename])
        #
        try:
            engine = tenjin.Engine()
            context = {}
            output = engine.render('base.pyhtml', context)
            expected = data['expected']
            assert output == expected
        finally:
            _remove_files(['base', 'part'])


    def test_template_args(self):
        data = TestEngine._testdata['test_template_args']
        content = data['content']
        expected = data['expected']
        context = data['context']
        for basename in ('content', ):
            write_file('%s.pyhtml' % basename, data[basename])
        #
        try:
            def f1():
                engine = tenjin.Engine(cache=True)
                assert engine.get_template('content.pyhtml').args != None
                output = engine.render('content.pyhtml', context)
            with pytest.raises(NameError) as exc_info: f1()
            ex = exc_info.value
            #import sys; sys.stderr.write("*** debug: ex=%s\n" % (repr(ex)))
            #engine = tenjin.Engine(cache=True)
            #assert engine.get_template('content.pyhtml').args != None
            #output = engine.render('content.pyhtml', context)
            #assert output == expected
            with pytest.raises(NameError) as exc_info: f1()
            ex = exc_info.value
        finally:
            _remove_files(['content'])


    def test__set_cache_storage(self):
        if "default then Engine.cache is TextCacheStorage instance":
            assert isinstance(tenjin.Engine.cache, tenjin.TextCacheStorage)
        if "cache=True specified then use default cache object":
            engine = tenjin.Engine(cache=True)
            assert ('cache' in engine.__dict__) == False
            assert engine.cache is tenjin.Engine.cache
            assert engine.cache is tenjin.Engine(cache=True).cache
        if "cache=True and default cache is not set then create MarshalCacheStorage object for each engine":
            bkup = tenjin.Engine.cache
            try:
                tenjin.Engine.cache = None
                engine = tenjin.Engine(cache=True)
                assert 'cache' in engine.__dict__
                assert isinstance(engine.cache, tenjin.MarshalCacheStorage)
                assert engine.cache is not tenjin.Engine(cache=True).cache
            finally:
                tenjin.Engine.cache = bkup
        #if "cache=None specified then set MemoryCacheObject instance as cache object":
        #    engine = tenjin.Engine(cache=None)
        #    assert ('cache' in engine.__dict__) == True
        #    assert isinstance(engine.cache, tenjin.MemoryCacheStorage)
        if "cache=None then do nothing":
            engine = tenjin.Engine(cache=None)
            assert 'cache' not in engine.__dict__
        if "cache=False specified then don't use cache object":
            engine = tenjin.Engine(cache=False)
            assert 'cache' in engine.__dict__
            assert engine.cache == None
        if "CacheStorage instance is specified then use it as cache object":
            cache_storage = tenjin.MarshalCacheStorage()
            engine = tenjin.Engine(cache=cache_storage)
            assert 'cache' in engine.__dict__
            assert engine.cache is cache_storage
        if "invalid object is specified as cache object then raise ValueError":
            def f():
                tenjin.Engine(cache=123)
            with pytest.raises(ValueError, match=_re.escape('123: invalid cache object.')): f()


    def test_cached_contents(self):
        data = TestEngine._testdata['test_cached_contents']
        def _test(filename, cachename, cachemode, input, expected_script, expected_args):
            if input:
                write_file(filename, input)
            engine = tenjin.Engine(cache=cachemode)
            t = engine.get_template(filename)
            assert t.args == expected_args
            assert t.script == expected_script
            #import marshal
            #f = open(filename + '.cache', 'rb')
            #try:
            #    dct = marshal.load(f)
            #    assert dct['args'] == expected_args
            #    assert dct['script'] == expected_script
            #finally:
            #    f.close()
        ##
        try:
            ## args=[x,y,z], cache=1
            filename = 'input.pyhtml'
            for f in glob(filename+'*'): os.path.exists(f) and os.remove(f)
            script = data['script1']
            args  = data['args1']
            input = data['input1']
            cachename = filename+'.cache'
            assert not os.path.exists(cachename)
            _test(filename, cachename, True, input, script, args)
            assert os.path.exists(cachename)
            _test(filename, cachename, True, None, script, args)
            ## args=[], cache=1
            cachename = filename+'.cache'
            input = data['input2']  # re.sub(r'<\?py #@ARGS.*?\?>\n', '<?py #@ARGS ?>\n', input)
            script = data['script2']  # re.sub(r'#@ARGS.*?\n', '#@ARGS \n', cache)
            args  = data['args2']   # []
            time.sleep(1)
            #assert os.path.exists(cachename)
            _test(filename, cachename, True, input, script, args)
            #assert os.path.exists(cachename)
            _test(filename, cachename, True, None, script, args)
        finally:
            _remove_files(['input.pyhtml'])


    def _test_template_path(self, keys):
        data = TestEngine._testdata['test_template_path']
        basedir = 'test_templates'
        try:
            os.mkdir(basedir)
            os.mkdir(basedir + '/common')
            os.mkdir(basedir + '/user')
            d = { 'layout':keys[0], 'body':keys[1], 'footer':keys[2], }
            for key in ('layout', 'body', 'footer'):
                filename = '%s/common/%s.pyhtml' % (basedir, key)
                write_file(filename, data['common_'+key])
                if d[key] == 'user':
                    filename = '%s/user/%s.pyhtml' % (basedir, key)
                    write_file(filename, data['user_'+key])
            #
            path = [basedir+'/user', basedir+'/common']
            engine = tenjin.Engine(postfix='.pyhtml', path=path, layout=':layout')
            context = {'items':('AAA', 'BBB', 'CCC')}
            output = engine.render(':body', context)
            #
            expected = data['expected_' + '_'.join(keys)]
            assert output == expected
        finally:
            #os.removedirs(basedir)
            #pass
            for filename in glob('%s/*/*' % basedir):
                os.unlink(filename)
            for filename in glob('%s/*' % basedir):
                os.rmdir(filename)
            os.rmdir(basedir)

    def test_template_path_common_common_common(self):
        self._test_template_path(('common', 'common', 'common'))
    def test_template_path_user_common_common(self):
        self._test_template_path(('user',   'common', 'common'))
    def test_template_path_common_user_common(self):
        self._test_template_path(('common', 'user',   'common'))
    def test_template_path_user_user_common(self):
        self._test_template_path(('user',   'user',   'common'))
    def test_template_path_common_common_user(self):
        self._test_template_path(('common', 'common', 'user'))
    def test_template_path_user_common_user(self):
        self._test_template_path(('user',   'common', 'user'))
    def test_template_path_common_user_user(self):
        self._test_template_path(('common', 'user',   'user'))
    def test_template_path_user_user_user(self):
        self._test_template_path(('user',   'user',   'user'))


    def test_preprocessor(self):
        data = TestEngine._testdata['test_preprocessor']
        try:
            basenames = ('form', 'create', 'update', 'layout', )
            filenames = []
            for name in basenames:
                filename = 'prep_%s.pyhtml' % name
                filenames.append(filename)
                write_file(filename, data[name])
            engine = tenjin.Engine(prefix='prep_', postfix='.pyhtml', layout=':layout', preprocess=True)
            #
            context = {
                'title': 'Create',
                'action': 'create',
                'params': { 'state': 'NY' },
            }
            actual = engine.render(':create', context)  # 1st
            assert actual == data['expected1']
            context['params'] = {'state': 'xx'}
            actual = engine.render(':create', context)  # 2nd
            #assert actual == data['expected1']
            expected = data['expected1'].replace(r' checked="checked"', '')
            assert actual == expected
            #
            context = {
                'title': 'Update',
                'action': 'update',
                'params': { 'state': 'NY' },
            }
            actual = engine.render(':update', context)  # 1st
            assert actual == data['expected2']
            context['params'] = { 'state': 'xx' }
            actual = engine.render(':update', context)  # 2nd
            assert actual == data['expected2'] # not changed!
            #
            assert engine.get_template(':form').script == data['cache1']
            assert engine.get_template(':create').script == data['cache2']
            assert engine.get_template(':layout').script == data['cache3']
            assert engine.get_template(':update').script == data['cache4']
            #
        finally:
            _remove_files(filenames)

    @_with_dummy_files
    def test_pp(self):
        # 'pp' paramater should be a list of preprocessor objects.
        pp1 = tenjin.TemplatePreprocessor()
        pp2 = tenjin.TrimPreprocessor()
        pp3 = tenjin.JavaScriptPreprocessor(type="text/javascript")
        e = tenjin.Engine(pp=[pp1, pp2, pp3])
        input = r"""
<body>
  <div>
    <!-- #JS: render_items(items) -->
    <ul>
    <?js for (var i = 0; i < items.length; i++) { ?>
      <li>${i}</li>
    <?js } ?>
    </ul>
    <!-- #/JS -->
  </div>
  <script>#{{tenjin.JS_FUNC}}</script>
</body>
"""[1:]
        expected = r"""
<body>
<div>
<script type="text/javascript">function render_items(items){var _buf='';
_buf+='<ul>\n';
 for (var i = 0; i < items.length; i++) {
_buf+='<li>'+_E(i)+'</li>\n';
 }
_buf+='</ul>\n';
return _buf;};</script>
</div>
<script>function _S(x){return x==null?'':x;}
function _E(x){return x==null?'':typeof(x)!=='string'?x:x.replace(/[&<>"']/g,_EF);}
var _ET={'&':"&amp;",'<':"&lt;",'>':"&gt;",'"':"&quot;","'":"&#039;"};
function _EF(c){return _ET[c];};</script>
</body>
"""[1:]
        fname = 'tmp_123.pyhtml'
        f = open(fname, 'w'); f.write(input); f.close()
        try:
            t = e.get_template(fname)
            context = {}
            output = e.render(fname, context)
            assert output == expected
        finally:
            for x in glob(fname + '*'): os.unlink(x)

    def test_init_creates_templatepreprocessor_object_when_preprocess_option_is_on(self):
        # #__init__(): creates TemplatePreprocessor object when 'preprocess' option is on.
        e = tenjin.Engine(preprocess=True)
        assert isinstance(e.pp, list); assert len(e.pp) == 1
        assert isinstance(e.pp[0], tenjin.TemplatePreprocessor)

    def test_init_creates_templatepreprocessor_object_with_preprocessorclass_class(self):
        # #__init__(): creates TemplatePreprocessor object with 'preprocessorclass' class.
        e = tenjin.Engine(preprocess=True)
        assert e.pp[0].factory == tenjin.Preprocessor
        e = tenjin.Engine(preprocess=True, preprocessorclass=tenjin.SafePreprocessor)
        assert e.pp[0].factory == tenjin.SafePreprocessor

    def test_include_with_kwargs(self):
        data = TestEngine._testdata['test_include_with_kwargs']
        write_file('index.pyhtml', data['index_html'])
        write_file('sub.pyhtml', data['sub_html'])
        expected = data['expected']
        #
        try:
            engine = tenjin.Engine()
            context = {}
            output = engine.render('index.pyhtml', context)
            assert output == expected
        finally:
            _remove_files(['index', 'sub'])


    def test_add_template(self):
        if "template is added then it can be got by get_template()":
            input = """val=#{val}"""
            template = tenjin.Template('foo.pyhtml', input=input)
            engine = tenjin.Engine(postfix='.pyhtml')
            engine.add_template(template)
            assert engine.get_template('foo.pyhtml') == template
            assert engine.get_template(':foo') == template
        if "template is added then it should not create cache file":
            assert engine.render(':foo', {'val': 'ABC'}) == 'val=ABC'
            assert not os.path.exists('foo.pyhtml')


    #def test_prefer_fullpath(self):
    #    fname = 'test_prefer_fullpath.pyhtml'
    #    input = ( "<?py for x in items: ?>\n"
    #              "  <p>${x.length}</p>\n"
    #              "<?py #end ?>\n" )
    #    context = {'items': ['A']}
    #    engine = None
    #    #
    #    def _test(fname, input, expected):
    #        write_file(fname, input)
    #        engine = tenjin.Engine()
    #        engine.cache.clear()
    #        t = engine.get_template(fname)
    #        assert t.filename == expected
    #        ex = error_file = None
    #        try:
    #            engine.render(fname, context)
    #        except:
    #            ex = sys.exc_info()[1]
    #            error_file = _filename_on_where_error_raised()
    #        assert ex != None
    #        assert error_file == expected
    #        # read from cache
    #        engine.cache.clear()
    #        engine = tenjin.Engine()
    #        t = engine.get_template(fname)
    #        assert t.filename == expected
    #    def _filename_on_where_error_raised():
    #        import traceback
    #        tb = sys.exc_info()[2]
    #        arr = traceback.format_tb(tb)
    #        msg = arr[-1]
    #        m = re.search(r'File "(.*?)"', msg)
    #        return m.group(1)
    #    #
    #    if "Engine.prefer_fullpath is False then set relative epath as template filename":
    #        assert tenjin.Engine.prefer_fullpath == False
    #        try:
    #            _test(fname, input, expected=fname)
    #        finally:
    #            _remove_files([fname, fname + '.cache'])
    #    if "Engine.prefer_fullpath is True then set fullpath as template filename":
    #        tenjin.Engine.prefer_fullpath = True
    #        try:
    #            _test(fname, input, expected=os.path.join(os.getcwd(), fname))
    #        finally:
    #            tenjin.Engine.prefer_fullpath = False
    #            _remove_files([fname, fname + '.cache'])


    ##################

    def test_cachename(self):
        engine = tenjin.Engine()
        # return cache file path
        assert engine.cachename('foo.pyhtml') == 'foo.pyhtml.cache'

    def test_to_filename(self):
        engine = tenjin.Engine(prefix='user_', postfix='.pyhtml')
        # if template_name starts with ':', add prefix and postfix to it.
        assert engine.to_filename(':list') == 'user_list.pyhtml'
        # if template_name doesn't start with ':', just return it.
        assert engine.to_filename('list') == 'list'

    @_with_dummy_files
    def test__create_template(self):
        e1 = tenjin.Engine(path=['_views/blog', '_views'])
        t = None
        # if input is not specified then just create empty template object.
        t = e1._create_template(None)
        assert isinstance(t, tenjin.Template)
        assert t.filename == None
        assert t.script == None
        # if input is specified then create template object and return it.
        t = e1._create_template('<p>#{_content}</p>', '_views/layout.pyhtml')
        assert isinstance(t, tenjin.Template)
        assert t.filename == "_views/layout.pyhtml"
        assert t.script == lvars + "_extend(('''<p>''', _to_str(_content), '''</p>''', ));"

    @_with_dummy_files
    def test__preprocess(self):
        e1 = tenjin.Engine(preprocess=True)
        # preprocess template and return result
        fpath = '_views/index.pyhtml'
        input, mtime = e1.loader.load(fpath)
        ret = e1._preprocess(input, fpath, {}, globals())
        assert ret == "<<SOS>>"

    @_with_dummy_files
    def test__get_template_from_cache(self):
        e1 = tenjin.Engine(path=['_views/blog', '_views'], postfix='.pyhtml')
        fpath = '_views/blog/index.pyhtml'
        cpath = fpath + '.cache'
        # if template not found in cache, return None
        ret = e1._get_template_from_cache(cpath, fpath)
        assert ret == None
        t = tenjin.Template(fpath)
        e1.cache.set(fpath + '.cache', t)
        # if checked within a sec, skip timestamp check.
        #try:
        #    t.timestamp = time.time() - 0.2
        #    #import pdb; pdb.set_trace()
        #    tenjin.logger = DebugLogger()
        #    ret = e1._get_template_from_cache(cpath, fpath)
        #    msg = tenjin.logger.messages[0]
        #    assert msg.startswith("[TRACE] [tenjin.Engine] timestamp check skipped (") == True
        #finally:
        #    tenjin.logger = None
        pass
        # if timestamp of template objectis same as file, return it.
        t._last_checked_at = None
        t.timestamp = os.path.getmtime(fpath)
        assert e1._get_template_from_cache(cpath, fpath) is t
        delta = JYTHON and 0.03 or 0.001
        assert abs(t._last_checked_at - time.time()) <= delta
        # if timestamp of template object is different from file, clear it
        t.timestamp = t.timestamp + 1
        t._last_checked_at = None
        try:
            #import pdb; pdb.set_trace()
            tenjin.logger = DebugLogger()
            ret = e1._get_template_from_cache(cpath, fpath)
            msg = tenjin.logger.messages[0]
            assert msg == "[INFO] [tenjin.Engine] cache expired (filepath='_views/blog/index.pyhtml')"
        finally:
            tenjin.logger = None

    @_with_dummy_files
    def test_get_template(self):
        e1 = tenjin.Engine(path=['_views/blog', '_views'], postfix='.pyhtml')
        filepath  = '_views/blog/index.pyhtml'
        fullpath  = os.getcwd() + filepath
        cachepath = fullpath + '.cache'
        assert not os.path.exists(cachepath)
        t = None
        # return template object.
        # accept template_name such as ':index'.
        t = e1.get_template(':index')
        assert isinstance(t, tenjin.Template)
        assert t.filename == filepath
        # if template object is added by add_template(), return it.
        tmp = tenjin.Template('foo.pyhtml', input="<<dummy>>")
        e1.add_template(tmp)
        assert e1.get_template('foo.pyhtml') is tmp
        # get filepath and fullpath of template
        e1._filepaths['index.pyhtml'] == (filepath, fullpath)
        # if template file is not found then raise TemplateNotFoundError
        def f(): e1.get_template('index')
        with pytest.raises(tenjin.TemplateNotFoundError, match=_re.escape("index: filename not found (path=['_views/blog', '_views']).")): f()
        # use full path as base of cache file path
        # get template object from cache
        assert list(e1.cache.items.keys()) == ["%s/_views/blog/index.pyhtml.cache" % os.getcwd()]
        # change template filename according to prefer_fullpath
        pass
        # use full path as base of cache file path
        pass
        # get template object from cache
        pass
        # if template object is not found in cache or is expired...
        e1.cache.clear()
        assert len(e1.cache.items) == 0
        tname = ':layout'
        fpath = '_views/layout.pyhtml'
        cpath = os.path.join(os.getcwd(), '_views/layout.pyhtml.cache')
        assert not os.path.exists(cpath)
        # create template object.
        t = e1.get_template(tname)
        assert isinstance(t, tenjin.Template)
        # set timestamp and filename of template object.
        assert t.timestamp == os.path.getmtime(filepath)
        assert t.filename == fpath
        delta = JYTHON and 0.03 or 0.003
        assert abs(t._last_checked_at - time.time()) <= delta
        # save template object into cache.
        assert os.path.exists(cpath)
        assert len(e1.cache.items) == 1
        assert cpath in e1.cache.items

    def test_include(self):
        # get local and global vars of caller.
        pass
        # get _context from caller's local vars.
        pass
        # if kwargs specified then add them into context.
        pass
        # get template object with context data and global vars.
        pass
        # if append_to_buf is true then add output to _buf.
        pass
        # if append_to_buf is false then don't add output to _buf.
        pass
        # render template and return output.
        pass
        # kwargs are removed from context data.
        pass

    def test_hook_context(self):
        e = tenjin.Engine()
        ctx = {}
        e.hook_context(ctx)
        # add engine itself into context data.
        assert ctx.get('_engine') is e
        # add include() method into context data.
        assert ctx.get('include') == (e.include)

    def test_get_template_ignores_syntax_error_when_compiling(self):
        # get_template(): ignores syntax error when compiling.
        input = """<p>${{foo}</p>"""
        fname = "tmp_999.pyhtml"
        f = open(fname, 'w'); f.write(input); f.close()
        try:
            e = tenjin.Engine()
            def fn(): e.get_template(fname)
            fn()
        finally:
            for x in glob(fname + '*'): os.unlink(x)


_DUMMY_VALUE = 'SOS'
