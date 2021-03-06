%global framework kio

Name:           kf5-%{framework}
Version:        5.13.0
Release:        0.1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for filesystem abstraction

License:        GPLv2+ and MIT and BSD
URL:            http://www.kde.org

%global versiondir %(echo %{version} | cut -d. -f1-2)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{versiondir}/%{framework}-%{version}.tar.xz

BuildRequires:  krb5-devel
BuildRequires:  libacl-devel
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  zlib-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kwallet-devel >= %{version}
BuildRequires:  qt5-qtscript-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kwallet-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel

Obsoletes:      kf5-kio-doc < 5.11.0-3
Provides:       kf5-kio-doc = %{version}-%{release}

Requires:       kf5-filesystem
%if ! 0%{?bootstrap}
# (apparently?) requires org.kde.klauncher5 service provided by kf5-kinit -- rex
Requires:       kf5-kinit
%endif

Requires:       %{name}-core%{?_isa} = %{version}-%{release}
Requires:       %{name}-widgets%{?_isa} = %{version}-%{release}
Requires:       %{name}-file-widgets%{?_isa} = %{version}-%{release}
Requires:       %{name}-ntlm%{?_isa} = %{version}-%{release}

%description
KDE Frameworks 5 Tier 3 solution for filesystem abstraction

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kbookmarks-devel
Requires:       kf5-kcompletion-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kitemviews-devel
Requires:       kf5-kjobwidgets-devel
Requires:       kf5-kservice-devel
Requires:       kf5-solid-devel
Requires:       kf5-kxmlgui-devel
Requires:       qt5-qtbase-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        core
Summary:        Core components of the KIO Framework
Requires:       %{name}-core-libs%{?_isa} = %{version}-%{release}
# last version of the main package before the split
Conflicts:      kf5-kio < 5.3.0-2
%description    core
KIOCore library provides core non-GUI components for working with KIO.

%package        core-libs
Summary:        Runtime libraries for KIO Core
Requires:       %{name}-core = %{version}-%{release}
%description    core-libs
%{summary}.

%package        widgets
Summary:        Widgets for KIO Framework
Requires:       %{name}-core%{?_isa} = %{version}-%{release}
# last version of the main package before the split
Conflicts:      kf5-kio < 5.3.0-2
%description    widgets
KIOWidgets contains classes that provide generic job control, progress
reporting, etc.

%package        widgets-libs
Summary:        Runtime libraries for KIO Widgets library
Requires:       %{name}-widgets = %{version}-%{release}
%description    widgets-libs
%{summary}.

%package        file-widgets
Summary:        Widgets for file-handling for KIO Framework
Requires:       %{name}-widgets%{?_isa} = %{version}-%{release}
%description    file-widgets
The KIOFileWidgets library provides the file selection dialog and
its components.

%package        ntlm
Summary:        NTLM support for KIO Framework
# last version of the main package before the split
Conflicts:      kf5-kio < 5.3.0-2
%description    ntlm
KIONTLM provides support for NTLM authentication mechanism in KIO


%prep
%autosetup -n %{framework}-%{version} -p1


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang %{name} --all-name --with-man --with-qt


%files
%license COPYING.LIB
%doc README.md

%posttrans core
/usr/bin/update-desktop-database -q &> /dev/null ||:

%postun core
if [ $1 -eq 0 ] ; then
/usr/bin/update-desktop-database -q &> /dev/null ||:
fi

