from zope.configuration.xmlconfig import xmlconfig
import zope.component as ZC
from pkg_resources import resource_stream
import sys

def main():
    xmlconfig(resource_stream(__name__, "configure.zcml"))
    app=ZC.createObject("Application")
    gsm = ZC.getGlobalSiteManager()
    gsm.registerUtility(app)
    gsm.registerUtility(app, name='application')
    return app.main()
    
if __name__ == "__main__":
    sys.exit(main())
