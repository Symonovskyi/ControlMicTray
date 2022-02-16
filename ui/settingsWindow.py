# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui_py.SettingsWindow_ui import Ui_SettingsWindow as SettingsUI
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


class SettingsWindow(QWidget):
    def __init__(self):
        # For initializing Qt things.
        super().__init__()

        # UI.
        self.settings_UI = SettingsUI()
        self.settings_UI.setupUi(self)

        # Database Controller class instance.
        self.db = DatabaseController()

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        self.settings_UI.setupUi(self)
        self.setWindowIcon(QIcon('ui\\resources\\Microphone_dark.svg'))

        self.settings_UI.NightTheme.clicked.connect(self.apply_theme)
        self.settings_UI.UrlUpdates.clicked.connect(self.check_updates_btn)

    def apply_theme(self):
        if self.settings_UI.NightTheme.isChecked():
            self.db.night_theme = 1
        else:
            self.db.night_theme = 0

    def check_updates_btn(self):
        WindowsDefault().open_new_tab(
            "https://github.com/Sif-on/ControlMicTray/releases")

    def closeEvent(self, event):
        self.destroy()

    def night_theme(self):
        pass

    def white_theme(self):
        pass
