#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1370: * @file components.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1371: ** components declarations
#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, gobject, sys

if __name__=="__main__":
    sys.path.append("..")

from icc.xray.views.interfaces import *
from zope.interface import implements, implementsOnly
import zope.component as ZC
import zope.component.interfaces as ZCI
from zope.component.factory import Factory
from pkg_resources import resource_stream, resource_string
from icc.rake.views import get_global_configuration

import icc.xray.models.components as mdl
import icc.xray.models.interfaces as mdli
import icc.rake.views.components as rakeviews
import icc.rake.views.interfaces as rakeints
from icc.xray.views.interfaces import *
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

XPM_META = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "   ......       ",
  "   .XXX.X.      ",
  "   .XXX.XX.     ",
  "   .XXX.....    ",
  "   .XXXXXXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXX.XXX.    ",
  "   .XXXXXXX.    ",
  "   .XXX.XXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                ",
  "                "
  ]

XPM_FILE = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "   ......       ",
  "   .XXX.X.      ",
  "   .XXX.XX.     ",
  "   .XXX.....    ",
  "   .XXXXXXX.    ",
  "   .X.....X.    ",
  "   .X.XXXXX.    ",
  "   .X.XXXXX.    ",
  "   .X...XXX.    ",
  "   .X.XXXXX.    ",
  "   .X.XXXXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                ",
  "                "
  ]

XPM_EMPTY = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "................",
  ".XX.XX.XX.XX.XX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXXXXXXXXXX..",
  ".XXXXXXXXXXXXXX.",
  ".XX.XX.XX.XX.XX.",
  "................"
  ]

XPM_SPECTRUM = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "................",
  ".XX.XX.XX.XX.XX.",
  ".XXXXXXXXXXXXXX.",
  "..XXXX.XXXXXXX..",
  ".XXXXX.XXXXXXXX.",
  ".XXXXX.XXXXXXXX.",
  "..XXXX.XXXXXXX..",
  ".XXXXX.XXXXXXXX.",
  ".XXXX.X.XXXXXXX.",
  "..XXX.X.XXXXXX..",
  ".XXXX.X.XXXXXXX.",
  ".XXX.XXX.XXX..X.",
  "....XXXXX...XX..",
  ".XXXXXXXXXXXXXX.",
  ".XX.XX.XX.XX.XX.",
  "................"
  ]

XPM_PROJECT = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "    .......     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .XXXXX.     ",
  "    .......     ",
  "     .XXX.      ",
  "     .....      ",
  "      .X.       ",
  "      .X.       ",
  "      .X.       ",
  "   .........    ",
  "   .XXXXXXX.    ",
  "   .XXXXXXX.    ",
  "   .........    ",
  "                "
  ]


XPM_STYLE = [
  "16 16 4 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "O      c #FFFF0000FFFF",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "................",
  ".OOOOOOOOOOOOOO.",
  ".OOOOOOOOOOOOOO.",
  "................",
  "                ",
  "                ",
  "                ",
  "                ",
  "                "
  ]

XPM_NONE = [
  "16 16 3 1",
  "       c None",
  ".      c #000000000000",
  "X      c #FFFFFFFFFFFF",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                ",
  "                "
  ]




#@+node:eugeneai.20110116171118.1372: ** gsm
def gsm():
    return ZC.getGlobalSiteManager()

#@+node:eugeneai.20110116171118.1373: ** class TXRFNavigationToolbar
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

    #@+others
    #@+node:eugeneai.20110116171118.1374: *3* __init__
    def __init__(self, canvas, view, subplots=False):
        self.view = view
        self.main_window = view.locate_widget('main_window')
        self.toolbar = view.locate_widget('toolbar')
        self.statusbar = view.locate_widget('statusbar')
        self.subplots = subplots
        #gtk.Toolbar.__init__(self)
        NavigationToolbar2.__init__(self, canvas)
        self._idle_draw_id = 0
        view.ui.main_frame.connect('destroy', self.on_destroy)

    #@+node:eugeneai.20110116171118.1375: *3* on_destroy
    def on_destroy(self, widget, data=None):
        # print self._widgets
        for w in self._widgets:
            if w and self.toolbar:
                self.toolbar.remove(w)
        self.view=None

    #@+node:eugeneai.20110116171118.1376: *3* _init_toolbar
    def _init_toolbar(self):
        self.toolbar.set_style(gtk.TOOLBAR_ICONS)
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

        if self.toolbar: self.toolbar.show_all()

    #@+node:eugeneai.20110116171118.1379: *3* draw_rubberband
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
        return NavigationToolbar2GTKAgg.pan(self, *args, **kwargs)

    #@+node:eugeneai.20110116171118.1383: *3* zoom
    def zoom(self, *args, **kwargs):
        self.pan_button.set_active(False)
        return NavigationToolbar2GTKAgg.zoom(self, *args, **kwargs)

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
#@+node:eugeneai.20110116171118.1391: ** class View
class View(rakeviews.View):
    resource=__name__

