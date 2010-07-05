#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, sys

if __name__=="__main__":
    sys.path.append("..")

from icc.xray.views.interfaces import *
from zope.interface import implements, implementsOnly
import zope.component as ZC
import zope.component.interfaces as ZCI
from zope.component.factory import Factory
from pkg_resources import resource_stream, resource_string
    
import icc.xray.models.components as mdl
import icc.xray.models.interfaces as mdli
import os
import subprocess as spp

import matplotlib.widgets as widgets
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

DEBUG = 2
if DEBUG>2:
    LOAD_FILE="test.rtx"

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

def gsm():
    return ZC.getGlobalSiteManager()

class Ui:
    pass
  
class TXRFNavigationToolbar(NavigationToolbar2GTKAgg):
    toolitems = (
        (False, 'Home', 'Reset original view', 'home.png', 'home', 'gtk-zoom-fit'),
        (False, 'Back', 'Back to  previous view','back.png', 'back', 'gtk-go-back'),
        (False, 'Forward', 'Forward to next view','forward.png', 'forward', 'gtk-go-forward'),
        (True,  'Pan', 'Pan axes with left mouse, zoom with right', 'move.png', 'pan', 'gtk-index'),
        (True,  'Zoom', 'Zoom to rectangle','zoom_to_rect.png', 'zoom', 'gtk-zoom-in'),
        # (None, None, None, None, None, None),
        (False, 'Subplots', 'Configure subplots','subplots.png', 'configure_subplots', 'gtk-preferences'),
        (False, 'Save', 'Save the figure','filesave.png', 'save_figure', 'gtk-convert'),
        (True,  'Channels', 'Explore channel counts','filesave.png', 'explore_channels', 'gtk-color-picker'),
        )
    
    def __init__(self, canvas, view, main_ui, subplots=False):
        self.view = view
        self.main_ui = main_ui
        self.toolbar = main_ui.toolbar
        self.statusbar = main_ui.statusbar
        self.subplots = subplots
        #gtk.Toolbar.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self._idle_draw_id = 0
        view.ui.main_frame.connect('destroy', self.on_destroy)

    def on_destroy(self, widget, data=None):
        # print self._widgets
        for w in self._widgets:
            if w:
                self.toolbar.remove(w)
        self.view=None

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
        for toggled, text, tooltip_text, image_file, callback, stock in self.toolitems:
            if text is None:
                self.insert( gtk.SeparatorToolItem(), -1 )
                continue
            if text=='Subplots' and not self.subplots:
                continue
            if stock is None:
                fname = os.path.join(basedir, image_file)
                image = gtk.Image()
                image.set_from_file(fname)
                if toggled:
                    tbutton = gtk.ToggleToolButton(image, text)
                else:
                    tbutton = gtk.ToolButton(image, text)
            else:
                if toggled:
                    tbutton = gtk.ToggleToolButton(stock)
                else:
                    tbutton = gtk.ToolButton(stock)
            self.insert(tbutton, -1)
            if toggled:
                tbutton.connect('toggled', getattr(self, callback))
            else:
                tbutton.connect('clicked', getattr(self, callback))
            setattr(self, callback+'_button', tbutton)
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

    def pan(self, *args, **kwargs):
        self.zoom_button.set_active(False)
        return NavigationToolbar2GTKAgg.pan(self, *args, **kwargs)

    def zoom(self, *args, **kwargs):
        self.pan_button.set_active(False)
        return NavigationToolbar2GTKAgg.zoom(self, *args, **kwargs)

    def explore_channels(self, widget, data=None):
        self.zoom_button.set_active(False)
        try:
            cur = self.view.ui.cursor
        except AttributeError:
            self.view.ui.cursor = Cursor(self.view.ui.ax, useblit=True, hline=False, color='red', linewidth=1, aa=False )
            cur = self.view.ui.cursor
        cur.toggle_active()
        self.zoom_button.set_sensitive(not cur.active)

class Cursor(widgets.Cursor):
    """
    A horizontal and vertical line span the axes that and move with
    the pointer.  You can turn off the hline or vline spectively with
    the attributes

      horizOn =True|False: controls visibility of the horizontal line
      vertOn =True|False: controls visibility of the horizontal line

    And the visibility of the cursor itself with visible attribute
    """
    def __init__(self, ax, useblit=False, hline=True, **lineprops):
        """
        Add a cursor to ax.  If useblit=True, use the backend
        dependent blitting features for faster updates (GTKAgg only
        now).  lineprops is a dictionary of line properties.  See
        examples/widgets/cursor.py.
        """
        self.ax = ax
        self.canvas = ax.figure.canvas
        
        self.visible = True
        self.horizOn = hline
        self.vertOn = True
        self.useblit = useblit

        self.lineh = ax.axhline(ax.get_ybound()[0], visible=False, **lineprops)
        self.linev = ax.axvline(ax.get_xbound()[0], visible=False, **lineprops)

        self.active = False

    def toggle_active(self):
        if self.active:
            self.canvas.mpl_disconnect(self.cid_d)
            self.canvas.mpl_disconnect(self.cid_m)
        else:
            self.cid_m = self.canvas.mpl_connect('motion_notify_event', self.onmove)
            self.cid_d = self.canvas.mpl_connect('draw_event', self.clear)
        self.active = not self.active
        self.linev.set_visible(False)
        self.lineh.set_visible(False)
        self.needclear = True
        self.background = None

    def clear(self, event):
        'clear the cursor'
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.linev.set_visible(False)
        self.lineh.set_visible(False)

    def onmove(self, event):
        'on mouse motion draw the cursor if visible'
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible: return
        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()


    def _update(self):

        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.linev)
            self.ax.draw_artist(self.lineh)
            self.canvas.blit(self.ax.bbox)
        else:

            self.canvas.draw_idle()

        return False

