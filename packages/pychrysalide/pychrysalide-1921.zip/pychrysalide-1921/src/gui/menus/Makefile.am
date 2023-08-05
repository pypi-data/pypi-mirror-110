
noinst_LTLIBRARIES  = libguimenus.la

libguimenus_la_SOURCES =				\
	binary.h binary.c					\
	debug.h debug.c						\
	edition.h edition.c					\
	file.h file.c						\
	help.h help.c						\
	options.h options.c					\
	project.h project.c					\
	view.h view.c

libguimenus_la_LDFLAGS = 

libguimenus_la_LIBADD = $(LIBINTL)


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libguimenus_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
