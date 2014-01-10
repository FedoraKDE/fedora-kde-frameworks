%define framework kconfig

Name:           kf5-%{framework}
Version:        4.95.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 1 addon with advanced configuration system

License:        GPLv2+
URL:            http://www.kde.org
Source0:        http://download.kde.org/unstable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-kconfig-core%{?_isa} = %{version}-%{release}
Requires:       kf5-kconfig-gui%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 1 addon with advanced configuration system made of two parts:
KConfigCore and KConfigGui.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        core
Summary:        Non-GUI part of KConfig framework

%description    core
KConfigCore provides access to the configuration files themselves. It features:

- centralized definition: define your configuration in an XML file and use
`kconfig_compiler` to generate classes to read and write configuration entries.

- lock-down (kiosk) support.

%package        gui
Summary:        GUI part of KConfig framework
Requires:       kf5-kconfig-core%{?_isa} = %{version}-%{release}

%description    gui
KConfigGui provides a way to hook widgets to the configuration so that they are
automatically initialized from the configuration and automatically propagate
their changes to their respective configuration files.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} DESTDIR=%{buildroot} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB DESIGN README.md TODO

%files core
%{_kf5_libexecdir}/kconf_update
%{_kf5_bindir}/kconfig_compiler
%{_kf5_libdir}/libKF5ConfigCore.so.*

%files gui
%{_kf5_libdir}/libKF5ConfigGui.so.*

%files devel
%{_kf5_includedir}/kconfig_version.h
%{_kf5_includedir}/KConfigCore
%{_kf5_includedir}/KConfigGui
%{_kf5_libdir}/libKF5ConfigCore.so
%{_kf5_libdir}/libKF5ConfigGui.so
%{_kf5_libdir}/cmake/KF5Config

%changelog
* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
