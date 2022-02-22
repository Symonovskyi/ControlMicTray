from PyQt6.QtWidgets import (
    QPushButton, QLabel, QCheckBox, QLineEdit, QComboBox)
from PyQt6.QtCore import QSize, QRect, QCoreApplication, QMetaObject


class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        # Window settings.
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(440, 440)
        SettingsWindow.setMinimumSize(QSize(440, 440))
        SettingsWindow.setMaximumSize(QSize(440, 440))
        SettingsWindow.setWindowOpacity(1.0)
        SettingsWindow.setStyleSheet("QWidget {\n"
"    color: #BECBD1;\n"
"    background-color: #273238;\n"
"    border: 0;\n"
"    font-size:14px;\n"
"    font-family: Arial, sans-serif;\n"
"}")

        # The elements of window.
        self.UrlUpdates = QPushButton(SettingsWindow)
        self.UrlUpdates.setGeometry(QRect(120, 377, 200, 30))
        self.UrlUpdates.setStyleSheet("QPushButton {\n"
"    color: #7D8A90;\n"
"    border-bottom: 1px solid #1F2A30;\n"
"}\n"
"QPushButton::hover {\n"
"    color: #CEDCDF;\n"
"    border-bottom: 1px solid #04BED5;\n"
"}")
        self.UrlUpdates.setObjectName("UrlUpdates")

        self.NightThemeLabel = QLabel(SettingsWindow)
        self.NightThemeLabel.setGeometry(QRect(20, 110, 343, 16))
        self.NightThemeLabel.setObjectName("NightThemeLabel")

        self.NightTheme = QCheckBox(SettingsWindow)
        self.NightTheme.setGeometry(QRect(383, 112, 24, 12))
        self.NightTheme.setText("")
        self.NightTheme.setObjectName("NightTheme")

        self.EnableMicLabel = QLabel(SettingsWindow)
        self.EnableMicLabel.setGeometry(QRect(20, 230, 343, 16))
        self.EnableMicLabel.setObjectName("EnableMicLabel")

        self.EnableProgramLabel = QLabel(SettingsWindow)
        self.EnableProgramLabel.setGeometry(QRect(20, 150, 343, 16))
        self.EnableProgramLabel.setObjectName("EnableProgramLabel")

        self.PrivacyStatusLabel = QLabel(SettingsWindow)
        self.PrivacyStatusLabel.setGeometry(QRect(20, 190, 343, 16))
        self.PrivacyStatusLabel.setObjectName("PrivacyStatusLabel")

        self.LanguageCodeLabel = QLabel(SettingsWindow)
        self.LanguageCodeLabel.setGeometry(QRect(20, 30, 143, 16))
        self.LanguageCodeLabel.setObjectName("LanguageCodeLabel")

        self.AlertsTypeLabel = QLabel(SettingsWindow)
        self.AlertsTypeLabel.setGeometry(QRect(20, 70, 143, 16))
        self.AlertsTypeLabel.setObjectName("AlertsTypeLabel")

        self.EnableProgram = QCheckBox(SettingsWindow)
        self.EnableProgram.setGeometry(QRect(383, 152, 24, 12))
        self.EnableProgram.setText("")
        self.EnableProgram.setObjectName("EnableProgram")

        self.PrivacyStatus = QCheckBox(SettingsWindow)
        self.PrivacyStatus.setGeometry(QRect(383, 192, 24, 12))
        self.PrivacyStatus.setText("")
        self.PrivacyStatus.setObjectName("PrivacyStatus")

        self.EnableMic = QCheckBox(SettingsWindow)
        self.EnableMic.setGeometry(QRect(383, 232, 24, 12))
        self.EnableMic.setText("")
        self.EnableMic.setObjectName("EnableMic")

        self.HotkeyWalkieLabel = QLabel(SettingsWindow)
        self.HotkeyWalkieLabel.setGeometry(QRect(20, 310, 143, 16))
        self.HotkeyWalkieLabel.setObjectName("HotkeyWalkieLabel")

        self.HotkeyMicLabel = QLabel(SettingsWindow)
        self.HotkeyMicLabel.setGeometry(QRect(20, 270, 143, 16))
        self.HotkeyMicLabel.setObjectName("HotkeyMicLabel")

        self.HotkeyMic = QLineEdit(SettingsWindow)
        self.HotkeyMic.setGeometry(QRect(175, 267, 240, 21))
        self.HotkeyMic.setStyleSheet("QLineEdit{\n"
"    border-bottom: 1px solid #444F55;\n"
"}\n"
"QLineEdit::hover{\n"
"    border-bottom: 1px solid #04BED5;\n"
"}")
        self.HotkeyMic.setReadOnly(True)
        self.HotkeyMic.setObjectName("HotkeyMic")

