# src/core/entities.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class Microphone:
    """
    Represents general (non-OS-specific) microphone object.
    """

    id: str
    name: str
    volume: float
    muted: bool
    active: bool
    default: bool


@dataclass(frozen=True)
class ToogleHotKey:
    """
    Represents general toggle only hotkey object.
    """

    key_sequence: str
    action: str


@dataclass(frozen=True)
class WalkieHotKey:
    """
    Represents general toggle only hotkey object.
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
