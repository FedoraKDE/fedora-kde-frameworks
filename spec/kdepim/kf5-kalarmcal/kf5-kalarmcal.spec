%global framework kalarmcal

Name:           kf5-%{framework}
Version:        15.11.80
Release:        1%{?dist}
Summary:        The KAlarmCal Library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/applications/%{version}/src/%{framework}-%{version}.tar.xz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kdelibs4support-devel >= 5.15

BuildRequires:  kf5-akonadi-devel >= 15.11.80
BuildRequires:  kf5-kcalendarcore-devel >= 15.11.80
BuildRequires:  kf5-kidentitymanagement-devel >= 15.11.80
BuildRequires:  kf5-kholidays-devel >= 15.11.80

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kdelibs4support-devel
Requires:       kf5-akonadi-devel
Requires:       kf5-kidentitymanagement-devel
Requires:       kf5-kholidays-devel
Requires:       kf5-kcalendarcore-devel
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0

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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%license COPYING.LIB
%{_kf5_libdir}/libKF5AlarmCalendar.so.*

%files devel
%{_kf5_includedir}/kalarmcal_version.h
%{_kf5_includedir}/KAlarmCal
%{_kf5_libdir}/libKF5AlarmCalendar.so
%{_kf5_libdir}/cmake/KF5AlarmCalendar
%{_kf5_archdatadir}/mkspecs/modules/qt_KAlarmCal.pri


%changelog
* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
