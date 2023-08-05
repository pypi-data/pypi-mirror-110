
noinst_LTLIBRARIES = libpychrysaglibext.la

libpychrysaglibext_la_SOURCES =			\
	constants.h constants.c				\
	binarycursor.h binarycursor.c		\
	binportion.h binportion.c			\
	buffercache.h buffercache.c			\
	bufferline.h bufferline.c			\
	bufferview.h bufferview.c			\
	configuration.h configuration.c		\
	linecursor.h linecursor.c			\
	linegen.h linegen.c					\
	loadedpanel.h loadedpanel.c			\
	module.h module.c					\
	named.h named.c						\
	singleton.h singleton.c

libpychrysaglibext_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaglibext_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
