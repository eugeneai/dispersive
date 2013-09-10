#@+leo-ver=5-thin
#@+node:eugeneai.20110115235621.1287: * @file setup.py
#@@language python
#@@tabwidth -4
#@+others
#@+node:eugeneai.20110115235621.1289: ** distribute imports
from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages, Extension
from distutils import log
#@+node:eugeneai.20110115235621.1288: ** setup

log.set_verbosity(100)

setup(
    zip_safe = False,
    name="icc.xray",
    version="0.0.7",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["icc"],
    scripts = ['src/icc/icc_xray_app.py'],
    install_requires=[
                    #@+<< requirenments >>
                    #@+node:eugeneai.20110116000634.1304: *3* << requirenments >>
                    "setuptools",
                    "numpy",
                    "rpyc",
                    "zope.component [zcml]",
                    "cfgparse",
                    "scipy",
                    "lxml",
                    #"periodictable",
                    "matplotlib",
                    #"rsvg",
                    #"PyGTK"
                    #@-<< requirenments >>
                      ],
    package_data = {
        'icc.rake': ['configure.zcml', 'application.ini'],
        'icc.rake.models': ['configure.zcml'],
        'icc.rake.views': ['*.zcml', 'ui/*.glade', "ui/icons/tango/*/*/*.png"],
        'icc.rake.modules': ['configure.zcml'],

        'icc.xray': ['configure.zcml', 'application.ini'],
        'icc.xray.models': ['configure.zcml'],
        'icc.xray.views': ['configure.zcml', 'ui/*.glade'],
        },
    author = "Evgeny Cherkashin",
    author_email = "eugene@irnok.net",
    description = "Dispersive XRF Component Library",
    license = "GNU GPL",
    keywords = "xray pygtk analysis tool application",
    url = "http://xray.irnok.net/",
    long_description = """ Dispersive (working name) ia a package of components for
      Dispersive X-Ray Fluorescence spectra analysis.  All explorations
      will be organized as projects.  The package will able to load
      various proprietrary data formats from various sources.""",
    # platform = "Os Independent.",
    # could also include long_description, download_url, classifiers, etc.
    )
#@-others
#@-leo
