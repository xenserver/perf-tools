Name:           xsifstat
Version:        1.0.0
Release:        1%{?dist}
Summary:        Tool for visualising XenServer VIF metrics
License:        LGPL+linking exception
Group:          Development/Other
URL:            https://github.com/xenserver/xsifstat/
Source0:        https://github.com/xenserver/xsifstat/archive/%{version}/xsifstat-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
Requires:       python

%description
The xsifstat is a tool to expose metrics of the XenServer network subsystem on
a per-VIF basis.

%prep
%setup -q

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot}/opt/xensource/debug %{__make} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/xensource/debug/xsifstat

%changelog
* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.2.0-1
- Initial package for planex
