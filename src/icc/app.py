#!/usr/bin/python
# encoding: utf-8
import sys
from zope.configuration.xmlconfig import xmlconfig
import dispersive.views.component as views

if __name__=="__main__":
    xmlconfig(open('dispersive/configure.zcml'))
    sys.exit(views.main())

    
