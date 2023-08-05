
noinst_LTLIBRARIES = libformat.la

libformat_la_SOURCES =					\
	debuggable-int.h					\
	debuggable.h debuggable.c			\
	executable-int.h executable-int.c	\
	executable.h executable.c			\
	flat-int.h							\
	flat.h flat.c						\
	format-int.h						\
	format.h format.c					\
	known-int.h							\
	known.h known.c						\
	preload-int.h						\
	preload.h preload.c					\
	strsym.h strsym.c					\
	symiter.h symiter.c					\
	symbol-int.h						\
	symbol.h symbol.c

libformat_la_LIBADD = 

libformat_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libformat_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
