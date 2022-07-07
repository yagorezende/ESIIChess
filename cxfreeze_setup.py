"""
to build an executable for the current target (need cx_Freeze installed):
python cxfreeze_setup.py build
"""

import sys

from cx_Freeze import Executable, setup

# Dependencies are automatically detected, but it might need
# fine tuning.
base = None
build_options = {
    'packages': [],
    'excludes': ["tkinter", "unittest", "email", "http", "html", "xml", "pydoc"],
    'include_files': [('./assets', './assets')],
    'optimize': 2,
}

if sys.platform == 'win32':
    base = 'Win32GUI'
    build_options['include_msvcr'] = True

executables = [
    Executable('main.py', base=base, target_name='ESIIChess')
]

setup(name='ESIIChess',
      version='1.0',
      description='A chess game developed for the "Software Engineering 2" class.',
      options={'build_exe': build_options},
      executables=executables)
