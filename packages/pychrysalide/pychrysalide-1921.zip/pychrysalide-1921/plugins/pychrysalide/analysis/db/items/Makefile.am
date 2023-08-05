
noinst_LTLIBRARIES = libpychrysaanalysisdbitems.la

libpychrysaanalysisdbitems_la_SOURCES =	\
	bookmark.h bookmark.c				\
	comment.h comment.c					\
	constants.h constants.c				\
	module.h module.c					\
	switcher.h switcher.c

libpychrysaanalysisdbitems_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaanalysisdbitems_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
