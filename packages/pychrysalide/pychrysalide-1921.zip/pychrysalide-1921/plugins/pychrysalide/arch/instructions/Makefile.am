
noinst_LTLIBRARIES = libpychrysaarchinstructions.la

libpychrysaarchinstructions_la_SOURCES =	\
	constants.h constants.c				\
	module.h module.c					\
	raw.h raw.c							\
	undefined.h undefined.c

libpychrysaarchinstructions_la_LIBADD = 

libpychrysaarchinstructions_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaarchinstructions_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
