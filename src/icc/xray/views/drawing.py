#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1370: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1371: ** components declarations
#!/usr/bin/python

import sys, os
from gi.repository import Gtk,GObject
from gi.repository.GdkPixbuf import Pixbuf



# uncomment to select /GTK/GTKAgg/GTKCairo
#from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas
#from matplotlib.backends.backend_gtkcairo import FigureCanvasGTKCairo as FigureCanvas

# or NavigationToolbar for classic
#from matplotlib.backends.backend_gtk import NavigationToolbar2GTK as NavigationToolbar
from matplotlib.backend_bases import NavigationToolbar2
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from matplotlib.backends.backend_gtk3 import FileChooserDialog
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.widgets as widgets


#@+node:eugeneai.20110116171118.1373: ** class TXRFNavigationToolbar
class NavigationToolbar(NavigationToolbar2GTK3):
    toolitems = (
        (False, 'Home', 'Reset original view', 'home.png', 'home', 'gtk-zoom-fit'),
        (False, 'Back', 'Back to  previous view','back.png', 'back', 'gtk-go-back'),
        (False, 'Forward', 'Forward to next view','forward.png', 'forward', 'gtk-go-forward'),
        (True,  'Pan', 'Pan axes with left mouse, zoom with right', 'move.png', 'pan', 'gtk-index'),
        (True,  'Zoom', 'Zoom to rectangle','zoom_to_rect.png', 'zoom', 'gtk-zoom-in')
        )

    #@+others
    #@+node:eugeneai.20110116171118.1374: *3* __init__
    def __init__(self, canvas, view, subplots=False):
        self.view = view
        self.main_window = view.locate_widget('main_window')
        self.toolbar = view.locate_widget('toolbar')
        self.statusbar = view.locate_widget('statusbar')
        self.subplots = subplots
        #Gtk.Toolbar.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self._idle_draw_id = 0
        view.ui.main_frame.connect('destroy', self.on_destroy)

    #@+node:eugeneai.20110116171118.1375: *3* on_destroy
    def on_destroy(self, widget, data=None):
        for w in self._widgets:
            if w and self.toolbar:
                self.toolbar.remove(w)
        self.view=None

    #@+node:eugeneai.20110116171118.1376: *3* _init_toolbar
    def _init_toolbar(self):
        #self.toolbar.set_style(Gtk.StyleType.ICONS)
        self._init_toolbar2_4()

    #@+node:eugeneai.20110116171118.1377: *3* insert
    def insert(self, widget, pos=-1):
        try:
            self._widgets
        except AttributeError:
            self._widgets = []
        if self.toolbar:
            self.toolbar.insert(widget, pos)
            self._widgets.append(widget)

    #@+node:eugeneai.20110116171118.1378: *3* _init_toolbar2_4
    def _init_toolbar2_4(self):
        basedir = os.path.join(matplotlib.rcParams['datapath'],'images')


        toolitem = Gtk.SeparatorToolItem()
        self.insert(toolitem, -1)
        for toggled, text, tooltip_text, image_file, callback, stock in self.toolitems:
            if text is None:
                self.insert( Gtk.SeparatorToolItem(), -1 )
                continue
            if text=='Subplots' and not self.subplots:
                continue
            if stock is None:
                fname = os.path.join(basedir, image_file)
                image = Gtk.Image()
                image.set_from_file(fname)
                if toggled:
                    tbutton = Gtk.ToggleToolButton(image, text)
                else:
                    tbutton = Gtk.ToolButton(image, text)
            else:
                if toggled:
                    tbutton = Gtk.ToggleToolButton(stock)
                else:
                    tbutton = Gtk.ToolButton(stock)
            self.insert(tbutton, -1)
            if toggled:
                tbutton.connect('toggled', getattr(self, callback))
            else:
                tbutton.connect('clicked', getattr(self, callback))
            setattr(self, callback+'_button', tbutton)
            tbutton.set_tooltip_text(tooltip_text)

        #toolitem = Gtk.SeparatorToolItem()
        #self.insert(toolitem, -1)
        # set_draw() not making separator invisible,
        # bug #143692 fixed Jun 06 2004, will be in GTK+ 2.6
        #toolitem.set_draw(False)
        #toolitem.set_expand(True)

        #toolitem = Gtk.ToolItem()
        #self.insert(toolitem, -1)
        #self.message = Gtk.Label()
        #toolitem.add(self.message)

        if self.toolbar: self.toolbar.show_all()

    #@+node:eugeneai.20110116171118.1379: *3* draw_rubberband
    def draw_rubberband_(self, event, x0, y0, x1, y1):
        'adapted from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/189744'
        drawable = self.canvas
        if drawable is None:
            return

        gc = drawable.new_gc()
        gc.function = Gtk.gdk.INVERT
        gc.foreground = Gtk.gdk.color_parse("#FFFFFFFFFFFF")
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

    #@+node:eugeneai.20110116171118.1380: *3* set_message
    def set_message(self, s):
        pass

    #@+node:eugeneai.20110116171118.1381: *3* get_filechooser
    def get_filechooser(self):
        return FileChooserDialog(
            title='Save the figure',
            parent=self.main_window,
            filetypes=self.canvas.get_supported_filetypes(),
            default_filetype=self.canvas.get_default_filetype())

    #@+node:eugeneai.20110116171118.1382: *3* pan
    def pan(self, *args, **kwargs):
        self.zoom_button.set_active(False)
        return NavigationToolbar2GTK3.pan(self, *args, **kwargs)

    #@+node:eugeneai.20110116171118.1383: *3* zoom
    def zoom(self, *args, **kwargs):
        self.pan_button.set_active(False)
        return NavigationToolbar2GTK3.zoom(self, *args, **kwargs)

    #@+node:eugeneai.20110116171118.1384: *3* explore_channels
    def explore_channels(self, widget, data=None):
        self.zoom_button.set_active(False)
        try:
            cur = self.view.ui.cursor
        except AttributeError:
            self.view.ui.cursor = Cursor(self.view.ui.ax, useblit=True, hline=False, color='red', linewidth=1, aa=False )
            cur = self.view.ui.cursor
        cur.toggle_active()
        self.zoom_button.set_sensitive(not cur.active)

    #@-others
