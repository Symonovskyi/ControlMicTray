# Built-in modules and own classes.
from sys import argv, exit
from logic.windows.trayIcon import TrayIcon
from ui.resources.icons import Icons
from traceback import extract_tb

# "pip install" modules.
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon


def error_diag(app: QApplication, exc: str):
    error_diag = QMessageBox()
    error_diag.setWindowIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark')))
    error_diag.setWindowTitle('ContolMicTray: Error!')
    error_diag.setText(f'Произошла ошибка при запуске приложения.\n'\
        'Проверьте подключённые микрофоны в Вашей системе и перезапустите приложение.\n\n'\
            f'Сообщение об ошибке:\n {exc}')
    error_diag.show()

    if error_diag.finished:
        print(extract_tb(exc.__traceback__))
        exit(app.exec())


if __name__ == '__main__':
    # If any error will be occured, program will show dialog with error info and exit.
    try:
        # Creating Qt application instance.
        app = QApplication(argv)
        tray = TrayIcon()
    except Exception as e:
        error_diag(app, e)
    else:
        # Disabling exiting main thread when closing any windows.
        app.setQuitOnLastWindowClosed(False)
        tray.show()
        exit(app.exec())
