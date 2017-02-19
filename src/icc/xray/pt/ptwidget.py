from gi.repository import Gtk, GObject, Gdk
import sys
from . import data

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

TABLE={row[0]:row for row in data.TABLE}

PAL_CFK=1
PAL_GROUP=2
PAL_NONE=0

PAL_GRP={
    'nonmetal':'00ee00',
    'noble gas':'66aaff',
    'alkali metal':'ffaa00',
    'alkaline earth metal':'f3f300',
    'metalloid':'55cc88',
    'halogen':'00ddbb',
    'transition metal':'dd9999',
    'metal':'99bbaa',
    'lanthanoid':'ffaa88',
    'actinoid':'ddaacc',
}

class UI:
    pass

class PTWidget(Gtk.VBox):
    def __init__(self, factory=Gtk.Button, palette=PAL_GROUP):
        Gtk.VBox.__init__(self)
        b=Gtk.Button("asd")
        self.ui=UI()
        self.ui.pt=Gtk.Table(rows=10, columns=18, homogeneous=True)
        self.pack_start(self.ui.pt, True, True, 0)
        self.ui.elements=[]
        white=Gdk.color_parse('white')
        black=Gdk.color_parse('black')
        for i in range(118):
            j=i+1
            T=TABLE[j]
            el=factory(label=T[1])
            self.ui.elements.append(el)
            if palette > PAL_NONE:
                if palette==PAL_CFK:
                    try:
                        color=Gdk.color_parse("#"+T[4])
                    except ValueError:
                        color = Gtk.gdk.Color("#eee")
                elif palette==PAL_GROUP:
                    grp=T[-2]
                    color=Gdk.color_parse("#"+PAL_GRP.get(grp, 'eee'))
                if color != None:
                    col =color.red_float,color.green_float,color.blue_float
                    ccol=[1.-_c for _c in col]
                    compcolor=Gdk.Color(*ccol)

                    dcol = [_c*70/100 for _c in col]
                    darkcolor=Gdk.Color(*dcol)

                    bcol = [min(1., _c*100/70) for _c in col]
                    brightcolor=Gdk.Color(*bcol)

                    el.modify_bg(Gtk.StateType.NORMAL, color)
                    #el.modify_bg(Gtk.StateType.ACTIVE, darkcolor)
                    el.modify_bg(Gtk.StateType.ACTIVE, black)
                    el.modify_bg(Gtk.StateType.PRELIGHT, brightcolor)
                    #el.modify_bg(Gtk.StateType.PRELIGHT, compcolor)
                    el.modify_bg(Gtk.StateType.SELECTED, color)

                    #style = el.get_style().copy()
                    #print ">>>>>>>>>>>>>", style
                    #style.bg[Gtk.StateType.NORMAL] = color
                    #style.bg[Gtk.StateType.ACTIVE] = black
                    #style.bg[Gtk.StateType.PRELIGHT] = brightcolor
                    #style.bg[Gtk.StateType.SELECTED] = color
                       #set the button's style to the one you created
                    #el.set_style(style)

                    lab=el.get_child()
                    lab.modify_fg(Gtk.StateType.ACTIVE, white)
                    lab.modify_fg(Gtk.StateType.NORMAL, black)


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
            self.set_size_request(500,200)

#DATA=[]

class PTToggleWidget(PTWidget):
    __gsignals__ = {
        'toggled': (
            GObject.SIGNAL_RUN_LAST,
            GObject.TYPE_NONE,
            (GObject.TYPE_INT, GObject.TYPE_STRING, GObject.TYPE_PYOBJECT)
            # Atomic number, Symbol, and the button itself
        ),
    }
    def __init__(self, factory=Gtk.ToggleButton, palette=PAL_GROUP):
        PTWidget.__init__(self, factory=factory, palette=palette)
        self.ui.eldict={}
        for i, el in enumerate(self.ui.elements):
            Z=i+1
            T=TABLE[Z]
            self.ui.eldict[Z]=el
            self.ui.eldict[T[1]]=el
            self.ui.eldict[el]=Z
            el.connect("toggled", self.on_toggled)

    def select(self, elements, active=True, only=False):
        """ Select or unselect an element denoted by
            their list of Zs or symbols."""

        if elements == None:
            return []

        if len(elements)==0:
            for e in self.ui.elements:
                e.set_active(not active)
            return []

        bad=[]
        good=set()
        for e in elements:
            el=self.ui.eldict.get(e, None)
            if el==None:
                bad.append(e)
            else:
                el.set_active(active)
                good.add(el)
        if only:
            for el in self.ui.elements:
                if el in good:
                    continue
                el.set_active(not active)

        return bad

    def selected(self, symbols=False):
        """Return a set of the selected elements as
        set of atom numbers or as set of symbols"""
        selected=[]
        for el in self.ui.elements:
            if el.get_active():
                Z=self.ui.eldict[el]
                if symbols:
                    Z=TABLE[Z][1]
                selected.append(Z)

        return selected

    def on_toggled(self, button):
        #print button, button.get_active()
        Z=self.ui.eldict[button]
        self.emit('toggled', Z, TABLE[Z][1], button)

GObject.type_register(PTToggleWidget)




def import_data(filename, module_name):
    """Import data from a CSV file """
    import csv
    o=open(module_name, "w")
    i=open(filename)
    o.write("# Generated automatically, do not edit.\n\n")
    o.write("TABLE=(\n")
    def _c(s):
        try:
            s=int(s)
            return s
        except ValueError:
            pass
        try:
            s=float(s)
            return s
        except ValueError:
            pass
        return s.strip()

    for row in csv.reader(i):
        nrow = [_c(c) for c in row]
        N = row[0]
        oxi=nrow[12]
        try:
            oxi=oxi.split(',')
            oxi=[_c(x.strip()) for x in oxi]
        except AttributeError:
            oxi=[oxi]
        if oxi==['']:
            oxi=[]
        nrow[12]=oxi
        o.write("(")
        nrow[4]=row[4] # color should not be converted
        for c in nrow:
            o.write(repr(c))
            o.write(',')
        o.write(")")
        o.write(',')
        o.write('\n')
    o.write(")\n")
    o.close()
    i.close()

def test():
    def action(ptw, Z, N, b):
        print("Toggled:", ptw, Z, N, b, b.get_active())
    testw = Gtk.Window(Gtk.WINDOW_TOPLEVEL)
    testw.connect("destroy", Gtk.main_quit)
    pt=PTToggleWidget()
    pt.connect('toggled', action)
    testw.add(pt)
    testw.show_all()
    pt.select(['Zn', 'Zr', 'Y'], active=True)
    Gtk.main()
    print(pt.selected(symbols=True))

if __name__=="__main__":
    #import_data("/home/eugeneai/Development/codes/dispersive/data/pt-data1.csv",
    #    "data_.py")
    test()
