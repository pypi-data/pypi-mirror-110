
noinst_LTLIBRARIES = libpychrysaarch.la

libpychrysaarch_la_SOURCES =			\
	constants.h constants.c				\
	context.h context.c					\
	instriter.h instriter.c				\
	instruction.h instruction.c			\
	module.h module.c					\
	operand.h operand.c					\
	processor.h processor.c				\
	register.h register.c				\
	vmpa.h vmpa.c

libpychrysaarch_la_LIBADD =				\
	instructions/libpychrysaarchinstructions.la \
	operands/libpychrysaarchoperands.la

libpychrysaarch_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libpychrysaarch_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) $(LIBPYTHON_CFLAGS) $(LIBPYGOBJECT_CFLAGS) \
	-I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)

SUBDIRS = instructions operands
