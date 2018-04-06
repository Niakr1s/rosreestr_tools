from cx_Freeze import setup, Executable

executables = [Executable('rosreestr_tools.py')]

setup(name='rosreestr_tools', version='0.1.1', description='Rosreestr Tools', executables=executables,
      package_dir={'': 'scripts'}, )
