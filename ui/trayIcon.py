# Built-in modules and own classes.
from sys import exit
from database.databaseController import DatabaseController
from ui.aboutWindow import AboutWindow
from ui.settingsWindow import SettingsWindow
from logic.absolutePath import loadFile
from logic.microphoneController import (MicrophoneController,
    CustomAudioEndpointVolumeCallback)

# 'pip install' modules.
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QObject, pyqtSignal
import keyboard as kb


class HotkeysManager(QObject):
    normal_mode = pyqtSignal()
    walkie_mode_on = pyqtSignal()
    walkie_mode_off = pyqtSignal()
    db = DatabaseController()

    normal_hotkey = None
    walkie_hotkey_on = None
    walkie_hotkey_off = None

    def register_normal_mode_hotkey(self):
        try:
            kb.remove_hotkey(self.walkie_hotkey_on)
            kb.remove_hotkey(self.walkie_hotkey_off)
        except Exception: pass

        self.normal_hotkey = kb.add_hotkey(
            self.db.hotkey_mic, self.normal_mode.emit, suppress=True)

    def register_walkie_mode_hotkey(self):
        try:
            kb.remove_hotkey(self.normal_hotkey)
        except Exception: pass

        self.walkie_hotkey_on = kb.add_hotkey(
            self.db.hotkey_walkie.upper(), self.walkie_mode_on.emit, suppress=True,\
                trigger_on_release=False)
        self.walkie_hotkey_off = kb.add_hotkey(
            self.db.hotkey_walkie.lower(), self.walkie_mode_off.emit, suppress=True,\
                trigger_on_release=True)

    def re_register_normal_mode_hotkey(self):
        kb.remove_hotkey(self.normal_hotkey)
        self.normal_hotkey = kb.add_hotkey(
            self.db.hotkey_mic, self.normal_mode.emit, suppress=True)

    def re_register_walkie_mode_hotkey(self):
        kb.remove_hotkey(self.walkie_hotkey_on)
        kb.remove_hotkey(self.walkie_hotkey_off)

        self.walkie_hotkey_on = kb.add_hotkey(
            self.db.hotkey_walkie.upper(), self.walkie_mode_on.emit, suppress=True,\
                trigger_on_release=False)
        self.walkie_hotkey_off = kb.add_hotkey(
            self.db.hotkey_walkie.lower(), self.walkie_mode_off.emit, suppress=True,\
                trigger_on_release=True)


class CustomQMenu(QMenu):
    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            e.ignore()
        else:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() != Qt.MouseButton.LeftButton:
            e.ignore()
        else:
            super().mouseReleaseEvent(e)


