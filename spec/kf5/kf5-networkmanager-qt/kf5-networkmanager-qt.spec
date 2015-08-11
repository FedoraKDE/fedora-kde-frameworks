%global framework networkmanager-qt

Name:           kf5-%{framework}
Version:        5.13.0
Release:        0.1%{?dist}
Summary:        A Tier 1 KDE Frameworks 5 module that wraps NetworkManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/frameworks/networkmanager-qt

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  pkgconfig(NetworkManager) >= 0.9.8
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
BuildRequires:  pkgconfig(libnm)
%else
BuildRequires:  pkgconfig(libnm-glib) pkgconfig(libnm-util)
%endif

Requires:       NetworkManager >= 0.9.9.0
Requires:       kf5-filesystem

# libmm-qt has been retired in F22
%if 0%{fedora} >= 22
Obsoletes:      libnm-qt < 5.10.0
Provides:       libnm-qt%{?_isa} = %{version}-%{release}
%endif

%description
A Tier 1 KDE Frameworks 5 Qt library for NetworkManager.

%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
Requires:       pkgconfig(libnm)
%else
Requires:       pkgconfig(libnm-glib) pkgconfig(libnm-util)
%endif
%if 0%{?fedora} >= 22
Obsoletes:      libnm-qt-devel < 5.10.0-1
Provides:       libnm-qt-devel%{?_isa} = %{version}-%{release}
%endif

%description    devel
Qt libraries and header files for developing applications
that use NetworkManager.

%prep
%setup -qn %{framework}-%{version}

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
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5NetworkManagerQt.so.*

%files devel
%{_kf5_libdir}/libKF5NetworkManagerQt.so
%{_kf5_libdir}/cmake/KF5NetworkManagerQt
%{_kf5_includedir}/NetworkManagerQt
%{_kf5_includedir}/networkmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_NetworkManagerQt.pri

%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Fri Jul 17 2015 Daniel Vrátil <dvratil@redhat.com> - 5.12.0-1
- KDE Frameworks 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-2
- F22+: Obsoletes/Provides libnm-qt

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Thu Apr 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-2
- -devel Requires NetworkManager

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Wed Feb 18 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Fix BR on Fedora > 21 (with NM 1.0)

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 15 2015 Jan Grulich <jgrulich@redhat.com> - 5.6.0-2
- Add generic setting
  Add minor vpn fixes

* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

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

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.91-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-3.20140611gitef654fd
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-2.20140514git107e27d
- Update to latest git snapshot

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-1.20140418git2afe13e
- Upgrade libnm-qt to a Tier 2 KDE Frameworks module kf5-networkmanagerqt

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1:0.9.9.1-1.20140403git2afe13e
- Qt 5 fork of libnm-qt
