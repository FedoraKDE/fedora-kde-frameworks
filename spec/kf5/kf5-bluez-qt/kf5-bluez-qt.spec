%global framework bluez-qt

Name:           kf5-%{framework}
Summary:        A Qt wrapper for Bluez
Version:        5.13.0
Release:        0.1%{?dist}

License:        LGPLv2+
URL:            https://projects.kde.org/projects/frameworks/bluez-qt

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-rpm-macros
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel

# For %%{_udevrulesdir}
BuildRequires:  systemd

Requires:       kf5-filesystem
Requires:       bluez >= 5

%if 0%{?fedora} >= 22
## libbluedevil 5.2.2 was the last release
Obsoletes:      libbluedevil < 5.2.90
%endif

%description
BluezQt is Qt-based library written handle all Bluetooth functionality.

%package        devel
Summary:        Development files for %{name}
%if 0%{?fedora} >= 22
## libbluedevil 5.2.2 was the last release
Obsoletes:      libbluedevil-devel < 5.2.90
%endif
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       qt5-qtbase-devel
%description    devel
Development files for %{name}.


%prep
%setup -q -n %{framework}-%{version}


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. \
  -DUDEV_RULES_INSTALL_DIR:PATH="%{_udevrulesdir}"
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc COPYING.LIB README.md
%{_libdir}/libKF5BluezQt.so.*
%{_kf5_qmldir}/org/kde/bluezqt/
%{_udevrulesdir}/61-kde-bluetooth-rfkill.rules

%files devel
%{_kf5_includedir}/BluezQt/
%{_kf5_includedir}/bluezqt_version.h
%{_kf5_libdir}/libKF5BluezQt.so
%{_kf5_libdir}/cmake/KF5BluezQt/
%{_qt5_archdatadir}/mkspecs/modules/qt_BluezQt.pri


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Thu Jul 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0, -devel Obsoletes too (f22+), update URLs

* Tue Jun 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-2
- Only obsolete libbluedevil on F>=22

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Sat Apr 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-1
- 5.3.0, %%build: explicitly set -DUDEV_RULES_INSTALL_DIR=%%_udevrulesdir

* Sat Apr 25 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.95-3
- Fix libbluedevil Obsoletes (including -devel), .spec cosmetics

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-2
- install %%doc
- Obsoletes: libbluedevil

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95
