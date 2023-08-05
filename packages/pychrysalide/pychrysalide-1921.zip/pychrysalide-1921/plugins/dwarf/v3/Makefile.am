
noinst_LTLIBRARIES = libdwarfv3.la

libdwarfv3_la_SOURCES =					\
	checks.h checks.c

libdwarfv3_la_LDFLAGS = $(LIBGTK_LIBS)


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdwarfv3_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
