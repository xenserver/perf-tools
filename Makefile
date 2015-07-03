DIST?=.el7.centos
MOCK=planex-cache --cachedirs=/rpmcache
FETCH_EXTRA_FLAGS=--mirror file:///distfiles/ocaml2

include /usr/share/planex/Makefile.rules

