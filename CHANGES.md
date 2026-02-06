# Changes

## Release 1.1.1 (2012-05-18)

- [Bugfix] Fix 'benchmark/bench.py' to work on PyPy.
- [Bugfix] Tweak document.

## Release 1.1.0 (2012-02-16)

- [Change] **IMPORTANT** Default cache file format is changed from marshal format to text format.
  You should remove all cache files to use this release: `find . -name '*.cache' | xargs rm`
