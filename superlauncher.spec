# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['superlauncher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'cryptography', 'cryptography.fernet', 'jwt', 'PIL', 'PIL.Image',
        'psutil', 'win10toast', 'pypresence', 'random_username',
        'minecraft_launcher_lib', 'minecraft_launcher_lib.utils',
        'minecraft_launcher_lib.install', 'minecraft_launcher_lib.command',
        'minecraft_launcher_lib.fabric', 'minecraft_launcher_lib.forge',
        'minecraft_launcher_lib.quilt', 'packaging', 'tqdm',
        'PyQt6.QtCore', 'PyQt6.QtWidgets', 'PyQt6.QtGui',
        'PyQt6.QtNetwork', 'PyQt6.QtMultimedia', 'PyQt6.QtWebEngineWidgets',
        'PyQt6.QtCharts', 'requests',
    ],
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
    name='superlauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # True для отладки, False для продакшена
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=[r'assets\icon.png'],
)
