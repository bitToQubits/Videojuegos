import sys
from cx_Freeze import setup, Executable

build_exe_options = {'include_files': ['data'], "excludes": ["tkinter"]}


setup(
    name ='Urban_Champion',
    author='rdn',
    version = '1.0',
    options={'build_exe': build_exe_options},
    executables = [Executable('urban_champion.py', base = 'Win32GUI',icon = None)])




#in command line(cmd)  change to current directory(cd) and write: "setup.py build" or "setup.py build_exe"
