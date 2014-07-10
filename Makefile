USE_BRANDING := yes
IMPORT_BRANDING := yes
include $(B_BASE)/common.mk
include $(B_BASE)/rpmbuild.mk

OPTDIR=/opt/xensource

PT_VERSION := 0.2.0
PT_LIBS    := rrdd-plugin-legacy
PT_PROGS   := xsiostat xsifstat rrd2csv rrdd-plugins gpumon
PT_TARGETS := $(PT_LIBS) $(PT_PROGS)

PT_SPECS := $(PT_TARGETS:=.spec)

GDK_TARBALL := $(CARBON_DISTFILES)/gdk_331_62_release.tgz

.PHONY: build
build: srpm $(MY_SOURCES)/MANIFEST
	mkdir -p $(RPM_RPMSDIR)/$(DOMAIN_ZERO_OPTIMIZED)
	# Build the library RPMs and install them in the chroot
	for dir in $(PT_LIBS); do \
		$(RPMBUILD) --rebuild --target $(DOMAIN0_ARCH_OPTIMIZED) $(MY_OUTPUT_DIR)/SRPMS/$$dir-$(PT_VERSION)-*.src.rpm; \
		rpm -Uvh --force $(MY_OUTPUT_DIR)/RPMS/$(DOMAIN0_ARCH_OPTIMIZED)/$$dir*-$(PT_VERSION)-*.rpm; \
	done
	# Build the RPMs we want installed on XenServer, and copy them to PACKAGES.main
	mkdir -p $(MY_MAIN_PACKAGES)
	for dir in $(PT_PROGS); do \
		($(RPMBUILD) --rebuild --target $(DOMAIN0_ARCH_OPTIMIZED) $(MY_OUTPUT_DIR)/SRPMS/$$dir-$(PT_VERSION)-*.src.rpm; \
		cp $(MY_OUTPUT_DIR)/RPMS/$(DOMAIN0_ARCH_OPTIMIZED)/$$dir-$(PT_VERSION)-*.rpm $(MY_MAIN_PACKAGES)); \
	done

$(MY_SOURCES)/MANIFEST: $(MY_OUTPUT_DIR)/SRPMS
	mkdir -p $(MY_SOURCES)
	/bin/sh ./srpms-to-manifest $(COMPONENT) $(MY_OUTPUT_DIR)/SRPMS > $@

%.spec: %.spec.in
	sed -e 's/@RPM_RELEASE@/$(shell cd $(call git_loc,$*) && git rev-list HEAD | wc -l)/g' < $< > $@
	sed -i 's/@PT_VERSION@/$(PT_VERSION)/g' $@
	sed -i "s!@OPTDIR@!$(OPTDIR)!g" $@

.PHONY: srpm
srpm: $(PT_SPECS)
	mkdir -p $(RPM_SOURCESDIR)
	cp $(GDK_TARBALL) $(RPM_SOURCESDIR)
	mkdir -p $(RPM_SRPMSDIR)
	$(foreach compspec,$^,\
		cd $(call git_loc,$(basename $(compspec))) && \
			git archive --prefix=$(basename $(compspec))-$(PT_VERSION)/ HEAD | \
			bzip2 > $(RPM_SOURCESDIR)/$(basename $(compspec))-$(PT_VERSION).tar.bz2;\
		cd - && $(RPMBUILD) --target $(DOMAIN0_ARCH_OPTIMIZED) -bs $(compspec);)
