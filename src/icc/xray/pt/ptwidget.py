import pygtk
pygtk.require('2.0')
import gtk, gobject
import sys

ROWS={
    ((1,),           (1, (1,))),
    ((2,),           (1, (18,))),
    ((3,4),         (2, (1,2))),
    ((5,10),       (2,(13,18))),
    ((11,12),     (3, (1,2))),
    ((13,18),     (3, (13,18))),
    ((19,36),     (4, (1,18))),
    ((37,54),     (5, (1,18))),
    ((55,56),     (6, (1,2))),
    ((72,86),     (6, (4,18))),
    ((87,88),     (7, (1,2))),
    ((104,118), (7, (4,18))),
    ((57,71),     (9, (4,18))),
    ((89,103),     (10, (4,18))),
}

LA = (6,3)
AC = (7,3)

class UI:
    pass

class PTWidget(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        self.ui=UI()
        self.ui.pt=gtk.Table(rows=10, columns=18)




if __name__=="__main__":
    testw = gtk.Window(gtk.WINDOW_TOPLEVEL)
    testw.connect("destroy", gtk.main_quit)
    pt=PTWidget()
    testw.add(pt)
    testw.show()
    gtk.main()
