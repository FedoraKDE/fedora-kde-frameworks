
Name:    muon
Summary: KDE and Plasma resources management GUI
Version: 5.5.95
Release: 1%{?dist}

License: GPLv2+
URL:     https://projects.kde.org/discover

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/discover-%{version}.tar.xz

## upstream patches
Patch0:  0001-org-kde-discover-desktop-validation-fixes.patch

BuildRequires: appstream-qt-devel >= 0.8.4
BuildRequires: cmake
BuildRequires: desktop-file-utils
BuildRequires: extra-cmake-modules
BuildRequires: gettext
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
BuildRequires: kf5-rpm-macros
BuildRequires: kf5-solid-devel
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
KDE and Plasma resources management GUI.

%package libs
Summary: Runtime libraries for %{name}
Requires: PackageKit
%description libs
%{summary}.

%package discover
Summary: KDE and Plasma resources management GUI
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
%autosetup -p1 -n discover-%{version}

# disable update notifier applet by default
sed -i \
  -e 's|X-KDE-PluginInfo-EnabledByDefault=.*|X-KDE-PluginInfo-EnabledByDefault=false|g' \
  notifier/plasmoid/metadata.desktop

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

%find_lang libdiscover --with-qt
%find_lang plasma-discover --with-qt
%find_lang plasma-discover-notifier --with-qt
%find_lang plasma-discover-updater --with-qt
%find_lang plasma-discover-exporter --with-qt
%find_lang plasma_applet_org.kde.muonnotifier

cat plasma-discover-notifier.lang >> plasma-discover-updater.lang
cat plasma-discover-exporter.lang >> plasma-discover-updater.lang
cat plasma_applet_org.kde.muonnotifier.lang >> plasma-discover-updater.lang


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/plasma-discover-updater.desktop
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

%files discover -f plasma-discover.lang
%{_bindir}/plasma-discover
%{_datadir}/applications/org.kde.discover.desktop
%{_datadir}/icons/hicolor/*/apps/plasmadiscover.*
%{_datadir}/plasmadiscover/
%{_datadir}/kxmlgui5/plasmadiscover/

%files updater -f plasma-discover-updater.lang
%{_bindir}/plasma-discover-updater
%{_datadir}/applications/plasma-discover-updater.desktop
%{_datadir}/kxmlgui5/plasmadiscoverupdater/
# notifier
%{_datadir}/plasma/plasmoids/org.kde.discovernotifier/
%{_datadir}/kservices5/plasma-applet-org.kde.discovernotifier.desktop

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs -f libdiscover.lang
%license COPYING COPYING.LIB
%{_libdir}/libDiscoverNotifiers.so
%{_libdir}/libDiscoverCommon.so
%{_datadir}/libdiscover/
%{_kf5_qtplugindir}/discover/
%{_qt5_prefix}/qml/org/kde/discover/
%{_qt5_prefix}/qml/org/kde/discovernotifier/
%{_datadir}/knotifications5/discoverabstractnotifier.notifyrc


%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Tue Dec 29 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-2
- update description, summary, url
- -updater: disable updater plasmoid by default

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Sun Dec 13 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- rebuild (appstream)

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

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

