Name:           kscreenlocker
Version:        5.4.90
Release:        1%{?dist}
Summary:        Library and components for secure lock screen architecture.

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/kscreenlocker

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

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

BuildRequires:	libXcursor-devel
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
%setup -q -n %{name}-%{version}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang kscreenlocker --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f kscreenlocker.lang
%license COPYING
%{_kf5_libdir}/libKScreenLocker.so.*
%{_kf5_datadir}/knotifications5/*.notifyrc
%{_kf5_datadir}/kconf_update/*
%{_libexecdir}/kcheckpass
%{_libexecdir}/kscreenlocker_greet
%{_kf5_datadir}/ksmserver
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_qtplugindir}/screenlocker_kcm.so
%{_kf5_datadir}/plasma/kcms/screenlocker_kcm/

%files devel
%{_kf5_libdir}/libKScreenLocker.so
%{_kf5_libdir}/cmake/ScreenSaverDBusInterface
%{_kf5_libdir}/cmake/KScreenLocker
%{_includedir}/KScreenLocker
%{_datadir}/dbus-1/interfaces/*.xml

%changelog
* Sun Nov 08 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.90-1
- Plasma 5.4.90
