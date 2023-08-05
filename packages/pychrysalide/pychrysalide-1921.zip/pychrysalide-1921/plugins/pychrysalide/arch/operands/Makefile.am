
noinst_LTLIBRARIES = libpychrysaarchoperands.la

libpychrysaarchoperands_la_SOURCES =	\
	constants.h constants.c				\
	feeder.h feeder.c					\
	immediate.h immediate.c				\
	module.h module.c					\
	proxy.h proxy.c						\
	register.h register.c				\
	rename.h rename.c					\
	target.h target.c					\
	targetable.h targetable.c

libpychrysaarchoperands_la_LIBADD = 

libpychrysaarchoperands_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaarchoperands_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
