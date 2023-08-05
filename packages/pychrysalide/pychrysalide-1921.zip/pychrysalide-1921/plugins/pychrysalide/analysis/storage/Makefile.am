
noinst_LTLIBRARIES = libpychrysaanalysisstorage.la

libpychrysaanalysisstorage_la_SOURCES =		\
	cache.h cache.c							\
	container.h container.c					\
	module.h module.c						\
	serialize.h serialize.c					\
	storage.h storage.c						\
	tpmem.h tpmem.c

libpychrysaanalysisstorage_la_LIBADD = 

libpychrysaanalysisstorage_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaanalysisstorage_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
