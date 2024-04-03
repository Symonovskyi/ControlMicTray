class BaseStyle:
    font_family = "Roboto, Arial, sans-serif"
    font_size_regular = "14px"
    font_size_small = "10px"
    text_align_left = "left"
    border = "1px solid"
    border_none = "0"
    border_radius_small = "3px"
    border_radius_none = "0"
    border_radius_medium = "5px"
    transparent_background = "rgba(0, 0, 0, 0)"

class DarkTheme(BaseStyle):
    color_primary = "#7D8A90"
    background_color_menu = "#1F2A30"
    border_color = "#444F55"
    background_color_general = "#273238"
    text_color = "#BECBD1"
    hover_text_color = "#04BED5"
    active_button_text = "#CEDCDF"
    link_text = "#127D91"

class LightTheme(BaseStyle):
    color_primary = "#7D8A90"
    background_color_dropdown_menu = "#FFFFFF"
    underline_border_color = "#444F55"
    background_color_general = "#FFFFFF"
    text_color = "#1F2A30"
    hover_text_color = "#04BED5"
    active_button_text = "#1F2A30"
    link_text = "#127D91"

class TrayIconStyles:
    def __init__(self, qinstance):
        self.tray = qinstance

    def dark_theme(self):
        self.tray.menu.setStyleSheet(f"""
            QMenu {{
                color: {DarkTheme.color_primary};
                background-color: {DarkTheme.background_color_menu};
                border: {BaseStyle.border} {DarkTheme.border_color};
                border-radius: {BaseStyle.border_radius_small};
                selection-background-color: {DarkTheme.background_color_general};
                selection-color: {DarkTheme.text_color};
            }}
        """)

    def white_theme(self):
        self.tray.menu.setStyleSheet(f"""
            QMenu {{
                color: {LightTheme.color_primary};
                background-color: {LightTheme.background_color_dropdown_menu};
                border: {BaseStyle.border} {LightTheme.underline_border_color};
                border-radius: {BaseStyle.border_radius_small};
                selection-background-color: {LightTheme.background_color_general};
                selection-color: {LightTheme.text_color};
            }}
        """)

