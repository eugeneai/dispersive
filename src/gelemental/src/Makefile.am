AM_CPPFLAGS = -I$(top_srcdir) -DLOCALEDIR=\"$(localedir)\" \
	$(GELEMENTAL_CPPFLAGS)
AM_CXXFLAGS = $(GELEMENTAL_CXXFLAGS) -I/usr/include/python2.7

bin_PROGRAMS = gelemental

gelemental_SOURCES = \
	private.hh misc.hh misc.cc \
	dialogs.hh dialogs.cc \
	buttons.hh buttons.cc \
	table-table.hh table-table.cc \
	table-list.hh table-list.cc \
	main.hh main.cc \
	elwidget.cpp

gelemental_LDADD = \
	$(GELEMENTAL_LIBS) \
	../libelemental/libelemental.la \
	../libelemental/misc/libmisc-gtk.la
