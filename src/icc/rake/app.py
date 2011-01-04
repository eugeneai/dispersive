from zope.configuration.xmlconfig import xmlconfig
import zope.component as ZC
from pkg_resources import resource_stream, resource_string
import sys
import cfgparse as cfg

def main(package=None):
    if package == None:
        package=__name__
    c=cfg.ConfigParser()
    c.add_file(resource_stream(package, "application.ini"))
    xmlconfig(resource_stream(package, "configure.zcml"))
    app=ZC.createObject("Application")
    gsm = ZC.getGlobalSiteManager()
    gsm.registerUtility(app)
    gsm.registerUtility(app, name='application')
    return app.main()
    
if __name__ == "__main__":
    sys.exit(main())
