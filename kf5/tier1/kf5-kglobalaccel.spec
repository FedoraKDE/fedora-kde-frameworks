%define framework kglobalaccel

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 integration module for global shortcuts

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-devel

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  extra-cmake-modules

%description
KDE Framework 5 Tier 1 integration module for global shortcuts


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
%doc COPYING.LIB README.md
%{_kf5_libdir}/libKF5GlobalAccel.so.*

%files devel
%doc
%{_kf5_includedir}/kglobalaccel_version.h
%{_kf5_includedir}/KGlobalAccel/
%{_kf5_libdir}/libKF5GlobalAccel.so
%{_kf5_datadir}/dbus-1/interfaces/*
%{_kf5_libdir}/cmake/KF5GlobalAccel


%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
