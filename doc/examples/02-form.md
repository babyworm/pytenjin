# Form

**Template: 'form.pyhtml':**

```html
<?py #@ARGS action, params, label ?>
<form action="${action}" method="post">
  <p>
    <label>Name:</label>
    <input type="text" name="name" value="${params.get('name')}" />
  </p>
  <p>
    <label>Gender:</label>
<?py gender = params.get('gender') ?>
<?py checked = {True:' checked="checked"', False:''} ?>
    <input type="radio" name="gender" value="M" #{checked[gender=='M']} />Man
    <input type="radio" name="gender" value="W" #{checked[gender=='W']} />Woman
  </p>
  <input type="submit" value="${label}" />
</form>
```

**Template: 'create.pyhtml':**

```html
<?py _context['title'] = 'Create user' ?>
<?py _context['label'] = 'Create' ?>
<?py _context['action'] = 'action.cgi' ?>
<?py include(':form') ?>
```

**Template: 'update.pyhtml':**

```html
<?py _context['title'] = 'Update user' ?>
<?py _context['label'] = 'Update' ?>
<?py _context['action'] = 'update.cgi' ?>
<?py include(':form') ?>
```

**Layout template: 'layout.pyhtml'**

```html
<html>
 <body>
  <h1>${title}</h1>
  <div class="main-content">
#{_content}
  </div>
 </body>
</html>
```

**Main program: 'main.py':**

```python
## create Engine object
import tenjin
from tenjin.helpers import *
engine = tenjin.Engine(postfix='.pyhtml', layout='layout.pyhtml')

## render template with context data
params = { 'name': 'Foo', 'gender': 'M' }
context = { 'params': params }
output = engine.render(':update', context)   # ':update' == 'update'+postfix
print(output)
```

**Result:**

```
$ python main.py
<html>
 <body>
  <h1>Update user</h1>
  <div class="main-content">
<form action="update.cgi" method="post">
  <p>
    <label>Name:</label>
    <input type="text" name="name" value="Foo" />
  </p>
  <p>
    <label>Gender:</label>
    <input type="radio" name="gender" value="M"  checked="checked" />Man
    <input type="radio" name="gender" value="W"  />Woman
  </p>
  <input type="submit" value="Update" />
</form>

  </div>
 </body>
</html>
```
