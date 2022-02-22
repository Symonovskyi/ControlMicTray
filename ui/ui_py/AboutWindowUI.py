from PyQt6.QtWidgets import QLabel, QPushButton
from PyQt6.QtCore import Qt, QSize, QRect, QCoreApplication, QMetaObject
from PyQt6.QtGui import QPixmap


class Ui_AboutWindow(object):
    def setupUi(self, AboutWindow):
        # Window settings.
        AboutWindow.setObjectName("AboutWindow")
        AboutWindow.setWindowModality(Qt.WindowModality.WindowModal)
        AboutWindow.resize(355, 290)
        AboutWindow.setMinimumSize(QSize(355, 290))
        AboutWindow.setMaximumSize(QSize(355, 290))
        AboutWindow.setStyleSheet("QWidget {\n"
"    color: #BECBD1;\n"
"    background-color: #273238;\n"
"    border: 0;\n"
"    font-size:14px;\n"
"    font-family: Arial, sans-serif;\n"
"}")
        # The elements of window.
        self.WebSiteLabel = QLabel(AboutWindow)
        self.WebSiteLabel.setGeometry(QRect(20, 70, 100, 16))
        self.WebSiteLabel.setObjectName("WebSiteLabel")

        self.ProgramVersionLabel = QLabel(AboutWindow)
        self.ProgramVersionLabel.setGeometry(QRect(20, 30, 100, 16))
        self.ProgramVersionLabel.setObjectName("ProgramVersionLabel")

        self.EmailLabel = QLabel(AboutWindow)
        self.EmailLabel.setGeometry(QRect(20, 110, 100, 16))
        self.EmailLabel.setObjectName("EmailLabel")

        self.ProgramVersion = QLabel(AboutWindow)
        self.ProgramVersion.setGeometry(QRect(140, 30, 130, 16))
        self.ProgramVersion.setObjectName("ProgramVersion")

        self.Logo = QLabel(AboutWindow)
        self.Logo.setGeometry(QRect(271, 20, 64, 64))
        self.Logo.setStyleSheet("")
        self.Logo.setText("")
        self.Logo.setPixmap(QPixmap("ui/ui_py\\../resources/Frame.svg"))
        self.Logo.setScaledContents(True)
        self.Logo.setObjectName("Logo")

        self.UrlPrivacyPolicy = QPushButton(AboutWindow)
        self.UrlPrivacyPolicy.setGeometry(QRect(53, 184, 250, 30))
        self.UrlPrivacyPolicy.setStyleSheet("QPushButton {\n"
"    color: #7D8A90;\n"
"    border-bottom: 1px solid #1F2A30;\n"
"}\n"
"QPushButton::hover {\n"
"    color: #CEDCDF;\n"
"    border-bottom: 1px solid #04BED5;\n"
"}")
        self.UrlPrivacyPolicy.setObjectName("UrlPrivacyPolicy")

        self.Copyright = QLabel(AboutWindow)
        self.Copyright.setGeometry(QRect(78, 224, 200, 40))
        self.Copyright.setStyleSheet("QLabel{\n"
"    color: #7D8A90;\n"
"    font-size:10px;\n"
"}")
        self.Copyright.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Copyright.setObjectName("Copyright")

        self.WebSite = QPushButton(AboutWindow)
        self.WebSite.setGeometry(QRect(140, 70, 130, 16))
        self.WebSite.setStyleSheet("QPushButton {\n"
"    color: #127D91;\n"
"    text-align: left;\n"
"}\n"
"QPushButton::hover {\n"
"    color: #04BED5;\n"
"}")
        self.WebSite.setObjectName("WebSite")

        self.Email = QPushButton(AboutWindow)
        self.Email.setGeometry(QRect(140, 110, 190, 16))
        self.Email.setStyleSheet("QPushButton {\n"
"    color: #127D91;\n"
"    text-align: left;\n"
"}\n"
"QPushButton::hover {\n"
"    color: #04BED5;\n"
"}")
        self.Email.setObjectName("Email")
        
        self.LogoFrame = QLabel(AboutWindow)
        self.LogoFrame.setGeometry(QRect(277, 26, 52, 52))
        self.LogoFrame.setStyleSheet("QLabel{\n"
"    background-color: rgba(0, 0, 0, 0);\n"
"}")
        self.LogoFrame.setText("")
        self.LogoFrame.setPixmap(QPixmap("ui/ui_py\\../resources/Microphone.svg"))
        self.LogoFrame.setScaledContents(True)
        self.LogoFrame.setObjectName("LogoFrame")

        self.retranslateUi(AboutWindow)
        QMetaObject.connectSlotsByName(AboutWindow)

    def retranslateUi(self, AboutWindow):
        _translate = QCoreApplication.translate
        AboutWindow.setWindowTitle(_translate("AboutWindow", "О программе"))
        self.WebSiteLabel.setText(_translate("AboutWindow", "Веб-сайт"))
        self.ProgramVersionLabel.setText(_translate("AboutWindow", "Версия"))
        self.EmailLabel.setText(_translate("AboutWindow", "Поддержка"))
        self.ProgramVersion.setText(_translate("AboutWindow", "2022.02.12"))
        self.UrlPrivacyPolicy.setText(_translate("AboutWindow", "Политика конфиденциальности"))
        self.Copyright.setText(_translate("AboutWindow", "Copyright © 2022\n"
"Simonovskiy & Lastivka\n"
"All rights reserved"))
        self.WebSite.setText(_translate("AboutWindow", "controlmictray.pp.ua"))
        self.Email.setText(_translate("AboutWindow", "info@controlmictray.pp.ua "))
