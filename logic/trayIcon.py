# Built-in modules and own classes.
from sys import exit
from database.databaseController import DatabaseController
from logic.aboutWindow import AboutWindow
from logic.settingsWindow import SettingsWindow
from absolutePath import loadFile
from logic.microphoneController import (MicrophoneController,
    CustomMicrophoneEndpointVolumeCallback)

# 'pip install' modules.
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from keyboard import add_hotkey as kb_add_hotkey, remove_hotkey as kb_remove_hotkey


class HotkeysManager(QObject):
    '''
    Implements hotkey manager functionality.

    Attributes:
        - db (DatabaseController): for getting hotkeys shortcuts from database.
        - normal_mode_hotkey_signal (pyqtSignal): Qt custom signal for normal
        mode hotkey.
        - walkie_mode_on_hotkey_signal (pyqtSignal): Qt custom signal for
        walkie-talkie mode hotkey. Used when user using walkie mode and
        holds hotkey so mic gets unmuted.
        - walkie_mode_off_hotkey_signal (pyqtSignal): Qt custom signal for
        walkie-talkie mode hotkey. Used when user using walkie mode and
        releases hotkey so mic gets muted.
        - normal_hotkey_attr (None | keyboard.KeyboardEvent): handles reference
        to normal hotkey keyboard event.
        - walkie_hotkey_on_attr (None | keyboard.KeyboardEvent): handles
        reference to "walkie hotkey on" keyboard event.
        - walkie_hotkey_off_attr (None | keyboard.KeyboardEvent): handles
        reference to "walkie hotkey off" keyboard event.
    '''
    db = DatabaseController()

    normal_mode_hotkey_signal = pyqtSignal()
    walkie_mode_on_hotkey_signal = pyqtSignal()
    walkie_mode_off_hotkey_signal = pyqtSignal()

    normal_hotkey_attr = None
    walkie_hotkey_on_attr = None
    walkie_hotkey_off_attr = None

    def register_normal_mode_hotkey(self):
        '''
        Registers hotkey for normal app mode using shortcuts from db.
        '''
        if not self.db.hotkey_mic == 'unmapped':
            self.normal_hotkey_attr = kb_add_hotkey(self.db.hotkey_mic,\
                self.normal_mode_hotkey_signal.emit)

    def register_walkie_mode_hotkey(self):
        '''
        Registers hotkey for walkie-talkie app mode using shortcuts from db.
        '''
        if not self.db.hotkey_walkie == 'unmapped':
            self.walkie_hotkey_on_attr = kb_add_hotkey(
                self.db.hotkey_walkie.upper(),\
                    self.walkie_mode_on_hotkey_signal.emit,\
                        trigger_on_release=False)
            self.walkie_hotkey_off_attr = kb_add_hotkey(
                self.db.hotkey_walkie.lower(),\
                    self.walkie_mode_off_hotkey_signal.emit,\
                        trigger_on_release=True)

    def re_register_normal_mode_hotkey(self):
        '''
        Removes actual registered hotkey for nomral app mode and registers
        new hotkey, using shortcut from db.
        '''
        try:
            kb_remove_hotkey(self.normal_hotkey_attr)
        except: pass
        self.register_normal_mode_hotkey()

    def re_register_walkie_mode_hotkey(self):
        '''
        Removes actual registered hotkeys for walkie-talkie app mode and
        registers new hotkeys, using shortcuts from db.
        '''
        try:
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
        except: pass
        self.register_walkie_mode_hotkey()

    def switch_hotkey_mode(self):
        '''
        Removes non-actual mode hotkey(s) and registers hotkey(s) for
        switched app mode.
        '''
        if self.db.walkie_status:
            kb_remove_hotkey(self.normal_hotkey_attr)
            self.register_walkie_mode_hotkey()
        else:
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
            self.register_normal_mode_hotkey()

    def unregister_normal_mode_hotkey(self):
        try:
            kb_remove_hotkey(self.normal_hotkey_attr)
        except: pass
        self.db.hotkey_mic = 'unmapped'

    def unregister_walkie_mode_hotkey(self):
        try:
            kb_remove_hotkey(self.walkie_hotkey_on_attr)
            kb_remove_hotkey(self.walkie_hotkey_off_attr)
        except: pass
        self.db.hotkey_walkie = 'unmapped'


