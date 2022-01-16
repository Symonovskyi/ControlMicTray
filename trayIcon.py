import sys
from ctypes import wintypes, WinDLL
import win32api
import win32gui
from ctypes import windll
from PyQt5 import QtGui, QtWidgets


WM_APPCOMMAND = 0x319
WM_HOTKEY = 0x0312
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000
VAL = 0x0002

class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        # Два состояния - 1 и 0
        self.status = bool()

        self.dll = WinDLL("winmm")

        self.menu = QtWidgets.QMenu()
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        self.turnMicro.triggered.connect(self.microControl)
        self.turnMicro.setCheckable(True)
        
        # self.testMenuItem = self.menu.addAction("Для тестов...")
        # self.testMenuItem.triggered.connect(self.testFunc)
        # self.testMenuItem.setCheckable(True)

        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {windll.winmm.waveInGetNumDevs()}")

        exitAction = self.menu.addAction("Выход")
        exitAction.triggered.connect(sys.exit)

        self.setIcon(QtGui.QIcon("images\\Microphone_dark.png"))
        self.setContextMenu(self.menu)
        self.setToolTip("Статус микрофона")
        self.show()

    def microControl(self):
        if self.turnMicro.isChecked():
            hwnd_active = win32gui.GetForegroundWindow()
            win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None,
            APPCOMMAND_MICROPHONE_VOLUME_MUTE)
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_ON.png"))
        else:
            hwnd_active = win32gui.GetForegroundWindow()
            win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None,
            APPCOMMAND_MICROPHONE_VOLUME_MUTE)
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_OFF.png"))

    # def testFunc(self):
    #     if self.testMenuItem.isEnabled():
    #         hwnd_active = win32gui.GetForegroundWindow()
    #         print(win32gui.PostMessage(hwnd_active, WM_APPCOMMAND,
    #             None, APPCOMMAND_MICROPHONE_VOLUME_MUTE))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
