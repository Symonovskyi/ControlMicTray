from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QRect

from core.widgets.ui.settings import Ui_SettingsWindow as SettingsUI
from core.widgets.hotkey import HotkeyButton
from core.styles import SettingsWindowStyles, BaseStyle
from core.events import EventBus


class SettingsWindow(QWidget):
    """
    Settings window for application configuration.
    
    Dependencies are injected via constructor:
    - db: DatabaseController for settings persistence
    - hotkeys_manager: HotkeysManager for hotkey registration
    - tray_instance: TrayIcon for UI updates
    - about_instance: AboutWindow for theme synchronization
    """

    def __init__(self, bus: EventBus, parent=None):
        super().__init__(parent)
        self._bus = bus

        # UI
        self.settings_UI = SettingsUI()
        self.settings_UI.setupUi(self)

        self.settings_styles = SettingsWindowStyles(self)

        # Dependencies
        self._bus = bus

        self.__setup_hotkey_widgets()
        self.__setup_connections()

    def __setup_connections(self):
        """Connect UI events directly to PyQt signals."""
        self._bus.storage.app_initial_state_loaded.connect(self.__init_set_display_data)
        self._bus.theme.app_theme_changed.connect(self._on_theme_changed)

        self._bus.shared.int_open_settings.connect(self.show)

        self.settings_UI.NightTheme.clicked.connect(self._on_theme_checkbox_changed)
        self.settings_UI.EnableProgram.clicked.connect(self._on_theme_checkbox_changed)
        self.settings_UI.PrivacyStatus.clicked.connect(self._on_privacy_status_changed)
        self.settings_UI.EnableMic.clicked.connect(self._on_startup_mute_checkbox_changed)
        self.settings_UI.UrlUpdates.clicked.connect(self._on_updates_url_click)

        # Обновление UI при "сдаче" оркестратора
        self._bus.shared.app_mode_updated.connect(self._on_mode_updated)
        self._bus.shared.app_hotkey_updated.connect(self._on_hotkey_updated)
        self._bus.shared.app_mic_state_updated.connect(self._on_mic_state_updated)
        self._bus.system.app_forced_mute_changed.connect(self._on_forced_mute_changed)

    def _on_mic_state_updated(self, is_muted: bool):
        """Обновить состояние микрофона в UI."""
        # TODO: обновить визуальное состояние когда будет реализовано
        ...

    def _on_mode_updated(self, is_walkie: bool):
        """Обновить UI при смене режима (в т.ч. при surrender)."""
        # TODO: обновить UI когда будет реализовано
        ...

    def _on_hotkey_updated(self, is_walkie: bool, hotkey: str):
        """Обновить текст кнопки хоткея при смене хоткея."""
        if is_walkie:
            self.btn_hotkey_walkie.set_hotkey(hotkey)
        else:
            self.btn_hotkey_mic.set_hotkey(hotkey)

    def _on_forced_mute_changed(self, state: bool):
        """Обновить галочку Force Mute при surrender."""
        # TODO: подключить когда UI элемент для Force Mute будет добавлен
        pass

    def __setup_hotkey_widgets(self):
        self.btn_hotkey_mic = HotkeyButton(
            mode_name="Mic",
            tooltip="Нажмите ЛКМ для записи. Нажмите Esc или Backspace для очистки.",
            parent=self
        )
        self.btn_hotkey_mic.setGeometry(QRect(175, 267, 240, 30))
        self.btn_hotkey_mic.hotkey_updated.connect(
            lambda hk: self._bus.shared.int_change_hotkey.emit(False, hk)
        )

        # Кнопка для режима рации (Walkie)
        self.btn_hotkey_walkie = HotkeyButton(
            mode_name="Walkie",
            tooltip="Внимание! Режим рации отключится при очистке хоткея.",
            parent=self
        )
        self.btn_hotkey_walkie.setGeometry(QRect(175, 307, 240, 30))
        self.btn_hotkey_walkie.hotkey_updated.connect(
            lambda hk: self._bus.shared.int_change_hotkey.emit(True, hk)
        )

    def __init_set_display_data(self, data: dict):
        # Disable unused features (temp)
        self.settings_UI.LanguageCode.setEnabled(False)
        self.settings_UI.AlertsType.setEnabled(False)

        # Theme
        theme_id = bool(data.get("theme_id", 1))
        self.settings_UI.NightTheme.setChecked(theme_id)
        self._bus.theme.int_change_theme.emit(theme_id) # apply theme on app init

        # Autorun
        autorun_enabled = bool(data.get("autorun", 1))
        self.settings_UI.EnableProgram.setChecked(autorun_enabled)
        self._bus.system.int_toggle_autorun.emit(autorun_enabled) # apply autorun on app init
        
        # Privacy
        self.settings_UI.PrivacyStatus.setChecked(bool(data.get("privacy_status", 1)))

        # Mute mic on startup
        self.settings_UI.EnableMic.setChecked(bool(data.get("mic_on_startup", 1)))
        # audio orchestrator then will set appropriate mic state on init

        # popukate hotkey buttons with data
        mic_hotkey = data.get("hotkey_mic", "unmapped")
        walkie_hotkey = data.get("hotkey_walkie", "unmapped")
        self.btn_hotkey_mic.setText(mic_hotkey)
        self.btn_hotkey_walkie.setText(walkie_hotkey)
        # audio orchestrator then will set appropriate app mode on init

    def _on_theme_changed(self, palette: BaseStyle):
        self.settings_styles.set_styles(palette)

    def _on_theme_checkbox_changed(self):
        checked = self.settings_UI.NightTheme.isChecked()
        self._bus.theme.int_change_theme.emit(int(checked))

    def _on_autorun_checkbox_changed(self):
        checked = self.settings_UI.EnableProgram.isChecked()
        self._bus.system.int_toggle_autorun.emit(checked)

    def _on_startup_mute_checkbox_changed(self):
        checked = self.settings_UI.EnableMic.isChecked()
        self._bus.system.int_toggle_mute_on_startup.emit(checked)

    def _on_updates_url_click(self):
        self._bus.system.open_url_intent.emit(
            "https://github.com/Symonovskyi/ControlMicTray/releases"
        )
    
    def _on_privacy_status_changed(self):
        checked = self.settings_UI.PrivacyStatus.isChecked()
        self._bus.system.int_toggle_privacy.emit(checked)
