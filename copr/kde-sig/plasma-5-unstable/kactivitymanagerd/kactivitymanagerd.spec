Name:           kactivitymanagerd
Summary:        Plasma service to manage user's activities
Version:        5.5.95
Release:        2%{?dist}

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/%{name}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5DBus)

BuildRequires:  cmake(KF5CoreAddons)
BuildRequires:  cmake(KF5Config)
BuildRequires:  cmake(KF5WindowSystem)
BuildRequires:  cmake(KF5GlobalAccel)
BuildRequires:  cmake(KF5XmlGui)
BuildRequires:  cmake(KF5KIO)
BuildRequires:  cmake(KF5DBusAddons)
BuildRequires:  cmake(KF5I18n)


BuildRequires:  boost-devel

Requires:       kf5-filesystem

# The KActivityManagerD was split from KActivities in KF5 5.20,
# but thanks to our clever packaging kf5-kactivities package
# already contained only the KActivityManagerD files
Obsoletes:      kf5-kactivities
# Fake workaround
Provides:       kf5-kactivities = 5.100.0

%description
%{summary}.


%prep
%setup -q -n %{name}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kactivities5 --with-qt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f kactivities5.lang
%license COPYING.GPL2 COPYING.GPL3
%doc README.md
%{_kf5_bindir}/kactivitymanagerd
%{_kf5_libdir}/libkactivitymanagerd_plugin.so
%{_kf5_qtplugindir}/kactivitymanagerd/
%{_kf5_datadir}/kservices5/kactivitymanagerd.desktop
%{_kf5_datadir}/kservicetypes5/kactivitymanagerd-plugin.desktop

%changelog
* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Initial version
