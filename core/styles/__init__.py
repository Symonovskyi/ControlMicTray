from typing import TYPE_CHECKING
from core.styles.icons import Icons, QIcon

if TYPE_CHECKING:
    from core.widgets import TrayIcon, SettingsWindow, AboutWindow

class BaseStyle:
    # for typing
    theme_id                :int
    primary_color           :str
    secondary_color         :str
    accent_color            :str
    accent_hover_color      :str
    background_color        :str
    text_color              :str
    button_color            :str
    button_hover_color      :str
    border_color            :str
    neutral_color           :str
    underline_color         :str
    highlighted_color       :str
    on_color                :str
    off_color               :str

    font_family =           "Roboto, Arial, sans-serif"
    font_size_regular =     "14px"
    font_size_small =       "10px"
    text_align_left =       "left"
    border =                "1px solid"
    border_none =           "0"
    border_radius_small =   "3px"
    border_radius_none =    "0"
    border_radius_medium =  "5px"
    transparent =           "rgba(0, 0, 0, 0)"


class DarkTheme(BaseStyle):
    theme_id =              1
    primary_color =         "#F3F3F3"
    secondary_color =       "#7D8A90"
    accent_color =          "#127D91"
    accent_hover_color =    "#04BED5"
    background_color =      "#273238"
    text_color =            "#BECBD1"
    button_color =          "#7D8A90"
    button_hover_color =    "#BECBD1"
    border_color =          "#1F2A30"
    neutral_color =         "#7D8A90"
    underline_color =       "#444F55"
    highlighted_color =     "#1F2A30"
    on_color =              "#22C245"
    off_color =             "#C22C22"


class LightTheme(BaseStyle):
    theme_id =              0
    primary_color =         "#1B1B1B"
    secondary_color =       "#7D8A90"
    accent_color =          "#127D91"
    accent_hover_color =    "#04BED5"
    background_color =      "#F3F3E4"
    text_color =            "#404040"
    button_color =          "#404040"
    button_hover_color =    "#1F2A30"
    border_color =          "#1F2A30"
    neutral_color =         "#7D8A90"
    underline_color =       "#444F55"
    highlighted_color =     "#1F2A30"
    on_color =              "#22C245"
    off_color =             "#C22C22"


class TrayIconStyles:
    def __init__(self, qinstance: TrayIcon):
        self.tray = qinstance
        self.curr_palette = None

    def update_tray_icons(self, state: bool, is_walkie: bool):
        palette = self.curr_palette if self.curr_palette is not None else DarkTheme

        self.tray.setIcon(Icons.get_icon(Icons.microphone_icon, palette=palette, state=state))

        if is_walkie:
            if self.tray.toggle_mic.isEnabled():
                self.tray.toggle_mic.setEnabled(True)
            self.tray.toggle_mic.setEnabled(False)
            self.tray.toggle_mic.setIcon(Icons.get_icon(Icons.switch_icon, palette=palette, state=False))
            self.tray.walkie_mic.setIcon(Icons.get_icon(Icons.switch_icon, palette=palette, state=True))
        else:
            if not self.tray.toggle_mic.isEnabled():
                self.tray.toggle_mic.setEnabled(True)
            self.tray.toggle_mic.setIcon(Icons.get_icon(Icons.switch_icon, palette=palette, state=state))
            self.tray.walkie_mic.setIcon(Icons.get_icon(Icons.switch_icon, palette=palette, state=False))

        for action in self.tray.device_action_group.actions():
            if action.isChecked():
                action.setIcon(Icons.get_icon(Icons.dot_icon, palette=palette))
            else:
                action.setIcon(QIcon())

    def set_styles(self, palette: BaseStyle):
        self.curr_palette = palette

        primary_color =         palette.primary_color
        background_color =      palette.background_color
        border_color =          palette.border_color
        text_color =            palette.text_color

        border =                palette.border
        border_radius_small =   palette.border_radius_small

        def q_icon(icon: Icons) -> str:
            return Icons.get_icon(icon, palette=palette)

        self.tray.devices_menu.setIcon(q_icon(Icons.microphone_icon))
        self.tray.settings_action.setIcon(q_icon(Icons.settings_icon))
        self.tray.about_action.setIcon(q_icon(Icons.about_icon))
        self.tray.exit_action.setIcon(q_icon(Icons.exit_icon))

        self.tray.menu.setStyleSheet(f"""
            QMenu {{
                color: {primary_color};
                background-color: {background_color};
                border: {border} {border_color};
                border-radius: {border_radius_small};
                selection-background-color: {background_color};
                selection-color: {text_color};
            }}
        """)

