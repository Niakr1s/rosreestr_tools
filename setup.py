import sys

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable('rosreestr_tools_GUI.py', shortcutDir='DesktopFolder', shortcutName='Rosreestr Tools GUI',
                          icon='static/rt.ico'),
               Executable('rosreestr_tools.py', shortcutDir='DesktopFolder', shortcutName='Rosreestr Tools',
                          icon='static/rt.ico'), ]

setup(name='rosreestr_tools', version='1.0.0', description='Rosreestr Tools', executables=executables,
      packages=['gui', 'scripts'], package_dir={'scripts': 'scripts', 'gui': 'gui'}, )
