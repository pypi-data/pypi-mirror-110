
noinst_LTLIBRARIES = libarmv7operands.la

libarmv7operands_la_SOURCES = 			\
	estate.h estate.c					\
	iflags.h iflags.c					\
	it.h it.c							\
	limitation.h limitation.c			\
	maccess.h maccess.c					\
	offset.h offset.c					\
	register.h register.c				\
	reglist.h reglist.c					\
	rotation.h rotation.c				\
	shift.h shift.c

libarmv7operands_la_LIBADD =


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libarmv7operands_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
