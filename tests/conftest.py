import sys
import os
import stat
import tempfile
import atexit
import shutil

# Add src to path so tenjin can be imported
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set PYTHONPATH so subprocesses can find tenjin
src_dir = os.path.join(os.path.dirname(__file__), '..', 'src')
os.environ['PYTHONPATH'] = os.path.abspath(src_dir) + os.pathsep + os.environ.get('PYTHONPATH', '')

# Create a pytenjin wrapper script so shell-based tests can find it
_bin_dir = tempfile.mkdtemp(prefix='pytenjin_bin_')
_wrapper = os.path.join(_bin_dir, 'pytenjin')
with open(_wrapper, 'w') as f:
    f.write('#!/usr/bin/env python\nfrom tenjin.cli import main\nmain()\n')
os.chmod(_wrapper, os.stat(_wrapper).st_mode | stat.S_IEXEC)
os.environ['PATH'] = _bin_dir + os.pathsep + os.environ.get('PATH', '')
atexit.register(lambda: shutil.rmtree(_bin_dir, ignore_errors=True))

import pytest

@pytest.fixture(autouse=True)
def _set_test_method_name(request):
    """Set _testMethodName on test instances for backward compatibility with unittest-style tests."""
    if request.instance is not None:
        request.instance._testMethodName = request.node.name
