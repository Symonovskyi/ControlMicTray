class BaseStyle:
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
    primary_color =         "#1B1B1B"
    secondary_color =       "#7D8A90"
    accent_color =          "#127D91"
    accent_hover_color =    "#04BED5"
    background_color =      "#F3F3F3"
    text_color =            "#404040"
    button_color =          "#BECBD1"
    button_hover_color =    "#7D8A90"
    border_color =          "#1F2A30"
    neutral_color =         "#7D8A90"
    underline_color =       "#444F55"
    highlighted_color =     "#1F2A30"
    on_color =              "#22C245"
    off_color =             "#C22C22"

class TrayIconStyles:
    def __init__(self, qinstance):
        self.tray = qinstance

    def set_styles(self, theme):
        theme_colors = LightTheme if theme == 'Light' else DarkTheme

        primary_color =         theme_colors.primary_color
        background_color =      theme_colors.background_color
        border_color =          theme_colors.border_color
        text_color =            theme_colors.text_color

        border =                BaseStyle.border
        border_radius_small =   BaseStyle.border_radius_small

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
    def __init__(self, qinstance, settings_instance=None):
        self.settings_win_qwidget = qinstance
        self.settings_win = self.settings_win_qwidget.settings_UI

    def set_styles(self, theme):
        theme_colors = LightTheme if theme == 'Light' else DarkTheme

        text_color =            theme_colors.text_color
        background_color =      theme_colors.background_color
        underline_color =       theme_colors.underline_color
        accent_hover_color =    theme_colors.accent_hover_color
        button_color =          theme_colors.button_color
        button_hover_color =    theme_colors.button_hover_color
        highlighted_color =     theme_colors.highlighted_color

        font_family =           BaseStyle.font_family
        font_size_regular =     BaseStyle.font_size_regular
        border =                BaseStyle.border
        border_none =           BaseStyle.border_none
        border_radius_none =    BaseStyle.border_radius_none
        border_radius_medium =  BaseStyle.border_radius_medium

        self.settings_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {text_color};
                background-color: {background_color};
                border: {border_none};
                font-size: {font_size_regular};
                font-family: {font_family};
            }}
        """)

        self.settings_win.AlertsType.setStyleSheet(f"""
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

        self.settings_win_qwidget.hotkey_mic.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {border} {underline_color};
            }}

            QLineEdit::hover {{
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self.settings_win_qwidget.hotkey_walkie.setStyleSheet(f"""
            QLineEdit {{
                border-bottom: {border} {underline_color};
            }}

            QLineEdit::hover {{
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self.settings_win.LanguageCode.setStyleSheet(f"""
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

        self.settings_win.UrlUpdates.setStyleSheet(f"""
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
    def __init__(self, qinstance):
        self.about_win_qwidget = qinstance
        self.about_win = self.about_win_qwidget.about_UI

    def set_styles(self, theme):
        theme_colors = LightTheme if theme == 'Light' else DarkTheme

        text_color =            theme_colors.text_color
        background_color =      theme_colors.background_color
        button_color =          theme_colors.button_color
        button_hover_color =    theme_colors.button_hover_color
        accent_color =          theme_colors.accent_color
        accent_hover_color =    theme_colors.accent_hover_color
        highlighted_color =     theme_colors.highlighted_color

        font_family =           BaseStyle.font_family
        font_size_regular =     BaseStyle.font_size_regular
        font_size_small =       BaseStyle.font_size_small
        text_align_left =       BaseStyle.text_align_left
        border =                BaseStyle.border
        border_none =           BaseStyle.border_none
        transparent =           BaseStyle.transparent

        self.about_win_qwidget.setStyleSheet(f"""
            QWidget {{
                color: {text_color};
                background-color: {background_color};
                border: {border_none};
                font-size: {font_size_regular};
                font-family: {font_family}
            }}
        """)

        self.about_win.LogoFrame.setStyleSheet(f"""
            QLabel {{
                background-color: {transparent};
            }}
        """)

        self.about_win.WebSite.setStyleSheet(f"""
            QPushButton {{
                color: {accent_color};
                text-align: {text_align_left};
            }}

            QPushButton::hover {{
                color: {accent_hover_color};
            }}
        """)


        self.about_win.Email.setStyleSheet(f"""
            QPushButton {{
                color: {accent_color};
                text-align: {text_align_left};
            }}
            
            QPushButton::hover {{
                color: {accent_hover_color};
            }}
        """)

        self.about_win.UrlPrivacyPolicy.setStyleSheet(f"""
            QPushButton {{
                color: {button_color};
                border-bottom: {border} {highlighted_color};
            }}

            QPushButton::hover {{
                color: {button_hover_color};
                border-bottom: {border} {accent_hover_color};
            }}
        """)

        self.about_win.Copyright.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: {font_size_small};
            }}
        """)
