
noinst_LTLIBRARIES = libdwarfv4.la

libdwarfv4_la_SOURCES =					\
	checks.h checks.c

libdwarfv4_la_LDFLAGS = $(LIBGTK_LIBS)


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdwarfv4_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
