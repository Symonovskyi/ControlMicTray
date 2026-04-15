# src/bus/events.py

from dataclasses import dataclass


# ============================= Hotkey Events ==============================
class BaseHotkeyEvent:
    """Base container for hotkey-related events."""

    hotkey_str: str


@dataclass
class HotkeyActivated(BaseHotkeyEvent):
    """Event: User-defined hotkey activated."""

    pass


@dataclass
class HotkeyReleased(BaseHotkeyEvent):
    """Event: User-defined hotkey released."""

    pass


@dataclass
class NewHotkeySet(BaseHotkeyEvent):
    """Event: New hotkey set."""

    pass
