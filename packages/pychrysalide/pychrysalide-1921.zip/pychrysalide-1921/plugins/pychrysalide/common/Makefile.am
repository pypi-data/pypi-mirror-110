
noinst_LTLIBRARIES = libpychrysacommon.la

libpychrysacommon_la_SOURCES =			\
	bits.h bits.c						\
	fnv1a.h fnv1a.c						\
	hex.h hex.c							\
	leb128.h leb128.c					\
	module.h module.c					\
	packed.h packed.c					\
	pathname.h pathname.c				\
	pearson.h pearson.c

libpychrysacommon_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysacommon_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
