%define framework kdelibs4support
#%define snapshot 20140206

Name:           kf5-%{framework}
Version:        4.98.0
Release:        2.20140423git52a66644%{?dist}
Summary:        KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4
License:        LGPLv2+
URL:            http://www.kde.org
# git archive --format=tar --prefix=%{framework}-%{version}/ \
#             --remote=git://anongit.kde.org/%{framework}.git master | \
# bzip2 -c > %{name}-%{version}-%{snapshot}git.tar.bz2
#Source0:        %{name}-%{version}-%{snapshot}git.tar.bz2
Source0:        kf5-kdelibs4support-52a66644.tar

Provides:       kf5-kde4support%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kde4support%{?_isa} =< 4.98.0-1

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

BuildRequires:  kf5-attica-devel
BuildRequires:  kf5-kjs-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kwidgetsaddons-devel
BuildRequires:  kf5-kdbusaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kauth-devel
BuildRequires:  kf5-kcodecs-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kitemviews-devel
BuildRequires:  kf5-kiconthemes-devel
BuildRequires:  kf5-kunitconversion-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-sonnet-devel
BuildRequires:  kf5-ktextwidgets-devel
BuildRequires:  kf5-kxmlgui-devel
BuildRequires:  kf5-kbookmarks-devel
BuildRequires:  kf5-kjobwidgets-devel
BuildRequires:  kf5-solid-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-karchive-devel
BuildRequires:  kf5-kdoctools-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-knotifications-devel
BuildRequires:  kf5-kparts-devel
BuildRequires:  kf5-kdesignerplugin-devel
BuildRequires:  kf5-kglobalaccel-devel

Requires:       kf5-filesystem

%description
KDE Frameworks 5 Tier 4 module with porting aid from KDELibs 4


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       kf5-kde4support-devel%{?_isa} = %{version}-%{release}
Obsoletes:      kf5-kde4support-devel%{?_isa} <= 4.98.0-1

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %{framework}-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
# Set absolute BIN_INSTALL_DIR, otherwise CMake will complain about mixed use of
# absolute and relative paths for some reason.
%{cmake_kf5} \
        -DBIN_INSTALL_DIR=/usr/bin \
        ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
%make_install -C %{_target_platform}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING.LIB README.md
%{_kf5_bindir}/kf5-config
%{_kf5_bindir}/kdebugdialog5
%{_kf5_libdir}/libKF5KDELibs4Support.so.*
%{_kf5_libexecdir}/fileshareset
%{_kf5_qtplugindir}/kf5/*.so
%{_kf5_qtplugindir}/designer/*.so
%{_kf5_mandir}/man1/*
%{_kf5_datadir}/kde5/services/*.protocol
%{_kf5_datadir}/kde5/services/*.desktop
%{_kf5_datadir}/kde5/services/qimageioplugins/*.desktop
%{_kf5_datadir}/kde5/servicetypes/*.desktop
%{_kf5_datadir}/kde5/services/kded/networkstatus.desktop
%{_kf5_datadir}/kdoctools5/customization
%{_kf5_datadir}/locale/*
%{_kf5_datadir}/kf5widgets/
%{_kf5_datadir}/kssl/ca-bundle.crt
%{_kf5_sysconfdir}/xdg/colors
%{_kf5_sysconfdir}/xdg/kdebug.areas
%{_kf5_sysconfdir}/xdg/kdebugrc
%{_kf5_sysconfdir}/xdg/ksslcalist
%{_kf5_docdir}/HTML/en/kdebugdialog

%files devel
%{_kf5_libdir}/libKF5KDELibs4Support.so
%{_kf5_libdir}/cmake/KF5KDELibs4Support/
%{_kf5_libdir}/cmake/KF5KDE4Support/
%{_kf5_libdir}/cmake/KDELibs4/
%{_kf5_includedir}/kdelibs4support_version.h
%{_kf5_includedir}/KDELibs4Support/
%{_kf5_datadir}/dbus-1/interfaces/*.xml



%changelog
* Wed Apr 23 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140423git52a66644
- Update to git: 52a66644

* Mon Apr 21 2014 Daniel Vrátil <dvratil@redhat.com> - 4.98.0-2
- Rename to KDELibs4Support, following upstream name change

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git757bc979
- Update to git: 757bc979

* Mon Apr 21 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140421git977151f9
- Update to git: 977151f9

* Fri Apr 18 2014 dvratil <dvratil@redhat.com> - 4.98.0-20140418git1f563691
- Update to git: 1f563691

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
