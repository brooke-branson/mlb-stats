# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['PyQt_Gui.py'],
    pathex=[],
    binaries=[],
    datas=[('utilities.py', '.'), ('team.py', '.')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtWidgets', 'statsapi', 'pandas', 'matplotlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MLB_Stats',
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
)
app = BUNDLE(
    exe,
    name='MLB_Stats.app',
    icon=None,
    bundle_identifier=None,
)
