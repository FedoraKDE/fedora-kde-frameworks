Name:    kscreenlocker
Version: 5.5.95
Release: 1%{?dist}
Summary: Library and components for secure lock screen architecture

License: GPLv2+
URL:     https://projects.kde.org/kscreenlocker

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

## upstream patches

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kglobalaccel-devel

BuildRequires:  kf5-kwayland-devel

BuildRequires:  libX11-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  pkgconfig(xi)

BuildRequires:  libXcursor-devel
BuildRequires:  pam-devel

Requires:       kf5-filesystem

%description
%{summary}.

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
%autosetup -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang %{name} --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%license COPYING
%{_kf5_libdir}/libKScreenLocker.so.*
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_kf5_datadir}/kconf_update/*
%{_libexecdir}/kcheckpass
%{_libexecdir}/kscreenlocker_greet
%dir %{_kf5_datadir}/ksmserver/
%{_kf5_datadir}/ksmserver/screenlocker/
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_qtplugindir}/screenlocker_kcm.so
%dir %{_kf5_datadir}/plasma/kcms/
%{_kf5_datadir}/plasma/kcms/screenlocker_kcm/

%files devel
%{_kf5_libdir}/libKScreenLocker.so
%{_kf5_libdir}/cmake/ScreenSaverDBusInterface/
%{_kf5_libdir}/cmake/KScreenLocker/
%{_includedir}/KScreenLocker/
%{_datadir}/dbus-1/interfaces/*.xml


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Wed Feb 10 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-3
- cosmetics
- pull in upstream fixes
- polish dir ownership
- enable XInput support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95
