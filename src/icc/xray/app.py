from zope.configuration.xmlconfig import xmlconfig
import icc.xray.views.components as views
from pkg_resources import resource_stream

def main():
    xmlconfig(resource_stream(__name__, "configure.zcml"))
    views.Application()
    return views.gtk.main()
    
if __name__ == "__main__":
    sys.exit(main())
