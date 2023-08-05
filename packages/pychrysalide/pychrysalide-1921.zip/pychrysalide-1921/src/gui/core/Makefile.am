
BUILT_SOURCES = resources.h resources.c

noinst_LTLIBRARIES = libguicore.la

RES_FILES =								\
	../../../pixmaps/palette.png		\
	../../../pixmaps/collapse.png		\
	../../../pixmaps/collapse_dark.png	\
	../../../pixmaps/expand.png			\
	../../../pixmaps/expand_dark.png	\
	../../../pixmaps/snapshot.png		\
	../../../pixmaps/snapshot_current.png

libguicore_la_SOURCES =					\
	core.h core.c						\
	global.h global.c					\
	items.h items.c						\
	panels.h panels.c					\
	resources.h resources.c				\
	theme.h theme.c

libguicore_la_LDFLAGS = $(LIBGTK_LIBS) $(LIBXML_LIBS)


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libguicore_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 


resources.c: gresource.xml $(RES_FILES)
	glib-compile-resources --target=$@ --sourcedir=$(srcdir) --generate-source --c-name gui_core gresource.xml

resources.h: gresource.xml
	glib-compile-resources --target=$@ --sourcedir=$(srcdir) --generate-header --c-name gui_core gresource.xml


CLEANFILES = resources.h resources.c

EXTRA_DIST = gresource.xml $(RES_FILES)
