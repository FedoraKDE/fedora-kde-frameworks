%global         wayland_min_version 1.3

Name:           kwayland-integration
Version:        5.3.95
Release:        1%{?dist}
Summary:        Provides integration plugins for various KDE Frameworks for Wayland

License:        GPLv2+
URL:            http://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  qt5-qtbase-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules

BuildRequires:  kf5-kidletime-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kwayland-devel

Requires:       kf5-filesystem

%description
%{summary}.


%prep
%setup -q -n %{name}-%{version}

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
%{_kf5_plugindir}/org.kde.kidletime.platforms/KF5IdleTimeKWaylandPlugin.so
%{_kf5_plugindir}/org.kde.kwindowsystem.platforms/KF5WindowSystemKWaylandPlugin.so

%changelog
* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Initial version
