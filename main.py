import sys
import faulthandler
import traceback

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QThread
# from PyQt6.QtCore import Qt

from core.widgets import TrayIcon, SettingsWindow, AboutWindow

from core.events import EventBus
from core.controllers.audio import AudioHotkeyOrchestrator

from core.services.audio import AudioInputService
from core.services.autorun import AutorunService
from core.services.hotkey import HotkeyService
from core.services.storage import StorageService
from core.services.system import SystemService
from core.services.theme import ThemeService


# Enable fault handler for debugging
faulthandler.enable()


def exception_hook(exctype, value, traceback):
    """Global exception handler."""
    # Ignore keyboard interrupt (Ctrl+C)
    if exctype is KeyboardInterrupt:
        # sys.__excepthook__(exctype, value, traceback)
        sys.exit(0)
        return

    # Log error
    sys.__excepthook__(exctype, value, traceback)


def main():
    """Application entry point."""
    sys.excepthook = exception_hook

    try:
        # os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=2"
        # Create Qt application
        app = QApplication(sys.argv)
        # app.setStyle("Light")
        app.setQuitOnLastWindowClosed(False)

        bus = EventBus()
        db = StorageService(bus)
        
        # Services
        audio_service = AudioInputService(bus)
        hotkey_service = HotkeyService(bus)

        autorun_service = AutorunService(bus, db)
        system_service = SystemService(bus, db)
        theme_service = ThemeService(bus, db)

        audio_thread = QThread()
        audio_service.moveToThread(audio_thread)
        
        audio_thread.started.connect(audio_service.initialize)
        app.aboutToQuit.connect(audio_service.cleanup)
        app.aboutToQuit.connect(hotkey_service.cleanup)
        app.aboutToQuit.connect(audio_thread.quit)
        audio_thread.finished.connect(audio_thread.deleteLater)
        audio_thread.start()

        orch = AudioHotkeyOrchestrator(bus, db)
        app.aboutToQuit.connect(orch.cleanup)

        about_widg = AboutWindow(bus)
        settings_widg = SettingsWindow(bus)
        tray_icon = TrayIcon(bus)

        bus.storage.int_load_initial_state.emit()
        tray_icon.show()

        # QApplication.styleHints().setColorScheme(Qt.ColorScheme.Dark)

        app.exec()

    except Exception as e:
        traceback.print_exc()

        error_diag = QMessageBox()
        error_diag.setIcon(QMessageBox.Icon.Critical)
        error_diag.setWindowTitle('ControlMicTray: Error!')
        error_diag.setText(
            'Произошла ошибка при запуске приложения.\n'
            'Проверьте доступность подключённых микрофонов к Вашей системе '
            'и перезапустите приложение.\n\n'
            f'Сообщение об ошибке:\n {e!r}'
        )
        error_diag.exec()
        sys.exit(1)


if __name__ == '__main__':
    main()