#@+node:eugeneai.20110116171118.1392: ** class PlottingView
class PlottingView(View):
    implements(IPlottingView)
    ZC.adapts(mdli.ISpectra, rakeints.IView)
    #@+others
    #@+node:eugeneai.20110116171118.1393: *3* __init__
    def __init__(self, model=None, parent=None):
        View.__init__(self, model, parent=parent)
        self.ui=rakeviews.Ui()
        self.ui.win=gtk.Frame()

        #parent_ui= ui = parent.ui #gsm().getUtility(rakeints.IApplication).ui
        parent_ui= ui = gsm().getUtility(rakeints.IApplication).ui

        local=rakeviews.Ui()
        self.local=local

        self.ui.main_frame = win = self.ui.win
        win.set_shadow_type(gtk.SHADOW_NONE)

        vbox = gtk.VBox()
        win.add(vbox)

        fig = Figure(figsize=(5,4), dpi=100)
        self.ui.fig = fig
        ax = fig.add_subplot(111)
        self.ui.ax = ax

        canvas = FigureCanvas(fig)  # a gtk.DrawingArea
        self.ui.canvas = canvas
        canvas.set_size_request(600, 400)
        vbox.pack_start(canvas, True, True)
        toolbar_ = TXRFNavigationToolbar(canvas, self)
        # vbox.pack_start(toolbar, False, False)

        self.ui.sb=ui.statusbar
        local.msg_id=None
        local.ctx_id=self.ui.sb.get_context_id("plotting")

        self.ui.cid = canvas.mpl_connect('button_press_event', self.on_click)
        # self.ui.check_buttons = widgets.CheckButtons(ax, ['1']*20, [True]*20)
        self.invalidate_model(model)

    def on_model_changed(self, model):
        try:
            ax=self.ui.ax
            fig=self.ui.fig
        except AttributeError:
            return
        if not self.model or not self.model.spectra:
            print "STUB:"
            t = arange(0.0,3.0,0.01)
            s = sin(2*pi*t)
            pl=ax.plot(t,s)
        else:
            print "SPECTRA:"
            for i, spec in enumerate(self.model.spectra):
                spectrum = spec['spectrum']
                sp_len = len(spectrum)
                X = arange(sp_len)
                kevs = self.model.scale.to_keV(X)
                spec.setdefault('aa', True)
                spec.setdefault('linewidth', 1)
                spec.setdefault('alpha',1.0)
                kwargs = {}
                kwargs.update(spec)
                del kwargs['spectrum']
                pl, = ax.plot(kevs, spectrum, **kwargs)
                spec['line2D'] = pl

            ax.set_ylabel('Counts')
            ax.set_xlabel('k$e$V')
            #ax.set_title('Spectra plot')
            ax.set_xlim(kevs[0],kevs[-1])
            # ax.set_yscale('log')
            ax.ticklabel_format(style='sci', scilimits=(3,0), axis='y')
            ax.grid(b=True, aa=False, alpha=0.3)
            #ax.legend()
            ax.minorticks_on()

    #@+node:eugeneai.20110116171118.1394: *3* on_click
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

    #@+node:eugeneai.20110116171118.1395: *3* on_spectra_clicked
    def on_spectra_clicked(self, project_view):
        #print "Spectra_clicked!!"
        any_vis = False
        for sp in self.model.spectra:
            alpha = sp.setdefault('alpha',1.0)
            if alpha>0.1:
                any_vis = True
        [self._set(sp, not any_vis) for sp in self.model.spectra]
        self.ui.canvas.draw()

    #@+node:eugeneai.20110116171118.1396: *3* on_spectrum_clicked
    def on_spectrum_clicked(self, project_view, spectrum_data, user_data=None):
        #print "Spectrum selected:", spectrum_data
        path = spectrum_data['path']
        index = path[-1]
        s=self.model.spectra
        print index, s, self.model.__class__
        spec = s[index]
        spec['path'] = path
        if spec['label'] != spectrum_data['name']:
            print "Warning: name difference!!"

        # print spec
        self._toggle(spec)
        self.ui.canvas.draw()

    #@+node:eugeneai.20110116171118.1397: *3* _toggle
    def _toggle(self, spec):
        print "Spec:", spec
        line = spec['line2D']
        newalpha = 1.0 - spec.get('alpha', 1.0)
        line.set(alpha=newalpha)
        spec['alpha']=newalpha

    #@+node:eugeneai.20110116171118.1398: *3* _set
    def _set(self, spec, vis):
        line = spec['line2D']
        newalpha = int(vis) * 1.0
        line.set(alpha=newalpha)
        spec['alpha']=newalpha


    #@-others
