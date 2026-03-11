# Built-in modules and own classes.
import sys
from logic.trayIcon import TrayIcon
from ui.resources.icons import Icons

# "pip install" modules.
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtGui import QIcon
from traceback import print_exc

import faulthandler
faulthandler.enable()

def exception_hook(exctype, value, traceback):
    # Игнорируем прерывание с клавиатуры (Ctrl+C), чтобы можно было закрыть приложение в консоли
    if exctype is KeyboardInterrupt:
        sys.__excepthook__(exctype, value, traceback)
        return

    # Вывод ошибки в консоль/лог
    sys.__excepthook__(exctype, value, traceback)


if __name__ == '__main__':
    sys.excepthook = exception_hook
    # If any error will be occured, program will show dialog with error info and exit.
    try:
        # Creating Qt application instance.
        app = QApplication(sys.argv)
        # Disabling exiting main thread when closing any windows.
        app.setQuitOnLastWindowClosed(False)

        tray = TrayIcon()
        tray.show()
        sys.exit(app.exec())
    except Exception as e:
        print_exc()
        error_diag = QMessageBox()
        error_diag.setWindowIcon(QIcon(Icons.get_icon(Icons.microphone_icon, theme='Dark' if tray.db.night_theme else 'Light')))
        error_diag.setWindowTitle('ContolMicTray: Error!')
        error_diag.setText(f'Произошла ошибка при запуске приложения.\n'\
            'Проверьте подключённые микрофоны в Вашей системе и перезапустите приложение.\n\n'\
                f'Сообщение об ошибке:\n {e.__repr__()}')
        error_diag.show()
        if error_diag.finished:
            sys.exit(app.exec())

