%define framework kscreen

Name:           kf5-%{framework}
Version:        5.0.91
Release:        1%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library with API to control screen settings

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org
Source0:        http://download.kde.org/stable/plasma/5.0.0/libkscreen-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

Requires:       kf5-filesystem

%description
%{Summary}.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n libkscreen-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_kf5_libdir}/libKF5Screen.so.*
%{_kf5_plugindir}/kscreen/


%files devel
%{_kf5_libdir}/libKF5Screen.so
%{_kf5_libdir}/cmake/KF5Screen
%{_kf5_includedir}/KScreen
%{_kf5_includedir}/kscreen_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_KScreen.pri
%{_kf5_libdir}/pkgconfig/kscreen2.pc

%changelog
* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-2.20140611git4ab583f
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 2.0.0-2.20140611gitdda3e7d
- Initial version
