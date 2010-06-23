# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spectra.ui'
#
# Created: Thu Jun 24 01:04:01 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Frame(object):
    def setupUi(self, Frame):
        Frame.setObjectName("Frame")
        Frame.resize(459, 386)
        Frame.setFrameShape(QtGui.QFrame.StyledPanel)
        Frame.setFrameShadow(QtGui.QFrame.Plain)
        Frame.setLineWidth(0)
        self.horizontalLayout = QtGui.QHBoxLayout(Frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtGui.QSplitter(Frame)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.treeView = QtGui.QTreeView(self.splitter)
        self.treeView.setObjectName("treeView")
        self.plot = QtGui.QLabel(self.splitter)
        self.plot.setFrameShape(QtGui.QFrame.Panel)
        self.plot.setText("")
        self.plot.setObjectName("plot")
        self.horizontalLayout.addWidget(self.splitter)

        self.retranslateUi(Frame)
        QtCore.QMetaObject.connectSlotsByName(Frame)

    def retranslateUi(self, Frame):
        Frame.setWindowTitle(QtGui.QApplication.translate("Frame", "Frame", None, QtGui.QApplication.UnicodeUTF8))

