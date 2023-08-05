
noinst_LTLIBRARIES = libdalvikoperands.la

libdalvikoperands_la_SOURCES =			\
	args.h args.c						\
	pool.h pool.c						\
	register.h register.c


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdalvikoperands_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)


SUBDIRS = 
