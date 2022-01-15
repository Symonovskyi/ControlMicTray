import sys
import win32api
import win32gui
from ctypes import windll
from PyQt5 import QtGui, QtWidgets

WM_APPCOMMAND = 0x319
APPCOMMAND_MICROPHONE_VOLUME_MUTE = 0x180000

class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        # Два состояния - 1 и 0
        self.status = bool()

        self.menu = QtWidgets.QMenu()
        turnMicroOn = self.menu.addAction("Вкл\выкл. микрофон")
        turnMicroOn.triggered.connect(self.Unmute)

        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {windll.winmm.waveInGetNumDevs()}")

        exitAction = self.menu.addAction("Выход")
        exitAction.triggered.connect(sys.exit)

        self.setIcon(QtGui.QIcon("images\\Microphone_light.png"))
        self.setContextMenu(self.menu)
        self.setToolTip("Статус микрофона")
        self.show()

    def Unmute(self):
        hwnd_active = win32gui.GetForegroundWindow()
        win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None,
            APPCOMMAND_MICROPHONE_VOLUME_MUTE)

        # win32api.SendMessage(hwnd_active, WM_APPCOMMAND, None,
        #     APPCOMMAND_MICROPHONE_VOLUME_MUTE)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
