#@+leo-ver=5-thin
#@+node:eugeneai.20110116171118.1423: * @file app.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110116171118.1424: ** app declarations

import pygtk
pygtk.require('2.0')
import gtk

#Initializing the gtk's thread engine
#gtk.threads_init()
#print "Gtk threads initized in", __file__

from zope.configuration.xmlconfig import xmlconfig
import zope.component as ZC
from pkg_resources import resource_stream, resource_string
import sys
import cfgparse as cfg
from icc.rake.interfaces import IConfiguration
from zope.interface import directlyProvides
from icc.rake.views import get_user_config_option
import os.path

#@+node:eugeneai.20110116171118.1425: ** main
def main(package=None):
    if package == None:
        package=__name__
    c=cfg.ConfigParser()
    config_file=resource_stream(package, "application.ini")
    main_conf=c.add_file(config_file)
    user_conf_opt=c.add_option('user_config_file', keys='app', default=None, type='string')
    user_config_file=user_conf_opt.get()
    if user_config_file != None:
        user_config_file=os.path.expanduser(user_config_file)
        if os.path.exists(user_config_file):
            user_conf = c.add_file(user_config_file)
        else:
            print "Warning: no user config file '%s' found." % user_config_file
            user_conf = None
    else:
        user_conf=None

    gsm = ZC.getGlobalSiteManager()
    directlyProvides(c, IConfiguration)
    conf=c.add_option('conf', default='configuration')
    c.USER_CONF=user_conf
    c.MAIN_CONF=main_conf
    gsm.registerUtility(c)
    gsm.registerUtility(c, name=conf.get())
    xmlconfig(resource_stream(package, "configure.zcml"))
    app=ZC.createObject("Application")
    view=c.add_option('view', default='application')
    gsm.registerUtility(app)
    gsm.registerUtility(app, name=view.get())

    #Open last project file if user has configured in their user config file.
    if get_user_config_option('load_last_project', default=0, type='int', keys='startup'):
        lp_fn=get_user_config_option('last_project_file_name', default='', type='string', keys='startup').strip()
        if lp_fn:
            app.emit("startup-open", lp_fn)

    rc = app.main()

    if user_conf: user_conf.write(user_config_file)

    return rc

#@-others
if __name__ == "__main__":
    sys.exit(main())
#@-leo
