%global framework plasma

Name:           kf5-%{framework}
Version:        5.13.0
Release:        0.1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 framework is foundation to build a primary user interface

License:        GPLv2+ and LGPLv2+ and BSD
URL:            https://projects.kde.org/projects/frameworks/plasma-framework

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-framework-%{version}.tar.xz

## upstream patches
# https://git.reviewboard.kde.org/r/124371

BuildRequires:  libX11-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXext-devel
BuildRequires:  libSM-devel
BuildRequires:  openssl-devel
BuildRequires:  libGL-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules >= %{version}
BuildRequires:  kf5-kactivities-devel >= %{version}
BuildRequires:  kf5-karchive-devel >= %{version}
BuildRequires:  kf5-kconfig-devel >= %{version}
BuildRequires:  kf5-kconfigwidgets-devel >= %{version}
BuildRequires:  kf5-kcoreaddons-devel >= %{version}
BuildRequires:  kf5-kdbusaddons-devel >= %{version}
BuildRequires:  kf5-kdeclarative-devel >= %{version}
BuildRequires:  kf5-kdesu-devel
BuildRequires:  kf5-kdoctools-devel >= %{version}
BuildRequires:  kf5-kglobalaccel-devel >= %{version}
BuildRequires:  kf5-kguiaddons-devel >= %{version}
BuildRequires:  kf5-ki18n-devel >= %{version}
BuildRequires:  kf5-kiconthemes-devel >= %{version}
BuildRequires:  kf5-kio-devel >= %{version}
BuildRequires:  kf5-knotifications-devel >= %{version}
BuildRequires:  kf5-kpackage-devel >= %{version}
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kservice-devel >= %{version}
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel >= %{version}
BuildRequires:  kf5-kxmlgui-devel >= %{version}
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kactivities-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kpackage-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-karchive-devel

Requires:       kf5-filesystem

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       extra-cmake-modules
Requires:       kf5-kpackage-devel
Requires:       kf5-kservice-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{framework}-framework-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang plasma5_qt --with-qt --all-name


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f plasma5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/plasmapkg2
%{_kf5_libdir}/libKF5Plasma.so.*
%{_kf5_libdir}/libKF5PlasmaQuick.so.*
%{_kf5_qmldir}/org/kde/*
%dir %{_kf5_qmldir}/QtQuick/Controls/
%dir %{_kf5_qmldir}/QtQuick/Controls/Styles/
%{_kf5_qmldir}/QtQuick/Controls/Styles/Plasma/
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/plasma/
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/plasma/
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_mandir}/man1/plasmapkg2.1*
%{_kf5_plugindir}/kded/platformstatus.so

%lang(lt) %{_datadir}/locale/lt/LC_SCRIPTS/libplasma5/*.js

%files devel
%{_kf5_libdir}/cmake/KF5Plasma/
%{_kf5_libdir}/cmake/KF5PlasmaQuick/
%{_kf5_libdir}/libKF5Plasma.so
%{_kf5_libdir}/libKF5PlasmaQuick.so
%{_kf5_includedir}/plasma_version.h
%{_kf5_includedir}/plasma/
%{_kf5_includedir}/Plasma/


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Thu Jul 16 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-2
- pull in proposed fix for renamed LookAndFeelPackage (review#124371)
- bump/sort build deps
- update URL
- polish dir ownership

* Fri Jul 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-3
- -devel: Requires: kf5-kservice-devel

* Tue May 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.10.0-2
- Panel stays light when theme is set to 'Breeze Dark' (kde#347143)

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Mon Dec 08 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- KDE Frameworks 5.4.0

* Thu Oct 23 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma Framework 5.3.1 (upstream hotfix)

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Mon Jul 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix plugin installation path

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Mon Jul 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-3
- Fix BR

* Mon Jul 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- Fixed license
- Removed old Provides/Obsoleted

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Sat Mar 15 2014 Jan Grulich <jgrulich@redhat.com 4.97.0-3.20140315git
- update git snapshot

* Wed Mar 12 2014 Jan Grulich <jgrulich@redhat.com 4.97.0-2.20140312git
- update to git snapshot

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Thu Feb 13 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1
- upgrade to Tier 3 Framework kf5-plasma

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
