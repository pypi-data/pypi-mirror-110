
noinst_LTLIBRARIES = libarch.la

libarch_la_SOURCES =					\
	archbase.h archbase.c				\
	context-int.h						\
	context.h context.c					\
	instriter.h instriter.c				\
	instruction-int.h					\
	instruction.h instruction.c			\
	link.h link.c						\
	meta.h meta.c						\
	operand-int.h						\
	operand.h operand.c					\
	post.h post.c						\
	processor-int.h						\
	processor.h processor.c				\
	register-int.h						\
	register.h register.c				\
	storage.h storage.c					\
	vmpa.h vmpa.c

libarch_la_LIBADD =						\
	instructions/libarchinstructions.la	\
	operands/libarchoperands.la

libarch_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=core/%)

dev_HEADERS = $(libarch_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)


SUBDIRS = instructions operands
