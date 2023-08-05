
noinst_LTLIBRARIES = libdalvikpythonv35.la

libdalvikpythonv35_la_SOURCES =			\
	instruction.h instruction.c			\
	module.h module.c					\
	processor.h processor.c

libdalvikpythonv35_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdalvikpythonv35_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src -DNO_IMPORT_PYGOBJECT

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
