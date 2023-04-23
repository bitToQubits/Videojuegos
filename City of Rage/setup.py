import sys
from cx_Freeze import setup, Executable

build_exe_options = {'include_files': ['data'], "excludes": ["tkinter"]}


setup(
    name ='City_of_Rage',
    author='rdn',
    version = '1.0',
    options={'build_exe': build_exe_options},
    executables = [Executable('city_of_rage.py', base = 'Win32GUI',icon = 'data\\axel.ico')])




#in command line(cmd)  change to current directory(cd) and write: "setup.py build" or "setup.py build_exe"
