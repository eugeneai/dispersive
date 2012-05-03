import pygtk
pygtk.require('2.0')
import gtk, gobject
import sys

ROWS=[
    ((1,),           (1, 1)),
    ((2,),           (1, 18)),
    ((3,4),         (2, 1)),
    ((5,10),       (2, 13)),
    ((11,12),     (3, 1)),
    ((13,18),     (3, 13)),
    ((19,36),     (4, 1)),
    ((37,54),     (5, 1)),
    ((55,56),     (6, 1)),
    ((72,86),     (6, 4)),
    ((87,88),     (7, 1)),
    ((104,118), (7, 4)),
    ((57,71),     (9, 4)),
    ((89,103),   (10, 4)),
]

LA = (6,3)
AC = (7,3)

class UI:
    pass

class PTWidget(gtk.VBox):
    def __init__(self):
        gtk.VBox.__init__(self)
        b=gtk.Button("asd")
        self.ui=UI()
        self.ui.pt=gtk.Table(rows=10, columns=18, homogeneous=True)
        self.pack_start(self.ui.pt, expand=True, fill=True)
        self.ui.elements=[]
        for i in range(118):
            j=i+1
            el=gtk.Button(label=str(j))
            self.ui.elements.append(el)
            for l, r in ROWS:
                if len(l) == 1:
                    if l[0]==j:
                        r,c = r
                        self.ui.pt.attach(el, c-1, c, r-1,r)
                        break
                else:
                    if l[0]<=j and j<=l[1]:
                        r, c = r
                        c=c+j-l[0]
                        self.ui.pt.attach(el, c-1, c, r-1,r)
                        break
                el.show()
            self.set_size_request(500,260)

DATA=[]

def import_data(filename):
    """Import data from a CSV file """

def test():
    testw = gtk.Window(gtk.WINDOW_TOPLEVEL)
    testw.connect("destroy", gtk.main_quit)
    pt=PTWidget()
    testw.add(pt)
    testw.show_all()
    gtk.main()

if __name__=="__main__":
    test()

