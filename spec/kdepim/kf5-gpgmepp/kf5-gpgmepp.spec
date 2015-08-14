%global framework gpgmepp
%global git_rev   00d57c

Name:           kf5-%{framework}
Version:        15.08.0
Release:        0.1.git%{git_rev}%{?dist}
Summary:        The GpgMe++ Library

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
#%license COPYING
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
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-0.1.git00d57c
- Initial snapshot
