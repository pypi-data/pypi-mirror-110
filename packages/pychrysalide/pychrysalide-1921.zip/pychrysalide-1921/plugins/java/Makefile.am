
noinst_LTLIBRARIES = libformatjava.la

libformatjava_la_SOURCES =				\
	java-int.h java-int.c				\
	java.h java.c						\
	java_def.h							\
	pool.h pool.c


# libformatjava_la_SOURCES =				\
# 	attribute.h attribute.c				\
# 	e_java.h e_java.c					\
# 	field.h field.c						\
# 	java-int.h							\
# 	method.h method.c					\
# 	pool.h pool.c

libformatjava_la_LDFLAGS = 


devdir = $(includedir)/chrysalide/$(subdir:src/%=%)

dev_HEADERS = $(libformatjava_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS)

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
