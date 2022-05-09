import PyInstaller.__main__

PyInstaller.__main__.run([
    'main.py',
    '--onefile',
    '--windowed',
    '--icon=ui\\resources\\ControlMicTray.ico',
    '--name=ControlMicTray',
    '--distpath=EXE_DIST',
    '--workpath=EXE_BUILD',
    '--add-data=ui\\resources\;resources',
    '--add-data=database\\SQL\;SQL',
])

