# %define planex_version 0.0.0
# %define planex_release 1

Name:           gdk
Version:        331.62
Release:        1
Summary:        NVIDIA GPU development kit
Group:          Development/Other
License:        NVIDIA
URL:            https://developer.nvidia.com/gpu-deployment-kit
Source0:        http://developer.download.nvidia.com/compute/cuda/6_0/rel/gdk/gdk_331_62_release.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

%description
This package contains a header file for the NVIDIA GPU development kit.

%package        devel
Summary:        Development files for %{name}
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%setup -q -n gdk_linux_amd64_release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/usr/lib64
install -m 644 nvml/lib/libnvidia-ml.so %{buildroot}/usr/lib64/libnvidia-ml.so
install -m 644 nvml/lib/libnvidia-ml.so.1 %{buildroot}/usr/lib64/libnvidia-ml.so.1
mkdir -p %{buildroot}/usr/include
install -m 644 nvml/include/nvml.h %{buildroot}/usr/include/nvml.h

%files
%defattr(-,root,root,-)
/usr/lib64/libnvidia-ml.so
/usr/lib64/libnvidia-ml.so.1

%files          devel
%defattr(-,root,root,-)
/usr/include/nvml.h

%changelog
* Mon Nov 10 2014 John Else <john.else@citrix.com> - 331.62-1
- Initial package for planex
