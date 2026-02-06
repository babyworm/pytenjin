# Overview

Tenjin is a very fast and full-featured template engine implemented in pure Python.

## Features

- [Very fast](#benchmark)
  - About 10 times faster than Django template
  - About 4 times faster than Cheetah
  - About 2 times faster than Mako
  - [Auto-escaping](#auto-escaping)
- Full featured
  - [Layout template](#layout-template)
  - [Partial template](#partial-template)
  - [Fragment cache](#fragment-cache)
  - [Capturing](#capturing)
  - [Preprocessing](#preprocessing)
  - [M17N Support](#m17n)
- Easy to learn
  - Because you can embed any python statements or expression in your template files
  - You don't have to study template-specific language
- Compact
  - Less than 2000 lines of code
  - Very ligthweight to load module (important for CGI script and Google App Engine)
- [Supports Google App Engine](#google-appengine)

## Install

PyTenjin supports Python 3.8 or later.

```console
$ pip install pytenjin
```

Or install from source:

```console
$ git clone https://github.com/babyworm/pytenjin.git
$ cd pytenjin
$ pip install .
```

## Benchmark

Tenjin package contains benchmark program.

**MacOS X 10.6 Snow Leopard, Intel CoreDuo2 2GHz, Memory 2GB**

```console
$ cd pytenjin-X.X.X/benchmark
$ python -V
Python 2.5.5
$ python bench.py -q -n 10000
compiling bench_cheetah.tmpl ... Compiling bench_cheetah.tmpl -> bench_cheetah.py (backup bench_cheetah.py.bak)
*** loading context data (file=bench_context.py)...
*** start benchmark
*** ntimes=10000
                                    utime     stime     total      real
tenjin                             3.7200    0.0300    3.7500    3.7593
tenjin-create                      4.7400    0.5800    5.3200    5.3128
tenjin-str                         2.4100    0.0300    2.4400    2.4326
tenjin-webext                      2.3700    0.0300    2.4000    2.4010
django                            87.3400    0.0700   87.4100   87.5328
django-create                    100.9000    0.3900  101.2900  101.4446
cheetah                           17.7300    0.0200   17.7500   17.7837
cheetah-create                    18.1300    0.0200   18.1500   18.2052
kid                              288.7300    0.3000  289.0300  289.3852
kid-create                       289.6800    0.4300  290.1100  290.5570
genshi                           179.2200    0.1700  179.3900  179.5859
genshi-create                    323.8500    0.9900  324.8400  325.2915
mako                               7.0000    0.0100    7.0100    7.0107
mako-create                        9.8100    0.8100   10.6200   10.6372
mako-nocache                     113.0900    0.5900  113.6800  113.7866
templetor                         10.6600    0.0100   10.6700   11.0737
templetor-create                 302.3700    1.8300  304.2000  304.6179
jinja2                             7.8900    0.0600    7.9500    7.9514
jinja2-create                    129.1300    0.7200  129.8500  130.6778
```

Versions:

- Python 2.5.5
- Tenjin 0.9.0
- Django 1.1.0
- Cheetah 2.2.2
- Kid 0.9.6
- Genshi 0.5.1
- Mako 0.2.5
- Templetor (web.py) 0.32
- Jinja2 2.2.1

This shows the followings.

- Tenjin is the fastest template engine.
- Cheetah's performance is good.
- Django's performance is not good.
- Kid's performance is worse. It is too slow.
- Genshi's performance is also worse. It is faster than Kid, but slower than others.
- Mako's performance is very good when module caching is enabled.
- Templetor's performance is not good for mod_python and worse for CGI program.
- Jinja's performance is very good if you can cache template object, but sad performance for CGI program.
