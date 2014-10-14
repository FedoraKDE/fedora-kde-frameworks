%define framework kwayland

Name:           kf5-%{framework}
Version:        5.1.0.1
Release:        1%{?dist}
Summary:        KDE Frameworks 5 library that wraps Client and Server Wayland libraries

License:        GPLv2+
URL:            http://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/kwayland-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-cursor-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  wayland-devel

Requires:       kf5-filesystem

%description
%{summary}.

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
%doc COPYING COPYING.LIB README
%{_kf5_libdir}/libKF5WaylandClient.so.*
#%{_kf5_libdir}/libKF5WaylandServer.so.*

%files devel
%{_kf5_includedir}/KWayland
%{_kf5_includedir}/kwayland_version.h
%{_kf5_libdir}/cmake/KF5Wayland
%{_kf5_libdir}/libKF5WaylandClient.so
#%{_kf5_libdir}/libKF5WaylandServer.so


%changelog
* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0
