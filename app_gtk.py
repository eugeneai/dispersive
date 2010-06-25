import pygtk
pygtk.require('2.0')
import gtk, sys
import models.component as mdl
import os
import subprocess as spp

if os.name!='nt':
    EPS_CMD="evince plot.eps &" # YYY Needs to be corrected
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
        #self.entry1 = builder.get_object("entry1");
        #self.label1 = builder.get_object("label1");
        # Connect all singals to methods in this class
        builder.connect_signals(self)
        # Show the window and all its children
        self.window.show_all()

    def on_file_new(self, widget, data=None):
        print "Created"

    def on_file_open(self, widget, data=None):
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
        self.spectra.r_plot()
        print "AAA:", EPS_CMD
        sp=spp.Popen([EPS_CMD, 'plot.eps'])
        sp.communicate()


def main():
    gtk.main()
    return
    
if __name__ == "__main__":
    BuilderExample()
    gtk.main()
