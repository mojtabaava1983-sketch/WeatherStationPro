# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=['C:/Users/Amelsystem/Desktop/WeatherStation Pro/src'],
    binaries=[],
    datas=[('src', 'src'), ('config', 'config'), ('database', 'database'), ('vba', 'vba'), ('ui', 'ui')],
    hiddenimports=['sqlite3', '_sqlite3', 'weather_api', 'forecast', 'data_analysis', 'reporting', 'backup', 'plugins', 'scheduler', 'sunlight'],
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
    [],
    exclude_binaries=True,
    name='WeatherStationPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='WeatherStationPro',
)
