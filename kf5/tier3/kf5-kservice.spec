%define framework kservice

Name:           kf5-%{framework}
Version:        4.95.0
Release:        2%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for working with .desktop files

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-karchive-devel


%description
KDE Frameworks 5 Tier 3 solution for working with .desktop files


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING COPYING.LIB README.md
%{_kf5_bindir}/kbuildsycoca5
%{_kf5_libdir}/libKF5Service.so.*
%{_kf5_sysconfdir}/xdg/menus/applications.menu
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_mandir}/man8/*

%files devel
%{_kf5_includedir}/kservice_version.h
%{_kf5_includedir}/KService
%{_kf5_bindir}/desktoptojson
%{_kf5_libdir}/libKF5Service.so
%{_kf5_libdir}/cmake/KF5Service


%changelog
* Thu Jan 16 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rebuild against new kf5-filesystem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
