%define planex_version 0.0.0
%define planex_release 1

Name:           xsiostat
Version:        %{planex_version}
Release:        %{planex_release}
Summary:        Tool for visualising XenServer VBD metrics
License:        LGPL+linking exception
Group:          Development/Other
URL:            https://github.com/xenserver/xsiostat/
Source0:        git://github.com/xenserver/xsiostat
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

%description
The xsiostat is a tool similar to iostat but that consider XenServer components
such as I/O rings and memory pool buffers.

%prep 
%setup -q

%build
mkdir %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot}/opt/xensource/debug %{__make} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/xensource/debug/xsiostat

%changelog
* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.3.0-1
- Initial package for planex
