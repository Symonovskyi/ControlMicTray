# Built-in modules and own classes.
from os import remove
from keyboard import add_hotkey, remove_hotkey
from webbrowser import WindowsDefault
from ui.ui_py.SettingsWindowUI import Ui_SettingsWindow as SettingsUI
from ui.styles.styles import TrayIconStyles, SettingsWindowStyles, AboutWindowStyles
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget, QKeySequenceEdit
from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtCore import QRect


class HotkeyMicKeySequnceEdit(QKeySequenceEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(QRect(175, 267, 240, 21))
        self.setObjectName("HotkeyMic")

    def keyReleaseEvent(self, event):
        sequenceString = self.keySequence().toString()
        if sequenceString:
            last_key_stroke = sequenceString.split(',')[-1].strip()
            self.setKeySequence(QKeySequence(last_key_stroke))
        self.editingFinished.emit()
        self.clearFocus()


class HotkeyWalkieKeySequnceEdit(QKeySequenceEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(QRect(175, 307, 240, 21))
        self.setObjectName("HotkeyWalkie")

    def keyReleaseEvent(self, event):
        sequenceString = self.keySequence().toString()
        if sequenceString:
            last_key_stroke = sequenceString.split(',')[-1].strip()
            self.setKeySequence(QKeySequence(last_key_stroke))
        self.editingFinished.emit()
        self.clearFocus()


class SettingsWindow(QWidget):
    def __init__(self, tray_instance=None, about_instance=None):
        # For initializing Qt things.
        super().__init__()
        self.tray = tray_instance
        self.about = about_instance

        # UI.
        self.settings_UI = SettingsUI()
        self.settings_UI.setupUi(self)

        # Database Controller class instance.
        self.db = DatabaseController()

        self.HotkeyMic = HotkeyMicKeySequnceEdit(self)
        self.HotkeyWalkie = HotkeyWalkieKeySequnceEdit(self)

        # Creating theme instances.
        try:
            self.tray_styles = TrayIconStyles(self.tray)
            self.settings_styles = SettingsWindowStyles(self)
            self.about_styles = AboutWindowStyles(self.about)
        except: pass

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        self.settings_UI.setupUi(self)
        self.setWindowIcon(QIcon('ui\\resources\\Microphone_dark.svg'))

        # Going through varoius initial checks.
        self.init_check_language()
        self.init_check_notifications()
        self.init_check_theme()
        self.init_check_autorun()
        self.init_check_privacy()
        self.init_check_mute_mic_on_startup()
        self.init_set_hotkeys_in_keysequenceedits()

        # Connecting slots to signals.
        self.settings_UI.NightTheme.clicked.connect(self.change_theme)
        self.settings_UI.EnableProgram.clicked.connect(self.change_autorun)
        self.settings_UI.PrivacyStatus.clicked.connect(self.change_privacy)
        self.settings_UI.EnableMic.clicked.connect(
            self.change_mute_mic_on_startup)
        self.settings_UI.UrlUpdates.clicked.connect(self.check_updates_btn)
        self.HotkeyMic.editingFinished.connect(self.change_mic_hotkey)
        self.HotkeyWalkie.editingFinished.connect(self.change_walkie_hotkey)

    # Next methods for init checks and applying everything up.
    def init_check_language(self):
        pass

    def init_check_notifications(self):
        pass

    def init_check_theme(self):
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

    def init_check_autorun(self):
        if self.db.enable_program:
            self.settings_UI.EnableProgram.setChecked(True)
        else:
            self.settings_UI.EnableProgram.setChecked(False)

    def init_check_privacy(self):
        if self.db.privacy_status:
            self.settings_UI.PrivacyStatus.setChecked(True)
        else:
            self.settings_UI.PrivacyStatus.setChecked(False)

    def init_check_mute_mic_on_startup(self):
        if self.db.enable_mic:
            self.settings_UI.EnableMic.setChecked(True)
            self.tray.mic.mute_mic()
        else:
            self.settings_UI.EnableMic.setChecked(False)
            self.tray.mic.unmute_mic()

    def init_set_hotkeys_in_keysequenceedits(self):
        if self.db.hotkey_mic == 'Scroll_lock':
            hotkey_mic = 'ScrollLock'
            self.HotkeyMic.setKeySequence(hotkey_mic)
        else:
            self.HotkeyMic.setKeySequence(self.db.hotkey_mic)
        
        if self.db.hotkey_walkie == 'Scroll_lock':
            hotkey_walkie = 'ScrollLock'
            self.HotkeyWalkie.setKeySequence(hotkey_walkie)
        else:
            self.HotkeyWalkie.setKeySequence(self.db.hotkey_walkie)

    # Next mehods are for interactive interface changing.
    def change_theme(self):
        if self.settings_UI.NightTheme.isChecked():
            self.db.night_theme = 1
            self.init_check_theme()
        else:
            self.db.night_theme = 0
            self.init_check_theme()

    def change_autorun(self):
        if self.settings_UI.EnableProgram.isChecked():
            self.db.enable_program = 1
        else:
            self.db.enable_program = 0

    def change_privacy(self):
        if self.settings_UI.PrivacyStatus.isChecked():
            self.db.privacy_status = 1
        else:
            self.db.privacy_status = 0

    def change_mute_mic_on_startup(self):
        if self.settings_UI.EnableMic.isChecked():
            self.db.enable_mic = 1
        else:
            self.db.enable_mic = 0

    def check_updates_btn(self):
        WindowsDefault().open_new_tab(
            "https://github.com/Sif-on/ControlMicTray/releases")

    def change_mic_hotkey(self):
        changed_hotkey = self.HotkeyMic.keySequence().toString()
        if changed_hotkey == self.HotkeyWalkie.keySequence().toString():
            self.HotkeyMic.setKeySequence(self.db.hotkey_mic)
            return
        elif changed_hotkey == 'ScrollLock':
            changed_hotkey = 'Scroll_lock'

        remove_hotkey(self.db.hotkey_mic)
        self.db.hotkey_mic = changed_hotkey
        self.tray.check_push_to_talk()

    def change_walkie_hotkey(self):
        changed_hotkey = self.HotkeyWalkie.keySequence().toString()
        if changed_hotkey == self.HotkeyMic.keySequence().toString():
            self.HotkeyWalkie.setKeySequence(self.db.hotkey_walkie)
            return
        elif changed_hotkey == 'ScrollLock':
            changed_hotkey = 'Scroll_lock'

        remove_hotkey(self.db.hotkey_walkie)
        self.db.hotkey_walkie = changed_hotkey
        self.tray.check_push_to_talk()

    def closeEvent(self, event):
        self.destroy()
