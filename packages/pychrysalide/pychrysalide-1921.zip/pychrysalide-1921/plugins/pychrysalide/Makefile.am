
DEFAULT_INCLUDES = -I$(top_builddir) -idirafter.

lib_LTLIBRARIES = pychrysalide.la

libdir = $(pluginslibdir)


if BUILD_PYTHON_PACKAGE

RUN_PATH = -Wl,-rpath,'$$ORIGIN/chrysalide-libs'

endif


pychrysalide_la_SOURCES =				\
	access.h access.c					\
	core.h core.c						\
	helpers.h helpers.c					\
	star.h star.c						\
	strenum.h strenum.c					\
	struct.h struct.c					\
	weak.h weak.c

pychrysalide_la_LIBADD =				\
	analysis/libpychrysaanalysis.la		\
	arch/libpychrysaarch.la				\
	common/libpychrysacommon.la			\
	core/libpychrysacore.la				\
	debug/libpychrysadebug.la			\
	format/libpychrysaformat.la			\
	glibext/libpychrysaglibext.la		\
	gtkext/libpychrysagtkext.la			\
	gui/libpychrysagui.la				\
	mangling/libpychrysamangling.la		\
	plugins/libpychrysaplugins.la

# -ldl: dladdr(), dlerror()
pychrysalide_la_LDFLAGS =					\
	-module -avoid-version -ldl				\
	$(LIBPYTHON_LIBS) $(LIBPYGOBJECT_LIBS)	\
	-L$(top_srcdir)/src/.libs -lchrysacore	\
	$(RUN_PATH)


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(pychrysalide_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = analysis arch common core debug format glibext gtkext gui mangling plugins
