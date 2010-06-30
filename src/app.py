#!/usr/bin/python
# encoding: utf-8
import sys
from zope.configuration.xmlconfig import xmlconfig
import views.component as views

# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)
        

if __name__=="__main__":
    xmlconfig(open('configure.zcml'))
    sys.exit(views.main())

    
