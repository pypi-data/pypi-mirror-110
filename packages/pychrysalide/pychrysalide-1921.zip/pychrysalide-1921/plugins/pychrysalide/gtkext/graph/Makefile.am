
noinst_LTLIBRARIES = libpychrysagtkextgraph.la

libpychrysagtkextgraph_la_SOURCES =		\
	constants.h constants.c				\
	cluster.h cluster.c					\
	edge.h edge.c						\
	module.h module.c

libpychrysagtkextgraph_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysagtkextgraph_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
