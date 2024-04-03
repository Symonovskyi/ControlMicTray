from ui.styles.styles import LightTheme, DarkTheme

from PyQt6.QtGui import QPixmap, QIcon, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import QByteArray, Qt

class Icons:
    _icon_cache = {}

    @classmethod
    def clear_cache(cls):
        cls._icon_cache.clear()

    @staticmethod
    def _render_svg(svg_data):
        svg_bytes = QByteArray(svg_data.encode('utf-8'))
        renderer = QSvgRenderer(svg_bytes)

        pixmap = QPixmap(renderer.defaultSize())
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()

        return QIcon(pixmap)

    @classmethod
    def get_icon(cls, icon_func, theme, *args, **kwargs):
        # Include the theme in the cache key
        cache_key = f"{icon_func.__name__}_{theme}_{args}_{kwargs}"
        if cache_key in cls._icon_cache:
            return cls._icon_cache[cache_key]

        # Generate the icon considering the theme
        svg_data = icon_func(theme=theme, *args, **kwargs)
        icon = cls._render_svg(svg_data)

        # Cache and return the icon
        cls._icon_cache[cache_key] = icon
        return icon

    @staticmethod
    def microphone_icon(theme='Dark', state=None):
        # If the theme is 'Light', choose the appropriate colors from LightTheme, otherwise from DarkTheme
        theme_colors = LightTheme if theme == 'Light' else DarkTheme
        # Determine stem color based on theme
        stem_color = theme_colors.primary_color
        # Determine head color based on theme and state
        head_color = (
            theme_colors.primary_color if state is None else
            theme_colors.on_color if state else
            theme_colors.off_color
        )

        # Generate SVG code using the determined colors
        return f"""
        <svg width="980" height="980" viewBox="0 0 980 980" fill="none" xmlns="http://www.w3.org/2000/svg">
            <g id="head" stroke="{head_color}">
                <rect x="330" y="40" width="320" height="645" rx="160" stroke-width="80"/>
                <path d="M290 220H460" stroke-width="60"/>
                <path d="M290 330H460" stroke-width="60"/>
            </g>
            <g id="stem" stroke="{stem_color}">
                <path d="M215 530V555C215 693.071 326.929 805 465 805H490H515C653.071 805 765 693.071 765 555V530" stroke-width="60" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="370" y1="950" x2="610" y2="950" stroke-width="60" stroke-linecap="round"/>
                <line x1="500" y1="805" x2="500" y2="980" stroke-width="60"/>
            </g>
        </svg>
        """

    @staticmethod
    def switch_icon(theme='Dark', state=False):
        switch_position = '217.5' if state else '72.5'
        # If the theme is 'Light', choose the appropriate colors from LightTheme, otherwise from DarkTheme
        theme_colors = LightTheme if theme == 'Light' else DarkTheme
        # Determine switch color based on theme and state
        track_color = (
            theme_colors.secondary_color if state else
            theme_colors.secondary_color
        )
        # Determine switch color based on theme and state
        switch_color = (
            theme_colors.accent_color if state else
            theme_colors.primary_color
        )

        # Generate SVG code using the determined colors
        return f"""
        <svg width="290" height="145" viewBox="0 0 290 145" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect y="24" width="290" height="96.6667" rx="48.3333" fill="{track_color}"/>
            <circle cx="{switch_position}" cy="72.5" r="72.5" fill="{switch_color}"/>
        </svg>
        """


    @staticmethod
    def frame_icon(theme='Dark'):
        # Determine frame color based on theme
        color = LightTheme.underline_color if theme == 'Light' else DarkTheme.underline_color

        # Generate SVG code using the determined colors
        return f"""
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="32" cy="32" r="31.5" stroke="{color}"/>
        </svg>
        """

    @staticmethod
    def frameError_icon(theme='Dark'):
        # Determine the color based on the specified theme
        color = LightTheme.off_color if theme == 'Light' else DarkTheme.off_color

        # Generate SVG code using the determined color
        return f"""
        <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M9.81079 10.457L54.06 54.7062" stroke="{color}" stroke-width="3"/>
            <circle cx="32" cy="32" r="30.5" stroke="{color}" stroke-width="3"/>
        </svg>
        """

    @staticmethod
    def about_icon(theme='Dark'):
        # Determine the color based on the specified theme
        color = LightTheme.primary_color if theme == 'Light' else DarkTheme.primary_color

        # Generate SVG code using the determined color
        return f"""
        <svg width="160" height="352" viewBox="0 0 160 352" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="16" y="78" width="128" height="258" rx="64" stroke="{color}" stroke-width="32"/>
            <path d="M0 150H68" stroke="{color}" stroke-width="24"/>
            <path d="M0 194H68" stroke="{color}" stroke-width="24"/>
            <line x1="36" y1="16" x2="124" y2="16" stroke="{color}" stroke-width="32" stroke-linecap="round"/>
        </svg>
        """

    @staticmethod
    def exit_icon(theme='Dark'):
        # Determine the color based on the specified theme
        color = LightTheme.primary_color if theme == 'Light' else DarkTheme.primary_color

        # Generate SVG code using the determined color
        return f"""
        <svg width="292" height="295" viewBox="0 0 292 295" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M225 70V65C225 37.3858 202.614 15 175 15H65C37.3858 15 15 37.3858 15 65V230C15 257.614 37.3858 280 65 280H125H175C202.614 280 225 257.614 225 230V225" stroke="{color}" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M5 93H69" stroke="{color}" stroke-width="24"/>
            <path d="M5 137H69" stroke="{color}" stroke-width="24"/>
            <path d="M277 141.34C283.667 145.189 283.667 154.811 277 158.66L187 210.622C180.333 214.471 172 209.66 172 201.962L172 98.0385C172 90.3405 180.333 85.5292 187 89.3782L277 141.34Z" fill="{color}"/>
        </svg>
        """

    @staticmethod
    def settings_icon(theme='Dark'):
        # Determine the color based on the specified theme
        color = LightTheme.primary_color if theme == 'Light' else DarkTheme.primary_color

        # Generate SVG code using the determined color
        return f"""
        <svg width="270" height="270" viewBox="0 0 270 270" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M130.058 0C120.085 0 112 8.08505 112 18.0585C112 26.5144 106.061 33.6821 98.1437 36.6507C95.6711 37.5777 93.2428 38.5953 90.8627 39.6995C83.3803 43.1707 74.3336 42.3336 68.5011 36.501C61.6418 29.6417 50.5206 29.6417 43.6613 36.501L36.6454 43.5169C29.8059 50.3564 29.8059 61.4455 36.6454 68.285C42.4726 74.1122 43.2987 83.1549 39.8116 90.6217C38.6642 93.0788 37.609 95.5876 36.6507 98.1437C33.6821 106.061 26.5144 112 18.0585 112C8.08505 112 0 120.085 0 130.058V139.143C0 149.005 7.99489 157 17.8571 157C26.2844 157 33.4107 162.96 36.2902 170.88C37.3602 173.823 38.5581 176.705 39.8771 179.518C43.4479 187.135 42.6271 196.373 36.6786 202.321C29.7213 209.279 29.7212 220.559 36.6786 227.516L43.139 233.977C50.1872 241.025 61.6147 241.025 68.663 233.977C74.6351 228.005 83.8898 227.133 91.5779 230.629C93.7287 231.607 95.9183 232.515 98.1437 233.349C106.061 236.318 112 243.486 112 251.942C112 261.915 120.085 270 130.058 270H139.143C149.005 270 157 262.005 157 252.143C157 243.716 162.96 236.589 170.88 233.71C173.559 232.736 176.187 231.656 178.759 230.475C186.61 226.871 196.089 227.728 202.198 233.837C209.368 241.007 220.993 241.007 228.163 233.837L233.981 228.019C241.171 220.829 241.171 209.171 233.981 201.981C227.867 195.867 226.998 186.385 230.585 178.518C231.723 176.023 232.766 173.475 233.71 170.88C236.589 162.96 243.716 157 252.143 157C262.005 157 270 149.005 270 139.143V130.058C270 120.085 261.915 112 251.942 112C243.486 112 236.318 106.061 233.349 98.1437C232.521 95.9343 231.62 93.7602 230.65 91.6244C227.145 83.9074 228.02 74.6201 234.013 68.6269C241.086 61.5537 241.086 50.0859 234.013 43.0127L227.642 36.6423C220.66 29.6602 209.34 29.6602 202.358 36.6423C196.388 42.6119 187.117 43.4351 179.472 39.8553C176.673 38.5449 173.807 37.3543 170.88 36.2902C162.96 33.4107 157 26.2844 157 17.8571C157 7.9949 149.005 0 139.143 0H130.058ZM135 210C176.421 210 210 176.421 210 135C210 93.5786 176.421 60 135 60C113.274 60 93.7057 69.2379 80.0086 84H101V108H65.0069C62.575 114.3 60.9692 121.011 60.3224 128H101V152H61.9349C69.6363 185.232 99.4257 210 135 210Z" fill="{color}"/>
        </svg>
        """
