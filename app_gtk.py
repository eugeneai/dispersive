#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk, sys
import models.component as mdl
import os
import subprocess as spp

from matplotlib.widgets import Cursor
from matplotlib.figure import Figure
from numpy import arange, sin, pi


# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTK, NavigationToolbar2GTKAgg
from matplotlib.backends.backend_gtk import FileChooserDialog
import matplotlib

CHANNEL_NO=4096
CALIBR_ZERO=90
CALIBR_KEV=20./(CHANNEL_NO-CALIBR_ZERO)


DEBUG = 5
if DEBUG>2:
    LOAD_FILE="/home/eugeneai/Development/codes/dispersive/test.rtx"

if os.name!='nt':
    #EPS_CMD="evince" 
    EPS_CMD="xdg-open" # YYY Needs to be corrected
else:
    #EPS_CMD="C:\\Program Files\\Ghostgum\\gsview\\gsview32.exe"
    EPS_CMD="start"


FILE_PATTERNS = {
    "*.rtx": "Spectra file, many spectra",
    "*.spx": "Single spectra file",
    }

class TXRFNavigationToolbar(NavigationToolbar2GTKAgg):
    toolitems = (
        ('Home', 'Reset original view', 'home.png', 'home', 'gtk-zoom-fit'),
        ('Back', 'Back to  previous view','back.png', 'back', 'gtk-go-back'),
        ('Forward', 'Forward to next view','forward.png', 'forward', 'gtk-go-forward'),
        ('Pan', 'Pan axes with left mouse, zoom with right', 'move.png', 'pan', 'gtk-index'),
        ('Zoom', 'Zoom to rectangle','zoom_to_rect.png', 'zoom', 'gtk-zoom-in'),
        # (None, None, None, None, None),
        ('Subplots', 'Configure subplots','subplots.png', 'configure_subplots', 'gtk-preferences'),
        ('Save', 'Save the figure','filesave.png', 'save_figure', 'gtk-convert'),
        )
    
    def __init__(self, canvas, window, main_ui, subplots=False):
        self.win = window
        self.main_ui = main_ui
        self.toolbar = main_ui.toolbar
        self.statusbar = main_ui.statusbar
        self.subplots = subplots
        #gtk.Toolbar.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self._idle_draw_id = 0
        window.connect('destroy', self.on_destroy)

    def on_destroy(self, widget, data=None):
        for w in self._widgets:
            self.toolbar.remove(w)
        return True

    def _init_toolbar(self):
        self.set_style(gtk.TOOLBAR_ICONS)
        self._init_toolbar2_4()

    def insert(self, widget, pos=-1):
        try:
            self._widgets
        except AttributeError:
            self._widgets = []
        self.toolbar.insert(widget, pos)
        self._widgets.append(widget)

    def _init_toolbar2_4(self):
        basedir = os.path.join(matplotlib.rcParams['datapath'],'images')
        self.tooltips = gtk.Tooltips()

        
        toolitem = gtk.SeparatorToolItem()
        self.insert(toolitem, -1)
        for text, tooltip_text, image_file, callback, stock in self.toolitems:
            if text is None:
                self.insert( gtk.SeparatorToolItem(), -1 )
                continue
            if text=='Subplots' and not self.subplots:
                continue
            if stock is None:
                fname = os.path.join(basedir, image_file)
                image = gtk.Image()
                image.set_from_file(fname)
                tbutton = gtk.ToolButton(image, text)
            else:
                tbutton = gtk.ToolButton(stock)
            self.insert(tbutton, -1)
            tbutton.connect('clicked', getattr(self, callback))
            tbutton.set_tooltip(self.tooltips, tooltip_text, 'Private')

        #toolitem = gtk.SeparatorToolItem()
        #self.insert(toolitem, -1)
        # set_draw() not making separator invisible,
        # bug #143692 fixed Jun 06 2004, will be in GTK+ 2.6
        #toolitem.set_draw(False)
        #toolitem.set_expand(True)

        #toolitem = gtk.ToolItem()
        #self.insert(toolitem, -1)
        #self.message = gtk.Label()
        #toolitem.add(self.message)

        self.toolbar.show_all()

    def draw_rubberband(self, event, x0, y0, x1, y1):
        'adapted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189744'
        drawable = self.canvas.window
        if drawable is None:
            return

        gc = drawable.new_gc()
        gc.function = gtk.gdk.INVERT
        gc.foreground = gtk.gdk.color_parse("#FFFFFFFFFFFF")
        height = self.canvas.figure.bbox.height
        y1 = height - y1
        y0 = height - y0

        w = abs(x1 - x0)
        h = abs(y1 - y0)

        rect = [int(val)for val in min(x0,x1), min(y0, y1), w, h]
        drawable.draw_rectangle(gc, False, *rect)
        try:
            rect_p = self._imageBack
            drawable.draw_rectangle(gc, False, *rect_p)
        except AttributeError:
            pass
        self._imageBack = rect
        return

    def set_message(self, s):
        pass 

    def get_filechooser(self):
        return FileChooserDialog(
            title='Save the figure',
            parent=self.main_ui.window,
            filetypes=self.canvas.get_supported_filetypes(),
            default_filetype=self.canvas.get_default_filetype())
class Ui:
    pass
  