class TrayIcon(QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - change_mic_status() - checks the actual state of mic, and mutes/unmutes
    it according to its status. Also, changes the tray icon and check mark on
    the first element menu.
    - change_mode_to_walkie() - checks if the 'Walkie-Talkie' mode is enabled.
    '''

    def __init__(self, parent=None):
        # For initializing Qt things.
        super().__init__(parent)

        # Declaring Microphone and Database Controllers class instances.
        self.mic = MicrophoneController()
        self.db = DatabaseController()

        # Test callback for discovering mic status.
        self.callback = CustomAudioEndpointVolumeCallback(self)

        # Creating About Window instance.
        self.about_win = AboutWindow()

        # Creating Hotkeys Manager instance.
        self.hotkeys = HotkeysManager()

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        # Menu of tray.
        self.menu = CustomQMenu()

        # Initializing and configuring 'On\Off Microphone' menu element.
        self.turn_micro = self.menu.addAction('Вкл.\Выкл. микрофон')
        self.turn_micro.triggered.connect(self.change_mic_status)

        # Initializing and configuring 'Walkie-talkie mode' menu element.
        self.push_to_talk = self.menu.addAction('Вкл.\Выкл. режим рации')
        self.push_to_talk.setCheckable(True)
        self.push_to_talk.triggered.connect(self.mode_switcher)

        self.menu.addSeparator()

        # Initializing and configuring 'Settings' menu element.
        settings_action = self.menu.addAction('Настройки')
        settings_action.setIcon(QIcon(loadFile('ui\\resources\\Settings.svg')))

        self.menu.addSeparator()

        # Initializing and configuring 'About program' menu element.
        about_action = self.menu.addAction('О программе...')
        about_action.setIcon(QIcon(loadFile('ui\\resources\\About.svg')))
        about_action.triggered.connect(self.about_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'Exit' menu element.
        exit_action = self.menu.addAction('Выход')
        exit_action.setIcon(QIcon(loadFile('ui\\resources\\Exit.svg')))
        exit_action.triggered.connect(exit)

        # For properly themes working.
        self.settings_win = SettingsWindow(self, self.about_win, self.hotkeys)
        settings_action.triggered.connect(self.settings_win.show)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip('ControlMicTray')

        # Setting icons to menu items accordingly to ControlMicTray mode.
        self.change_icons_according_to_status()

        # Cheking ControlMicTray mode on startup.
        self.mode_switcher()

        # Connect hotkey signals to appropriate actions (slots).
        self.hotkeys.normal_mode.connect(self.change_mic_status)
        self.hotkeys.walkie_mode_on.connect(self.mic.unmute_mic)
        self.hotkeys.walkie_mode_off.connect(self.mic.mute_mic)

        # Register callback controlling when mic changes it's state.
        self.mic.register_control_change_notify(self.callback)

    def change_icons_according_to_status(self):
        if self.db.walkie_status:
            self.setIcon(QIcon(loadFile('ui\\resources\\Microphone_dark_OFF.svg')))
            self.push_to_talk.setIcon(QIcon(loadFile('ui\\resources\\On.svg')))
            self.turn_micro.setIcon(QIcon(loadFile('ui\\resources\\Off.svg')))
        else:
            self.push_to_talk.setIcon(QIcon(loadFile('ui\\resources\\Off.svg')))
            if self.mic.get_mic_status:
                self.setIcon(QIcon(loadFile('ui\\resources\\Microphone_dark_OFF.svg')))
                self.turn_micro.setIcon(QIcon(loadFile('ui\\resources\\Off.svg')))
            else:
                self.setIcon(QIcon(loadFile('ui\\resources\\Microphone_dark_ON.svg')))
                self.turn_micro.setIcon(QIcon(loadFile('ui\\resources\\On.svg')))

    def change_mic_status(self):
        '''
        According to mic status, method sets mic state to "muted" or "unmuted".
        '''
        if self.mic.get_mic_status:
            self.mic.unmute_mic()
        else:
            self.mic.mute_mic()

    def mode_switcher(self):
        '''
        Switches ControlMicTray mode according to walkie-talkie menu enrty status.
        '''
        # Talkie-Walkie Mode enabled.
        if self.push_to_talk.isChecked():
            # First of all, forced muting mic in this mode.
            self.mic.mute_mic()

            # Setting walkie-talkie status turned on in db. Also cheking for
            # appropriate changing icons in menu.
            self.db.walkie_status = 1
            self.change_icons_according_to_status()

            # Disabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(False)
            self.settings_win.HotkeyMic.setEnabled(False)
            # Enabling input field for hotkey of walkie-talkie mode.
            self.settings_win.HotkeyWalkie.setEnabled(True)

            # Register hotkey for this mode.
            self.hotkeys.register_walkie_mode_hotkey()
        # Normal mode enabled.
        else:
            # Setting walkie-talkie status turned off in db. Also cheking for
            # appropriate changing icons in menu.
            self.db.walkie_status = 0
            self.change_icons_according_to_status()

            # Enabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(True)
            self.settings_win.HotkeyMic.setEnabled(True)
            # Disabling input field for hotkey of walkie-talkie mode.
            self.settings_win.HotkeyWalkie.setEnabled(False)

            # Register hotkey for this mode.
            self.hotkeys.register_normal_mode_hotkey()
