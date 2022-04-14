class TrayIconStyles:
    def __init__(self, qinstance):
        self.tray = qinstance

    def dark_theme(self):
        self.tray.menu.setStyleSheet(
            """QMenu {
                color: #7D8A90;
                background-color: #1F2A30;
                border: 1px solid #444F55;
                border-radius: 3px;
                selection-background-color: #273238;
                selection-color: #BECBD1;
            }""")

    def white_theme(self):
        self.tray.menu.setStyleSheet(
            """QMenu { }""")


class SettingsWindowStyles:
    def __init__(self, qinstance):
        self.settings_win = qinstance.settings_UI

    def dark_theme(self):
        # self.settings_win.элемент_управления.setStyleSheet("""
        # background-color: white;
        # """)
        pass

    def white_theme(self):
        pass


class AboutWindowStyles:
    def __init__(self, qinstance):
        self.about_win = qinstance.about_UI

    def dark_theme(self):
        pass

    def white_theme(self):
        pass
