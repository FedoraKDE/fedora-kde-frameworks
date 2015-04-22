Name:           libksysguard
Version:        5.2.2
Release:        2%{?dist}
Summary:        Library for managing processes running on the system

License:        GPLv2+
URL:            https://projects.kde.org/projects/kde/workspace/libksysguard

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/plasma/%{version}/%{name}-%{version}.tar.xz

BuildRequires:  zlib-devel
BuildRequires:  libXres-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kdelibs4support-devel
BuildRequires:  kf5-plasma-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-knewstuff-devel

Requires:       kf5-filesystem

Obsoletes:      kf5-ksysguard < 5.1.95
Provides:       kf5-ksysguard = %{version}-%{release}

Requires:       libksysguard-common = %{version}-%{release}

%description
KSysGuard library provides API to read and manage processes
running on the system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-ksysguard-devel < 5.1.95
Provides:       kf5-ksysguard-devel = %{version}-%{release}
Conflicts:      kde-workspace-devel < 1:4.11.16-11

%package        common
Summary:        Runtime data files shared by libksysguard and ksysguard-libs
Conflicts:      libksysguard < 5.2.1-2
Conflicts:      ksysguard < 5.2
%description    common
%{summary}.

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{name}-%{version}

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} .. -DINCLUDE_INSTALL_DIR=%{_kf5_includedir}
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang ksysguard_qt5 --with-qt --with-kde --all-name

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f ksysguard_qt5.lang
%doc COPYING.LIB
%{_kf5_libdir}/liblsofui.so.*
%{_kf5_libdir}/libprocessui.so.*
%{_kf5_libdir}/libprocesscore.so.*
%{_kf5_libdir}/libksignalplotter.so.*
%{_kf5_libdir}/libksgrd.so.*
%{_kf5_datadir}/ksysguard

%files common
%{_kf5_libexecdir}/kauth/ksysguardprocesslist_helper
%{_sysconfdir}/dbus-1/system.d/org.kde.ksysguard.processlisthelper.conf
%{_datadir}/dbus-1/system-services/org.kde.ksysguard.processlisthelper.service
%{_datadir}/polkit-1/actions/org.kde.ksysguard.processlisthelper.policy

%files devel
%{_kf5_includedir}/ksysguard
%{_kf5_libdir}/liblsofui.so
%{_kf5_libdir}/libprocessui.so
%{_kf5_libdir}/libprocesscore.so
%{_kf5_libdir}/libksignalplotter.so
%{_kf5_libdir}/libksgrd.so
%{_kf5_libdir}/cmake/KF5SysGuard

%changelog
* Sat Apr 04 2015 Rex Dieter <rdieter@fedoraproject.org> 
- 5.2.2-2
- -common: Conflicts: ksysguard < 5.2 (#1185851)
- -devel: Conflicts: kde-workspace-devel < 1:4.11.16-11

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Wed Feb 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- split shared parts needed by both KF5 and KDE4 versions into -common

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Feb 02 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.0-2
- bump Obsoletes: kf5-ksysguard < 5.1.95

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 21 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.95-3
- Obsolete kf5-ksysguard

* Tue Jan 20 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.95-2
- Rename to libksysguard

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1
- Plasma 5.1.95 Beta

* Mon Jan 05 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.1-2
- Better URL
  Use make install instead of make_install macro

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed Jun 11 2014 Daniel Vrátil <dvratil@redhat.com> - 4.97.0-2.20140611git887e946
- Update to latest git snapshot


* Sat May 17 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-2.20140514git87ae01f
- Fix Source

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-2.20140611gitf7a2bbe
- Update to latest git snapshot

* Fri Apr 25 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1.20140425git1908ec8
- Initial package
