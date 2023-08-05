
noinst_LTLIBRARIES  = libanalysisdbitems.la

libanalysisdbitems_la_SOURCES =			\
	bookmark.h bookmark.c				\
	comment.h comment.c					\
	move.h move.c						\
	switcher.h switcher.c

libanalysisdbitems_la_LIBADD =	

libanalysisdbitems_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysisdbitems_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
