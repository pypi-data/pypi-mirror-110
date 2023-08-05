
noinst_LTLIBRARIES  = libanalysishumanasm.la


libanalysishumanasm_la_SOURCES =		\
	lang.h lang.c

libanalysishumanasm_la_LIBADD = 

libanalysishumanasm_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysishumanasm_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
