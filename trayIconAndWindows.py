# Built-in modules and own classes.
from microphoneController import MicrophoneController
from databaseController import DatabaseController

# "pip install" modules.
from PyQt5.QtWidgets import (
    QWidget, QSystemTrayIcon, QMenu, QGridLayout, QLabel, QComboBox)
from PyQt5.QtGui import QIcon
from keyboard import add_hotkey, on_press, hook


class TrayIcon(QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - check_mic_if_muted() - checks the actual state of mic, and mutes/unmutes it 
    according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    - check_push_to_talk() - checks if the "Walkie-Talkie" mode is enabled.
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
        self.__tray_init()

        # Applying user settings.
        self.__apply_user_settings()

    def __tray_init(self):
        # Initializing and configuring "On\Off Microphone" menu element.
        self.turn_micro = self.menu.addAction("Вкл\выкл. микрофон")
        self.turn_micro.triggered.connect(self.check_mic_if_muted)

        # Initializing and configuring "Walkie-talkie mode (push-to-talk)" menu element.
        self.push_to_talk = self.menu.addAction("Режим рации (push-to-talk)")
        self.push_to_talk.triggered.connect(self.check_push_to_talk)
        self.push_to_talk.setEnabled(False)

        self.menu.addSeparator()

        # Initializing and configuring "Mics quantity: {quantity}" menu element.
        quantity_of_active_mics = self.menu.addAction(
            f"Кол-ство микрофонов: {self.mic.get_devices_count}")
        quantity_of_active_mics.setIcon(QIcon("images\\Microphone_light.svg"))
        quantity_of_active_mics.setEnabled(False)

        # Initializing and configuring "Settings" menu element.
        settings_action = self.menu.addAction("Настройки")
        settings_action.setIcon(QIcon("images\\settings.png"))
        settings_action.triggered.connect(self.settingsWin.show)
        # settings_action.setEnabled(False)

        self.menu.addSeparator()

        # Initializing and configuring "About..." menu element.
        about_action = self.menu.addAction("О программе...")
        about_action.setIcon(QIcon("images\\about.png"))
        about_action.setEnabled(False)

        self.menu.addSeparator()

        # Initializing and configuring "Exit" menu element.
        exit_action = self.menu.addAction("Выход")
        exit_action.setIcon(QIcon("images\\exit.png"))
        exit_action.triggered.connect(exit)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip("ControlMicTray")

        # Cheking mic status on startup.
        self.check_mic_if_muted(mode="InterfaceOnly")

        self.show()

    def __apply_user_settings(self):
        # Adding hotkey for controling mic.
        add_hotkey(self.db.user_hotkey_mic, self.check_mic_if_muted)

    def check_mic_if_muted(self, mode=None):
        ''' According to mic status, these changes are applied:
        - Tray Icon;
        - First menu element icon;
        - Change text of the first menu element;
        - Mute/Unmute microphone if mode =! "InterfaceOnly".
        '''
        mic_status = self.mic.get_mic_muted_state
        if mode == "InterfaceOnly":
            if mic_status:
                self.setIcon(QIcon("images\\Microphone_dark_OFF.svg"))
                self.turn_micro.setIcon(QIcon("images\\off.png"))
                self.turn_micro.setText("Включить микрофон")
            else:
                self.setIcon(QIcon("images\\Microphone_dark_ON.svg"))
                self.turn_micro.setIcon(QIcon("images\\on.png"))
                self.turn_micro.setText("Выключить микрофон")
        else:
            if mic_status:
                self.mic.unmute_mic()
                self.check_mic_if_muted(mode="InterfaceOnly")
            else:
                self.mic.mute_mic()
                self.check_mic_if_muted(mode="InterfaceOnly")

    def check_push_to_talk(self):
        pass


class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configuring window.
        self.__configureWin()

    def closeEvent(self, event):
        self.destroy()

    def __configureWin(self):
        self.setFixedHeight(500)
        self.setFixedWidth(500)
        self.setWindowTitle('Настройки')
        self.setWindowIcon(QIcon('images\\Microphone_dark.svg'))

        lay = QGridLayout(self)

        lang_selection_label = QLabel("Выбрать язык:")

        combo = QComboBox()
        combo.addItems(
            ["Русский", "Английский", "Украинский", "Китайский"])

        lay.addWidget(lang_selection_label)
        lay.addWidget(combo)

        self.setLayout(lay)
        self.__setStyles()

    def __setStyles(self):
        self.setStyleSheet("""
            background-color: #234768;
        """)


class AboutWindow(QWidget):
    pass
