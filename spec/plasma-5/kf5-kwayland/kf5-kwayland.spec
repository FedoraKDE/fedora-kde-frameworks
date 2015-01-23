%global         framework kwayland

%global         wayland_min_version 1.3

Name:           kf5-%{framework}
Version:        5.2.0
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

BuildRequires:  libwayland-client-devel >= %{wayland_min_version}
BuildRequires:  libwayland-cursor-devel >= %{wayland_min_version}
BuildRequires:  libwayland-server-devel >= %{wayland_min_version}
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  wayland-devel >= %{wayland_min_version}

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
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB
%{_kf5_libdir}/libKF5WaylandClient.so.*
%{_kf5_libdir}/libKF5WaylandServer.so.*

%files devel
%{_kf5_includedir}/KWayland
%{_kf5_includedir}/kwayland_version.h
%{_kf5_libdir}/cmake/KF5Wayland
%{_kf5_libdir}/libKF5WaylandClient.so
%{_kf5_libdir}/libKF5WaylandServer.so


%changelog
* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0
