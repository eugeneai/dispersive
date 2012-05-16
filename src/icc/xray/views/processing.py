import icc.xray.analysis.scaling as scaling
import icc.xray.analysis.lines as lines
import sys
#import pygtk
#pygtk.require('2.0')
#import gtk, gobject, sys, os

def line_db_conn():
    if os.name!="nt":
        ldb=lines.Lines(dbname='/home/eugeneai/Development/codes/dispersive/data/lines.sqlite3')
    else:
        ldb=lines.Lines(dbname='C:\\dispersive\\data\\lines.sqlite3')
    return ldb

HOST='localhost'
PORT=12211
if __name__=="__main__" and len(sys.argv)==2 and sys.argv[1]=='server':
    from rpyc.core import SlaveService
    from rpyc.utils.server import ThreadedServer, ForkingServer
    SERVER = True
else:
    SERVER = False
    import rpyc
    import os
    if not sys.argv[0].endswith('rpyc_classic.py'):
        server=rpyc.classic.connect(HOST, PORT)
        sprocessing = server.modules['icc.xray.views.processing']
        print "Client:", server, sprocessing

class Stub:
    pass

class Parameters(object):
    e_0 = 0.0086
    def __init__(self, model=None, view=None, client=None):
        #threading.Thread.__init__(self)
        global SERVER
        self.SERVER=SERVER
        if client:
            self.model = client.model
            self.view = client.view
            self._methods=client._methods
            self._active=client._active
        else:
            self.model = model
            self.view = view
            if model == None:
                model=Stub()
                model.parameters=Stub()
                self.model=model
            if self.model.parameters == None:
                self.model.parameters = scaling.Parameters(model.channels)
            self._methods=[]
            self._active=False

    def reself(self):
        if not SERVER:
            self.obj=sprocessing.Parameters(client=self)

    def set_progressbar(self, pb):
        self.progressbar=pb

    def set_max_step(self, steps):
        self.pb_max=steps
        self.set_fraction(0., steps)

    def set_step(self, step):
        self.pb_step=step
        self.set_fraction(step, self.pb_max)

    def reset_progress(self, steps=None):
        self.pb_step=0
        if steps:
            self.set_max_step(steps)
        else:
            self.set_fraction(step, self.pb_max)

    def next_step(self):
        self.pb_step+=1
        self.set_fraction(self.pb_step, self.pb_max)

    def set_fraction(self, step, steps=None):
        if steps != None:
            frac=float(step)/steps
        else:
            frac=step
        #gtk.threads_enter()
        #self.progressbar.set_fraction(frac)
        #gtk.threads_leave()
        print "SET frac:",  frac

    def methods(self, names):
        self._methods=names

    def run(self):
        if not self.stopthread.isSet() :
            self._active=True
            for m in self._methods:
                getattr(self, m)()
            self._active=False

    def scaling(self):
        #While the stopthread event isn't setted, the thread keeps going on
        self.reset_progress(9)

        par=self.model.parameters
        pb=self.progressbar
        # Acquiring the gtk global mutex
        ##gtk.threads_enter()
        #Setting a random value for the fraction
        ##progressbar.set_fraction(random.random())
        # Releasing the gtk global mutex
        ##gtk.threads_leave()

        #Delaying 100ms until the next iteration
        ##time.sleep(0.1)

        par.set_scale_lines(self.e_0, ['Mo'], 20.) # 20 keV max
        ldb=line_db_conn()
        par.set_line_db_conn(ldb)
        par.calculate(plot=False, pb=self.next_step)
        #par.scan_peakes_cwt(plot=True)

    def show(self):
        par=self.model.parameters
        elements=self.model.ptelements
        print "EL:", elements
        le=len(elements)
        if le:
            ldb=line_db_conn()
            ls = ldb.as_deltafun(order_by="keV", element=elements,
                    where="not l.name like 'M%' and keV<20.0")
            ls=list(ls)
        gtk.threads_enter()
        self.view.paint_model([self.model], draw=False)
        par.set_figure(self.view.ui.ax)
        if le:
            par.line_plot(ls, self.view.plot_options)
        self.view.ui.canvas.draw()
        gtk.threads_leave()

    def refine(self):
        par=self.model.parameters
        elements=self.model.ptelements
        self.scaling()
        self.reset_progress(3)
        par.refine_scale(elements=elements, pb=self.next_step)

    def background(self):
        par=self.model.parameters
        elements=self.model.ptelements
        self.scaling()
        self.reset_progress(11)
        par.approx_background(elements=elements, pb=self.next_step)

    def stop(self):
        """Stop method, sets the event to terminate the thread's main loop"""
        #self.stopthread.set()

    def is_active(self):
        return self._active

if SERVER:
    t = ThreadedServer(SlaveService, hostname = 'localhost',
        port = PORT, #reuse_addr = True, # ipv6 = options.ipv6,
        #authenticator = options.authenticator, registrar = options.registrar,
        #auto_register = options.auto_register
        )
    t.logger.quiet = True
    t.start()
else:
    p=Parameters()
    p.reself()
    print "OK"

