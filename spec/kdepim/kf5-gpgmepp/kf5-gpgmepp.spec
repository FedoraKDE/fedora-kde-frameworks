%global framework gpgmepp

Name:           kf5-%{framework}
Version:        15.08.0
Release:        1%{?dist}
Summary:        C++ wrapper and Qt integreation for GpgMe library

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
BuildRequires:  gpgme-devel
BuildRequires:  boost-devel

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Obsoletes:      kdepimlibs-devel%{?_isa} < 15.08.0
Conflicts:      kdepimlibs-devel%{?_isa} < 15.08.0
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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%{_kf5_libdir}/libKF5Gpgmepp.so.*
%{_kf5_libdir}/libKF5Gpgmepp-pthread.so.*
%{_kf5_libdir}/libKF5QGpgme.so.*

%files devel
%{_kf5_includedir}/gpgmepp_version.h
%{_kf5_includedir}/gpgme++
%{_kf5_includedir}/qgpgme
%{_kf5_libdir}/libKF5Gpgmepp.so
%{_kf5_libdir}/libKF5Gpgmepp-pthread.so
%{_kf5_libdir}/libKF5QGpgme.so
%{_kf5_libdir}/cmake/KF5Gpgmepp
%{_kf5_archdatadir}/mkspecs/modules/qt_QGpgme.pri


%changelog
* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
