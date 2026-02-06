"""PyTenjin - a fast and full-featured template engine based on embedded Python.

Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com)
License: MIT License

This is a maintained fork of the original Tenjin template engine.
Original project: https://pypi.org/project/Tenjin/
Original author: makoto kuwata (kuwata-lab.com)
See THIRD_PARTY_LICENSES for the original license.
"""

# Import everything from the core tenjin module, including private names.
# The original tenjin was a single-file module, so all names (including _private)
# were accessible via `import tenjin`. We preserve this for backward compatibility.
import tenjin.tenjin as _core

from tenjin.tenjin import *  # noqa: F401,F403

# Re-export all names (including private) from the core module
# so that code like `tenjin._read_binary_file` continues to work.
import types as _types
for _name in dir(_core):
    _obj = getattr(_core, _name)
    if _name.startswith('__') and _name.endswith('__'):
        continue  # skip dunder attributes
    if not isinstance(_obj, _types.ModuleType) or _name in ('helpers', 'escaped', 'html', 'gae'):
        globals()[_name] = _obj
del _name, _obj, _types

__version__ = "1.1.2"
__license__ = "MIT License"
__all__ = ('Template', 'Engine')
