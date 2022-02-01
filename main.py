# Built-in modules and own classes.
from sys import argv, exit
from trayIconAndWindows import TrayIcon

# "pip install" modules.
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(argv)
    win = TrayIcon()
    win.show()
    exit(app.exec())
