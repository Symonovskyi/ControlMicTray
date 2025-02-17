# Built-in modules and own classes.
from sys import exit
from logic.controllers.databaseController import DatabaseController
from logic.windows.aboutWindow import AboutWindow
from logic.windows.settingsWindow import SettingsWindow
from logic.controllers.hotkeysController import HotkeysManager
from logic.controllers.microphoneController import (MicrophoneController,
    CustomMicrophoneEndpointVolumeCallback)
from ui.resources.icons import Icons

# 'pip install' modules.
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSlot


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


class MicrophonesMenu(CustomQMenu):
    '''
    '''

    def __init__(self, mic_controller_inst: MicrophoneController):
        super().__init__()
        self.menu = self
        self.mic_controller = mic_controller_inst
        self.all_mics = self.mic_controller.get_all_sys_microphones()

        self.setIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark')))
        self.setTitle('Микрофоны')

        self.init_mics_menu()

    def init_mics_menu(self):
        for mic_name, mic_dev in self.all_mics.items():
            self.addSeparator()
            mic_action = self.addAction(mic_name)
            mic_action.triggered.connect(self.change_default_mic)
            mic_action.setCheckable(True)
            mic_action.setChecked(self.mic_controller.is_mic_active(mic_dev._dev))

    def update_mics_menu(self):
        '''
        '''
        actions = self.actions()

        for k in self.all_mics.keys():
            if k not in [action.text() for action in actions]:
                self.init_mics_menu()

        for action in actions:
            if action.text() != '':
                mic_name = action.text()
                action.setChecked(self.mic_controller.is_mic_active(self.all_mics[mic_name]._dev))


    @pyqtSlot()
    def change_default_mic(self):
        '''
        '''
        mic_name = self.sender().text()
        self.mic_controller.set_microphone_by_default(mic_name)
        self.update_mics_menu()


class TrayIcon(QSystemTrayIcon):
    '''
    Implements main Qt System Tray Icon functionality.

    What happens at init stage (app startup):
        - If this is first app startup ever, creating database and tables,
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
        # Hotkeys Manager instance;
        # Microphones Menu instance.
        self.mic = MicrophoneController()
        self.db = DatabaseController()
        self.callback = CustomMicrophoneEndpointVolumeCallback(self)
        self.about_win = AboutWindow()
        self.hotkeys = HotkeysManager()
        self.mics_menu = MicrophonesMenu(self.mic)

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

        # Initializing 'Microphones' menu element.
        self.menu.addMenu(self.mics_menu)

        self.menu.addSeparator()

        # Initializing 'Settings' menu element.
        settings_action = self.menu.addAction('Настройки')
        settings_action.setIcon(QIcon(Icons.get_icon(Icons.settings_icon, theme='Dark')))

        self.menu.addSeparator()

        # Initializing and configuring 'About program' menu element.
        about_action = self.menu.addAction('О программе...')
        about_action.setIcon(QIcon(Icons.get_icon(Icons.about_icon, theme='Dark')))
        about_action.triggered.connect(self.about_win.show)

        self.menu.addSeparator()

        # Initializing and configuring 'Exit' menu element.
        exit_action = self.menu.addAction('Выход')
        exit_action.setIcon(QIcon(Icons.get_icon(Icons.exit_icon, theme='Dark')))
        exit_action.triggered.connect(exit)

        # Declaring Settings Window instance here for proerly
        # theme initializing. Also configuring 'Settings' menu element.
        self.settings_win = SettingsWindow(self, self.about_win, self.hotkeys, self.mics_menu)
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
            self.turn_micro.setIcon(QIcon(Icons.get_icon(Icons.switch_icon, theme='Dark', state=False)))
            self.push_to_talk.setIcon(QIcon(Icons.get_icon(Icons.switch_icon, theme='Dark', state=True)))
        else:
            self.push_to_talk.setIcon(QIcon(Icons.get_icon(Icons.switch_icon, theme='Dark', state=False)))

        if self.mic.get_mic_status:
            self.setIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark', state=False)))
            self.turn_micro.setIcon(QIcon(Icons.get_icon(Icons.switch_icon, theme='Dark', state=False)))
        else:
            self.setIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark', state=True)))
            self.turn_micro.setIcon(QIcon(Icons.get_icon(Icons.switch_icon, theme='Dark', state=True)))

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