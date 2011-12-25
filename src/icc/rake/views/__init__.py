from zope.component import getUtility
from icc.rake.interfaces import IConfiguration

def get_global_configuration():
    return getUtility(IConfiguration) 

def get_user_config_option(name, default=None, **kwargs):
    c = get_global_configuration()
    if c.USER_CONF == None:
        return None
    kw={}
    kw.update(kwargs)
    if default!=None:
        kw['default']=None
    op = c.add_option(name, **kw)
    if default!=None and op.get()==None:
        c.USER_CONF.set_option(name, default, keys=kw.get('keys', 'DEFAULT'))
        return default
    else:
        return op.get()

def set_user_config_option(name, value, **kwargs):
    c = get_global_configuration()
    if c.USER_CONF == None:
        return None
    kw={}
    kw.update(kwargs)
    op = c.add_option(name, **kw)
    c.USER_CONF.set_option(name, value, keys=kw.get('keys', 'DEFAULT'))
    return op

