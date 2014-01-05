%define snapshot  20140104

Name:           kf5-kconfig
Version:        5.0.0
Release:        0.2.%{snapshot}git
Summary:        KDE Frameworks tier 1 addon with advanced configuration system

License:        GPLv2+
URL:            http://www.kde.org

# git archive --format=tar --prefix=%{name}-%{version}/ \
#             --remote=git://anongit.kde.org/%{name}.git master | \
# gzip -c > %{name}-%{snapshot}.tar.gz
Source0:        %{name}-%{snapshot}.tar.gz

BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel

Requires:       kf5-kconfig-core
Requires:       kf5-kconfig-gui

%description
KDE Frameworks tier 1 addon with advanced configuration system made of two parts:
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

%description    gui
KConfigGui provides a way to hook widgets to the configuration so that they are
automatically initialized from the configuration and automatically propagate
their changes to their respective configuration files.

%prep
%setup -q


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
%doc
%{_kf5_libexecdir}/*
%{_kf5_bindir}/*
%{_kf5_libdir}/libKF5ConfigCore.so.*

%files gui
%doc
%{_kf5_libdir}/libKF5ConfigGui.so.*

%files devel
%doc
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5Config

%changelog
* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
