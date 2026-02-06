# Google App Engine

> **NOTE:** Google App Engine's legacy runtime (webapp framework) used in these examples is no longer supported by Google. This section is kept for historical reference only.

**app.yaml**

```yaml
application: pytenjin-example
version: 1
runtime: python
api_version: 1

handlers:
- url: .*
  script: main.py
```

**main.py**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
### Example application for Google App Engine
###
### Before trying this example, copy 'tenjin.py' to 'lib' folder.
###
###     $ mkdir lib
###     $ cp ../../lib2/tenjin.py lib
###

import sys, os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

is_dev = (os.environ.get("SERVER_SOFTWARE") or "").startswith("Devel")

##
## import tenjin module and helper functions
##
sys.path.insert(0, "lib")        # necessary to import library under 'lib'
import tenjin
#tenjin.set_template_encoding("utf-8")            # if you like
from tenjin import *
from tenjin.helpers import *
from tenjin.helpers.html import *
import tenjin.gae; tenjin.gae.init()              # DON'T FORGET THIS LINE!

##
## engine object
##
tenjin_config = {
    "path":   ["templates"],
    "layout": "_layout.pyhtml",
}
engine = tenjin.Engine(**tenjin_config)
#engine = tenjin.SafeEngine(**tenjin_config)      # if you like

##
## logger
##
import logging
logger = logging.getLogger()
if is_dev:
    logger.setLevel(logging.DEBUG)
tenjin.logger = logger                            # set tenjin logger

##
## handler class
##
class MainHandler(webapp.RequestHandler):
    def get(self):
        context = { "page_title": "Tenjin Example in Google App Engine",
                    "environ": self.request.environ }
        html = engine.render("index.pyhtml", context)
        self.response.out.write(html)

##
## WSGI application
##
mappings = [
    ("/", MainHandler),
]

def main():
    app = webapp.WSGIApplication(mappings, debug=is_dev)
    util.run_wsgi_app(app)


if __name__ == "__main__":
    main()
```

**templates/index.pyhtml**

```html
<?py #@ARGS page_title, environ ?>

<h1>${page_title}</h1>

<table class="list">
  <tbody>
    <?py cycle = new_cycle('odd', 'even') ?>
    <?py for key in sorted(environ.keys()): ?>
    <tr class="${cycle()}">
      <th>${key}</th><td>${repr(environ[key])}</td>
    </tr>
    <?py #endfor ?>
  </tbody>
</table>
```

**templates/_layout.pyhtml**

```html
<?py #@ARGS _content, page_title ?>
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
    <meta http-equiv="Content-Style-Type" content="text/css">
    <meta http-equiv="Content-Script-Type" content="text/javascript">
    <title>${page_title}</title>
    <style type="text/css">
      .odd  {
        background: #FFE;
      }
      .even {
        background: #EFF;
      }
      table.list {
        border-collapse: collapse;
      }
      table.list th, table.list td {
        border: solid 1px #DDD;
        text-align: left;
        vertical-align: top;
        padding: 2px 5px;
      }
    </style>
  </head>
  <body>

{== _content ==}

  </body>
</html>
```
