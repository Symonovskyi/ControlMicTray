# Built-in modules and own classes.
from webbrowser import WindowsDefault
from ui.ui.AboutWindowUI import Ui_AboutWindow as AboutUI
from database.databaseController import DatabaseController
from absolutePath import loadFile

# 'pip install' modules.
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon


class AboutWindow(QWidget):
    '''
    Implements "About" window of app, which contains info about program itself.

    Attributes:
        - about_UI (AboutUI): "about" window styles class instance.
        - db (DatabaseController): database controller class instance.
    '''
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
        '''
        Sets icon and title of window. Also connects signals to slots.
        '''
        self.setWindowIcon(QIcon(loadFile('ui/resources/Microphone_dark.svg')))

        self.about_UI.ProgramVersion.setText(self.db.program_version)
        self.about_UI.WebSite.clicked.connect(self.open_site)
        self.about_UI.Email.clicked.connect(self.open_email)
        self.about_UI.UrlPrivacyPolicy.clicked.connect(self.open_privacy)

    def open_site(self):
        '''
        Opens releases on github in new tab using default system browser.
        '''
        print(self.db.web_site)
        WindowsDefault().open_new_tab(self.db.web_site)

    def open_email(self):
        '''
        Opens email tab using default system browser.
        '''
        WindowsDefault().open_new_tab(f"mailto:{self.db.email}")

    def open_privacy(self):
        '''
        Opens licence of this app in new tab using default system browser.
        '''
        WindowsDefault().open_new_tab(self.db.url_privacy_policy)
