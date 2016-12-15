Name:           rrd2csv
Version:        1.0.2
Release:        1%{?dist}
Summary:        Tool for converting Xen API RRDs to CSV
License:        LGPL+linking exception
Group:          System/Hypervisor
URL:            https://github.com/xenserver/rrd2csv/
Source0:        https://github.com/xenserver/rrd2csv/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}
BuildRequires:  ocaml
BuildRequires:  omake
BuildRequires:  ocaml-xcp-idl-devel
BuildRequires:  xapi-client-devel
BuildRequires:  ocaml-xen-api-libs-transitional-devel
BuildRequires:  ocaml-xcp-rrd-devel

%description
This package contains the rrd2csv tool, useful to expose live RRDD metrics on
standard output, in the CSV format.

%prep
%setup -q

%build
mkdir -p %{buildroot}
DESTDIR=%{buildroot} %{__make}

%install
rm -rf %{buildroot}
DESTDIR=%{buildroot} %{__make} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/opt/xensource/bin/rrd2csv
/opt/xensource/man/man1/rrd2csv.1.man

%changelog
* Thu Dec 15 2016 Rob Hoes <rob.hoes@citrix.com> - 1.0.2-1
- git: Add metadata to the result of `git archive`

* Tue Aug 16 2016 Christian Lindig <christian.lindig@citrix.com> - 1.0.1-1
- Bump version to track new upstream release

* Tue Apr 26 2016 Si Beaumont <simon.beaumont@citrix.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 11 2014 John Else <john.else@citrix.com> - 0.1.0-1
- Initial package for planex
