USE_BRANDING := yes
IMPORT_BRANDING := yes
include $(B_BASE)/common.mk
include $(B_BASE)/rpmbuild.mk

OPTDIR=/opt/xensource

PT_VERSION := 0.2.0
PT_TARGETS := xsiostat xsifstat

PT_SPECS := $(PT_TARGETS:=.spec)

.PHONY: build
build: srpm $(MY_SOURCES)/MANIFEST
	mkdir -p $(RPM_RPMSDIR)/$(DOMAIN_ZERO_OPTIMIZED)
	$(RPMBUILD) --rebuild --target $(DOMAIN0_ARCH_OPTIMIZED) $(MY_OUTPUT_DIR)/SRPMS/*src.rpm
	mkdir -p $(MY_MAIN_PACKAGES)
	for dir in $(MODULES); do \
		(cp $(MY_OUTPUT_DIR)/RPM/$(DOMAIN0_ARCH_OPTIMIZED)/$$dir-*.rpm $(MY_MAIN_PACKAGES)) \
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
	cd $(call git_loc,$(basename $<)) && git archive --prefix=$(basename $<)-$(PT_VERSION)/ HEAD | \
		bzip2 > $(RPM_SOURCESDIR)/$(basename $<)-$(PT_VERSION).tar.bz2
	mkdir -p $(RPM_SRPMSDIR)
	$(RPMBUILD) --target $(DOMAIN0_ARCH_OPTIMIZED) -bs $<
