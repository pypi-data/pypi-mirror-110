
noinst_LTLIBRARIES  = libanalysisstorage.la


libanalysisstorage_la_SOURCES =				\
	cache-int.h								\
	cache.h cache.c							\
	container-int.h							\
	container.h container.c					\
	serialize-int.h							\
	serialize.h serialize.c					\
	storage-int.h							\
	storage.h storage.c						\
	tpmem.h tpmem.c

libanalysisstorage_la_LIBADD = 

libanalysisstorage_la_LDFLAGS = $(LIBSSL_LIBS)


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysisstorage_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS) $(LIBSSL_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
