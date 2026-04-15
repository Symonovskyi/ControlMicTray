from webbrowser import WindowsDefault

from core.events import EventBus
from core.services.storage import StorageService


class SystemService:
    def __init__(self, bus: EventBus, db: StorageService):
        self._bus = bus
        self._db = db
        
        # Connecting requests (commands) to slots
        self._bus.system.open_url_intent.connect(self._open_url)
        self._bus.system.int_toggle_privacy.connect(self._change_privacy_status)


    # Slots
    def _open_url(self, url: str):
        WindowsDefault().open_new_tab(url)

    def _change_privacy_status(self, state: bool):
        self._db.privacy_status = int(state)
