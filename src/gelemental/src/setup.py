from setuptools import setup
from setuptools import Extension
from Cython.Distutils import build_ext

sourcefiles = ['elwidget.pyx', 'table-table.cc']

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension(
            "_elwidget",
            sourcefiles,
            language="c++",
            include_dirs=['../','/usr/include',
                '/usr/include/glibmm-2.4',
                '/usr/lib/glibmm-2.4/include',
                '/usr/include/sigc++-2.0',
                '/usr/lib/sigc++-2.0/include',
                '/usr/include/atkmm-1.6',
                '/usr/include/giomm-2.4',
                '/usr/lib/giomm-2.4/include',
                '/usr/include/pangomm-1.4',
                '/usr/lib/pangomm-1.4/include',
                '/usr/include/gtk-2.0',
                '/usr/include/gtk-unix-print-2.0',
                '/usr/include/gtkmm-2.4',
                '/usr/lib/gtkmm-2.4/include',
                '/usr/include/gdkmm-2.4',
                '/usr/lib/gdkmm-2.4/include',
                '/usr/include/atk-1.0',
                '/usr/include/glib-2.0',
                '/usr/lib/glib-2.0/include',
                '/usr/include/cairomm-1.0',
                '/usr/lib/cairomm-1.0/include',
                '/usr/include/pango-1.0',
                '/usr/include/cairo',
                '/usr/include/pixman-1',
                '/usr/include/freetype2',
                '/usr/include/libpng15',
                '/usr/include/qt4',
                '/usr/include/qt4/QtGui',
                '/usr/include/libdrm',
                '/usr/include/qt4/QtCore',
                '/usr/lib/gtk-2.0/include',
                '/usr/include/gdk-pixbuf-2.0',
                ]
        )
    ]
)


