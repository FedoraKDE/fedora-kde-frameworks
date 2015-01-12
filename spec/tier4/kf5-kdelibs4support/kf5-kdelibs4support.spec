%global framework kdelibs4support

Name:           kf5-%{framework}
Version:        5.6.0
Release:        1%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4
License:        GPLv2+ and LGPLv2+ and BSD
URL:            http://www.kde.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0:        http://download.kde.org/%{stable}/frameworks/%{version}/portingAids/%{framework}-%{version}.tar.xz

BuildRequires:  libX11-devel
BuildRequires:  libSM-devel
BuildRequires:  openssl-devel
BuildRequires:  gettext-devel

BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-designer-plugin-webkit

BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kxmlgui-devel

Requires:       kf5-filesystem
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
This framework provides code and utilities to ease the transition from kdelibs 4
to KDE Frameworks 5. This includes CMake macros and C++ classes whose
functionality has been replaced by code in CMake, Qt and other frameworks.

%package        libs
Summary:        Runtime libraries for %{name}
Requires:       %{name} = %{version}-%{release}
# When the split occured
Conflicts:      %{name} < 5.4.0-1
%description    libs
%{summary}.

%package        doc
Summary:        Documentation and user manuals for %{name}
Requires:       %{name} = %{version}-%{release}
Conflicts:      %{name} < 5.4.0-1
BuildArch:      noarch
%description    doc
%{summary}.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       kf5-kauth-devel
Requires:       kf5-kconfigwidgets-devel
Requires:       kf5-kcoreaddons-devel
Requires:       kf5-kcrash-devel
Requires:       kf5-kdesignerplugin-devel
Requires:       kf5-kdoctools-devel
Requires:       kf5-kemoticons-devel
Requires:       kf5-kguiaddons-devel
Requires:       kf5-kiconthemes-devel
Requires:       kf5-kitemmodels-devel
Requires:       kf5-kinit-devel
Requires:       kf5-knotifications-devel
Requires:       kf5-kparts-devel
Requires:       kf5-ktextwidgets-devel
Requires:       kf5-kunitconversion-devel
Requires:       kf5-kwindowsystem-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
# Set absolute BIN_INSTALL_DIR, otherwise CMake will complain about mixed use of
# absolute and relative paths for some reason
# Remove once fixed upstream
%{cmake_kf5} \
        -DBIN_INSTALL_DIR=/usr/bin \
        ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}
%find_lang kdelibs4support5_qt --with-qt --all-name



%files -f kdelibs4support5_qt.lang
%doc COPYING.LIB README.md
%{_kf5_bindir}/kf5-config
%{_kf5_bindir}/kdebugdialog5
%{_kf5_libexecdir}/fileshareset
%{_kf5_datadir}/kservices5/*.protocol
%{_kf5_datadir}/kservices5/*.desktop
%{_kf5_datadir}/kservices5/qimageioplugins/*.desktop
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/kservices5/kded/networkstatus.desktop
%{_kf5_datadir}/kf5/kdoctools/customization
%{_kf5_datadir}/kf5/locale/*
%{_kf5_datadir}/locale/kf5_all_languages
%{_kf5_datadir}/kf5/widgets/
%{_kf5_datadir}/kf5/kssl/ca-bundle.crt
%config %{_kf5_sysconfdir}/xdg/colors
%config %{_kf5_sysconfdir}/xdg/kdebug.areas
%config %{_kf5_sysconfdir}/xdg/kdebugrc
%config %{_kf5_sysconfdir}/xdg/ksslcalist

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files libs
%{_kf5_libdir}/libKF5KDELibs4Support.so.*
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/designer/*.so
%{_kf5_plugindir}/kio/metainfo.so
%{_kf5_plugindir}/kded/networkstatus.so

%files doc
%{_kf5_docdir}/HTML/*/kdebugdialog5
%{_kf5_mandir}/man1/*
%{_kf5_mandir}/*/man1/*
%exclude %{_kf5_mandir}/man1

%files devel
%{_kf5_libdir}/libKF5KDELibs4Support.so
%{_kf5_libdir}/cmake/KF5KDELibs4Support/
%{_kf5_libdir}/cmake/KF5KDE4Support/
%{_kf5_libdir}/cmake/KDELibs4/
%{_kf5_includedir}/kdelibs4support_version.h
%{_kf5_includedir}/KDELibs4Support/
%{_kf5_datadir}/dbus-1/interfaces/*.xml


%changelog
* Tue Jan 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.6.0-1
- KDE Frameworks 5.6.0

* Sat Dec 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.5.0-1
- KDE Frameworks 5.5.0

* Mon Nov 03 2014 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- KDE Frameworks 5.4.0
- Create -libs subpackage

* Wed Oct 22 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Rebuild against Qt 5.4 (see https://git.reviewboard.kde.org/r/119604 why)

* Fri Oct 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Rebuild

* Tue Oct 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- KDE Frameworks 5.3.0

* Mon Sep 15 2014 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- KDE Frameworks 5.2.0

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- KDE Frameworks 5.1.0

* Mon Jul 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-2
- Fix plugin installation path

* Wed Jul 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- KDE Frameworks 5.0.0

* Mon Jul 07 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-2
- Fixed license
- Fixed Source0 URL
- Fixed installation of config files

* Tue Jun 03 2014 Daniel Vrátil <dvratil@redhat.com> - 4.100.0-1
- KDE Frameworks 4.100.0

* Fri May 16 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-6
- Fix typo

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-4
- Fix -devel Requires

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-3
- -devel Requires kf5-kemoticons-devel

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-2
- Fix typo in Obsoletes

* Mon May 05 2014 Daniel Vrátil <dvratil@redhat.com> - 4.99.0-1
- KDE Frameworks 4.99.0

* Mon Apr 21 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2
- Rename to KDELibs4Support, following upstream name change

* Mon Mar 31 2014 Jan Grulich <jgrulich@redhat.com> 4.98.0-1
- Update to KDE Frameworks 5 Beta 1 (4.98.0)

* Wed Mar 05 2014 Jan Grulich <jgrulich@redhat.com> 4.97.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.97.0)

* Wed Feb 12 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-1
- Update to KDE Frameworks 5 Alpha 1 (4.96.0)

* Fri Feb 07 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.2.20140206git
- Rebuild against kwindowsystem

* Thu Feb 06 2014 Daniel Vrátil <dvratil@redhat.com> 4.96.0-0.1.20140206git
- Update to pre-relase snapshot of 4.96.0

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com> 4.95.0-1
- Update to KDE Frameworks 5 TP1 (4.95.0)

* Thu Jan 09 2014 Daniel Vrátil <dvratil@redhat.com>
- initial version
