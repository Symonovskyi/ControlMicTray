class GlobalStyles:
	border1 = "1px solid"
	border2 = "0"
	font_family = "Roboto, Arial, sans-serif"
	font_size1 = "14px"
	font_size2 = "10px"
	text_align1 = "left"
	border_radius1 = "3px"
	border_radius2 = "0"
	border_radius3 = "5px"

	# Dark theme
	dark_color1 = "#7D8A90"  # Кнопки в трее, обновления, политика, копирайт.
	dark_color2 = "#1F2A30"  # Фон меню в трее.
	dark_color3 = "#444F55"
	dark_color4 = "#273238"  # Фон общий.
	dark_color5 = "#BECBD1"  # Текст.
	dark_color6 = "#04BED5"
	dark_color7 = "#CEDCDF"  # Текст кнопки активный.
	dark_color8 = "#127D91"
	dark_color9 = "rgba(0, 0, 0, 0)"

	# White theme
	white_color1 = "#7D8A90"  # Кнопки в трее, обновления, политика, копирайт.
	white_color2 = "#FFFFFF"  # Фон выпадающем меню и в трее.
	white_color3 = "#444F55"  # Подчеркивания / бордеры.
	white_color4 = "#FFFFFF"  # Фон.
	white_color5 = "#1F2A30"  # Текст.
	white_color6 = "#04BED5"  # Текст hover и border.
	white_color7 = "#1F2A30"  # Текст кнопки активный.
	white_color8 = "#127D91"  # Текст ссылок.
	white_color9 = "rgba(0, 0, 0, 0)"

class TrayIconStyles(GlobalStyles):
	def __init__(self, qinstance):
		self.tray = qinstance

	def dark_theme(self):
		self.tray.menu.setStyleSheet(
			"""QMenu {"""
				f'color: {self.dark_color1};'
				f'background-color: {self.dark_color2};'
				f'border: {self.border1} {self.dark_color3};'
				f'border-radius: {self.border_radius1};'
				f'selection-background-color: {self.dark_color4};'
				f'selection-color: {self.dark_color5};'
			"""}"""
		)

	def white_theme(self):
		self.tray.menu.setStyleSheet(
			"""QMenu {"""
				f'color: {self.white_color1};'
				f'background-color: {self.white_color2};'
				f'border: {self.border1} {self.white_color3};'
				f'border-radius: {self.border_radius1};'
				f'selection-background-color: {self.white_color4};'
				f'selection-color: {self.white_color5};'
			"""}"""
		)


class SettingsWindowStyles(GlobalStyles):
	def __init__(self, qinstance):
		self.settings_win_qwidget = qinstance
		self.settings_win = self.settings_win_qwidget.settings_UI

	def dark_theme(self):
		self.settings_win_qwidget.setStyleSheet(
			"""QWidget {"""
				f'color: {self.dark_color5};'
				f'background-color: {self.dark_color4};'
				f'border: {self.border2};'
				f'font-size: {self.font_size1};'
				f'font-family: {self.font_family}'
			"""}"""
		)

		self.settings_win.AlertsType.setStyleSheet(
			"""QComboBox {"""
				f'border-bottom: {self.border1} {self.dark_color3};'
			"""}"""

			"""QComboBox::hover{"""
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""
			
			"""QComboBox QAbstractItemView {"""
				f'background-color: {self.dark_color2};'
				f'border: {self.border1} {self.dark_color6};'
				f'color: {self.dark_color1};'
				f'selection-background-color: {self.dark_color4};'
				f'selection-color: {self.dark_color5};'
				f'border-top-left-radius: {self.border_radius2};'
				f'border-top-right-radius: {self.border_radius2};'
				f'border-bottom-right-radius: {self.border_radius3};'
				f'border-bottom-left-radius: {self.border_radius3};'
			"""}"""
		)

		self.settings_win.HotkeyMic.setStyleSheet(
			"""QLineEdit {"""
				f'border-bottom: {self.border1} {self.dark_color3};'
			"""}"""

			"""QLineEdit::hover{"""
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""
		)

		self.settings_win.HotkeyWalkie.setStyleSheet(
			"""QLineEdit {"""
				f'border-bottom: {self.border1} {self.dark_color3};'
			"""}"""

			"""QLineEdit::hover{"""
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""
		)

		self.settings_win.LanguageCode.setStyleSheet(
			"""QComboBox {"""
				f'border-bottom: {self.border1} {self.dark_color3};'
			"""}"""

			"""QComboBox::hover{"""
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""

			"""QComboBox QAbstractItemView {"""
				f'background-color: {self.dark_color2};'
				f'border: {self.border1} {self.dark_color6};'
				f'color: {self.dark_color1};'
				f'selection-background-color: {self.dark_color4};'
				f'selection-color: {self.dark_color5};'
				f'border-top-left-radius: {self.border_radius2};'
				f'border-top-right-radius: {self.border_radius2};'
				f'border-bottom-right-radius: {self.border_radius3};'
				f'border-bottom-left-radius: {self.border_radius3};'
			"""}"""
		)

		self.settings_win.UrlUpdates.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.dark_color1};'
				f'border-bottom: {self.border1} {self.dark_color2};'
			"""}"""
			
			"""QPushButton::hover {"""
				f'color: {self.dark_color7};'
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""
		)

	def white_theme(self):
		self.settings_win_qwidget.setStyleSheet(
			"""QWidget {"""
				f'color: {self.white_color5};'
				f'background-color: {self.white_color4};'
				f'border: {self.border2};'
				f'font-size: {self.font_size1};'
				f'font-family: {self.font_family}'
			"""}"""
		)

		self.settings_win.AlertsType.setStyleSheet(
			"""QComboBox {"""
				f'border-bottom: {self.border1} {self.white_color3};'
			"""}"""

			"""QComboBox::hover{"""
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""

			"""QComboBox QAbstractItemView {"""
				f'background-color: {self.white_color2};'
				f'border: {self.border1} {self.white_color6};'
				f'color: {self.white_color1};'
				f'selection-background-color: {self.white_color4};'
				f'selection-color: {self.white_color5};'
				f'border-top-left-radius: {self.border_radius2};'
				f'border-top-right-radius: {self.border_radius2};'
				f'border-bottom-right-radius: {self.border_radius3};'
				f'border-bottom-left-radius: {self.border_radius3};'
			"""}"""
		)

		self.settings_win.HotkeyMic.setStyleSheet(
			"""QLineEdit {"""
				f'border-bottom: {self.border1} {self.white_color3};'
			"""}"""

			"""QLineEdit::hover{"""
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""
		)

		self.settings_win.HotkeyWalkie.setStyleSheet(
			"""QLineEdit {"""
				f'border-bottom: {self.border1} {self.white_color3};'
			"""}"""

			"""QLineEdit::hover{"""
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""
		)

		self.settings_win.LanguageCode.setStyleSheet(
			"""QComboBox {"""
				f'border-bottom: {self.border1} {self.white_color3};'
			"""}"""

			"""QComboBox::hover{"""
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""

			"""QComboBox QAbstractItemView {"""
				f'background-color: {self.white_color2};'
				f'border: {self.border1} {self.white_color6};'
				f'color: {self.white_color1};'
				f'selection-background-color: {self.white_color4};'
				f'selection-color: {self.white_color5};'
				f'border-top-left-radius: {self.border_radius2};'
				f'border-top-right-radius: {self.border_radius2};'
				f'border-bottom-right-radius: {self.border_radius3};'
				f'border-bottom-left-radius: {self.border_radius3};'
			"""}"""
		)

		self.settings_win.UrlUpdates.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.white_color1};'
				f'border-bottom: {self.border1} {self.white_color2};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.white_color7};'
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""
		)


