
noinst_LTLIBRARIES  = libanalysisdb.la


libanalysisdb_la_SOURCES =				\
	admin.h admin.c						\
	analyst.h analyst.c					\
	auth.h auth.c						\
	backend-int.h						\
	backend.h backend.c					\
	cdb.h cdb.c							\
	certs.h certs.c						\
	client-int.h						\
	client.h client.c					\
	collection-int.h					\
	collection.h collection.c			\
	controller.h controller.c			\
	item-int.h							\
	item.h item.c						\
	protocol.h							\
	server.h server.c					\
	snapshot.h snapshot.c

libanalysisdb_la_LIBADD =				\
	items/libanalysisdbitems.la			\
	misc/libanalysisdbmisc.la

libanalysisdb_la_LDFLAGS = $(LIBSSL_LIBS)


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysisdb_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBARCHIVE_CFLAGS) $(LIBSQLITE_CFLAGS) $(LIBSSL_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = items misc
