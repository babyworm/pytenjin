###
### $Release: 1.0.0 $
### Copyright (c) 2024-present Hyun-Gyu Kim (babyworm@gmail.com). MIT License.
### Original: copyright(c) 2007-2012 kuwata-lab.com all rights reserved.
###

# This file is kept for backwards compatibility.
# Use `pytest` to run tests instead:
#   python -m pytest tests/ -v

import subprocess
import sys

if __name__ == '__main__':
    sys.exit(subprocess.call([sys.executable, '-m', 'pytest', '-v'] + sys.argv[1:]))
