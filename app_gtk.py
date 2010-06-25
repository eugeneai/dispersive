#!/usr/bin/python
import pygtk
pygtk.require('2.0')
import gtk, sys
import models.component as mdl
import os
import subprocess as spp

from matplotlib.figure import Figure
from numpy import arange, sin, pi

# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
from matplotlib.backends.backend_gtkagg import FigureCanvasGTKAgg as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backends.backend_gtkagg import NavigationToolbar2GTKAgg as NavigationToolbar



DEBUG = 2
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
  
class BuilderExample:

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
        self.window = builder.get_object("main_window")
        #self.exp_area = builder.get_object("exp_area")
        self.vbox = builder.get_object("vbox")
        self.statusbar = builder.get_object("statusbar")
        #self.entry1 = builder.get_object("entry1");
        #self.label1 = builder.get_object("label1");
        # Connect all singals to methods in this class
        builder.connect_signals(self)
        # Show the window and all its children
        self.window.show_all()
        if DEBUG>2:
            self.on_file_open(self, LOAD_FILE)
        self.active_widget=None
        self.spectra = None
        self.default_view()

    def default_view(self):
        self.insert_plotting_area()

    def on_file_new(self, widget, data=None):
        print "Created"
        # check wether data has been saved. YYY
        self.spectra = None
        self.insert_plotting_area()

    def on_file_open(self, widget, filename=None):
        if filename is None:
            filename = self.get_open_filename()
        if filename:
            self.spectra=mdl.Spectra(filename)
            self.default_action()
            
    def get_open_filename(self):
        
        filename = None
        chooser = gtk.FileChooserDialog("Open Project...", self.window,
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
        self.default_view()
        #self.spectra.r_plot()
        #print "AAA:", EPS_CMD
        #sp=spp.Popen([EPS_CMD, 'plot.eps'])
        #sp.communicate()

    def remove_active_widget(self):
        if self.active_widget is None:
            return
        self.vbox.remove(self.active_widget)
        self.active_widget.destroy()
        self.active_widget=None

    def insert_plotting_area(self):
        self.remove_active_widget()

        win = gtk.Frame()
        vbox = gtk.VBox()
        win.add(vbox)
        
        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)

        if not self.spectra or not self.spectra.spectra:
            t = arange(0.0,3.0,0.01)
            s = sin(2*pi*t)
            ax.plot(t,s)
        else:
            X=arange(len(self.spectra.spectra[0]))
            for spectrum in self.spectra.spectra:
                ax.plot(X,spectrum)

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True)
        toolbar = NavigationToolbar(canvas, win)
        vbox.pack_start(toolbar, False, False)
        self.vbox.pack_start(win,True, True)
        win.show_all()
        self.active_widget=win
        


def main():
    gtk.main()
    return
    
if __name__ == "__main__":
    BuilderExample()
    gtk.main()
