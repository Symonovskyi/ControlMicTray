# Built-in modules and own classes.
from sys import exit
from webbrowser import open_new_tab
from database.databaseController import DatabaseController
from logic.microphoneController import MicrophoneController, COMObject,\
    IAudioEndpointVolumeCallback

# 'pip install' modules.
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from pynput.keyboard import Listener, GlobalHotKeys
from ui.aboutWindow import AboutWindow

from ui.settingsWindow import SettingsWindow


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

        # Microphone Controller class instance.
        self.mic = MicrophoneController()

        # Database Controller class instance.
        self.db = DatabaseController()

        # Test callback for discovering mic status.
        self.callback = CustomAudioEndpointVolumeCallback()

        # Creating Settings Window instance.
        self.settings_win = SettingsWindow()

        # Creating Settings Window instance.
        self.about_win = AboutWindow()

        # Calling the initialization ui func.
        self.setup_ui()

        # Applying user settings.
        self.apply_user_settings()

    def setup_ui(self):
        # Menu of tray. Also, configuring stylesheet for menu.
        self.menu = QMenu()
        self.menu.setStyleSheet(
            """QMenu { color: #BECBD1;
            background-color: #273238;
            border: 1px solid #04BED5;
            border-radius: 5px; }""")

        # Initializing and configuring 'On\Off Microphone' menu element.
        self.turn_micro = self.menu.addAction('')
        self.turn_micro.triggered.connect(self.check_mic_if_muted)

        # Initializing and configuring 'Walkie-talkie mode (push-to-talk)' menu element.
        self.push_to_talk = self.menu.addAction('Режим рации (push-to-talk)')
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
        settings_action.setIcon(QIcon('ui\\resources\\settings.svg'))
        settings_action.triggered.connect(self.settings_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'About program' menu element.
        about_action = self.menu.addAction('О программе...')
        about_action.setIcon(QIcon('ui\\resources\\about.svg'))
        about_action.triggered.connect(self.about_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'Exit' menu element.
        exit_action = self.menu.addAction('Выход')
        exit_action.setIcon(QIcon('ui\\resources\\exit.svg'))
        exit_action.triggered.connect(exit)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip('ControlMicTray')

        # Cheking mic status on startup.
        self.check_mic_if_muted(mode='init')
        self.walkie_talkie_status = False
        self.check_push_to_talk(mode='init')

        self.mic.register_control_change_notify(
            self.callback)

    def apply_user_settings(self):
        # Adding hotkeys for controling mic.
        hotkeys = GlobalHotKeys({
            '<Scroll_lock>': self.check_mic_if_muted,
            '<Home>': self.check_push_to_talk
        })

        # Hotkey listener for mic.
        mic_listener = Listener(
            on_press=hotkeys._hotkeys[0].press,
            on_release=hotkeys._hotkeys[0].release
        )
        mic_listener.start()

        # Hotkey listener for walkie-talkie.
        walkie_listener = Listener(
            on_press=hotkeys._hotkeys[1].press,
            on_release=hotkeys._hotkeys[1].release
        )
        walkie_listener.start()

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

    def check_push_to_talk(self, mode=None):
        pass


class CustomAudioEndpointVolumeCallback(COMObject):
    _com_interfaces_ = [IAudioEndpointVolumeCallback]

    def OnNotify(self, pNotify):
        TrayIcon().check_push_to_talk()


class TrayIconStyles:
    tray_icon = TrayIcon()

    def dark_theme(self):
        pass

    def white_theme(self):
        pass
