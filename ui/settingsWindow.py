# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui_py.SettingsWindowUI import Ui_SettingsWindow as SettingsUI
from ui.styles.styles import TrayIconStyles, SettingsWindowStyles, AboutWindowStyles
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget, QKeySequenceEdit
from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtCore import QRect


class HotkeyMicKeySequenceEdit(QKeySequenceEdit):
    '''
    Implements all general functionality of Qt Sequence Edit field.

    Reimplements method keyReleaseEvent(), changing logic of setting hotkey
    shortcut to Qt Sequence Edit field. This class used for normal
    app mode only.
    '''
    def __init__(self, parent=None):
        '''
        Main initialization method. Sets custom location of Sequence Edit field.

        Args:
            parent (None | QObject): sets the widget parent for
            Sequence Edit field.
        '''
        super().__init__(parent)

        self.setGeometry(QRect(175, 267, 240, 21))
        self.setObjectName("HotkeyMic")

    def keyReleaseEvent(self, e):
        '''
        Reimplemented method. Changes shortcut string view to human-readable.

        Args:
            - e (PyQt6.QtGui.QKeyEvent): Qt key event.
        '''
        sequenceString = self.keySequence().toString()
        if sequenceString:
            last_key_stroke = sequenceString.split(',')[-1].strip()
            self.setKeySequence(QKeySequence(last_key_stroke))
        self.editingFinished.emit()
        self.clearFocus()


class HotkeyWalkieKeySeqeunceEdit(QKeySequenceEdit):
    '''
    Implements all general functionality of Qt Sequence Edit field.

    Reimplements method keyReleaseEvent(), changing logic of setting hotkey
    shortcut to Qt Sequence Edit field. This class used for walkie-talkie
    app mode only.
    '''
    def __init__(self, parent=None):
        '''
        Main initialization method. Sets custom location of Sequence Edit field.

        Args:
            parent (None | QObject): sets the widget parent for
            Sequence Edit field.
        '''
        super().__init__(parent)

        self.setGeometry(QRect(175, 307, 240, 21))
        self.setObjectName("HotkeyWalkie")

    def keyReleaseEvent(self, e):
        '''
        Reimplemented method. Changes shortcut string view to human-readable.

        Args:
            - e (PyQt6.QtGui.QKeyEvent): Qt key event.
        '''
        sequenceString = self.keySequence().toString()
        if sequenceString:
            last_key_stroke = sequenceString.split(',')[-1].strip()
            self.setKeySequence(QKeySequence(last_key_stroke))
        self.editingFinished.emit()
        self.clearFocus()


