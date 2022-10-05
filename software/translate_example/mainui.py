# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui',
# licensing of 'main.ui' applies.
#
# Created: Fri Nov 16 11:28:42 2018
#      by: pyside2-uic  running on PySide2 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mainwinlabel = QtWidgets.QLabel(self.centralwidget)
        self.mainwinlabel.setGeometry(QtCore.QRect(180, 150, 251, 17))
        self.mainwinlabel.setObjectName("mainwinlabel")
        self.testlabel = QtWidgets.QLabel(self.centralwidget)
        self.testlabel.setGeometry(QtCore.QRect(190, 260, 201, 17))
        self.testlabel.setObjectName("testlabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionConfigure = QtWidgets.QAction(MainWindow)
        self.actionConfigure.setObjectName("actionConfigure")
        self.actionChinese = QtWidgets.QAction(MainWindow)
        self.actionChinese.setObjectName("actionChinese")
        self.menuFile.addAction(self.actionConfigure)
        self.menuLanguage.addAction(self.actionChinese)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "MainWindow", None, -1))
        self.mainwinlabel.setText(QtWidgets.QApplication.translate("MainWindow", "This is the main window", None, -1))
        self.testlabel.setText(QtWidgets.QApplication.translate("MainWindow", "Used for test", None, -1))
        self.menuFile.setTitle(QtWidgets.QApplication.translate("MainWindow", "Option", None, -1))
        self.menuLanguage.setTitle(QtWidgets.QApplication.translate("MainWindow", "Language", None, -1))
        self.actionConfigure.setText(QtWidgets.QApplication.translate("MainWindow", "Configure", None, -1))
        self.actionChinese.setText(QtWidgets.QApplication.translate("MainWindow", "Chinese", None, -1))

