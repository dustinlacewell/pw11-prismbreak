#! /usr/bin/env python

import os, sys, platform
minor = "py2{0}".format(sys.version_info[1])
if os.name == 'posix':
    if platform.system() == 'Darwin':
        sys.path.append(os.path.join("./lib/osx", minor))
    else:
        if platform.architecture()[0] == '64bit':
            sys.path.append(os.path.join("./lib/lin64", minor))
        else:
            sys.path.append(os.path.join("./lib/lin32", minor))
else:
    sys.path.append(os.path.join("./lib/win32", minor))

from src import app, scenes

editor = scenes.get('editor')()
app = app.Application()
app.run(editor)
