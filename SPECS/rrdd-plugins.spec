%define planex_version 0.0.0
%define planex_release 2

Name:           rrdd-plugins
Version:        %{planex_version}
Release:        %{planex_release}
Summary:        RRDD metrics plugins
License:        LGPL+linking exception
Group:          System/Hypervisor
URL:            https://github.com/xenserver/rrdd-plugins/
Source0:        git://github.com/xenserver/rrdd-plugins
Source1:        xcp-rrdd-plugins.service
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml
BuildRequires:  omake
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
BuildRequires:  systemd-devel

Requires:       xsifstat
Requires:       xsiostat

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

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
%{__install} -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/xcp-rrdd-plugins.service

%clean
rm -rf %{buildroot}

%post
%systemd_post xcp-rrdd-plugins.service

%preun
%systemd_preun xcp-rrdd-plugins.service

%postun
%systemd_postun_with_restart xcp-rrdd-plugins.service

%files
%defattr(-,root,root,-)
/etc/logrotate.d/xcp-rrdd-plugins
/etc/sysconfig/xcp-rrdd-plugins
/opt/xensource/libexec/xcp-rrdd-plugins-init
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-iostat
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-xenpm
/etc/xensource/bugtool/xcp-rrdd-plugins.xml
/etc/xensource/bugtool/xcp-rrdd-plugins/stuff.xml
%{_unitdir}/xcp-rrdd-plugins.service

%changelog
* Wed Mar 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.1.0-2
- Package for systemd

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
