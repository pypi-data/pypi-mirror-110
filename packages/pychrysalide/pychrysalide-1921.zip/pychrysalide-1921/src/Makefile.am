
lib_LTLIBRARIES = libchrysacore.la

bin_PROGRAMS = chrysalide chrysalide-hub



############################################################
# Bibliothèque dynamique
############################################################

#--- libchrysacore

if TRACK_GOBJECT_LEAKS

GOBJECT_LEAKS_SOURCES = gleak.h gleak.c

endif

libchrysacore_la_SOURCES = 				\
	$(GOBJECT_LEAKS_SOURCES)

# -ldl: dladdr(), dlerror()
libchrysacore_la_LDFLAGS =					\
	-avoid-version -ldl						\
	$(LIBGTK_LIBS) $(LIBXML_LIBS)			\
	$(LIBSQLITE_LIBS) $(LIBARCHIVE_LIBS)

libchrysacore_la_LIBADD =				\
	analysis/libanalysis.la				\
	arch/libarch.la						\
	common/libcommon.la					\
	core/libcore.la						\
	debug/libdebug.la					\
	format/libformat.la					\
	glibext/libglibext.la				\
	gtkext/libgtkext.la					\
	gui/libgui.la						\
	mangling/libmangling.la				\
	plugins/libplugins.la



############################################################
# Programme principal
############################################################

EXTRA_chrysalide_DEPENDENCIES = $(lib_LTLIBRARIES)

chrysalide_SOURCES = 					\
	main.c


AM_CPPFLAGS = -I$(top_srcdir) -I$(top_srcdir)/intl $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) `pkg-config --cflags gthread-2.0` $(LIBPYTHON_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)


chrysalide_LDFLAGS = $(LIBGTK_LIBS) -L/usr/X11R6/lib -ldl -lm $(LIBXML_LIBS) `pkg-config --libs gthread-2.0` $(LIBPYTHON_LIBS) $(LIBARCHIVE_LIBS) $(LIBSQLITE_LIBS) \
	-L.libs -lchrysacore


chrysalide_LDADD = $(LIBINTL)



############################################################
# Gestionnaire de serveurs distants
############################################################

EXTRA_chrysalide_hub_DEPENDENCIES = $(lib_LTLIBRARIES)

chrysalide_hub_SOURCES =				\
	hub.c


chrysalide_hub_LDFLAGS = $(LIBGTK_LIBS) -L.libs -lchrysacore



############################################################
# Le reste du monde
############################################################

# glibext doit être traité en premier, à cause des marshals GLib

SUBDIRS = core glibext gtkext analysis arch format common debug gui mangling plugins
