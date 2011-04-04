#!/bin/env python
from icc.rake.modules.interfaces import *
from icc.rake.modules.components import *
from icc.rake.models.components import Module, OrderedDict
import zope.component.factory as zope_factory
from zope.component import getGlobalSiteManager, getUtility
from zope.component.interfaces import IFactory
from zope.interface import implements

class ModuleRegistry(object):
    implements(IModuleRegistry)
    def __init__(self):
        self.categories=OrderedDict()
        self.modules=OrderedDict()

module_registry=ModuleRegistry()

class Factory(zope_factory.Factory):
    def __call__(self, *args, **kwargs):
        c=self._callable
        obj = c(*args, **kwargs)
        obj.name=c.name
        obj.title=self.title
        obj.description=''
        return obj

def registerModuleFactory(f):
    name=f._callable.name
    module_registry=getUtility(IModuleRegistry)
    module_registry.modules[name]=f
    c=module_registry.categories.setdefault(f.category, {})
    c[name]=f

    # Taken from ZCA
    gsm = getGlobalSiteManager()
    gsm.registerUtility(f, IFactory, name)

"""
To use the factory, you may do it like this::

  >>> from zope.component import queryUtility
  >>> queryUtility(IFactory, 'fakedb')() #doctest: +ELLIPSIS
  <FakeDb object at ...>

There is a shortcut to use factory::

  >>> from zope.component import createObject
  >>> createObject('fakedb') #doctest: +ELLIPSIS
  <FakeDb object at ...>

""" 

def registerModule(context, name, factory, title, func, src, lang, category, icon=None, description='', inputs='{}', outputs='{}'
                   ):
    f=Factory(factory, title, description)
    factory.name=name
    factory.src=src
    factory.lang=lang
    factory.func=func
    factory.icon=icon
    f.category=category
    factory.inputs=OrderedDict(eval(inputs))
    factory.outputs=OrderedDict(eval(outputs))

    context.action(discriminator=('RegisterModule', src, func),
                   callable=registerModuleFactory,
                   args=(f,)
                   )

def get_module_registry():
    return module_registry

if __name__=="__main__":
    print "Engine to run mofule configuration."
