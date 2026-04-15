from PyQt6.QtCore import QObject, pyqtSignal


class SharedAudioHotkeySignals(QObject):

    # INTENTS
    # Emitters: UI or HotkeyService
    # Subscribers: AudioHotkeyOrchestrator
    int_toggle_mic = pyqtSignal(bool)             # tray icon click\tray menu click\hotkey btn click
    int_change_mode = pyqtSignal(bool)            # request app for mode change to (true: walkie, false: toggle)
    int_walkie_press = pyqtSignal()               # hotkey walkie pressed
    int_walkie_release = pyqtSignal()             # hotkey walkie released
    int_change_default_mic = pyqtSignal(str)      # GUID of device to change to
    int_change_hotkey = pyqtSignal(bool, str)     # request for toggle/walkie hotkey change (bool: toggle|walkie, str: hk)

    int_open_settings = pyqtSignal()              # open settings window from tray
    int_open_about = pyqtSignal()                 # open about window from tray

    int_hotkey_toggle_mic = pyqtSignal(object)    # HotkeyService -> tray._toggler()

    # COMMANDS
    # Emitters: AudioHotkeyOrchestrator
    # Subscribers: HotkeyService and AudioInputService
    cmd_bind_hotkeys = pyqtSignal(bool, str)      # cmd for HotkeyService to rebind hotkeys
    cmd_set_mic_mute = pyqtSignal(bool)           # cmd for AudioInputService to change device mute state
    cmd_set_default_mic = pyqtSignal(str)         # GUID of device to change to

    # SERVICE EVENTS (Answers to Orchestrator from Services)
    answ_bind_hotkeys = pyqtSignal(bool, str)     # bool: mode | str: hotkey - if successful, `None` otherwise
    answ_set_mic_mute = pyqtSignal(bool)          # bool: muted? - if successful, `None` otherwise
    answ_set_default_mic = pyqtSignal(str)        # str: device_id - if successful, `None` otherwise

    # OS EVENTS
    # Emitters: AudioInputService
    # Subscribers: AudioHotkeyOrchestrator (for Forced Mute verification)
    os_mic_state_changed = pyqtSignal(bool)       # from OS: mic was muted by system
    os_default_mic_changed = pyqtSignal(str)      # from OS: default mic was changed
    os_devices_list_changed = pyqtSignal(dict)    # from OS: mic was unplugged

    # APP EVENTS (emitted from app/OS events)
    # Emitters: AudioHotkeyOrchestrator
    # Subscribers: UI (SettingsWindow, TrayIcon)
    app_mode_updated = pyqtSignal(bool)           # from orchestrator: mode was changed to (true: walkie, false: toggle)
    app_hotkey_updated = pyqtSignal(bool, str)    # from orchestrator: hotkey updated for (bool: mode, str: hk)
    app_mic_state_updated = pyqtSignal(bool)      # from orchestrator: mic was muted, accept to redraw_icons()
    app_default_mic_updated = pyqtSignal(str)     # from orchestrator: default mic `mic_id` changed
    app_devices_list_updated = pyqtSignal(dict)   # from orchestrator: devices list chaged to `dict`


class ThemeSignals(QObject):
    # intents (UI -> Service)
    int_change_theme = pyqtSignal(int)            # theme_id

    # events (Service -> UI)
    app_theme_changed = pyqtSignal(object)        # theme "BaseStyle" object
    tray_icon_change = pyqtSignal(bool, bool)     # states (is_muted, is_walkie)


class SystemSignals(QObject):
    # intents (UI -> Service)
    int_toggle_mute_on_startup = pyqtSignal(bool)
    int_toggle_force_mute = pyqtSignal(bool)
    int_change_language = pyqtSignal(str)          # lanugage_code
    int_toggle_privacy = pyqtSignal()
    int_toggle_autorun = pyqtSignal(bool)
    open_url_intent = pyqtSignal(str)              # url

    # events (Service -> UI)
    app_mute_on_startup_changed = pyqtSignal(bool) # ↓
    app_autorun_state_changed = pyqtSignal(bool)   # for errors handling (error notification\dialog call)
    app_forced_mute_changed = pyqtSignal(bool)     # ↑
    app_language_changed = pyqtSignal(str)         # lanugage_code


class StorageSignals(QObject):
    # INTENTS
    # Emitters: main.py (on app start)
    # Subscribers: StorageService
    int_load_initial_state = pyqtSignal()
    # int_get_property = pyqtSignal(str) # property_name
    # int_set_property = pyqtSignal(str) # property_name

    # APP EVENTS
    # Emitters: StorageService
    # Subscribers: UI (SettingsWindow, TrayIcon), Orchestrators
    app_initial_state_loaded = pyqtSignal(dict) # dict with all data from db
