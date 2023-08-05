
noinst_LTLIBRARIES = libyamlpython.la

libyamlpython_la_SOURCES =					\
	collection.h collection.c				\
	line.h line.c							\
	module.h module.c						\
	node.h node.c							\
	pair.h pair.c							\
	reader.h reader.c						\
	scalar.h scalar.c						\
	tree.h tree.c

libyamlpython_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libyamlpython_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src -DNO_IMPORT_PYGOBJECT

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
