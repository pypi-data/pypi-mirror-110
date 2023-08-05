
lib_LTLIBRARIES = libyaml.la

libdir = $(pluginslibdir)


if BUILD_PYTHON_PACKAGE

RUN_PATH = -Wl,-rpath,'$$ORIGIN/../chrysalide-libs'

endif

if BUILD_PYTHON3_BINDINGS

PYTHON3_LIBADD = python/libyamlpython.la

if BUILD_DISCARD_LOCAL

if BUILD_PYTHON_PACKAGE
PYTHON3_RUN_PATH = -Wl,-rpath,'$$ORIGIN/..'
else
PYTHON3_RUN_PATH = -Wl,-rpath,'$$ORIGIN'
endif

else

PYTHON3_RUN_PATH = -Wl,-rpath,$(abs_top_srcdir)/plugins/pychrysalide/.libs

endif

PYTHON3_LDFLAGS = $(PYTHON3_RUN_PATH) -L$(top_srcdir)/plugins/pychrysalide/.libs -l:pychrysalide.so

PYTHON3_SUBDIRS = python

endif


libyaml_la_SOURCES =						\
	collection.h collection.c				\
	core.h core.c							\
	line.h line.c							\
	node-int.h								\
	node.h node.c							\
	pair.h pair.c							\
	reader.h reader.c						\
	scalar.h scalar.c						\
	tree.h tree.c

libyaml_la_LIBADD =							\
	$(PYTHON3_LIBADD)

libyaml_la_LDFLAGS =						\
	-avoid-version							\
	-L$(top_srcdir)/src/.libs -lchrysacore	\
	$(RUN_PATH) $(PYTHON3_LDFLAGS)


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libyaml_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = $(PYTHON3_SUBDIRS)