#         self.HotkeyMic = QLineEdit(SettingsWindow)
#         self.HotkeyMic.setGeometry(QRect(175, 267, 240, 21))
#         self.HotkeyMic.setStyleSheet("QLineEdit{\n"
# "    border-bottom: 1px solid #444F55;\n"
# "}\n"
# "QLineEdit::hover{\n"
# "    border-bottom: 1px solid #04BED5;\n"
# "}")
#         self.HotkeyMic.setReadOnly(True)
#         self.HotkeyMic.setObjectName("HotkeyMic")

        self.HotkeyWalkie = QLineEdit(SettingsWindow)
        self.HotkeyWalkie.setGeometry(QRect(175, 307, 240, 21))
        self.HotkeyWalkie.setStyleSheet("QLineEdit{\n"
"    border-bottom: 1px solid #444F55;\n"
"}\n"
"QLineEdit::hover{\n"
"    border-bottom: 1px solid #04BED5;\n"
"}")
        self.HotkeyWalkie.setReadOnly(True)
        self.HotkeyWalkie.setObjectName("HotkeyWalkie")

        self.LanguageCode = QComboBox(SettingsWindow)
        self.LanguageCode.setGeometry(QRect(180, 27, 240, 21))
        self.LanguageCode.setStyleSheet("QComboBox {\n"
"    border-bottom: 1px solid #444F55;\n"
"}\n"
"QComboBox::hover{\n"
"    border-bottom: 1px solid #04BED5;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1F2A30;;\n"
"    border: 1px solid #04BED5;\n"
"    color: #7D8A90;\n"
"    selection-background-color: #273238;\n"
"    selection-color: #BECBD1;\n"
"    border-top-left-radius: 0;\n"
"    border-top-right-radius: 0;\n"
"    border-bottom-right-radius: 5px;\n"
"    border-bottom-left-radius: 5px;\n"
"}")
        self.LanguageCode.setObjectName("LanguageCode")
        self.LanguageCode.addItem("")
        self.LanguageCode.addItem("")
        self.LanguageCode.addItem("")
        
        self.AlertsType = QComboBox(SettingsWindow)
        self.AlertsType.setGeometry(QRect(180, 67, 240, 21))
        self.AlertsType.setStyleSheet("QComboBox {\n"
"    border-bottom: 1px solid #444F55;\n"
"}\n"
"QComboBox::hover{\n"
"    border-bottom: 1px solid #04BED5;\n"
"}\n"
"QComboBox QAbstractItemView {\n"
"    background-color: #1F2A30;;\n"
"    border: 1px solid #04BED5;\n"
"    color: #7D8A90;\n"
"    selection-background-color: #273238;\n"
"    selection-color: #BECBD1;\n"
"    border-top-left-radius: 0;\n"
"    border-top-right-radius: 0;\n"
"    border-bottom-right-radius: 5px;\n"
"    border-bottom-left-radius: 5px;\n"
"}")
        self.AlertsType.setObjectName("AlertsType")
        self.AlertsType.addItem("")
        self.AlertsType.addItem("")
        self.AlertsType.addItem("")
        self.AlertsType.addItem("")

        self.retranslateUi(SettingsWindow)
        QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Настройки"))
        self.UrlUpdates.setText(_translate("SettingsWindow", "Проверить обновления"))
        self.NightThemeLabel.setText(_translate("SettingsWindow", "Тёмная тема"))
        self.EnableMicLabel.setText(_translate("SettingsWindow", "Выкл. микрофон при запуске"))
        self.EnableProgramLabel.setText(_translate("SettingsWindow", "Автозапуск с ОС"))
        self.PrivacyStatusLabel.setText(_translate("SettingsWindow", "Конфиденциальность"))
        self.LanguageCodeLabel.setText(_translate("SettingsWindow", "Язык"))
        self.AlertsTypeLabel.setText(_translate("SettingsWindow", "Оповещения"))
        self.HotkeyWalkieLabel.setText(_translate("SettingsWindow", "Рация Вкл./Выкл"))
        self.HotkeyMicLabel.setText(_translate("SettingsWindow", "Микрофон Вкл./Выкл"))
        self.HotkeyMic.setText(_translate("SettingsWindow", "CTRL+SHIFT+/"))
        self.HotkeyWalkie.setText(_translate("SettingsWindow", "SCROLL LOCK"))
        self.LanguageCode.setItemText(0, _translate("SettingsWindow", "Русский"))
        self.LanguageCode.setItemText(1, _translate("SettingsWindow", "Украинська"))
        self.LanguageCode.setItemText(2, _translate("SettingsWindow", "English"))
        self.AlertsType.setItemText(0, _translate("SettingsWindow", "Без оповещений"))
        self.AlertsType.setItemText(1, _translate("SettingsWindow", "Всплывающее окно"))
        self.AlertsType.setItemText(2, _translate("SettingsWindow", "Звук"))
        self.AlertsType.setItemText(3, _translate("SettingsWindow", "Свой звук"))
