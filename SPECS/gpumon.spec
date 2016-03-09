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
Source1:        init.d-rrdd-gpumon
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
%{__install} -D -m 0755 %{SOURCE1} %{buildroot}etc/rc.d/init.d/xcp-rrdd-gpumon

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
* Mon Nov 10 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
