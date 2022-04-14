# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui_py.AboutWindowUI import Ui_AboutWindow as AboutUI
from database.databaseController import DatabaseController

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


class AboutWindow(QWidget):
    def __init__(self):
        # For initializing Qt things.
        super().__init__()

        # UI.
        self.about_UI = AboutUI()
        self.about_UI.setupUi(self)

        # Database Controller class instance.
        self.db = DatabaseController()

        # Calling the initialization ui func.
        self.setup_ui()

    def setup_ui(self):
        self.setWindowIcon(QIcon('ui\\resources\\Microphone_dark.svg'))

        self.about_UI.ProgramVersion.setText(self.db.program_version)
        self.about_UI.WebSite.clicked.connect(self.open_site)
        self.about_UI.Email.clicked.connect(self.open_email)
        self.about_UI.UrlPrivacyPolicy.clicked.connect(self.open_privacy)

    def open_site(self):
        WindowsDefault().open_new_tab(self.db.web_site)

    def open_email(self):
        WindowsDefault().open_new_tab(f"mailto:{self.db.email}")

    def open_privacy(self):
        WindowsDefault().open_new_tab(self.db.url_privacy_policy)

    def closeEvent(self, event):
        self.destroy()
