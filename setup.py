from distutils.core import setup
import py2exe, os, sys
import asyncio, psutil
import PyQt5

sys.argv.append('py2exe')

# def module_path():
#     if hasattr(sys, "frozen"):
#         return os.path.dirname(
#             sys.executable, sys.getfilesystemencoding( )
#         )
#     return os.path.dirname(__file__, sys.getfilesystemencoding( ))

includes = ['PyQt5', 'pycaw.pycaw', 'comtypes', 'keyboard', 'sys', 'ctypes',
    'PyQt5.QtGui', 'atexit']

data_files = [
        "images\\about.png",
        "images\\exit.png",
        "images\\off.png",
        "images\\on.png",
        "images\\settings.png",
        "images\\Microphone_dark_OFF.svg",
        "images\\Microphone_dark_ON.svg",
        "images\\Microphone_dark.svg",
        "images\\Microphone_light_OFF.svg",
        "images\\Microphone_light_ON.svg",
        "images\\Microphone_light.svg"]

setup(
    name='TrayMicControl',
    windows=[{'script':'trayIcon.py'}],
    options={
        'py2exe': {
            'bundle_files': 1,
            'compressed': True,
            'optimize': 2,
            'includes':includes, 
            },
        },
    data_files=[("", data_files)],
    zipfile=None
    )