#@+node:eugeneai.20110116171118.1385: ** class Cursor
class Cursor(widgets.Cursor):
    """
    A horizontal and vertical line span the axes that and move with
    the pointer.  You can turn off the hline or vline spectively with
    the attributes

      horizOn =True|False: controls visibility of the horizontal line
      vertOn =True|False: controls visibility of the horizontal line

    And the visibility of the cursor itself with visible attribute
    """
    #@+others
    #@+node:eugeneai.20110116171118.1386: *3* __init__
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

    #@+node:eugeneai.20110116171118.1387: *3* toggle_active
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

    #@+node:eugeneai.20110116171118.1388: *3* clear
    def clear(self, event):
        'clear the cursor'
        if self.useblit:
            self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.linev.set_visible(False)
        self.lineh.set_visible(False)

    #@+node:eugeneai.20110116171118.1389: *3* onmove
    def onmove(self, event):
        'on mouse motion draw the cursor if visible'
        if event.inaxes != self.ax:
            self.linev.set_visible(False)
            self.lineh.set_visible(False)

            if self.needclear:
                self.canvas.draw_idle()
                self.needclear = False
            return
        self.needclear = True
        if not self.visible: return
        self.linev.set_xdata((event.xdata, event.xdata))

        self.lineh.set_ydata((event.ydata, event.ydata))
        self.linev.set_visible(self.visible and self.vertOn)
        self.lineh.set_visible(self.visible and self.horizOn)

        self._update()


    #@+node:eugeneai.20110116171118.1390: *3* _update
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

    #@-others
