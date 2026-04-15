# file: event_bus.py
from PyQt6.QtCore import QObject, pyqtSignal
from src.services.bus.events import HotkeyActivated, HotkeyReleased, NewHotkeySet


class EventBus(QObject):
    """
    Wide-Application Event Bus.


    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._handlers = {}  # Initialize attributes here
        return cls._instance

    def subscribe(self, event_type, handler):
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event_type, *args, **kwargs):
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                handler(*args, **kwargs)

    shortcut_activated = pyqtSignal(HotkeyActivated)
    shortcut_released = pyqtSignal(HotkeyReleased)
    new_shortcut_set = pyqtSignal(NewHotkeySet)


# Создаем единственный экземпляр, который будет импортироваться
# во всем приложении.
event_bus = EventBus()
