%global         plasma_version 5.1.0

Name:           khotkeys
Version:        5.1.0.1
Release:        1%{?dist}
Summary:        Application to show KDE Application's documentation

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/stable/plasma/%{version}/%{name}-%{version}.tar.xz

Patch0:         khotkeys-kded-install-path.patch

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kdoctools-devel

BuildRequires:  plasma-workspace-devel

BuildRequires:  libX11-devel

BuildRequires:  chrpath

Requires:       kf5-filesystem

Obsoletes:      kde-workspace < 5.0.0-1

%description
An advanced editor component which is used in numerous KDE applications
requiring a text editing component.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{plasma_version}

%patch0 -p1 -b .kded-install

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang khotkeys5 --with-qt --all-name

#chrpath --delete %{buildroot}/%{_kde5_plugindir}/kded_khotkeys.so
#chrpath --delete %{buildroot}/%{_kde5_plugindir}/kcm_hotkeys.so
#chrpath --delete %{buildroot}/%{_kde5_libdir}/libkhotkeysprivate.so.4.96.0

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f khotkeys5.lang
%doc COPYING
%{_kf5_libdir}/libkhotkeysprivate.so.*
%{_kf5_plugindir}/kded/*.so
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservices5/khotkeys.desktop
%{_datadir}/khotkeys
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/doc/HTML/en/kcontrol/khotkeys

%files devel
%{_libdir}/cmake/KHotKeysDBusInterface

%changelog
* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514gite1c386a
- Intial snapshot
