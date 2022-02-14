# Built-in modules and own classes.
from ui.ui_py.AboutWindow_ui import Ui_AboutWindow as AboutUI
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

        web_site = f"""<a href='{self.db.web_site}'>
        <span style='color:white;'>controlmictray.pp.ua</span>"""
        self.about_UI.WebSite.setText(web_site)
        self.about_UI.WebSite.setOpenExternalLinks(True)

        email_link = f"<a href='{self.db.email}'>info@controlmictray.pp.ua</a>"
        self.about_UI.Email.setText(email_link)
        self.about_UI.Email.setOpenExternalLinks(True)

    def closeEvent(self, event):
        self.destroy()


class AboutWindowStyles(AboutUI):

    def dark_theme(self):
        pass

    def white_theme(self):
        pass
