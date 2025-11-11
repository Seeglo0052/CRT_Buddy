# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

block_cipher = None

# Collect all PyQt6 modules
pyqt6_datas, pyqt6_binaries, pyqt6_hiddenimports = collect_all('PyQt6')

# Collect all PIL/Pillow modules
pil_datas, pil_binaries, pil_hiddenimports = collect_all('PIL')

# Collect all cv2/OpenCV modules
cv2_datas, cv2_binaries, cv2_hiddenimports = collect_all('cv2')

# Add pixel font
font_datas = [
    ('../DinkieBitmap-v1.5.0-KeDingKeMao/ttf/DinkieBitmap-9px.ttf', 'DinkieBitmap-v1.5.0-KeDingKeMao/ttf')
]

# Additional hidden imports
additional_hiddenimports = [
    'numpy',
    'numpy.core',
    'numpy.core._multiarray_umath',
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.sip',
    'PIL',
    'PIL.Image',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    'PIL.ImageEnhance',
    'cv2',
]

# Collect custom modules
custom_hiddenimports = collect_submodules('core') + \
                       collect_submodules('effects') + \
                       collect_submodules('generators')

# Combine all hidden imports
all_hiddenimports = list(set(
    pyqt6_hiddenimports + 
    pil_hiddenimports + 
    cv2_hiddenimports + 
    additional_hiddenimports +
    custom_hiddenimports
))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pyqt6_binaries + pil_binaries + cv2_binaries,
    datas=pyqt6_datas + pil_datas + cv2_datas + font_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'pandas',
        'scipy',
        'pytest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CRT_Buddy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
