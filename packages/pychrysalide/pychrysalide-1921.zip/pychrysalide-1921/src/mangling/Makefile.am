
noinst_LTLIBRARIES = libmangling.la

libmangling_la_SOURCES =				\
	context-int.h						\
	context.h context.c					\
	demangler-int.h						\
	demangler.h demangler.c

libmangling_la_LDFLAGS = 

libmangling_la_LIBADD = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libmangling_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
