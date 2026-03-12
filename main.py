# Built-in modules and own classes.
import sys
from logic.trayIcon import TrayIcon

# "pip install" modules.
from PyQt6.QtWidgets import QApplication, QMessageBox
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
        app.exec()
    except Exception as e:
        print_exc()
        error_diag = QMessageBox()
        error_diag.setIcon(QMessageBox.Icon.Critical)
        error_diag.setWindowTitle('ControlMicTray: Error!')
        error_diag.setText(
            'Произошла ошибка при запуске приложения.\n'
            'Проверьте доступность подключённых микрофонов к Вашей системе и перезапустите приложение.\n\n'
            f'Сообщение об ошибке:\n {e!r}'
        )
        error_diag.exec()
    finally:
        sys.exit(1)
