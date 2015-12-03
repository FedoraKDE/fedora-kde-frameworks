%global framework kldap

Name:           kf5-%{framework}
Version:        15.11.80
Release:        1%{?dist}
Summary:        The KLDAP Library

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
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openldap-devel

BuildRequires:  kf5-kcompletion-devel >= 5.15
BuildRequires:  kf5-kwidgetsaddons-devel >= 5.15
BuildRequires:  kf5-ki18n-devel >= 5.15

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       openldap-devel
Requires:       cyrus-sasl-devel
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
%license COPYING.LIB
%{_kf5_libdir}/libKF5Ldap.so.*

%files devel
%{_kf5_includedir}/kldap_version.h
%{_kf5_includedir}/KLDAP
%{_kf5_libdir}/libKF5Ldap.so
%{_kf5_libdir}/cmake/KF5Ldap
%{_kf5_archdatadir}/mkspecs/modules/qt_Ldap.pri


%changelog
* Thu Dec 03 2015 Jan Grulich <jgrulich@redhat.com> - 15.11.80-1
- Update to 15.11.80

* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
