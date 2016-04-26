Name:           gpumon
Version:        0.2.0
Release:        1%{?dist}
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
[ ! -x /sbin/chkconfig ] || chkconfig --add xcp-rrdd-gpumon
exit 0

%preun
# Run chkconfig --del if this is an uninstall (rather than an upgrade)
[ $1 -eq 0 ] && [ -x /sbin/chkconfig ] && chkconfig --del xcp-rrdd-gpumon
exit 0

%files
%defattr(-,root,root,-)
/etc/rc.d/init.d/xcp-rrdd-gpumon
/opt/xensource/libexec/xcp-rrdd-plugins/xcp-rrdd-gpumon

%changelog
* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 0.2.0-1
- Update to 0.2.0

* Mon Nov 10 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
