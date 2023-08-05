
noinst_LTLIBRARIES = libarchinstructions.la

libarchinstructions_la_SOURCES =		\
	raw.h raw.c							\
	undefined-int.h						\
	undefined.h undefined.c

libarchinstructions_la_LIBADD =	

libarchinstructions_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libarchinstructions_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)


SUBDIRS = 
