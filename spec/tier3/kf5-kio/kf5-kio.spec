#%define snapshot 20140205
%define framework kio

Name:           kf5-%{framework}
Version:        5.1.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for filesystem abstraction

License:        GPLv2+ and MIT and BSD
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        http://download.kde.org/stable/frameworks/%{version}/%{framework}-%{version}.tar.xz

BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  zlib-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kcodecs-devel
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
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kwallet-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for filesystem abstraction


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-karchive-devel
Requires:       kf5-kbookmarks-devel
Requires:       kf5-kcodecs-devel
Requires:       kf5-kcompletion-devel
Requires:       kf5-kconfig-devel
Requires:       kf5-kconfigwidgets-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kdbusaddons-devel
Requires:       kf5-kdoctools-devel
Requires:       kf5-ki18n-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kitemviews-devel
Requires:       kf5-kjobwidgets-devel
Requires:       kf5-knotifications-devel
Requires:       kf5-kservice-devel
Requires:       kf5-solid-devel
Requires:       kf5-kwidgetsaddons-devel
Requires:       kf5-kwindowsystem-devel
Requires:       kf5-kxmlgui-devel
Requires:       kf5-kwallet-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    doc
Documentation for %{name}.

# TODO: Split the package

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
%find_lang kio5_qt --with-qt --all-name

%post
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database &> /dev/null || :


%files -f kio5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_libdir}/*.so.*
%{_kf5_bindir}/ktelnetservice5
%{_kf5_bindir}/kcookiejar5
%{_kf5_bindir}/kmailservice5
%config %{_kf5_sysconfdir}/xdg/kshorturifilterrc
%config %{_kf5_sysconfdir}/xdg/accept-languages.codes
%{_kf5_plugindir}/kio/*.so
%{_kf5_plugindir}/urifilters/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_libexecdir}/kio_http_cache_cleaner
%{_kf5_libexecdir}/kioexec
%{_kf5_libexecdir}/kpac_dhcp_helper
%{_kf5_libexecdir}/kioslave
%{_kf5_datadir}/applications/*.desktop
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/kservices5/*
%{_kf5_datadir}/kservicetypes5/*
%{_kf5_datadir}/knotifications5/proxyscout.*
%{_kf5_datadir}/kf5/kcookiejar/domain_info

%files devel
%{_kf5_includedir}/*
%{_kf5_libdir}/*.so
%{_kf5_libdir}/cmake/KF5KIO
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOCore.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOFileWidgets.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KNTLM.pri
%{_kf5_archdatadir}/mkspecs/modules/qt_KIOWidgets.pri

%files doc
%{_kf5_mandir}/man8/*
%{_kf5_datadir}/doc/HTML/en/kioslave5/

%changelog
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

