Name:           kdeplasma-addons
Version:        5.2.0
Release:        1%{?dist}
Summary:        Additional Plasmoids for Plasma 5.

License:        GPLv2+
URL:            http://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

Obsoletes:      kdeplasma-addons-libs < 5.0.0
Provides:       kdeplasma-addons-libs = %{version}-%{release}
Provides:       kdeplasma-addons-libs%{?dist} = %{version}-%{release}


BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-krunner-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kdelibs4support-devel


BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel

BuildRequires:  ibus-devel
BuildRequires:  scim-devel

Requires:       kf5-filesystem

%description
%{summary}.

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
%find_lang kdeplasmaaddons5_qt --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f kdeplasmaaddons5_qt.lang
%doc COPYING COPYING.LIB
%{_libexecdir}/kimpanel-scim-panel
%{_libexecdir}/kimpanel-ibus-panel
%{_kf5_datadir}/plasma/plasmoids/*
%{_kf5_datadir}/plasma/desktoptheme/default/widgets/*.svgz
%{_kf5_datadir}/plasma/wallpapers/*
%{_kf5_datadir}/plasma/services/*.operations
%{_kf5_qtplugindir}/plasma/dataengine/*.so
%{_kf5_qtplugindir}/*.so
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/kwin/*.desktop
%{_kf5_qmldir}/org/kde/plasma/*
%{_datadir}/kwin/desktoptabbox
%{_datadir}/kwin/tabbox
%{_datadir}/icons/hicolor/scalable/apps/fifteenpuzzle.svgz


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Thu Oct 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-2
- Obsoletes & Provides kdeplasma-addons-libs

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0
