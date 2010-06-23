# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_win.ui'
#
# Created: Wed Jun 23 22:23:39 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_AppWindow(object):
    def setupUi(self, AppWindow):
        AppWindow.setObjectName("AppWindow")
        AppWindow.resize(605, 541)
        self.centralwidget = QtGui.QWidget(AppWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        AppWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(AppWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 605, 27))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuAction = QtGui.QMenu(self.menubar)
        self.menuAction.setObjectName("menuAction")
        self.menuMacro = QtGui.QMenu(self.menubar)
        self.menuMacro.setObjectName("menuMacro")
        AppWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(AppWindow)
        self.statusbar.setObjectName("statusbar")
        AppWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(AppWindow)
        self.toolBar.setObjectName("toolBar")
        AppWindow.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        self.actionOpen = QtGui.QAction(AppWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.menuFile.addAction(self.actionOpen)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuAction.menuAction())
        self.menubar.addAction(self.menuMacro.menuAction())

        self.retranslateUi(AppWindow)
        QtCore.QMetaObject.connectSlotsByName(AppWindow)

    def retranslateUi(self, AppWindow):
        AppWindow.setWindowTitle(QtGui.QApplication.translate("AppWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("AppWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("AppWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("AppWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAction.setTitle(QtGui.QApplication.translate("AppWindow", "Action", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMacro.setTitle(QtGui.QApplication.translate("AppWindow", "Macro", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("AppWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen.setText(QtGui.QApplication.translate("AppWindow", "Open", None, QtGui.QApplication.UnicodeUTF8))