class SettingsWindow(QWidget):
    # TODO: replace themes initializing into another module "appearanceManager".
    '''
    Implements "settings" window of app.
    Sets actual theme of app and checkboxes of window on app startup.

    Parameters:
        - tray_instance (QSystemTrayIcon): TrayIcon class instance.
        - about_instance (QWidget): AboutWindow class instance.
        - hotkeys_manager (QObject): HotkeysManager class instance.

    Attributes:
        - tray (QSystemTrayIcon): TrayIcon class instance.
        - about (QWidget): AboutWindow class instance.
        - hotkeys (QObject): HotkeysManager class instance.
        - settings_UI (QObject): "settings" window styles instance.
        - db (DatabaseController): database controller class instance.
        - hotkey_mic (QKeySequenceEdit): custom Qt Sequence Edit field for
        normal app mode only.
        - hotkey_walkie (QKeySequenceEdit): custom Qt Sequence Edit field for
        walkie-talkie app mode only.
        - tray_styles (TrayIconStyles): custom themes styles for Tray Menu
        instance.
        - settings_styles (SettingsStyles): custom themes styles for settings
        window instance.
        - about_styles (AboutStyles): custom themes styles for about window
        instance.

    '''
    def __init__(self, tray_instance, about_instance, hotkeys_manager):
        # For initializing Qt functionality.
        super().__init__()

        # A bunch of instances for properly themes working.
        self.tray = tray_instance
        self.about = about_instance
        self.hotkeys = hotkeys_manager

        # UI.
        self.settings_UI = SettingsUI()
        self.settings_UI.setupUi(self)

        # Database Controller class instance.
        self.db = DatabaseController()

        # Custom Key Sequence Edits.
        self.hotkey_mic = HotkeyMicKeySequenceEdit(self)
        self.hotkey_walkie = HotkeyWalkieKeySeqeunceEdit(self)

        # Creating theme instances.
        self.tray_styles = TrayIconStyles(self.tray)
        self.settings_styles = SettingsWindowStyles(self)
        self.about_styles = AboutWindowStyles(self.about)

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        '''
        Sets icons, checkboxes in their state according with values in db and
        connects various signals to their appropriate slots.
        '''
        self.settings_UI.setupUi(self)
        self.setWindowIcon(QIcon('ui\\resources\\Microphone_dark.svg'))

        # Going through varoius initial checks.
        self.init_check_everything()

        # Connecting slots to signals.
        self.settings_UI.NightTheme.clicked.connect(self.change_theme)
        self.settings_UI.EnableProgram.clicked.connect(self.change_autorun)
        self.settings_UI.PrivacyStatus.clicked.connect(self.change_privacy)
        self.settings_UI.EnableMic.clicked.connect(
            self.change_mute_mic_on_startup)
        self.settings_UI.UrlUpdates.clicked.connect(self.check_updates_btn)
        self.hotkey_mic.editingFinished.connect(self.change_mic_hotkey)
        self.hotkey_walkie.editingFinished.connect(self.change_walkie_hotkey)

    def init_check_everything(self):
        '''
        Does check for language and notification field and every checkbox
        settings. Also checks muting state on startup if needed.
        '''
        # TODO: Cheking language setting.
        # TODO: Checking notifications setting.

        # Theme setting.
        if self.db.night_theme:
            self.settings_UI.NightTheme.setChecked(True)
            self.tray_styles.dark_theme()
            self.settings_styles.dark_theme()
            self.about_styles.dark_theme()
        else:
            self.settings_UI.NightTheme.setChecked(False)
            self.tray_styles.white_theme()
            self.settings_styles.white_theme()
            self.about_styles.white_theme()

        # Setting autorun checkbox.
        self.settings_UI.EnableProgram.setChecked(bool(self.db.enable_program))

        # Setting privacy agreement checkbox.
        self.settings_UI.PrivacyStatus.setChecked(bool(self.db.privacy_status))

        # Checking mute state of mic on startup.
        self.settings_UI.EnableMic.setChecked(bool(not self.db.enable_mic))
        if self.settings_UI.EnableMic.isChecked(): self.tray.mic.mute_mic()

        # Setting hotkey shortcuts in key sequence edits.
        self.init_set_hotkeys_in_keysequenceedits()

    def init_set_hotkeys_in_keysequenceedits(self):
        '''
        Sets shortcuts of hotkeys in appropriate way.
        Also, sets value "Scroll_lock" for "ScrollLock" button because of it's
        unsupported case.
        '''
        if self.db.hotkey_mic == 'Scroll_lock':
            hotkey_mic = 'ScrollLock'
            self.hotkey_mic.setKeySequence(hotkey_mic)
        else:
            self.hotkey_mic.setKeySequence(self.db.hotkey_mic)
        
        if self.db.hotkey_walkie == 'Scroll_lock':
            hotkey_walkie = 'ScrollLock'
            self.hotkey_walkie.setKeySequence(hotkey_walkie)
        else:
            self.hotkey_walkie.setKeySequence(self.db.hotkey_walkie)

    # Next mehods are for interactive interface changing.
    def change_theme(self):
        '''
        Chages theme value in db and applies appropriate theme dynamically.
        '''
        self.db.night_theme = int(self.settings_UI.NightTheme.isChecked())
        self.init_check_everything()

    def change_autorun(self):
        '''
        Changes value of autorun setting in database according to
        'Autorun Program' checkbox status.
        '''
        self.db.enable_program = int(self.settings_UI.EnableProgram.isChecked())

    def change_privacy(self):
        '''
        Changes value of privacy agreement setting in database according to
        'Privacy Agreement' checkbox status.
        '''
        self.db.privacy_status = int(self.settings_UI.PrivacyStatus.isChecked())

    def change_mute_mic_on_startup(self):
        '''
        Changes value of mic muting on starup setting in database according to
        'Mute Mic on Startup' checkbox status.
        '''
        self.db.enable_mic = not self.settings_UI.EnableMic.isChecked()

    def check_updates_btn(self):
        '''
        Opens new tab with program releases on github with default system browser.
        '''
        WindowsDefault().open_new_tab(
            "https://github.com/Sif-on/ControlMicTray/releases")

    def change_mic_hotkey(self):
        '''
        Writes shortcuts of normal mode hotkey to database in appropriate way.
        Also, sets value "Scroll_lock" for "ScrollLock" button because of it's
        unsupported case.
        '''
        changed_hotkey = self.hotkey_mic.keySequence().toString()
        if changed_hotkey == self.hotkey_walkie.keySequence().toString():
            self.hotkey_mic.setKeySequence(self.db.hotkey_mic)
            return
        elif changed_hotkey == 'ScrollLock':
            changed_hotkey = 'Scroll_lock'

        self.db.hotkey_mic = changed_hotkey
        self.hotkeys.re_register_normal_mode_hotkey()

    def change_walkie_hotkey(self):
        '''
        Writes shortcuts of walkie-talkie mode hotkey to database in
        appropriate way.
        Also, sets value "Scroll_lock" for "ScrollLock" button because of it's
        unsupported case.
        '''
        changed_hotkey = self.hotkey_walkie.keySequence().toString()
        if changed_hotkey == self.hotkey_mic.keySequence().toString():
            self.hotkey_walkie.setKeySequence(self.db.hotkey_walkie)
            return
        elif changed_hotkey == 'ScrollLock':
            changed_hotkey = 'Scroll_lock'

        self.db.hotkey_walkie = changed_hotkey
        self.hotkeys.re_register_walkie_mode_hotkey()
