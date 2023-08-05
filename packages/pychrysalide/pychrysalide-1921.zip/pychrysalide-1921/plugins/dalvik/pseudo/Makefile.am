
noinst_LTLIBRARIES = libdalvikpseudo.la

libdalvikpseudo_la_SOURCES =			\
	fill.h fill.c						\
	identifiers.h						\
	switch.h switch.c

libdalvikpseudo_la_LIBADD = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdalvikpseudo_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
