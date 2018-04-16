import os
import site

from PyInstaller.utils.hooks import collect_submodules

module_to_hook = 'progressbar'
datas = [(os.path.join(site.getsitepackages()[1], module_to_hook), module_to_hook)]

hiddenimports = collect_submodules(module_to_hook)
