import logging
from PyQt6.QtCore import QObject, QTimer

from core.events import EventBus
from core.services.storage import StorageService
from core.domain.policy import MutePolicy, AudioContextSnapshot
from core.domain.states import BaseAudioState, ToggleModeState, WalkieModeState


class AudioServiceCommandError(Exception):
    """Кастомное исключение при техническом сбое в AudioInputService."""
    pass


class AudioHotkeyOrchestrator(QObject):
    MAX_FORCE_MUTE_ATTEMPTS = 20

    def __init__(self, bus: EventBus, db: StorageService):
        super().__init__()
        self._bus = bus
        self._db = db

        # --- ЧТЕНИЕ БАЗОВЫХ НАСТРОЕК ---
        self._is_walkie_mode = bool(self._db.walkie_status)
        self._force_mute_enabled = bool(self._db.forced_mute)
        
        # --- СТАРТОВАЯ ПОЛИТИКА (MutePolicy) ---
        self.expected_is_muted = MutePolicy.resolve_startup_state(
            is_walkie=self._is_walkie_mode,
            mute_on_startup=bool(self._db.enable_mic),
            last_db_status=bool(self._db.mic_status)
        )

        # --- ИНИЦИАЛИЗАЦИЯ СОСТОЯНИЯ (State Pattern) ---
        self._current_state: BaseAudioState = None
        self._apply_mode_state(self._is_walkie_mode)

        # --- ЗАЩИТА ОТ ВОЙНЫ ДРАЙВЕРОВ (Anti-Hot-Loop) ---
        self._force_mute_attempts = 0
        self._debounce_timer = QTimer(self)
        self._debounce_timer.setInterval(2000)
        self._debounce_timer.setSingleShot(True)
        self._debounce_timer.timeout.connect(self.__reset_debouncer)

        self.__connect_signals()
        
        # Запуск первоначального состояния железа
        self.send_mic_command()
        self.__init_set_hotkeys()

    def __connect_signals(self):
        # 1. INTENTS (От пользователя)
        self._bus.shared.int_toggle_mic.connect(self._on_toggle_mic)
        self._bus.shared.int_walkie_press.connect(self._on_walkie_press)
        self._bus.shared.int_walkie_release.connect(self._on_walkie_release)
        self._bus.shared.int_change_mode.connect(self._on_change_mode)
        self._bus.shared.int_change_hotkey.connect(self._on_change_hotkey)
        self._bus.shared.int_change_default_mic.connect(self._on_change_default_mic)
        
        # Настройки пользователя
        self._bus.system.int_toggle_force_mute.connect(self._on_toggle_force_mute)
        self._bus.system.int_toggle_mute_on_startup.connect(self._on_toggle_mute_on_startup)

        # 2. ANSWERS (Ответы на системные вызовы)
        self._bus.shared.answ_set_mic_mute.connect(self._on_answ_set_mic_mute)
        self._bus.shared.answ_set_default_mic.connect(self._on_answ_set_default_mic)
        self._bus.shared.answ_bind_hotkeys.connect(self._on_answ_bind_hotkeys)

        # 3. OS EVENTS (Сырые данные от Windows)
        self._bus.shared.os_mic_state_changed.connect(self._enforce_mute_rules)
        self._bus.shared.os_devices_list_changed.connect(self._on_os_devices_list_changed)
        self._bus.shared.os_default_mic_changed.connect(self._on_os_default_mic_changed)

    # =========================================================
    # ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ОРКЕСТРАТОРА
    # =========================================================

    def _apply_mode_state(self, is_walkie: bool):
        """Смена паттерна State"""
        self._is_walkie_mode = is_walkie
        if is_walkie:
            self._current_state = WalkieModeState(self)
        else:
            self._current_state = ToggleModeState(self)
        self._current_state.on_enter()

    def send_mic_command(self):
        """Сохраняет состояние и отдает приказ железу"""
        self._db.mic_status = int(self.expected_is_muted)
        self._bus.shared.cmd_set_mic_mute.emit(self.expected_is_muted)

    def __reset_debouncer(self):
        if self._force_mute_attempts > 0:
            self._force_mute_attempts = 0
            logging.debug("Hot-loop counter reset (Peace restored).")

    def __init_set_hotkeys(self):
        hk = self._db.hotkey_walkie if self._is_walkie_mode else self._db.hotkey_mic
        self._bus.shared.int_change_hotkey.emit(self._is_walkie_mode, hk)

    # =========================================================
    # ОБРАБОТЧИКИ НАМЕРЕНИЙ (Делегируем в State)
    # =========================================================

    def _on_toggle_mic(self):
        self._current_state.handle_toggle()

    def _on_walkie_press(self):
        self._current_state.handle_walkie_press()

    def _on_walkie_release(self):
        self._current_state.handle_walkie_release()

    # =========================================================
    # УПРАВЛЕНИЕ НАСТРОЙКАМИ И РЕЖИМАМИ
    # =========================================================

    def _on_change_mode(self, mode: bool):
        self._db.walkie_status = int(mode)
        self._apply_mode_state(mode)
        # Передаем команду на перебинд хоткеев
        self.__init_set_hotkeys()
        self._bus.shared.app_mode_updated.emit(mode)

    def _on_change_hotkey(self, mode: bool, hotkey: str):
        hk = 'unmapped' if not hotkey else hotkey
        
        # Сохраняем в БД для нужного режима
        if mode:
            self._db.hotkey_walkie = hk
        else:
            self._db.hotkey_mic = hk

        self._bus.shared.cmd_bind_hotkeys.emit(mode, hk)
        self._bus.shared.app_hotkey_updated.emit(mode, hk)

    def _on_toggle_force_mute(self, state: bool):
        self._force_mute_enabled = state
        self._db.forced_mute = int(state)
        self._bus.system.app_forced_mute_changed.emit(state)

    def _on_toggle_mute_on_startup(self, state: bool):
        self._db.enable_mic = int(state)
        self._bus.system.app_mute_on_startup_changed.emit(state)

    def _on_change_default_mic(self, device_id: str):
        self._bus.shared.cmd_set_default_mic.emit(device_id)

    # =========================================================
    # ЗАЩИТА ОС (Используем Policy)
    # =========================================================

    def _enforce_mute_rules(self, os_is_muted: bool):
        """Обработка события ОС с использованием Политики."""
        
        # 1. Собираем слепок данных для Политики
        ctx_snapshot = AudioContextSnapshot(
            is_walkie_mode=self._is_walkie_mode,
            is_force_mute_enabled=self._force_mute_enabled,
            expected_is_muted=self.expected_is_muted,
            os_is_muted=os_is_muted
        )

        # 2. Спрашиваем Политику: Нужно ли нам сопротивляться ОС?
        if MutePolicy.should_enforce_mute(ctx_snapshot):
            self._force_mute_attempts += 1
            self._debounce_timer.start() # Перезапуск таймера

            logging.warning(f"OS state violated app rules! Enforcing Force Mute (attempt {self._force_mute_attempts}/{self.MAX_FORCE_MUTE_ATTEMPTS}).")

            if self._force_mute_attempts >= self.MAX_FORCE_MUTE_ATTEMPTS:
                logging.error("Anti-Hot-Loop triggered! Surrendering to OS state.")
                self._surrender_to_os(os_is_muted)
                return

            self.send_mic_command()
        else:
            # 3. Политика разрешила ОС изменить звук
            self.expected_is_muted = os_is_muted
            self._bus.shared.app_mic_state_updated.emit(self.expected_is_muted)

    def _surrender_to_os(self, os_is_muted: bool):
        """Сдача позиций при войне драйверов."""
        self._force_mute_attempts = 0
        self.expected_is_muted = os_is_muted

        if self._is_walkie_mode:
            logging.warning("Surrender: disabling Walkie-talkie mode.")
            self._db.walkie_status = 0
            self._apply_mode_state(False) # Переходим в Toggle Mode
            
            self._bus.shared.app_mode_updated.emit(False)
            self.__init_set_hotkeys()
            
        elif self._force_mute_enabled:
            logging.warning("Surrender: disabling Force Mute.")
            self._force_mute_enabled = False
            self._db.forced_mute = 0
            self._bus.system.app_forced_mute_changed.emit(False)

        self._bus.shared.app_mic_state_updated.emit(self.expected_is_muted)

    # =========================================================
    # ОБРАБОТКА ИЗМЕНЕНИЙ В СИСТЕМЕ АУДИО
    # =========================================================

    def _on_os_default_mic_changed(self, device_id: str):
        logging.info(f"OS default mic changed to {device_id}.")
        # UI узнает о новом микрофоне
        self._bus.shared.app_default_mic_updated.emit(device_id)

    def _on_os_devices_list_changed(self, devices: dict[str, str]):
        self._bus.shared.app_devices_list_updated.emit(devices)

    def _on_answ_set_mic_mute(self, muted: bool):
        if muted is None:
            raise AudioServiceCommandError("AudioInputService failed to execute SetMute.")

    def _on_answ_set_default_mic(self, device_id: str):
        if device_id is None:
            raise AudioServiceCommandError("AudioInputService failed to execute SetDefaultDevice.")

    def _on_answ_bind_hotkeys(self, mode: bool, hotkey: str):
        if not hotkey:
            logging.error(f"Failed to bind hotkey for mode: {'Walkie' if mode else 'Toggle'}")

    def cleanup(self):
        self._debounce_timer.stop()