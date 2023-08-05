
noinst_LTLIBRARIES  = libanalysiscontents.la

libanalysiscontents_la_SOURCES =		\
	encapsulated.h encapsulated.c		\
	file.h file.c						\
	memory.h memory.c					\
	restricted.h restricted.c

libanalysiscontents_la_LIBADD =	

libanalysiscontents_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysiscontents_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
