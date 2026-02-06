###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

import pytest
import sys, os, time
import tenjin

from test_engine import _with_dummy_files


class TestFileSystemLoader:

    def setup_method(self):
        self.loader = tenjin.FileSystemLoader()
        self.dirs = ['_views/blog', '_views']

    @_with_dummy_files
    def test_find(self):
        # if dirs provided then search template file from it.
        assert self.loader.find('index.pyhtml', self.dirs) == '_views/blog/index.pyhtml'
        assert self.loader.find('layout.pyhtml', self.dirs) == '_views/layout.pyhtml'
        # if dirs not provided then just return filename if file exists.
        assert self.loader.find('_views/index.pyhtml') == '_views/index.pyhtml'
        # if file not found then return None.
        assert self.loader.find('index2.pyhtml', self.dirs) == None
        assert self.loader.find('index2.pyhtml') == None

    @_with_dummy_files
    def test_abspath(self):
        # return full-path of filepath
        ret = self.loader.abspath('_views/blog/index.pyhtml')
        assert ret == os.path.join(os.getcwd(), '_views/blog/index.pyhtml')

    @_with_dummy_files
    def test_timestamp(self):
        # return mtime of file
        ts = float(int(time.time())) - 3.0
        os.utime('_views/blog/index.pyhtml', (ts, ts))
        ret = self.loader.timestamp('_views/blog/index.pyhtml')
        assert ret == ts

    @_with_dummy_files
    def test_read(self):
        # if file exists, return file content and mtime
        ts = float(int(time.time())) - 1.0
        os.utime('_views/layout.pyhtml', (ts, ts))
        ret = self.loader.load('_views/layout.pyhtml')
        assert ret == ("<div>#{_content}</div>", ts)
        # if file not exist, return None
        ret = self.loader.load('_views/layout2.pyhtml')
        assert ret == None
