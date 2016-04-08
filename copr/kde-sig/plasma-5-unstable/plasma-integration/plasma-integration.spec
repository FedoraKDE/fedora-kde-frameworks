Name:           plasma-integration
Summary:        Qt Platform Theme integration plugin for Plasma
Version:        5.6.0
Release:        1%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

%global majmin_ver %(echo %{version} | cut -d. -f1,2)

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcursor)

BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  pkgconfig(Qt5X11Extras)

BuildRequires:  cmake(KF5Config)
BuildRequires:  cmake(KF5ConfigWidgets)
BuildRequires:  cmake(KF5I18n)
BuildRequires:  cmake(KF5IconThemes)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5Notifications)
BuildRequires:  cmake(KF5WidgetsAddons)

BuildRequires:  cmake(KF5Wayland) >= %{majmin_ver}

Requires:       plasma-breeze >= %{majmin_ver}
Requires:       breeze-icon-theme >= %{majmin_ver}
Requires:       kde-style-breeze >= %{majmin_ver}
Requires:       plasma-workspace >= %{majmin_ver}

%description
%{summary}.


%prep
%setup -q -n %{name}-%{version}

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_flags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang plasmaintegration5 --with-qt

%files -f plasmaintegration5.lang
%doc README.md
%license COPYING.LIB COPYING.LGPL-2
%{_kf5_qtplugindir}/platformthemes/KDEPlasmaPlatformTheme.so

%changelog
* Sun Mar 20 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.6.0-1
- Plasma 5.6.0

* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Initial package
