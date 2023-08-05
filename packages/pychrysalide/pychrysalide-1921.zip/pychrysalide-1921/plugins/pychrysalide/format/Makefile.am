
noinst_LTLIBRARIES = libpychrysaformat.la

libpychrysaformat_la_SOURCES =			\
	constants.h constants.c				\
	executable.h executable.c			\
	flat.h flat.c						\
	format.h format.c					\
	known.h known.c						\
	module.h module.c					\
	strsym.h strsym.c					\
	symbol.h symbol.c					\
	symiter.h symiter.c

libpychrysaformat_la_LIBADD = 

libpychrysaformat_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaformat_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
