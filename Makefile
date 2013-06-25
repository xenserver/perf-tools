USE_BRANDING := yes
IMPORT_BRANDING := yes
include $(B_BASE)/common.mk
include $(B_BASE)/rpmbuild.mk

OPTDIR=/opt/xensource

PT_VERSION := 0.2.0
PT_TARGETS := xsiostat xsifstat rrd2csv rrdd-plugins

PT_SPECS := $(PT_TARGETS:=.spec)

.PHONY: build
build: srpm $(MY_SOURCES)/MANIFEST
	mkdir -p $(RPM_RPMSDIR)/$(DOMAIN_ZERO_OPTIMIZED)
	$(RPMBUILD) --rebuild --target $(DOMAIN0_ARCH_OPTIMIZED) $(MY_OUTPUT_DIR)/SRPMS/*src.rpm
	mkdir -p $(MY_MAIN_PACKAGES)
	for dir in $(PT_TARGETS); do \
		(cp $(MY_OUTPUT_DIR)/RPMS/$(DOMAIN0_ARCH_OPTIMIZED)/$$dir-$(PT_VERSION)-*.rpm $(MY_MAIN_PACKAGES)) \
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
	mkdir -p $(RPM_SRPMSDIR)
	$(foreach compspec,$^,\
		cd $(call git_loc,$(basename $(compspec))) && \
			git archive --prefix=$(basename $(compspec))-$(PT_VERSION)/ HEAD | \
			bzip2 > $(RPM_SOURCESDIR)/$(basename $(compspec))-$(PT_VERSION).tar.bz2;\
		cd - && $(RPMBUILD) --target $(DOMAIN0_ARCH_OPTIMIZED) -bs $(compspec);)
