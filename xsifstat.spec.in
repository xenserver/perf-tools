%define planex_version 0.0.0
%define planex_release 1

Name:           xsifstat
Version:        %{planex_version}
Release:        %{planex_release}
Summary:        Tool for visualising XenServer VIF metrics
License:        LGPL+linking exception
Group:          Development/Other
URL:            https://github.com/xenserver/xsifstat/
Source0:        git://github.com/xenserver/xsifstat
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
* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.2.0-1
- Initial package for planex
