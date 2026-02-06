import tenjin
from tenjin.helpers import *
import html
engine = tenjin.Engine(path=['views'], escapefunc="html.escape", tostrfunc="str")
print(engine.get_template('page.pyhtml').script)
