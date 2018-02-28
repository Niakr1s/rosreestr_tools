from cx_Freeze import setup, Executable

""" Type command in commandline: py setup.py build """
setup(
    name='dxfinxmlcheck',
    version='0.2',
    description='smth', executables=[Executable('console.py')], requires=['ezdxf', 'lxml'])
