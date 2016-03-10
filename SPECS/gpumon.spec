%define planex_version 0.0.0
%define planex_release 1

Name:           gpumon
Version:        %{planex_version}
Release:        %{planex_release}
Summary:        RRDD GPU metrics plugin
Group:          System/Hypervisor
License:        LGPL+linking exception
URL:            https://github.com/xenserver/gpumon
Source0:        git://github.com/xenserver/gpumon
Source1:        xcp-rrdd-gpumon.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  gdk-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-rrdd-plugin-devel
BuildRequires:  ocaml-stdext-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  ocaml-xenstore-clients-devel
BuildRequires:  systemd-devel

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

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
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd-gpumon.service

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
* Thu Mar 10 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.1.0-2
- Package for systemd

* Mon Nov 10 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
