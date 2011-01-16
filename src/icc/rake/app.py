#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1423: * @file app.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1424: ** app declarations
from zope.configuration.xmlconfig import xmlconfig
import zope.component as ZC
from pkg_resources import resource_stream, resource_string
import sys
import cfgparse as cfg
from icc.rake.interfaces import IConfiguration
from zope.interface import directlyProvides

#@+node:eugeneai.20110116171118.1425: ** main
def main(package=None):
    if package == None:
        package=__name__
    c=cfg.ConfigParser()
    c.add_file(resource_stream(package, "application.ini"))
    c.parse()
    gsm = ZC.getGlobalSiteManager()
    directlyProvides(c, IConfiguration)
    conf=c.add_option('conf', default='configuration')
    gsm.registerUtility(c)    
    gsm.registerUtility(c, name=conf.get())    
    xmlconfig(resource_stream(package, "configure.zcml"))
    app=ZC.createObject("Application")
    view=c.add_option('view', default='application')
    gsm.registerUtility(app)
    gsm.registerUtility(app, name=view.get())
    return app.main()

#@-others
if __name__ == "__main__":
    sys.exit(main())
#@-leo
