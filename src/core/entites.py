# src/core/entities.py

from dataclasses import dataclass
from typing import Optional

from src.core.exceptions import VolumeOutOfRangeError


@dataclass
class Microphone:
    """
    Represents general (non-OS-specific) microphone object.
    """

    id: str
    name: str
    volume: float
    is_muted: bool
    is_active: bool
    is_default: bool

    def toggle_mute(self) -> None:
        """Internal mute toggler for mic object."""
        self.is_muted = not self.is_muted

    def change_volume(self, new_level: float) -> None:
        """Internal volume changer for mic object."""
        if not 0 <= new_level <= 100:
            raise VolumeOutOfRangeError(new_level)
        self.volume = new_level


@dataclass(frozen=True)
class HotKey:
    """
    Represents general hotkey object.
    """

    key_sequence: str
    action: str


@dataclass
class AppSettings:
    """
    Represents app settings class
    """

    # About
    AppVersion: str
    Website: str = "https://controlmictray.pp.ua"
    Email: str = "i@controlmictray.pp.ua"
    CopyrightText: str = """Copyright © 2024
Symonovskyi & Lastivka
All rights reserved"""
    PrivacyPolicyUrl: str = "https://controlmictray.pp.ua/PrivacyPolicy.html"

    # Alerts
    # Alerts types: "DefaultSound", "OwnSound", "TrayNotification", "All", None
    AlertsType: Optional[str] = None
    OwnSoundPath: Optional[str] = None
    DefaultSoundPath: str = "sound\\notif.mp3"

    # Autorun
    AutoStartup: bool = True
    AutoEnableMic: bool = False
    LastMicStatus: bool = False
    LastWalkieStatus: bool = False
    LastActiveMicID: Optional[str] = None

    # Hotkeys
    MicHotkey: Optional[str] = None
    WalkieHotkey: Optional[str] = None

    # Settings
    # Theme types: "System", "Dark", "White", "PyQtDefaults"
    Theme: str = "Dark"
    LanguageCode: str = "ru"
    PrivacyAccepted: bool = False
