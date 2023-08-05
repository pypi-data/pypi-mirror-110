
noinst_LTLIBRARIES  = libanalysishuman.la


libanalysishuman_la_SOURCES =			\
	lang-int.h							\
	lang.h lang.c

libanalysishuman_la_LIBADD =			\
	asm/libanalysishumanasm.la

libanalysishuman_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysishuman_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = asm
