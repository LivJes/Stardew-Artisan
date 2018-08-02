# -*- mode: python -*-

block_cipher = None


a = Analysis(['stardew_artisan.py'],
             pathex=['.', 'D:\\Documents\\Stardew Artisan'],
             binaries=[],
             datas=[("Images", "Images"), ("crops_data.txt", "."), ("stardew_artisan_log.txt", "."), ("Keg.ico", "."), ("tk_ToolTip.py", ".")],
             hiddenimports=[],
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
          name='StardewArtisan',
          debug=False,
          strip=False,
          upx=False,
          console=False , icon='Keg.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='StardewArtisan')
