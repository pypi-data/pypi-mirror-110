
noinst_LTLIBRARIES = libpychrysacore.la

libpychrysacore_la_SOURCES =			\
	constants.h constants.c				\
	demanglers.h demanglers.c			\
	global.h global.c					\
	logs.h logs.c						\
	module.h module.c					\
	params.h params.c					\
	processors.h processors.c			\
	queue.h queue.c

libpychrysacore_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysacore_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
