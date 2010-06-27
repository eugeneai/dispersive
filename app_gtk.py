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
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar

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

class TXRFNavigationToolbar(NavigationToolbar):
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
            X=arange(len(self.spectra.spectra[0]))
            kevs = self.spectra.scale.to_keV(X)
            for spectrum in self.spectra.spectra:
                ax.plot(kevs,spectrum)

        #axes = fig.add_axes([0.075, 0.25, 0.9, 0.725], axisbg='#FFFFCC')


        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True)
        toolbar = TXRFNavigationToolbar(canvas, win)
        vbox.pack_start(toolbar, False, False)
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
