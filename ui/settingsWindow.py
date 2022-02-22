# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui_py.SettingsWindowUI import Ui_SettingsWindow as SettingsUI
from ui.styles.styles import TrayIconStyles, SettingsWindowStyles, AboutWindowStyles
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


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

        self.settings_UI.HotkeyMic.setReadOnly(False)
        self.settings_UI.HotkeyMic.setPlaceholderText(
            'e.g. "Ctrl+Shift+/"')

        self.settings_UI.HotkeyWalkie.setReadOnly(False)
        self.settings_UI.HotkeyWalkie.setPlaceholderText(
            'e.g. "Scroll_lock"')

        # Going through varoius initial checks.
        self.init_check_language()
        self.init_check_notifications()
        self.init_check_theme()
        self.init_check_autorun()
        self.init_check_privacy()
        self.init_check_mute_mic_on_startup()
        self.settings_UI.HotkeyMic.setText(self.db.hotkey_mic)
        self.settings_UI.HotkeyWalkie.setText(self.db.hotkey_walkie)

        # Connecting slots to signals.
        self.settings_UI.NightTheme.clicked.connect(self.change_theme)
        self.settings_UI.EnableProgram.clicked.connect(self.change_autorun)
        self.settings_UI.PrivacyStatus.clicked.connect(self.change_privacy)
        self.settings_UI.EnableMic.clicked.connect(
            self.change_mute_mic_on_startup)
        self.settings_UI.UrlUpdates.clicked.connect(self.check_updates_btn)

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

    def closeEvent(self, event):
        self.destroy()
