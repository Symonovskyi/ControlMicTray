from core.styles import DarkTheme, LightTheme, BaseStyle
from core.events import EventBus
from core.services.storage import StorageService


class ThemeService:
    """
    Сервис управления темой.

    Подписывается на события микрофона и режима, чтобы при смене темы
    или любом обновлении состояния — эмитить актуальную палитру
    для перерисовки UI (TrayIcon, SettingsWindow, AboutWindow).
    """

    def __init__(self, bus: EventBus, db: StorageService):
        self.__current_theme_obj = None
        self._bus = bus
        self._db = db

        self._available_themes = {
            0: LightTheme,
            1: DarkTheme
        }

        # connecting requests to slots
        self._bus.theme.int_change_theme.connect(self.change_theme_handler)

        # Подписка на события для актуализации палитры при перерисовке
        self._bus.shared.app_mic_state_updated.connect(self._on_mic_state_updated)
        self._bus.shared.app_mode_updated.connect(self._on_mode_updated)

        # Инициализация темы при загрузке начального состояния
        self._bus.storage.app_initial_state_loaded.connect(self._on_initial_state_loaded)

    @property
    def curr_palette(self) -> BaseStyle:
        return self.__current_theme_obj

    @property
    def palettes(self) -> list[BaseStyle | str]:
        return list(self._available_themes.values())

    # Slot
    def change_theme_handler(self, theme_id: int):
        self._db.theme = theme_id

        # Defining what theme to use using param, fallback to DarkTheme otherwise
        theme_class = self._available_themes.get(theme_id, DarkTheme)
        self.__current_theme_obj = theme_class()

        # Emitting theme_changed with appropriate theme obj for UI updates
        self._bus.theme.app_theme_changed.emit(self.__current_theme_obj)

    def _on_initial_state_loaded(self, data: dict):
        """Инициализация темы при загрузке начального состояния из БД."""
        theme_id = data.get("theme_id", 1)
        self._bus.theme.int_change_theme.emit(theme_id)

    def _on_mic_state_updated(self, muted: bool):
        self._bus.theme.tray_icon_change.emit(muted, bool(self._db.walkie_status))

    def _on_mode_updated(self, mode: bool):
        self._bus.theme.tray_icon_change.emit(self._db.mic_status, mode)
