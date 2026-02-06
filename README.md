# PyTenjin

This is a maintained fork of the original [Tenjin](https://github.com/kwatch/tenjin) template engine, which is no longer actively maintained.

Original project: https://pypi.org/project/Tenjin/

## About

PyTenjin is a very fast and full-featured template engine. You can embed Python statements and expressions into your template file. PyTenjin converts it into Python script and evaluates it.

## Features

- **Very fast**: Approximately 10x faster than Django, 4x faster than Cheetah, 2x faster than Mako
- **Full featured**:
  - Nestable layout templates
  - Partial templates
  - Fragment caching
  - Capturing
  - Preprocessing
- **Easy to learn**: Simple and intuitive syntax

## Installation

```bash
pip install pytenjin
```

## Quick Example

**Template file (table.pyhtml):**

```html
<?py #@ARGS items ?>
<table>
  <?py for item in items: ?>
  <tr>
    <td>${item}</td>
  </tr>
  <?py #end ?>
</table>
```

**Python code:**

```python
import tenjin
from tenjin.helpers import *

engine = tenjin.Engine()
context = {'items': ['AAA', 'BBB', 'CCC']}
html = engine.render('table.pyhtml', context)
print(html)
```

**Output:**

```html
<table>
  <tr>
    <td>AAA</td>
  </tr>
  <tr>
    <td>BBB</td>
  </tr>
  <tr>
    <td>CCC</td>
  </tr>
</table>
```

## License

MIT License

Original copyright by kuwata-lab.com
