%global framework akonadi-calendar
%global git_rev   8fce9f

Name:           kf5-%{framework}
Version:        15.08.0
Release:        0.1.git%{git_rev}%{?dist}
Summary:        The Akonadi Calendar Library

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/pim/%{framework}

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
#Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz
Source0:        %{framework}-%{git_rev}.tar.gz

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-kwallet-devel
BuildRequires:  kf5-kcodecs-devel

BuildRequires:  kf5-kmailtransport-devel
BuildRequires:  kf5-kcontacts-devel
BuildRequires:  kf5-kidentitymanagement-devel
BuildRequires:  kf5-kcalendarcore-devel
BuildRequires:  kf5-kcalendarutils-devel

BuildRequires:  kf5-akonadi-devel

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-akonadi-devel
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
%license COPYING
%{_kf5_libdir}/libKF5AkonadiCalendar.so.*

%files devel
%{_kf5_includedir}/akonadicalendar_version.h
%{_kf5_includedir}/AkonadiCalendar
%{_kf5_libdir}/libKF5AkonadiCalendar.so
%{_kf5_libdir}/cmake/KF5AkonadiCalendar
%{_kf5_archdatadir}/mkspecs/modules/qt_AkonadiCalendar.pri


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-0.1.git8fce9f
- Initial snapshot
