"""PyTenjin - a fast and full-featured template engine based on embedded Python.

Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com)
License: MIT License

This is a maintained fork of the original Tenjin template engine.
Original project: https://pypi.org/project/Tenjin/ by makoto kuwata.
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
    if not isinstance(_obj, _types.ModuleType) or _name in ('helpers', 'escaped', 'html'):
        globals()[_name] = _obj
del _name, _obj

__version__ = "1.0.0"
__license__ = "MIT License"
__all__ = ('Template', 'Engine')

# Proxy mutable module-level variables to tenjin.tenjin so that
# `tenjin.logger = logging` also sets `tenjin.tenjin.logger`.
# Without this, tenjin.tenjin's internal code would never see the update.
# PEP 562 only supports module __getattr__, not __setattr__, so we use
# a custom module subclass to intercept attribute setting.
import sys as _sys

_PROXIED_ATTRS = frozenset(('logger',))

class _TenjinModule(_types.ModuleType):
    def __setattr__(self, name, value):
        if name in _PROXIED_ATTRS:
            setattr(_core, name, value)
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in _PROXIED_ATTRS:
            return getattr(_core, name)
        raise AttributeError(f"module 'tenjin' has no attribute {name!r}")

# Replace module in sys.modules with our custom subclass instance
_this = _sys.modules[__name__]
_new = _TenjinModule(__name__, __doc__)
_new.__dict__.update({k: v for k, v in _this.__dict__.items()
                      if k not in _PROXIED_ATTRS})
_new.__path__ = _this.__path__
_new.__package__ = _this.__package__
_new.__loader__ = _this.__loader__
_new.__spec__ = _this.__spec__
_new.__file__ = _this.__file__
_sys.modules[__name__] = _new
