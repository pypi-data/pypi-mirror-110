
noinst_LTLIBRARIES = libpychrysagtkext.la

libpychrysagtkext_la_SOURCES =			\
	blockdisplay.h blockdisplay.c		\
	bufferdisplay.h bufferdisplay.c		\
	displaypanel.h displaypanel.c		\
	dockable.h dockable.c				\
	easygtk.h easygtk.c					\
	module.h module.c					\
	named.h named.c

libpychrysagtkext_la_LIBADD =			\
	graph/libpychrysagtkextgraph.la

libpychrysagtkext_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysagtkext_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)


SUBDIRS = graph
