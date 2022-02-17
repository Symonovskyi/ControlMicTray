# Built-in modules and own classes.
from sys import exit
from keyboard import add_hotkey, remove_hotkey
from database.databaseController import DatabaseController
from ui.aboutWindow import AboutWindow
from ui.settingsWindow import SettingsWindow
from logic.microphoneController import (MicrophoneController,
    CustomAudioEndpointVolumeCallback)

# 'pip install' modules.
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon


class TrayIcon(QSystemTrayIcon):
    '''
    Class that actually creates the tray icon and it's menu elements.
    Also, this class configures the behaviour of menu items.

    Methods:
    - check_mic_if_muted() - checks the actual state of mic, and mutes/unmutes
    it according to its status. Also, changes the tray icon and check mark on 
    the first element menu.
    - check_push_to_talk() - checks if the 'Walkie-Talkie' mode is enabled.
    '''

    def __init__(self):
        # For initializing Qt things.
        super().__init__()

        # Declaring Microphone and Database Controllers class instances.
        self.mic = MicrophoneController()
        self.db = DatabaseController()

        # Test callback for discovering mic status.
        self.callback = CustomAudioEndpointVolumeCallback(self)

        # Creating About Window instance.
        self.about_win = AboutWindow()

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        # Menu of tray.
        self.menu = QMenu()

        # Initializing and configuring 'On\Off Microphone' menu element.
        self.turn_micro = self.menu.addAction('')
        self.turn_micro.triggered.connect(self.check_mic_if_muted)

        # Initializing and configuring 'Walkie-talkie mode (push-to-talk)' menu element.
        self.push_to_talk = self.menu.addAction('Режим рации (push-to-talk)')
        self.push_to_talk.setCheckable(True)
        self.init_check_walkie()
        self.push_to_talk.triggered.connect(self.check_push_to_talk)

        self.menu.addSeparator()

        # Initializing and configuring 'Mics quantity: {quantity}' menu element.
        # quantity_of_active_mics = self.menu.addAction(
        #     f'Кол-ство микрофонов: {self.mic.get_devices_count}')
        # quantity_of_active_mics.setIcon(
        #     QIcon('ui\\resources\\Microphone_light.svg'))
        # quantity_of_active_mics.setEnabled(False)

        # Initializing and configuring 'Settings' menu element.
        settings_action = self.menu.addAction('Настройки')
        settings_action.setIcon(QIcon('ui\\resources\\Settings.svg'))

        self.menu.addSeparator()

        # Initializing and configuring 'About program' menu element.
        about_action = self.menu.addAction('О программе...')
        about_action.setIcon(QIcon('ui\\resources\\About.svg'))
        about_action.triggered.connect(self.about_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'Exit' menu element.
        exit_action = self.menu.addAction('Выход')
        exit_action.setIcon(QIcon('ui\\resources\\Exit.svg'))
        exit_action.triggered.connect(exit)

        # For properly themes working.
        self.settings_win = SettingsWindow(self, self.about_win)
        settings_action.triggered.connect(self.settings_win.show)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip('ControlMicTray')

        # Cheking mic status on startup.
        self.check_mic_if_muted(mode='init')

        self.mic.register_control_change_notify(self.callback)

    def check_mic_if_muted(self, mode=None):
        ''' According to mic status, these changes are applied:
        - Tray Icon;
        - First menu element icon;
        - Change text of the first menu element;
        - Mute/Unmute microphone if mode =! 'init'.
        '''
        mic_status = self.mic.get_mic_status
        if mode == 'init':
            if mic_status:
                self.setIcon(QIcon('ui\\resources\\Microphone_dark_OFF.svg'))
                self.turn_micro.setIcon(QIcon('ui\\resources\\Off.svg'))
                self.turn_micro.setText('Включить микрофон')
            else:
                self.setIcon(QIcon('ui\\resources\\Microphone_dark_ON.svg'))
                self.turn_micro.setIcon(QIcon('ui\\resources\\On.svg'))
                self.turn_micro.setText('Выключить микрофон')
        else:
            if mic_status:
                self.mic.unmute_mic()
                self.check_mic_if_muted(mode='init')
            else:
                self.mic.mute_mic()
                self.check_mic_if_muted(mode='init')

    def init_check_walkie(self):
        if self.db.walkie_status:
            self.push_to_talk.setChecked(True)
            self.check_push_to_talk()
        else:
            self.push_to_talk.setChecked(False)
            self.check_push_to_talk()

    def check_push_to_talk(self):
        self.db.mic_status = self.mic.get_mic_status
        if self.push_to_talk.isChecked():
            self.mic.mute_mic()
            self.turn_micro.setEnabled(False)
            self.push_to_talk.setIcon(QIcon('ui\\resources\\On.svg'))
            add_hotkey(self.db.hotkey_walkie, self.push_to_talk_pressed)
            add_hotkey(
                self.db.hotkey_walkie, self.push_to_talk_released, trigger_on_release=True)
            try:
                remove_hotkey(self.db.hotkey_mic)
            except: pass
            self.setIcon(QIcon('ui\\resources\\Microphone_dark_OFF.svg'))
        else:
            try:
                if self.db.mic_status:
                    self.mic.mute_mic()
                else:
                    self.mic.unmute_mic()
                self.turn_micro.setEnabled(True)
                self.push_to_talk.setIcon(QIcon('ui\\resources\\Off.svg'))
                add_hotkey(self.db.hotkey_mic, self.check_mic_if_muted)
                try:
                    remove_hotkey(self.db.hotkey_walkie)
                except: pass
                self.check_mic_if_muted(mode='init')
            except: pass

    def push_to_talk_pressed(self):
        self.setIcon(QIcon('ui\\resources\\Microphone_dark_ON.svg'))
        self.mic.unmute_mic()

    def push_to_talk_released(self):
        self.setIcon(QIcon('ui\\resources\\Microphone_dark_OFF.svg'))
        self.mic.mute_mic()
