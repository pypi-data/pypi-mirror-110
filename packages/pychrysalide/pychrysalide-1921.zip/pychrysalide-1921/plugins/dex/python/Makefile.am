
noinst_LTLIBRARIES = libdexpython.la

libdexpython_la_SOURCES =				\
	class.h class.c						\
	constants.h constants.c				\
	field.h field.c						\
	format.h format.c					\
	method.h method.c					\
	module.h module.c					\
	pool.h pool.c						\
	routine.h routine.c					\
	translate.h translate.c

libdexpython_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libdexpython_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src -DNO_IMPORT_PYGOBJECT

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
