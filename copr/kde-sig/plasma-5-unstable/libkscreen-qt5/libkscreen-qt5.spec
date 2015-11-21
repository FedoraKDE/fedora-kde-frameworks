%global base_name    libkscreen

Name:    libkscreen-qt5
Summary: KDE display configuration library
Version: 5.4.90
Release: 1%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/workspace/libkscreen


%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz

## upstreamable patches
## upstream patches

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

Requires:       kf5-filesystem

Provides:       kf5-kscreen%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen = %{version}-%{release}
Obsoletes:      kf5-kscreen <= 1:5.2.0


%description
LibKScreen is a library that provides access to current configuration
of connected displays and ways to change the configuration.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       kf5-kscreen-devel = %{version}-%{release}
Provides:       kf5-kscreen-devel%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kscreen-devel <= 1:5.2.0
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{base_name}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING
%{_kf5_libexecdir}/kscreen_backend_launcher
%{_kf5_libdir}/libKF5Screen.so.*
%{_kf5_plugindir}/kscreen/
%{_datadir}/dbus-1/services/org.kde.kscreen.service

%files devel
%{_kf5_includedir}/KScreen/
%{_kf5_includedir}/kscreen_version.h
%{_kf5_libdir}/libKF5Screen.so
%{_kf5_libdir}/cmake/KF5Screen/
%{_libdir}/pkgconfig/kscreen2.pc
%{_kf5_archdatadir}/mkspecs/modules/qt_KScreen.pri


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- .spec cosmetics

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Thu Apr 30 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Fix Obsoletes once more

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Wed Jan 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Fix Obsoletes

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0
  (new package, forked from libkscreen)
