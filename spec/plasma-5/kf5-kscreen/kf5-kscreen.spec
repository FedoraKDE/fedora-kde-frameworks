%global         framework kscreen

%global git_version 1e0ea14
%global git_date 20141128

Name:           kf5-%{framework}
Version:        5.1.1
Release:        1.%{git_date}git%{git_version}%{?dist}
Summary:        A Tier 3 KDE Frameworks 5 Library with API to control screen settings

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0:        http://download.kde.org/%{stable}/plasma/%{version}/libkscreen-%{version}.tar.xz
Source0:        libkscreen-%{git_version}.tar.gz

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
* Fri Nov 28 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-10.20141128git1e0ea14
- Update to latest git snapshot

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.93-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.0-2.20140611git4ab583f
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 2.0.0-2.20140611gitdda3e7d
- Initial version
