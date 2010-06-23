#!/usr/bin/python
# encoding: utf-8

import sys
from PyQt4 import QtGui
from ui.main_win import Ui_AppWindow
from ui.spectra import Ui_Frame as Ui_SpectraFrame

class SpectraFrame(QtGui.QFrame):
    def __init__(self, parent=None):
        QtGui.QFrame.__init__(self, parent)
        self.ui=Ui_SpectraFrame()
        self.ui.setupUi(self)

class AppWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui=Ui_AppWindow()
        self.ui.setupUi(self)
        self.ui.main_frame_layout=QtGui.QVBoxLayout(self.ui.main_frame)
        self.ui.main_frame_layout.setMargin(0)
        self.ui.verticalLayout.setMargin(0)
        self.ui.active_frame=None
        self.init_browser()

    def init_browser(self):
        self.change_active('start_spectra')

    def start_spectra(self, parent):
        return SpectraFrame(parent)
        return SpectraFrame(parent)
        return SpectraFrame(parent)

    def change_active(self, frame_name):
        if self.ui.active_frame:
            active_frame = self.ui.active_frame
            self.ui.active_frame=None
            active_frame.hide()
            self.ui.main_frame.removeChild(active_frame)
            active_frame.reparent(None)
            active_frame.deleteLater()
            del active_frame

        method = getattr(self, frame_name)
        frame = method(self.ui.main_frame)
        self.ui.main_frame_layout.addWidget(frame)
        frame.show()
        self.ui.active_frame = frame
        
        
        

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    
    #widget = SpectraFrame()
    widget = AppWindow()
    widget.setWindowTitle('simple')
    widget.show()

    sys.exit(app.exec_())

    
