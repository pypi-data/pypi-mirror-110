
noinst_LTLIBRARIES = libarmv7registers.la

libarmv7registers_la_SOURCES = 			\
	banked.h banked.c					\
	basic.h basic.c						\
	coproc.h coproc.c					\
	simd.h simd.c						\
	special.h special.c

libarmv7registers_la_LIBADD =


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libarmv7registers_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