class SettingsWindowStyles:
    def __init__(self, qinstance: SettingsWindow):
        self._settings_win_qwidget = qinstance
        self._settings_win = self._settings_win_qwidget.settings_UI

    def set_styles(self, palette: BaseStyle):
        text_color =            palette.text_color
        background_color =      palette.background_color
        underline_color =       palette.underline_color
        neutral_color =         palette.neutral_color
        accent_hover_color =    palette.accent_hover_color
        button_color =          palette.button_color
        button_hover_color =    palette.button_hover_color
        highlighted_color =     palette.highlighted_color

        font_family =           BaseStyle.font_family
        font_size_regular =     BaseStyle.font_size_regular
        border =                BaseStyle.border
        border_none =           BaseStyle.border_none
        border_radius_none =    BaseStyle.border_radius_none
        border_radius_medium =  BaseStyle.border_radius_medium
        border_radius_small =   BaseStyle.border_radius_small

        icon = Icons.get_icon(Icons.frame_icon, palette=palette)
        self._settings_win_qwidget.setWindowIcon(icon)

        qcheckbox_styles = f"""
            QCheckBox::indicator:unchecked {{
                border: 1px solid {neutral_color};
                border-top-left-radius: {border_radius_small};
                border-top-right-radius: {border_radius_small};
                border-bottom-right-radius: {border_radius_small};
                border-bottom-left-radius: {border_radius_small};
            }}

            QCheckBox::indicator:checked {{
                color: {neutral_color};
            }}
        """

        self._settings_win.NightTheme.setStyleSheet(qcheckbox_styles)
        self._settings_win.EnableProgram.setStyleSheet(qcheckbox_styles)
        self._settings_win.PrivacyStatus.setStyleSheet(qcheckbox_styles)
        self._settings_win.EnableMic.setStyleSheet(qcheckbox_styles)

        self._settings_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {text_color};
                background-color: {background_color};
                border: {border_none};
                font-size: {font_size_regular};
                font-family: {font_family};
            }}
        """)

        self._settings_win.AlertsType.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {border} {underline_color};
            }}

            QComboBox::hover {{
                border-bottom: {border} {accent_hover_color};
            }}

            QComboBox QAbstractItemView {{
                background-color: {background_color};
                border: {border} {accent_hover_color};
                color: {text_color};
                selection-background-color: {background_color};
                selection-color: {text_color};
                border-top-left-radius: {border_radius_none};
                border-top-right-radius: {border_radius_none};
                border-bottom-right-radius: {border_radius_medium};
                border-bottom-left-radius: {border_radius_medium};
            }}
        """)

        self._settings_win_qwidget.btn_hotkey_mic.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {border} {underline_color};
            }}

            QLineEdit::hover {{
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self._settings_win_qwidget.btn_hotkey_walkie.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {border} {underline_color};
            }}

            QLineEdit::hover {{
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self._settings_win.LanguageCode.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {border} {underline_color};
            }}

            QComboBox::hover {{
                border-bottom: {border} {accent_hover_color};
            }}

            QComboBox QAbstractItemView {{
                background-color: {background_color};
                border: {border} {accent_hover_color};
                color: {text_color};
                selection-background-color: {background_color};
                selection-color: {text_color};
                border-top-left-radius: {border_radius_none};
                border-top-right-radius: {border_radius_none};
                border-bottom-right-radius: {border_radius_medium};
                border-bottom-left-radius: {border_radius_medium};
            }}
        """)

        self._settings_win.UrlUpdates.setStyleSheet(f"""
            QPushButton {{
                color: {button_color};
                border-bottom: {border} {highlighted_color};
            }}

            QPushButton::hover {{
                color: {button_hover_color};
                border-bottom: {border} {accent_hover_color};
            }}
        """)

class AboutWindowStyles:
    def __init__(self, qinstance: AboutWindow):
        self._about_win_qwidget = qinstance
        self._about_win = self._about_win_qwidget.about_UI

    def set_styles(self, palette: BaseStyle):
        text_color =            palette.text_color
        background_color =      palette.background_color
        button_color =          palette.button_color
        button_hover_color =    palette.button_hover_color
        accent_color =          palette.accent_color
        accent_hover_color =    palette.accent_hover_color
        highlighted_color =     palette.highlighted_color

        font_family =           BaseStyle.font_family
        font_size_regular =     BaseStyle.font_size_regular
        font_size_small =       BaseStyle.font_size_small
        text_align_left =       BaseStyle.text_align_left
        border =                BaseStyle.border
        border_none =           BaseStyle.border_none
        transparent =           BaseStyle.transparent

        icon = Icons.get_icon(Icons.frame_icon, palette=palette)
        logo_obj = self._about_win.Logo
        logo_obj.setPixmap(icon.pixmap(logo_obj.width(), logo_obj.height()))
        self._about_win_qwidget.setWindowIcon(icon)

        self._about_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {text_color};
                background-color: {background_color};
                border: {border_none};
                font-size: {font_size_regular};
                font-family: {font_family}
            }}
        """)

        self._about_win.LogoFrame.setStyleSheet(f"""
            QLabel {{
                background-color: {transparent};
            }}
        """)

        self._about_win.WebSite.setStyleSheet(f"""
            QPushButton {{
                color: {accent_color};
                text-align: {text_align_left};
            }}

            QPushButton::hover {{
                color: {accent_hover_color};
            }}
        """)


        self._about_win.Email.setStyleSheet(f"""
            QPushButton {{
                color: {accent_color};
                text-align: {text_align_left};
            }}
            
            QPushButton::hover {{
                color: {accent_hover_color};
            }}
        """)

        self._about_win.UrlPrivacyPolicy.setStyleSheet(f"""
            QPushButton {{
                color: {button_color};
                border-bottom: {border} {highlighted_color};
            }}

            QPushButton::hover {{
                color: {button_hover_color};
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self._about_win.Copyright.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: {font_size_small};
            }}
        """)