%files core -f %{name}.lang
%config %{_kf5_sysconfdir}/xdg/accept-languages.codes
%{_kf5_libexecdir}/kio_http_cache_cleaner
%{_kf5_libexecdir}/kpac_dhcp_helper
%{_kf5_libexecdir}/kioexec
%{_kf5_libexecdir}/kioslave
%{_kf5_libexecdir}/kiod5
%{_kf5_bindir}/ktelnetservice5
%{_kf5_bindir}/kcookiejar5
%{_kf5_mandir}/man8/kcookiejar5.8*
%{_kf5_bindir}/kmailservice5
%{_kf5_bindir}/ktrash5
%{_kf5_plugindir}/kio/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_qtplugindir}/kcm_kio.so
%{_kf5_qtplugindir}/kcm_trash.so
%dir %{_kf5_plugindir}/kiod/
%{_kf5_plugindir}/kiod/*.so
%{_kf5_datadir}/kservices5/cache.desktop
%{_kf5_datadir}/kservices5/cookies.desktop
%{_kf5_datadir}/kservices5/netpref.desktop
%{_kf5_datadir}/kservices5/proxy.desktop
%{_kf5_datadir}/kservices5/smb.desktop
%{_kf5_datadir}/kservices5/useragent.desktop
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/http_cache_cleaner.desktop
%dir %{_kf5_datadir}/kservices5/kded/
%{_kf5_datadir}/kservices5/kded/*.desktop
%{_kf5_datadir}/kservices5/kcmtrash.desktop
%{_kf5_datadir}/kservices5/useragentstrings
%{_kf5_datadir}/knotifications5/proxyscout.*
%{_kf5_datadir}/kf5/kcookiejar/domain_info
%{_kf5_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/org.kde.kiod5.service
%{_kf5_docdir}/HTML/en/kioslave5/

%post core-libs -p /sbin/ldconfig
%postun core-libs -p /sbin/ldconfig

%files core-libs
%{_kf5_libdir}/libKF5KIOCore.so.*

%posttrans widgets
/usr/bin/update-desktop-database -q &> /dev/null ||:

%postun widgets
if [ $1 -eq 0 ] ; then
/usr/bin/update-desktop-database -q &> /dev/null ||:
fi

%files widgets
%config %{_kf5_sysconfdir}/xdg/kshorturifilterrc
%{_kf5_qtplugindir}/kcm_webshortcuts.so
%{_kf5_plugindir}/urifilters/*.so
%{_kf5_datadir}/kservices5/fixhosturifilter.desktop
%{_kf5_datadir}/kservices5/kshorturifilter.desktop
%{_kf5_datadir}/kservices5/kuriikwsfilter.desktop
%{_kf5_datadir}/kservices5/kurisearchfilter.desktop
%{_kf5_datadir}/kservices5/localdomainurifilter.desktop
%{_kf5_datadir}/kservices5/webshortcuts.desktop
%{_kf5_datadir}/kservices5/searchproviders
%{_kf5_datadir}/kservicetypes5/*.desktop

%post widgets-libs -p /sbin/ldconfig
%postun widgets-libs -p /sbin/ldconfig

%files widgets-libs
%{_kf5_libdir}/libKF5KIOWidgets.so.*

%post file-widgets -p /sbin/ldconfig
%postun file-widgets -p /sbin/ldconfig

%files file-widgets
%{_kf5_libdir}/libKF5KIOFileWidgets.so.*

%post ntlm -p /sbin/ldconfig
%postun ntlm -p /sbin/ldconfig

%files ntlm
%{_kf5_libdir}/libKF5KIONTLM.so.*

%files devel
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5KIO/
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOFileWidgets.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KNTLM.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOWidgets.pri
%{_datadir}/dbus-1/interfaces/*.xml


%changelog
* Tue Aug 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.13.0-0.1
- KDE Frameworks 5.13

* Fri Jul 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.12.0-1
- 5.12.0

* Thu Jul 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.11.0-3
- .spec cleanup, cleanup Conflicts
- use %%license
- drop -doc subpkg
- Requires: kf5-kinit (kio apparently needs org.kde.klauncher5 service provided by kinit)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Daniel Vrátil <dvratil@redhat.com> - 5.11.0-1
- KDE Frameworks 5.11.0

* Mon May 11 2015 Daniel Vrátil <dvratil@redhat.com> - 5.10.0-1
- KDE Frameworks 5.10.0

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.9.0-3
- Added folders to left panel "Places" disappear (kde#345174)
- optimize scriptlets
- .spec cosmetics

* Thu Apr 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.9.0-2
- BR: krb5-devel libacl-devel

* Tue Apr 07 2015 Daniel Vrátil <dvratil@redhat.com> - 5.9.0-1
- KDE Frameworks 5.9.0

* Fri Apr 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.8.0-2
- -core: own %%{_kf5_datadir}/kservices5/kded/

* Mon Mar 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.8.0-1
- KDE Frameworks 5.8.0

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-2
- Rebuild (GCC 5)

* Mon Feb 16 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.7.0-1
- KDE Frameworks 5.7.0

* Thu Jan 08 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Mon Dec 08 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- KDE Frameworks 5.4.0

* Thu Oct 30 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Fix typo in deps

* Wed Oct 29 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Split into subpackages

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Mon Jul 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix plugin install path

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Sat Jun 28 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- fixed licenses
- added %%config
- added update-desktop-database

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0
- KDE Frameworks 4.99.0

* Wed Apr 02 2014 Daniel Vrátil <dvratil@redhat.com> 4.98.0-2
- Fix conflict of kf5-kio-doc with kdelibs4

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Tue Mar 11 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-2
- remove public dependencies

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Wed Feb 05 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140205git
- Update to pre-relase snapshot of 4.96.0

* Mon Jan 20 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-2
- rebuild against new kf5-filesystem

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Sat Jan  4 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version

