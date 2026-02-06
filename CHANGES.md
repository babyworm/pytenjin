# Changes

## Release 1.1.2 (2026-02-06)

- [Fork] Forked from Tenjin 1.1.1 as PyTenjin, a maintained fork.
- [Change] Drop Python 2.x support; require Python 3.8+.
- [Change] Replace `cgi.escape` with `html.escape` (cgi module removed in Python 3.8).
- [Change] Replace `yaml.load()` with `yaml.safe_load()` for PyYAML 5.1+ compatibility.
- [Bugfix] Fix SyntaxWarning for invalid escape sequences in Python 3.12+.
- [Change] Modernize project structure with PEP 621 pyproject.toml (src layout).
- [Change] Convert HTML documentation to Markdown, split into sections.
- [Change] Update documentation for Python 3.8+ (remove Python 2.x examples, update install instructions).

## Release 1.1.1 (2012-05-18)

- [Bugfix] Fix 'benchmark/bench.py' to work on PyPy.
- [Bugfix] Tweak document.

## Release 1.1.0 (2012-02-16)

- [Change] **IMPORTANT** Default cache file format is changed from marshal format to text format.
  You should remove all cache files to use this release: `find . -name '*.cache' | xargs rm`
