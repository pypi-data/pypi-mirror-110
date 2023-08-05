
BUILT_SOURCES = chrysamarshal.h chrysamarshal.c

noinst_LTLIBRARIES  = libglibext.la

libglibext_la_SOURCES =					\
	buffercache-int.h					\
	buffercache.h buffercache.c			\
	bufferline.h bufferline.c			\
	bufferview.h bufferview.c			\
	chrysamarshal.h chrysamarshal.c		\
	configuration-int.h					\
	configuration.h configuration.c		\
	delayed-int.h						\
	delayed.h delayed.c					\
	gbinarycursor.h gbinarycursor.c		\
	gbinportion-int.h					\
	gbinportion.h gbinportion.c			\
	gdisplayoptions.h gdisplayoptions.c	\
	glinecursor-int.h					\
	glinecursor.h glinecursor.c			\
	gloadedpanel-int.h					\
	gloadedpanel.h gloadedpanel.c		\
	gnhash.h gnhash.c					\
	linecolumn.h linecolumn.c			\
	linegen-int.h						\
	linegen.h linegen.c					\
	linesegment.h linesegment.c			\
	named-int.h							\
	named.h named.c						\
	objhole.h							\
	proto.h								\
	seq.h seq.c							\
	signal.h signal.c					\
	singleton.h singleton.c				\
	widthtracker.h widthtracker.c

libglibext_la_LIBADD = 					\
	generators/libglibextgenerators.la

libglibext_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libglibext_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = generators


chrysamarshal.h: chrysamarshal.list
	glib-genmarshal --header $< > $@

chrysamarshal.c: chrysamarshal.list
	echo "#include <$(subst .c,.h,$@)>" > $@
	glib-genmarshal --body $< >> $@
