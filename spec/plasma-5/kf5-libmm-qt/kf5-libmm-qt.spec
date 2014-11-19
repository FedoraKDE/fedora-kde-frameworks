%global         framework libmm-qt

Name:           kf5-%{framework}
Version:        5.1.1
Release:        1%{?dist}
Summary:        A Tier 1 KDE Frameworks module wrapping ModemManager DBus API

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            https://projects.kde.org/projects/extragear/libs/libmm-qt

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  ModemManager-devel >= 1.0.0

Requires:       kf5-filesystem

%description
A Qt 5 library for ModemManager

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
Qt 5 libraries and header files for developing applications
that use ModemManager.

%prep
%setup -qn %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast  DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README README.md COPYING.LIB
%{_kf5_libdir}/libKF5ModemManagerQt.so.*

%files devel
%{_kf5_libdir}/libKF5ModemManagerQt.so
%{_kf5_libdir}/cmake/KF5ModemManagerQt
%{_kf5_includedir}/ModemManagerQt
%{_kf5_includedir}/modemmanagerqt_version.h
%{_kf5_archdatadir}/mkspecs/modules/qt_ModemManagerQt.pri

%changelog
* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.93-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.92-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.91-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-3.20140611gitf6c10ff
- Update to latest git snapshot

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-2.20140514gitf6c10ff
- Update to latest git snapshot

* Fri Apr 18 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.90-1.20140418gitd257bb2
- Upgrade libmm-qt to Tier 1 KDE Framework kf5-modemmanagerqt

* Thu Apr 03 2014 Daniel Vrátil <dvratil@redhat.com> - 1:1.0.1-1.20140403gitd257bb2
- Qt 5 fork of libmm-qt
