# set the themeService responsible for all Icon redraws, except mic icon in tray

from PyQt6.QtWidgets import QWidget

from core.widgets.ui.about import Ui_AboutWindow as AboutUI
from core.styles import AboutWindowStyles, BaseStyle
from core.events import EventBus


class AboutWindow(QWidget):
    """
    About window displaying application information.
    """

    def __init__(self, bus: EventBus, parent=None):
        super().__init__(parent)
        self._bus = bus

        # UI
        self.about_UI = AboutUI()
        self.about_UI.setupUi(self)

        # Styles
        self.about_styles = AboutWindowStyles(self)

        self._setup_connections()

    def _setup_connections(self):
        """Connect UI events directly to PyQt signals."""
        self._bus.storage.app_initial_state_loaded.connect(self.__init_set_display_data)
        self._bus.theme.app_theme_changed.connect(self._on_theme_changed)

        self._bus.shared.int_open_about.connect(self.show)


    def __init_set_display_data(self, data: dict):
        # Set version
        self.about_UI.ProgramVersion.setText(data.get("program_version", "v.2026.30.03"))

        # Set privacy policy url
        self.about_UI.UrlPrivacyPolicy.setText(data.get("url_privacy_policy", "localhost"))

    def _on_theme_changed(self, palette: BaseStyle):
        self.about_styles.set_styles(palette)
