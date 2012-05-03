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
                        c=c[0]
                        self.ui.pt.attach(el, c, c+1, r,r+1)
                        break
                else:
                    if l[0]>=j and l[1]<=j:
                        r, c = r
                        c=c[j-l[0]]
                        self.ui.pt.attach(el, c, c+1, r,r+1)
                        break
                el.show()
            self.set_size_request(600,400)




if __name__=="__main__":
    testw = gtk.Window(gtk.WINDOW_TOPLEVEL)
    testw.connect("destroy", gtk.main_quit)
    pt=PTWidget()
    testw.add(pt)
    pt.show()
    testw.show()
    gtk.main()
