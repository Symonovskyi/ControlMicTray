from dataclasses import dataclass

@dataclass
class AudioContextSnapshot:
    """Слепок текущего состояния системы для передачи в Политику."""
    is_walkie_mode: bool
    is_force_mute_enabled: bool
    expected_is_muted: bool
    os_is_muted: bool


class MutePolicy:
    """
    Движок бизнес-правил микрофона. 
    Изолирует сложную логику приоритетов и защиты состояния.
    """

    @staticmethod
    def resolve_startup_state(is_walkie: bool, mute_on_startup: bool, last_db_status: bool) -> bool:
        """
        Определяет состояние микрофона при запуске приложения.
        Приоритет: Walkie Mode -> Mute on Startup -> Last Saved Status.
        """
        if is_walkie:
            return True  # В режиме рации всегда стартуем заглушенными
        if mute_on_startup:
            return True  # Пользовательская настройка безопасности
        return last_db_status

    @staticmethod
    def should_enforce_mute(context: AudioContextSnapshot) -> bool:
        """
        Определяет, нужно ли нам "драться" с операционной системой,
        если реальное состояние микрофона не совпадает с ожидаемым.
        """
        if context.os_is_muted == context.expected_is_muted:
            return False  # Совпадает — защищать нечего

        if context.is_walkie_mode:
            return True   # В режиме рации мы ВСЕГДА защищаем состояние (Implied Force Mute)

        if context.is_force_mute_enabled:
            return True   # В Toggle-режиме защищаем, только если включена настройка

        return False      # Иначе смиряемся с изменением из ОС