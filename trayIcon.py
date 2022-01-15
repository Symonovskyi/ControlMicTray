import sys
#import ctypes
from ctypes import windll
from PyQt5 import QtGui, QtWidgets


class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        # Два состояния - 1 и 0
        self.status = bool()

        icon = QtGui.QIcon("icon.ico")

        self.menu = QtWidgets.QMenu()
        turnMicroOn = self.menu.addAction("Включить микрофон")

        turnMicroOff = self.menu.addAction("Выключить микрофон")

        quantityOfActiveMics = self.menu.addAction(f"{windll.winmm.waveInGetNumDevs()}")

        exitAction = self.menu.addAction("Выход")
        exitAction.triggered.connect(sys.exit)

        self.setIcon(icon)
        self.setContextMenu(self.menu)
        self.setToolTip("Статус микрофона")
        self.show()

#    def signalStatus(self):


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
