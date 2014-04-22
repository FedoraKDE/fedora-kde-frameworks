#%define snapshot 20140205
%define framework kio

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140422gitb03063a8%{?dist}
Summary:        KDE Frameworks 5 Tier 3 solution for filesystem abstraction

License:        GPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kio-b03063a8.tar

BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel
BuildRequires:  zlib-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtscript-devel

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kwallet-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 3 solution for filesystem abstraction


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

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

# Rename kioslave documentation to kioslave5 to avoid conflict with kdelibs4
mv $RPM_BUILD_ROOT/%{_kf5_datadir}/doc/HTML/en/kioslave{,5}
mv $RPM_BUILD_ROOT/%{_kf5_datadir}/doc/HTML/en/khelpcenter{,5}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_libdir}/*.so.*
%{_kf5_bindir}/*
%{_kf5_sysconfdir}/xdg/accept-languages.codes
%{_kf5_qtplugindir}/kf5/*.so
%{_kf5_libexecdir}/*
%{_kf5_datadir}/applications/*.desktop
%{_kf5_datadir}/dbus-1/interfaces/*.xml
%{_kf5_datadir}/kconf_update/*
%{_kf5_datadir}/kde5/services/*
%{_kf5_datadir}/kde5/servicetypes/*
%{_kf5_datadir}/proxyscout/
%{_kf5_datadir}/khtml/domain_info

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
%{_kf5_datadir}/doc/HTML/en/khelpcenter5/documentationnotfound

%changelog
* Tue Apr 22 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140422gitb03063a8
- Update to git: b03063a8

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418gitbdc2d142
- Update to git: bdc2d142

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