#@+node:eugeneai.20110116171118.1399: ** class ProjectView
#pffactory = Factory(PlottingFrame, 'PlottingFrame', 'Frame, where one can plot spectra.')
#gsm().registerUtility(pffactory, ZCI.IFactory, 'PlottingFrame')

class ProjectView(View):
    __gsignals__ = {
        'spectrum-clicked': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)), # filename and spectrum choosen
        'file-clicked': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE,
            (gobject.TYPE_STRING, gobject.TYPE_PYOBJECT)), # filename and all its spectra
    }
    template = "ui/project_frame.glade"
    widget_names = ["project_frame",
                    "project_tree_view", "main_vbox", "common_label",
                    "project_list_model", "project_tree_model", "paned_top", "paned_bottom",
                    "ag_spectra"]
    implements(rakeints.IProjectView)
    ZC.adapts(mdli.IProject, rakeints.IView)
    #@+others
    #@+node:eugeneai.20110116171118.1400: *3* __init__
    def __init__(self, model=None, parent=None):
        self.active_view = None
        View.__init__(self, model=model, parent=parent)
        self.ui.main_frame=self.ui.project_frame

        _conf=get_global_configuration()
        opt=_conf.add_option('spectra_file_ext', default='.*:All Files', keys='app')
        self.FILE_PATTERNS=[e.split(':') for e in opt.get().split('|')]

        self.active_view = ZC.getMultiAdapter((mdli.ISpectra(self.model), self), IPlottingView)
        #self.connect('spectrum-clicked', self.active_view.on_spectrum_clicked)
        #self.connect('file-clicked', self.active_view.on_spectra_clicked)
        self.connect('spectrum-clicked', self.on_spectrum_clicked)
        self.connect('file-clicked', self.on_file_clicked)
        self.ui.main_vbox.pack_start(self.active_view.ui.main_frame)
        self.ui.hpaned_list=[self.ui.paned_top, self.ui.paned_bottom]

        self.add_actions_to_menu(self.ui.ag_spectra, label='Spectra')
        self.ui.tb_widgets=self.add_actions_to_toolbar(self.ui.ag_spectra)

        parent.connect('project-open', self.on_file_open)
        parent.connect('project-save', self.on_file_save)

    def do_destroy_view(self, self_widget, data=None):
        self.del_actions_from_menu(self.ui.ag_spectra)
        self.del_actions_from_toolbar(self.ui.ag_spectra, self.ui.tb_widgets)

    def on_file_open(self, app, filename, data=None):
        print "Opening file", filename
        try:
            self.model.load(filename)
        except OSError:
            return False
        self.set_model(self.model)
        return True

    def on_file_save(self, app, filename, data=None):
        print "Saving file", filename
        self.model.save(filename)
        return True

    #@+node:eugeneai.20110116171118.1401: *3* get_objects
    def get_objects(self):
        try:
            d = self._obj_cache
            return d
        except AttributeError:
            try:
                int('df')
                d = self.model.get_objects()
                self._obj_cache = d
            except ValueError, exc:
                #print "EXC:", exc
                d = {"creator":'', 'comment':'',
                     'spectra':[]}
                # skip cache !!!
        return d

    #@+node:eugeneai.20110116171118.1402: *3* set_model
    def set_model(self, model=None):
        View.set_model(self, model=model)
        #if self.active_view:
        #    self.active_view.set_model(mdli.ISpectra(self.model))
        #    self.active_view.invalidate_model(self.active_view.model)

        try:
            t = self.ui.project_tree_model
        except AttributeError:
            return
        t.clear()

        d = self.get_objects()

        pb = gtk.gdk.pixbuf_new_from_xpm_data(XPM_PROJECT)
        pm = gtk.gdk.pixbuf_new_from_xpm_data(XPM_META)
        pc = gtk.gdk.pixbuf_new_from_xpm_data(XPM_SPECTRUM)
        ps = gtk.gdk.pixbuf_new_from_xpm_data(XPM_STYLE)
        pn = gtk.gdk.pixbuf_new_from_xpm_data(XPM_NONE)
        pf = gtk.gdk.pixbuf_new_from_xpm_data(XPM_FILE)
        self.ui.pb_project = pb
        self.ui.pb_meta = pm
        self.ui.pb_file = pf
        self.ui.pb_spectrum = pc
        self.ui.pb_empty = gtk.gdk.pixbuf_new_from_xpm_data(XPM_EMPTY)
        self.ui.pb_none = pn
        self.ui.ps_style= ps
        root = t.append(None, ('Project', pb, False, False, pn))
        meta = t.append(root, ('Info', pm, False, False, pn))
        print self.model.spectral_data
        for name, sd in self.model.spectral_data.iteritems():
           f = t.append(root, (sd.name, pf, False, False, pn))
           for sp in sd().data:
               s = t.append(f, (sp.name, pc, False, False, ps))
        """
        self.spectra_it = spectra
        for sp in d['spectra']:
            sp_it = t.append(spectra, (sp['name'], pc, False, False, ps))
            sp['path']=t.get_path(sp_it)
        """
        self.ui.project_tree_view.expand_all()


    #@+node:eugeneai.20110116171118.1403: *3* set_pb
    def set_pb(self, path, pb):
        tm =  self.ui.project_tree_model
        it = tm.get_iter(path)
        tm.set_value(it, 1, pb)

    #@+node:eugeneai.20110116171118.1404: *3* on_spectra_clicked
    def on_file_clicked(self, widget, filename, sp, user_data=None):
        print "File:", filename, sp
        self._renew_vis_project_tree()

    #@+node:eugeneai.20110116171118.1405: *3* on_spectrum_clicked
    def on_spectrum_clicked(self, widget, filename, spec, user_data=None):
        print "Spectrum:", filename, spec
        self._renew_vis_project_tree()

    #@+node:eugeneai.20110116171118.1406: *3* _renew_vis_project_tree
    def _renew_vis_project_tree(self):
        any_vis = False
        sd = self.get_objects()['spectra']
        t = self.ui.project_tree_model
        for i, sp in enumerate(self.active_view.model.spectra):
            alpha = sp.setdefault('alpha', 1.0)
            path = sp.setdefault('path', sd[i].get('path', None))
            if path is None:
                continue
            if alpha>0.1:
                self.set_pb(path, self.ui.pb_spectrum)
                any_vis = True
            else:
                self.set_pb(path, self.ui.pb_empty)
        path = t.get_path(self.spectra_it)
        if any_vis:
            self.set_pb(path, self.ui.pb_spectrum)
        else:
            self.set_pb(path, self.ui.pb_empty)


    #@+node:eugeneai.20110116171118.1407: *3* on_row_activated
    def on_row_activated(self, tree_view, path, column, data=None):
        #print 'Clicked:', tree_view, path, column, data
        lp=len(path)
        if lp==1:
            # root clicked
            return
        file_no=path[1]-1 # Minus info node
        filename, sp=self.model.spectral_data.items()[file_no]
        if lp==2:
            #file clicked
            self.emit('file-clicked', filename, sp)
            return
        else:
            self.emit('spectrum-clicked', filename, sp.data[path[-1]])

    #Horizontal paned synchronisation.

    def on_paned_notify(self, paned, spec, data=None):
        if spec.name=='position':
            pos=paned.get_property('position')
            [p.set_position(pos) for p in self.ui.hpaned_list if p!=paned] # recursion breaks due to position property: it can be unchanged.

    def on_spectra_close(self, widget, data=None):
        print "On spectra close", widget, data

    def on_spectra_export(self, widget, data=None):
        print "On spectra export", widget, data

    def on_spectra_load(self, widget, data=None):
        file_name = self.get_filename(self.FILE_PATTERNS, open_msg="Load spectra ...", filter_name='Spectra Files')
        if file_name != None:
            self.load_spectra(file_name)

    def load_spectra(self, file_name):
        self.model.add_spectral_data_source(file_name)
        self.set_model(self.model)
        self.emit('model-changed', self.model)
        self.active_view.canvas.draw()
        print 'need to be refreshed'

    #@-others

gobject.type_register(ProjectView)

if __name__=="__main__":
    import icc.icc_xray_app
    icc.icc_xray_app.main()

#@-others
#@-leo
