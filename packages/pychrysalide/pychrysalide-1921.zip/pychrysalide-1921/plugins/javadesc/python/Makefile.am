
noinst_LTLIBRARIES = libjavadescpython.la

libjavadescpython_la_SOURCES =			\
	demangler.h demangler.c				\
	module.h module.c

libjavadescpython_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libjavadescpython_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src -DNO_IMPORT_PYGOBJECT

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
