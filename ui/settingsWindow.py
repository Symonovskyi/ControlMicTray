# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui_py.SettingsWindow_ui import Ui_SettingsWindow as SettingsUI
from ui.styles import TrayIconStyles, SettingsWindowStyles, AboutWindowStyles
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

        # Setting actual theme of app.
        self.apply_theme(mode='init')

        self.settings_UI.NightTheme.clicked.connect(self.apply_theme)
        self.settings_UI.UrlUpdates.clicked.connect(self.check_updates_btn)

    def apply_theme(self, mode=None):
        if mode == 'init':
            if self.db.night_theme:
                self.settings_UI.NightTheme.setChecked(True)
                self.tray_styles.night_theme()
                self.settings_styles.night_theme()
                self.about_styles.night_theme()
            else:
                self.settings_UI.NightTheme.setChecked(False)
                self.tray_styles.white_theme()
                self.settings_styles.white_theme()
                self.about_styles.white_theme()
        else:
            if self.settings_UI.NightTheme.isChecked():
                self.db.night_theme = 1
                self.apply_theme(mode='init')
            else:
                self.db.night_theme = 0
                self.apply_theme(mode='init')

    def check_updates_btn(self):
        WindowsDefault().open_new_tab(
            "https://github.com/Sif-on/ControlMicTray/releases")

    def closeEvent(self, event):
        self.destroy()
