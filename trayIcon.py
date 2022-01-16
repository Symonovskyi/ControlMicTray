import sys
from PyQt5 import QtGui, QtWidgets
from microphoneUtil import AudioUtilities as audio


class Main(QtWidgets.QSystemTrayIcon):
    def __init__(self):
        super().__init__()
        self.audio = audio()

        self.trayInit()

    def trayInit(self):
        self.menu = QtWidgets.QMenu()
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        self.turnMicro.triggered.connect(self.microControl)
        self.turnMicro.setCheckable(True)

        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {len(self.audio.micsCount)}")
        # quantityOfActiveMics.setEnabled(False)
        quantityOfActiveMics.triggered.connect(self.t)

        exitAction = self.menu.addAction("Выход")
        exitAction.triggered.connect(sys.exit)

        self.setContextMenu(self.menu)
        self.setToolTip("Статус микрофона")
        
        self.IsMutedCheck()

        self.show()

    def IsMutedCheck(self):
        if self.audio.GetMicrophoneState() == 0:
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_ON.svg"))
        else:
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_OFF.svg"))
        return

    def microControl(self):
        if self.turnMicro.isChecked():
            self.audio.UnMuteMicrophone()
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_ON.svg"))
        else:
            self.audio.MuteMicrophone()
            self.setIcon(QtGui.QIcon("images\\Microphone_dark_OFF.svg"))

    def t(self):
        print(self.audio.GetMicrophoneState())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    sys.exit(app.exec())
