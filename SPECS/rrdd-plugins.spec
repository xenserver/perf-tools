Name:           rrdd-plugins
Version:        1.0.1
Release:        4%{?dist}
Summary:        RRDD metrics plugins
License:        LGPL+linking exception
Group:          System/Hypervisor
URL:            https://github.com/xenserver/rrdd-plugins/
Source0:        https://github.com/xenserver/rrdd-plugins/archive/%{version}/rrdd-plugins-%{version}.tar.gz
Patch0:         HFX-1989-CA-248332-Fix-race-condition-in-iostat.patch
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
Requires:       xsifstat
Requires:       xsiostat

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
This package contains plugins registering to the RRD daemon and exposing
various metrics.

%prep
%setup -q
%patch0 -p1

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} %{__make} install

%clean
rm -rf %{buildroot}

%post
case $1 in
  1) # install
    /sbin/chkconfig --add xcp-rrdd-plugins
    ;;
  2) # upgrade
    /sbin/chkconfig --del xcp-rrdd-plugins
    /sbin/chkconfig --add xcp-rrdd-plugins
    ;;
esac

%preun
case $1 in
  0) # uninstall
    /sbin/service xcp-rrdd-plugins stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xcp-rrdd-plugins
    ;;
  1) # upgrade
    ;;
esac

%files
%defattr(-,root,root,-)
/etc/logrotate.d/xcp-rrdd-plugins
/etc/rc.d/init.d/xcp-rrdd-plugins
/etc/sysconfig/xcp-rrdd-plugins
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-iostat
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-squeezed
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-xenpm
/etc/xensource/bugtool/xcp-rrdd-plugins.xml
/etc/xensource/bugtool/xcp-rrdd-plugins/stuff.xml

%changelog
* Tue Sep 19 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 1.0.1-4
- HFX-1989: Add patch for backporting fix for CA-248332: Fix race
  condition in iostat while updating VDI-to-VM map

* Mon Sep 18 2017 Frederico Mazzone <frederico.mazzone@citrix.com> - 1.0.1-3
- HFX-1986: Compile against new xen-api-libs-transitional which
  contains the fix for CA-245559

* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.1-2
- Re-run chkconfig on upgrade
- Stop service on uninstall

* Mon May 16 2016 John Else <john.else@citrix.com> - 1.0.1-1
- Update to 1.0.1

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
