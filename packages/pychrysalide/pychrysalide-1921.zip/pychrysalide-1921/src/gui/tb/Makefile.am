
noinst_LTLIBRARIES  = libguitb.la

libguitb_la_SOURCES =					\
	portions.h portions.c				\
	tbitem-int.h						\
	tbitem.h tbitem.c

libguitb_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libguitb_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
