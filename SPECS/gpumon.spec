Name:           gpumon
Version:        0.3.2
Release:        1%{?dist}
Summary:        RRDD GPU metrics plugin
Group:          System/Hypervisor
License:        LGPL+linking exception
URL:            https://github.com/xenserver/gpumon
Source0:        https://github.com/xenserver/gpumon/archive/%{version}/gpumon-%{version}.tar.gz
Source1:        xcp-rrdd-gpumon.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  gdk-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-rrdd-plugin-devel
BuildRequires:  ocaml-stdext-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  ocaml-xenstore-clients-devel
%{?systemd_requires}
BuildRequires:  systemd

%description
This package contains a plugin registering to the RRD daemon and exposing GPU
metrics.

%prep
%setup -q

%build
DESTDIR=%{buildroot} %{__make}

%check
%{__make} test

%install
DESTDIR=%{buildroot} %{__make} install
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd-gpumon.service

%post
%systemd_post xcp-rrdd-gpumon.service

%preun
%systemd_preun xcp-rrdd-gpumon.service

%postun
%systemd_postun_with_restart xcp-rrdd-gpumon.service

%files
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-gpumon
%{_unitdir}/xcp-rrdd-gpumon.service

%changelog
* Thu Dec 15 2016 Rob Hoes <rob.hoes@citrix.com> - 0.3.2-1
- git: Add metadata to the result of `git archive`

* Mon Nov 21 2016 Rob Hoes <rob.hoes@citrix.com> - 0.3.0-3
- Install systemd service files with 644 permissions (non-executable)

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 0.3.0-2
- Package for systemd

* Tue Aug 16 2016 Christian Lindig <christian.lindig@citrix.com> - 0.3.0-1
- Update to 0.3.0 for new upstream release

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.2.0-2
- Re-run chkconfig on upgrade
- Stop service on uninstall

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.2.0-1
- Update to 0.2.0

* Mon Nov 10 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
