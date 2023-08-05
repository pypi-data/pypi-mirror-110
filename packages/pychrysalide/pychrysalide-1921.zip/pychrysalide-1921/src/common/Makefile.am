
noinst_LTLIBRARIES = libcommon.la

libcommon_la_SOURCES =					\
	alloc.h alloc.c						\
	array.h array.c						\
	asm.h asm.c							\
	bconst.h							\
	bits.h bits.c						\
	compression.h compression.c			\
	cpp.h								\
	dllist.h dllist.c					\
	endianness.h endianness.c			\
	environment.h environment.c			\
	extstr.h extstr.c					\
	hex.h hex.c							\
	ibuf.h ibuf.c						\
	io.h io.c							\
	fnv1a.h fnv1a.c						\
	leb128.h leb128.c					\
	macros.h							\
	net.h net.c							\
	packed.h packed.c					\
	pathname.h pathname.c				\
	pearson.h pearson.c					\
	shuffle.h shuffle.c					\
	sort.h sort.c						\
	sqlite.h sqlite.c					\
	utf8.h utf8.c						\
	xdg.h xdg.c							\
	xml.h xml.c

libcommon_la_LDFLAGS = $(LIBGTK_LIBS) $(LIBXML_LIBS)


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libcommon_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
