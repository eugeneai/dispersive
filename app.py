#!/usr/bin/python
# encoding: utf-8
import sys
from zope.configuration.xmlconfig import xmlconfig
#import views.component as views
        

if __name__=="__main__":
    xmlconfig(open('configure.zcml'))
    #sys.exit(views.main())

    
