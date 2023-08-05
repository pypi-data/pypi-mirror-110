
lib_LTLIBRARIES = libfmtp.la

libdir = $(pluginslibdir)


if BUILD_PYTHON_PACKAGE

RUN_PATH = -Wl,-rpath,'$$ORIGIN/../chrysalide-libs'

endif


libfmtp_la_SOURCES =					\
	def.h								\
	parser.h parser.c

libfmtp_la_LDFLAGS =						\
	-avoid-version							\
	-L$(top_srcdir)/src/.libs -lchrysacore	\
	$(RUN_PATH)


devdir = $(includedir)/chrysalide/$(subdir)

dev_HEADERS = $(libfmtp_la_SOURCES:%c=)


AM_CPPFLAGS = $(LIBGTK_CFLAGS) $(LIBXML_CFLAGS) -I$(top_srcdir)/src

AM_CFLAGS = $(DEBUG_CFLAGS) $(WARNING_FLAGS) $(COMPLIANCE_FLAGS)
