import logging
from PyQt6.QtCore import QObject, QTimer

from core.events import EventBus
from core.services.storage import StorageService


class AudioServiceCommandError(Exception):
    """Custom exception for handling errors from AudioInputService."""
    pass


class AudioHotkeyOrchestrator(QObject):
    """
    Центральный оркестратор управления микрофоном.

    Четыре "рычага влияния" на состояние микрофона (приоритет сверху вниз):
    1. Walkie-status — в Walkie-mode микрофон ВСЕГДА заглушен (implied force mute).
       При "гонке состояний" (20 попыток) — режим сдаётся и выключается.
    2. Enable-mic (галочка "Выкл. микро при запуске") — микрофон выключается
       при запуске приложения, игнорируя last state.
    3. Mic-status (последнее состояние при закрытии) — восстанавливается
       если не активны пункты 1 и 2.
    4. Force Mute — активен ТОЛЬКО в Toggle-mode. При 20 попытках — выключается.
    """

    MAX_FORCE_MUTE_ATTEMPTS = 20  # порог "гонки состояний"

    def __init__(self, bus: EventBus, db: StorageService):
        super().__init__()
        self._bus = bus
        self._db = db

        # reading init settings from db
        self._walkie_mode = bool(self._db.walkie_status)
        self._force_mute_enabled = bool(self._db.forced_mute)
        # self._force_mute_enabled = False
        self._enable_mic = bool(self._db.enable_mic)          # галочка "Выкл. микро при запуске"
        self._mic_status = bool(self._db.mic_status)          # последнее состояние микрофона при закрытии

        # status of pressed btn in walkie mode
        self._walkie_pressed = False

        if self._walkie_mode:
            # В walkie-режиме микрофон всегда заглушен по умолчанию
            self._expected_is_muted = True
        elif self._enable_mic:
            # Если стоит галочка "Выключать микрофон при запуске" — заглушаем
            self._expected_is_muted = True
        else:
            # Иначе восстанавливаем последнее состояние микрофона при закрытии
            self._expected_is_muted = self._mic_status

        # hot loop control with debouncer
        self._force_mute_attempts = 0
        self.debounce_timer = QTimer(self)
        self.debounce_timer.setInterval(2000)
        self.debounce_timer.setSingleShot(True)
        self.debounce_timer.timeout.connect(self.__reset_debouncer)
        self.debounce_timer.thread().finished.connect(
            self.debounce_timer.thread().deleteLater
        )
        self.debounce_timer.start()

        self.__connect_signals()

        # settings mic state on app init
        self.__init_set_mic_state()
        self.__init_set_hotkkeys()

    def __connect_signals(self):
        # 1. INTENTS
        self._bus.shared.int_toggle_mic.connect(self._on_toggle_mic)
        self._bus.shared.int_walkie_press.connect(self._on_walkie_press)
        self._bus.shared.int_walkie_release.connect(self._on_walkie_release)
        self._bus.shared.int_change_mode.connect(self._on_change_mode)
        self._bus.shared.int_change_hotkey.connect(self._on_change_hotkey)
        self._bus.shared.int_change_default_mic.connect(self._on_change_default_mic)
        
        # settings signals
        self._bus.system.int_toggle_force_mute.connect(self._on_toggle_force_mute)
        self._bus.system.int_toggle_mute_on_startup.connect(self._on_toggle_mute_on_startup)

        # 2. SERVICE ANSWERS
        self._bus.shared.answ_set_mic_mute.connect(self._on_answ_set_mic_mute)
        self._bus.shared.answ_set_default_mic.connect(self._on_answ_set_default_mic)
        self._bus.shared.answ_bind_hotkeys.connect(self._on_answ_bind_hotkeys)

        # 3. OS EVENTS
        self._bus.shared.os_mic_state_changed.connect(self._enforce_mute_rules)
        self._bus.shared.os_devices_list_changed.connect(self._on_os_devices_list_changed)
        self._bus.shared.os_default_mic_changed.connect(self._on_os_default_mic_changed)

    def __init_set_mic_state(self):
        """
        Установка начального состояния микрофона при запуске.

        Приоритет (4 рычага):
        1. Walkie-status → микрофон всегда заглушен
        2. Enable-mic (галочка "Выкл. микро при запуске") → микрофон выключается
        3. Mic-status (последнее состояние при закрытии) → восстанавливается
        """
        if self._walkie_mode:
            return  # В walkie-режиме микрофон заглушается через _enforce_mute_rules

        # В toggle-режиме: применяем настройку
        self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)

    def __init_set_hotkkeys(self):
        if self._db.walkie_status:
            hk = self._db.hotkey_walkie
        else:
            hk = self._db.hotkey_mic

        self._bus.shared.int_change_hotkey.emit(self._db.walkie_status, hk)

    def __reset_debouncer(self):
        if self._force_mute_attempts > 0:
            self._force_mute_attempts = 0
            logging.debug("Hot-loop counter reset.")

    # --- intent handlers ---

    def _on_toggle_mic(self, muted: bool):
        if self._walkie_mode:
            return # ignore in toggle mode
        self._expected_is_muted = muted
        self._db.mic_status = self._expected_is_muted
        self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)

    def _on_walkie_press(self):
        if not self._walkie_mode:
            return # ignore in toggle mode
        self._walkie_pressed = True
        self._expected_is_muted = False
        self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)

    def _on_walkie_release(self):
        if not self._walkie_mode:
            return # ignore in toggle mode
        self._walkie_pressed = False
        self._expected_is_muted = True
        self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)

    def _on_change_hotkey(self, mode: bool, hotkey: str):
        print("_on_change_hotkey")
        print(f"Mode: {mode}")
        print(f"Hotkey: {hotkey}")
        print(type(hotkey))

        self._walkie_mode = mode
        hk = None

        if hotkey == '':
            if self._walkie_mode:
                hk = self._db.hotkey_walkie
            elif not self._walkie_mode:
                hk = self._db.hotkey_mic
        elif hotkey:
            hk = hotkey

        # sending command for HotkeyService to rebind hotkeys
        self._bus.shared.cmd_bind_hotkeys.emit(mode, hk)
        
        if mode:
            self._expected_is_muted = True

        self._db.mic_status = self._expected_is_muted
        self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)

        if self._walkie_mode:
            self._db.hotkey_walkie = hk
        elif not self._walkie_mode:
            self._db.hotkey_mic = hk

        self._bus.shared.app_hotkey_updated.emit(mode, hotkey)
    
    def _on_change_mode(self, mode: bool):
        self._db.walkie_status = mode
        # self._bus.shared.int_change_hotkey.emit(mode, '')
        self._bus.shared.app_mode_updated.emit(mode)

    def _on_change_default_mic(self, device_id: str):
        self._bus.shared.cmd_set_default_mic.emit(device_id)

    def _on_toggle_force_mute(self, state: bool):
        self._force_mute_enabled = state
        self._db.forced_mute = int(state)
        self._bus.system.app_forced_mute_changed.emit(state)

    def _on_toggle_mute_on_startup(self, state: bool):
        """Обработка изменения настройки 'Выключать микрофон при запуске'."""
        self._enable_mic = state
        self._db.enable_mic = int(state)
        self._bus.system.app_mute_on_startup_changed.emit(state)


    # --- answer from services handlers ---

    def _on_answ_set_mic_mute(self, muted: bool):
        if muted is None:
            raise AudioServiceCommandError("AudioInputService failed to execute SetMute.")
        self._bus.shared.app_mic_state_updated.emit(muted)

    def _on_answ_set_default_mic(self, device_id: str):
        if device_id is None:
            raise AudioServiceCommandError("AudioInputService failed to execute SetDefaultDevice.")
        self._bus.shared.app_default_mic_updated.emit(device_id)

    def _on_answ_bind_hotkeys(self, mode: bool, hotkey: str):
        if mode and hotkey == '':
            self._db.hotkey_walkie = 'unmapped'
        elif not mode and hotkey == '':
            self._db.hotkey_mic = 'unmapped'

        if mode and hotkey:
            self._db.hotkey_walkie = hotkey
        elif not mode and hotkey:
            self._db.hotkey_mic = hotkey


    def _on_os_default_mic_changed(self, device_id: str):
        logging.warning(f"OS default mic changed to {device_id}.")
        self._bus.shared.app_default_mic_updated.emit(device_id)

    def _on_os_devices_list_changed(self, devices: dict[str, str]):
        logging.warning(f"OS devices list changed to {devices}.")
        self._bus.shared.app_devices_list_updated.emit(devices)

    def _enforce_mute_rules(self, os_is_muted: bool):
        """
        Принудительное применение правил управления микрофоном.

        Логика:
        - Если состояние ОС совпадает с ожидаемым — всё ОК, сброс счётчика.
        - В Walkie-mode: микрофон ВСЕГДА должен быть заглушен (когда не нажата кнопка).
          Force Mute подразумевается режимом.
        - В Toggle-mode с Force Mute: микрофон должен соответствовать _expected_is_muted.
        - В Toggle-mode БЕЗ Force Mute: синхронизируемся с ОС.
        - При 20 попытках "гонки состояний" — режим сдаётся и выключается.
        """
        # 1. Если состояние ОС совпадает с ожидаемым — всё ОК
        if os_is_muted == self._expected_is_muted:
            self._bus.shared.app_mic_state_updated.emit(self._expected_is_muted)
            return

        # 2. Определяем, применяется ли принудительный контроль
        # В walkie-режиме — всегда применяется (implied force mute)
        # В toggle-режиме — только если включён Force Mute
        force_mute_applies = self._walkie_mode or self._force_mute_enabled

        if force_mute_applies:
            logging.warning(
                f"OS state violated application rules! "
                f"Enforcing Force Mute (attempt {self._force_mute_attempts + 1}/{self.MAX_FORCE_MUTE_ATTEMPTS})."
            )

            self._force_mute_attempts += 1
            self.debounce_timer.start(2000)
 
            if self._force_mute_attempts >= self.MAX_FORCE_MUTE_ATTEMPTS:
                logging.warning(
                    f"Anti-Hot-Loop triggered after {self.MAX_FORCE_MUTE_ATTEMPTS} attempts! "
                    f"Surrendering to OS state."
                )
                self._surrender_to_os(os_is_muted)
                return

            # Принудительно возвращаем микрофон в ожидаемое состояние
            self._bus.shared.cmd_set_mic_mute.emit(self._expected_is_muted)
        else:
            # Force Mute выключен — просто синхронизируемся с ОС
            logging.warning("Synced expected state with OS (Forced Mute is OFF).")
            self._expected_is_muted = os_is_muted
            self._bus.shared.app_mic_state_updated.emit(self._expected_is_muted)

    def _surrender_to_os(self, os_is_muted: bool):
        """
        Действия при "сдаче" после MAX_FORCE_MUTE_ATTEMPTS попыток контроля.

        - В Walkie-mode: выключить режим, сбросить галочку в БД, переключиться в toggle.
        - В Toggle-mode с Force Mute: выключить Force Mute, снять галочку.
        - Синхронизировать _expected_is_muted с реальным состоянием ОС.
        """
        self._force_mute_attempts = 0
        self._expected_is_muted = os_is_muted

        if self._walkie_mode:
            logging.warning("Surrender: disabling Walkie-talkie mode.")
            self._walkie_mode = False
            self._walkie_pressed = False
            self._db.walkie_status = 0

            # Уведомляем UI и сервисы
            self._bus.shared.app_mode_updated.emit(False)
            self._bus.shared.app_hotkey_updated.emit(False, self._db.hotkey_mic)
            self._bus.shared.cmd_bind_hotkeys.emit(False, self._db.hotkey_mic)
        elif self._force_mute_enabled:
            logging.warning("Surrender: disabling Force Mute.")
            self._force_mute_enabled = False
            self._db.forced_mute = 0
            self._bus.system.app_forced_mute_changed.emit(False)

        # Уведомляем UI о новом состоянии микрофона
        self._bus.shared.app_mic_state_updated.emit(self._expected_is_muted)

    def cleanup(self):
        self.debounce_timer.thread().quit()
