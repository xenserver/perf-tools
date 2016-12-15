Name:           xsiostat
Version:        1.0.1
Release:        1%{?dist}
Summary:        Tool for visualising XenServer VBD metrics
License:        LGPL+linking exception
Group:          Development/Other
URL:            https://github.com/xenserver/xsiostat/
Source0:        https://github.com/xenserver/xsiostat/archive/%{version}/xsiostat-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  blktap-devel
BuildRequires:  xen-libs-devel

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
* Thu Dec 15 2016 Rob Hoes <rob.hoes@citrix.com> - 1.0.1-1
- git: Add metadata to the result of `git archive`

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.3.0-1
- Initial package for planex