class CustomQMenu(QMenu):
    '''
    Implements all general functionality of Qt Menu.

    Reimplements methods mousePressEvent() and mouseReleaseEvent(), disabling
    any mouse button pressing and releasing, except left mouse button.
    '''
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        '''
        Reimplemented method. Disables any mouse button pressing, except
        left mouse button.

        Args:
            - e (PyQt6.QtGui.QMouseEvent): Qt mouse event.
        '''
        if e.button() != Qt.MouseButton.LeftButton:
            e.ignore()
        else:
            super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        '''
        Reimplemented method. Disables any mouse button releasing, except
        left mouse button.

        Args:
            - e (PyQt6.QtGui.QMouseEvent): Qt mouse event.
        '''
        if e.button() != Qt.MouseButton.LeftButton:
            e.ignore()
        else:
            super().mouseReleaseEvent(e)


class TrayIcon(QSystemTrayIcon):
    '''
    Implements main Qt System Tray Icon functionality.

    What happens at init stage (app startup):
        - If this is first app startup ever, creating database and tables
        filling them with different default app data;
        - Generating Qt Menu custom elements;
        - Connecting menu elements signals to their appropriate slots;
        - Setting up all icons, registering hotkeys and callback on mic status
        changing, accroding to app mode on startup.

    Methods functionality:
        - change_mic_status_on_mouse_click():
        Changes mic status on single mouse click of tray icon.
        - change_icons_according_to_status():
        Change menu and app icons color accroding to app mode switches;
        - change_mic_status():
        Change mic status according to it's actual status
        (If mic is muted it gets unmuted, conversely otherwise).
        - mode_switcher():
        Switches app mode according to the walkie-talkie menu element status.
    '''
    def __init__(self):
        # Initializing main Qt functionality of Qt System Tray Icon.
        super().__init__()

        # Declaring a bunch of instaces:
        # Microphone instance;
        # Database Controller instance;
        # Callback instance for changing icons status on mic change status;
        # "About" Window instance;
        # Hotkeys Manager instance.
        self.mic = MicrophoneController()
        self.db = DatabaseController()
        self.callback = CustomMicrophoneEndpointVolumeCallback(self)
        self.about_win = AboutWindow()
        self.hotkeys = HotkeysManager()

        # Calling the initialization ui method.
        self.__setup_ui()

    def __setup_ui(self):
        '''
        Setting up all menu elements, and connecting signals to their slots.
        For more details, see docstring to this class in
        "What happens at init stage" section.
        '''
        # See docstings of this class to find out why using custom Qt Menu.
        self.menu = CustomQMenu()

        # Initializing and configuring 'On\Off Microphone' menu element.
        self.turn_micro = self.menu.addAction('Вкл.\Выкл. микрофон')
        self.turn_micro.triggered.connect(self.change_mic_status)

        # Initializing and configuring 'Walkie-talkie mode' menu element.
        self.push_to_talk = self.menu.addAction('Вкл.\Выкл. режим рации')
        self.push_to_talk.triggered.connect(self.mode_switcher)

        self.menu.addSeparator()

        # Initializing 'Settings' menu element.
        settings_action = self.menu.addAction('Настройки')
        settings_action.setIcon(QIcon(loadFile('ui/resources/Settings.svg')))

        self.menu.addSeparator()

        # Initializing and configuring 'About program' menu element.
        about_action = self.menu.addAction('О программе...')
        about_action.setIcon(QIcon(loadFile('ui/resources/About.svg')))
        about_action.triggered.connect(self.about_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'Exit' menu element.
        exit_action = self.menu.addAction('Выход')
        exit_action.setIcon(QIcon(loadFile('ui/resources/Exit.svg')))
        exit_action.triggered.connect(exit)

        # Declaring Settings Window instance here for proerly
        # theme initializing. Also configuring 'Settings' menu element.
        self.settings_win = SettingsWindow(self, self.about_win, self.hotkeys)
        settings_action.triggered.connect(self.settings_win.show)

        # Connecting menu with tray and setting tooltip for tray icon.
        self.setContextMenu(self.menu)
        self.setToolTip('ControlMicTray')

        # Setting icons to menu items accordingly to ControlMicTray mode.
        self.change_icons_according_to_mic_status()

        # Connect hotkey signals to appropriate actions (slots).
        self.hotkeys.normal_mode_hotkey_signal.connect(self.change_mic_status)
        self.hotkeys.walkie_mode_on_hotkey_signal.connect(self.mic.unmute_mic)
        self.hotkeys.walkie_mode_off_hotkey_signal.connect(self.mic.mute_mic)

        # Connect single mouse click on tray icon to changing mic status.
        self.activated.connect(self.change_mic_status_on_mouse_click)

        # Registering hotkeys and configuring menu entries accordingly to ControlMicTray mode.
        self.init_mode_switcher()

        # Register callback controlling when mic changes it's state.
        self.mic.register_control_change_notify(self.callback)

    def change_mic_status_on_mouse_click(self, reason):
        '''
        Changes mic status by single mouse click on tray icon.
        '''
        if reason == self.ActivationReason.Trigger and not self.db.walkie_status:
            self.change_mic_status()

    def change_icons_according_to_mic_status(self):
        '''Changes icons according to mic status and app mode.'''

        if self.db.walkie_status:
            self.turn_micro.setIcon(QIcon(loadFile('ui/resources/Off.svg')))
            self.push_to_talk.setIcon(QIcon(loadFile('ui/resources/On.svg')))
        else:
            self.push_to_talk.setIcon(QIcon(loadFile('ui/resources/Off.svg')))

        if self.mic.get_mic_status:
            self.setIcon(QIcon(loadFile('ui/resources/Microphone_dark_OFF.svg')))
            self.turn_micro.setIcon(QIcon(loadFile('ui/resources/Off.svg')))
        else:
            self.setIcon(QIcon(loadFile('ui/resources/Microphone_dark_ON.svg')))
            self.turn_micro.setIcon(QIcon(loadFile('ui/resources/On.svg')))

    def init_mode_switcher(self):
        '''
        According to ControlMicTray mode, configures menu entries and
        registering appropriate hotkey(s).
        '''
        if self.db.walkie_status:
            # Disabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(False)
            self.settings_win.hotkey_mic.setEnabled(False)
            # Enabling input field for hotkey of walkie-talkie mode.
            self.settings_win.hotkey_walkie.setEnabled(True)

            # Registering hotkeys for walkie-talkie app mode.
            self.hotkeys.register_walkie_mode_hotkey()
        else:
            # Enabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(True)
            self.settings_win.hotkey_mic.setEnabled(True)
            # Disabling input field for hotkey of walkie-talkie mode.
            self.settings_win.hotkey_walkie.setEnabled(False)

            # Registering hotkey for normal app mode.
            self.hotkeys.register_normal_mode_hotkey()

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
        # Normal mode enabling.
        if self.db.walkie_status:
            # Setting walkie-talkie status turned off in db. Also cheking for
            # appropriate changing icons in menu.
            self.db.walkie_status = 0
            self.change_icons_according_to_mic_status()

            # Enabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(True)
            self.settings_win.hotkey_mic.setEnabled(True)
            # Disabling input field for hotkey of walkie-talkie mode.
            self.settings_win.hotkey_walkie.setEnabled(False)

        # Talkie-Walkie Mode enabling.
        else:
            # First of all, forced muting mic in this mode.
            self.mic.mute_mic()

            # Setting walkie-talkie status turned on in db. Also cheking for
            # appropriate changing icons in menu.
            self.db.walkie_status = 1
            self.change_icons_according_to_mic_status()

            # Disabling menu entry "Turn Mic On\Off" and input field for hotkey
            # of normal mode.
            self.turn_micro.setEnabled(False)
            self.settings_win.hotkey_mic.setEnabled(False)
            # Enabling input field for hotkey of walkie-talkie mode.
            self.settings_win.hotkey_walkie.setEnabled(True)

        # Registeting hotkey(s) accordingly to ControlMicTray mode.
        self.hotkeys.switch_hotkey_mode()