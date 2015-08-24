%global framework kcalendarutils

Name:           kf5-%{framework}
Version:        15.08.0
Release:        1%{?dist}
Summary:        The KCalendarUtils Library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/kcalutils

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/kcalutils-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kcoreaddons-devel >= 5.12
BuildRequires:  kf5-kconfig-devel >= 5.12
BuildRequires:  kf5-ki18n-devel >= 5.12
BuildRequires:  kf5-kdelibs4support-devel >= 5.12
BuildRequires:  kf5-kcodecs-devel >= 5.12

BuildRequires:  kf5-kcalendarcore-devel >= 15.08
BuildRequires:  kf5-kidentitymanagement-devel >= 15.08

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-kcalendarcore-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n kcalutils-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_kf5_libdir}/libKF5CalendarUtils.so.*

%files devel
%{_kf5_includedir}/kcalutils_version.h
%{_kf5_includedir}/KCalUtils
%{_kf5_libdir}/libKF5CalendarUtils.so
%{_kf5_libdir}/cmake/KF5CalendarUtils
%{_kf5_archdatadir}/mkspecs/modules/qt_KCalUtils.pri


%changelog
* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