class View(object):
    template = None
    widget_names    = None
    #implements(IView)
    ZC.adapts(mdli.IModel)
    def __init__(self, model = None):
        self.ui=Ui()
        self.set_model(model)
        self.load_ui(self.__class__.template,
                     self.__class__.widget_names)

    def set_model(self, model):
        self.model=model
        # some update needed???

    def load_ui(self, template, widget_names = None):
        if template:
            builder=self.ui._builder = gtk.Builder()
            builder.add_from_string(resource_string(__name__, template))
            builder.connect_signals(self, builder)
            if widget_names:
                for name in widget_names:
                    widget = builder.get_object(name)
                    if widget is None:
                        raise ValueError("widget '%s' not found in  template '%s'" % (name, template))
                    setattr(self.ui, name, widget)
        

class PlottingView(View):
    implements(IPlottingView)
    ZC.adapts(mdli.ISpectra)
    def __init__(self, model=None, label=None):
        View.__init__(self, model)
        self.ui=Ui()   
        self.ui.win=gtk.Frame(label=label)
        self.spectra = model
        parent_ui= ui = gsm().getUtility(IApplication).ui

        local=Ui()
        self.local=local

        self.ui.main_frame = win = self.ui.win
        win.set_shadow_type(gtk.SHADOW_NONE)
        
        vbox = gtk.VBox()
        win.add(vbox)
        
        fig = Figure(figsize=(5,4), dpi=100)
        self.ui.fig = fig
        ax = fig.add_subplot(111)
        self.ui.ax = ax

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
        self.ui.canvas = canvas
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True)
        toolbar_ = TXRFNavigationToolbar(canvas, self, parent_ui)
        # vbox.pack_start(toolbar, False, False)

        self.ui.sb=ui.statusbar
        local.msg_id=None
        local.ctx_id=self.ui.sb.get_context_id("plotting")

        self.ui.cid = canvas.mpl_connect('button_press_event', self.on_click)
        # self.ui.check_buttons = widgets.CheckButtons(ax, ['1']*20, [True]*20)

    def on_click(self, event, data=None): 
        local = self.local
        if local.msg_id is not None:
            self.ui.sb.remove_message(local.ctx_id, local.msg_id)
        if event.xdata and event.ydata:
            s='button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
                event.button, event.x, event.y, event.xdata, event.ydata)
        else:
            s=' '.join([str(x) for x in [event.button, event.x, event.y, event.xdata, event.ydata]])

        local.msg_id=self.ui.sb.push(local.ctx_id, s)

#pffactory = Factory(PlottingFrame, 'PlottingFrame', 'Frame, where one can plot spectra.')
#gsm().registerUtility(pffactory, ZCI.IFactory, 'PlottingFrame')

class ProjectView(View):
    template = "ui/project_frame.glade"
    widget_names = ["project_frame", "vpaned_left", "vpaned_right",
                    "project_tree_view", "main_vbox", "common_label",
                    "project_list_model", "project_tree_model"]
    def __init__(self, model=None, label=None):
        View.__init__(self, model=model)
        self.ui.main_frame=self.ui.project_frame

class Application(View):
    implements(IApplication)
    template = "ui/main_win_gtk.glade"
    widget_names = ['main_window', 'statusbar', 'toolbar',
             "main_vbox"]

    def __init__(self, model = None):
        View.__init__(self, model=model)
        self.ui.window=self.ui.main_window
        self.ui.window.show_all()
        self.active_view=None

        # Shoul be the last one, it seems
        if DEBUG>2:
            self.default_view()
            self.open_project(self, LOAD_FILE)

    def set_model(self, model = None):
        if model is None:
            model = mdl.Spectra()
        return View.set_model(self, model)

    # Signal connection is linked in the glade XML file
    def main_window_delete_event_cb(self, widget, data1=None, data2=None):
        gtk.main_quit()
    m_quit_activate_cb=main_window_delete_event_cb

    def default_view(self):
        self.insert_plotting_area(self.ui)

    def on_file_new(self, widget, data=None):
        # print "Created"
        # check wether data has been saved. YYY
        self.spectra = None
        self.insert_plotting_area(self.ui)

    def open_project(self, filename=None):
        if filename is None:
            filename = self.get_open_filename()
        if filename:
            self.model = mdl.Spectra(filename)
            self.default_action()

    def on_file_open(self, widget, data=None):
        return self.open_project()
            
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
        # print "File:", filename
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
        self.model.get_spectra()
        self.model.set_scale(mdl.Scale(zero=CALIBR_ZERO, scale=CALIBR_KEV))
        self.default_view()
        #self.spectra.r_plot()
        #print "AAA:", EPS_CMD
        #sp=spp.Popen([EPS_CMD, 'plot.eps'])
        #sp.communicate()

    def remove_active_view(self):
        if self.active_view is None:
            return
        main_widget = self.active_view.ui.main_frame
        self.ui.main_vbox.remove(main_widget)
        main_widget.destroy()
        self.active_wiew=None

    def insert_active_view(self, view):
        if self.active_view:
            self.remove_active_view()
        self.active_view = view
        self.ui.main_vbox.pack_start(view.ui.main_frame, True, True)
        view.ui.main_frame.show_all()

    def insert_plotting_area(self, ui):
        view = IPlottingView(self.model)
        self.insert_active_view(view)

    def main(self):
        return gtk.main()
    
    run = main


