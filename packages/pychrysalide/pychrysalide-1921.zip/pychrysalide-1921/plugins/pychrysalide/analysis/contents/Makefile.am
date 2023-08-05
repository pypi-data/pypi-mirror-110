
noinst_LTLIBRARIES = libpychrysaanalysiscontents.la

libpychrysaanalysiscontents_la_SOURCES = \
	encapsulated.h encapsulated.c		\
	file.h file.c						\
	memory.h memory.c					\
	module.h module.c					\
	restricted.h restricted.c

libpychrysaanalysiscontents_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaanalysiscontents_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
