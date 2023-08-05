
noinst_LTLIBRARIES = libanalysisdisass.la

libanalysisdisass_la_SOURCES =			\
	area.h area.c						\
	block.h block.c						\
	disassembler.h disassembler.c		\
	dragon.h dragon.c					\
	fetch.h fetch.c						\
	instructions.h instructions.c		\
	limit.h limit.c						\
	links.h links.c						\
	loop.h loop.c						\
	output.h output.c					\
	rank.h rank.c						\
	routines.h routines.c

libanalysisdisass_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libanalysisdisass_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
