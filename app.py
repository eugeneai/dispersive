#!/usr/bin/python
# encoding: utf-8

import sys
from PyQt4 import QtGui
from ui.main_win import Ui_AppWindow

class AppWindow(QtGui.QMainWindow):
    pass



if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    
    widget = QtGui.QWidget()
    widget.resize(250, 150)
    widget.setWindowTitle('simple')
    widget.show()

    sys.exit(app.exec_())
