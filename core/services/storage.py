from core.database import DatabaseManager
from core.events import EventBus


class StorageService:
    def __init__(self, bus: EventBus):
        self._bus = bus
        self._db = DatabaseManager()

        # on init
        self._bus.storage.int_load_initial_state.connect(self._on_load_initial_state)

    def _on_load_initial_state(self):
        initial_state = {
            "theme_id": self.theme,
            "language": self.language_code,
            "walkie_status": bool(self.walkie_status),
            "forced_mute": bool(self.forced_mute),
            "mic_on_startup": bool(self.enable_mic),
            "mic_status": bool(self.mic_status),
            "hotkey_mic": self.hotkey_mic,
            "hotkey_walkie": self.hotkey_walkie,
            "autorun": bool(self.enable_program),
            "program_version": self.program_version,
            "web_site": self.web_site,
            "email": self.email,
            "copyright": self.copyright,
            "url_privacy_policy": self.url_privacy_policy,
            "privacy_status": self.privacy_status
        }

        # emit all neccessary data on app init
        self._bus.storage.app_initial_state_loaded.emit(initial_state)

    # === User Properties ===
    @property
    def user_id(self):
        return self._db.get_property("User", "ID")

    @property
    def user_name(self):
        return self._db._user_name

    # === Hotkey Properties ===
    @property
    def hotkey_mic(self):
        return self._db.get_property("Hotkey", "HotkeyMic")

    @hotkey_mic.setter
    def hotkey_mic(self, value):
        self._db.set_property("Hotkey", "HotkeyMic", value)


    @property
    def hotkey_walkie(self):
        return self._db.get_property("Hotkey", "HotkeyWalkie")

    @hotkey_walkie.setter
    def hotkey_walkie(self, value):
        self._db.set_property("Hotkey", "HotkeyWalkie", value)

    # === Alerts Properties ===
    @property
    def alerts_type(self):
        return self._db.get_property("Alerts", "AlertsType")

    @alerts_type.setter
    def alerts_type(self, value):
        self._db.set_property("Alerts", "AlertsType", value)

    @property
    def standard_sound(self):
        return self._db.get_property("Alerts", "StandardSound")

    @standard_sound.setter
    def standard_sound(self, value):
        self._db.set_property("Alerts", "StandardSound", value)

    @property
    def own_sound(self):
        return self._db.get_property("Alerts", "OwnSound")

    @own_sound.setter
    def own_sound(self, value):
        self._db.set_property("Alerts", "OwnSound", value)

    # === Autorun Properties ===
    @property
    def enable_program(self):
        return self._db.get_property("Autorun", "EnableProgram")

    @enable_program.setter
    def enable_program(self, value):
        self._db.set_property("Autorun", "EnableProgram", value)

    @property
    def enable_mic(self):
        return self._db.get_property("Autorun", "EnableMic")

    @enable_mic.setter
    def enable_mic(self, value):
        self._db.set_property("Autorun", "EnableMic", value)

    @property
    def mic_status(self):
        return self._db.get_property("Autorun", "MicStatus")

    @mic_status.setter
    def mic_status(self, value):
        self._db.set_property("Autorun", "MicStatus", value)

    @property
    def walkie_status(self):
        return self._db.get_property("Autorun", "WalkieStatus")

    @walkie_status.setter
    def walkie_status(self, value):
        self._db.set_property("Autorun", "WalkieStatus", value)

    # === Settings Properties ===
    @property
    def language_code(self):
        return self._db.get_property("Settings", "LanguageCode")

    @language_code.setter
    def language_code(self, value):
        self._db.set_property("Settings", "LanguageCode", value)

    @property
    def theme(self):
        return self._db.get_property("Settings", "Theme")

    @theme.setter
    def theme(self, value):
        self._db.set_property("Settings", "Theme", value)

    @property
    def privacy_status(self):
        return self._db.get_property("Settings", "PrivacyStatus")

    @privacy_status.setter
    def privacy_status(self, value):
        self._db.set_property("Settings", "PrivacyStatus", value)

    @property
    def forced_mute(self):
        return self._db.get_property("Settings", "ForcedMute")
    
    @forced_mute.setter
    def forced_mute(self, value):
        self._db.set_property("Settings", "ForcedMute", value)

    # === About Properties ===
    @property
    def program_version(self):
        return self._db.get_property("About", "ProgramVersion")

    @property
    def web_site(self):
        return self._db.get_property("About", "WebSite")

    @property
    def email(self):
        return self._db.get_property("About", "Email")

    @property
    def copyright(self):
        return self._db.get_property("About", "Copyright")

    @property
    def url_privacy_policy(self):
        return self._db.get_property("About", "UrlPrivacyPolicy")
