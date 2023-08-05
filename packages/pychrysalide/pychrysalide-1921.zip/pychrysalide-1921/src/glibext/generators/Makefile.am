
noinst_LTLIBRARIES  = libglibextgenerators.la

libglibextgenerators_la_SOURCES =		\
	hex.h hex.c							\
	prologue.h prologue.c				\
	rborder.h rborder.c

libglibextgenerators_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libglibextgenerators_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
