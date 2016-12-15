Name:           rrdd-plugins
Version:        1.0.3
Release:        1%{?dist}
Summary:        RRDD metrics plugins
License:        LGPL+linking exception
Group:          System/Hypervisor
URL:            https://github.com/xenserver/rrdd-plugins/
Source0:        https://github.com/xenserver/rrdd-plugins/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        xcp-rrdd-iostat.service
Source2:        xcp-rrdd-squeezed.service
Source3:        xcp-rrdd-xenpm.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml
BuildRequires:  oasis
BuildRequires:  blktap-devel
BuildRequires:  forkexecd-devel
BuildRequires:  ocaml-rrdd-plugin-devel
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  xen-ocaml-devel
BuildRequires:  ocaml-xenops-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  ocaml-xcp-rrd-devel
BuildRequires:  xen-dom0-libs-devel
BuildRequires:  xen-libs-devel
%{?systemd_requires}
BuildRequires: systemd

Requires:       xsifstat
Requires:       xsiostat

%description
This package contains plugins registering to the RRD daemon and exposing
various metrics.

%prep
%setup -q

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} %{__make} install
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd-iostat.service
%{__install} -D -m 0644 %{SOURCE2} %{buildroot}%{_unitdir}/xcp-rrdd-squeezed.service
%{__install} -D -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/xcp-rrdd-xenpm.service

%clean
rm -rf %{buildroot}

%post
%systemd_post xcp-rrdd-iostat.service
%systemd_post xcp-rrdd-squeezed.service
%systemd_post xcp-rrdd-xenpm.service

%preun
%systemd_prerun xcp-rrdd-iostat.service
%systemd_prerun xcp-rrdd-squeezed.service
%systemd_prerun xcp-rrdd-xenpm.service

%postun
%systemd_postrun xcp-rrdd-iostat.service
%systemd_postrun xcp-rrdd-squeezed.service
%systemd_postrun xcp-rrdd-xenpm.service

%files
%defattr(-,root,root,-)
/etc/logrotate.d/xcp-rrdd-plugins
/etc/sysconfig/xcp-rrdd-plugins
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-iostat
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-xenpm
/etc/xensource/bugtool/xcp-rrdd-plugins.xml
/etc/xensource/bugtool/xcp-rrdd-plugins/stuff.xml
%{_unitdir}/xcp-rrdd-iostat.service
%{_unitdir}/xcp-rrdd-squeezed.service
%{_unitdir}/xcp-rrdd-xenpm.service

%changelog
* Wed Oct 19 2016 Euan Harris <euan.harris@citrix.com> - 1.0.3-1
- Remove final vestiges of previous init system

* Mon Aug 22 2016 Rafal Mielniczuk <rafal.mielniczuk@citrix.com> - 1.0.2-2
- Package for systemd

* Tue Aug 16 2016 Christian Lindig <christian.lindig@citrix.com> - 1.0.2-1
- Update to 1.0.2
- Bump version to match new upstream version

* Mon May 16 2016 John Else <john.else@citrix.com> - 1.0.1-3
- Update to 1.0.1
- Bump release to 3 for upgrade against old versions

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-2
- Re-run chkconfig on upgrade
- Stop service on uninstall

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
