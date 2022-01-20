# Built-in modules.
from os import environ
from sys import argv, exit
from microphoneController import MicrophoneController

# "pip install" modules.
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon
from keyboard import add_hotkey


class TrayApp(QtWidgets.QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - TrayInit() - initializates all tray menu elements and configuring them.
    - CheckIfMuted() - checks the actual state of mic, and mutes/unmutes it 
    according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    '''
    def __init__(self):
        # For initializing Qt things.
        super().__init__()

        # Creating Microphone Controller class instance.
        self.mic = MicrophoneController()

        # Creating menu of tray.
        self.menu = QtWidgets.QMenu()

        # Calling the initialization func.
        self.TrayInit()

        # Adding hotkey for controling mic.
        add_hotkey('CTRL + SHIFT + Z', self.CheckIfMuted)

    def TrayInit(self):
        # Adding and configuring "On\Off Microphone" menu element.
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        # Connecting menu element to appropriate method.
        self.turnMicro.triggered.connect(self.CheckIfMuted)

        self.menu.addSeparator()

        # Adding and configuring "Mics quantity: {quantity}" menu element.
        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.getDevicesCount}")
        quantityOfActiveMics.setIcon(QIcon("images\\Microphone_light.svg"))
        quantityOfActiveMics.setEnabled(False)

        # Adding and configuring "Settings" menu element.
        settingsAction = self.menu.addAction("Настройки")
        settingsAction.setIcon(QIcon("images\\settings.png"))
        settingsAction.setEnabled(False)

        self.menu.addSeparator()

        # Adding and configuring "About..." menu element.
        aboutAction = self.menu.addAction("О программе...")
        aboutAction.setIcon(QIcon("images\\about.png"))
        aboutAction.setEnabled(False)

        # Adding and configuring "Exit" menu element.
        exitAction = self.menu.addAction("Выход")
        exitAction.setIcon(QIcon("images\\exit.png"))
        exitAction.triggered.connect(exit)

        # Connecting menu with tray.
        self.setContextMenu(self.menu)
        self.setToolTip("ControlMicTray")

        # Cheking mic status on startup.
        self.CheckIfMuted(mode="InterfaceOnly")

        self.show()

    def CheckIfMuted(self, mode=None):
        ''' According to mic status, these changes are applied:
        - Tray Icon;
        - First menu element icon;
        - Change text of the first menu element;
        - Mute/Unmute microphone if mode =! "InterfaceOnly".
        '''
        micStatus = self.mic.getMicMuteState
        if mode == "InterfaceOnly":
            if micStatus == 0:
                self.setIcon(QIcon("images\\Microphone_dark_ON.svg"))
                self.turnMicro.setIcon(QIcon("images\\on.png"))
                self.turnMicro.setText("Выключить микрофон")
            elif micStatus == 1:
                self.setIcon(QIcon("images\\Microphone_dark_OFF.svg"))
                self.turnMicro.setIcon(QIcon("images\\off.png"))
                self.turnMicro.setText("Включить микрофон")
        else:
            if micStatus == 0:
                self.mic.MuteMic()
                self.CheckIfMuted(mode="InterfaceOnly")
            elif micStatus == 1:
                self.mic.UnMuteMic()
                self.CheckIfMuted(mode="InterfaceOnly")


if __name__ == '__main__':
    app = QtWidgets.QApplication(argv)
    win = TrayApp()
    exit(app.exec())
