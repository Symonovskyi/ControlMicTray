# Built-in modules and own classes.
from microphoneController import MicrophoneController
from databaseController import DatabaseController

# "pip install" modules.
from PyQt5.QtWidgets import QWidget, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from keyboard import add_hotkey, remove_all_hotkeys


class TrayIcon(QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - TrayInit() - initializates all tray menu elements and configuring them.
    - CheckMicIfMuted() - checks the actual state of mic, and mutes/unmutes it 
    according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    '''
    def __init__(self):
        # For initializing Qt things.
        super().__init__()

        # Microphone Controller class instance.
        self.mic = MicrophoneController()

        # Database Controller class instance.
        self.db = DatabaseController()

        # Settings Window class instance.
        self.settingsWin = SettingsWindow()

        # Menu of tray.
        self.menu = QMenu()

        # Calling the initialization func.
        self.TrayInit()

        # Adding hotkey for controling mic.
        add_hotkey('CTRL + SHIFT + Z', self.CheckMicIfMuted)

    def TrayInit(self):
        # Initializing and configuring "On\Off Microphone" menu element.
        self.turnMicro = self.menu.addAction("Вкл\выкл. микрофон")
        # Connecting menu element to appropriate method.
        self.turnMicro.triggered.connect(self.CheckMicIfMuted)

        self.menu.addSeparator()

        # Initializing and configuring "Mics quantity: {quantity}" menu element.
        quantityOfActiveMics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.getDevicesCount}")
        quantityOfActiveMics.setIcon(QIcon("images\\Microphone_light.svg"))
        quantityOfActiveMics.setEnabled(False)

        # Initializing and configuring "Settings" menu element.
        settingsAction = self.menu.addAction("Настройки")
        settingsAction.setIcon(QIcon("images\\settings.png"))
        settingsAction.triggered.connect(self.settingsWin.show)
        settingsAction.setEnabled(False)

        self.menu.addSeparator()

        # Initializing and configuring "About..." menu element.
        aboutAction = self.menu.addAction("О программе...")
        aboutAction.setIcon(QIcon("images\\about.png"))
        aboutAction.setEnabled(False)

        # Initializing and configuring "Exit" menu element.
        exitAction = self.menu.addAction("Выход")
        exitAction.setIcon(QIcon("images\\exit.png"))
        exitAction.triggered.connect(exit)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip("ControlMicTray")

        # Cheking mic status on startup.
        self.CheckMicIfMuted(mode="InterfaceOnly")

        self.show()

    def CheckMicIfMuted(self, mode=None):
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
                self.CheckMicIfMuted(mode="InterfaceOnly")
            elif micStatus == 1:
                self.mic.UnMuteMic()
                self.CheckMicIfMuted(mode="InterfaceOnly")


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        # self.setStyleSheet()
