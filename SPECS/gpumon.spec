Name:           gpumon
Version:        0.2.0
Release:        2%{?dist}
Summary:        RRDD GPU metrics plugin
Group:          System/Hypervisor
License:        LGPL+linking exception
URL:            https://github.com/xenserver/gpumon
Source0:        https://github.com/xenserver/gpumon/archive/%{version}/gpumon-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root
BuildRequires:  gdk-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-rrdd-plugin-devel
BuildRequires:  ocaml-stdext-devel
BuildRequires:  ocaml-xenstore-devel
BuildRequires:  ocaml-xenstore-clients-devel

Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
This package contains a plugin registering to the RRD daemon and exposing GPU
metrics.

%prep
%setup -q

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%check
%{__make} test

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} %{__make} install

%clean
rm -rf %{buildroot}

%post
case $1 in
  1) # install
    /sbin/chkconfig --add xcp-rrdd-gpumon
    ;;
  2) # upgrade
    /sbin/chkconfig --del xcp-rrdd-gpumon
    /sbin/chkconfig --add xcp-rrdd-gpumon
    ;;
esac

%preun
case $1 in
  0) # uninstall
    /sbin/service xcp-rrdd-gpumon stop >/dev/null 2>&1 || :
    /sbin/chkconfig --del xcp-rrdd-gpumon
    ;;
  1) # upgrade
    ;;
esac

%files
%defattr(-,root,root,-)
/etc/rc.d/init.d/xcp-rrdd-gpumon
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-gpumon

%changelog
* Mon May 16 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.2.0-1
- Re-run chkconfig on upgrade
- Stop service on uninstall

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.2.0-1
- Update to 0.2.0

* Mon Nov 10 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
