
noinst_LTLIBRARIES  = libanalysis.la

libanalysis_la_SOURCES =				\
	binary.h binary.c					\
	block-int.h							\
	block.h block.c						\
	cattribs.h cattribs.c				\
	content-int.h						\
	content.h content.c					\
	loaded-int.h						\
	loaded.h loaded.c					\
	loading.h loading.c					\
	project.h project.c					\
	routine-int.h						\
	routine.h routine.c					\
	type-int.h							\
	type.h type.c						\
	variable.h variable.c

libanalysis_la_LIBADD =					\
	contents/libanalysiscontents.la		\
	db/libanalysisdb.la					\
	disass/libanalysisdisass.la			\
	human/libanalysishuman.la			\
	storage/libanalysisstorage.la		\
	types/libanalysistypes.la

libanalysis_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysis_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = contents db disass human storage types
