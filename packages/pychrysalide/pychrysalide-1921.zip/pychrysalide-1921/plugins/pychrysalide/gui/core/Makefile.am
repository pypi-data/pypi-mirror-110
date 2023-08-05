
noinst_LTLIBRARIES = libpychrysaguicore.la

libpychrysaguicore_la_SOURCES =			\
	global.h global.c					\
	items.h items.c						\
	module.h module.c					\
	panels.h panels.c

libpychrysaguicore_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaguicore_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
