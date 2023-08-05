
noinst_LTLIBRARIES = libpychrysaanalysisdb.la

libpychrysaanalysisdb_la_SOURCES =		\
	admin.h admin.c						\
	analyst.h analyst.c					\
	certs.h certs.c						\
	client.h client.c					\
	collection.h collection.c			\
	constants.h constants.c				\
	item.h item.c						\
	module.h module.c					\
	server.h server.c

libpychrysaanalysisdb_la_LIBADD = 		\
	items/libpychrysaanalysisdbitems.la

libpychrysaanalysisdb_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaanalysisdb_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = items
