"""PyTenjin - a fast and full-featured template engine based on embedded Python.

This is a maintained fork of the original Tenjin template engine.
Original project: https://pypi.org/project/Tenjin/
Original author: makoto kuwata (kuwata-lab.com)

See User's Guide and examples for details.
"""

# Import everything from the core tenjin module
from tenjin.tenjin import *  # noqa: F401,F403
from tenjin.tenjin import (  # explicit re-exports
    Template,
    Engine,
    SafeTemplate,
    SafeEngine,
    Preprocessor,
    SafePreprocessor,
    TemplateSyntaxError,
    CacheStorage,
    MarshalCacheStorage,
    TextCacheStorage,
    MemoryCacheStorage,
    KeyValueStore,
    MemoryBaseStore,
    FileBaseStore,
    helpers,
    escaped,
    html,
    create_module,
    set_template_encoding,
)

__version__ = "1.1.1"
__license__ = "MIT License"
__all__ = ('Template', 'Engine')
