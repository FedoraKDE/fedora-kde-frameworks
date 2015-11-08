
Name:    muon
Summary: A collection of package management tools for KDE
Version: 5.4.90
Release: 1%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/projects/kde/workspace/muon
Source0: http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

## upstream patches
Patch0:  0001-org-kde-discover-desktop-validation-fixes.patch

BuildRequires: appstream-qt-devel >= 0.8.4
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: extra-cmake-modules
BuildRequires: kf5-karchive-devel
BuildRequires: kf5-kconfig-devel
BuildRequires: kf5-kconfigwidgets-devel
BuildRequires: kf5-kcoreaddons-devel
BuildRequires: kf5-kdbusaddons-devel
BuildRequires: kf5-kdeclarative-devel
BuildRequires: kf5-ki18n-devel
BuildRequires: kf5-kiconthemes-devel
BuildRequires: kf5-kio-devel
BuildRequires: kf5-kitemviews-devel
BuildRequires: kf5-knewstuff-devel
BuildRequires: kf5-knotifications-devel
BuildRequires: kf5-ktextwidgets-devel
BuildRequires: kf5-kwallet-devel
BuildRequires: kf5-kwidgetsaddons-devel
BuildRequires: kf5-plasma-devel
BuildRequires: kf5-solid-devel
BuildRequires: kf5-rpm-macros
BuildRequires: pkgconfig(packagekitqt5)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: pkgconfig(Qt5Concurrent)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5QuickWidgets)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5Test)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)

Requires: %{name}-discover = %{version}-%{release}
Requires: %{name}-updater = %{version}-%{release}

%description
A collection of package management tools for KDE.

%package libs
Summary: Runtime libraries for %{name}
Requires: PackageKit
%description libs
%{summary}.

%package discover
Summary: Muon Discover
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description discover
%{summary}.

%package updater
Summary: Muon Updater
Provides: %{name}-notifier = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description updater
%{summary}.


%prep
%autosetup -p1

## unpackaged files, these bits are not currently shipped
rm -fv po/*/muon.po
rm -fv po/*/muon-installer.po
rm -fv po/*/muon-exporter.po


%build
mkdir %{_target_platform}
pushd %{_target_platform}
# hack to avoid unused-direct-shlib-dependency rpmlint warnings
#export LDFLAGS="-Wl,--as-needed %{?__global_ldflags}"
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%find_lang libmuon
%find_lang muon-discover
%find_lang muon-notifier
%find_lang muon-updater
%find_lang plasma_applet_org.kde.muonnotifier

cat muon-notifier.lang >> muon-updater.lang
cat plasma_applet_org.kde.muonnotifier.lang >> muon-updater.lang

## unpackaged files
rm -fv %{buildroot}%{_libdir}/libmuonprivate.so

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/muon-updater.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.discover.desktop


%files
# empty metapackage

%post discover
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun discover
if [ $1 -eq 0 ] ; then
touch --no-create     %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q 2> /dev/null ||:
fi

%posttrans discover
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
update-desktop-database -q 2> /dev/null ||:

%files discover -f muon-discover.lang
%{_bindir}/muon-discover
%{_datadir}/applications/org.kde.discover.desktop

%{_datadir}/icons/hicolor/*/apps/muondiscover.*
%{_datadir}/muondiscover/
%{_datadir}/kxmlgui5/muondiscover/
%{_datadir}/desktoptheme/muon-contenttheme/

%files updater -f muon-updater.lang
%{_bindir}/muon-updater
%{_datadir}/applications/muon-updater.desktop
%{_datadir}/kxmlgui5/muonupdater/
# notifier
%{_datadir}/plasma/plasmoids/org.kde.muonnotifier/
%{_datadir}/kservices5/plasma-applet-org.kde.muonnotifier.desktop

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f libmuon.lang
%doc README
%license COPYING
%{_libdir}/libMuonNotifiers.so
%{_libdir}/libMuonCommon.so
%{_datadir}/libmuon/
%{_kf5_qtplugindir}/muon/
%dir %{_kf5_qtplugindir}/muon-notifier/
%{_kf5_qtplugindir}/muon-notifier/MuonPackageKitNotifier.so
%{_qt5_prefix}/qml/org/kde/muon/
%{_qt5_prefix}/qml/org/kde/muonnotifier/
%{_datadir}/knotifications5/muonabstractnotifier.notifyrc


%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Tue Nov 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- more upstream fixes

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- rebuild (PackageKit-Qt)

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- -libs: (explicitly) Requires: PackageKit

* Wed Oct 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- backport fix package removal (kde#354415)

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Tue Sep 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- pull in upstream fixes (notably discover .desktop rename)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- rebuild (appstream)

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- rebuild (appstream)

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- BR: kf5-kiconthemes-devel kf5-kio-devel kf5-kitemviews-devel

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Daniel Vrátil <dvratil@redhat.com> 5.3.1-1
- Plasma 5.3.1

* Sun May 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-1
- 5.3.0

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- -discover, -updater, -libs subpkgs (w/ main metapackage)

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-1
- 5.2.2, %%license COPYING

* Tue Mar 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- fix .desktop validation errors

* Mon Mar 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- cleanup for review

* Mon Mar 16 2015 Elia Devito <eliadevito@yahoo.it> 5.2.1-1
- Initial SPEC file

