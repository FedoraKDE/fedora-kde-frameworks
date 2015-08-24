%global framework kpimtextedit

Name:           kf5-%{framework}
Version:        15.08.0
Release:        1%{?dist}
Summary:        The KPimTextEdit Library

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

BuildRequires:  kf5-kcoreaddons-devel >= 5.12
BuildRequires:  kf5-kemoticons-devel >= 5.12
BuildRequires:  kf5-sonnet-devel >= 5.12
BuildRequires:  kf5-ktextwidgets-devel >= 5.12
BuildRequires:  kf5-kwidgetsaddons-devel >= 5.12
BuildRequires:  kf5-kio-devel >= 5.12
BuildRequires:  kf5-kcodecs-devel >= 5.12
BuildRequires:  kf5-kdelibs4support-devel >= 5.12

Obsoletes:      kdepimlibs%{?_isa} < 15.08.0
Conflicts:      kdepimlibs%{?_isa} < 15.08.0

%description
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-ktextwidgets-devel
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
%{_kf5_libdir}/libKF5PimTextEdit.so.*

%files devel
%{_kf5_includedir}/kpimtextedit_version.h
%{_kf5_includedir}/KPIMTextEdit
%{_kf5_libdir}/libKF5PimTextEdit.so
%{_kf5_libdir}/cmake/KF5PimTextEdit
%{_kf5_archdatadir}/mkspecs/modules/qt_KPIMTextEdit.pri


%changelog
* Mon Aug 24 2015 Daniel Vrátil <dvratil@redhat.com> - 15.08.0-1
- Initial version
