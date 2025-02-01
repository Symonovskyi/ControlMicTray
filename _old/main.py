# Built-in modules and own classes.
from sys import argv, exit
from logic.trayIcon import TrayIcon
from absolutePath import loadFile
from ui.resources.icons import Icons

# "pip install" modules.
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon


if __name__ == '__main__':
    # Creating Qt application instance.
    app = QApplication(argv)
    # If any error will be occured, program will show dialog with error info and exit.
    try:
        tray = TrayIcon()
    except Exception as e:
        error_diag = QMessageBox()
        error_diag.setWindowIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark')))
        error_diag.setWindowTitle('ContolMicTray: Error!')
        error_diag.setText(f'Произошла ошибка при запуске приложения.\n'\
            'Проверьте подключённые микрофоны в Вашей системе и перезапустите приложение.\n\n'\
                f'Сообщение об ошибке:\n {e.__repr__()}')
        error_diag.show()
        if error_diag.finished:
            exit(app.exec())
    else:
        # Disabling exiting main thread when closing any windows.
        app.setQuitOnLastWindowClosed(False)
        tray.show()
        exit(app.exec())
