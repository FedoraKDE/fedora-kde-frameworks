Name:           plasma-sdk
Version:        5.3.95
Release:        1%{?dist}
Summary:        Development tools for Plasma 5

License:        GPLv2+ and LGPLv2+
URL:            https://projects.kde.org/projects/extragear/sdk/plasma-sdk

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtxmlpatterns-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kdeclarative-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-knewstuff-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-ktexteditor-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kwindowsystem-devel

Requires:       kf5-filesystem

# Little lie: this package does not provide the actual plasmate tool yet (but
# eventually it will), but it still has some tools that were part of the KDE4
# plasmate package (and which are useless in Plasma 5)
Obsoletes:      plasmate < 5.2
Provides:       plasmate = %{version}-%{release}

%description
Plasma SDK contains the following tools for Plasma-related development:
    - CuttleFish - icon theme browser
    - EngineExplorer - tool to browse and interact with data engines
    - PlasmoidViewer - an isolated Plasma environment for testing applets
    - ThemeExplorer - shows all components of a widget theme

# Not avilable yet:
#    - RemoteWidgetsBrowser - browser for applets shared on network
#    - WallpaperViewer - preview a wallpaper in different form factors

# Requires unreleased KF5 kdevplatform
#    - Plasmate - simple IDE for applet development

%prep
%setup -q -n %{name}-%{version}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang plasmasdk5 --with-qt --all-name

%files -f plasmasdk5.lang
%doc COPYING COPYING.LIB
%{_bindir}/cuttlefish
%{_bindir}/plasmaengineexplorer
%{_bindir}/plasmathemeexplorer
%{_bindir}/plasmoidviewer
%{_qt5_plugindir}/ktexteditor/cuttlefishplugin.so
%{_kf5_datadir}/kpackage/genericqml/org.kde.plasma.themeexplorer
%{_kf5_datadir}/plasma/packages/org.kde.plasma.cuttlefish
%{_kf5_datadir}/plasma/shells/org.kde.plasma.plasmoidviewershell
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/applications/cuttlefish.desktop
%{_kf5_datadir}/applications/org.kde.plasma.themeexplorer.desktop

%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Tue Apr 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Initial version
