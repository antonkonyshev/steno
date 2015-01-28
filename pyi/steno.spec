# -*- mode: python -*-

import sys
import os.path as op

from steno import steno

projectpath = op.abspath(op.join(op.dirname(steno.__file__), op.pardir))
imgrelpath = op.join('steno', 'resources', 'img', '{0}.png')
imgabspath = op.abspath(op.join(projectpath, imgrelpath))

a = Analysis(['steno/defaults.py', 'steno/dialogs.py', 'steno/droptargets.py', 'steno/events.py', 'steno/ids.py', 'steno/__init__.py', 'steno/player_content.py', 'steno/player_gui.py', 'steno/player.py', 'steno/player_settings.py', 'steno/steno.py', 'steno/translator.py', 'steno/verificator.py', 'steno/widgets.py'],
             pathex=[projectpath],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [ (imgrelpath.format(img), imgabspath.format(img), 'DATA') for img in [
            'help', 'icon_64x64', 'icon_128x128', 'pause', 'play', 'repeat', 'stop'] ]
a.datas += [ (op.join('steno', 'resources', 'html', 'user_manual.html'),
              op.join(projectpath, 'steno', 'resources', 'html', 'user_manual.html'),
              'DATA') ]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='steno.exe' if sys.platform.startswith('win') else 'steno.bin',
          debug=False,
          strip=None,
          upx=True,
          console=False )
