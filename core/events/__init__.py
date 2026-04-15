from PyQt6.QtCore import QObject
from core.events.signals import (
    SystemSignals, ThemeSignals, SharedAudioHotkeySignals, StorageSignals
)


class EventBus(QObject):
    """Event Bus for decoupling core components."""
    def __init__(self):
        super().__init__()
        self.shared = SharedAudioHotkeySignals()
        self.theme = ThemeSignals()
        self.system = SystemSignals()
        self.storage = StorageSignals()
