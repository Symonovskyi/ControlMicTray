# Built-in modules and own classes.
from sys import argv, exit
from ui.trayIcon import TrayIcon
from logic.absolutePath import loadFile

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
        error_diag.setWindowIcon(QIcon('ui/resources/Microphone_light.svg'))
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
