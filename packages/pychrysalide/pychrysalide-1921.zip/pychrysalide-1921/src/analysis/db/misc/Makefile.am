
noinst_LTLIBRARIES  = libanalysisdbmisc.la

libanalysisdbmisc_la_SOURCES =			\
	rlestr.h rlestr.c					\
	snapshot.h snapshot.c				\
	timestamp.h timestamp.c

libanalysisdbmisc_la_LIBADD = 

libanalysisdbmisc_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysisdbmisc_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