class AboutWindowStyles(GlobalStyles):
	def __init__(self, qinstance):
		self.about_win_qwidget = qinstance
		self.about_win = self.about_win_qwidget.about_UI

	def dark_theme(self):
		self.about_win_qwidget.setStyleSheet(
			"""QWidget {"""
				f'color: {self.dark_color5};'
				f'background-color: {self.dark_color4};'
				f'border: {self.border2};'
				f'font-size: {self.font_size1};'
				f'font-family: {self.font_family}'
			"""}"""
		)

		self.about_win.Copyright.setStyleSheet(
			"""QLabel{"""
				f'color: {self.dark_color1};'
				f'font-size: {self.font_size2};'
			"""}"""
		)

		self.about_win.Email.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.dark_color8};'
				f'text-align: {self.text_align1};'
			"""}"""
			
			"""QPushButton::hover {"""
				f'color: {self.dark_color6};'
			"""}"""
		)

		self.about_win.LogoFrame.setStyleSheet(
			"""QLabel{"""
				f'background-color: {self.dark_color9};'
			"""}"""
		)

		self.about_win.UrlPrivacyPolicy.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.dark_color1};'
				f'border-bottom: {self.border1} {self.dark_color2};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.dark_color7};'
				f'border-bottom: {self.border1} {self.dark_color6};'
			"""}"""
		)

		self.about_win.WebSite.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.dark_color8};'
				f'text-align: {self.text_align1};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.dark_color6};'
			"""}"""
		)

	def white_theme(self):
		self.about_win_qwidget.setStyleSheet(
			"""QWidget {"""
				f'color: {self.white_color5};'
				f'background-color: {self.white_color4};'
				f'border: {self.border2};'
				f'font-size: {self.font_size1};'
				f'font-family: {self.font_family}'
			"""}"""
		)

		self.about_win.Copyright.setStyleSheet(
			"""QLabel{"""
				f'color: {self.white_color1};'
				f'font-size: {self.font_size2};'
			"""}"""
		)

		self.about_win.Email.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.white_color8};'
				f'text-align: {self.text_align1};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.white_color6};'
			"""}"""
		)

		self.about_win.LogoFrame.setStyleSheet(
			"""QLabel{"""
				f'background-color: {self.white_color9};'
			"""}"""
		)

		self.about_win.UrlPrivacyPolicy.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.white_color1};'
				f'border-bottom: {self.border1} {self.white_color2};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.white_color7};'
				f'border-bottom: {self.border1} {self.white_color6};'
			"""}"""
		)

		self.about_win.WebSite.setStyleSheet(
			"""QPushButton {"""
				f'color: {self.white_color8};'
				f'text-align: {self.text_align1};'
			"""}"""

			"""QPushButton::hover {"""
				f'color: {self.white_color6};'
			"""}"""
		)
