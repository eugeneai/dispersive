#!/usr/bin/python
# encoding: utf-8
import sys
from zope.configuration.xmlconfig import xmlconfig
import icc.xray.views.components as views

if __name__=="__main__":
    xmlconfig(open('xray/configure.zcml'))
    sys.exit(views.main())

    
