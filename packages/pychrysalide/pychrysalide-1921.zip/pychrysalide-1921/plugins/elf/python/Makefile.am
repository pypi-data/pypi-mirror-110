
noinst_LTLIBRARIES = libelfpython.la

libelfpython_la_SOURCES =				\
	constants.h constants.c				\
	dynamic.h dynamic.c					\
	elf_def.h elf_def.c					\
	format.h format.c					\
	module.h module.c					\
	program.h program.c					\
	section.h section.c					\
	translate.h translate.c

libelfpython_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libelfpython_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src -DNO_IMPORT_PYGOBJECT

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