class SettingsWindowStyles:
    def __init__(self, qinstance, settings_instance=None):
        self.settings_win_qwidget = qinstance
        self.settings_win = self.settings_win_qwidget.settings_UI

    def dark_theme(self):
        self.settings_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {DarkTheme.text_color};
                background-color: {DarkTheme.background_color_general};
                border: {BaseStyle.border_none};
                font-size: {BaseStyle.font_size_regular};
                font-family: {BaseStyle.font_family};
            }}
        """)

        self.settings_win.AlertsType.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {BaseStyle.border} {DarkTheme.border_color};
            }}

            QComboBox::hover{{
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}
            
            QComboBox QAbstractItemView {{
                background-color: {DarkTheme.background_color_menu};
                border: {BaseStyle.border} {DarkTheme.hover_text_color};
                color: {DarkTheme.color_primary};
                selection-background-color: {DarkTheme.background_color_general};
                selection-color: {DarkTheme.text_color};
                border-top-left-radius: {BaseStyle.border_radius_none};
                border-top-right-radius: {BaseStyle.border_radius_none};
                border-bottom-right-radius: {BaseStyle.border_radius_medium};
                border-bottom-left-radius: {BaseStyle.border_radius_medium};
            }}
        """)

        self.settings_win_qwidget.hotkey_mic.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {BaseStyle.border} {DarkTheme.border_color};
            }}

            QLineEdit::hover {{
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}
        """)

        self.settings_win_qwidget.hotkey_walkie.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {BaseStyle.border} {DarkTheme.border_color};
            }}

            QLineEdit::hover {{
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}
        """)

        self.settings_win.LanguageCode.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {BaseStyle.border} {DarkTheme.border_color};
            }}

            QComboBox::hover {{
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}

            QComboBox QAbstractItemView {{
                background-color: {DarkTheme.background_color_menu};
                border: {BaseStyle.border} {DarkTheme.hover_text_color};
                color: {DarkTheme.color_primary};
                selection-background-color: {DarkTheme.background_color_general};
                selection-color: {DarkTheme.text_color};
                border-top-left-radius: {BaseStyle.border_radius_none};
                border-top-right-radius: {BaseStyle.border_radius_none};
                border-bottom-right-radius: {BaseStyle.border_radius_medium};
                border-bottom-left-radius: {BaseStyle.border_radius_medium};
            }}
        """)

        self.settings_win.UrlUpdates.setStyleSheet(f"""
            QPushButton {{
                color: {DarkTheme.color_primary};
                border-bottom: {BaseStyle.border} {DarkTheme.background_color_menu};
            }}
            
            QPushButton::hover {{
                color: {DarkTheme.active_button_text};
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}
        """)

    def white_theme(self):
        self.settings_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {LightTheme.text_color};
                background-color: {LightTheme.background_color_general};
                border: {BaseStyle.border_none};
                font-size: {BaseStyle.font_size_regular};
                font-family: {BaseStyle.font_family}
            }}
        """)

        self.settings_win.AlertsType.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {BaseStyle.border} {LightTheme.underline_border_color};
            }}

            QComboBox::hover {{
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}

            QComboBox QAbstractItemView {{
                background-color: {LightTheme.background_color_dropdown_menu};
                border: {BaseStyle.border} {LightTheme.hover_text_color};
                color: {LightTheme.color_primary};
                selection-background-color: {LightTheme.background_color_general};
                selection-color: {LightTheme.text_color};
                border-top-left-radius: {BaseStyle.border_radius_none};
                border-top-right-radius: {BaseStyle.border_radius_none};
                border-bottom-right-radius: {BaseStyle.border_radius_medium};
                border-bottom-left-radius: {BaseStyle.border_radius_medium};
            }}
        """)

        self.settings_win_qwidget.hotkey_mic.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {BaseStyle.border} {LightTheme.underline_border_color};
            }}

            QLineEdit::hover {{
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}
        """)

        self.settings_win_qwidget.hotkey_walkie.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {BaseStyle.border} {LightTheme.underline_border_color};
            }}

            QLineEdit::hover {{
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}
        """)

        self.settings_win.LanguageCode.setStyleSheet(f"""
            QComboBox {{
                border-bottom: {BaseStyle.border} {LightTheme.underline_border_color};
            }}

            QComboBox::hover {{
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}

            QComboBox QAbstractItemView {{
                background-color: {LightTheme.background_color_dropdown_menu};
                border: {BaseStyle.border} {LightTheme.hover_text_color};
                color: {LightTheme.color_primary};
                selection-background-color: {LightTheme.background_color_general};
                selection-color: {LightTheme.text_color};
                border-top-left-radius: {BaseStyle.border_radius_none};
                border-top-right-radius: {BaseStyle.border_radius_none};
                border-bottom-right-radius: {BaseStyle.border_radius_medium};
                border-bottom-left-radius: {BaseStyle.border_radius_medium};
            }}
        """)

        self.settings_win.UrlUpdates.setStyleSheet(f"""
            QPushButton {{
                color: {LightTheme.color_primary};
                border-bottom: {BaseStyle.border} {LightTheme.background_color_dropdown_menu};
            }}

            QPushButton::hover {{
                color: {LightTheme.active_button_text};
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}
        """)

class AboutWindowStyles():
    def __init__(self, qinstance):
        self.about_win_qwidget = qinstance
        self.about_win = self.about_win_qwidget.about_UI

    def dark_theme(self):
        self.about_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {DarkTheme.text_color};
                background-color: {DarkTheme.background_color_general};
                border: {BaseStyle.border_none};
                font-size: {BaseStyle.font_size_regular};
                font-family: {BaseStyle.font_family}
            }}
        """)

        self.about_win.Copyright.setStyleSheet(f"""
            QLabel {{
                color: {DarkTheme.color_primary};
                font-size: {BaseStyle.font_size_small};
            }}
        """)

        self.about_win.Email.setStyleSheet(f"""
            QPushButton {{
                color: {DarkTheme.link_text};
                text-align: {BaseStyle.text_align_left};
            }}
            
            QPushButton::hover {{
                color: {DarkTheme.hover_text_color};
            }}
        """)

        self.about_win.LogoFrame.setStyleSheet(f"""
            QLabel {{
                background-color: {BaseStyle.transparent_background};
            }}
        """)

        self.about_win.UrlPrivacyPolicy.setStyleSheet(f"""
            QPushButton {{
                color: {DarkTheme.color_primary};
                border-bottom: {BaseStyle.border} {DarkTheme.background_color_menu};
            }}

            QPushButton::hover {{
                color: {DarkTheme.active_button_text};
                border-bottom: {BaseStyle.border} {DarkTheme.hover_text_color};
            }}
        """)

        self.about_win.WebSite.setStyleSheet(f"""
            QPushButton {{
                color: {DarkTheme.link_text};
                text-align: {BaseStyle.text_align_left};
            }}

            QPushButton::hover {{
                color: {DarkTheme.hover_text_color};
            }}
        """)

    def white_theme(self):
        self.about_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {LightTheme.text_color};
                background-color: {LightTheme.background_color_general};
                border: {BaseStyle.border_none};
                font-size: {BaseStyle.font_size_regular};
                font-family: {BaseStyle.font_family}
            }}
        """)

        self.about_win.Copyright.setStyleSheet(f"""
            QLabel {{
                color: {LightTheme.color_primary};
                font-size: {BaseStyle.font_size_small};
            }}
        """)

        self.about_win.Email.setStyleSheet(f"""
            QPushButton {{
                color: {LightTheme.link_text};
                text-align: {BaseStyle.text_align_left};
            }}

            QPushButton::hover {{
                color: {LightTheme.hover_text_color};
            }}
        """)

        self.about_win.LogoFrame.setStyleSheet(f"""
            QLabel {{
                background-color: {BaseStyle.transparent_background};
            }}
        """)

        self.about_win.UrlPrivacyPolicy.setStyleSheet(f"""
            QPushButton {{
                color: {LightTheme.color_primary};
                border-bottom: {BaseStyle.border} {LightTheme.background_color_dropdown_menu};
            }}

            QPushButton::hover {{
                color: {LightTheme.active_button_text};
                border-bottom: {BaseStyle.border} {LightTheme.hover_text_color};
            }}
        """)

        self.about_win.WebSite.setStyleSheet(f"""
            QPushButton {{
                color: {LightTheme.link_text};
                text-align: {BaseStyle.text_align_left};
            }}

            QPushButton::hover {{
                color: {LightTheme.hover_text_color};
            }}
        """)
