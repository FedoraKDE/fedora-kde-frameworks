# libksysguard
%define framework ksysguard

Name:           kf5-%{framework}
Version:        5.1.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 addon for process management

License:        GPLv2+
URL:            http://www.kde.org


%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/libksysguard-%{version}.tar.xz

Patch0:		ksysguard-framework-libs-names.patch

BuildRequires:  zlib-devel
BuildRequires:  libXres-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-knewstuff-devel

Requires:       kf5-filesystem

%description
KSysGuard library provides API to read and manage processes
running on the system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n libksysguard-%{version}

%patch0 -p1 -b .libsnames

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DINCLUDE_INSTALL_DIR=%{_kf5_includedir}
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang ksysguard_qt5 --with-qt --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f ksysguard_qt5.lang
%doc COPYING.LIB
%{_kf5_libdir}/libKF5LsofUi.so.*
%{_kf5_libdir}/libKF5ProcessUi.so.*
%{_kf5_libdir}/libKF5ProcessCore.so.*
%{_kf5_libdir}/libKF5SignalPlotter.so.*
%{_kf5_libdir}/libKF5SGrd.so.*
%{_kf5_datadir}/ksysguard

%files devel
%{_kf5_includedir}/ksysguard
%{_kf5_libdir}/libKF5LsofUi.so
%{_kf5_libdir}/libKF5ProcessUi.so
%{_kf5_libdir}/libKF5ProcessCore.so
%{_kf5_libdir}/libKF5SignalPlotter.so
%{_kf5_libdir}/libKF5SGrd.so
%{_kf5_libdir}/cmake/KF5SysGuard

%changelog
* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-2.20140611git887e946
- Update to latest git snapshot


* Sat May 17 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-2.20140514git87ae01f
- Fix Source

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-2.20140611gitf7a2bbe
- Update to latest git snapshot

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1.20140425git1908ec8
- Initial package
