
noinst_LTLIBRARIES  = libanalysistypes.la

libanalysistypes_la_SOURCES =			\
	array.h array.c						\
	basic.h basic.c						\
	cse.h cse.c							\
	encaps.h encaps.c					\
	expr.h expr.c						\
	literal.h literal.c					\
	override.h override.c				\
	proto.h proto.c						\
	template.h template.c

libanalysistypes_la_LIBADD =	

libanalysistypes_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysistypes_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = 
