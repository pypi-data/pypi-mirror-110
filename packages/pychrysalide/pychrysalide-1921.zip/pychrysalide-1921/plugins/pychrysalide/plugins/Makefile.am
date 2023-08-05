
noinst_LTLIBRARIES = libpychrysaplugins.la

libpychrysaplugins_la_SOURCES =			\
	constants.h constants.c				\
	plugin.h plugin.c					\
	module.h module.c					\
	translate.h translate.c

libpychrysaplugins_la_LIBADD = 

libpychrysaplugins_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaplugins_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
