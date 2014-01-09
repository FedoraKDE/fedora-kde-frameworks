%define framework kapidox

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module for API documentation generation

License:        GPLv3 BSD  LGPLv3 QPLv1
URL:            http://download.kde.org/
Source0:        http://download.kde.org/unstable/frameworks/${version}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

%description
KDE Frameworks 5 Tier 4 module for API documentation generation

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_kf5_datadir}/LICENSES/
%{_kf5_datadir}/doc/

%changelog
* Thu Jan 09 2014 Siddharth Sharma <siddharths@fedoraproject.org> - 4.95.0-1
- Initial Release
