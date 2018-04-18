# -*- mode: python -*-

block_cipher = None


a = Analysis(['rosreestr_tools.py'],
             pathex=['D:\\git\\projects_main\\rosreestr_tools'],
             binaries=[],
             datas=[('static/*', 'static')],
             hiddenimports=['ezdxf', 'progressbar'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='rosreestr_tools',
          debug=False,
          strip=False,
          upx=True,
          console=True , icon='static\\rt.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='rosreestr_tools')
