from typing import TYPE_CHECKING
from abc import ABC, abstractmethod
from threading import RLock
import logging

if TYPE_CHECKING:
    from core.orchestrators.audio import AudioHotkeyOrchestrator


class BaseAudioState(ABC):
    """
    Base `State` pattern.
    Defines a scope of base functionality depending on app modes.
    """
    def __init__(self, orchestrator: AudioHotkeyOrchestrator):
        # using orchestrator (Context) as a bridge
        self.ctx = orchestrator 

    def on_enter(self):
        """Hook when switching to some state."""
        pass

    def on_exit(self):
        """Hook when switching from some state."""

    @abstractmethod
    def handle_toggle(self): pass
    
    @abstractmethod
    def handle_walkie_press(self): pass
    
    @abstractmethod
    def handle_walkie_release(self): pass


class ToggleModeState(BaseAudioState):
    def on_enter(self):
        self.lock = RLock()
        logging.info("--- Toggle Mode State ---")

    def handle_toggle(self):
        with self.lock:
            # Инвертируем состояние и отправляем команду железу
            self.ctx.expected_is_muted = not self.ctx.expected_is_muted
            self.ctx.send_mic_command()

    def handle_walkie_press(self):
        pass # Игнорируем зажатие хоткея рации в этом режиме

    def handle_walkie_release(self):
        pass


class WalkieModeState(BaseAudioState):
    def on_enter(self):
        self.lock = RLock()
        logging.info("--- АКТИВИРОВАН РЕЖИМ РАЦИИ (WALKIE) ---")
        # Безопасность: при переходе в этот режим микрофон ОБЯЗАН выключиться
        with self.lock:
            self.ctx.expected_is_muted = True
            self.ctx.send_mic_command()

    def handle_toggle(self):
        pass # Игнорируем клики по тумблеру в трее

    def handle_walkie_press(self):
        with self.lock:
            self.ctx.expected_is_muted = False
            self.ctx.send_mic_command()

    def handle_walkie_release(self):
        with self.lock:
            self.ctx.expected_is_muted = True
            self.ctx.send_mic_command()