class TXRFApplication(object):

    # Signal connection is linked in the glade XML file
    def main_window_delete_event_cb(self, widget, data=None):
        gtk.main_quit()
    m_quit_activate_cb=main_window_delete_event_cb

    # Signal connection is linked in the glade XML file
    def on_button1_clicked(self, widget, data=None):
        text = self.entry1.get_text()
        self.label1.set_text(text)
     
    def __init__(self):
        # Create a new Builder object
        builder = gtk.Builder()
        # Add the UI objects (widgets) from the Glade XML file
        builder.add_from_file("ui/main_win_gtk.glade")
        #builder.add_from_file("builder.ui")
        
        # Get objects (widgets) from the Builder
        self.ui=Ui()
        self.ui.window = builder.get_object("main_window")
        #self.exp_area = builder.get_object("exp_area")
        self.ui.main_vbox = builder.get_object("main_vbox")
        self.ui.statusbar = builder.get_object("statusbar")
        self.ui.toolbar = builder.get_object("toolbar")
        #self.entry1 = builder.get_object("entry1");
        #self.label1 = builder.get_object("label1");
        # Connect all singals to methods in this class
        builder.connect_signals(self)
        # Show the window and all its children
        self.ui.window.show_all()
        self.ui.active_widget=None
        self.spectra = None
        self.default_view()

        # Shoul be the last one, it seems
        if DEBUG>2:
            self.on_file_open(self, LOAD_FILE)

    def default_view(self):
        self.insert_plotting_area(self.ui)

    def on_file_new(self, widget, data=None):
        print "Created"
        # check wether data has been saved. YYY
        self.spectra = None
        self.insert_plotting_area(self.ui)

    def on_file_open(self, widget, filename=None):
        if filename is None:
            filename = self.get_open_filename()
        if filename:
            self.spectra=mdl.Spectra(filename)
            self.default_action()
            
    def get_open_filename(self):
        
        filename = None
        chooser = gtk.FileChooserDialog("Open Project...", self.ui.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, 
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

        ffilter = gtk.FileFilter()
        for pattern, name in FILE_PATTERNS.iteritems():
            ffilter.add_pattern(pattern)

        chooser.set_filter(ffilter)
        #print gtk.FileChooserDialog.__doc__
        
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            filename = chooser.get_filename()
        chooser.destroy()
        print "File:", filename
        return filename
    
    def error_message(self, message):
    
        # log to terminal window
        # print message
        
        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        
        dialog.run()
        dialog.destroy()

    def default_action(self):
        self.spectra.get_spectra()
        self.spectra.set_scale(mdl.Scale(zero=CALIBR_ZERO, scale=CALIBR_KEV))
        self.default_view()
        #self.spectra.r_plot()
        #print "AAA:", EPS_CMD
        #sp=spp.Popen([EPS_CMD, 'plot.eps'])
        #sp.communicate()

    def remove_active_widget(self):
        if self.ui.active_widget is None:
            return
        self.ui.main_vbox.remove(self.ui.active_widget)
        self.ui.active_widget.destroy()
        self.ui.active_widget=None

    def insert_plotting_area(self, ui):
        local=Ui()
        self.remove_active_widget()

        win = gtk.Frame()
        win.set_shadow_type(gtk.SHADOW_NONE)
        
        vbox = gtk.VBox()
        win.add(vbox)
        
        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)
        #print ax.grid

        if not self.spectra or not self.spectra.spectra:
            t = arange(0.0,3.0,0.01)
            s = sin(2*pi*t)
            ax.plot(t,s)
        else:
            sp_len = len(self.spectra.spectra[0])
            X = arange(sp_len)
            kevs = self.spectra.scale.to_keV(X)
            for i,spectrum in enumerate(self.spectra.spectra):
                ax.plot(kevs,spectrum, label='plot_%i' % (i+1))
            ax.set_ylabel('Counts')
            ax.set_xlabel('k$e$V')
            ax.set_title('Spectra plot')
            ax.set_xlim(kevs[0],kevs[-1])
            # ax.set_yscale('log')
            ax.ticklabel_format(style='sci', scilimits=(3,0), axis='y')
            ax.grid(b=True, aa=False, alpha=0.3)
            # ax.legend(loc=0) # best location.
            ax.minorticks_on()

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True)
        toolbar_ = TXRFNavigationToolbar(canvas, win, self.ui)
        # vbox.pack_start(toolbar, False, False)
        ui.main_vbox.pack_start(win,True, True)
        win.show_all()

        sb=ui.statusbar
        local.msg_id=None
        local.ctx_id=sb.get_context_id("plotting")

        def onclick(event): # I like closures. It is cool!
            if local.msg_id is not None:
                sb.remove(local.ctx_id, local.msg_id)
            if event.xdata and event.ydata:
                s='button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
                    event.button, event.x, event.y, event.xdata, event.ydata)
            else:
                s=' '.join([str(x) for x in [event.button, event.x, event.y, event.xdata, event.ydata]])
                
            print s
            local.msg_id=sb.push(local.ctx_id, s)

        cid = canvas.mpl_connect('button_press_event', onclick)
        #cursor = Cursor(ax, useblit=False, color='red', linewidth=1 )

        
        ui.active_widget=win
        


def main():
    gtk.main()
    return
    
if __name__ == "__main__":
    TXRFApplication()
    gtk.main()
